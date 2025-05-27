# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
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

"""Get the git build info."""

from collections import OrderedDict
import subprocess

import ansys.fluent.core as pyfluent


def get_build_version():
    """Get build version."""
    build_details = OrderedDict()
    try:
        last_commit_time = (
            subprocess.check_output(["git", "log", "-n", "1", "--pretty=tformat:%ad"])
            .decode("ascii")
            .strip()
            .split()
        )
        time_zone = last_commit_time[5][:3] + ":" + last_commit_time[5][3:] + ":00"
        build_details["Build Time"] = (
            f"{last_commit_time[1]} {last_commit_time[2]} {last_commit_time[4]} {last_commit_time[3]} UTC{time_zone}"
        )
        build_details["Current Version"] = f"{pyfluent.__version__}"
        build_details["ShaID"] = (
            subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
            .decode("ascii")
            .strip()
        )
        build_details["Branch"] = (
            subprocess.check_output(["git", "branch", "--show-current"])
            .decode("ascii")
            .strip()
        )
    except Exception:
        pass
    return build_details


def get_build_version_string():
    """Get build version string."""
    return "  ".join([f"{k}: {v}" for k, v in get_build_version().items()])
