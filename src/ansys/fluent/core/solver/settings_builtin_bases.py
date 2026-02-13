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

from typing import Any, Protocol, cast, runtime_checkable

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


def _get_settings_obj(
    settings_root: Settings, builtin_settings_obj: "_SettingsObjectMixin"
) -> SettingsBase[object]:
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
    else:
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
    _db_name: str
    kwargs: dict[str, Any]

    def __init__(
        self,
        settings_source: Solver | None = None,
        _db_name: str | None = None,
        **kwargs: Any,
    ):
        if _db_name is not None:
            self._db_name = _db_name  # used to change the cardinality in .all()
        active_session = _get_active_session()
        self.kwargs = kwargs
        if settings_source is not None:
            self.settings_source = settings_source
        elif active_session:
            self.settings_source = active_session
        else:
            raise RuntimeError("No active session and no settings_source provided.")

        settings_root = _get_settings_root(self.settings_source)
        parent = _get_settings_obj(settings_root, self)
        obj = self._init_settings_instance(parent)
        self.__class__ = obj.__class__
        self.__dict__.clear()
        self.__dict__.update(obj.__dict__ | {"settings_source": settings_root})

    def _init_settings_instance(
        self, parent: SettingsBase[object]
    ) -> SettingsBase[object]:
        raise NotImplementedError


class _SingletonSetting(_SettingsObjectMixin):
    # Covers groups, named-object containers and commands.
    def __init__(self, settings_source: Solver | None = None, **kwargs):
        super().__init__(settings_source, **kwargs)

    def _init_settings_instance(
        self, parent: SettingsBase[object]
    ) -> SettingsBase[object]:
        return parent


class _NonCreatableNamedObjectSetting(_SettingsObjectMixin):
    def __init__(
        self,
        settings_source: Solver | None = None,
        name: str | None = None,
        **kwargs: Any,
    ):
        self.name = name
        super().__init__(
            settings_source,
            name=name,
            **kwargs,
            _db_name=(  # initialise as the parent container
                (
                    DATA[self.__class__._db_name][2]
                    if name is None
                    else kwargs.get("_db_name")
                ),
            ),
        )

    def _init_settings_instance(
        self, parent: SettingsBase[object]
    ) -> SettingsBase[object]:
        return parent[self.name]

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
        solver: Solver | None = None,
        /,
        *,
        name: str,
    ) -> Self:
        """Get and return the named instance of this object in Fluent.

        Parameters
        ----------
        solver
            Something with a ``settings`` attribute. If omitted the active session is assumed from the :func:`using` context manager.
        name
            Name of the object to get, if applicable, can be a wildcard pattern.
        """
        return cls(settings_source=solver, name=name)


class _CreatableNamedObjectSetting(_SettingsObjectMixin):
    name: str | None
    new_instance_name: str | None

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
        self.name = name
        self.new_instance_name = new_instance_name

        super().__init__(
            settings_source,
            **kwargs,
            # _db_name=(  # initialise as the parent container
            #     DATA[self.__class__._db_name][2]
            #     if name is None and not _from_create
            #     else kwargs.get("_db_name"),
            # ),
        )

    @classmethod
    def get(
        cls,
        solver: Solver | None = None,
        /,
        *,
        name: str,
    ) -> Self:
        """Get and return a named instance of this object in Fluent.

        Parameters
        ----------
        solver
            Something with a ``settings`` attribute. If omitted the active session is assumed from the :func:`using` context manager.
        name
            Name of the object to get, if applicable, can be a wildcard pattern.
        """
        return cls(settings_source=solver, name=name)

    @classmethod
    def create(
        cls,
        solver: Solver | None = None,
        /,
        name: str | None = None,
        **kwargs: Any,
    ) -> Self:
        """Create and return an instance of this object in Fluent.

        Parameters
        ----------
        solver
            Something with a ``settings`` attribute. If omitted the active session is assumed from the :func:`using` context manager.
        name
            Name of the new object to create. If omitted, a default name will be assigned by Fluent.
        **kwargs
            Additional attributes to set on the created object. This only works for direct value assignments, not for nested objects.
        """
        root = _get_settings_root(
            solver or _get_active_session()
        )  # validate settings_source
        instance = _CreatableNamedObjectSetting(
            settings_source=root,
            _from_create=True,
            new_instance_name=name,
            _db_name=DATA[cls._db_name][2],
        )

        obj = _get_settings_obj(root, instance)
        return obj.create(name=name, **kwargs)

    def _init_settings_instance(
        self, parent: SettingsBase[object]
    ) -> SettingsBase[object]:
        if self.name:
            instance = parent[self.name]
        elif self.new_instance_name:  # create a new potentially anonymous instance
            instance = parent.create(self.new_instance_name, **self.kwargs)
        else:  # using _db_name
            instance = parent
        return instance


_CommandSetting = _SingletonSetting
