from ctypes import c_int, sizeof
from dataclasses import dataclass
import itertools
import logging
import os
from pathlib import Path
import socket
import subprocess
import threading
import time
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
import warnings
import weakref

from docker.models.containers import Container
import grpc

from ansys.fluent.core.services.health_check import HealthCheckService
from ansys.fluent.core.services.scheme_eval import SchemeEval, SchemeEvalService
from ansys.fluent.core.utils.execution import timeout_exec
from ansys.platform.instancemanagement import Instance
import docker

logger = logging.getLogger("pyfluent.general")


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
        """Run monitor thread."""
        main_thread = threading.main_thread()
        main_thread.join()
        for cb in self.cbs:
            cb()


def get_container(container_id_or_name: str) -> Union[bool, Container, None]:
    """Get the Docker container object.

    Returns
    -------
    Union[bool, Container, None]
        If the system is not correctly set up to run Docker containers, returns ``None``.
        If the container was not found, returns ``False``.
        If the container is found, returns the associated Docker container object.

    Notes
    -----
    See `Docker container`_ for more information.

    .. _Docker container: https://docker-py.readthedocs.io/en/stable/containers.html#docker.models.containers.Container

    """
    if not isinstance(container_id_or_name, str):
        container_id_or_name = str(container_id_or_name)
    try:
        docker_client = docker.from_env()
        container = docker_client.containers.get(container_id_or_name)
    except docker.errors.NotFound:  # NotFound is a child from DockerException
        return False
    except docker.errors.DockerException as exc:
        logger.info(f"{type(exc).__name__}: {exc}")
        return None
    return container


class ErrorState:
    """Object to indicate the error state of the connected Fluent client.

    Examples
    --------
    >>> import ansys.fluent.core as pyfluent
    >>> session = pyfluent.launch_fluent()
    >>> session.fluent_connection.error_state.set("test", "test details")
    >>> session.fluent_connection.error_state.name
    'test'
    >>> session.fluent_connection.error_state.details
    'test details'
    >>> session.fluent_connection.error_state.clear()
    >>> session.fluent_connection.error_state.name
    ''
    """

    @property
    def name(self):
        return self._name

    @property
    def details(self):
        return self._details

    def __init__(self, name: str = "", details: str = ""):
        """Initializes the error state object.

        Parameters
        ----------
            name : str
                The name of the error state, by default an empty string, indicating no errors.
            details : str
                Additional details of the error, by default an empty string.
        """
        self._name = name
        self._details = details

    def set(self, name: str, details: str):
        """Method to set the error state name and details to new values."""
        self._name = name
        self._details = details

    def clear(self):
        """Method to clear the current error state, emptying the error name and details properties."""
        self._name = ""
        self._details = ""


@dataclass(frozen=True)
class FluentConnectionProperties:
    """Stores Fluent connection properties, including connection IP, port and password;
    Fluent Cortex working directory, process ID and hostname;
    and whether Fluent was launched in a docker container.

    Examples
    --------
    These properties are also available through the session object and can be accessed as:

    >>> import ansys.fluent.core as pyfluent
    >>> session = pyfluent.launch_fluent()
    >>> session.connection_properties.list_names()
    ['ip', 'port', 'password', 'cortex_pwd', 'cortex_pid', 'cortex_host', 'inside_container']
    >>> session.connection_properties.ip
    '127.0.0.1'
    """

    ip: str = None
    port: int = None
    password: str = None
    cortex_pwd: str = None
    cortex_pid: int = None
    cortex_host: str = None
    fluent_host_pid: int = None
    inside_container: Union[bool, Container, None] = None

    def list_names(self) -> list:
        """Returns list with all property names."""
        return [k for k, _ in vars(self).items()]

    def list_values(self) -> dict:
        """Returns dictionary with all property names and values."""
        return vars(self)


