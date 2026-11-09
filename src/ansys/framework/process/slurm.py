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

"""Slurm job control for servers launched through a Slurm scheduler."""

from __future__ import annotations

from collections.abc import Iterable
import shutil
import subprocess

_SUBMITTED_PREFIX = b"Submitted batch job"


def read_job_id(lines: Iterable[bytes]) -> int | None:
    """Return the job ID from ``sbatch`` output, or ``None`` if it is not found.

    Reading stops at the line that reports the submitted job.
    """
    for line in lines:
        if line.startswith(_SUBMITTED_PREFIX):
            return int(line.decode().removeprefix(_SUBMITTED_PREFIX.decode()).strip())
    return None


class SlurmScheduler:
    """Slurm commands run from the current machine."""

    @classmethod
    def is_available(cls) -> bool:
        """Return whether Slurm is installed and has at least one queue."""
        return shutil.which("sinfo") is not None and len(cls.list_queues()) > 0

    @staticmethod
    def list_queues() -> list[str]:
        """Return the names of the Slurm queues (partitions)."""
        out = subprocess.check_output(["sinfo", "--format=%P", "--noheader"])
        return [q.removesuffix("*") for q in out.decode().strip().split()]

    @staticmethod
    def get_state(job_id: int) -> str:
        """Return the state of a job.

        Returns
        -------
        str
            Any of ``""``, ``"RUNNING"``, ``"CANCELLED"`` or ``"COMPLETED"``.
        """
        out = subprocess.check_output(["squeue", "-j", f"{job_id}", "-o", '"%T"', "-h"])
        return out.decode().strip().strip('"')

    @staticmethod
    def cancel(job_id: int) -> None:
        """Cancel a job."""
        subprocess.run(["scancel", f"{job_id}"])
