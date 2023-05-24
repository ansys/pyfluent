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

    def dim_to_unit_str(dimensions: list) -> str:
        """ """
        dimensions = [float(dim) for dim in ((9 - len(dimensions)) * [0])]
        si_order = ["kg", "m", "s", "K", "A", "mol", "cd", "radian", "sr"]
        unit_str = ""

        for dim in range(len(dimensions)):
            if dimensions[dim] == 1.0:
                unit_str += si_order[dim] + " "
            elif dimensions[dim] != 0.0:
                unit_str += si_order[dim] + "^" + str(int(dimensions[dim])) + " "

        return unit_str[:-1]

    def map_to_unit_str(quantity_map: dict) -> str:
        """"""
        pass

    def unit_str_to_dim():
        """"""
        pass

    def unit_str_to_map():
        pass
