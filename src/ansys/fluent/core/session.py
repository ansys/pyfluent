"""Module containing class encapsulating Fluent connection and the Base
Session."""
import importlib
import json
import logging
import os
from typing import Any
import warnings

from ansys.fluent.core.fluent_connection import FluentConnection
from ansys.fluent.core.journaling import Journal
from ansys.fluent.core.services.batch_ops import BatchOpsService
from ansys.fluent.core.services.datamodel_se import (
    DatamodelService as DatamodelService_SE,
)
from ansys.fluent.core.services.datamodel_tui import (
    DatamodelService as DatamodelService_TUI,
)
from ansys.fluent.core.services.events import EventsService
from ansys.fluent.core.services.field_data import FieldData, FieldDataService, FieldInfo
from ansys.fluent.core.services.monitor import MonitorsService
from ansys.fluent.core.services.settings import SettingsService
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

from .rpvars import RPVars

try:
    from ansys.fluent.core.solver.settings import root
except Exception:
    root = Any

datamodel_logger = logging.getLogger("pyfluent.datamodel")
logger = logging.getLogger("pyfluent.general")


def _parse_server_info_file(filename: str):
    with open(filename, encoding="utf-8") as f:
        lines = f.readlines()
    ip_and_port = lines[0].strip().split(":")
    ip = ip_and_port[0]
    port = int(ip_and_port[1])
    password = lines[1].strip()
    return ip, port, password


def _get_datamodel_attributes(session, attribute: str):
    try:
        preferences_module = importlib.import_module(
            f"ansys.fluent.core.datamodel_{session.version}." + attribute
        )
        return preferences_module.Root(session._se_service, attribute, [])
    except ImportError:
        datamodel_logger.warning(_CODEGEN_MSG_DATAMODEL)


def _get_preferences(session):
    return _get_datamodel_attributes(session, "preferences")


