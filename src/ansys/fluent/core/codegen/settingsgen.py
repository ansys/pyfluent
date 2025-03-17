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

"""Module to generate the classes corresponding to the Fluent settings API."""

import argparse
import hashlib
from io import StringIO
import keyword
import pickle
import time
from typing import IO

import ansys.fluent.core as pyfluent
from ansys.fluent.core import launch_fluent
from ansys.fluent.core.codegen import StaticInfoType, walk_api
from ansys.fluent.core.solver import _docstrings
from ansys.fluent.core.solver.flobject import (
    ListObject,
    NamedObject,
    get_cls,
    to_python_name,
)
from ansys.fluent.core.utils.fix_doc import fix_settings_doc
from ansys.fluent.core.utils.fluent_version import get_version_for_file_name


def _construct_bases(original_bases, child_object_name):
    bases = []
    for base in original_bases:
        if base in (
            "NamedObject",
            "ListObject",
            "CreatableNamedObjectMixinOld",
            "CreatableNamedObjectMixin",
            "_NonCreatableNamedObjectMixin",
        ):
            bases.append(f"{base}[{child_object_name}]")
        else:
            bases.append(base)
    return bases


def _construct_bases_stub(original_bases, child_object_name):
    bases = []
    for base in original_bases:
        # Removing these bases from stub file
        # as intellisense doesn't work otherwise
        if base in (
            "_ChildNamedObjectAccessorMixin",
            "CreatableNamedObjectMixinOld",
            "CreatableNamedObjectMixin",
            "_NonCreatableNamedObjectMixin",
        ):
            continue
        elif base in (
            "NamedObject",
            "ListObject",
        ):
            bases.append(f"{base}[{child_object_name}]")
        else:
            bases.append(base)
    return bases


def strip_parameters(docstring: str) -> str:
    """
    Strips everything from the 'Parameters' section onwards in the given docstring.

    Parameters
    ----------
    docstring: str
        The original docstring to process.

    Returns
    -------
        The modified docstring with the 'Parameters' section removed.
    """
    lines = docstring.strip().splitlines()
    filtered_lines = []

    for line in lines:
        if line.strip().startswith("Parameters"):
            break
        filtered_lines.append(line)

    return "\n".join(filtered_lines).strip()


def _populate_data(cls, api_tree: dict, version: str) -> dict:
    data = {}
    data["version"] = version
    data["name"] = cls.__name__
    data["bases"] = [base.__name__ for base in cls.__bases__]
    if "command" in cls.__doc__:
        data["doc"] = strip_parameters(cls.__doc__)
    else:
        data["doc"] = fix_settings_doc(cls.__doc__)
    data["fluent_name"] = getattr(cls, "fluent_name")
    data["child_names"] = getattr(cls, "child_names", [])
    command_names = getattr(cls, "command_names", [])
    data["command_names"] = command_names
    query_names = getattr(cls, "query_names", [])
    data["query_names"] = query_names
    data["argument_names"] = getattr(cls, "argument_names", [])
    data["child_aliases"] = getattr(cls, "_child_aliases", {})
    data["return_type"] = getattr(cls, "return_type", None)
    child_classes = data.setdefault("child_classes", {})
    for k, v in cls._child_classes.items():
        if k in command_names:
            api_tree[k] = "Command"
            child_classes[k] = _populate_data(v, {}, version)
        elif k in query_names:
            api_tree[k] = "Query"
            child_classes[k] = _populate_data(v, {}, version)
        else:
            if issubclass(v, NamedObject):
                api_key = f"{k}:<name>"
            elif issubclass(v, ListObject):
                api_key = f"{k}:<index>"
            else:
                api_key = k
            child_api_tree = api_tree.setdefault(api_key, {})
            child_classes[k] = _populate_data(v, child_api_tree, version)
            if not child_api_tree:
                api_tree[api_key] = "Parameter"
    child_object_type = getattr(cls, "child_object_type", None)
    if child_object_type:
        data["child_object_type"] = _populate_data(child_object_type, api_tree, version)
        data["child_object_type"]["doc"] = f"'child_object_type' of {cls.__name__}."
    else:
        data["child_object_type"] = None
    return data


def _gethash(obj_info):
    dhash = hashlib.sha256()
    dhash.update(pickle.dumps(obj_info))
    return dhash.hexdigest()


# Store the top level class names and their data hash.
# This is used to avoid name collisions and data duplication.
_NAME_BY_HASH = {}

# Keeps tracks of which classes have been written to the file.
# See the implementation note in _write_data() for more details.
_CLASS_WRITTEN = set()


def _get_unique_name(name):
    names = _NAME_BY_HASH.values()
    if name not in names and name not in keyword.kwlist:
        return name
    i = 1
    while f"{name}_{i}" in names:
        i += 1
    name = f"{name}_{i}"
    return name


