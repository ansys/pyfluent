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
    - - Populate files dictionary with hash as key and filename as value.
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
import pickle
import pprint
import shutil

from ansys.fluent.core.solver import flobject
from ansys.fluent.core.utils.fix_doc import fix_settings_doc
from ansys.fluent.core.utils.fluent_version import get_version_for_filepath

hash_dict = {}
files_dict = {}
root_class_path = ""


def _gethash(obj_info):
    dhash = hashlib.sha256()
    dhash.update(pickle.dumps(obj_info))
    return dhash.hexdigest()


def _get_indent_str(indent):
    return f"{' '*indent*4}"


def _populate_hash_dict(name, info, cls):
    children = info.get("children")
    if children:
        children_hash = []
        for cname, cinfo in children.items():
            for child in getattr(cls, "child_names", None):
                child_cls = getattr(cls, child)
                if cname == child_cls.fluent_name:
                    children_hash.append(_populate_hash_dict(cname, cinfo, child_cls))
                    break
    else:
        children_hash = None

    commands = info.get("commands")
    if commands:
        commands_hash = []
        for cname, cinfo in commands.items():
            for command in getattr(cls, "command_names", None):
                command_cls = getattr(cls, command)
                if cname == command_cls.fluent_name:
                    commands_hash.append(_populate_hash_dict(cname, cinfo, command_cls))
                    break
    else:
        commands_hash = None

    queries = info.get("queries")
    if queries:
        queries_hash = []
        for qname, qinfo in queries.items():
            for query in getattr(cls, "query_names", None):
                query_cls = getattr(cls, query)
                if qname == query_cls.fluent_name:
                    queries_hash.append(_populate_hash_dict(qname, qinfo, query_cls))
                    break
    else:
        queries_hash = None

    arguments = info.get("arguments")
    if arguments:
        arguments_hash = []
        for aname, ainfo in arguments.items():
            for argument in getattr(cls, "argument_names", None):
                argument_cls = getattr(cls, argument)
                if aname == argument_cls.fluent_name:
                    arguments_hash.append(
                        _populate_hash_dict(aname, ainfo, argument_cls)
                    )
                    break
    else:
        arguments_hash = None

    object_type = info.get("object-type")
    if object_type:
        object_hash = _populate_hash_dict(
            "child-object-type",
            object_type,
            getattr(cls, "child_object_type", None),
        )
    else:
        object_hash = None

    cls_touple = (
        name,
        info["type"],
        info.get("help"),
        children_hash,
        commands_hash,
        queries_hash,
        arguments_hash,
        object_hash,
    )
    hash = _gethash(cls_touple)
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
        filepath = os.path.normpath(os.path.join(parent_dir, file_name))
        with open(filepath, "w") as f:
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
        filepath = os.path.normpath(os.path.join(parent_dir, file_name + ".py"))
        with open(filepath, "w") as f:
            # disclaimer to py file
            f.write("#\n")
            f.write("# This is an auto-generated file.  DO NOT EDIT!\n")
            f.write("#\n")
            f.write("\n")

            # write imports to py file
            f.write("from ansys.fluent.core.solver.flobject import *\n\n")
            f.write(
                "from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin\n\n"
            )
            f.write(
                "from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin\n\n"
            )
            f.write(
                "from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin\n\n"
            )
            if children_hash:
                for child in children_hash:
                    pchild_name = hash_dict.get(child)[0].__name__
                    f.write(
                        f"from .{files_dict.get(child)} import {pchild_name} as {pchild_name}_cls\n"
                    )

            if commands_hash:
                for child in commands_hash:
                    pchild_name = hash_dict.get(child)[0].__name__
                    f.write(
                        f"from .{files_dict.get(child)} import {pchild_name} as {pchild_name}_cls\n"
                    )

            if queries_hash:
                for child in queries_hash:
                    pchild_name = hash_dict.get(child)[0].__name__
                    f.write(
                        f"from .{files_dict.get(child)} import {pchild_name} as {pchild_name}_cls\n"
                    )

            if arguments_hash:
                for child in arguments_hash:
                    pchild_name = hash_dict.get(child)[0].__name__
                    f.write(
                        f"from .{files_dict.get(child)} import {pchild_name} as {pchild_name}_cls\n"
                    )

            if object_hash:
                pchild_name = hash_dict.get(object_hash)[0].__name__
                f.write(f"from .{files_dict.get(object_hash)} import {pchild_name}\n\n")

            # class name
            f.write(
                f"{istr}class {cls_name}"
                f'({", ".join(f"{c.__name__}[{hash_dict.get(object_hash)[0].__name__}]" if object_hash else c.__name__ for c in cls.__bases__)}):\n'
            )

            doc = fix_settings_doc(cls.__doc__)
            # Custom doc for child object type
            if cls.fluent_name == "child-object-type":
                doc = f"'child_object_type' of {file_name[: file_name.find('_child')]}."

            doc = ("\n" + istr1).join(doc.split("\n"))
            f.write(f'{istr1}"""\n')
            f.write(f"{istr1}{doc}")
            f.write(f'\n{istr1}"""\n\n')
            f.write(f'{istr1}fluent_name = "{cls.fluent_name}"\n\n')

            # write children objects
            child_names = getattr(cls, "child_names", None)
            if child_names:
                f.write(f"{istr1}child_names = \\\n")
                strout = io.StringIO()
                pprint.pprint(child_names, stream=strout, compact=True, width=70)
                mn = ("\n" + istr2).join(strout.getvalue().strip().split("\n"))
                f.write(f"{istr2}{mn}\n\n")

                for child in child_names:
                    f.write(f"{istr1}{child}: {child}_cls = {child}_cls\n")
                    f.write(f'{istr1}"""\n')
                    f.write(f"{istr1}{child} child of {cls_name}.")
                    f.write(f'\n{istr1}"""\n')

            # write command objects
            command_names = getattr(cls, "command_names", None)
            if command_names:
                f.write(f"{istr1}command_names = \\\n")
                strout = io.StringIO()
                pprint.pprint(command_names, stream=strout, compact=True, width=70)
                mn = ("\n" + istr2).join(strout.getvalue().strip().split("\n"))
                f.write(f"{istr2}{mn}\n\n")

                for command in command_names:
                    f.write(f"{istr1}{command}: {command}_cls = {command}_cls\n")
                    f.write(f'{istr1}"""\n')
                    f.write(f"{istr1}{command} command of {cls_name}.")
                    f.write(f'\n{istr1}"""\n')

            # write query objects
            query_names = getattr(cls, "query_names", None)
            if query_names:
                f.write(f"{istr1}query_names = \\\n")
                strout = io.StringIO()
                pprint.pprint(query_names, stream=strout, compact=True, width=70)
                mn = ("\n" + istr2).join(strout.getvalue().strip().split("\n"))
                f.write(f"{istr2}{mn}\n\n")

                for query in query_names:
                    f.write(f"{istr1}{query}: {query}_cls = {query}_cls\n")
                    f.write(f'{istr1}"""\n')
                    f.write(f"{istr1}{query} query of {cls_name}.")
                    f.write(f'\n{istr1}"""\n')

            # write arguments
            arguments = getattr(cls, "argument_names", None)
            if arguments:
                f.write(f"{istr1}argument_names = \\\n")
                strout = io.StringIO()
                pprint.pprint(arguments, stream=strout, compact=True, width=70)
                mn = ("\n" + istr2).join(strout.getvalue().strip().split("\n"))
                f.write(f"{istr2}{mn}\n\n")

                for argument in arguments:
                    f.write(f"{istr1}{argument}: {argument}_cls = {argument}_cls\n")
                    f.write(f'{istr1}"""\n')
                    f.write(f"{istr1}{argument} argument of {cls_name}.")
                    f.write(f'\n{istr1}"""\n')

            # write object type
            child_object_type = getattr(cls, "child_object_type", None)
            if child_object_type:
                f.write(f"{istr1}child_object_type: {pchild_name} = {pchild_name}\n")
                f.write(f'{istr1}"""\n')
                f.write(f"{istr1}child_object_type of {cls_name}.")
                f.write(f'\n{istr1}"""\n')


