"""Base classes for builtin setting classes."""

from ansys.fluent.core.session_solver import Solver
from ansys.fluent.core.solver.settings_builtin_data import DATA


class _SingletonSetting:
    def __new__(cls, solver: Solver):
        obj = solver.settings
        path = DATA[cls.__name__][1]
        if isinstance(path, dict):
            version = solver.get_fluent_version()
            path = path.get(version)
            if path is None:
                raise RuntimeError(
                    f"{cls.__name__} is not supported in Fluent version {version}."
                )
        for comp in path.split("."):
            obj = getattr(obj, comp)
        return obj


class _NamedObjectSetting(_SingletonSetting):
    def __new__(cls, solver: Solver, name: str):
        obj = super().__new__(cls, solver)
        return obj[name]
