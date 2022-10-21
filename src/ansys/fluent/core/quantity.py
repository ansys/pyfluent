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
    to(to_unit)
        Converts to given unit string.

    toSystem(baseSystem)
        Converts to given base system.

    getDimensions(unit)
        Extracts dimensions from unit.

    isDimensionless()
        Determines type of quantity.

    checkDimensionsMatch(quantity1, quantity2)
        Compares dimensions of 2 quantities.

    Returns
    -------
    Quantity instance.

    All the instances of this class are converted to base SI units system to have
    consistency in all arithmetic operations.
    """

    def __new__(cls, real_value, units_string):
        return float.__new__(cls, real_value)

    def __init__(self, real_value, units_string):
        float.__init__(real_value)
        self.value = self.__float__()
        self.unit = units_string

    def __str__(self):
        return f'({self.value}, "{self.unit}")'

    def __repr__(self):
        return f'(Quantity ({self.value}, "{self.unit}"))'
