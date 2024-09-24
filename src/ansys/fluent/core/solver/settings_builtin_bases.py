"""Base classes for builtin setting classes."""

from typing import Optional

from ansys.fluent.core.session_solver import Solver
from ansys.fluent.core.solver.flobject import SettingsBase
from ansys.fluent.core.solver.settings_builtin_data import DATA


def _get_obj(solver: Solver, cls_name: str):
    if not isinstance(solver, Solver):
        raise TypeError(f"{solver} is not a Solver object.")
    path = DATA[cls_name][1]
    obj = solver.settings
    if isinstance(path, dict):
        version = solver.get_fluent_version()
        path = path.get(version)
        if path is None:
            raise RuntimeError(
                f"{cls_name} is not supported in Fluent version {version}."
            )
    for comp in path.split("."):
        obj = SettingsBase.__getattribute__(obj, comp)  # bypass InactiveObjectError
    return obj


class _SingletonSetting:
    def __init__(self, solver: Optional[Solver] = None):
        self.__dict__.update(dict(solver=None))
        if solver is not None:
            self.solver = solver

    def __setattr__(self, name, value):
        if name == "solver":
            obj = _get_obj(value, self.__class__.__name__)
            self.__class__ = obj.__class__
            self.__dict__.clear()
            self.__dict__.update(obj.__dict__)
        else:
            super().__setattr__(name, value)


class _NonCreatableNamedObjectSetting:
    def __init__(self, name: str, solver: Optional[Solver] = None):
        self.__dict__.update(dict(solver=None, name=name))
        if solver is not None:
            self.solver = solver

    def __setattr__(self, name, value):
        if name == "solver":
            obj = _get_obj(value, self.__class__.__name__)
            obj = obj[self.name]
            self.__class__ = obj.__class__
            self.__dict__.clear()
            self.__dict__.update(obj.__dict__)
        else:
            super().__setattr__(name, value)


class _CreatableNamedObjectSetting:
    def __init__(
        self,
        solver: Optional[Solver] = None,
        name: Optional[str] = None,
        new_instance_name: Optional[str] = None,
    ):
        if name and new_instance_name:
            raise ValueError("Cannot specify both name and new_instance_name.")
        self.__dict__.update(
            dict(solver=None, name=name, new_instance_name=new_instance_name)
        )
        if solver is not None:
            self.solver = solver

    def __setattr__(self, name, value):
        if name == "solver":
            obj = _get_obj(value, self.__class__.__name__)
            if self.name:
                obj = obj[self.name]
            elif self.new_instance_name:
                obj = obj.create(self.new_instance_name)
            else:
                obj = obj.create()
            self.__class__ = obj.__class__
            self.__dict__.clear()
            self.__dict__.update(obj.__dict__)
        else:
            super().__setattr__(name, value)
