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

"""A package providing Fluent's Solver and Meshing capabilities in Python."""

import os
from pathlib import Path
import pydoc

# isort: off
# Logging has to be imported before importing other PyFluent modules
from ansys.fluent.core.logger import set_console_logging_level  # noqa: F401

# isort: on

from ansys.fluent.core.field_data_interfaces import (  # noqa: F401
    PathlinesFieldDataRequest,
    ScalarFieldDataRequest,
    SurfaceDataType,
    SurfaceFieldDataRequest,
    VectorFieldDataRequest,
)
from ansys.fluent.core.get_build_details import (  # noqa: F401
    get_build_version,
    get_build_version_string,
)
from ansys.fluent.core.launcher.launch_options import (  # noqa: F401
    Dimension,
    FluentLinuxGraphicsDriver,
    FluentMode,
    FluentWindowsGraphicsDriver,
    Precision,
    UIMode,
)
from ansys.fluent.core.launcher.launcher import (  # noqa: F401
    connect_to_fluent,
    launch_fluent,
)
from ansys.fluent.core.parametric import LocalParametricStudy  # noqa: F401
from ansys.fluent.core.pyfluent_warnings import (  # noqa: F401
    PyFluentDeprecationWarning,
    PyFluentUserWarning,
    warning,
)
from ansys.fluent.core.search import search  # noqa: F401
from ansys.fluent.core.services.batch_ops import BatchOps  # noqa: F401
from ansys.fluent.core.session import BaseSession as Fluent  # noqa: F401
from ansys.fluent.core.session_utilities import (  # noqa: F401
    Meshing,
    PrePost,
    PureMeshing,
    Solver,
    SolverAero,
    SolverIcing,
)
from ansys.fluent.core.streaming_services.events_streaming import *  # noqa: F401, F403
from ansys.fluent.core.utils import fldoc, get_examples_download_dir
from ansys.fluent.core.utils.fluent_version import FluentVersion  # noqa: F401
from ansys.fluent.core.utils.setup_for_fluent import setup_for_fluent  # noqa: F401

__version__ = "0.33.1"

_VERSION_INFO = None
"""
Global variable indicating the version info of the PyFluent package.
Build timestamp and commit hash are added to this variable during packaging.
"""

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


# Latest released Fluent version
FLUENT_RELEASE_VERSION = "25.2.0"

# Current dev Fluent version
FLUENT_DEV_VERSION = "26.1.0"

# Path to the example input/data files are downloaded
EXAMPLES_PATH = str(get_examples_download_dir())

# Host path which is mounted to the container
CONTAINER_MOUNT_SOURCE = None

# Path inside the container where the host path is mounted
CONTAINER_MOUNT_TARGET = "/home/container/workdir"

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

# Directory where API files are written out during codegen
CODEGEN_OUTDIR = os.getenv(
    "PYFLUENT_CODEGEN_OUTDIR", (Path(__file__) / ".." / "generated").resolve()
)

# Whether to show mesh in Fluent after case read
FLUENT_SHOW_MESH_AFTER_CASE_READ = False

# Whether to write the automatic transcript in Fluent
FLUENT_AUTOMATIC_TRANSCRIPT = False

# Whether to interrupt Fluent solver from PyFluent
SUPPORT_SOLVER_INTERRUPT = False

# Whether to start watchdog
START_WATCHDOG = None

# Health check timeout in seconds
CHECK_HEALTH_TIMEOUT = 60

# Whether to skip health check
CHECK_HEALTH = True

# Whether to print search results
PRINT_SEARCH_RESULTS = True

# Whether to clear environment variables related to Fluent parallel mode
CLEAR_FLUENT_PARA_ENVS = False

# Set stdout of the launched Fluent process
# Valid values are same as subprocess.Popen's stdout argument
LAUNCH_FLUENT_STDOUT = None

# Set stderr of the launched Fluent process
# Valid values are same as subprocess.Popen's stderr argument
LAUNCH_FLUENT_STDERR = None

# Set the IP address of the Fluent server while launching Fluent
LAUNCH_FLUENT_IP = None

# Set the port of the Fluent server while launching Fluent
LAUNCH_FLUENT_PORT = None

# Skip password check during rpc execution when Fluent is launched from PyFluent
LAUNCH_FLUENT_SKIP_PASSWORD_CHECK = False
