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
        "slugmol": "N",
        "cd": "Iv",
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
        "cal": "J",
        "delta_K": "K",
        "delta_C": "C",
        "delta_F": "F",
        "delta_R": "R",
    }

    derived_units_with_conversion_factor = {
        "l": (0.001, "m^3"),
        "gal": (0.0037854117839999993, "m^3"),
        "BTU": (1055.056, "J"),
        "cal": (4.184, "J"),
    }

    multipliers = {
        "d": 10**-1,
        "c": 10**-2,
        "m": 10**-3,
        "u": 10**-6,
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
            ("Light", "Iv"),
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
        "slugmol": 14593.9,
        "cd": 1,
        "sr": 1,
        "radian": 1,
        "degree": 0.017453292519943295,
        "K": 1,
        "C": 1,
        "F": 0.5555555555555556,
        "R": 0.5555555555555556,
        "delta_K": 1,
        "delta_C": 1,
        "delta_F": 0.5555555555555556,
        "delta_R": 0.5555555555555556,
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
        "slugmol": "mol",
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

    temperature_conversions = {
        # from : { to : formula }
        "C": {
            "K": lambda c: c + 273.15,
            "R": lambda c: (c + 273.15) * 1.8,
            "F": lambda c: c * 9 / 5 + 32,
            "C": lambda c: c,
        },
        "F": {
            "K": lambda f: (f - 32) * 5 / 9 + 273.15,
            "R": lambda f: f + 459.67,
            "F": lambda f: f,
            "C": lambda f: (f - 32) * 5 / 9,
        },
        "R": {
            "K": lambda r: r / 1.8,
            "R": lambda r: r,
            "F": lambda r: r - 459.67,
            "C": lambda r: (r - 491.67) / 1.8,
        },
        "K": {
            "K": lambda k: k,
            "R": lambda k: k * 1.8,
            "F": lambda k: k * 1.8 - 459.67,
            "C": lambda k: k - 273.15,
        },
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
        unit_str, lambda item, unit: len(unit) > 0.0 and unit.startswith(item)
    )
    if has_multiplier:
        unit_str = unit_str[len(prefix) :]
    return unit_str


def is_temperature_quantity(dim_obj):
    temp_dim = dim_obj["Temp"]
    total_dims_sum = sum([abs(val) for val in dim_obj.values()])
    return temp_dim == 1 and total_dims_sum == temp_dim


class Unit(object):
    def __init__(self, unit_str):
        self._unit = unit_str
        self._si_multiplier = 1
        self._si_offset = 0
        self._si_unit = ""
        self._offset_power = 1
        self._compute_multipliers(unit_str, 1)
        self._compute_offset(unit_str)
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

    @property
    def si_offset(self):
        return self._si_offset

    @property
    def offset_power(self):
        return self._offset_power

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
                    term_power_dict[term] += 1.0
                else:
                    term_power_dict[term] = 1.0

        self._si_unit = ""

        for key, power in term_power_dict.items():
            spacechar = " " if len(self._si_unit) > 0 else ""

            if power == 1.0:
                self._si_unit += spacechar + key
            elif power != 0.0:
                self._si_unit += (
                    spacechar
                    + key
                    + "^"
                    + str(int(power) if power.is_integer() else power)
                )
            else:
                self._si_unit += spacechar + key

    def _compute_multipliers(self, unit_str, power):
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
                    unit_str,
                    lambda item, unit: len(unit) > 0.0 and unit.startswith(item),
                )

                if len(prefix):
                    self._si_multiplier *= _UnitsTable.multipliers[prefix] ** term_power

                unit_str = remove_multiplier(unit_str)

            if unit_str in _UnitsTable.fundamental_units:
                spacechar = " " if len(self._si_unit) > 0 else ""

                if term_power == 1.0:
                    self._si_unit += spacechar + _UnitsTable.si_map[unit_str]
                elif term_power != 0.0:
                    self._si_unit += (
                        spacechar + _UnitsTable.si_map[unit_str] + "^" + str(term_power)
                    )
                elif term_power == 0.0:
                    self._si_unit += ""
                else:
                    self._si_unit += spacechar + _UnitsTable.si_map[unit_str]

                self._si_multiplier *= get_si_conversion_factor(unit_str) ** term_power

            elif unit_str in _UnitsTable.derived_units_with_conversion_factor:
                (
                    conversion_factor,
                    unit_str,
                ) = _UnitsTable.derived_units_with_conversion_factor[unit_str]
                self._si_multiplier *= conversion_factor**term_power
                self._compute_multipliers(unit_str, term_power)
            elif unit_str in _UnitsTable.derived_units:
                self._compute_multipliers(
                    _UnitsTable.derived_units[unit_str], term_power
                )

    @staticmethod
    def _power_sum(base, unit_str):
        if "^" in unit_str:
            return sum(
                [
                    float(term.split("^")[1])
                    for term in unit_str.split(" ")
                    if term.split("^")[0] == base
                ]
            )
        else:
            return 1.0

    def _compute_offset(self, unit_str):
        if unit_str == "C":
            self._si_offset = 273.15
            self._offset_power = self._power_sum("C", unit_str)
        elif unit_str == "F":
            self._si_offset = 255.3722
            self._offset_power = self._power_sum("F", unit_str)
        else:
            self._si_offset = 0
            self._offset_power = 1.0

    def _quantity_type(self):
        temperature_units = ["K", "C", "F", "R"]
        qty_type = ""
        for temp_unit in temperature_units:
            unit_power = Unit._power_sum(temp_unit, self._unit)
            if temp_unit in self._unit and unit_power == 1.0:
                qty_type = "Temperature"
            elif "delta" in self._unit:
                qty_type = "Temperature Difference"
            elif temp_unit in self._unit and unit_power not in [0.0, 1.0]:
                qty_type = "Temperature Difference"
        return qty_type


