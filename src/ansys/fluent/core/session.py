"""Module containing class encapsulating Fluent connection and the Base
Session."""
import importlib
import json
import os
from typing import Any
import warnings

import grpc

from ansys.fluent.core.fluent_connection import _FluentConnection
from ansys.fluent.core.services.datamodel_tui import TUIMenuGeneric
from ansys.fluent.core.session_base_meshing import _BaseMeshing
from ansys.fluent.core.session_shared import _CODEGEN_MSG_DATAMODEL, _CODEGEN_MSG_TUI
from ansys.fluent.core.solver.flobject import get_root as settings_get_root
from ansys.fluent.core.utils.fluent_version import get_version_for_filepath
from ansys.fluent.core.utils.logging import LOG

try:
    from ansys.fluent.core.solver.settings import root
except Exception:
    root = Any


def parse_server_info_file(filename: str):
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
    except (ImportError, ModuleNotFoundError):
        LOG.warning(_CODEGEN_MSG_DATAMODEL)


def _get_preferences(session):
    return _get_datamodel_attributes(session, "preferences")


def _get_solverworkflow(session):
    return _get_datamodel_attributes(session, "solverworkflow")


class _BaseSession:
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

    def __init__(self, fluent_connection: _FluentConnection):
        self.fluent_connection = fluent_connection
        self.scheme_eval = self.fluent_connection.scheme_eval
        self._uploader = None
        self._preferences = None
        self._solverworkflow = None

    @classmethod
    def create_from_server_info_file(
        cls,
        server_info_filepath: str,
        cleanup_on_exit: bool = True,
        start_transcript: bool = True,
    ):
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
        ip, port, password = parse_server_info_file(server_info_filepath)
        session = cls(
            fluent_connection=_FluentConnection(
                ip=ip,
                port=port,
                password=password,
                cleanup_on_exit=cleanup_on_exit,
                start_transcript=start_transcript,
            )
        )
        return session

    def execute_tui(self, command: str) -> None:
        """Executes a tui command."""
        self.fluent_connection.scheme_eval.scheme_eval(
            f'(tui-menu-execute {json.dumps(command)} "")'
        )

    def __enter__(self):
        """Close the Fluent connection and exit Fluent."""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any):
        self.fluent_connection.exit()

    def __getattr__(self, attr):
        return getattr(self.fluent_connection, attr)

    def __dir__(self):
        return sorted(
            set(
                list(self.__dict__.keys())
                + dir(type(self))
                + dir(self.fluent_connection)
            )
        )

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


class Session:
    """Instantiates a Fluent connection. This is a deprecated class. This has
    been replaced by the "_BaseSession" class to implement the new fluent
    launch modes.

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
    """

    def __init__(
        self,
        ip: str = None,
        port: int = None,
        password: str = None,
        channel: grpc.Channel = None,
        cleanup_on_exit: bool = True,
        start_transcript: bool = True,
        remote_instance=None,
        fluent_connection=None,
    ):
        warnings.warn("Please use the new fluent launch modes", DeprecationWarning)
        if not fluent_connection:
            self.fluent_connection = _FluentConnection(
                ip=ip,
                port=port,
                password=password,
                channel=channel,
                cleanup_on_exit=cleanup_on_exit,
                start_transcript=start_transcript,
                remote_instance=remote_instance,
            )
        else:
            self.fluent_connection = fluent_connection

        self.scheme_eval = self.fluent_connection.scheme_eval

        self.meshing = _BaseMeshing(None, self.fluent_connection)

        self._datamodel_service_se = self.fluent_connection.datamodel_service_se
        self._datamodel_service_tui = self.fluent_connection.datamodel_service_tui
        self._settings_service = self.fluent_connection.settings_service

        self.solver = Session.Solver(self.fluent_connection)

        self._uploader = None
        self._preferences = None
        self._solverworkflow = None

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
        ip, port, password = parse_server_info_file(server_info_filepath)
        session = Session(
            fluent_connection=_FluentConnection(
                ip=ip,
                port=port,
                password=password,
                cleanup_on_exit=cleanup_on_exit,
                start_transcript=start_transcript,
            )
        )
        return session

    def __enter__(self):
        """Close the Fluent connection and exit Fluent."""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any):
        self.fluent_connection.exit()

    def __getattr__(self, attr):
        return getattr(self.fluent_connection, attr)

    def __dir__(self):
        return sorted(
            set(
                list(self.__dict__.keys())
                + dir(type(self))
                + dir(self.fluent_connection)
            )
        )

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

    @property
    def preferences(self):
        """preferences datamodel root."""
        if self._preferences is None:
            self._preferences = _get_preferences(self)
        return self._preferences

    @property
    def solverworkflow(self):
        """solverworkflow datamodel root."""
        if self._solverworkflow is None:
            self._solverworkflow = _get_solverworkflow(self)
        return self._solverworkflow

    class Solver:
        def __init__(self, fluent_connection: _FluentConnection):
            self._fluent_connection = fluent_connection
            self._tui_service = fluent_connection.datamodel_service_tui
            self._settings_service = fluent_connection.settings_service
            self._tui = None
            self._settings_root = None
            self._version = None

        def get_fluent_version(self):
            """Gets and returns the fluent version."""
            return self._fluent_connection.get_fluent_version()

        @property
        def version(self):
            if self._version is None:
                self._version = get_version_for_filepath(session=self)
            return self._version

        @property
        def tui(self):
            """Instance of ``main_menu`` on which Fluent's SolverTUI methods
            can be executed."""
            if self._tui is None:
                try:
                    tui_module = importlib.import_module(
                        f"ansys.fluent.core.solver.tui_{self.version}"
                    )
                    self._tui = tui_module.main_menu([], self._tui_service)
                except (ImportError, ModuleNotFoundError):
                    LOG.warning(_CODEGEN_MSG_TUI)
                    self._tui = TUIMenuGeneric([], self._tui_service)
            return self._tui

        @property
        def root(self):
            """root settings object."""
            if self._settings_root is None:
                self._settings_root = settings_get_root(
                    flproxy=self._settings_service, version=self.version
                )
            return self._settings_root


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
