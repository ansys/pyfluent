"""A package providing Fluent's Solver and Meshing capabilities in Python."""

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
from ansys.fluent.core.launcher.launcher import (  # noqa: F401
    connect_to_fluent,
    launch_fluent,
)
from ansys.fluent.core.launcher.pyfluent_enums import (  # noqa: F401
    Dimension,
    FluentLinuxGraphicsDriver,
    FluentMode,
    FluentWindowsGraphicsDriver,
    Precision,
    UIMode,
)
from ansys.fluent.core.parametric import LocalParametricStudy  # noqa: F401
from ansys.fluent.core.search import search  # noqa: F401
from ansys.fluent.core.services.batch_ops import BatchOps  # noqa: F401
from ansys.fluent.core.session import BaseSession as Fluent  # noqa: F401
from ansys.fluent.core.streaming_services.events_streaming import (  # noqa: F401
    Event,
    MeshingEvent,
    SolverEvent,
)
from ansys.fluent.core.utils import fldoc
from ansys.fluent.core.utils.fluent_version import FluentVersion  # noqa: F401
from ansys.fluent.core.utils.setup_for_fluent import setup_for_fluent  # noqa: F401
from ansys.fluent.core.warnings import (  # noqa: F401
    PyFluentDeprecationWarning,
    PyFluentUserWarning,
    warning,
)

try:
    from ansys.fluent.core.generated.solver.settings_builtin import *  # noqa: F401, F403
except (ImportError, AttributeError, SyntaxError):
    pass

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


EXAMPLES_PATH = os.path.join(
    platformdirs.user_documents_dir(), "ansys_fluent_core_examples"
)

# Host path which is mounted to the container
CONTAINER_MOUNT_SOURCE = None

# Path inside the container where the host path is mounted
CONTAINER_MOUNT_TARGET = "/mnt/pyfluent"

# Set this to False to stop automatically inferring and setting REMOTING_SERVER_ADDRESS
INFER_REMOTING_IP = True

# Time in second to wait for response for each ip while inferring remoting ip
INFER_REMOTING_IP_TIMEOUT_PER_IP = 2

pydoc.text.docother = fldoc.docother.__get__(pydoc.text, pydoc.TextDoc)

# Whether to use datamodel state caching
DATAMODEL_USE_STATE_CACHE = True

# Whether to use datamodel attribute caching
DATAMODEL_USE_ATTR_CACHE = True

# Whether to stream and cache commands state
DATAMODEL_USE_NOCOMMANDS_DIFF_STATE = True

# Whether to return the state changes on mutating datamodel rpcs
DATAMODEL_RETURN_STATE_CHANGES = True

# Whether to use remote gRPC file transfer service
USE_FILE_TRANSFER_SERVICE = False

# Directory where API files are writes out during codegen
CODEGEN_OUTDIR = (Path(__file__) / ".." / "generated").resolve()

# Whether to zip settings API files during codegen
CODEGEN_ZIP_SETTINGS = os.getenv("PYFLUENT_CODEGEN_ZIP_SETTINGS", False)

# Whether to show mesh after case read
SHOW_MESH_AFTER_CASE_READ = False

# Whether to interrupt Fluent solver from PyFluent
SUPPORT_SOLVER_INTERRUPT = False

# Whether to start watchdog
START_WATCHDOG = None

# Whether to skip health check
CHECK_HEALTH = True
