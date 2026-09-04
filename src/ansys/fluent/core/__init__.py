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

from ansys.fluent.core.exceptions import *
from ansys.fluent.core.fields.field_data_interfaces import *
from ansys.fluent.core.get_build_details import *
from ansys.fluent.core.launcher.launch_options import *
from ansys.fluent.core.launcher.launcher import *
from ansys.fluent.core.legacy.local_parametric_study import *
from ansys.fluent.core.meshing import *
from ansys.fluent.core.search import *
from ansys.fluent.core.services.batch_ops import *
from ansys.fluent.core.session import *
from ansys.fluent.core.session.session import BaseSession
from ansys.fluent.core.solver.flobject import ExposureLevel  # noqa: E402
from ansys.fluent.core.streaming_services.events_streaming import *
from ansys.fluent.core.utils import *
from ansys.fluent.core.utils.context_managers import *
from ansys.fluent.core.utils.fluent_version import *
from ansys.fluent.core.utils.setup_for_fluent import *

__version__ = "0.43.dev0"

_VERSION_INFO = None
"""
Global variable indicating the version info of the PyFluent package.
Build timestamp and commit hash are added to this variable during packaging.
"""

import os as _os  # noqa: E402
import sys as _sys  # noqa: E402
import warnings as _warnings  # noqa: E402

_THIS_DIRNAME = _os.path.dirname(__file__)
_README_FILE = _os.path.normpath(_os.path.join(_THIS_DIRNAME, "docs", "README.rst"))

if _os.path.exists(_README_FILE):
    with open(_README_FILE, encoding="utf8") as f:
        __doc__ = f.read()

from ansys.fluent.core import exceptions as _exceptions  # noqa: E402
from ansys.fluent.core import file_reader as _file_reader  # noqa: E402
from ansys.fluent.core.legacy import (  # noqa: E402
    local_parametric_study as _local_parametric_study,
)
from ansys.fluent.core.legacy import rpvars as _rpvars  # noqa: E402
from ansys.fluent.core.session import file as _session_file  # noqa: E402

_sys.modules["ansys.fluent.core.file_session"] = _session_file
_sys.modules["ansys.fluent.core.rpvars"] = _rpvars
_sys.modules["ansys.fluent.core.parametric"] = _local_parametric_study
_sys.modules["ansys.fluent.core.pyfluent_warnings"] = _exceptions
_sys.modules["ansys.fluent.core.filereader"] = _file_reader


class Fluent(BaseSession):
    """Fluent session management.

    This class serves as the primary base class for both meshing and solver
    sessions within PyFluent. It extends the core functionality
    provided by the base session instance.

    Attributes
    ----------
    Inherits all attributes from :class:`~ansys.fluent.core.session.session.BaseSession`.
    """


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


# ──────────────────────────────────────────────────────────────────────────────
# Module docstring from README
# ──────────────────────────────────────────────────────────────────────────────
_THIS_DIRNAME = _os.path.dirname(__file__)
_README_FILE = _os.path.normpath(_os.path.join(_THIS_DIRNAME, "docs", "README.rst"))

if _os.path.exists(_README_FILE):
    with open(_README_FILE, encoding="utf8") as f:
        __doc__ = f.read()

