"""Solver settings."""

from ansys.fluent.core.session_solver import Solver


class _SingletonSettings:
    def __new__(cls, solver: Solver, path: str):
        obj = solver.settings
        for comp in path.split("."):
            obj = getattr(obj, comp)
        return obj


class _NamedObjectSettings:
    def __new__(cls, solver: Solver, path: str, name: str):
        container = _SingletonSettings(solver, path)
        return container[name]


class viscous:
    """Viscous settings."""

    def __new__(self, solver: Solver):
        """Create a new viscous settings object.

        Parameters
        ----------
        solver : Solver
            Fluent solver object.
        """
        return _SingletonSettings(solver, "setup.models.viscous")


class boundary_conditions:
    """Boundary conditions settings."""

    def __new__(self, solver: Solver):
        """Create a new boundary conditions settings object.

        Parameters
        ----------
        solver : Solver
            Fluent solver object.
        """
        return _SingletonSettings(solver, "setup.boundary_conditions")


class boundary_condition:
    """Boundary condition settings."""

    def __new__(self, solver: Solver, name: str):
        """Create a new boundary condition settings object.

        Parameters
        ----------
        solver : Solver
            Fluent solver object.
        name : str
            Boundary condition name.
        """
        return _NamedObjectSettings(solver, "setup.boundary_conditions", name)


class velocity_inlet:
    """Velocity inlet settings."""

    def __new__(self, solver: Solver, name: str):
        """Create a new velocity inlet settings object.

        Parameters
        ----------
        solver : Solver
            Fluent solver object.
        name : str
            Velocity inlet name.
        """
        return _NamedObjectSettings(solver, "setup.boundary_conditions", name)
