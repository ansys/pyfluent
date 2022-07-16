"""Module for accessing and modifying hierarchy of Fluent settings.

The only useful method is 'get_root' which returns the root object for
accessing Fluent settings.

Child objects can be generally accessed/modified using attribute access.
Named child objects can be accessed/modified using index operator.

Calling an object will return its current value.

Example
-------
r = flobject.get_root(proxy)
is_energy_on = r.setup.models.energy.enabled()
r.setup.models.energy.enabled = True
r.boundary_conditions.velocity_inlet['inlet'].vmag.constant = 20
"""
import collections
import hashlib
import keyword
import pickle
import string
import sys
from typing import Any, Dict, Generic, List, NewType, Tuple, TypeVar, Union
import weakref

from ansys.fluent.core.utils.logging import LOG

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

_ttable = str.maketrans(string.punctuation, "_" * len(string.punctuation), "?'")


def to_python_name(fluent_name: str) -> str:
    """Convert a scheme string to python variable name.

    The function does this by replacing symbols with _. '?'s are
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
           name of the object if a child of named-object.
    parent: Base
           Object's parent.

    Attributes
    ----------
    flproxy
    obj_name
    fluent_name
    """

    def __init__(self, name: str = None, parent=None):
        """__init__ of Base class."""
        self._setattr("_parent", weakref.proxy(parent) if parent is not None else None)
        self._setattr("_flproxy", None)
        if name is not None:
            self._setattr("_name", name)

    def set_flproxy(self, flproxy):
        """Set flproxy object."""
        self._setattr("_flproxy", flproxy)

    @property
    def flproxy(self):
        """Proxy object.

        This is set at the root level, and accessed via parent for child
        classes.
        """
        if self._flproxy is None:
            return self._parent.flproxy
        return self._flproxy

    _name = None
    fluent_name = None

    @property
    def parent(self):
        """The parent (container) object."""
        return self._parent

    @property
    def obj_name(self) -> str:
        """Scheme name of this object.

        By default, this returns the object's static name. If the object
        is a named-object child, the object's name is returned.
        """
        if self._name is None:
            return self.fluent_name
        return self._name

    @property
    def path(self) -> str:
        """Path of this object.

        Constructed from obj_name of self and path of parent.
        """
        if self._parent is None:
            return self.obj_name
        ppath = self._parent.path
        if not ppath:
            return self.obj_name
        return ppath + "/" + self.obj_name

    def get_attrs(self, attrs) -> Any:
        """Get the requested attributes for the object."""
        return self.flproxy.get_attrs(self.path, attrs)

    def get_attr(self, attr) -> Any:
        """Get the requested attribute for the object."""
        attrs = self.get_attrs([attr])
        if attr != "active?" and attrs.get("active?", True) is False:
            raise RuntimeError("Object is not active")
        return attrs[attr]

    def is_active(self) -> bool:
        """Indicates if the object is active."""
        return self.get_attr("active?")

    def __setattr__(self, name, value):
        raise AttributeError(name)

    # __setattr__ is overridden to prevent creation of new attributes or
    # overriding existing ones. _setattr is the backdoor to set attributes
    def _setattr(self, name, value):
        super().__setattr__(name, value)


StateT = TypeVar("StateT")


class SettingsBase(Base, Generic[StateT]):
    """Base class for settings objects.

    Methods
    -------
    get_state()
        Return the current state of the object

    set_state(state)
        Set the state of the object
    """

    @classmethod
    def to_scheme_keys(cls, value: StateT) -> StateT:
        """Convert value to have keys with scheme names.

        This is overridden in Group, NamedObject and ListObject classes.
        """
        return value

    @classmethod
    def to_python_keys(cls, value: StateT) -> StateT:
        """Convert value to have keys with python names.

        This is overridden in Group, NamedObject and ListObject classes.
        """
        return value

    def __call__(self) -> StateT:
        """Alias for self.get_state."""
        return self.get_state()

    def get_state(self) -> StateT:
        """Get the state of this object."""
        return self.to_python_keys(self.flproxy.get_var(self.path))

    def set_state(self, state: StateT):
        """Set the state of this object."""
        return self.flproxy.set_var(self.path, self.to_scheme_keys(state))

    @staticmethod
    def _print_state_helper(state, out=sys.stdout, indent=0, indent_factor=2):
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

    def print_state(self, out=sys.stdout, indent_factor=2):
        """Print the state of this object."""
        self._print_state_helper(self.get_state(), out, indent_factor=indent_factor)


class Integer(SettingsBase[int]):
    """An Integer object represents an integer value setting."""

    _state_type = int


