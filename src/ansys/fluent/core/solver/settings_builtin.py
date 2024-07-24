"""Solver settings."""

from ansys.fluent.core.session_solver import Solver


class _SingletonSettings:
    def __new__(cls, solver: Solver):
        obj = solver.settings
        for comp in cls.path.split("."):
            obj = getattr(obj, comp)
        return obj


class _NamedObjectSettings(_SingletonSettings):
    def __new__(cls, solver: Solver, name: str):
        obj = super().__new__(cls, solver)
        return obj[name]


class viscous(_SingletonSettings):
    """Viscous settings."""

    path = "setup.models.viscous"


class boundary_conditions(_SingletonSettings):
    """Boundary conditions settings."""

    path = "setup.boundary_conditions"


class boundary_condition(_NamedObjectSettings):
    """Boundary condition settings."""

    path = "setup.boundary_conditions"


class velocity_inlet(_NamedObjectSettings):
    """Velocity inlet settings."""

    path = "setup.boundary_conditions"
