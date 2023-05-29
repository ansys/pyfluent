"""A package providing Fluent's Solver and Meshing capabilities in Python."""

import logging.config
import os
import pydoc

import appdirs
import yaml

from ansys.fluent.core._version import __version__  # noqa: F401
from ansys.fluent.core.launcher.launcher import (  # noqa: F401
    FluentVersion,
    LaunchMode,
    launch_fluent,
)
from ansys.fluent.core.services.batch_ops import BatchOps  # noqa: F401
from ansys.fluent.core.session import BaseSession as Fluent  # noqa: F401
from ansys.fluent.core.utils import fldoc
from ansys.fluent.core.utils.setup_for_fluent import setup_for_fluent  # noqa: F401

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


def set_global_log_level(level: str | int) -> None:
    """Method changing the levels of all PyFluent loggers.

    Parameters
    ----------
    level : str or int
        Specified logging level to set PyFluent loggers to. See logging levels in
        https://docs.python.org/3/library/logging.html#logging-levels

    Examples
    --------
    >>> import ansys.fluent.core as pyfluent
    >>> pyfluent.set_global_log_level(10)

    or

    >>> pyfluent.set_global_log_level("DEBUG")

    Notes
    -------
    By default loggers are set to WARNING.
    """
    if isinstance(level, str):
        if level.isdigit():
            level = int(level)
    print(f"Setting PyFluent global logging level to {level}.")
    pyfluent_loggers = list_loggers()
    for name in pyfluent_loggers:
        logging.getLogger(name).setLevel(level)


def list_loggers():
    """List with all PyFluent loggers.

    Returns
    -------
    list of str
        Each list element is a PyFluent logger name that can be controlled with logging.getLogger().

    Examples
    --------
    >>> import ansys.fluent.core as pyfluent
    >>> import logging
    >>> pyfluent.list_loggers()
    ['pyfluent_general', 'pyfluent_launcher', 'pyfluent_networking', ...]
    >>> logger = logging.getLogger('pyfluent_networking')
    >>> logger.setLevel("DEBUG")

    Notes
    -------
    By default loggers are set to WARNING.
    """
    logger_dict = logging.root.manager.loggerDict
    pyfluent_loggers = []
    for name in logger_dict:
        if name.startswith("pyfluent"):
            pyfluent_loggers.append(name)
    return pyfluent_loggers


# Configure the logging system
file_path = os.path.abspath(__file__)
file_dir = os.path.dirname(file_path)
yaml_path = os.path.join(file_dir, "logging_config.yaml")

with open(yaml_path, "rt") as f:
    config = yaml.safe_load(f)

logging.config.dictConfig(config)
print(f"PyFluent logging file in {os.path.join(os.getcwd(),'pyfluent.log')}")
env_logging_level = os.getenv("PYFLUENT_LOGGING")
if env_logging_level:
    print(
        "PYFLUENT_LOGGING environment variable found, setting global logging level..."
    )
    set_global_log_level(env_logging_level)

# Setup data directory
USER_DATA_PATH = appdirs.user_data_dir(appname="ansys_fluent_core", appauthor="Ansys")
EXAMPLES_PATH = os.path.join(USER_DATA_PATH, "examples")

BUILDING_GALLERY = False

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
