"""Module for accessing Fluent units labels per quantity type.

Example
-------
>>> units = get_si_unit_for_fluent_quantity("pressure")

The following code is employed to translate the source data
into Python data structures:

>>> from ansys.fluent.core.filereader import lispy
>>> from ansys.units import Quantity, Unit
>>> from ansys.units.quantity import get_si_value
>>> import re
>>> from pprint import pprint
>>>
>>> fl_unit_re_subs = {
...     'deg': 'radian',
...     'rad': 'radian',
...     'Ohm': 'ohm'
... }
>>>
>>> fl_unit_subs = {'%': ''}
>>>
>>> def replace_units(match):
...     return fl_unit_re_subs[match.group(0)]
...
>>> def substitute_fl_units_with_py_units(fl_units_dict):
...     subs = {}
...     for k, v in fl_units_dict.items():
...         new_val = re.sub('|'.join(r'\b%s\b' % re.escape(s) for s in fl_unit_re_subs), replace_units, v)
...         if new_val != v:
...             subs[k] = new_val
...         else:
...             new_val = fl_unit_subs.get(v, None)
...             if new_val is not None:
...                 subs[k] = new_val
...     print("Substitutions:")
...     for k, v in subs.items():
...         print(f"'{fl_units_dict[k]}' -> '{v}' for '{k}'")
...     fl_units_dict.update(subs)
...     return fl_units_dict
...
>>> def remove_unhandled_units(fl_units_dict):
...     not_si = {}
...     unhandled = {}
...     for k, v in fl_units_dict.items():
...         try:
...             Unit(v)
...             q = Quantity(1.0, v)
...             if get_si_value(q) != 1.0:
...                 not_si[k] = v
...         except Exception:
...             unhandled[k] = v
...     print("Not SI:")
...     pprint(not_si)
...     print("Unhandled:")
...     pprint(unhandled)
...     [fl_units_dict.pop(key) for key in list(not_si) + list(unhandled)]
...     return fl_units_dict
...
>>> def make_python_fl_unit_table(scheme_unit_table):
...     as_list = lispy.parse(scheme_unit_table)[1][1]
...     as_dict = { x[0]:x[1][3].split('"')[1] for x in as_list }
...     return remove_unhandled_units(substitute_fl_units_with_py_units(as_dict))
...

Output from most recent run to generate the table below:

>>> pprint(make_python_fl_unit_table(fl_scheme_unit_table))
Substitutions:
'deg' -> 'radian' for 'angle'
'rad s^-1' -> 'radian s^-1' for 'angular-velocity'
'Ohm m^3' -> 'ohm m^3' for 'contact-resistance-vol'
'deg' -> 'radian' for 'crank-angle'
'Ohm m^2' -> 'ohm m^2' for 'elec-contact-resistance'
'Ohm m' -> 'ohm m' for 'elec-resistivity'
'Ohm' -> 'ohm' for 'elec-resistance'
'%' -> '' for 'percentage'
'N m rad^-1' -> 'N m radian^-1' for 'spring-constant-angular'
Not SI:
{'concentration': 'kmol m^-3',
 'elec-charge': 'A h',
 'molec-wt': 'kg kmol^-1',
 'soot-sitespecies-concentration': 'kmol m^-3'}
Unhandled:
{'crank-angular-velocity': 'rev min^-1',
 'energy-density': 'J/m2',
 'mole-con-henry-const': 'Pa m^3 kgmol^-1',
 'mole-specific-energy': 'J kgmol^-1',
 'mole-specific-entropy': 'J kgmol^-1 K^-1',
 'mole-transfer-rate': 'kgmol m^-3 s^-1',
 'particles-conc': '1.e15-particles/kg',
 'particles-rate': '1.e15 m^-3 s^-1',
 'site-density': 'kgmol m^-2',
 'soot-limiting-nuclei-rate': '1e+15-particles/m3-s',
 'soot-oxidation-constant': 'kg m kgmol^-1 K^-0.5 s^-1',
 'soot-pre-exponential-constant': '1.e15 kg^-1 s^-1',
 'soot-surface-growth-scale-factor': 'kg m kgmol^-1 s^-1',
 'surface-mole-transfer-rate': 'kgmol m^-2 s^-1',
 'univ-gas-constant': 'J K^-1 kgmol^-1',
 'viscosity-consistency-index': 'kg s^n-2 m^-1',
 'wave-length': 'Angstrom'}
"""

from __future__ import annotations

from typing import TypeVar

