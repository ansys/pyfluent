import json


class UnitsTable(object):
    """ """

    def __init__(self):
        self._data: dict = self._get_data()
        self._api_quantity_map: dict = self._data["api_quantity_map"]
        self._fundamental_units: dict = self._data["fundamental_units"]
        self._derived_units: dict = self._data["derived_units"]
        self._multipliers: dict = self._data["multipliers"]

    def _get_data(self):
        """Reads quantity data from json file"""

        path = "src/ansys/fluent/core/quantity/"

        with open(path + "quantity_config.json", "r") as data_json:
            return json.load(data_json)

    @property
    def api_quantity_map(self):
        """Settings API quantity map values"""
        return self._api_quantity_map

    @property
    def fundamental_units(self):
        """Fundamental units"""
        return self.fundamental_units

    @property
    def derived_units(self):
        """Derived units"""
        return self.derived_units

    def filter_unit_term(self, unit_term: str) -> str:
        """Separate multiplier, base, and exponent from unit term.

        Parameters
        ----------
        unit_term : str
            Unit term of a unit string.

        Returns
        -------
        filtered_unit_term : dict
            Dictionary containing all components of the unit term.
        """
        multiplier = ""
        base = ""
        exponent = 0.0

        # strip exponent from unit term
        if "^" in unit_term:
            exponent = float(unit_term[unit_term.index("^") + 1 :])
            unit_term = base = unit_term[: unit_term.index("^")]

        # strip multiplier and base from unit term
        if self.has_multiplier(unit_term):
            for mult in self._multipliers.keys():
                if unit_term.startswith(mult):
                    if not self.has_multiplier(unit_term[len(mult) :]):
                        multiplier = mult
                        base = unit_term[len(mult) :]

        return {
            "multiplier": multiplier,
            "base": base,
            "exponent": exponent,
        }

    def has_multiplier(self, unit_term: str) -> bool:
        """"""
        return not (
            (unit_term in self._fundamental_units) or (unit_term in self._derived_units)
        )

    def compute_multiplier(self):
        """ """
        pass
