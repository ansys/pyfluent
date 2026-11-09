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

"""Resilient-mode adapter for Fluent solver sessions.

This module holds every Fluent-specific detail used by resilient mode: the
session's error state and health check, Fluent's settings exceptions, the clean
stop of an interrupted solve, case and data files as checkpoints,
``launch_fluent`` for standby sessions, and the energy model as the built-in
governing model of inactive thermal settings.
"""

from __future__ import annotations

import functools
import inspect
from typing import Any, Callable

from ansys.fluent.core.connectivity._file_staging import FileLocation, file_location
from ansys.fluent.core.diagnostics.exceptions import (
    DisallowedValuesError,
    InvalidArgument,
)
from ansys.fluent.core.execution.launcher.launch_options import UIMode
from ansys.fluent.core.resilient.engine import (
    ActivationCandidate,
    ErrorClasses,
    ResilientAdapter,
)
from ansys.fluent.core.resilient.engine.adapter import instance_attr
from ansys.fluent.core.solver.flobject import InactiveObjectError, ReadOnlyActionError

#: ``launch_fluent`` arguments that are never forwarded to standby sessions.
_NOT_FORWARDED = frozenset({"dry_run", "resilient_mode", "resilient_config"})

_CASE_SUFFIX = ".cas.h5"


def _data_file(case_file: str) -> str:
    """Return the data file written next to the case file ``case_file``."""
    stem = (
        case_file[: -len(_CASE_SUFFIX)]
        if case_file.endswith(_CASE_SUFFIX)
        else case_file
    )
    return stem + ".dat.h5"


