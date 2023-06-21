import os
from pathlib import Path
import subprocess
import tempfile
import time
from typing import List

from ansys.fluent.core.session import _parse_server_info_file
from ansys.fluent.core.utils.networking import get_free_port


def start_fluent_container(
    host_mount_path: str, container_mount_path: str, args: List[str]
) -> (int, str):
    """Start a Fluent container.

    Parameters
    ----------
    host_mount_path : str
        Existing path in the host operating system that will be available inside the container.
    container_mount_path : str
        Path inside the container where host mount path will be mounted to.
    args : List[str]
        List of Fluent launch arguments.

    Returns
    -------
    int
        Fluent gPRC server port exposed from the container.
    str
        Fluent gPRC server password exposed from the container.
    """
    fd, sifile = tempfile.mkstemp(
        suffix=".txt", prefix="serverinfo-", dir=host_mount_path
    )
    os.close(fd)
    timeout = 100
    license_server = os.environ["ANSYSLMD_LICENSE_FILE"]
    port = get_free_port()
    password = ""
    container_sifile = container_mount_path + "/" + Path(sifile).name
    image_tag = os.getenv("FLUENT_IMAGE_TAG", "v23.1.0")
    test_name = os.getenv("PYFLUENT_TEST_NAME", "none")

    try:
        subprocess.run(
            [
                "docker",
                "run",
                "--detach",
                "--rm",
                "--publish",
                f"{port}:{port}",
                "--volume",
                f"{host_mount_path}:{container_mount_path}",
                "--env",
                f"ANSYSLMD_LICENSE_FILE={license_server}",
                "--env",
                f"REMOTING_PORTS={port}/portspan=2",
                "--label",
                f"test_name={test_name}",
                "--workdir",
                f"{container_mount_path}",
                f"ghcr.io/ansys/pyfluent:{image_tag}",
                "-gu",
                f"-sifile={container_sifile}",
            ]
            + args
        )

        sifile_last_mtime = os.stat(sifile).st_mtime
        while True:
            if os.stat(sifile).st_mtime > sifile_last_mtime:
                time.sleep(1)
                _, _, password = _parse_server_info_file(sifile)
                break
            if timeout == 0:
                break
            time.sleep(1)
            timeout -= 1
        return port, password

    except OSError as exc:
        raise exc

    finally:
        if os.path.exists(sifile):
            os.remove(sifile)
