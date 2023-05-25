from ansys.fluent.core.quantity.units_table import UnitsTable


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
        """"""
        pass

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
