# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

"""Phase 5: Test whole-package runtime type-checking support.

This module audits the TYPE_CHECKING-guarded modules to ensure they work
when beartype.claw's whole-package import hook is applied.

Each test is subprocess-based to isolate import-time state. Modules are checked
individually so that fixes can be tracked and verified one at a time.

DEPENDENCY: Requires Phase 1-4 changes to be in place (stripped _type_checking.py,
removed hook wiring from __init__.py/module_config.py, etc.).
"""

import subprocess
import sys

import pytest

# Modules with TYPE_CHECKING guards that need whole-package coverage.
# Line numbers refreshed 2026-10-06 after the launcher/session module reorganization
# (ansys.fluent.core.launcher.* -> ansys.fluent.core.execution.launcher.*, etc.).
MODULES_TO_CHECK = [
    ("ansys.fluent.core._data_model_cache", 33),
    ("ansys.fluent.core._types", 34),
    ("ansys.fluent.core.execution.launcher.container_launcher", 71),
    ("ansys.fluent.core.execution.launcher.launch_options", 33),
    ("ansys.fluent.core.execution.launcher.launcher", 78),
    ("ansys.fluent.core.execution.launcher.pim_launcher", 61),
    ("ansys.fluent.core.execution.launcher.slurm_launcher", 104),
    ("ansys.fluent.core.execution.launcher.standalone_launcher", 80),
    ("ansys.fluent.core.execution.session.session", 89),
    ("ansys.fluent.core.fields.field_data._field_data_interfaces", 36),
    ("ansys.fluent.core.fields.field_data.abstract_field_data", 30),
    ("ansys.fluent.core.meshing.meshing_workflow", 39),
    ("ansys.fluent.core.meshing.session.base_meshing", 58),
    ("ansys.fluent.core.services._protocols", 28),
    ("ansys.fluent.core.solver.session.solver", 72),
]


def _run_import_under_beartype(module_name: str) -> str:
    """Run a module import under beartype whole-package hook in fresh interpreter.

    Parameters
    ----------
    module_name : str
        Fully-qualified module name to import.

    Returns
    -------
    str
        Stdout output (empty if import succeeds silently).

    Raises
    ------
    subprocess.CalledProcessError
        If the import fails (exit code != 0).
    """
    source = f"""
import sys
try:
    from beartype.claw import beartype_package
    beartype_package('ansys.fluent.core')
    __import__('{module_name}')
    print('OK')
except Exception as e:
    print(f'FAIL: {{type(e).__name__}}: {{e}}', file=sys.stderr)
    raise
"""
    result = subprocess.run(
        [sys.executable, "-W", "ignore", "-c", source],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise subprocess.CalledProcessError(
            result.returncode, result.args, output=result.stdout, stderr=result.stderr
        )
    return result.stdout.strip()


@pytest.mark.parametrize("module_name,line_ref", MODULES_TO_CHECK)
def test_module_imports_under_whole_package_beartype(module_name, line_ref):
    """Test that a TYPE_CHECKING-guarded module imports cleanly under beartype.

    This is the core Phase 5 test: it checks whether each of the 14 modules
    can be imported after applying `beartype_package('ansys.fluent.core')`.

    Each module that fails indicates a forward-reference issue that needs fixing.
    See Phase 5 plan in /memories/session/plan.md for fix strategies.

    Parameters
    ----------
    module_name : str
        Module to test (e.g., "ansys.fluent.core._types").
    line_ref : int or None
        Line number where TYPE_CHECKING guard appears (for reference in logs).
    """
    pytest.importorskip("beartype")
    # This will raise subprocess.CalledProcessError if the module crashes.
    # Catch it to get a readable failure message, or let it propagate for pytest.
    try:
        output = _run_import_under_beartype(module_name)
        assert output == "OK", f"Expected 'OK', got: {output}"
    except subprocess.CalledProcessError as e:
        pytest.fail(
            f"Module {module_name} (TYPE_CHECKING @ line {line_ref}) failed to import "
            f"under beartype_package('ansys.fluent.core').\n"
            f"Exit code: {e.returncode}\n"
            f"Stdout: {e.output}\n"
            f"Stderr: {e.stderr}"
        )


def test_whole_package_import_succeeds():
    """Final smoke test: whole-package import succeeds after beartype.claw applied."""
    pytest.importorskip("beartype")
    source = """
from beartype.claw import beartype_package
beartype_package('ansys.fluent.core')
import ansys.fluent.core
print('OK')
"""
    result = subprocess.run(
        [sys.executable, "-W", "ignore", "-c", source],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.strip() == "OK"


def test_whole_package_catches_violations():
    """Verify that beartype still catches real violations in whole-package mode."""
    pytest.importorskip("beartype")
    source = """
from beartype.claw import beartype_package
beartype_package('ansys.fluent.core')
from ansys.fluent.core.utils.fluent_version import get_version_for_file_name
try:
    get_version_for_file_name(version=123)
    print('no-raise')
except Exception as exc:
    print(type(exc).__name__)
"""
    result = subprocess.run(
        [sys.executable, "-W", "ignore", "-c", source],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.strip() == "BeartypeCallHintParamViolation"
