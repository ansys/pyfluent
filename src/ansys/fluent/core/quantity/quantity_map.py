from units_table import UnitsTable


class QuantityMap(object):
    """ """

    def __init__(self, unit_str=None, quantity_map=None):
        self._units_table = UnitsTable()

        if unit_str:
            self._unit_str = unit_str
            self._quantity_map = self._unit_str_to_map(unit_str)

        if quantity_map:
            self._quantity_map = quantity_map
            self._unit_str = self._map_to_unit_str(quantity_map)

    def _map_to_unit_str(self, quantity_map: dict) -> str:
        """Convert a quantity map into a unit string.

        Parameters
        ----------
        quantity_map : dict
            Quantity map to be converted to unit string.

        Returns
        -------
        : str
            Unit string representation of quantity map.
        """
        unit_dict = {
            self._units_table.api_quantity_map[term]: power
            for term, power in quantity_map.items()
        }

        unit_str = ""

        for terms in unit_dict:
            for term in terms.split(" "):
                _, unit_term, unit_term_power = self._units_table.filter_unit_term(term)

                unit_term_power *= unit_dict[terms]

                if unit_term_power == 1.0:
                    unit_str += f"{unit_term} "
                else:
                    unit_str += f"{unit_term}^{unit_term_power} "

        return self._units_table.condense(unit_str=unit_str)

    def _unit_str_to_map(self, unit_str: str) -> dict:
        """"""
        pass

    @property
    def unit_str(self):
        """Unit string representation of quantity map"""
        return self._unit_str

    @property
    def quantity_map(self):
        """Quantity map representation of unit string"""
        return self._quantity_map
