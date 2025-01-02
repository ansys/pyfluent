"""Module for accessing and modifying hierarchy of Fluent settings.

The only useful method is '`get_root``, which returns the root object for
accessing Fluent settings.

Child objects can be generally accessed or modified using attribute access.
Named child objects can be accessed or modified using index operators.

Calling an object will return its current value.

Example
-------
>>> r = flobject.get_root(proxy)
>>> is_energy_on = r.setup.models.energy.enabled()
>>> r.setup.models.energy.enabled = True
>>> r.boundary_conditions.velocity_inlet['inlet'].vmag.constant = 20
"""

from __future__ import annotations

import collections
from contextlib import contextmanager, nullcontext
import fnmatch
import hashlib
import keyword
import logging
import os
import os.path
import pickle
import string
import sys
import types
from typing import (
    Any,
    Dict,
    ForwardRef,
    Generic,
    List,
    NewType,
    Tuple,
    TypeVar,
    Union,
    _eval_type,
    get_args,
    get_origin,
)
import warnings
import weakref

import ansys.fluent.core as pyfluent
from ansys.fluent.core.utils.fluent_version import FluentVersion
from ansys.fluent.core.warnings import PyFluentDeprecationWarning, PyFluentUserWarning

from .error_message import allowed_name_error_message, allowed_values_error
from .flunits import UnhandledQuantity, get_si_unit_for_fluent_quantity
from .settings_external import expand_api_file_argument


def _ansys_units():

    try:
        import ansys.units

        return ansys.units
    except ImportError:
        pass


settings_logger = logging.getLogger("pyfluent.settings_api")


class InactiveObjectError(RuntimeError):
    """Inactive object access."""

    def __init__(self, python_path):
        """Initialize InactiveObjectError."""
        super().__init__(f"'{python_path}' is currently inactive.")


class _InlineConstants:
    is_active = "active?"
    is_stable = "webui-release-active?"
    is_read_only = "read-only?"
    default_value = "default"
    min = "min"
    max = "max"
    user_creatable = "user-creatable?"
    allowed_values = "allowed-values"
    file_purpose = "file-purpose"


# Type hints
RealType = NewType("real", Union[float, str])  # constant or expression
RealListType = List[RealType]
RealVectorType = Tuple[RealType, RealType, RealType]
IntListType = List[int]
StringListType = List[str]
BoolListType = List[bool]
PrimitiveStateType = Union[
    str,
    RealType,
    int,
    bool,
    RealListType,
    IntListType,
    StringListType,
    BoolListType,
]
DictStateType = Dict[str, "StateType"]
ListStateType = List["StateType"]
StateType = Union[PrimitiveStateType, DictStateType, ListStateType]


def check_type(val, tp):
    """Check type of object."""
    if hasattr(tp, "__supertype__"):
        return check_type(val, tp.__supertype__)
    if isinstance(tp, ForwardRef):
        return check_type(val, _eval_type(tp, globals(), locals()))
    origin = get_origin(tp)
    if origin == list:
        return isinstance(val, list) and all(
            check_type(x, get_args(tp)[0]) for x in val
        )
    elif origin == tuple:
        return isinstance(val, tuple) and all(
            check_type(x, t) for x, t in zip(val, get_args(tp))
        )
    elif origin == Union:
        return any(check_type(val, t) for t in get_args(tp))
    elif origin == dict:
        k_t, k_v = get_args(tp)
        return isinstance(val, dict) and all(
            check_type(k, k_t) and check_type(v, k_v) for k, v in val.items()
        )
    elif origin is None:
        try:
            return isinstance(val, tp)
        except TypeError:
            return False
    else:
        return False


def assert_type(val, tp):
    """Assert type.

    Raises
    ------
    TypeError
        If the given value is not of the given type.
    """
    if not check_type(val, tp):
        raise TypeError(f"{val} is not of type {tp}.")


_ttable = str.maketrans(string.punctuation, "_" * len(string.punctuation), "?'")


def to_python_name(fluent_name: str) -> str:
    """Convert a scheme string to a Python variable name.

    This function replaces symbols with _. Any ``?`` symbols are
    ignored.
    """
    if not fluent_name:
        return fluent_name
    name = fluent_name.translate(_ttable)
    while name in keyword.kwlist:
        name = name + "_"
    return name


def _get_python_path_comps(obj):
    """Get python path components for traversing class hierarchy."""
    comps = []
    while obj:
        python_name = obj._python_name
        obj = obj._parent
        if isinstance(obj, (NamedObject, ListObject)):
            comps.append(obj._python_name)
            obj = obj._parent
        else:
            comps.append(python_name)
    comps.reverse()
    return comps[1:]


def _get_class_from_paths(root_cls, some_path: list[str], other_path: list[str]):
    """Get the class for the given alias path."""
    parent_count = 0
    while other_path[0] == "..":
        parent_count += 1
        other_path.pop(0)
    for _ in range(parent_count):
        some_path.pop()
    full_path = some_path + other_path
    cls = root_cls
    for comp in full_path:
        cls = cls._child_classes[comp]
        if issubclass(cls, (NamedObject, ListObject)):
            cls = cls.child_object_type
    return cls, full_path


