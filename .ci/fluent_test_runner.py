"""Script to run Fluent test in Docker container."""

import argparse
import concurrent.futures
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


def _run_single_test(
    src_test_dir: Path, journal_file: Path, launcher_args: str
) -> None:
    """Run a single Fluent test.

    Parameters
    ----------
    src_test_dir : Path
        Path to the Fluent test directory in the host.

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
    src_gen_dir = (
        Path(pyfluent.__file__).parent / "ansys" / "fluent" / "core" / "generated"
    )
    dst_gen_dir = f"/ansys_inc/v{verion_for_file_name}/fluent/fluent{FluentVersion.current_dev()!r}/cortex/pylib/flapi/generated"
    dst_test_dir = "/testing"
    working_dir = Path(dst_test_dir)
    parent = journal_file.parent
    parents = []
    while parent != src_test_dir:
        parents.append(parent.name)
        parent = parent.parent
    parents.reverse()
    for parent in parents:
        working_dir /= parent
    working_dir = str(working_dir)
    src_test_dir = str(src_test_dir)
    logging.debug(f"src_pyfluent_dir: {src_pyfluent_dir}")
    logging.debug(f"dst_pyfluent_dir: {dst_pyfluent_dir}")
    logging.debug(f"src_test_dir: {src_test_dir}")
    logging.debug(f"dst_test_dir: {dst_test_dir}")
    logging.debug(f"working_dir: {working_dir}")

    docker_client = docker.from_env()
    version_for_image_tag = FluentVersion.current_dev().docker_image_tag
    image_name = f"ghcr.io/ansys/pyfluent:{version_for_image_tag}"
    container = docker_client.containers.run(
        image=image_name,
        volumes=[
            f"{src_pyfluent_dir}:{dst_pyfluent_dir}",
            f"{src_gen_dir}:{dst_gen_dir}",  # Try removing this after pyfluent is updated in commonfiles
            f"{src_test_dir}:{dst_test_dir}",
        ],
        working_dir=working_dir,
        environment={"ANSYSLMD_LICENSE_FILE": os.environ["ANSYSLMD_LICENSE_FILE"]},
        command=f"{launcher_args} -gu -py -i {journal_file.name}",
        detach=True,
        stdout=True,
        stderr=True,
        auto_remove=True,
    )
    try:
        while True:
            container.reload()
            if container.status == "exited":
                break
            stderr = container.logs(stdout=False, stderr=True)
            if stderr:
                stderr = stderr.decode()
                for line in stderr.splitlines():
                    if line.strip().startswith("Error:"):
                        if "Expected exception" in line:  # for check_assert.py
                            container.stop()
                        else:
                            raise FluentRuntimeError(stderr)
            sleep(1)
        print(container.logs(stderr=True).decode())
        container.remove()
    except docker.errors.DockerException:
        pass


MAX_TEST_PATH_LENGTH = 100


def _run_single_test_with_status_print(
    src_test_dir: Path, journal_file: Path, launcher_args: str, test_file_relpath: str
) -> bool:
    try:
        _run_single_test(src_test_dir, journal_file, launcher_args)
        print(
            f"{test_file_relpath}{(MAX_TEST_PATH_LENGTH + 10 - len(test_file_relpath)) * '·'}PASSED"
        )
    except FluentRuntimeError as e:
        print(
            f"{test_file_relpath}{(MAX_TEST_PATH_LENGTH + 10 - len(test_file_relpath)) * '·'}FAILED"
        )
        print(e)
        return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Fluent test.")
    parser.add_argument(
        "test_dir",
        help="Path to the Fluent test directory relative to the PyFluent repository root.",
    )
    args = parser.parse_args()
    test_dir = Path.cwd() / args.test_dir
    with TemporaryDirectory(ignore_cleanup_errors=True) as src_test_dir:
        copytree(test_dir, src_test_dir, dirs_exist_ok=True)
        statuses = []
        arguments = []
        src_test_dir = Path(src_test_dir)
        for test_file in (src_test_dir / "fluent").rglob("*.py"):
            config_file = test_file.with_suffix(".yaml")
            launcher_args = ""
            if config_file.exists():
                configs = yaml.safe_load(config_file.read_text())
                launcher_args = configs.get("launcher_args", "")
            test_file_relpath = str(test_file.relative_to(src_test_dir))
            arguments.append(
                (src_test_dir, test_file, launcher_args, test_file_relpath)
            )
        max_workers = int(os.getenv("MAX_WORKERS_FLUENT_TESTS", 4))
        if max_workers > 1:
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=max_workers
            ) as executor:
                futures = [
                    executor.submit(_run_single_test_with_status_print, *args)
                    for args in arguments
                ]
                for future in concurrent.futures.as_completed(futures):
                    statuses.append(future.result())
        else:
            for args in arguments:
                statuses.append(_run_single_test_with_status_print(*args))
        if any(statuses):
            exit(1)
