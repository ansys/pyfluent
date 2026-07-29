# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
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

"""High level object model wrapper."""

from collections.abc import Callable, Iterator, Sequence
import functools
import logging
from typing import Any, Iterable, TypeVar

from ansys.fluent.core.data_model_cache import DataModelCache, NameKey
from ansys.fluent.core.module_config import config
from ansys.fluent.core.services.abstract_object_model import AbstractObjectModel
from ansys.fluent.core.services.object_model_utilities import (
    Attribute,
    DisallowedFilePurpose,
    InvalidNamedObject,
    ReadOnlyObjectError,
    _get_completer_info,
    _InOutFile,
    _InputFile,
    _OutputFile,
    convert_path_to_se_path,
    convert_se_path_to_path,
    false_if_none,
    true_if_none,
)
from ansys.fluent.core.utils.fluent_version import FluentVersion

PyMenuT = TypeVar("PyMenuT", bound="PyMenu")
ValueT = None | bool | int | float | str | Sequence["ValueT"] | dict[str, "ValueT"]
Path = list[tuple[str, str]]
logger: logging.Logger = logging.getLogger("pyfluent.object_model")


class _FilterDatamodelNames:
    def __init__(self, service):
        self._filter_fn = getattr(service, "is_in_datamodel", None)

    def __call__(self, parent, names):
        if self._filter_fn is None:
            return names

        def validate_name(name):
            obj = getattr(parent, name)
            # might need to make this more flexible (e.g., enhanced workflow types)
            is_in_datamodel = isinstance(obj, (PyCommand, PyStateContainer))
            if is_in_datamodel:
                return self._filter_fn(parent.rules, convert_path_to_se_path(obj.path))
            else:
                return True

        return [name for name in names if validate_name(name)]


