import pint
from pint import Unit

ureg = pint.UnitRegistry(autoconvert_offset_to_baseunit=True)
ureg.default_system = "SI"

quantity = ureg.Quantity


class Quantity(float):
    """This class instantiates physical quantities using their real values and
    units. Attributes of every instance of this class are used to construct a
    new quantity instance supported by unit registry of pint module.

    Attributes
    ----------
    value: Real value
        Value of quantity is stored as float.

    unit: Unit string
        Unit of quantity is stored as string.

    Methods
    -------
    to(to_unit)
        Converts to given unit string.

    Returns
    -------
    Quantity instance.

    The pint module supports methods for unit conversions, unit compatibility and
    dimensionality check.

    All the instances of this class are converted to base SI units system to have
    consistency in all arithmetic operations.
    """

    def __new__(self, real_value, units_string):
        return float.__new__(self, real_value)

    def __init__(self, real_value, units_string):
        float.__init__(real_value)
        self.value = self.__float__()
        self.unit = units_string
        self._quantity = quantity(self.value, self.unit)
        self._base_si_quantity = self._quantity.to_base_units()

    def __str__(self):
        return f'({self.value}, "{self.unit}")'

    def __repr__(self):
        return f'(Quantity ({self.value}, "{self.unit}"))'

    def to(self, to_unit):

        """This method checks the compatibility between current instance unit
        and user provided unit, if both of them are compatible, then only it
        performs required conversion otherwise raises a Value Error."""

        user_unit = Unit(to_unit)

        if not self._quantity.is_compatible_with(user_unit):
            raise ValueError("Units are not compatible.")

        converted = self._quantity.to(to_unit)

        return Quantity(converted.magnitude, to_unit)

    def __mul__(self, other):

        if isinstance(other, Quantity):
            temp = self._base_si_quantity * other._quantity
        elif isinstance(other, int) or isinstance(other, float):
            temp = quantity(self._base_si_quantity * other, self.unit)
        return Quantity(temp.magnitude, temp.units)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):

        if isinstance(other, Quantity):
            temp = self._base_si_quantity / other._quantity
        elif isinstance(other, int) or isinstance(other, float):
            temp = quantity(self._base_si_quantity / other, self.unit)
        return Quantity(temp.magnitude, temp.units)

    def __add__(self, other):

        if isinstance(other, Quantity):
            temp = self._base_si_quantity + other._quantity
        elif self._base_si_quantity.dimensionless and (
            isinstance(other, int) or isinstance(other, float)
        ):
            temp = quantity(
                self._base_si_quantity.magnitude + other, self._base_si_quantity.units
            )
        else:
            raise ValueError(f"Quantity{(self.value, self.unit)} is not dimensionless.")
        return Quantity(temp.magnitude, temp.units)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):

        if isinstance(other, Quantity):
            temp = self._base_si_quantity - other._quantity
        elif self._base_si_quantity.dimensionless and (
            isinstance(other, int) or isinstance(other, float)
        ):
            temp = quantity(
                self._base_si_quantity.magnitude - other, self._base_si_quantity.units
            )
        else:
            raise ValueError(f"Quantity{(self.value, self.unit)} is not dimensionless.")
        return Quantity(temp.magnitude, temp.units)

    def __rsub__(self, other):

        if isinstance(other, Quantity):
            temp = other._quantity - self._base_si_quantity
        elif self._base_si_quantity.dimensionless and (
            isinstance(other, int) or isinstance(other, float)
        ):
            temp = quantity(
                other - self._base_si_quantity.magnitude, self._base_si_quantity.units
            )
        else:
            raise ValueError(f"Quantity{(self.value, self.unit)} is not dimensionless.")
        return Quantity(temp.magnitude, temp.units)

    def __eq__(self, other):
        return (
            other._quantity == self._quantity if isinstance(other, Quantity) else False
        )
