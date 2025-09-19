#!/usr/bin/env python3
"""
Test script to run all PyFluent examples and check for deprecation warnings.

This script runs each example in the examples/00-fluent directory and:
1. Captures all output (stdout and stderr)
2. Checks for deprecation warnings
3. Reports success/failure for each example
4. Provides a summary of all warnings found
"""

import os
import subprocess
import sys
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import TypedDict

from ansys.fluent.core.utils.fluent_version import FluentVersion

# Common deprecation warning patterns to look for
DEPRECATION_PATTERNS = [
    "DeprecationWarning",
    "FutureWarning",
    "UserWarning",
    "deprecated",
    "will be removed",
    "is deprecated",
    "Please use",
    "instead use",
]

# Examples that might require special handling or longer timeouts


class SpecialCase(TypedDict, total=False):
    timeout: int
    skip: bool


SPECIAL_CASES: dict[str, SpecialCase] = {
    "external_compressible_flow.py": {"timeout": 2400, "skip": False},
    "modeling_ablation.py": {"timeout": 2400, "skip": False},
    "frozen_rotor_workflow.py": {"timeout": 2400, "skip": False},
    "conjugate_heat_transfer.py": {"timeout": 2400, "skip": False},
    "radiation_headlamp.py": {"timeout": 2400, "skip": False},
    "mixing_tank_workflow.py": {"timeout": 2400, "skip": False},
    "DOE_ML.py": {"timeout": 2400, "skip": False},  # Might need special ML dependencies
}


class ExampleRunResult(TypedDict):
    success: bool
    output: str
    warnings: list[str]
    duration: float
    log_file: str


