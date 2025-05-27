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

"""Module to write Fluent version information."""

from ansys.fluent.core import CODEGEN_OUTDIR, FluentVersion, launch_fluent


def print_fluent_version(app_utilities):
    """Write Fluent version information to file."""
    version = FluentVersion(app_utilities.get_product_version()).number
    build_info = app_utilities.get_build_info()
    version_file = (CODEGEN_OUTDIR / f"fluent_version_{version}.py").resolve()
    with open(version_file, "w", encoding="utf8") as f:
        f.write(f'FLUENT_VERSION = "{version}"\n')
        f.write(f'FLUENT_BUILD_TIME = "{build_info["build_time"]}"\n')
        f.write(f'FLUENT_BUILD_ID = "{build_info["build_id"]}"\n')
        f.write(f'FLUENT_REVISION = "{build_info["vcs_revision"]}"\n')
        f.write(f'FLUENT_BRANCH = "{build_info["vcs_branch"]}"\n')


if __name__ == "__main__":
    solver = launch_fluent()
    print_fluent_version(solver._app_utilities)
