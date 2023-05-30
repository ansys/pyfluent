from dimensions import Dimensions
from quantity_map import QuantityMap
from units_table import UnitsTable


class Quantity(float):
    """Quantity instantiates physical quantities using their real values and
    units. All the instances of this class are converted to base SI units system to have
    consistency in all arithmetic operations.

    Properties
    ----------
    value : float
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

    def __new__(cls, value, unit_str=None, quantity_map=None, dimensions=None):
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

    def __init__(self, value, unit_str=None, quantity_map=None, dimensions=None):
        self._units_table = UnitsTable()
        self._value = float(value)

        if unit_str:
            self._unit_string = unit_str
            self._dimensions = Dimensions(unit_str=unit_str)

        if quantity_map:
            unit_str = QuantityMap(quantity_map).unit_str
            self._unit_string = unit_str
            self._dimensions = Dimensions(unit_str=unit_str)

        if dimensions:
            self._dimensions = Dimensions(dimensions=dimensions)
            self._unit_string = self._dimensions.unit_str

        si_unit_str, si_multiplier, si_offset = self._units_table.si_conversion(
            unit_str=self._unit_string
        )

        self._si_unit_str = si_unit_str
        self._si_value = self.value * si_multiplier + si_offset
        self._type = self._units_table.get_type(unit_str)

    def _validate_matching_dimensions(self, __value):
        """Validate dimensions of quantities.

        Parameters
        ----------
        __value : Quantity | int | float
            Value modifying current quantity object.
        """
        if isinstance(__value, Quantity) and (self.dimensions != __value.dimensions):
            raise QuantityError(from_unit=self.unit_str, to_unit=__value.unit_str)
        elif (
            (all([dim == 0.0 for dim in self.dimensions]))
            and (not isinstance(__value, Quantity))
            and isinstance(__value, (float, int))
        ):
            raise TypeError(
                f"Error: '{__value}' is incompatible with the current quantity object."
            )

    @property
    def value(self):
        """Real value of quantity"""
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    @property
    def unit_str(self):
        """Unit string of quantity"""
        return self._unit_string

    @property
    def si_unit_str(self):
        """SI conversion unit string of quantity."""
        return self._si_unit_str

    @property
    def si_value(self):
        """SI conversion value of quantity."""
        return self._si_value

    @property
    def dimensions(self):
        """Dimensions of quantity"""
        return self._dimensions.dimensions

    @property
    def type(self):
        """Type of quantity."""
        return self._type

    @type.setter
    def type(self, new_type):
        self._type = new_type

    def to(self, to_unit_str: str) -> "Quantity":
        """Perform quantity conversions.

        Parameters
        ----------
        to_unit_str : str
            Desired unit to be converted to.

        Returns
        -------
        : Quantity
            Quantity object containing desired quantity conversion.
        """

        if not isinstance(to_unit_str, str):
            raise TypeError("'to_unit_str' should be of 'str' type.")

        new = Quantity(value=1.0, unit_str=to_unit_str)

        self._validate_matching_dimensions(new)

        new.value = (self.si_value / new.si_value) * self.value

        return new

    def convert(self, to_sys: str) -> "Quantity":
        """Perform unit system conversions.

        Parameters
        ----------
        to_sys : str
            Desired unit system to convert to.

        Returns
        -------
        : Quantity
            Quantity object containing desired unit system conversion.
        """

        if to_sys not in ["SI", "CGS", "BT"]:
            raise ValueError(
                f"'{to_sys}' is not a supported unit system. Only 'SI', 'CGS', 'BT' are supported."
            )

        new = Dimensions(dimensions=self.dimensions, unit_sys=to_sys)

        return Quantity(value=self.value, unit_str=new.unit_str)

    def __str__(self):
        return f'({self.value}"{self.unit_str}")'

    def __repr__(self):
        return f'Quantity ({self.value}, "{self.unit_str}")'

    def __pow__(self, __value):
        temp_dimensions = [dim * __value for dim in self.dimensions]
        new_si_value = self.si_value**__value

        new_dimensions = Dimensions(dimensions=temp_dimensions)
        return Quantity(value=new_si_value, unit_str=new_dimensions.unit_str)

    def __mul__(self, __value):
        if isinstance(__value, Quantity):
            temp_dimensions = [
                dim + __value.dimensions[idx] for idx, dim in enumerate(self.dimensions)
            ]
            new_si_value = self.si_value * __value.si_value

            new_dimensions = Dimensions(dimensions=temp_dimensions)
            return Quantity(value=new_si_value, unit_str=new_dimensions.unit_str)

        if isinstance(__value, (float, int)):
            return Quantity(value=self.si_value * __value, unit_str=self.si_unit_str)

    def __rmul__(self, __value):
        return self.__mul__(__value)

    def __truediv__(self, __value):
        if isinstance(__value, Quantity):
            temp_dimensions = [
                dim - __value.dimensions[idx] for idx, dim in enumerate(self.dimensions)
            ]
            new_si_value = self.si_value / __value.si_value

            new_dimensions = Dimensions(dimensions=temp_dimensions)
            return Quantity(value=new_si_value, unit_str=new_dimensions.unit_str)

        if isinstance(__value, (float, int)):
            return Quantity(value=self.si_value / __value, unit_str=self.si_unit_str)

    def __rtruediv__(self, __value):
        if not isinstance(__value, Quantity) and isinstance(__value, float):
            return Quantity(__value / self._si_value, self._si_unit_str)
        return __value / self

    def __add__(self, __value):
        self._validate_matching_dimensions(__value)
        new_value = float(self) + float(__value)
        return Quantity(value=new_value, unit_str=self.si_unit_str)

    def __radd__(self, __value):
        return Quantity(__value, "") + self

    def __sub__(self, __value):
        self._validate_matching_dimensions(__value)
        new_value = float(self) - float(__value)
        return Quantity(value=new_value, unit_str=self.si_unit_str)

    def __rsub__(self, __value):
        return Quantity(__value, "") - self

    def __neg__(self):
        return Quantity(-self.value, self.unit_str)

    def __gt__(self, __value):
        self._validate_matching_dimensions(__value)
        return float(self) > float(__value)

    def __ge__(self, __value):
        self._validate_matching_dimensions(__value)
        return float(self) >= float(__value)

    def __lt__(self, __value):
        self._validate_matching_dimensions(__value)
        return float(self) < float(__value)

    def __le__(self, __value):
        self._validate_matching_dimensions(__value)
        return float(self) <= float(__value)

    def __eq__(self, __value):
        self._validate_matching_dimensions(__value)
        return float(self) == float(__value)

    def __neq__(self, __value):
        self._validate_matching_dimensions(__value)
        return float(self) != float(__value)


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
        return f"'{self.from_unit}' and '{self.to_unit}' have incompatible dimensions."


test = Quantity(1, "l")
print(test.value, test.dimensions)

import ansys.fluent.core.quantity as q

t2 = q.Quantity(1, "l")
print(t2.value, t2.get_dimensions_list())