# ──────────────────────────────────────────────────────────────────────────────
# Lazy imports via PEP 562 __getattr__ / __dir__
# Maps public name -> (module_path, attribute_name)
# ──────────────────────────────────────────────────────────────────────────────
_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    # fields.field_data_interfaces
    "PathlinesFieldDataRequest": (
        "ansys.fluent.core.fields.field_data_interfaces",
        "PathlinesFieldDataRequest",
    ),
    "ScalarFieldDataRequest": (
        "ansys.fluent.core.fields.field_data_interfaces",
        "ScalarFieldDataRequest",
    ),
    "SurfaceDataType": (
        "ansys.fluent.core.fields.field_data_interfaces",
        "SurfaceDataType",
    ),
    "SurfaceFieldDataRequest": (
        "ansys.fluent.core.fields.field_data_interfaces",
        "SurfaceFieldDataRequest",
    ),
    "VectorFieldDataRequest": (
        "ansys.fluent.core.fields.field_data_interfaces",
        "VectorFieldDataRequest",
    ),
    # get_build_details
    "get_build_version": (
        "ansys.fluent.core.get_build_details",
        "get_build_version",
    ),
    "get_build_version_string": (
        "ansys.fluent.core.get_build_details",
        "get_build_version_string",
    ),
    # launcher.launch_options
    "FluentMode": (
        "ansys.fluent.core.launcher.launch_options",
        "FluentMode",
    ),
    "UIMode": (
        "ansys.fluent.core.launcher.launch_options",
        "UIMode",
    ),
    "Dimension": (
        "ansys.fluent.core.launcher.launch_options",
        "Dimension",
    ),
    "Precision": (
        "ansys.fluent.core.launcher.launch_options",
        "Precision",
    ),
    "FluentWindowsGraphicsDriver": (
        "ansys.fluent.core.launcher.launch_options",
        "FluentWindowsGraphicsDriver",
    ),
    "FluentLinuxGraphicsDriver": (
        "ansys.fluent.core.launcher.launch_options",
        "FluentLinuxGraphicsDriver",
    ),
    # launcher.launcher
    "create_launcher": (
        "ansys.fluent.core.launcher.launcher",
        "create_launcher",
    ),
    "launch_fluent": (
        "ansys.fluent.core.launcher.launcher",
        "launch_fluent",
    ),
    "connect_to_fluent": (
        "ansys.fluent.core.launcher.launcher",
        "connect_to_fluent",
    ),
    # parametric
    "LocalParametricStudy": (
        "ansys.fluent.core.parametric",
        "LocalParametricStudy",
    ),
    # search
    "search": (
        "ansys.fluent.core.search",
        "search",
    ),
    # services.batch_ops
    "BatchOps": (
        "ansys.fluent.core.services.batch_ops",
        "BatchOps",
    ),
    # session
    "BaseSession": (
        "ansys.fluent.core.session",
        "BaseSession",
    ),
    "Fluent": (
        "ansys.fluent.core.session",
        "BaseSession",
    ),
    # session_utilities
    "Meshing": (
        "ansys.fluent.core.session_utilities",
        "Meshing",
    ),
    "PureMeshing": (
        "ansys.fluent.core.session_utilities",
        "PureMeshing",
    ),
    "PrePost": (
        "ansys.fluent.core.session_utilities",
        "PrePost",
    ),
    "Solver": (
        "ansys.fluent.core.session_utilities",
        "Solver",
    ),
    "SolverAero": (
        "ansys.fluent.core.session_utilities",
        "SolverAero",
    ),
    "SolverIcing": (
        "ansys.fluent.core.session_utilities",
        "SolverIcing",
    ),
    # solver.exposure_level (lightweight, no ansys.units dependency)
    "ExposureLevel": (
        "ansys.fluent.core.solver.exposure_level",
        "ExposureLevel",
    ),
    # streaming_services.events_streaming
    "EventsManager": (
        "ansys.fluent.core.streaming_services.events_streaming",
        "EventsManager",
    ),
    "Event": (
        "ansys.fluent.core.streaming_services.events_streaming",
        "Event",
    ),
    "SolverEvent": (
        "ansys.fluent.core.streaming_services.events_streaming",
        "SolverEvent",
    ),
    "MeshingEvent": (
        "ansys.fluent.core.streaming_services.events_streaming",
        "MeshingEvent",
    ),
    "TimestepStartedEventInfo": (
        "ansys.fluent.core.streaming_services.events_streaming",
        "TimestepStartedEventInfo",
    ),
    "TimestepEndedEventInfo": (
        "ansys.fluent.core.streaming_services.events_streaming",
        "TimestepEndedEventInfo",
    ),
    "IterationEndedEventInfo": (
        "ansys.fluent.core.streaming_services.events_streaming",
        "IterationEndedEventInfo",
    ),
    "CalculationsStartedEventInfo": (
        "ansys.fluent.core.streaming_services.events_streaming",
        "CalculationsStartedEventInfo",
    ),
    "CalculationsEndedEventInfo": (
        "ansys.fluent.core.streaming_services.events_streaming",
        "CalculationsEndedEventInfo",
    ),
    "CalculationsPausedEventInfo": (
        "ansys.fluent.core.streaming_services.events_streaming",
        "CalculationsPausedEventInfo",
    ),
    "CalculationsResumedEventInfo": (
        "ansys.fluent.core.streaming_services.events_streaming",
        "CalculationsResumedEventInfo",
    ),
    "AboutToLoadCaseEventInfo": (
        "ansys.fluent.core.streaming_services.events_streaming",
        "AboutToLoadCaseEventInfo",
    ),
    "CaseLoadedEventInfo": (
        "ansys.fluent.core.streaming_services.events_streaming",
        "CaseLoadedEventInfo",
    ),
    "AboutToLoadDataEventInfo": (
        "ansys.fluent.core.streaming_services.events_streaming",
        "AboutToLoadDataEventInfo",
    ),
    "DataLoadedEventInfo": (
        "ansys.fluent.core.streaming_services.events_streaming",
        "DataLoadedEventInfo",
    ),
    "AboutToInitializeSolutionEventInfo": (
        "ansys.fluent.core.streaming_services.events_streaming",
        "AboutToInitializeSolutionEventInfo",
    ),
    "SolutionInitializedEventInfo": (
        "ansys.fluent.core.streaming_services.events_streaming",
        "SolutionInitializedEventInfo",
    ),
    "ReportDefinitionUpdatedEventInfo": (
        "ansys.fluent.core.streaming_services.events_streaming",
        "ReportDefinitionUpdatedEventInfo",
    ),
    "ReportPlotSetUpdatedEventInfo": (
        "ansys.fluent.core.streaming_services.events_streaming",
        "ReportPlotSetUpdatedEventInfo",
    ),
    "ResidualPlotUpdatedEventInfo": (
        "ansys.fluent.core.streaming_services.events_streaming",
        "ResidualPlotUpdatedEventInfo",
    ),
    "SettingsClearedEventInfo": (
        "ansys.fluent.core.streaming_services.events_streaming",
        "SettingsClearedEventInfo",
    ),
    "SolutionPausedEventInfo": (
        "ansys.fluent.core.streaming_services.events_streaming",
        "SolutionPausedEventInfo",
    ),
    "ProgressUpdatedEventInfo": (
        "ansys.fluent.core.streaming_services.events_streaming",
        "ProgressUpdatedEventInfo",
    ),
    "SolverTimeEstimateUpdatedEventInfo": (
        "ansys.fluent.core.streaming_services.events_streaming",
        "SolverTimeEstimateUpdatedEventInfo",
    ),
    "FatalErrorEventInfo": (
        "ansys.fluent.core.streaming_services.events_streaming",
        "FatalErrorEventInfo",
    ),
    # utils
    "load_module": (
        "ansys.fluent.core.utils",
        "load_module",
    ),
    "get_user_data_dir": (
        "ansys.fluent.core.utils",
        "get_user_data_dir",
    ),
    # utils.context_managers
    "using": (
        "ansys.fluent.core.utils.context_managers",
        "using",
    ),
    # utils.fluent_version
    "FluentVersion": (
        "ansys.fluent.core.utils.fluent_version",
        "FluentVersion",
    ),
    # utils.setup_for_fluent
    "setup_for_fluent": (
        "ansys.fluent.core.utils.setup_for_fluent",
        "setup_for_fluent",
    ),
}

