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

written_classes = {}

string_classes = {}


def _write_utils_cls_helper(out, cls, indent=0):
    try:

        if hasattr(cls, "__name__"):
            if cls.__name__ == "lightweight_setup":
                print("lightweight_setup")
        if isinstance(cls, str):
            if cls == "lightweight_setup":
                print(cls)

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
            istr2 = _get_indent_str(indent + 2)

            if hasattr(cls, "__name__"):
                cls_name = cls.__name__

                bases = [c.__name__ for c in cls.__bases__]
                bases_str = ", ".join(bases)
                arguments_str = ""

                if hasattr(cls, "argument_names"):
                    arguments = cls.argument_names
                    arguments_str = ", ".join(arguments)

                if arguments_str:
                    bases_arguments_str = "_".join([bases_str, arguments_str])
                else:
                    bases_arguments_str = ", ".join(bases)

                if cls_name in written_classes:
                    if bases_arguments_str in written_classes[cls_name]:
                        written_classes[cls_name][bases_arguments_str] += 1
                    else:
                        written_classes[cls_name].update({bases_arguments_str: 1})
                else:
                    written_classes[cls_name] = {bases_arguments_str: 1}
            elif isinstance(cls, str):
                cls_name = cls
                if cls_name in string_classes:
                    string_classes[cls_name] += 1
                else:
                    string_classes[cls_name] = 1

            if (
                hasattr(cls, "__name__")
                and written_classes[cls_name][bases_arguments_str] > 1
            ):
                pass
            elif isinstance(cls, str) and string_classes[cls] > 1:
                pass
            else:
                out.write("\n")
                if hasattr(cls, "__name__"):
                    out.write(f"{istr}class {cls.__name__}" f"({bases_str}):\n")
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

        # root_childs = {
        #     "file": 0,
        #     "mesh": 0,
        #     "server": 0,
        #     "setup": 0,
        #     "solution": 0,
        #     "results": 0,
        #     "design": 0,
        #     "parametric_studies": 0,
        #     "current_parametric_study": 0,
        #     "parameters": 0,
        #     "parallel": 0,
        #     "transient_post_processing": 0,
        #     "exit": 0,
        # }

        # written_classes = {}
        # string_classes = {}

        # _write_dynamic_cls_helper(out=out, cls=cls)


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


root_childs_dict = {
    "file": {"count": 0},
    "mesh": {"count": 0},
    "server": {"count": 0},
    "setup": {"count": 0},
    "solution": {"count": 0},
    "results": {"count": 0},
    "design": {"count": 0},
    "parametric_studies": {"count": 0},
    "current_parametric_study": {"count": 0},
    "parameters": {"count": 0},
    "parallel": {"count": 0},
    "transient_post_processing": {"count": 0},
    "exit": {"count": 0},
}


