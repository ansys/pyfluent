"""Module containing class encapsulating Fluent connection."""

from ctypes import c_int, sizeof
import itertools
import os
import threading
from typing import Any, Callable, List, Optional, Tuple
import weakref

import grpc

from ansys.fluent.core.services.datamodel_se import (
    DatamodelService as DatamodelService_SE,
)
from ansys.fluent.core.services.datamodel_se import PyMenuGeneric
from ansys.fluent.core.services.datamodel_tui import (
    DatamodelService as DatamodelService_TUI,
)
from ansys.fluent.core.services.datamodel_tui import TUIMenuGeneric
from ansys.fluent.core.services.events import EventsService
from ansys.fluent.core.services.field_data import FieldData, FieldDataService, FieldInfo
from ansys.fluent.core.services.health_check import HealthCheckService
from ansys.fluent.core.services.monitor import MonitorsService
from ansys.fluent.core.services.scheme_eval import SchemeEval, SchemeEvalService
from ansys.fluent.core.services.settings import SettingsService
from ansys.fluent.core.services.transcript import TranscriptService
from ansys.fluent.core.solver.events_manager import EventsManager
from ansys.fluent.core.solver.flobject import get_root as settings_get_root
from ansys.fluent.core.solver.monitors_manager import MonitorsManager

try:
    from ansys.fluent.core.solver.settings import root
except Exception:
    root = Any
from ansys.fluent.core.utils.logging import LOG


def _parse_server_info_file(filename: str):
    with open(filename, encoding="utf-8") as f:
        lines = f.readlines()
    ip_and_port = lines[0].strip().split(":")
    ip = ip_and_port[0]
    port = int(ip_and_port[1])
    password = lines[1].strip()
    return ip, port, password


class MonitorThread(threading.Thread):
    """A class used for monitoring a Fluent session.

    Daemon thread which will ensure cleanup of session objects, shutdown of
    non-deamon threads etc.

    Attributes
    ----------
    cbs : List[Callable]
        Cleanup/shutdown functions
    """

    def __init__(self):
        super().__init__(daemon=True)
        self.cbs: List[Callable] = []

    def run(self) -> None:
        main_thread = threading.main_thread()
        main_thread.join()
        for cb in self.cbs:
            cb()


def _get_max_c_int_limit() -> int:
    """Get the maximum limit of a C int.

    Returns
    -------
    int
        The maximum limit of a C int
    """
    return 2 ** (sizeof(c_int) * 8 - 1) - 1


_CODEGEN_MSG_DATAMODEL = (
    "Currently calling the datamodel API in a generic manner. "
    "Please run `python codegen/allapigen.py` from the top-level pyfluent "
    "directory to generate the local datamodel API classes."
)

_CODEGEN_MSG_TUI = (
    "Currently calling the TUI commands in a generic manner. "
    "Please run `python codegen/allapigen.py` from the top-level pyfluent "
    "directory to generate the local TUI commands classes."
)


