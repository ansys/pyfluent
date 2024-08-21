"""Provide a module to generate the Fluent settings tree.

Running this module generates a python module with the definition of the Fluent
settings classes. The out is placed at:

- src/ansys/fluent/core/generated/solver/settings.py

Running this module requires Fluent to be installed.

Usage
-----
python <path to settingsgen.py>
"""

import hashlib
import io
import os
import pickle
import pprint
from typing import IO

import ansys.fluent.core as pyfluent
from ansys.fluent.core.solver import flobject

dirname = os.path.dirname(__file__)


def _gethash(obj_info):
    dhash = hashlib.sha256()
    dhash.update(pickle.dumps(obj_info))
    return dhash.hexdigest()


def _get_indent_str(indent):
    return f"{' '*indent*4}"


def _check_in_existing_classes(cls, class_list: list):
    if hasattr(cls, "__name__") and cls.__name__ in class_list:
        return True
    elif isinstance(cls, str) and cls in class_list:
        return True
    else:
        return False


written_classes = []


def _write_utils_cls_helper(out, cls, indent=0):
    try:
        istr = _get_indent_str(indent)
        istr1 = _get_indent_str(indent + 1)
        istr2 = _get_indent_str(indent + 2)
        if not _check_in_existing_classes(cls, written_classes):
            out.write("\n")
            if hasattr(cls, "__name__"):
                out.write(
                    f"{istr}class {cls.__name__}"
                    f'({", ".join(c.__name__ for c in cls.__bases__)}):\n'
                )
            else:
                out.write(f'{istr1}return_type = "{cls}"\n')

            doc = ("\n" + istr1).join(cls.__doc__.split("\n"))
            out.write(f'{istr1}"""\n')
            out.write(f"{istr1}{doc}")
            out.write(f'\n{istr1}"""\n')
            if hasattr(cls, "fluent_name"):
                out.write(f'{istr1}fluent_name = "{cls.fluent_name}"\n\n')

            child_names = getattr(cls, "child_names", None)
            if child_names:
                out.write(f"{istr1}child_names = \\\n")
                strout = io.StringIO()
                pprint.pprint(
                    child_names,
                    stream=strout,
                    compact=True,
                    width=80 - indent * 4 - 10,
                )
                mn = ("\n" + istr2).join(strout.getvalue().strip().split("\n"))
                out.write(f"{istr2}{mn}\n")
                for _, child in cls._child_classes.items():
                    _write_utils_cls_helper(out, child)

            command_names = getattr(cls, "command_names", None)
            if command_names:
                out.write(f"{istr1}command_names = \\\n")
                strout = io.StringIO()
                pprint.pprint(
                    command_names,
                    stream=strout,
                    compact=True,
                    width=80 - indent * 4 - 10,
                )
                mn = ("\n" + istr2).join(strout.getvalue().strip().split("\n"))
                out.write(f"{istr2}{mn}\n")
                for _, child in cls._child_classes.items():
                    _write_utils_cls_helper(out, child)

            query_names = getattr(cls, "query_names", None)
            if query_names:
                out.write(f"{istr1}query_names = \\\n")
                strout = io.StringIO()
                pprint.pprint(
                    query_names,
                    stream=strout,
                    compact=True,
                    width=80 - indent * 4 - 10,
                )
                mn = ("\n" + istr2).join(strout.getvalue().strip().split("\n"))
                out.write(f"{istr2}{mn}\n")
                for _, child in cls._child_classes.items():
                    _write_utils_cls_helper(out, child)

            arguments = getattr(cls, "argument_names", None)
            if arguments:
                out.write(f"{istr1}argument_names = \\\n")
                strout = io.StringIO()
                pprint.pprint(
                    arguments,
                    stream=strout,
                    compact=True,
                    width=80 - indent * 4 - 10,
                )
                mn = ("\n" + istr2).join(strout.getvalue().strip().split("\n"))
                out.write(f"{istr2}{mn}\n")
                for _, child in cls._child_classes.items():
                    _write_utils_cls_helper(out, child)

            child_object_type = getattr(cls, "child_object_type", None)
            if child_object_type:
                _write_utils_cls_helper(
                    out,
                    child_object_type,
                )

            child_aliases = getattr(cls, "_child_aliases", None)
            if child_aliases:
                out.write(f"\n{istr1}_child_aliases = dict(\n")
                out.writelines(
                    [f'{istr2}{k}="{v}",\n' for k, v in child_aliases.items()]
                )
                out.write(f"{istr1})\n\n")

            return_type = getattr(cls, "return_type", None)
            if return_type:
                _write_utils_cls_helper(out, return_type)
        if hasattr(cls, "__name__"):
            written_classes.append(cls.__name__)
        else:
            written_classes.append(cls)
    except Exception:
        raise


def write_settings_classes(out: IO, cls, obj_info: dict, settings: bool):
    """Write the settings classes in 'out' stream.

    Parameters
    ----------
    out: Stream
        Out file object.
    cls: class
        Settings top level object.
    obj_info: dict
        Static info.
    settings: bool
        Whether to write settings classes separately.
    """
    hash = _gethash(obj_info)
    if settings:
        out.write("#\n")
        out.write("# This is an auto-generated file.  DO NOT EDIT!\n")
        out.write("#\n")
        out.write("\n")
        out.write(f'SHASH = "{hash}"\n\n')
        for written_class in set(written_classes):
            out.write(
                f"from .settings_utils_{session._version} import {written_class} as {written_class} \n"
            )
        out.write("\n")
        out.write("from ansys.fluent.core.solver.flobject import *\n")
        out.write("\n")
        _write_settings_cls_helper(out=out, cls=cls, indent=0)
    else:
        _write_utils_cls_helper(out=out, cls=cls, indent=0)


