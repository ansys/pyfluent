"""Report BasedPyright type completeness for PyFluent's public API.

Install the project's pinned checker and run from the repository root:
    python -m pip install basedpyright==1.40.2
    python .ci/type_completeness.py

The generated model is excluded from the reported score by filtering its
exported symbols from BasedPyright's JSON report. A temporary ``py.typed``
marker is created only when the package does not already have one.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


PACKAGE = "ansys.fluent.core"
GENERATED_PREFIX = f"{PACKAGE}.generated"
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_DIRECTORY = REPOSITORY_ROOT / "src" / Path(*PACKAGE.split("."))


def main() -> int:
    executable = shutil.which("basedpyright")
    if executable is None:
        print(
            "basedpyright is not installed or is not available on PATH.",
            file=sys.stderr,
        )
        return 2

    marker = PACKAGE_DIRECTORY / "py.typed"
    created_marker = False
    try:
        # verifytypes requires a PEP 561 marker, even when checking source files.
        try:
            with marker.open("x", encoding="utf-8") as marker_file:
                marker_file.write("\n")
            created_marker = True
        except FileExistsError:
            pass

        with tempfile.TemporaryFile(mode="w+t", encoding="utf-8") as stderr:
            environment = os.environ.copy()
            source_directory = str(REPOSITORY_ROOT / "src")
            existing_pythonpath = environment.get("PYTHONPATH")
            environment["PYTHONPATH"] = os.pathsep.join(
                path
                for path in (source_directory, existing_pythonpath)
                if path
            )
            result = subprocess.run(
                [
                    executable,
                    "--verifytypes",
                    PACKAGE,
                    "--outputjson",
                ],
                cwd=REPOSITORY_ROOT,
                stdout=subprocess.PIPE,
                stderr=stderr,
                env=environment,
                text=True,
                check=False,
            )
            stderr.seek(0)
            stderr_text = stderr.read()

        try:
            report = json.loads(result.stdout)
            completeness = report["typeCompleteness"]
            symbols = completeness["symbols"]
        except (json.JSONDecodeError, KeyError, TypeError) as error:
            detail = stderr_text or result.stdout
            print(f"Could not read BasedPyright's JSON report: {error}", file=sys.stderr)
            if detail:
                print(detail, file=sys.stderr)
            return 1

        if not completeness.get("pyTypedPath") or not symbols:
            diagnostics = report.get("generalDiagnostics", [])
            print(
                "BasedPyright did not verify the package. Ensure the source "
                "package can be imported and has no conflicting configuration.",
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
        print(
            f"Excluded generated symbols: "
            f"{len(exported) - len(measured):,}"
        )
        print(f"BasedPyright version: {report.get('version', 'unknown')}")
        return 0
    finally:
        if created_marker:
            marker.unlink()


if __name__ == "__main__":
    raise SystemExit(main())
