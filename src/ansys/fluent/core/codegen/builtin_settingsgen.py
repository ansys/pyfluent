# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
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
from typing import Literal, cast

from ansys.fluent.core.module_config import config
from ansys.fluent.core.solver.flobject import (
    CreatableNamedObjectMixin,
    NamedObject,
    _ChildNamedObjectAccessorMixin,
    get_full_path,
)
from ansys.fluent.core.solver.settings_builtin_data import DATA
from ansys.fluent.core.utils.fluent_version import FluentVersion, all_versions

_PY_FILE = config.codegen_outdir / "solver" / "settings_builtin.py"
_PYI_FILE = config.codegen_outdir / "solver" / "settings_builtin.pyi"

_CLASS_NAME_OVERRIDES = {
    "ReadCaseData": "ReadCaseAndData",
    "WriteCaseData": "WriteCaseAndData",
}

SettingKind = Literal["Singleton", "NamedObject", "Command"]


def _get_settings_root(version: str):
    from ansys.fluent.core.utils import load_module as _load_module

    settings = _load_module(
        f"settings_{version}",
        config.codegen_outdir / "solver" / f"settings_{version}.py",
    )
    return settings.root


def _convert_camel_case_to_snake_case(name: str) -> str:
    """Convert CamelCase to snake_case."""
    # Replace uppercase letters with lowercase and prepend an underscore
    name = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
    return name


def _get_public_class_name(legacy_name: str) -> str:
    return _CLASS_NAME_OVERRIDES.get(legacy_name, legacy_name)


def _get_named_objects_in_path(
    root, path: list[str], kind: SettingKind
) -> tuple[list[str], bool]:
    """Get the named objects in the path and whether the final type of the setting is creatable.

    Parameters
    ----------
    root : type
        The root class to start from.
    path : list[str]
        The path to traverse.
    kind : {'Singleton', 'NamedObject', 'Command'}
        The kind of setting.

    Returns
    -------
    tuple[list[str], bool]
        A tuple containing the list of named objects in the path and a boolean indicating if the final type of the setting is creatable.
    """
    named_objects = []
    cls = root
    comps = path.copy()
    for i, comp in enumerate(comps):
        if comp in cls._child_classes:
            cls = cls._child_classes[comp]
        elif comp in cls._child_aliases:
            child_path = cls._child_aliases[comp][0]
            full_path = get_full_path(comps[:i], child_path.split("/"))
            full_path.extend(comps[i + 1 :])
            return _get_named_objects_in_path(root, full_path, kind)
        else:
            raise KeyError(
                f"Unable to resolve path component {comp!r} in path {path!r} "
                f"for setting kind {kind!r} from class {cls.__name__}."
            )
        if i < len(comps) - 1 and issubclass(cls, NamedObject):
            named_objects.append(comp)
            cls = cls.child_object_type
    is_creatable = False
    if kind == "NamedObject":
        if not issubclass(cls, (NamedObject, _ChildNamedObjectAccessorMixin)):
            raise TypeError(f"{cls.__name__} is not NamedObject type.")
        if issubclass(cls, CreatableNamedObjectMixin):
            is_creatable = True
    return named_objects, is_creatable


def generate(version: str):
    """Generate builtin setting classes."""
    print("Generating builtin settings...")
    config.codegen_outdir.mkdir(exist_ok=True)
    root = _get_settings_root(version)
    version = FluentVersion(version)
    _generate_py_file(root, version)
    _generate_pyi_file()


def _write_name_to_all(f, name: str) -> None:
    f.write(f'    "{name}",\n')


def _write_symbol_to_all(f, name: str, kind: str) -> None:
    _write_name_to_all(f, name)
    if kind == "Command":
        _write_name_to_all(f, _convert_camel_case_to_snake_case(name))


def _write_deprecation_warning(
    f, alias_name: str, preferred_name: str, indentation: str
) -> None:
    f.write(
        f"{indentation}warnings.warn(\"'{alias_name}' is deprecated, use '{preferred_name}' instead.\","
        " PyFluentDeprecationWarning, stacklevel=2)\n"
    )


def _write_deprecated_alias_class(
    f, alias_name: str, preferred_name: str, alias_kind_desc: str
) -> None:
    f.write(f"class {alias_name}({preferred_name}):\n")
    f.write(
        f'    """{alias_name} {alias_kind_desc} (deprecated alias of {preferred_name})."""\n\n'
    )
    f.write("    def __init__(self, *args, **kwargs):\n")
    _write_deprecation_warning(f, alias_name, preferred_name, "       ")
    f.write("       super().__init__(*args, **kwargs)\n\n")


def _resolve_path_for_version(path, version) -> tuple:
    """Resolve a version-keyed path dict to a string for *version*.

    Returns ``(resolved_path, True)`` when supported, ``(None, False)`` otherwise.
    """
    if isinstance(path, str):
        return path, True
    for version_set, p in path.items():
        if version in version_set:
            return p, True
    return None, False


def _write_init_signature(f, kind: str, named_objects: list) -> None:
    """Write ``__init__`` parameters and ``super().__init__()`` call."""
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


