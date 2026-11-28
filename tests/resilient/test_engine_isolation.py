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

"""The resilient engine must stay product-agnostic and relocatable.

These checks keep the engine ready to move to its own distribution: its modules
may import only the standard library and each other (relatively).
"""

import ast
from pathlib import Path
import sys

import pytest

import ansys.fluent.core.resilient.engine as engine

pytestmark = pytest.mark.resilient

_ENGINE_DIR = Path(engine.__file__).parent
_MODULES = sorted(_ENGINE_DIR.glob("*.py"))


@pytest.mark.parametrize("module", _MODULES, ids=lambda p: p.name)
def test_engine_imports_only_stdlib_and_relative_modules(module):
    tree = ast.parse(module.read_text(encoding="utf-8"))
    offending = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.level == 0 and node.module.split(".")[0] not in (
                sys.stdlib_module_names | {"__future__"}
            ):
                offending.append(node.module)
        elif isinstance(node, ast.Import):
            offending.extend(
                alias.name
                for alias in node.names
                if alias.name.split(".")[0] not in sys.stdlib_module_names
            )
    assert not offending, f"{module.name} imports {offending}"


def test_engine_package_exports_its_public_api():
    for name in engine.__all__:
        assert hasattr(engine, name), name
