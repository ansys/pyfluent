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

"""Generate builtin setting classes."""

import re

from ansys.fluent.core import FluentVersion, config
from ansys.fluent.core.solver.flobject import (
    CreatableNamedObjectMixin,
    NamedObject,
    _ChildNamedObjectAccessorMixin,
)
from ansys.fluent.core.solver.settings_builtin_data import DATA
from ansys.fluent.core.utils.fluent_version import all_versions

_PY_FILE = config.codegen_outdir / "solver" / "settings_builtin.py"
_PYI_FILE = config.codegen_outdir / "solver" / "settings_builtin.pyi"


def _get_settings_root(version: str):
    from ansys.fluent.core import config, utils

    settings = utils.load_module(
        f"settings_{version}",
        config.codegen_outdir / "solver" / f"settings_{version}.py",
    )
    return settings.root


def _convert_camel_case_to_snake_case(name: str) -> str:
    """Convert CamelCase to snake_case."""
    # Replace uppercase letters with lowercase and prepend an underscore
    name = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
    return name


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
        if not issubclass(cls, (NamedObject, _ChildNamedObjectAccessorMixin)):
            raise TypeError(f"{cls.__name__} is not NamedObject type.")
        if issubclass(cls, CreatableNamedObjectMixin):
            final_type = "Creatable"
        else:
            final_type = "NonCreatable"
    return named_objects, final_type


def generate(version: str):
    """Generate builtin setting classes."""
    print("Generating builtin settings...")
    config.codegen_outdir.mkdir(exist_ok=True)
    root = _get_settings_root(version)
    version = FluentVersion(version)
    with open(_PY_FILE, "w") as f:
        f.write('"""Solver settings."""\n\n')
        f.write(
            "from ansys.fluent.core.solver.settings_builtin_bases import _SingletonSetting, _CreatableNamedObjectSetting, _NonCreatableNamedObjectSetting, _CommandSetting, Solver\n"
            "from ansys.fluent.core.solver.flobject import SettingsBase\n\n\n"
        )
        f.write("__all__ = [\n")
        for name, (kind, _) in DATA.items():
            f.write(f'    "{name}",\n')
            if kind == "Command":
                command_name = _convert_camel_case_to_snake_case(name)
                f.write(f'    "{command_name}",\n')
        f.write("]\n\n")
        for name, v in DATA.items():
            kind, path = v
            if isinstance(path, dict):
                version_supported = False
                for version_set, p in path.items():
                    if version in version_set:
                        path = p
                        version_supported = True
                        break
                if not version_supported:
                    continue
            named_objects, final_type = _get_named_objects_in_path(root, path, kind)
            if kind == "NamedObject":
                kind = f"{final_type}NamedObject"
            f.write(f"class {name}(_{kind}Setting):\n")
            doc_kind = "command object" if kind == "Command" else "setting"
            f.write(f'    """{name} {doc_kind}."""\n\n')
            f.write(f'    _db_name = "{name}"\n\n')
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
            if kind == "Command":
                command_name = _convert_camel_case_to_snake_case(name)
                f.write(f"class {command_name}(_{kind}Setting):\n")
                f.write(f'    """{command_name} command."""\n\n')
                f.write(f'    _db_name = "{name}"\n\n')
                f.write(
                    "    def __new__(cls, settings_source: SettingsBase | Solver | None = None, **kwargs):\n"
                )
                f.write("       instance = super().__new__(cls)\n")
                f.write(
                    "       instance.__init__(settings_source=settings_source, **kwargs)\n"
                )
                f.write("       return instance(**kwargs)\n\n")

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
                path = {all_versions(): path}
            for version_set, p in path.items():
                if kind == "NamedObject":
                    p = f"{p}.child_object_type"
                for v in reversed(list(version_set)):
                    f.write(f"    type(settings_root_{v.number}.{p}),\n")
            f.write("): ...\n\n")


if __name__ == "__main__":
    version = "261"  # for development
    generate(version)
