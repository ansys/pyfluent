"""Provides a module for enums used in the PyFluent."""

from enum import Enum
from functools import total_ordering
import os
from typing import Optional, Union

from ansys.fluent.core.exceptions import DisallowedValuesError
from ansys.fluent.core.fluent_connection import FluentConnection
import ansys.fluent.core.launcher.error_handler as exceptions
from ansys.fluent.core.launcher.launcher_utils import check_docker_support
from ansys.fluent.core.session_meshing import Meshing
from ansys.fluent.core.session_pure_meshing import PureMeshing
from ansys.fluent.core.session_solver import Solver
from ansys.fluent.core.session_solver_icing import SolverIcing
from ansys.fluent.core.utils.fluent_version import FluentVersion
import ansys.platform.instancemanagement as pypim


class LaunchMode(Enum):
    """Enumerates over supported Fluent launch modes."""

    STANDALONE = 1
    PIM = 2
    CONTAINER = 3
    SLURM = 4


class FluentMode(Enum):
    """Enumerates over supported Fluent modes."""

    MESHING_MODE = (Meshing, "meshing")
    PURE_MESHING_MODE = (PureMeshing, "pure-meshing")
    SOLVER = (Solver, "solver")
    SOLVER_ICING = (SolverIcing, "solver-icing")

    @staticmethod
    def get_mode(mode: str) -> "FluentMode":
        """Get the FluentMode based on the provided mode string.

        Parameters
        ----------
        mode : str
            Mode

        Returns
        -------
        FluentMode
            Fluent mode.

        Raises
        ------
        DisallowedValuesError
            If an unknown mode is passed.
        """
        allowed_modes = []
        for m in FluentMode:
            allowed_modes.append(m.value[1])
            if mode == m.value[1]:
                return m
        raise DisallowedValuesError("mode", mode, allowed_modes)

    @staticmethod
    def is_meshing(mode: "FluentMode") -> bool:
        """Check if the current mode is meshing.

        Parameters
        ----------
        mode : FluentMode
            mode

        Returns
        -------
        bool
            ``True`` if the mode is ``FluentMode.MESHING_MODE`` or ``FluentMode.PURE_MESHING_MODE``,
            ``False`` otherwise.
        """
        return mode in [FluentMode.MESHING_MODE, FluentMode.PURE_MESHING_MODE]


@total_ordering
class FluentEnum(Enum):
    """Provides the base class for Fluent-related enums.

    Accepts lowercase member names as values and supports comparison operators.
    """

    @classmethod
    def _missing_(cls, value: str):
        for member in cls:
            if str(member) == value:
                return member
        raise ValueError(
            f"The specified value '{value}' is a supported value of {cls.__name__}."
            f""" The supported values are: '{", '".join(str(member) for member in cls)}'."""
        )

    def __str__(self):
        return self.name.lower()

    def __lt__(self, other):
        if not isinstance(other, type(self)):
            raise TypeError(
                f"Cannot compare between {type(self).__name__} and {type(other).__name__}"
            )
        if self == other:
            return False
        for member in type(self):
            if self == member:
                return True
            if other == member:
                return False


class UIMode(FluentEnum):
    """Provides supported user interface mode of Fluent."""

    NO_GUI_OR_GRAPHICS = ("g",)
    NO_GRAPHICS = ("gr",)
    NO_GUI = ("gu",)
    HIDDEN_GUI = ("hidden",)
    GUI = ("",)


class FluentWindowsGraphicsDriver(FluentEnum):
    """Provides supported graphics driver of Fluent in Windows."""

    NULL = ("null",)
    MSW = ("msw",)
    DX11 = ("dx11",)
    OPENGL2 = ("opengl2",)
    OPENGL = ("opengl",)
    AUTO = ("",)


class FluentLinuxGraphicsDriver(FluentEnum):
    """Provides supported graphics driver of Fluent in Linux."""

    NULL = ("null",)
    X11 = ("x11",)
    OPENGL2 = ("opengl2",)
    OPENGL = ("opengl",)
    AUTO = ("",)


def _get_mode(mode: Optional[Union[FluentMode, str, None]] = None):
    """Update the session information."""
    if mode is None:
        mode = FluentMode.SOLVER

    if isinstance(mode, str):
        mode = FluentMode.get_mode(mode)

    return mode


def _get_running_session_mode(
    fluent_connection: FluentConnection, mode: Optional[FluentMode] = None
):
    """Get the mode of the running session if the mode has not been explicitly given."""
    if mode:
        session_mode = mode
    else:
        try:
            session_mode = FluentMode.get_mode(
                "solver"
                if fluent_connection.scheme_eval.scheme_eval("(cx-solver-mode?)")
                else "meshing"
            )
        except Exception as ex:
            raise exceptions.InvalidPassword() from ex
    return session_mode.value[0]


def _get_fluent_launch_mode(start_container, container_dict, scheduler_options):
    """Get the Fluent launch mode.

    Parameters
    ----------
    start_container: bool
        Whether to launch a Fluent Docker container image.
    container_dict: dict
        Dictionary for Fluent Docker container configuration.

    Returns
    -------
    fluent_launch_mode: LaunchMode
        Fluent launch mode.
    """
    if pypim.is_configured():
        fluent_launch_mode = LaunchMode.PIM
    elif start_container is True or (
        start_container is None
        and (container_dict or os.getenv("PYFLUENT_LAUNCH_CONTAINER") == "1")
    ):
        if check_docker_support():
            fluent_launch_mode = LaunchMode.CONTAINER
        else:
            raise exceptions.DockerContainerLaunchNotSupported()
    elif scheduler_options and scheduler_options["scheduler"] == "slurm":
        fluent_launch_mode = LaunchMode.SLURM
    else:
        fluent_launch_mode = LaunchMode.STANDALONE
    return fluent_launch_mode


def _get_standalone_launch_fluent_version(
    product_version: Union[FluentVersion, str, None]
) -> Optional[FluentVersion]:
    """Determine the Fluent version during the execution of the ``launch_fluent()``
    method in standalone mode.

    The search for the version is performed in this order:

    1. The ``product_version`` parameter passed with the ``launch_fluent`` method.
    2. The latest Ansys version from ``AWP_ROOTnnn``` environment variables.

    Returns
    -------
    FluentVersion, optional
        Fluent version or ``None``
    """

    # (DEV) if "PYFLUENT_FLUENT_ROOT" environment variable is defined, we cannot
    # determine the Fluent version, so returning None.
    if os.getenv("PYFLUENT_FLUENT_ROOT"):
        return None

    # Look for Fluent version in the following order:
    # 1. product_version parameter passed with launch_fluent
    if product_version:
        return FluentVersion(product_version)

    # 2. the latest ANSYS version from AWP_ROOT environment variables
    return FluentVersion.get_latest_installed()
