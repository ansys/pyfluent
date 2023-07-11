"""Provides a module for launching and configuring local Fluent Docker container runs.

Notes
-----

For configuration details, see :func:`configure_container_dict`, and for a list of additional Docker container run
configuration options that can also be specified through the
``container_dict`` argument for :func:`~ansys.fluent.core.launcher.launcher.launch_fluent()`,
see `Docker run documentation`_.

.. _Docker run documentation: https://docker-py.readthedocs.io/en/stable/containers.html#docker.models.containers.ContainerCollection.run

Examples
--------
Launching a Fluent Docker container with system default configuration:

>>> import ansys.fluent.core as pyfluent
>>> session = pyfluent.launch_fluent(start_container=True)

Launching with custom configuration:

>>> import ansys.fluent.core as pyfluent
>>> custom_config = {}
>>> custom_config.update(fluent_image='custom_fluent:v23.1.0', host_mount_path='/testing', auto_remove=False)
>>> session = pyfluent.launch_fluent(container_dict=custom_config)

Getting default Fluent Docker container configuration, then launching with customized configuration:

>>> import ansys.fluent.core as pyfluent
>>> config_dict = pyfluent.launch_fluent(start_container=True, dry_run=True)
Container run configuration information:
image_name = 'ghcr.io/ansys/pyfluent:v23.1.0'
>>> config_dict
{'auto_remove': True,
 'command': ['-gu',
             '-sifile=/home/user/.local/share/ansys_fluent_core/examples/serverinfo-reh96tuo.txt',
             '3ddp'],
 'detach': True,
 'environment': {'ANSYSLMD_LICENSE_FILE': '1450@license_server.com',
                 'REMOTING_PORTS': '57193/portspan=2'},
 'labels': {'test_name': 'none'},
 'ports': {'57193': 57193},
 'volumes': ['/home/user/.local/share/ansys_fluent_core/examples:/home/user/.local/share/ansys_fluent_core/examples'],
 'working_dir': '/home/user/.local/share/ansys_fluent_core/examples'}
>>> config_dict.update(image_name='custom_fluent', image_tag='v23.1.0', mem_limit='1g')
>>> session = pyfluent.launch_fluent(container_dict=config_dict)

"""
import logging
import os
from pathlib import Path
import tempfile
from typing import List, Union

import ansys.fluent.core as pyfluent
from ansys.fluent.core.session import _parse_server_info_file
from ansys.fluent.core.utils.execution import timeout_loop
from ansys.fluent.core.utils.networking import get_free_port
import docker

logger = logging.getLogger("pyfluent.launcher")


def configure_container_dict(
    args: List[str],
    host_mount_path: Union[str, Path] = None,
    container_mount_path: Union[str, Path] = None,
    timeout: int = 30,
    port: int = None,
    license_server: str = None,
    container_server_info_file: Union[str, Path] = None,
    remove_server_info_file: bool = True,
    fluent_image: str = None,
    image_name: str = None,
    image_tag: str = None,
    **container_dict,
) -> (str, dict, int, int, Path, bool):
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
        to be passed directly to the Docker run execution. See examples below and `Docker run documentation`_.

    Returns
    -------
    fluent_image : str
    container_dict : dict
    timeout : int
    port : int
    container_server_info_file : Path
    remove_server_info_file: bool

    Notes
    -----
    This function should usually not be called directly, it will be automatically used by
    :func:`~ansys.fluent.core.launcher.launcher.launch_fluent()` instead.

    For a list of additional Docker container run configuration options that can also be specified using
    ``container_dict``, see `Docker run documentation`_.
    """

    logger.debug(f"container_dict before processing: {container_dict}")

    if not host_mount_path:
        host_mount_path = pyfluent.EXAMPLES_PATH
    if not os.path.exists(host_mount_path):
        os.makedirs(host_mount_path)

    if not container_mount_path:
        container_mount_path = os.getenv(
            "PYFLUENT_CONTAINER_MOUNT_PATH", host_mount_path
        )

    if "volumes" not in container_dict:
        container_dict.update(volumes=[f"{host_mount_path}:{container_mount_path}"])

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
                container_server_info_file = Path(v.lstrip("-sifile=")).name
                logger.debug(
                    f"Found server info file specification for {container_server_info_file}."
                )

    if container_server_info_file:
        container_server_info_file = (
            Path(container_mount_path) / Path(container_server_info_file).name
        )
    else:
        fd, sifile = tempfile.mkstemp(
            suffix=".txt", prefix="serverinfo-", dir=host_mount_path
        )
        os.close(fd)
        container_server_info_file = Path(container_mount_path) / Path(sifile).name

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
                "Missing 'fluent_image' specification for Docker container launch."
            )

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

    logger.debug(f"container_dict after processing: {container_dict}")

    return (
        fluent_image,
        container_dict,
        timeout,
        port,
        container_server_info_file,
        remove_server_info_file,
    )


def start_fluent_container(args: List[str], container_dict: dict = None) -> (int, str):
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

    Notes
    -----
    See also :func:`configure_container_dict`.
    """

    if container_dict is None:
        container_dict = {}

    container_vars = configure_container_dict(args, **container_dict)

    logger.debug(f"container_vars:{container_vars}")

    (
        fluent_image,
        config_dict,
        timeout,
        port,
        container_server_info_file,
        remove_server_info_file,
    ) = container_vars

    try:
        if not container_server_info_file.exists():
            container_server_info_file.mkdir(exist_ok=True)

        container_server_info_file.touch(exist_ok=True)
        last_mtime = container_server_info_file.stat().st_mtime

        docker_client = docker.from_env()

        logger.debug("Starting Fluent docker container...")

        docker_client.containers.run(fluent_image, **config_dict)

        success = timeout_loop(
            lambda: container_server_info_file.stat().st_mtime > last_mtime, timeout
        )

        if not success:
            raise RuntimeError(
                "Fluent container launch timeout, will have to stop container manually."
            )
        else:
            _, _, password = _parse_server_info_file(str(container_server_info_file))

            return port, password
    finally:
        if remove_server_info_file and container_server_info_file.exists():
            container_server_info_file.unlink()
