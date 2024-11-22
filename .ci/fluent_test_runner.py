"""Script to run Fluent test in Docker container."""

import argparse
import logging
import os
from pathlib import Path
from shutil import copytree
from tempfile import TemporaryDirectory
from time import sleep

import yaml

import ansys.fluent.core as pyfluent
from ansys.fluent.core import FluentVersion
import docker


class FluentRuntimeError(RuntimeError):
    """Exception raised when stderr is detected in Fluent output."""

    pass


def run_fluent_test(journal_file: Path, launcher_args: str = "") -> None:
    """Run Fluent test.

    Parameters
    ----------
    journal_file : Path
        Absolute path to the journal file.

    launcher_args : str, optional
        Additional arguments for the Fluent launcher.

    Raises
    ------
    FluentRuntimeError
        Raised when stderr is detected in Fluent output.
    """
    logging.debug(f"journal_file: {journal_file}")
    src_pyfluent_dir = str(Path(pyfluent.__file__).parent)
    verion_for_file_name = FluentVersion.current_dev().number
    dst_pyfluent_dir = f"/ansys_inc/v{verion_for_file_name}/commonfiles/CPython/3_10/linx64/Release/python/lib/python3.10/site-packages/ansys/fluent/core"
    src_test_dir = str(journal_file.parent.parent)
    dst_test_dir = "/testing"
    logging.debug(f"src_pyfluent_dir: {src_pyfluent_dir}")
    logging.debug(f"dst_pyfluent_dir: {dst_pyfluent_dir}")
    logging.debug(f"src_test_dir: {src_test_dir}")
    logging.debug(f"dst_test_dir: {dst_test_dir}")

    docker_client = docker.from_env()
    version_for_image_tag = FluentVersion.current_dev().docker_image_tag
    image_name = f"ghcr.io/ansys/pyfluent:{version_for_image_tag}"
    container = docker_client.containers.run(
        image=image_name,
        volumes=[
            f"{src_pyfluent_dir}:{dst_pyfluent_dir}",
            f"{src_test_dir}:{dst_test_dir}",
        ],
        working_dir=dst_test_dir,
        environment={"ANSYSLMD_LICENSE_FILE": os.environ["ANSYSLMD_LICENSE_FILE"]},
        command=f"3ddp {launcher_args} -gu -py -i {journal_file.name}",
        detach=True,
        stdout=True,
        stderr=True,
    )
    while True:
        container.reload()
        if container.status == "exited":
            break
        stderr = container.logs(stdout=False, stderr=True)
        if stderr:
            stderr = stderr.decode()
            for line in stderr.split("\n"):
                if line.strip().startswith("Error:"):
                    if "Expected exception" in line:  # for check_assert.py
                        container.stop()
                    else:
                        raise FluentRuntimeError(line)
        sleep(1)
    logging.debug(container.logs(stderr=True).decode())
    container.remove()


MAX_TEST_PATH_LENGTH = 40


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Fluent test.")
    parser.add_argument(
        "test_dir",
        help="Path to the Fluent test directory relative to the PyFluent repository root.",
    )
    args = parser.parse_args()
    test_dir = Path.cwd() / args.test_dir
    with TemporaryDirectory(ignore_cleanup_errors=True) as tmpdir:
        copytree(test_dir, tmpdir, dirs_exist_ok=True)
        exception_occurred = False
        for test_file in (Path(tmpdir) / "fluent").rglob("*.py"):
            config_file = test_file.with_suffix(".yaml")
            launcher_args = ""
            if config_file.exists():
                configs = yaml.safe_load(config_file.read_text())
                launcher_args = configs.get("launcher_args", "")
            test_file_relpath = str(test_file.relative_to(tmpdir))
            print(f"Running {test_file_relpath}", end="", flush=True)
            try:
                run_fluent_test(test_file, launcher_args)
                print(
                    f"{(MAX_TEST_PATH_LENGTH + 10 - len(test_file_relpath)) * '·'}PASSED"
                )
            except FluentRuntimeError as e:
                print(
                    f"{(MAX_TEST_PATH_LENGTH + 10 - len(test_file_relpath)) * '·'}FAILED"
                )
                print(e)
                exception_occurred = True
        if exception_occurred:
            exit(1)
