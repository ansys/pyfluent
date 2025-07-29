# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
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
from typing import Any, Callable
import warnings


class _ConfigDescriptor:
    """Descriptor for managing configuration attributes."""

    def __init__(self, default_fn: Callable[[], Any], deprecated_var: str):
        self._default_fn = default_fn
        self._deprecated_var = deprecated_var
        self._backing_field = f"_{self._deprecated_var.lower()}"

    def _get_config(self, instance):
        if not hasattr(instance, self._backing_field):
            instance._backing_field = self._default_fn()
        return instance._backing_field

    def _set_config(self, instance, value):
        instance._backing_field = value

    def __get__(self, instance, owner):
        import ansys.fluent.core as pyfluent

        if self._deprecated_var in vars(pyfluent):
            return getattr(pyfluent, self._deprecated_var)
        return self._get_config(instance)

    def __set__(self, instance, value):
        import ansys.fluent.core as pyfluent

        if self._deprecated_var in vars(pyfluent):
            warnings.warn(
                f"Deleting deprecated variable '{self._deprecated_var}' which was previously set."
            )
            delattr(pyfluent, self._deprecated_var)
        self._set_config(instance, value)


def _get_default_examples_path() -> str:
    """Get the default examples path."""
    parent_path = Path.home() / "Downloads"
    parent_path.mkdir(exist_ok=True)
    return str(parent_path / "ansys_fluent_core_examples")


class Config:
    """Set the global configuration variables for PyFluent."""

    #: Directory where example files are downloaded
    examples_path = _ConfigDescriptor(_get_default_examples_path, "EXAMPLES_PATH")

    def __init__(self):
        """__init__ method of Config class."""
        # Read the environment variable once when pyfluent is imported
        # and reuse it throughout process lifetime.
        self._env = os.environ.copy()

        #: Host path which is mounted to the container
        self.container_mount_source = self._env.get("PYFLUENT_CONTAINER_MOUNT_SOURCE")

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

        #: Directory where API files are written out during codegen
        self.codegen_outdir = self._env.get(
            "PYFLUENT_CODEGEN_OUTDIR",
            (Path(__file__) / ".." / "generated").resolve(),
        )

        #: Whether to show mesh in Fluent after case read
        self.fluent_show_mesh_after_case_read = False

        #: Whether to write the automatic transcript in Fluent.
        self.fluent_automatic_transcript = (
            self._env.get("PYFLUENT_FLUENT_AUTOMATIC_TRANSCRIPT") == "1"
        )

        #: Whether to interrupt Fluent solver from PyFluent
        self.support_solver_interrupt = False

        #: Whether to start watchdog
        self.start_watchdog = None

        #: Whether to enable debug logging for the watchdog
        self.watchdog_debug = self._env.get("PYFLUENT_WATCHDOG_DEBUG") == "1"

        #: Whether to raise an exception when the watchdog encounters an error
        self.watchdog_exception_on_error = (
            self._env.get("PYFLUENT_WATCHDOG_EXCEPTION_ON_ERROR") == "1"
        )

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
        self.launch_fluent_ip = self._env.get("PYFLUENT_FLUENT_IP")

        #: Set the port of the Fluent server while launching Fluent
        self.launch_fluent_port = self._env.get("PYFLUENT_FLUENT_PORT")

        #: Skip password check during RPC execution when Fluent is launched from PyFluent
        self.launch_fluent_skip_password_check = False

        #: The timeout in seconds to wait for Fluent to exit.
        self.force_exit_timeout = self._env.get("PYFLUENT_FORCE_EXIT_TIMEOUT")

        #: Whether to skip code generation of built-in settings.
        self.codegen_skip_builtin_settings = (
            self._env.get("PYFLUENT_CODEGEN_SKIP_BUILTIN_SETTINGS") == "1"
        )

        #: Whether to launch Fluent in a container.
        self.launch_fluent_container = self._env.get("PYFLUENT_LAUNCH_CONTAINER") == "1"

        #: The tag of the Fluent image to use when launching in a container.
        self.fluent_image_tag = self._env.get(
            "FLUENT_IMAGE_TAG", f"v{self.fluent_release_version}"
        )

        #: The name of the Fluent image to use when launching in a container.
        self.fluent_image_name = self._env.get("FLUENT_IMAGE_NAME")

        #: The name of the Fluent container to use when launching in a container.
        self.fluent_container_name = self._env.get("FLUENT_CONTAINER_NAME")

        #: Whether to use Docker Compose for launching Fluent in a container.
        self.use_docker_compose = self._env.get("PYFLUENT_USE_DOCKER_COMPOSE") == "1"

        #: Whether to use Podman Compose for launching Fluent in a container.
        self.use_podman_compose = self._env.get("PYFLUENT_USE_PODMAN_COMPOSE") == "1"

        #: The timeout in seconds to wait for Fluent to launch.
        self.launch_fluent_timeout = int(
            self._env.get("PYFLUENT_LAUNCH_FLUENT_TIMEOUT", 60)
        )

        #: Whether to show the Fluent GUI when launching the server.
        self.show_fluent_gui = self._env.get("PYFLUENT_SHOW_SERVER_GUI") == "1"

        #: Whether to launch Fluent in debug mode.
        self.fluent_debug = self._env.get("PYFLUENT_FLUENT_DEBUG") == "1"

        #: Whether to skip API upgrade advice.
        self.skip_api_upgrade_advice = (
            self._env.get("PYFLUENT_SKIP_API_UPGRADE_ADVICE") == "1"
        )

        #: The maximum number of bytes to log in gRPC logs.
        self.grpc_log_bytes_limit = int(
            self._env.get("PYFLUENT_GRPC_LOG_BYTES_LIMIT", 1000)
        )

        #: Whether to disable the fix for returning parameter lists via settings API.
        self.disable_parameter_list_return_fix = (
            self._env.get("PYFLUENT_NO_FIX_PARAMETER_LIST_RETURN") == "1"
        )

        #: Whether to use runtime Python classes for settings.
        self.use_runtime_python_classes = (
            self._env.get("PYFLUENT_USE_RUNTIME_PYTHON_CLASSES") == "1"
        )

        #: Whether to hide sensitive information in logs.
        self.hide_log_secrets = self._env.get("PYFLUENT_HIDE_LOG_SECRETS") == "1"

        #: The Fluent root directory to be used for PyFluent.
        self.fluent_root = self._env.get("PYFLUENT_FLUENT_ROOT")

        #: The Ansys license path to be used in Fluent.
        self.ansyslmd_license_file = self._env.get("ANSYSLMD_LICENSE_FILE")

        #: The remoting server address to be used in Fluent.
        self.remoting_server_address = self._env.get("REMOTING_SERVER_ADDRESS")

        #: The directory where server info will be written from Fluent.
        self.fluent_server_info_dir = self._env.get("SERVER_INFO_DIR")

        #: Current unit test name, if any.
        self.test_name = self._env.get("PYFLUENT_TEST_NAME")

        #: The default logging level for PyFluent.
        self.logging_level_default = self._env.get("PYFLUENT_LOGGING")

    @property
    def fluent_release_version(self) -> str:
        """The latest released version of Fluent."""
        return "25.2.0"

    @property
    def fluent_dev_version(self) -> str:
        """The latest development version of Fluent."""
        return "26.1.0"


# Global configuration object for PyFluent
config = Config()
