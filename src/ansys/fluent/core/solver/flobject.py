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
import importlib
import keyword
import logging
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
    Optional,
    Tuple,
    TypeVar,
    Union,
    _eval_type,
    get_args,
    get_origin,
)
import warnings
import weakref

try:
    import ansys.units as ansys_units

    from .flunits import UnhandledQuantity, get_si_unit_for_fluent_quantity
except ImportError:
    get_unit_for_fl_quantity_attr = None
    ansys_units = None

from .error_message import allowed_name_error_message, allowed_values_error

settings_logger = logging.getLogger("pyfluent.settings_api")


class InactiveObjectError(RuntimeError):
    """Inactive object access."""

    def __init__(self, python_path):
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


class Base:
    """Base class for settings and command objects.

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

    def __init__(self, name: Optional[str] = None, parent=None):
        """__init__ of Base class."""
        self._setattr("_parent", weakref.proxy(parent) if parent is not None else None)
        self._setattr("_flproxy", None)
        self._setattr("_file_transfer_service", None)
        if name is not None:
            self._setattr("_name", name)
        self._setattr("_child_alias_objs", {})

    def set_flproxy(self, flproxy):
        """Set flproxy object."""
        self._setattr("_flproxy", flproxy)

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
    def file_transfer_service(self):
        """Remote file handler.

        Supports file upload and download.
        """
        if self._file_transfer_service:
            return self._file_transfer_service
        elif self._parent:
            return self._parent.file_transfer_service

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
            return "<session>"
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
        attr_type_or_types: Optional[Union[type, Tuple[type]]] = None,
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

    def before_execute(self, value):
        """Executes before command execution."""
        if hasattr(self, "_do_before_execute"):
            self._do_before_execute(value)

    def after_execute(self, value):
        """Executes after command execution."""
        if hasattr(self, "_do_after_execute"):
            self._do_after_execute(value)

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

    def as_quantity(self) -> Optional[ansys_units.Quantity]:
        """Get the state of the object as an ansys.units.Quantity."""
        error = None
        if not ansys_units:
            error = "Code not configured to support units."
        if not error:
            quantity = self.get_attr("units-quantity")
            units = get_si_unit_for_fluent_quantity(quantity)
            if units is not None:
                try:
                    return ansys_units.Quantity(
                        value=self.get_state(),
                        units=units,
                    )
                except (TypeError, ValueError) as e:
                    error = e
            else:
                error = "Could not determine units."
        warnings.warn(f"Unable to construct 'Quantity'. {error}")

    def set_state(self, state: Optional[StateT] = None, **kwargs):
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

            if ansys_units and isinstance(state, (ansys_units.Quantity, tuple)):
                state = (
                    ansys_units.Quantity(*state) if isinstance(state, tuple) else state
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

    def units(self) -> Optional[str]:
        """Get the physical units of the object as a string."""
        quantity = self.get_attr("units-quantity")
        return get_si_unit_for_fluent_quantity(quantity)


class Textual(Property):
    """Exposes attribute accessor on settings object - specific to string objects."""


class DeprecatedSettingWarning(FutureWarning):
    """Provides deprecated settings warning."""

    pass


class UnstableSettingWarning(UserWarning):
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
                ).strip()
                warnings.warn(
                    "Note: A newer syntax is available to perform the last operation:\n"
                    f"{journal_str}",
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
    def to_scheme_keys(cls, value: StateT) -> StateT:
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

    @classmethod
    def _unalias(cls, value):
        """Unalias the given value.

        Raises
        ------
        NotImplementedError
            If '..' is present in the alias path.
        """
        if isinstance(value, collections.abc.Mapping):
            ret = {}
            for k, v in value.items():
                if hasattr(cls, "_child_aliases") and k in cls._child_aliases:
                    alias = cls._child_aliases[k]
                    # TODO: handle ".." in alias path
                    if ".." in alias:
                        raise NotImplementedError(
                            'Cannot handle ".." in alias path while setting dictionary state.'
                        )
                    ret_alias = ret
                    comps = alias.split("/")
                    for i, comp in enumerate(comps):
                        cls = cls._child_classes[comp]
                        if i == len(comps) - 1:
                            ret_alias[comp] = cls._unalias(v)
                        else:
                            ret_alias[comp] = {}
                            ret_alias = ret_alias[comp]
                else:
                    if issubclass(cls, Group):
                        ccls = cls._child_classes[k]
                        ret[k] = ccls._unalias(v)
                    else:
                        ret[k] = cls._unalias(v)
            return ret
        else:
            return value

    def set_state(self, state: Optional[StateT] = None, **kwargs):
        """Set the state of the object."""
        with self._while_setting_state():
            if isinstance(state, (tuple, ansys_units.Quantity)) and hasattr(
                self, "value"
            ):
                self.value.set_state(state, **kwargs)
            else:
                state = self._unalias(kwargs or state)
                return self.flproxy.set_var(self.path, self.to_scheme_keys(state))

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
    def _do_before_execute(self, value):
        if self.file_transfer_service:
            self.file_transfer_service.upload(file_name=value)


class _OutputFile(FileName):
    def _do_after_execute(self, value):
        if self.file_transfer_service:
            self.file_transfer_service.download(file_name=value)


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

    def __init__(self, name: Optional[str] = None, parent=None):
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
    def to_scheme_keys(cls, value):
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
                    ret[ccls.fluent_name] = ccls.to_scheme_keys(v)
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
            return value

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

    def _get_parent_of_active_child_names(self, name):
        with warnings.catch_warnings():
            warnings.filterwarnings(action="ignore", category=UnstableSettingWarning)
            parents = ""
            path_list = []
            for parent in self.get_active_child_names():
                try:
                    if hasattr(getattr(self, parent), str(name)):
                        path_list.append(f"    {self.python_path}.{parent}.{str(name)}")
                        if len(parents) != 0:
                            parents += ", " + parent
                        else:
                            parents += parent
                except AttributeError:
                    pass
            if len(path_list):
                print(f"\n {str(name)} can be accessed from the following paths: \n")
                for path in path_list:
                    print(path)
            if len(parents):
                return f"\n {name} is a child of {parents} \n"

    def __getattribute__(self, name):
        if name in super().__getattribute__("child_names"):
            if self.is_active() is False:
                raise InactiveObjectError(self.python_path)
        alias = super().__getattribute__("_child_aliases").get(name)
        if alias:
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
            self._get_parent_of_active_child_names(name)
            error_msg = allowed_name_error_message(
                trial_name=name,
                allowed_values=super().__getattribute__("child_names"),
                message=ex.args[0],
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
            allowed = attr.allowed_values()
            if allowed and value not in allowed:
                raise allowed_values_error(name, value, allowed) from ex
            else:
                raise ex


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
                    context=self._state_cls.__name__,
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

    def to_scheme_keys(self, value):
        """Convert value to have keys with scheme names."""
        return self._state_cls.to_scheme_keys(value)

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
    def __init__(self, name: Optional[str] = None, parent=None):
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
    def to_scheme_keys(cls, value):
        """Convert value to have keys with scheme names."""
        if isinstance(value, collections.abc.Mapping):
            ret = {}
            for k, v in value.items():
                ret[k] = cls.child_object_type.to_scheme_keys(v)
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
            return value

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
                    context=self.__class__.__name__,
                    trial_name=name,
                    allowed_values=self.get_object_names(),
                )
            )

        obj = self._objects.get(name)
        if not obj:
            obj = self._create_child_object(name)
        return obj

    def __getattr__(self, name: str):
        alias = self._child_aliases.get(name)
        if alias:
            alias_obj = self._child_alias_objs.get(name)
            if alias_obj is None:
                obj = self.find_object(alias)
                alias_obj = self._child_alias_objs[name] = _create_child(
                    obj.__class__, None, obj.parent, alias
                )
            return alias_obj
        else:
            return getattr(super(), name)


def _rename(obj: Union[NamedObject, _Alias], new: str, old: str):
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
    def to_scheme_keys(cls, value):
        """Convert value to have keys with scheme names."""
        if isinstance(value, collections.abc.Sequence):
            return [cls.child_object_type.to_scheme_keys(v) for v in value]
        else:
            return value

    @classmethod
    def to_python_keys(cls, value):
        """Convert value to have keys with scheme names."""
        if isinstance(value, collections.abc.Sequence):
            return [cls.child_object_type.to_python_keys(v) for v in value]
        else:
            return value

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


def _get_new_keywords(obj, args, kwds):
    newkwds = {}
    argNames = []
    argumentNames = []
    if args:
        argNames = obj.argument_names[:]
        for i, arg in enumerate(args):
            ccls = getattr(obj, argNames[0])
            newkwds[ccls.fluent_name] = ccls.to_scheme_keys(arg)
            argNames.pop(0)
    if kwds:
        argumentNames = obj.argument_names[:]
        if argNames:
            argumentNames = argNames
    for k, v in kwds.items():
        if k in argumentNames:
            ccls = getattr(obj, k)
            newkwds[ccls.fluent_name] = ccls.to_scheme_keys(v)
        else:
            raise RuntimeError("Argument '" + str(k) + "' is invalid")
    return newkwds


class Action(Base):
    """Intermediate Base class for Command and Query class."""

    _child_classes = {}
    _child_aliases = {}

    def __init__(self, name: Optional[str] = None, parent=None):
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

    def execute_command(self, *args, **kwds):
        """Execute command."""
        for arg, value in kwds.items():
            argument = getattr(self, arg)
            argument.before_execute(value)
        ret = self._execute_command(*args, **kwds)
        for arg, value in kwds.items():
            argument = getattr(self, arg)
            argument.after_execute(value)
        return_t = getattr(self, "return_type", None)
        if return_t:
            base_t = _baseTypes.get(return_t)
            if base_t:
                assert_type(ret, base_t._state_type)
            return ret

    def __call__(self, *args, **kwds):
        return self.execute_command(*args, **kwds)


class Command(BaseCommand):
    """Command object."""

    def _execute_command(self, **kwds):
        """Execute a command with the specified keyword arguments."""
        newkwds = _get_new_keywords(self, [], kwds)
        if self.flproxy.is_interactive_mode():
            prompt = self.flproxy.get_command_confirmation_prompt(
                self._parent.path, self.obj_name, **newkwds
            )
            if prompt:
                while True:
                    response = input(prompt + ": y[es]/n[o] ")
                    if response in ["y", "Y", "n", "N", "yes", "no"]:
                        break
                    else:
                        print("Enter y[es]/n[o]")
                if response in ["n", "N", "no"]:
                    return
        with self._while_executing_command():
            return self.flproxy.execute_cmd(self._parent.path, self.obj_name, **newkwds)

    def __call__(self, **kwds):
        """Call a command with the specified keyword arguments."""
        return self.execute_command(**kwds)


class CommandWithPositionalArgs(BaseCommand):
    """Command Object."""

    def _execute_command(self, *args, **kwds):
        """Execute a command with the specified keyword arguments."""
        newkwds = _get_new_keywords(self, args, kwds)
        if self.flproxy.is_interactive_mode():
            prompt = self.flproxy.get_command_confirmation_prompt(
                self._parent.path, self.obj_name, **newkwds
            )
            if prompt:
                while True:
                    response = input(prompt + ": y[es]/n[o] ")
                    if response in ["y", "Y", "n", "N", "yes", "no"]:
                        break
                    else:
                        print("Enter y[es]/n[o]")
                if response in ["n", "N", "no"]:
                    return
        with self._while_executing_command():
            return self.flproxy.execute_cmd(self._parent.path, self.obj_name, **newkwds)

    def __call__(self, *args, **kwds):
        """Call a command with the specified keyword arguments."""
        return self.execute_command(*args, **kwds)


class Query(Action):
    """Query object."""

    def __call__(self, **kwds):
        """Call a query with the specified keyword arguments."""
        newkwds = _get_new_keywords(self, [], kwds)
        return self.flproxy.execute_query(self._parent.path, self.obj_name, **newkwds)


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
        l = 0
        for cname in self.child_names:
            cobj = getattr(self, cname)
            if isinstance(cobj, NamedObject):
                l += len(cobj)
        return l


class _CreatableNamedObjectMixin(collections.abc.MutableMapping, Generic[ChildTypeT]):
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

    def __setitem__(self, name: str, value):
        if name not in self.get_object_names():
            with self._while_creating():
                self.flproxy.create(self.path, name)
        child = self._objects.get(name)
        if not child:
            child = self._create_child_object(name)
        child.set_state(value)


class _NonCreatableNamedObjectMixin(
    collections.abc.MutableMapping, Generic[ChildTypeT]
):
    def __setitem__(self, name: str, value):
        if name not in self.get_object_names():
            raise KeyError(name)
        child = self._objects.get(name)
        if not child:
            child = self._create_child_object(name)
        child.set_state(value)


class _HasAllowedValuesMixin:
    def allowed_values(self):
        """Get the allowed values of the object."""
        try:
            return self.get_attr(_InlineConstants.allowed_values, (list, str))
        except Exception:
            return []


_bases_by_class = {}


# pylint: disable=missing-raises-doc
def get_cls(name, info, parent=None, version=None):
    """Create a class for the object identified by "path"."""
    try:
        if name == "":
            pname = "root"
        else:
            pname = to_python_name(name)
        obj_type = info["type"]
        base = _baseTypes.get(obj_type)
        if obj_type == "command" and name in ["rename", "delete", "resize"]:
            base = CommandWithPositionalArgs
        if base is None:
            settings_logger.warning(
                f"Unable to find base class for '{name}' "
                f"(type = '{obj_type}'). "
                f"Falling back to String."
            )
            base = String
        dct = {"fluent_name": name}
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
            bases = bases + (_CreatableNamedObjectMixin,)
        elif obj_type == "named-object":
            bases = bases + (_NonCreatableNamedObjectMixin,)
        elif info.get("has-allowed-values"):
            bases += (_HasAllowedValuesMixin,)
        elif info.get("file_purpose") == "input":
            bases += (_InputFile,)
        elif info.get("file_purpose") == "output":
            bases += (_OutputFile,)
        elif info.get("file_purpose") == "inout":
            bases += (_InOutFile,)

        original_pname = pname
        if any(
            x in bases for x in (_InputFile, _OutputFile, _InOutFile)
        ):  # not generalizing for performance
            i = 0
            while pname in _bases_by_class and _bases_by_class[pname] != bases:
                if i > 0:
                    pname = pname[: pname.rfind("_")]
                i += 1
                pname += f"_{str(i)}"
            _bases_by_class[pname] = bases

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
                ccls, original_pname = get_cls(cname, cinfo, cls, version=version)
                ccls_name = ccls.__name__

                i = 0
                if write_doc:
                    nonlocal doc
                    th = ccls._state_type
                    th = th.__name__ if hasattr(th, "__name__") else str(th)
                    doc += f"    {ccls.__name__} : {th}\n"
                    doc += f"        {ccls.__doc__}\n"

                while ccls_name in taboo:
                    if i > 0:
                        ccls_name = ccls_name[: ccls_name.rfind("_")]
                    i += 1
                    ccls_name += f"_{str(i)}"

                ccls.__name__ = ccls_name
                names.append(ccls.__name__ if i > 0 else original_pname)
                taboo.add(ccls_name)
                cls._child_classes[ccls.__name__ if i > 0 else original_pname] = ccls

        children = info.get("children")
        if children:
            taboo.add("child_names")
            cls.child_names = []
            _process_cls_names(children, cls.child_names)

        commands = info.get("commands")
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
        if child_aliases or command_aliases or query_aliases:
            cls._child_aliases = {}
            # No need to differentiate in the Python implementation
            for k, v in (child_aliases | command_aliases | query_aliases).items():
                cls._child_aliases[to_python_name(k)] = "/".join(
                    to_python_name(x) for x in v.split("/")
                )

    except Exception:
        print(
            f"Unable to construct class for '{name}' of "
            f"'{parent.fluent_name if parent else None}'"
        )
        raise
    return cls, original_pname


def _gethash(obj_info):
    dhash = hashlib.sha256()
    dhash.update(pickle.dumps(obj_info))
    return dhash.hexdigest()


def get_root(
    flproxy,
    version: str = "",
    file_transfer_service: Optional[Any] = None,
    scheme_eval=None,
) -> Group:
    """Get the root settings object.

    Parameters
    ----------
    flproxy: Proxy
        Object that interfaces with the Fluent backend.
    file_transfer_service : optional
        File transfer service. Uploads/downloads files to/from the server.
    scheme_eval : Any
        A gRPC service to execute Scheme code.
    version : str
        Fluent version.

    Raises
    ------
    RuntimeError
        If hash values are inconsistent.

    Returns
    -------
    root object
    """
    obj_info = flproxy.get_static_info()
    try:
        settings = importlib.import_module(
            f"ansys.fluent.core.solver.settings_{version}"
        )

        if settings.SHASH != _gethash(obj_info):
            settings_logger.warning(
                "Mismatch between generated file and server object "
                "info. Dynamically created settings classes will "
                "be used."
            )
            raise RuntimeError("Mismatch in hash values")
        cls = settings.root
    except Exception:
        cls, _ = get_cls("", obj_info, version=version)
    root = cls()
    root.set_flproxy(flproxy)
    root._set_file_transfer_service(file_transfer_service)
    _Alias.scheme_eval = scheme_eval
    root._setattr("_static_info", obj_info)
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
