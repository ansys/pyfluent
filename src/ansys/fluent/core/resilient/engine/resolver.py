# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Propose bounded repairs for recoverable errors by live introspection.

* out of range -> clamp to the live ``[min, max]``;
* not an allowed value -> snap to the closest live ``allowed_values`` entry;
* wrong type -> convert a numeric string to a number;
* inactive target -> enable the governing model that activates it (only when
  model activation is allowed). The candidates are the ones configured in
  ``ResilientConfig.activation_candidates``, then the product's built-in ones.
  A candidate is kept only if it activates the target.

The resolver never guesses: if live introspection does not yield a safe repair,
it proposes nothing and the caller re-raises the original error.
"""

from __future__ import annotations

import difflib
from typing import Any, Callable

from . import paths
from .adapter import ResilientAdapter
from .types import ActivationCandidate, Classification, ErrorCategory, Fix

#: Minimum similarity for snapping a string to an allowed value.
_SNAP_CUTOFF = 0.6


def _call(obj: Any, name: str) -> Any:
    """Call a zero-argument introspection method; return ``None`` on failure."""
    try:
        method = getattr(obj, name, None)
        return method() if callable(method) else None
    except Exception:  # noqa: BLE001
        return None


def is_active(obj: Any) -> bool | None:
    """Return ``obj.is_active()``, or ``None`` if it cannot be determined."""
    value = _call(obj, "is_active")
    return None if value is None else bool(value)


class RecoverableErrorResolver:
    """Propose repairs for recoverable errors on one session."""

    def __init__(
        self,
        adapter: ResilientAdapter,
        session: Any,
        *,
        allow_model_activation: bool = False,
        extra_candidates: tuple[ActivationCandidate, ...] = (),
    ):
        self._adapter = adapter
        self.session = session
        self.allow_model_activation = allow_model_activation
        self.extra_candidates = tuple(extra_candidates)

    # -- helpers -------------------------------------------------------------

    def resolve(self, path: str) -> Any:
        """Resolve a dotted or server path on the current session.

        Raises
        ------
        PathResolutionError
            If the path cannot be resolved.
        """
        return paths.resolve_any(
            self._adapter.settings_root(self.session),
            path,
            prefixes=self._adapter.path_prefixes,
            name_attr=self._adapter.server_name_attr,
        )

    def _try_resolve(self, path: str) -> Any:
        try:
            return self.resolve(path)
        except Exception:  # noqa: BLE001
            return None

    # -- proposing repairs ---------------------------------------------------

    def propose(self, path: str, value: Any, cls: Classification) -> Fix | None:
        """Propose a repair for a failed write of ``value`` to ``path``."""
        target = self._try_resolve(path)
        # A write to an inactive target fails whatever the value, and products
        # report it with varying messages, so check activity first.
        if cls.category is ErrorCategory.INACTIVE_TARGET or (
            target is not None and is_active(target) is False
        ):
            return self._fix_inactive(path, target)
        if cls.category is ErrorCategory.OUT_OF_RANGE:
            return self.fix_range(target, value)
        if cls.category is ErrorCategory.WRONG_VALUE:
            return self.fix_allowed_value(target, value)
        if cls.category is ErrorCategory.WRONG_TYPE:
            return self.fix_type(value)
        return None

    @staticmethod
    def fix_range(target: Any, value: Any) -> Fix | None:
        """Clamp a numeric value to the live bounds of ``target``."""
        if target is None or isinstance(value, bool):
            return None
        if not isinstance(value, (int, float)):
            return None
        low, high = _call(target, "min"), _call(target, "max")
        clamped = value
        if isinstance(low, (int, float)) and value < low:
            clamped = low
        if isinstance(high, (int, float)) and value > high:
            clamped = high
        if clamped == value:
            return None
        return Fix(
            kind="clamp",
            description=f"clamped {value!r} to the allowed range -> {clamped!r}",
            new_value=clamped,
        )

    @staticmethod
    def fix_allowed_value(target: Any, value: Any) -> Fix | None:
        """Snap a string to the closest live allowed value of ``target``."""
        if target is None or not isinstance(value, str):
            return None
        allowed = _call(target, "allowed_values")
        if not isinstance(allowed, (list, tuple)) or not allowed:
            return None
        if value in allowed:
            return None
        candidates = [str(item) for item in allowed]
        matches = difflib.get_close_matches(value, candidates, n=1, cutoff=_SNAP_CUTOFF)
        if not matches:
            return None
        return Fix(
            kind="nearest_allowed",
            description=f"replaced {value!r} with the closest allowed value "
            f"{matches[0]!r}",
            new_value=matches[0],
        )

    @staticmethod
    def fix_type(value: Any) -> Fix | None:
        """Convert a numeric string to a number."""
        if not isinstance(value, str):
            return None
        text = value.strip()
        for caster in (int, float):
            try:
                converted = caster(text)
            except ValueError:
                continue
            return Fix(
                kind="coerce_type",
                description=f"converted {value!r} to {converted!r}",
                new_value=converted,
            )
        return None

    # -- inactive targets ------------------------------------------------------

    def _fix_inactive(self, path: str, target: Any) -> Fix | None:
        if not self.allow_model_activation:
            return None
        if target is not None:
            activated = self.activate(target)
        else:
            activated = self._discover(
                probe=lambda: self._try_resolve(path), initially_resolvable=False
            )
        if not activated:
            return None
        names = ", ".join(f"{c.path} = {c.value!r}" for c in activated)
        return Fix(
            kind="activate_model",
            description=f"enabled {names}",
            activations=tuple(activated),
        )

    def activate(self, target: Any) -> list[ActivationCandidate]:
        """Activate an inactive settings object by enabling its governing model.

        Each configured candidate, then each built-in candidate of the adapter,
        that is not already in its activating state is applied in turn. A candidate is kept only if the
        target becomes active; otherwise it is reverted. Returns the candidates
        that were kept (empty if model activation is not allowed or nothing
        activated the target).
        """
        if not self.allow_model_activation:
            return []
        return self._discover(probe=lambda: target, initially_resolvable=True)

    def _discover(
        self, probe: Callable[[], Any], *, initially_resolvable: bool
    ) -> list[ActivationCandidate]:
        if initially_resolvable and is_active(probe()) is True:
            return []
        candidates = (
            *self.extra_candidates,
            *self._adapter.activation_candidates(self.session),
        )
        for candidate in candidates:
            setting = self._try_resolve(candidate.path)
            if setting is None:
                continue
            current = _call(setting, "get_state")
            if current is None or current == candidate.value:
                # Unreadable (cannot be reverted safely) or already applied.
                continue
            if not self._try_set(setting, candidate.value):
                continue
            if is_active(probe()) is True:
                return [candidate]
            self._try_set(setting, current)
        return []

    @staticmethod
    def _try_set(setting: Any, value: Any) -> bool:
        try:
            setting.set_state(value)
            return True
        except Exception:  # noqa: BLE001
            return False
