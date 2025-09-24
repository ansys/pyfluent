# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
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

"""Module containing class encapsulating Fluent connection."""

import logging
import threading
from typing import TYPE_CHECKING, Any, Dict, cast
import warnings
import weakref

from ansys.api.fluent.v0 import svar_pb2 as SvarProtoModule
import ansys.fluent.core as pyfluent
from ansys.fluent.core.exceptions import BetaFeaturesNotEnabled
from ansys.fluent.core.pyfluent_warnings import PyFluentDeprecationWarning
from ansys.fluent.core.services import SchemeEval, service_creator
from ansys.fluent.core.services.field_data import ZoneInfo, ZoneType
from ansys.fluent.core.services.reduction import ReductionService
from ansys.fluent.core.services.solution_variables import (
    SolutionVariableData,
    SolutionVariableInfo,
)
from ansys.fluent.core.session import BaseSession
from ansys.fluent.core.session_shared import _make_datamodel_module, _make_tui_module
from ansys.fluent.core.solver import flobject
from ansys.fluent.core.solver.flobject import (
    DeprecatedSettingWarning,
    Group,
    NamedObject,
    SettingsBase,
    StateT,
    StateType,
)
import ansys.fluent.core.solver.function.reduction as reduction_old
from ansys.fluent.core.streaming_services.events_streaming import SolverEvent
from ansys.fluent.core.streaming_services.monitor_streaming import MonitorsManager
from ansys.fluent.core.system_coupling import SystemCoupling
from ansys.fluent.core.utils.fluent_version import (
    FluentVersion,
    get_version_for_file_name,
)
from ansys.fluent.core.workflow import ClassicWorkflow

if TYPE_CHECKING:
    from ansys.fluent.core.generated.datamodel_252.preferences import (
        Root as preferences_root,
    )
    import ansys.fluent.core.generated.solver.settings_252 as settings_root
    from ansys.fluent.core.generated.solver.tui_252 import main_menu


tui_logger = logging.getLogger("pyfluent.tui")
datamodel_logger = logging.getLogger("pyfluent.datamodel")


def _set_state_safe(obj: SettingsBase, state: StateType):
    try:
        obj.set_state(state)
    except RuntimeError:
        if isinstance(obj, NamedObject):
            for k, v in state.items():
                _set_state_safe(obj[k], v)
        elif isinstance(obj, Group):
            for k, v in state.items():
                _set_state_safe(getattr(obj, k), v)
        else:
            datamodel_logger.debug(f"set_state failed at {obj.path}")


