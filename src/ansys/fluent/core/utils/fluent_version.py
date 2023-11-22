from enum import Enum
import os
from typing import Optional

import ansys.fluent.core as pyfluent


class AnsysVersionNotFound(RuntimeError):
    """Provides the error when Ansys version is not found."""

    def __init__(self):
        super().__init__("Verify the value of the 'AWP_ROOT' environment variable.")


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
    """An enumeration over supported Fluent versions."""

    v24R2 = "24.2.0"
    v24R1 = "24.1.0"
    v23R2 = "23.2.0"
    v23R1 = "23.1.0"
    v22R2 = "22.2.0"

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

    @classmethod
    def current(cls):
        """Return the version member corresponding to the most recent, available ANSYS
        installation.

        Returns
        -------
        FluentVersion
            FluentVersion member corresponding to the Fluent version.

        Raises
        ------
        AnsysVersionNotFound
            If an Ansys version cannot be found.
        """
        for v in FluentVersion:
            if "AWP_ROOT" + "".join(v.value.split("."))[:-1] in os.environ:
                return v

        raise AnsysVersionNotFound()

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