class Real(SettingsBase[RealType]):
    """A Real object represents a real value setting.

    Some Real objects also accept string arguments representing
    expression values.
    """

    _state_type = RealType


class String(SettingsBase[str]):
    """A String object represents a string value setting."""

    _state_type = str


class Filename(SettingsBase[str]):
    """A Filename object represents a file name."""

    _state_type = str


class Boolean(SettingsBase[bool]):
    """A Boolean object represents a boolean value setting."""

    _state_type = bool


class RealList(SettingsBase[RealListType]):
    """A RealList object represents a real list setting."""

    _state_type = RealListType


class IntegerList(SettingsBase[IntListType]):
    """An Integer object represents a integer list setting."""

    _state_type = IntListType


class RealVector(SettingsBase[RealVectorType]):
    """An object to represent a 3D vector.

    A RealVector object represents a real vector setting consisting of 3
    real values.
    """

    _state_type = RealVectorType


class StringList(SettingsBase[StringListType]):
    """A StringList object represents a string list setting."""

    _state_type = StringListType


class BooleanList(SettingsBase[BoolListType]):
    """A BooleanList object represents a boolean list setting."""

    _state_type = BoolListType


class Group(SettingsBase[DictStateType]):
    """A Group container object.

    A Group object is a container similar to a C++ struct object. Child objects
    can be accessed via attribute access.

    Attributes
    ----------
    child_names: list[str]
                 Names of the child objects
    command_names: list[str]
                   Names of the commands
    """

    _state_type = DictStateType

    def __init__(self, name: str = None, parent=None):
        """__init__ of Group class."""
        super().__init__(name, parent)
        for child in self.child_names:
            cls = getattr(self.__class__, child)
            self._setattr(child, cls(None, self))
        for cmd in self.command_names:
            cls = getattr(self.__class__, cmd)
            self._setattr(cmd, cls(None, self))
        for query in self.query_names:
            cls = getattr(self.__class__, query)
            self._setattr(query, cls(None, self))

    @classmethod
    def to_scheme_keys(cls, value):
        """Convert value to have keys with scheme names."""
        if isinstance(value, collections.abc.Mapping):
            ret = {}
            for k, v in value.items():
                if k in cls.child_names:
                    ccls = getattr(cls, k)
                    ret[ccls.fluent_name] = ccls.to_scheme_keys(v)
                else:
                    raise RuntimeError("Key '" + str(k) + "' is invalid")
            return ret
        else:
            return value

    @classmethod
    def to_python_keys(cls, value):
        """Convert value to have keys with python names."""
        if isinstance(value, collections.abc.Mapping):
            ret = {}
            undef = object()
            for mname in cls.child_names:
                ccls = getattr(cls, mname)
                mvalue = value.get(ccls.fluent_name, undef)
                if mvalue is not undef:
                    ret[mname] = ccls.to_python_keys(mvalue)
            return ret
        else:
            return value

    child_names = []
    command_names = []
    query_names = []

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

    def __getattribute__(self, name):
        if name in super().__getattribute__("child_names"):
            if not self.is_active():
                raise RuntimeError(f"'{self.path}' is currently not active")
        return super().__getattribute__(name)

    def __setattr__(self, name: str, value):
        return getattr(self, name).set_state(value)


ChildTypeT = TypeVar("ChildTypeT")


