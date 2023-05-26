from units_table import UnitsTable


class Dimensions(object):
    """ """

    def __init__(self, unit_str=None, dimensions=None):
        """ """
        self._units_table = UnitsTable()
        self._unit_str = ""
        self._dimensions = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        if unit_str:
            self._unit_str = unit_str
            self._unit_str_to_dim(unit_str)

        if dimensions:
            self._dimensions = dimensions
            self._dim_to_unit_str(dimensions)

    def _dim_to_unit_str(self, dimensions: list) -> str:
        """ """
        dimensions = [float(dim) for dim in dimensions + ((9 - len(dimensions)) * [0])]
        si_order = ["kg", "m", "s", "K", "A", "mol", "cd", "radian", "sr"]
        unit_str = ""

        for idx, dim in enumerate(dimensions):
            if dim == 1.0:
                unit_str += si_order[idx] + " "
            elif dim != 0.0:
                unit_str += si_order[idx] + "^" + str(int(dim)) + " "

        self._unit_str = unit_str[:-1]

    def _unit_str_to_dim(self, unit_str: str, power: float = 1.0) -> list:
        """"""
        if not unit_str:
            return

        for term in unit_str.split(" "):
            filtered_unit = self._units_table.filter_unit_term(term)

            unit_term = filtered_unit["base"]
            unit_term_power = filtered_unit["exponent"] * power

            if unit_term in self._units_table.fundamental_units:
                idx = self._units_table.fundamental_units.index(unit_term)
                self._dimensions[idx] += unit_term_power
                continue

            if unit_term in self._units_table.derived_units:
                self._unit_str_to_dim(
                    self._units_table.derived_units[unit_term], unit_term_power
                )
                continue

            # IMPLEMENT derived_units_with_conversion_factor

    @property
    def unit_str(self):
        """Unit string representation of dimensions"""
        return self._unit_str

    @property
    def dimensions(self):
        """Dimensions representation of unit string"""
        return self._dimensions
