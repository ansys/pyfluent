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


def _get_settings_root(settings_source: Solver | SettingsBase[object]) -> Settings:
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
    settings_root: Settings,
    builtin_cls_db_name: str,
    *,
    extras: dict[str, Any] | None = None,
) -> SettingsBase[object]:
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
            obj_name = (extras or {}).get(comp)
            if obj_name is None:
                raise RuntimeError(
                    f"Named object key for '{comp}' is required to resolve"
                    f" '{builtin_cls_db_name}'."
                )
            obj = obj[obj_name]
    return obj


def _swap(instance, settings_root: Settings, obj: SettingsBase[object]) -> None:
    """Replace *instance* in-place with the underlying settings object *obj*."""
    instance.__class__ = obj.__class__
    instance.__dict__.clear()
    instance.__dict__.update(obj.__dict__)
    instance.__dict__["settings_source"] = settings_root


class _SettingsObjectMixin:
    _db_name: str
    settings_source: SettingsBase[object] | None  # None when deferred

    def _should_materialize(self) -> bool:
        # Singletons always materialize; subclasses override for named objects.
        return True

    def _init_settings_instance(
        self, parent: SettingsBase[object]
    ) -> SettingsBase[object]:
        raise NotImplementedError

    def _init_deferred_settings_instance(
        self, parent: SettingsBase[object]
    ) -> SettingsBase[object]:
        return self._init_settings_instance(parent)


class _SingletonSetting(_SettingsObjectMixin):
    # Covers groups, named-object containers and commands.
    def __init__(
        self,
        settings_source: SettingsBase[object] | Solver | None = None,
        /,
        **kwargs: Any,
    ):
        # Store extras (e.g. parametric_studies="...") for intermediate NamedObject paths.
        self.__dict__.update(kwargs)
        effective_source = _get_active_session() or settings_source
        if effective_source is None:
            raise TypeError("No active session or settings source provided.")
        settings_root = _get_settings_root(effective_source)
        parent = _get_settings_obj(settings_root, self._db_name, extras=self.__dict__)
        obj = self._init_settings_instance(parent)
        _swap(self, settings_root, obj)

    def _init_settings_instance(
        self, parent: SettingsBase[object]
    ) -> SettingsBase[object]:
        return parent


class _NonCreatableNamedObjectSetting(_SettingsObjectMixin):
    def __init__(
        self,
        settings_source: SettingsBase[object] | Solver | None = None,
        /,
        *,
        name: str | None = None,
    ):
        # Store name only if not None to avoid polluting __dict__
        if name is not None:
            self.__dict__["name"] = name

        effective_source = _get_active_session() or settings_source
        if effective_source is None:
            raise TypeError("No active session or settings source provided.")
        db_name_to_use = DATA[self.__class__._db_name][2]
        if db_name_to_use is not None:
            self.__dict__["_db_name"] = db_name_to_use
        settings_root = _get_settings_root(effective_source)
        if self._should_materialize():
            # Create extras dict with navigation params only (exclude wrapper params)
            extras = {
                k: v for k, v in self.__dict__.items() if k not in {"name", "kwargs"}
            }
            parent = _get_settings_obj(settings_root, self._db_name, extras=extras)
            obj = self._init_settings_instance(parent)
            _swap(self, settings_root, obj)
            if db_name_to_use is not None:
                self.__dict__["_db_name"] = db_name_to_use
        else:
            # Container proxy: store session for get()/all().
            self.__dict__["settings_source"] = settings_root

    def _init_settings_instance(
        self, parent: SettingsBase[object]
    ) -> SettingsBase[object]:
        name = self.__dict__.get("name")
        if name:
            return parent[name]
        else:
            return parent

    def _should_materialize(self) -> bool:
        return self.__dict__.get("name") is not None

    def all(self) -> list[Self]:
        """Return a list of all instances of this object in Fluent."""
        return cast(
            list[Self],
            list(
                _get_settings_obj(
                    self.settings_source,
                    DATA[self._db_name][2],
                )["*"]
            ),
        )

    def get(self, name: str) -> Self:
        """Get and return the named instance of this object in Fluent.

        Parameters
        ----------
        name
            Name of the object to get, if applicable, can be a wildcard pattern.
        """
        return cast(
            Self,
            _get_settings_obj(self.settings_source, self._db_name)[name],
        )


class _CreatableNamedObjectSetting(_SettingsObjectMixin):
    def __init__(
        self,
        settings_source: SettingsBase[object] | Solver | None = None,
        /,
        *,
        new_instance_name: str | None = None,
        name: str | None = None,
        **kwargs: Any,
    ):

        # Store only non-None wrapper params; avoid polluting __dict__ with None values
        if new_instance_name is not None:
            self.__dict__["new_instance_name"] = new_instance_name
        if name is not None:
            self.__dict__["name"] = name
        # For proxy delegation, store only navigation kwargs (not wrapper-specific ones)
        self.__dict__.update(kwargs)
        self.__dict__["kwargs"] = kwargs

        effective_source = _get_active_session() or settings_source
        if effective_source is None:
            raise TypeError("No active session or settings source provided.")
        settings_root = _get_settings_root(effective_source)
        if self._should_materialize():
            # Create extras dict with navigation params only (exclude wrapper params)
            extras = {
                k: v
                for k, v in self.__dict__.items()
                if k not in {"new_instance_name", "name", "kwargs"}
            }
            parent = _get_settings_obj(settings_root, self._db_name, extras=extras)
            obj = self._init_settings_instance(parent)
            _swap(self, settings_root, obj)
        else:
            # Container proxy mode: store settings source without creating instance
            self.__dict__["settings_source"] = settings_root

    def _should_materialize(self) -> bool:
        return (
            self.__dict__.get("new_instance_name") is not None
            or self.__dict__.get("name") is not None
        )

    def _init_settings_instance(
        self, parent: SettingsBase[object]
    ) -> SettingsBase[object]:
        new_instance_name = self.__dict__.get("new_instance_name")
        name = self.__dict__.get("name")
        if new_instance_name:
            instance = parent.create(new_instance_name)
            if self.__dict__.get("kwargs"):
                instance.set_state(self.__dict__["kwargs"])
            return instance
        elif name:
            return parent[name]
        else:
            return parent  # container proxy path -- not reached via eager init

    def get(self, name: str) -> Self:
        """Get and return a named instance of this object in Fluent.

        Parameters
        ----------
        name
            Name of the object to get, if applicable, can be a wildcard pattern.
        """
        return cast(
            Self,
            _get_settings_obj(self.settings_source, self._db_name)[name],
        )

    def all(self) -> list[Self]:
        """Return a list of all instances of this object in Fluent."""
        return cast(
            list[Self],
            list(
                _get_settings_obj(
                    self.settings_source,
                    DATA[self._db_name][2],
                )["*"]
            ),
        )

    def create(
        self,
        name: str | None = None,
        **kwargs: Any,
    ) -> Self:
        """Create and return an instance of this object in Fluent.

        Parameters
        ----------
        name
            Name of the new object to create. If omitted, a default name will be assigned by Fluent.
        **kwargs
            Additional attributes to set on the created object. This only works for direct value assignments, not for nested objects.
        """
        # Only pass name if it's not None to avoid sending name=None to Fluent

        return cast(
            Self,
            _get_settings_obj(self.settings_source, self._db_name).create(
                name, **kwargs
            ),
        )


_CommandSetting = _SingletonSetting