class NamedObject(SettingsBase[DictStateType], Generic[ChildTypeT]):
    """A NamedObject container.

    A NamedObject is a container object, similar to a Python dict object.
    Generally, many such objects can be created with different names.

    Attributes
    ----------
    command_names: list[str]
                   Names of the commands
    """

    # New objects could get inserted by other operations, so we cannot assume
    # that the local cache in self._objects is always up-to-date
    def __init__(self, name: str = None, parent=None):
        """__init__ of NamedObject class."""
        super().__init__(name, parent)
        self._setattr("_objects", {})
        for cmd in self.command_names:
            cls = getattr(self.__class__, cmd)
            self._setattr(cmd, cls(None, self))
        for query in self.query_names:
            cls = getattr(self.__class__, query)
            self._setattr(query, cls(None, self))

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
        """Convert value to have keys with python names."""
        if isinstance(value, collections.abc.Mapping):
            ret = {}
            for k, v in value.items():
                ret[k] = cls.child_object_type.to_python_keys(v)
            return ret
        else:
            return value

    command_names = []
    query_names = []

    def _create_child_object(self, cname: str):
        ret = self._objects.get(cname)
        if not ret:
            # pylint: disable=no-member
            cls = self.__class__.child_object_type
            ret = self._objects[cname] = cls(cname, self)
        return ret

    def _update_objects(self):
        names = self.get_object_names()
        for name in list(self._objects.keys()):
            if name not in names:
                del self._objects[name]
        for name in names:
            if name not in self._objects:
                self._create_child_object(name)

    def rename(self, new: str, old: str):
        """Rename a named object.

        Parameters
        ----------
        new: str
             New name
        old: str
             Old name
        """
        self.flproxy.rename(self.path, new, old)
        if old in self._objects:
            del self._objects[old]
        self._create_child_object(new)

    def __delitem__(self, name: str):
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

    def create(self, name: str):
        """Create a named object with given name.

        Parameters
        ----------
        name: str
              Name of new object

        Returns
        -------
        The object that has been created
        """
        self.flproxy.create(self.path, name)
        return self._create_child_object(name)

    def get_object_names(self):
        """Object names."""
        return self.flproxy.get_object_names(self.path)

    def __getitem__(self, name: str) -> ChildTypeT:
        if name not in self.get_object_names():
            raise KeyError(name)
        obj = self._objects.get(name)
        if not obj:
            obj = self._create_child_object(name)
        return obj

    def __setitem__(self, name: str, value):
        if name not in self.get_object_names():
            self.flproxy.create(self.path, name)
        child = self._objects.get(name)
        if not child:
            child = self._create_child_object(name)
        child.set_state(value)


class ListObject(SettingsBase[ListStateType], Generic[ChildTypeT]):
    """A ListObject container.

    A ListObject is a container object, similar to a Python list object.
    Generally, many such objects can be created.

    Attributes
    ----------
    command_names: list[str]
                   Names of the commands

    Methods
    -------
    get_size()
        Return the size of the list

    resize(size)
        Resize the list
    """

    # New objects could get inserted by other operations, so we cannot assume
    # that the local cache in self._objects is always up-to-date
    def __init__(self, name=None, parent=None):
        """__init__ of ListObject class."""
        super().__init__(name, parent)
        self._setattr("_objects", [])
        for cmd in self.command_names:
            cls = getattr(self.__class__, cmd)
            self._setattr(cmd, cls(None, self))
        for query in self.query_names:
            cls = getattr(self.__class__, query)
            self._setattr(query, cls(None, self))

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

    command_names = []
    query_names = []

    def _update_objects(self):
        # pylint: disable=no-member
        cls = self.__class__.child_object_type
        self._setattr("_objects", [cls(str(x), self) for x in range(self.get_size())])

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

    def resize(self, size: int):
        """Resize the list object.

        Parameters
        ----------
        size: int
              New size
        """
        self.flproxy.resize_list_object(self.path, size)

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


class Map(SettingsBase[DictStateType]):
    """A Map object represents key-value settings."""


class Command(Base):
    """Command object."""

    def __call__(self, **kwds):
        """Call a command with the specified keyword arguments."""
        newkwds = {}
        for k, v in kwds.items():
            if k in self.argument_names:
                ccls = getattr(self, k)
                newkwds[ccls.fluent_name] = ccls.to_scheme_keys(v)
            else:
                raise RuntimeError("Argument '" + str(k) + "' is invalid")
        return self.flproxy.execute_cmd(self._parent.path, self.obj_name, **newkwds)


class Query(Base):
    """Query object."""

    def __call__(self, **kwds):
        """Call a query with the specified keyword arguments."""
        newkwds = {}
        for k, v in kwds.items():
            if k in self.argument_names:
                ccls = getattr(self, k)
                newkwds[ccls.fluent_name] = ccls.to_scheme_keys(v)
            else:
                raise RuntimeError("Argument '" + str(k) + "' is invalid")
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
    "map": Map,
}


def _clean_helpinfo(helpinfo):
    helpinfo = helpinfo.strip("\n")
    if not helpinfo.endswith("."):
        helpinfo += "."
    helpinfo = helpinfo[0].upper() + helpinfo[1:]
    return helpinfo