def _get_solverworkflow(session):
    return _get_datamodel_attributes(session, "solverworkflow")


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
        server_info_filepath, cleanup_on_exit, start_transcript
        )
        Create a Session instance from server-info file

    exit()
        Close the Fluent connection and exit Fluent.
    """

    def __init__(self, fluent_connection: FluentConnection):
        """BaseSession.

        Args:
            fluent_connection (:ref:`ref_fluent_connection`): Encapsulates a Fluent connection.
        """
        BaseSession.build_from_fluent_connection(self, fluent_connection)

    def build_from_fluent_connection(self, fluent_connection: FluentConnection):
        """Build a BaseSession object from fluent_connection object."""
        self.fluent_connection = fluent_connection
        self.error_state = self.fluent_connection.error_state
        self.scheme_eval = self.fluent_connection.scheme_eval
        self.rp_vars = RPVars(self.scheme_eval.string_eval)
        self._uploader = None
        self._preferences = None
        self._solverworkflow = None
        self.journal = Journal(self.scheme_eval)

        self.transcript = self.fluent_connection.create_service(Transcript)
        if fluent_connection.start_transcript:
            self.transcript.start()

        self.datamodel_service_tui = self.fluent_connection.create_service(
            DatamodelService_TUI, self.error_state
        )

        self.datamodel_service_se = self.fluent_connection.create_service(
            DatamodelService_SE, self.error_state
        )
        self.datamodel_events = DatamodelEvents(self.datamodel_service_se)
        self.datamodel_events.start()

        self._batch_ops_service = self.fluent_connection.create_service(BatchOpsService)
        self.events_service = self.fluent_connection.create_service(EventsService)
        self.events_manager = EventsManager(
            self.events_service, self.error_state, self.fluent_connection._id
        )

        self._monitors_service = self.fluent_connection.create_service(
            MonitorsService, self.error_state
        )
        self.monitors_manager = MonitorsManager(
            self.fluent_connection._id, self._monitors_service
        )

        self.events_manager.register_callback(
            "InitializedEvent", self.monitors_manager.refresh
        )
        self.events_manager.register_callback(
            "DataReadEvent", self.monitors_manager.refresh
        )

        self.events_manager.start()

        self._field_data_service = self.fluent_connection.create_service(
            FieldDataService, self.error_state
        )
        self.field_info = FieldInfo(
            self._field_data_service, _IsDataValid(self.scheme_eval)
        )
        self.field_data = FieldData(
            self._field_data_service,
            self.field_info,
            _IsDataValid(self.scheme_eval),
            self.scheme_eval,
        )
        self.field_data_streaming = FieldDataStreaming(
            self.fluent_connection._id, self._field_data_service
        )

        self.settings_service = self.fluent_connection.create_service(
            SettingsService, self.scheme_eval, self.error_state
        )

        self.health_check_service = fluent_connection.health_check_service
        self.connection_properties = fluent_connection.connection_properties

        self.fluent_connection.register_finalizer_cb(
            self.datamodel_service_se.unsubscribe_all_events
        )
        for obj in (
            self.datamodel_events,
            self.transcript,
            self.events_manager,
            self.monitors_manager,
        ):
            self.fluent_connection.register_finalizer_cb(obj.stop)

    @property
    def id(self) -> str:
        """Return the session id."""
        return self.fluent_connection._id

    def start_journal(self, file_path: str):
        """Executes tui command to start journal."""
        warnings.warn("Use -> journal.start()", DeprecationWarning)
        self.journal.start(file_path)

    def stop_journal(self):
        """Executes tui command to stop journal."""
        warnings.warn("Use -> journal.stop()", DeprecationWarning)
        self.journal.stop()

    @classmethod
    def create_from_server_info_file(
        cls, server_info_filepath: str, **connection_kwargs
    ):
        """Create a Session instance from server-info file.

        Parameters
        ----------
        server_info_filepath : str
            Path to server-info file written out by Fluent server
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
        ip, port, password = _parse_server_info_file(server_info_filepath)
        session = cls(
            fluent_connection=FluentConnection(
                ip=ip, port=port, password=password, **connection_kwargs
            )
        )
        return session

    def execute_tui(self, command: str) -> None:
        """Executes a tui command."""
        self.scheme_eval.scheme_eval(f'(tui-menu-execute {json.dumps(command)} "")')

    def get_fluent_version(self):
        """Gets and returns the fluent version."""
        return self.scheme_eval.version

    def exit(self, **kwargs) -> None:
        """Exit session."""
        logger.debug("session.exit() called")
        self.fluent_connection.exit(**kwargs)

    def force_exit(self) -> None:
        """Terminate session."""
        self.fluent_connection.force_exit()

    def force_exit_container(self) -> None:
        """Terminate Docker container session."""
        self.fluent_connection.force_exit_container()

    def __enter__(self):
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any):
        """Close the Fluent connection and exit Fluent."""
        logger.debug("session.__exit__() called")
        self.exit()

    def upload(self, file_path: str, remote_file_name: str = None):
        """Uploads a file on the server."""
        if not self._uploader:
            self._uploader = _Uploader(self.fluent_connection._remote_instance)
        return self._uploader.upload(file_path, remote_file_name)

    def download(self, file_name: str, local_file_path: str = None):
        """Downloads a file from the server."""
        if not self._uploader:
            self._uploader = _Uploader(self.fluent_connection._remote_instance)
        return self._uploader.download(file_name, local_file_path)


class _Uploader:
    """Instantiates a file uploader and downloader to have a seamless file
    reading / writing in the cloud particularly in Ansys lab . Here we are
    exposing upload and download methods on session objects. These would be no-
    ops if PyPIM is not configured or not authorized with the appropriate
    service. This will be used for internal purpose only.

    Attributes
    ----------
    pim_instance: PIM instance
        Instance of PIM which supports upload server services.

    file_service: Client instance
        Instance of Client which supports upload and download methods.

    Methods
    -------
    upload(
        file_path, remote_file_name
        )
        Upload a file to the server.

    download(
        file_name, local_file_path
        )
        Download a file from the server.
    """

    def __init__(self, pim_instance):
        self.pim_instance = pim_instance
        self.file_service = None
        try:
            upload_server = self.pim_instance.services["http-simple-upload-server"]
        except (AttributeError, KeyError):
            pass
        else:
            from simple_upload_server.client import Client

            self.file_service = Client(
                token="token", url=upload_server.uri, headers=upload_server.headers
            )

    def upload(self, file_path: str, remote_file_name: str = None):
        """Uploads a file on the server."""
        if self.file_service:
            expanded_file_path = os.path.expandvars(file_path)
            upload_file_name = remote_file_name or os.path.basename(expanded_file_path)
            self.file_service.upload_file(expanded_file_path, upload_file_name)

    def download(self, file_name: str, local_file_path: str = None):
        """Downloads a file from the server."""
        if self.file_service:
            if self.file_service.file_exist(file_name):
                self.file_service.download_file(file_name, local_file_path)
            else:
                raise FileNotFoundError("Remote file does not exist.")
