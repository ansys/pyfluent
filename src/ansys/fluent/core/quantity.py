import pint
from pint import Unit

unit = pint.UnitRegistry(autoconvert_offset_to_baseunit=True, system="SI")
quantity = unit.Quantity

restricted_conversions = (
    ("Hz", "rad/s"),
    ("Hz", "radian/s"),
    ("Hz", "rpm"),
    ("Hz", "rps"),
    ("Hz", "cps"),
    ("hertz", "rad/s"),
    ("hertz", "radian/s"),
    ("hertz", "rpm"),
    ("hertz", "rps"),
    ("hertz", "cps"),
    ("rpm", "Hz"),
    ("rpm", "hertz"),
    ("rpm", "rad/s"),
    ("rpm", "radian/s"),
    ("rpm", "rps"),
    ("rpm", "cps"),
    ("rps", "Hz"),
    ("rps", "hertz"),
    ("rps", "rad/s"),
    ("rps", "radian/s"),
    ("rps", "rpm"),
    ("rps", "cps"),
    ("cps", "Hz"),
    ("cps", "hertz"),
    ("cps", "rad/s"),
    ("cps", "radian/s"),
    ("cps", "rpm"),
    ("cps", "rps"),
    ("rad/s", "Hz"),
    ("rad/s", "hertz"),
    ("rad/s", "rpm"),
    ("rad/s", "rps"),
    ("rad/s", "cps"),
    ("radian/s", "Hz"),
    ("radian/s", "hertz"),
    ("radian/s", "rpm"),
    ("radian/s", "rps"),
    ("radian/s", "cps"),
)

restricted_unit_expansion = {
    "Hz": [
        "yHz",
        "zHz",
        "aHz",
        "fHz",
        "pHz",
        "nHz",
        "uHz",
        "cHz",
        "dHz",
        "daHz",
        "hHz",
        "mHz",
        "kHz",
        "MHz",
        "GHz",
        "THz",
        "PHz",
        "EHz",
        "ZHz",
        "YHz",
        "Hz",
    ],
    "hertz": [
        "yhertz",
        "zhertz",
        "ahertz",
        "fhertz",
        "phertz",
        "nhertz",
        "uhertz",
        "chertz",
        "dhertz",
        "dahertz",
        "hhertz",
        "mhertz",
        "khertz",
        "Mhertz",
        "Ghertz",
        "Thertz",
        "Phertz",
        "Ehertz",
        "Zhertz",
        "Yhertz",
        "hertz",
    ],
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
    system. Any conversion between Hz, hertz, rad/s, radian/s,
    revolution/min, revolution/s, counts/s is restricted.
    """

    def __init__(self, real_value, units_string):
        self._real_value = real_value
        self._unit_string = units_string
        self._quantity = quantity(self._real_value, self._unit_string)
        self._base_si_quantity = self._quantity.to_base_units()
        self._restricted_conversions = restricted_units

    def __float__(self):
        return Quantity(self._real_value, self._unit_string)

    def __str__(self):
        return f'({self._real_value}, "{self._unit_string}")'

    def __repr__(self):
        return f'(Quantity ({self._real_value}, "{self._unit_string}"))'

    def __getitem__(self, unit):

        """This method checks the compatibility between current instance unit
        and user provided unit, if both of them are compatible, then only it
        performs required conversion otherwise raises a Value Error."""

        if (
            self._unit_string in self._restricted_conversions.keys()
            and unit in self._restricted_conversions[self._unit_string]
        ):
            raise ValueError(
                f"Conversion between '{self._unit_string}' and '{unit}' is restricted."
            )

        user_unit = Unit(unit)

        if not self._quantity.is_compatible_with(user_unit):
            raise ValueError("Units are not compatible")

        convert = self._quantity.to(unit)

        return Quantity(convert.magnitude, unit)

    def __mul__(self, other):

        if isinstance(other, Quantity):
            temp = self._base_si_quantity * other._quantity
        elif isinstance(other, int) or isinstance(other, float):
            temp = quantity(self._base_si_quantity * other, self._unit_string)
        return Quantity(temp.magnitude, temp.units)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):

        if isinstance(other, Quantity):
            temp = self._base_si_quantity / other._quantity
        elif isinstance(other, int) or isinstance(other, float):
            temp = quantity(self._base_si_quantity / other, self._unit_string)
        return Quantity(temp.magnitude, temp.units)

    def __add__(self, other):
        if self._unit_string in self._restricted_conversions.keys():
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
        if self._unit_string in self._restricted_conversions.keys():
            raise ValueError("This arithmetic operation is restricted")

        if isinstance(other, Quantity):
            temp = self._base_si_quantity - other._quantity
        elif isinstance(other, int) or isinstance(other, float):
            temp = quantity(
                self._base_si_quantity.magnitude - other, self._base_si_quantity.units
            )
        return Quantity(temp.magnitude, temp.units)

    def __rsub__(self, other):
        if self._unit_string in self._restricted_conversions.keys():
            raise ValueError("This arithmetic operation is restricted")

        if isinstance(other, Quantity):
            temp = other._quantity - self._base_si_quantity
        elif isinstance(other, int) or isinstance(other, float):
            temp = quantity(
                other - self._base_si_quantity.magnitude, self._base_si_quantity.units
            )
        return Quantity(temp.magnitude, temp.units)
