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

import ast

import pytest

from ansys.fluent.core import CODEGEN_OUTDIR


@pytest.mark.codegen_required
@pytest.mark.fluent_version("==25.1")
def test_settings_stub():
    # The type-stub files, which are generated for settings API, are parsed by the
    # intellisense engine while typing in editors like vscode. This test validates the
    # information contained in a type-stub file.
    version = "251"
    stub_file = CODEGEN_OUTDIR / "solver" / f"settings_{version}.pyi"
    assert stub_file.exists()
    with open(stub_file) as f:
        module_def = ast.parse(f.read())
    assert isinstance(module_def, ast.Module)
    assert any(isinstance(x, ast.ImportFrom) for x in module_def.body)
    class_def = next(
        x for x in module_def.body if isinstance(x, ast.ClassDef) and x.name == "export"
    )
    assert len(class_def.bases) > 0
    assigns = [x for x in class_def.body if isinstance(x, ast.AnnAssign)]
    for class_attr in [
        "_version",
        "fluent_name",
        "_python_name",
        "child_names",
        "command_names",
    ]:
        print(class_attr)
        assert any(x.target.id == class_attr for x in assigns)
    fn_def = next(x for x in class_def.body if isinstance(x, ast.FunctionDef))
    assert ast.get_docstring(fn_def)
    assert all(x.annotation for x in fn_def.args.args[1:])
