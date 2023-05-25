import json


class UnitsTable(object):
    """ """

    def __init__(self):
        self._data = self._get_data()
        self._api_quantity_map = self._data["api_quantity_map"]
        self._fundamental_units = self._data["fundamental_units"]
        self._derived_units = self._data["derived_units"]

    def _get_data(self):
        """Reads quantity data from json file"""

        with open("qunatity_config.json", "r") as data_json:
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

    def filter_multiplier(self):
        """ """
        pass

    def remove_multiplier(self):
        """ """
        pass

    def compute_multiplier(self):
        """ """
        pass
