from enum import Enum
from functools import total_ordering
import os
from typing import Optional

import ansys.fluent.core as pyfluent
from ansys.fluent.core._version import fluent_release_version


class AnsysVersionNotFound(RuntimeError):
    """Provides the error when Ansys version is not found."""

    pass


class ComparisonError(RuntimeError):
    """Provides the error when a comparison can't be completed."""

    def __init__(self):
        super().__init__(
            f"Comparison operations are only supported between two members of 'FluentVersion'."
        )


def get_version(session=None):
    if session is None:
        # for CI runs, get the version statically from env var set within CI
        image_tag = os.getenv("FLUENT_IMAGE_TAG")
        if image_tag is not None:
            return image_tag.lstrip("v")
        session = pyfluent.launch_fluent(mode="solver")

    return session.get_fluent_version()


def get_version_for_file_name(version: Optional[str] = None, session=None):
    if version is None:
        version = get_version(session)

    return "".join(version.split(".")[0:2])


@total_ordering
class FluentVersion(Enum):
    """An enumeration over supported Fluent versions.

    Examples
    --------
    FluentVersion("23.2.0") == FluentVersion.v232

    FluentVersion.v232.number == 232

    FluentVersion.v232.awp_var == 'AWP_ROOT232'
    """

    v242 = "24.2.0"
    v241 = "24.1.0"
    v232 = "23.2.0"
    v231 = "23.1.0"
    v222 = "22.2.0"

    @classmethod
    def _missing_(cls, version):
        if isinstance(version, (int, float, str)):
            version = str(version)
            if len(version) == 3:
                version = version[:2] + "." + version[2:]
            version += ".0"
            for member in cls:
                if version == member.value:
                    return member
        raise AnsysVersionNotFound(
            f"The specified version '{version[:-2]}' is not supported."
            + " Supported versions are: "
            + ", ".join([member.value for member in cls][::-1])
        )

    @classmethod
    def get_latest_installed(cls):
        """Return the version member corresponding to the most recent, available ANSYS
        installation.

        Returns
        -------
        FluentVersion
            FluentVersion member corresponding to the newest Fluent version.

        Raises
        ------
        AnsysVersionNotFound
            If an Ansys version cannot be found.
        """
        for member in cls:
            if member.awp_var in os.environ:
                return member

        raise AnsysVersionNotFound(
            "Verify the value of the 'AWP_ROOT' environment variable."
        )

    @classmethod
    def current_release(cls):
        """Return the version member of the current release.

        Returns
        -------
        FluentVersion
            FluentVersion member corresponding to the latest release.
        """
        return cls(fluent_release_version)

    @property
    def awp_var(self):
        """Get the Fluent version in AWP environment variable format."""
        return f"AWP_ROOT{self.number}"

    @property
    def number(self):
        """Get the Fluent version as a plain integer."""
        return int(self.value.replace(".", "")[:-1])

    def __lt__(self, other):
        if isinstance(other, FluentVersion):
            return self.value < other.value
        raise ComparisonError()
