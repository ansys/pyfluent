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

"""Provides a module for launching and configuring local Fluent Docker container runs.

Notes
-----

For configuration details, see :func:`configure_container_dict`, and for a list of additional Docker container run
configuration options that can also be specified through the
``container_dict`` argument for :func:`~ansys.fluent.core.launcher.launcher.launch_fluent()`,
see documentation for `Docker run`_.

For the Fluent Docker container to be able to find license information, the license file or server needs to be specified
through the ``ANSYSLMD_LICENSE_FILE`` environment variable,
or the ``license_server`` argument for the ``container_dict`` (see :func:`configure_container_dict`).

.. _Docker run: https://docker-py.readthedocs.io/en/stable/containers.html#docker.models.containers.ContainerCollection.run

Examples
--------
Launching a Fluent Docker container with system default configuration:

>>> import ansys.fluent.core as pyfluent
>>> session = pyfluent.launch_fluent(start_container=True)

Launching with custom configuration, using ``mount_source`` and ``fluent_image``
which are arguments for :func:`configure_container_dict`, and ``auto_remove`` which is an argument for `Docker run`_:

>>> import ansys.fluent.core as pyfluent
>>> custom_config = {}
>>> custom_config.update(fluent_image='custom_fluent:v23.1.0', mount_source='/testing', auto_remove=False)
>>> session = pyfluent.launch_fluent(container_dict=custom_config)

Getting default Fluent Docker container configuration, then launching with customized configuration:

>>> import ansys.fluent.core as pyfluent
>>> config_dict = pyfluent.launch_fluent(start_container=True, dry_run=True)
Docker container run configuration information:
config_dict =
{'auto_remove': True,
 'command': ['-gu', '-sifile=/mnt/pyfluent/serverinfo-lpqsdldw.txt', '3ddp'],
 'detach': True,
 'environment': {'ANSYSLMD_LICENSE_FILE': '2048@licenseserver.com',
                 'REMOTING_PORTS': '54000/portspan=2'},
 'fluent_image': '<image registry>:v23.2.0',
 'labels': {'test_name': 'none'},
 'ports': {'54000': 54000},
 'volumes': ['/home/user/.local/share/ansys_fluent_core/examples:/mnt/pyfluent'],
 'working_dir': '/mnt/pyfluent'}
>>> config_dict.update(image_name='custom_fluent', image_tag='v23.1.0', mem_limit='1g')
>>> session = pyfluent.launch_fluent(container_dict=config_dict)
"""

import logging
import os
from pathlib import Path, PurePosixPath
from pprint import pformat
import tempfile
from typing import Any, List
import warnings

import ansys.fluent.core as pyfluent
from ansys.fluent.core.docker.docker_compose import ComposeBasedLauncher
from ansys.fluent.core.docker.utils import get_ghcr_fluent_image_name
from ansys.fluent.core.launcher.error_handler import (
    LaunchFluentError,
)
from ansys.fluent.core.launcher.launcher_utils import ComposeConfig
from ansys.fluent.core.pyfluent_warnings import PyFluentDeprecationWarning
from ansys.fluent.core.session import _parse_server_info_file
from ansys.fluent.core.utils.deprecate import all_deprecators
from ansys.fluent.core.utils.execution import timeout_loop
from ansys.fluent.core.utils.networking import get_free_port

logger = logging.getLogger("pyfluent.launcher")


class FluentImageNameTagNotSpecified(ValueError):
    """Raised when Fluent image name or image tag is not specified."""

    def __init__(self):
        """Initializes FluentImageNameTagNotSpecified."""
        super().__init__(
            "Specify either 'fluent_image' or 'image_tag' and 'image_name'."
        )


class ServerInfoFileError(ValueError):
    """Raised when server info file is not given properly."""

    def __init__(self):
        """Initializes ServerInfoFileError."""
        super().__init__(
            "Specify server info file either using 'container_server_info_file' argument or in the 'container_dict'."
        )


