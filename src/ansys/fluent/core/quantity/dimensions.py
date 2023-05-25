from ansys.fluent.core.quantity.units_table import UnitsTable


class Dimensions(object):
    """ """

    def __init__(self, unit_str):
        self._units_table = UnitsTable()
        self._unit_str = unit_str

    def dim_to_unit_str(dimensions: list) -> str:
        """ """
        dimensions = [float(dim) for dim in ((9 - len(dimensions)) * [0])]
        si_order = ["kg", "m", "s", "K", "A", "mol", "cd", "radian", "sr"]
        unit_str = ""

        for dim in range(len(dimensions)):
            if dimensions[dim] == 1.0:
                unit_str += si_order[dim] + " "
            elif dimensions[dim] != 0.0:
                unit_str += si_order[dim] + "^" + str(int(dimensions[dim])) + " "

        return unit_str[:-1]

    def unit_str_to_dim():
        """"""
        pass
