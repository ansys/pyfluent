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
        "version",
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
