from ansys.fluent.core.exceptions import InvalidArgument
from ansys.fluent.core.launcher.launcher_arguments import _is_windows


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
    if _is_windows() and (
        ("-g" in additional_arg_list) or ("-gu" in additional_arg_list)
    ):
        raise InvalidArgument("Unsupported '-g' and '-gu' on windows platform.")
