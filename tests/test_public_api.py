# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Test suite to verify the public API of ansys.fluent.core remains stable."""

import inspect

import pytest


def test_ansys_fluent_core_public_api():
    """
    Test that the public API of ansys.fluent.core hasn't changed.

    This test ensures that:
    1. No public symbols are accidentally removed
    2. The __all__ attribute correctly exports expected symbols
    3. Future changes don't inadvertently break the public API

    Baseline captured from main branch on 2026-01-21
    """
    import ansys.fluent.core as pyfluent

    # Expected public API symbols captured from main branch
    EXPECTED_PUBLIC_API = [
        "AboutToInitializeSolutionEventInfo",
        "AboutToLoadCaseEventInfo",
        "AboutToLoadDataEventInfo",
        "BatchOps",
        "CalculationsEndedEventInfo",
        "CalculationsPausedEventInfo",
        "CalculationsResumedEventInfo",
        "CalculationsStartedEventInfo",
        "CaseLoadedEventInfo",
        "CaseSettings",
        "DataLoadedEventInfo",
        "Dimension",
        "Event",
        "EventsManager",
        "FatalErrorEventInfo",
        "Fluent",
        "FluentLinuxGraphicsDriver",
        "FluentMode",
        "FluentVersion",
        "FluentWindowsGraphicsDriver",
        "IterationEndedEventInfo",
        "LocalParametricStudy",
        "Meshing",
        "MeshingEvent",
        "PathlinesFieldDataRequest",
        "PrePost",
        "Precision",
        "ProgressUpdatedEventInfo",
        "PureMeshing",
        "PyFluentDeprecationWarning",
        "PyFluentUserWarning",
        "ReportDefinitionUpdatedEventInfo",
        "ReportPlotSetUpdatedEventInfo",
        "ResidualPlotUpdatedEventInfo",
        "ScalarFieldDataRequest",
        "SettingsClearedEventInfo",
        "SolutionInitializedEventInfo",
        "SolutionPausedEventInfo",
        "Solver",
        "SolverAero",
        "SolverEvent",
        "SolverIcing",
        "SolverTimeEstimateUpdatedEventInfo",
        "SurfaceDataType",
        "SurfaceFieldDataRequest",
        "TimestepEndedEventInfo",
        "TimestepStartedEventInfo",
        "UIMode",
        "VectorFieldDataRequest",
        "config",
        "connect_to_fluent",
        "examples",
        "connectivity",
        "diagnostics",
        "execution",
        "generated",
        "offline",
        "launch_fluent",
        "module_config",
        "rpvars",
        "search",
        "services",
        "enable",
        "get_default_config",
        "get_logger",
        "is_active",
        "set_console_logging_level",
        "set_global_level",
        "setup_for_fluent",
        "solver",
        "system_coupling",
        "using",
        "utils",
        "version_info",
        "warning",
    ]

    # Get actual public API
    actual_api = dir(pyfluent)
    actual_public = sorted([name for name in actual_api if not name.startswith("_")])
    expected_public = sorted(
        [name for name in EXPECTED_PUBLIC_API if not name.startswith("_")]
    )

    # Convert to sets for comparison
    actual_set = set(actual_public)
    expected_set = set(expected_public)

    # Check for missing symbols (regressions)
    missing_symbols = expected_set - actual_set

    # Check for new symbols
    new_symbols = actual_set - expected_set

    # Known additions that can be safely ignored
    ignored_new_symbols = {"examples", "generated"}
    unexpected_new_symbols = new_symbols - ignored_new_symbols

    # Report results
    # print("\n" + "=" * 80)
    # print("PUBLIC API VERIFICATION RESULTS")
    # print("=" * 80)

    if missing_symbols:
        print(f"\nMISSING SYMBOLS (REGRESSION): {len(missing_symbols)}")
        for symbol in sorted(missing_symbols):
            print(f"  - {symbol}")
    else:
        print("\nNo missing symbols - all expected symbols are present")

    if new_symbols:
        print(f"\nNEW SYMBOLS DETECTED: {len(new_symbols)}")
        for symbol in sorted(new_symbols):
            status = "(ignored)" if symbol in ignored_new_symbols else "(new)"
            print(f"  + {symbol} {status}")

    if unexpected_new_symbols:
        print(f"\nUNEXPECTED NEW SYMBOLS: {len(unexpected_new_symbols)}")
        for symbol in sorted(unexpected_new_symbols):
            print(f"  ? {symbol}")

    # print("=" * 80 + "\n")

    # Assert no regressions
    assert not missing_symbols, (
        f"\nPublic API regression detected!\n"
        f"Missing {len(missing_symbols)} symbols: {sorted(missing_symbols)}\n"
        f"These symbols existed in the main branch but are now removed."
    )


