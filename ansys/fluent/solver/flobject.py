"""
Module for accessing and modifying hierarchy of Fluent settings.

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
__all__ = ['get_root']

import collections
import weakref
import string
from typing import Union, List, Dict, Generic, TypeVar

# Type hints
RealType = Union[float, str] # constant or expression
RealListType = List[RealType]
RealVectorType = List[RealType]
IntListType = List[int]
StringListType = List[str]
BoolListType = List[bool]
PrimitiveStateType = Union[str, RealType, int,  bool,
        RealListType, IntListType, StringListType, BoolListType]
DictStateType = Dict[str, 'StateType']
ListStateType = List['StateType']
StateType = Union[PrimitiveStateType, DictStateType, ListStateType]

_ttable = str.maketrans(string.punctuation, '_'*len(string.punctuation), "?'")

def to_python_name(scheme_name: str) -> str:
    """
    Convert a scheme string to python variable name by replacing symbols
    with _. `?`s are  ignored.
    """
    if not scheme_name:
        return scheme_name
    return scheme_name.translate(_ttable)

class Base:
    """
    Base class for settings and command objects.

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
    scheme_name

    """
    _initialized = False

    def __init__(self, name: str = None, parent = None):
        self._parent = weakref.proxy(parent) if parent is not None else None
        if name is not None:
            self._name = name

    _flproxy = None

    @classmethod
    def set_flproxy(cls, flproxy):
        """Set flproxy object"""
        cls._flproxy = flproxy

    @property
    def flproxy(self):
        """
        Proxy object. Is set at the root level, and accessed via parent for
        child classes
        """
        if self._flproxy is None:
            return self._parent.flproxy
        return self._flproxy

    _name = None
    scheme_name = None

    @property
    def obj_name(self):
        """
        Scheme name of this object.
        By default, this returns the object's static name.
        If the object is a named-object child, the object's name is returned
        """
        if self._name is None:
            return self.scheme_name
        return self._name

    @property
    def path(self):
        """
        Path of this object.
        Constructed from obj_name of self and path of parent
        """
        if self._parent is None:
            return self.obj_name
        ppath = self._parent.path
        if not ppath:
            return self.obj_name
        return ppath + '/' + self.obj_name

StateT = TypeVar('StateT')
class SettingsBase(Base, Generic[StateT]):
    """Base class for settings objects"""

    @classmethod
    def to_scheme_keys(cls, value):
        """
        Convert value to have keys with scheme names.
        This is overridden in Group, NamedObject and ListObject classes.
        """
        return value

    @classmethod
    def to_python_keys(cls, value):
        """
        Convert value to have keys with python names.
        This is overridden in Group, NamedObject and ListObject classes.
        """
        return value

    def __call__(self) -> StateT:
        """
        Alias for self.get_state
        """
        return self.get_state()

    def get_state(self) -> StateT:
        """
        Get the state of this object
        """
        return self.to_python_keys(self.flproxy.get_var(self.path))

    def set_state(self, state: StateT):
        """
        Set the state of this object
        """
        return self.flproxy.set_var(self.path, self.to_scheme_keys(state))


class Integer(SettingsBase[int]):
    """
    An Integer object represents an integer value setting.
    """

class Real(SettingsBase[RealType]):
    """
    A Real object represents a real value setting.
    Some Real objects also accept string arguments representing expression
    values.
    """

class String(SettingsBase[str]):
    """
    A String object represents a string value setting.
    """

class Boolean(SettingsBase[bool]):
    """
    A Boolean object represents a boolean value setting.
    """

class RealList(SettingsBase[RealListType]):
    """
    A RealList object represents a real list setting.
    """

class IntegerList(SettingsBase[IntListType]):
    """
    An Integer object represents a integer list setting.
    """

class RealVector(SettingsBase[RealVectorType]):
    """
    A RealVector object represents a real vector setting consisting of
    3 real values.
    """

class StringList(SettingsBase[StringListType]):
    """
    A StringList object represents a string list setting.
    """

class BooleanList(SettingsBase[StringListType]):
    """
    A BooleanList object represents a boolean list setting.
    """

class Group(SettingsBase[DictStateType]):
    """
    A Group object is a container object, similar to a C++ struct object.
    Child objects can be accessed via attribute access.

    Attributes
    ----------
    member_names: list[str]
                  Names of the child (member) objects
    command_names: list[str]
                   Names of the commands
    """
    def __init__(self, name: str = None, parent = None):
        super().__init__(name, parent)
        for member in self.member_names:
            cls = getattr(self.__class__, member)
            setattr(self, member, cls(None, self))
        for cmd in self.command_names:
            cls = getattr(self.__class__, cmd)
            setattr(self, cmd, cls(None, self))
        self._initialized = True

    @classmethod
    def to_scheme_keys(cls, value):
        """
        Convert value to have keys with scheme names.
        """
        if isinstance(value, collections.abc.Mapping):
            ret = {}
            for k, v in value.items():
                if k in cls.member_names:
                    ccls = getattr(cls, k)
                    ret[ccls.scheme_name] = ccls.to_scheme_keys(v)
                else:
                    raise RuntimeError("Key '" + str(k) + "' is invalid")
            return ret
        else:
            return value

    @classmethod
    def to_python_keys(cls, value):
        """
        Convert value to have keys with python names.
        """
        if isinstance(value, collections.abc.Mapping):
            ret = {}
            undef = object()
            for mname in cls.member_names:
                ccls = getattr(cls, mname)
                mvalue = value.get(ccls.scheme_name, undef)
                if mvalue is not undef:
                    ret[mname] = ccls.to_python_keys(mvalue)
            return ret
        else:
            return value

    member_names = []
    command_names = []

    def __setattr__(self, name: str, value):
        if not self._initialized or name[0] == '_':
            super().__setattr__(name, value)
        else:
            getattr(self, name).set_state(value)

class NamedObject(SettingsBase[DictStateType]):
    """
    A NamedObject object is a container object, similar to a Python dict
    object. Generally, many such objects can be created with different
    names.

    Attributes
    ----------
    object_names: list[str]
                  Names of the created objects
    command_names: list[str]
                   Names of the commands
    """
    # New objects could get inserted by other operations, so we cannot assume
    # that the local cache in self._objects is always up-to-date
    def __init__(self, name: str = None, parent = None):
        super().__init__(name, parent)
        self._objects = {}
        for cmd in self.command_names:
            cls = getattr(self.__class__, cmd)
            setattr(self, cmd, cls(None, self))

    @classmethod
    def to_scheme_keys(cls, value):
        """
        Convert value to have keys with scheme names.
        """
        if isinstance(value, collections.abc.Mapping):
            ret = {}
            for k, v in value.items():
                ret[k] = cls.child_object_type.to_scheme_keys(v)
            return ret
        else:
            return value

    @classmethod
    def to_python_keys(cls, value):
        if isinstance(value, collections.abc.Mapping):
            ret = {}
            for k, v in value.items():
                ret[k] = cls.child_object_type.to_python_keys(v)
            return ret
        else:
            return value

    command_names = []

    def _create_child_object(self, cname: str):
        ret = self._objects.get(cname)
        if not ret:
            #pylint: disable=no-member
            cls = self.__class__.child_object_type
            ret = self._objects[cname] = cls(cname, self)
        return ret

    def _update_objects(self):
        names = self.object_names
        for name in list(self._objects.keys()):
            if name not in names:
                del self._objects[name]
        for name in names:
            if name not in self._objects:
                self._create_child_object(name)

    def rename(self, new: str, old: str):
        """
        Rename a named object

        Parameters:
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
        return name in self.object_names

    def __len__(self):
        return len(self.keys())

    def __iter__(self):
        self._update_objects()
        return iter(self._objects)

    def keys(self):
        """object names"""
        self._update_objects()
        return self._objects.keys()

    def values(self):
        """object values"""
        self._update_objects()
        return self._objects.values()

    def items(self):
        """Items"""
        self._update_objects()
        return self._objects.items()

    def create(self, name: str):
        """
        Create a named object with given name

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

    @property
    def object_names(self):
        """object names"""
        return self.flproxy.get_object_names(self.path)

    def __getitem__(self, name: str):
        if name not in self.object_names:
            raise KeyError(name)
        obj = self._objects.get(name)
        if not obj:
            obj = self._create_child_object(name)
        return obj

    def __setitem__(self, name: str, value):
        if name not in self.object_names:
            self.flproxy.create(self.path, name)
        child = self._objects.get(name)
        if not child:
            child = self._create_child_object(name)
        child.set_state(value)

class ListObject(SettingsBase[ListStateType]):
    """
    A ListObject object is a container object, similar to a Python list object.
    Generally, many such objects can be created.

    Attributes
    ----------
    size: int
          Number of items in the list
    command_names: list[str]
                   Names of the commands
    """
    # New objects could get inserted by other operations, so we cannot assume
    # that the local cache in self._objects is always up-to-date
    def __init__(self, name = None, parent = None):
        super().__init__(name, parent)
        self._objects = []
        for cmd in self.command_names:
            cls = getattr(self.__class__, cmd)
            setattr(self, cmd, cls(None, self))

    @classmethod
    def to_scheme_keys(cls, value):
        """
        Convert value to have keys with scheme names.
        """
        if isinstance(value, collections.abc.Sequence):
            return [cls.child_object_type.to_scheme_keys(v) for v in value]
        else:
            return value

    @classmethod
    def to_python_keys(cls, value):
        """
        Convert value to have keys with scheme names.
        """
        if isinstance(value, collections.abc.Sequence):
            return [cls.child_object_type.to_python_keys(v) for v in value]
        else:
            return value

    command_names = []

    def _update_objects(self):
        # pylint: disable=no-member
        cls = self.__class__.child_object_type
        self._objects = [cls(str(x), self) for x in range(self.size)]

    def __len__(self):
        return self.size

    def __iter__(self):
        self._update_objects()
        return iter(self._objects)

    @property
    def size(self) -> int:
        """
        Return the number of elements in a list object

        Returns
        -------
        int
        """
        return self.flproxy.get_list_size(self.path)

    def resize(self, size: int):
        """
        Resize a list object

        Parameters
        ----------
        size: int
              New size
        """
        self.flproxy.resize_list_object(self.path, size)

    def __getitem__(self, index: int):
        size = self.size
        if index >= size:
            raise IndexError(index)
        if len(self._objects) != size:
            self._update_objects()
        return self._objects[index]

    def __setitem__(self, index: int, value):
        child = self[index]
        child.set_state(value)

class Command(Base):
    """Command object"""
    def __call__(self, **kwds):
        """
        Call a command with the specified keyword arguments
        """
        newkwds = {}
        for k, v in kwds.items():
            if k in self.argument_names:
                ccls = getattr(self, k)
                newkwds[ccls.scheme_name] = ccls.to_scheme_keys(v)
            else:
                raise RuntimeError("Argument '" + str(k) + "' is invalid")
        return self.flproxy.execute_cmd(self._parent.path,
                self.obj_name,
                **newkwds)

_baseTypes = {
        'group'        : Group,
        'integer'      : Integer,
        'real'         : Real,
        'string/symbol': String,
        'boolean'      : Boolean,
        'real-list'    : RealList,
        'integer-list' : IntegerList,
        'string-list'  : StringList,
        'boolean-list' : BooleanList,
        'named-object' : NamedObject,
        'vector'       : RealVector,
        'command'      : Command,
        'material-property' : String,
        'thread-var'   : String,
        'list-object' : ListObject,
        }

def get_cls(name, info, parent = None):
    """
    Create a class for the object identified by "path"
    """
    if name == '':
        pname = 'root'
    else:
        pname = to_python_name(name)
    obj_type = info['type']
    base = _baseTypes[obj_type]
    dct = { 'scheme_name' : name }
    helpinfo = info.get('help')
    if helpinfo:
        dct['__doc__'] = helpinfo
    else:
        if parent is None:
            dct['__doc__'] = 'root object'
        else:
            dct['__doc__'] = f"'{pname}' member of '{parent.__name__}' object"
    cls = type(pname, (base,), dct)

    children = info.get('children')
    if children:
        cls.member_names = []
        for cname, cinfo in children.items():
            ccls = get_cls(cname, cinfo, cls)
            #pylint: disable=no-member
            cls.member_names.append(ccls.__name__)
            setattr(cls, ccls.__name__, ccls)
    commands = info.get('commands')
    if commands:
        cls.command_names = []
        for cname, cinfo in commands.items():
            ccls = get_cls(cname, cinfo, cls)
            #pylint: disable=no-member
            cls.command_names.append(ccls.__name__)
            setattr(cls, ccls.__name__, ccls)
    arguments = info.get('arguments')
    if arguments:
        cls.argument_names = []
        for aname, ainfo in arguments.items():
            ccls = get_cls(aname, ainfo, cls)
            #pylint: disable=no-member
            cls.argument_names.append(ccls.__name__)
            setattr(cls, ccls.__name__, ccls)
    object_type = info.get('object-type')
    if object_type:
        cls.child_object_type = \
                get_cls(cls.__name__ + '-object-type', object_type, cls)
    return cls

def get_root(flproxy):
    """
    Get the root settings object.

    Parameters
    ----------
    flproxy: Proxy
             Object that interfaces with the Fluent backend
    """

    obj_info = flproxy.get_obj_static_info()
    cls = get_cls('', obj_info)
    #pylint: disable=no-member
    cls.set_flproxy(flproxy)
    return cls()