def _get_settings_path(version: str):
    return os.path.normpath(
        os.path.join(
            dirname,
            "..",
            "generated",
            "solver",
            f"settings_{version}.py",
        )
    )


def _get_settings_utils_path(version: str):
    return os.path.normpath(
        os.path.join(
            dirname,
            "..",
            "generated",
            "solver",
            f"settings_utils_{version}.py",
        )
    )


root_childs = {
    "file": 0,
    "mesh": 0,
    "server": 0,
    "setup": 0,
    "solution": 0,
    "results": 0,
    "design": 0,
    "parametric_studies": 0,
    "current_parametric_study": 0,
    "parameters": 0,
    "parallel": 0,
    "transient_post_processing": 0,
    "exit": 0,
}


def _write_settings_cls_helper(out, cls, indent=0):
    try:
        if hasattr(cls, "__name__") and cls.__name__ in root_childs:
            root_childs[cls.__name__] += 1
        elif isinstance(cls, str) and cls in root_childs:
            root_childs[cls] += 1
        if (
            hasattr(cls, "__name__")
            and root_childs.get(cls.__name__)
            and root_childs.get(cls.__name__) > 1
        ):
            pass
        elif isinstance(cls, str) and root_childs.get(cls) and root_childs.get(cls) > 1:
            pass
        else:
            istr = _get_indent_str(indent)
            istr1 = _get_indent_str(indent + 1)
            out.write("\n")
            if hasattr(cls, "__name__"):
                out.write(f"{istr}class {cls.__name__}\n")
            else:
                out.write(f'{istr1}return_type = "{cls}"\n')

            child_names = getattr(cls, "child_names", None)
            if child_names:
                for _, child in cls._child_classes.items():
                    _write_settings_cls_helper(out, child, indent + 1)

            command_names = getattr(cls, "command_names", None)
            if command_names:
                for _, child in cls._child_classes.items():
                    _write_settings_cls_helper(out, child, indent + 1)

            query_names = getattr(cls, "query_names", None)
            if query_names:
                for _, child in cls._child_classes.items():
                    _write_settings_cls_helper(out, child, indent + 1)

            arguments = getattr(cls, "argument_names", None)
            if arguments:
                for _, child in cls._child_classes.items():
                    _write_settings_cls_helper(out, child, indent + 1)

            child_object_type = getattr(cls, "child_object_type", None)
            if child_object_type:
                _write_settings_cls_helper(out, child_object_type, indent + 1)

            return_type = getattr(cls, "return_type", None)
            if return_type:
                _write_settings_cls_helper(out, return_type, indent + 1)
    except Exception:
        raise


attrs = {}


def _dynamic_class_generation(cls):
    try:
        attrs[cls.__name__] = {}
        cls_data = attrs[cls.__name__]
    except AttributeError:
        attrs[cls] = {}
        cls_data = attrs[cls]

    bases = tuple([c for c in cls.__bases__])
    cls_data["bases"] = bases

    if hasattr(cls, "__doc__"):
        cls_data["__doc__"] = cls.__doc__

    if hasattr(cls, "fluent_name"):
        cls_data["fluent_name"] = cls.fluent_name

    if hasattr(cls, "_child_aliases"):
        cls_data["_child_aliases"] = cls._child_aliases

    if hasattr(cls, "return_type"):
        cls_data["return_type"] = cls.return_type

    if hasattr(cls, "child_names"):
        cls_data["child_names"] = cls.child_names

    if hasattr(cls, "child_object_type"):
        _dynamic_class_generation(cls.child_object_type)

    if hasattr(cls, "_child_classes"):
        for _, child in cls._child_classes.items():
            _dynamic_class_generation(child)


def _set_all_attrs(cls, attrs):
    try:
        attrs[cls.__name__] = {}
        cls_data = attrs[cls.__name__]
    except AttributeError:
        attrs[cls] = {}
        cls_data = attrs[cls]

    child_names = cls_data.get("child_names")
    if child_names:
        for child_name in child_names:
            cls_data[child_name] = type(
                child_name, attrs[child_name]["bases"], attrs[child_name]
            )
            _set_all_attrs(child)


if __name__ == "__main__":
    import time

    # from ansys.fluent.core.launcher.launcher import launch_fluent

    session = pyfluent.connect_to_fluent(
        ip="10.18.44.94", port=61221, password="l0uz1n73"
    )
    # session = launch_fluent()
    start_time = time.time()
    sinfo = session._settings_service.get_static_info()
    cls = flobject.get_cls("", sinfo, version=session._version)
    dyna_root = cls[0]()
    # with open(
    #     _get_settings_utils_path(version=session._version), "w"
    # ) as settings_utils:
    #     write_settings_classes(settings_utils, cls[0], sinfo, settings=False)

    # with open(_get_settings_path(version=session._version), "w") as settings:
    #     write_settings_classes(settings, cls[0], sinfo, settings=True)
    print(f"settingsgen.py took {time.time() - start_time} seconds.")

    root = _dynamic_class_generation(cls[0])
    set_attrs = attrs
    set_root = _set_all_attrs(cls[0])

    print(f"unique written classes = {len(set(written_classes))}")
    print(f"unique attrs keys = {len(set(list(attrs.keys())))}")
    print(
        f"unique common = {len(set(written_classes).intersection(set(list(attrs.keys()))))}"
    )
