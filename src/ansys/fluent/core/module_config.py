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
import inspect
import os
from pathlib import Path
from typing import Any, Callable, Generic, TypeVar
import warnings

TConfig = TypeVar("TConfig", bound="Config")


class _ConfigDescriptor(Generic[TConfig]):
    """Descriptor for managing configuration attributes."""

    def __init__(
        self, default_fn: Callable[[TConfig], Any], deprecated_var: str | None = None
    ):
        self._default_fn = default_fn
        self._deprecated_var = deprecated_var

    def _get_config(self, instance: TConfig) -> Any:
        if not hasattr(instance, self._backing_field):
            setattr(instance, self._backing_field, self._default_fn(instance))
        return getattr(instance, self._backing_field)

    def _set_config(self, instance: TConfig, value: Any):
        setattr(instance, self._backing_field, value)

    def __set_name__(self, owner: type[TConfig], name: str):
        self._backing_field = "_" + name

    def __get__(self, instance: TConfig, owner: type[TConfig]) -> Any:
        import ansys.fluent.core as pyfluent

        if self._deprecated_var is not None and self._deprecated_var in vars(pyfluent):
            return getattr(pyfluent, self._deprecated_var)
        return self._get_config(instance)

    def __set__(self, instance: TConfig, value: Any):
        import ansys.fluent.core as pyfluent

        if self._deprecated_var is not None and self._deprecated_var in vars(pyfluent):
            warnings.warn(
                f"Deleting deprecated module-level variable '{self._deprecated_var}' which was previously set."
            )
            delattr(pyfluent, self._deprecated_var)
        self._set_config(instance, value)


def _get_default_examples_path(instance: "Config") -> str:
    """Get the default examples path."""
    parent_path = Path.home() / "Downloads"
    parent_path.mkdir(exist_ok=True)
    return str(parent_path / "ansys_fluent_core_examples")