class LicenseServerNotSpecified(KeyError):
    """Raised when license server is not specified."""

    def __init__(self):
        """Initializes LicenseServerNotSpecified."""
        super().__init__(
            "Specify licence server either using 'ANSYSLMD_LICENSE_FILE' environment variable or in the 'container_dict'."
        )


def dict_to_str(dict: dict) -> str:
    """Converts the dict to string while hiding the 'environment' argument from the dictionary,
    if the environment variable 'PYFLUENT_HIDE_LOG_SECRETS' is '1'.
    This is useful for logging purposes, to avoid printing sensitive information such as license server details.
    """

    if "environment" in dict and pyfluent.config.hide_log_secrets:
        modified_dict = dict.copy()
        modified_dict.pop("environment")
        return pformat(modified_dict)
    else:
        return pformat(dict)


@all_deprecators(
    deprecate_arg_mappings=[
        {
            "old_arg": "container_mount_path",
            "new_arg": "mount_target",
            "converter": lambda old_arg_val: old_arg_val,
        },
        {
            "old_arg": "host_mount_path",
            "new_arg": "mount_source",
            "converter": lambda old_arg_val: old_arg_val,
        },
    ],
    data_type_converter=None,
    deprecated_version="v0.23.dev1",
    deprecated_reason="'container_mount_path' and 'host_mount_path' are deprecated. Use 'mount_target' and 'mount_source' instead.",
    warn_message="",
)
def configure_container_dict(
    args: List[str],
    mount_source: str | Path | None = None,
    mount_target: str | Path | None = None,
    timeout: int | None = None,
    port: int | None = None,
    license_server: str | None = None,
    container_server_info_file: str | Path | None = None,
    remove_server_info_file: bool = True,
    fluent_image: str | None = None,
    image_name: str | None = None,
    image_tag: str | None = None,
    file_transfer_service: Any | None = None,
    compose_config: ComposeConfig | None = None,
    **container_dict,
) -> (dict, int, int, Path, bool):
    """Parses the parameters listed below, and sets up the container configuration file.

    Parameters
    ----------
    args : List[str]
        List of Fluent launch arguments.
    mount_source : str | Path, optional
        Path on the host system to mount into the container. This directory will serve as the working directory
        for the Fluent process inside the container. If not specified, PyFluent's current working directory will
        be used.
    mount_target : str | Path, optional
        Path inside the container where ``mount_source`` will be mounted. This will be the working directory path
        visible to the Fluent process running inside the container.
    timeout : int, optional
        Time limit for the Fluent container to start, in seconds.
    port : int, optional
        Port for Fluent container to use.
    license_server : str, optional
        License server for Ansys Fluent to use.
    container_server_info_file : str | Path, optional
        Name of the server information file for Fluent to write on the ``mount_source``.
    remove_server_info_file : bool, optional
        Defaults to True, and automatically deletes the server information file after PyFluent has finished using it.
    fluent_image : str, optional
        Specifies full image name for Docker container run, with the format ``"image_name:image_tag"``.
        ``image_tag`` and ``image_name`` are ignored if ``fluent_image`` has been specified.
    image_name : str, optional
        Ignored if ``fluent_image`` has been specified.
    image_tag : str, optional
        Ignored if ``fluent_image`` has been specified.
    file_transfer_service : optional
        Supports file upload and download.
    compose_config : ComposeConfig, optional
        Configuration for Docker Compose, if using Docker Compose to launch the container.
    **container_dict
        Additional keyword arguments can be specified, they will be treated as Docker container run options
        to be passed directly to the Docker run execution. See examples below and `Docker run`_ documentation.

    Returns
    -------
    fluent_image : str
    container_dict : dict
    timeout : int
    port : int
    host_server_info_file : Path
    remove_server_info_file: bool

    Raises
    ------
    LicenseServerNotSpecified
        If license server is not specified through an environment variable or in ``container_dict``.
    ServerInfoFileError
        If server info file is specified through both a command-line argument inside ``container_dict`` and the  ``container_server_info_file`` parameter.
    FluentImageNameTagNotSpecified
        If ``fluent_image`` or ``image_tag`` and ``image_name`` are not specified.

    Notes
    -----
    This function should usually not be called directly, it is automatically used by
    :func:`~ansys.fluent.core.launcher.launcher.launch_fluent()`.

    For a list of additional Docker container run configuration options that can also be specified using
    ``container_dict``, see `Docker run`_ documentation.

    See also :func:`start_fluent_container`.
    """

    compose_config = compose_config if compose_config else ComposeConfig()

    if timeout is not None:
        warnings.warn(
            "configure_container_dict(timeout) is deprecated, use launch_fluent(start_timeout) instead.",
            PyFluentDeprecationWarning,
        )

    logger.debug(f"container_dict before processing:\n{dict_to_str(container_dict)}")

    # Starting with 'mount_source' because it is not tied to the 'working_dir'.
    # The intended 'mount_source' logic is as follows, if it is not directly specified:
    # 1. If 'file_transfer_service' is provided, use its 'mount_source'.
    # 2. Use the value from 'pyfluent.config.container_mount_source', if it is set.
    # 3. If 'volumes' is specified in 'container_dict', try to infer the value from it.
    # 4. Finally, use the current working directory, which is always available.

    if not mount_source:
        if file_transfer_service:
            mount_source = file_transfer_service.mount_source
        else:
            mount_source = pyfluent.config.container_mount_source

    if "volumes" in container_dict:
        if len(container_dict["volumes"]) != 1:
            logger.warning(
                "Multiple volumes being mounted in the Docker container, "
                "Assuming the first mount is the working directory for Fluent."
            )
        volumes_string = container_dict["volumes"][0]
        if mount_source:
            logger.warning(
                "'volumes' keyword specified in 'container_dict', but "
                "it is going to be overwritten by specified 'mount_source'."
            )
        else:
            mount_source = volumes_string.split(":")[0]
            logger.debug(f"mount_source: {mount_source}")
        inferred_mount_target = volumes_string.split(":")[1]
        logger.debug(f"inferred_mount_target: {inferred_mount_target}")

    if not mount_source:
        logger.debug("No container 'mount_source' specified, using default value.")
        mount_source = os.getcwd()

    # The intended 'mount_target' logic is as follows, if it is not directly specified:
    # 1. If 'working_dir' is specified in 'container_dict', use it as 'mount_target'.
    # 2. Try to infer the value from the 'volumes' keyword in 'container_dict', if available.
    # 3. Finally, use the value from 'pyfluent.config.container_mount_target', which is always set.

    if not mount_target:
        if "working_dir" in container_dict:
            mount_target = container_dict["working_dir"]
        else:
            mount_target = pyfluent.config.container_mount_target

    if "working_dir" in container_dict and mount_target:
        # working_dir will be set later to the final value of mount_target
        container_dict.pop("working_dir")

    if not mount_target and "volumes" in container_dict:
        mount_target = inferred_mount_target

    if not mount_target:
        logger.debug("No container 'mount_target' specified, using default value.")
        mount_target = pyfluent.config.container_mount_target

    if "volumes" not in container_dict:
        container_dict.update(volumes=[f"{mount_source}:{mount_target}"])
    else:
        container_dict["volumes"][0] = f"{mount_source}:{mount_target}"

    logger.warning(
        f"Configuring Fluent container to mount to {mount_source}, "
        f"with this path available as {mount_target} for the Fluent session running inside the container."
    )

    if "working_dir" not in container_dict:
        container_dict.update(
            working_dir=mount_target,
        )

    port_mapping = {port: port} if port else {}
    if not port_mapping and "ports" in container_dict:
        # take the specified 'port', OR the first port value from the specified 'ports', for Fluent to use
        port_mapping = container_dict["ports"]
    if not port_mapping and pyfluent.config.launch_fluent_port:
        port = pyfluent.config.launch_fluent_port
        port_mapping = {port: port}
    if not port_mapping:
        port = get_free_port()
        port_mapping = {port: port}

    container_dict.update(
        ports={str(x): y for x, y in port_mapping.items()}
    )  # container port : host port
    container_grpc_port = next(
        iter(port_mapping.values())
    )  # the first port in the mapping is chosen as the gRPC port

    if "environment" not in container_dict:
        if not license_server:
            license_server = os.getenv("ANSYSLMD_LICENSE_FILE")

        if not license_server:
            raise LicenseServerNotSpecified()
        container_dict.update(
            environment={
                "ANSYSLMD_LICENSE_FILE": license_server,
                "REMOTING_PORTS": f"{container_grpc_port}/portspan=2",
                "FLUENT_ALLOW_REMOTE_GRPC_CONNECTION": "1",
            }
        )
        if compose_config.is_compose:
            container_dict["environment"]["FLUENT_SERVER_INFO_PERMISSION_SYSTEM"] = "1"

    if "labels" not in container_dict:
        test_name = pyfluent.config.test_name
        container_dict.update(
            labels={"test_name": test_name},
        )

    # Find the server info file name from the command line arguments
    if "command" in container_dict:
        for v in container_dict["command"]:
            if v.startswith("-sifile="):
                if container_server_info_file:
                    raise ServerInfoFileError()
                container_server_info_file = PurePosixPath(
                    v.replace("-sifile=", "")
                ).name
                logger.debug(
                    f"Found server info file specification for {container_server_info_file}."
                )

    if container_server_info_file:
        container_server_info_file = (
            PurePosixPath(mount_target) / PurePosixPath(container_server_info_file).name
        )
    else:
        fd, sifile = tempfile.mkstemp(
            suffix=".txt", prefix="serverinfo-", dir=mount_source
        )
        os.close(fd)
        container_server_info_file = PurePosixPath(mount_target) / Path(sifile).name

    logger.debug(
        f"Using server info file '{container_server_info_file}' for Fluent container."
    )

    # If the 'command' had already been specified in the 'container_dict',
    # maintain other 'command' arguments but update the '-sifile' argument,
    # as the 'mount_target' or 'working_dir' may have changed.
    if "command" in container_dict:
        for i, item in enumerate(container_dict["command"]):
            if item.startswith("-sifile="):
                container_dict["command"][i] = f"-sifile={container_server_info_file}"
    else:
        container_dict["command"] = args + [f"-sifile={container_server_info_file}"]

    if not fluent_image:
        if not image_tag:
            image_tag = pyfluent.config.fluent_image_tag
        if not image_name and image_tag:
            image_name = (
                pyfluent.config.fluent_image_name
                or get_ghcr_fluent_image_name(image_tag)
            )
        if not image_tag or not image_name:
            fluent_image = pyfluent.config.fluent_container_name
        elif image_tag and image_name:
            if image_tag.startswith("sha"):
                fluent_image = f"{image_name}@{image_tag}"
            else:
                fluent_image = f"{image_name}:{image_tag}"
        else:
            raise FluentImageNameTagNotSpecified()

    container_dict["fluent_image"] = fluent_image

    if not pyfluent.config.fluent_automatic_transcript:
        if "environment" not in container_dict:
            container_dict["environment"] = {}
        container_dict["environment"]["FLUENT_NO_AUTOMATIC_TRANSCRIPT"] = "1"

    if pyfluent.config.launch_fluent_ip or pyfluent.config.remoting_server_address:
        if "environment" not in container_dict:
            container_dict["environment"] = {}
        container_dict["environment"]["REMOTING_SERVER_ADDRESS"] = (
            pyfluent.config.launch_fluent_ip or pyfluent.config.remoting_server_address
        )

    if pyfluent.config.launch_fluent_skip_password_check:
        if "environment" not in container_dict:
            container_dict["environment"] = {}
        container_dict["environment"]["FLUENT_LAUNCHED_FROM_PYFLUENT"] = "1"

    container_dict_base = {}
    container_dict_base.update(
        detach=True,
        auto_remove=True,
    )

    for k, v in container_dict_base.items():
        if k not in container_dict:
            container_dict[k] = v

    if not Path(mount_source).exists():
        Path(mount_source).mkdir(parents=True, exist_ok=True)
    host_server_info_file = Path(mount_source) / container_server_info_file.name

    if compose_config.is_compose:
        container_dict["host_server_info_file"] = host_server_info_file
        container_dict["mount_source"] = mount_source
        container_dict["mount_target"] = mount_target

    logger.debug(
        f"Fluent container container_grpc_port: {container_grpc_port}, "
        f"host_server_info_file: '{host_server_info_file}', "
        f"remove_server_info_file: {remove_server_info_file}"
    )
    logger.debug(f"container_dict after processing:\n{dict_to_str(container_dict)}")

    return (
        container_dict,
        timeout,
        container_grpc_port,
        host_server_info_file,
        remove_server_info_file,
    )


