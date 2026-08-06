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

"""High-level solution-variable wrappers.

This module owns the business-logic layer on top of the SolutionVariable
gRPC service. The grpc service implementation lives in:

* ``ansys.fluent.core._grpc_services.solution_variable_service`` (v1 proto API)
* ``ansys.fluent.core._grpc_services.solution_variable_service_v0`` (v0 proto API)

The public API is centered around:

* ``SolutionVariableInfo`` for zone and SVAR metadata access.
* ``SolutionVariableData`` for reading and writing SVAR data arrays.
"""

from typing import Any

import numpy as np
import numpy.typing as npt

from ansys.fluent.core.fields.live_field_data import override_help_text
from ansys.fluent.core.services.abstract_solution_variables import (
    AbstractData,
    AbstractSolutionVariableData,
    AbstractSolutionVariableInfo,
)
from ansys.fluent.core.solver.error_message import allowed_name_error_message
from ansys.fluent.core.utils.deprecate import deprecate_arguments
from ansys.fluent.core.variable_strategies import (
    FluentSVarNamingStrategy as naming_strategy,
)

_to_field_name_str = naming_strategy().to_string


class Data(AbstractData):
    """Solution variable data."""

    def __init__(self, domain_name, zone_id_name_map, solution_variable_data):
        """Initialize Data."""
        self._domain_name = domain_name
        self._data = {
            zone_id_name_map[zone_id]: zone_data
            for zone_id, zone_data in solution_variable_data.items()
        }

    @property
    def domain(self):
        """Domain name."""
        return self._domain_name

    @property
    def zone_names(self):
        """Zone names."""
        return list(self._data.keys())

    @property
    def data(self):
        """Solution variable data."""
        return self._data

    def __getitem__(self, name):
        return self._data.get(name, None)


class SolutionVariableInfo(AbstractSolutionVariableInfo):
    """Provide access to Fluent SVARs and Zones information.

    Examples
    --------
    >>> solution_variable_info = solver_session.fields.solution_variable_info
    >>> wall_fluid_info = solution_variable_info.get_variables_info(zone_names=['wall' , "fluid"], domain_name="mixture")
    >>> print(wall_fluid_info.solution_variables)
    >>> ['SV_CENTROID', 'SV_D', 'SV_H', 'SV_K', 'SV_P', 'SV_T', 'SV_U', 'SV_V', 'SV_W']
    >>> solution_variable_info_centroid = wall_fluid_info['SV_CENTROID']
    >>> print(solution_variable_info_centroid)
    >>> name:SV_CENTROID dimension:3 field_type:<class 'numpy.float64'>
    >>> zones_info = solution_variable_info.get_zones_info()
    >>> print(zones_info.zone_names)
    >>> ['fluid', 'wall', 'symmetry', 'pressure-outlet-7', 'velocity-inlet-6', 'velocity-inlet-5', 'default-interior']
    >>> zone_info = zones_info['wall']
    >>> print(zone_info)
    >>> name:wall count: 3630 zone_id:3 zone_type:wall thread_type:Face
    """

    def __init__(
        self,
        service,
    ):
        """Initialize SolutionVariableInfo."""
        self._service = service

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

        return self._service.get_variables_info(
            zone_names=zone_names,
            domain_name=domain_name,
            allowed_zone_names=_AllowedZoneNames(self),
            allowed_domain_names=_AllowedDomainNames(self),
        )

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
        return self._service.get_zones_info()


class InvalidSolutionVariableNameError(ValueError):
    """Exception class for errors in solution variable name."""

    def __init__(self, variable_name: str, allowed_values: list[str]):
        """Initialize InvalidSolutionVariableNameError."""
        super().__init__(
            allowed_name_error_message(
                context="solution variable",
                trial_name=variable_name,
                allowed_values=allowed_values,
            )
        )


class ZoneError(ValueError):
    """Exception class for errors in Zone name."""

    def __init__(self, zone_name: str, allowed_values: list[str]):
        """Initialize ZoneError."""
        self.zone_name = zone_name
        super().__init__(
            allowed_name_error_message(
                context="zone", trial_name=zone_name, allowed_values=allowed_values
            )
        )


class _AllowedNames:
    def is_valid(self, name):
        """Check whether a given name is valid or not."""
        return name in self()


class _AllowedSvarNames:
    def __init__(self, solution_variable_info: SolutionVariableInfo):
        self._solution_variable_info = solution_variable_info

    def __call__(
        self, zone_names: list[str], domain_name: str | None = "mixture"
    ) -> list[str]:
        return self._solution_variable_info.get_variables_info(
            zone_names=zone_names, domain_name=domain_name
        ).solution_variables

    @deprecate_arguments(
        old_args="solution_variable_name",
        new_args="variable_name",
        version="v0.35.1",
    )
    def is_valid(
        self,
        variable_name,
        zone_names: list[str],
        domain_name: str | None = "mixture",
    ):
        """Check whether solution variable name is valid or not."""
        return variable_name in self(zone_names=zone_names, domain_name=domain_name)

    @deprecate_arguments(
        old_args="solution_variable_name",
        new_args="variable_name",
        version="v0.35.1",
    )
    def valid_name(
        self,
        variable_name,
        zone_names: list[str],
        domain_name: str | None = "mixture",
    ):
        """Get a valid solution variable name.

        Raises
        ------
        InvalidSolutionVariableNameError
            If the given solution variable name is invalid.
        """
        variable_name = _to_field_name_str(variable_name)
        if not self.is_valid(
            variable_name, zone_names=zone_names, domain_name=domain_name
        ):
            raise InvalidSolutionVariableNameError(
                variable_name=variable_name,
                allowed_values=self(zone_names=zone_names, domain_name=domain_name),
            )
        return variable_name


