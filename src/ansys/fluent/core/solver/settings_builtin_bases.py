"""Base classes for builtin setting classes."""

from typing import Protocol, runtime_checkable

from ansys.fluent.core.solver.flobject import NamedObject, SettingsBase
from ansys.fluent.core.solver.settings_builtin_data import DATA
from ansys.fluent.core.utils.fluent_version import FluentVersion


@runtime_checkable
class Solver(Protocol):
    """Solver session class for type hinting."""

    settings: SettingsBase


def _get_settings_root(settings_source: SettingsBase | Solver):
    def is_root_obj(obj):
        return isinstance(obj, SettingsBase) and obj.parent is None

    if is_root_obj(settings_source):
        return settings_source
    elif isinstance(settings_source, Solver) and is_root_obj(settings_source.settings):
        return settings_source.settings
    else:
        raise TypeError(
            f"{settings_source} is not a Settings root or a Solver session object."
        )


def _get_settings_obj(settings_root, builtin_settings_obj):
    builtin_cls_name = builtin_settings_obj.__class__.__name__
    obj = settings_root
    path = DATA[builtin_cls_name][1]
    if isinstance(path, dict):
        version = FluentVersion(obj.version)
        path = path.get(version)
        if path is None:
            raise RuntimeError(
                f"{builtin_cls_name} is not supported in Fluent version {version}."
            )
    comps = path.split(".")
    for i, comp in enumerate(comps):
        obj = SettingsBase.__getattribute__(obj, comp)  # bypass InactiveObjectError
        if i < len(comps) - 1 and isinstance(obj, NamedObject):
            obj_name = getattr(builtin_settings_obj, comp)
            obj = obj[obj_name]
    return obj


class _SingletonSetting:
    # Covers both groups and named-object containers
    def __init__(self, settings_source: SettingsBase | Solver | None = None, **kwargs):
        self.__dict__.update(dict(settings_source=None) | kwargs)
        if settings_source is not None:
            self.settings_source = settings_source

    def __setattr__(self, name, value):
        if name == "settings_source":
            settings_root = _get_settings_root(value)
            obj = _get_settings_obj(settings_root, self)
            self.__class__ = obj.__class__
            self.__dict__.clear()
            self.__dict__.update(obj.__dict__ | dict(settings_source=settings_root))
        else:
            super().__setattr__(name, value)


class _NonCreatableNamedObjectSetting:
    def __init__(
        self, name: str, settings_source: SettingsBase | Solver | None = None, **kwargs
    ):
        self.__dict__.update(dict(settings_source=None, name=name) | kwargs)
        if settings_source is not None:
            self.settings_source = settings_source

    def __setattr__(self, name, value):
        if name == "settings_source":
            settings_root = _get_settings_root(value)
            obj = _get_settings_obj(settings_root, self)
            obj = obj[self.name]
            self.__class__ = obj.__class__
            self.__dict__.clear()
            self.__dict__.update(obj.__dict__ | dict(settings_source=settings_root))
        else:
            super().__setattr__(name, value)


class _CreatableNamedObjectSetting:
    def __init__(
        self,
        settings_source: SettingsBase | Solver | None = None,
        name: str | None = None,
        new_instance_name: str | None = None,
        **kwargs,
    ):
        if name and new_instance_name:
            raise ValueError("Cannot specify both name and new_instance_name.")
        self.__dict__.update(
            dict(settings_source=None, name=name, new_instance_name=new_instance_name)
            | kwargs
        )
        if settings_source is not None:
            self.settings_source = settings_source

    def __setattr__(self, name, value):
        if name == "settings_source":
            settings_root = _get_settings_root(value)
            obj = _get_settings_obj(settings_root, self)
            if self.name:
                obj = obj[self.name]
            elif self.new_instance_name:
                obj = obj.create(self.new_instance_name)
            else:
                obj = obj.create()
            self.__class__ = obj.__class__
            self.__dict__.clear()
            self.__dict__.update(obj.__dict__ | dict(settings_source=settings_root))
        else:
            super().__setattr__(name, value)