class Base:
    """Provides the base class for settings and command objects.

    Parameters
    ----------
    name : str
        Name of the object if a child of a named object.
    parent: Base
           Parent of the object.

    Attributes
    ----------
    flproxy
    obj_name
    fluent_name
    """

    def __init__(self, name: str | None = None, parent=None):
        """__init__ of Base class."""
        self._setattr("_parent", weakref.proxy(parent) if parent is not None else None)
        self._setattr("_flproxy", None)
        self._setattr("_file_transfer_service", None)
        if name is not None:
            self._setattr("_name", name)
        self._setattr("_child_alias_objs", {})

    @property
    def _root(self):
        if self._parent is None:
            return self
        else:
            return self._parent._root

    def set_flproxy(self, flproxy):
        """Set flproxy object."""
        self._setattr("_flproxy", flproxy)

    def _set_on_interrupt(self, on_interrupt):
        """Set interrupt method."""
        self._setattr("_on_interrupt", on_interrupt)

    def _set_file_transfer_service(self, file_transfer_service):
        """Set file_transfer_service."""
        self._setattr("_file_transfer_service", file_transfer_service)

    @property
    def flproxy(self):
        """Proxy object.

        The proxy object is set at the root level and accessed via the parent for the
        child classes.
        """
        if self._flproxy is None:
            return self._parent.flproxy
        return self._flproxy

    @property
    def _file_transfer_handler(self):
        """Remote file handler.

        Supports file upload and download.
        """
        with warnings.catch_warnings():
            warnings.filterwarnings(action="ignore", category=UnstableSettingWarning)
            if self._file_transfer_service:
                return self._file_transfer_service
            elif self._parent:
                return self._parent._file_transfer_handler

    _name = None
    fluent_name = None
    _python_name = None

    @property
    def parent(self):
        """Parent (container) object."""
        return self._parent

    @property
    def obj_name(self) -> str:
        """Name of the scheme of this object.

        By default, this returns the object's static name. If the object is a child of a
        named object, the object's name is returned.
        """
        if self._name is None:
            return self.fluent_name
        return self._name

    @property
    def python_name(self) -> str:
        """Python name of this object.

        By default, this returns the object's static name. If the object is a child of a
        named object, the object's name is returned.
        """
        return getattr(self, "_python_name", None) or self.__class__.__name__

    @property
    def path(self) -> str:
        """Path of the object.

        Constructed from the ``obj_name`` of self and the path of
        parent.
        """
        if self._parent is None:
            return self.obj_name
        ppath = self._parent.path
        if not ppath:
            return self.obj_name
        return ppath + "/" + self.obj_name

    @property
    def python_path(self) -> str:
        """Path of the object.

        Constructed in python syntax from 'python_path' and the parents python path.
        """
        if self._parent is None:
            if FluentVersion(self.version).number < 251:
                return "<session>"
            else:
                return "<session>.settings"
        ppath = self._parent.python_path
        if not ppath:
            return self.python_name
        if self.python_name[0] == "[":
            return ppath + self.python_name
        return ppath + "." + self.python_name

    def get_attrs(self, attrs, recursive=False) -> Any:
        """Get the requested attributes for the object."""
        return self.flproxy.get_attrs(self.path, attrs, recursive)

    def get_attr(
        self,
        attr: str,
        attr_type_or_types: type | Tuple[type] | None = None,
    ) -> Any:
        """Get the requested attribute for the object.

        Parameters
        ----------
        attr : str
            attribute name
        attr_type_or_types : type or tuple of type, optional
            attribute type, by default None

        Returns
        -------
        Any
            attribute value

        Raises
        ------
        InactiveObjectError
            If any attribute other than ``"active?`` is queried when the object is not active.
        """
        attrs = self.get_attrs([attr])
        if attrs:
            attrs = attrs.get("attrs", attrs)
        if attr != "active?" and attrs and attrs.get("active?", True) is False:
            raise InactiveObjectError(self.python_path)
        val = None
        if attrs:
            val = attrs[attr]

        if attr_type_or_types:
            if not isinstance(attr_type_or_types, tuple):
                attr_type_or_types = (attr_type_or_types,)
            if isinstance(val, attr_type_or_types):
                return val
            if val is not None and any(
                issubclass(x, bool) for x in attr_type_or_types
            ):  # cast to bool for boolean attributes
                return bool(val)
            return None
        return val

    def is_active(self) -> bool:
        """Whether the object is active."""
        attr = self.get_attr(_InlineConstants.is_active)
        return False if attr is False else True

    def _check_stable(self) -> None:
        """Whether the object is stable."""
        if not self.is_active():
            return
        attr = self.get_attr(_InlineConstants.is_stable)
        attr = True if attr is None else attr
        if not attr:
            warnings.warn(
                f"The API feature at '{self.path}' is not stable. "
                f"It is not guaranteed that it is fully validated and "
                f"there is no commitment to its backwards compatibility.",
                UnstableSettingWarning,
            )

    def is_read_only(self) -> bool:
        """Whether the object is read-only."""
        attr = self.get_attr(_InlineConstants.is_read_only)
        return False if attr is None else attr

    def __setattr__(self, name, value):
        raise AttributeError(name)

    # __setattr__ is overridden to prevent creation of new attributes or
    # overriding existing ones. _setattr is the backdoor to set attributes
    def _setattr(self, name, value):
        super().__setattr__(name, value)

    def find_object(self, relative_path):
        """Find object."""
        obj = self
        for comp in relative_path.split("/"):
            if comp == "..":
                obj = obj.parent
            else:
                obj = getattr(obj, comp)
        return obj

    def before_execute(self, command_name, value, kwargs):
        """Executes before command execution."""
        if hasattr(self, "_do_before_execute"):
            base_file_name = self._do_before_execute(
                command_name=command_name, value=value, kwargs=kwargs
            )
            return base_file_name
        else:
            return value

    def after_execute(self, command_name, value, kwargs):
        """Executes after command execution."""
        if hasattr(self, "_do_after_execute"):
            base_file_name = self._do_after_execute(
                command_name=command_name, value=value, kwargs=kwargs
            )
            return base_file_name
        else:
            return value

    def _while_setting_state(self):
        """Avoid additional processing while setting the state."""
        return nullcontext()

    def _while_renaming(self):
        """Avoid additional processing while renaming."""
        return nullcontext()

    def _while_deleting(self):
        """Avoid additional processing while deleting."""
        return nullcontext()

    def _while_creating(self):
        """Avoid additional processing while creating."""
        return nullcontext()

    def _while_resizing(self):
        """Avoid additional processing while resizing."""
        return nullcontext()

    def _while_executing_command(self):
        """Avoid additional processing while executing a command."""
        return nullcontext()

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.flproxy == other.flproxy and self.path == other.path


StateT = TypeVar("StateT")


class Property(Base):
    """Exposes attribute accessor on settings object."""

    def default_value(self):
        """Gets the default value of the object."""
        return self.get_attr(_InlineConstants.default_value)


class Numerical(Property):
    """Exposes attribute accessor on settings object - specific to numerical objects."""

    def min(self):
        """Get the minimum value of the object."""
        val = self.get_attr(_InlineConstants.min, (float, int))
        return None if isinstance(val, bool) else val

    def max(self):
        """Get the maximum value of the object."""
        val = self.get_attr(_InlineConstants.max, (float, int))
        return None if isinstance(val, bool) else val


QuantityT = TypeVar("QuantityT")


class RealNumerical(Numerical):
    """A ``RealNumerical`` object representing a real value setting, including single
    real values and containers of real values, such as lists.

    Methods
    -------
    as_quantity()
        Get the current state of the object as an ansys.units.Quantity.

    set_state(state)
        Set the state of the object.

    units()
        Get the units string.
    """

    def as_quantity(self) -> QuantityT | None:
        """Get the state of the object as an ansys.units.Quantity."""
        error = None
        if not _ansys_units():
            error = "Code not configured to support units."
        if not error:
            quantity = self.get_attr("units-quantity")
            units = get_si_unit_for_fluent_quantity(quantity)
            if units is not None:
                try:
                    return _ansys_units().Quantity(
                        value=self.get_state(),
                        units=units,
                    )
                except (TypeError, ValueError) as e:
                    error = e
            else:
                error = "Could not determine units."
        warnings.warn(f"Unable to construct 'Quantity'. {error}")

    def set_state(self, state: StateT | None = None, **kwargs):
        """Set the state of the object.

        Parameters
        ----------
        state
            The type of state can be float, str (representing either
            an expression or a value with units), or an ansys.units.Quantity.
        kwargs : Any
            Keyword arguments.

        Raises
        ------
        UnhandledQuantity
            If the quantity object cannot be handled for the given path. This can
            happen if the quantity attribute specifies an unsupported quantity, or if
            the units specified for the quantity are not supported.
        """
        try:

            def get_units():
                units = self.units()
                if units is None:
                    raise UnhandledQuantity(self.path, state)
                return units

            if _ansys_units() and isinstance(state, (_ansys_units().Quantity, tuple)):
                state = (
                    _ansys_units().Quantity(*state)
                    if isinstance(state, tuple)
                    else state
                )
                state = state.to(get_units()).value
            elif isinstance(state, tuple):
                if state[1] == get_units():
                    state = state[0]
                else:
                    raise UnhandledQuantity(self.path, state)
        except Exception as ex:
            raise UnhandledQuantity(self.path, state) from ex

        return self.base_set_state(state=state, **kwargs)

    def units(self) -> str | None:
        """Get the physical units of the object as a string."""
        quantity = self.get_attr("units-quantity")
        return get_si_unit_for_fluent_quantity(quantity)


class Textual(Property):
    """Exposes attribute accessor on settings object - specific to string objects."""


class DeprecatedSettingWarning(PyFluentDeprecationWarning):
    """Provides deprecated settings warning."""

    pass


class UnstableSettingWarning(PyFluentUserWarning):
    """Provides unstable settings warning."""

    pass


