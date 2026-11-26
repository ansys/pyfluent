import subprocess
import sys
from pathlib import Path
from runpy import run_path
from types import SimpleNamespace

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


def test_user_command_defaults_to_the_steady_cavity_case() -> None:
    script_path = Path(__file__).parents[1] / "examples" / "run_user_case.py"
    workflow = run_path(str(script_path))
    arguments = workflow["build_argument_parser"]().parse_args([])

    assert arguments.case.name == "lid_driven_cavity_re100_steady.json"


def test_user_command_parses_checkpoint_and_restart_options() -> None:
    script_path = Path(__file__).parents[1] / "examples" / "run_user_case.py"
    workflow = run_path(str(script_path))
    arguments = workflow["build_argument_parser"]().parse_args(
        [
            "--checkpoint-every",
            "100",
            "--retain-checkpoints",
            "3",
            "--restart",
            "latest",
        ]
    )

    assert arguments.checkpoint_every == 100
    assert arguments.retain_checkpoints == 3
    assert arguments.restart == "latest"


def test_live_plot_history_starts_with_restored_checkpoint_history() -> None:
    script_path = Path(__file__).parents[1] / "examples" / "run_user_case.py"
    workflow = run_path(str(script_path))
    history = (
        SimpleNamespace(step=20, velocity_change=0.25, max_divergence_after=0.02),
        SimpleNamespace(step=40, velocity_change=0.1, max_divergence_after=0.01),
    )

    steps, velocity_changes, divergences = workflow["_history_plot_values"](history)

    assert steps == [20, 40]
    assert velocity_changes == [0.25, 0.1]
    assert divergences == [0.02, 0.01]


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