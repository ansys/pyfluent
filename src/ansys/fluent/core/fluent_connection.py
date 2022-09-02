from ctypes import c_int, sizeof
import itertools
import os
import threading
from typing import Callable, List, Optional, Tuple
import weakref

import grpc

from ansys.fluent.core.services.datamodel_se import (
    DatamodelService as DatamodelService_SE,
)
from ansys.fluent.core.services.datamodel_tui import (
    DatamodelService as DatamodelService_TUI,
)
from ansys.fluent.core.services.events import EventsService
from ansys.fluent.core.services.field_data import FieldData, FieldDataService, FieldInfo
from ansys.fluent.core.services.health_check import HealthCheckService
from ansys.fluent.core.services.monitor import MonitorsService
from ansys.fluent.core.services.scheme_eval import SchemeEval, SchemeEvalService
from ansys.fluent.core.services.settings import SettingsService
from ansys.fluent.core.services.transcript import TranscriptService
from ansys.fluent.core.solver.events_manager import EventsManager
from ansys.fluent.core.solver.monitors_manager import MonitorsManager


def _get_max_c_int_limit() -> int:
    """Get the maximum limit of a C int.

    Returns
    -------
    int
        The maximum limit of a C int
    """
    return 2 ** (sizeof(c_int) * 8 - 1) - 1


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


class _FluentConnection:
    """Encapsulates a Fluent connection.

    Methods
    -------
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
        self._id = f"session-{next(_FluentConnection._id_iter)}"

        if not _FluentConnection._monitor_thread:
            _FluentConnection._monitor_thread = MonitorThread()
            _FluentConnection._monitor_thread.start()

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
        self.datamodel_service_tui = DatamodelService_TUI(self._channel, self._metadata)
        self.datamodel_service_se = DatamodelService_SE(self._channel, self._metadata)
        self.settings_service = SettingsService(self._channel, self._metadata)

        self._field_data_service = FieldDataService(self._channel, self._metadata)
        self.field_info = FieldInfo(self._field_data_service)
        self.field_data = FieldData(self._field_data_service, self.field_info)

        self._health_check_service = HealthCheckService(self._channel, self._metadata)

        self._scheme_eval_service = SchemeEvalService(self._channel, self._metadata)
        self.scheme_eval = SchemeEval(self._scheme_eval_service)

        self._cleanup_on_exit = cleanup_on_exit
        self._start_transcript = start_transcript

        if start_transcript:
            self.start_transcript()

        self._remote_instance = remote_instance

        self._finalizer = weakref.finalize(
            self,
            _FluentConnection._exit,
            self._channel,
            self._cleanup_on_exit,
            self.scheme_eval,
            self._transcript_service,
            self.events_manager,
            self._remote_instance,
        )
        _FluentConnection._monitor_thread.cbs.append(self._finalizer)

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
                    _FluentConnection._print_transcript(transcript[0:-1])
                    transcript = ""
            except StopIteration:
                break

    def get_current_fluent_mode(self):
        """Gets and returns the mode of the current instance of fluent (meshing
        or solver)."""
        if self.scheme_eval.scheme_eval("(cx-solver-mode?)"):
            return "solver"
        else:
            return "meshing"

    def start_transcript(self) -> None:
        """Start streaming of Fluent transcript."""
        self._transcript_thread = threading.Thread(
            target=_FluentConnection._process_transcript,
            args=(self._transcript_service,),
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

    def get_fluent_version(self):
        """Gets and returns the fluent version."""
        return ".".join(map(str, self.scheme_eval.scheme_eval("(cx-version)")))

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
