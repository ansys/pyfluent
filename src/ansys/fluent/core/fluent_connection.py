from ctypes import c_int, sizeof
from dataclasses import dataclass
import itertools
import logging
import multiprocessing
from multiprocessing.context import TimeoutError
import os
from pathlib import Path
import socket
import subprocess
import threading
import time
from typing import Any, Callable, Dict, List, Optional, Tuple
import warnings
import weakref

import grpc

from ansys.fluent.core.services.health_check import HealthCheckService
from ansys.fluent.core.services.scheme_eval import SchemeEval, SchemeEvalService
from ansys.platform.instancemanagement import Instance

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
        main_thread = threading.main_thread()
        main_thread.join()
        for cb in self.cbs:
            cb()


def get_container_ids() -> List[str]:
    try:
        logger.debug("Attempting to get docker container IDs...")
        proc = subprocess.Popen(
            ["docker", "ps", "-q"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
        )
        output_bytes = proc.stdout.read()
        output_str = output_bytes.decode()
        ids = output_str.strip().split()
    except:
        logger.warning("Failed to get docker container IDs.")
        ids = []
    return ids


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
    inside_container: bool = None

    def list_names(self) -> list:
        """List all property names."""
        return [k for k, _ in vars(self).items()]

    def list_values(self) -> dict:
        """Dictionary with all property names and values."""
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
        start_timeout: int = 100,
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
        inside_container: bool, optional
            Whether the Fluent session that is being connected to
            is running inside a docker container.
        """
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

        self.health_check_service = HealthCheckService(self._channel, self._metadata)

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
        self._scheme_eval_service = SchemeEvalService(self._channel, self._metadata)
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
                "Cortex properties unobtainable, force exit "
                " methods are not going to work, proceeding..."
            )
            cortex_host = None
            cortex_pid = None
            cortex_pwd = None
            fluent_host_pid = None

        if inside_container is None and not remote_instance and cortex_host is not None:
            logger.debug("Checking if Fluent is running inside a container.")
            if cortex_host in get_container_ids():
                logger.debug("Fluent is running inside a container.")
                inside_container = True
            else:
                logger.debug("Assuming Fluent is not running inside a container.")
                inside_container = False

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
                f"Cannot execute cleanup script, Fluent running inside container. "
                f"Use force_exit_container() instead."
            )
            return
        if self._remote_instance is not None:
            logger.error(f"Cannot execute cleanup script, Fluent running remotely.")
            return

        pwd = self.connection_properties.cortex_pwd
        pid = self.connection_properties.fluent_host_pid
        host = self.connection_properties.cortex_host
        if not host == socket.gethostname():
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
                f"Unrecognized or unsupported operating system, cancelling Fluent cleanup script execution."
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
            logger.error(f"Could not find cleanup file.")

    def force_exit_container(self):
        """
        Immediately terminates the docker container running the Fluent client,
        losing unsaved progress and data.

        Notes
        -----
        By default, Fluent does not run in a container,
        in that case use :func:`force_exit()`.
        If the Fluent session is responsive, prefer using :func:`exit()` instead.
        """
        if not self.connection_properties.inside_container:
            logger.error(
                f"Session is not inside a container, cannot kill Fluent container. "
                f"Use force_exit() instead."
            )
            return
        if self._remote_instance is not None:
            logger.error(f"Fluent is running remotely, cannot kill Fluent container.")
            return
        container_id = self.connection_properties.cortex_host
        subprocess.run(["docker", "kill", container_id])

    def register_finalizer_cb(self, cb):
        self.finalizer_cbs.append(cb)

    def create_service(self, service, add_arg=None):
        if add_arg:
            return service(self._channel, self._metadata, add_arg)
        return service(self._channel, self._metadata)

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
            self._finalizer()
        else:
            if not self.health_check_service.is_serving:
                logger.debug("gRPC service not working, cancelling soft exit call.")
            else:
                logger.debug("Attempting session.exit()")

                def _connection_finalizer(connection):
                    return connection._finalizer()

                pool = multiprocessing.pool.ThreadPool(processes=1)
                async_result = pool.apply_async(_connection_finalizer, args=(self,))
                try:
                    _ = async_result.get(timeout=timeout)
                    logger.debug("session.exit() successful")
                    pool.close()
                    return
                except TimeoutError:
                    logger.debug("session.exit() timeout")
                    pool.terminate()

            logger.debug("Continuing...")
            if timeout_force:
                if self._remote_instance:
                    logger.warning("Cannot force exit from Fluent remote instance.")
                    return
                elif self.connection_properties.inside_container:
                    logger.debug(
                        "Fluent running inside container, killing container..."
                    )
                    self.force_exit_container()
                else:
                    logger.debug("Fluent running locally, killing processes...")
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
