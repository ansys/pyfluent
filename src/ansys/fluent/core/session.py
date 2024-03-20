"""Module containing class encapsulating Fluent connection and the Base Session."""

import importlib
import json
import logging
from typing import Any, Optional
import warnings

from ansys.fluent.core.fluent_connection import FluentConnection
from ansys.fluent.core.journaling import Journal
from ansys.fluent.core.services import service_creator
from ansys.fluent.core.services.field_data import FieldDataService
from ansys.fluent.core.session_shared import (  # noqa: F401
    _CODEGEN_MSG_DATAMODEL,
    _CODEGEN_MSG_TUI,
)
from ansys.fluent.core.streaming_services.datamodel_event_streaming import (
    DatamodelEvents,
)
from ansys.fluent.core.streaming_services.events_streaming import EventsManager
from ansys.fluent.core.streaming_services.field_data_streaming import FieldDataStreaming
from ansys.fluent.core.streaming_services.monitor_streaming import MonitorsManager
from ansys.fluent.core.streaming_services.transcript_streaming import Transcript
from ansys.fluent.core.utils.fluent_version import FluentVersion

from .rpvars import RPVars

try:
    from ansys.fluent.core.solver.settings import root
except Exception:
    root = Any

datamodel_logger = logging.getLogger("pyfluent.datamodel")
logger = logging.getLogger("pyfluent.general")


def _parse_server_info_file(file_name: str):
    with open(file_name, encoding="utf-8") as f:
        lines = f.readlines()
    ip_and_port = lines[0].strip().split(":")
    ip = ip_and_port[0]
    port = int(ip_and_port[1])
    password = lines[1].strip()
    return ip, port, password


def _get_datamodel_attributes(session, attribute: str):
    try:
        preferences_module = importlib.import_module(
            f"ansys.fluent.core.datamodel_{session._version}." + attribute
        )
        return preferences_module.Root(session._se_service, attribute, [])
    except ImportError:
        datamodel_logger.warning(_CODEGEN_MSG_DATAMODEL)


def _get_preferences(session):
    return _get_datamodel_attributes(session, "preferences")


class _IsDataValid:
    def __init__(self, scheme_eval):
        self._scheme_eval = scheme_eval

    def __bool__(self):
        return self()

    def __call__(self):
        return self._scheme_eval.scheme_eval("(data-valid?)")


