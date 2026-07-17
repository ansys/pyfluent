# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
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

"""Abstract monitor wrapper."""

from abc import ABC, abstractmethod

import numpy as np


class AbstractSolutionVariableInfo(ABC):
    """Abstract base class for solution variable information."""

    @abstractmethod
    def get_variables_info(
        self, zone_names: list[str], domain_name: str | None = "mixture"
    ):
        """Get SVARs info for zones in the domain.

        Parameters
        ----------
        zone_names : List[str]
            List of zone names.
        domain_name: str, optional
            Domain name.The default is ``mixture``.

        Returns
        -------
        SolutionVariableInfo.SolutionVariables
            Object containing information for SVARs which are common for list of zone names.
        """
        pass

    @abstractmethod
    def get_zones_info(self):
        """Get Zones info.

        Parameters
        ----------
        None

        Returns
        -------
        SolutionVariableInfo.ZonesInfo
            Object containing information for all zones.
        """
        pass


class AbstractSolutionVariableData(ABC):
    """Abstract base class for solution variable data."""

    @abstractmethod
    def get_data(
        self,
        variable_name: str,
        zone_names: list[str],
        domain_name: str | None = "mixture",
    ) -> "AbstractData":
        """Get SVAR data on zones.

        Parameters
        ----------
        variable_name : str
            Name of the solution variable.
        zone_names: List[str]
            Zone names list for solution variable data.
        domain_name : str, optional
            Domain name. The default is ``mixture``.

        Returns
        -------
        AbstractData
            Object containing SVAR data.
        """
        pass

    @abstractmethod
    def set_data(
        self,
        variable_name: str,
        zone_names_to_data: dict[str, np.ndarray],
        domain_name: str | None = "mixture",
    ) -> None:
        """Set SVAR data on zones.

        Parameters
        ----------
        variable_name : str
            Name of the solution variable.
        zone_names_to_data: Dict[str, np.array]
            Dictionary containing zone names for solution variable data.
        domain_name : str, optional
            Domain name. The default is ``mixture``.

        Returns
        -------
        None
        """
        pass


class AbstractData(ABC):
    """Abstract base class for solution variable data."""

    @property
    @abstractmethod
    def domain(self):
        """Domain name."""
        pass

    @property
    @abstractmethod
    def zone_names(self):
        """Zone names."""
        pass

    @property
    @abstractmethod
    def data(self):
        """Solution variable data."""
        pass
