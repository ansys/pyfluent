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
from ansys.fluent.core.diagnostics.logger import *

# isort: on

# Only cheap, dependency-free modules are imported eagerly here. Everything
# else is deferred via the PEP 562 __getattr__ defined below to keep
# `import ansys.fluent.core` fast (see issue #4924 - avoid eager imports
# where possible).
from ansys.fluent.core.diagnostics.exceptions import *

__version__ = "0.43.dev0"

_VERSION_INFO = None
"""
Global variable indicating the version info of the PyFluent package.
Build timestamp and commit hash are added to this variable during packaging.
"""

import importlib as _importlib  # noqa: E402
import os as _os  # noqa: E402
import sys as _sys  # noqa: E402
from typing import TYPE_CHECKING as _TYPE_CHECKING  # noqa: E402
import warnings as _warnings  # noqa: E402

_THIS_DIRNAME = _os.path.dirname(__file__)
_README_FILE = _os.path.normpath(_os.path.join(_THIS_DIRNAME, "docs", "README.rst"))

if _os.path.exists(_README_FILE):
    with open(_README_FILE, encoding="utf8") as f:
        __doc__ = f.read()

# ──────────────────────────────────────────────────────────────────────────────
# Backward-compat module path aliases. These targets are all cheap (stdlib-only
# or already-imported) so registering them eagerly costs nothing; unlike
# `session.file`/`file_reader`/`local_parametric_study`, which pull in numpy,
# `ansys.units` (and therefore pandas) transitively, so those old flat-path
# aliases are no longer provided (see issue #4924 - avoid eager imports).
# `ansys.fluent.core.generated.solver.settings_builtin` imports from
# `ansys.fluent.core.exceptions`, so that alias must exist before `solver` is
# ever touched, even lazily.
# ──────────────────────────────────────────────────────────────────────────────
from ansys.fluent.core.diagnostics import exceptions as _exceptions  # noqa: E402
from ansys.fluent.core.diagnostics import journaling as _journaling  # noqa: E402
from ansys.fluent.core.diagnostics import logger as _logger  # noqa: E402

_sys.modules["ansys.fluent.core.exceptions"] = _exceptions
_sys.modules["ansys.fluent.core.journaling"] = _journaling
_sys.modules["ansys.fluent.core.logger"] = _logger

