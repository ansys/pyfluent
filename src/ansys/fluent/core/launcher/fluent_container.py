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

Launching with custom configuration, using ``host_mount_path`` and ``fluent_image``
which are arguments for :func:`configure_container_dict`, and ``auto_remove`` which is an argument for `Docker run`_:

>>> import ansys.fluent.core as pyfluent
>>> custom_config = {}
>>> custom_config.update(fluent_image='custom_fluent:v23.1.0', host_mount_path='/testing', auto_remove=False)
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
 'fluent_image': 'ghcr.io/ansys/pyfluent:v23.2.0',
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
import tempfile
from typing import List, Optional, Union

import ansys.fluent.core as pyfluent
from ansys.fluent.core.session import _parse_server_info_file
from ansys.fluent.core.utils.execution import timeout_loop
from ansys.fluent.core.utils.networking import get_free_port
import docker

logger = logging.getLogger("pyfluent.launcher")
DEFAULT_CONTAINER_MOUNT_PATH = "/mnt/pyfluent"


def configure_container_dict(
    args: List[str],
    host_mount_path: Optional[Union[str, Path]] = None,
    container_mount_path: Optional[Union[str, Path]] = None,
    timeout: int = 60,
    port: Optional[int] = None,
    license_server: Optional[str] = None,
    container_server_info_file: Optional[Union[str, Path]] = None,
    remove_server_info_file: bool = True,
    fluent_image: Optional[str] = None,
    image_name: Optional[str] = None,
    image_tag: Optional[str] = None,
    **container_dict,
) -> (dict, int, int, Path, bool):
    """Parses the parameters listed below, and sets up the container configuration file.

    Parameters
    ----------
    args : List[str]
        List of Fluent launch arguments.
    host_mount_path : Union[str, Path], optional
        Existing path in the host operating system that will be available inside the container.
    container_mount_path : Union[str, Path], optional
        Path inside the container where host mount path will be mounted to.
    timeout : int, optional
        Time limit  for the Fluent container to start, in seconds. By default, 30 seconds.
    port : int, optional
        Port for Fluent container to use.
    license_server : str, optional
        License server for Ansys Fluent to use.
    container_server_info_file : Union[str, Path], optional
        Name of the server information file for Fluent to write on the ``host_mount_path``.
    remove_server_info_file : bool, optional
        Defaults to True, and automatically deletes the server information file after PyFluent has finished using it.
    fluent_image : str, optional
        Specifies full image name for Docker container run, with the format ``"image_name:image_tag"``.
        ``image_tag`` and ``image_name`` are ignored if ``fluent_image`` has been specified.
    image_name : str, optional
        Ignored if ``fluent_image`` has been specified.
    image_tag : str, optional
        Ignored if ``fluent_image`` has been specified.
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
    KeyError
        If license server is not specified through an environment variable or in ``container_dict``.
    ValueError
        If server info file is specified through both a command-line argument inside ``container_dict`` and the  ``container_server_info_file`` parameter.
    ValueError
        If ``fluent_image`` or ``image_tag`` and ``image_name`` are not specified.

    Notes
    -----
    This function should usually not be called directly, it is automatically used by
    :func:`~ansys.fluent.core.launcher.launcher.launch_fluent()`.

    For a list of additional Docker container run configuration options that can also be specified using
    ``container_dict``, see `Docker run`_ documentation.

    See also :func:`start_fluent_container`.
    """

    if (
        container_dict
        and "environment" in container_dict
        and os.getenv("PYFLUENT_HIDE_LOG_SECRETS") == "1"
    ):
        container_dict_h = container_dict.copy()
        container_dict_h.pop("environment")
        logger.debug(f"container_dict before processing: {container_dict_h}")
        del container_dict_h
    else:
        logger.debug(f"container_dict before processing: {container_dict}")

    if not host_mount_path:
        host_mount_path = pyfluent.EXAMPLES_PATH
    elif "volumes" in container_dict:
        logger.warning(
            "'volumes' keyword specified in 'container_dict', but "
            "it is going to be overwritten by specified 'host_mount_path'."
        )
        container_dict.pop("volumes")

    if not os.path.exists(host_mount_path):
        os.makedirs(host_mount_path)

    if not container_mount_path:
        container_mount_path = os.getenv(
            "PYFLUENT_CONTAINER_MOUNT_PATH", DEFAULT_CONTAINER_MOUNT_PATH
        )
    elif "volumes" in container_dict:
        logger.warning(
            "'volumes' keyword specified in 'container_dict', but "
            "it is going to be overwritten by specified 'container_mount_path'."
        )
        container_dict.pop("volumes")

    if "volumes" not in container_dict:
        container_dict.update(volumes=[f"{host_mount_path}:{container_mount_path}"])
    else:
        logger.debug(f"container_dict['volumes']: {container_dict['volumes']}")
        if len(container_dict["volumes"]) != 1:
            logger.warning(
                "Multiple volumes being mounted in the Docker container, "
                "using the first mount as the working directory for Fluent."
            )
        volumes_string = container_dict["volumes"][0]
        container_mount_path = ""
        for c in reversed(volumes_string):
            if c == ":":
                break
            else:
                container_mount_path += c
        container_mount_path = container_mount_path[::-1]
        host_mount_path = volumes_string.replace(":" + container_mount_path, "")
        logger.debug(f"host_mount_path: {host_mount_path}")
        logger.debug(f"container_mount_path: {container_mount_path}")

    if "ports" not in container_dict:
        if not port:
            port = get_free_port()
        container_dict.update(ports={str(port): port})  # container port : host port
    else:
        # take the specified 'port', OR the first port value from the specified 'ports', for Fluent to use
        if not port:
            port = next(iter(container_dict["ports"].values()))

    if "environment" not in container_dict:
        if not license_server:
            license_server = os.getenv("ANSYSLMD_LICENSE_FILE")

        if not license_server:
            raise KeyError(
                "License server needs to be specified through an environment variable, "
                "or in the `container_dict`."
            )
        container_dict.update(
            environment={
                "ANSYSLMD_LICENSE_FILE": license_server,
                "REMOTING_PORTS": f"{port}/portspan=2",
            }
        )

    if "labels" not in container_dict:
        test_name = os.getenv("PYFLUENT_TEST_NAME", "none")
        container_dict.update(
            labels={"test_name": test_name},
        )

    if "working_dir" not in container_dict:
        container_dict.update(
            working_dir=container_mount_path,
        )

    if "command" in container_dict:
        for v in container_dict["command"]:
            if v.startswith("-sifile="):
                if container_server_info_file:
                    raise ValueError(
                        "Specified a server info file command argument as well as "
                        "a container_server_info_file, pick one."
                    )
                container_server_info_file = PurePosixPath(
                    v.replace("-sifile=", "")
                ).name
                logger.debug(
                    f"Found server info file specification for {container_server_info_file}."
                )

    if container_server_info_file:
        container_server_info_file = (
            PurePosixPath(container_mount_path)
            / PurePosixPath(container_server_info_file).name
        )
    else:
        fd, sifile = tempfile.mkstemp(
            suffix=".txt", prefix="serverinfo-", dir=host_mount_path
        )
        os.close(fd)
        container_server_info_file = (
            PurePosixPath(container_mount_path) / Path(sifile).name
        )

    if not fluent_image:
        if not image_tag:
            image_tag = os.getenv("FLUENT_IMAGE_TAG", "v23.2.0")
        if not image_name:
            image_name = os.getenv("FLUENT_IMAGE_NAME", "ghcr.io/ansys/pyfluent")
        if not image_tag or not image_name:
            fluent_image = os.getenv("FLUENT_CONTAINER_IMAGE", None)
        elif image_tag and image_name:
            fluent_image = f"{image_name}:{image_tag}"
        else:
            raise ValueError(
                "Missing 'fluent_image', or 'image_tag' and 'image_name', specification for Docker container launch."
            )

    container_dict["fluent_image"] = fluent_image

    fluent_commands = ["-gu", f"-sifile={container_server_info_file}"] + args

    container_dict_default = {}
    container_dict_default.update(
        command=fluent_commands,
        detach=True,
        auto_remove=True,
    )

    for k, v in container_dict_default.items():
        if k not in container_dict:
            container_dict[k] = v

    host_server_info_file = Path(host_mount_path) / container_server_info_file.name

    return (
        container_dict,
        timeout,
        port,
        host_server_info_file,
        remove_server_info_file,
    )


