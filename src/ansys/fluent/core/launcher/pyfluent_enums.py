"""Provides a module for enums used in the PyFluent."""

from enum import Enum
import os

from ansys.fluent.core.exceptions import DisallowedValuesError
from ansys.fluent.core.fluent_connection import FluentConnection
import ansys.fluent.core.launcher.error_handler as exceptions
from ansys.fluent.core.launcher.launcher_utils import is_windows
from ansys.fluent.core.session_meshing import Meshing
from ansys.fluent.core.session_pure_meshing import PureMeshing
from ansys.fluent.core.session_solver import Solver
from ansys.fluent.core.session_solver_aero import SolverAero
from ansys.fluent.core.session_solver_icing import SolverIcing
from ansys.fluent.core.utils.fluent_version import FluentVersion
import ansys.platform.instancemanagement as pypim


class FluentEnum(Enum):
    """Provides the base class for Fluent-related enums.

    Accepts lowercase member names as values and supports comparison operators.
    """

    def _get_enum_map(self):
        return {}

    def get_fluent_value(self):
        """Returns the fluent value of the enum."""
        return self._get_enum_map()[self]

    def _default(self):
        return

    @classmethod
    def _missing_(cls, value: str | int | None):
        if value is None:
            return cls._default(cls)
        for member in cls:
            if member.value == value:
                return member

        def is_int():
            for m in cls:
                return True if isinstance(m.value, int) else False

        msg = ", " if is_int() else "', '"
        msg = (
            f"{msg.join(str(member.value) for member in cls)}"
            if is_int()
            else f"'{msg.join(str(member.value) for member in cls)}'"
        )
        raise DisallowedValuesError(
            f"""The specified value: {repr(value)} """
            f"""is not a supported value of {cls.__name__}."""
            f""" The supported values are: {msg}."""
        )


class LaunchMode(FluentEnum):
    """Enumerates over supported Fluent launch modes."""

    STANDALONE = "standalone"
    PIM = "pim"
    CONTAINER = "container"
    SLURM = "slurm"

    def _get_enum_map(self):
        return {
            self.STANDALONE: 1,
            self.PIM: 2,
            self.CONTAINER: 3,
            self.SLURM: 4,
        }


class FluentMode(FluentEnum):
    """Enumerates over supported Fluent modes."""

    MESHING = "meshing"
    PURE_MESHING = "pure_meshing"
    SOLVER = "solver"
    SOLVER_ICING = "solver_icing"
    SOLVER_AERO = "solver_aero"

    def _default(self):
        return self.SOLVER

    def _get_enum_map(self):
        return {
            self.MESHING: Meshing,
            self.PURE_MESHING: PureMeshing,
            self.SOLVER: Solver,
            self.SOLVER_ICING: SolverIcing,
            self.SOLVER_AERO: SolverAero,
        }

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


class UIMode(FluentEnum):
    """Provides supported user interface mode of Fluent."""

    NO_GUI_OR_GRAPHICS = "no_gui_or_graphics"
    NO_GRAPHICS = "no_graphics"
    NO_GUI = "no_gui"
    HIDDEN_GUI = "hidden_gui"
    GUI = "gui"

    def _default(self):
        # Not using NO_GUI in windows as it opens a new cmd or
        # shows Fluent output in the current cmd if start <launch_string> is not used
        return self.HIDDEN_GUI if is_windows() else self.NO_GUI

    def _get_enum_map(self):
        return {
            self.NO_GUI_OR_GRAPHICS: ("g",),
            self.NO_GRAPHICS: ("gr",),
            self.NO_GUI: ("gu",),
            self.HIDDEN_GUI: ("hidden",),
            self.GUI: ("",),
        }


class Dimension(FluentEnum):
    """Geometric dimensionality of the Fluent simulation."""

    TWO = 2
    THREE = 3

    def _default(self):
        return self.THREE

    def _get_enum_map(self):
        return {
            self.TWO: ("2d",),
            self.THREE: ("3d",),
        }


class Precision(FluentEnum):
    """Floating point precision."""

    SINGLE = "single"
    DOUBLE = "double"

    def _default(self):
        return self.DOUBLE

    def _get_enum_map(self):
        return {
            self.SINGLE: ("",),
            self.DOUBLE: ("dp",),
        }


class FluentWindowsGraphicsDriver(FluentEnum):
    """Provides supported graphics driver of Fluent in Windows."""

    NULL = "null"
    MSW = "msw"
    DX11 = "dx11"
    OPENGL2 = "opengl2"
    OPENGL = "opengl"
    AUTO = "auto"

    def _default(self):
        return self.AUTO

    def _get_enum_map(self):
        return {
            self.NULL: ("null",),
            self.MSW: ("msw",),
            self.DX11: ("dx11",),
            self.OPENGL2: ("opengl2",),
            self.OPENGL: ("opengl",),
            self.AUTO: ("",),
        }


class FluentLinuxGraphicsDriver(FluentEnum):
    """Provides supported graphics driver of Fluent in Linux."""

    NULL = "null"
    X11 = "x11"
    OPENGL2 = "opengl2"
    OPENGL = "opengl"
    AUTO = "auto"

    def _default(self):
        return self.AUTO

    def _get_enum_map(self):
        return {
            self.NULL: ("null",),
            self.X11: ("x11",),
            self.OPENGL2: ("opengl2",),
            self.OPENGL: ("opengl",),
            self.AUTO: ("",),
        }


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
    # Currently, only Slurm scheduler is supported and within SlurmLauncher we check the value of the scheduler
    elif scheduler_options:
        fluent_launch_mode = LaunchMode.SLURM
    else:
        fluent_launch_mode = LaunchMode.STANDALONE
    return fluent_launch_mode


def _get_graphics_driver(
    graphics_driver: (
        FluentWindowsGraphicsDriver | FluentLinuxGraphicsDriver | str | None
    ) = None,
):
    if isinstance(
        graphics_driver, (FluentWindowsGraphicsDriver, FluentLinuxGraphicsDriver)
    ):
        graphics_driver = graphics_driver.value
    graphics_driver = (
        FluentWindowsGraphicsDriver(graphics_driver)
        if is_windows()
        else FluentLinuxGraphicsDriver(graphics_driver)
    )
    return graphics_driver


def _get_running_session_mode(
    fluent_connection: FluentConnection, mode: FluentMode | None = None
):
    """Get the mode of the running session if the mode has not been explicitly given."""
    if mode:
        session_mode = mode
    else:
        try:
            session_mode = fluent_connection._connection_interface.get_mode()
        except Exception as ex:
            raise exceptions.InvalidPassword() from ex
    return session_mode.get_fluent_value()


def _get_standalone_launch_fluent_version(argvals) -> FluentVersion | None:
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
    product_version = argvals.get("product_version")
    if product_version:
        return FluentVersion(product_version)

    # If fluent_path is provided, we cannot determine the Fluent version, so returning None.
    if argvals.get("fluent_path"):
        return None

    # (DEV) if "PYFLUENT_FLUENT_ROOT" environment variable is defined, we cannot
    # determine the Fluent version, so returning None.
    if os.getenv("PYFLUENT_FLUENT_ROOT"):
        return None

    # 2. the latest ANSYS version from AWP_ROOT environment variables
    return FluentVersion.get_latest_installed()


def _validate_gpu(gpu: bool | list, dimension: int):
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
    argvals["mode"] = FluentMode(argvals["mode"])
    del argvals["self"]
    new_session = argvals["mode"].get_fluent_value()
    return argvals, new_session