_fl_unit_table = {
    "acceleration": "m s^-2",
    "angle": "radian",
    "angular-velocity": "radian s^-1",
    "area": "m^2",
    "area-inverse": "m^-2",
    "collision-rate": "m^-3 s^-1",
    "contact-resistance": "m^2 K W^-1",
    "contact-resistance-vol": "ohm m^3",
    "crank-angle": "radian",
    "current": "A",
    "current-density": "A m^-2",
    "current-vol-density": "A m^-3",
    "density": "kg m^-3",
    "density*specific-energy": "J m^-3",
    "density*specific-heat": "J m^-3 K^-1",
    "density*velocity": "kg m^-2 s^-1",
    "density-gradient": "kg m^-4",
    "density-inverse": "m^3 kg^-1",
    "depth": "m",
    "elec-charge-density": "A s m^-3",
    "elec-conductivity": "S m^-1",
    "elec-contact-resistance": "ohm m^2",
    "elec-field": "V m^-1",
    "elec-permittivity": "farad m^-1",
    "elec-resistance": "ohm",
    "elec-resistivity": "ohm m",
    "energy": "J",
    "force": "N",
    "force*time-per-volume": "N s m^-3",
    "force-per-area": "N m^-2",
    "force-per-volume": "N m^-3",
    "frequency": "Hz",
    "gas-constant": "J kg^-1 K^-1",
    "heat-flux": "W m^-2",
    "heat-flux-resolved": "m K s^-1",
    "heat-generation-rate": "W m^-3",
    "heat-transfer-coefficient": "W m^-2 K^-1",
    "ignition-energy": "J mol^-1",
    "kinematic-viscosity": "m^2 s^-1",
    "length": "m",
    "length-inverse": "m^-1",
    "length-time-inverse": "m^-1 s^-1",
    "mag-permeability": "H m^-1",
    "mass": "kg",
    "mass-diffusivity": "m^2 s^-1",
    "mass-flow": "kg s^-1",
    "mass-flow-per-depth": "kg m^-1 s^-1",
    "mass-flow-per-time": "kg s^-2",
    "mass-flux": "kg m^-2 s^-1",
    "mass-transfer-rate": "kg m^-3 s^-1",
    "moment": "N m",
    "moment-of-inertia": "kg m^2",
    "nucleation-rate": "m^-3 s^-1",
    "number-density": "m^-3",
    "percentage": "",
    "power": "W",
    "power-per-time": "W s^-1",
    "pressure": "Pa",
    "pressure-2nd-time-derivative": "Pa s^-2",
    "pressure-gradient": "Pa m^-1",
    "pressure-time-deriv-sqr": "Pa^2 s^-2",
    "pressure-time-derivative": "Pa s^-1",
    "resistance": "m^-1",
    "soot-formation-constant-unit": "kg N^-1 m^-1 s^-1",
    "soot-linear-termination": "m^3 s^-1",
    "source-elliptic-relaxation-function": "kg m^-3 s^-2",
    "source-energy": "W m^-3",
    "source-kinetic-energy": "kg m^-1 s^-3",
    "source-mass": "kg m^-3 s^-1",
    "source-momentum": "N m^-3",
    "source-specific-dissipation-rate": "kg m^-3 s^-2",
    "source-temperature-variance": "K^2 m^-3 s^-1",
    "source-turbulent-dissipation-rate": "kg m^-1 s^-4",
    "source-turbulent-viscosity": "kg m^-1 s^-2",
    "specific-area": "m^2 kg^-1",
    "specific-energy": "J kg^-1",
    "specific-heat": "J kg^-1 K^-1",
    "spring-constant": "N m^-1",
    "spring-constant-angular": "N m radian^-1",
    "stefan-boltzmann-constant": "W m^-2 K^-4",
    "surface-density": "kg m^-2",
    "surface-tension": "N m^-1",
    "surface-tension-gradient": "N m^-1 K^-1",
    "temperature": "K",
    "temperature-difference": "K",
    "temperature-gradient": "K m^-1",
    "temperature-inverse": "K^-1",
    "temperature-variance": "K^2",
    "thermal-conductivity": "W m^-1 K^-1",
    "thermal-resistance": "m^2 K W^-1",
    "thermal-resistivity": "m K W^-1",
    "thermophoretic-diffusivity": "kg m^2 s^-2",
    "time": "s",
    "time-inverse": "s^-1",
    "time-inverse-cubed": "s^-3",
    "time-inverse-squared": "s^-2",
    "turb-kinetic-energy-production": "kg m^-1 s^-3",
    "turbulent-energy-diss-rate": "m^2 s^-3",
    "turbulent-energy-diss-rate-gradient": "m s^-3",
    "turbulent-kinetic-energy": "m^2 s^-2",
    "turbulent-kinetic-energy-gradient": "m s^-2",
    "velocity": "m s^-1",
    "viscosity": "kg m^-1 s^-1",
    "voltage": "V",
    "volume": "m^3",
    "volume-flow-rate": "m^3 s^-1",
    "volume-flow-rate-per-depth": "m^3 s^-1 m^-1",
    "volume-inverse": "m^-3",
    "youngs-modulus": "N m^-2",
}


class InvalidQuantityType(TypeError):
    """Raised on an attempt to get a Quantity with invalid type."""

    def __init__(
        self,
        quantity,
    ) -> None:
        """Initialize InvalidQuantityType."""
        super().__init__(
            f"The specified quantity, '{quantity}' is not a string ({type(quantity)})."
        )


class UnitsNotDefinedForQuantity(ValueError):
    """Raised on an attempt to get undefined units for the specified Quantity."""

    def __init__(
        self,
        quantity: str,
    ) -> None:
        """Initialize UnitsNotDefinedForQuantity."""
        super().__init__(
            f"The units for the specified quantity, '{quantity}' are not defined in PyFluent."
        )


QuantityT = TypeVar("QuantityT")


class UnhandledQuantity(RuntimeError):
    """Raised on an attempt to get an unhandled Quantity."""

    def __init__(
        self,
        path: str,
        quantity: QuantityT,
    ) -> None:
        """Initialize UnhandledQuantity."""
        super().__init__(
            f"Could not handle the quantity, '{quantity}' for the path, {path}."
        )


def get_si_unit_for_fluent_quantity(
    quantity: str | None, unit_table: dict | None = None
):
    """Get the SI unit for the given Fluent quantity.

    Raises
    ------
    InvalidQuantityType
        If ``quantity`` is not a string instance, unless it is None.
    """
    # The settings API should return None for the units-quantity
    # attribute only for dimensionless variables
    if quantity is None:
        return ""
    if not isinstance(quantity, str):
        raise InvalidQuantityType(quantity)
    try:
        return (unit_table or _fl_unit_table)[quantity]
    except KeyError:
        # if it's not configured, None signifies that
        # we don't know the units. no need to raise
        # as this is pretty normal
        pass
