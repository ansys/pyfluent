import os

import yaml

from ansys.fluent.core.quantity._constants import _QuantityType
from ansys.fluent.core.quantity.quantity import Quantity, QuantityError  # noqa: F401
from ansys.fluent.core.quantity.units import parse_temperature_units


class UnitsTable(object):
    """Initializes a UnitsTable object with all table values and unit string
    manipulation methods.

    Methods
    -------
    filter_unit_term()
        Separate multiplier, base, and power from a unit term.
    si_data()
        Compute the SI unit string, SI multiplier, and SI offset from a unit string of any type.
    si_conversion()
        Perform SI conversion based on quantity type.
    condense()
        Condenses a unit string by collecting like-terms.
    get_type()
        Returns the type associated with a unit string.

    Returns
    -------
    UnitsTable instance.
    """

    def __init__(self):
        file_path = os.path.relpath(__file__)
        file_dir = os.path.dirname(file_path)
        qc_path = os.path.join(file_dir, "cfg.yaml")

        with open(qc_path, "r") as qc_yaml:
            qc_data = yaml.safe_load(qc_yaml)

        self._dimension_order: dict = qc_data["dimension_order"]
        self._multipliers: dict = qc_data["multipliers"]
        self._unit_systems: dict = qc_data["unit_systems"]
        self._api_quantity_map: dict = qc_data["api_quantity_map"]
        self._fundamental_units: dict = qc_data["fundamental_units"]
        self._derived_units: dict = qc_data["derived_units"]

    def _has_multiplier(self, unit_term: str) -> bool:
        """Check if a unit term contains a multiplier.

        Parameters
        ----------
        unit_term : str
            Unit term of a unit string.

        Returns
        -------
        bool
            Boolean of multiplier within unit_term.
        """
        # Check if the unit term is not an existing fundamental or derived unit.
        return unit_term and not (
            (unit_term in self._fundamental_units) or (unit_term in self._derived_units)
        )

    def _si_map(self, unit_term: str) -> str:
        """Maps unit to SI unit equivalent.

        Parameters
        ----------
        unit_term : str
            Unit term of a unit string.

        Returns
        -------
        term : str
            SI unit equivalent.
        """
        # Retrieve type associated with unit term
        unit_term_type = self._fundamental_units[unit_term]["type"]

        # Find SI unit with same type as unit term
        for term, term_info in self._fundamental_units.items():
            if term_info["type"] == unit_term_type and term_info["factor"] == 1.0:
                return term

    @property
    def api_quantity_map(self):
        """Quantity map values from settings API."""
        return self._api_quantity_map

    @property
    def fundamental_units(self):
        """Fundamental units and properties representing Mass, Length, Time, Current,
        Chemical Amount, Light, Solid Angle, Angle, Temperature and Temperature
        Difference."""
        return self._fundamental_units

    @property
    def derived_units(self):
        """Derived units and properties composed of fundamental units."""
        return self._derived_units

    @property
    def multipliers(self):
        """Multiplier prefixes and respective factors."""
        return self._multipliers

    @property
    def unit_systems(self):
        """Predefined unit systems and units."""
        return self._unit_systems

    @property
    def dimension_order(self):
        """Order of dimensions."""
        return self._dimension_order

    def filter_unit_term(self, unit_term: str) -> tuple:
        """Separate multiplier, base, and power from a unit term.

        Parameters
        ----------
        unit_term : str
            Unit term of a unit string.

        Returns
        -------
        tuple
            Tuple containing multiplier, base, and power of the unit term.
        """
        multiplier = ""
        power = 1.0

        # strip power from unit term
        if "^" in unit_term:
            power = float(unit_term[unit_term.index("^") + 1 :])
            unit_term = unit_term[: unit_term.index("^")]

        base = unit_term

        # strip multiplier and base from unit term
        has_multiplier = self._has_multiplier(unit_term)
        if has_multiplier:
            for mult in self._multipliers:
                if unit_term.startswith(mult):
                    if not self._has_multiplier(unit_term[len(mult) :]):
                        multiplier = mult
                        base = unit_term[len(mult) :]
                        break

        # if we thought it had a multiplier, that's just because the string wasn't
        # a known unit on its own. So if we can't actually find its multiplier then
        # this string is an invalid unit string
        if has_multiplier and not multiplier:
            raise QuantityError.UNKNOWN_UNITS(unit_term)
        return multiplier, base, power

    def si_data(
        self,
        units: str,
        power: float = None,
        si_units: str = None,
        si_multiplier: float = None,
    ) -> tuple:
        """Compute the SI unit string, SI multiplier, and SI offset.

        Parameters
        ----------
        units : str
            Unit string representation of quantity.
        power : float
            Power of unit string
        si_unitsing : str
            SI unit string representation of quantity.
        si_multiplier : float
            SI multiplier of unit string.
        si_offset : float
            SI offset of a unit string.

        Returns
        -------
        tuple
            Tuple containing si_unitsing, si_multiplier and si_offset.
        """

        # Initialize default values
        units = units or " "
        power = power or 1.0
        si_units = si_units or ""
        si_multiplier = si_multiplier or 1.0
        si_offset = (
            self._fundamental_units[units]["offset"]
            if units in self._fundamental_units
            else 0.0
        )

        # Split unit string into terms and parse data associated with individual terms
        for term in units.split(" "):
            unit_multiplier, unit_term, unit_term_power = self.filter_unit_term(term)

            unit_term_power *= power

            si_multiplier *= (
                self._multipliers[unit_multiplier] ** unit_term_power
                if unit_multiplier
                else 1.0
            )

            # Retrieve data associated with fundamental unit
            if unit_term in self._fundamental_units:
                if unit_term_power == 1.0:
                    si_units += f" {self._si_map(unit_term)}"
                elif unit_term_power != 0.0:
                    si_units += f" {self._si_map(unit_term)}^{unit_term_power}"

                si_multiplier *= (
                    self._fundamental_units[unit_term]["factor"] ** unit_term_power
                )

            # Retrieve derived unit composition unit string and factor.
            if unit_term in self._derived_units:
                si_multiplier *= (
                    self._derived_units[unit_term]["factor"] ** unit_term_power
                )

                # Recursively parse composition unit string
                si_units, si_multiplier, _ = self.si_data(
                    units=self._derived_units[unit_term]["composition"],
                    power=unit_term_power,
                    si_units=si_units,
                    si_multiplier=si_multiplier,
                )

        return self.condense(si_units), si_multiplier, si_offset

    def condense(self, units: str) -> str:
        """Condenses a unit string by collecting like-terms.

        Parameters
        ----------
        unitsing : str
            Unit string to be simplified.

        Returns
        -------
        str
            Simplified unit string.
        """
        terms_and_powers = {}
        units = units.strip()

        # Split unit string into terms and parse data associated with individual terms
        for term in units.split(" "):
            _, unit_term, unit_term_power = self.filter_unit_term(term)

            if unit_term in terms_and_powers:
                terms_and_powers[unit_term] += unit_term_power
            else:
                terms_and_powers[unit_term] = unit_term_power

        units = ""

        # Concatenate unit string
        for term, power in terms_and_powers.items():
            if not (power):
                continue
            if power == 1.0:
                units += f"{term} "
            else:
                power = int(power) if power % 1 == 0 else power
                units += f"{term}^{power} "

        return units.rstrip()

    def get_type(self, units: str) -> str:
        """Returns the type associated with a unit string.

        Parameters
        ----------
        units : str
            Unit string of quantity.

        Returns
        -------
        str
            Type of quantity.
        """

        if units == "":
            return _QuantityType.no_type

        if units in self.fundamental_units:
            return self.fundamental_units[units]["type"]

        if units in self.derived_units:
            return _QuantityType.derived

        # HACK
        temperature_units_to_search = ("K", "C", "F", "R")
        if any([temp in units for temp in temperature_units_to_search]):
            terms = parse_temperature_units(
                units,
                ignore_exponent=False,
                units_to_search=temperature_units_to_search,
            )
            if any(is_diff for (_, is_diff) in terms):
                return _QuantityType.temperature_difference
            return _QuantityType.temperature

        return _QuantityType.composite
