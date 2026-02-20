"""Script to run Fluent journal tests with a standalone Fluent executable."""

import argparse
import concurrent.futures
import logging
import os
from pathlib import Path
import shlex
from shutil import copytree
import subprocess
from tempfile import TemporaryDirectory

import yaml


class FluentRuntimeError(RuntimeError):
    """Exception raised when stderr is detected in Fluent output."""

    pass


def _run_single_test(
    src_test_dir: Path, journal_file: Path, launcher_args: str, fluent_cmd: str
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
    if "ANSYSLMD_LICENSE_FILE" not in os.environ:
        raise FluentRuntimeError("ANSYSLMD_LICENSE_FILE is not set in the environment")

    # Ensure the copied tests directory is on PYTHONPATH so wrapper scripts can import originals.
    env = os.environ.copy()
    python_path_entries = [str(src_test_dir)]
    if existing := env.get("PYTHONPATH"):
        python_path_entries.append(existing)
    env["PYTHONPATH"] = os.pathsep.join(python_path_entries)

    cmd = [fluent_cmd]
    if launcher_args:
        cmd.extend(shlex.split(launcher_args))
    cmd.extend(["-gu", "-py", "-i", journal_file.name])

    logging.debug("fluent command: %s", " ".join(cmd))
    completed = subprocess.run(
        cmd,
        cwd=journal_file.parent,
        env=env,
        capture_output=True,
        text=True,
    )

    stderr = completed.stderr or ""
    stdout = completed.stdout or ""
    for line in stderr.splitlines():
        if line.strip().startswith("Error:") and "Expected exception" not in line:
            raise FluentRuntimeError(stderr)
    if completed.returncode != 0:
        raise FluentRuntimeError(stderr or stdout)
    if stdout:
        print(stdout)


MAX_TEST_PATH_LENGTH = 100


def _run_single_test_with_status_print(
    src_test_dir: Path,
    journal_file: Path,
    launcher_args: str,
    test_file_relpath: str,
    fluent_cmd: str,
) -> bool:
    try:
        _run_single_test(src_test_dir, journal_file, launcher_args, fluent_cmd)
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
    parser.add_argument(
        "--fluent-cmd",
        default="fluent",
        help="Command used to launch Fluent (default: fluent).",
    )
    args = parser.parse_args()
    fluent_cmd = args.fluent_cmd
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
                (src_test_dir, test_file, launcher_args, test_file_relpath, fluent_cmd)
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