class ObjectModelBase:
    """Base ObjectModel class for Fluent datamodel service wrapper."""

    def __init__(
        self,
        service,
        scheme_interpreter_service,
    ):
        self._service = service
        self._cache = DataModelCache() if config.datamodel_use_state_cache else None
        self.file_transfer_service = None
        self._version = FluentVersion(
            ".".join(
                scheme_interpreter_service.string_eval("(cx-version)")
                .strip("()")
                .split()
            )
        )

    def get_attribute_value(self, rules: str, path: str, attribute: str) -> ValueT:
        """Get attribute value."""
        return self._service.get_attribute_value(rules, path, attribute)

    @property
    def subscriptions(self):
        """Access the subscription list of the underlying gRPC service."""
        return self._service.subscriptions

    def get_state(self, rules: str, path: str) -> ValueT:
        """Get state."""
        return self._service.get_state(rules, path)

    def get_object_names(self, rules: str, path: str) -> list[str]:
        """Get object names."""
        return self._service.get_object_names(rules, path)

    def rename(self, rules: str, path: str, new_name: str) -> None:
        """Rename an object."""
        state, deleted_paths = self._service.rename(rules, path, new_name)
        if self._cache is not None:
            self._cache.update_cache(
                rules,
                state,
                deleted_paths,
                self._version,
            )

    def delete_child_objects(
        self, rules: str, path: str, obj_type: str, child_names: list[str]
    ) -> None:
        """Delete child objects."""
        state, deleted_paths = self._service.delete_child_objects(
            rules, path, obj_type, child_names
        )
        if self._cache is not None:
            self._cache.update_cache(
                rules,
                state,
                deleted_paths,
                version=self._version,
            )

    def delete_all_child_objects(self, rules: str, path: str, obj_type: str) -> None:
        """Delete all child objects."""
        state, deleted_paths = self._service.delete_all_child_objects(
            rules, path, obj_type
        )
        if self._cache is not None:
            self._cache.update_cache(
                rules,
                state,
                deleted_paths,
                version=self._version,
            )

    def set_state(self, rules: str, path: str, state: ValueT) -> None:
        """Set state."""
        state, deleted_paths = self._service.set_state(rules, path, state)
        if self._cache is not None:
            self._cache.update_cache(
                rules,
                state,
                deleted_paths,
                version=self._version,
            )

    def fix_state(self, rules: str, path: str) -> None:
        """Fix state."""
        state, deleted_paths = self._service.fix_state(rules, path)
        if self._cache is not None:
            self._cache.update_cache(
                rules,
                state,
                deleted_paths,
                version=self._version,
            )

    def update_dict(
        self,
        rules: str,
        path: str,
        dict_state: dict[str, ValueT],
        recursive=False,
    ) -> None:
        """Update the dict."""
        state, deleted_paths = self._service.update_dict(
            rules, path, dict_state, recursive=recursive
        )
        if self._cache is not None:
            self._cache.update_cache(
                rules,
                state,
                deleted_paths,
                version=self._version,
            )

    def delete_object(self, rules: str, path: str) -> None:
        """Delete an object."""
        state, deleted_paths = self._service.delete_object(rules, path)
        if self._cache is not None:
            self._cache.update_cache(
                rules,
                state,
                deleted_paths,
                version=self._version,
            )

    def execute_command(
        self, rules: str, path: str, command: str, args: dict[str, ValueT]
    ) -> ValueT:
        """Execute the command."""
        result, state, deleted_paths = self._service.execute_command(
            rules, path, command, args
        )
        if self._cache is not None:
            self._cache.update_cache(
                rules,
                state,
                deleted_paths,
                version=self._version,
            )
        return result

    def execute_query(
        self, rules: str, path: str, query: str, args: dict[str, ValueT]
    ) -> ValueT:
        """Execute the query."""
        return self._service.execute_query(rules, path, query, args)

    def create_command_arguments(self, rules: str, path: str, command: str) -> str:
        """Create command arguments."""
        return self._service.create_command_arguments(rules, path, command)

    def delete_command_arguments(
        self, rules: str, path: str, command: str, commandid: str
    ) -> None:
        """Delete command arguments."""
        return self._service.delete_command_arguments(rules, path, command, commandid)

    def register_command_arguments(
        self, rules: str, path: str, command: str, commandid: str
    ) -> None:
        """Register command arguments for explicit cleanup during shutdown."""
        return self._service.register_command_arguments(rules, path, command, commandid)

    def release_command_arguments(
        self, rules: str, path: str, command: str, commandid: str
    ) -> None:
        """Release command arguments when their Python wrapper is deleted."""
        return self._service.release_command_arguments(rules, path, command, commandid)

    def delete_all_command_arguments(self) -> None:
        """Delete all tracked command arguments as part of shutdown finalization."""
        return self._service.delete_all_command_arguments()

    def get_static_info(self, rules: str) -> dict[str, Any]:
        """Get static info."""
        return self._service.get_static_info(rules)

    def subscribe_events(self, request_dict: dict[str, Any]) -> dict[str, Any]:
        """Subscribe events."""
        return self._service.subscribe_events(request_dict)

    def unsubscribe_events(self, tags: list[str]) -> dict[str, Any]:
        """Unsubscribe events."""
        return self._service.unsubscribe_events(tags)

    def unsubscribe_all_events(self) -> None:
        """Unsubscribe all subscribed events."""
        self._service.unsubscribe_all_events()

    def add_on_child_created(
        self, rules: str, path: str, child_type: str, cb: Callable[[str], None]
    ):
        """Add on child created."""
        return self._service.add_on_child_created(rules, path, child_type, cb)

    def add_on_deleted(self, rules: str, path: str, cb: Callable[[], None]):
        """Add on deleted."""
        return self._service.add_on_deleted(rules, path, cb)

    def add_on_changed(self, rules: str, path: str, cb: Callable[[ValueT], None]):
        """Add on changed."""
        return self._service.add_on_changed(rules, path, cb)

    def add_on_affected(self, rules: str, path: str, cb: Callable[[], None]):
        """Add on affected."""
        return self._service.add_on_affected(rules, path, cb)

    def add_on_affected_at_type_path(
        self, rules: str, path: str, child_type: str, cb: Callable[[], None]
    ):
        """Add on affected at type path."""
        return self._service.add_on_affected_at_type_path(rules, path, child_type, cb)

    def add_on_command_executed_old(
        self,
        rules: str,
        path: str,
        command: str,
        obj,
        cb: Callable[[str, ValueT], None],
    ):
        """Add on command executed."""
        return self._service.add_on_command_executed_old(rules, path, command, obj, cb)

    def add_on_command_executed(
        self, rules: str, path: str, cb: Callable[[str, ValueT], None]
    ):
        """Add on command executed."""
        return self._service.add_on_command_executed(rules, path, cb)

    def add_on_attribute_changed(
        self, rules: str, path: str, attribute: str, cb: Callable[[ValueT], None]
    ):
        """Add on attribute changed."""
        return self._service.add_on_attribute_changed(rules, path, attribute, cb)

    def add_on_command_attribute_changed(
        self,
        rules: str,
        path: str,
        command: str,
        attribute: str,
        cb: Callable[[ValueT], None],
    ):
        """Add on command attribute changed."""
        return self._service.add_on_command_attribute_changed(
            rules, path, command, attribute, cb
        )


class ObjectModelV261(ObjectModelBase, AbstractObjectModel):
    """ObjectModel class for Fluent datamodel service wrapper for Fluent version <= 26.1."""

    def __init__(
        self,
        service,
        scheme_interpreter_service,
    ):
        super().__init__(service, scheme_interpreter_service)

    def create_object(self, rules: str, path: str, name: str) -> None:
        """Create an object."""
        raise NotImplementedError(
            "`create_object` is not supported in Fluent version <= 26.1."
            "Please use Fluent version >= 27.1 to use this feature."
        )


class ObjectModel(ObjectModelBase, AbstractObjectModel):
    """ObjectModel class for Fluent datamodel service wrapper for Fluent version >= 27.1."""

    def __init__(
        self,
        service,
        scheme_interpreter_service,
    ):
        super().__init__(service, scheme_interpreter_service)

    def create_object(self, rules: str, path: str, name: str) -> None:
        """Create an object."""
        state, deleted_paths = self._service.create_object(rules, path, name)
        if self._cache is not None:
            self._cache.update_cache(
                rules,
                state,
                deleted_paths,
                version=self._version,
            )


