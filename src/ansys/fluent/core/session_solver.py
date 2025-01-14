"""Module containing class encapsulating Fluent connection."""

from asyncio import Future
import functools
import logging
import threading
from typing import Any, Dict
import warnings
import weakref

from ansys.api.fluent.v0 import svar_pb2 as SvarProtoModule
import ansys.fluent.core as pyfluent
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
from ansys.fluent.core.systemcoupling import SystemCoupling
from ansys.fluent.core.utils.execution import asynchronous
from ansys.fluent.core.utils.fluent_version import (
    FluentVersion,
    get_version_for_file_name,
)
from ansys.fluent.core.warnings import PyFluentDeprecationWarning
from ansys.fluent.core.workflow import ClassicWorkflow

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


def _import_settings_root(root):
    _class_dict = {}
    api_keys = []
    if hasattr(root, "child_names"):
        api_keys = root.child_names

    for root_item in api_keys:
        _class_dict[root_item] = root.__dict__[root_item]

    settings_api_root = type("SettingsRoot", (object,), _class_dict)
    return settings_api_root()


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
        self._build_from_fluent_connection(fluent_connection, scheme_eval)

    def _build_from_fluent_connection(
        self,
        fluent_connection,
        scheme_eval: SchemeEval,
        file_transfer_service: Any | None = None,
    ):
        self._tui_service = self._datamodel_service_tui
        self._se_service = self._datamodel_service_se
        self._tui = None
        self._workflow = None
        self._system_coupling = None
        self._settings_root = None
        self._fluent_version = None
        self._lck = threading.Lock()
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
        self._settings_api_root = None
        self.fields.solution_variable_data = self._solution_variable_data()

        monitors_service = service_creator("monitors").create(
            fluent_connection._channel, fluent_connection._metadata, self._error_state
        )
        self.monitors = MonitorsManager(fluent_connection._id, monitors_service)
        self.events.register_callback(
            SolverEvent.SOLUTION_INITIALIZED, self.monitors.refresh
        )
        self.events.register_callback(SolverEvent.DATA_LOADED, self.monitors.refresh)

        fluent_connection.register_finalizer_cb(self.monitors.stop)

    def _solution_variable_data(self) -> SolutionVariableData:
        """Return the SolutionVariableData handle."""
        return service_creator("svar_data").create(
            self._solution_variable_service, self.fields.solution_variable_info
        )

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
    def tui(self):
        """Instance of ``main_menu`` on which Fluent's SolverTUI methods can be
        executed."""
        if self._tui is None:
            self._tui = _make_tui_module(self, "solver")

        return self._tui

    @property
    def workflow(self):
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
        if pyfluent.SUPPORT_SOLVER_INTERRUPT:
            if command.path in interruptible_commands:
                command._root.solution.run_calculation.interrupt()

    @property
    def settings(self):
        """Root settings object."""
        if self._settings_root is None:
            self._settings_root = flobject.get_root(
                flproxy=self._settings_service,
                version=self._version,
                interrupt=Solver._interrupt,
                file_transfer_service=self._file_transfer_service,
                scheme_eval=self.scheme_eval.scheme_eval,
            )
        return self._settings_root

    @property
    def system_coupling(self):
        """System coupling object."""
        if self._system_coupling is None:
            self._system_coupling = SystemCoupling(self)
        return self._system_coupling

    @property
    def preferences(self):
        """Datamodel root of preferences."""
        if self._preferences is None:
            self._preferences = _make_datamodel_module(self, "preferences")
        return self._preferences

    def _sync_from_future(self, fut: Future):
        with self._lck:
            try:
                fut_session = fut.result()
            except Exception as ex:
                raise RuntimeError("Unable to read mesh") from ex
            state = self.settings.get_state()
            super(Solver, self)._build_from_fluent_connection(
                fut_session._fluent_connection,
                fut_session._fluent_connection._connection_interface.scheme_eval,
                event_type=SolverEvent,
            )
            self._build_from_fluent_connection(
                fut_session._fluent_connection,
                fut_session._fluent_connection._connection_interface.scheme_eval,
            )
            # TODO temporary fix till set_state at settings root is fixed
            _set_state_safe(self.settings, state)

    def read_case_lightweight(self, file_name: str):
        """Read a case file using light IO mode.

        Parameters
        ----------
        file_name : str
            Case file name
        """
        import ansys.fluent.core as pyfluent

        self.file.read(file_type="case", file_name=file_name, lightweight_setup=True)
        launcher_args = dict(self._launcher_args)
        launcher_args.pop("lightweight_mode", None)
        launcher_args["case_file_name"] = file_name
        fut: Future = asynchronous(pyfluent.launch_fluent)(**launcher_args)
        fut.add_done_callback(functools.partial(Solver._sync_from_future, self))

    def get_state(self) -> StateT:
        """Get the state of the object."""
        return self.settings.get_state()

    def set_state(self, state: StateT | None = None, **kwargs):
        """Set the state of the object."""
        self.settings.set_state(state, **kwargs)

    def __call__(self):
        return self.get_state()

    def _populate_settings_api_root(self):
        if not self._settings_api_root:
            self._settings_api_root = _import_settings_root(self.settings)

    def __getattr__(self, attr):
        self._populate_settings_api_root()
        if attr in [x for x in dir(self._settings_api_root) if not x.startswith("_")]:
            if self.get_fluent_version() > FluentVersion.v242:
                warnings.warn(
                    f"'{attr}' is deprecated. Use 'settings.{attr}' instead.",
                    DeprecatedSettingWarning,
                )
        return getattr(self._settings_api_root, attr)

    def __dir__(self):
        settings_dir = []
        if self.get_fluent_version() <= FluentVersion.v242:
            self._populate_settings_api_root()
            settings_dir = dir(self._settings_api_root)
        dir_list = set(list(self.__dict__.keys()) + dir(type(self)) + settings_dir) - {
            "svar_data",
            "svar_info",
            "reduction",
            "field_data",
            "field_info",
            "field_data_streaming",
            "start_journal",
            "stop_journal",
        }
        return sorted(dir_list)