class Session:
    """Encapsulates a Fluent connection.

    Attributes
    ----------
    meshing: Session.Meshing
        Instance of Session.Meshing which holds the top-level objects
        for meshing TUI and various meshing datamodel API calls.
    solver: Session.Solver
        Instance of Session.Solver which holds the top-level objects
        for solver TUI and settings objects calls.
    scheme_eval: SchemeEval
        Instance of SchemeEval on which Fluent's scheme code can be
        executed.

    Methods
    -------
    create_from_server_info_file(
        server_info_filepath, cleanup_on_exit, start_transcript
        )
        Create a Session instance from server-info file

    start_transcript()
        Start streaming of Fluent transcript

    stop_transcript()
        Stop streaming of Fluent transcript

    check_health()
        Check health of Fluent connection

    exit()
        Close the Fluent connection and exit Fluent.
    """

    _on_exit_cbs: List[Callable] = []
    _id_iter = itertools.count()
    _monitor_thread: Optional[MonitorThread] = None

    def __init__(
        self,
        ip: str = None,
        port: int = None,
        password: str = None,
        channel: grpc.Channel = None,
        cleanup_on_exit: bool = True,
        start_transcript: bool = True,
        remote_instance=None,
    ):
        """Instantiate a Session.

        Parameters
        ----------
        ip : str, optional
            IP address to connect to existing Fluent instance. Used only
            when ``channel`` is ``None``.  Defaults to ``"127.0.0.1"``
            and can also be set by the environment variable
            ``PYFLUENT_FLUENT_IP=<ip>``.
        port : int, optional
            Port to connect to existing Fluent instance. Used only
            when ``channel`` is ``None``.  Defaults value can be set by
            the environment variable ``PYFLUENT_FLUENT_PORT=<port>``.
        password : str, optional
            Password to connect to existing Fluent instance.
        channel : grpc.Channel, optional
            Grpc channel to use to connect to existing Fluent instance.
            ip and port arguments will be ignored when channel is
            specified.
        cleanup_on_exit : bool, optional
            When True, the connected Fluent session will be shut down
            when PyFluent is exited or exit() is called on the session
            instance, by default True.
        start_transcript : bool, optional
            The Fluent transcript is started in the client only when
            start_transcript is True. It can be started and stopped
            subsequently via method calls on the Session object.
        remote_instance : ansys.platform.instancemanagement.Instance
            The corresponding remote instance when Fluent is launched through
            PyPIM. This instance will be deleted when calling
            ``Session.exit()``.
        """
        self._channel_str = None
        if channel is not None:
            self._channel = channel
        else:
            if not ip:
                ip = os.getenv("PYFLUENT_FLUENT_IP", "127.0.0.1")
            if not port:
                port = os.getenv("PYFLUENT_FLUENT_PORT")
            self._channel_str = f"{ip}:{port}"
            if not port:
                raise ValueError(
                    "The port to connect to Fluent session is not provided."
                )
            # Same maximum message length is used in the server
            max_message_length = _get_max_c_int_limit()
            self._channel = grpc.insecure_channel(
                f"{ip}:{port}",
                options=[
                    ("grpc.max_send_message_length", max_message_length),
                    ("grpc.max_receive_message_length", max_message_length),
                ],
            )
        self._metadata: List[Tuple[str, str]] = (
            [("password", password)] if password else []
        )
        self._id = f"session-{next(Session._id_iter)}"

        if not Session._monitor_thread:
            Session._monitor_thread = MonitorThread()
            Session._monitor_thread.start()

        self._transcript_service = TranscriptService(self._channel, self._metadata)
        self._transcript_thread: Optional[threading.Thread] = None

        self._events_service = EventsService(self._channel, self._metadata)
        self.events_manager = EventsManager(self._id, self._events_service)

        self._monitors_service = MonitorsService(self._channel, self._metadata)
        self.monitors_manager = MonitorsManager(self._id, self._monitors_service)

        self.events_manager.register_callback(
            "InitializedEvent", self.monitors_manager.refresh
        )
        self.events_manager.register_callback(
            "DataReadEvent", self.monitors_manager.refresh
        )
        self.events_manager.start()
        self._datamodel_service_tui = DatamodelService_TUI(
            self._channel, self._metadata
        )
        self._datamodel_service_se = DatamodelService_SE(self._channel, self._metadata)
        self._settings_service = SettingsService(self._channel, self._metadata)

        self._field_data_service = FieldDataService(self._channel, self._metadata)
        self.field_info = FieldInfo(self._field_data_service)
        self.field_data = FieldData(self._field_data_service, self.field_info)

        self.meshing = Session.Meshing(
            self._datamodel_service_tui, self._datamodel_service_se
        )
        self.solver = Session.Solver(
            self._datamodel_service_tui, self._settings_service
        )

        self._health_check_service = HealthCheckService(self._channel, self._metadata)

        self._scheme_eval_service = SchemeEvalService(self._channel, self._metadata)
        self.scheme_eval = SchemeEval(self._scheme_eval_service)

        self._cleanup_on_exit = cleanup_on_exit

        if start_transcript:
            self.start_transcript()

        self._remote_instance = remote_instance

        self._finalizer = weakref.finalize(
            self,
            Session._exit,
            self._channel,
            self._cleanup_on_exit,
            self.scheme_eval,
            self._transcript_service,
            self.events_manager,
            self._remote_instance,
        )
        Session._monitor_thread.cbs.append(self._finalizer)

    @classmethod
    def create_from_server_info_file(
        cls,
        server_info_filepath: str,
        cleanup_on_exit: bool = True,
        start_transcript: bool = True,
    ) -> "Session":
        """Create a Session instance from server-info file.

        Parameters
        ----------
        server_info_filepath : str
            Path to server-info file written out by Fluent server
        cleanup_on_exit : bool, optional
            When True, the connected Fluent session will be shut down
            when PyFluent is exited or exit() is called on the session
            instance, by default True.
        start_transcript : bool, optional
            The Fluent transcript is started in the client only when
            start_transcript is True. It can be started and stopped
            subsequently via method calls on the Session object.
            Defaults to true.

        Returns
        -------
        Session
            Session instance
        """
        ip, port, password = _parse_server_info_file(server_info_filepath)
        session = Session(
            ip=ip,
            port=port,
            password=password,
            cleanup_on_exit=cleanup_on_exit,
            start_transcript=start_transcript,
        )
        return session

    @property
    def id(self) -> str:
        """Return the session id."""
        return self._id

    @staticmethod
    def _print_transcript(transcript: str):
        print(transcript)

    @staticmethod
    def _process_transcript(transcript_service):
        responses = transcript_service.begin_streaming()
        transcript = ""
        while True:
            try:
                response = next(responses)
                transcript += response.transcript
                if transcript[-1] == "\n":
                    Session._print_transcript(transcript[0:-1])
                    transcript = ""
            except StopIteration:
                break

    def start_transcript(self) -> None:
        """Start streaming of Fluent transcript."""
        self._transcript_thread = threading.Thread(
            target=Session._process_transcript, args=(self._transcript_service,)
        )

        self._transcript_thread.start()

    def stop_transcript(self) -> None:
        """Stop streaming of Fluent transcript."""
        self._transcript_service.end_streaming()

    def check_health(self) -> str:
        """Check health of Fluent connection."""
        if self._channel:
            try:
                return self._health_check_service.check_health()
            except Exception:
                return HealthCheckService.Status.NOT_SERVING.name
        else:
            return HealthCheckService.Status.NOT_SERVING.name

    def exit(self) -> None:
        """Close the Fluent connection and exit Fluent."""
        self._finalizer()

    @staticmethod
    def _exit(
        channel,
        cleanup_on_exit,
        scheme_eval,
        transcript_service,
        events_manager,
        remote_instance,
    ) -> None:
        if channel:
            if cleanup_on_exit:
                scheme_eval.exec(("(exit-server)",))
            transcript_service.end_streaming()
            events_manager.stop()
            channel.close()
            channel = None

        if remote_instance:
            remote_instance.delete()

    def __enter__(self):
        """Close the Fluent connection and exit Fluent."""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any):
        self._finalizer()

    class Meshing:
        def __init__(
            self, tui_service: DatamodelService_TUI, se_service: DatamodelService_SE
        ):
            self._tui_service = tui_service
            self._se_service = se_service
            self._tui = None
            self._meshing = None
            self._workflow = None
            self._part_management = None
            self._pm_file_management = None

        @property
        def tui(self):
            """Instance of ``main_menu`` on which Fluent's SolverTUI methods
            can be executed."""
            if self._tui is None:
                try:
                    from ansys.fluent.core.meshing.tui import (
                        main_menu as MeshingMainMenu,
                    )

                    self._tui = MeshingMainMenu([], self._tui_service)
                except (ImportError, ModuleNotFoundError):
                    LOG.warning(_CODEGEN_MSG_TUI)
                    self._tui = TUIMenuGeneric([], self._tui_service)
            return self._tui

        @property
        def meshing(self):
            """meshing datamodel root."""
            if self._meshing is None:
                try:
                    from ansys.fluent.core.datamodel.meshing import Root as meshing_root

                    self._meshing = meshing_root(self._se_service, "meshing", [])
                except (ImportError, ModuleNotFoundError):
                    LOG.warning(_CODEGEN_MSG_DATAMODEL)
                    self._meshing = PyMenuGeneric(self._se_service, "meshing")
            return self._meshing

        @property
        def workflow(self):
            """workflow datamodel root."""
            if self._workflow is None:
                try:
                    from ansys.fluent.core.datamodel.workflow import (
                        Root as workflow_root,
                    )

                    self._workflow = workflow_root(self._se_service, "workflow", [])
                except (ImportError, ModuleNotFoundError):
                    LOG.warning(_CODEGEN_MSG_DATAMODEL)
                    self._workflow = PyMenuGeneric(self._se_service, "workflow")
            return self._workflow

        @property
        def PartManagement(self):
            """PartManagement datamodel root."""
            if self._part_management is None:
                try:
                    from ansys.fluent.core.datamodel.PartManagement import (
                        Root as PartManagement_root,
                    )

                    self._part_management = PartManagement_root(
                        self._se_service, "PartManagement", []
                    )
                except (ImportError, ModuleNotFoundError):
                    LOG.warning(_CODEGEN_MSG_DATAMODEL)
                    self._part_management = PyMenuGeneric(
                        self._se_service, "PartManagement"
                    )
            return self._part_management

        @property
        def PMFileManagement(self):
            """PMFileManagement datamodel root."""
            if self._pm_file_management is None:
                try:
                    from ansys.fluent.core.datamodel.PMFileManagement import (
                        Root as PMFileManagement_root,
                    )

                    self._pm_file_management = PMFileManagement_root(
                        self._se_service, "PMFileManagement", []
                    )
                except (ImportError, ModuleNotFoundError):
                    LOG.warning(_CODEGEN_MSG_DATAMODEL)
                    self._pm_file_management = PyMenuGeneric(
                        self._se_service, "PMFileManagement"
                    )
            return self._pm_file_management

    class Solver:
        def __init__(
            self, tui_service: DatamodelService_TUI, settings_service: SettingsService
        ):
            self._tui_service = tui_service
            self._settings_service = settings_service
            self._tui = None
            self._settings_root = None

        @property
        def tui(self):
            """Instance of ``main_menu`` on which Fluent's SolverTUI methods
            can be executed."""
            if self._tui is None:
                try:
                    from ansys.fluent.core.solver.tui import main_menu as SolverMainMenu

                    self._tui = SolverMainMenu([], self._tui_service)
                except (ImportError, ModuleNotFoundError):
                    LOG.warning(_CODEGEN_MSG_TUI)
                    self._tui = TUIMenuGeneric([], self._tui_service)
            return self._tui

        @property
        def root(self):
            """root settings object."""
            if self._settings_root is None:
                LOG.warning("The settings API is currently experimental.")
                self._settings_root = settings_get_root(flproxy=self._settings_service)
            return self._settings_root