_show_warning_orig = warnings.showwarning


def _show_warning(message, category, *args, **kwargs):
    if category == DeprecatedSettingWarning:
        print(message)
    else:
        _show_warning_orig(message, category, *args, **kwargs)


warnings.showwarning = _show_warning


class _Alias:
    scheme_eval = None
    once = False

    @contextmanager
    def _print_newer_api(self):
        scheme_eval = _Alias.scheme_eval
        if scheme_eval:
            scheme_eval("(define pyfluent-journal-str-port (open-output-string))")
            scheme_eval("(api-echo-python-port pyfluent-journal-str-port)")
        try:
            yield
        finally:
            if scheme_eval:
                scheme_eval("(api-unecho-python-port pyfluent-journal-str-port)")
                journal_str = scheme_eval(
                    "(close-output-port pyfluent-journal-str-port)"
                )
                if isinstance(journal_str, str):
                    warnings.warn(
                        "Note: A newer syntax is available to perform the last operation:\n"
                        f"{journal_str.strip()}",
                        DeprecatedSettingWarning,
                    )
                if not _Alias.once:
                    warnings.warn(
                        "\nExecute the following code to suppress future warnings like the above:\n\n"
                        ">>> import warnings\n"
                        '>>> warnings.filterwarnings("ignore", category=DeprecatedSettingWarning)',
                        DeprecatedSettingWarning,
                    )
                    _Alias.once = True

    def _while_setting_state(self):
        return self._print_newer_api()

    def _while_renaming(self):
        return self._print_newer_api()

    def _while_deleting(self):
        return self._print_newer_api()

    def _while_creating(self):
        return self._print_newer_api()

    def _while_resizing(self):
        return self._print_newer_api()

    def _while_executing_command(self):
        return self._print_newer_api()


def _create_child(cls, name, parent: weakref.CallableProxyType, alias_path=None):
    if alias_path or isinstance(parent, _Alias):
        alias_cls = type(
            f"{cls.__name__}_alias",
            (_Alias, cls),
            dict(cls.__dict__) | {"alias_path": alias_path},
        )
        return alias_cls(name, parent.__repr__.__self__)
    return cls(name, parent)


class SettingsBase(Base, Generic[StateT]):
    """Base class for settings objects.

    Methods
    -------
    get_state()
        Get the current state of the object.

    set_state(state)
        Set the state of the object.
    """

    @classmethod
    def to_scheme_keys(cls, value: StateT, root_cls, path: list[str]) -> StateT:
        """Convert value to have keys with scheme names.

        This is overridden in the ``Group``, ``NamedObject``, and
        ``ListObject`` classes.
        """
        return value

    @classmethod
    def to_python_keys(cls, value: StateT) -> StateT:
        """Convert value to have keys with Python names.

        This is overridden in the ``Group``, ``NamedObject``, and
        ``ListObject`` classes.
        """
        return value

    def __call__(self) -> StateT:
        """Alias for self.get_state."""
        return self.get_state()

    def get_state(self) -> StateT:
        """Get the state of the object."""
        return self.to_python_keys(self.flproxy.get_var(self.path))

    def set_state(self, state: StateT | None = None, **kwargs):
        """Set the state of the object."""
        with self._while_setting_state():
            if isinstance(state, (tuple, _ansys_units().Quantity)) and hasattr(
                self, "value"
            ):
                self.value.set_state(state, **kwargs)
            else:
                self.flproxy.set_var(
                    self.path,
                    self.to_scheme_keys(
                        kwargs or state,
                        self._root.__class__,
                        _get_python_path_comps(self),
                    ),
                )

    @staticmethod
    def _print_state_helper(state, out, indent=0, indent_factor=2):
        if isinstance(state, dict):
            out.write("\n")
            for key, value in state.items():
                if value is not None:
                    out.write(f'{indent*indent_factor*" "}{key} : ')
                    SettingsBase._print_state_helper(
                        value, out, indent + 1, indent_factor
                    )
        elif isinstance(state, list):
            out.write("\n")
            for index, value in enumerate(state):
                out.write(f'{indent*indent_factor*" "}{index} : ')
                SettingsBase._print_state_helper(value, out, indent + 1, indent_factor)
        else:
            out.write(f"{state}\n")

    def print_state(self, out=None, indent_factor=2):
        """Print the state of the object."""
        out = sys.stdout if out is None else out
        self._print_state_helper(self.get_state(), out, indent_factor=indent_factor)

    def state_with_units(self) -> StateT:
        """Get the state of the object with units where available."""
        state = self.get_state()
        if isinstance(self, RealNumerical):
            return (state, self.units())
        elif isinstance(state, collections.abc.Mapping):
            self._add_units_to_state(state)
        return state

    def _add_units_to_state(self, state):
        if isinstance(state, collections.abc.Mapping):
            for k, v in state.items():
                child = None
                if isinstance(self, collections.abc.Mapping):
                    try:
                        child = self[k]
                    except KeyError:
                        pass
                child = child or getattr(self, k, None)
                if child is None:
                    raise RuntimeError(
                        "Unexpected None child {k} encountered while getting units for state."
                    )
                elif isinstance(child, RealNumerical):
                    state[k] = (state[k], child.units())
                else:
                    child._add_units_to_state(state[k])


class Integer(SettingsBase[int], Numerical):
    """An ``Integer`` object representing an integer value setting."""

    _state_type = int


class Real(SettingsBase[RealType], RealNumerical):
    """A ``Real`` object representing a real value setting.

    Some ``Real`` objects also accept string arguments representing
    expression values.
    """

    base_set_state = SettingsBase[RealType].set_state
    set_state = RealNumerical.set_state

    _state_type = RealType


class String(SettingsBase[str], Textual):
    """A ``String`` object representing a string value setting."""

    _state_type = str


class Filename(SettingsBase[str], Textual):
    """A ``Filename`` object representing a file name."""

    _state_type = str

    def file_purpose(self):
        """Specifies whether this file is used as input or output by Fluent."""
        return self.get_attr(_InlineConstants.file_purpose)


class FilenameList(SettingsBase[StringListType], Textual):
    """A FilenameList object represents a list of file names."""

    _state_type = StringListType

    def file_purpose(self):
        """Specifies whether this file is used as input or output by Fluent."""
        return self.get_attr(_InlineConstants.file_purpose)


class FileName(Base):
    """Resolves MRO for child classes."""

    pass


class _InputFile(FileName):
    def _do_before_execute(self, command_name, value, kwargs):
        file_names = expand_api_file_argument(command_name, value, kwargs)
        if self._file_transfer_handler:
            for file_name in file_names:
                self._file_transfer_handler.upload(file_name=file_name)
            return os.path.basename(value)
        else:
            return value


class _OutputFile(FileName):
    def _do_after_execute(self, command_name, value, kwargs):
        file_names = expand_api_file_argument(command_name, value, kwargs)
        if self._file_transfer_handler:
            for file_name in file_names:
                self._file_transfer_handler.download(file_name=file_name)
            return os.path.basename(value)
        else:
            return value


class _InOutFile(_InputFile, _OutputFile):
    pass


class Boolean(SettingsBase[bool], Property):
    """A ``Boolean`` object representing a Boolean value setting."""

    _state_type = bool


class RealList(SettingsBase[RealListType], RealNumerical):
    """A ``RealList`` object representing a real list setting."""

    base_set_state = SettingsBase[RealListType].set_state
    set_state = RealNumerical.set_state

    _state_type = RealListType


class IntegerList(SettingsBase[IntListType], Numerical):
    """An ``Integer`` object representing an integer list setting."""

    _state_type = IntListType