class FluentConnection:
    """Encapsulates a Fluent connection.

    Methods
    -------
    check_health()
        Check health of Fluent connection.
    exit()
        Close the Fluent connection and exit Fluent.
    """

    _on_exit_cbs: List[Callable] = []
    _id_iter = itertools.count()
    _monitor_thread: Optional[MonitorThread] = None
    _writing_transcript_to_interpreter = False

    def __init__(
        self,
        start_timeout: int = 60,
        ip: str = None,
        port: int = None,
        password: str = None,
        channel: grpc.Channel = None,
        cleanup_on_exit: bool = True,
        start_transcript: bool = True,
        remote_instance: Instance = None,
        launcher_args: Dict[str, Any] = None,
        inside_container: bool = None,
    ):
        """Initialize a Session.

        Parameters
        ----------
        start_timeout: int, optional
            Maximum allowable time in seconds for connecting to the Fluent
            server. The default is ``60``.
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
        inside_container: bool, optional
            Whether the Fluent session that is being connected to
            is running inside a docker container.
        """
        self.error_state = ErrorState()
        self._data_valid = False
        self._channel_str = None
        self.finalizer_cbs = []
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

        self.health_check_service = HealthCheckService(
            self._channel, self._metadata, self.error_state
        )

        counter = 0
        while not self.health_check_service.is_serving:
            time.sleep(1)
            counter += 1
            if counter > start_timeout:
                raise RuntimeError(
                    f"The connection to the Fluent server could not be established within the configurable {start_timeout} second time limit."
                )

        self._id = f"session-{next(FluentConnection._id_iter)}"

        if not FluentConnection._monitor_thread:
            FluentConnection._monitor_thread = MonitorThread()
            FluentConnection._monitor_thread.start()

        # Move this service later.
        # Currently, required by launcher to connect to a running session.
        self._scheme_eval_service = SchemeEvalService(
            self._channel, self._metadata, self.error_state
        )
        self.scheme_eval = SchemeEval(self._scheme_eval_service)

        self._cleanup_on_exit = cleanup_on_exit
        self.start_transcript = start_transcript
        from grpc._channel import _InactiveRpcError

        try:
            logger.debug("Obtaining Cortex connection properties...")
            fluent_host_pid = self.scheme_eval.scheme_eval("(cx-client-id)")
            cortex_host = self.scheme_eval.scheme_eval("(cx-cortex-host)")
            cortex_pid = self.scheme_eval.scheme_eval("(cx-cortex-id)")
            cortex_pwd = self.scheme_eval.scheme_eval("(cortex-pwd)")
            logger.debug("Cortex connection properties successfully obtained.")
        except _InactiveRpcError:
            logger.warning(
                "Fluent Cortex properties unobtainable, force exit and other"
                "methods are not going to work properly, proceeding..."
            )
            cortex_host = None
            cortex_pid = None
            cortex_pwd = None
            fluent_host_pid = None

        if (
            (inside_container is None or inside_container is True)
            and not remote_instance
            and cortex_host is not None
        ):
            logger.info("Checking if Fluent is running inside a container.")
            inside_container = get_container(cortex_host)
            logger.debug(f"get_container({cortex_host}): {inside_container}")
            if inside_container is False:
                logger.info("Fluent is not running inside a container.")
            elif inside_container is None:
                logger.info(
                    "The current system does not support Docker containers. "
                    "Assuming Fluent is not inside a container."
                )

        self.connection_properties = FluentConnectionProperties(
            ip,
            port,
            password,
            cortex_pwd,
            cortex_pid,
            cortex_host,
            fluent_host_pid,
            inside_container,
        )

        self._remote_instance = remote_instance
        self.launcher_args = launcher_args

        self._finalizer = weakref.finalize(
            self,
            FluentConnection._exit,
            self._channel,
            self._cleanup_on_exit,
            self.scheme_eval,
            self.finalizer_cbs,
            self._remote_instance,
        )
        FluentConnection._monitor_thread.cbs.append(self._finalizer)

    def force_exit(self):
        """
        Immediately terminates the Fluent client,
        losing unsaved progress and data.

        Notes
        -----
        If the Fluent session is responsive, prefer using :func:`exit()` instead.

        Examples
        --------
        >>> import ansys.fluent.core as pyfluent
        >>> session = pyfluent.launch_fluent()
        >>> session.force_exit()
        """
        if self.connection_properties.inside_container:
            logger.error(
                "Cannot execute cleanup script, Fluent running inside container. "
                "Use force_exit_container() instead."
            )
            return
        if self._remote_instance is not None:
            logger.error("Cannot execute cleanup script, Fluent running remotely.")
            return

        pwd = self.connection_properties.cortex_pwd
        pid = self.connection_properties.fluent_host_pid
        host = self.connection_properties.cortex_host
        if host != socket.gethostname():
            logger.error(
                "Fluent host is not the current host, cancelling forced exit..."
            )
            return
        if os.name == "nt":
            cleanup_file_ext = "bat"
            cmd_list = []
        elif os.name == "posix":
            cleanup_file_ext = "sh"
            cmd_list = ["bash"]
        else:
            logger.error(
                "Unrecognized or unsupported operating system, cancelling Fluent cleanup script execution."
            )
            return
        cleanup_filename = f"cleanup-fluent-{host}-{pid}.{cleanup_file_ext}"
        logger.debug(f"Looking for {cleanup_filename}...")
        cleanup_filepath = Path(pwd, cleanup_filename)
        if cleanup_filepath.is_file():
            logger.info(
                f"Executing Fluent cleanup script, filepath: {cleanup_filepath}"
            )
            cmd_list.append(cleanup_filepath)
            logger.debug(f"Cleanup command list = {cmd_list}")
            subprocess.Popen(
                cmd_list,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        else:
            logger.error("Could not find cleanup file.")

    def force_exit_container(self):
        """
        Immediately terminates the Fluent client running inside a container,
        losing unsaved progress and data.

        Notes
        -----
        By default, Fluent does not run in a container,
        in that case use :func:`force_exit()`.
        If the Fluent session is responsive, prefer using :func:`exit()` instead.
        """
        if self._remote_instance is not None:
            logger.error(
                "Fluent is running remotely, cannot terminate Fluent container."
            )
            return
        container = self.connection_properties.inside_container
        if not container:
            logger.error(
                "Session is not inside a container, cannot terminate Fluent container. "
                "Try force_exit() instead."
            )
            return
        container_id = self.connection_properties.cortex_host
        pid = self.connection_properties.fluent_host_pid
        cleanup_filename = f"cleanup-fluent-{container_id}-{pid}.sh"
        logger.debug(f"Executing Fluent container cleanup script: {cleanup_filename}")
        if get_container(container_id):
            try:
                container.exec_run(["bash", cleanup_filename], detach=True)
            except docker.errors.APIError as e:
                logger.info(f"{type(e).__name__}: {e}")
                logger.debug(
                    "Caught Docker APIError, Docker container probably not running anymore."
                )
        else:
            logger.debug("Container not found, cancelling cleanup script execution.")

    def register_finalizer_cb(self, cb):
        """Register a callback to run with the finalizer."""
        self.finalizer_cbs.append(cb)

    def create_service(self, service, *args):
        """Create a gRPC service.

        Parameters
        ----------
        service : Any
            service class
        args : Any, optional
            additional arguments, by default empty

        Returns
        -------
        Any
            service object
        """
        return service(self._channel, self._metadata, *args)

    def check_health(self) -> str:
        """Check health of Fluent connection."""
        warnings.warn("Use -> health_check_service.status()", DeprecationWarning)
        return self.health_check_service.status()

    def exit(self, timeout: float = None, timeout_force: bool = True) -> None:
        """Close the Fluent connection and exit Fluent.

        Parameters
        ----------
        timeout : float, optional
            Time in seconds before considering that the exit request has timed out.
            If omitted or specified as None, then request will not time out and will lock up the interpreter
            while waiting for a response.
        timeout_force : bool, optional
            If not specified, defaults to True. If True, attempts to terminate the Fluent process if
            exit request reached timeout. Executes :func:`force_exit()` or :func:`force_exit_container()`,
            depending on how Fluent was launched.

        Notes
        -----
        Can also set the ``PYFLUENT_TIMEOUT_FORCE_EXIT`` environment variable to specify the number of seconds and
        alter the default ``timeout`` value. Setting this env var to a non-number value, such as ``OFF``,
        will return this function to default behavior. Note that the environment variable will be ignored if
        timeout is specified when calling this function.

        Examples
        --------

        >>> import ansys.fluent.core as pyfluent
        >>> session = pyfluent.launch_fluent()
        >>> session.exit()
        """

        if timeout is None:
            env_timeout = os.getenv("PYFLUENT_TIMEOUT_FORCE_EXIT")

            if env_timeout:
                logger.debug("Found PYFLUENT_TIMEOUT_FORCE_EXIT env var")
                try:
                    timeout = float(env_timeout)
                    logger.debug(f"Setting TIMEOUT_FORCE_EXIT to {timeout}")
                except ValueError:
                    logger.debug(
                        "Off or unrecognized PYFLUENT_TIMEOUT_FORCE_EXIT value, not enabling timeout force exit"
                    )

        if timeout is None:
            logger.info("Finalizing Fluent connection...")
            self._finalizer()
        else:
            if not self.health_check_service.is_serving:
                logger.debug("gRPC service not working, cancelling soft exit call.")
            else:
                logger.info("Attempting to finalize Fluent connection...")

                success = timeout_exec(self._finalizer, timeout)
                if success:
                    return

            logger.debug("Continuing...")
            if timeout_force:
                if self._remote_instance:
                    logger.warning("Cannot force exit from Fluent remote instance.")
                    return
                elif self.connection_properties.inside_container:
                    logger.debug(
                        "Fluent running inside container, cleaning up Fluent inside container..."
                    )
                    self.force_exit_container()
                else:
                    logger.debug(
                        "Fluent running locally, cleaning up Fluent processes..."
                    )
                    self.force_exit()
                logger.debug("Done.")
            else:
                logger.debug("Timeout force exit disabled, returning...")

    @staticmethod
    def _exit(
        channel,
        cleanup_on_exit,
        scheme_eval,
        finalizer_cbs,
        remote_instance,
    ) -> None:
        logger.debug("FluentConnection exit method called.")
        if channel:
            for cb in finalizer_cbs:
                cb()
            if cleanup_on_exit:
                try:
                    scheme_eval.exec(("(exit-server)",))
                except Exception:
                    pass
            channel.close()
            channel = None

        if remote_instance:
            remote_instance.delete()
