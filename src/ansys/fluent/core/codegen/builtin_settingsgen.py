"""Generate builtin setting classes."""

from ansys.fluent.core import CODEGEN_OUTDIR, FluentVersion
from ansys.fluent.core.solver.flobject import CreatableNamedObjectMixin, NamedObject
from ansys.fluent.core.solver.settings_builtin_data import DATA

_PY_FILE = CODEGEN_OUTDIR / "solver" / "settings_builtin.py"
_PYI_FILE = CODEGEN_OUTDIR / "solver" / "settings_builtin.pyi"


def _get_settings_root(version: str):
    from ansys.fluent.core import CODEGEN_OUTDIR, utils

    settings = utils.load_module(
        f"settings_{version}",
        CODEGEN_OUTDIR / "solver" / f"settings_{version}.py",
    )
    return settings.root


def _get_named_objects_in_path(root, path, kind):
    named_objects = []
    cls = root
    comps = path.split(".")
    for i, comp in enumerate(comps):
        cls = cls._child_classes[comp]
        if i < len(comps) - 1 and issubclass(cls, NamedObject):
            named_objects.append(comp)
            cls = cls.child_object_type
    final_type = ""
    if kind == "NamedObject":
        if issubclass(cls, CreatableNamedObjectMixin):
            final_type = "Creatable"
        else:
            final_type = "NonCreatable"
    return named_objects, final_type


def generate(version: str):
    """Generate builtin setting classes."""
    print("Generating builtin settings...")
    CODEGEN_OUTDIR.mkdir(exist_ok=True)
    root = _get_settings_root(version)
    version = FluentVersion(version)
    with open(_PY_FILE, "w") as f:
        f.write('"""Solver settings."""\n\n')
        f.write(
            "from ansys.fluent.core.solver.settings_builtin_bases import _SingletonSetting, _CreatableNamedObjectSetting, _NonCreatableNamedObjectSetting, Solver\n"
            "from ansys.fluent.core.solver.flobject import SettingsBase\n\n\n"
        )
        f.write("__all__ = [\n")
        for name, _ in DATA.items():
            f.write(f'    "{name}",\n')
        f.write("]\n\n")
        for name, v in DATA.items():
            kind, path = v
            if isinstance(path, dict):
                if version not in path:
                    continue
                path = path[version]
            named_objects, final_type = _get_named_objects_in_path(root, path, kind)
            if kind == "NamedObject":
                kind = f"{final_type}NamedObject"
            f.write(f"class {name}(_{kind}Setting):\n")
            f.write(f'    """{name} setting."""\n\n')
            f.write("    def __init__(self")
            for named_object in named_objects:
                f.write(f", {named_object}: str")
            f.write(", settings_source: SettingsBase | Solver | None = None")
            if kind == "NonCreatableNamedObject":
                f.write(", name: str = None")
            elif kind == "CreatableNamedObject":
                f.write(", name: str = None, new_instance_name: str = None")
            f.write("):\n")
            f.write("        super().__init__(settings_source=settings_source")
            if kind == "NonCreatableNamedObject":
                f.write(", name=name")
            elif kind == "CreatableNamedObject":
                f.write(", name=name, new_instance_name=new_instance_name")
            for named_object in named_objects:
                f.write(f", {named_object}={named_object}")
            f.write(")\n\n")

    with open(_PYI_FILE, "w") as f:
        for version in FluentVersion:
            f.write(
                f"from ansys.fluent.core.generated.solver.settings_{version.number} import root as settings_root_{version.number}\n"
            )
        f.write("\n\n")
        for name, v in DATA.items():
            kind, path = v
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
