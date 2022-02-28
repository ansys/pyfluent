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
import collections
import hashlib
import keyword
import pickle
import string
import sys
import weakref
from typing import Union, List, Tuple, Dict, Generic, TypeVar, NewType
from ansys.fluent.core import LOG

# Type hints
RealType = NewType('real', Union[float, str]) # constant or expression
RealListType = List[RealType]
RealVectorType = Tuple[RealType, RealType, RealType]
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
    name = scheme_name.translate(_ttable)
    while name in keyword.kwlist:
        name = name + '_'
    return name

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
    def obj_name(self) -> str:
        """
        Scheme name of this object.
        By default, this returns the object's static name.
        If the object is a named-object child, the object's name is returned
        """
        if self._name is None:
            return self.scheme_name
        return self._name

    @property
    def path(self) -> str:
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

    def get_attrs(self, attrs) -> DictStateType:
        return self.flproxy.get_attrs(self.path, attrs)

    def get_attr(self, attr) -> StateType:
        attrs = self.get_attrs([attr])
        if attr != 'active?' and attrs.get('active?', True) is False:
            raise RuntimeError('Object is not active')
        return attrs[attr]

    def is_active(self) -> bool:
        return self.get_attr('active?')

StateT = TypeVar('StateT')
class SettingsBase(Base, Generic[StateT]):
    """
    Base class for settings objects

    Methods
    -------
    get_state()
        Return the current state of the object

    set_state(state)
        Set the state of the object
    """

    @classmethod
    def to_scheme_keys(cls, value: StateT) -> StateT:
        """
        Convert value to have keys with scheme names.
        This is overridden in Group, NamedObject and ListObject classes.
        """
        return value

    @classmethod
    def to_python_keys(cls, value: StateT) -> StateT:
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

    @staticmethod
    def _print_state_helper(state, out=sys.stdout, indent=0, indent_factor=2):
        if isinstance(state, dict):
            out.write('\n')
            for key, value in state.items():
                if value is not None:
                    out.write(f'{indent*indent_factor*" "}{key} : ')
                    SettingsBase._print_state_helper(value, out, indent+1,
                            indent_factor)
        elif isinstance(state, list):
            out.write('\n')
            for index, value in enumerate(state):
                out.write(f'{indent*indent_factor*" "}{index} : ')
                SettingsBase._print_state_helper(value, out, indent+1,
                        indent_factor)
        else:
            out.write(f'{state}\n')

    def print_state(self, out=sys.stdout, indent_factor=2):
        """
        Print the state of this object
        """
        self._print_state_helper(self.get_state(), out,
                indent_factor=indent_factor)

class Integer(SettingsBase[int]):
    """
    An Integer object represents an integer value setting.
    """
    _state_type = int

class Real(SettingsBase[RealType]):
    """
    A Real object represents a real value setting.
    Some Real objects also accept string arguments representing expression
    values.
    """
    _state_type = RealType

class String(SettingsBase[str]):
    """
    A String object represents a string value setting.
    """
    _state_type = str

class Filename(SettingsBase[str]):
    """
    A Filename object represents a file name
    """
    _state_type = str

class Boolean(SettingsBase[bool]):
    """
    A Boolean object represents a boolean value setting.
    """
    _state_type = bool

class RealList(SettingsBase[RealListType]):
    """
    A RealList object represents a real list setting.
    """
    _state_type = RealListType

class IntegerList(SettingsBase[IntListType]):
    """
    An Integer object represents a integer list setting.
    """
    _state_type = IntListType

class RealVector(SettingsBase[RealVectorType]):
    """
    A RealVector object represents a real vector setting consisting of
    3 real values.
    """
    _state_type = RealVectorType

class StringList(SettingsBase[StringListType]):
    """
    A StringList object represents a string list setting.
    """
    _state_type = StringListType

