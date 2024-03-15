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
"""

from concurrent.futures import Future, ThreadPoolExecutor
import logging
from pathlib import Path
import subprocess
import time
from typing import Any, Callable, Union

from ansys.fluent.core.exceptions import InvalidArgument
from ansys.fluent.core.launcher.error_handler import _process_invalid_args
from ansys.fluent.core.launcher.launcher_utils import (
    _await_fluent_launch,
    _build_journal_argument,
    _get_subprocess_kwargs_for_fluent,
)
from ansys.fluent.core.launcher.process_launch_string import _generate_launch_string
from ansys.fluent.core.launcher.pyfluent_enums import _get_mode
from ansys.fluent.core.launcher.server_info import _get_server_info_file_name
from ansys.fluent.core.session_meshing import Meshing
from ansys.fluent.core.session_pure_meshing import PureMeshing
from ansys.fluent.core.session_solver import Solver
from ansys.fluent.core.session_solver_icing import SolverIcing

logger = logging.getLogger("pyfluent.launcher")


def _get_slurm_job_id(proc: subprocess.Popen):
    prefix = "Submitted batch job"
    for line in proc.stdout:
        if line.startswith(prefix.encode()):
            line = line.decode().removeprefix(prefix).strip()
            return int(line)


class SlurmFuture:
    """Encapsulates asynchronous launch of Fluent within a Slurm environment.

    The interface is similar to Python's
    `future object <https://docs.python.org/3/library/asyncio-future.html#future-object>`_.
    """

    def __init__(self, future: Future, job_id: int):
        self._future = future
        self._job_id = job_id

    def __enter__(self):
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any):
        self.cancel()

    def _get_state(self) -> str:
        out = subprocess.check_output(
            ["squeue", "-j", f"{self._job_id}", "-o", '"%T"', "-h"]
        )
        return out.decode().strip().strip('"')

    def _cancel(self):
        subprocess.run(["scancel", f"{self._job_id}"])

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
    ) -> Union[Meshing, PureMeshing, Solver, SolverIcing]:
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
        **kwargs,
    ):
        dry_run = kwargs.get("dry_run")
        mode = kwargs.get("mode")
        argvals = kwargs.copy()
        del kwargs
        _process_invalid_args(dry_run, "slurm", argvals)
        if argvals["start_timeout"] is None:
            argvals["start_timeout"] = -1
        for arg_name, arg_values in argvals.items():
            setattr(self, f"_{arg_name}", arg_values)
        self._argvals = argvals
        self.mode = _get_mode(mode)
        self._new_session = self.mode.value[0]

        if self._scheduler_options:
            if "scheduler" not in self._scheduler_options:
                raise InvalidArgument(
                    "The scheduler must be specified within scheduler options."
                )
            elif self._scheduler_options["scheduler"] != "slurm":
                raise InvalidArgument("Only slurm is supported as scheduler.")

    def _prepare(self):
        self._server_info_file_name = _get_server_info_file_name(use_tmpdir=False)
        self._argvals.update(self._argvals["scheduler_options"])
        launch_cmd = _generate_launch_string(
            self._argvals,
            self.mode,
            self._additional_arguments,
            self._server_info_file_name,
        )

        self._sifile_last_mtime = Path(self._server_info_file_name).stat().st_mtime
        if self._env is None:
            self._env = {}
        kwargs = _get_subprocess_kwargs_for_fluent(self._env, self._argvals)
        launch_cmd += _build_journal_argument(self._topy, self._journal_file_names)

        logger.debug(f"Launching Fluent with command: {launch_cmd}")
        proc = subprocess.Popen(launch_cmd, **kwargs)
        slurm_job_id = _get_slurm_job_id(proc)
        logger.info(f"Slurm job id = {slurm_job_id}")
        self._argvals["slurm_job_id"] = slurm_job_id
        return slurm_job_id

    def _launch(self, slurm_job_id) -> Union[Meshing, PureMeshing, Solver, SolverIcing]:
        _await_fluent_launch(
            self._server_info_file_name, self._start_timeout, self._sifile_last_mtime
        )
        session = self._new_session._create_from_server_info_file(
            server_info_file_name=self._server_info_file_name,
            file_transfer_service=None,
            cleanup_on_exit=self._cleanup_on_exit,
            start_transcript=self._start_transcript,
            inside_container=False,
        )
        return session

    def __call__(self) -> SlurmFuture:
        slurm_job_id = self._prepare()
        return SlurmFuture(
            ThreadPoolExecutor(max_workers=1).submit(self._launch, slurm_job_id),
            slurm_job_id,
        )