class Config:
    """Set the global configuration variables for PyFluent."""

    #: Directory where example files are downloaded.
    examples_path = _ConfigDescriptor["Config"](
        _get_default_examples_path, "EXAMPLES_PATH"
    )

    #: Host path which is mounted to the container, defaults to the value of ``PYFLUENT_CONTAINER_MOUNT_SOURCE`` environment variable.
    container_mount_source = _ConfigDescriptor["Config"](
        lambda instance: instance._env.get("PYFLUENT_CONTAINER_MOUNT_SOURCE"),
        "CONTAINER_MOUNT_SOURCE",
    )

    #: Path inside the container where the host path is mounted, defaults to "/home/container/workdir".
    container_mount_target = _ConfigDescriptor["Config"](
        lambda instance: "/home/container/workdir", "CONTAINER_MOUNT_TARGET"
    )

    #: Set this to False to stop automatically inferring and setting REMOTING_SERVER_ADDRESS, defaults to True.
    infer_remoting_ip = _ConfigDescriptor["Config"](
        lambda instance: True, "INFER_REMOTING_IP"
    )

    # Time in seconds to wait for response for each ip while inferring remoting ip, defaults to 2.
    infer_remoting_ip_timeout_per_ip = _ConfigDescriptor["Config"](
        lambda instance: 2, "INFER_REMOTING_IP_TIMEOUT_PER_IP"
    )

    #: Whether to use datamodel state caching, defaults to True.
    datamodel_use_state_cache = _ConfigDescriptor["Config"](
        lambda instance: True, "DATAMODEL_USE_STATE_CACHE"
    )

    #: Whether to use datamodel attribute caching, defaults to True.
    datamodel_use_attr_cache = _ConfigDescriptor["Config"](
        lambda instance: True, "DATAMODEL_USE_ATTR_CACHE"
    )

    #: Whether to stream and cache commands state, defaults to True.
    datamodel_use_nocommands_diff_state = _ConfigDescriptor["Config"](
        lambda instance: True, "DATAMODEL_USE_NOCOMMANDS_DIFF_STATE"
    )

    #: Whether to return the state changes on mutating datamodel RPCs, defaults to True.
    datamodel_return_state_changes = _ConfigDescriptor["Config"](
        lambda instance: True, "DATAMODEL_RETURN_STATE_CHANGES"
    )

    #: Whether to use remote gRPC file transfer service, defaults to False.
    use_file_transfer_service = _ConfigDescriptor["Config"](
        lambda instance: False, "USE_FILE_TRANSFER_SERVICE"
    )

    #: Directory where API files are written out during codegen.
    codegen_outdir = _ConfigDescriptor["Config"](
        lambda instance: instance._env.get(
            "PYFLUENT_CODEGEN_OUTDIR", (Path(__file__) / ".." / "generated").resolve()
        ),
        "CODEGEN_OUTDIR",
    )

    #: Whether to show mesh in Fluent after case read, defaults to False.
    fluent_show_mesh_after_case_read = _ConfigDescriptor["Config"](
        lambda instance: False, "FLUENT_SHOW_MESH_AFTER_CASE_READ"
    )

    #: Whether to write the automatic transcript in Fluent, defaults to True if ``PYFLUENT_SKIP_FLUENT_AUTOMATIC_TRANSCRIPT`` environment variable is not set to "1".
    fluent_automatic_transcript = _ConfigDescriptor["Config"](
        lambda instance: instance._env.get("PYFLUENT_SKIP_FLUENT_AUTOMATIC_TRANSCRIPT")
        != "1",
        "FLUENT_AUTOMATIC_TRANSCRIPT",
    )

    #: Whether to interrupt Fluent solver from PyFluent, defaults to False.
    support_solver_interrupt = _ConfigDescriptor["Config"](
        lambda instance: False, "SUPPORT_SOLVER_INTERRUPT"
    )

    #: Whether to start watchdog.
    start_watchdog = _ConfigDescriptor["Config"](
        lambda instance: None, "START_WATCHDOG"
    )

    #: Whether to enable debug logging for the watchdog, defaults to the value of ``PYFLUENT_WATCHDOG_DEBUG`` environment variable.
    watchdog_debug = _ConfigDescriptor["Config"](
        lambda instance: instance._env.get("PYFLUENT_WATCHDOG_DEBUG") == "1",
        "WATCHDOG_DEBUG",
    )

    #: Whether to raise an exception when the watchdog encounters an error, defaults to the value of ``PYFLUENT_WATCHDOG_EXCEPTION_ON_ERROR`` environment variable.
    watchdog_exception_on_error = _ConfigDescriptor["Config"](
        lambda instance: instance._env.get("PYFLUENT_WATCHDOG_EXCEPTION_ON_ERROR")
        == "1",
        "WATCHDOG_EXCEPTION_ON_ERROR",
    )

    #: Health check timeout in seconds, defaults to 60 seconds.
    check_health_timeout = _ConfigDescriptor["Config"](
        lambda instance: 60, "CHECK_HEALTH_TIMEOUT"
    )

    #: Whether to skip health check, defaults to True.
    check_health = _ConfigDescriptor["Config"](lambda instance: True, "CHECK_HEALTH")

    #: Whether to print search results, defaults to True.
    print_search_results = _ConfigDescriptor["Config"](
        lambda instance: True, "PRINT_SEARCH_RESULTS"
    )

    #: Whether to clear environment variables related to Fluent parallel mode, defaults to False.
    clear_fluent_para_envs = _ConfigDescriptor["Config"](
        lambda instance: False, "CLEAR_FLUENT_PARA_ENVS"
    )

    #: Set stdout of the launched Fluent process.
    #: Valid values are the same as subprocess.Popen's stdout argument.
    launch_fluent_stdout = _ConfigDescriptor["Config"](
        lambda instance: None, "LAUNCH_FLUENT_STDOUT"
    )

    #: Set stderr of the launched Fluent process.
    #: Valid values are the same as subprocess.Popen's stderr argument.
    launch_fluent_stderr = _ConfigDescriptor["Config"](
        lambda instance: None, "LAUNCH_FLUENT_STDERR"
    )

    #: Set the IP address of the Fluent server while launching Fluent, defaults to the value of ``PYFLUENT_FLUENT_IP`` environment variable.
    launch_fluent_ip = _ConfigDescriptor["Config"](
        lambda instance: instance._env.get("PYFLUENT_FLUENT_IP"), "LAUNCH_FLUENT_IP"
    )

    #: Set the port of the Fluent server while launching Fluent, defaults to the value of ``PYFLUENT_FLUENT_PORT`` environment variable.
    launch_fluent_port = _ConfigDescriptor["Config"](
        lambda instance: instance._env.get("PYFLUENT_FLUENT_PORT"), "LAUNCH_FLUENT_PORT"
    )

    #: Skip password check during RPC execution when Fluent is launched from PyFluent, defaults to False.
    launch_fluent_skip_password_check = _ConfigDescriptor["Config"](
        lambda instance: False, "LAUNCH_FLUENT_SKIP_PASSWORD_CHECK"
    )

    #: The timeout in seconds to wait for Fluent to exit, defaults to the value of ``PYFLUENT_FORCE_EXIT_TIMEOUT`` environment variable.
    force_exit_timeout = _ConfigDescriptor["Config"](
        lambda instance: instance._env.get("PYFLUENT_FORCE_EXIT_TIMEOUT")
    )

    #: Whether to skip code generation of built-in settings, defaults to the value of ``PYFLUENT_CODEGEN_SKIP_BUILTIN_SETTINGS`` environment variable.
    codegen_skip_builtin_settings = _ConfigDescriptor["Config"](
        lambda instance: instance._env.get("PYFLUENT_CODEGEN_SKIP_BUILTIN_SETTINGS")
        == "1"
    )

    #: Whether to launch Fluent in a container, defaults to the value of ``PYFLUENT_LAUNCH_CONTAINER`` environment variable.
    launch_fluent_container = _ConfigDescriptor["Config"](
        lambda instance: instance._env.get("PYFLUENT_LAUNCH_CONTAINER") == "1"
    )

    #: The tag of the Fluent image to use when launching in a container, defaults to the value of ``FLUENT_IMAGE_TAG`` environment variable or the latest release version of Fluent.
    fluent_image_tag = _ConfigDescriptor["Config"](
        lambda instance: instance._env.get(
            "FLUENT_IMAGE_TAG", f"v{instance.fluent_release_version}"
        )
    )

    #: The name of the Fluent image to use when launching in a container, defaults to the value of ``FLUENT_IMAGE_NAME`` environment variable.
    fluent_image_name = _ConfigDescriptor["Config"](
        lambda instance: instance._env.get("FLUENT_IMAGE_NAME")
    )

    #: The name of the Fluent container to use when launching in a container, defaults to the value of ``FLUENT_CONTAINER_NAME`` environment variable.
    fluent_container_name = _ConfigDescriptor["Config"](
        lambda instance: instance._env.get("FLUENT_CONTAINER_NAME")
    )

    #: Whether to use Docker Compose for launching Fluent in a container, defaults to the value of ``PYFLUENT_USE_DOCKER_COMPOSE`` environment variable.
    use_docker_compose = _ConfigDescriptor["Config"](
        lambda instance: instance._env.get("PYFLUENT_USE_DOCKER_COMPOSE") == "1"
    )

    #: Whether to use Podman Compose for launching Fluent in a container, defaults to the value of ``PYFLUENT_USE_PODMAN_COMPOSE`` environment variable.
    use_podman_compose = _ConfigDescriptor["Config"](
        lambda instance: instance._env.get("PYFLUENT_USE_PODMAN_COMPOSE") == "1"
    )

    #: The timeout in seconds to wait for Fluent to launch, defaults to the value of ``PYFLUENT_LAUNCH_FLUENT_TIMEOUT`` environment variable or 60 seconds.
    launch_fluent_timeout = _ConfigDescriptor["Config"](
        lambda instance: int(instance._env.get("PYFLUENT_LAUNCH_FLUENT_TIMEOUT", 60))
    )

    #: Whether to show the Fluent GUI when launching the server, defaults to the value of ``PYFLUENT_SHOW_SERVER_GUI`` environment variable.
    show_fluent_gui = _ConfigDescriptor["Config"](
        lambda instance: instance._env.get("PYFLUENT_SHOW_SERVER_GUI") == "1"
    )

    #: Whether to launch Fluent in debug mode, defaults to the value of ``PYFLUENT_FLUENT_DEBUG`` environment variable.
    fluent_debug = _ConfigDescriptor["Config"](
        lambda instance: instance._env.get("PYFLUENT_FLUENT_DEBUG") == "1"
    )

    #: Whether to skip API upgrade advice, defaults to the value of ``PYFLUENT_SKIP_API_UPGRADE_ADVICE`` environment variable.
    skip_api_upgrade_advice = _ConfigDescriptor["Config"](
        lambda instance: instance._env.get("PYFLUENT_SKIP_API_UPGRADE_ADVICE") == "1"
    )

    #: The maximum number of bytes to log in gRPC logs, defaults to the value of ``PYFLUENT_GRPC_LOG_BYTES_LIMIT`` environment variable or 1000 bytes.
    grpc_log_bytes_limit = _ConfigDescriptor["Config"](
        lambda instance: int(instance._env.get("PYFLUENT_GRPC_LOG_BYTES_LIMIT", 1000))
    )

    #: Whether to disable the fix for returning parameter lists via settings API, defaults to the value of ``PYFLUENT_NO_FIX_PARAMETER_LIST_RETURN`` environment variable.
    disable_parameter_list_return_fix = _ConfigDescriptor["Config"](
        lambda instance: instance._env.get("PYFLUENT_NO_FIX_PARAMETER_LIST_RETURN")
        == "1"
    )

    #: Whether to use runtime Python classes for settings, defaults to the value of ``PYFLUENT_USE_RUNTIME_PYTHON_CLASSES`` environment variable.
    use_runtime_python_classes = _ConfigDescriptor["Config"](
        lambda instance: instance._env.get("PYFLUENT_USE_RUNTIME_PYTHON_CLASSES") == "1"
    )

    #: Whether to hide sensitive information in logs, defaults to the value of ``PYFLUENT_HIDE_LOG_SECRETS`` environment variable.
    hide_log_secrets = _ConfigDescriptor["Config"](
        lambda instance: instance._env.get("PYFLUENT_HIDE_LOG_SECRETS") == "1"
    )

    #: The remoting server address to be used in Fluent, defaults to the value of ``REMOTING_SERVER_ADDRESS`` environment variable.
    remoting_server_address = _ConfigDescriptor["Config"](
        lambda instance: instance._env.get("REMOTING_SERVER_ADDRESS")
    )

    #: The directory where server info will be written from Fluent, defaults to the value of ``SERVER_INFO_DIR`` environment variable.
    fluent_server_info_dir = _ConfigDescriptor["Config"](
        lambda instance: instance._env.get("SERVER_INFO_DIR")
    )

    #: Current unit test name, defaults to the value of ``PYFLUENT_TEST_NAME`` environment variable.
    test_name = _ConfigDescriptor["Config"](
        lambda instance: instance._env.get("PYFLUENT_TEST_NAME")
    )

    #: The default logging level for PyFluent, defaults to the value of ``PYFLUENT_LOGGING`` environment variable.
    logging_level_default = _ConfigDescriptor["Config"](
        lambda instance: instance._env.get("PYFLUENT_LOGGING")
    )

    #: Whether to disable monitor refresh on solution initialization, defaults to False.
    disable_monitor_refresh_on_init = _ConfigDescriptor["Config"](
        lambda instance: False
    )

    def __init__(self):
        """__init__ method of Config class."""
        # Read the environment variable once when pyfluent is imported
        # and reuse it throughout process lifetime.
        self._env = os.environ.copy()

    @property
    def fluent_release_version(self) -> str:
        """The latest released version of Fluent."""
        return "25.2.0"

    @property
    def fluent_dev_version(self) -> str:
        """The latest development version of Fluent."""
        return "26.1.0"

    def print(self):
        """Print all configuration variables."""
        config_dict = {}
        for k, v in inspect.getmembers_static(self):
            if isinstance(v, (_ConfigDescriptor, property)):
                config_dict[k] = v.__get__(self, self.__class__)
        max_key_length = max(len(k) for k in config_dict)
        print("PyFluent Configuration:")
        print("-" * (max_key_length + 20))
        for k, v in config_dict.items():
            print(f"{k.ljust(max_key_length)} : {v}")


#: Global configuration object for PyFluent
config = Config()
