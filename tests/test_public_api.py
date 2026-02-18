# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
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
        "data_model_cache",
        "docker",
        "examples",
        "exceptions",
        "field_data_interfaces",
        "filereader",
        "fluent_connection",
        "generated",
        "get_build_details",
        "get_build_version",
        "get_build_version_string",
        "journaling",
        "launch_fluent",
        "launcher",
        "logger",
        "module_config",
        "parametric",
        "pyfluent_warnings",
        "rpvars",
        "scheduler",
        "search",
        "services",
        "session",
        "session_base_meshing",
        "session_meshing",
        "session_pure_meshing",
        "session_shared",
        "session_solver",
        "session_solver_aero",
        "session_solver_icing",
        "session_utilities",
        "set_console_logging_level",
        "setup_for_fluent",
        "solver",
        "streaming_services",
        "system_coupling",
        "utils",
        "variable_strategies",
        "version_info",
        "warning",
        "workflow",
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
        "session_base_meshing",
        "session_meshing",
        "session_pure_meshing",
        "session_shared",
        "session_solver",
        "session_solver_aero",
        "session_solver_icing",
        "session_utilities",
        "services",
        "streaming_services",
        "field_data_interfaces",
        "module_config",
        "pyfluent_warnings",
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
