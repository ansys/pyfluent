# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
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

"""Automatic repair of recoverable Fluent errors.

When a set fails with a *recoverable* classification, the resolver introspects
the live target (``is_active`` / ``is_read_only`` / ``allowed_values`` / ``min``
/ ``max``) plus static knowledge of the error category to propose a :class:`Fix`:

* **inactive target** -> enable the governing model (a ``pre_mutation``), retry;
* **out of range** -> clamp the value to the live ``[min, max]`` bounds;
* **wrong value** -> snap to the nearest live ``allowed_values`` entry;
* **wrong type** -> coerce the value to the expected scalar type when safe.

It never guesses blindly: if no safe fix can be derived it returns ``None`` and
the caller raises :class:`UnrecoverableStepError`.
"""

from __future__ import annotations

import difflib

from ansys.fluent.core.resilient import _compat
from ansys.fluent.core.resilient.types import Classification, ErrorCategory, Fix


def _call_safe(obj, attr):
    """Call a zero-arg introspection method, returning ``None`` on any failure."""
    fn = getattr(obj, attr, None)
    if not callable(fn):
        return None
    try:
        return fn()
    except Exception:  # noqa: BLE001
        return None


#: Candidate governing models the resolver may toggle to activate an inactive
#: target, in priority order. Each entry is the dotted path (relative to the
#: settings root) of a boolean ``enabled`` flag that turns a model on. These are
#: *candidates only*: the resolver verifies, by live introspection, that enabling
#: one actually makes the target active before keeping the change.
_CANDIDATE_MODEL_FLAGS: tuple[str, ...] = (
    "setup.models.energy.enabled",
    "setup.models.viscous.enabled",
    "setup.models.radiation.enabled",
    "setup.models.species.enabled",
    "setup.models.multiphase.enabled",
    "setup.models.discrete_phase.enabled",
)


def _is_active(obj) -> bool | None:
    """Return the object's ``is_active()`` value, or ``None`` if indeterminable."""
    fn = getattr(obj, "is_active", None)
    if not callable(fn):
        return None
    try:
        return bool(fn())
    except Exception:  # noqa: BLE001
        return None


