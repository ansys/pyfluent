"""Provide a module to generate the Fluent settings tree.

Running this module generates a python module with the definition of the Fluent
settings classes. The out is placed at:

- src/ansys/fluent/core/solver/settings.py

Running this module requires Fluent to be installed.

Process
-------
    - Launch fluent and get static info. Parse the class with flobject.get_cls()
    - Generate a dictionary of unique classes with their hash as a key and a tuple of cls, children hash, commands hash, arguments hash, child object type hash as value.
    - - This eliminates reduandancy and only unique classes are written.
    - Generate .py files for the classes in hash dictionary. Resolve named conflicts with integer suffix.
    - - Populate files dictionary with hash as key and file name as value.
    - - child_object_type handled specially to avoid a lot of files with same name and to provide more insight of the child.
    - Populate the classes.
    - - For writing the import statements, get the hash of the child/command/argument/named object stored in the hash dict tuple value.
    - - Use that hash to locate the corresponding children file name in the hash dict.

Usage
-----
python <path to settingsgen.py>
"""

import hashlib
import io
import os
from pathlib import Path
import pickle
import pprint
import shutil

import ansys.fluent.core as pyfluent
from ansys.fluent.core import launch_fluent
from ansys.fluent.core.codegen import StaticInfoType
from ansys.fluent.core.solver import flobject
from ansys.fluent.core.utils.fix_doc import fix_settings_doc
from ansys.fluent.core.utils.fluent_version import get_version_for_file_name

hash_dict = {}
files_dict = {}
root_class_path = ""


def _gethash(obj_info):
    dhash = hashlib.sha256()
    dhash.update(pickle.dumps(obj_info))
    return dhash.hexdigest()


def _get_indent_str(indent):
    return f"{' '*indent*4}"


def _populate_hash_dict(name, info, cls, api_tree):
    children = info.get("children")
    if children:
        children_hash = []
        for cname, cinfo in children.items():
            for child in getattr(cls, "child_names", None):
                child_cls = cls._child_classes[child]
                if cname == child_cls.fluent_name:
                    api_tree[child] = {}
                    children_hash.append(
                        _populate_hash_dict(cname, cinfo, child_cls, api_tree[child])
                    )
                    okey = f"{child}:<name>"
                    if okey in api_tree[child]:
                        api_tree[child].update(api_tree[child][okey])
                        del api_tree[child][okey]
                        api_tree[okey] = api_tree.pop(child)
                    else:
                        api_tree[child] = api_tree[child] or "Parameter"
                    break
    else:
        children_hash = None

    commands = info.get("commands")
    if commands:
        commands_hash = []
        for cname, cinfo in commands.items():
            for command in getattr(cls, "command_names", None):
                command_cls = cls._child_classes[command]
                if cname == command_cls.fluent_name:
                    api_tree[command] = "Command"
                    commands_hash.append(
                        _populate_hash_dict(cname, cinfo, command_cls, {})
                    )
                    break
    else:
        commands_hash = None

    queries = info.get("queries")
    if queries:
        queries_hash = []
        for qname, qinfo in queries.items():
            for query in getattr(cls, "query_names", None):
                query_cls = cls._child_classes[query]
                if qname == query_cls.fluent_name:
                    api_tree[query] = "Query"
                    queries_hash.append(
                        _populate_hash_dict(qname, qinfo, query_cls, {})
                    )
                    break
    else:
        queries_hash = None

    arguments = info.get("arguments")
    if arguments:
        arguments_hash = []
        for aname, ainfo in arguments.items():
            for argument in getattr(cls, "argument_names", None):
                argument_cls = cls._child_classes[argument]
                if aname == argument_cls.fluent_name:
                    arguments_hash.append(
                        _populate_hash_dict(aname, ainfo, argument_cls, {})
                    )
                    break
    else:
        arguments_hash = None

    object_type = info.get("object-type")
    if object_type:
        key = f"{cls.__name__}:<name>"
        api_tree[key] = {}
        object_hash = _populate_hash_dict(
            "child-object-type",
            object_type,
            getattr(cls, "child_object_type", None),
            api_tree[key],
        )
    else:
        object_hash = None

    cls_tuple = (
        name,
        cls.__name__,
        cls.__bases__,
        info["type"],
        info.get("help"),
        children_hash,
        commands_hash,
        queries_hash,
        arguments_hash,
        object_hash,
    )
    hash = _gethash(cls_tuple)
    if not hash_dict.get(hash):
        hash_dict[hash] = (
            cls,
            children_hash,
            commands_hash,
            queries_hash,
            arguments_hash,
            object_hash,
        )
    return hash


