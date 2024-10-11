"""Module to generate the classes corresponding to the Fluent settings API."""

import hashlib
from io import StringIO
import keyword
import pickle
import time

import ansys.fluent.core as pyfluent
from ansys.fluent.core import launch_fluent
from ansys.fluent.core.codegen import StaticInfoType
from ansys.fluent.core.solver.flobject import Command, NamedObject, Query, get_cls
from ansys.fluent.core.utils.fluent_version import get_version_for_file_name


def _populate_data(cls, api_tree):
    data = {}
    data["name"] = cls.__name__
    data["bases"] = cls.__bases__
    data["doc"] = cls.__doc__
    data["fluent_name"] = getattr(cls, "fluent_name")
    data["child_names"] = getattr(cls, "child_names", [])
    data["command_names"] = getattr(cls, "command_names", [])
    data["query_names"] = getattr(cls, "query_names", [])
    data["argument_names"] = getattr(cls, "argument_names", [])
    data["child_aliases"] = getattr(cls, "_child_aliases", {})
    data["return_type"] = getattr(cls, "return_type", None)
    child_classes = data.setdefault("child_classes", {})
    for k, v in cls._child_classes.items():
        if issubclass(v, Command):
            api_tree[k] = "Command"
            child_classes[k] = _populate_data(v, {})
        elif issubclass(v, Query):
            api_tree[k] = "Query"
            child_classes[k] = _populate_data(v, {})
        else:
            api_key = f"{k}:<name>" if issubclass(v, NamedObject) else k
            child_api_tree = api_tree.setdefault(api_key, {})
            child_classes[k] = _populate_data(v, child_api_tree)
            if not child_api_tree:
                api_tree[k] = "Parameter"
    child_object_type = getattr(cls, "child_object_type", None)
    if child_object_type:
        data["child_object_type"] = _populate_data(child_object_type, api_tree)
    else:
        data["child_object_type"] = None
    return data


def _gethash(obj_info):
    dhash = hashlib.sha256()
    dhash.update(pickle.dumps(obj_info))
    return dhash.hexdigest()


# Takes care of data duplication and name collisions
_NAME_BY_HASH = {}


def _get_unique_name(name):
    names = _NAME_BY_HASH.values()
    if name not in names and name not in keyword.kwlist:
        return name
    i = 1
    while f"{name}_{i}" in names:
        i += 1
    name = f"{name}_{i}"
    return name


def _write_data(cls_name, python_name, data, f, f_stub, version):
    bases = ", ".join([base.__name__ for base in data["bases"]])
    s = StringIO()
    s_stub = StringIO()
    cls_def = f"class {cls_name}({bases}):\n"
    s.write(cls_def)
    s_stub.write(cls_def)
    doc = data["doc"]
    doc = doc.replace("\n", "\n    ")
    s.write('    """\n')
    s.write(f"    {doc}\n")
    s.write('    """\n')
    s.write(f"    version = {version!r}\n")
    s.write(f"    fluent_name = {data['fluent_name']!r}\n")
    s.write(f"    _python_name = {python_name!r}\n")
    s_stub.write(f"    version: str\n")
    s_stub.write(f"    fluent_name: str\n")
    s_stub.write(f"    _python_name: str\n")
    child_names = data["child_names"]
    if child_names:
        s.write(f"    child_names = {child_names}\n")
        s_stub.write(f"    child_names: List[str]\n")
    command_names = data["command_names"]
    if command_names:
        s.write(f"    command_names = {command_names}\n")
        s_stub.write(f"    command_names: List[str]\n")
    query_names = data["query_names"]
    if query_names:
        s.write(f"    query_names = {query_names}\n")
        s_stub.write(f"    query_names: List[str]\n")
    argument_names = data["argument_names"]
    if argument_names:
        s.write(f"    argument_names = {argument_names}\n")
        s_stub.write(f"    argument_names: List[str]\n")
    classes_to_write = {}
    if data["child_classes"]:
        s.write("    _child_classes = dict(\n")
        for k, v in data["child_classes"].items():
            name = v["name"]
            hash_ = _gethash(v)
            unique_name = _NAME_BY_HASH.get(hash_)
            if unique_name:
                s.write(f"        {k}={unique_name},\n")
                s_stub.write(f"    {k}: {unique_name}\n")
            else:
                unique_name = _get_unique_name(name)
                s.write(f"        {k}={unique_name},\n")
                s_stub.write(f"    {k}: {unique_name}\n")
                classes_to_write[unique_name] = (name, v, hash_)
        s.write("    )\n")
    child_object_type = data["child_object_type"]
    if child_object_type:
        name = f"{cls_name}_child"
        s.write(f"    child_object_type = {name}\n")
        classes_to_write[name] = (
            f"{python_name}_child",
            child_object_type,
            _gethash(child_object_type),
        )
        s_stub.write(f"    child_object_type: {name}\n")
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
        s_stub.write(f"    return_type: str\n")
    s.write("\n")
    for name, (python_name, data, hash_) in classes_to_write.items():
        _NAME_BY_HASH[hash_] = name
        _write_data(name, python_name, data, f, f_stub, version)
    f.write(s.getvalue())
    f_stub.write(s_stub.getvalue())


def generate(version: str, static_infos: dict) -> None:
    """Generate the classes corresponding to the Fluent settings API."""
    start_time = time.time()
    api_tree = {}
    sinfo = static_infos.get(StaticInfoType.SETTINGS)
    if not sinfo:
        return {"<solver_session>": api_tree}
    output_file = (
        pyfluent.CODEGEN_OUTDIR / "solver" / f"settings_{version}.py"
    ).resolve()
    output_stub_file = output_file.parent / f"{output_file.stem}.pyi"
    cls, _ = get_cls("", sinfo, version=version)
    data = _populate_data(cls, api_tree)
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
        f.write(f'SHASH = "{_gethash(sinfo)}"\n\n')
        f_stub.write("from typing import Union, List, Tuple\n\n")
        name = data["name"]
        _NAME_BY_HASH[_gethash(data)] = name
        _write_data(name, name, data, f, f_stub, version)
    file_size = output_file.stat().st_size / 1024 / 1024
    file_size_stub = output_stub_file.stat().st_size / 1024 / 1024
    print(
        f"Generated {output_file.name} and {output_stub_file.name} in {time.time() - start_time:.2f} seconds."
    )
    print(f"{output_file.name} size: {file_size:.2f} MB")
    print(f"{output_stub_file.name} size: {file_size_stub:.2f} MB")
    return {"<solver_session>": api_tree}


if __name__ == "__main__":
    solver = launch_fluent()
    version = get_version_for_file_name(session=solver)
    static_info = solver._settings_service.get_static_info()
    # version = "251"
    # static_info = pickle.load(open("static_info.pkl", "rb"))
    static_infos = {StaticInfoType.SETTINGS: static_info}
    generate(version, static_infos)
