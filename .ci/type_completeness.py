"""Report BasedPyright type completeness for PyFluent's public API.

Install the project's pinned checker and run from the repository root:
    python -m pip install basedpyright==1.40.2
    python .ci/type_completeness.py

The generated model is excluded from the reported score by filtering its
exported symbols from BasedPyright's JSON report. The package's ``py.typed``
marker lets BasedPyright verify the installed package.
"""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


PACKAGE = "ansys.fluent.core"
GENERATED_PREFIX = f"{PACKAGE}.generated"
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    result = subprocess.run(
        [
            "basedpyright",
            "--verifytypes",
            PACKAGE,
            "--outputjson",
        ],
        cwd=REPOSITORY_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    try:
        report = json.loads(result.stdout)
        completeness = report["typeCompleteness"]
        symbols = completeness["symbols"]
    except (json.JSONDecodeError, KeyError, TypeError) as error:
        detail = result.stderr or result.stdout
        print(f"Could not read BasedPyright's JSON report: {error}", file=sys.stderr)
        if detail:
            print(detail, file=sys.stderr)
        return 1

    if not completeness.get("pyTypedPath") or not symbols:
        diagnostics = report.get("generalDiagnostics", [])
        print(
            "BasedPyright did not verify the package. Ensure it is installed "
            "in the active environment and includes py.typed.",
            file=sys.stderr,
        )
        for diagnostic in diagnostics:
            print(diagnostic.get("message", diagnostic), file=sys.stderr)
        return 1

    exported = [symbol for symbol in symbols if symbol["isExported"]]
    # verifytypes can still report excluded exports, so omit them from the metric too.
    measured = [
        symbol
        for symbol in exported
        if not (
            symbol["name"] == GENERATED_PREFIX
            or symbol["name"].startswith(f"{GENERATED_PREFIX}.")
        )
    ]

    def summarize(label: str, selected: list[dict[str, object]]) -> None:
        known = sum(bool(symbol["isTypeKnown"]) for symbol in selected)
        ambiguous = sum(bool(symbol["isTypeAmbiguous"]) for symbol in selected)
        unknown = len(selected) - known - ambiguous
        score = 100 * known / len(selected) if selected else 0
        print(
            f"{label}: {score:.1f}% "
            f"({known:,} known / {len(selected):,} exported; "
            f"{ambiguous:,} ambiguous, {unknown:,} unknown)"
        )

    summarize("Public API, excluding generated model", measured)
    summarize("Public API, including generated model", exported)
    print(f"Excluded generated symbols: {len(exported) - len(measured):,}")
    print(f"BasedPyright version: {report.get('version', 'unknown')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
