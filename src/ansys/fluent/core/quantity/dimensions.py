from units_table import UnitsTable


class Dimensions(object):
    """Initialize a Dimensions object using a dimensions list or a unit string.

    Parameters
    ----------
    unit_str: str
        Unit string of quantity.
    dimensions: list
        List of dimensions.

    Returns
    -------
    Dimensions instance.
    """

    def __init__(
        self, unit_str: str = None, dimensions: list = None, unit_sys: str = None
    ):
        self._units_table = UnitsTable()

        unit_sys = unit_sys or "SI"

        if unit_str:
            self._unit_str = unit_str
            self._dimensions = self._unit_str_to_dim(unit_str=unit_str)

        if dimensions:
            self._dimensions = dimensions
            self._unit_str = self._dim_to_unit_str(
                dimensions=dimensions, unit_sys=unit_sys
            )

    def _dim_to_unit_str(self, dimensions: list, unit_sys: str) -> str:
        """Convert a dimensions list into a unit string.

        Parameters
        ----------
        dimensions : list
            List of unit dimensions.

        unit_sys : str
            Unit system of dimensions.

        Returns
        -------
        unit_str : str
            Unit string representation of dimensions.
        """
        dimensions = [float(dim) for dim in dimensions + ((9 - len(dimensions)) * [0])]
        sys_order = {
            "SI": ["kg", "m", "s", "K", "radian", "mol", "cd", "A", "sr"],
            "CGS": ["g", "cm", "s", "K", "radian", "mol", "cd", "A", "sr"],
            "BT": ["slug", "ft", "s", "R", "radian", "slugmol", "cd", "A", "sr"],
        }
        unit_str = ""

        for idx, dim in enumerate(dimensions):
            if dim == 1.0:
                unit_str += f"{sys_order[unit_sys][idx]} "
            elif dim != 0.0:
                unit_str += f"{sys_order[unit_sys][idx]}^{dim} "

        return unit_str[:-1]

    def _unit_str_to_dim(
        self, unit_str: str, power: float = None, dimensions: list = None
    ) -> list:
        """Convert a unit string into a dimensions list.

        Parameters
        ----------
        unit_str : str
            Unit string of quantity.
        power : float
            Power of unit string.

        Returns
        -------
        dimensions : list
            Dimensions representation of unit string.
        """
        if not unit_str:
            return

        power = power or 1.0
        dimensions = dimensions or [0.0] * 9

        for term in unit_str.split(" "):
            _, unit_term, unit_term_power = self._units_table.filter_unit_term(term)

            unit_term_power *= power

            if unit_term in self._units_table.fundamental_units:
                idx = (
                    self._units_table.fundamental_units[unit_term]["dimension_order"]
                    - 1
                )
                dimensions[idx] += unit_term_power

            if unit_term in self._units_table.derived_units:
                dimensions = self._unit_str_to_dim(
                    unit_str=self._units_table.derived_units[unit_term],
                    power=unit_term_power,
                    dimensions=dimensions,
                )

        return dimensions

    @property
    def unit_str(self):
        """Unit string representation of dimensions"""
        return self._unit_str

    @property
    def dimensions(self):
        """Dimensions representation of unit string"""
        return self._dimensions