class PyCallableStateObject:
    """Any object which can be called to get its state.

    Methods
    -------
    __call__()
        Get the state of the current object.
    """

    def __call__(self, *args, **kwds) -> Any:
        return self.get_state()


class PyStateContainer(PyCallableStateObject):
    """Object class using StateEngine based DatamodelService as backend. Use this class
    instead of directly calling DatamodelService's method.

    Methods
    -------
    get_attr(attrib)
        Get the attribute value of the current object.
    getAttribValue(attrib)
        Get the attribute value of the current object.
        (This method is the same as the get_attr(attrib)
        method.)
    get_state()
        Get the state of the current object.
    getState()
        Deprecated camel case alias of get_state.
    set_state()
        Set the state of the current object.
    setState()
        Deprecated camel case alias of set_state.
    __call__()
        Set the state of the current object if state is provided else get its state.
    """

    def __init__(self, service, rules: str, path: Path | None = None) -> None:
        """__init__ method of PyStateContainer class."""
        super().__init__()
        self.__dict__.update(
            dict(
                service=service,
                rules=rules,
                path=[] if path is None else path,
                _cached_attrs={},
            )
        )

    def get_remote_state(self) -> Any:
        """Get state of the current object."""
        return self.service.get_state(self.rules, convert_path_to_se_path(self.path))

    def get_state(self) -> Any:
        """Get state."""
        if self.service._cache is not None:
            state = self.service._cache.get_state(self.rules, self, NameKey.DISPLAY)
            if self.service._cache.is_unassigned(state):
                state = self.get_remote_state()
        else:
            state = self.get_remote_state()
        return state

    getState = get_state

    def fix_state(self) -> None:
        """Fix state."""
        self.service.fix_state(self.rules, self.path)

    fixState = fix_state

    def set_state(self, state: Any | None = None, **kwargs) -> None:
        """Set state of the current object.

        Parameters
        ----------
        state : Any, optional
            state
        kwargs : Any
            Keyword arguments.

        Raises
        ------
        ReadOnlyObjectError
            If the object is read-only.
        """
        if self.get_attr(Attribute.IS_READ_ONLY.value):
            raise ReadOnlyObjectError(type(self).__name__)
        self.service.set_state(
            self.rules, convert_path_to_se_path(self.path), kwargs or state
        )

    setState = set_state

    def get_completer_info(
        self, prefix: str = "", excluded: Iterable = None
    ) -> list[list[str]]:
        """Get completer information of all children.

        Returns
        -------
        list[list[str]]
            Name, type and docstring of all children.
        """
        return _get_completer_info(
            obj=self, base_class=PyStateContainer, prefix=prefix, excluded=excluded
        )

    def _get_remote_attr(self, attrib: str) -> Any:
        return self.service.get_attribute_value(
            self.rules, convert_path_to_se_path(self.path), attrib
        )

    def _get_cached_attr(self, attrib: str) -> Any:
        cached_val = self._cached_attrs.get(attrib)
        if cached_val is None:
            cached_val = self._get_remote_attr(attrib)
            try:
                self.add_on_attribute_changed(
                    attrib,
                    functools.partial(dict.__setitem__, self._cached_attrs, attrib),
                )
                self._cached_attrs[attrib] = cached_val
            except Exception as ex:
                # will fail for paths/attributes
                # that the server does not support event subscriptions on (e.g.
                # isReadOnly at the workflow datamodel root)
                logger.warning(ex)
        return cached_val

    def get_attr(self, attrib: str) -> Any:
        """Get attribute value of the current object.

        Parameters
        ----------
        attrib : str
            Name of the attribute.

        Returns
        -------
        Any
            Value of the attribute.
        """
        if config.datamodel_use_attr_cache and self.rules != "meshing_workflow":
            return self._get_cached_attr(attrib)
        return self._get_remote_attr(attrib)

    getAttribValue = get_attr

    def is_active(self) -> bool:
        """Returns true if the object is active."""
        return true_if_none(self.get_attr(Attribute.IS_ACTIVE.value))

    def is_read_only(self) -> bool:
        """Checks whether the object is read only."""
        return false_if_none(self.get_attr(Attribute.IS_READ_ONLY.value))

    def __call__(self, *args, **kwargs) -> Any:
        if kwargs:
            self.set_state(kwargs)
        elif args:
            self.set_state(args)
        else:
            return self.get_state()

    def add_on_attribute_changed(self, attribute: str, cb: Callable[[ValueT], None]):
        """Register a callback for when an attribute is changed.

        Parameters
        ----------
        attribute : str
            attribute name
        cb : Callable[[ValueT], None]
            Callback function

        Returns
        -------
        EventSubscription
            EventSubscription instance which can be used to unregister the callback
        """
        return self.service.add_on_attribute_changed(
            self.rules, convert_path_to_se_path(self.path), attribute, cb
        )

    def add_on_command_attribute_changed(
        self, command: str, attribute: str, cb: Callable[[ValueT], None]
    ):
        """Register a callback for when an attribute is changed.

        Parameters
        ----------
        command : str
            command name
        attribute : str
            attribute name
        cb : Callable[[ValueT], None]
            Callback function

        Returns
        -------
        EventSubscription
            EventSubscription instance which can be used to unregister the callback
        """
        return self.service.add_on_command_attribute_changed(
            self.rules, convert_path_to_se_path(self.path), command, attribute, cb
        )

    def __dir__(self):
        all_children = list(self.__dict__) + dir(type(self))

        filtered_children = _FilterDatamodelNames(self.service)(self, all_children)

        dir_set = set(filtered_children)
        if self.get_attr(Attribute.IS_READ_ONLY.value):
            dir_set = dir_set - {"setState", "set_state"}

        return sorted(dir_set)


