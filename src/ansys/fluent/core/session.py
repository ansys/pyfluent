"""Module containing class encapsulating Fluent connection."""

import atexit
from ctypes import c_int, sizeof
import itertools
import os
import threading
from typing import Any, Callable, List, Optional, Tuple

import grpc

from ansys.fluent.core.services.datamodel_tui import (
    DatamodelService as DatamodelService_TUI,
)

try:
    from ansys.fluent.core.meshing.tui import main_menu as MeshingMainMenu
    from ansys.fluent.core.solver.tui import main_menu as SolverMainMenu
except ImportError:
    pass

from ansys.fluent.core.services.datamodel_se import (
    DatamodelService as DatamodelService_SE,
)

try:
    from ansys.fluent.core.datamodel.PMFileManagement import (
        Root as PMFileManagement_root,
    )
    from ansys.fluent.core.datamodel.PartManagement import Root as PartManagement_root
    from ansys.fluent.core.datamodel.meshing import Root as meshing_root
    from ansys.fluent.core.datamodel.workflow import Root as workflow_root   
except ImportError:
    pass

try:    
    from ansys.fluent.core.datamodel.flicing import Root as icing_root
except ImportError:
    pass

try:    
    from ansys.fluent.core.datamodel.flaero import Root as aero_root
except ImportError:
    pass

from ansys.fluent.core.services.events import EventsService
from ansys.fluent.core.services.field_data import FieldData, FieldDataService, FieldInfo
from ansys.fluent.core.services.health_check import HealthCheckService
from ansys.fluent.core.services.scheme_eval import SchemeEval, SchemeEvalService
from ansys.fluent.core.services.settings import SettingsService
from ansys.fluent.core.services.transcript import TranscriptService
from ansys.fluent.core.solver.events_manager import EventsManager
from ansys.fluent.core.solver.flobject import get_root as settings_get_root

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


class Session:
    """Encapsulates a Fluent connection.

    Attributes
    ----------
    tui : Session.Tui
        Instance of Session.Tui on which Fluent's TUI methods can be
        executed.
    setup: flobject.Group
        Instance of flobject.Group object from which setup related
        settings can be accessed or modified.
    solution: flobject.Group
        Instance of flobject.Group object from which solution related
        settings can be accessed or modified.
    results: flobject.Group
        Instance of flobject.Group object from which results related
        settings can be accessed or modified.
    scheme_eval: SchemeEval
        Instance of SchemeEval on which Fluent's scheme code can be
        executed.

    Methods
    -------
    create_from_server_info_file(server_info_filepath, cleanup_on_exit)
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
        """
        if channel is not None:
            self._channel = channel
        else:
            if not ip:
                ip = os.getenv("PYFLUENT_FLUENT_IP", "127.0.0.1")
            if not port:
                port = os.getenv("PYFLUENT_FLUENT_PORT")
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
        self._settings_root = None

        if not Session._monitor_thread:
            Session._monitor_thread = MonitorThread()
            Session._monitor_thread.start()

        self._transcript_service = TranscriptService(self._channel, self._metadata)
        self._transcript_thread: Optional[threading.Thread] = None

        self._events_service = EventsService(self._channel, self._metadata)
        self.events_manager = EventsManager(self._id, self._events_service)

        self._datamodel_service_tui = DatamodelService_TUI(
            self._channel, self._metadata
        )

        self._field_data_service = FieldDataService(self._channel, self._metadata)
        self.field_info = FieldInfo(self._field_data_service)
        self.field_data = FieldData(self._field_data_service)
        self.tui = Session.Tui(self._datamodel_service_tui)

        self._health_check_service = HealthCheckService(self._channel, self._metadata)

        self._scheme_eval_service = SchemeEvalService(self._channel, self._metadata)
        self.scheme_eval = SchemeEval(self._scheme_eval_service)        

        self._datamodel_service_se = DatamodelService_SE(self._channel, self._metadata)
        if "meshing_root" in globals():
            self.meshing = meshing_root(self._datamodel_service_se, "meshing", [])
        if "workflow_root" in globals():
            self.workflow = workflow_root(self._datamodel_service_se, "workflow", [])
        if "icing_root" in globals() and self.scheme_eval.scheme_eval("(dm-icing?)"):
            self.icing = icing_root(self._datamodel_service_se, "flserver", [])
        if "aero_root" in globals()and self.scheme_eval.scheme_eval("(dm-aero?)"):
            self.aero = aero_root(self._datamodel_service_se, "flserver", [])
        if "PartManagement_root" in globals():
            self.part_management = PartManagement_root(
                self._datamodel_service_se, "PartManagement", []
            )
            self.PartManagement = self.part_management
        if "PMFileManagement_root" in globals():
            self.pm_file_management = PMFileManagement_root(
                self._datamodel_service_se, "PMFileManagement", []
            )
            self.PMFileManagement = self.pm_file_management


        self._cleanup_on_exit = cleanup_on_exit
        Session._monitor_thread.cbs.append(self.exit)

    @classmethod
    def create_from_server_info_file(
        cls, server_info_filepath: str, cleanup_on_exit: bool = True
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
        )
        return session

    @property
    def id(self) -> str:
        """Return the session id."""
        return self._id

    def get_settings_service(self) -> SettingsService:
        """Return an instance of SettingsService object."""
        return SettingsService(self._channel, self._metadata)

    def get_settings_root(self) -> root:
        """Return root settings object."""
        if self._settings_root is None:
            LOG.warning("The settings API is currently experimental.")
            self._settings_root = settings_get_root(flproxy=self.get_settings_service())
        return self._settings_root

    def _process_transcript(self):
        responses = self._transcript_service.begin_streaming()
        transcript = ""
        while True:
            try:
                response = next(responses)
                transcript += response.transcript
                if transcript[-1] == "\n":
                    print(transcript[0:-1])
                    transcript = ""
            except StopIteration:
                break

    def start_transcript(self) -> None:
        """Start streaming of Fluent transcript."""
        self._transcript_thread = threading.Thread(
            target=Session._process_transcript, args=(self,)
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
        if self._channel:
            if self._cleanup_on_exit:
                self.scheme_eval.exec(("(exit-server)",))
            self._transcript_service.end_streaming()
            self.events_manager.stop()
            self._channel.close()
            self._channel = None

    def __enter__(self):
        """Close the Fluent connection and exit Fluent."""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any):
        self.exit()

    @classmethod
    def register_on_exit(cls, callback: Callable) -> None:
        cls._on_exit_cbs.append(callback)

    @staticmethod
    def exit_all() -> None:
        for cb in Session._on_exit_cbs:
            cb()

    class Tui:
        def __init__(self, service: DatamodelService_TUI):
            if "MeshingMainMenu" in globals():
                self.meshing = MeshingMainMenu([], service)
            if "SolverMainMenu" in globals():
                self.solver = SolverMainMenu([], service)


atexit.register(Session.exit_all)
