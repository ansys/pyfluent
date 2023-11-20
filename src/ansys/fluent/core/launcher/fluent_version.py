"""Provides the Fluent version."""

from enum import Enum
import os

supported_versions = ["24.2.0", "24.1.0", "23.2.0", "23.1.0", "22.2.0"]


def get_current_version() -> str:
    """Return the version string corresponding to the most recent, available ANSYS
    installation.

    The returned value is the string component of one of the members of the
    FluentVersion class.

    Returns
    -------
    str
        Ansys version string

    Raises
    ------
    RuntimeError
        If an Ansys version cannot be found.
    """
    for v in supported_versions:
        if "AWP_ROOT" + "".join(str(v).split("."))[:-1] in os.environ:
            return v

    raise RuntimeError("An Ansys version cannot be found.")


class FluentVersion(Enum):
    """An enumeration over supported Fluent versions."""

    _24R2 = supported_versions[0]
    _24R1 = supported_versions[1]
    _23R2 = supported_versions[2]
    _23R1 = supported_versions[3]
    _22R2 = supported_versions[4]

    current = get_current_version()

    @classmethod
    def _missing_(cls, version):
        if isinstance(version, (float, str)):
            version = str(version) + ".0"
            for v in FluentVersion:
                if version == v.value:
                    return FluentVersion(version)
            else:
                raise RuntimeError(
                    f"The specified version '{version[:-2]}' is not supported."
                    + " Supported versions are: "
                    + ", ".join([ver.value for ver in FluentVersion][::-1])
                )

    def __str__(self):
        return str(self.value)

    def __lt__(self, other):
        if isinstance(other, FluentVersion):
            return self.value < other.value
        return RuntimeError(
            "'<' is only supported between instances of 'FluentVersion' and 'FluentVersion'."
        )

    def __le__(self, other):
        if isinstance(other, FluentVersion):
            return self.value <= other.value
        return RuntimeError(
            "'<=' is only supported between instances of 'FluentVersion' and 'FluentVersion'."
        )

    def __gt__(self, other):
        if isinstance(other, FluentVersion):
            return self.value > other.value
        return RuntimeError(
            "'>' is only supported between instances of 'FluentVersion' and 'FluentVersion'."
        )

    def __ge__(self, other):
        if isinstance(other, FluentVersion):
            return self.value >= other.value
        return RuntimeError(
            "'>=' is only supported between instances of 'FluentVersion' and 'FluentVersion'."
        )
