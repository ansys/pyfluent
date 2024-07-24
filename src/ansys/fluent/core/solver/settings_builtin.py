"""Solver settings."""

from ansys.fluent.core.session_solver import Solver


class _SingletonSettings:
    def __new__(cls, solver: Solver):
        obj = solver.settings
        for comp in cls.path.split("."):
            obj = getattr(obj, comp)
        return obj


class _NamedObjectSettings:
    def __new__(cls, solver: Solver, name: str):
        obj = solver.settings
        for comp in cls.path.split("."):
            obj = getattr(obj, comp)
        return obj[name]


def _create_singleton_settings(name: str, path: str):
    return type(name, (_SingletonSettings,), {"path": path})


def _create_named_object_settings(name: str, path: str):
    return type(name, (_NamedObjectSettings,), {"path": path})


viscous = _create_singleton_settings("viscous", "setup.models.viscous")
boundary_conditions = _create_singleton_settings(
    "boundary_conditions", "setup.boundary_conditions"
)
boundary_condition = _create_named_object_settings(
    "boundary_condition", "setup.boundary_conditions"
)
velocity_inlet = _create_named_object_settings(
    "velocity_inlet", "setup.boundary_conditions"
)