def test_star_import_exports_all_public_symbols():
    """
    Test that star import exports all critical public symbols.

    This ensures __all__ is properly defined in ansys.fluent.core.__init__.py
    """
    import ansys.fluent.core as pyfluent

    # Get symbols from dir()
    dir_symbols = sorted([name for name in dir(pyfluent) if not name.startswith("_")])

    # Get symbols from star import
    star_import_namespace = {}
    exec("from ansys.fluent.core import *", star_import_namespace)
    star_symbols = sorted(
        [
            name
            for name in star_import_namespace.keys()
            if not name.startswith("_") and name not in ["__builtins__"]
        ]
    )

    # Calculate differences
    missing_in_star = set(dir_symbols) - set(star_symbols)
    extra_in_star = set(star_symbols) - set(dir_symbols)

    # Internal modules expected to be excluded from star import
    expected_internal = {
        "os",
        "pydoc",
        "fldoc",
        "warnings",
        "examples",
        "generated",
        "services",
        "module_config",
        "utils",
    }

    # Critical symbols that must be available via star import
    critical_symbols = {
        "Fluent",
        "Solver",
        "Meshing",
        "PureMeshing",
        "PrePost",
        "launch_fluent",
        "connect_to_fluent",
        "FluentMode",
        "FluentVersion",
        "Precision",
        "Dimension",
    }

    missing_critical = critical_symbols - set(star_symbols)
    unexpected_missing = missing_in_star - expected_internal - critical_symbols

    # Report results
    # print("\n" + "=" * 80)
    # print("STAR IMPORT VERIFICATION RESULTS")
    # print("=" * 80)
    # print(f"\nTotal symbols in dir(): {len(dir_symbols)}")
    # print(f"Total symbols from star import: {len(star_symbols)}")

    if missing_in_star:
        print(f"\nSymbols missing from star import: {len(missing_in_star)}")

        expected_internal_missing = missing_in_star & expected_internal
        if expected_internal_missing:
            print(f"\n  Internal modules (expected): {len(expected_internal_missing)}")
            for symbol in sorted(expected_internal_missing):
                print(f"    - {symbol}")

        if unexpected_missing:
            print(f"\n  Unexpected missing: {len(unexpected_missing)}")
            for symbol in sorted(unexpected_missing):
                print(f"    - {symbol}")

    if missing_critical:
        print("\nCRITICAL SYMBOLS MISSING:")
        for symbol in sorted(missing_critical):
            print(f"  - {symbol}")
    else:
        print("\nAll critical symbols present in star import")

    if extra_in_star:
        print(f"\nExtra symbols in star import: {len(extra_in_star)}")
        for symbol in sorted(extra_in_star):
            print(f"  + {symbol}")

    # print("=" * 80 + "\n")

    # Assert critical symbols are present
    assert not missing_critical, (
        f"\nCritical symbols missing from star import!\n"
        f"Missing: {sorted(missing_critical)}\n"
        f"These must be added to __all__ in ansys/fluent/core/__init__.py"
    )


# Ordered, keyword-only parameters of ``launch_fluent``. Baseline captured
# 2026-11-03. Reordering, renaming, or removing a parameter, or making an
# optional parameter required, is a public API change and must be intentional.
_EXPECTED_LAUNCH_FLUENT_PARAMS = [
    "product_version",
    "dimension",
    "precision",
    "processor_count",
    "journal_file_names",
    "start_timeout",
    "additional_arguments",
    "env",
    "start_container",
    "container_dict",
    "dry_run",
    "cleanup_on_exit",
    "start_transcript",
    "ui_mode",
    "graphics_driver",
    "case_file_name",
    "case_data_file_name",
    "lightweight_mode",
    "mode",
    "py",
    "gpu",
    "cwd",
    "fluent_path",
    "topy",
    "start_watchdog",
    "scheduler_options",
    "file_transfer_service",
    "use_docker_compose",
    "use_podman_compose",
    "certificates_folder",
    "insecure_mode",
    "resilient_mode",
    "resilient_config",
]


def test_launch_fluent_signature_is_stable():
    """Snapshot the ``launch_fluent`` public signature.

    Guards against accidental renaming, reordering or removal of parameters,
    and against an optional parameter silently becoming required.
    """
    from ansys.fluent.core import launch_fluent

    params = inspect.signature(launch_fluent).parameters
    actual_names = list(params)

    assert actual_names == _EXPECTED_LAUNCH_FLUENT_PARAMS, (
        "\nlaunch_fluent signature changed!\n"
        f"Expected order: {_EXPECTED_LAUNCH_FLUENT_PARAMS}\n"
        f"Actual order:   {actual_names}\n"
        "If this change is intentional, update "
        "_EXPECTED_LAUNCH_FLUENT_PARAMS in this test."
    )

    for name, param in params.items():
        assert (
            param.kind is inspect.Parameter.KEYWORD_ONLY
        ), f"launch_fluent parameter '{name}' must remain keyword-only."
        assert param.default is not inspect.Parameter.empty, (
            f"launch_fluent parameter '{name}' lost its default value; "
            "making it required is a breaking API change."
        )