class RealVector(SettingsBase[RealVectorType], Numerical):
    """An object representing a 3D vector.

    A ``RealVector`` object representing a real vector setting
    consisting of three real values.
    """

    _state_type = RealVectorType


class StringList(SettingsBase[StringListType], Textual):
    """A ``StringList`` object representing a string list setting."""

    _state_type = StringListType


class BooleanList(SettingsBase[BoolListType], Property):
    """A ``BooleanList`` object representing a Boolean list setting."""

    _state_type = BoolListType


def _command_query_name_filter(
    parent, list_attr: str, prefix: str, excluded: List[str]
) -> List:
    """Auto completer info of commands and queries."""
    ret = []
    names = getattr(parent, list_attr)
    for name in names:
        if name not in excluded and name.startswith(prefix):
            child = getattr(parent, name)
            if child.is_active():
                ret.append([name, child.__class__.__bases__[0].__name__, child.__doc__])
    return ret


class Group(SettingsBase[DictStateType]):
    """A ``Group`` container object.

    A ``Group`` object is a container similar to a C++ structure object.
    Child objects can be accessed via attribute access.

    Attributes
    ----------
    child_names: list[str]
        Names of the child objects
    command_names: list[str]
        Names of the commands
    """

    _state_type = DictStateType

    def __init__(self, name: str | None = None, parent=None):
        """__init__ of Group class."""
        super().__init__(name, parent)
        for child in self.child_names:
            cls = self.__class__._child_classes[child]
            self._setattr(child, _create_child(cls, None, self))
        for cmd in self.command_names:
            cls = self.__class__._child_classes[cmd]
            self._setattr(cmd, _create_child(cls, None, self))
        for query in self.query_names:
            cls = self.__class__._child_classes[query]
            self._setattr(query, _create_child(cls, None, self))

    def __call__(self, *args, **kwargs):
        if kwargs:
            self.set_state(kwargs)
        elif args:
            self.set_state(args)
        else:
            return self.get_state()

    @classmethod
    def to_scheme_keys(cls, value, root_cls, path: list[str]):
        """Convert value to have keys with scheme names.

        Raises
        ------
        RuntimeError
            If key is invalid.
        """
        if isinstance(value, collections.abc.Mapping):
            ret = {}
            for k, v in value.items():
                if k in cls.child_names:
                    ccls = cls._child_classes[k]
                    ret[ccls.fluent_name] = ccls.to_scheme_keys(v, root_cls, path + [k])
                elif k in cls._child_aliases:
                    alias, scm_alias_name = cls._child_aliases[k]
                    alias_cls, alias_path = _get_class_from_paths(
                        root_cls, path.copy(), alias.split("/")
                    )
                    ret[scm_alias_name] = alias_cls.to_scheme_keys(
                        v, root_cls, alias_path
                    )
                else:
                    raise RuntimeError("Key '" + str(k) + "' is invalid")
            return ret
        else:
            return value

    @classmethod
    def to_python_keys(cls, value):
        """Convert value to have keys with Python names."""
        if isinstance(value, collections.abc.Mapping):
            ret = {}
            undef = object()
            for mname in cls.child_names:
                ccls = cls._child_classes[mname]
                mvalue = value.get(ccls.fluent_name, undef)
                if mvalue is not undef:
                    ret[mname] = ccls.to_python_keys(mvalue)
            return ret
        else:
            return {}

    _child_classes = {}
    child_names = []
    command_names = []
    query_names = []
    _child_aliases = {}

    def get_active_child_names(self):
        """Names of children that are currently active."""
        ret = []
        for child in self.child_names:
            if getattr(self, child).is_active():
                ret.append(child)
        return ret

    def get_active_command_names(self):
        """Names of commands that are currently active."""
        ret = []
        for command in self.command_names:
            if getattr(self, command).is_active():
                ret.append(command)
        return ret

    def get_active_query_names(self):
        """Names of queries that are currently active."""
        ret = []
        for query in self.query_names:
            if getattr(self, query).is_active():
                ret.append(query)
        return ret

    def get_completer_info(self, prefix="", excluded=None) -> List[List[str]]:
        """Get completer info of all children.

        Returns
        -------
        List[List[str]]
            Name, type and docstring of all children.
        """
        excluded = excluded or []
        ret = []
        for child_name in self.child_names:
            if child_name not in excluded and child_name.startswith(prefix):
                child = getattr(self, child_name)
                if child.is_active():
                    ret.append(
                        [
                            child_name,
                            child.__class__.__bases__[0].__name__,
                            child.__doc__,
                        ]
                    )
        command_info = _command_query_name_filter(
            self, "command_names", prefix, excluded
        )
        query_info = _command_query_name_filter(self, "query_names", prefix, excluded)
        for items in [command_info, query_info]:
            ret.extend(items)
        return ret

    def __getattribute__(self, name):
        if name in super().__getattribute__("child_names"):
            if self.is_active() is False:
                raise InactiveObjectError(self.python_path)
        alias = super().__getattribute__("_child_aliases").get(name)
        if alias:
            alias = alias[0]
            alias_obj = self._child_alias_objs.get(name)
            if alias_obj is None:
                obj = self.find_object(alias)
                alias_obj = self._child_alias_objs[name] = _create_child(
                    obj.__class__, None, obj.parent, alias
                )
            return alias_obj
        try:
            attr = super().__getattribute__(name)
            if name in super().__getattribute__("_child_classes"):
                attr._check_stable()
            return attr
        except AttributeError as ex:
            pyfluent.PRINT_SEARCH_RESULTS = False
            search_results = pyfluent.utils.search(
                search_string=name,
                match_case=False,
                match_whole_word=False,
            )
            pyfluent.PRINT_SEARCH_RESULTS = True
            results = search_results if search_results else []
            error_msg = allowed_name_error_message(
                trial_name=name,
                message=ex.args[0],
                search_results=results,
            )
            ex.args = (error_msg,)
            raise

    def __setattr__(self, name: str, value):
        attr = None
        try:
            attr = getattr(self, name)
        except AttributeError as ex:
            error_msg = allowed_name_error_message(
                trial_name=name,
                allowed_values=super().__getattribute__("child_names"),
                message=ex.args[0],
            )
            ex.args = (error_msg,)
            raise
        try:
            return attr.set_state(value)
        except Exception as ex:
            if hasattr(attr, "allowed_values"):
                allowed = attr.allowed_values()
                if allowed and value not in allowed:
                    raise allowed_values_error(name, value, allowed) from ex
            else:
                raise