class PyMenu(PyStateContainer):
    """Object class using StateEngine based DatamodelService as backend. Use this class
    instead of directly calling DatamodelService's method.

    Methods
    -------
    __setattr__(name, value)
        Set state of the child object
    rename(new_name)
    name()
    create_command_arguments(command)
    """

    def __init__(self, service, rules: str, path: Path | None = None) -> None:
        """__init__ method of PyMenu class."""
        super().__init__(service, rules, path)

    def __setattr__(self, name: str, value: Any) -> None:
        """Set state of the child object.

        Parameters
        ----------
        name : str
            child object name
        value : Any
            state
        """
        if hasattr(self, name) and isinstance(getattr(self, name), PyStateContainer):
            getattr(self, name).set_state(value)
        else:
            super().__setattr__(name, value)

    def name(self) -> str:
        """Get the name of the named object.

        Returns
        -------
        str
            name

        Raises
        ------
        InvalidNamedObject
            If the object is not a named object.
        """
        try:
            return self._name_()
        except AttributeError:
            raise InvalidNamedObject(self.__class__.__name__)

    def _raise_method_not_yet_implemented_exception(self):
        raise AttributeError("This method is yet to be implemented in pyfluent.")

    def delete_child(self) -> None:
        """Delete child object."""
        self._raise_method_not_yet_implemented_exception()

    def rename(self, new_name: str) -> None:
        """Rename the named object.

        Parameters
        ----------
        new_name : str
            New name for the object.
        """
        self.service.rename(self.rules, convert_path_to_se_path(self.path), new_name)

    def delete_child_objects(self, obj_type: str, child_names: list[str]):
        """Delete the named objects in 'child_names' from  the container..

        Parameters
        ----------
        obj_type: str
            Type of the named object container.
        child_names : list[str]
            List of named objects.
        """
        for child_name in child_names:
            child_path = f"{convert_path_to_se_path(self.path)}/{obj_type}:{child_name}"
            # delete_child_objects doesn't stream back on-deleted events. Thus
            # unsubscribing all subscription objects before the deletion.
            for stage in ["before", "after"]:
                self.service.subscriptions.unsubscribe_while_deleting(
                    self.rules, child_path, stage
                )
        self.service.delete_child_objects(
            self.rules, convert_path_to_se_path(self.path), obj_type, child_names
        )

    deleteChildObjects = delete_child_objects

    def delete_all_child_objects(self, obj_type):
        """Delete all the named objects in the container.

         Parameters
        ----------
        obj_type: str
            Type of the named object container.
        """
        child_path = f"{convert_path_to_se_path(self.path)}/{obj_type}:"
        # delete_all_child_objects doesn't stream back on-deleted events. Thus
        # unsubscribing all subscription objects before the deletion.
        for stage in ["before", "after"]:
            self.service.subscriptions.unsubscribe_while_deleting(
                self.rules, child_path, stage
            )
        self.service.delete_all_child_objects(
            self.rules, convert_path_to_se_path(self.path), obj_type
        )

    deleteAllChildObjects = delete_all_child_objects

    def create_command_arguments(self, command: str) -> str:
        """Create command arguments.

        Parameters
        ----------
        command : str
            Command name

        Returns
        -------
        str
            Command ID
        """
        return self.service.create_command_arguments(
            self.rules, convert_path_to_se_path(self.path), command
        )

    def add_on_child_created(self, child_type: str, cb: Callable[[PyMenuT], None]):
        """Register a callback for when a child object is created.

        Parameters
        ----------
        child_type : str
            Type of the child object
        cb : Callable[[PyMenuT], None]
            Callback function

        Returns
        -------
        EventSubscription
            EventSubscription instance which can be used to unregister the callback
        """

        def cb_service(child_path: str):
            child_path = convert_se_path_to_path(child_path)
            child_type, child_name = child_path[-1]
            child = getattr(self, child_type)[child_name]
            cb(child)

        return self.service.add_on_child_created(
            self.rules, convert_path_to_se_path(self.path), child_type, cb_service
        )

    def add_on_deleted(self, cb: Callable[[], None]):
        """Register a callback for when the object is deleted.

        Parameters
        ----------
        cb : Callable[[], None]
            Callback function

        Returns
        -------
        EventSubscription
            EventSubscription instance which can be used to unregister the callback
        """
        return self.service.add_on_deleted(
            self.rules, convert_path_to_se_path(self.path), cb
        )

    def add_on_changed(self, cb: Callable[[PyMenuT], None]):
        """Register a callback for when the object is modified.

        Parameters
        ----------
        cb : Callable[[PyMenuT], None]
            Callback function

        Returns
        -------
        EventSubscription
            EventSubscription instance which can be used to unregister the callback
        """

        def cb_service(value: ValueT):
            cb(self)

        return self.service.add_on_changed(
            self.rules, convert_path_to_se_path(self.path), cb_service
        )

    def add_on_affected(self, cb: Callable[[PyMenuT], None]):
        """Register a callback for when the object is affected.

        Parameters
        ----------
        cb : Callable[[PyMenuT], None]
            Callback function

        Returns
        -------
        EventSubscription
            EventSubscription instance which can be used to unregister the callback
        """

        def cb_service():
            cb(self)

        return self.service.add_on_affected(
            self.rules, convert_path_to_se_path(self.path), cb_service
        )

    def add_on_affected_at_type_path(
        self, child_type: str, cb: Callable[[PyMenuT], None]
    ):
        """Register a callback for when the object is affected at child type.

        Parameters
        ----------
        child_type : str
            child type
        cb : Callable[[PyMenuT], None]
            Callback function

        Returns
        -------
        EventSubscription
            EventSubscription instance which can be used to unregister the callback
        """

        def cb_service():
            cb(self)

        return self.service.add_on_affected_at_type_path(
            self.rules, convert_path_to_se_path(self.path), child_type, cb_service
        )

    def add_on_command_executed_old(
        self, command: str, cb: Callable[[PyMenuT, str, ValueT], None]
    ):
        """Register a callback for when a command is executed.

        Parameters
        ----------
        command : str
            Command name
        cb : Callable[[PyMenuT, str, ValueT], None]
            Callback function

        Returns
        -------
        EventSubscription
            EventSubscription instance which can be used to unregister the callback
        """

        def cb_service(command: str, args: ValueT):
            cb(self, command, args)

        return self.service.add_on_command_executed_old(
            self.rules, convert_path_to_se_path(self.path), command, self, cb_service
        )

    def add_on_command_executed(self, cb: Callable[[PyMenuT, str, ValueT], None]):
        """Register a callback for when a command is executed.

        Parameters
        ----------
        cb : Callable[[PyMenuT, str, ValueT], None]
            Callback function

        Returns
        -------
        EventSubscription
            EventSubscription instance which can be used to unregister the callback
        """

        def cb_service(command: str, args: ValueT):
            cb(self, command, args)

        return self.service.add_on_command_executed(
            self.rules, convert_path_to_se_path(self.path), cb_service
        )


