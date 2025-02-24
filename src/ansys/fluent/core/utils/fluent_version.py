# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Provides a module to get Fluent version."""

from enum import Enum
from functools import total_ordering
import os

import ansys.fluent.core as pyfluent


class AnsysVersionNotFound(RuntimeError):
    """Raised when Ansys version is not found."""

    pass


class ComparisonError(RuntimeError):
    """Raised when a comparison can't be completed."""

    def __init__(self):
        """Initialize ComparisonError."""
        super().__init__(
            "Comparison operations are only supported between two members of 'FluentVersion'."
        )


def get_version(session=None):
    """Get Fluent version."""
    if session is None:
        session = pyfluent.launch_fluent()

    return session.get_fluent_version().value


def get_version_for_file_name(version: str | None = None, session=None):
    """Get Fluent version for file name."""
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

    v252 = "25.2.0"
    v251 = "25.1.0"
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
        return cls(pyfluent.FLUENT_RELEASE_VERSION)

    @classmethod
    def current_dev(cls):
        """Return the version member of the current development version.

        Returns
        -------
        FluentVersion
            FluentVersion member corresponding to the latest development version.
        """
        return cls(pyfluent.FLUENT_DEV_VERSION)

    @property
    def awp_var(self):
        """Get the Fluent version in AWP environment variable format."""
        return f"AWP_ROOT{self.number}"

    @property
    def number(self):
        """Get the Fluent version as a plain integer."""
        return int(self.value.replace(".", "")[:-1])

    @property
    def docker_image_tag(self):
        """Get the Fluent version as a Docker image tag."""
        return f"v{self.value}"

    def __lt__(self, other):
        if isinstance(other, FluentVersion):
            return self.value < other.value
        raise ComparisonError()

    def __repr__(self) -> str:
        """Return a string representation for the Fluent version."""
        return self.value

    def __str__(self) -> str:
        """String output for the Fluent version."""
        return (
            f"Fluent version 20{self.value.split('.')[0]} R{self.value.split('.')[1]}"
        )