# Backward-compatibility module aliases registered in sys.modules by
# ansys.fluent.core.__init__. Each legacy import path must resolve to the exact
# same object the package assigns to it. Baseline captured 2026-11-03.
def test_backward_compatibility_sys_modules_aliases():
    """Ensure legacy module import paths still resolve to the right objects.

    These aliases let old ``import ansys.fluent.core.<legacy>`` paths keep
    working after modules were relocated. Removing or repointing one breaks
    backward compatibility. Identity is checked (not ``__name__``) because some
    aliases point to a re-exported callable rather than a module.
    """
    import importlib
    import sys

    import ansys.fluent.core  # noqa: F401  (registers the aliases)
    from ansys.fluent.core import offline
    from ansys.fluent.core.connectivity import fluent_connection
    from ansys.fluent.core.diagnostics import exceptions, journaling, logger
    from ansys.fluent.core.diagnostics.search import search
    from ansys.fluent.core.execution.session import file as session_file
    from ansys.fluent.core.offline import parametric_study

    expected_aliases = {
        "ansys.fluent.core.file_session": session_file,
        "ansys.fluent.core.fluent_connection": fluent_connection,
        "ansys.fluent.core.parametric": parametric_study,
        "ansys.fluent.core.pyfluent_warnings": exceptions,
        "ansys.fluent.core.filereader": offline,
        "ansys.fluent.core.logger": logger,
        "ansys.fluent.core.journaling": journaling,
        "ansys.fluent.core.exceptions": exceptions,
        "ansys.fluent.core.search": search,
    }

    for alias, target in expected_aliases.items():
        assert (
            alias in sys.modules
        ), f"Backward-compatibility alias '{alias}' is missing from sys.modules."
        assert sys.modules[alias] is target, (
            f"Alias '{alias}' no longer resolves to its canonical object. "
            "Update the baseline in this test if the move is intentional."
        )
        # The alias must also resolve through the normal import machinery.
        assert importlib.import_module(alias) is target


# Fully-qualified "module:qualname" of the public session classes. Baseline
# captured 2026-11-03. Relocating a session class without preserving its public
# import path is a backward-compatibility break.
_EXPECTED_SESSION_CLASS_PATHS = {
    "Fluent": "ansys.fluent.core:Fluent",
    "Solver": "ansys.fluent.core.solver.session.solver:Solver",
    "SolverAero": "ansys.fluent.core.solver.session.solver_aero:SolverAero",
    "SolverIcing": "ansys.fluent.core.solver.session.solver_icing:SolverIcing",
    "PrePost": "ansys.fluent.core.solver.session.solver_pre_post:PrePost",
    "Meshing": "ansys.fluent.core.meshing.session.meshing:Meshing",
    "PureMeshing": "ansys.fluent.core.meshing.session.pure_meshing:PureMeshing",
}


def test_session_class_paths_are_stable():
    """Snapshot the defining module and qualified name of the session classes.

    Guards the backward-compatible import paths of the session classes exposed
    at the top level of ``ansys.fluent.core``.
    """
    import ansys.fluent.core as pyfluent

    for name, expected_path in _EXPECTED_SESSION_CLASS_PATHS.items():
        cls = getattr(pyfluent, name)
        actual_path = f"{cls.__module__}:{cls.__qualname__}"
        assert actual_path == expected_path, (
            f"Session class '{name}' moved from '{expected_path}' to "
            f"'{actual_path}'. Keep a backward-compatible alias or update the "
            "baseline in this test if the move is intentional."
        )

    from ansys.fluent.core.execution.session.session import BaseSession

    assert (
        f"{BaseSession.__module__}:{BaseSession.__qualname__}"
        == "ansys.fluent.core.execution.session.session:BaseSession"
    )


# Builtin solver settings classes that must remain importable from
# ``ansys.fluent.core.solver``. This is a stable subset, not the full list, so
# the test does not churn as new settings classes are added.
_EXPECTED_BUILTIN_SETTINGS = [
    "Setup",
    "General",
    "Models",
    "Energy",
    "Viscous",
    "Materials",
    "BoundaryConditions",
    "Solution",
    "Results",
]


def test_builtin_settings_classes_available():
    """Ensure key builtin solver settings classes stay publicly importable.

    Skipped when generated settings are not present (for example a lightweight
    checkout without codegen), since the builtin classes are generated.
    """
    from ansys.fluent.core import solver

    if not getattr(solver, "_settings_all", []):
        pytest.skip("Generated settings_builtin not available in this environment.")

    missing = [name for name in _EXPECTED_BUILTIN_SETTINGS if not hasattr(solver, name)]
    assert not missing, (
        f"Builtin solver settings classes no longer available: {missing}. "
        "These are part of the public API exported by ansys.fluent.core.solver."
    )
