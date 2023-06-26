import ansys.fluent.core.quantity as q


class QuantityMap(object):
    """Creates a Quantity Map object based on a given quantity map.

    Parameters
    ----------
    quantity_map : dict
        Dictionary containing quantity map units and values.

    Returns
    -------
    QuantityMap instance.
    """

    def __init__(self, quantity_map):
        self._units_table = q.UnitsTable()
        self._unit = self._map_to_units(quantity_map)

    def _map_to_units(self, quantity_map: dict) -> str:
        """Convert a quantity map into a unit string.

        Parameters
        ----------
        quantity_map : dict
            Quantity map to be converted to unit string.

        Returns
        -------
        str
            Unit string representation of quantity map.
        """
        unit_dict = {
            self._units_table.api_quantity_map[term]: power
            for term, power in quantity_map.items()
        }

        units = ""

        # Split unit string into terms and parse data associated with individual terms
        for terms in unit_dict:
            for term in terms.split(" "):
                _, unit_term, unit_term_power = self._units_table.filter_unit_term(term)

                unit_term_power *= unit_dict[terms]

                if unit_term_power == 1.0:
                    units += f"{unit_term} "
                elif unit_term_power != 0.0:
                    units += f"{unit_term}^{unit_term_power} "

        return self._units_table.condense(units=units)[:-1]

    @property
    def units(self):
        """Unit string representation of quantity map."""
        return self._unit
