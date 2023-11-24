from enum import Enum
import os
from typing import Optional

import ansys.fluent.core as pyfluent


class AnsysVersionNotFound(RuntimeError):
    """Provides the error when Ansys version is not found."""

    def __init__(self):
        super().__init__("Verify the value of the 'AWP_ROOT' environment variable.")


class ComparisonError(RuntimeError):
    """Provides the error when a comparison can't be completed."""

    def __init__(self, op: str):
        super().__init__(
            f"'{op}' is only supported between two members of 'FluentVersion'."
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


class FluentVersion(Enum):
    """An enumeration over supported Fluent versions.

    Examples
    --------
    FluentVersion(None) == <FluentVersion.default: None>

    FluentVersion("23.2.0") == FluentVersion.v23R2

    int(FluentVersion.v23R2) == 232

    str(FluentVersion.v23R2) == 'AWP_ROOT232'

    FluentVersion.v23R2.value == '23.2.0'
    """

    v24R2 = "24.2.0"
    v24R1 = "24.1.0"
    v23R2 = "23.2.0"
    v23R1 = "23.1.0"
    v22R2 = "22.2.0"
    default = ""

    @classmethod
    def _missing_(cls, version):
        if not version:
            return FluentVersion.default
        if isinstance(version, (int, float, str)):
            version = str(version)
            if len(version) == 3:
                version = version[:2] + "." + version[2:]
            version += ".0"
            for v in FluentVersion:
                if version == v.value:
                    return FluentVersion(version)
            else:
                raise RuntimeError(
                    f"The specified version '{version[:-2]}' is not supported."
                    + " Supported versions are: "
                    + ", ".join([v.value for v in FluentVersion][::-1])
                )

    @classmethod
    def current(cls):
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
        for version in FluentVersion:
            if str(version) in os.environ:
                return version

        raise AnsysVersionNotFound()

    def __int__(self):
        """Return the version as a number (e.g. 232)"""
        if self.value:
            return int(self.value.replace(".", "")[:-1])
        return 0

    def __str__(self):
        """Return the version path (e.g. "AWP_ROOT232")"""
        return str(f"AWP_ROOT{int(self)}")

    def __lt__(self, other):
        if isinstance(other, FluentVersion):
            return self.value < other.value
        return ComparisonError(op="<")

    def __le__(self, other):
        if isinstance(other, FluentVersion):
            return self.value <= other.value
        return ComparisonError(op="<=")

    def __gt__(self, other):
        if isinstance(other, FluentVersion):
            return self.value > other.value
        return ComparisonError(op=">")

    def __ge__(self, other):
        if isinstance(other, FluentVersion):
            return self.value >= other.value
        return ComparisonError(op=">=")
