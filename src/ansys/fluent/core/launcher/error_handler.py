"""Provides a module for customized error handling."""

from ansys.fluent.core.exceptions import InvalidArgument
from ansys.fluent.core.launcher import launcher_utils
from ansys.fluent.core.launcher.pyfluent_enums import LaunchMode, UIMode
from ansys.fluent.core.utils.fluent_version import FluentVersion


class InvalidPassword(ValueError):
    """Raised when password is invalid."""

    def __init__(self):
        super().__init__("Provide correct 'password'.")


class GPUSolverSupportError(ValueError):
    """Raised when an unsupported Fluent version is specified."""

    def __init__(self):
        super().__init__("Fluent GPU Solver is only supported for 3D.")


class IpPortNotProvided(ValueError):
    """Raised when IP address and port are not specified."""

    def __init__(self):
        super().__init__("Provide either 'ip' and 'port' or 'server_info_file_name'.")


class UnexpectedKeywordArgument(TypeError):
    """Raised when a valid keyword argument is not specified."""

    pass


class DockerContainerLaunchNotSupported(SystemError):
    """Raised when Docker container launch is not supported."""

    def __init__(self):
        super().__init__("Python Docker SDK is unsupported on this system.")


class LaunchFluentError(Exception):
    """Exception class representing launch errors."""

    def __init__(self, launch_string):
        """__init__ method of LaunchFluentError class."""
        details = "\n" + "Fluent Launch string: " + launch_string
        super().__init__(details)


def _raise_non_gui_exception_in_windows(
    ui_mode: UIMode, product_version: FluentVersion
) -> None:
    """Fluent user interface mode lower than ``UIMode.HIDDEN_GUI`` is not supported in
    Windows in Fluent versions earlier than 2024 R1."""
    if (
        launcher_utils.is_windows()
        and ui_mode < UIMode.HIDDEN_GUI
        and product_version < FluentVersion.v241
    ):
        raise InvalidArgument(
            f"'{ui_mode}' supported in Windows only for Fluent version 24.1 or later."
        )


def _process_kwargs(kwargs):
    """Verify whether keyword arguments are valid or not.

    Parameters
    ----------
    kwargs: Any
        Keyword arguments.

    Raises
    ------
    UnexpectedKeywordArgument
        If an unexpected keyword argument is provided.
    """
    if kwargs:
        if "meshing_mode" in kwargs:
            raise UnexpectedKeywordArgument(
                "Use 'launch_fluent(mode='meshing')' to launch Fluent in meshing mode."
            )
        else:
            raise UnexpectedKeywordArgument(
                f"launch_fluent() got an unexpected keyword argument {next(iter(kwargs))}"
            )


def _process_invalid_args(dry_run, fluent_launch_mode, argvals):
    """Get invalid arguments.

    Parameters
    ----------
    dry_run: bool
        Whether to dry run a container start.
         If ``True``, the ``launch_fluent()`` will return the configured ``container_dict``.
    fluent_launch_mode: LaunchMode
        Fluent launch mode.
    argvals: dict
        Local arguments.
    """
    if dry_run and fluent_launch_mode != LaunchMode.CONTAINER:
        launcher_utils.logger.warning(
            "'dry_run' argument for 'launch_fluent' currently is only "
            "supported when starting containers."
        )
    if fluent_launch_mode != LaunchMode.STANDALONE:
        arg_names = [
            "env",
            "cwd",
            "topy",
            "case_file_name",
            "lightweight_mode",
            "journal_file_names",
            "case_data_file_name",
        ]
        invalid_arg_names = list(
            filter(lambda arg_name: argvals[arg_name] is not None, arg_names)
        )
        if len(invalid_arg_names) != 0:
            invalid_str_names = ", ".join(invalid_arg_names)
            launcher_utils.logger.warning(
                f"These specified arguments are only supported when starting "
                f"local standalone Fluent clients: {invalid_str_names}."
            )