class PyParameter(PyStateContainer):
    """Object class using StateEngine based DatamodelService as backend.

    Use this class instead of directly calling DatamodelService's method.
    """

    def default_value(self) -> Any:
        """Get default value of the parameter."""
        return self.get_attr(Attribute.DEFAULT.value)

    def add_on_changed(self, cb: Callable[[PyMenuT], None]):
        """Register a callback for when the object is modified.

        Parameters
        ----------
        cb : Callable[[PyMenuT], None]
            Callback function

        Returns
        -------
        EventSubscription
            EventSubscription instance which can be used to unregister the callback
        """

        def cb_service(value: ValueT):
            cb(self)

        return self.service.add_on_changed(
            self.rules, convert_path_to_se_path(self.path), cb_service
        )


class PyTextual(PyParameter):
    """Provides interface for textual parameters."""

    def allowed_values(self) -> list[str]:
        """Get allowed values."""
        return self.get_attr(Attribute.ALLOWED_VALUES.value)


class PyNumerical(PyParameter):
    """Provides interface for numerical parameters."""

    def min(self) -> float:
        """Minimum value of the numerical parameter."""
        return self.get_attr(Attribute.MIN.value)

    def max(self) -> float:
        """Maximum value of the numerical parameter."""
        return self.get_attr(Attribute.MAX.value)


class PyDictionary(PyParameter):
    """Provides interface for dictionaries.

    Methods
    -------
    update_dict(dict_state)
        Update the state of the current object if the current object
        is a Dict in the data model, else throws RuntimeError
        (currently not showing up in Python). Update is executed according
        to dict.update semantics
    updateDict(dict_state)
        Update the state of the current object if the current object
        is a Dict in the data model, else throws RuntimeError
        (currently not showing up in Python). Update is executed according
        to dict.update semantics (same as update_dict(dict_state))]
    """

    def update_dict(self, dict_state: dict[str, Any], recursive=False) -> None:
        """Update the state of the current object if the current object is a Dict in the
        data model, else throws RuntimeError (currently not showing up in Python).
        Update is executed according to dict.update semantics.

        Parameters
        ----------
        dict_state : dict[str, Any]
            Incoming dict state

        recursive: bool
            Flag to update the nested dictionary structure.

        Raises
        ------
        ReadOnlyObjectError
            If the object is read-only.
        """
        if self.get_attr(Attribute.IS_READ_ONLY.value):
            raise ReadOnlyObjectError(type(self).__name__)
        self.service.update_dict(
            self.rules, convert_path_to_se_path(self.path), dict_state, recursive
        )

    updateDict = update_dict

    def __dir__(self):
        dir_list = set(list(self.__dict__.keys()) + dir(type(self)))
        if self.get_attr(Attribute.IS_READ_ONLY.value):
            dir_list = dir_list - {"updateDict", "update_dict"}

        return sorted(dir_list)