class WildcardPath(Group):
    """Class wrapping a wildcard path to perform get_var and set_var on flproxy."""

    def __init__(self, flproxy, path: str, state_cls, settings_cls, parent):
        """__init__ of WildcardPath class."""
        self._setattr("_flproxy", flproxy)
        self._setattr("_path", path)
        # _state_cls is the settings class at which the state is constructed.
        # _state_cls isn't changed after the first wildcard, i.e.
        # a.b["*"], a.b["*"].c, a.b["*"].c.d["*"] have the same _state_cls.
        # It is used to convert between python and scheme keys within the state.
        self._setattr("_state_cls", state_cls)
        # _settings_cls is the settings cls at the wildcard path level. It is used to
        # construct the scheme path for children.
        self._setattr("_settings_cls", settings_cls)
        self._setattr("_parent", parent)

    @property
    def flproxy(self):
        """Proxy object."""
        return self._flproxy

    @property
    def path(self):
        """Path with wildcards."""
        return self._path

    def __getattr__(self, name: str):
        try:
            child_settings_cls = self._settings_cls._child_classes[name]
            scheme_name = child_settings_cls.fluent_name
            wildcard_cls = (
                NamedObjectWildcardPath
                if issubclass(child_settings_cls, NamedObject)
                else WildcardPath
            )
            return wildcard_cls(
                self.flproxy,
                self.path + "/" + scheme_name,
                self._state_cls,
                child_settings_cls,
                self,
            )
        except KeyError as ex:
            raise AttributeError(
                allowed_name_error_message(
                    context=self._state_cls._python_name,
                    trial_name=name,
                    allowed_values=self.get_active_child_names(),
                )
            ) from ex

    def items(self):
        """Items."""
        for key, value in self._parent.items():
            if fnmatch.fnmatch(key, self._path.rsplit(sep="/", maxsplit=1)[-1]):
                yield key, value

    def __iter__(self):
        for item in self._parent:
            if fnmatch.fnmatch(item, self._path.rsplit(sep="/", maxsplit=1)[-1]):
                yield item

    # Note that following 2 are not symmetric as get_state and set_state
    # are not symmetric.
    # get_state example: a.b["*"].c.d.get_state() == {"<bN>" {"c": {"d": <d_value>}}}
    # set_state example: a.b["*"].set_state({"c": {"d": <d_value>}})

    def to_scheme_keys(self, value, root_cls, path):
        """Convert value to have keys with scheme names."""
        return self._settings_cls.to_scheme_keys(value, root_cls, path)

    def to_python_keys(self, value):
        """Convert value to have keys with Python names."""
        return self._state_cls.to_python_keys(value)


class NamedObjectWildcardPath(WildcardPath):
    """WildcardPath at a NamedObject path, so it can be looked up by wildcard again."""

    def __getitem__(self, name: str):
        return WildcardPath(
            self.flproxy,
            self.path + "/" + name,
            self._state_cls,
            self._settings_cls.child_object_type,
            self,
        )

    def __setitem__(self, name, value):
        self[name].set_state(value)


ChildTypeT = TypeVar("ChildTypeT")


class NamedObject(SettingsBase[DictStateType], Generic[ChildTypeT]):
    """A ``NamedObject`` container is a container object similar to a Python dictionary
    object. Generally, many such objects can be created with different names.

    Attributes
    ----------
    command_names: list[str]
        Names of the commands
    """

    # New objects could get inserted by other operations, so we cannot assume
    # that the local cache in self._objects is always up-to-date
    def __init__(self, name: str | None = None, parent=None):
        """__init__ of NamedObject class."""
        super().__init__(name, parent)
        self._setattr("_objects", {})
        for cmd in self.command_names:
            cls = self.__class__._child_classes[cmd]
            self._setattr(cmd, _create_child(cls, None, self))
        for query in self.query_names:
            cls = self.__class__._child_classes[query]
            self._setattr(query, _create_child(cls, None, self))
        if not hasattr(
            self, "rename"
        ):  # if rename command is not available from settings API
            self._setattr(
                "rename",
                types.MethodType(lambda obj, new, old: _rename(obj, new, old), self),
            )

    @classmethod
    def to_scheme_keys(cls, value, root_cls, path: list[str]):
        """Convert value to have keys with scheme names."""
        if isinstance(value, collections.abc.Mapping):
            ret = {}
            for k, v in value.items():
                ret[k] = cls.child_object_type.to_scheme_keys(v, root_cls, path)
            return ret
        else:
            return value

    @classmethod
    def to_python_keys(cls, value):
        """Convert value to have keys with Python names."""
        if isinstance(value, collections.abc.Mapping):
            ret = {}
            for k, v in value.items():
                ret[k] = cls.child_object_type.to_python_keys(v)
            return ret
        else:
            return {}

    _child_classes = {}
    command_names = []
    query_names = []
    _child_aliases = {}

    def _create_child_object(self, cname: str):
        ret = self._objects.get(cname)
        if not ret:
            cls = self.__class__.child_object_type
            ret = self._objects[cname] = _create_child(cls, cname, self)
        ret._setattr("_python_name", f'["{cname}"]')
        ret._setattr(
            "rename",
            types.MethodType(lambda obj, name: _rename(self, name, cname), ret),
        )
        return ret

    def _update_objects(self):
        names = self.get_object_names()
        for name in list(self._objects.keys()):
            if name not in names:
                del self._objects[name]
        for name in names:
            if name not in self._objects:
                self._create_child_object(name)

    def __delitem__(self, name: str):
        with self._while_deleting():
            self.flproxy.delete(self.path, name)
        if name in self._objects:
            del self._objects[name]

    def __contains__(self, name: str):
        return name in self.get_object_names()

    def __len__(self):
        return len(self.keys())

    def __iter__(self):
        self._update_objects()
        return iter(self._objects)

    def keys(self):
        """Object names."""
        self._update_objects()
        return self._objects.keys()

    def values(self):
        """Object values."""
        self._update_objects()
        return self._objects.values()

    def items(self):
        """Items."""
        self._update_objects()
        return self._objects.items()

    def user_creatable(self) -> bool:
        """Whether the object is user-creatable."""
        return self.get_attr(_InlineConstants.user_creatable, bool)

    def get_object_names(self):
        """Object names."""
        obj_names = self.flproxy.get_object_names(self.path)
        obj_names_list = obj_names if isinstance(obj_names, list) else list(obj_names)
        return obj_names_list

    def get_completer_info(self, prefix="", excluded=None) -> List[List[str]]:
        """Get completer info of all children.

        Returns
        -------
        List[List[str]]
            Name, type and docstring of all children.
        """
        excluded = excluded or []
        ret = []
        command_info = _command_query_name_filter(
            self, "command_names", prefix, excluded
        )
        query_info = _command_query_name_filter(self, "query_names", prefix, excluded)
        for items in [command_info, query_info]:
            ret.extend(items)
        return ret

    def __getitem__(self, name: str) -> ChildTypeT:
        if name not in self.get_object_names():
            if self.flproxy.has_wildcard(name):
                child_cls = self.__class__.child_object_type
                # TODO: alias
                return WildcardPath(
                    self.flproxy,
                    self.path + "/" + name,
                    self.__class__,
                    child_cls,
                    self,
                )
            raise KeyError(
                allowed_name_error_message(
                    context=self.__class__._python_name,
                    trial_name=name,
                    allowed_values=self.get_object_names(),
                )
            )

        obj = self._objects.get(name)
        if not obj:
            obj = self._create_child_object(name)
        return obj

    def get(self, name: str) -> ChildTypeT:
        """Return the child object by key.

        Parameters
        ----------
        name : str
            Name of the child object.

        Returns
        -------
        ChildTypeT
            Child object.
        """
        try:
            return self.__getitem__(name)
        except Exception:
            return

    def __getattr__(self, name: str):
        alias = self._child_aliases.get(name)
        if alias:
            alias = alias[0]
            alias_obj = self._child_alias_objs.get(name)
            if alias_obj is None:
                obj = self.find_object(alias)
                alias_obj = self._child_alias_objs[name] = _create_child(
                    obj.__class__, None, obj.parent, alias
                )
            return alias_obj
        else:
            return getattr(super(), name)


def _rename(obj: NamedObject | _Alias, new: str, old: str):
    """Rename a named object.

    Parameters
    ----------
    obj: NamedObject
        named-object to be renamed
    new: str
        New name.
    old : str
        Current name.
    """
    with obj._while_renaming():
        obj.flproxy.rename(obj.path, new, old)
    if old in obj._objects:
        del obj._objects[old]
    obj._create_child_object(new)