class Dimension(object):
    def __init__(self, unit_str):
        self._dimensions = {
            "M": 0.0,
            "L": 0.0,
            "T": 0.0,
            "Temp": 0.0,
            "I": 0.0,
            "N": 0.0,
            "Iv": 0.0,
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

    def as_dict(self):
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
    dim_to_unit_map = UnitSystem("SI").base_units()

    for key, power in zip(_UnitsTable.dimension_order.values(), dim_list):
        unit_str = dim_to_unit_map[key]
        spacechar = " " if len(si_unit) > 0 else ""
        if power == 1.0:
            si_unit += spacechar + unit_str
        elif power != 0.0:
            si_unit += (
                spacechar
                + unit_str
                + "^"
                + str(int(power) if power.is_integer() else power)
            )
    return si_unit


class UnitSystem:

    _dim_to_unit_sys_map = {
        "SI": {
            "M": "kg",
            "L": "m",
            "T": "s",
            "Temp": "K",
            "I": "A",
            "N": "mol",
            "Iv": "cd",
            "Angle": "radian",
            "SAngle": "sr",
            "": "",
        },
        "CGS": {
            "M": "g",
            "L": "cm",
            "T": "s",
            "Temp": "K",
            "I": "A",
            "N": "mol",
            "Iv": "cd",
            "Angle": "radian",
            "SAngle": "sr",
            "": "",
        },
        "BT": {
            "M": "slug",
            "L": "ft",
            "T": "s",
            "Temp": "R",
            "I": "A",
            "N": "slugmol",
            "Iv": "cd",
            "Angle": "radian",
            "SAngle": "sr",
            "": "",
        },
    }

    _supported_unit_sys = ("SI", "CGS", "BT")

    def __init__(self, unit_sys):
        self._unit_system = unit_sys.upper()

        if self._unit_system not in UnitSystem._supported_unit_sys:
            raise ValueError(
                "Unsupported unit system, only 'SI', 'CGS', 'BT' is allowed."
            )

    def _get_unit_from_dim(self, dim_list):
        unit = ""

        base_units = UnitSystem._dim_to_unit_sys_map[self._unit_system]
        for key, power in zip(_UnitsTable.dimension_order.values(), dim_list):
            spacechar = " " if len(unit) > 0 else ""
            if power == 1:
                unit += spacechar + base_units[key]
            elif power != 0:
                unit += (
                    spacechar
                    + base_units[key]
                    + "^"
                    + str(int(power) if power.is_integer() else power)
                )
        return unit

    def convert(self, quantity):
        if not isinstance(quantity, Quantity):
            raise TypeError("Not instance of Quantity.")
        dims = quantity.get_dimensions_list()
        unit_str = self._get_unit_from_dim(dims)
        return quantity.to(unit_str)

    def base_units(self):
        return UnitSystem._dim_to_unit_sys_map[self._unit_system]


class QuantityError(ValueError):
    def __init__(self, from_unit, to_unit):
        self.from_unit = from_unit
        self.to_unit = to_unit

    def __str__(self):
        return f"{self.unit} and {self.to_unit} have incompatible dimensions."


class Quantity(float):
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
    get_dimensions_list()
        Extracts dimensions from unit.

    is_dimensionless()
        Determines type of quantity.

    to(to_unit)
        Converts to given unit string.

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
        self._si_value = (
            self._unit.si_factor * self._value + self._unit.si_offset
        ) ** self._unit.offset_power
        self._si_unit = self._unit.si_unit
        self._type = self._unit._quantity_type()

    def __new__(cls, real_value, unit_str):
        _unit = Unit(unit_str)
        return float.__new__(
            cls, (_unit.si_factor * real_value + _unit.si_offset) ** _unit.offset_power
        )

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
    def type(self):
        return self._type

    @type.setter
    def type(self, type_str):
        self._type = type_str

    def is_dimensionless(self):
        return all([value == 0 for value in self.get_dimensions_list()])

    def get_dimensions_list(self):
        dims = self._dimension.as_dict()
        return [
            dims[_UnitsTable.dimension_order[key]]
            for key in _UnitsTable.dimension_order.keys()
        ]

    def to(self, to_unit_str):
        temp_quantity = Quantity(1, to_unit_str)

        curr_unit_dim_obj = self.dimension
        to_unit_dim_obj = temp_quantity.dimension

        if curr_unit_dim_obj.as_dict() != to_unit_dim_obj.as_dict():
            raise QuantityError(self.unit, to_unit_str)
        else:
            pass

        if is_temperature_quantity(curr_unit_dim_obj.as_dict()):
            return self._get_converted_temperature(to_unit_str)
        else:
            curr_unit_obj = self._unit
            to_unit_obj = temp_quantity._unit
            temp_quantity.value = (
                curr_unit_obj.si_factor / to_unit_obj.si_factor
            ) * self.value
            return temp_quantity

    def _get_converted_temperature(self, to_unit_str):
        from_unit_str = self.unit

        if "^" in from_unit_str:
            from_unit_str = from_unit_str.split("^")[0]

        if "^" in to_unit_str:
            to_unit_str = to_unit_str.split("^")[0]

        _, prefix = filter_multiplier(
            from_unit_str, lambda item, unit: len(unit) > 0.0 and unit.startswith(item)
        )
        from_unit_multiplier = (
            _UnitsTable.multipliers[prefix] if len(prefix) != 0 else 1.0
        )

        _, prefix = filter_multiplier(
            to_unit_str, lambda item, unit: len(unit) > 0.0 and unit.startswith(item)
        )
        to_unit_multiplier = (
            _UnitsTable.multipliers[prefix] if len(prefix) != 0 else 1.0
        )

        from_key = remove_multiplier(from_unit_str)
        to_key = remove_multiplier(to_unit_str)

        return Quantity(
            _UnitsTable.temperature_conversions[from_key][to_key](
                from_unit_multiplier * self.value
            )
            / to_unit_multiplier,
            to_unit_str,
        )

    def _get_si_unit(self, other, func):
        curr_dim = self.get_dimensions_list()
        other_dim = other.get_dimensions_list()
        temp_dim = [func(curr_dim[i], other_dim[i]) for i in range(len(other_dim))]
        temp_unit = get_si_unit_from_dim(temp_dim)
        return temp_unit

    def __pow__(self, exponent):
        new_dims = list(map(lambda x: x * exponent, self.get_dimensions_list()))
        new_si_unit = get_si_unit_from_dim(new_dims)
        new_si_value = pow(self._si_value, exponent)
        return Quantity(new_si_value, new_si_unit)

    def __str__(self):
        return f'({self.value}, "{self.unit}")'

    def __repr__(self):
        return f'Quantity ({self.value}, "{self.unit}")'

    def __mul__(self, other):
        if isinstance(other, Quantity):
            temp_value = self._si_value * other._si_value
            temp_unit = self._get_si_unit(other, lambda x, y: x + y)
            return Quantity(temp_value, temp_unit)
        elif isinstance(other, int) or isinstance(other, float):
            return Quantity(self._si_value * other, self._si_unit)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, Quantity):
            temp_value = self._si_value / other._si_value
            temp_unit = self._get_si_unit(other, lambda x, y: x - y)
            return Quantity(temp_value, temp_unit)
        elif isinstance(other, int) or isinstance(other, float):
            temp = Quantity(self._si_value / other, self._si_unit)
            return temp

    def __rtruediv__(self, other):
        if not isinstance(other, Quantity) and isinstance(other, float):
            return Quantity(other / self._si_value, self._si_unit)
        else:
            return other / self

    def validate_matching_dimensions(self, other):
        if isinstance(other, Quantity) and (
            self.get_dimensions_list() != other.get_dimensions_list()
        ):
            raise ValueError("Incompatible dimensions.")
        elif (
            (not self.is_dimensionless())
            and (not isinstance(other, Quantity))
            and isinstance(other, (float, int))
        ):
            raise TypeError("Incompatible quantities.")

    def __add__(self, other):
        self.validate_matching_dimensions(other)
        temp_value = float(self) + float(other)
        return Quantity(temp_value, self._si_unit)

    def __radd__(self, other):
        return Quantity(other, "") + self

    def __sub__(self, other):
        self.validate_matching_dimensions(other)
        temp_types = ["Temperature", "Temperature Difference"]
        if self.type in temp_types and other.type in temp_types:
            result = Quantity(float(self) - float(other), "delta_K")
            result.type = "Temperature Difference"
            return result
        temp_value = float(self) - float(other)
        return Quantity(temp_value, self._si_unit)

    def __rsub__(self, other):
        return Quantity(other, "") - self

    def __neg__(self):
        return Quantity(-self.value, self.unit)

    def __gt__(self, other):
        self.validate_matching_dimensions(other)
        return float(self) > float(other)

    def __ge__(self, other):
        self.validate_matching_dimensions(other)
        return float(self) >= float(other)

    def __lt__(self, other):
        self.validate_matching_dimensions(other)
        return float(self) < float(other)

    def __le__(self, other):
        self.validate_matching_dimensions(other)
        return float(self) <= float(other)

    def __eq__(self, other):
        self.validate_matching_dimensions(other)
        return float(self) == float(other)

    def __neq__(self, other):
        self.validate_matching_dimensions(other)
        return float(self) != float(other)
