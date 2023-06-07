import os

import yaml


class Quantity(float):
    """Quantity instantiates physical quantities using their real values and
    units. All the instances of this class are converted to base SI units system to have
    consistency in all arithmetic operations.


    Parameters
    ----------
    value : int | float
        Real value of quantity.
    unit_str : str
        Unit string representation of quantity.
    quantity_map : dict
        Quantity map representation of quantity.
    dimensions : list
        Dimensions representation of quantity.

    Properties
    ----------
    value : float
        Real value of quantity.
    unit_str : str
        Unit string representation of quantity.
    si_value : float
        SI value of quantity.
    si_unit_str : str
        SI unit string representation of quantity.
    dimensions : list
        Dimensions representation of quantity.
    type : str
        Type associated with quantity.

    Methods
    -------
    to(to_unit)
        Converts to given unit string.
    convert(to_sys)
        Converts to given unit system.

    Returns
    -------
    Quantity instance.
    """

    def __new__(cls, value, unit_str=None, quantity_map=None, dimensions=None):
        if (
            (unit_str and quantity_map)
            or (unit_str and dimensions)
            or (quantity_map and dimensions)
        ):
            raise ValueError(
                "Quantity only accepts 1 of the following: unit_str, quantity_map, dimensions"
            )

        _units_table = UnitsTable()
        _value = float(value)

        if unit_str or unit_str == "":
            _unit_string = unit_str

        if quantity_map:
            unit_str = QuantityMap(quantity_map).unit_str
            _unit_string = unit_str

        if dimensions:
            _dimensions = Dimensions(dimensions=dimensions)
            _unit_string = _dimensions.unit_str

        _type = _units_table.get_type(_unit_string)
        _, si_multiplier, si_offset = _units_table.si_data(unit_str=_unit_string)
        _si_value = _units_table.si_conversion(_value, _type, si_multiplier, si_offset)

        return float.__new__(cls, _si_value)

    def __init__(self, value, unit_str=None, quantity_map=None, dimensions=None):
        self._units_table = UnitsTable()
        self._value = float(value)

        if unit_str or unit_str == "":
            self._unit_string = unit_str
            self._dimensions = Dimensions(unit_str=unit_str)

        if quantity_map:
            unit_str = QuantityMap(quantity_map).unit_str
            self._unit_string = unit_str
            self._dimensions = Dimensions(unit_str=unit_str)

        if dimensions:
            self._dimensions = Dimensions(dimensions=dimensions)
            self._unit_string = self._dimensions.unit_str

        self._type = self._units_table.get_type(self._unit_string)

        si_unit_str, si_multiplier, si_offset = self._units_table.si_data(
            unit_str=self._unit_string
        )

        self._si_unit_str = si_unit_str[:-1]
        self._si_value = self._units_table.si_conversion(
            self._value, self._type, si_multiplier, si_offset
        )

    def _arithmetic_precheck(self, __value, caller=None) -> str:
        """Validate dimensions of quantities.

        Parameters
        ----------
        __value : Quantity | int | float
            Value modifying current quantity object.
        caller : str
            Name of caller function.
        Returns
        -------
        : str
            SI unit string of new quantity.
        """
        # Cannot perform operations between quantities with opposing dimensions
        if isinstance(__value, Quantity) and (self.dimensions != __value.dimensions):
            raise QuantityError(from_unit=self.unit_str, to_unit=__value.unit_str)
        # Cannot perform operations on a non-dimensionless quantity
        if (
            caller not in ["__mul__", "__truediv__"]
            and (any([dim != 0.0 for dim in self.dimensions]))
            and (not isinstance(__value, Quantity))
            and isinstance(__value, (float, int))
        ):
            raise TypeError(
                f"Error: '{__value}' is incompatible with the current quantity object."
            )

        return (
            "delta_K"
            if self.type in ["Temperature", "Temperature Difference"]
            else self.si_unit_str
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

        # Retrieve all SI required SI data and perform conversion
        _, si_multiplier, si_offset = self._units_table.si_data(to_unit_str)
        new_value = self._units_table.si_conversion(
            self.si_value, self.type, si_multiplier, si_offset, reverse=True
        )

        new_obj = Quantity(value=new_value, unit_str=to_unit_str)

        # Confirm conversion compatibility
        self._arithmetic_precheck(new_obj)

        return new_obj

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

        # Verify specified system is supported
        if to_sys not in ["SI", "CGS", "BT"]:
            raise ValueError(
                f"'{to_sys}' is not a supported unit system. Only 'SI', 'CGS', 'BT' are supported."
            )

        # Create new dimensions with desired unit system
        new_dim = Dimensions(dimensions=self.dimensions, unit_sys=to_sys)

        return Quantity(value=self.value, unit_str=new_dim.unit_str)

    def __str__(self):
        return f'({self.value}, "{self.unit_str}")'

    def __repr__(self):
        return f'Quantity ({self.value}, "{self.unit_str}")'

    def __pow__(self, __value):
        temp_dimensions = [dim * __value for dim in self.dimensions]
        new_si_value = self.si_value**__value
        new_dimensions = Dimensions(dimensions=temp_dimensions)
        return Quantity(value=new_si_value, unit_str=new_dimensions.unit_str)

    def __mul__(self, __value):
        new_unit_str = self._arithmetic_precheck(__value, "__mul__")
        if isinstance(__value, Quantity):
            temp_dimensions = [
                dim + __value.dimensions[idx] for idx, dim in enumerate(self.dimensions)
            ]
            new_si_value = self.si_value * __value.si_value
            new_dimensions = Dimensions(dimensions=temp_dimensions)
            new_unit_str = (
                new_unit_str if new_unit_str == "delta_K" else new_dimensions.unit_str
            )
            return Quantity(value=new_si_value, unit_str=new_unit_str)

        if isinstance(__value, (float, int)):
            return Quantity(value=self.si_value * __value, unit_str=new_unit_str)

    def __rmul__(self, __value):
        return self.__mul__(__value)

    def __truediv__(self, __value):
        new_unit_str = self._arithmetic_precheck(__value, "__truediv__")
        if isinstance(__value, Quantity):
            temp_dimensions = [
                dim - __value.dimensions[idx] for idx, dim in enumerate(self.dimensions)
            ]
            new_si_value = self.si_value / __value.si_value
            new_dimensions = Dimensions(dimensions=temp_dimensions)
            new_unit_str = (
                new_unit_str if new_unit_str == "delta_K" else new_dimensions.unit_str
            )
            return Quantity(value=new_si_value, unit_str=new_unit_str)

        if isinstance(__value, (float, int)):
            return Quantity(value=self.si_value / __value, unit_str=new_unit_str)

    def __rtruediv__(self, __value):
        return self.__truediv__(__value)

    def __add__(self, __value):
        new_unit_str = self._arithmetic_precheck(__value)
        new_value = float(self) + float(__value)
        return Quantity(value=new_value, unit_str=new_unit_str)

    def __radd__(self, __value):
        return self.__add__(__value)

    def __sub__(self, __value):
        new_unit_str = self._arithmetic_precheck(__value)
        new_value = float(self) - float(__value)
        return Quantity(value=new_value, unit_str=new_unit_str)

    def __rsub__(self, __value):
        return self.__sub__(__value)

    def __neg__(self):
        return Quantity(-self.value, self.unit_str)

    def __gt__(self, __value):
        self._arithmetic_precheck(__value)
        return float(self) > float(__value)

    def __ge__(self, __value):
        self._arithmetic_precheck(__value)
        return float(self) >= float(__value)

    def __lt__(self, __value):
        self._arithmetic_precheck(__value)
        return float(self) < float(__value)

    def __le__(self, __value):
        self._arithmetic_precheck(__value)
        return float(self) <= float(__value)

    def __eq__(self, __value):
        self._arithmetic_precheck(__value)
        return float(self) == float(__value)

    def __neq__(self, __value):
        self._arithmetic_precheck(__value)
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


class UnitsTable(object):
    """Initializes a UnitsTable object with all table values and unit string manipluation methods.

    Properties
    ----------
    api_quantity_map : dict
        Quantity map values from settings API.
    fundamental_units : dict
        Fundamental units and properties representing Mass, Length, Time, Current, Chemical Amount, Light, Solid Angle, Angle, Temperature and Temperature Difference.
    derived_units : dict
        Derived units and properties composed of fundamental units.
    multipliers : dict
        Multiplier prefixes and respective factors.

    Methods
    -------
    filter_unit_term()
        Separate multiplier, base, and power from a unit term.
    si_data()
        Compute the SI unit string, SI multiplier, and SI offset from a unit string of any type.
    si_converion()
        Perform SI conversion based on quantity type.
    condense()
        Condenses a unit string by collecting like-terms.
    get_type()
        Returns the type associated with a unit string.

    Returns
    -------
    UnitsTable instance.
    """

    def __init__(self):
        self._data: dict = self._get_data()
        self._api_quantity_map: dict = self._data["api_quantity_map"]
        self._fundamental_units: dict = self._data["fundamental_units"]
        self._derived_units: dict = self._data["derived_units"]
        self._multipliers: dict = self._data["multipliers"]

    def _get_data(self) -> dict:
        """Reads quantity data from json file.

        Returns
        -------
        : dict
            Quantity data loaded in from JSON file.
        """

        # Retrieve config yaml file within module
        file_path = os.path.relpath(__file__)
        file_dir = os.path.dirname(file_path)
        qc_path = os.path.join(file_dir, "utils/quantity_config.yaml")

        # Load config data
        with open(qc_path, "r") as qc_yaml:
            return yaml.safe_load(qc_yaml)

    def _has_multiplier(self, unit_term: str) -> bool:
        """Check if a unit term contains a multiplier.

        Parameters
        ----------
        unit_term : str
            Unit term of a unit string.

        Returns
        -------
        : bool
            Boolean of multiplier within unit_term.
        """
        # Check if the unit term is not an existing fundamental or derived unit.
        return not (
            (unit_term in self._fundamental_units) or (unit_term in self._derived_units)
        )

    def _si_map(self, unit_term: str) -> str:
        """Maps unit to SI unit equivalent.

        Parameters
        ----------
        unit_term : str
            Unit term of a unit string.

        Returns
        -------
        term : str
            SI unit equivalent.
        """
        # Retrieve type associated with unit term
        unit_term_type = self._fundamental_units[unit_term]["type"]

        # Find SI unit with same type as unit term
        for term, term_info in self._fundamental_units.items():
            if term_info["type"] == unit_term_type and term_info["factor"] == 1.0:
                return term

    @property
    def api_quantity_map(self):
        """Settings API quantity map values"""
        return self._api_quantity_map

    @property
    def fundamental_units(self):
        """Fundamental units"""
        return self._fundamental_units

    @property
    def derived_units(self):
        """Derived units"""
        return self._derived_units

    @property
    def multipliers(self):
        """Multipliers"""
        return self._multipliers

    def filter_unit_term(self, unit_term: str) -> tuple:
        """Separate multiplier, base, and power from a unit term.

        Parameters
        ----------
        unit_term : str
            Unit term of a unit string.

        Returns
        -------
        : tuple
            Tuple containing multiplier, base, and power of the unit term.
        """
        multiplier = ""
        power = 1.0

        # strip power from unit term
        if "^" in unit_term:
            power = float(unit_term[unit_term.index("^") + 1 :])
            unit_term = unit_term[: unit_term.index("^")]

        base = unit_term

        # strip multiplier and base from unit term
        if self._has_multiplier(unit_term):
            for mult in self._multipliers:
                if unit_term.startswith(mult):
                    if not self._has_multiplier(unit_term[len(mult) :]):
                        multiplier = mult
                        base = unit_term[len(mult) :]
                        break

        return multiplier, base, power

    def si_data(
        self,
        unit_str: str,
        power: float = None,
        si_unit_str: str = None,
        si_multiplier: float = None,
        si_offset: float = None,
    ) -> tuple:
        """Compute the SI unit string, SI multiplier, and SI offset.

        Parameters
        ----------
        unit_str : str
            Unit string representation of quantity.
        power : float
            Power of unit string
        si_unit_string : str
            SI unit string representation of quantity.
        si_multiplier : float
            SI multiplier of unit string.
        si_offset : float
            SI offset of a unit string.

        Returns
        -------
        : tuple
            Tuple containing si_unit_string, si_multiplier and si_offset.
        """

        # Initialize default values
        unit_str = unit_str or " "
        power = power or 1.0
        si_unit_str = si_unit_str or ""
        si_multiplier = si_multiplier or 1.0
        si_offset = si_offset or 0.0

        # Split unit string into terms and parse data associated with individual terms
        for term in unit_str.split(" "):
            unit_multiplier, unit_term, unit_term_power = self.filter_unit_term(term)

            unit_term_power *= power

            si_multiplier *= (
                self._multipliers[unit_multiplier] ** unit_term_power
                if unit_multiplier
                else 1.0
            )

            # Retrieve data associated with fundamental unit
            if unit_term in self._fundamental_units:
                si_offset = self._fundamental_units[unit_term]["offset"]

                if unit_term_power == 1.0:
                    si_unit_str += f"{self._si_map(unit_term)} "
                elif unit_term_power != 0.0:
                    si_unit_str += f"{self._si_map(unit_term)}^{unit_term_power} "

                si_multiplier *= (
                    self._fundamental_units[unit_term]["factor"] ** unit_term_power
                )

            # Retrieve derived unit composition unit string and factor.
            if unit_term in self._derived_units:
                si_multiplier *= (
                    self._derived_units[unit_term]["factor"] ** unit_term_power
                )

                # Recursively parse composition unit string
                si_unit_str, si_multiplier, si_offset = self.si_data(
                    unit_str=self._derived_units[unit_term]["composition"],
                    power=unit_term_power,
                    si_unit_str=si_unit_str,
                    si_multiplier=si_multiplier,
                    si_offset=si_offset,
                )

        return self.condense(si_unit_str), si_multiplier, si_offset

    def si_conversion(
        self,
        value: float,
        type: str,
        si_multiplier: float,
        si_offset: float,
        reverse: bool = False,
    ) -> float:
        """Performs SI conversion based on quantity type.

        Parameters
        ----------
        value : float
            Real value of quantity.
        type : str
            Quantity type.
        si_multiplier : float
            SI factor of quantity object.
        si_offset : float
            SI offset of quantity object.
        reverse : bool
            SI conversion direction. Setting reverse to `True` performs the inverse of a conversion.

        Returns
        -------
        : float
            SI value of quantity.
        """
        # Perform conversion from SI value
        if reverse:
            return (
                ((value / si_multiplier) - si_offset)
                if type == "Temperature"
                else (value / si_multiplier)
            )

        # Perform conversion to SI value
        return (
            ((value + si_offset) * si_multiplier)
            if type == "Temperature"
            else (value * si_multiplier)
        )

    def condense(self, unit_str: str) -> str:
        """Condenses a unit string by collecting like-terms.

        Parameters
        ----------
        unit_string : str
            Unit string to be simplified.

        Returns
        -------
        unit_string : str
            Simplified unit string.
        """
        terms_and_powers = {}

        # Split unit string into terms and parse data associated with individual terms
        for term in unit_str[:-1].split(" "):
            _, unit_term, unit_term_power = self.filter_unit_term(term)

            if unit_term in terms_and_powers:
                terms_and_powers[unit_term] += unit_term_power
            else:
                terms_and_powers[unit_term] = unit_term_power

        unit_str = ""

        # Concatenate unit string based on terms and powers (Removed duplications)
        for term, power in terms_and_powers.items():
            if power == 1.0:
                unit_str += f"{term} "
            else:
                unit_str += f"{term}^{power} "

        return unit_str

    def get_type(self, unit_str: str) -> str:
        """Returns the type associated with a unit string.

        Parameters
        ----------
        unit_str : str
            Unit string of quantity.

        Returns
        -------
        : str
            Type of quantity.
        """

        if unit_str == "":
            return "No Type"

        if unit_str in self.fundamental_units:
            return self.fundamental_units[unit_str]["type"]

        if unit_str in self.derived_units:
            return "Derived"

        if any([temp in unit_str for temp in ["K", "C", "F", "R"]]):
            return "Temperature Difference"

        return "Composite"


class Dimensions(object):
    """Initialize a Dimensions object using a dimensions list or a unit string.

    Parameters
    ----------
    unit_str: str
        Unit string of quantity.
    dimensions: list
        List of dimensions.

    Properties
    ----------
    unit_str : str
        Unit string of quantity.
    dimensions : list
        List of unit dimensions.

    Returns
    -------
    Dimensions instance.
    """

    def __init__(
        self, unit_str: str = None, dimensions: list = None, unit_sys: str = None
    ):
        self._units_table = UnitsTable()
        unit_sys = unit_sys or "SI"
        unit_str = unit_str or " "

        if unit_str:
            self._unit_str = unit_str
            self._dimensions = self._unit_str_to_dim(unit_str=unit_str)

        if dimensions:
            self._dimensions, self._unit_str = self._dim_to_unit_str(
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
        # Ensure dimensions list contains 9 terms
        dimensions = [float(dim) for dim in dimensions + ((9 - len(dimensions)) * [0])]
        sys_order = {
            "SI": ["kg", "m", "s", "K", "radian", "mol", "cd", "A", "sr"],
            "CGS": ["g", "cm", "s", "K", "radian", "mol", "cd", "A", "sr"],
            "BT": ["slug", "ft", "s", "R", "radian", "slugmol", "cd", "A", "sr"],
        }
        unit_str = ""

        # Define unit term and associated value from dimension with dimensions list
        for idx, dim in enumerate(dimensions):
            if dim == 1.0:
                unit_str += f"{sys_order[unit_sys][idx]} "
            elif dim != 0.0:
                unit_str += f"{sys_order[unit_sys][idx]}^{dim} "

        return dimensions, unit_str[:-1]

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

        power = power or 1.0
        dimensions = dimensions or [0.0] * 9

        # Split unit string into terms and parse data associated with individual terms
        for term in unit_str.split(" "):
            _, unit_term, unit_term_power = self._units_table.filter_unit_term(term)

            unit_term_power *= power

            # retrieve data associated with fundamental unit
            if unit_term in self._units_table.fundamental_units:
                idx = (
                    self._units_table.fundamental_units[unit_term]["dimension_order"]
                    - 1
                )
                dimensions[idx] += unit_term_power

            # Retrieve derived unit composition unit string and factor.
            if unit_term in self._units_table.derived_units:
                # Recursively parse composition unit string
                dimensions = self._unit_str_to_dim(
                    unit_str=self._units_table.derived_units[unit_term]["composition"],
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


class QuantityMap(object):
    """Creates a Quantity Map object based on a given quantity map.

    Parameters
    ----------
    quantity_map : dict
        Dictionary containing quantity map units and values.

    Properties
    ----------
    unit_str : str
        Unit string representation of quantity map.

    Returns
    -------
    QuantityMap instance.
    """

    def __init__(self, quantity_map):
        self._units_table = UnitsTable()
        self._unit_str = self._map_to_unit_str(quantity_map)

    def _map_to_unit_str(self, quantity_map: dict) -> str:
        """Convert a quantity map into a unit string.

        Parameters
        ----------
        quantity_map : dict
            Quantity map to be converted to unit string.

        Returns
        -------
        : str
            Unit string representation of quantity map.
        """
        unit_dict = {
            self._units_table.api_quantity_map[term]: power
            for term, power in quantity_map.items()
        }

        unit_str = ""

        # Split unit string into terms and parse data associated with individual terms
        for terms in unit_dict:
            for term in terms.split(" "):
                _, unit_term, unit_term_power = self._units_table.filter_unit_term(term)

                unit_term_power *= unit_dict[terms]

                if unit_term_power == 1.0:
                    unit_str += f"{unit_term} "
                elif unit_term_power != 0.0:
                    unit_str += f"{unit_term}^{unit_term_power} "

        return self._units_table.condense(unit_str=unit_str)[:-1]

    @property
    def unit_str(self):
        """Unit string representation of quantity map"""
        return self._unit_str
