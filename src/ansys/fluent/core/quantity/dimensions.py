class Dimensions(object):
    """ """

    def __init__(self, dimensions):
        self._dimensions = dimensions
        self._unit_str = self._dim_to_unit_string(dimensions)

    def _dim_to_unit_string(dimensions: list) -> str:
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