class BaseSession:
    """Instantiates a Fluent connection.

    Attributes
    ----------
    scheme_eval: SchemeEval
        Instance of SchemeEval on which Fluent's scheme code can be
        executed.

    Methods
    -------
    create_from_server_info_file(
        server_info_file_name, cleanup_on_exit, start_transcript
        )
        Create a Session instance from server-info file

    exit()
        Close the Fluent connection and exit Fluent.
    """

    def __init__(
        self,
        fluent_connection: FluentConnection,
        file_transfer_service: Optional[Any] = None,
    ):
        """BaseSession.

        Args:
            fluent_connection (:ref:`ref_fluent_connection`): Encapsulates a Fluent connection.
            file_transfer_service: Supports file upload and download.
        """
        BaseSession.build_from_fluent_connection(
            self, fluent_connection, file_transfer_service
        )

    def build_from_fluent_connection(
        self,
        fluent_connection: FluentConnection,
        file_transfer_service: Optional[Any] = None,
    ):
        """Build a BaseSession object from fluent_connection object."""
        self._fluent_connection = fluent_connection
        self._file_transfer_service = file_transfer_service
        self._error_state = fluent_connection._error_state
        self.scheme_eval = fluent_connection.scheme_eval
        self.rp_vars = RPVars(self.scheme_eval.string_eval)
        self._preferences = None
        self.journal = Journal(self.scheme_eval)

        self._transcript_service = service_creator("transcript").create(
            fluent_connection._channel, fluent_connection._metadata
        )
        self.transcript = Transcript(self._transcript_service)
        if fluent_connection.start_transcript:
            self.transcript.start()

        self.datamodel_service_tui = service_creator("tui").create(
            fluent_connection._channel,
            fluent_connection._metadata,
            self._error_state,
            self.scheme_eval,
        )

        self.datamodel_service_se = service_creator("datamodel").create(
            fluent_connection._channel,
            fluent_connection._metadata,
            self._error_state,
            self._file_transfer_service,
        )

        self.datamodel_events = DatamodelEvents(self.datamodel_service_se)
        self.datamodel_events.start()

        self._batch_ops_service = service_creator("batch_ops").create(
            fluent_connection._channel, fluent_connection._metadata
        )
        self._events_service = service_creator("events").create(
            fluent_connection._channel, fluent_connection._metadata
        )
        self.events_manager = EventsManager(
            self._events_service, self._error_state, fluent_connection._id
        )

        self._monitors_service = service_creator("monitors").create(
            fluent_connection._channel, fluent_connection._metadata, self._error_state
        )
        self.monitors_manager = MonitorsManager(
            fluent_connection._id, self._monitors_service
        )

        self.events_manager.register_callback(
            "InitializedEvent", self.monitors_manager.refresh
        )
        self.events_manager.register_callback(
            "DataReadEvent", self.monitors_manager.refresh
        )

        self.events_manager.start()

        self._field_data_service = self._fluent_connection.create_grpc_service(
            FieldDataService, self._error_state
        )

        class Fields:
            """Container for field and solution variables."""

            def __init__(self, _session):
                """Initialize Fields."""
                self.field_info = service_creator("field_info").create(
                    _session._field_data_service, _IsDataValid(_session.scheme_eval)
                )
                self.field_data = service_creator("field_data").create(
                    _session._field_data_service,
                    self.field_info,
                    _IsDataValid(_session.scheme_eval),
                    _session.scheme_eval,
                )
                self.field_data_streaming = FieldDataStreaming(
                    _session._fluent_connection._id, _session._field_data_service
                )

        self.fields = Fields(self)

        self._settings_service = service_creator("settings").create(
            fluent_connection._channel,
            fluent_connection._metadata,
            self.scheme_eval,
            self._error_state,
        )

        self.health_check_service = fluent_connection.health_check_service
        self.connection_properties = fluent_connection.connection_properties

        self._fluent_connection.register_finalizer_cb(
            self.datamodel_service_se.unsubscribe_all_events
        )
        for obj in (
            self.datamodel_events,
            self.transcript,
            self.events_manager,
            self.monitors_manager,
        ):
            self._fluent_connection.register_finalizer_cb(obj.stop)

    @property
    def field_info(self):
        """Provides access to Fluent field information."""
        warnings.warn(
            "field_info is deprecated. Use fields.field_info instead.",
            DeprecationWarning,
        )
        return self.fields.field_info

    @property
    def field_data(self):
        """Fluent field data on surfaces."""
        warnings.warn(
            "field_data is deprecated. Use fields.field_data instead.",
            DeprecationWarning,
        )
        return self.fields.field_data

    @property
    def field_data_streaming(self):
        """Field gRPC streaming service of Fluent."""
        warnings.warn(
            "field_data_streaming is deprecated. Use fields.field_data_streaming instead.",
            DeprecationWarning,
        )
        return self.fields.field_data_streaming

    @property
    def id(self) -> str:
        """Return the session ID."""
        return self._fluent_connection._id

    def start_journal(self, file_name: str):
        """Executes tui command to start journal."""
        warnings.warn("Use -> journal.start()", DeprecationWarning)
        self.journal.start(file_name)

    def stop_journal(self):
        """Executes tui command to stop journal."""
        warnings.warn("Use -> journal.stop()", DeprecationWarning)
        self.journal.stop()

    @classmethod
    def _create_from_server_info_file(
        cls,
        server_info_file_name: str,
        file_transfer_service: Optional[Any] = None,
        **connection_kwargs,
    ):
        """Create a Session instance from server-info file.

        Parameters
        ----------
        server_info_file_name : str
            Path to server-info file written out by Fluent server
        file_transfer_service : Optional
            Support file upload and download.
        **connection_kwargs : dict, optional
            Additional keyword arguments may be specified, and they will be passed to the `FluentConnection`
            being initialized. For example, ``cleanup_on_exit = True``, or ``start_transcript = True``.
            See :func:`FluentConnection initialization <ansys.fluent.core.fluent_connection.FluentConnection.__init__>`
            for more details and possible arguments.

        Returns
        -------
        Session
            Session instance
        """
        ip, port, password = _parse_server_info_file(server_info_file_name)
        session = cls(
            fluent_connection=FluentConnection(
                ip=ip, port=port, password=password, **connection_kwargs
            ),
            file_transfer_service=file_transfer_service,
        )
        return session

    def execute_tui(self, command: str) -> None:
        """Executes a tui command."""
        self.scheme_eval.scheme_eval(f"(ti-menu-load-string {json.dumps(command)})")

    def get_fluent_version(self) -> FluentVersion:
        """Gets and returns the fluent version."""
        return FluentVersion(self.scheme_eval.version)

    def exit(self, **kwargs) -> None:
        """Exit session."""
        logger.debug("session.exit() called")
        self._fluent_connection.exit(**kwargs)

    def force_exit(self) -> None:
        """Immediately terminates the Fluent session, losing unsaved progress and
        data."""
        self._fluent_connection.force_exit()

    def upload(self, file_name: str):
        """Upload a file to the server.

        Parameters
        ----------
        file_name : str
            Name of the local file to upload to the server.
        """
        if self._file_transfer_service:
            return self._file_transfer_service.upload_file(file_name)

    def download(self, file_name: str, local_directory: Optional[str] = "."):
        """Download a file from the server.

        Parameters
        ----------
        file_name : str
            Name of the file to download from the server.
        local_directory : str, optional
            Local destination directory. The default is the current working directory.
        """
        if self._file_transfer_service:
            return self._file_transfer_service.download_file(file_name, local_directory)

    def __enter__(self):
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any):
        """Close the Fluent connection and exit Fluent."""
        logger.debug("session.__exit__() called")
        self.exit()

    def __dir__(self):
        dir_list = set(list(self.__dict__.keys()) + dir(type(self))) - {
            "field_data",
            "field_info",
            "field_data_streaming",
        }
        return sorted(dir_list)