class RecoverableErrorResolver:
    """Propose and apply bounded automatic repairs for recoverable errors."""

    def __init__(self, session, *, max_attempts: int = 3):
        self.session = session
        self.max_attempts = max_attempts

    # -- proposing a fix --------------------------------------------------

    def propose(self, path: str, value, cls: Classification) -> Fix | None:
        """Propose a :class:`Fix` for a recoverable error, or ``None``."""
        try:
            obj = _compat.resolve_any(self.session, path)
        except Exception:  # noqa: BLE001
            obj = None

        if cls.category is ErrorCategory.INACTIVE_TARGET:
            return self._fix_inactive(path, obj)
        if cls.category is ErrorCategory.OUT_OF_RANGE:
            return self._fix_range(obj, value)
        if cls.category is ErrorCategory.WRONG_VALUE:
            return self._fix_value(obj, value)
        if cls.category is ErrorCategory.WRONG_TYPE:
            return self._fix_type(obj, value)
        return None

    def propose_for_object(self, obj, value, cls: Classification) -> Fix | None:
        """Propose a :class:`Fix` from a live object directly (no path resolution).

        Used by the client-side ``__setattr__`` recovery path, which already holds
        the target object. Only the value-repair categories (range / allowed value
        / type) apply here; inactive targets are handled on the access path.
        """
        if cls.category is ErrorCategory.OUT_OF_RANGE:
            return self._fix_range(obj, value)
        if cls.category is ErrorCategory.WRONG_VALUE:
            return self._fix_value(obj, value)
        if cls.category is ErrorCategory.WRONG_TYPE:
            return self._fix_type(obj, value)
        return None

    def _fix_inactive(self, path: str, obj) -> Fix | None:
        """Discover, by live introspection, which model activates an inactive target.

        Rather than guessing a governing model from the path, this probes each
        candidate model flag that is currently *off*: it tentatively enables the
        flag, re-checks whether the target has become active, and -- if so --
        proposes a fix that keeps that flag enabled. Flags that do not help are
        reverted, so the session is left unchanged except for the one(s) that
        genuinely activate the target. This handles cases the path cannot express,
        e.g. a thermal boundary condition that is inactive only because the energy
        model is off.
        """
        # The failing leaf may itself be unreachable while inactive (attribute
        # access raises), so probe the nearest resolvable ancestor instead.
        probe = obj if obj is not None else self._resolve_active_probe(path)
        if probe is None:
            return None
        enabled_flags = self._discover_activation(
            probe, recheck=lambda: self._resolve_active_probe(path) or probe
        )
        if not enabled_flags:
            return None
        names = ", ".join(p for p, _ in enabled_flags)
        return Fix(
            kind="activate_model",
            description=(
                f"Enable governing model(s) {names} (discovered live) then retry."
            ),
            pre_mutations=enabled_flags,
        )

    def activate_object(self, obj) -> list[str]:
        """Attempt to activate an inactive live object by discovering its model.

        Probes candidate model flags and keeps the one that makes ``obj`` active,
        reverting the rest. Returns the list of flag paths that were enabled (empty
        if none activated the object). Used by the transparent attribute-access
        patch, which already holds the inactive object.
        """
        enabled = self._discover_activation(obj, recheck=lambda: obj)
        return [p for p, _ in enabled]

    def _discover_activation(self, probe, recheck):
        """Shared discovery: toggle candidate flags until ``probe`` becomes active.

        ``recheck`` returns the (possibly re-resolved) object to test for activeness
        after each candidate flag is enabled. Returns the list of
        ``(flag_path, True)`` pairs that were kept enabled.
        """
        if _is_active(probe) is True:
            return []
        enabled_flags: list[tuple[str, object]] = []
        for flag_path in _CANDIDATE_MODEL_FLAGS:
            flag = self._resolve_target(flag_path)
            if flag is None:
                continue
            current = _call_safe(flag, "get_state")
            if current is True:
                continue  # already on; not the cause
            if not self._try_enable(flag):
                continue
            # Re-resolve the target: enabling a model can change tree activeness.
            fresh = recheck()
            if _is_active(fresh) is True:
                enabled_flags.append((flag_path, True))
                break
            # Did not help: revert it so we do not change unrelated state.
            self._try_set(flag, current if current is not None else False)
        return enabled_flags

    def _resolve_active_probe(self, path: str):
        """Resolve the deepest object on ``path`` that can be reached and probed.

        Walks from the leaf up: an inactive leaf often raises on attribute access,
        but one of its ancestors is resolvable and exposes ``is_active()``.
        """
        # Try the full path first, then progressively shorter dotted prefixes.
        candidates = [path]
        dotted = path.replace("/", ".")
        parts = dotted.split(".")
        for cut in range(len(parts) - 1, 0, -1):
            candidates.append(".".join(parts[:cut]))
        for candidate in candidates:
            obj = self._resolve_target(candidate)
            if obj is not None and getattr(obj, "is_active", None) is not None:
                return obj
        return None

    def _resolve_target(self, path: str):
        try:
            return _compat.resolve_any(self.session, path)
        except Exception:  # noqa: BLE001
            return None

    @staticmethod
    def _try_enable(flag) -> bool:
        return RecoverableErrorResolver._try_set(flag, True)

    @staticmethod
    def _try_set(obj, value) -> bool:
        setter = getattr(obj, "set_state", None)
        if not callable(setter):
            return False
        try:
            setter(value)
            return True
        except Exception:  # noqa: BLE001
            return False

    @staticmethod
    def _fix_range(obj, value) -> Fix | None:
        if (
            obj is None
            or not isinstance(value, (int, float))
            or isinstance(value, bool)
        ):
            return None
        low = _call_safe(obj, "min")
        high = _call_safe(obj, "max")
        clamped = value
        if low is not None and value < low:
            clamped = low
        if high is not None and value > high:
            clamped = high
        if clamped == value:
            return None
        return Fix(
            kind="clamp",
            description=f"Clamp {value!r} to live bounds -> {clamped!r}.",
            new_value=clamped,
        )

    @staticmethod
    def _fix_value(obj, value) -> Fix | None:
        if obj is None or not isinstance(value, str):
            return None
        allowed = _call_safe(obj, "allowed_values")
        if not allowed or not isinstance(allowed, (list, tuple)):
            return None
        matches = difflib.get_close_matches(value, list(allowed), n=1, cutoff=0.4)
        if not matches:
            return None
        return Fix(
            kind="nearest_allowed",
            description=(f"{value!r} is not allowed; snap to nearest {matches[0]!r}."),
            new_value=matches[0],
        )

    @staticmethod
    def _fix_type(obj, value) -> Fix | None:
        # Only attempt the safe numeric-string widening cases.
        if isinstance(value, str):
            text = value.strip()
            for caster in (int, float):
                try:
                    coerced = caster(text)
                except (TypeError, ValueError):
                    continue
                return Fix(
                    kind="coerce_type",
                    description=f"Coerce {value!r} to {coerced!r}.",
                    new_value=coerced,
                )
        return None

    # -- applying a fix and retrying -------------------------------------

    def resolve_and_retry(self, path: str, value, applier, cls: Classification):
        """Bounded fix-and-retry loop driven by ``applier`` (a SafeApplier).

        Returns the :class:`StepOutcome` of the first successful retry, or raises
        :class:`UnrecoverableStepError` if no fix works within ``max_attempts``.
        If a retry hits a *fatal* error the exception propagates so the caller
        can fail over.

        Raises
        ------
        Exception
            Re-raises a catastrophic (fatal) error so the caller can fail over.
        UnrecoverableStepError
            If no safe fix can be derived or the retry budget is exhausted.
        """
        # Imported lazily to avoid a circular import with apply.py.
        from ansys.fluent.core.resilient.exceptions import UnrecoverableStepError

        current_value = value
        current_cls = cls
        fixes: list[str] = []
        last_error: str | None = current_cls.message

        for attempt in range(1, self.max_attempts + 1):
            fix = self.propose(path, current_value, current_cls)
            if fix is None:
                break
            fixes.append(fix.kind)
            for pre_path, pre_value in fix.pre_mutations:
                try:
                    applier.set(pre_path, pre_value, _recover=False)
                except Exception as err:  # noqa: BLE001
                    last_error = f"pre-mutation {pre_path!r} failed: {err}"
                    break
            if fix.new_value is not None:
                current_value = fix.new_value
            try:
                outcome = applier.set(path, current_value, _recover=False)
            except Exception as err:  # noqa: BLE001
                # Re-classify: a fatal error must propagate to trigger failover.
                retry_cls = applier.classifier.classify(err, self.session)
                if retry_cls.catastrophic:
                    raise
                current_cls = retry_cls
                last_error = str(err)
                continue
            outcome.attempts = attempt + 1
            outcome.fixes_applied = fixes
            return outcome

        raise UnrecoverableStepError(
            f"Could not resolve error at {path!r} after {len(fixes)} fix "
            f"attempt(s): {last_error}"
        )
