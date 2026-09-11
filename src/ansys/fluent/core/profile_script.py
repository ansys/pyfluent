# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
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

"""Profile script for measuring ansys.fluent.core import performance.

Run with:
    python -X importtime profile_script.py
    python -X importtime -c "import ansys.fluent.core"

This script measures the wall-clock time for importing the pyfluent public API.
"""

import time

t0 = time.perf_counter()
import ansys.fluent.core as pyfluent  # noqa: E402

t1 = time.perf_counter()
print(f"import ansys.fluent.core: {(t1 - t0) * 1000:.1f} ms")

# Verify key symbols are accessible (lazy or eager)
for _sym in ("launch_fluent", "connect_to_fluent", "FluentVersion", "config"):
    if not hasattr(pyfluent, _sym):
        raise RuntimeError(f"Missing expected symbol: {_sym}")
