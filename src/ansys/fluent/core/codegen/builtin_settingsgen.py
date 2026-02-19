# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
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


def _has_create_method(root, path):
    """Check if a setting object has a create method."""
    try:
        cls = root
        comps = path.split(".")
        for comp in comps:
            cls = cls._child_classes[comp]
        # Check if the class has 'create' in its child classes or command names
        return "create" in getattr(cls, "_child_classes", {}) or "create" in getattr(
            cls, "command_names", []
        )
    except (KeyError, AttributeError):
        return False


def _get_reciprocal_name(name: str) -> str | None:
    """Get the reciprocal name (singular/plural counterpart) from DATA."""
    try:
        return DATA[name][2]
    except KeyError:
        return None


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
        for name, (kind, _, _) in DATA.items():
            f.write(f'    "{name}",\n')
            if kind == "Command":
                command_name = _convert_camel_case_to_snake_case(name)
                f.write(f'    "{command_name}",\n')
        f.write("]\n\n")
        for name, v in DATA.items():
            kind, path, _ = v
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

    # Generate version-specific .pyi files
    pyi_file = (
        config.codegen_outdir / "solver" / f"settings_builtin_{version.number}.pyi"
    )
    with open(pyi_file, "w") as f:
        # Import base classes and deprecated decorator
        f.write(
            "from typing_extensions import deprecated\n"
            "from ansys.fluent.core.solver.settings_builtin_bases import _SingletonSetting, _CreatableNamedObjectSetting, _NonCreatableNamedObjectSetting, _CommandSetting\n"
        )
        # Import version-specific root for type hints
        f.write(
            f"from ansys.fluent.core.generated.solver.settings_{version.number} import root as settings_root_{version.number}\n"
        )
        f.write("\n\n")
        for name, v in DATA.items():
            kind, path, recip = v
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
                path_with_child = f"{path}.child_object_type"
                f.write(f"class {name}(\n")
                f.write(f"    _{kind}Setting,\n")
                f.write(
                    f"    type(settings_root_{version.number}.{path_with_child}),\n"
                )
                f.write("):\n")
                if final_type == "Creatable":
                    f.write(
                        f"    create = settings_root_{version.number}.{path}.create\n"
                    )
                else:
                    f.write("    ...\n")
                f.write("\n")
            else:
                # For Singleton and Command types
                # Check if this is a plural class by looking at its reciprocal
                if kind == "Singleton" and recip:
                    # Add deprecated decorator for plural container classes
                    f.write(f'@deprecated("Use {recip}.all() instead")\n')

                f.write(f"class {name}(\n")
                f.write(f"    _{kind}Setting,\n")
                f.write(f"    type(settings_root_{version.number}.{path}),\n")
                f.write("):\n")
                # Check if singleton has create method
                if kind == "Singleton" and _has_create_method(root, path):
                    f.write(
                        f"    create = settings_root_{version.number}.{path}.create\n"
                    )
                else:
                    f.write("    ...\n")
                f.write("\n")


def generate_main_pyi(version_str: str):
    """Generate main settings_builtin.pyi that imports from a specific version."""
    _MAIN_PYI_FILE = config.codegen_outdir / "solver" / "settings_builtin.pyi"
    version_obj = FluentVersion(version_str)
    with open(_MAIN_PYI_FILE, "w") as f:
        f.write(f"# Re-export from version {version_str}\n")
        f.write(
            f"from ansys.fluent.core.generated.solver.settings_builtin_{version_obj.number} import *\n"
        )


if __name__ == "__main__":
    # Generate for all available versions
    versions = sorted([v.number for v in all_versions()])
    for version in versions:
        try:
            generate(str(version))
        except Exception as e:
            print(f"Failed to generate for version {version}: {e}")
    # Generate main .pyi that imports from the latest version
    generate_main_pyi(str(versions[-1]))