class FluentAdapter(ResilientAdapter):
    """Resilient-mode adapter for Fluent solver sessions."""

    product_name = "Fluent"
    path_prefixes = ("solver.settings.", "settings.")
    server_name_attr = "fluent_name"
    irreversible_commands = frozenset(
        {
            "iterate",
            "calculate",
            "dual_time_iterate",
            "read_case",
            "read_case_data",
            "read_data",
            "read_mesh",
            "read",
            "replace_mesh",
            "replace",
        }
    )
    interruptible_commands = frozenset({"iterate", "calculate", "dual_time_iterate"})
    non_replayable_commands = frozenset({"interrupt"})
    non_replayable_prefixes = ("write", "export", "save", "print", "display")
    checkpoint_suffix = _CASE_SUFFIX

    # -- settings tree ---------------------------------------------------------

    def invalidate_settings_cache(self, session: Any) -> None:
        """Drop the cached settings root of a solver session."""
        if "_settings" in vars(session):
            session._settings = None

    # -- health ------------------------------------------------------------------

    def is_fatal(self, session: Any) -> bool:
        """Return whether Fluent reported a fatal error for the session."""
        state = instance_attr(session, "_error_state")
        return getattr(state, "name", "") == "fatal"

    def fatal_details(self, session: Any) -> str | None:
        """Return the details of Fluent's fatal error, if any."""
        state = instance_attr(session, "_error_state")
        return getattr(state, "details", None) or None

    def is_server_healthy(self, session: Any) -> bool:
        """Return whether the Fluent server answers its health check."""
        health = instance_attr(session, "_health_check")
        if health is None:
            # Transports without a health service (for example REST) cannot be
            # probed; never treat them as dead.
            return True
        try:
            return bool(health.is_serving)
        except Exception:  # noqa: BLE001
            return False

    # -- errors --------------------------------------------------------------------

    def error_classes(self) -> ErrorClasses:
        """Return Fluent's settings exception classes."""
        return ErrorClasses(
            inactive=InactiveObjectError,
            read_only=ReadOnlyActionError,
            disallowed=DisallowedValuesError,
            invalid_arg=InvalidArgument,
        )

    def is_interrupt(self, err: BaseException) -> bool:
        """Return whether ``err`` is the clean stop of an interrupted solve.

        Fluent ends an interrupted ``iterate`` or ``calculate`` with
        ``RuntimeError("()")``.
        """
        return isinstance(err, RuntimeError) and str(err).strip() == "()"

    # -- session lifecycle -----------------------------------------------------------

    def launch(self, **kwargs: Any) -> Any:
        """Launch a Fluent session with ``launch_fluent``."""
        from ansys.fluent.core import launch_fluent

        return launch_fluent(**kwargs)

    def standby_launcher(self, session: Any) -> Callable[[], Any] | None:
        """Return a launcher that repeats the launch of a local Fluent session.

        Only sessions launched locally by PyFluent are supported. For container,
        remote, or connected sessions, pass ``PoolConfig(launch_kwargs=...)``.
        """
        from ansys.fluent.core import launch_fluent

        args = instance_attr(session, "_launcher_args")
        if not args or not self.shares_client_filesystem(session):
            return None
        if args.get("container_dict") is not None:
            return None
        accepted = inspect.signature(launch_fluent).parameters
        kwargs = {
            key: value
            for key, value in args.items()
            if key in accepted and key not in _NOT_FORWARDED
        }
        # The recorded arguments include the graphics driver the launcher resolved,
        # which only applies to graphical modes; the launcher warns otherwise.
        if UIMode(args.get("ui_mode")) not in (UIMode.GUI, UIMode.HIDDEN_GUI):
            kwargs.pop("graphics_driver", None)
        return functools.partial(launch_fluent, **kwargs)

    def register_exit_callback(
        self, session: Any, callback: Callable[[], None]
    ) -> bool:
        """Run ``callback`` when the session's Fluent connection is finalized."""
        connection = instance_attr(session, "_fluent_connection")
        register = getattr(connection, "register_finalizer_cb", None)
        if not callable(register):
            return False
        register(callback)
        return True

    # -- checkpoints -------------------------------------------------------------------

    def shares_client_filesystem(self, session: Any) -> bool:
        """Return whether Fluent runs locally, outside a container."""
        return file_location(session) is FileLocation.LOCAL

    @staticmethod
    def _scheme_flag(session: Any, expression: str) -> bool | None:
        scheme = instance_attr(session, "scheme")
        evaluate = getattr(scheme, "eval", None)
        if not callable(evaluate):
            return None
        try:
            return bool(evaluate(expression))
        except Exception:  # noqa: BLE001
            return None

    def can_checkpoint(self, session: Any) -> bool:
        """Return whether a case is loaded."""
        return self._scheme_flag(session, "(case-valid?)") is not False

    def checkpoint_artifacts(self, file_path: str, *, include_data: bool) -> list[str]:
        """Return the case file and, with data, the companion data file."""
        return [file_path, _data_file(file_path)] if include_data else [file_path]

    def write_checkpoint(
        self, session: Any, file_path: str, *, include_data: bool
    ) -> bool:
        """Write the case, and the data when it exists, to ``file_path``."""
        file_group = self.settings_root(session).file
        with_data = include_data and self._scheme_flag(session, "(data-valid?)") is True
        if with_data:
            file_group.write_case_data(file_name=file_path)
        else:
            file_group.write_case(file_name=file_path)
        return with_data

    def read_checkpoint(
        self, session: Any, file_path: str, *, include_data: bool
    ) -> None:
        """Read the case (and data) written by :meth:`write_checkpoint`.

        The case and the data are read separately: after a floating point
        exception, Fluent reads the case of a combined case and data read but
        skips the data.

        Raises
        ------
        RuntimeError
            If Fluent did not load the data.
        """
        file_group = self.settings_root(session).file
        file_group.read_case(file_name=file_path)
        if not include_data:
            return
        file_group.read_data(file_name=_data_file(file_path))
        if self._scheme_flag(session, "(data-valid?)") is False:
            raise RuntimeError(f"Fluent did not load the data of {file_path!r}.")

    # -- recovery knowledge ------------------------------------------------------------

    def activation_candidates(self, session: Any) -> tuple[ActivationCandidate, ...]:
        """Return the built-in governing models: the energy model.

        Enabling the energy model activates thermal settings. Users add their own
        candidates with ``ResilientConfig.activation_candidates``.
        """
        return (ActivationCandidate("setup.models.energy.enabled", True),)
