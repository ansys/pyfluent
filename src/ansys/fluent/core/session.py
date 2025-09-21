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

"""Module containing class encapsulating Fluent connection and the Base Session."""

from enum import Enum
import json
import logging
from typing import Any, Callable, Dict
import warnings
import weakref

from deprecated.sphinx import deprecated

from ansys.fluent.core.fluent_connection import FluentConnection
from ansys.fluent.core.journaling import Journal
from ansys.fluent.core.pyfluent_warnings import (
    PyFluentDeprecationWarning,
    PyFluentUserWarning,
)
from ansys.fluent.core.services import service_creator
from ansys.fluent.core.services.app_utilities import AppUtilitiesOld
from ansys.fluent.core.services.field_data import FieldDataService, ZoneInfo
from ansys.fluent.core.services.scheme_eval import SchemeEval
from ansys.fluent.core.streaming_services.datamodel_event_streaming import (
    DatamodelEvents,
)
from ansys.fluent.core.streaming_services.events_streaming import EventsManager
from ansys.fluent.core.streaming_services.transcript_streaming import Transcript
from ansys.fluent.core.utils.fluent_version import FluentVersion

from .rpvars import RPVars

try:
    from ansys.fluent.core.solver.settings import root
except Exception:
    root = Any

logger = logging.getLogger("pyfluent.general")


def _parse_server_info_file(file_name: str):
    with open(file_name, encoding="utf-8") as f:
        lines = f.readlines()
    ip_and_port = lines[0].strip().split(":")
    ip = ip_and_port[0]
    port = int(ip_and_port[1])
    password = lines[1].strip()
    return ip, port, password


class _IsDataValid:
    def __init__(self, scheme_eval):
        self._scheme_eval = scheme_eval

    def __bool__(self):
        return self()

    def __call__(self):
        return self._scheme_eval.scheme_eval("(data-valid?)")


class _AppUtilitiesFactory:
    """AppUtilities factory."""

    @staticmethod
    def _create_app_utilities(scheme_eval, fluent_connection):
        if FluentVersion(scheme_eval.version) < FluentVersion.v252:
            return AppUtilitiesOld(scheme_eval)
        else:
            return fluent_connection._connection_interface._app_utilities