class _CommandInfo:
    def __init__(self, doc, args_info):
        self.doc = doc
        self.args_info = args_info


_arg_type_strings = {
    flobject.Boolean: "bool",
    flobject.Integer: "int",
    flobject.Real: "float | str",
    flobject.String: "str",
    flobject.Filename: "str",
    flobject.BooleanList: "List[bool]",
    flobject.IntegerList: "List[int]",
    flobject.RealVector: "Tuple[float | str, float | str, float | str",
    flobject.RealList: "List[float | str]",
    flobject.StringList: "List[str]",
    flobject.FilenameList: "List[str]",
}


def _get_commands_info(commands_hash):
    commands_info = {}
    for command_hash in commands_hash:
        command_hash_info = hash_dict.get(command_hash)
        command_cls = command_hash_info[0]
        command_name = command_cls.__name__
        command_info = _CommandInfo(command_cls.__doc__, [])
        if command_hash_info[4]:
            for arg_hash in command_hash_info[4]:
                arg_hash_info = hash_dict.get(arg_hash)
                arg_cls = arg_hash_info[0]
                arg_name = arg_cls.__name__
                arg_type = _arg_type_strings[arg_cls.__bases__[0]]
                command_info.args_info.append(f"{arg_name}: {arg_type}")
        commands_info[command_name] = command_info
    return commands_info


def _write_doc_string(doc, indent, writer):
    doc = ("\n" + indent).join(doc.split("\n"))
    writer.write(f'{indent}"""\n')
    writer.write(f"{indent}{doc}")
    writer.write(f'\n{indent}"""\n\n')


