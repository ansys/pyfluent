"""Base classes for builtin setting classes."""

from typing import Optional

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


class _CreatableNamedObjectSetting(_SingletonSetting):
    def __new__(
        cls,
        solver: Solver,
        name: Optional[str] = None,
        new_instance_name: Optional[str] = None,
    ):
        if name and new_instance_name:
            raise ValueError("Cannot specify both name and new_instance_name.")
        obj = super().__new__(cls, solver)
        if name:
            return obj[name]
        elif new_instance_name:
            return obj.create(new_instance_name)
        else:
            return obj.create()


class _NonCreatableNamedObjectSetting(_SingletonSetting):
    def __new__(cls, solver: Solver, name: str):
        obj = super().__new__(cls, solver)
        return obj[name]
