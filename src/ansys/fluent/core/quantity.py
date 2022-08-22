from itertools import permutations

import pint
from pint import Unit

unit = pint.UnitRegistry(autoconvert_offset_to_baseunit=True, system="SI")
quantity = unit.Quantity


restricted_units = ["Hz", "hertz", "rad/s", "radian/s", "rpm", "rps", "cps"]
restricted_conversions = list((permutations(restricted_units, 2)))


std_prefixes = [
    "y",
    "z",
    "a",
    "f",
    "p",
    "n",
    "u",
    "c",
    "d",
    "da",
    "h",
    "m",
    "k",
    "M",
    "G",
    "T",
    "P",
    "E",
    "Z",
    "Y",
    "",
]


restricted_unit_expansion = {
    "Hz": [prefix + "Hz" for prefix in std_prefixes],
    "hertz": [prefix + "hertz" for prefix in std_prefixes],
    "rad/s": ["radian/s", "rad/s"],
    "radian/s": ["rad/s", "radian/s"],
    "rpm": ["revolutions_per_minute", "rpm"],
    "rps": ["revolutions_per_second", "rps"],
    "cps": ["counts_per_second", "cps"],
}


def build_restricted_conversions(conversions, unit_expansion):

    """This function generates required final restricted mappings."""

    keys = set([i[0] for i in conversions])
    restricted_units_dict = {unit[0]: [] for unit in conversions}

    for key in keys:
        temp_list = [unit_expansion[i] for i in keys.difference(set([key]))]
        for temp in temp_list:
            restricted_units_dict[key] += temp
    for key in keys:
        restricted_units_dict[key] = list(set(restricted_units_dict[key]))
    return restricted_units_dict


restricted_units = build_restricted_conversions(
    restricted_conversions, restricted_unit_expansion
)


class Quantity:

    """This class instantiates physical quantities using their real values and
    units.

    All the instances of this class are converted to base SI units
    system. Any conversion between "Hz", "hertz", "rad/s", "radian/s",
    "rpm", "rps", "cps" is restricted.
    """

    def __init__(self, real_value, units_string):
        self.value = real_value
        self.unit = units_string
        self._quantity = quantity(self.value, self.unit)
        self._base_si_quantity = self._quantity.to_base_units()
        self._restricted_conversions = restricted_units

    def __float__(self):
        return Quantity(self.value, self.unit)

    def __str__(self):
        return f'({self.value}, "{self.unit}")'

    def __repr__(self):
        return f'(Quantity ({self.value}, "{self.unit}"))'

    def convertTo(self, to_unit):

        """This method checks the compatibility between current instance unit
        and user provided unit, if both of them are compatible, then only it
        performs required conversion otherwise raises a Value Error."""

        if (
            self.unit in self._restricted_conversions.keys()
            and to_unit in self._restricted_conversions[self.unit]
        ):
            raise ValueError(
                f"Conversion between '{self.unit}' and '{to_unit}' is restricted."
            )

        user_unit = Unit(to_unit)

        if not self._quantity.is_compatible_with(user_unit):
            raise ValueError("Units are not compatible")

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
        if self.unit in self._restricted_conversions.keys():
            raise ValueError("This arithmetic operation is restricted")

        if isinstance(other, Quantity):
            temp = self._base_si_quantity + other._quantity
        elif isinstance(other, int) or isinstance(other, float):
            temp = quantity(
                self._base_si_quantity.magnitude + other, self._base_si_quantity.units
            )
        return Quantity(temp.magnitude, temp.units)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if self.unit in self._restricted_conversions.keys():
            raise ValueError("This arithmetic operation is restricted")

        if isinstance(other, Quantity):
            temp = self._base_si_quantity - other._quantity
        elif isinstance(other, int) or isinstance(other, float):
            temp = quantity(
                self._base_si_quantity.magnitude - other, self._base_si_quantity.units
            )
        return Quantity(temp.magnitude, temp.units)

    def __rsub__(self, other):
        if self.unit in self._restricted_conversions.keys():
            raise ValueError("This arithmetic operation is restricted")

        if isinstance(other, Quantity):
            temp = other._quantity - self._base_si_quantity
        elif isinstance(other, int) or isinstance(other, float):
            temp = quantity(
                other - self._base_si_quantity.magnitude, self._base_si_quantity.units
            )
        return Quantity(temp.magnitude, temp.units)
