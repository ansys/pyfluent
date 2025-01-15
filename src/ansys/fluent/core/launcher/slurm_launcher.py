"""Provides a module for launching Fluent within a Slurm environment.

Examples
--------
Note that the keys ``scheduler_headnode``, ``scheduler_queue`` and ``scheduler_account``
are optional and should be specified in a similar manner to Fluent's scheduler options.

>>> slurm = pyfluent.launch_fluent(
...   scheduler_options={
...     "scheduler": "slurm",
...     "scheduler_headnode": "<headnode>",
...     "scheduler_queue": "<queue>",
...     "scheduler_account": "<account>"
...   },
...   additional_arguments="-t16 -cnf=m1:8,m2:8",
... )
>>> type(slurm)
<class 'ansys.fluent.core.launcher.slurm_launcher.SlurmFuture'>
>>> slurm.pending(), slurm.running(), slurm.done() # before Fluent is launched
(True, False, False)
>>> slurm.pending(), slurm.running(), slurm.done() # after Fluent is launched
(False, True, False)
>>> session = slurm.result()
>>> type(session)
<class 'ansys.fluent.core.session_solver.Solver'>
>>> session.exit()
>>> slurm.pending(), slurm.running(), slurm.done()
(False, False, True)

# Callable slurm launcher

>>> from ansys.fluent.core.launcher.launcher import create_launcher
>>> from ansys.fluent.core.launcher.pyfluent_enums import LaunchMode, FluentMode

>>> slurm_meshing_launcher = create_launcher(LaunchMode.SLURM, mode=FluentMode.MESHING)
>>> slurm_meshing_session = slurm_meshing_launcher()

>>> slurm_solver_launcher = create_launcher(LaunchMode.SLURM)
>>> slurm_solver_session = slurm_solver_launcher()
"""

from concurrent.futures import Future, ThreadPoolExecutor
import logging
import os
from pathlib import Path
import shutil
import subprocess
import time
from typing import Any, Callable, Dict

from ansys.fluent.core.exceptions import InvalidArgument
from ansys.fluent.core.launcher.launcher_utils import (
    _await_fluent_launch,
    _build_journal_argument,
    _get_subprocess_kwargs_for_fluent,
)
from ansys.fluent.core.launcher.process_launch_string import _generate_launch_string
from ansys.fluent.core.launcher.pyfluent_enums import (
    Dimension,
    FluentLinuxGraphicsDriver,
    FluentMode,
    FluentWindowsGraphicsDriver,
    Precision,
    UIMode,
    _get_argvals_and_session,
)
from ansys.fluent.core.launcher.server_info import _get_server_info_file_names
from ansys.fluent.core.session_meshing import Meshing
from ansys.fluent.core.session_pure_meshing import PureMeshing
from ansys.fluent.core.session_solver import Solver
from ansys.fluent.core.session_solver_icing import SolverIcing
from ansys.fluent.core.utils.fluent_version import FluentVersion

logger = logging.getLogger("pyfluent.launcher")


def _get_slurm_job_id(proc: subprocess.Popen):
    prefix = "Submitted batch job"
    for line in proc.stdout:
        if line.startswith(prefix.encode()):
            line = line.decode().removeprefix(prefix).strip()
            return int(line)


class _SlurmWrapper:
    """A class wrapping Slurm commands."""

    @staticmethod
    def is_available() -> bool:
        """Check whether Slurm is available.

        Returns
        -------
        bool
            ``True`` if Slurm is available, otherwise ``False``.
        """
        return shutil.which("sinfo") and len(_SlurmWrapper.list_queues()) > 0

    @staticmethod
    def list_queues() -> list[str]:
        """Return list of queues.

        Returns
        -------
        list[str]
        List of queues.
        """
        out = subprocess.check_output(["sinfo", "--format=%P", "--noheader"])
        queues = out.decode().strip().split()
        queues = [q.removesuffix("*") for q in queues]
        return queues

    @staticmethod
    def get_state(job_id: int) -> str:
        """Return state of a job.

        Parameters
        ----------
        job_id : int
            Job id.

        Returns
        -------
        str
            Any of ``""``, ``"RUNNING"``, ``"CANCELLED"`` or ``"COMPLETED"``.
        """
        out = subprocess.check_output(["squeue", "-j", f"{job_id}", "-o", '"%T"', "-h"])
        return out.decode().strip().strip('"')

    @staticmethod
    def cancel(job_id: int) -> None:
        """Cancel a job.

        Parameters
        ----------
        job_id : int
            Job id.
        """
        subprocess.run(["scancel", f"{job_id}"])