class ListObject(SettingsBase[ListStateType], Generic[ChildTypeT]):
    """A ``ListObject`` container is a container object, similar to a Python list
    object. Generally, many such objects can be created.

    Attributes
    ----------
    command_names: list[str]
        Names of the commands.

    Methods
    -------
    get_size()
       Get the size of the list.
    """

    # New objects could get inserted by other operations, so we cannot assume
    # that the local cache in self._objects is always up-to-date
    def __init__(self, name=None, parent=None):
        """__init__ of ListObject class."""
        super().__init__(name, parent)
        self._setattr("_objects", [])
        for cmd in self.command_names:
            cls = self.__class__._child_classes[cmd]
            self._setattr(cmd, _create_child(cls, None, self))
        for query in self.query_names:
            cls = self.__class__._child_classes[query]
            self._setattr(query, _create_child(cls, None, self))

    @classmethod
    def to_scheme_keys(cls, value, root_cls, path: list[str]):
        """Convert value to have keys with scheme names."""
        if isinstance(value, collections.abc.Sequence):
            return [
                cls.child_object_type.to_scheme_keys(v, root_cls, path) for v in value
            ]
        else:
            return value

    @classmethod
    def to_python_keys(cls, value):
        """Convert value to have keys with scheme names."""
        if isinstance(value, collections.abc.Sequence):
            return [cls.child_object_type.to_python_keys(v) for v in value]
        else:
            return []

    _child_classes = {}
    command_names = []
    query_names = []
    _child_aliases = {}

    def _update_objects(self):
        cls = self.__class__.child_object_type
        self._setattr(
            "_objects",
            [_create_child(cls, str(x), self) for x in range(self.get_size())],
        )

    def __len__(self):
        return self.get_size()

    def __iter__(self):
        self._update_objects()
        return iter(self._objects)

    def get_size(self) -> int:
        """Return the number of elements in a list object.

        Returns
        -------
        int
        """
        return self.flproxy.get_list_size(self.path)

    def __getitem__(self, index: int) -> ChildTypeT:
        size = self.get_size()
        if index >= size:
            raise IndexError(index)
        if len(self._objects) != size:
            self._update_objects()
        return self._objects[index]

    def __setitem__(self, index: int, value):
        child = self[index]
        child.set_state(value)

    def __getattr__(self, name: str):
        alias = self._child_aliases.get(name)
        if alias:
            alias = alias[0]
            alias_obj = self._child_alias_objs.get(name)
            if alias_obj is None:
                obj = self.find_object(alias)
                alias_obj = self._child_alias_objs[name] = _create_child(
                    obj.__class__, None, obj.parent, alias
                )
            return alias_obj
        else:
            return getattr(super(), name)


class Map(SettingsBase[DictStateType]):
    """A ``Map`` object representing key-value settings."""


def _get_new_keywords(obj, *args, **kwds):
    newkwds = {}
    unknown_keywords = set()
    # Convert positional arguments to keyword arguments
    if args:
        argNames = obj.argument_names[:]
        for arg in args:
            argName = argNames.pop(0)
            newkwds[argName] = arg
    if kwds:
        # Convert deprecated keywords through aliases
        # We don't get arguments-aliases from static-info yet.
        argument_aliases_scm = obj.get_attr("arguments-aliases") or {}
        argument_aliases = {}
        for k, v in argument_aliases_scm.items():
            argument_aliases[to_python_name(k)] = to_python_name(v.removeprefix("'"))
        for k, v in kwds.items():
            alias = argument_aliases.get(k)
            if alias:
                newkwds[alias] = v
            elif k in obj.argument_names:
                newkwds[k] = v
            else:
                unknown_keywords.add(k)
    for k in unknown_keywords:
        # Noisily ignore unknown keywords
        warnings.warn(
            f"Unknown keyword '{k}' for command '{obj.python_path}'. "
            "It will be ignored.",
            PyFluentUserWarning,
        )
    return newkwds


class Action(Base):
    """Intermediate Base class for Command and Query class."""

    _child_classes = {}
    _child_aliases = {}
    argument_names = []

    def __init__(self, name: str | None = None, parent=None):
        """__init__ of Action class."""
        super().__init__(name, parent)
        if hasattr(self, "argument_names"):
            for argument in self.argument_names:
                cls = self.__class__._child_classes[argument]
                self._setattr(argument, _create_child(cls, None, self))

    def get_completer_info(self, prefix="", excluded=None) -> List[List[str]]:
        """Get completer info of all arguments.

        Returns
        -------
        List[List[str]]
            Name, type and docstring of all arguments.
        """
        excluded = excluded or []
        ret = []
        for argument_name in self.argument_names:
            if argument_name not in excluded and argument_name.startswith(prefix):
                argument = getattr(self, argument_name)
                if argument.is_active():
                    ret.append(
                        [
                            argument_name,
                            argument.__class__.__bases__[0].__name__,
                            argument.__doc__,
                        ]
                    )
        return ret

    def __getattr__(self, name: str):
        alias = self._child_aliases.get(name)
        if alias:
            alias = alias[0]
            alias_obj = self._child_alias_objs.get(name)
            if alias_obj is None:
                obj = self.find_object(alias)
                alias_obj = self._child_alias_objs[name] = _create_child(
                    obj.__class__, None, obj.parent, alias
                )
            return alias_obj
        else:
            return getattr(super(), name)


class BaseCommand(Action):
    """Executes command."""

    def _execute_command(self, *args, **kwds):
        """Execute a command with the specified positional and keyword arguments."""
        if self.flproxy.is_interactive_mode():
            prompt = self.flproxy.get_command_confirmation_prompt(
                self._parent.path, self.obj_name, **kwds
            )
            if prompt:
                valid_responses = {"y": True, "yes": True, "n": False, "no": False}
                while True:
                    response = input(prompt + ": y[es]/n[o] ").strip().lower()
                    if response in valid_responses:
                        if not valid_responses[response]:
                            return
                        break
                    else:
                        print("Please enter 'y[es]' or 'n[o]'.")
        with self._while_executing_command():
            ret = self.flproxy.execute_cmd(self._parent.path, self.obj_name, **kwds)
            if os.getenv("PYFLUENT_NO_FIX_PARAMETER_LIST_RETURN") != "1":
                if (self._parent.path, self.obj_name) in [
                    ("parameters/input-parameters", "list"),
                    ("parameters/output-parameters", "list"),
                ]:
                    ret = _fix_parameter_list_return(ret)
            return ret

    def execute_command(self, *args, **kwds):
        """Execute command."""
        kwds = _get_new_keywords(self, *args, **kwds)
        scmKwds = {}
        for arg, value in kwds.items():
            argument = getattr(self, arg)
            # Convert path-like values for possible file transfer
            value = argument.before_execute(
                command_name=self.python_name, value=value, kwargs=kwds
            )
            # Convert key-value to Scheme key-value
            scmKwds[argument.fluent_name] = argument.to_scheme_keys(
                value,
                argument._root.__class__,
                _get_python_path_comps(argument),
            )
        ret = self._execute_command(*args, **scmKwds)
        for arg, value in kwds.items():
            argument = getattr(self, arg)
            argument.after_execute(
                command_name=self.python_name, value=value, kwargs=kwds
            )
        if (
            self.obj_name in ["create", "make-a-copy"]
            and isinstance(self._parent, NamedObject)
            and ret in self._parent
        ):
            return self._parent[ret]
        return_t = getattr(self, "return_type", None)
        if return_t:
            base_t = _baseTypes.get(return_t)
            if base_t:
                assert_type(ret, base_t._state_type)
            return ret

    def __call__(self, *args, **kwds):
        try:
            return self.execute_command(*args, **kwds)
        except KeyboardInterrupt:
            self._root._on_interrupt(self)
            raise KeyboardInterrupt


