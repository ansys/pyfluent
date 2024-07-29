"""Generate builtin setting classes."""

from ansys.fluent.core import CODEGEN_OUTDIR, FluentVersion
from ansys.fluent.core.solver.settings_builtin_data import DATA

_PY_FILE = CODEGEN_OUTDIR / "solver" / "settings_builtin.py"
_PYI_FILE = CODEGEN_OUTDIR / "solver" / "settings_builtin.pyi"


def generate():
    """Generate builtin setting classes."""
    CODEGEN_OUTDIR.mkdir(exist_ok=True)
    with open(_PY_FILE, "w") as f:
        f.write('"""Solver settings."""\n\n')
        f.write(
            "from ansys.fluent.core.solver.settings_builtin_bases import _SingletonSetting, _NamedObjectSetting\n\n\n"
        )
        f.write("__all__ = [\n")
        for name, _ in DATA.items():
            f.write(f'    "{name}",\n')
        f.write("]\n\n")
        for name, v in DATA.items():
            kind, path = v
            f.write(f"class {name}(_{kind}Setting):\n")
            f.write(f'    """{name} setting."""\n\n')
            f.write(f'    path = "{path}"\n\n')

    with open(_PYI_FILE, "w") as f:
        for version in FluentVersion:
            f.write(
                f"from ansys.fluent.core.generated.solver.settings_{version} import root as settings_root_{version}\n"
            )
        f.write("\n\n")
        for name, v in DATA.items():
            kind, path = v
            f.write(f"class {name}(\n")
            if kind == "NamedObject":
                path = f"{path}.child_object_type"
            for version in FluentVersion:
                f.write(f"    type(settings_root_{version}.{path}),\n")
            f.write("): ...\n\n")


if __name__ == "__main__":
    generate()