# ──────────────────────────────────────────────────────────────────────────────
# Explicit __all__ (preserves the same public API surface)
# ──────────────────────────────────────────────────────────────────────────────
__all__ = [
    # Eager
    "config",
    "set_console_logging_level",
    "PyFluentDeprecationWarning",
    "PyFluentUserWarning",
    "FluentDevVersionWarning",
    "warning",
    "__version__",
    "version_info",
    # Lazy
    *_LAZY_IMPORTS.keys(),
]

# ──────────────────────────────────────────────────────────────────────────────
# Deprecated config variable names (backward compat)
# ──────────────────────────────────────────────────────────────────────────────
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

# ──────────────────────────────────────────────────────────────────────────────
# PEP 562: module-level __getattr__ for lazy imports + deprecated config names
# ──────────────────────────────────────────────────────────────────────────────
from typing import TYPE_CHECKING as _TYPE_CHECKING  # noqa: E402

if not _TYPE_CHECKING:

    def __getattr__(name: str):
        """Lazy-load public symbols on first access; also handles deprecated names."""
        # 1. Lazy imports
        if name in _LAZY_IMPORTS:
            module_path, attr_name = _LAZY_IMPORTS[name]
            module = _importlib.import_module(module_path)
            value = getattr(module, attr_name)
            globals()[name] = value  # cache for subsequent access
            return value

        # 2. Deprecated config variable names
        if name in _config_by_deprecated_name:
            config_name = _config_by_deprecated_name[name]
            _warnings.warn(
                f"'{name}' is deprecated, use 'config.{config_name}' instead.",
                category=PyFluentDeprecationWarning,
            )
            return getattr(config, config_name)

        raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


# Submodules that should appear in dir() for backward compatibility
_SUBMODULES = {
    "data_model_cache",
    "docker",
    "examples",
    "exceptions",
    "expressions",
    "fields",
    "filereader",
    "file_session",
    "fluent_connection",
    "generated",
    "get_build_details",
    "journaling",
    "launcher",
    "logger",
    "meshing",
    "module_config",
    "parametric",
    "pyfluent_warnings",
    "report",
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
    "workflow_new",
}


def __dir__():
    """Return all public names (eager + lazy + submodules) for tab-completion."""
    return sorted(
        set(__all__) | set(globals().keys()) | _SUBMODULES - {"_TYPE_CHECKING"}
    )


# ──────────────────────────────────────────────────────────────────────────────
# pydoc customization (lightweight, stdlib only)
# ──────────────────────────────────────────────────────────────────────────────
import pydoc as _pydoc  # noqa: E402

from ansys.fluent.core.utils import fldoc as _fldoc  # noqa: E402

_pydoc.text.docother = _fldoc.docother.__get__(_pydoc.text, _pydoc.TextDoc)


# ──────────────────────────────────────────────────────────────────────────────
# Utility: force-load all lazy symbols (for tests and AOT scenarios)
# ──────────────────────────────────────────────────────────────────────────────
def _eager_load():
    """Force-load all lazy symbols. Used by test_public_api.py and AOT setups."""
    for name in _LAZY_IMPORTS:
        getattr(__import__(__name__), name)
