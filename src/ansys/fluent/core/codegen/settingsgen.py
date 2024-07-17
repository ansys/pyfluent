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

from ansys.fluent.core.solver import flobject


def _gethash(obj_info):
    dhash = hashlib.sha256()
    dhash.update(pickle.dumps(obj_info))
    return dhash.hexdigest()


def _get_indent_str(indent):
    return f"{' '*indent*4}"


def _write_cls_helper(out, cls, indent=0):
    try:
        istr = _get_indent_str(indent)
        istr1 = _get_indent_str(indent + 1)
        istr2 = _get_indent_str(indent + 2)
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
                _write_cls_helper(out, child, indent + 1)

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
                _write_cls_helper(out, child, indent + 1)

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
                _write_cls_helper(out, child, indent + 1)

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
                _write_cls_helper(out, child, indent + 1)

        child_object_type = getattr(cls, "child_object_type", None)
        if child_object_type:
            _write_cls_helper(out, child_object_type, indent + 1)

        child_aliases = getattr(cls, "_child_aliases", None)
        if child_aliases:
            out.write(f"{istr1}_child_aliases = dict(\n")
            out.writelines([f'{istr2}{k}="{v}",\n' for k, v in child_aliases.items()])
            out.write(f"{istr1})\n\n")

        return_type = getattr(cls, "return_type", None)
        if return_type:
            _write_cls_helper(out, return_type, indent + 1)
    except Exception:
        raise


def write_settings_classes(out: IO, cls, obj_info: dict):
    """Write the settings classes in 'out' stream.

    Parameters
    ----------
    out: Stream
        Out file object.
    cls: class
        Settings top level object.
    obj_info: dict
        Static info.
    """
    hash = _gethash(obj_info)
    out.write("#\n")
    out.write("# This is an auto-generated file.  DO NOT EDIT!\n")
    out.write("#\n")
    out.write("\n")
    out.write("from ansys.fluent.core.solver.flobject import *\n\n")
    out.write(f'SHASH = "{hash}"\n')
    _write_cls_helper(out, cls)


if __name__ == "__main__":
    # from ansys.fluent.core.launcher.launcher import launch_fluent

    dirname = os.path.dirname(__file__)
    filepath = os.path.normpath(
        os.path.join(
            dirname,
            "..",
            "generated",
            "solver",
            "settings.py",
        )
    )
    import ansys.fluent.core as pyfluent

    session = pyfluent.connect_to_fluent(
        ip="10.18.44.94", port=57998, password="rqauxqpu"
    )
    # session = launch_fluent()
    sinfo = session._settings_service.get_static_info()
    cls = flobject.get_cls("", sinfo, version=session._version)
    with open(filepath, "w") as f:
        write_settings_classes(f, cls[0], sinfo)
