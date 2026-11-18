import subprocess
import sys
from pathlib import Path
from runpy import run_path

import pytest


@pytest.mark.parametrize(
    ("arguments", "expected_mode"),
    [([], "save"), (["--mode", "save"], "save"), (["--mode", "live"], "live"), (["--live"], "live")],
)
def test_user_command_selects_save_and_live_modes(arguments, expected_mode) -> None:
    script_path = Path(__file__).parents[1] / "examples" / "run_user_case.py"
    workflow = run_path(str(script_path))
    parser = workflow["build_argument_parser"]()

    assert parser.parse_args(arguments).mode == expected_mode


def test_run_user_case_exports_expected_artifacts(tmp_path: Path) -> None:
    repo_root = Path(__file__).parents[1]
    script_path = repo_root / "examples" / "run_user_case.py"
    case_path = repo_root / "cases" / "lid_driven_cavity_re100_workflow.json"
    output_dir = tmp_path / "workflow_output"

    result = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "--case",
            str(case_path),
            "--output",
            str(output_dir),
            "--mode",
            "save",
        ],
        capture_output=True,
        text=True,
        cwd=repo_root,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "Status: converged" in result.stdout
    assert output_dir.exists()
    for expected_file in (
        "case.json",
        "summary.json",
        "fields.npz",
        "metadata.json",
        "history.csv",
        "ghia_re100.json",
        "geometry.png",
        "cavity_fields.png",
        "ghia_profiles.png",
        "convergence_history.png",
    ):
        assert (output_dir / expected_file).exists()