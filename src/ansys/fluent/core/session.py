"""Module containing class encapsulating Fluent connection and the Base Session."""
import importlib
import json
import logging
from typing import Any, Optional
import warnings

from ansys.fluent.core.fluent_connection import FluentConnection
from ansys.fluent.core.journaling import Journal
from ansys.fluent.core.services import service_creator
from ansys.fluent.core.services.batch_ops import BatchOpsService
from ansys.fluent.core.services.events import EventsService
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
from ansys.fluent.core.utils.file_transfer_service import PimFileTransferService
import ansys.platform.instancemanagement as pypim

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
            f"ansys.fluent.core.datamodel_{session.version}." + attribute
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

    _pim_methods = ["upload", "download"]

    def __init__(
        self,
        fluent_connection: FluentConnection,
        remote_file_handler: Optional[Any] = None,
    ):
        """BaseSession.

        Args:
            fluent_connection (:ref:`ref_fluent_connection`): Encapsulates a Fluent connection.
            remote_file_handler: Supports file upload and download.
        """
        BaseSession.build_from_fluent_connection(
            self, fluent_connection, remote_file_handler
        )

    def build_from_fluent_connection(
        self,
        fluent_connection: FluentConnection,
        remote_file_handler: Optional[Any] = None,
    ):
        """Build a BaseSession object from fluent_connection object."""
        self.fluent_connection = fluent_connection
        self._remote_file_handler = remote_file_handler
        self.error_state = self.fluent_connection.error_state
        self.scheme_eval = self.fluent_connection.scheme_eval
        self.rp_vars = RPVars(self.scheme_eval.string_eval)
        self._preferences = None
        self.journal = Journal(self.scheme_eval)

        self.transcript = self.fluent_connection.create_grpc_service(Transcript)
        if fluent_connection.start_transcript:
            self.transcript.start()

        self.datamodel_service_tui = service_creator("tui").create(
            fluent_connection._channel,
            fluent_connection._metadata,
            self.error_state,
            self.scheme_eval,
        )

        self.datamodel_service_se = service_creator("datamodel").create(
            fluent_connection._channel,
            fluent_connection._metadata,
            self.error_state,
        )

        self.datamodel_events = DatamodelEvents(self.datamodel_service_se)
        self.datamodel_events.start()

        self._batch_ops_service = self.fluent_connection.create_grpc_service(
            BatchOpsService
        )
        self.events_service = self.fluent_connection.create_grpc_service(EventsService)
        self.events_manager = EventsManager(
            self.events_service, self.error_state, self.fluent_connection._id
        )

        self._monitors_service = service_creator("monitors").create(
            fluent_connection._channel, fluent_connection._metadata, self.error_state
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

        self._field_data_service = self.fluent_connection.create_grpc_service(
            FieldDataService, self.error_state
        )
        self.field_info = service_creator("field_info").create(
            self._field_data_service, _IsDataValid(self.scheme_eval)
        )
        self.field_data = service_creator("field_data").create(
            self._field_data_service,
            self.field_info,
            _IsDataValid(self.scheme_eval),
            self.scheme_eval,
        )
        self.field_data_streaming = FieldDataStreaming(
            self.fluent_connection._id, self._field_data_service
        )

        self.settings_service = service_creator("settings").create(
            fluent_connection._channel,
            fluent_connection._metadata,
            self.scheme_eval,
            self.error_state,
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
        """Return the session ID."""
        return self.fluent_connection._id

    def start_journal(self, file_name: str):
        """Executes tui command to start journal."""
        warnings.warn("Use -> journal.start()", DeprecationWarning)
        self.journal.start(file_name)

    def stop_journal(self):
        """Executes tui command to stop journal."""
        warnings.warn("Use -> journal.stop()", DeprecationWarning)
        self.journal.stop()

    @classmethod
    def create_from_server_info_file(
        cls,
        server_info_file_name: str,
        remote_file_handler: Optional[Any] = None,
        **connection_kwargs,
    ):
        """Create a Session instance from server-info file.

        Parameters
        ----------
        server_info_file_name : str
            Path to server-info file written out by Fluent server
        remote_file_handler : Optional
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
            remote_file_handler=remote_file_handler,
        )
        return session

    def execute_tui(self, command: str) -> None:
        """Executes a tui command."""
        self.scheme_eval.scheme_eval(f"(ti-menu-load-string {json.dumps(command)})")

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

    def upload(self, file_name: str, remote_file_name: Optional[str] = None):
        """Upload a file to the server supported by `PyPIM<https://pypim.docs.pyansys.com/version/stable/>`.

        Parameters
        ----------
        file_name : str
            file name
        remote_file_name : str, optional
            remote file name, by default None
        """
        return PimFileTransferService(self.fluent_connection._remote_instance).upload(
            file_name, remote_file_name
        )

    def download(self, file_name: str, local_file_name: Optional[str] = "."):
        """Download a file from the server supported by `PyPIM<https://pypim.docs.pyansys.com/version/stable/>`.

        Parameters
        ----------
        file_name : str
            file name
        local_file_name : str, optional
            local file path, by default current directory
        """
        return PimFileTransferService(self.fluent_connection._remote_instance).download(
            file_name, local_file_name
        )

    def __dir__(self):
        returned_list = sorted(set(list(self.__dict__.keys()) + dir(type(self))))
        if not pypim.is_configured():
            for method in BaseSession._pim_methods:
                if method in returned_list:
                    returned_list.remove(method)
        return returned_list

    def __enter__(self):
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any):
        """Close the Fluent connection and exit Fluent."""
        logger.debug("session.__exit__() called")
        self.exit()