def _populate_classes(parent_dir):
    istr = _get_indent_str(0)
    istr1 = _get_indent_str(1)
    istr2 = _get_indent_str(2)
    files = []
    # generate files
    for key, (
        cls,
        children_hash,
        commands_hash,
        queries_hash,
        arguments_hash,
        object_hash,
    ) in hash_dict.items():
        cls_name = file_name = cls.__name__
        if cls_name == "child_object_type":
            # Get the first parent for this class.
            for (
                cls1,
                children_hash1,
                commands_hash1,
                queries_hash1,
                arguments_hash1,
                object_hash1,
            ) in hash_dict.values():
                if key == object_hash1:
                    cls.__name__ = file_name = cls1.__name__ + "_child"
                    break
        i = 0
        while file_name in files:
            if i > 0:
                file_name = file_name[: file_name.rfind("_")]
            i += 1
            file_name += "_" + str(i)
        files.append(file_name)
        files_dict[key] = file_name

        # Store root class path for __init__.py
        if cls_name == "root":
            global root_class_path
            root_class_path = file_name

        file_name += ".py"
        file_name = os.path.normpath(os.path.join(parent_dir, file_name))
        with open(file_name, "w") as f:
            f.write(f"name: {cls_name}")

    # populate files
    for key, (
        cls,
        children_hash,
        commands_hash,
        queries_hash,
        arguments_hash,
        object_hash,
    ) in hash_dict.items():
        file_name = files_dict.get(key)
        cls_name = cls.__name__
        file_name = os.path.normpath(os.path.join(parent_dir, file_name + ".py"))
        stub_f = None
        if not pyfluent.CODEGEN_ZIP_SETTINGS:
            stub_file_name = file_name + "i"
            stub_f = open(stub_file_name, "w")
        with open(file_name, "w") as f:
            # disclaimer to py file
            f.write("#\n")
            f.write("# This is an auto-generated file.  DO NOT EDIT!\n")
            f.write("#\n")
            f.write("\n")
            if stub_f:
                stub_f.write("#\n")
                stub_f.write("# This is an auto-generated file.  DO NOT EDIT!\n")
                stub_f.write("#\n")
                stub_f.write("\n\n")

            # write imports to py file
            import_str = (
                "from ansys.fluent.core.solver.flobject import *\n\n"
                "from ansys.fluent.core.solver.flobject import (\n"
                f"{istr1}_ChildNamedObjectAccessorMixin,\n"
                f"{istr1}CreatableNamedObjectMixin,\n"
                f"{istr1}_NonCreatableNamedObjectMixin,\n"
                f"{istr1}AllowedValuesMixin,\n"
                f"{istr1}_InputFile,\n"
                f"{istr1}_OutputFile,\n"
                f"{istr1}_InOutFile,\n"
                ")\n\n"
            )
            f.write(import_str)
            if stub_f:
                stub_f.write(import_str)
                stub_f.write("from typing import Union, List, Tuple\n\n")

            if children_hash:
                for child in children_hash:
                    pchild_name = hash_dict.get(child)[0].__name__
                    import_str = f"from .{files_dict.get(child)} import {pchild_name} as {pchild_name}_cls\n"
                    f.write(import_str)
                    if stub_f:
                        stub_f.write(import_str)

            if commands_hash:
                for child in commands_hash:
                    pchild_name = hash_dict.get(child)[0].__name__
                    import_str = f"from .{files_dict.get(child)} import {pchild_name} as {pchild_name}_cls\n"
                    f.write(import_str)
                    if stub_f:
                        stub_f.write(import_str)

            if queries_hash:
                for child in queries_hash:
                    pchild_name = hash_dict.get(child)[0].__name__
                    import_str = f"from .{files_dict.get(child)} import {pchild_name} as {pchild_name}_cls\n"
                    f.write(import_str)
                    if stub_f:
                        stub_f.write(import_str)

            if arguments_hash:
                for child in arguments_hash:
                    pchild_name = hash_dict.get(child)[0].__name__
                    import_str = f"from .{files_dict.get(child)} import {pchild_name} as {pchild_name}_cls\n"
                    f.write(import_str)
                    if stub_f:
                        stub_f.write(import_str)

            if object_hash:
                pchild_name = hash_dict.get(object_hash)[0].__name__
                import_str = (
                    f"from .{files_dict.get(object_hash)} import {pchild_name}\n\n"
                )
                f.write(import_str)
                if stub_f:
                    stub_f.write(import_str)

            # class name
            class_def_str = (
                f"\n{istr}class {cls_name}"
                f'({", ".join(f"{c.__name__}[{hash_dict.get(object_hash)[0].__name__}]" if object_hash else c.__name__ for c in cls.__bases__)}):\n'
            )
            f.write(class_def_str)
            if stub_f:
                stub_f.write(class_def_str)

            doc = fix_settings_doc(cls.__doc__)
            # Custom doc for child object type
            if cls.fluent_name == "child-object-type":
                parent_name = Path(file_name).stem[
                    0 : Path(file_name).stem.find("_child")
                ]
                doc = f"'child_object_type' of {parent_name}."

            _write_doc_string(doc, istr1, f)
            f.write(f'{istr1}fluent_name = "{cls.fluent_name}"\n\n')
            if stub_f:
                stub_f.write(f"{istr1}fluent_name = ...\n")

            child_class_strings = []

            # write children objects
            child_names = getattr(cls, "child_names", None)
            if child_names:
                f.write(f"{istr1}child_names = \\\n")
                strout = io.StringIO()
                pprint.pprint(child_names, stream=strout, compact=True, width=70)
                mn = ("\n" + istr2).join(strout.getvalue().strip().split("\n"))
                f.write(f"{istr2}{mn}\n\n")
                if stub_f:
                    stub_f.write(f"{istr1}child_names = ...\n")

                for child in child_names:
                    child_cls = cls._child_classes[child]
                    child_class_strings.append(f"{child}={child_cls.__name__}_cls")
                    if stub_f:
                        stub_f.write(
                            f"{istr1}{child}: {child_cls.__name__}_cls = ...\n"
                        )

            # write command objects
            command_names = getattr(cls, "command_names", None)
            if command_names:
                f.write(f"{istr1}command_names = \\\n")
                strout = io.StringIO()
                pprint.pprint(command_names, stream=strout, compact=True, width=70)
                mn = ("\n" + istr2).join(strout.getvalue().strip().split("\n"))
                f.write(f"{istr2}{mn}\n\n")
                if stub_f:
                    stub_f.write(f"{istr1}command_names = ...\n\n")

                commands_info = _get_commands_info(commands_hash)
                for command in command_names:
                    command_cls = cls._child_classes[command]
                    child_class_strings.append(f"{command}={command_cls.__name__}_cls")
                    # function annotation for commands
                    command_info = commands_info[command]
                    if stub_f:
                        stub_f.write(f"{istr1}def {command}(self, ")
                        stub_f.write(", ".join(command_info.args_info))
                        stub_f.write("):\n")
                        _write_doc_string(command_info.doc, istr2, stub_f)

            # write query objects
            query_names = getattr(cls, "query_names", None)
            if query_names:
                f.write(f"{istr1}query_names = \\\n")
                strout = io.StringIO()
                pprint.pprint(query_names, stream=strout, compact=True, width=70)
                mn = ("\n" + istr2).join(strout.getvalue().strip().split("\n"))
                f.write(f"{istr2}{mn}\n\n")
                if stub_f:
                    stub_f.write(f"{istr1}query_names = ...\n\n")

                queries_info = _get_commands_info(queries_hash)
                for query in query_names:
                    query_cls = cls._child_classes[query]
                    child_class_strings.append(f"{query}={query_cls.__name__}_cls")
                    # function annotation for queries
                    query_info = queries_info[query]
                    if stub_f:
                        stub_f.write(f"{istr1}def {query}(self, ")
                        stub_f.write(", ".join(query_info.args_info))
                        stub_f.write("):\n")
                        _write_doc_string(query_info.doc, istr2, stub_f)

            # write arguments
            arguments = getattr(cls, "argument_names", None)
            if arguments:
                f.write(f"{istr1}argument_names = \\\n")
                strout = io.StringIO()
                pprint.pprint(arguments, stream=strout, compact=True, width=70)
                mn = ("\n" + istr2).join(strout.getvalue().strip().split("\n"))
                f.write(f"{istr2}{mn}\n\n")
                if stub_f:
                    stub_f.write(f"{istr1}argument_names = ...\n")

                for argument in arguments:
                    argument_cls = cls._child_classes[argument]
                    child_class_strings.append(
                        f"{argument}={argument_cls.__name__}_cls"
                    )
                    if stub_f:
                        stub_f.write(
                            f"{istr1}{argument}: {argument_cls.__name__}_cls = ...\n"
                        )

            if child_class_strings:
                f.write(f"{istr1}_child_classes = dict(\n")
                f.writelines(
                    [f"{istr2}{cls_str},\n" for cls_str in child_class_strings]
                )
                f.write(f"{istr1})\n\n")

            child_aliases = getattr(cls, "_child_aliases", None)
            if child_aliases:
                f.write(f"{istr1}_child_aliases = dict(\n")
                f.writelines([f'{istr2}{k}="{v}",\n' for k, v in child_aliases.items()])
                f.write(f"{istr1})\n\n")

            # write object type
            child_object_type = getattr(cls, "child_object_type", None)
            if child_object_type:
                f.write(f"{istr1}child_object_type: {pchild_name} = {pchild_name}\n")
                f.write(f'{istr1}"""\n')
                f.write(f"{istr1}child_object_type of {cls_name}.")
                f.write(f'\n{istr1}"""\n')
                if stub_f:
                    stub_f.write(f"{istr1}child_object_type: {pchild_name} = ...\n")

            return_type = getattr(cls, "return_type", None)
            if return_type:
                f.write(f'{istr1}return_type = "{return_type}"\n')
                if stub_f:
                    stub_f.write(f"{istr1}return_type = ...\n")
            if stub_f:
                stub_f.close()


