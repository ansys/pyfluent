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

from collections.abc import Set
from enum import Enum
from functools import total_ordering
import os
from pathlib import Path
import platform
from typing import Any

import ansys.fluent.core as pyfluent


class AnsysVersionNotFound(RuntimeError):
    """Raised when Ansys version is not found."""

    def __init__(self, version: Any):
        """Initialize VersionNotFound.

        Parameters
        ----------
        version : str
            Version that was not found.
        """
        super().__init__(
            f"The specified version '{version}' is not supported."
            + " Supported versions are: "
            + ", ".join([member.value for member in FluentVersion][::-1])
        )


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

    v261 = "26.1.0"
    v252 = "25.2.0"
    v251 = "25.1.0"
    v242 = "24.2.0"
    v241 = "24.1.0"
    v232 = "23.2.0"
    v231 = "23.1.0"
    v222 = "22.2.0"

    @classmethod
    def _missing_(cls, version: Any):
        if isinstance(version, (int, float, str)):
            version = str(version)
            if len(version) == 3:
                version = version[:2] + "." + version[2:]
            version += ".0"
            for member in cls:
                if version == member.value:
                    return member

        raise AnsysVersionNotFound(version[:-2])

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
        FileNotFoundError
            If an Ansys version cannot be found.
        """
        for member in cls:
            if member.awp_var in os.environ and member.get_fluent_exe_path().exists():
                return member

        raise FileNotFoundError(
            "Unable to locate a compatible Ansys Fluent installation. "
            "Ensure that an environment variable like 'AWP_ROOT242' or 'AWP_ROOT251' "
            "points to a supported Ansys version, and that Fluent is included in the installation."
        )

    def get_fluent_exe_path(self) -> Path:
        """Get the path for the Fluent executable file.

        Returns
        -------
        Path
            Fluent executable path.
        """
        awp_root = os.environ[self.awp_var]
        fluent_root = Path(awp_root) / "fluent"
        return (
            fluent_root / "ntbin" / "win64" / "fluent.exe"
            if platform.system() == "Windows"
            else fluent_root / "bin" / "fluent"
        )

    @classmethod
    def current_release(cls):
        """Return the version member of the current release.

        Returns
        -------
        FluentVersion
            FluentVersion member corresponding to the latest release.
        """
        return cls(pyfluent.config.fluent_release_version)

    @classmethod
    def current_dev(cls):
        """Return the version member of the current development version.

        Returns
        -------
        FluentVersion
            FluentVersion member corresponding to the latest development version.
        """
        return cls(pyfluent.config.fluent_dev_version)

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
        return f"v{self.value.rsplit('.', 1)[0]}.latest"

    def __lt__(self, other):
        if isinstance(other, FluentVersion):
            return self.value < other.value
        raise ComparisonError()

    def __repr__(self) -> str:
        """Return a string representation for the Fluent version."""
        return self.value

    def __str__(self) -> str:
        """String output for the Fluent version."""
        return f"Ansys Fluent 20{self.value.split('.')[0]} R{self.value.split('.')[1]}"


class FluentVersionSet(Set[FluentVersion]):
    """A set of Fluent versions defined by a predicate."""

    def __init__(self, predicate):
        """Initialize the FluentVersionSet with a predicate."""
        self._predicate = predicate
        self._versions = tuple(
            v for v in reversed(FluentVersion) if self._predicate(v)
        )  # precompute versions for efficiency

    def __contains__(self, version: FluentVersion) -> bool:
        """Check if the version is in the set."""
        return self._predicate(version)

    def __iter__(self):
        """Iterate over all Fluent versions."""
        yield from self._versions

    def __len__(self) -> int:
        """Return the number of versions in the set."""
        return len(self._versions)

    def __eq__(self, other) -> bool:
        """Check equality with another FluentVersionSet."""
        if isinstance(other, FluentVersionSet):
            if len(self) != len(other):
                return False
            return all(v in other for v in self)
        return False

    def __lt__(self, other: "FluentVersionSet") -> bool:
        """Compare two FluentVersionSets."""
        if not isinstance(other, FluentVersionSet):
            raise TypeError("Can only compare with another FluentVersionSet.")
        return all(v in other for v in self) and len(self) < len(other)

    def __le__(self, other: "FluentVersionSet") -> bool:
        """Check if this FluentVersionSet is a subset of another."""
        if not isinstance(other, FluentVersionSet):
            raise TypeError("Can only compare with another FluentVersionSet.")
        return all(v in other for v in self)

    def __gt__(self, other: "FluentVersionSet") -> bool:
        """Check if this FluentVersionSet is a superset of another."""
        if not isinstance(other, FluentVersionSet):
            raise TypeError("Can only compare with another FluentVersionSet.")
        return all(v in self for v in other) and len(self) > len(other)

    def __ge__(self, other: "FluentVersionSet") -> bool:
        """Check if this FluentVersionSet is a superset or equal to another."""
        if not isinstance(other, FluentVersionSet):
            raise TypeError("Can only compare with another FluentVersionSet.")
        return all(v in self for v in other)

    def __and__(self, other: "FluentVersionSet") -> "FluentVersionSet":
        """Return the intersection of two FluentVersionSets."""
        if not isinstance(other, FluentVersionSet):
            raise TypeError("Can only intersect with another FluentVersionSet.")
        return FluentVersionSet(lambda v: self._predicate(v) and other._predicate(v))

    def __or__(self, other):
        """Return the union of two FluentVersionSets."""
        if not isinstance(other, FluentVersionSet):
            raise TypeError("Can only union with another FluentVersionSet.")
        return FluentVersionSet(lambda v: self._predicate(v) or other._predicate(v))

    def __sub__(self, other):
        """Return the difference of two FluentVersionSets."""
        if not isinstance(other, FluentVersionSet):
            raise TypeError("Can only subtract another FluentVersionSet.")
        return FluentVersionSet(
            lambda v: self._predicate(v) and not other._predicate(v)
        )

    def __hash__(self):
        return hash(self._versions)


def all_versions() -> FluentVersionSet:
    """
    Create a FluentVersionSet that includes all supported Fluent versions.

    Returns
    -------
    FluentVersionSet
        A set containing all Fluent versions.
    """
    return FluentVersionSet(lambda v: True)


def since(version: FluentVersion) -> FluentVersionSet:
    """
    Create a FluentVersionSet that includes all versions since the specified version.

    Parameters
    ----------
    version : FluentVersion
        The version since which the set should include versions.

    Returns
    -------
    FluentVersionSet
    """
    return FluentVersionSet(lambda v: v >= version)


def until(version: FluentVersion) -> FluentVersionSet:
    """
    Create a FluentVersionSet that includes all versions until the specified version.

    Parameters
    ----------
    version : FluentVersion
        The version until which the set should include versions.

    Returns
    -------
    FluentVersionSet
    """
    return FluentVersionSet(lambda v: v < version)


def only_at(version: FluentVersion) -> FluentVersionSet:
    """
    Create a FluentVersionSet that includes only the specified version.

    Parameters
    ----------
    version : FluentVersion
        The version to include in the set.

    Returns
    -------
    FluentVersionSet
    """
    return FluentVersionSet(lambda v: v == version)


def except_for(version: FluentVersion) -> FluentVersionSet:
    """
    Create a FluentVersionSet that includes all versions except the specified version.

    Parameters
    ----------
    version : FluentVersion
        The version to exclude from the set.

    Returns
    -------
    FluentVersionSet
    """
    return FluentVersionSet(lambda v: v != version)


def between(start: FluentVersion, end: FluentVersion) -> FluentVersionSet:
    """
    Create a FluentVersionSet that includes all versions between the specified start (inclusive) and end (exclusive) versions.

    Parameters
    ----------
    start : FluentVersion
        The starting version of the range, inclusive.
    end : FluentVersion
        The ending version of the range, exclusive.

    Returns
    -------
    FluentVersionSet
    """
    return FluentVersionSet(lambda v: start <= v < end)