class SlurmFuture:
    """Encapsulates asynchronous launch of Fluent within a Slurm environment.

    The interface is similar to Python's
    `future object <https://docs.python.org/3/library/asyncio-future.html#future-object>`_.
    """

    def __init__(self, future: Future, job_id: int):
        """Initialize SlurmFuture."""
        self._future = future
        self._job_id = job_id

    def __enter__(self):
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any):
        self.cancel()

    def _get_state(self) -> str:
        return _SlurmWrapper.get_state(self._job_id)

    def _cancel(self):
        _SlurmWrapper.cancel(self._job_id)

    def cancel(self, timeout: int = 60) -> bool:
        """Attempt to cancel the Fluent launch within timeout seconds.

        Parameters
        ----------
        timeout : int, optional
            timeout in seconds, by default 60

        Returns
        -------
        bool
            ``True`` if the Fluent launch is successfully cancelled, otherwise ``False``.
        """
        if self.done():
            return False
        self._cancel()
        for _ in range(timeout):
            if self._get_state() in ["", "CANCELLED"]:
                return True
            time.sleep(1)
        return False

    def running(self) -> bool:
        """Return ``True`` if Fluent is currently running, otherwise ``False``."""
        return self._get_state() == "RUNNING" and self._future.done()

    def pending(self) -> bool:
        """Return ``True`` if the Fluent launch is currently waiting for Slurm
        allocation or Fluent is being launched, otherwise ``False``."""
        return self._future.running()

    def done(self) -> bool:
        """Return ``True`` if the Fluent launch was successfully cancelled or Fluent was
        finished running, otherwise ``False``."""
        return self._get_state() in ["", "CANCELLED", "COMPLETED"]

    def result(
        self, timeout: int = None
    ) -> Meshing | PureMeshing | Solver | SolverIcing:
        """Return the session instance corresponding to the Fluent launch. If Fluent
        hasn't yet launched, then this method will wait up to timeout seconds. If Fluent
        hasn't launched in timeout seconds, then a TimeoutError will be raised. If
        timeout is not specified or None, there is no limit to the wait time.

        If the Fluent launch raised an exception, this method will raise the same exception.

        Parameters
        ----------
        timeout : int, optional
            timeout in seconds

        Returns
        -------
        :obj:`~typing.Union` [:class:`Meshing<ansys.fluent.core.session_meshing.Meshing>`, \
        :class:`~ansys.fluent.core.session_pure_meshing.PureMeshing`, \
        :class:`~ansys.fluent.core.session_solver.Solver`, \
        :class:`~ansys.fluent.core.session_solver_icing.SolverIcing`]
            The session instance corresponding to the Fluent launch.
        """
        return self._future.result(timeout)

    def exception(self, timeout: int = None) -> Exception:
        """Return the exception raised by the Fluent launch. If Fluent hasn't yet
        launched, then this method will wait up to timeout seconds. If Fluent hasn't
        launched in timeout seconds, then a TimeoutError will be raised. If timeout is
        not specified or None, there is no limit to the wait time.

        If the Fluent launch completed without raising, None is returned.

        Parameters
        ----------
        timeout : int, optional
            timeout in seconds

        Returns
        -------
        Exception
            The exception raised by the Fluent launch.
        """
        return self._future.exception(timeout)

    def add_done_callback(self, fn: Callable):
        """Attaches the callable function. The function will be called, with the session
        as its only argument, when Fluent is launched.

        Parameters
        ----------
        fn : Callable
            Callback function.
        """
        self._future.add_done_callback(fn)


