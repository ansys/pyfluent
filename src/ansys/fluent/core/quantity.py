from collections import OrderedDict


class _UnitsTable(object):
    fundamental_units = {
        "kg": "M",
        "g": "M",
        "lb": "M",
        "lbm": "M",
        "slug": "M",
        "m": "L",
        "cm": "L",
        "ft": "L",
        "in": "L",
        "s": "T",
        "A": "I",
        "K": "Temp",
        "C": "Temp",
        "F": "Temp",
        "R": "Temp",
        "mol": "N",
        "cd": "J",
        "sr": "SAngle",
        "radian": "Angle",
        "degree": "Angle",
    }

    derived_units = {
        "N": "kg m s^-2",
        "Pa": "N m^-2",
        "W": "N m s^-1",
        "J": "N m",
        "V": "A ohm",
        "F": "N m V^-2",
        "H": "N m A^-2",
        "S": "ohm^-1",
        "Wb": "N m A^-1",
        "T": "Wb m^-2",
        "dyne": "g cm s^-2",
        "erg": "dyne cm",
        "pdl": "lbm ft s^-2",
        "BTU": "J",
        "psi": "lbf in^-2",
        "lbf": "slug ft s^-2",
        "psf": "lbf ft^-2",
        "ohm": "kg m^2 s^-3 A^-2",
        "Hz": "s^-1",
    }

    derived_units_with_conversion_factor = {
        "l": (0.001, "m^3"),
        "gal": (0.0037854117839999993, "m^3"),
        "BTU": (1055.056, "J"),
    }

    multipliers = {
        "d": 10**-1,
        "c": 10**-2,
        "m": 10**-3,
        "μ": 10**-6,
        "n": 10**-9,
        "p": 10**-12,
        "f": 10**-15,
        "a": 10**-18,
        "z": 10**-21,
        "y": 10**-24,
        "da": 10**1,
        "h": 10**2,
        "k": 10**3,
        "M": 10**6,
        "G": 10**9,
        "T": 10**12,
        "P": 10**15,
        "E": 10**18,
        "Z": 10**21,
        "Y": 10**24,
    }

    dimension_order = OrderedDict(
        [
            ("Mass", "M"),
            ("Length", "L"),
            ("Time", "T"),
            ("Temperature", "Temp"),
            ("Angle", "Angle"),
            ("ChemicalAmount", "N"),
            ("Light", "J"),
            ("Current", "I"),
            ("SolidAngle", "SAngle"),
            ("", ""),
        ]
    )

    conversion_map = {
        "kg": 1,
        "g": 0.001,
        "lb": 0.45359237,
        "lbm": 0.45359237,
        "slug": 14.59390293720637,
        "m": 1,
        "cm": 0.01,
        "ft": 0.30479999999999996,
        "in": 0.0254,
        "s": 1,
        "A": 1,
        "mol": 1,
        "cd": 1,
        "sr": 1,
        "radian": 1,
        "degree": 0.017453292519943295,
        "K": 1,
        "C": 1,
        "F": 0.5555555555555556,
        "R": 0.5555555555555556,
    }

    si_map = {
        "kg": "kg",
        "g": "kg",
        "lb": "kg",
        "lbm": "kg",
        "slug": "kg",
        "m": "m",
        "cm": "m",
        "ft": "m",
        "in": "m",
        "s": "s",
        "A": "A",
        "mol": "mol",
        "cd": "cd",
        "sr": "sr",
        "radian": "radian",
        "degree": "radian",
        "K": "K",
        "C": "K",
        "F": "K",
        "R": "K",
        "": "",
    }

    offset_conversions = {
        "K": 1,
        "C": 274.15,
        "F": 255.92777777777778,
        "R": 0.5555555555555556,
    }

    offset_dict = {
        "K": {"C": 274.15, "F": 255.92777777777778, "R": 0.5555555555555556},
        "C": {"K": -272.15, "F": -17.2222222222222, "R": -272.59444444444443},
        "F": {"C": 33.79999999999993, "K": -457.87, "R": -458.67},
        "R": {"C": 493.4699999999999, "F": 460.66999999999996, "K": 1.7999999999999998},
    }


def get_si_conversion_factor(unit_str):
    return (
        _UnitsTable.conversion_map[unit_str]
        if unit_str in _UnitsTable.conversion_map.keys()
        else 1
    )


def filter_multiplier(unit_str, predicate=None):
    result = False
    matched = ""
    for item in _UnitsTable.multipliers.keys():
        result = predicate(item, unit_str) if predicate else item == unit_str
        if result:
            matched = item
            result = True
            temp_unit_str = unit_str[len(item) :]
            if (
                temp_unit_str in _UnitsTable.fundamental_units
                or temp_unit_str in _UnitsTable.derived_units
            ):
                break
            else:
                result = False
                continue
    return result, matched


def remove_multiplier(unit_str):
    has_multiplier, prefix = filter_multiplier(
        unit_str, lambda item, unit: len(unit) > 1 and unit.startswith(item)
    )
    if has_multiplier:
        unit_str = unit_str[len(prefix) :]
    return unit_str


