from ctypes import c_int, sizeof
import itertools
import os
import threading
import time
from typing import Callable, List, Optional, Tuple
import warnings
import weakref

import grpc

from ansys.fluent.core.journaling import Journal
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
from ansys.fluent.core.streaming_services.events_streaming import EventsManager
from ansys.fluent.core.streaming_services.monitor_streaming import MonitorsManager
from ansys.fluent.core.streaming_services.transcript_streaming import Transcript


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


class _IsDataValid:
    def __init__(self, scheme_eval):
        self._scheme_eval = scheme_eval

    def __bool__(self):
        return self()

    def __call__(self):
        return self._scheme_eval.scheme_eval("(data-valid?)")


class _FluentConnection:
    """Encapsulates a Fluent connection.

    Methods
    -------
    get_current_fluent_mode()
        Gets the mode of the current instance of Fluent (meshing or
        solver).

    get_fluent_version()
        Gets and returns the fluent version.

    exit()
        Close the Fluent connection and exit Fluent.
    """

    _on_exit_cbs: List[Callable] = []
    _id_iter = itertools.count()
    _monitor_thread: Optional[MonitorThread] = None
    _writing_transcript_to_interpreter = False

    def __init__(
        self,
        start_timeout: int = 100,
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
        start_timeout: int, optional
            Maximum allowable time in seconds for connecting to the Fluent
            server. The default is ``100``.
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
        self._data_valid = False
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

        self.health_check_service = HealthCheckService(self._channel, self._metadata)

        counter = 0
        while not self.health_check_service.is_serving:
            time.sleep(1)
            counter += 1
            if counter > start_timeout:
                raise RuntimeError(
                    f"The connection to the Fluent server could not be established within the configurable {start_timeout} second time limit."
                )

        self._id = f"session-{next(_FluentConnection._id_iter)}"

        if not _FluentConnection._monitor_thread:
            _FluentConnection._monitor_thread = MonitorThread()
            _FluentConnection._monitor_thread.start()

        self.transcript = Transcript(self._channel, self._metadata)

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

        self._scheme_eval_service = SchemeEvalService(self._channel, self._metadata)
        self.scheme_eval = SchemeEval(self._scheme_eval_service)

        self._field_data_service = FieldDataService(self._channel, self._metadata)
        self.field_info = FieldInfo(self._field_data_service)

        self.field_data = FieldData(
            self._field_data_service, self.field_info, _IsDataValid(self.scheme_eval)
        )

        self.journal = Journal(self.scheme_eval)

        self._cleanup_on_exit = cleanup_on_exit

        self.callback_id1 = None
        self.callback_id2 = None

        if start_transcript:
            self.transcript.start()

        self._remote_instance = remote_instance

        self._finalizer = weakref.finalize(
            self,
            _FluentConnection._exit,
            self._channel,
            self._cleanup_on_exit,
            self.scheme_eval,
            self.transcript,
            self.events_manager,
            self._remote_instance,
        )
        _FluentConnection._monitor_thread.cbs.append(self._finalizer)

    @property
    def id(self) -> str:
        """Return the session id."""
        return self._id

    def get_current_fluent_mode(self):
        """Gets the mode of the current instance of Fluent (meshing or
        solver)."""
        if self.scheme_eval.scheme_eval("(cx-solver-mode?)"):
            return "solver"
        else:
            return "meshing"

    def start_transcript(
        self, file_path: str = None, write_to_interpreter: bool = True
    ) -> None:
        """Start streaming of Fluent transcript."""
        warnings.warn("Use -> transcript.start()", DeprecationWarning)
        self.transcript.start(file_path, write_to_interpreter)

    def stop_transcript(self) -> None:
        """Stop streaming of Fluent transcript."""
        warnings.warn("Use -> transcript.stop()", DeprecationWarning)
        self.transcript.stop()

    def start_journal(self, file_path: str):
        """Executes tui command to start journal."""
        warnings.warn("Use -> journal.start()", DeprecationWarning)
        self.journal.start(file_path)

    def stop_journal(self):
        """Executes tui command to stop journal."""
        warnings.warn("Use -> journal.stop()", DeprecationWarning)
        self.journal.stop()

    def check_health(self) -> str:
        """Check health of Fluent connection."""
        warnings.warn("Use -> health_check_service.status()", DeprecationWarning)
        return self.health_check_service.status()

    def get_fluent_version(self):
        """Gets and returns the fluent version."""
        return self.scheme_eval.version

    def exit(self) -> None:
        """Close the Fluent connection and exit Fluent."""
        self._finalizer()

    @staticmethod
    def _exit(
        channel,
        cleanup_on_exit,
        scheme_eval,
        transcript,
        events_manager,
        remote_instance,
    ) -> None:
        if channel:
            if cleanup_on_exit:
                try:
                    scheme_eval.exec(("(exit-server)",))
                except Exception:
                    pass
            transcript.stop()
            events_manager.stop()
            channel.close()
            channel = None

        if remote_instance:
            remote_instance.delete()