def _write_setting_class(
    f, name: str, kind: str, legacy_name: str, named_objects: list
) -> None:
    doc_kind = "command object" if kind == "Command" else "setting"
    f.write(f"class {name}(_{kind}Setting):\n")
    f.write(f'    """{name} {doc_kind}."""\n\n')
    f.write(f'    _db_name = "{legacy_name}"\n\n')
    _write_init_signature(f, kind, named_objects)


def _write_command_callable_class(f, name: str, kind: str, legacy_name: str) -> str:
    """Write the snake_case callable wrapper and return its name."""
    command_name = _convert_camel_case_to_snake_case(name)
    f.write(f"class {command_name}(_{kind}Setting):\n")
    f.write(f'    """{command_name} command."""\n\n')
    f.write(f'    _db_name = "{legacy_name}"\n\n')
    f.write(
        "    def __new__(cls, settings_source: SettingsBase | Solver | None = None, **kwargs):\n"
    )
    f.write("       instance = super().__new__(cls)\n")
    f.write("       instance.__init__(settings_source=settings_source, **kwargs)\n")
    f.write("       return instance(**kwargs)\n\n")
    return command_name


def _write_deprecated_command_aliases(
    f, legacy_name: str, name: str, kind: str, command_name: str
) -> None:
    """Write deprecated alias classes for a renamed command."""
    _write_deprecated_alias_class(f, legacy_name, name, "command object")
    legacy_command_name = _convert_camel_case_to_snake_case(legacy_name)
    f.write(f"class {legacy_command_name}({command_name}):\n")
    f.write(
        f'    """{legacy_command_name} command (deprecated alias of {command_name})."""\n\n'
    )
    f.write(
        "    def __new__(cls, settings_source: SettingsBase | Solver | None = None, **kwargs):\n"
    )
    _write_deprecation_warning(f, legacy_command_name, command_name, "        ")
    f.write(
        "        return super().__new__(cls, settings_source=settings_source, **kwargs)\n\n"
    )


def _write_py_entry(f, legacy_name: str, v, root, version) -> None:
    """Write all classes for one DATA entry to the .py file."""
    kind, path = v
    name = _get_public_class_name(legacy_name)
    path, version_supported = _resolve_path_for_version(path, version)
    if not version_supported:
        return
    named_objects, is_creatable = _get_named_objects_in_path(
        root, path.split("."), cast(SettingKind, kind)
    )
    if kind == "NamedObject":
        kind = f"{'Creatable' if is_creatable else 'NonCreatable'}NamedObject"
    _write_setting_class(f, name, kind, legacy_name, named_objects)
    command_name = None
    if kind == "Command":
        command_name = _write_command_callable_class(f, name, kind, legacy_name)
    if name != legacy_name and kind == "Command":
        _write_deprecated_command_aliases(f, legacy_name, name, kind, command_name)


def _write_pyi_entry(f, legacy_name: str, kind: str, path, name: str) -> None:
    """Write the stub class for one DATA entry to the .pyi file."""
    f.write(f"class {name}(\n")
    if isinstance(path, str):
        path = {all_versions(): path}
    for version_set, p in path.items():
        if kind == "NamedObject":
            p = f"{p}.child_object_type"
        for fv in reversed(list(version_set)):
            f.write(f"    type(settings_root_{fv.number}.{p}),\n")
    f.write("): ...\n\n")
    if name != legacy_name:
        f.write(f"class {legacy_name}({name}): ...\n\n")


def _generate_py_file(root, version) -> None:
    """Write ``settings_builtin.py``."""
    with open(_PY_FILE, "w") as f:
        f.write('"""Solver settings."""\n\n')
        f.write(
            "from ansys.fluent.core.solver.settings_builtin_bases import"
            " _SingletonSetting, _CreatableNamedObjectSetting,"
            " _NonCreatableNamedObjectSetting, _CommandSetting, Solver\n"
            "from ansys.fluent.core.solver.flobject import SettingsBase\n"
            "from ansys.fluent.core.pyfluent_warnings import PyFluentDeprecationWarning\n"
            "import warnings\n\n\n"
        )
        f.write("__all__ = [\n")
        for legacy_name, (kind, _) in DATA.items():
            name = _get_public_class_name(legacy_name)
            _write_symbol_to_all(f, name, kind)
            if name != legacy_name:
                _write_symbol_to_all(f, legacy_name, kind)
        f.write("]\n\n")
        for legacy_name, v in DATA.items():
            _write_py_entry(f, legacy_name, v, root, version)


def _generate_pyi_file() -> None:
    """Write ``settings_builtin.pyi``."""
    with open(_PYI_FILE, "w") as f:
        for version in FluentVersion:
            f.write(
                f"from ansys.fluent.core.generated.solver.settings_{version.number}"
                f" import root as settings_root_{version.number}\n"
            )
        f.write("\n\n")
        for legacy_name, v in DATA.items():
            kind, path = v
            name = _get_public_class_name(legacy_name)
            _write_pyi_entry(f, legacy_name, kind, path, name)


if __name__ == "__main__":
    version = "271"  # for development
    generate(version)