class Unit(object):
    def __init__(self, unit_str):
        self._unit = unit_str
        self._si_multiplier = 1
        self._si_offset = 0
        self._si_unit = ""
        self._computemultipliers_and_offsets(unit_str, 1)
        self._reduce_to_si_unit(self._si_unit)

    @property
    def user_unit(self):
        return self._unit

    @property
    def si_factor(self):
        return self._si_multiplier

    @property
    def si_unit(self):
        return self._si_unit

    def __call__(self):
        return self.user_unit

    def _reduce_to_si_unit(self, unit_str):
        term_power_dict = OrderedDict()
        unit_split = unit_str.split(" ")

        for term in unit_split:
            if "^" in term:
                term_split = term.split("^")
                if term_split[0] in term_power_dict.keys():
                    term_power_dict[term_split[0]] += float(term_split[1])
                else:
                    term_power_dict[term_split[0]] = float(term_split[1])
            else:
                if term in term_power_dict.keys():
                    term_power_dict[term] += 1
                else:
                    term_power_dict[term] = 1

        self._si_unit = ""

        for key, power in term_power_dict.items():
            spacechar = " " if len(self._si_unit) > 0 else ""
            if power > 1 or power < 0:
                self._si_unit += spacechar + key + "^" + str(power)
            else:
                self._si_unit += spacechar + key

    def _computemultipliers_and_offsets(self, unit_str, power):
        if len(unit_str) == 0:
            return

        unit_list = unit_str.split(" ")

        for term in unit_list:
            unit_str = term
            term_power = 1

            if "^" in unit_str:
                unit_str, term_power = unit_str[: unit_str.index("^")], float(
                    unit_str[unit_str.index("^") + 1 :]
                )

            term_power *= power
            has_multiplier = not (
                unit_str in _UnitsTable.fundamental_units
                or unit_str in _UnitsTable.derived_units
            )

            if has_multiplier:
                _, prefix = filter_multiplier(
                    unit_str, lambda item, unit: len(unit) > 1 and unit.startswith(item)
                )

                if len(prefix):
                    self._si_multiplier *= _UnitsTable.multipliers[prefix] ** term_power

                unit_str = remove_multiplier(unit_str)

            if unit_str in _UnitsTable.fundamental_units:
                spacechar = " " if len(self._si_unit) > 0 else ""

                if term_power > 1 or term_power < 0:
                    self._si_unit += (
                        spacechar + _UnitsTable.si_map[unit_str] + "^" + str(term_power)
                    )
                else:
                    self._si_unit += spacechar + _UnitsTable.si_map[unit_str]

                self._si_multiplier *= get_si_conversion_factor(unit_str) ** term_power

            elif unit_str in _UnitsTable.derived_units_with_conversion_factor:
                (
                    conversion_factor,
                    unit_str,
                ) = _UnitsTable.derived_units_with_conversion_factor[unit_str]
                self._si_multiplier *= conversion_factor**term_power
                self._computemultipliers_and_offsets(unit_str, term_power)
            elif unit_str in _UnitsTable.derived_units:
                self._computemultipliers_and_offsets(
                    _UnitsTable.derived_units[unit_str], term_power
                )


class Dimension(object):
    def __init__(self, unit_str):
        self._dimensions = {
            "M": 0.0,
            "L": 0.0,
            "T": 0.0,
            "Temp": 0.0,
            "I": 0.0,
            "N": 0.0,
            "J": 0.0,
            "Angle": 0.0,
            "SAngle": 0.0,
            "": 0.0,
        }
        self._parser(unit_str)

    def _add_or_update_dimension(self, dim_dict):
        for key in dim_dict.keys():
            self._dimensions[key] += dim_dict[key]

    def _parser(self, unit, power=1):
        if len(unit) == 0:
            return

        unit_list = unit.split(" ")
        for term in unit_list:
            unit_dim = ""
            has_multiplier = not (
                term in _UnitsTable.fundamental_units
                or term in _UnitsTable.derived_units
            )
            unit_str = remove_multiplier(term) if has_multiplier else term
            term_power = 1

            if "^" in term:
                unit_str, term_power = term[: term.index("^")], float(
                    term[term.index("^") + 1 :]
                )
                has_multiplier = not (
                    unit_str in _UnitsTable.fundamental_units
                    or unit_str in _UnitsTable.derived_units
                )
                unit_str = remove_multiplier(unit_str) if has_multiplier else unit_str

            term_power *= power
            unit_dim = self._get_dim(unit_str, term_power)

            if unit_dim != None:
                self._add_or_update_dimension(unit_dim)

    def get_dimensions_dict(self):
        return self._dimensions

    def _get_dim(self, unit_str, power):
        if unit_str in _UnitsTable.fundamental_units:
            return {_UnitsTable.fundamental_units[unit_str]: power}
        elif unit_str in _UnitsTable.derived_units:
            self._parser(_UnitsTable.derived_units[unit_str], power)
        elif unit_str in _UnitsTable.derived_units_with_conversion_factor:
            _, unit_str = _UnitsTable.derived_units_with_conversion_factor[unit_str]
            self._parser(unit_str, power)
        else:
            raise ValueError("Not implemented")


