from typing import Optional, Tuple

import ansys.fluent.core.quantity as q
from ansys.fluent.core.quantity._constants import _QuantityType
from ansys.fluent.core.quantity.units import parse_temperature_units


class Quantity(float):
    """Quantity instantiates physical quantities using their real values and units. All
    the instances of this class are converted to base SI units system to have
    consistency in arithmetic operations.

    Parameters
    ----------
    value : int | float
        Real value of quantity.
    units : str
        Unit string representation of quantity.
    quantity_map : dict
        Quantity map representation of quantity.
    dimensions : list
        Dimensions representation of quantity.

    Methods
    -------
    to()
        Converts to given unit string.

    Returns
    -------
    Quantity instance.
    """

    def __new__(
        cls, value, units=None, quantity_map=None, dimensions=None, _type_hint=None
    ):
        if (
            (units and quantity_map)
            or (units and dimensions)
            or (quantity_map and dimensions)
        ):
            raise QuantityError.EXCESSIVE_PARAMETERS()

        _units_table = q.UnitsTable()
        _value = float(value)

        if units is not None:
            _unit = units

        if quantity_map:
            units = q.QuantityMap(quantity_map).units
            _unit = units

        if dimensions:
            _dimensions = q.Dimensions(dimensions=dimensions)
            _unit = _dimensions.units

        _, si_multiplier, si_offset = _units_table.si_data(units=_unit)
        _si_value = (_value + si_offset) * si_multiplier

        return float.__new__(cls, _si_value)

    def __init__(
        self, value, units=None, quantity_map=None, dimensions=None, _type_hint=None
    ):
        if (
            (units and quantity_map)
            or (units and dimensions)
            or (quantity_map and dimensions)
        ):
            raise QuantityError.EXCESSIVE_PARAMETERS()

        self._units_table = q.UnitsTable()
        self._value = float(value)

        if units is not None:
            self._unit = units
            self._dimensions = q.Dimensions(units=units)

        if quantity_map:
            units = q.QuantityMap(quantity_map).units
            self._unit = units
            self._dimensions = q.Dimensions(units=units)

        if dimensions:
            self._dimensions = q.Dimensions(dimensions=dimensions)
            self._unit = self._dimensions.units

        self._type = self._units_table.get_type(self._unit)
        if (
            self._type == _QuantityType.temperature
            and _type_hint == _QuantityType.temperature_difference
        ):
            self._type = _QuantityType.temperature_difference

        si_units, si_multiplier, si_offset = self._units_table.si_data(units=self._unit)

        self._si_units = si_units

        # Well, this is going to have to be a hack, but we
        # need to fix the wider design to do this properly
        self._fix_temperature_units()

        self._si_value = (self.value + si_offset) * si_multiplier

    def _arithmetic_precheck(self, __value) -> str:
        """Validate dimensions of quantities.

        Parameters
        ----------
        __value : Quantity | int | float
            Value modifying current quantity object.
        Returns
        -------
        str
            SI unit string of new quantity.
        """
        # Cannot perform operations between quantities with incompatible dimensions
        if isinstance(__value, Quantity) and (self.dimensions != __value.dimensions):
            raise QuantityError.INCOMPATIBLE_DIMENSIONS(self.units, __value.units)
        # Cannot perform operations on a non-dimensionless quantity
        if not isinstance(__value, Quantity) and (not self.is_dimensionless):
            raise QuantityError.INCOMPATIBLE_VALUE(__value)

    def _temp_precheck(self) -> Optional[str]:
        """Validate units for temperature differences.

        Returns
        -------
        str | None
            Units of temperature difference.
        """
        if self.type in [
            _QuantityType.temperature,
            _QuantityType.temperature_difference,
        ]:
            return "delta_K"

    @property
    def value(self):
        """Real value."""
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    @property
    def units(self):
        """Unit string."""
        return self._unit

    @property
    def si_value(self):
        """SI conversion value."""
        return self._si_value

    @property
    def si_units(self):
        """SI conversion unit string."""
        return self._si_units

    @property
    def dimensions(self):
        """Dimensions."""
        return self._dimensions.dimensions

    @property
    def is_dimensionless(self) -> bool:
        """Check if quantity is dimensionless."""
        return all([dim == 0.0 for dim in self.dimensions])

    @property
    def type(self):
        """Type."""
        return self._type

    def to(self, to_units: str) -> "Quantity":
        """Perform quantity conversions.

        Parameters
        ----------
        to_units : str
            Desired unit to be converted to.

        Returns
        -------
        Quantity
            Quantity object containing desired quantity conversion.
        """

        if not isinstance(to_units, str):
            raise TypeError("`to_units` should be a `str` type.")

        new_type = None

        if self.type == _QuantityType.temperature_difference:
            new_type = _QuantityType.temperature_difference
            to_units = Quantity._fix_these_temperature_units(
                to_units, ignore_exponent=True
            )

        # Retrieve all SI required SI data and perform conversion
        _, si_multiplier, si_offset = self._units_table.si_data(to_units)
        new_value = (self.si_value / si_multiplier) - si_offset

        new_obj = Quantity(value=new_value, units=to_units, _type_hint=new_type)

        # Confirm conversion compatibility
        self._arithmetic_precheck(new_obj)

        return new_obj

    def __str__(self):
        return f'({self.value}, "{self.units}")'

    def __repr__(self):
        return f'Quantity ({self.value}, "{self.units}")'

    def __pow__(self, __value):
        temp_dimensions = [dim * __value for dim in self.dimensions]
        new_si_value = self.si_value**__value
        new_dimensions = q.Dimensions(dimensions=temp_dimensions)
        return Quantity(value=new_si_value, units=new_dimensions.units)

    def __mul__(self, __value):
        if isinstance(__value, Quantity):
            temp_dimensions = [
                dim + __value.dimensions[idx] for idx, dim in enumerate(self.dimensions)
            ]
            new_si_value = self.si_value * __value.si_value
            new_dimensions = q.Dimensions(dimensions=temp_dimensions)
            new_units = new_dimensions.units
            return Quantity(
                value=new_si_value,
                units=new_units,
                _type_hint=self._determine_new_type(__value),
            )

        if isinstance(__value, (float, int)):
            new_units = self._temp_precheck() or self.si_units
            return Quantity(value=self.si_value * __value, units=new_units)

    def __rmul__(self, __value):
        return self.__mul__(__value)

    def __truediv__(self, __value):
        if isinstance(__value, Quantity):
            temp_dimensions = [
                dim - __value.dimensions[idx] for idx, dim in enumerate(self.dimensions)
            ]
            new_si_value = self.si_value / __value.si_value
            new_dimensions = q.Dimensions(dimensions=temp_dimensions)
            new_units = new_dimensions.units
            result = Quantity(value=new_si_value, units=new_units)
            # HACK
            convert_to_temp_difference = (
                _QuantityType.temperature == result.type
                and __value.type
                in (_QuantityType.temperature, _QuantityType.temperature_difference)
            )
            if convert_to_temp_difference:
                result._type = _QuantityType.temperature_difference
            return result

        if isinstance(__value, (float, int)):
            new_units = self.si_units
            return Quantity(value=self.si_value / __value, units=new_units)

    def __rtruediv__(self, __value):
        return Quantity(__value, "") / self

    def __add__(self, __value):
        self._arithmetic_precheck(__value)
        new_units = self._temp_precheck() or self.si_units
        new_value = float(self) + float(__value)
        return Quantity(value=new_value, units=new_units)

    def __radd__(self, __value):
        return self.__add__(__value)

    def __sub__(self, __value):
        self._arithmetic_precheck(__value)
        new_units = self._temp_precheck() or self.si_units
        new_value = float(self) - float(__value)
        return Quantity(value=new_value, units=new_units)

    def __rsub__(self, __value):
        return self.__sub__(__value)

    def __neg__(self):
        return Quantity(-self.value, self.units)

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

    @staticmethod
    def _fix_these_temperature_units(
        units: str, ignore_exponent: bool, units_to_search: Tuple[str] = None
    ) -> str:
        new_units = parse_temperature_units(units, ignore_exponent, units_to_search)
        return " ".join(
            ("delta_" + term[0])
            if (term[1] and not term[0].startswith("delta_"))
            else term[0]
            for term in new_units
        )

    def _fix_temperature_units(self):
        # HACK
        ignore_exponent = self.type == _QuantityType.temperature_difference
        self._unit = Quantity._fix_these_temperature_units(self._unit, ignore_exponent)
        self._si_units = Quantity._fix_these_temperature_units(
            self._si_units, ignore_exponent, ("K",)
        )

    def _determine_new_type(self, other=None):
        # HACK the only concern here is to fix the loss of
        # Temperature Difference information. Return
        # Temperature Difference if it's involved else None
        # such that the caller figures it out in the usual way
        if _QuantityType.temperature_difference in (self.type, other.type):
            return _QuantityType.temperature_difference


class QuantityError(ValueError):
    """Custom quantity errors."""

    def __init__(self, err):
        super().__init__(err)

    @classmethod
    def EXCESSIVE_PARAMETERS(cls):
        return cls(
            "Quantity only accepts 1 of the following parameters: (units) or (quantity_map) or (dimensions)."
        )

    @classmethod
    def INCOMPATIBLE_DIMENSIONS(cls, from_unit, to_unit):
        return cls(f"`{from_unit}` and `{to_unit}` have incompatible dimensions.")

    @classmethod
    def INCOMPATIBLE_VALUE(cls, value):
        return cls(f"`{value}` is incompatible with the current quantity object.")

    @classmethod
    def UNKNOWN_UNITS(cls, unit: str):
        return cls(f"`{unit}` is an unknown or unconfigured unit.")