class PyNamedObjectContainer:
    """Container class using the StateEngine-based DatamodelService as the backend. Use
    this class instead of directly calling the DatamodelService's method.

    Methods
    -------
    __len__()
        Return a count of the child objects.
    __iter__()
        Return the next child object.
    __getitem__(key)
        Return the child object by key.
    __setitem__(key, value)
        Set the state of the child object by name.
    __delitem__(key)
        Delete the child object by name.
    """

    def __init__(self, service, rules: str, path: Path | None = None) -> None:
        """__init__ method of PyNamedObjectContainer class."""
        self.service = service
        self.rules = rules
        if path is None:
            self.path = []
        else:
            self.path = path

    def get_object_names(self) -> Any:
        """Displays the name of objects within a container."""
        return self.service.get_object_names(
            self.rules, convert_path_to_se_path(self.path)
        )

    getChildObjectDisplayNames = get_object_names

    def get_completer_info(
        self, prefix: str = "", excluded: Iterable = None
    ) -> list[list[str]]:
        """Get completer information of all children.

        Returns
        -------
        list[list[str]]
            Name, type and docstring of all children.
        """
        return _get_completer_info(
            obj=self,
            base_class=PyNamedObjectContainer,
            prefix=prefix,
            excluded=excluded,
        )

    def __len__(self) -> int:
        """Return a count of child objects.

        Returns
        -------
        int
            Count of child objects.
        """
        return len(self.get_object_names())

    def __iter__(self) -> Iterator[PyMenu]:
        """Return the next child object.

        Yields
        -------
        Iterator[PyMenu]
            Iterator of child objects.
        """
        for name in self.get_object_names():
            child_path = self.path[:-1]
            child_path.append((self.path[-1][0], name))
            yield getattr(self.__class__, f"_{self.__class__.__name__}")(
                self.service, self.rules, child_path
            )

    def _get_item(self, key: str) -> PyMenu:
        if key in self.get_object_names():
            child_path = self.path[:-1]
            child_path.append((self.path[-1][0], key))
            return getattr(self.__class__, f"_{self.__class__.__name__}")(
                self.service, self.rules, child_path
            )
        else:
            raise LookupError(
                f"{key} is not found at path {convert_path_to_se_path(self.path)}"
            )

    def _del_item(self, key: str) -> None:
        if key in self.get_object_names():
            child_path = self.path[:-1]
            child_path.append((self.path[-1][0], key))
            se_path = convert_path_to_se_path(child_path)
            # All subscription objects except those of on-deleted type are unsubscribed
            # before the datamodel object is deleted.
            self.service.subscriptions.unsubscribe_while_deleting(
                self.rules, se_path, "before"
            )
            # On-deleted subscription objects are unsubscribed after the datamodel
            # object is deleted.
            self[key].add_on_deleted(
                lambda: self.service.subscriptions.unsubscribe_while_deleting(
                    self.rules, se_path, "after"
                )
            )
            self.service.delete_object(self.rules, se_path)
        else:
            raise LookupError(
                f"{key} is not found at path {convert_path_to_se_path(self.path)}"
            )

    def __getitem__(self, key: str) -> PyMenu:
        """Return the child object by key.

        Parameters
        ----------
        key : str
            Name of the child object.

        Returns
        -------
        PyMenu
            Child object.
        """
        return self._get_item(key)

    def get(self, key: str) -> PyMenu | None:
        """Return the child object by key.

        Parameters
        ----------
        key : str
            Name of the child object.

        Returns
        -------
        PyMenu
            Child object.
        """
        try:
            return self._get_item(key)
        except LookupError:
            return

    def __setitem__(self, key: str, value: Any) -> None:
        """Set state of the child object by name.

        Parameters
        ----------
        key : str
            Name of the child object.
        value : Any
            State of the child object.
        """
        if isinstance(value, dict) and not value:
            value["_name_"] = key
        parent_state = {f"{self.__class__.__name__}:{key}": value}
        PyMenu(self.service, self.rules, self.path[:-1]).set_state(parent_state)

    def __delitem__(self, key: str) -> None:
        """Delete the child object by name.

        Parameters
        ----------
        key : str
            Name of the child object.
        """
        self._del_item(key)

    @staticmethod
    def _get_type_and_name(type_and_name):
        return type_and_name.split(":", maxsplit=1)

    def _compare_type(self, obj_type):
        child_obj_type = self.path[-1][0]
        return child_obj_type == obj_type

    def get_state(self):
        """Returns state of the container."""
        parent_state = PyMenu(self.service, self.rules, self.path[:-1]).get_state()
        returned_state = {}

        for key, value in parent_state.items():
            type_and_name = self._get_type_and_name(key)
            if len(type_and_name) == 2 and self._compare_type(type_and_name[0]):
                returned_state[type_and_name[1]] = value

        return dict(sorted(returned_state.items()))

    getState = __call__ = get_state


