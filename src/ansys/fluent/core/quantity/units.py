import json


class Units(object):
    """ """

    def __init__(self):
        self._data = self._get_data()
        self._quantity_map = self._data["quantity_map"]
        self._fundamental_units = self._data["fundamental_units"]
        self._derived_units = self._data["derived_units"]

    def _get_data(self):
        """Reads quantity data from json file"""

        with open("qunatity_config.json", "r") as data_json:
            return json.load(data_json)

    @property
    def quantity_map(self):
        """Quantity map values"""
        return self._quantity_map

    @property
    def fundamental_units(self):
        """Fundamental units"""
        return self.fundamental_units

    @property
    def derived_units(self):
        """Derived units"""
        return self.derived_units