def _write_settings_cls_helper(out, cls, indent=0):
    try:
        if hasattr(cls, "__name__"):
            if cls.__name__ == "lightweight_setup":
                print("lightweight_setup")
        if isinstance(cls, str):
            if cls == "lightweight_setup":
                print(cls)

        if hasattr(cls, "__name__") and cls.__name__ in root_childs_dict:
            root_childs_dict[cls.__name__]["count"] += 1
        elif isinstance(cls, str) and cls in root_childs_dict:
            root_childs_dict[cls]["count"] += 1
        if (
            hasattr(cls, "__name__")
            and cls.__name__ in root_childs_dict
            and root_childs_dict[cls.__name__].get("count")
            and root_childs_dict[cls.__name__].get("count") > 1
        ):
            pass
        elif (
            isinstance(cls, str)
            and cls in root_childs_dict
            and root_childs_dict[cls].get("count")
            and root_childs_dict[cls].get("count") > 1
        ):
            pass
        else:
            if hasattr(cls, "__name__"):
                cls_name = cls.__name__
            elif isinstance(cls, str):
                cls_name = cls

            istr = _get_indent_str(indent)
            istr1 = _get_indent_str(indent + 1)
            out.write("\n")
            if hasattr(cls, "__name__"):
                out.write(f"{istr}class {cls.__name__}\n")
            else:
                out.write(f'{istr1}return_type = "{cls}"\n')

            child_names = getattr(cls, "child_names", None)
            if child_names:
                for child_name, child in cls._child_classes.items():
                    if (
                        cls_name in root_childs_dict
                        and child_name in root_childs_dict[cls_name]
                    ):
                        root_childs_dict[cls_name][child_name] += 1
                    elif cls_name in root_childs_dict:
                        root_childs_dict[cls_name][child_name] = 1
                    if (
                        cls_name in root_childs_dict
                        and root_childs_dict[cls_name][child_name] > 1
                    ):
                        pass
                    else:
                        _write_settings_cls_helper(out, child, indent + 1)

            command_names = getattr(cls, "command_names", None)
            if command_names:
                for child_name, child in cls._child_classes.items():
                    if (
                        cls_name in root_childs_dict
                        and child_name in root_childs_dict[cls_name]
                    ):
                        root_childs_dict[cls_name][child_name] += 1
                    elif cls_name in root_childs_dict:
                        root_childs_dict[cls_name][child_name] = 1
                    if (
                        cls_name in root_childs_dict
                        and root_childs_dict[cls_name][child_name] > 1
                    ):
                        pass
                    else:
                        _write_settings_cls_helper(out, child, indent + 1)

            query_names = getattr(cls, "query_names", None)
            if query_names:
                for child_name, child in cls._child_classes.items():
                    if (
                        cls_name in root_childs_dict
                        and child_name in root_childs_dict[cls_name]
                    ):
                        root_childs_dict[cls_name][child_name] += 1
                    elif cls_name in root_childs_dict:
                        root_childs_dict[cls_name][child_name] = 1
                    if (
                        cls_name in root_childs_dict
                        and root_childs_dict[cls_name][child_name] > 1
                    ):
                        pass
                    else:
                        _write_settings_cls_helper(out, child, indent + 1)

            arguments = getattr(cls, "argument_names", None)
            if arguments:
                for child_name, child in cls._child_classes.items():
                    if (
                        cls_name in root_childs_dict
                        and child_name in root_childs_dict[cls_name]
                    ):
                        root_childs_dict[cls_name][child_name] += 1
                    elif cls_name in root_childs_dict:
                        root_childs_dict[cls_name][child_name] = 1
                    if (
                        cls_name in root_childs_dict
                        and root_childs_dict[cls_name][child_name] > 1
                    ):
                        pass
                    else:
                        _write_settings_cls_helper(out, child, indent + 1)

            child_object_type = getattr(cls, "child_object_type", None)
            if child_object_type:
                _write_settings_cls_helper(out, child_object_type, indent + 1)

            return_type = getattr(cls, "return_type", None)
            if return_type:
                _write_settings_cls_helper(out, return_type, indent + 1)
    except Exception:
        raise


all_classes = {}


def _write_dynamic_cls_helper(out, cls):
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
            if hasattr(cls, "__name__"):
                cls_name = cls.__name__

                bases = [c.__name__ for c in cls.__bases__]
                bases_str = ", ".join(bases)
                arguments_str = ""

                if hasattr(cls, "argument_names"):
                    arguments = cls.argument_names
                    arguments_str = ", ".join(arguments)

                if arguments_str:
                    bases_arguments_str = "_".join([bases_str, arguments_str])
                else:
                    bases_arguments_str = ", ".join(bases)

                if cls_name in written_classes:
                    if bases_arguments_str in written_classes[cls_name]:
                        written_classes[cls_name][bases_arguments_str] += 1
                    else:
                        written_classes[cls_name].update({bases_arguments_str: 1})
                else:
                    written_classes[cls_name] = {bases_arguments_str: 1}
            elif isinstance(cls, str):
                cls_name = cls
                if cls_name in string_classes:
                    string_classes[cls_name] += 1
                else:
                    string_classes[cls_name] = 1

            if (
                hasattr(cls, "__name__")
                and written_classes[cls_name][bases_arguments_str] > 1
            ):
                pass
            elif isinstance(cls, str) and string_classes[cls] > 1:
                pass
            else:
                cls_data = {}

                if hasattr(cls, "__name__"):
                    cls_data["__bases__"] = cls.__bases__
                else:
                    cls_data["return_type"] = cls

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

                if hasattr(cls, "command_names"):
                    cls_data["command_names"] = cls.command_names

                if hasattr(cls, "query_names"):
                    cls_data["query_names"] = cls.query_names

                if hasattr(cls, "argument_names"):
                    cls_data["argument_names"] = cls.argument_names

                if cls_name in all_classes:
                    if bases_arguments_str in all_classes[cls_name]:
                        pass
                    else:
                        all_classes[cls_name].update({bases_arguments_str: cls_data})
                else:
                    all_classes[cls_name] = {bases_arguments_str: cls_data}

                if hasattr(cls, "child_object_type"):
                    _write_dynamic_cls_helper(out, cls.child_object_type)

                if hasattr(cls, "_child_classes"):
                    for _, child in cls._child_classes.items():
                        _write_dynamic_cls_helper(out, child)
    except Exception:
        raise


