"""A package providing Fluent's Solver and Meshing capabilities in Python."""

import os

import appdirs

from ansys.fluent.core._version import __version__  # noqa: F401
from ansys.fluent.core.launcher.launcher import launch_fluent  # noqa: F401
from ansys.fluent.core.session import Session
from ansys.fluent.core.utils.logging import LOG

try:
    from ansys.fluent.core.meshing import tui as meshing_tui
    from ansys.fluent.core.solver import tui as solver_tui

    Session.MeshingTui.register_module(meshing_tui)
    Session.SolverTui.register_module(solver_tui)
except ImportError:
    pass

_VERSION_INFO = None
"""Global variable indicating the version of the PyFluent package - Empty by default"""


def version_info():
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


def set_log_level(level):
    """Set logging level.

    Parameters
    ----------
    level : Any
        Any of the logging level (CRITICAL, ERROR, WARNING, INFO, DEBUG)
        in string or enum format
    """
    LOG.set_level(level)


def enable_logging_to_stdout():
    """Enable logging to stdout."""
    LOG.enable_logging_to_stdout()


def disable_logging_to_stdout():
    """Disable logging to stdout."""
    LOG.disable_logging_to_stdout()


def enable_logging_to_file(filepath: str = None):
    """Enable logging to file.

    Parameters
    ----------
    filepath : str, optional
        filapath, a default filepath will be chosen if filepath is not
        passed
    """
    LOG.enable_logging_to_file(filepath)


def disable_logging_to_file():
    """Disable logging to file."""
    LOG.disable_logging_to_file()


# Setup data directory
try:
    USER_DATA_PATH = appdirs.user_data_dir("ansys_fluent_core")
    if not os.path.exists(USER_DATA_PATH):
        os.makedirs(USER_DATA_PATH)

    EXAMPLES_PATH = os.path.join(USER_DATA_PATH, "examples")
    if not os.path.exists(EXAMPLES_PATH):
        os.makedirs(EXAMPLES_PATH)

except:
    pass