def _populate_init(parent_dir, hash):
    file_name = os.path.normpath(os.path.join(parent_dir, "__init__.py"))
    with open(file_name, "w") as f:
        f.write("#\n")
        f.write("# This is an auto-generated file.  DO NOT EDIT!\n")
        f.write("#\n")
        f.write("\n")
        f.write(f'"""A package providing Fluent\'s Settings Objects in Python."""')
        f.write("\n")
        f.write("from ansys.fluent.core.solver.flobject import *\n\n")
        f.write(f'SHASH = "{hash}"\n')
        f.write(f"from .{root_class_path} import root")


def generate(version, static_infos: dict):
    """Generate settings API classes."""
    parent_dir = (pyfluent.CODEGEN_OUTDIR / "solver" / f"settings_{version}").resolve()
    api_tree = {}
    sinfo = static_infos.get(StaticInfoType.SETTINGS)

    # Clear previously generated data
    if os.path.exists(parent_dir):
        shutil.rmtree(parent_dir)

    if sinfo:
        hash = _gethash(sinfo)
        os.makedirs(parent_dir)

        if pyfluent.CODEGEN_ZIP_SETTINGS:
            parent_dir = parent_dir / "settings"
            os.makedirs(parent_dir)

        cls, _ = flobject.get_cls("", sinfo, version=version)

        _populate_hash_dict("", sinfo, cls, api_tree)
        _populate_classes(parent_dir)
        _populate_init(parent_dir, hash)

        if pyfluent.CODEGEN_ZIP_SETTINGS:
            shutil.make_archive(parent_dir.parent, "zip", parent_dir.parent)
            shutil.rmtree(parent_dir.parent)

    return {"<solver_session>": api_tree}


if __name__ == "__main__":
    solver = launch_fluent()
    version = get_version_for_file_name(session=solver)
    static_infos = {StaticInfoType.SETTINGS: solver._settings_service.get_static_info()}
    generate(version, static_infos)
