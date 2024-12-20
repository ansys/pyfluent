"""The top-level module of PyFluent providing solver-related functionality."""

try:
    from ansys.fluent.core.generated.solver.settings_builtin import *  # noqa: F401, F403
except (ImportError, AttributeError, SyntaxError):
    pass