# TODO: Remove this after parameter list() method is fixed from Fluent side
def _fix_parameter_list_return(val):
    if isinstance(val, dict):
        new_val = {}
        for name, v in val.items():
            value, units = v
            if len(units) > 0 and isinstance(units[0], str):
                # Symbols are not stripped in the command return in PyConsole.
                # Following code will work in both PyConsole and PyFluent.
                unit = units[0].lstrip("'")
                unit_labels = _fix_parameter_list_return.scheme_eval(
                    f"(units/inquire-available-label-strings-for-quantity '{unit})"
                )
                unit_label = unit_labels[0] if len(unit_labels) > 0 else ""
            else:
                unit_label = ""
            new_val[name] = [value, unit_label]
        return new_val
    return val


_fix_parameter_list_return.scheme_eval = None


class Command(BaseCommand):
    """Command object."""

    def __call__(self, **kwds):
        """Call a command with the specified keyword arguments."""
        try:
            return self.execute_command(**kwds)
        except KeyboardInterrupt:
            self._root._on_interrupt(self)
            raise KeyboardInterrupt


class CommandWithPositionalArgs(BaseCommand):
    """Command Object supporting positional arguments."""

    def __call__(self, *args, **kwds):
        """Call a command with the specified positional and keyword arguments."""
        try:
            return self.execute_command(*args, **kwds)
        except KeyboardInterrupt:
            self._root._on_interrupt(self)
            raise KeyboardInterrupt


class Query(Action):
    """Query object."""

    def __call__(self, **kwds):
        """Call a query with the specified keyword arguments."""
        kwds = _get_new_keywords(self, **kwds)
        scmKwds = {}
        for arg, value in kwds.items():
            argument = getattr(self, arg)
            # Convert key-value to Scheme key-value
            scmKwds[argument.fluent_name] = argument.to_scheme_keys(
                value,
                argument._root.__class__,
                _get_python_path_comps(argument),
            )
        return self.flproxy.execute_query(self._parent.path, self.obj_name, **scmKwds)


_baseTypes = {
    "group": Group,
    "integer": Integer,
    "real": Real,
    "string/symbol": String,
    "string": String,
    "boolean": Boolean,
    "real-list": RealList,
    "integer-list": IntegerList,
    "string-list": StringList,
    "boolean-list": BooleanList,
    "named-object": NamedObject,
    "vector": RealVector,
    "command": Command,
    "query": Query,
    "material-property": String,
    "thread-var": String,
    "list-object": ListObject,
    "file": Filename,
    "file-list": FilenameList,
    "map": Map,
}


def _clean_helpinfo(helpinfo):
    helpinfo = helpinfo.strip("\n")
    if not helpinfo.endswith("."):
        helpinfo += "."
    helpinfo = helpinfo[0].upper() + helpinfo[1:]
    return helpinfo


class _ChildNamedObjectAccessorMixin(collections.abc.MutableMapping):
    """A mixin class to provide a dictionary interface at a Group class level if the
    Group has multiple named objects of a similar type. For example, boundary conditions
    are grouped by type but quite often we want to access them without the type context.

    The following can be used:
    for name, boundary in setup.boundary_conditions.items():
        print (name, boundary())

    even though actual boundary conditions are stored one level lower to
    boundary_conditions.
    """

    def __getitem__(self, name):
        """Get a child object."""
        for cname in self.child_names:
            cobj = getattr(self, cname)
            try:
                return cobj[name]
            except Exception:
                pass
        raise KeyError(name)

    def __setitem__(self, name, value):
        """Set the state of a child object."""
        self[name].set_state(value)

    def __delitem__(self, name):
        """Delete a child object."""
        for cname in self.child_names:
            cobj = getattr(self, cname)
            try:
                del cobj[name]
                return
            except Exception:
                pass
        raise KeyError(name)

    def __iter__(self):
        """Iterator for child named objects."""
        for cname in self.child_names:
            try:
                for item in getattr(self, cname):
                    yield item
            except Exception:
                continue

    def __len__(self):
        """Number of child named objects."""
        count = 0
        for cname in self.child_names:
            cobj = getattr(self, cname)
            if isinstance(cobj, NamedObject):
                count += len(cobj)
        return count


class CreatableNamedObjectMixin(collections.abc.MutableMapping, Generic[ChildTypeT]):
    """Provides creatable named objects for Fluent 2025 R1 and later."""

    def __setitem__(self, name: str, value):
        if name not in self.get_object_names():
            if self.flproxy.has_wildcard(name):
                child = WildcardPath(
                    self.flproxy,
                    self.path + "/" + name,
                    self.__class__,
                    self.__class__.child_object_type,
                    self,
                )
            else:
                with self._while_creating():
                    self.flproxy.create(self.path, name)
                child = self._create_child_object(name)
        else:
            child = self._objects.get(name)
            if not child:
                child = self._create_child_object(name)
        child.set_state(value)


class CreatableNamedObjectMixinOld(CreatableNamedObjectMixin):
    """Provides creatable named objects for Fluent 2024 R2 and earlier."""

    # In Fluent 2025 R1, the ``create()`` method is available as commands in the ``NamedObject`` class.
    def create(self, name: str = "") -> ChildTypeT:
        """Create a named object.

        Parameters
        ----------
        name: str
            Name of the new object.

        Returns
        -------
        Object
            Object that has been created.
        """
        with self._while_creating():
            self.flproxy.create(self.path, name)
        return self._create_child_object(name)


class _NonCreatableNamedObjectMixin(
    collections.abc.MutableMapping, Generic[ChildTypeT]
):
    def __setitem__(self, name: str, value):
        if name not in self.get_object_names():
            if self.flproxy.has_wildcard(name):
                child = WildcardPath(
                    self.flproxy,
                    self.path + "/" + name,
                    self.__class__,
                    self.__class__.child_object_type,
                    self,
                )
            else:
                raise KeyError(
                    allowed_name_error_message(
                        context=self.__class__._python_name,
                        trial_name=name,
                        allowed_values=self.get_object_names(),
                    )
                )
        else:
            child = self._objects.get(name)
            if not child:
                child = self._create_child_object(name)
        child.set_state(value)


class AllowedValuesMixin:
    """Provides allowed values."""

    def allowed_values(self):
        """Get the allowed values of the object."""
        try:
            return self.get_attr(_InlineConstants.allowed_values, (list, str))
        except Exception:
            return []


_bases_by_class = {}