class BaseSession:
    """Encapsulates a Fluent session.

    This class exposes methods for interacting with a Fluent session.

    Attributes
    ----------
    scheme: SchemeEval
        Instance of ``SchemeEval`` to execute Fluent's scheme code on.

    Methods
    -------
    _create_from_server_info_file(
        server_info_file_name, cleanup_on_exit, start_transcript
        )
        Create a Session instance from server-info file

    exit()
        Close the Fluent connection and exit Fluent.
    """

    # We are passing around an WeakMethod to avoid circular references
    def __init__(
        self,
        fluent_connection: FluentConnection,
        scheme_eval: SchemeEval,
        file_transfer_service: Any | None = None,
        start_transcript: bool = True,
        launcher_args: Dict[str, Any] | None = None,
        event_type: Enum | None = None,
        get_zones_info: weakref.WeakMethod[Callable[[], list[ZoneInfo]]] | None = None,
    ):
        """BaseSession.

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
        event_type : Enum, optional
            Event enumeration specific to the session type.
        """
        self._start_transcript = start_transcript
        self._launcher_args = launcher_args
        BaseSession._build_from_fluent_connection(
            self,
            fluent_connection,
            scheme_eval,
            file_transfer_service,
            event_type,
            get_zones_info,
            launcher_args,
        )
        self.register_finalizer_callback = fluent_connection.register_finalizer_cb

    def _build_from_fluent_connection(
        self,
        fluent_connection: FluentConnection,
        scheme_eval: SchemeEval,
        file_transfer_service: Any | None = None,
        event_type=None,
        get_zones_info: weakref.WeakMethod[Callable[[], list[ZoneInfo]]] | None = None,
        launcher_args: Dict[str, Any] | None = None,
    ):
        """Build a BaseSession object from fluent_connection object."""
        self._fluent_connection = fluent_connection
        # Stores the backup of the fluent connection for later reference.
        self._fluent_connection_backup = self._fluent_connection
        self._file_transfer_service = file_transfer_service
        self._launcher_args = launcher_args
        self._error_state = fluent_connection._error_state
        self.scheme = scheme_eval
        self.rp_vars = RPVars(self.scheme.string_eval)
        self._preferences = None

        self._transcript_service = service_creator("transcript").create(
            fluent_connection._channel, fluent_connection._metadata
        )
        self.transcript = Transcript(self._transcript_service)
        if self._start_transcript:
            self.transcript.start()

        self._app_utilities = _AppUtilitiesFactory._create_app_utilities(
            self.scheme, self._fluent_connection
        )

        self.journal = Journal(self._app_utilities)

        self._datamodel_service_tui = service_creator("tui").create(
            fluent_connection._channel,
            fluent_connection._metadata,
            self._error_state,
            self._app_utilities,
            self.scheme,
        )

        self._datamodel_service_se = service_creator("datamodel").create(
            fluent_connection._channel,
            fluent_connection._metadata,
            self.get_fluent_version(),
            self._error_state,
            self._file_transfer_service,
        )

        self._datamodel_events = DatamodelEvents(self._datamodel_service_se)
        self._datamodel_events.start()

        self._batch_ops_service = service_creator("batch_ops").create(
            fluent_connection._channel, fluent_connection._metadata
        )

        if event_type:
            events_service = service_creator("events").create(
                fluent_connection._channel, fluent_connection._metadata
            )
            self.events = EventsManager[event_type](
                event_type, events_service, self._error_state, weakref.proxy(self)
            )
            self.events.start()
        else:
            self.events = None

        self._field_data_service = self._fluent_connection.create_grpc_service(
            FieldDataService, self._error_state
        )

        self.fields = Fields(self, get_zones_info)

        self._settings_service = service_creator("settings").create(
            fluent_connection._channel,
            fluent_connection._metadata,
            self._app_utilities,
            self.scheme,
            self._error_state,
        )

        self._health_check = fluent_connection._health_check
        self.connection_properties = fluent_connection.connection_properties

        self._fluent_connection.register_finalizer_cb(
            self._datamodel_service_se.unsubscribe_all_events
        )
        for obj in filter(None, (self._datamodel_events, self.transcript, self.events)):
            self._fluent_connection.register_finalizer_cb(obj.stop)

    def is_server_healthy(self) -> bool:
        """Whether the current session is healthy (i.e. The server is 'SERVING')."""
        return self._health_check.is_serving

    def is_active(self) -> bool:
        """Whether the current session is active."""
        return True if self._fluent_connection else False

    @property
    @deprecated(version="0.32", reason="Use ``session.scheme``.")
    def scheme_eval(self):
        """Provides access to Fluent field information."""
        return self.scheme

    @property
    @deprecated(version="0.32", reason="Use ``session.is_server_healthy``.")
    def health_check(self):
        """Provides access to Health Check service."""
        return self._health_check

    @property
    @deprecated(version="0.20.dev9", reason="Use ``session.fields.field_info``.")
    def field_info(self):
        """Provides access to Fluent field information."""
        return self.fields.field_info

    @property
    @deprecated(version="0.20.dev9", reason="Use ``session.fields.field_data``.")
    def field_data(self):
        """Fluent field data on surfaces."""
        return self.fields.field_data

    @property
    @deprecated(
        version="0.20.dev9", reason="Use ``session.fields.field_data_streaming``."
    )
    def field_data_streaming(self):
        """Field gRPC streaming service of Fluent."""
        return self.fields.field_data_streaming

    @property
    def id(self) -> str:
        """Return the session ID."""
        return self._fluent_connection._id

    def start_journal(self, file_name: str):
        """Executes tui command to start journal."""
        warnings.warn("Use -> journal.start()", PyFluentDeprecationWarning)
        self.journal.start(file_name)

    def stop_journal(self):
        """Executes tui command to stop journal."""
        warnings.warn("Use -> journal.stop()", PyFluentDeprecationWarning)
        self.journal.stop()

    @classmethod
    def _create_from_server_info_file(
        cls,
        server_info_file_name: str,
        file_transfer_service: Any | None = None,
        start_transcript: bool = True,
        launcher_args: Dict[str, Any] | None = None,
        **connection_kwargs,
    ):
        """Create a Session instance from server-info file.

        Parameters
        ----------
        server_info_file_name : str
            Path to server-info file written out by Fluent server
        file_transfer_service : Optional
            Support file upload and download.
        start_transcript : bool, optional
            Whether to start the Fluent transcript in the client.
            The default is ``True``, in which case the Fluent
            transcript can be subsequently started and stopped
            using method calls on the ``Session`` object.
        **connection_kwargs : dict, optional
            Additional keyword arguments may be specified, and they will be passed to the `FluentConnection`
            being initialized. For example, ``cleanup_on_exit = True``.
            See :func:`FluentConnection initialization <ansys.fluent.core.fluent_connection.FluentConnection.__init__>`
            for more details and possible arguments.

        Returns
        -------
        Session
            Session instance
        """
        ip, port, password = _parse_server_info_file(server_info_file_name)
        fluent_connection = FluentConnection(
            ip=ip,
            port=port,
            password=password,
            file_transfer_service=file_transfer_service,
            **connection_kwargs,
        )
        session = cls(
            fluent_connection=fluent_connection,
            scheme_eval=fluent_connection._connection_interface.scheme_eval,
            file_transfer_service=file_transfer_service,
            start_transcript=start_transcript,
            launcher_args=launcher_args,
        )
        return session

    def execute_tui(self, command: str) -> None:
        """Executes a tui command."""
        self.scheme.eval(f"(ti-menu-load-string {json.dumps(command)})")

    def get_fluent_version(self) -> FluentVersion:
        """Gets and returns the fluent version."""
        return FluentVersion(self.scheme.version)

    def _exit_compose_service(self):
        args = self._launcher_args or {}
        compose_config = args.get("compose_config", None)

        container = self._fluent_connection._container
        if compose_config and compose_config.is_compose:
            container.stop()

    def wait_process_finished(self, wait: float | int | bool = 60):
        """Returns ``True`` if local Fluent processes have finished, ``False`` if they
        are still running when wait limit (default 60 seconds) is reached. Immediately
        cancels and returns ``None`` if ``wait`` is set to ``False``.

        Parameters
        ----------
        wait : float, int or bool, optional
            How long to wait for processes to finish before returning, by default 60 seconds.
            Can also be set to ``True``, which will result in waiting indefinitely.

        Raises
        ------
        UnsupportedRemoteFluentInstance
            If current Fluent instance is running remotely.
        WaitTypeError
            If ``wait`` is specified improperly.
        """
        return self._fluent_connection_backup.wait_process_finished()

    def exit(self, **kwargs) -> None:
        """Exit session."""
        logger.debug("session.exit() called")
        if self._fluent_connection:
            self._exit_compose_service()
            self._fluent_connection.exit(**kwargs)
            self._fluent_connection = None

    def force_exit(self) -> None:
        """Forces the Fluent session to exit, losing unsaved progress and data."""
        self._exit_compose_service()
        self._fluent_connection.force_exit()

    def file_exists_on_remote(self, file_name: str) -> bool:
        """Check if remote file exists.

        Parameters
        ----------
        file_name: str
            File name.

        Returns
        -------
            Whether file exists.
        """
        if self._file_transfer_service:
            return self._file_transfer_service.file_exists_on_remote(file_name)

    def _file_transfer_api_warning(self, method_name: str) -> str:
        """User warning for upload/download methods."""
        return f"You have directly called the {method_name} method of the session. \
        Please be advised that for the current version of Fluent, many API methods \
        automatically handle file uploads and downloads internally. You may not \
        need to explicitly call {method_name} in most cases. \
        However, there are exceptions, particularly in PMFileManagement, where complex \
        file interactions require explicit use of {method_name}  method \
        for relevant files."

    def upload(self, file_name: list[str] | str, remote_file_name: str | None = None):
        """Upload a file to the server.

        Parameters
        ----------
        file_name : str
            Name of the local file to upload to the server.
        remote_file_name : str, optional
            remote file name, by default None
        """
        warnings.warn(self._file_transfer_api_warning("upload()"), PyFluentUserWarning)
        if self._file_transfer_service:
            return self._file_transfer_service.upload(file_name, remote_file_name)

    def download(self, file_name: str, local_directory: str | None = None):
        """Download a file from the server.

        Parameters
        ----------
        file_name : str
            Name of the file to download from the server.
        local_directory : str, optional
            Local destination directory. The default is the current working directory.
        """
        warnings.warn(
            self._file_transfer_api_warning("download()"), PyFluentUserWarning
        )
        if self._file_transfer_service:
            return self._file_transfer_service.download(file_name, local_directory)

    def chdir(self, path: str) -> None:
        """Change Fluent working directory.

        Parameters
        ----------
        path : str
            Path of the directory to change.
        """
        self._app_utilities.set_working_directory(path)

    def __enter__(self):
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any):
        """Close the Fluent connection and exit Fluent."""
        logger.debug("session.__exit__() called")
        self.exit()

    def __dir__(self):
        if self._fluent_connection is None:
            return ["is_active"]
        dir_list = set(list(self.__dict__.keys()) + dir(type(self))) - {
            "field_data",
            "field_info",
            "field_data_streaming",
            "start_journal",
            "stop_journal",
            "scheme_eval",
        }
        return sorted(dir_list)

    def enable_beta_features(self):
        """Enable access to Fluent beta-features"""
        self._app_utilities.enable_beta()

    @property
    def _is_beta_enabled(self):
        return self._app_utilities.is_beta_enabled()


class Fields:
    """Container for field and solution variables."""

    def __init__(
        self,
        _session: BaseSession,
        get_zones_info: weakref.WeakMethod[Callable[[], list[ZoneInfo]]] | None = None,
    ):
        """Initialize Fields."""
        self._is_solution_data_valid = (
            _session._app_utilities.is_solution_data_available
        )
        self._field_info = service_creator("field_info").create(
            _session._field_data_service,
            self._is_solution_data_valid,
        )
        self.field_data = service_creator("field_data").create(
            _session._field_data_service,
            self.field_info,
            self._is_solution_data_valid,
            _session.scheme,
            get_zones_info,
        )
        self.field_data_streaming = service_creator("field_data_streaming").create(
            _session._fluent_connection._id, _session._field_data_service
        )
        self.field_data_old = service_creator("field_data_old").create(
            _session._field_data_service,
            self.field_info,
            self._is_solution_data_valid,
            _session.scheme,
        )

    @property
    @deprecated(version="0.34.0", reason="Use relevant ``field_data`` methods..")
    def field_info(self):
        """Field Information."""
        return self._field_info