_arg_type_strings = {
    "Boolean": "bool",
    "Integer": "int",
    "Real": "float | str",
    "String": "str",
    "Filename": "str",
    "BooleanList": "list[bool]",
    "IntegerList": "list[int]",
    "RealVector": "tuple[float | str, float | str, float | str]",
    "RealList": "list[float | str]",
    "StringList": "list[str]",
    "FilenameList": "list[str]",
}


def _write_function_stub(name, data, s_stub):
    s_stub.write(f"    def {name}(self")
    for arg_name in data["argument_names"]:
        arg_type = data["child_classes"][arg_name]["bases"][0]
        py_arg_type = _arg_type_strings.get(arg_type, "Any")
        s_stub.write(f", {arg_name}: {py_arg_type}")
    s_stub.write("):\n")
    # TODO: add return type
    doc = data["doc"]
    doc = doc.strip().replace("\n", "\n        ")
    s_stub.write('        """\n')
    s_stub.write(f"        {doc}\n")
    s_stub.write('        """\n')


def _write_data(cls_name: str, python_name: str, data: dict, f: IO, f_stub: IO | None):
    # We are traversing the class tree from root to leaves. But the class definitions must
    # be written to the file from leaves to root. We gather the parent definition within
    # in a string buffer which is written after writing the child class definitions.
    s = StringIO()
    s_stub = StringIO()
    child_object_name = f"{cls_name}_child" if data["child_object_type"] else None
    bases = _construct_bases(data["bases"], child_object_name)
    bases = ", ".join(bases)
    bases_stub = _construct_bases_stub(data["bases"], child_object_name)
    bases_stub = ", ".join(bases_stub)
    s.write(f"class {cls_name}({bases}):\n")
    s_stub.write(f"class {cls_name}({bases_stub}):\n")
    doc = data["doc"]
    doc = doc.strip().replace("\n", "\n    ")
    s.write('    """\n')
    s.write(f"    {doc}\n")
    s.write('    """\n')
    s.write(f"    _version = {data['version']!r}\n")
    s.write(f"    fluent_name = {data['fluent_name']!r}\n")
    # _python_name preserves the original non-suffixed name of the class.
    s.write(f"    _python_name = {python_name!r}\n")
    s_stub.write("    _version: str\n")
    s_stub.write("    fluent_name: str\n")
    s_stub.write("    _python_name: str\n")
    child_names = data["child_names"]
    if child_names:
        s.write(f"    child_names = {child_names}\n")
        s_stub.write("    child_names: list[str]\n")
    command_names = data["command_names"]
    if command_names:
        s.write(f"    command_names = {command_names}\n")
        s_stub.write("    command_names: list[str]\n")
    query_names = data["query_names"]
    if query_names:
        s.write(f"    query_names = {query_names}\n")
        s_stub.write("    query_names: list[str]\n")
    argument_names = data["argument_names"]
    if argument_names:
        s.write(f"    argument_names = {argument_names}\n")
        s_stub.write("    argument_names: list[str]\n")
    classes_to_write = {}  # values are (class_name, data, hash, should_write_stub)
    if data["child_classes"]:
        s.write("    _child_classes = dict(\n")
        for k, v in data["child_classes"].items():
            name = v["name"]
            # Retrieving the original python name before get_cls() modifies it.
            child_python_name = to_python_name(v["fluent_name"])
            hash_ = _gethash(v)
            # We are within a tree-traversal, so the global _NAME_BY_HASH dict
            # must be updated immediately at the point of lookup. Same lookup
            # can happen at a child-level which will be evaluated incorrectly
            # without the previous lookup result.
            unique_name = _NAME_BY_HASH.get(hash_)
            if not unique_name:
                unique_name = _get_unique_name(name)
                _NAME_BY_HASH[hash_] = unique_name
            s.write(f"        {k}={unique_name},\n")
            # We include the child-class to write irrespective of the above
            # _NAME_BY_HASH lookup result and later use the global _CLASS_WRITTEN
            # set to avoid duplicate writes. This is necessary because class
            # definition must be written to the file before writing its usage.
            # If we didn't have this constraint, we could include the child-class
            # to write only if it is not found in the _NAME_BY_HASH dict and avoid
            # the _CLASS_WRITTEN set.
            if k in command_names + query_names:
                _write_function_stub(k, v, s_stub)
                classes_to_write[unique_name] = (child_python_name, v, hash_, False)
            else:
                s_stub.write(f"    {k}: {unique_name}\n")
                classes_to_write[unique_name] = (child_python_name, v, hash_, True)
        s.write("    )\n")
    if child_object_name:
        child_object_type = data["child_object_type"]
        s.write(f"    child_object_type = {child_object_name}\n")
        classes_to_write[child_object_name] = (
            f"{python_name}_child",
            child_object_type,
            _gethash(child_object_type),
            True,
        )
        s_stub.write(f"    child_object_type: {child_object_name}\n")
    child_aliases = data["child_aliases"]
    if child_aliases:
        s.write("    _child_aliases = dict(\n")
        for k, v in child_aliases.items():
            s.write(f"        {k}={v!r},\n")
        s.write("    )\n")
        s_stub.write("    _child_aliases: dict\n")
    return_type = data["return_type"]
    if return_type:
        s.write(f"    return_type = {return_type!r}\n")
        s_stub.write("    return_type: str\n")
    s.write("\n")
    for name, (python_name, data, hash_, should_write_stub) in classes_to_write.items():
        if name not in _CLASS_WRITTEN:
            _write_data(
                name, python_name, data, f, f_stub if should_write_stub else None
            )
            _CLASS_WRITTEN.add(name)
    f.write(s.getvalue())
    if f_stub:
        f_stub.write(s_stub.getvalue())


