import json


class UnitsTable(object):
    """ """

    def __init__(self):
        self._data: dict = self._get_data()
        self._api_quantity_map: dict = self._data["api_quantity_map"]
        self._fundamental_units: dict = self._data["fundamental_units"]
        self._derived_units: dict = self._data["derived_units"]
        self._multipliers: dict = self._data["multipliers"]

    def _get_data(self) -> dict:
        """Reads quantity data from json file.

        Returns
        -------
        : dict
            Quantity data loaded in from JSON file.
        """

        path = "src/ansys/fluent/core/quantity/"

        with open(path + "quantity_config.json", "r") as data_json:
            return json.load(data_json)

    def _has_multiplier(self, unit_term: str) -> bool:
        """Check if a unit term contains a multiplier.

        Parameters
        ----------
        unit_term : str
            Unit term of a unit string.

        Returns
        -------
        : bool
            Boolean of multiplier within unit_term.
        """
        return not (
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
        unit_term_type = self._fundamental_units[unit_term]["type"]

        for term, term_info in self._fundamental_units.items():
            if term_info["type"] == unit_term_type and term_info["factor"] == 1.0:
                return term

    @property
    def api_quantity_map(self):
        """Settings API quantity map values"""
        return self._api_quantity_map

    @property
    def fundamental_units(self):
        """Fundamental units"""
        return self._fundamental_units

    @property
    def derived_units(self):
        """Derived units"""
        return self._derived_units

    @property
    def multipliers(self):
        """Multipliers"""
        return self._multipliers

    def filter_unit_term(self, unit_term: str) -> str:
        """Separate multiplier, base, and power from a unit term.

        Parameters
        ----------
        unit_term : str
            Unit term of a unit string.

        Returns
        -------
        : dict
            Dictionary containing all components of the unit term.
        """
        multiplier = ""
        power = 1.0

        # strip power from unit term
        if "^" in unit_term:
            power = float(unit_term[unit_term.index("^") + 1 :])
            unit_term = unit_term[: unit_term.index("^")]

        base = unit_term

        # strip multiplier and base from unit term
        if self._has_multiplier(unit_term):
            for mult in self._multipliers:
                if unit_term.startswith(mult):
                    if not self._has_multiplier(unit_term[len(mult) :]):
                        multiplier = mult
                        base = unit_term[len(mult) :]
                        break

        return multiplier, base, power

    def si_conversion(
        self,
        unit_str: str,
        power: float = None,
        si_unit_str: str = None,
        si_multiplier: float = None,
        si_offset: float = None,
    ) -> tuple:
        """Compute the SI unit string, SI multiplier, and SI offset.

        Parameters
        ----------
        unit_str : str
            Unit string representation of quantity.
        power : float
            Power of unit string
        si_unit_string : str
            SI unit string representation of quantity.
        si_multiplier : float
            SI multiplier of unit string.
        si_offset : float
            SI offset of a unit string.

        Returns
        -------
        : tuple
            Tuple containing si_unit_string and si_multiplier.
        """
        if not unit_str:
            return

        power = power or 1.0
        si_unit_str = si_unit_str or ""
        si_multiplier = si_multiplier or 1.0
        si_offset = si_offset or 0.0

        for term in unit_str.split(" "):
            unit_multiplier, unit_term, unit_term_power = self.filter_unit_term(term)

            unit_term_power *= power

            si_multiplier *= (
                self._multipliers[unit_multiplier] ** unit_term_power
                if unit_multiplier
                else 1.0
            )

            if unit_term in self._fundamental_units:
                si_offset = self._fundamental_units[unit_term]["offset"]

                if unit_term_power == 1.0:
                    si_unit_str += f"{self._si_map(unit_term)} "
                elif unit_term_power != 0.0:
                    si_unit_str += f"{self._si_map(unit_term)}^{unit_term_power} "

                si_multiplier *= (
                    self._fundamental_units[unit_term]["factor"] ** unit_term_power
                )

            if unit_term in self._derived_units:
                si_multiplier *= self._derived_units[unit_term]["factor"]

                si_unit_str, si_multiplier, si_offset = self.si_conversion(
                    unit_str=self._derived_units[unit_term]["composition"],
                    power=unit_term_power,
                    si_unit_str=si_unit_str,
                    si_multiplier=si_multiplier,
                    si_offset=si_offset,
                )

        return self.condense(si_unit_str), si_multiplier, si_offset

    def condense(self, unit_str: str) -> str:
        """Condenses a unit string by collecting like-terms.

        Parameters
        ----------
        unit_string : str
            Unit string to be simplified.

        Returns
        -------
        unit_string : str
            Simplified unit string.
        """
        terms_and_powers = {}

        for term in unit_str[:-1].split(" "):
            _, unit_term, unit_term_power = self.filter_unit_term(term)

            if unit_term in terms_and_powers:
                terms_and_powers[unit_term] += unit_term_power
            else:
                terms_and_powers[unit_term] = unit_term_power

        unit_str = ""

        for term, power in terms_and_powers.items():
            if power == 1.0:
                unit_str += f"{term} "
            else:
                unit_str += f"{term}^{power} "

        return unit_str

    def get_type(self, unit_str: str) -> str:
        """Returns unit string type.

        Parameters
        ----------
        unit_str : str
            Unit string of quantity.

        Returns
        -------
        : str
            Type of quantity.
        """

        if unit_str in self.fundamental_units:
            return self.fundamental_units[unit_str]["type"]

        if unit_str in self.derived_units:
            return "Derived"

        return "Composite"
