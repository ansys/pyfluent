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

"""Regression tests guarding `import ansys.fluent.core` cold-import performance.

See issue #4924 - avoid eager imports where possible. These tests use a
subprocess for cold-import measurement to avoid cross-test module caching
contamination.
"""

import importlib
import re
import statistics
import subprocess
import sys

import pytest

_COLD_IMPORT_CMD = [sys.executable, "-c", "import ansys.fluent.core"]


class TestImportPerformance:
    """Validate `import ansys.fluent.core` stays fast (issue #4924)."""

    HARD_LIMIT_MS = 300
    STRETCH_GOAL_MS = 100

    @staticmethod
    def _measure_cold_import_ms() -> float:
        timing_cmd = [
            sys.executable,
            "-c",
            "import time; t = time.perf_counter(); import ansys.fluent.core; "
            "print((time.perf_counter() - t) * 1000)",
        ]
        result = subprocess.run(timing_cmd, capture_output=True, text=True, check=True)
        return float(result.stdout.strip())

    def test_cold_import_under_hard_limit(self):
        """`import ansys.fluent.core` must stay under the 300ms hard limit."""
        samples = [self._measure_cold_import_ms() for _ in range(3)]
        median = statistics.median(samples)
        assert median < self.HARD_LIMIT_MS, (
            f"Cold import median {median:.1f}ms exceeds hard limit of "
            f"{self.HARD_LIMIT_MS}ms. Samples: {samples}"
        )

    def test_cold_import_warn_if_slow(self):
        """Soft check: warn (via skip) if we're not meeting the stretch goal."""
        samples = [self._measure_cold_import_ms() for _ in range(3)]
        median = statistics.median(samples)
        if median >= self.STRETCH_GOAL_MS:
            pytest.skip(
                f"Cold import median {median:.1f}ms exceeds stretch goal of "
                f"{self.STRETCH_GOAL_MS}ms (not a hard failure). Samples: {samples}"
            )

    def test_warm_import_under_limit(self):
        """Repeated (warm) imports via importlib.reload should stay fast."""
        import ansys.fluent.core as pyfluent

        timings = []
        for _ in range(5):
            import time

            t = time.perf_counter()
            importlib.reload(pyfluent)
            timings.append((time.perf_counter() - t) * 1000)

        median = statistics.median(timings)
        assert median < 150, f"Warm reload median {median:.1f}ms is too slow."

    def test_importtime_cumulative(self):
        """Parse `-X importtime` output to ensure the cumulative cost of
        importing `ansys.fluent.core` itself stays under the hard limit.
        """
        result = subprocess.run(
            [sys.executable, "-X", "importtime", "-c", "import ansys.fluent.core"],
            capture_output=True,
            text=True,
            check=True,
        )
        match = None
        for line in result.stderr.splitlines():
            if line.strip().endswith("ansys.fluent.core"):
                match = line
        assert (
            match is not None
        ), "Could not find ansys.fluent.core in importtime output"

        # Format: "import time:   <self us> | <cumulative us> | <name>"
        parts = [p.strip() for p in match.split("|")]
        cumulative_us = int(re.sub(r"[^\d]", "", parts[1]))
        cumulative_ms = cumulative_us / 1000
        assert cumulative_ms < TestImportPerformance.HARD_LIMIT_MS, (
            f"ansys.fluent.core cumulative import time {cumulative_ms:.1f}ms "
            f"exceeds hard limit of {TestImportPerformance.HARD_LIMIT_MS}ms"
        )
