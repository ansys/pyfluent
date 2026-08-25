# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
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

"""Internal base class for all Fluent sessions.

This module is private.  Do not import from it directly; use the concrete
session classes exposed by :mod:`ansys.fluent.core.session`.
"""

from collections.abc import Callable
from enum import Enum
from functools import cached_property
import json
import logging
import os
from typing import TYPE_CHECKING, Any, Literal, overload
import warnings
import weakref

from deprecated.sphinx import deprecated
from typing_extensions import Unpack

from ansys.fluent.core._types import PathType
from ansys.fluent.core.fields.live_field_data import LiveFieldData, ZoneInfo, _FieldInfo
from ansys.fluent.core.launcher.launch_options import FluentMode

if TYPE_CHECKING:
    from ansys.fluent.core.launcher.standalone_launcher import (
        StandaloneArgsWithoutDryRunMode,
    )
    from ansys.fluent.core.launcher.container_launcher import (
        ContainerArgsWithoutDryRunMode,
    )
    from ansys.fluent.core.launcher.pim_launcher import PIMArgsWithoutMode

from ansys.fluent.core.fluent_connection import FluentConnection
from ansys.fluent.core.journaling import Journal
from ansys.fluent.core.pyfluent_warnings import (
    PyFluentDeprecationWarning,
    PyFluentUserWarning,
)
from ansys.fluent.core.rpvars import RPVars
from ansys.fluent.core.services.scheme_interpreter import SchemeInterpreter
from ansys.fluent.core.utils.deprecate import deprecate_function
from ansys.fluent.core.utils.fluent_version import FluentVersion

try:
    from ansys.fluent.core.solver.settings import root
except Exception:
    root = Any

logger = logging.getLogger("pyfluent.general")


__all__ = ("BaseSession",)


def _parse_server_info_file(file_name: str):
    """Parse server info file.
    Returns (ip, port, password) or (unix_socket, password)"""
    with open(file_name, encoding="utf-8") as f:
        lines = f.readlines()
    address = lines[0].strip()
    password = lines[1].strip()
    if address.startswith("unix:"):
        return address, password
    else:
        ip_and_port = address.split(":")
        ip = ip_and_port[0]
        port = int(ip_and_port[1])
        return ip, port, password