class ExampleTester:
    def __init__(
        self,
        examples_dir: Path | str,
        timeout: int = 1800,
        max_workers: int | None = None,
    ):
        self.examples_dir: Path = Path(examples_dir)
        self.default_timeout: int = timeout
        self.results: dict[str, ExampleRunResult] = {}
        self.all_warnings: list[str] = []
        self.max_workers: int = max_workers or max(1, min(8, os.cpu_count() or 1))
        script_dir = Path(__file__).parent
        self.logs_dir: Path = script_dir / "example_logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self._print_lock: threading.Lock = threading.Lock()

    def find_examples(self) -> list[Path]:
        """Find all Python example files."""
        examples: list[Path] = []
        for file in self.examples_dir.glob("*.py"):
            if file.name != "__init__.py":
                examples.append(file)
        return sorted(examples)

    def _safe_print(self, message: str) -> None:
        with self._print_lock:
            print(message, flush=True)

    def _write_log(
        self,
        example_name: str,
        success: bool,
        duration: float,
        warnings: list[str],
        output: str,
        note: str | None = None,
    ) -> Path:
        status = "PASS" if success else "FAIL"
        if note:
            status = f"{status} ({note})"

        log_lines: list[str] = [
            f"Example: {example_name}",
            f"Status: {status}",
            f"Duration: {duration:.2f}s",
            f"Warnings: {len(warnings)}",
        ]

        if warnings:
            log_lines.append("")
            log_lines.append("Warnings:")
            log_lines.extend([f"- {warning}" for warning in warnings])

        log_lines.append("")
        log_lines.append("Output:")
        log_lines.append(output)

        log_file = self.logs_dir / f"{example_name}.log"
        _ = log_file.write_text("\n".join(log_lines))
        return log_file

    def run_example(
        self, example_path: Path
    ) -> tuple[bool, str, list[str], float, Path]:
        """
        Run a single example and return (success, output, warnings).

        Returns:
            success: True if example ran without errors
            output: Combined stdout/stderr output
            warnings: List of detected warning lines
        """
        example_name = example_path.name
        config = SPECIAL_CASES.get(example_name, {})
        timeout: int = config.get("timeout", self.default_timeout)

        if config.get("skip", False):
            output = f"Skipped {example_name}"
            log_file = self._write_log(
                example_name, True, 0.0, [], output, note="Skipped"
            )
            self._safe_print(f"Skipped {example_name} (log: {log_file.name})")
            return True, output, [], 0.0, log_file

        self._safe_print(f"Running {example_name}...")

        start_time = time.time()
        full_output = ""
        warnings: list[str] = []
        success = False
        note: str | None = None

        try:
            with tempfile.TemporaryDirectory() as dir:
                result = subprocess.run(
                    [sys.executable, str(example_path)],
                    cwd=dir,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    env={
                        **os.environ,
                        FluentVersion.v261.awp_var: "/home/ANSYSDev/v261",
                        "PYTHONWARNINGS": "default",
                    },
                )

            full_output = f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
            warnings = self.extract_warnings(full_output)
            success = result.returncode == 0
        except subprocess.TimeoutExpired as exc:
            note = "Timeout"
            captured_stdout = exc.stdout or ""
            captured_stderr = exc.stderr or ""
            full_output = f"Example timed out after {timeout} seconds\n\nSTDOUT:\n{captured_stdout}\n\nSTDERR:\n{captured_stderr}"
        except Exception as exc:  # pylint: disable=broad-except
            note = "Error"
            full_output = f"Exception occurred: {exc}"

        duration = time.time() - start_time
        log_file = self._write_log(
            example_name, success, duration, warnings, full_output, note
        )

        status = "✓ PASS" if success else "✗ FAIL"
        if note:
            status = f"{status} ({note})"
        warning_note = f" with {len(warnings)} warning(s)" if warnings else ""
        self._safe_print(
            f"Finished {example_name}: {status} in {duration:.2f}s{warning_note} (log: {log_file.name})"
        )

        return success, full_output, warnings, duration, log_file

    def extract_warnings(self, output: str) -> list[str]:
        """Extract warning lines from output."""
        warnings: list[str] = []
        lines: list[str] = output.split("\n")

        for i, line in enumerate(lines):
            line_lower = line.lower()
            for pattern in DEPRECATION_PATTERNS:
                if pattern.lower() in line_lower:
                    # Include some context around the warning
                    context_start = max(0, i - 1)
                    context_end = min(len(lines), i + 2)
                    context = lines[context_start:context_end]
                    warnings.append("\n".join(context))
                    break

        return warnings

    def run_all_examples(self) -> dict[str, ExampleRunResult]:
        """Run all examples and collect results."""
        examples = self.find_examples()

        print(f"Found {len(examples)} examples to test")
        print("=" * 60)

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_example = {
                executor.submit(self.run_example, example): example
                for example in examples
            }

            for future in as_completed(future_to_example):
                example = future_to_example[future]
                try:
                    success, output, warnings, duration, log_file = future.result()
                except Exception as exc:  # pylint: disable=broad-except
                    success = False
                    output = f"Unhandled exception: {exc}"
                    warnings: list[str] = []
                    duration = 0.0
                    log_file = self._write_log(
                        example.name,
                        success,
                        duration,
                        warnings,
                        output,
                        note="UnhandledException",
                    )
                    self._safe_print(
                        f"Finished {example.name}: ✗ FAIL (UnhandledException) (log: {log_file.name})"
                    )

                self.results[example.name] = {
                    "success": success,
                    "output": output,
                    "warnings": warnings,
                    "duration": duration,
                    "log_file": str(log_file),
                }

                # Collect all warnings for summary
                self.all_warnings.extend(warnings)

        return self.results

    def print_summary(self):
        """Print a summary of all test results."""
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)

        total_examples = len(self.results)
        successful = sum(1 for r in self.results.values() if r["success"])
        failed = total_examples - successful
        total_warnings = sum(len(r["warnings"]) for r in self.results.values())

        print(f"Total examples: {total_examples}")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        print(f"Total warnings: {total_warnings}")
        print(f"Logs saved to: {self.logs_dir}")

        if failed > 0:
            print("\nFAILED EXAMPLES:")
            for name, result in self.results.items():
                if not result["success"]:
                    print(f"  - {name}")

        if total_warnings > 0:
            print("\nEXAMPLES WITH WARNINGS:")
            for name, result in self.results.items():
                if result["warnings"]:
                    print(f"  - {name}: {len(result['warnings'])} warning(s)")

        # Show unique warnings
        if self.all_warnings:
            print("\nUNIQUE WARNINGS DETECTED:")
            unique_warnings = list(set(self.all_warnings))
            for i, warning in enumerate(unique_warnings[:10], 1):  # Show first 10
                print(f"\n{i}. {warning}")
            if len(unique_warnings) > 10:
                print(f"\n... and {len(unique_warnings) - 10} more warnings")

    def save_detailed_report(self, filename: str = "example_test_report.txt"):
        """Save detailed report to file."""
        with open(filename, "w") as f:
            _ = f.write("PyFluent Examples Deprecation Warning Test Report\n")
            _ = f.write("=" * 60 + "\n\n")

            for name, result in self.results.items():
                _ = f.write(f"Example: {name}\n")
                _ = f.write(f"Status: {'PASS' if result['success'] else 'FAIL'}\n")
                _ = f.write(f"Duration: {result['duration']:.2f}s\n")
                _ = f.write(f"Warnings: {len(result['warnings'])}\n")
                _ = f.write(f"Log file: {result['log_file']}\n")

                if result["warnings"]:
                    _ = f.write("\nWarnings detected:\n")
                    for warning in result["warnings"]:
                        _ = f.write(f"  {warning}\n")

                _ = f.write("\nFull output:\n")
                _ = f.write(result["output"][:5000])  # Truncate very long outputs
                if len(result["output"]) > 5000:
                    _ = f.write("\n... (output truncated)")
                _ = f.write("\n" + "-" * 60 + "\n\n")

        print(f"\nDetailed report saved to: {filename}")


def main():
    """Main function to run the example tests."""
    print("PyFluent Examples Deprecation Warning Checker")
    print("=" * 60)

    # Find examples directory
    script_dir = Path(__file__).parent
    examples_dir = script_dir / "examples" / "00-fluent"

    if not examples_dir.exists():
        print(f"Error: Examples directory not found at {examples_dir}")
        sys.exit(1)

    # Initialize tester
    max_workers_env = os.environ.get("PYFLUENT_EXAMPLES_WORKERS")
    max_workers = int(max_workers_env) if max_workers_env else None
    tester = ExampleTester(examples_dir, max_workers=max_workers)

    # Run all examples
    try:
        results = tester.run_all_examples()
        tester.print_summary()
        tester.save_detailed_report()

        # Exit with error code if any examples failed or had warnings
        total_warnings = sum(len(r["warnings"]) for r in results.values())
        failed_count = sum(1 for r in results.values() if not r["success"])

        if failed_count > 0:
            print(f"\n❌ {failed_count} examples failed!")
            sys.exit(1)
        elif total_warnings > 0:
            print(f"\n⚠️  {total_warnings} deprecation warnings found!")
            sys.exit(2)  # Different exit code for warnings vs failures
        else:
            print("\n✅ All examples passed without warnings!")
            sys.exit(0)

    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
