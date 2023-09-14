import ansys.fluent.core.quantity as q


class UnitSystem:
    """Initializes a unit system based on user-defined units or a pre-definned unit
    system.

    Parameters
    ----------
    name: str
        Custom name associated with a user-defined unit system.
    base_units: list
        Custom units associated with a user-defined unit system.
    unit_sys: str
        Pre-defined unit system.

    Methods
    -------
    convert()
        Converts from one unit system to to given unit system.

    Returns
    -------
    Quantity instance.
    """

    def __init__(self, name: str = None, base_units: list = None, unit_sys: str = None):
        self._units_table = q.UnitsTable()

        if name and unit_sys or base_units and unit_sys:
            raise UnitSystemError.EXCESSIVE_PARAMETERS()

        if base_units:
            if len(base_units) != q.Dimensions.max_dim_len():
                raise UnitSystemError.BASE_UNITS_LENGTH(len(base_units))

            for idx, unit in enumerate(base_units):
                if unit not in self._units_table.fundamental_units:
                    raise UnitSystemError.UNIT_UNDEFINED(unit)

                if (idx + 1) != self._units_table.dimension_order[
                    self._units_table.fundamental_units[unit]["type"]
                ]:
                    raise UnitSystemError.UNIT_ORDER(
                        t1=list(self._units_table.dimension_order.keys())[idx],
                        o1=idx + 1,
                        t2=self._units_table.fundamental_units[unit]["type"],
                        o2=self._units_table.dimension_order[
                            self._units_table.fundamental_units[unit]["type"]
                        ],
                    )

            self._name = name
            self._base_units = base_units

        if unit_sys is not None:
            if unit_sys not in self._units_table.unit_systems:
                raise UnitSystemError.INVALID_UNIT_SYS(unit_sys)

            self._name = unit_sys
            self._base_units = self._units_table.unit_systems[unit_sys]

    def convert(self, quantity: q.Quantity) -> q.Quantity:
        """Perform unit system conversions.

        Parameters
        ----------
        quantity : Quantity
            Desired quantity object to convert.

        Returns
        -------
        Quantity
            Quantity object containing desired unit system conversion.
        """

        new_dim = q.Dimensions(
            dimensions=quantity.dimensions, unit_sys=self._base_units
        )

        _, si_multiplier, si_offset = self._units_table.si_data(new_dim.units)
        new_value = (quantity.si_value / si_multiplier) - si_offset

        return q.Quantity(value=new_value, units=new_dim.units)

    @property
    def name(self):
        """Name associated with unit system."""
        return self._name

    @property
    def base_units(self):
        """Units associated with unit system."""
        return self._base_units


class UnitSystemError(ValueError):
    """Custom unit system errors."""

    def __init__(self, err):
        super().__init__(err)

    @classmethod
    def EXCESSIVE_PARAMETERS(cls):
        return cls(
            "UnitSystem only accepts 1 of the following parameters: (name, base_units) or (unit_sys)."
        )

    @classmethod
    def BASE_UNITS_LENGTH(cls, len):
        return cls(
            f"The `base_units` argument must contain 9 units, currently there are {len}."
        )

    @classmethod
    def UNIT_UNDEFINED(cls, unit):
        return cls(
            f"`{unit}` is an undefined unit. To use `{unit}` add it to the `fundamental_units` table within cfg.yaml."
        )

    @classmethod
    def UNIT_ORDER(cls, t1, o1, t2, o2):
        return cls(
            f"Expected unit of type: `{t1}` (order: {o1}), received unit of type: `{t2}` (order: {o2})."
        )

    @classmethod
    def INVALID_UNIT_SYS(cls, sys):
        return cls(f"`{sys}` is not a supported unit system.")
