"""A package providing Fluent's Solver and Meshing capabilities in Python."""

import os
import pydoc

import platformdirs

# Logging has to be set up before importing other PyFluent modules
import ansys.fluent.core.logging as logging

logging.root_config()
logging.configure_env_var()

from ansys.fluent.core._version import __version__  # noqa: F401
from ansys.fluent.core.file_session import (  # noqa: F401
    InvalidFieldName,
    InvalidFieldNamePrefix,
    SurfaceNamesIDsNotProvided,
)
from ansys.fluent.core.filereader.data_file import InvalidFilePath  # noqa: F401
from ansys.fluent.core.fluent_connection import (  # noqa: F401
    PortNotProvided,
    RemoteNotSupported,
    WaitTypeError,
)
from ansys.fluent.core.launcher.fluent_container import (  # noqa: F401
    FluentImageNameTagNotSpecified,
    LicenseServerNotSpecified,
    ServerInfoFileError,
)
from ansys.fluent.core.launcher.launcher import (  # noqa: F401
    AnsysVersionNotFound,
    DockerContainerLaunchNotSupported,
    FluentMode,
    FluentVersion,
    InvalidPassword,
    IpPortNotProvided,
    UnexpectedKeywordArgument,
    connect_to_fluent,
    launch_fluent,
)
from ansys.fluent.core.launcher.watchdog import WatchdogLaunchFailed  # noqa: F401
from ansys.fluent.core.post_objects.post_helper import (  # noqa: F401
    IncompleteISOSurfaceDefinition,
    SurfaceCreationError,
)
from ansys.fluent.core.services.batch_ops import BatchOps  # noqa: F401
from ansys.fluent.core.services.datamodel_se import (  # noqa: F401
    InvalidNamedObject,
    SubscribeEventError,
    UnsubscribeEventError,
)
from ansys.fluent.core.session import BaseSession as Fluent  # noqa: F401
from ansys.fluent.core.solver.flobject import InactiveObjectError  # noqa: F401
from ansys.fluent.core.utils import fldoc
from ansys.fluent.core.utils.search import search  # noqa: F401
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


# Setup data directory
USER_DATA_PATH = platformdirs.user_data_dir(
    appname="ansys_fluent_core", appauthor="Ansys"
)
EXAMPLES_PATH = os.path.join(USER_DATA_PATH, "examples")

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