class _ChildNamedObjectAccessorMixin(collections.abc.MutableMapping):
    """A mixin class to provide dict interface at a Group class level if the
    Group has multiple named objects of similar type. For example, boundary
    conditions are grouped by type but quite often we want to access them
    without the type context.

    e.g. the following can be used:
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


def get_cls(name, info, parent=None):
    """Create a class for the object identified by "path"."""
    try:
        if name == "":
            pname = "root"
        else:
            pname = to_python_name(name)
        obj_type = info["type"]
        base = _baseTypes.get(obj_type)
        if base is None:
            LOG.error(
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

        include_child_named_objects = obj_type == "group" and pname in [
            "boundary_conditions",
            "cell_zone_conditions",
            "report_definitions",
        ]
        # include_child_name_objects = info.get("include_child_named_objects", False)
        if include_child_named_objects:
            cls = type(pname, (base, _ChildNamedObjectAccessorMixin), dct)
        else:
            cls = type(pname, (base,), dct)

        children = info.get("children")
        taboo = set(dir(cls))
        taboo |= set(
            ["child_names", "command_names", "argument_names", "child_object_type"]
        )
        if children:
            taboo.add("child_names")
            cls.child_names = []
            for cname, cinfo in children.items():
                ccls = get_cls(cname, cinfo, cls)
                i = 0
                ccls_name = ccls.__name__
                while ccls_name in taboo:
                    if i > 0:
                        ccls_name = ccls_name[: ccls_name.rfind("_")]
                    i += 1
                    ccls_name += f"_{str(i)}"
                ccls.__name__ = ccls_name
                # pylint: disable=no-member
                cls.child_names.append(ccls.__name__)
                taboo.add(ccls_name)
                setattr(cls, ccls.__name__, ccls)
        commands = info.get("commands")
        if commands:
            cls.command_names = []
            for cname, cinfo in commands.items():
                ccls = get_cls(cname, cinfo, cls)
                i = 0
                ccls_name = ccls.__name__
                while ccls_name in taboo:
                    if i > 0:
                        ccls_name = ccls_name[: ccls_name.rfind("_")]
                    i += 1
                    ccls_name += f"_{str(i)}"
                ccls.__name__ = ccls_name
                # pylint: disable=no-member
                cls.command_names.append(ccls.__name__)
                taboo.add(ccls_name)
                setattr(cls, ccls.__name__, ccls)
        queries = info.get("queries")
        if queries:
            cls.query_names = []
            for cname, cinfo in queries.items():
                ccls = get_cls(cname, cinfo, cls)
                ccls_name = ccls.__name__
                while ccls_name in cls.query_names:
                    if i > 0:
                        ccls_name = ccls_name[: ccls_name.rfind("_")]
                    i += 1
                    ccls_name += f"_{str(i)}"
                ccls.__name__ = ccls_name
                # pylint: disable=no-member
                cls.query_names.append(ccls.__name__)
                setattr(cls, ccls.__name__, ccls)

        arguments = info.get("arguments")
        if arguments:
            doc = cls.__doc__
            doc += "\n\n"
            doc += "Parameters\n"
            doc += "----------\n"
            cls.argument_names = []
            for aname, ainfo in arguments.items():
                ccls = get_cls(aname, ainfo, cls)
                i = 0
                th = ccls._state_type
                th = th.__name__ if hasattr(th, "__name__") else str(th)
                doc += f"    {ccls.__name__} : {th}\n"
                doc += f"        {ccls.__doc__}\n"
                ccls_name = ccls.__name__
                while ccls_name in taboo:
                    if i > 0:
                        ccls_name = ccls_name[: ccls_name.rfind("_")]
                    i += 1
                    ccls_name += f"_{str(i)}"
                ccls.__name__ = ccls_name
                # pylint: disable=no-member
                cls.argument_names.append(ccls.__name__)
                taboo.add(ccls_name)
                setattr(cls, ccls.__name__, ccls)

            cls.__doc__ = doc
        object_type = info.get("object-type")
        if object_type:
            cls.child_object_type = get_cls("child-object-type", object_type, cls)
            cls.child_object_type.rename = lambda self, name: self._parent.rename(
                name, self._name
            )
            cls.child_object_type.get_name = lambda self: self._name
    except Exception:
        print(
            f"Unable to construct class for '{name}' of "
            f"'{parent.fluent_name if parent else None}'"
        )
        raise
    return cls


def _gethash(obj_info):
    dhash = hashlib.sha256()
    dhash.update(pickle.dumps(obj_info))
    return dhash.hexdigest()


def get_root(flproxy) -> Group:
    """Get the root settings object.

    Parameters
    ----------
    flproxy: Proxy
             Object that interfaces with the Fluent backend

    Returns
    -------
    root object
    """
    obj_info = flproxy.get_static_info()
    try:
        from ansys.fluent.core.solver import settings

        if settings.SHASH != _gethash(obj_info):
            LOG.warning(
                "Mismatch between generated file and server object "
                "info. Dynamically created settings classes will "
                "be used."
            )
            raise RuntimeError("Mismatch in hash values")
        cls = settings.root
    except Exception:
        cls = get_cls("", obj_info)
    # pylint: disable=no-member
    root = cls()
    root.set_flproxy(flproxy)
    root._setattr("_static_info", obj_info)
    return root