class Solver(BaseSession):
    """Encapsulates a Fluent solver session.

    A ``tui`` object for solver TUI
    commanding, and solver settings objects are all exposed here.
    """

    def __init__(
        self,
        fluent_connection,
        scheme_eval: SchemeEval,
        file_transfer_service: Any | None = None,
        start_transcript: bool = True,
        launcher_args: Dict[str, Any] | None = None,
    ):
        """Solver session.

        Parameters
        ----------
        fluent_connection (:ref:`ref_fluent_connection`):
            Encapsulates a Fluent connection.
        scheme_eval: SchemeEval
            Instance of ``SchemeEval`` to execute Fluent's scheme code on.
        file_transfer_service : Optional
            Service for uploading and downloading files.
        start_transcript : bool, optional
            Whether to start the Fluent transcript in the client.
            The default is ``True``, in which case the Fluent
            transcript can be subsequently started and stopped
            using method calls on the ``Session`` object.
        """
        super(Solver, self).__init__(
            fluent_connection=fluent_connection,
            scheme_eval=scheme_eval,
            file_transfer_service=file_transfer_service,
            start_transcript=start_transcript,
            launcher_args=launcher_args,
            event_type=SolverEvent,
            get_zones_info=weakref.WeakMethod(self._get_zones_info),
        )
        self._settings = None
        self._build_from_fluent_connection(
            fluent_connection, scheme_eval, launcher_args=launcher_args
        )

    def _build_from_fluent_connection(
        self,
        fluent_connection,
        scheme_eval: SchemeEval,
        file_transfer_service: Any | None = None,
        launcher_args: Dict[str, Any] | None = None,
    ):
        self._tui_service = self._datamodel_service_tui
        self._se_service = self._datamodel_service_se
        self._tui = None
        self._workflow = None
        self._system_coupling = None
        self._fluent_version = None
        self._bg_session_threads = []
        self._launcher_args = launcher_args
        self._solution_variable_service = service_creator("svar").create(
            fluent_connection._channel, fluent_connection._metadata
        )
        self.fields.solution_variable_info = SolutionVariableInfo(
            self._solution_variable_service
        )
        self._reduction_service = self._fluent_connection.create_grpc_service(
            ReductionService, self._error_state
        )
        if FluentVersion(self._version) >= FluentVersion.v241:
            self.fields.reduction = service_creator("reduction").create(
                self._reduction_service, self
            )
        else:
            self.fields.reduction = reduction_old
        self.fields.solution_variable_data = self._solution_variable_data()

        monitors_service = service_creator("monitors").create(
            fluent_connection._channel, fluent_connection._metadata, self._error_state
        )
        #: Manage Fluent's solution monitors.
        self.monitors = MonitorsManager(fluent_connection._id, monitors_service)
        if not pyfluent.config.disable_monitor_refresh_on_init:
            self.events.register_callback(
                (SolverEvent.SOLUTION_INITIALIZED, SolverEvent.DATA_LOADED),
                self.monitors.refresh,
            )

        fluent_connection.register_finalizer_cb(self.monitors.stop)

        # Background sessions should be finalized before finalizing the
        # gRPC services of the main session.
        fluent_connection.register_finalizer_cb(
            weakref.WeakMethod(self._stop_bg_sessions), at_start=True
        )

    def _solution_variable_data(self) -> SolutionVariableData:
        """Return the SolutionVariableData handle."""
        return service_creator("svar_data").create(
            self._solution_variable_service, self.fields.solution_variable_info
        )

    @property
    def settings(self) -> "settings_root.root":
        """Settings root handle."""
        if self._settings is None:
            #: Root settings object.
            self._settings = flobject.get_root(
                flproxy=self._settings_service,
                version=self._version,
                interrupt=Solver._interrupt,
                file_transfer_service=self._file_transfer_service,
                scheme_eval=self.scheme.eval,
            )
        return cast("settings_root.root", self._settings)

    @property
    def svar_data(self):
        """``SolutionVariableData`` handle."""
        warnings.warn(
            "svar_data is deprecated. Use fields.solution_variable_data instead.",
            PyFluentDeprecationWarning,
        )
        return self.fields.solution_variable_data

    @property
    def svar_info(self):
        """``SolutionVariableInfo`` handle."""
        warnings.warn(
            "svar_info is deprecated. Use fields.solution_variable_info instead.",
            PyFluentDeprecationWarning,
        )
        return self.fields.solution_variable_info

    def _get_zones_info(self) -> list[ZoneInfo]:
        zones_info = []
        for (
            zone_info
        ) in self.fields.solution_variable_info.get_zones_info()._zones_info.values():
            zone_type = (
                ZoneType.CELL
                if zone_info.thread_type == SvarProtoModule.ThreadType.CELL_THREAD
                else ZoneType.FACE
            )
            zones_info.append(
                ZoneInfo(
                    _id=zone_info.zone_id, name=zone_info.name, zone_type=zone_type
                )
            )
        return zones_info

    @property
    def reduction(self):
        """``Reduction`` handle."""
        warnings.warn(
            "reduction is deprecated. Use fields.reduction instead.",
            PyFluentDeprecationWarning,
        )
        return self.fields.reduction

    @property
    def _version(self):
        """Fluent's product version."""
        if self._fluent_version is None:
            self._fluent_version = get_version_for_file_name(session=self)
        return self._fluent_version

    @property
    def tui(self) -> "main_menu":
        """Instance of ``main_menu`` on which Fluent's SolverTUI methods can be
        executed."""
        if self._tui is None:
            self._tui = _make_tui_module(self, "solver")

        return cast("main_menu", self._tui)

    @property
    def workflow(self) -> ClassicWorkflow:
        """Datamodel root for workflow."""
        if not self._workflow:
            self._workflow = ClassicWorkflow(
                _make_datamodel_module(self, "workflow"),
                Solver,
                self.get_fluent_version(),
            )
        return self._workflow

    @classmethod
    def _interrupt(cls, command):
        interruptible_commands = [
            "solution/run-calculation/iterate",
            "solution/run-calculation/calculate",
            "solution/run-calculation/dual-time-iterate",
        ]
        if pyfluent.config.support_solver_interrupt:
            if command.path in interruptible_commands:
                command._root.solution.run_calculation.interrupt()

    @property
    def system_coupling(self) -> SystemCoupling:
        """System coupling object."""
        if self._system_coupling is None:
            self._system_coupling = SystemCoupling(self)
        return self._system_coupling

    @property
    def preferences(self) -> "preferences_root":
        """Datamodel root of preferences."""
        if self._preferences is None:
            self._preferences = _make_datamodel_module(self, "preferences")
        return cast("preferences_root", self._preferences)

    def _start_bg_session_and_sync(self, launcher_args):
        """Start a background session and sync it with the current session."""
        try:
            bg_session = pyfluent.launch_fluent(**launcher_args)
        except Exception as ex:
            raise RuntimeError("Unable to read mesh") from ex
        state = self.settings.get_state()
        super(Solver, self)._build_from_fluent_connection(
            bg_session._fluent_connection,
            bg_session._fluent_connection._connection_interface.scheme_eval,
            event_type=SolverEvent,
            launcher_args=launcher_args,
        )
        self._build_from_fluent_connection(
            bg_session._fluent_connection,
            bg_session._fluent_connection._connection_interface.scheme_eval,
            launcher_args=launcher_args,
        )
        # TODO temporary fix till set_state at settings root is fixed
        _set_state_safe(self.settings, state)

    def _stop_bg_sessions(self):
        """Stop all background sessions."""
        for thread in self._bg_session_threads:
            if thread.is_alive():
                thread.join()

    def read_case_lightweight(self, file_name: str):
        """Read a case file using light IO mode.

        Parameters
        ----------
        file_name : str
            Case file name
        """

        self.file.read(file_type="case", file_name=file_name, lightweight_setup=True)
        launcher_args = dict(self._launcher_args)
        launcher_args.pop("lightweight_mode", None)
        launcher_args["case_file_name"] = file_name
        self._bg_session_threads.append(
            threading.Thread(
                target=self._start_bg_session_and_sync, args=(launcher_args,)
            )
        )

    def get_state(self) -> StateT:
        """Get the state of the object."""
        return self.settings.get_state()

    def set_state(self, state: StateT | None = None, **kwargs):
        """Set the state of the object."""
        self.settings.set_state(state, **kwargs)

    def __call__(self):
        return self.get_state()

    def __getattr__(self, name):
        try:
            return super().__getattribute__(name)
        except AttributeError as ex:
            if name in self.settings.child_names:
                warnings.warn(
                    f"'{name}' is deprecated. Use 'settings.{name}' instead.",
                    DeprecatedSettingWarning,
                )
                return getattr(self.settings, name)
            else:
                raise ex

    def __dir__(self):
        dir_list = set(super().__dir__()) - {
            "svar_data",
            "svar_info",
            "reduction",
        }
        return sorted(dir_list)

    def switch_to_meshing(self):
        """Switch to meshing mode and return a meshing session object. Deactivate this
        object's public interface and streaming services.

        Raises
        ------
        AttributeError
            If beta features are not enabled in Fluent.

        Returns
        -------
        Meshing
        """
        if not self._is_beta_enabled:
            raise BetaFeaturesNotEnabled("switch_to_meshing")
        from ansys.fluent.core.session_meshing import Meshing

        self.settings.switch_to_meshing_mode()
        for cb in self._fluent_connection.finalizer_cbs:
            cb()
        meshing_session = Meshing(
            fluent_connection=self._fluent_connection,
            scheme_eval=self.scheme,
            file_transfer_service=self._file_transfer_service,
        )
        self._fluent_connection = None
        self.__doc__ = (
            "The solver session is no longer usable after switching to meshing mode."
        )
        return meshing_session