# ──────────────────────────────────────────────────────────────────────────────
# Static type-checking / IDE support only. Nothing in this block executes at
# runtime; the PEP 562 __getattr__ further below performs the actual lazy
# import. This keeps autocomplete and static analysis (mypy/pyright/Pylance)
# fully working while avoiding the runtime cost of eagerly importing every
# submodule.
# ──────────────────────────────────────────────────────────────────────────────
if _TYPE_CHECKING:
    from ansys.fluent.core._get_build_details import (
        get_build_version as get_build_version,
    )
    from ansys.fluent.core._get_build_details import (
        get_build_version_string as get_build_version_string,
    )
    from ansys.fluent.core.context_manager import using as using
    from ansys.fluent.core.diagnostics.search import search as search
    from ansys.fluent.core.execution.launcher.launch_options import (
        Dimension as Dimension,
    )
    from ansys.fluent.core.execution.launcher.launch_options import (
        FluentLinuxGraphicsDriver as FluentLinuxGraphicsDriver,
    )
    from ansys.fluent.core.execution.launcher.launch_options import (
        FluentMode as FluentMode,
    )
    from ansys.fluent.core.execution.launcher.launch_options import (
        FluentWindowsGraphicsDriver as FluentWindowsGraphicsDriver,
    )
    from ansys.fluent.core.execution.launcher.launch_options import (
        Precision as Precision,
    )
    from ansys.fluent.core.execution.launcher.launch_options import UIMode as UIMode
    from ansys.fluent.core.execution.launcher.launcher import (
        connect_to_fluent as connect_to_fluent,
    )
    from ansys.fluent.core.execution.launcher.launcher import (
        create_launcher as create_launcher,
    )
    from ansys.fluent.core.execution.launcher.launcher import (
        launch_fluent as launch_fluent,
    )
    from ansys.fluent.core.fields.field_data import (
        PathlinesFieldDataRequest as PathlinesFieldDataRequest,
    )
    from ansys.fluent.core.fields.field_data import (
        ScalarFieldDataRequest as ScalarFieldDataRequest,
    )
    from ansys.fluent.core.fields.field_data import (
        SurfaceFieldDataRequest as SurfaceFieldDataRequest,
    )
    from ansys.fluent.core.fields.field_data import (
        VectorFieldDataRequest as VectorFieldDataRequest,
    )
    from ansys.fluent.core.fields.field_data import SurfaceDataType as SurfaceDataType
    from ansys.fluent.core.local_parametric_study import (
        LocalParametricStudy as LocalParametricStudy,
    )
    from ansys.fluent.core.services.batch_ops import BatchOps as BatchOps
    from ansys.fluent.core.services.streaming_services.events_streaming import (
        AboutToInitializeSolutionEventInfo as AboutToInitializeSolutionEventInfo,
    )
    from ansys.fluent.core.services.streaming_services.events_streaming import (
        AboutToLoadCaseEventInfo as AboutToLoadCaseEventInfo,
    )
    from ansys.fluent.core.services.streaming_services.events_streaming import (
        AboutToLoadDataEventInfo as AboutToLoadDataEventInfo,
    )
    from ansys.fluent.core.services.streaming_services.events_streaming import (
        CalculationsEndedEventInfo as CalculationsEndedEventInfo,
    )
    from ansys.fluent.core.services.streaming_services.events_streaming import (
        CalculationsPausedEventInfo as CalculationsPausedEventInfo,
    )
    from ansys.fluent.core.services.streaming_services.events_streaming import (
        CalculationsResumedEventInfo as CalculationsResumedEventInfo,
    )
    from ansys.fluent.core.services.streaming_services.events_streaming import (
        CalculationsStartedEventInfo as CalculationsStartedEventInfo,
    )
    from ansys.fluent.core.services.streaming_services.events_streaming import (
        CaseLoadedEventInfo as CaseLoadedEventInfo,
    )
    from ansys.fluent.core.services.streaming_services.events_streaming import (
        DataLoadedEventInfo as DataLoadedEventInfo,
    )
    from ansys.fluent.core.services.streaming_services.events_streaming import (
        Event as Event,
    )
    from ansys.fluent.core.services.streaming_services.events_streaming import (
        EventsManager as EventsManager,
    )
    from ansys.fluent.core.services.streaming_services.events_streaming import (
        FatalErrorEventInfo as FatalErrorEventInfo,
    )
    from ansys.fluent.core.services.streaming_services.events_streaming import (
        IterationEndedEventInfo as IterationEndedEventInfo,
    )
    from ansys.fluent.core.services.streaming_services.events_streaming import (
        MeshingEvent as MeshingEvent,
    )
    from ansys.fluent.core.services.streaming_services.events_streaming import (
        ProgressUpdatedEventInfo as ProgressUpdatedEventInfo,
    )
    from ansys.fluent.core.services.streaming_services.events_streaming import (
        ReportDefinitionUpdatedEventInfo as ReportDefinitionUpdatedEventInfo,
    )
    from ansys.fluent.core.services.streaming_services.events_streaming import (
        ReportPlotSetUpdatedEventInfo as ReportPlotSetUpdatedEventInfo,
    )
    from ansys.fluent.core.services.streaming_services.events_streaming import (
        ResidualPlotUpdatedEventInfo as ResidualPlotUpdatedEventInfo,
    )
    from ansys.fluent.core.services.streaming_services.events_streaming import (
        SettingsClearedEventInfo as SettingsClearedEventInfo,
    )
    from ansys.fluent.core.services.streaming_services.events_streaming import (
        SolutionInitializedEventInfo as SolutionInitializedEventInfo,
    )
    from ansys.fluent.core.services.streaming_services.events_streaming import (
        SolutionPausedEventInfo as SolutionPausedEventInfo,
    )
    from ansys.fluent.core.services.streaming_services.events_streaming import (
        SolverEvent as SolverEvent,
    )
    from ansys.fluent.core.services.streaming_services.events_streaming import (
        SolverTimeEstimateUpdatedEventInfo as SolverTimeEstimateUpdatedEventInfo,
    )
    from ansys.fluent.core.services.streaming_services.events_streaming import (
        TimestepEndedEventInfo as TimestepEndedEventInfo,
    )
    from ansys.fluent.core.services.streaming_services.events_streaming import (
        TimestepStartedEventInfo as TimestepStartedEventInfo,
    )
    from ansys.fluent.core.session import Meshing as Meshing
    from ansys.fluent.core.session import PrePost as PrePost
    from ansys.fluent.core.session import PureMeshing as PureMeshing
    from ansys.fluent.core.session import Solver as Solver
    from ansys.fluent.core.session import SolverAero as SolverAero
    from ansys.fluent.core.session import SolverIcing as SolverIcing
    from ansys.fluent.core.session.session import BaseSession as BaseSession
    from ansys.fluent.core.solver.flobject import ExposureLevel as ExposureLevel
    from ansys.fluent.core.utils import get_user_data_dir as get_user_data_dir
    from ansys.fluent.core.utils import load_module as load_module
    from ansys.fluent.core.utils.fluent_version import FluentVersion as FluentVersion
    from ansys.fluent.core.utils.setup_for_fluent import (
        setup_for_fluent as setup_for_fluent,
    )

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
# Lazy imports via PEP 562 __getattr__ / __dir__
# Maps public name -> (module_path, attribute_name)
# ──────────────────────────────────────────────────────────────────────────────
_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    # fields.field_data
    "PathlinesFieldDataRequest": (
        "ansys.fluent.core.fields.field_data",
        "PathlinesFieldDataRequest",
    ),
    "ScalarFieldDataRequest": (
        "ansys.fluent.core.fields.field_data",
        "ScalarFieldDataRequest",
    ),
    "SurfaceDataType": (
        "ansys.fluent.core.fields.field_data",
        "SurfaceDataType",
    ),
    "SurfaceFieldDataRequest": (
        "ansys.fluent.core.fields.field_data",
        "SurfaceFieldDataRequest",
    ),
    "VectorFieldDataRequest": (
        "ansys.fluent.core.fields.field_data",
        "VectorFieldDataRequest",
    ),
    # _get_build_details
    "get_build_version": (
        "ansys.fluent.core._get_build_details",
        "get_build_version",
    ),
    "get_build_version_string": (
        "ansys.fluent.core._get_build_details",
        "get_build_version_string",
    ),
    # execution.launcher.launch_options
    "FluentMode": (
        "ansys.fluent.core.execution.launcher.launch_options",
        "FluentMode",
    ),
    "UIMode": (
        "ansys.fluent.core.execution.launcher.launch_options",
        "UIMode",
    ),
    "Dimension": (
        "ansys.fluent.core.execution.launcher.launch_options",
        "Dimension",
    ),
    "Precision": (
        "ansys.fluent.core.execution.launcher.launch_options",
        "Precision",
    ),
    "FluentWindowsGraphicsDriver": (
        "ansys.fluent.core.execution.launcher.launch_options",
        "FluentWindowsGraphicsDriver",
    ),
    "FluentLinuxGraphicsDriver": (
        "ansys.fluent.core.execution.launcher.launch_options",
        "FluentLinuxGraphicsDriver",
    ),
    # execution.launcher.launcher
    "create_launcher": (
        "ansys.fluent.core.execution.launcher.launcher",
        "create_launcher",
    ),
    "launch_fluent": (
        "ansys.fluent.core.execution.launcher.launcher",
        "launch_fluent",
    ),
    "connect_to_fluent": (
        "ansys.fluent.core.execution.launcher.launcher",
        "connect_to_fluent",
    ),
    # local_parametric_study
    "LocalParametricStudy": (
        "ansys.fluent.core.local_parametric_study",
        "LocalParametricStudy",
    ),
    # diagnostics.search
    "search": (
        "ansys.fluent.core.diagnostics.search",
        "search",
    ),
    # services.batch_ops
    "BatchOps": (
        "ansys.fluent.core.services.batch_ops",
        "BatchOps",
    ),
    # session.session
    "BaseSession": (
        "ansys.fluent.core.session.session",
        "BaseSession",
    ),
    # Note: "Fluent" is handled as a special case in __getattr__ below (it is
    # dynamically subclassed from BaseSession), so it is not listed here.
    # session
    "Meshing": (
        "ansys.fluent.core.session",
        "Meshing",
    ),
    "PureMeshing": (
        "ansys.fluent.core.session",
        "PureMeshing",
    ),
    "PrePost": (
        "ansys.fluent.core.session",
        "PrePost",
    ),
    "Solver": (
        "ansys.fluent.core.session",
        "Solver",
    ),
    "SolverAero": (
        "ansys.fluent.core.session",
        "SolverAero",
    ),
    "SolverIcing": (
        "ansys.fluent.core.session",
        "SolverIcing",
    ),
    # solver.flobject
    "ExposureLevel": (
        "ansys.fluent.core.solver.flobject",
        "ExposureLevel",
    ),
    # services.streaming_services.events_streaming
    "EventsManager": (
        "ansys.fluent.core.services.streaming_services.events_streaming",
        "EventsManager",
    ),
    "Event": (
        "ansys.fluent.core.services.streaming_services.events_streaming",
        "Event",
    ),
    "SolverEvent": (
        "ansys.fluent.core.services.streaming_services.events_streaming",
        "SolverEvent",
    ),
    "MeshingEvent": (
        "ansys.fluent.core.services.streaming_services.events_streaming",
        "MeshingEvent",
    ),
    "TimestepStartedEventInfo": (
        "ansys.fluent.core.services.streaming_services.events_streaming",
        "TimestepStartedEventInfo",
    ),
    "TimestepEndedEventInfo": (
        "ansys.fluent.core.services.streaming_services.events_streaming",
        "TimestepEndedEventInfo",
    ),
    "IterationEndedEventInfo": (
        "ansys.fluent.core.services.streaming_services.events_streaming",
        "IterationEndedEventInfo",
    ),
    "CalculationsStartedEventInfo": (
        "ansys.fluent.core.services.streaming_services.events_streaming",
        "CalculationsStartedEventInfo",
    ),
    "CalculationsEndedEventInfo": (
        "ansys.fluent.core.services.streaming_services.events_streaming",
        "CalculationsEndedEventInfo",
    ),
    "CalculationsPausedEventInfo": (
        "ansys.fluent.core.services.streaming_services.events_streaming",
        "CalculationsPausedEventInfo",
    ),
    "CalculationsResumedEventInfo": (
        "ansys.fluent.core.services.streaming_services.events_streaming",
        "CalculationsResumedEventInfo",
    ),
    "AboutToLoadCaseEventInfo": (
        "ansys.fluent.core.services.streaming_services.events_streaming",
        "AboutToLoadCaseEventInfo",
    ),
    "CaseLoadedEventInfo": (
        "ansys.fluent.core.services.streaming_services.events_streaming",
        "CaseLoadedEventInfo",
    ),
    "AboutToLoadDataEventInfo": (
        "ansys.fluent.core.services.streaming_services.events_streaming",
        "AboutToLoadDataEventInfo",
    ),
    "DataLoadedEventInfo": (
        "ansys.fluent.core.services.streaming_services.events_streaming",
        "DataLoadedEventInfo",
    ),
    "AboutToInitializeSolutionEventInfo": (
        "ansys.fluent.core.services.streaming_services.events_streaming",
        "AboutToInitializeSolutionEventInfo",
    ),
    "SolutionInitializedEventInfo": (
        "ansys.fluent.core.services.streaming_services.events_streaming",
        "SolutionInitializedEventInfo",
    ),
    "ReportDefinitionUpdatedEventInfo": (
        "ansys.fluent.core.services.streaming_services.events_streaming",
        "ReportDefinitionUpdatedEventInfo",
    ),
    "ReportPlotSetUpdatedEventInfo": (
        "ansys.fluent.core.services.streaming_services.events_streaming",
        "ReportPlotSetUpdatedEventInfo",
    ),
    "ResidualPlotUpdatedEventInfo": (
        "ansys.fluent.core.services.streaming_services.events_streaming",
        "ResidualPlotUpdatedEventInfo",
    ),
    "SettingsClearedEventInfo": (
        "ansys.fluent.core.services.streaming_services.events_streaming",
        "SettingsClearedEventInfo",
    ),
    "SolutionPausedEventInfo": (
        "ansys.fluent.core.services.streaming_services.events_streaming",
        "SolutionPausedEventInfo",
    ),
    "ProgressUpdatedEventInfo": (
        "ansys.fluent.core.services.streaming_services.events_streaming",
        "ProgressUpdatedEventInfo",
    ),
    "SolverTimeEstimateUpdatedEventInfo": (
        "ansys.fluent.core.services.streaming_services.events_streaming",
        "SolverTimeEstimateUpdatedEventInfo",
    ),
    "FatalErrorEventInfo": (
        "ansys.fluent.core.services.streaming_services.events_streaming",
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
    # context_manager
    "using": (
        "ansys.fluent.core.context_manager",
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
    "enable",
    "get_default_config",
    "get_logger",
    "is_active",
    "set_console_logging_level",
    "set_global_level",
    "PyFluentDeprecationWarning",
    "PyFluentUserWarning",
    "FluentDevVersionWarning",
    "warning",
    "__version__",
    "version_info",
    # Fluent is constructed dynamically on first access (see __getattr__)
    "Fluent",
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
if not _TYPE_CHECKING:

    def _prime_session_import_order() -> None:
        """Work around a circular import between ``session.session`` and
        ``fluent_connection`` (via ``execution.launcher``). Importing
        ``execution.launcher`` first avoids the cycle; see issue #4924.
        """
        _importlib.import_module("ansys.fluent.core.execution.launcher")

    def __getattr__(name: str):
        """Lazy-load public symbols on first access; also handles deprecated names."""
        # 1. Fluent is dynamically subclassed from BaseSession on first access,
        # since BaseSession itself must stay lazily imported.
        if name == "Fluent":
            _prime_session_import_order()
            from ansys.fluent.core.session.session import BaseSession as _BaseSession

            class Fluent(_BaseSession):
                """Fluent session management.

                This class serves as the primary base class for both meshing and
                solver sessions within PyFluent. It extends the core functionality
                provided by the base session instance.

                Attributes
                ----------
                Inherits all attributes from :class:`~ansys.fluent.core.session.session.BaseSession`.
                """

            globals()["Fluent"] = Fluent  # cache for subsequent access
            return Fluent

        # 2. Lazy imports
        if name in _LAZY_IMPORTS:
            module_path, attr_name = _LAZY_IMPORTS[name]
            if module_path.startswith("ansys.fluent.core.session"):
                _prime_session_import_order()
            module = _importlib.import_module(module_path)
            value = getattr(module, attr_name)
            globals()[name] = value  # cache for subsequent access
            return value

        # 3. Deprecated config variable names
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
    "codegen",
    "context_manager",
    "diagnostics",
    "examples",
    "execution",
    "expressions",
    "fields",
    "file_reader",
    "file_transfer_service",
    "fluent_connection",
    "generated",
    "local_parametric_study",
    "meshing",
    "module_config",
    "rest",
    "rpvars",
    "services",
    "session",
    "solver",
    "system_coupling",
    "ui",
    "utils",
    "workflow",
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
