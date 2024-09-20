"""Generate builtin setting classes."""

from ansys.fluent.core import CODEGEN_OUTDIR, FluentVersion
from ansys.fluent.core.solver.flobject import CreatableNamedObjectMixin
from ansys.fluent.core.solver.settings_builtin_data import DATA

_PY_FILE = CODEGEN_OUTDIR / "solver" / "settings_builtin.py"
_PYI_FILE = CODEGEN_OUTDIR / "solver" / "settings_builtin.pyi"


def _get_settings_root(version: str):
    from ansys.fluent.core import CODEGEN_OUTDIR, CODEGEN_ZIP_SETTINGS, utils

    if CODEGEN_ZIP_SETTINGS:
        importer = zipimporter(
            str(CODEGEN_OUTDIR / "solver" / f"settings_{version}.zip")
        )
        settings = importer.load_module("settings")
    else:
        settings = utils.load_module(
            f"settings_{version}",
            CODEGEN_OUTDIR / "solver" / f"settings_{version}" / "__init__.py",
        )
    return settings.root


def _get_named_object_type(root, path):
    for comp in path.split("."):
        root = root._child_classes[comp]
    return (
        "Creatable" if issubclass(root, CreatableNamedObjectMixin) else "NonCreatable"
    )


def generate(version: str):
    """Generate builtin setting classes."""
    CODEGEN_OUTDIR.mkdir(exist_ok=True)
    root = _get_settings_root(version)
    with open(_PY_FILE, "w") as f:
        f.write('"""Solver settings."""\n\n')
        f.write(
            "from ansys.fluent.core.solver.settings_builtin_bases import _SingletonSetting, _CreatableNamedObjectSetting, _NonCreatableNamedObjectSetting\n\n\n"
        )
        f.write("__all__ = [\n")
        for name, _ in DATA.items():
            f.write(f'    "{name}",\n')
        f.write("]\n\n")
        for name, v in DATA.items():
            kind, path = v
            if kind == "NamedObject":
                if isinstance(path, dict):
                    if FluentVersion(version) not in path:
                        continue
                    path = path[FluentVersion(version)]
                kind = f"{_get_named_object_type(root, path)}NamedObject"
            f.write(f"class {name}(_{kind}Setting):\n")
            f.write(f'    """{name} setting."""\n\n')

    with open(_PYI_FILE, "w") as f:
        for version in FluentVersion:
            f.write(
                f"from ansys.fluent.core.generated.solver.settings_{version.number} import root as settings_root_{version.number}\n"
            )
        f.write("\n\n")
        for name, v in DATA.items():
            kind, path = v
            if isinstance(path, dict):
                if FluentVersion(version) not in path:
                    continue
                path = path[FluentVersion(version)]
            f.write(f"class {name}(\n")
            if isinstance(path, str):
                path = {v: path for v in FluentVersion}
            for v, p in path.items():
                if kind == "NamedObject":
                    p = f"{p}.child_object_type"
                f.write(f"    type(settings_root_{v.number}.{p}),\n")
            f.write("): ...\n\n")


if __name__ == "__main__":
    version = "251"  # for development
    generate(version)
