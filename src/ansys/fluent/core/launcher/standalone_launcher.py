"""Provides a module for launching Fluent in standalone mode."""

import logging
import os
from pathlib import Path
import subprocess
from typing import Any, Dict, Optional, Union

from ansys.fluent.core.launcher.launcher_utils import (
    FluentMode,
    LaunchFluentError,
    _await_fluent_launch,
    _build_journal_argument,
    _confirm_watchdog_start,
    _generate_launch_string,
    _get_argvals,
    _get_server_info,
    _get_server_info_file_name,
    _get_subprocess_kwargs_for_fluent,
    _is_windows,
    _process_invalid_args,
    _process_kwargs,
    _raise_exception_g_gu_in_windows_os,
)
import ansys.fluent.core.launcher.watchdog as watchdog
from ansys.fluent.core.utils.file_transfer_service import RemoteFileHandler

_THIS_DIR = os.path.dirname(__file__)
_OPTIONS_FILE = os.path.join(_THIS_DIR, "fluent_launcher_options.json")
logger = logging.getLogger("pyfluent.launcher")


class StandaloneLauncher:
    """Instantiates Fluent session in standalone mode."""

    def __init__(
        self,
        argvals: Optional[Any] = None,
        product_version: Optional[str] = None,
        version: Optional[str] = None,
        precision: Optional[str] = None,
        processor_count: Optional[int] = None,
        journal_file_names: Union[None, str, list[str]] = None,
        start_timeout: int = 60,
        additional_arguments: Optional[str] = "",
        env: Optional[Dict[str, Any]] = None,
        start_container: Optional[bool] = None,
        container_dict: Optional[dict] = None,
        dry_run: bool = False,
        cleanup_on_exit: bool = True,
        start_transcript: bool = True,
        show_gui: Optional[bool] = None,
        case_file_name: Optional[str] = None,
        case_data_file_name: Optional[str] = None,
        lightweight_mode: Optional[bool] = None,
        mode: Optional[Union[FluentMode, str, None]] = None,
        py: Optional[bool] = None,
        gpu: Optional[bool] = None,
        cwd: Optional[str] = None,
        topy: Optional[Union[str, list]] = None,
        start_watchdog: Optional[bool] = None,
        scheduler_options: Optional[dict] = None,
        **kwargs,
    ):
        """Launch Fluent session in standalone mode.

        Parameters
        ----------
        product_version : str, optional
            Select an installed version of ANSYS. The string must be in a format like
            ``"23.2.0"`` (for 2023 R2) matching the documented version format in the
            FluentVersion class. The default is ``None``, in which case the newest installed
            version is used.
        version : str, optional
            Geometric dimensionality of the Fluent simulation. The default is ``None``,
            in which case ``"3d"`` is used. Options are ``"3d"`` and ``"2d"``.
        precision : str, optional
            Floating point precision. The default is ``None``, in which case ``"double"``
            is used. Options are ``"double"`` and ``"single"``.
        processor_count : int, optional
            Number of processors. The default is ``None``, in which case ``1``
            processor is used.  In job scheduler environments the total number of
            allocated cores is clamped to value of ``processor_count``.
        journal_file_names : str or list of str, optional
            The string path to a Fluent journal file, or a list of such paths. Fluent will execute the
            journal(s). The default is ``None``.
        start_timeout : int, optional
            Maximum allowable time in seconds for connecting to the Fluent
            server. The default is ``60``.
        additional_arguments : str, optional
            Additional arguments to send to Fluent as a string in the same
            format they are normally passed to Fluent on the command line.
        env : dict[str, str], optional
            Mapping to modify environment variables in Fluent. The default
            is ``None``.
        start_container : bool, optional
            Specifies whether to launch a Fluent Docker container image. For more details about containers, see
            :mod:`~ansys.fluent.core.launcher.fluent_container`.
        container_dict : dict, optional
            Dictionary for Fluent Docker container configuration. If specified,
            setting ``start_container = True`` as well is redundant.
            Will launch Fluent inside a Docker container using the configuration changes specified.
            See also :mod:`~ansys.fluent.core.launcher.fluent_container`.
        dry_run : bool, optional
            Defaults to False. If True, will not launch Fluent, and will instead print configuration information
            that would be used as if Fluent was being launched. If dry running a container start,
            ``launch_fluent()`` will return the configured ``container_dict``.
        cleanup_on_exit : bool, optional
            Whether to shut down the connected Fluent session when PyFluent is
            exited, or the ``exit()`` method is called on the session instance,
            or if the session instance becomes unreferenced. The default is ``True``.
        start_transcript : bool, optional
            Whether to start streaming the Fluent transcript in the client. The
            default is ``True``. You can stop and start the streaming of the
            Fluent transcript subsequently via the method calls, ``transcript.start()``
            and ``transcript.stop()`` on the session object.
        show_gui : bool, optional
            Whether to display the Fluent GUI. The default is ``None``, which does not
            cause the GUI to be shown. If a value of ``False`` is
            not explicitly provided, the GUI will also be shown if
            the environment variable ``PYFLUENT_SHOW_SERVER_GUI`` is set to 1.
        case_file_name : str, optional
            If provided, the case file at ``case_file_name`` is read into the Fluent session.
        case_data_file_name : str, optional
            If provided, the case and data files at ``case_data_file_name`` are read into the Fluent session.
        lightweight_mode : bool, optional
            Whether to run in lightweight mode. In lightweight mode, the lightweight settings are read into the
            current Fluent solver session. The mesh is read into a background Fluent solver session which will
            replace the current Fluent solver session once the mesh read is complete and the lightweight settings
            made by the user in the current Fluent solver session have been applied in the background Fluent
            solver session. This is all orchestrated by PyFluent and requires no special usage.
            This parameter is used only when ``case_file_name`` is provided. The default is ``False``.
        mode : str, optional
            Launch mode of Fluent to point to a specific session type.
            The default value is ``None``. Options are ``"meshing"``,
            ``"pure-meshing"`` and ``"solver"``.
        py : bool, optional
            If True, Fluent will run in Python mode. Default is None.
        gpu : bool, optional
            If True, Fluent will start with GPU Solver.
        cwd : str, Optional
            Working directory for the Fluent client.
        topy : bool or str, optional
            A boolean flag to write the equivalent Python journal(s) from the journal(s) passed.
            Can optionally take the file name of the new python journal file.
        start_watchdog : bool, optional
            When ``cleanup_on_exit`` is True, ``start_watchdog`` defaults to True,
            which means an independent watchdog process is run to ensure
            that any local GUI-less Fluent sessions started by PyFluent are properly closed (or killed if frozen)
            when the current Python process ends.

        Returns
        -------
        :obj:`~typing.Union` [:class:`Meshing<ansys.fluent.core.session_meshing.Meshing>`, \
        :class:`~ansys.fluent.core.session_pure_meshing.PureMeshing`, \
        :class:`~ansys.fluent.core.session_solver.Solver`, \
        :class:`~ansys.fluent.core.session_solver_icing.SolverIcing`, dict]
            Session object or configuration dictionary if ``dry_run = True``.

        Raises
        ------
        UnexpectedKeywordArgument
            If an unexpected keyword argument is provided.
        DockerContainerLaunchNotSupported
            If a Fluent Docker container launch is not supported.

        Notes
        -----
        Job scheduler environments such as SLURM, LSF, PBS, etc. allocates resources / compute nodes.
        The allocated machines and core counts are queried from the scheduler environment and
        passed to Fluent.
        """
        _process_kwargs(kwargs)
        del kwargs
        del start_container
        argvals = locals().copy()
        _process_invalid_args(dry_run, "standalone", argvals)
        args = _get_argvals(argvals, mode)
        argvals.update(args)
        if argvals["start_timeout"] is None:
            argvals["start_timeout"] = 60
        for arg_name, arg_values in argvals.items():
            setattr(self, arg_name, arg_values)
        self.argvals = argvals

    def __call__(self):
        if self.lightweight_mode is None:
            # note argvals is no longer locals() here due to _get_session_info() pass
            self.argvals.pop("lightweight_mode")
            setattr(self, "lightweight_mode", False)

        if self.additional_arguments:
            _raise_exception_g_gu_in_windows_os(self.additional_arguments)

        if os.getenv("PYFLUENT_FLUENT_DEBUG") == "1":
            self.argvals["fluent_debug"] = True

        server_info_file_name = _get_server_info_file_name()
        launch_string = _generate_launch_string(
            self.argvals,
            self.meshing_mode,
            self.show_gui,
            self.additional_arguments,
            server_info_file_name,
        )

        sifile_last_mtime = Path(server_info_file_name).stat().st_mtime
        if self.env is None:
            setattr(self, "env", {})
        kwargs = _get_subprocess_kwargs_for_fluent(self.env, self.argvals)
        if self.cwd:
            kwargs.update(cwd=self.cwd)
        launch_string += _build_journal_argument(self.topy, self.journal_file_names)

        if _is_windows():
            # Using 'start.exe' is better, otherwise Fluent is more susceptible to bad termination attempts
            launch_cmd = 'start "" ' + launch_string
        else:
            launch_cmd = launch_string

        try:
            logger.debug(f"Launching Fluent with command: {launch_cmd}")

            subprocess.Popen(launch_cmd, **kwargs)

            try:
                _await_fluent_launch(
                    server_info_file_name, self.start_timeout, sifile_last_mtime
                )
            except TimeoutError as ex:
                if _is_windows():
                    logger.warning(f"Exception caught - {type(ex).__name__}: {ex}")
                    launch_cmd = launch_string.replace('"', "", 2)
                    kwargs.update(shell=False)
                    logger.warning(
                        f"Retrying Fluent launch with less robust command: {launch_cmd}"
                    )
                    subprocess.Popen(launch_cmd, **kwargs)
                    _await_fluent_launch(
                        server_info_file_name, self.start_timeout, sifile_last_mtime
                    )
                else:
                    raise ex

            session = self.new_session.create_from_server_info_file(
                server_info_file_name=server_info_file_name,
                remote_file_handler=RemoteFileHandler(),
                cleanup_on_exit=self.cleanup_on_exit,
                start_transcript=self.start_transcript,
                launcher_args=self.argvals,
                inside_container=False,
            )
            start_watchdog = _confirm_watchdog_start(
                self.start_watchdog, self.cleanup_on_exit, session.fluent_connection
            )
            if start_watchdog:
                logger.info("Launching Watchdog for local Fluent client...")
                ip, port, password = _get_server_info(server_info_file_name)
                watchdog.launch(os.getpid(), port, password, ip)
            if self.case_file_name:
                if self.meshing_mode:
                    session.tui.file.read_case(self.case_file_name)
                elif self.lightweight_mode:
                    session.read_case_lightweight(self.case_file_name)
                else:
                    session.file.read(
                        file_type="case",
                        file_name=self.case_file_name,
                    )
            if self.case_data_file_name:
                if not self.meshing_mode:
                    session.file.read(
                        file_type="case-data",
                        file_name=self.case_data_file_name,
                    )
                else:
                    raise RuntimeError(
                        "Case and data file cannot be read in meshing mode."
                    )

            return session
        except Exception as ex:
            logger.error(f"Exception caught - {type(ex).__name__}: {ex}")
            raise LaunchFluentError(launch_cmd) from ex
        finally:
            server_info_file = Path(server_info_file_name)
            if server_info_file.exists():
                server_info_file.unlink()
