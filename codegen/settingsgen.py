"""Provide a module to generate the Fluent settings tree.

Running this module generates a python module with the definition of the Fluent
settings classes. The out is placed at:

- src/ansys/fluent/core/solver/settings.py

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
        out.write(
            f"{istr}class {cls.__name__}"
            f'({", ".join(c.__name__ for c in cls.__bases__)}):\n'
        )

        doc = ("\n" + istr1).join(cls.__doc__.split("\n"))
        out.write(f'{istr1}"""\n')
        out.write(f"{istr1}{doc}")
        out.write(f'\n{istr1}"""\n')
        out.write(f'{istr1}scheme_name = "{cls.scheme_name}"\n')

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
            for child in child_names:
                _write_cls_helper(out, getattr(cls, child), indent + 1)

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
            for command in command_names:
                _write_cls_helper(out, getattr(cls, command), indent + 1)

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
            for argument in arguments:
                _write_cls_helper(out, getattr(cls, argument), indent + 1)
        child_object_type = getattr(cls, "child_object_type", None)
        if child_object_type:
            _write_cls_helper(out, child_object_type, indent + 1)
    except Exception:
        raise


def write_settings_classes(out: IO, cls, obj_info):
    """Write the settings classes in 'out' stream.

    Parameters
    ----------
    out:     Stream
    flproxy: Proxy
             Object that interfaces with the Fluent backend
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
    from ansys.fluent.core.launcher.launcher import launch_fluent

    dirname = os.path.dirname(__file__)
    filepath = os.path.normpath(
        os.path.join(
            dirname,
            "..",
            "src",
            "ansys",
            "fluent",
            "core",
            "solver",
            "settings.py",
        )
    )
    session = launch_fluent()
    sinfo = session.get_settings_service().get_static_info()
    cls = flobject.get_cls("", sinfo)
    with open(filepath, "w") as f:
        write_settings_classes(f, cls, sinfo)
