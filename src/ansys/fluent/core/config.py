# Copyright (C) 2022 - 2025 ANSYS, Inc. and/or its affiliates.
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
"""Configuration variables for PyFluent."""
import os
from pathlib import Path

from ansys.fluent.core.utils import get_examples_download_dir


class Config:
    """Set the global configuration variables for PyFluent."""

    def __init__(self):
        """__init__ method of Config class."""
        # Read the environment variable once when pyfluent is imported
        # and reuse it throughout process lifetime.
        self._env = os.environ.copy()

        # Variables which has some additional logic in getter/setter methods
        # are implemented as properties. Rest of the variables are public attributes.
        # All properties and public attributes returns a valid value.

        # Backend variables of the properties
        self._examples_path = None
        self._codegen_outdir = None
        self._fluent_automatic_transcript = None

        #: Host path which is mounted to the container
        self.container_mount_source = None

        #: Path inside the container where the host path is mounted
        self.container_mount_target = "/home/container/workdir"

        #: Set this to False to stop automatically inferring and setting REMOTING_SERVER_ADDRESS
        self.infer_remoting_ip = True

        # Time in second to wait for response for each ip while inferring remoting ip
        self.infer_remoting_ip_timeout_per_ip = 2

        #: Whether to use datamodel state caching
        self.datamodel_use_state_cache = True

        #: Whether to use datamodel attribute caching
        self.datamodel_use_attr_cache = True

        #: Whether to stream and cache commands state
        self.datamodel_use_nocommands_diff_state = True

        #: Whether to return the state changes on mutating datamodel RPCs
        self.datamodel_return_state_changes = True

        #: Whether to use remote gRPC file transfer service
        self.use_file_transfer_service = False

        #: Whether to show mesh in Fluent after case read
        self.fluent_show_mesh_after_case_read = False

        #: Whether to interrupt Fluent solver from PyFluent
        self.support_solver_interrupt = False

        #: Whether to start watchdog
        self.start_watchdog = None

        #: Health check timeout in seconds
        self.check_health_timeout = 60

        #: Whether to skip health check
        self.check_health = True

        #: Whether to print search results
        self.print_search_results = True

        #: Whether to clear environment variables related to Fluent parallel mode
        self.clear_fluent_para_envs = False

        #: Set stdout of the launched Fluent process
        #: Valid values are the same as subprocess.Popen's stdout argument
        self.launch_fluent_stdout = None

        #: Set stderr of the launched Fluent process
        #: Valid values are the same as subprocess.Popen's stderr argument
        self.launch_fluent_stderr = None

        #: Set the IP address of the Fluent server while launching Fluent
        self.launch_fluent_ip = None

        #: Set the port of the Fluent server while launching Fluent
        self.launch_fluent_port = None

        #: Skip password check during RPC execution when Fluent is launched from PyFluent
        self.launch_fluent_skip_password_check = False

    @property
    def fluent_release_version(self) -> str:
        """The latest released version of Fluent."""
        return "25.2.0"

    @property
    def fluent_dev_version(self) -> str:
        """The latest development version of Fluent."""
        return "26.1.0"

    @property
    def examples_path(self) -> str:
        """The path to the example input/data files are downloaded."""
        if self._examples_path is None:
            self._examples_path = str(get_examples_download_dir())
        return self._examples_path

    @examples_path.setter
    def examples_path(self, val: str) -> None:
        """Set the path to the example input/data files are downloaded."""
        self._examples_path = val

    @property
    def codegen_outdir(self) -> str:
        """The directory where API files are written out during codegen."""
        if self._codegen_outdir is None:
            self._codegen_outdir = self._env.get(
                "PYFLUENT_CODEGEN_OUTDIR",
                (Path(__file__) / ".." / "generated").resolve(),
            )
        return self._codegen_outdir

    @codegen_outdir.setter
    def codegen_outdir(self, val: str) -> None:
        """Set the directory where API files are written out during codegen."""
        self._codegen_outdir = val

    @property
    def fluent_automatic_transcript(self) -> bool:
        """Whether to write the automatic transcript in Fluent."""
        return self._env.get("PYFLUENT_FLUENT_AUTOMATIC_TRANSCRIPT") == "1"

    @fluent_automatic_transcript.setter
    def fluent_automatic_transcript(self, val: bool) -> None:
        """Set whether to write the automatic transcript in Fluent."""
        self._fluent_automatic_transcript = val
