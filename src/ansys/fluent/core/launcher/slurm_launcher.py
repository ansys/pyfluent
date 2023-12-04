from concurrent.futures import Future, ThreadPoolExecutor
import logging
from pathlib import Path
import subprocess
from typing import Any, Union

from ansys.fluent.core.exceptions import InvalidArgument
from ansys.fluent.core.launcher.launcher_utils import (
    _await_fluent_launch,
    _build_journal_argument,
    _generate_launch_string,
    _get_argvals,
    _get_server_info_file_name,
    _get_subprocess_kwargs_for_fluent,
    _process_invalid_args,
)
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

    def cancel(self, timeout: int = 60) -> bool:
        if self.done():
            return False
        subprocess.run(["scancel", f"{self._job_id}"])
        for _ in range(timeout):
            if self.cancelled():
                return True
        return False

    def cancelled(self) -> bool:
        return self._get_state() == "CANCELLED"

    def running(self) -> bool:
        return self._get_state() == "RUNNING" and self._future.done()

    def pending(self) -> bool:
        return self._future.running()

    def done(self) -> bool:
        return self._get_state() in ["", "CANCELLED", "COMPLETED"]

    def result(self, timeout=None):
        return self._future.result(timeout)

    def exception(self, timeout=None):
        return self._future.exception(timeout)

    def add_done_callback(self, fn):
        self._future.add_done_callback(fn)


class SlurmLauncher:
    def __init__(
        self,
        **kwargs,
    ):
        dry_run = kwargs.get("dry_run")
        mode = kwargs.get("mode")
        argvals = kwargs.copy()
        del kwargs
        _process_invalid_args(dry_run, "slurm", argvals)
        args = _get_argvals(argvals, mode)
        argvals.update(args)
        if argvals["start_timeout"] is None:
            argvals["start_timeout"] = -1
        for arg_name, arg_values in argvals.items():
            setattr(self, f"_{arg_name}", arg_values)
        self._argvals = argvals

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
            self._meshing_mode,
            self._show_gui,
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
        session = self._new_session.create_from_server_info_file(
            server_info_file_name=self._server_info_file_name,
            remote_file_handler=None,
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
