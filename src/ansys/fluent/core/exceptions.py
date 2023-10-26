"""Custom common higher level exceptions."""


class DisallowedValuesError(ValueError):
    def __init__(self, error):
        super().__init__(error)


class InvalidArgument(ValueError):
    def __init__(self, error):
        super().__init__(error)
