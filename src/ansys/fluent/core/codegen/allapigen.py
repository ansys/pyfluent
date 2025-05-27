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

"""Module to generate Fluent API classes."""

import argparse
import os
from pathlib import Path
import pickle

from ansys.fluent.core.codegen import (  # noqa: F401
    builtin_settingsgen,
    datamodelgen,
    settingsgen,
    tuigen,
)
from ansys.fluent.core.search import get_api_tree_file_name


def _update_first_level(d, u):
    for k in d:
        d[k].update(u.get(k, {}))


def generate(version: str, static_infos: dict, verbose: bool = False):
    """Generate Fluent API classes."""
    api_tree = {"<meshing_session>": {}, "<solver_session>": {}}
    _update_first_level(api_tree, tuigen.generate(version, static_infos, verbose))
    _update_first_level(api_tree, datamodelgen.generate(version, static_infos, verbose))
    _update_first_level(api_tree, settingsgen.generate(version, static_infos, verbose))
    api_tree_file = get_api_tree_file_name(version)
    Path(api_tree_file).parent.mkdir(parents=True, exist_ok=True)
    with open(api_tree_file, "wb") as f:
        pickle.dump(api_tree, f)
    if os.getenv("PYFLUENT_CODEGEN_SKIP_BUILTIN_SETTINGS") != "1":
        builtin_settingsgen.generate(version)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A script to write Fluent API files with an optional verbose output."
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show paths of written Fluent API files.",
    )
    args = parser.parse_args()
    generate(verbose=args.verbose)