def _populate_init(parent_dir, sinfo):
    hash = _gethash(sinfo)
    filepath = os.path.normpath(os.path.join(parent_dir, "__init__.py"))
    with open(filepath, "w") as f:
        f.write("#\n")
        f.write("# This is an auto-generated file.  DO NOT EDIT!\n")
        f.write("#\n")
        f.write("\n")
        f.write(f'"""A package providing Fluent\'s Settings Objects in Python."""')
        f.write("\n")
        f.write("from ansys.fluent.core.solver.flobject import *\n\n")
        f.write(f'SHASH = "{hash}"\n')
        f.write(f"from .{root_class_path} import root")


def generate():
    from ansys.fluent.core.launcher.launcher import launch_fluent

    session = launch_fluent(mode="solver")
    version = get_version_for_filepath(session=session)
    dirname = os.path.dirname(__file__)
    parent_dir = os.path.normpath(
        os.path.join(
            dirname,
            "..",
            "src",
            "ansys",
            "fluent",
            "core",
            "solver",
            f"settings_{version}",
        )
    )

    # Clear previously generated data
    if os.path.exists(parent_dir):
        shutil.rmtree(parent_dir)
    os.makedirs(parent_dir)

    sinfo = session._settings_service.get_static_info()
    session.exit()
    cls = flobject.get_cls("", sinfo, version=version)

    _populate_hash_dict("", sinfo, cls)
    _populate_classes(parent_dir)
    _populate_init(parent_dir, sinfo)


if __name__ == "__main__":
    generate()