class SlurmLauncher:
    """Instantiates Fluent session within a Slurm environment."""

    def __init__(
        self,
        mode: FluentMode | str | None = None,
        ui_mode: UIMode | str | None = None,
        graphics_driver: (
            FluentWindowsGraphicsDriver | FluentLinuxGraphicsDriver | str | None
        ) = None,
        product_version: FluentVersion | str | float | int | None = None,
        dimension: Dimension | int | None = None,
        precision: Precision | str | None = None,
        processor_count: int | None = None,
        journal_file_names: None | str | list[str] = None,
        start_timeout: int = -1,
        additional_arguments: str | None = "",
        env: Dict[str, Any] | None = None,
        cleanup_on_exit: bool = True,
        start_transcript: bool = True,
        case_file_name: str | None = None,
        case_data_file_name: str | None = None,
        lightweight_mode: bool | None = None,
        py: bool | None = None,
        gpu: bool | None = None,
        cwd: str | None = None,
        fluent_path: str | None = None,
        topy: str | list | None = None,
        start_watchdog: bool | None = None,
        scheduler_options: dict | None = None,
        file_transfer_service: Any | None = None,
    ):
        """Launch Fluent session in standalone mode.

        Parameters
        ----------
        mode : FluentMode
            Launch mode of Fluent to point to a specific session type.
        ui_mode : UIMode
            Fluent user interface mode. Options are the values of the ``UIMode`` enum.
        graphics_driver : FluentWindowsGraphicsDriver or FluentLinuxGraphicsDriver
            Graphics driver of Fluent. Options are the values of the
            ``FluentWindowsGraphicsDriver`` enum in Windows or the values of the
            ``FluentLinuxGraphicsDriver`` enum in Linux.
        product_version : FluentVersion or str or float or int, optional
            Version of Ansys Fluent to launch. To use Fluent version 2025 R1, pass
            ``FluentVersion.v251``, ``"25.1.0"``, ``"25.1"``, ``25.1``, or ``251``.
            The default is ``None``, in which case the newest installed version is used.
        dimension : Dimension or int, optional
            Geometric dimensionality of the Fluent simulation. The default is ``None``,
            in which case ``Dimension.THREE`` is used. Options are either the values of the
            ``Dimension`` enum (``Dimension.TWO`` or ``Dimension.THREE``) or any of ``2`` and ``3``.
        precision : Precision or str, optional
            Floating point precision. The default is ``None``, in which case ``Precision.DOUBLE``
            is used. Options are either the values of the ``Precision`` enum (``Precision.SINGLE``
            or ``Precision.DOUBLE``) or any of ``"double"`` and ``"single"``.
        processor_count : int, optional
            Number of processors. The default is ``None``, in which case ``1``
            processor is used.  In job scheduler environments the total number of
            allocated cores is clamped to value of ``processor_count``.
        journal_file_names : str or list of str, optional
            The string path to a Fluent journal file or a list of such paths. Fluent executes the
            journals. The default is ``None``.
        start_timeout : int, optional
            Maximum allowable time in seconds for connecting to the Fluent
            server. The default is ``60``.
        additional_arguments : str, optional
            Additional arguments to send to Fluent as a string in the same
            format they are normally passed to Fluent on the command line.
        env : dict[str, str], optional
            Mapping to modify environment variables in Fluent. The default
            is ``None``.
        cleanup_on_exit : bool, optional
            Whether to shut down the connected Fluent session when PyFluent is
            exited, or the ``exit()`` method is called on the session instance,
            or if the session instance becomes unreferenced. The default is ``True``.
        start_transcript : bool, optional
            Whether to start streaming the Fluent transcript in the client. The
            default is ``True``. You can stop and start the streaming of the
            Fluent transcript subsequently via the method calls, ``transcript.start()``
            and ``transcript.stop()`` on the session object.
        case_file_name : str, optional
            Name of the case file to read into the
            Fluent session. The default is ``None``.
        case_data_file_name : str, optional
            Name of the case data file. If names of both a case file and case data file are provided, they are read into the Fluent session.
        lightweight_mode : bool, optional
            Whether to run in lightweight mode. In lightweight mode, the lightweight settings are read into the
            current Fluent solver session. The mesh is read into a background Fluent solver session,
            which replaces the current Fluent solver session once the mesh is read and the lightweight settings
            made by the user in the current Fluent solver session have been applied in the background Fluent
            solver session. This is all orchestrated by PyFluent and requires no special usage.
            This parameter is used only when ``case_file_name`` is provided. The default is ``False``.
        py : bool, optional
            If True, Fluent will run in Python mode. Default is None.
        gpu : bool, optional
            If True, Fluent will start with GPU Solver.
        cwd : str, Optional
            Working directory for the Fluent client.
        fluent_path: str, Optional
            User provided Fluent installation path.
        topy : bool or str, optional
            A boolean flag to write the equivalent Python journal(s) from the journal(s) passed.
            Can optionally take the file name of the new python journal file.
        start_watchdog : bool, optional
            When ``cleanup_on_exit`` is True, ``start_watchdog`` defaults to True,
            which means an independent watchdog process is run to ensure
            that any local GUI-less Fluent sessions started by PyFluent are properly closed (or killed if frozen)
            when the current Python process ends.
        scheduler_options : dict, optional
            Dictionary containing scheduler options. Default is None.

            Currently only the Slurm scheduler is supported. The ``scheduler_options``
            dictionary must be of the form ``{"scheduler": "slurm",
            "scheduler_headnode": "<headnode>", "scheduler_queue": "<queue>",
            "scheduler_account": "<account>"}``. The keys ``scheduler_headnode``,
            ``scheduler_queue`` and ``scheduler_account`` are optional and should be
            specified in a similar manner to Fluent's scheduler options.
        file_transfer_service : optional
            File transfer service for uploading and downloading files to and from the server.

        Returns
        -------
        :obj:`~typing.Union` [:class:`Meshing<ansys.fluent.core.session_meshing.Meshing>`, \
        :class:`~ansys.fluent.core.session_pure_meshing.PureMeshing`, \
        :class:`~ansys.fluent.core.session_solver.Solver`, \
        :class:`~ansys.fluent.core.session_solver_icing.SolverIcing`, dict]
            Session object or configuration dictionary if ``dry_run = True``.

        Notes
        -----
        Job scheduler environments such as SLURM, LSF, and PBS, allocate resources and compute nodes.
        The allocated machines and core counts are queried from the scheduler environment and
        passed to Fluent.
        """
        if not _SlurmWrapper.is_available():
            raise RuntimeError("Slurm is not available.")
        self._argvals, self._new_session = _get_argvals_and_session(locals().copy())
        self.file_transfer_service = file_transfer_service
        if os.getenv("PYFLUENT_SHOW_SERVER_GUI") == "1":
            ui_mode = UIMode.GUI
        self._argvals["ui_mode"] = UIMode(ui_mode)
        if self._argvals["start_timeout"] is None:
            self._argvals["start_timeout"] = -1
        if self._argvals["scheduler_options"]:
            if "scheduler" not in self._argvals["scheduler_options"]:
                raise InvalidArgument(
                    "The scheduler must be specified within scheduler options."
                )
            elif self._argvals["scheduler_options"]["scheduler"] != "slurm":
                raise InvalidArgument("Only slurm is supported as scheduler.")
            queue = self._argvals["scheduler_options"].get("scheduler_queue")
            if queue is not None:
                queues = _SlurmWrapper.list_queues()
                if queue not in queues:
                    raise InvalidArgument(
                        f"""Slurm queue is not valid. Valid queues are "{'", "'.join(queues)}"."""
                    )

    def _prepare(self):
        server_info_file_name_for_server, server_info_file_name_for_client = (
            _get_server_info_file_names(use_tmpdir=False)
        )
        self._server_info_file_name = server_info_file_name_for_client
        self._argvals.update(self._argvals["scheduler_options"])
        launch_cmd = _generate_launch_string(
            self._argvals,
            server_info_file_name_for_server,
        )

        self._sifile_last_mtime = Path(self._server_info_file_name).stat().st_mtime
        kwargs = _get_subprocess_kwargs_for_fluent(self._argvals["env"], self._argvals)
        launch_cmd += _build_journal_argument(
            self._argvals["topy"], self._argvals["journal_file_names"]
        )

        logger.debug(f"Launching Fluent with command: {launch_cmd}")
        proc = subprocess.Popen(launch_cmd, **kwargs)
        slurm_job_id = _get_slurm_job_id(proc)
        logger.info(f"Slurm job id = {slurm_job_id}")
        self._argvals["slurm_job_id"] = slurm_job_id
        return slurm_job_id

    def _launch(self, slurm_job_id) -> Meshing | PureMeshing | Solver | SolverIcing:
        _await_fluent_launch(
            self._server_info_file_name,
            self._argvals["start_timeout"],
            self._sifile_last_mtime,
        )
        session = self._new_session._create_from_server_info_file(
            server_info_file_name=self._server_info_file_name,
            file_transfer_service=None,
            cleanup_on_exit=self._argvals["cleanup_on_exit"],
            start_transcript=self._argvals["start_transcript"],
            inside_container=False,
        )
        return session

    def __call__(self) -> SlurmFuture:
        slurm_job_id = self._prepare()
        return SlurmFuture(
            ThreadPoolExecutor(max_workers=1).submit(self._launch, slurm_job_id),
            slurm_job_id,
        )
