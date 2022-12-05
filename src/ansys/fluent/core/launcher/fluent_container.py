import os
from pathlib import Path
import socket
import subprocess
import tempfile
import time
from typing import List

from ansys.fluent.core.session import parse_server_info_file


def _get_free_port() -> int:
    sock = socket.socket()
    sock.bind(("", 0))
    return sock.getsockname()[1]


def start_fluent_container(mounted_from: str, mounted_to: str, args: List[str]) -> int:
    """Start a Fluent container.

    Parameters
    ----------
    mounted_from : str
        Path to mount from. Within the container, ``mounted_from`` is mounted as
        ``mount_to``.
    mounted_to : str
        Path to mount to. Within the container, ``mounted_from`` is mounted as
        ``mount_to``.
    args : List[str]
        List of Fluent launch arguments.

    Returns
    -------
    int
        gPRC server port exposed from the container.
    """
    fd, sifile = tempfile.mkstemp(suffix=".txt", prefix="serverinfo-", dir=mounted_from)
    os.close(fd)
    timeout = 100
    license_server = os.environ["ANSYSLMD_LICENSE_FILE"]
    port = _get_free_port()
    password = ""
    container_sifile = mounted_to + "/" + Path(sifile).name
    image_tag = os.getenv("FLUENT_IMAGE_TAG", "v23.1.0")
    test_name = os.getenv("PYFLUENT_TEST_NAME", "none")

    try:
        subprocess.run(
            [
                "docker",
                "run",
                "-d",
                "--rm",
                "-p",
                f"{port}:{port}",
                "-v",
                f"{mounted_from}:{mounted_to}",
                "-e",
                f"ANSYSLMD_LICENSE_FILE={license_server}",
                "-e",
                f"REMOTING_PORTS={port}/portspan=2",
                "-l",
                f"test_name={test_name}",
                f"ghcr.io/pyansys/pyfluent:{image_tag}",
                "-gu",
                f"-sifile={container_sifile}",
            ]
            + args
        )

        sifile_last_mtime = os.stat(sifile).st_mtime
        while True:
            if os.stat(sifile).st_mtime > sifile_last_mtime:
                time.sleep(1)
                _, _, password = parse_server_info_file(sifile)
                break
            if timeout == 0:
                break
            time.sleep(1)
            timeout -= 1
        return port, password
    except OSError:
        pass
    finally:
        if os.path.exists(sifile):
            os.remove(sifile)