def get_si_unit_from_dim(dim_list):
    si_unit = ""
    dim_to_unit_map = {
        "M": "kg",
        "L": "m",
        "T": "s",
        "Temp": "K",
        "I": "A",
        "N": "mol",
        "J": "cd",
        "Angle": "radian",
        "SAngle": "sr",
        "": "",
    }
    for key, power in zip(_UnitsTable.dimension_order.values(), dim_list):
        unit_str = dim_to_unit_map[key]
        spacechar = " " if len(si_unit) > 0 else ""
        if power > 1 or power < 0:
            si_unit += spacechar + unit_str + "^" + str(power)
        elif power == 1:
            si_unit += spacechar + unit_str
    return si_unit


class Quantity:
    """This class instantiates physical quantities using their real values and
    units.

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

    getDimensions(unit)
        Extracts dimensions from unit.

    isDimensionless()
        Determines type of quantity.

    Returns
    -------
    Quantity instance.

    All the instances of this class are converted to base SI units system to have
    consistency in all arithmetic operations.
    """

    def __init__(self, real_value, unit_str):
        self._value = float(real_value)
        self._unit = Unit(unit_str)
        self._dimension = Dimension(unit_str)

    @property
    def value(self):
        return self._value

    @property
    def unit(self):
        return self._unit.user_unit

    @value.setter
    def value(self, val):
        self._value = val

    @property
    def dimension(self):
        return self._dimension

    @property
    def si_value(self):
        return self._unit.si_factor * self._value

    @property
    def si_unit(self):
        return self._unit.si_unit

    def is_dimension_less(self):
        return all([value == 0 for value in self.get_dimensions_list()])

    def get_dimensions_list(self):
        dims = self._dimension.get_dimensions_dict()
        return [
            dims[_UnitsTable.dimension_order[key]]
            for key in _UnitsTable.dimension_order.keys()
        ]

    def to(self, to_unit_str):
        temp_quantity = Quantity(1, to_unit_str)

        curr_unit_dim_obj = self.dimension
        to_unit_dim_obj = temp_quantity.dimension

        if (
            curr_unit_dim_obj.get_dimensions_dict()
            != to_unit_dim_obj.get_dimensions_dict()
        ):
            raise ValueError(
                f"Incompatible conversion from {self.unit} : to {to_unit_str}"
            )
        else:
            pass

        curr_unit_obj = self._unit
        to_unit_obj = temp_quantity._unit
        temp_quantity.value = (
            curr_unit_obj.si_factor / to_unit_obj.si_factor
        ) * self.value

        return temp_quantity

    def _get_si_unit(self, other, func):
        curr_dim = self.get_dimensions_list()
        other_dim = other.get_dimensions_list()
        temp_dim = [func(curr_dim[i], other_dim[i]) for i in range(len(other_dim))]
        temp_unit = get_si_unit_from_dim(temp_dim)
        return temp_unit

    def __pow__(self, exponent):
        new_dims = list(
            map(lambda x: x * exponent if x != 0 else x, self.get_dimensions_list())
        )
        new_si_unit = get_si_unit_from_dim(new_dims)
        new_si_value = pow(self.si_value, exponent)
        return Quantity(new_si_value, new_si_unit)

    def __float__(self):
        return float(self.si_value)

    def __str__(self):
        return f'({self.value}, "{self.unit}")'

    def __repr__(self):
        return f'(Quantity ({self.value}, "{self.unit}"))'

    def __mul__(self, other):
        if isinstance(other, Quantity):
            temp_value = self.si_value * other.si_value
            temp_unit = self._get_si_unit(other, lambda x, y: x + y)
            return Quantity(temp_value, temp_unit)
        elif isinstance(other, int) or isinstance(other, float):
            temp = Quantity(self.si_value * other, self.si_unit)
            return temp

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, Quantity):
            temp_value = self.si_value / other.si_value
            temp_unit = self._get_si_unit(other, lambda x, y: x - y)
            return Quantity(temp_value, temp_unit)
        elif isinstance(other, int) or isinstance(other, float):
            temp = Quantity(self.si_value / other, self.si_unit)
            return temp

    def __add__(self, other):
        if isinstance(other, Quantity):
            temp_value = self.si_value + other.si_value
        elif self.is_dimension_less() and (
            isinstance(other, int) or isinstance(other, float)
        ):
            temp_value = self.si_value + other
        else:
            raise ValueError(f"Quantity{(self.value, self.unit)} is not dimensionless.")
        return Quantity(temp_value, self.si_unit)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, Quantity):
            temp_value = self.si_value - other.si_value
        elif self.is_dimension_less() and (
            isinstance(other, int) or isinstance(other, float)
        ):
            temp_value = self.si_value - other
        else:
            raise ValueError(f"Quantity{(self.value, self.unit)} is not dimensionless.")
        return Quantity(temp_value, self.si_unit)

    def __rsub__(self, other):
        return Quantity(other, "") - self