def start_fluent_container(
    args: List[str], container_dict: Optional[dict] = None
) -> (int, str):
    """Start a Fluent container.

    Parameters
    ----------
    args : List[str]
        List of Fluent launch arguments.
    container_dict : dict, optional
        Dictionary with Docker container configuration.

    Returns
    -------
    int
        Fluent gPRC server port exposed from the container.
    str
        Fluent gPRC server password exposed from the container.

    Raises
    ------
    RuntimeError
        If Fluent container launch reaches timeout.

    Notes
    -----
    Uses :func:`configure_container_dict` to parse the optional ``container_dict`` configuration.

    This function should usually not be called directly, it is automatically used by
    :func:`~ansys.fluent.core.launcher.launcher.launch_fluent()`.
    """

    if container_dict is None:
        container_dict = {}

    container_vars = configure_container_dict(args, **container_dict)

    (
        config_dict,
        timeout,
        port,
        host_server_info_file,
        remove_server_info_file,
    ) = container_vars

    if os.getenv("PYFLUENT_HIDE_LOG_SECRETS") != "1":
        logger.debug(f"container_vars: {container_vars}")
    else:
        config_dict_h = config_dict.copy()
        config_dict_h.pop("environment")
        container_vars_tmp = (
            config_dict_h,
            timeout,
            port,
            host_server_info_file,
            remove_server_info_file,
        )
        logger.debug(f"container_vars: {container_vars_tmp}")
        del container_vars_tmp

    try:
        if not host_server_info_file.exists():
            host_server_info_file.parents[0].mkdir(exist_ok=True)

        host_server_info_file.touch(exist_ok=True)
        last_mtime = host_server_info_file.stat().st_mtime

        docker_client = docker.from_env()

        logger.debug("Starting Fluent docker container...")

        docker_client.containers.run(config_dict.pop("fluent_image"), **config_dict)

        success = timeout_loop(
            lambda: host_server_info_file.stat().st_mtime > last_mtime, timeout
        )

        if not success:
            raise RuntimeError(
                "Fluent container launch timeout, will have to stop container manually."
            )
        else:
            _, _, password = _parse_server_info_file(str(host_server_info_file))

            return port, password
    finally:
        if remove_server_info_file and host_server_info_file.exists():
            host_server_info_file.unlink()
