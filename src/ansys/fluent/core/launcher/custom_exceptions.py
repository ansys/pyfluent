from ansys.fluent.core.exceptions import InvalidArgument
import ansys.fluent.core.launcher.launcher_arguments as launch_args
from ansys.fluent.core.launcher.launcher_utils import FluentUI
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
    """Raised when ip and port are not specified."""

    def __init__(self):
        super().__init__("Provide either 'ip' and 'port' or 'server_info_file_name'.")


class UnexpectedKeywordArgument(TypeError):
    """Raised when a valid keyword argument is not specified."""

    pass


class DockerContainerLaunchNotSupported(SystemError):
    """Raised when docker container launch is not supported."""

    def __init__(self):
        super().__init__("Python Docker SDK is unsupported on this system.")


# pylint: disable=missing-raises-doc
class LaunchFluentError(Exception):
    """Exception class representing launch errors."""

    def __init__(self, launch_string):
        """__init__ method of LaunchFluentError class."""
        details = "\n" + "Fluent Launch string: " + launch_string
        super().__init__(details)


def _raise_exception_g_gu_in_windows_os(additional_arguments: str) -> None:
    """If -g or -gu is passed in Windows OS, the exception should be raised."""
    additional_arg_list = additional_arguments.split()
    if launch_args._is_windows() and (
        ("-g" in additional_arg_list) or ("-gu" in additional_arg_list)
    ):
        raise InvalidArgument("Unsupported '-g' and '-gu' on windows platform.")


def _raise_non_gui_exception_in_windows(
    ui: FluentUI, product_version: FluentVersion
) -> None:
    """Fluent user interface mode lower than ``FluentUI.HIDDEN_GUI`` is not supported in
    Windows in Fluent versions lower than 2024 R1."""
    if (
        launch_args._is_windows()
        and ui < FluentUI.HIDDEN_GUI
        and product_version < FluentVersion.v241
    ):
        raise InvalidArgument(
            f"'{ui}' supported in Windows only for Fluent version 24.1 or later."
        )
