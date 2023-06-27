import ansys.fluent.core.quantity as q


class UnitSystem:
    def __init__(self, name: str = None, base_units: list = None, unit_sys: str = None):
        self._units_table = q.UnitsTable()

        if name and unit_sys:
            raise ValueError(
                "Cannot define `name` when using a pre-defined unit system."
            )

        if base_units and unit_sys:
            raise ValueError(
                "Cannot define `base_units` when using a pre-defined unit system."
            )

        if base_units:
            if len(base_units) != 9:
                raise ValueError(
                    f"`base_units` must contain 9 units, currently there are {len(base_units)}."
                )

            for idx, unit in enumerate(base_units):
                if unit not in self._units_table.fundamental_units:
                    raise ValueError(
                        f"`{unit}` is an undefined unit. To use `{unit}` add it to the `fundamental_units` table within `quantity_config.yaml`."
                    )

                if (idx + 1) != self._units_table.dimension_order[
                    self._units_table.fundamental_units[unit]["type"]
                ]:
                    raise ValueError(
                        f"Expected unit of type: `{list(self._units_table.dimension_order.keys())[idx]}` (order: {idx+1}), received unit of type: `{self._units_table.fundamental_units[unit]['type']}` (order: {self._units_table.dimension_order[self._units_table.fundamental_units[unit]['type']]})."
                    )

            self._name = name
            self._base_units = base_units

        if unit_sys:
            if unit_sys not in self._units_table.unit_systems:
                raise ValueError(f"`{unit_sys}` is not a supported unit system.")

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

        return q.Quantity(value=quantity.value, units=new_dim.units)
