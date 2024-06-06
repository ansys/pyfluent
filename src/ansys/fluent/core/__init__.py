"""A package providing Fluent's Solver and Meshing capabilities in Python."""

import importlib
import os
from pathlib import Path
import pydoc

import platformdirs

# isort: off
# Logging has to be imported before importing other PyFluent modules
from ansys.fluent.core.logging import set_console_logging_level  # noqa: F401

# isort: on

from ansys.fluent.core._version import __version__  # noqa: F401
from ansys.fluent.core.get_build_details import (  # noqa: F401
    get_build_version,
    get_build_version_string,
)
from ansys.fluent.core.utils import fldoc
from ansys.fluent.core.utils.fluent_version import FluentVersion  # noqa: F401
from ansys.fluent.core.warnings import (  # noqa: F401
    PyFluentDeprecationWarning,
    PyFluentUserWarning,
    warning,
)

_VERSION_INFO = None
"""Global variable indicating the version of the PyFluent package - Empty by default"""

_THIS_DIRNAME = os.path.dirname(__file__)
_README_FILE = os.path.normpath(os.path.join(_THIS_DIRNAME, "docs", "README.rst"))

if os.path.exists(_README_FILE):
    with open(_README_FILE, encoding="utf8") as f:
        __doc__ = f.read()


def version_info() -> str:
    """Method returning the version of PyFluent being used.

    Returns
    -------
    str
        The PyFluent version being used.

    Notes
    -------
    Only available in packaged versions. Otherwise it will return __version__.
    """
    return _VERSION_INFO if _VERSION_INFO is not None else __version__


# Setup data directory
USER_DATA_PATH = platformdirs.user_data_dir(
    appname="ansys_fluent_core", appauthor="Ansys"
)
EXAMPLES_PATH = os.path.join(USER_DATA_PATH, "examples")

CONTAINER_MOUNT_PATH = None

# Set this to False to stop automatically inferring and setting REMOTING_SERVER_ADDRESS
INFER_REMOTING_IP = True

# Time in second to wait for response for each ip while inferring remoting ip
INFER_REMOTING_IP_TIMEOUT_PER_IP = 2

pydoc.text.docother = fldoc.docother.__get__(pydoc.text, pydoc.TextDoc)

# Whether to use datamodel state caching
DATAMODEL_USE_STATE_CACHE = True

# Whether to use datamodel attribute caching
DATAMODEL_USE_ATTR_CACHE = True

# Whether stream and cache commands state
DATAMODEL_USE_NOCOMMANDS_DIFF_STATE = True

# Whether to use remote gRPC file transfer service
USE_FILE_TRANSFER_SERVICE = False

# Directory where API files are writes out during codegen
CODEGEN_OUTDIR = (Path(__file__) / ".." / "generated").resolve()

# Whether to zip settings API files during codegen
CODEGEN_ZIP_SETTINGS = False

# Whether to show mesh after case read
SHOW_MESH_AFTER_CASE_READ = False

_launcher = "ansys.fluent.core.launcher.launcher"
_pyfluent_enums = "ansys.fluent.core.launcher.pyfluent_enums"

_pyfluent_modules = {
    "launch_fluent": _launcher,
    "connect_to_fluent": _launcher,
    "FluentLinuxGraphicsDriver": _pyfluent_enums,
    "FluentWindowsGraphicsDriver": _pyfluent_enums,
    "FluentMode": _pyfluent_enums,
    "UIMode": _pyfluent_enums,
    "BatchOps": "ansys.fluent.core.services.batch_ops",
    "setup_for_fluent": "ansys.fluent.core.utils.setup_for_fluent",
    "search": "ansys.fluent.core.utils.search",
}


def __getattr__(attr):
    if attr in _pyfluent_modules:
        return getattr(importlib.import_module(_pyfluent_modules[attr]), attr)

    elif attr == "Fluent":
        from ansys.fluent.core.session import BaseSession as Fluent

        return Fluent


_pyfluent_modules["Fluent"] = ""
__all__ = list(_pyfluent_modules)


def __dir__():
    public_modules = globals().keys() | _pyfluent_modules
    public_modules -= {
        "os",
        "importlib",
        "Path",
    }
    return list(public_modules)