class PyAction:
    """Base class for command/query objects using Datamodel Service."""

    _operation: str = ""  # "command" or "query"

    def __init__(
        self,
        service,
        rules: str,
        name: str,
        path: Path | None = None,
    ) -> None:
        """__init__ method of PyAction class."""
        self.service = service
        self.rules = rules
        setattr(self, self._operation, name)
        self.path = path or []

    def __call__(self, *args, **kwds) -> Any:
        """Execute the operation (command or query)."""
        execute_method = getattr(self.service, f"execute_{self._operation}")
        return execute_method(
            self.rules,
            convert_path_to_se_path(self.path),
            getattr(self, self._operation),
            kwds,
        )

    def _create_arguments(self) -> str:
        """Create arguments for this operation."""
        return self.service.create_command_arguments(
            self.rules,
            convert_path_to_se_path(self.path),
            getattr(self, self._operation),
        )

    def _get_create_instance_args(self):
        """Prepare arguments for PyArguments constructor."""
        try:
            id = self._create_arguments()
            return [
                self.service,
                self.rules,
                getattr(self, self._operation),
                self.path.copy(),
                id,
            ]
        except (RuntimeError, ValueError) as e:
            logger.warning(
                f"datamodels_se.{self.__class__.__name__} could not create {self._operation} arguments. "
                f"The underlying DatamodelService reported an error: {e}."
            )

    def create_instance(self) -> "PyArguments":
        """Create an operation instance."""
        args = self._get_create_instance_args()
        if args is not None:
            return PyArguments(*args)

    def get_completer_info(
        self, prefix: str = "", excluded: Iterable = None
    ) -> list[list[str]]:
        """Get completer information of all children.

        Returns
        -------
        list[list[str]]
            Name, type and docstring of all children.
        """
        return _get_completer_info(
            obj=self, base_class=PyAction, prefix=prefix, excluded=excluded
        )


class PyQuery(PyAction):
    """Enables querying Fluent’s data model through a simple Python interface."""

    _operation = "query"


class PyCommand(PyAction):
    """Enables commanding Fluent’s data model through a simple Python interface."""

    _operation = "command"

    def __init__(
        self,
        service,
        rules: str,
        command: str,
        path: Path | None = None,
    ):
        """__init__ method of PyCommand class."""
        super().__init__(service, rules, command, path)
        self.file_behavior = None

    def _update_file_behavior(self, file_purpose):
        purpose_to_class = {
            "input": _InputFile,
            "output": _OutputFile,
            "inout": _InOutFile,
        }

        if file_purpose:
            if file_purpose in purpose_to_class:
                file_class = purpose_to_class[file_purpose]
                self.file_behavior = file_class()
                setattr(self.file_behavior, "service", self.service)
            else:
                raise DisallowedFilePurpose(
                    "File purpose", file_purpose, ["input", "output", "inout"]
                )

    def _get_file_purpose(self, arg):
        try:
            cmd_instance = self.create_instance()
            arg_instance = getattr(cmd_instance, arg)
            file_purpose = arg_instance.get_attr("filePurpose")
            del cmd_instance, arg_instance
            self._update_file_behavior(file_purpose)
            return file_purpose if file_purpose else None
        except AttributeError:
            pass

    def before_execute(self, value):
        """Executes before command execution."""
        if hasattr(self.file_behavior, "_do_before_execute"):
            return self.file_behavior._do_before_execute(value)
        else:
            return value

    def after_execute(self, value):
        """Executes after command execution."""
        if hasattr(self.file_behavior, "_do_after_execute"):
            self.file_behavior._do_after_execute(value)

    def __call__(self, *args, **kwds) -> Any:
        """Execute the command.

        Returns
        -------
        Any
            Return value.
        """
        processed = []
        for arg, value in kwds.items():
            if self._get_file_purpose(arg):
                kwds[arg] = self.before_execute(value)
                processed.append(kwds[arg])
        try:
            return super().__call__(*args, **kwds)
        finally:
            for value in processed:
                self.after_execute(value)


class PyArgumentsSubItem(PyCallableStateObject):
    """Class representing command argument in datamodel."""

    def __init__(
        self,
        parent,
        name: str,
        service,
        rules: str,
        path: Path,
    ) -> None:
        """__init__ method of PyArgumentsSubItem class."""
        self.__dict__.update(
            dict(
                parent=parent,
                name=name,
                service=service,
                rules=rules,
                path=path,
            )
        )

    def get_state(self) -> Any:
        """Get state of the command argument."""
        parent_state = self.parent.get_state()
        return parent_state[self.name]

    getState = get_state

    def set_state(self, state) -> Any:
        """Set state of the command argument."""
        self.parent.set_state({self.name: state})

    setState = set_state

    def get_attr(self, attrib: str) -> Any:
        """Get attribute value of the command argument.

        Parameters
        ----------
        attrib : str
            attribute name

        Returns
        -------
        Any
            attribute value
        """
        attrib_path = f"{self.name}/{attrib}"
        return self.parent.get_attr(attrib_path)

    getAttribValue = get_attr

    def __setattr__(self, key, value):
        if isinstance(value, PyArgumentsSubItem):
            super().__setattr__(key, value)
        else:
            getattr(self, key).set_state(value)


