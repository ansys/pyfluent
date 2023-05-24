from ansys.fluent.core.quantity.units import Units


class Quantity(float):
    """ """

    def __init__(self, real_value, unit_str=None, quantity_map=None, dimensions=None):
        """ """

        if (
            (unit_str and quantity_map)
            or (unit_str and dimensions)
            or (quantity_map and dimensions)
        ):
            raise ValueError("unit_str or quantity_map or dimension is allowed.")

        self._units = Units()
        self._value = float(real_value)

        if quantity_map:
            unit_str = self._units.get_unit_from_map(quantity_map)

        if dimensions:
            unit_str = self._units.get_unit_from_dim(dimensions)