# pylint: disable=missing-raises-doc
def get_cls(name, info, parent=None, version=None, parent_taboo=None):
    """Create a class for the object identified by "path"."""
    try:
        if name == "":
            pname = "root"
        else:
            pname = to_python_name(name)
        obj_type = info["type"]
        base = _baseTypes.get(obj_type)
        if obj_type == "command" and name in ["create", "rename", "delete", "resize"]:
            base = CommandWithPositionalArgs
        if base is None:
            settings_logger.warning(
                f"Unable to find base class for '{name}' "
                f"(type = '{obj_type}'). "
                f"Falling back to String."
            )
            base = String
        dct = {"fluent_name": name, "version": version}
        helpinfo = info.get("help")
        if helpinfo:
            dct["__doc__"] = _clean_helpinfo(helpinfo)
        else:
            if parent is None:
                dct["__doc__"] = "'root' object."
            else:
                if obj_type == "command":
                    dct["__doc__"] = f"'{pname.strip('_')}' command."
                elif obj_type == "query":
                    dct["__doc__"] = f"'{pname.strip('_')}' query."
                else:
                    dct["__doc__"] = f"'{pname.strip('_')}' child."

        include_child_named_objects = info.get(
            "include-child-named-objects?", False
        ) or info.get("include_child_named_objects", False)
        user_creatable = info.get("user-creatable?", False) or info.get(
            "user_creatable", False
        )

        if version == "222":
            user_creatable = True

        bases = (base,)
        if include_child_named_objects:
            bases = bases + (_ChildNamedObjectAccessorMixin,)
        if obj_type == "named-object" and user_creatable:
            if version < "251":
                bases = bases + (CreatableNamedObjectMixinOld,)
            else:
                bases = bases + (CreatableNamedObjectMixin,)
        elif obj_type == "named-object":
            bases = bases + (_NonCreatableNamedObjectMixin,)
        elif info.get("has-allowed-values"):
            bases += (AllowedValuesMixin,)
        elif info.get("file_purpose") == "input":
            bases += (_InputFile,)
        elif info.get("file_purpose") == "output":
            bases += (_OutputFile,)
        elif info.get("file_purpose") == "inout":
            bases += (_InOutFile,)

        original_pname = pname
        i = 1
        if parent_taboo:
            while pname in parent_taboo:
                pname = f"{original_pname}_{i}"
                i += 1
        parent_attr_name = pname
        if info.get("file_purpose"):  # not generalizing for performance
            while pname in _bases_by_class and _bases_by_class[pname] != bases:
                pname = f"{original_pname}_{i}"
                i += 1
            _bases_by_class[pname] = bases
        if parent_taboo:
            parent_taboo.add(pname)

        dct["_child_classes"] = {}
        cls = type(pname, bases, dct)

        taboo = set(dir(cls))
        taboo |= set(
            [
                "child_names",
                "command_names",
                "query_names",
                "argument_names",
                "child_object_type",
            ]
        )

        doc = ""

        def _process_cls_names(info_dict, names, write_doc=False):
            nonlocal taboo
            nonlocal cls

            for cname, cinfo in info_dict.items():
                ccls, parent_attr_name = get_cls(
                    cname, cinfo, cls, version=version, parent_taboo=taboo
                )

                if write_doc:
                    nonlocal doc
                    th = ccls._state_type
                    th = th.__name__ if hasattr(th, "__name__") else str(th)
                    doc += f"    {ccls.__name__} : {th}\n"
                    doc += f"        {ccls.__doc__}\n"

                names.append(parent_attr_name)
                taboo.add(ccls.__name__)
                cls._child_classes[parent_attr_name] = ccls

        children = info.get("children")
        if children:
            taboo.add("child_names")
            cls.child_names = []
            _process_cls_names(children, cls.child_names)

        commands = info.get("commands")
        if commands:
            commands.pop("exit", None)
            commands.pop("switch-to-meshing-mode", None)
        if commands and not user_creatable:
            commands.pop("create", None)
        if commands:
            cls.command_names = []
            _process_cls_names(commands, cls.command_names)

        queries = info.get("queries")
        if queries:
            cls.query_names = []
            _process_cls_names(queries, cls.query_names)

        arguments = info.get("arguments")
        if arguments:
            doc = cls.__doc__
            doc += "\n\n"
            doc += "Parameters\n"
            doc += "----------\n"
            cls.argument_names = []
            _process_cls_names(arguments, cls.argument_names, write_doc=True)
            cls.__doc__ = doc

        if version < "242":
            cls.return_type = "object"
        else:
            return_type = info.get("return-type") or info.get("return_type")
            if return_type:
                cls.return_type = return_type

        object_type = info.get("object-type", False) or info.get("object_type", False)
        if object_type:
            cls.child_object_type, _ = get_cls(
                "child-object-type", object_type, cls, version=version
            )
            cls.child_object_type.get_name = lambda self: self._name

        child_aliases = info.get("child-aliases") or info.get("child_aliases", {})
        command_aliases = info.get("command-aliases") or info.get("command_aliases", {})
        query_aliases = info.get("query-aliases") or info.get("query_aliases", {})
        argument_aliases = info.get("arguments-aliases") or info.get(
            "arguments_aliases", {}
        )
        if child_aliases or command_aliases or query_aliases or argument_aliases:
            cls._child_aliases = {}
            # No need to differentiate in the Python implementation
            for k, v in (
                child_aliases | command_aliases | query_aliases | argument_aliases
            ).items():
                # Storing the original name as we don't have any other way
                # to recover it at runtime.
                cls._child_aliases[to_python_name(k)] = (
                    "/".join(
                        x if x == ".." else to_python_name(x) for x in v.split("/")
                    ),
                    k,
                )

    except Exception:
        print(
            f"Unable to construct class for '{name}' of "
            f"'{parent.fluent_name if parent else None}'"
        )
        raise
    return cls, parent_attr_name


def _gethash(obj_info):
    dhash = hashlib.sha256()
    dhash.update(pickle.dumps(obj_info))
    return dhash.hexdigest()


def get_root(
    flproxy,
    version: str = "",
    interrupt: Any | None = None,
    file_transfer_service: Any | None = None,
    scheme_eval=None,
) -> Group:
    """Get the root settings object.

    Parameters
    ----------
    flproxy: Proxy
        Object that interfaces with the Fluent backend.
    interrupt: optional
        To interrupt interruptible commands.
    file_transfer_service : optional
        File transfer service. Uploads/downloads files to/from the server.
    scheme_eval : Any
        A gRPC service to execute Scheme code.
    version : str
        Fluent version.

    Returns
    -------
    root object

    Raises
    ------
    RuntimeError
        If hash values are inconsistent.
    """
    from ansys.fluent.core import CODEGEN_OUTDIR, utils

    try:
        settings = utils.load_module(
            f"settings_{version}",
            CODEGEN_OUTDIR / "solver" / f"settings_{version}.py",
        )
        root_cls = settings.root
    except FileNotFoundError:
        obj_info = flproxy.get_static_info()
        root_cls, _ = get_cls("", obj_info, version=version)
    root = root_cls()
    root.set_flproxy(flproxy)
    root._set_on_interrupt(interrupt)
    root._set_file_transfer_service(file_transfer_service)
    _Alias.scheme_eval = scheme_eval
    _fix_parameter_list_return.scheme_eval = scheme_eval
    root._setattr("_file_transfer_service", file_transfer_service)
    return root


def find_children(obj, identifier="*"):
    """Returns path of all the child objects matching an identifier.

    Parameters
    ----------
    obj: Object
        Object whose children need to be queried.
    identifier: str
        Identifier to find specific children.

    Returns
    -------
    List
    """
    list_of_children = []
    _list_children(obj.__class__, identifier, [], list_of_children)
    return list_of_children


def _list_children(cls, identifier, path, list_of_children):
    if issubclass(cls, (NamedObject, ListObject)):
        if hasattr(cls.child_object_type, "child_names"):
            _get_child_path(cls.child_object_type, path, identifier, list_of_children)
    if issubclass(cls, Group):
        _get_child_path(cls, path, identifier, list_of_children)


def _get_child_path(cls, path, identifier, list_of_children):
    for name in cls.child_names:
        path.append(name)
        if fnmatch.fnmatch(name, identifier):
            path_to_append = "/".join(path)
            if path_to_append not in list_of_children:
                list_of_children.append(path_to_append)
        _list_children(cls._child_classes[name], identifier, path, list_of_children)
        path.pop()