def _check_written_docstrings(version, output_file, verbose):
    settings = pyfluent.utils.load_module(
        f"settings_{version}",
        output_file,
    )
    analysis = _docstrings._DocStringAnalysis()
    walk_api.walk_api(getattr(settings, "root"), analysis.analyse, "")
    dubious = analysis.dubious
    if dubious:
        print(
            f"Some docstrings appear to be dubious in the solver settings generated classes: {dubious}."
        )
    elif verbose:
        print(
            "The solver settings generated classes contain no reported docstring issues."
        )


def generate(version: str, static_infos: dict, verbose: bool = False) -> None:
    """Generate the classes corresponding to the Fluent settings API."""
    start_time = time.time()
    api_tree = {}
    sinfo = static_infos.get(StaticInfoType.SETTINGS)
    shash = _gethash(sinfo)
    if not sinfo:
        return {"<solver_session>": api_tree}
    output_dir = (pyfluent.CODEGEN_OUTDIR / "solver").resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"settings_{version}.py"
    output_stub_file = output_dir / f"settings_{version}.pyi"
    cls, _ = get_cls("", sinfo, version=version)
    # _populate_data() collects all strings to write to the file in a nested dict.
    # which is then written to the file using _write_data().
    data = _populate_data(cls, api_tree, version)
    _NAME_BY_HASH.clear()
    _CLASS_WRITTEN.clear()
    if verbose:
        print(f"{str(output_file)}")
        print(f"{str(output_stub_file)}")
    with open(output_file, "w") as f, open(output_stub_file, "w") as f_stub:
        header = StringIO()
        header.write("#\n")
        header.write("# This is an auto-generated file.  DO NOT EDIT!\n")
        header.write("#\n")
        header.write("\n")
        header.write("from ansys.fluent.core.solver.flobject import *\n\n")
        header.write("from ansys.fluent.core.solver.flobject import (\n")
        header.write("    _ChildNamedObjectAccessorMixin,\n")
        header.write("    _NonCreatableNamedObjectMixin,\n")
        header.write("    _InputFile,\n")
        header.write("    _OutputFile,\n")
        header.write("    _InOutFile,\n")
        header.write(")\n\n")
        f.write(header.getvalue())
        f_stub.write(header.getvalue())
        f_stub.write("from typing import Any\n\n")
        f.write(f'SHASH = "{shash}"\n\n')
        name = data["name"]
        _NAME_BY_HASH[_gethash(data)] = name
        _write_data(name, name, data, f, f_stub)
    file_size = output_file.stat().st_size / 1024 / 1024
    file_size_stub = output_stub_file.stat().st_size / 1024 / 1024
    print(
        f"\nGenerated {output_file.name} and {output_stub_file.name} in {time.time() - start_time:.2f} seconds."
    )
    print(f"{output_file.name} size: {file_size:.2f} MB")
    print(f"{output_stub_file.name} size: {file_size_stub:.2f} MB")
    _check_written_docstrings(version, output_file, verbose)
    return {"<solver_session>": api_tree}


if __name__ == "__main__":
    solver = launch_fluent()
    version = get_version_for_file_name(session=solver)
    static_info = solver._settings_service.get_static_info()
    # version = "251"
    # static_info = pickle.load(open("static_info.pkl", "rb"))
    static_infos = {StaticInfoType.SETTINGS: static_info}
    parser = argparse.ArgumentParser(
        description="A script to write Fluent API files with an optional verbose output."
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show paths of written Fluent API files.",
    )
    args = parser.parse_args()
    generate(version, static_infos, args.verbose)
