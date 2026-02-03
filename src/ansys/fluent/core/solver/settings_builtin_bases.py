# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Base classes for builtin setting classes."""

from typing import TYPE_CHECKING, Any, Protocol, cast, runtime_checkable

from typing_extensions import Self

from ansys.fluent.core.generated.solver.settings_261 import root as Settings
from ansys.fluent.core.solver.flobject import (
    InactiveObjectError,
    NamedObject,
    SettingsBase,
)
from ansys.fluent.core.solver.settings_builtin_data import DATA
from ansys.fluent.core.utils.context_managers import _get_active_session
from ansys.fluent.core.utils.fluent_version import FluentVersion


@runtime_checkable
class Solver(Protocol):
    """Solver session class for type hinting."""

    @property
    def settings(self) -> Settings:
        """The settings root object."""
        ...


def _get_settings_root(settings_source: Solver | SettingsBase[object]):
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
    builtin_cls_db_name = builtin_settings_obj._db_name
    obj = settings_root
    path = DATA[builtin_cls_db_name][1]
    found_path = None
    if isinstance(path, dict):
        version = FluentVersion(obj._version)
        for version_set, p in path.items():
            if version in version_set:
                found_path = p
                break
        if found_path is None:
            raise RuntimeError(f"{builtin_cls_db_name} is not supported in {version}.")
    elif isinstance(path, str):
        found_path = path
    comps = found_path.split(".")
    for i, comp in enumerate(comps):
        try:
            obj = getattr(obj, comp)
        except InactiveObjectError:
            raise InactiveObjectError(builtin_cls_db_name) from None
        if i < len(comps) - 1 and isinstance(obj, NamedObject):
            obj_name = getattr(builtin_settings_obj, comp)
            obj = obj[obj_name]
    return obj


class _SettingsObjectMixin:
    def __init__(
        self,
        defaults: dict,
        settings_source: Solver | None = None,
        **kwargs: Any,
    ):
        if (db_name := kwargs.pop("_db_name", None)) is not None:
            self._db_name = db_name  # used to change the cardinality in .all()
        active_session = _get_active_session()
        self.kwargs = kwargs
        self.__dict__.update(defaults)
        if (
            settings_source is not None
        ):  # after this the object is converted to a settings object
            self.settings_source = settings_source
        elif active_session:
            self.settings_source = active_session


class _SingletonSetting(_SettingsObjectMixin):
    # Covers groups, named-object containers and commands.
    def __init__(self, settings_source: Solver | None = None, **kwargs):
        super().__init__({"settings_source": None}, settings_source, **kwargs)

    if not TYPE_CHECKING:

        def __setattr__(self, name, value):
            if name == "settings_source":
                settings_root = _get_settings_root(value)
                obj = _get_settings_obj(settings_root, self)
                self.__class__ = obj.__class__
                self.__dict__.clear()
                self.__dict__.update(obj.__dict__ | {"settings_source": settings_root})
            else:
                super().__setattr__(name, value)


class _NonCreatableNamedObjectSetting(_SettingsObjectMixin):
    _db_name: str  # pyright: ignore[reportUninitializedInstanceVariable]

    def __init__(
        self,
        settings_source: Solver | None = None,
        name: str | None = None,
        **kwargs: Any,
    ):
        kwargs["_db_name"] = (
            DATA[self.__class__._db_name][2] if name is None else kwargs.get("_db_name")
        )  # initialise as the parent container
        super().__init__(
            {"settings_source": None, "name": name}, settings_source, **kwargs
        )

    if not TYPE_CHECKING:

        def __setattr__(self, name, value):
            if name == "settings_source":
                settings_root = _get_settings_root(value)
                obj = _get_settings_obj(settings_root, self)
                obj = obj[self.name]
                self.__class__ = obj.__class__
                self.__dict__.clear()
                self.__dict__.update(obj.__dict__ | {"settings_source": settings_root})
            else:
                super().__setattr__(name, value)

    @classmethod
    def all(cls, solver: Solver | None = None, /) -> list[Self]:
        """Return a list of all instances of this object in Fluent."""
        return cast(
            list[
                Self
            ],  # yes this looks like an unsafe cast but this works via clearing the instance's dict
            list(
                cast(
                    Any,
                    _NonCreatableNamedObjectSetting(
                        settings_source=solver,
                        name="*",
                        _db_name=DATA[cls._db_name][2],  # initialise parent container
                    ),
                ),
            ),
        )

    @classmethod
    def get(
        cls,
        settings_source: Solver | None = None,
        /,
        *,
        name: str,
    ) -> Self:
        """Get and return the named instance of this object in Fluent.

        Parameters
        ----------
        settings_source
            Something with a ``settings`` attribute. If omitted the active session is assumed from the :func:`using` context manager.
        name
            Name of the object to get, if applicable, can be a wildcard pattern.
        """
        return cls(settings_source=settings_source, name=name)


class _CreatableNamedObjectSetting(_SettingsObjectMixin):
    def __init__(
        self,
        settings_source: Solver | None = None,
        name: str | None = None,
        new_instance_name: str | None = None,
        _from_create: bool = False,
        **kwargs: Any,
    ):
        if name and new_instance_name:
            raise ValueError("Cannot specify both name and new_instance_name.")
        kwargs["_db_name"] = (
            DATA[self.__class__._db_name][2]
            if name is None and not _from_create
            else kwargs.get("_db_name")
        )  # initialise as the parent container
        super().__init__(
            {
                "settings_source": None,
                "name": name,
                "new_instance_name": new_instance_name,
            },
            settings_source,
            **kwargs,
        )

    @classmethod
    def get(
        cls,
        settings_source: Solver | None = None,
        /,
        *,
        name: str,
    ) -> Self:
        """Get and return a named instance of this object in Fluent.

        Parameters
        ----------
        settings_source
            Something with a ``settings`` attribute. If omitted the active session is assumed from the :func:`using` context manager.
        name
            Name of the object to get, if applicable, can be a wildcard pattern.
        """
        return cls(settings_source=settings_source, name=name)

    @classmethod
    def create(
        cls,
        settings_source: Solver | None = None,
        /,
        name: str | None = None,
        **kwargs: Any,
    ) -> Self:
        """Create and return an instance of this object in Fluent.

        Parameters
        ----------
        settings_source
            Something with a ``settings`` attribute. If omitted the active session is assumed from the :func:`using` context manager.
        name
            Name of the new object to create. If omitted, a default name will be assigned by Fluent.
        **kwargs
            Additional attributes to set on the created object. This only works for direct value assignments, not for nested objects.
        """
        root = _get_settings_root(
            settings_source or _get_active_session()
        )  # validate settings_source
        instance = _CreatableNamedObjectSetting(
            _from_create=True, new_instance_name=name, _db_name=DATA[cls._db_name][2]
        )

        obj = _get_settings_obj(root, instance)
        return obj.create(name=name, **kwargs)

    if not TYPE_CHECKING:

        def __setattr__(self, name, value):
            if name == "settings_source":
                settings_root = _get_settings_root(value)
                obj = _get_settings_obj(settings_root, self)
                if self.name:
                    obj = obj[self.name]
                elif (
                    self.new_instance_name or self._db_name == self.__class__._db_name
                ):  # create a new potentially anonymous instance
                    obj = obj.create(self.new_instance_name, **self.kwargs)
                self.__class__ = obj.__class__
                self.__dict__.clear()
                self.__dict__.update(obj.__dict__ | {"settings_source": settings_root})
            else:
                super().__setattr__(name, value)


_CommandSetting = _SingletonSetting
