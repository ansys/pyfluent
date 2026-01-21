# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
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
import pydoc
import warnings

# isort: off

# config must be initialized before logging setup.
from ansys.fluent.core.module_config import config

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
from ansys.fluent.core.utils import fldoc
from ansys.fluent.core.utils.fluent_version import FluentVersion  # noqa: F401
from ansys.fluent.core.utils.setup_for_fluent import setup_for_fluent  # noqa: F401

__version__ = "0.38.dev3"

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


pydoc.text.docother = fldoc.docother.__get__(pydoc.text, pydoc.TextDoc)


_config_by_deprecated_name = {
    "FLUENT_RELEASE_VERSION": "fluent_release_version",
    "FLUENT_DEV_VERSION": "fluent_dev_version",
    "EXAMPLES_PATH": "examples_path",
    "CONTAINER_MOUNT_SOURCE": "container_mount_source",
    "CONTAINER_MOUNT_TARGET": "container_mount_target",
    "INFER_REMOTING_IP": "infer_remoting_ip",
    "INFER_REMOTING_IP_TIMEOUT_PER_IP": "infer_remoting_ip_timeout_per_ip",
    "DATAMODEL_USE_STATE_CACHE": "datamodel_use_state_cache",
    "DATAMODEL_USE_ATTR_CACHE": "datamodel_use_attr_cache",
    "DATAMODEL_USE_NOCOMMANDS_DIFF_STATE": "datamodel_use_nocommands_diff_state",
    "DATAMODEL_RETURN_STATE_CHANGES": "datamodel_return_state_changes",
    "USE_FILE_TRANSFER_SERVICE": "use_file_transfer_service",
    "CODEGEN_OUTDIR": "codegen_outdir",
    "FLUENT_SHOW_MESH_AFTER_CASE_READ": "fluent_show_mesh_after_case_read",
    "FLUENT_AUTOMATIC_TRANSCRIPT": "fluent_automatic_transcript",
    "SUPPORT_SOLVER_INTERRUPT": "support_solver_interrupt",
    "START_WATCHDOG": "start_watchdog",
    "CHECK_HEALTH_TIMEOUT": "check_health_timeout",
    "CHECK_HEALTH": "check_health",
    "PRINT_SEARCH_RESULTS": "print_search_results",
    "CLEAR_FLUENT_PARA_ENVS": "clear_fluent_para_envs",
    "LAUNCH_FLUENT_STDOUT": "launch_fluent_stdout",
    "LAUNCH_FLUENT_STDERR": "launch_fluent_stderr",
    "LAUNCH_FLUENT_IP": "launch_fluent_ip",
    "LAUNCH_FLUENT_PORT": "launch_fluent_port",
    "LAUNCH_FLUENT_SKIP_PASSWORD_CHECK": "launch_fluent_skip_password_check",
}


def __getattr__(name: str) -> str:
    """Get the value of a deprecated configuration variable."""
    if name in _config_by_deprecated_name:
        config_name = _config_by_deprecated_name[name]
        warnings.warn(
            f"'{name}' is deprecated, use 'config.{config_name}' instead.",
            category=PyFluentDeprecationWarning,
        )
        return getattr(config, config_name)
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