def start_fluent_container(
    args: List[str],
    container_dict: dict | None = None,
    start_timeout: int = 60,
    compose_config: ComposeConfig | None = None,
) -> tuple[int, str, Any]:
    """Start a Fluent container.

    Parameters
    ----------
    args : List[str]
        List of Fluent launch arguments.
    container_dict : dict, optional
        Dictionary with Docker container configuration.
    start_timeout : int, optional
        Timeout in seconds for the container to start. If not specified, it defaults to 60
        seconds.
    compose_config : ComposeConfig, optional
        Configuration for Docker Compose, if using Docker Compose to launch the container.

    Returns
    -------
    int
        Fluent gPRC server port exposed from the container.
    str
        Fluent gPRC server password exposed from the container.

    Raises
    ------
    TimeoutError
        If Fluent container launch reaches timeout.

    Notes
    -----
    Uses :func:`configure_container_dict` to parse the optional ``container_dict`` configuration.

    This function should usually not be called directly, it is automatically used by
    :func:`~ansys.fluent.core.launcher.launcher.launch_fluent()`.
    """

    compose_config = compose_config if compose_config else ComposeConfig()

    if container_dict is None:
        container_dict = {}

    container_vars = configure_container_dict(
        args,
        compose_config=compose_config,
        **container_dict,
    )

    (
        config_dict,
        timeout,
        port,
        host_server_info_file,
        remove_server_info_file,
    ) = container_vars
    launch_string = " ".join(config_dict["command"])

    if timeout:
        logger.warning(
            "launch_fluent(start_timeout) overridden by configure_container_dict(timeout) value."
        )
        start_timeout = timeout
        del timeout

    try:
        if compose_config.is_compose:
            config_dict["fluent_port"] = port

            compose_container = ComposeBasedLauncher(
                compose_config=compose_config,
                container_dict=config_dict,
            )

            if not compose_container.check_image_exists():
                logger.debug(
                    f"Fluent image {config_dict['fluent_image']} not found. Pulling image..."
                )
                compose_container.pull_image()

            compose_container.start()

            return port, config_dict, compose_container
        else:
            if not host_server_info_file.exists():
                host_server_info_file.parents[0].mkdir(exist_ok=True)

            host_server_info_file.touch(exist_ok=True)
            last_mtime = host_server_info_file.stat().st_mtime

            import docker

            docker_client = docker.from_env()

            logger.debug("Starting Fluent docker container...")

            container = docker_client.containers.run(
                config_dict.pop("fluent_image"), **config_dict
            )

            logger.debug(
                f"Waiting for Fluent container for up to {start_timeout} seconds..."
            )

            success = timeout_loop(
                lambda: host_server_info_file.stat().st_mtime > last_mtime,
                start_timeout,
            )

            if not success:
                try:
                    container.stop()
                except Exception as stop_ex:
                    logger.error(f"Failed to stop container: {stop_ex}")
                    raise TimeoutError(
                        f"Fluent container launch has timed out after {start_timeout} seconds. "
                        f"Additionally, stopping the container failed: {stop_ex}"
                    ) from stop_ex
                else:
                    raise TimeoutError(
                        f"Fluent container launch has timed out after {start_timeout} seconds."
                        " The container was stopped."
                    )
            else:
                _, _, password = _parse_server_info_file(str(host_server_info_file))

                return port, password, container
    except Exception as ex:
        logger.error(f"Exception caught - {type(ex).__name__}: {ex}")
        raise LaunchFluentError(launch_string) from ex
    finally:
        if remove_server_info_file and host_server_info_file.exists():
            host_server_info_file.unlink()
