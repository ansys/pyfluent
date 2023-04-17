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


file_path = os.path.abspath(__file__)
file_dir = os.path.dirname(file_path)
yaml_path = os.path.join(file_dir, "logging_config.yaml")

# Load the logging configuration from a YAML file
with open(yaml_path, "rt") as f:
    config = yaml.safe_load(f)

# Configure the logging system
logging.config.dictConfig(config)

# Setup data directory
try:
    USER_DATA_PATH = appdirs.user_data_dir("ansys_fluent_core")
    if not os.path.exists(USER_DATA_PATH):
        os.makedirs(USER_DATA_PATH)

    EXAMPLES_PATH = os.path.join(USER_DATA_PATH, "examples")
    if not os.path.exists(EXAMPLES_PATH):
        os.makedirs(EXAMPLES_PATH)

except Exception:
    pass

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
DATAMODEL_USE_NOCOMMANDS_DIFF_STATE = False
