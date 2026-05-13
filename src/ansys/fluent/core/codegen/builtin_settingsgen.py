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

from ansys.fluent.core.codegen.settingsgen import (
    camel_to_snake_case,
    snake_to_camel_case,
)
from ansys.fluent.core.module_config import config
from ansys.fluent.core.solver.flobject import (
    CreatableNamedObjectMixin,
    NamedObject,
    _ChildNamedObjectAccessorMixin,
)
from ansys.fluent.core.solver.settings_builtin_data import DATA
from ansys.fluent.core.utils.fluent_version import FluentVersion, all_versions

_PY_FILE = config.codegen_outdir / "solver" / "settings_builtin.py"

_CLASS_NAME_OVERRIDES = {
    "ReadCaseData": "ReadCaseAndData",
    "WriteCaseData": "WriteCaseAndData",
}


def _get_settings_root(version: str):
    from ansys.fluent.core.utils import load_module as _load_module

    settings = _load_module(
        f"settings_{version}",
        config.codegen_outdir / "solver" / f"settings_{version}.py",
    )
    return settings.root


def _get_public_class_name(legacy_name: str) -> str:
    return _CLASS_NAME_OVERRIDES.get(legacy_name, legacy_name)


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
        # Check if the class has 'create' its command names (singletons) or its child classes ()
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


def _get_settings_runtime_class_name(root, path: str, kind: str) -> str:
    """Return the generated settings class name for a path.

    For named objects, this returns the child object class name.
    """
    cls = root
    comps = path.split(".")
    for i, comp in enumerate(comps):
        cls = cls._child_classes[comp]
        if i < len(comps) - 1 and issubclass(cls, NamedObject):
            cls = cls.child_object_type
    if kind == "NamedObject":
        if issubclass(cls, NamedObject):
            cls = cls.child_object_type
        elif issubclass(cls, _ChildNamedObjectAccessorMixin):
            # Accessor classes are already the concrete child settings type.
            pass
        else:
            raise TypeError(f"{cls.__name__} is not NamedObject type.")
    return cls.__name__


