"""Provides a module for enums used in the PyFluent."""

from enum import Enum
from functools import total_ordering
import os
from typing import Optional, Union

from ansys.fluent.core.exceptions import DisallowedValuesError
from ansys.fluent.core.fluent_connection import FluentConnection
import ansys.fluent.core.launcher.error_handler as exceptions
from ansys.fluent.core.launcher.launcher_utils import is_windows
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

    MESHING = (Meshing, "meshing")
    PURE_MESHING = (PureMeshing, "pure-meshing")
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
            ``True`` if the mode is ``FluentMode.MESHING`` or ``FluentMode.PURE_MESHING``,
            ``False`` otherwise.
        """
        return mode in [FluentMode.MESHING, FluentMode.PURE_MESHING]


@total_ordering
class FluentEnum(Enum):
    """Provides the base class for Fluent-related enums.

    Accepts lowercase member names as values and supports comparison operators.
    """

    @classmethod
    def _missing_(cls, value: str):
        for member in cls:
            if member.str_value() == value:
                return member
        raise ValueError(
            f"The specified value '{value}' is not a supported value of {cls.__name__}."
            f""" The supported values are: '{"', '".join(member.str_value() for member in cls)}'."""
        )

    def str_value(self):
        """Returns string value of the enum."""
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


class Dimension(Enum):
    """Geometric dimensionality of the Fluent simulation."""

    TWO = ("2d",)
    THREE = ("3d",)

    @classmethod
    def _missing_(cls, value: int):
        if value is None:
            return cls.THREE
        for member in cls:
            if int(member.value[0][0]) == value:
                return member
        raise ValueError(
            f"The specified value '{value}' is not a supported value of {cls.__name__}."
            f""" The supported values are: {", ".join((member.value[0][0]) for member in cls)}."""
        )


class Precision(FluentEnum):
    """Floating point precision."""

    SINGLE = ("",)
    DOUBLE = ("dp",)


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
        fluent_launch_mode = LaunchMode.CONTAINER
    elif scheduler_options and scheduler_options["scheduler"] == "slurm":
        fluent_launch_mode = LaunchMode.SLURM
    else:
        fluent_launch_mode = LaunchMode.STANDALONE
    return fluent_launch_mode


def _get_graphics_driver(
    graphics_driver: Union[FluentWindowsGraphicsDriver, FluentLinuxGraphicsDriver, str]
):
    if graphics_driver is None:
        graphics_driver = "auto"
    if isinstance(
        graphics_driver, (FluentWindowsGraphicsDriver, FluentLinuxGraphicsDriver)
    ):
        graphics_driver = graphics_driver.str_value()
    graphics_driver = (
        FluentWindowsGraphicsDriver(graphics_driver)
        if is_windows()
        else FluentLinuxGraphicsDriver(graphics_driver)
    )
    return graphics_driver


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
                if fluent_connection._connection_interface.is_solver_mode()
                else "meshing"
            )
        except Exception as ex:
            raise exceptions.InvalidPassword() from ex
    return session_mode.value[0]


def _get_standalone_launch_fluent_version(
    product_version: Union[FluentVersion, str, float, int, None]
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

    # Look for Fluent version in the following order:
    # 1. product_version parameter passed with launch_fluent
    if product_version:
        return FluentVersion(product_version)

    # (DEV) if "PYFLUENT_FLUENT_ROOT" environment variable is defined, we cannot
    # determine the Fluent version, so returning None.
    if os.getenv("PYFLUENT_FLUENT_ROOT"):
        return None

    # 2. the latest ANSYS version from AWP_ROOT environment variables
    return FluentVersion.get_latest_installed()


def _get_ui_mode(
    ui_mode: UIMode,
):
    """Get the graphics driver.

    Parameters
    ----------
    ui_mode: UIMode
        Fluent GUI mode.

    Returns
    -------
    ui_mode: UIMode
        Fluent GUI mode.
    """
    if os.getenv("PYFLUENT_SHOW_SERVER_GUI") == "1":
        ui_mode = UIMode.GUI
    if ui_mode is None:
        # Not using NO_GUI in windows as it opens a new cmd or
        # shows Fluent output in the current cmd if start <launch_string> is not used
        ui_mode = UIMode.HIDDEN_GUI if is_windows() else UIMode.NO_GUI
    if isinstance(ui_mode, str):
        ui_mode = UIMode(ui_mode)
    return ui_mode


def _validate_gpu(gpu: Union[bool, list], dimension: int):
    """Raise an exception if the GPU Solver is unsupported.

    Parameters
    ----------
    gpu : bool or list, optional
        This option will start Fluent with the GPU Solver.
    dimension : int, optional
        Geometric dimensionality of the Fluent simulation.
    """
    if Dimension(dimension) == Dimension.TWO and gpu:
        raise exceptions.GPUSolverSupportError()


def _get_argvals_and_session(argvals):
    _validate_gpu(argvals["gpu"], argvals["dimension"])
    argvals["graphics_driver"] = _get_graphics_driver(argvals["graphics_driver"])
    argvals["mode"] = _get_mode(argvals["mode"])
    del argvals["self"]
    new_session = argvals["mode"].value[0]
    return argvals, new_session
