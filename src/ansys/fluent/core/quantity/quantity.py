from ansys.fluent.core.quantity import Dimensions, QuantityMap, Units, UnitString


class Quantity(float):
    """Quantity instantiates physical quantities using their real values and
    units. All the instances of this class are converted to base SI units system to have
    consistency in all arithmetic operations.

    Properties
    ----------
    real_value : float
        Real value of quantity.

    unit_str : str
        Unit string representation of quantity.

    quantity_map : dict
        Quantity map representation of quantity.

    dimensions : list
        Dimensions representation of quantity.

    Methods
    -------
    to(to_unit)
        Converts to given unit string.

    Returns
    -------
    Quantity instance.
    """

    def __new__(cls, real_value, unit_str=None, quantity_map=None, dimensions=None):
        """Parameter pre-check before Quantity initialization."""
        if (
            (unit_str and quantity_map)
            or (unit_str and dimensions)
            or (quantity_map and dimensions)
        ):
            raise ValueError(
                "Quantity only accepts 1 of the following: unit_str, quantity_map, dimensions"
            )

        return float.__new__(cls)

    def __init__(self, real_value, unit_str=None, quantity_map=None, dimensions=None):
        """
        initialize Quantity using a unit string, quantity map or dimensions.

        Parameters
        ----------
        real_value: float
            Value of quantity
        unit_str: str
            Unit of quantity
        quantity_map: dict
            Map of quantity and it's unit
        dimensions: list
            array of dimensions

        """
        self._units = Units
        self._real_value = float(real_value)

        if quantity_map:
            unit_str = self._units.map_to_unit_str(quantity_map)

        if dimensions:
            unit_str = self._units.dim_to_unit_str(dimensions)

        self._unit_string = UnitString(unit_str)
        self._quantity_map = QuantityMap(unit_str)
        self._dimensions = Dimensions(unit_str)

    @property
    def real_value(self):
        """Real value of quantity"""
        return self._real_value

    @property
    def unit_str(self):
        """Unit string of quantity"""
        return self._unit_string.unit_str

    @property
    def dimensions(self):
        """Dimensions of quantity"""
        return self._dimensions.dimensions

    @property
    def quantity_map(self):
        """Quantity map of quantity"""
        return self._quantity_map.quantity_map

    def to():
        """"""
        pass


class QuantityError(ValueError):
    """Custom quantity errors."""

    def __init__(self, from_unit, to_unit):
        """
        Quantity errors with custom messages.

        Parameters
        ----------
        from_unit: str
            Unit of quantity
        to_unit: str
            Desired conversion unit
        """
        self.from_unit = from_unit
        self.to_unit = to_unit

    def __str__(self):
        return f"{self.unit} and {self.to_unit} have incompatible dimensions."
