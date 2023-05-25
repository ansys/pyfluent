from ansys.fluent.core.quantity.units_table import UnitsTable


class Dimensions(object):
    """ """

    def __init__(self, unit_str=None, dimensions=None):
        self._units_table = UnitsTable()

        if unit_str:
            self._unit_str = unit_str
            self._dimensions = self._unit_str_to_dim(unit_str)

        if dimensions:
            self._dimensions = dimensions
            self._unit_str = self._dim_to_unit_str(dimensions)

    def _dim_to_unit_str(self, dimensions: list) -> str:
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

    def _unit_str_to_dim(self, unit_str: str, power: int = 1) -> list:
        """"""
        if len(unit_str) == 0:
            return

        for term in unit_str.split(" "):
            pass

    @property
    def unit_str(self):
        """Unit string representation of dimensions"""
        return self._unit_str

    @property
    def dimensions(self):
        """Dimensions representation of unit string"""
        return self._dimensions