from ansys.fluent.core.solver.flobject import *  # noqa F403


class root(Group):
    "Root object."
    pass


def _set_all_classes(cls, all_classes):
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
            if hasattr(cls, "__name__"):
                cls_name = cls.__name__

                bases = [c.__name__ for c in cls.__bases__]
                bases_str = ", ".join(bases)
                arguments_str = ""

                if hasattr(cls, "argument_names"):
                    arguments = cls.argument_names
                    arguments_str = ", ".join(arguments)

                if arguments_str:
                    bases_arguments_str = "_".join([bases_str, arguments_str])
                else:
                    bases_arguments_str = ", ".join(bases)

                if cls_name in written_classes:
                    if bases_arguments_str in written_classes[cls_name]:
                        written_classes[cls_name][bases_arguments_str] += 1
                    else:
                        written_classes[cls_name].update({bases_arguments_str: 1})
                else:
                    written_classes[cls_name] = {bases_arguments_str: 1}
            elif isinstance(cls, str):
                cls_name = cls
                if cls_name in string_classes:
                    string_classes[cls_name] += 1
                else:
                    string_classes[cls_name] = 1

            if (
                hasattr(cls, "__name__")
                and written_classes[cls_name][bases_arguments_str] > 1
            ):
                pass
            elif isinstance(cls, str) and string_classes[cls] > 1:
                pass
            else:
                if cls_name == "root":
                    for attr, attr_value in all_classes[cls_name][
                        bases_arguments_str
                    ].items():
                        setattr(root, attr, attr_value)
                if hasattr(cls, "_child_classes"):
                    if cls_name == "root":
                        cls_class = root
                    else:
                        cls_class = type(
                            cls_name,
                            all_classes[cls_name][bases_arguments_str]["__bases__"],
                            all_classes[cls_name][bases_arguments_str],
                        )
                    for child_name, child in cls._child_classes.items():
                        child_class = type(
                            child_name,
                            all_classes[cls_name][bases_arguments_str]["__bases__"],
                            all_classes[cls_name][bases_arguments_str],
                        )
                        setattr(cls_class, child_name, child_class)
                        _set_all_classes(child, all_classes)
                if hasattr(cls, "child_object_type"):
                    _set_all_classes(cls.child_object_type, all_classes)
    except Exception:
        raise


if __name__ == "__main__":
    import time

    # from ansys.fluent.core.launcher.launcher import launch_fluent

    session = pyfluent.connect_to_fluent(
        ip="10.18.44.94", port=62923, password="fozrzpu5"
    )
    # session = launch_fluent()
    start_time = time.time()
    sinfo = session._settings_service.get_static_info()
    cls = flobject.get_cls("", sinfo, version=session._version)

    with open(
        _get_settings_utils_path(version=session._version), "w"
    ) as settings_utils:
        write_settings_classes(settings_utils, cls[0], sinfo, settings=False)

    # with open(
    #     _get_settings_utils_path(version=session._version), "w"
    # ) as settings_utils:
    #     write_settings_classes(settings_utils, cls[0], sinfo, settings=False)
    #     settings_utils.write("\n")
    #     settings_utils.write(f"all_classes = {all_classes}")

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

    written_classes = {}
    string_classes = {}

    with open(_get_settings_path(version=session._version), "w") as settings:
        write_settings_classes(settings, cls[0], sinfo, settings=True)

    print(f"settingsgen.py took {time.time() - start_time} seconds.")

    # root_childs = {
    #     "file": 0,
    #     "mesh": 0,
    #     "server": 0,
    #     "setup": 0,
    #     "solution": 0,
    #     "results": 0,
    #     "design": 0,
    #     "parametric_studies": 0,
    #     "current_parametric_study": 0,
    #     "parameters": 0,
    #     "parallel": 0,
    #     "transient_post_processing": 0,
    #     "exit": 0,
    # }

    # written_classes = {}
    # string_classes = {}

    # _set_all_classes(cls[0], all_classes)
    # final_root = root

    # print(f"written_classes = {len(written_classes)}")
    # print(f"string_classes = {len(string_classes)}")
    # print(len(all_classes.keys()))
    # print(all_classes["name"]["String"])
