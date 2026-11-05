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

"""The product seam for the resilient execution runtime.

The resilient engine (journal, checkpoint manager, controller, interceptor,
resolver, classifier, health monitor, pool) is **product-agnostic**. Everything
that differs between Ansys products -- how to reach the fatal-error state, which
typed exceptions a product raises, how to launch a session, how to roll a solver
state back, what the governing-model paths are -- is isolated behind the single
:class:`ResilientAdapter` interface defined here.

To bring resilient mode to a new product (e.g. CFX), implement a small subclass
of :class:`ResilientAdapter`; the whole engine then works unchanged. A
:class:`DefaultAdapter` is provided that covers the common case (a session with a
``_<product>_connection._error_state`` object and a ``settings`` tree), so most
products only need to override a handful of methods.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass
class ErrorClasses:
    """Typed exception classes a product raises, used by the classifier.

    Any member may be ``None`` when the product does not define it; the classifier
    falls back to text heuristics in that case.
    """

    inactive: type | None = None
    read_only: type | None = None
    disallowed: type | None = None
    invalid_arg: type | None = None


class ResilientAdapter:
    """Product-specific seam for the resilient runtime.

    The base implementation provides sensible, duck-typed defaults that work for
    any product whose sessions expose a ``settings`` tree and a connection object
    carrying an ``_error_state``. Override only what differs.
    """

    #: Human-readable product name (for messages / logs).
    product_name: str = "generic"

    #: Dotted-path prefixes a user may prepend; stripped before walking the tree.
    path_prefixes: tuple[str, ...] = ("settings.",)

    #: Attribute names on the connection object to try for the error state.
    _connection_attrs: tuple[str, ...] = (
        "_fluent_connection",
        "_cfx_connection",
        "_connection",
    )

    # -- settings tree / service -----------------------------------------

    def settings_root(self, session):
        """Return the settings root for a session (``session.settings`` or self)."""
        settings = getattr(session, "settings", None)
        return settings if settings is not None else session

    def settings_service(self, session):
        """Return the live settings service (the ``set_var`` / ``execute_cmd`` object)."""
        return getattr(session, "_settings_service", None)

    def set_settings_service(self, session, service) -> None:
        """Install a (wrapped) settings service on the session."""
        session._settings_service = service

    def invalidate_settings_cache(self, session) -> None:
        """Drop any cached settings root so it rebinds to a swapped service."""
        if getattr(session, "_settings", None) is not None:
            session._settings = None

    def inner_service(self, service):
        """Unwrap a possibly-wrapped service to the underlying product service."""
        return getattr(service, "inner", service)

    # -- fatal / health signals ------------------------------------------

    def error_state(self, session):
        """Return the session's error-state object, or ``None``."""
        for attr in self._connection_attrs:
            connection = getattr(session, attr, None)
            if connection is not None:
                state = getattr(connection, "_error_state", None)
                if state is not None:
                    return state
        return None

    def is_fatal(self, session) -> bool:
        """Whether the server is in a fatal error state (authoritative)."""
        state = self.error_state(session)
        return bool(state is not None and getattr(state, "name", "") == "fatal")

    def fatal_details(self, session) -> str | None:
        """Return the fatal-error details string, if any."""
        state = self.error_state(session)
        if state is None:
            return None
        return getattr(state, "details", None) or None

    def is_server_healthy(self, session) -> bool:
        """Best-effort health probe that never raises."""
        for attr in ("_is_server_healthy", "is_active"):
            probe = getattr(session, attr, None)
            if callable(probe):
                try:
                    return bool(probe())
                except Exception:  # noqa: BLE001
                    return False
        return True

    def fatal_event(self):
        """Return the product's fatal-error event object, or ``None``.

        Used to subscribe for push-based fatal detection. Return ``None`` to rely
        only on the polling backstop.
        """
        return None

    # -- typed error classes ---------------------------------------------

    def error_classes(self) -> ErrorClasses:
        """Return the typed exception classes the product raises."""
        return ErrorClasses()

    # -- launch / pool ---------------------------------------------------

    def launch(self, **kwargs):
        """Launch a fresh product session (for warm-pool standbys).

        The default raises; a product that supports failover must override this.
        """
        raise NotImplementedError(
            f"{self.product_name} adapter does not implement launch(); "
            "warm-pool failover is unavailable."
        )

    def exit_session(self, session) -> None:
        """Tear a session down (best-effort)."""
        exit_fn = getattr(session, "exit", None)
        if callable(exit_fn):
            try:
                exit_fn()
            except Exception:  # noqa: BLE001  # nosec B110
                pass

    # -- irreversible commands / checkpoint tier -------------------------

    #: Command leaf names that are irreversible and warrant a checkpoint before
    #: they run. Products override with their own solver/IO command names.
    irreversible_leaves: frozenset[str] = frozenset()

    def is_irreversible(self, path: str) -> bool:
        """Whether a command path refers to an irreversible operation."""
        leaf = path.strip().rstrip(")").split("(")[0].split(".")[-1]
        return leaf in self.irreversible_leaves

    #: How the checkpoint file tier behaves for this product:
    #:   "file"   -> adapter writes/reads a case/data file (Fluent);
    #:   "native" -> adapter uses a server-side undo (CFX file.undo());
    #:   "none"   -> no file tier (settings-journal only).
    checkpoint_kind: str = "file"

    def write_checkpoint(self, session, name: str):
        """Capture a product-native checkpoint; return an opaque reference.

        Only called when ``checkpoint_kind == "file"``. ``native`` products need
        not implement this (they roll back via :meth:`restore_native`).
        """
        raise NotImplementedError

    def restore_checkpoint(self, session, ref) -> None:
        """Reload a checkpoint written by :meth:`write_checkpoint`."""
        raise NotImplementedError

    def restore_native(self, session, steps: int = 1) -> None:
        """Server-side undo of the last ``steps`` operations (``checkpoint_kind``
        == ``"native"``), e.g. CFX ``file.undo()``.
        """
        raise NotImplementedError

    # -- recovery knowledge (optional product physics) -------------------

    def governing_model_flags(self) -> tuple[str, ...]:
        """Candidate governing-model boolean paths to toggle for an inactive
        target. Empty by default (inactive-target activation then degrades to a
        clear error). Fluent supplies energy/viscous/... paths.
        """
        return ()

    # -- inactive-navigation patch (optional) ----------------------------

    def install_inactive_patch(
        self, register_session, unregister_session, controller_for
    ) -> Callable[[], None] | None:
        """Install a product-specific guard for client-side inactive-target
        navigation errors (e.g. wrapping ``Group.__getattribute__``).

        Return a callable that unregisters this session, or ``None`` if the
        product does not raise inactive errors during attribute access.
        """
        return None


# A ready-to-use default for products matching the common shape.
DEFAULT_ADAPTER = ResilientAdapter()


def adapter_for(session) -> ResilientAdapter:
    """Return the resilient adapter governing a session.

    The adapter is attached to a resilient session as ``session._resilient_adapter``
    (done by :func:`enable_resilient_mode`). This is **per-session**, so a single
    Python process can drive multiple products (e.g. Fluent and CFX) concurrently,
    each with its own adapter. Falls back to the generic default.
    """
    return getattr(session, "_resilient_adapter", None) or DEFAULT_ADAPTER
