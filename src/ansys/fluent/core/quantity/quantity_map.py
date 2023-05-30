from units_table import UnitsTable


class QuantityMap(object):
    """Creates a Quantity Map object based on a given quantity map.

    Attributes
    ----------
    unit_str : str
        Unit string representation of quantity map.

    quantity_map : dict
        Quantity map.

    Returns
    -------
    QuantityMap instance.
    """

    def __init__(self, quantity_map=None):
        self._units_table = UnitsTable()
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
                elif unit_term_power != 0.0:
                    unit_str += f"{unit_term}^{unit_term_power} "

        return self._units_table.condense(unit_str=unit_str)

    @property
    def unit_str(self):
        """Unit string representation of quantity map"""
        return self._unit_str

    @property
    def quantity_map(self):
        """Quantity map representation of unit string"""
        return self._quantity_map
