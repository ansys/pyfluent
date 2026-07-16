# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
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

# isort: off

# config must be initialized before logging setup.
from ansys.fluent.core.module_config import *

# Logging has to be imported before importing other PyFluent modules
from ansys.fluent.core.logger import *

# isort: on

from ansys.fluent.core.fields.field_data_interfaces import *
from ansys.fluent.core.get_build_details import *
from ansys.fluent.core.launcher.launch_options import *
from ansys.fluent.core.launcher.launcher import *
from ansys.fluent.core.parametric import *
from ansys.fluent.core.pyfluent_warnings import *
from ansys.fluent.core.search import *
from ansys.fluent.core.services.batch_ops import *
from ansys.fluent.core.session import *
from ansys.fluent.core.session import BaseSession as Fluent
from ansys.fluent.core.session_utilities import *
from ansys.fluent.core.solver.flobject import ExposureLevel  # noqa: E402
from ansys.fluent.core.streaming_services.events_streaming import *
from ansys.fluent.core.streaming_services.events_streaming_v1 import *
from ansys.fluent.core.utils import *
from ansys.fluent.core.utils.context_managers import *
from ansys.fluent.core.utils.fluent_version import *
from ansys.fluent.core.utils.setup_for_fluent import *

__all__ = [
    # Explicitly exported symbols from wildcard imports
    "Fluent",
    "ExposureLevel",
    # Submodules for explicit import support
    "docker",
    "examples",
    "exceptions",
    "field_data_interfaces",
    "filereader",
    "fluent_connection",
    "generated",
    "journaling",
    "launcher",
    "logger",
    "module_config",
    "parametric",
    "pyfluent_warnings",
    "rpvars",
    "scheduler",
    "search",
    "services",
    "session",
    "session_base_meshing",
    "session_meshing",
    "session_pure_meshing",
    "session_shared",
    "session_solver",
    "session_solver_aero",
    "session_solver_icing",
    "session_utilities",
    "solver",
    "streaming_services",
    "system_coupling",
    "utils",
    "variable_strategies",
    "workflow",
]

# Submodules for lazy loading - avoid circular imports
_submodules = {
    "docker": "ansys.fluent.core.docker",
    "examples": "ansys.fluent.core.examples",
    "exceptions": "ansys.fluent.core.exceptions",
    "field_data_interfaces": "ansys.fluent.core.field_data_interfaces",
    "filereader": "ansys.fluent.core.filereader",
    "fluent_connection": "ansys.fluent.core.fluent_connection",
    "generated": "ansys.fluent.core.generated",
    "journaling": "ansys.fluent.core.journaling",
    "launcher": "ansys.fluent.core.launcher",
    "module_config": "ansys.fluent.core.module_config",
    "parametric": "ansys.fluent.core.parametric",
    "pyfluent_warnings": "ansys.fluent.core.pyfluent_warnings",
    "rpvars": "ansys.fluent.core.rpvars",
    "scheduler": "ansys.fluent.core.scheduler",
    "search": "ansys.fluent.core.search",
    "services": "ansys.fluent.core.services",
    "session": "ansys.fluent.core.session",
    "session_base_meshing": "ansys.fluent.core.session_base_meshing",
    "session_meshing": "ansys.fluent.core.session_meshing",
    "session_pure_meshing": "ansys.fluent.core.session_pure_meshing",
    "session_shared": "ansys.fluent.core.session_shared",
    "session_solver": "ansys.fluent.core.session_solver",
    "session_solver_aero": "ansys.fluent.core.session_solver_aero",
    "session_solver_icing": "ansys.fluent.core.session_solver_icing",
    "session_utilities": "ansys.fluent.core.session_utilities",
    "solver": "ansys.fluent.core.solver",
    "streaming_services": "ansys.fluent.core.streaming_services",
    "system_coupling": "ansys.fluent.core.system_coupling",
    "utils": "ansys.fluent.core.utils",
    "variable_strategies": "ansys.fluent.core.variable_strategies",
    "workflow": "ansys.fluent.core.workflow",
}
__version__ = "0.41.dev1"

_VERSION_INFO = None
"""
Global variable indicating the version info of the PyFluent package.
Build timestamp and commit hash are added to this variable during packaging.
"""

import os as _os  # noqa: E402
import warnings as _warnings  # noqa: E402

_THIS_DIRNAME = _os.path.dirname(__file__)
_README_FILE = _os.path.normpath(_os.path.join(_THIS_DIRNAME, "docs", "README.rst"))

if _os.path.exists(_README_FILE):
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


import pydoc as _pydoc  # noqa: E402

from ansys.fluent.core.utils import fldoc as _fldoc  # noqa: E402

_pydoc.text.docother = _fldoc.docother.__get__(_pydoc.text, _pydoc.TextDoc)


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
    "LAUNCH_FLUENT_SKIP_PASSWORD_CHECK": "launch_fluent_skip_password_check",  # nosec B105: Not a password
}


def __getattr__(name: str):
    """Handle lazy module loading and deprecated config variable access."""
    # Try lazy module loading first
    if name in _submodules:
        module_name = _submodules[name]
        import importlib

        mod = importlib.import_module(module_name)
        globals()[name] = mod
        return mod

    # Try deprecated config variable access
    if name in _config_by_deprecated_name:
        import warnings as _warnings_module

        config_name = _config_by_deprecated_name[name]
        _warnings_module.warn(
            f"'{name}' is deprecated, use 'config.{config_name}' instead.",
            category=PyFluentDeprecationWarning,
        )
        return getattr(config, config_name)

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    """Return list of public symbols including lazy-loaded submodules."""
    # Get all symbols currently in globals (from wildcard imports)
    module_symbols = set(globals().keys())

    # Add submodule names (even if not yet loaded, they can be accessed via __getattr__)
    all_symbols = module_symbols | set(_submodules.keys())

    # Explicitly add version_info if not already present
    all_symbols.add("version_info")

    # Return sorted list of public symbols (exclude private ones)
    return sorted([s for s in all_symbols if not s.startswith("_")])


# Build __all__ to include only imported symbols, excluding submodule names from _submodules
# This ensures that `from ansys.fluent.core import *` only imports public symbols,
# not submodules (which can still be accessed via lazy loading via __getattr__)
_submodule_names = set(_submodules.keys())
__all__ = sorted(
    [
        name
        for name in dir()
        if not name.startswith("_") and name not in _submodule_names
    ]
)


__version__ = "0.41.dev0"
