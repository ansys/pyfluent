"""Base classes for builtin setting classes."""

from ansys.fluent.core.session_solver import Solver


class _SingletonSetting:
    def __new__(cls, solver: Solver):
        obj = solver.settings
        for comp in cls.path.split("."):
            obj = getattr(obj, comp)
        return obj


class _NamedObjectSetting(_SingletonSetting):
    def __new__(cls, solver: Solver, name: str):
        obj = super().__new__(cls, solver)
        return obj[name]
