"""Provides a module to compare flobject.py."""

import platform
import subprocess  # nosec B404
import uuid


def compare_flobject():
    """Compare flobject.py.

    Raises
    ------
    RuntimeError
        If flobject.py is inconsistent in Fluent and PyFluent.
    """
    image_name = "ghcr.io/ansys/pyfluent:v24.1.0"
    container_name = uuid.uuid4().hex
    is_linux = platform.system() == "Linux"
    subprocess.run(
        [f"docker container create --name {container_name} {image_name}"],
        shell=is_linux,
    )  # nosec B602
    xml_source = "/ansys_inc/v241/fluent/fluent24.1.0/cortex/pylib/flapi/flobject.py"
    subprocess.run(
        [f"docker cp {container_name}:{xml_source} fluent_flobject.py"], shell=is_linux
    )  # nosec B602
    subprocess.run(
        [f"docker container rm {container_name}"], shell=is_linux
    )  # nosec B602
    p = subprocess.run(
        ["diff -u fluent_flobject.py src/ansys/fluent/core/solver/flobject.py"],
        shell=is_linux,
        capture_output=True,
        text=True,
    )  # nosec B602 B607
    print(p.stdout)
    if p.returncode != 0:
        raise RuntimeError("flobject.py is different in Fluent and PyFLuent.")


if __name__ == "__main__":
    compare_flobject()