class BooleanList(SettingsBase[BoolListType]):
    """
    A BooleanList object represents a boolean list setting.
    """
    _state_type = BoolListType

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
    _state_type = DictStateType

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

    def get_active_member_names(self):
        """
        Names of members that are currently active
        """
        ret = []
        for member in self.member_names:
            if getattr(self, member).is_active():
                ret.append(member)
        return ret

    def get_active_command_names(self):
        """
        Names of commands that are currently active
        """
        ret = []
        for command in self.command_names:
            if getattr(self, command).is_active():
                ret.append(command)
        return ret

    def __getattribute__(self, name):
        if name in super().__getattribute__('member_names'):
            if not self.is_active():
                raise RuntimeError(f"'{self.path}' is currently not active")
        return super().__getattribute__(name)

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
        names = self.get_object_names()
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
        return name in self.get_object_names()

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

    def get_object_names(self):
        """object names"""
        return self.flproxy.get_object_names(self.path)

    def __getitem__(self, name: str):
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

class ListObject(SettingsBase[ListStateType]):
    """
    A ListObject object is a container object, similar to a Python list object.
    Generally, many such objects can be created.

    Methods
    -------
    get_size()
        Return the size of the list

    resize(size)
        Resize the list

    Attributes
    ----------
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
        self._objects = [cls(str(x), self) for x in range(self.get_size())]

    def __len__(self):
        return self.get_size()

    def __iter__(self):
        self._update_objects()
        return iter(self._objects)

    def get_size(self) -> int:
        """
        Return the number of elements in a list object

        Returns
        -------
        int
        """
        return self.flproxy.get_list_size(self.path)

    def resize(self, size: int):
        """
        Resize the list object

        Parameters
        ----------
        size: int
              New size
        """
        self.flproxy.resize_list_object(self.path, size)

    def __getitem__(self, index: int):
        size = self.get_size()
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
        'string'       : String,
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
        'list-object'  : ListObject,
        'file'         : Filename,
        }

def get_cls(name, info, parent = None):
    """
    Create a class for the object identified by "path"
    """
    try:
        if name == '':
            pname = 'root'
        else:
            pname = to_python_name(name)
        obj_type = info['type']
        base = _baseTypes.get(obj_type)
        if base is None:
            LOG.warning(f"Unable to find base class for '{name}' "
                    f"(type = '{obj_type}'). "
                    f"Falling back to String. "
                    f"Please report this serious "
                    f"issue including the details shown.")
            base = String
        dct = { 'scheme_name' : name }
        helpinfo = info.get('help')
        if helpinfo:
            dct['__doc__'] = helpinfo
        else:
            if parent is None:
                dct['__doc__'] = 'root object'
            else:
                if obj_type == 'command':
                    dct['__doc__'] = \
                            f"'{pname}' command of '{parent.__name__}' object"
                else:
                    dct['__doc__'] = \
                            f"'{pname}' member of '{parent.__name__}' object"
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
            doc = cls.__doc__
            doc += '\n\n'
            doc += 'Parameters\n'
            doc += '----------\n'
            cls.argument_names = []
            for aname, ainfo in arguments.items():
                ccls = get_cls(aname, ainfo, cls)
                th = ccls._state_type
                th = th.__name__ if hasattr(th, '__name__') else str(th)
                doc += f'    {ccls.__name__} : {th}\n'
                doc += f'        {ccls.__doc__}\n'
                #pylint: disable=no-member
                cls.argument_names.append(ccls.__name__)
                setattr(cls, ccls.__name__, ccls)
            cls.__doc__ = doc
        object_type = info.get('object-type')
        if object_type:
            cls.child_object_type = \
                    get_cls('child-object-type', object_type, cls)
    except Exception:
        print (f"Unable to construct class for '{name}' of "
                 f"'{parent.scheme_name if parent else None}'")
        raise
    return cls

def _gethash(obj_info):
    dhash = hashlib.sha256()
    dhash.update(pickle.dumps(obj_info))
    return dhash.hexdigest()

def get_root(flproxy) -> Group:
    """
    Get the root settings object.

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
        from ansys.fluent.solver import settings
        if settings.SHASH != _gethash(obj_info):
            LOG.warning("Mismatch between generated file and server object "
                        "info. Dynamically created settings classes will "
                        "be used.")
            raise RuntimeError("Mismatch in hash values")
        cls = settings.root
    except Exception:
        cls = get_cls('', obj_info)
    #pylint: disable=no-member
    cls.set_flproxy(flproxy)
    return cls()