def generate(version: str):
    """Generate builtin setting classes."""
    print("Generating builtin settings...")
    config.codegen_outdir.mkdir(exist_ok=True)
    root = _get_settings_root(version)
    version: FluentVersion = FluentVersion(version)
    with open(_PY_FILE, "w") as f:

        def _write_name_to_all(name: str):
            f.write(f'    "{name}",\n')

        def _write_command_name_to_all(command_class_name: str):
            _write_name_to_all(camel_to_snake_case(command_class_name))

        def _write_symbol_to_all(name: str, kind: str):
            _write_name_to_all(name)
            if kind == "Command":
                _write_command_name_to_all(name)

        def _write_deprecation_warning(
            alias_name: str,
            preferred_name: str,
            indentation: str,
        ):
            f.write(
                f"{indentation}warnings.warn(\"'{alias_name}' is deprecated, use '{preferred_name}' instead.\", PyFluentDeprecationWarning, stacklevel=2)\n"
            )

        def _write_deprecated_alias_class(
            alias_name: str,
            preferred_name: str,
            alias_kind_desc: str,
        ):
            f.write(f"class {alias_name}({preferred_name}):\n")
            f.write(
                f'    """{alias_name} {alias_kind_desc} (deprecated alias of {preferred_name})."""\n\n'
            )
            f.write("    def __init__(self, *args, **kwargs):\n")
            _write_deprecation_warning(alias_name, preferred_name, "       ")
            f.write("       super().__init__(*args, **kwargs)\n\n")

        f.write('"""Solver settings."""\n\n')
        f.write(
            "from ansys.fluent.core.solver.settings_builtin_bases import _SingletonSetting, _CreatableNamedObjectSetting, _NonCreatableNamedObjectSetting, _CommandSetting, Solver\n"
            "from ansys.fluent.core.solver.flobject import SettingsBase\n"
            "from ansys.fluent.core.pyfluent_warnings import PyFluentDeprecationWarning\n"
            "import warnings\n\n\n"
        )
        f.write("__all__ = [\n")
        for legacy_name, (kind, _, _) in DATA.items():
            name = _get_public_class_name(legacy_name)
            _write_symbol_to_all(name, kind)
            if name != legacy_name:
                _write_symbol_to_all(legacy_name, kind)
        f.write("]\n\n")
        for legacy_name, v in DATA.items():
            kind, path, _ = v
            name = _get_public_class_name(legacy_name)
            if isinstance(path, dict):  # version constraint key with settings API path values
                version_supported = False
                for version_set, p in path.items():
                    if version in version_set:
                        path = p
                        version_supported = True
                        break
                if not version_supported:
                    continue
            _, final_type = _get_named_objects_in_path(root, path, kind)
            if kind == "NamedObject":
                kind = f"{final_type}NamedObject"
            f.write(f"class {name}(_{kind}Setting):\n")
            doc_kind = "command object" if kind == "Command" else "setting"
            f.write(f'    """{name} {doc_kind}."""\n\n')
            f.write(f'    _db_name = "{legacy_name}"\n\n')
            f.write("\n\n")
            if kind == "Command":
                command_name = camel_to_snake_case(name)
                f.write(f"class {command_name}(_{kind}Setting):\n")
                f.write(f'    """{command_name} command."""\n\n')
                f.write(f'    _db_name = "{legacy_name}"\n\n')
                f.write(
                    "    def __new__(cls, settings_source: SettingsBase | Solver | None = None, **kwargs):\n"
                )
                f.write("       instance = super().__new__(cls)\n")
                f.write(
                    "       instance.__init__(settings_source=settings_source, **kwargs)\n"
                )
                f.write("       return instance(**kwargs)\n\n")

            if name != legacy_name:
                if kind == "Command":
                    _write_deprecated_alias_class(
                        alias_name=legacy_name,
                        preferred_name=name,
                        alias_kind_desc="command object",
                    )
                    legacy_command_name = camel_to_snake_case(legacy_name)
                    f.write(f"class {legacy_command_name}({command_name}):\n")
                    f.write(
                        f'    """{legacy_command_name} command (deprecated alias of {command_name})."""\n\n'
                    )
                    f.write(
                        "    def __new__(cls, settings_source: SettingsBase | Solver | None = None, **kwargs):\n"
                    )
                    _write_deprecation_warning(
                        legacy_command_name, command_name, "        "
                    )
                    f.write(
                        "        return super().__new__(cls, settings_source=settings_source, **kwargs)\n\n"
                    )

    # Generate version-specific .pyi files
    pyi_file = (
        config.codegen_outdir / "solver" / f"settings_builtin_{version.number}.pyi"
    )
    pyi_entries = []  # list of (decorator: str|None, class_def: str)
    base_class_names = set()  # PascalCase names to import from settings_{version}
    for legacy_name, v in DATA.items():
        kind, path, recip = v  # reciprical name (singleton -> parent, parent -> singleton)
        name = _get_public_class_name(legacy_name)
        if isinstance(path, dict):
            version_supported = False
            for version_set, p in path.items():
                if version in version_set:
                    path = p
                    version_supported = True
                    break
            if not version_supported:
                continue
        _, final_type = _get_named_objects_in_path(root, path, kind)
        # Resolve the concrete class name (PascalCase) for use as a base.
        raw_cls_name = _get_settings_runtime_class_name(root, path, kind)
        base_cls_name = snake_to_camel_case(raw_cls_name)
        base_class_names.add(base_cls_name)
        # Always alias base imports to avoid any shadowing
        ref_name = f"{base_cls_name}Base"
        decorator = None
        if kind == "Singleton" and recip:
            decorator = f'@deprecated("Use {recip}.all() instead")'
        if kind == "NamedObject":
            effective_kind = f"{final_type}NamedObject"
            lines = [
                f"class {name}(\n",
                f"    _{effective_kind}Setting,\n",
                f"    {ref_name},\n",
                "):\n",
            ]
            if final_type == "Creatable":
                lines.append(
                    f"    create = settings_root_{version.number}.{path}.create\n"
                )
            else:
                lines.append("    ...\n")
        else:
            lines = [
                f"class {name}(\n",
                f"    _{kind}Setting,\n",
                f"    {ref_name},\n",
                "):\n",
            ]
            if kind == "Singleton" and _has_create_method(root, path):
                lines.append(
                    f"    create = settings_root_{version.number}.{path}.create\n"
                )
            else:
                lines.append("    ...\n")
        lines.append("\n")
        pyi_entries.append((decorator, "".join(lines)))

        if name != legacy_name:
            pyi_entries.append((None, f"class {legacy_name}({name}): ...\n\n"))

    with pyi_file.open("w") as f:
        f.write(
            "from typing_extensions import deprecated\n"
            "from ansys.fluent.core.solver.settings_builtin_bases import _SingletonSetting, _CreatableNamedObjectSetting, _NonCreatableNamedObjectSetting, _CommandSetting\n"
        )
        # Import concrete base classes from the versioned settings stub with Base suffix
        f.write(
            f"from ansys.fluent.core.generated.solver.settings_{version.number} import (\n"
        )
        for cls_name in sorted(base_class_names):
            f.write(f"    {cls_name} as {cls_name}Base,\n")
        f.write(")\n")
        # Keep root import for create-method body references.
        f.write(
            f"from ansys.fluent.core.generated.solver.settings_{version.number} import root as settings_root_{version.number}\n"
        )
        f.write("\n\n")
        for decorator, cls_def in pyi_entries:
            if decorator:
                f.write(decorator + "\n")
            f.write(cls_def)

    # Keep main settings_builtin.pyi as a latest-version re-export.
    generate_main_pyi(str(version.number))


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