class _AllowedZoneNames(_AllowedNames):
    def __init__(self, solution_variable_info: SolutionVariableInfo):
        self._zones_info = solution_variable_info.get_zones_info()

    def __call__(self) -> list[str]:
        return self._zones_info.zone_names

    def valid_name(self, zone_name):
        """Get a valid zone name.

        Raises
        ------
        ZoneError
            If the given zone name is invalid.
        """
        if not self.is_valid(zone_name):
            raise ZoneError(
                zone_name=zone_name,
                allowed_values=self(),
            )
        return self._zones_info[zone_name].zone_id


class _AllowedDomainNames(_AllowedNames):
    def __init__(self, solution_variable_info: SolutionVariableInfo):
        self._zones_info = solution_variable_info.get_zones_info()

    def __call__(self) -> list[str]:
        return self._zones_info.domains

    def valid_name(self, domain_name):
        """Get a valid domain name.

        Raises
        ------
        ZoneError
            If the given domain name is invalid.
        """
        if not self.is_valid(domain_name):
            raise ZoneError(
                domain_name=domain_name,
                allowed_values=self(),
            )
        return self._zones_info.domain_id(domain_name)


class _SvarMethod:
    class _Arg:
        def __init__(self, accessor):
            self._accessor = accessor

        def allowed_values(self):
            """Get allowed values."""
            return sorted(self._accessor())

    def __init__(self, svar_accessor, args_allowed_values_accessors):
        self._svar_accessor = svar_accessor
        for arg_name, accessor in args_allowed_values_accessors.items():
            setattr(self, arg_name, _SvarMethod._Arg(accessor))

    def __call__(self, *args, **kwargs):
        return self._svar_accessor(*args, **kwargs)


class SolutionVariableData(AbstractSolutionVariableData):
    """Provides access to Fluent SVAR data on zones.

    Examples
    --------
    >>> solution_variable_data = solver_session.fields.solution_variable_data
    >>> sv_t_wall_fluid=solver_session.fields.solution_variable_data.get_data(variable_name="SV_T", domain_name="mixture", zone_names=["fluid", "wall"])
    >>> print(sv_t_wall_fluid.domain)
    >>> 'mixture'
    >>> print(sv_t_wall_fluid.zone_names)
    >>> ['fluid', 'wall']
    >>> fluid_temp = sv_t_wall_fluid['fluid']
    >>> print(fluid_temp.size)
    >>> 13852
    >>> print(fluid_temp.dtype)
    >>> float64
    >>> print(fluid_temp)
    >>> array([600., 600., 600., ..., 600., 600., 600.])
    >>> wall_temp_array = solution_variable_data.create_empty_array("SV_T", "wall")
    >>> fluid_temp_array =solution_variable_data.create_empty_array("SV_T", "fluid")
    >>> wall_temp_array[:]= 500
    >>> fluid_temp_array[:]= 600
    >>> zone_names_to_data = {'wall':wall_temp_array, 'fluid':fluid_temp_array}
    >>> solution_variable_data.set_data(variable_name="SV_T", domain_name="mixture", zone_names_to_data=zone_names_to_data)
    """

    def __init__(
        self,
        service,
        solution_variable_info: SolutionVariableInfo,
    ):
        """Initialize SolutionVariableData."""
        self._service = service
        self._solution_variable_info = solution_variable_info

        self.get_data = override_help_text(
            _SvarMethod(
                svar_accessor=self.get_data,
                args_allowed_values_accessors={},
            ),
            SolutionVariableData.get_data,
        )

    def _update_solution_variable_info(self):
        self._allowed_zone_names = _AllowedZoneNames(self._solution_variable_info)

        self._allowed_domain_names = _AllowedDomainNames(self._solution_variable_info)

        self._allowed_solution_variable_names = _AllowedSvarNames(
            self._solution_variable_info
        )

    def create_empty_array(
        self,
        variable_name: str,
        zone_name: str,
        domain_name: str | None = "mixture",
    ) -> npt.NDArray[Any] | None:
        """Get numpy zeros array for the SVAR on a zone.

        This array can be populated  with values to set SVAR data.
        """
        self._update_solution_variable_info()
        variable_name = self._allowed_solution_variable_names.valid_name(
            variable_name,
            [zone_name],
            domain_name,
        )

        zones_info = self._solution_variable_info.get_zones_info()
        if zone_name in zones_info.zone_names:
            solution_variables_info = self._solution_variable_info.get_variables_info(
                zone_names=[zone_name], domain_name=domain_name
            )
            if variable_name in solution_variables_info.solution_variables:
                return np.zeros(
                    zones_info[zone_name].count
                    * solution_variables_info[variable_name].dimension,
                    dtype=solution_variables_info[variable_name].field_type,
                )

    def get_data(
        self,
        variable_name: str,
        zone_names: list[str],
        domain_name: str | None = "mixture",
    ) -> Data:
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
        Data
            Object containing SVAR data.
        """
        self._update_solution_variable_info()
        zone_id_name_map, svar_data = self._service.get_data(
            variable_name=variable_name,
            zone_names=zone_names,
            domain_name=domain_name,
            allowed_solution_variable_names=self._allowed_solution_variable_names,
            allowed_domain_names=self._allowed_domain_names,
            allowed_zone_names=self._allowed_zone_names,
        )
        return Data(
            domain_name,
            zone_id_name_map,
            svar_data,
        )

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
        self._update_solution_variable_info()
        self._service.set_data(
            variable_name=variable_name,
            zone_names_to_data=zone_names_to_data,
            domain_name=domain_name,
            allowed_solution_variable_names=self._allowed_solution_variable_names,
            allowed_domain_names=self._allowed_domain_names,
            allowed_zone_names=self._allowed_zone_names,
        )