class BaseSession:
    """Encapsulates a Fluent session.

    This class exposes methods for interacting with a Fluent session.

    Attributes
    ----------
    scheme: SchemeInterpreter
        Instance of ``SchemeInterpreter`` to execute Fluent's scheme code on.

    Methods
    -------
    _create_from_server_info_file(
        server_info_file_name, cleanup_on_exit, start_transcript
        )
        Create a Session instance from server-info file

    exit()
        Close the Fluent connection and exit Fluent.
    """

    @classmethod
    def _validate_mode_not_in_kwargs(
        cls, kwargs: dict[str, Any], method_name: str
    ) -> None:
        """Validate that 'mode' is not in kwargs.

        Parameters
        ----------
        kwargs : dict[str, Any]
            Keyword arguments to validate
        method_name : str
            Name of calling method (e.g., 'from_install')

        Raises
        ------
        ValueError
            If 'mode' is present in kwargs
        """
        if "mode" in kwargs:
            raise ValueError(
                f"Cannot specify 'mode' in {cls.__name__}.{method_name}(). "
                "The mode is determined by the session class. "
                f"You are already using {cls.__name__}, which sets mode to {FluentMode.from_session_class(cls)}."
            )

    def __new__(cls, *args, **kwargs):
        if cls is BaseSession:
            raise TypeError(
                "BaseSession cannot be instantiated directly. "
                "Use Solver, SolverAero, SolverIcing, SolverLite, Meshing, or PureMeshing."
            )
        return super().__new__(cls)

    @classmethod
    def _create_instance(cls, *args, **kwargs):
        """Private factory bypassing the direct-instantiation guard."""
        instance = object.__new__(cls)
        instance.__init__(*args, **kwargs)
        return instance

    # We are passing around an WeakMethod to avoid circular references
    def __init__(
        self,
        fluent_connection: FluentConnection,
        scheme_eval: SchemeInterpreter,
        file_transfer_service: Any | None = None,
        start_transcript: bool = True,
        launcher_args: dict[str, Any] | None = None,
        event_type: Enum | None = None,
        get_zones_info: weakref.WeakMethod[Callable[[], list[ZoneInfo]]] | None = None,
    ):
        """BaseSession.

        Parameters
        ----------
        fluent_connection (:ref:`ref_fluent_connection`):
            Encapsulates a Fluent connection.
        scheme_eval: SchemeInterpreter
            Instance of ``SchemeInterpreter`` to execute Fluent's scheme code on.
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

    _inactive_session_allow_list = [
        "is_active",
        "_fluent_connection",
        "_fluent_connection_backup",
        "wait_process_finished",
        # `_exit` is kept accessible even for inactive sessions to allow callers
        # to trigger a clean shutdown/teardown on sessions that are no longer active.
        "_exit",
    ]

    def _build_from_fluent_connection(
        self,
        fluent_connection: FluentConnection,
        scheme_eval: SchemeInterpreter,
        file_transfer_service: Any | None = None,
        event_type=None,
        get_zones_info: weakref.WeakMethod[Callable[[], list[ZoneInfo]]] | None = None,
        launcher_args: dict[str, Any] | None = None,
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

        self.transcript = fluent_connection._service_factory.transcript_streaming
        if self._start_transcript:
            self.transcript.start()

        self.application_runtime = self._fluent_connection.application_runtime

        self.journal = Journal(self.application_runtime)

        self._datamodel_service_tui = fluent_connection._service_factory.text_interface

        self._datamodel_service_se = fluent_connection._service_factory.object_model
        self._datamodel_service_se.file_transfer_service = file_transfer_service

        self._datamodel_events = (
            fluent_connection._service_factory.object_model_events_streaming
        )
        self._datamodel_events.start()

        if event_type:
            self.events = fluent_connection._service_factory._get_events_manager(
                event_type=event_type,
                session_ref=weakref.proxy(self),
            )
            self.events.start()
        else:
            self.events = None

        self.fields = Fields(
            _session=self,
            get_zones_info=get_zones_info,
            fluent_connection=fluent_connection,
        )

        self._settings_service = fluent_connection._service_factory.settings

        self._health_check = fluent_connection._health_check
        self.connection_properties = fluent_connection.connection_properties

        self._fluent_connection.register_finalizer_cb(
            self._datamodel_service_se.unsubscribe_all_events
        )
        self._fluent_connection.register_finalizer_cb(
            self._datamodel_service_se.delete_all_command_arguments
        )
        for obj in filter(None, (self._datamodel_events, self.transcript, self.events)):
            self._fluent_connection.register_finalizer_cb(obj.stop)

    @cached_property
    def _batch_ops_service(self):
        """gRPC service for batch operations (loaded on first use)."""
        return self._fluent_connection._service_factory.batch_ops

    @deprecate_function(version="v0.38.0", new_func="is_active")
    def is_server_healthy(self) -> bool:
        """Whether the current session is healthy (i.e. the server is 'SERVING')."""
        return self._is_server_healthy()

    def _is_server_healthy(self) -> bool:
        """Whether the current session is healthy (i.e. the server is 'SERVING')."""
        return self._health_check.is_serving

    def is_active(self) -> bool:
        """Whether the current session is active."""
        return self._fluent_connection is not None and self._is_server_healthy()

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
        launcher_args: dict[str, Any] | None = None,
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
        values = _parse_server_info_file(server_info_file_name)
        if len(values) == 2:
            address, password = values
            ip, port = None, None
        else:
            ip, port, password = values
            address = None
        fluent_connection = FluentConnection(
            ip=ip,
            port=port,
            password=password,
            address=address,
            file_transfer_service=file_transfer_service,
            **connection_kwargs,
        )
        session = cls(
            fluent_connection=fluent_connection,
            scheme_eval=fluent_connection.scheme_eval,
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

    def wait_process_finished(self, wait: float | int | bool = 100):
        """Returns ``True`` if local Fluent processes have finished, ``False`` if they
        are still running when wait limit (default 100 seconds) is reached. Immediately
        cancels and returns ``None`` if ``wait`` is set to ``False``.

        Parameters
        ----------
        wait : float, int or bool, optional
            How long to wait for processes to finish before returning, by default 100 seconds.
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
        """Exit session.

        This public method is a convenience wrapper that delegates directly to
        :meth:`_exit`.
        """
        logger.debug("session.exit() called")
        self._exit(**kwargs)

    def _exit(self, **kwargs) -> None:
        """Exit session."""
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
        if self._file_transfer_service:
            warnings.warn(
                self._file_transfer_api_warning("upload()"), PyFluentUserWarning
            )
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
        if self._file_transfer_service:
            warnings.warn(
                self._file_transfer_api_warning("download()"), PyFluentUserWarning
            )
            return self._file_transfer_service.download(file_name, local_directory)

    def chdir(self, path: PathType) -> None:
        """Change Fluent working directory.

        Parameters
        ----------
        path : os.PathLike[str | bytes] | str | bytes
            Path of the directory to change.
        """
        self.application_runtime.set_working_directory(os.fspath(path))

    def __enter__(self):
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any):
        """Close the Fluent connection and exit Fluent."""
        logger.debug("session.__exit__() called")
        self._exit()

    def __dir__(self):
        if self._fluent_connection is None:
            names = super().__dir__()
            return [
                name
                for name in names
                if (name.startswith("__") and name.endswith("__"))
                or name in {"is_active", "wait_process_finished"}
            ]
        dir_list = set(list(self.__dict__.keys()) + dir(type(self))) - {
            "start_journal",
            "stop_journal",
            "scheme_eval",
        }
        return sorted(dir_list)

    def enable_beta_features(self):
        """Enable access to Fluent beta-features"""
        self.application_runtime.enable_beta()

    @property
    def _is_beta_enabled(self):
        return self.application_runtime.is_beta_enabled()

    @overload
    @classmethod
    def from_install(
        cls,
        *,
        dry_run: Literal[False] = False,
        **kwargs: Unpack["StandaloneArgsWithoutDryRunMode"],
    ) -> "BaseSession": ...

    @overload
    @classmethod
    def from_install(
        cls,
        *,
        dry_run: Literal[True],
        **kwargs: Unpack["StandaloneArgsWithoutDryRunMode"],
    ) -> tuple[str, str]: ...

    @classmethod
    def from_install(  # pylint: disable=missing-param-doc
        cls,
        *,
        dry_run: bool = False,
        **kwargs: Unpack["StandaloneArgsWithoutDryRunMode"],
    ) -> "BaseSession | tuple[str, str]":
        """
        Launch a Fluent session in standalone mode.

        Parameters
        ----------
        ui_mode : UIMode or str, optional
            Defines the user interface mode for Fluent. Accepts either a ``UIMode`` value
            or a corresponding string such as ``"no_gui"``, ``"hidden_gui"``, or ``"gui"``.
        graphics_driver : FluentWindowsGraphicsDriver or FluentLinuxGraphicsDriver
            Specifies the graphics driver for Fluent. Options are from the ``FluentWindowsGraphicsDriver`` enum
            (for Windows) or the ``FluentLinuxGraphicsDriver`` enum (for Linux).
        product_version : FluentVersion or str or float or int, optional
            Indicates the version of Ansys Fluent to launch. For example, to use version 2025 R1, pass
            ``FluentVersion.v251``, ``"25.1.0"``, ``"25.1"``, ``25.1``, or ``251``. Defaults to ``None``,
            which uses the newest installed version.
        dimension : Dimension or int, optional
            Specifies the geometric dimensionality of the Fluent simulation. Defaults to ``None``,
            which corresponds to ``Dimension.THREE``. Acceptable values are from the ``Dimension`` enum
            (``Dimension.TWO`` or ``Dimension.THREE``) or integers ``2`` and ``3``.
        precision : Precision or str, optional
            Defines the floating point precision. Defaults to ``None``, which corresponds to
            ``Precision.DOUBLE``. Acceptable values are from the ``Precision`` enum (``Precision.SINGLE``
            or ``Precision.DOUBLE``) or strings ``"single"`` and ``"double"``.
        processor_count : int, optional
            Specifies the number of processors to use. Defaults to ``None``, which uses 1 processor.
            In job scheduler environments, this value limits the total number of allocated cores.
        journal_file_names : str or list of str, optional
            Path(s) to a Fluent journal file(s) that Fluent will execute. Defaults to ``None``.
        start_timeout : int, optional
            Maximum time in seconds allowed for connecting to the Fluent server. Defaults to 100 seconds.
        additional_arguments : str, optional
            Additional command-line arguments for Fluent, formatted as they would be on the command line.
        env : dict[str, str], optional
            A mapping for modifying environment variables in Fluent. Defaults to ``None``.
        cleanup_on_exit : bool, optional
            Determines whether to shut down the connected Fluent session when exiting PyFluent or calling
            the session's `exit()` method. Defaults to True.
        dry_run : bool, optional
            If True, does not launch Fluent but prints configuration information instead. The `call()` method
            returns a tuple containing the launch string and server info file name. Defaults to False.
        start_transcript : bool, optional
            Indicates whether to start streaming the Fluent transcript in the client. Defaults to True;
            streaming can be controlled via `transcript.start()` and `transcript.stop()` methods on the session object.
        case_file_name : :class:`os.PathLike` or str, optional
            Name of the case file to read into the Fluent session. Defaults to None.
        case_data_file_name : :class:`os.PathLike` or str, optional
            Name of the case data file. If both case and data files are provided, they are read into the session.
        lightweight_mode : bool, optional
            If True, runs in lightweight mode where mesh settings are read into a background solver session,
            replacing it once complete. This parameter is only applicable when `case_file_name` is provided; defaults to False.
        py : bool, optional
            If True, runs Fluent in Python mode. Defaults to None.
        gpu : bool, optional
            If True, starts Fluent with GPU Solver enabled.
        cwd : :class:`os.PathLike` or str, optional
            Working directory for the Fluent client.
        fluent_path: :class:`os.PathLike` or str, optional
            User-specified path for Fluent installation.
        topy :  bool or str, optional
            A flag indicating whether to write equivalent Python journals from provided journal files; can also specify
            a filename for the new Python journal.
        start_watchdog : bool, optional
            When `cleanup_on_exit` is True, defaults to True; an independent watchdog process ensures that any local
            GUI-less Fluent sessions started by PyFluent are properly closed when the current Python process ends.
        file_transfer_service : Any
            Service for uploading/downloading files to/from the server.

        Raises
        ------
        UnexpectedKeywordArgument
            If an unexpected keyword argument is provided.

        ValueError
            If 'mode' is passed in kwargs along with container parameter.

        Notes
        -----
        In job scheduler environments (e.g., SLURM, LSF, PBS), resources and compute nodes are allocated,
        and core counts are queried from these environments before being passed to Fluent.
        """
        cls._validate_mode_not_in_kwargs(kwargs, "from_install")
        from ansys.fluent.core.launcher.standalone_launcher import StandaloneLauncher

        launcher = StandaloneLauncher(
            **kwargs, dry_run=dry_run, mode=FluentMode.from_session_class(cls)
        )
        return launcher()

    @overload
    @classmethod
    def from_container(
        cls,
        *,
        dry_run: Literal[False] = False,
        **kwargs: Unpack["ContainerArgsWithoutDryRunMode"],
    ) -> "BaseSession": ...

    @overload
    @classmethod
    def from_container(
        cls,
        *,
        dry_run: Literal[True],
        **kwargs: Unpack["ContainerArgsWithoutDryRunMode"],
    ) -> dict[str, Any]: ...

    @classmethod
    def from_container(  # pylint: disable=missing-param-doc
        cls,
        *,
        dry_run: bool = False,
        **kwargs: Unpack["ContainerArgsWithoutDryRunMode"],
    ) -> "BaseSession | dict[str, Any]":
        """
        Launch a Fluent session in container mode.

        Parameters
        ----------
        ui_mode : UIMode or str, optional
            Defines the user interface mode for Fluent. Accepts either a ``UIMode`` value
            or a corresponding string such as ``"no_gui"``, ``"hidden_gui"``, or ``"gui"``.
        graphics_driver : FluentWindowsGraphicsDriver or FluentLinuxGraphicsDriver
            Specifies the graphics driver for Fluent. Options are from the ``FluentWindowsGraphicsDriver`` enum
            (for Windows) or the ``FluentLinuxGraphicsDriver`` enum (for Linux).
        product_version :  FluentVersion or str or float or int, optional
            Indicates the version of Ansys Fluent to launch. For example, to use version 2025 R1, pass
            any of ``FluentVersion.v251``, ``"25.1.0"``, ``"25.1"``, ``25.1``, or ``251``. Defaults to ``None``,
            which uses the newest installed version.
        dimension : Dimension or int, optional
            Specifies the geometric dimensionality of the Fluent simulation. Defaults to ``None``,
            which corresponds to ``Dimension.THREE``. Acceptable values include ``Dimension.TWO``,
            ``Dimension.THREE``, or integers ``2`` and ``3``.
        precision : Precision or str, optional
            Defines the floating point precision. Defaults to ``None``, which corresponds to
            ``Precision.DOUBLE``. Acceptable values include ``Precision.SINGLE``,
            ``Precision.DOUBLE``, or strings ``"single"`` and ``"double"``.
        processor_count : int, optional
            Specifies the number of processors to use. Defaults to ``None``, which uses 1 processor.
            In job scheduler environments, this value limits the total number of allocated cores.
        start_timeout : int, optional
            Maximum allowable time in seconds for connecting to the Fluent server. Defaults to 100 seconds.
        additional_arguments : str, optional
            Additional command-line arguments for Fluent, formatted as they would be on the command line.
        container_dict : dict, optional
            Configuration dictionary for launching Fluent inside a Docker container. See also
            :mod:`~ansys.fluent.core.launcher.fluent_container`.
        dry_run : bool, optional
            If True, does not launch Fluent but prints configuration information instead. If dry running a
            container start, this method will return the configured ``container_dict``. Defaults to False.
        cleanup_on_exit : bool
            Determines whether to shut down the connected Fluent session upon exit or when calling
            the session's `exit()` method. Defaults to True.
        start_transcript : bool
            Indicates whether to start streaming the Fluent transcript in the client. Defaults to True;
            streaming can be controlled via `transcript.start()` and `transcript.stop()` methods on the session object.
        py : bool, optional
            If True, runs Fluent in Python mode. Defaults to None.
        gpu : bool, optional
            If True, starts Fluent with GPU Solver enabled.
        start_watchdog : bool, optional
            If True and `cleanup_on_exit` is True, an independent watchdog process is run to ensure that any local
            GUI-less Fluent sessions started by PyFluent are properly closed when the current Python process ends.
        file_transfer_service : Any, optional
            Service for uploading/downloading files to/from the server.
        use_docker_compose: bool
            Whether to use Docker Compose to launch Fluent.
        use_podman_compose: bool
            Whether to use Podman Compose to launch Fluent.
        certificates_folder : str, optional
            Path to the folder containing TLS certificates for Fluent's gRPC server.
        insecure_mode : bool, optional
            If True, Fluent's gRPC server will be started in insecure mode without TLS.
            This mode is not recommended. For more details on the implications
            and usage of insecure mode, refer to the Fluent documentation.

        Returns
        -------
        Meshing | PureMeshing | Solver | SolverIcing | dict
            Session object or configuration dictionary if ``dry_run`` is True.

        Raises
        ------
        UnexpectedKeywordArgument
            If an unexpected keyword argument is provided.

        ValueError
            If 'mode' is passed in kwargs.

        Notes
        -----
        In job scheduler environments (e.g., SLURM, LSF, PBS), resources and compute nodes are allocated,
        and core counts are queried from these environments before being passed to Fluent.
        """
        cls._validate_mode_not_in_kwargs(kwargs, "from_container")
        from ansys.fluent.core.launcher.container_launcher import DockerLauncher

        launcher = DockerLauncher(
            **kwargs, dry_run=dry_run, mode=FluentMode.from_session_class(cls)
        )
        return launcher()

    @classmethod
    def from_pim(  # pylint: disable=missing-param-doc
        cls,
        **kwargs: Unpack["PIMArgsWithoutMode"],
    ) -> "BaseSession":
        """
        Launch a Fluent session in `PIM <https://pypim.docs.pyansys.com/version/stable/>`_ mode.

        Parameters
        ----------
        ui_mode : UIMode or str, optional
            Defines the user interface mode for Fluent. Accepts either a ``UIMode`` value
            or a corresponding string such as ``"no_gui"``, ``"hidden_gui"``, or ``"gui"``.
        graphics_driver : FluentWindowsGraphicsDriver or FluentLinuxGraphicsDriver
            Specifies the graphics driver for Fluent. Options are from the ``FluentWindowsGraphicsDriver`` enum
            (for Windows) or the ``FluentLinuxGraphicsDriver`` enum (for Linux).
        product_version : FluentVersion or str or float or int, optional
            Indicates the version of Ansys Fluent to launch. For example, to use version 2025 R1, pass
            any of ``FluentVersion.v251``, ``"25.1.0"``, ``"25.1"``, ``25.1``, or ``251``. Defaults to ``None``,
            which uses the newest installed version.
        dimension : Dimension or int, optional
            Specifies the geometric dimensionality of the Fluent simulation. Defaults to ``None``,
            which corresponds to ``Dimension.THREE``. Acceptable values include ``Dimension.TWO``,
            ``Dimension.THREE``, or integers ``2`` and ``3``.
        precision : Precision or str, optional
            Defines the floating point precision. Defaults to ``None``, which corresponds to
            ``Precision.DOUBLE``. Acceptable values include ``Precision.SINGLE``,
            ``Precision.DOUBLE``, or strings ``"single"`` and ``"double"``.
        processor_count : int, optional
            Specifies the number of processors to use. Defaults to ``None``, which uses 1 processor.
            In job scheduler environments, this value limits the total number of allocated cores.
        start_timeout : int, optional
            Maximum allowable time in seconds for connecting to the Fluent server. Defaults to 100 seconds.
        additional_arguments : str, optional
            Additional command-line arguments for Fluent, formatted as they would be on the command line.
        cleanup_on_exit : bool
            Determines whether to shut down the connected Fluent session upon exit or when calling
            the session's `exit()` method. Defaults to True.
        dry_run : bool, optional
            If True, does not launch Fluent but prints configuration information instead. If dry running a
            PIM start, this method will return a configuration dictionary. Defaults to False.
        start_transcript : bool
            Indicates whether to start streaming the Fluent transcript in the client. Defaults to True;
            streaming can be controlled via `transcript.start()` and `transcript.stop()` methods on the session object.
        gpu : bool, optional
            If True, starts Fluent with GPU Solver enabled.
        start_watchdog : bool, optional
            If True and `cleanup_on_exit` is True, an independent watchdog process is run to ensure that any local
            GUI-less Fluent sessions started by PyFluent are properly closed when the current Python process ends.
        file_transfer_service : Any, optional
            Service for uploading/downloading files to/from the server.

        Returns
        -------
        Union[Meshing, PureMeshing, Solver, SolverIcing, dict]
            Session object or configuration dictionary if ``dry_run`` is True.

        Raises
        ------
        UnexpectedKeywordArgument
            If an unexpected keyword argument is provided.

        Notes
        -----
        In job scheduler environments (e.g., SLURM, LSF, PBS), resources and compute nodes are allocated,
        and core counts are queried from these environments before being passed to Fluent.
        """
        from ansys.fluent.core.launcher.pim_launcher import PIMLauncher

        launcher = PIMLauncher(**kwargs, mode=FluentMode.from_session_class(cls))
        return launcher()

    @classmethod
    def from_connection(
        cls,
        ip: str | None = None,
        port: int | None = None,
        server_info_file_name: str | None = None,
        password: str | None = None,
        allow_remote_host: bool = False,
        certificates_folder: str | None = None,
        insecure_mode: bool = False,
    ):
        """Connect to an existing Fluent server instance.

        Parameters
        ----------
        ip : str, optional
            IP address for connecting to an existing Fluent instance. The
            IP address defaults to ``"127.0.0.1"``. You can also use the environment
            variable ``PYFLUENT_FLUENT_IP=<ip>`` to set this parameter.
            The explicit value of ``ip`` takes precedence over ``PYFLUENT_FLUENT_IP=<ip>``.
        port : int, optional
            Port to listen on for an existing Fluent instance. You can use the
            environment variable ``PYFLUENT_FLUENT_PORT=<port>`` to set a default
            value. The explicit value of ``port`` takes precedence over
            ``PYFLUENT_FLUENT_PORT=<port>``.
        server_info_file_name: str
            Path to server-info file written out by Fluent server. The default is
            ``None``. PyFluent uses the connection information in the file to
            connect to a running Fluent session.
        password : str, optional
            Password to connect to existing Fluent instance.
        allow_remote_host : bool, optional
            Whether to allow connecting to a remote Fluent instance.
        certificates_folder : str, optional
            Path to the folder containing TLS certificates for Fluent's gRPC server.
        insecure_mode : bool, optional
            If True, Fluent's gRPC server will be connected in insecure mode without TLS.
            This mode is not recommended. For more details on the implications
            and usage of insecure mode, refer to the Fluent documentation.

        Raises
        ------
        TypeError
            If the session type does not match the expected session type.
        """
        from ansys.fluent.core.launcher.launcher import connect_to_fluent

        session = connect_to_fluent(
            ip=ip,
            port=port,
            server_info_file_name=server_info_file_name,
            password=password,
            allow_remote_host=allow_remote_host,
            certificates_folder=certificates_folder,
            insecure_mode=insecure_mode,
        )

        expected = "Solver" if cls.__name__ == "PrePost" else cls.__name__
        actual = session.__class__.__name__

        if actual != expected:
            raise TypeError(
                f"Session type mismatch: expected {expected}, got {actual}."
            )

        return session


class Fields:
    """Container for field and solution variables."""

    def __init__(
        self,
        _session: BaseSession,
        fluent_connection: FluentConnection,
        get_zones_info: weakref.WeakMethod[Callable[[], list[ZoneInfo]]] | None = None,
    ):
        """Initialize Fields."""
        field_data = fluent_connection._service_factory.field_data
        self._field_info = _FieldInfo(field_data)
        self.field_data = LiveFieldData(
            field_data, self._field_info, _session.scheme, get_zones_info
        )
        self.field_data_streaming = (
            fluent_connection._service_factory.field_data_streaming
        )
