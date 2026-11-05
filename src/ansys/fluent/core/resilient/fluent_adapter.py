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

"""The Fluent product adapter for the resilient runtime.

This concrete :class:`ResilientAdapter` captures every Fluent-specific coupling:
the ``_fluent_connection._error_state`` fatal signal, the typed settings
exceptions, the ``FATAL_ERROR`` solver event, ``launch_fluent`` for warm-pool
standbys, the case/data file-checkpoint tier, the solver governing-model paths for
inactive-target activation, and the ``Group.__getattribute__`` navigation guard.

A CFX (or any other product) adapter subclasses :class:`ResilientAdapter` and
supplies its own equivalents; the engine is otherwise identical.
"""

from __future__ import annotations

from ansys.fluent.core.resilient.adapter import ErrorClasses, ResilientAdapter


class FluentAdapter(ResilientAdapter):
    """Resilient-mode adapter for Ansys Fluent solver sessions."""

    product_name = "fluent"
    path_prefixes = ("solver.settings.", "settings.", "solver.")
    checkpoint_kind = "file"
    irreversible_leaves = frozenset(
        {
            "iterate",
            "calculate",
            "dual_time_iterate",
            "read_case",
            "read_case_data",
            "read_data",
            "read",
        }
    )

    # -- fatal signal / health -------------------------------------------

    def error_state(self, session):
        """Reach ``session._fluent_connection._error_state`` (guarded)."""
        connection = getattr(session, "_fluent_connection", None)
        if connection is None:
            return None
        return getattr(connection, "_error_state", None)

    def fatal_event(self):
        """Return ``SolverEvent.FATAL_ERROR`` for push-based fatal detection."""
        try:
            from ansys.fluent.core.services.streaming_services.events_streaming import (  # noqa: E501
                SolverEvent,
            )

            return SolverEvent.FATAL_ERROR
        except Exception:  # noqa: BLE001
            return None

    # -- typed error classes ---------------------------------------------

    def error_classes(self) -> ErrorClasses:
        """Return Fluent's typed settings/diagnostic exception classes."""
        inactive = read_only = disallowed = invalid_arg = None
        try:
            from ansys.fluent.core.solver.flobject import (
                InactiveObjectError,
                ReadOnlyActionError,
            )

            inactive, read_only = InactiveObjectError, ReadOnlyActionError
        except Exception:  # noqa: BLE001  # nosec B110
            pass
        try:
            from ansys.fluent.core.diagnostics.exceptions import (
                DisallowedValuesError,
                InvalidArgument,
            )

            disallowed, invalid_arg = DisallowedValuesError, InvalidArgument
        except Exception:  # noqa: BLE001  # nosec B110
            pass
        return ErrorClasses(
            inactive=inactive,
            read_only=read_only,
            disallowed=disallowed,
            invalid_arg=invalid_arg,
        )

    # -- launch / pool ---------------------------------------------------

    def launch(self, **kwargs):
        """Launch a fresh Fluent session via ``launch_fluent``."""
        import ansys.fluent.core as pyfluent

        return pyfluent.launch_fluent(**kwargs)

    # -- file-checkpoint tier (delegated to the generic store) -----------

    def write_file_checkpoint(self, session, name, store):
        """Write a case/data checkpoint via the generic file store."""
        return store.write(session, name)

    def restore_file_checkpoint(self, session, entry, store) -> None:
        """Reload a case/data checkpoint via the generic file store."""
        store.restore(session, entry)

    # -- recovery knowledge (solver physics) -----------------------------

    def governing_model_flags(self) -> tuple[str, ...]:
        """Candidate governing-model flags to toggle for an inactive target."""
        return (
            "setup.models.energy.enabled",
            "setup.models.viscous.enabled",
            "setup.models.radiation.enabled",
            "setup.models.species.enabled",
            "setup.models.multiphase.enabled",
            "setup.models.discrete_phase.enabled",
        )

    # -- inactive-navigation guard ---------------------------------------

    def install_inactive_patch(
        self, register_session, unregister_session, controller_for
    ):
        """Fluent raises ``InactiveObjectError`` during attribute navigation, so
        use the built-in ``Group.__getattribute__`` / ``__setattr__`` guard.

        Returning ``None`` lets :func:`enable_resilient_mode` fall back to the
        default registration (which installs the Fluent patch).
        """
        return None