class PyArguments(PyStateContainer):
    """Class representing command arguments in datamodel."""

    def __init__(
        self,
        service,
        rules: str,
        command: str,
        path: Path,
        id: str,
    ) -> None:
        """__init__ method of PyArguments class."""
        super().__init__(service, rules, path)
        self.__dict__.update(
            dict(
                command=command,
                id=id,
            )
        )
        self.path.append((command, id))
        self.service.register_command_arguments(
            self.rules,
            convert_path_to_se_path(self.path[:-1]),
            self.path[-1][0],
            self.path[-1][1],
        )

    def __del__(self) -> None:
        try:
            self.service.release_command_arguments(
                self.rules,
                convert_path_to_se_path(self.path[:-1]),
                self.path[-1][0],
                self.path[-1][1],
            )
        except Exception as exc:
            logger.info(f"__del__ {type(exc).__name__}: {exc}")

    def get_attr(self, attrib: str) -> Any:
        """Get attribute value of the current object.

        Parameters
        ----------
        attrib : str
            Name of the attribute.

        Returns
        -------
        Any
            Value of the attribute.
        """
        return self._get_remote_attr(attrib)

    def __setattr__(self, key, value):
        if isinstance(value, PyArgumentsSubItem):
            super().__setattr__(key, value)
        else:
            getattr(self, key).set_state(value)


class PyArgumentsTextualSubItem(PyArgumentsSubItem, PyTextual):
    """Class representing textual command argument in datamodel."""

    def __init__(
        self,
        parent,
        attr: str,
        service,
        rules: str,
        path: Path,
    ) -> None:
        """__init__ method of PyArgumentsTextualSubItem class."""
        PyArgumentsSubItem.__init__(self, parent, attr, service, rules, path)
        PyTextual.__init__(self, service, rules, path)


class PyArgumentsNumericalSubItem(PyArgumentsSubItem, PyNumerical):
    """Class representing numerical command argument in datamodel."""

    def __init__(
        self,
        parent,
        attr: str,
        service,
        rules: str,
        path: Path,
    ) -> None:
        """__init__ method of PyArgumentsNumericalSubItem class."""
        PyArgumentsSubItem.__init__(self, parent, attr, service, rules, path)
        PyNumerical.__init__(self, service, rules, path)


class PyArgumentsDictionarySubItem(PyArgumentsSubItem, PyDictionary):
    """Class representing dictionary-like command argument in datamodel."""

    def __init__(
        self,
        parent,
        attr: str,
        service,
        rules: str,
        path: Path,
    ) -> None:
        """__init__ method of PyArgumentsDictionarySubItem class."""
        PyArgumentsSubItem.__init__(self, parent, attr, service, rules, path)
        PyDictionary.__init__(self, service, rules, path)


class PyArgumentsParameterSubItem(PyArgumentsSubItem, PyParameter):
    """Class representing generic parameter-like command argument in datamodel."""

    def __init__(
        self,
        parent,
        attr: str,
        service,
        rules: str,
        path: Path,
    ) -> None:
        """__init__ method of PyArgumentsParameterSubItem class."""
        PyArgumentsSubItem.__init__(
            self,
            parent,
            attr,
            service,
            rules,
            path,
        )
        PyParameter.__init__(self, service, rules, path)


class PyArgumentsSingletonSubItem(PyArgumentsSubItem):
    """Class representing singleton-like command argument in datamodel."""

    def __init__(
        self,
        parent,
        attr: str,
        service,
        rules: str,
        path: Path,
    ) -> None:
        """__init__ method of PyArgumentsSingletonSubItem class."""
        PyArgumentsSubItem.__init__(
            self,
            parent,
            attr,
            service,
            rules,
            path,
        )


class PySimpleMenuGeneric(PyMenu, PyDictionary):
    """A simple implementation of PyMenuGeneric applicable only for SINGLETONS.

    This is required for the stand-alone datamodel server to avoid the usage of
    'service.get_specs'
    """

    attrs = ("service", "rules", "path")

    def _get_child(self, name: str) -> "PySimpleMenuGeneric":
        child_path = self.path + [(name, "")]
        return PySimpleMenuGeneric(self.service, self.rules, child_path)

    def __getattr__(self, name: str):
        if name in PySimpleMenuGeneric.attrs:
            return super().__getattr__(name)
        else:
            return self._get_child(name)


arg_class_by_type = {
    **dict.fromkeys(["String", "ListString", "String List"], PyArgumentsTextualSubItem),
    **dict.fromkeys(
        ["Real", "Int", "ListReal", "Real List", "Integer", "ListInt", "Integer List"],
        PyArgumentsNumericalSubItem,
    ),
    "Dict": PyArgumentsDictionarySubItem,
    **dict.fromkeys(["Bool", "Logical", "Logical List"], PyArgumentsParameterSubItem),
    "ModelObject": PyArgumentsSingletonSubItem,
}
