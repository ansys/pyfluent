"""Metaclasses used in various explicit classes in PyFluent."""

from abc import ABCMeta
from collections.abc import MutableMapping
import inspect
from pprint import pformat
from typing import List

from ansys.fluent.core.exceptions import DisallowedValuesError, InvalidArgument

# pylint: disable=unused-private-member
# pylint: disable=bad-mcs-classmethod-argument


class Attribute:
    """Attributes."""

    VALID_NAMES = [
        "range",
        "allowed_values",
        "display_name_allowed_values",
        "help_str",
        "is_read_only",
        "is_active",
        "on_create",
        "on_change",
        "show_as_separate_object",
        "display_text",
        "layout",
        "previous",
        "next",
        "include",
        "exclude",
        "sort_by",
        "style",
        "icon",
        "show_text",
        "widget",
        "dir_info",
        "extensions",
    ]

    def __init__(self, function):
        self.function = function

    def __set_name__(self, obj, name):
        if name not in self.VALID_NAMES:
            raise DisallowedValuesError("attribute", name, self.VALID_NAMES)
        self.name = name
        if not hasattr(obj, "attributes"):
            obj.attributes = set()
        obj.attributes.add(name)

    def __set__(self, obj, value):
        raise AttributeError("Attributes are read only.")

    def __get__(self, obj, objtype=None):
        return self.function(obj)


class Command:
    """Executes command."""

    def __init__(self, method):
        self.arguments_attrs = {}
        cmd_args = inspect.signature(method).parameters
        for arg_name in cmd_args:
            if arg_name != "self":
                self.arguments_attrs[arg_name] = {}

        def _init(_self, obj):
            _self.obj = obj

        def _execute(_self, *args, **kwargs):
            for arg, attr_data in self.arguments_attrs.items():
                arg_value = None
                if arg in kwargs:
                    arg_value = kwargs[arg]
                else:
                    index = list(self.arguments_attrs.keys()).index(arg)
                    if len(args) > index:
                        arg_value = args[index]
                if arg_value is not None:
                    for attr, attr_value in attr_data.items():
                        if attr == "allowed_values":
                            allowed_values = attr_value(_self.obj)
                            if isinstance(arg_value, list):
                                if not all(
                                    elem in allowed_values for elem in arg_value
                                ):
                                    raise DisallowedValuesError(
                                        arg, arg_value, allowed_values
                                    )
                            else:
                                if arg_value not in allowed_values:
                                    raise DisallowedValuesError(
                                        arg, arg_value, allowed_values
                                    )

                        elif attr == "range":
                            if not isinstance(arg_value, (int, float)):
                                raise RuntimeError(
                                    f"{arg} value {arg_value} is not number."
                                )

                            minimum, maximum = attr_value(_self.obj)
                            if arg_value < minimum or arg_value > maximum:
                                raise DisallowedValuesError(
                                    arg, arg_value, allowed_values
                                )
            return method(_self.obj, *args, **kwargs)

        self.command_cls = type(
            "command",
            (),
            {
                "__init__": _init,
                "__call__": _execute,
                "argument_attribute": lambda _self, argument_name, attr_name: self.arguments_attrs[
                    argument_name
                ][
                    attr_name
                ](
                    _self.obj
                ),
                "arguments": lambda _self: list(self.arguments_attrs.keys()),
            },
        )

    def __set_name__(self, obj, name):
        self.obj = obj
        if not hasattr(obj, "commands"):
            obj.commands = {}
        obj.commands[name] = {}

    def __get__(self, obj, obj_type=None):
        if hasattr(self, "command"):
            return self.command
        else:
            return self.command_cls(obj)


def CommandArgs(command_object, argument_name):
    """Command arguments."""

    def wrapper(attribute):
        if argument_name in command_object.arguments_attrs:
            command_object.arguments_attrs[argument_name].update(
                {attribute.__name__: attribute}
            )
        else:
            raise InvalidArgument(f"{argument_name} not a valid argument.")
        return attribute

    return wrapper


class PyLocalBaseMeta(type):
    """Local base metaclass."""

    @classmethod
    def __create_get_ancestors_by_type(cls):
        def wrapper(self, obj_type, obj=None):
            obj = self if obj is None else obj
            parent = None
            if getattr(obj, "_parent", None):
                if isinstance(obj._parent, obj_type):
                    return obj._parent
                parent = self.get_ancestors_by_type(obj_type, obj._parent)
            return parent

        return wrapper

    @classmethod
    def __create_get_ancestors_by_name(cls):
        def wrapper(self, obj_type, obj=None):
            obj = self if obj is None else obj
            parent = None
            if getattr(obj, "_parent", None):
                if obj._parent.__class__.__name__ == obj_type:
                    return obj._parent
                if getattr(obj._parent, "PLURAL", None) == obj_type:
                    return obj._parent._parent
                parent = self.get_ancestors_by_name(obj_type, obj._parent)
            return parent

        return wrapper

    @classmethod
    def __create_get_root(cls):
        def wrapper(self, obj=None):
            obj = self if obj is None else obj
            parent = obj
            if getattr(obj, "_parent", None):
                parent = self.get_root(obj._parent)
            return parent

        return wrapper

    @classmethod
    def __create_get_session(cls):
        def wrapper(self, obj=None):
            root = self.get_root(obj)
            return root.session

        return wrapper

    @classmethod
    def __create_get_session_handle(cls):
        def wrapper(self, obj=None):
            root = self.get_root(obj)
            return getattr(root, "session_handle", None)

        return wrapper

    @classmethod
    def __create_get_path(cls):
        def wrapper(self):
            if getattr(self, "_parent", None):
                return self._parent.get_path() + "/" + self._name
            return self._name

        return wrapper

    def __new__(cls, name, bases, attrs):
        attrs["get_ancestors_by_type"] = cls.__create_get_ancestors_by_type()
        attrs["get_ancestors_by_name"] = cls.__create_get_ancestors_by_name()
        attrs["get_root"] = cls.__create_get_root()
        attrs["get_session"] = cls.__create_get_session()
        attrs["get_session_handle"] = cls.__create_get_session_handle()
        if "get_path" not in attrs:
            attrs["get_path"] = cls.__create_get_path()
        attrs["root"] = property(lambda self: self.get_root())
        attrs["path"] = property(lambda self: self.get_path())
        attrs["session"] = property(lambda self: self.get_session())
        attrs["session_handle"] = property(lambda self: self.get_session_handle())
        return super(PyLocalBaseMeta, cls).__new__(cls, name, bases, attrs)


class PyLocalPropertyMeta(PyLocalBaseMeta):
    """Metaclass for local property classes."""

    @classmethod
    def __create_validate(cls):
        def wrapper(self, value):
            attrs = getattr(self, "attributes", None)
            if attrs:
                for attr in attrs:
                    if attr == "range":
                        if self.range and (
                            value < self.range[0] or value > self.range[1]
                        ):
                            raise DisallowedValuesError("value", value, self.range)
                    elif attr == "allowed_values":
                        if isinstance(value, list):
                            if not all(
                                v is None or v in self.allowed_values for v in value
                            ):
                                raise DisallowedValuesError(
                                    "value", value, self.allowed_values
                                )
                        elif value is not None and value not in self.allowed_values:
                            raise DisallowedValuesError(
                                "value", value, self.allowed_values
                            )
            return value

        return wrapper

    @classmethod
    def __create_init(cls):
        def wrapper(self, parent, api_helper, name=""):
            """Create the initialization method for 'PyLocalPropertyMeta'."""
            self._name = name
            self._api_helper = api_helper(self)
            self._parent = parent
            self._on_change_cbs = []
            annotations = self.__class__.__dict__.get("__annotations__")
            if isinstance(getattr(self.__class__, "value", None), property):
                value_annotation = annotations.get("_value")
            else:
                value_annotation = annotations.get("value")
            self.type = value_annotation
            reset_on_change = (
                hasattr(self, "_reset_on_change")
                and getattr(self, "_reset_on_change")()
            )

            on_change = getattr(self, "on_change", None)
            if on_change is not None:
                self._register_on_change_cb(on_change)
            if reset_on_change:
                for obj in reset_on_change:

                    def reset():
                        setattr(self, "_value", None)
                        for on_change_cb in self._on_change_cbs:
                            on_change_cb()

                    obj._register_on_change_cb(reset)

        return wrapper

    @classmethod
    def __create_get_state(cls, show_attributes=False):
        def wrapper(self):
            rv = self.value

            if hasattr(self, "allowed_values"):
                allowed_values = self.allowed_values
                if len(allowed_values) > 0 and (
                    rv is None
                    or (not isinstance(rv, list) and rv not in allowed_values)
                ):
                    self.set_state(allowed_values[0])
                    rv = self.value

            return rv

        return wrapper

    @classmethod
    def __create_set_state(cls):
        def wrapper(self, value, validate=True):
            self.value = self._validate(value) if validate else value
            for on_change_cb in self._on_change_cbs:
                on_change_cb()

        return wrapper

    @classmethod
    def __create_register_on_change(cls):
        def wrapper(self, on_change_cb):
            self._on_change_cbs.append(on_change_cb)

        return wrapper

    @classmethod
    def __create_repr(cls):
        def wrapper(self):
            data = self()
            return f"{data}"

        return wrapper

    def __new__(cls, name, bases, attrs):
        attrs["__init__"] = cls.__create_init()
        attrs["__call__"] = cls.__create_get_state()
        attrs["__repr__"] = cls.__create_repr()
        attrs["_validate"] = cls.__create_validate()
        attrs["_register_on_change_cb"] = cls.__create_register_on_change()
        attrs["set_state"] = cls.__create_set_state()
        return super(PyLocalPropertyMeta, cls).__new__(cls, name, bases, attrs)


class PyReferenceObjectMeta(PyLocalBaseMeta):
    """Metaclass for local object classes."""

    @classmethod
    def __create_init(cls):
        def wrapper(self, parent, path, location, session_id, name=""):
            """Create the initialization method for 'PyReferenceObjectMeta'."""
            self._parent = parent
            self.type = "object"
            self.parent = parent
            self._path = path
            self.location = location
            self.session_id = session_id

            def update(clss):
                for name, cls in clss.__dict__.items():
                    if cls.__class__.__name__ in (
                        "PyLocalPropertyMeta",
                        "PyLocalObjectMeta",
                    ):
                        setattr(
                            self,
                            name,
                            cls(self, lambda arg: None, name),
                        )
                    if (
                        cls.__class__.__name__ == "PyLocalNamedObjectMeta"
                        or cls.__class__.__name__ == "PyLocalNamedObjectMetaAbstract"
                    ):
                        setattr(
                            self,
                            cls.PLURAL,
                            PyLocalContainer(self, cls, lambda arg: None, cls.PLURAL),
                        )
                for base_class in clss.__bases__:
                    update(base_class)

            update(self.__class__)

        return wrapper

    @classmethod
    def __create_get_path(cls):
        def wrapper(self):
            return self._path

        return wrapper

    @classmethod
    def __create_reset(cls):
        def wrapper(self, path, location, session_id):
            self._path = path
            self.location = location
            self.session_id = session_id
            if hasattr(self, "_object"):
                delattr(self, "_object")

        return wrapper

    @classmethod
    def __create_getattr(cls):
        def wrapper(self, item):
            if item == "_object":
                top_most_parent = self.get_root(self)

                if self.session_id is None:
                    self.session_id = top_most_parent.session.id
                property_editor_data = top_most_parent.accessor(
                    "AnsysUser", self.session_id
                )
                (
                    obj,
                    cmd_data,
                ) = property_editor_data.get_object_and_command_data_from_properties_info(
                    {"path": self.path, "properties": {}, "type": self.location}
                )
                if obj is not None:
                    self._object = obj
                return obj
            if item == "ref":
                return self._object._object

        return wrapper

    def __new__(cls, name, bases, attrs):
        attrs["__init__"] = attrs.get("__init__", cls.__create_init())
        attrs["__getattr__"] = attrs.get("__getattr__", cls.__create_getattr())
        attrs["reset"] = cls.__create_reset()
        attrs["get_path"] = cls.__create_get_path()
        return super(PyReferenceObjectMeta, cls).__new__(cls, name, bases, attrs)


class PyLocalObjectMeta(PyLocalBaseMeta):
    """Metaclass for local object classes."""

    @classmethod
    def __create_init(cls):
        def wrapper(self, parent, api_helper, name=""):
            """Create the initialization method for 'PyLocalObjectMeta'."""
            self._parent = parent
            self._name = name
            self._api_helper = api_helper(self)
            self._command_names = []
            self.type = "object"

            def update(clss):
                for name, cls in clss.__dict__.items():
                    if cls.__class__.__name__ in ("PyLocalCommandMeta"):
                        self._command_names.append(name)

                    if cls.__class__.__name__ in (
                        "PyLocalPropertyMeta",
                        "PyLocalObjectMeta",
                        "PyLocalCommandMeta",
                    ):
                        setattr(
                            self,
                            name,
                            cls(self, api_helper, name),
                        )
                    if (
                        cls.__class__.__name__ == "PyLocalNamedObjectMeta"
                        or cls.__class__.__name__ == "PyLocalNamedObjectMetaAbstract"
                    ):
                        setattr(
                            self,
                            cls.PLURAL,
                            PyLocalContainer(self, cls, api_helper, cls.PLURAL),
                        )
                    if cls.__class__.__name__ == "PyReferenceObjectMeta":
                        setattr(
                            self,
                            name,
                            cls(self, cls.PATH, cls.LOCATION, cls.SESSION, name),
                        )
                for base_class in clss.__bases__:
                    update(base_class)

            update(self.__class__)

        return wrapper

    @classmethod
    def __create_getattribute(cls):
        def wrapper(self, name):
            obj = object.__getattribute__(self, name)
            return obj

        return wrapper

    @classmethod
    def __create_updateitem(cls):
        def wrapper(self, value):
            properties = value
            sort_by = None
            if hasattr(self, "sort_by"):
                sort_by = self.sort_by
            elif hasattr(self, "include"):
                sort_by = self.include
            if sort_by:
                sorted_properties = {
                    prop: properties[prop] for prop in sort_by if prop in properties
                }
                sorted_properties.update(
                    {k: v for k, v in properties.items() if k not in sort_by}
                )
                properties.clear()
                properties.update(sorted_properties)
            for name, val in properties.items():
                obj = getattr(self, name)
                if obj.__class__.__class__.__name__ == "PyLocalPropertyMeta":
                    obj.set_state(val)
                else:
                    if obj.__class__.__class__.__name__ == "PyReferenceObjectMeta":
                        obj = obj.ref
                    obj.update(val)

        wrapper.__doc__ = "Update object."
        return wrapper

    @classmethod
    def __create_get_state(cls):
        def wrapper(self, show_attributes=False):
            state = {}

            if not getattr(self, "is_active", True):
                return

            def update_state(clss):
                for name, cls in clss.__dict__.items():
                    o = getattr(self, name)
                    if o is None or name.startswith("_") or name.startswith("__"):
                        continue

                    if cls.__class__.__name__ == "PyReferenceObjectMeta":
                        if o.LOCATION == "local":
                            o = o.ref
                        else:
                            continue
                    elif cls.__class__.__name__ == "PyLocalCommandMeta":
                        args = {}
                        for arg in o._args:
                            args[arg] = getattr(o, arg)()
                        state[name] = args
                    if (
                        cls.__class__.__name__ == "PyLocalObjectMeta"
                        or cls.__class__.__name__ == "PyReferenceObjectMeta"
                    ):
                        if getattr(o, "is_active", True):
                            state[name] = o(show_attributes)
                    elif (
                        cls.__class__.__name__ == "PyLocalNamedObjectMeta"
                        or cls.__class__.__name__ == "PyLocalNamedObjectMetaAbstract"
                    ):
                        container = getattr(self, cls.PLURAL)
                        if getattr(container, "is_active", True):
                            state[cls.PLURAL] = {}
                            for child_name in container:
                                o = container[child_name]
                                if getattr(o, "is_active", True):
                                    state[cls.PLURAL][child_name] = o()

                    elif cls.__class__.__name__ == "PyLocalPropertyMeta":
                        if getattr(o, "is_active", True):
                            state[name] = o()
                            attrs = show_attributes and getattr(o, "attributes", None)
                            if attrs:
                                for attr in attrs:
                                    state[name + "." + attr] = getattr(o, attr)

                for base_class in clss.__bases__:
                    update_state(base_class)

            update_state(self.__class__)
            return state

        return wrapper

    @classmethod
    def __create_setattr(cls):
        def wrapper(self, name, value):
            attr = getattr(self, name, None)
            if attr and attr.__class__.__class__.__name__ == "PyLocalPropertyMeta":
                attr.set_state(value)
            else:
                object.__setattr__(self, name, value)

        return wrapper

    @classmethod
    def __create_repr(cls):
        def wrapper(self):
            return pformat(self(True), depth=1, indent=2)

        return wrapper

    def __new__(cls, name, bases, attrs):
        attrs["__getattribute__"] = cls.__create_getattribute()
        attrs["__init__"] = attrs.get("__init__", cls.__create_init())
        if "__call__" not in attrs:
            attrs["__call__"] = cls.__create_get_state()
        attrs["__setattr__"] = cls.__create_setattr()
        # attrs["__repr__"] = cls.__create_repr()
        attrs["update"] = cls.__create_updateitem()
        return super(PyLocalObjectMeta, cls).__new__(cls, name, bases, attrs)


class PyLocalCommandMeta(PyLocalObjectMeta):
    """Local object metaclass."""

    @classmethod
    def __create_init(cls):
        def wrapper(self, parent, api_helper, name=""):
            """Create the initialization method for 'PyLocalObjectMeta'."""
            self._parent = parent
            self._name = name
            self._api_helper = api_helper(self)
            self.type = "object"
            self._args = []
            self._command_names = []
            self._exe_cmd = getattr(self, "_exe_cmd")

            def update(clss):
                for name, cls in clss.__dict__.items():
                    if cls.__class__.__name__ in (
                        "PyLocalCommandArgMeta",
                        "PyLocalPropertyMeta",
                    ):
                        self._args.append(name)
                        setattr(
                            self,
                            name,
                            cls(self, api_helper, name),
                        )
                for base_class in clss.__bases__:
                    update(base_class)

            update(self.__class__)

        return wrapper

    @classmethod
    def __execute_command(cls):
        def wrapper(self, **kwargs):
            for arg_name, arg_value in kwargs.items():
                getattr(self, arg_name).set_state(arg_value)
            cmd_args = {}
            for arg_name in self._args:
                cmd_args[arg_name] = getattr(self, arg_name)()
            rv = self._exe_cmd(**cmd_args)
            return rv

        return wrapper

    def __new__(cls, name, bases, attrs):
        attrs["__init__"] = cls.__create_init()
        attrs["__call__"] = cls.__execute_command()
        return super(PyLocalCommandMeta, cls).__new__(cls, name, bases, attrs)


class PyLocalNamedObjectMeta(PyLocalObjectMeta):
    """Metaclass for local named object classes."""

    @classmethod
    def __create_init(cls):
        def wrapper(self, name, parent, api_helper):
            """Create the initialization method for 'PyLocalNamedObjectMeta'."""
            self._name = name
            self._api_helper = api_helper(self)
            self._parent = parent
            self._command_names = []
            self.type = "object"

            def update(clss):
                for name, cls in clss.__dict__.items():
                    if cls.__class__.__name__ in ("PyLocalCommandMeta"):
                        self._command_names.append(name)

                    if cls.__class__.__name__ in (
                        "PyLocalPropertyMeta",
                        "PyLocalObjectMeta",
                        "PyLocalCommandMeta",
                    ):
                        # delete old property if overridden
                        if getattr(self, name).__class__.__name__ == name:
                            delattr(self, name)
                        setattr(
                            self,
                            name,
                            cls(self, api_helper, name),
                        )
                    elif (
                        cls.__class__.__name__ == "PyLocalNamedObjectMeta"
                        or cls.__class__.__name__ == "PyLocalNamedObjectMetaAbstract"
                    ):
                        setattr(
                            self,
                            cls.PLURAL,
                            PyLocalContainer(self, cls, api_helper, cls.PLURAL),
                        )
                    elif cls.__class__.__name__ == "PyReferenceObjectMeta":
                        setattr(
                            self, name, cls(self, cls.PATH, cls.LOCATION, cls.SESSION)
                        )
                for base_class in clss.__bases__:
                    update(base_class)

            update(self.__class__)

        return wrapper

    def __new__(cls, name, bases, attrs):
        attrs["__init__"] = cls.__create_init()
        return super(PyLocalNamedObjectMeta, cls).__new__(cls, name, bases, attrs)


class PyLocalNamedObjectMetaAbstract(ABCMeta, PyLocalNamedObjectMeta):
    """Local named object abstract metaclass."""

    pass


class PyLocalContainer(MutableMapping):
    """Local container for named objects."""

    def __init__(self, parent, object_class, api_helper, name=""):
        """Initialize the 'PyLocalContainer' object."""
        self._parent = parent
        self._name = name
        self.__object_class = object_class
        self.__collection: dict = {}
        self.__api_helper = api_helper
        self.type = "named-object"
        self._command_names = []

        if hasattr(object_class, "SHOW_AS_SEPARATE_OBJECT"):
            PyLocalContainer.show_as_separate_object = property(
                lambda self: self.__object_class.SHOW_AS_SEPARATE_OBJECT(self)
            )
        if hasattr(object_class, "EXCLUDE"):
            PyLocalContainer.exclude = property(
                lambda self: self.__object_class.EXCLUDE(self)
            )
        if hasattr(object_class, "INCLUDE"):
            PyLocalContainer.include = property(
                lambda self: self.__object_class.INCLUDE(self)
            )
        if hasattr(object_class, "LAYOUT"):
            PyLocalContainer.layout = property(
                lambda self: self.__object_class.LAYOUT(self)
            )
        if hasattr(object_class, "STYLE"):
            PyLocalContainer.style = property(
                lambda self: self.__object_class.STYLE(self)
            )
        if hasattr(object_class, "ICON"):
            PyLocalContainer.icon = property(
                lambda self: self.__object_class.ICON(self)
            )
        if hasattr(object_class, "IS_ACTIVE"):
            PyLocalContainer.is_active = property(
                lambda self: self.__object_class.IS_ACTIVE(self)
            )

        for name, cls in self.__class__.__dict__.items():
            if cls.__class__.__name__ in ("PyLocalCommandMeta"):
                self._command_names.append(name)

            if cls.__class__.__name__ in ("PyLocalCommandMeta"):
                setattr(
                    self,
                    name,
                    cls(self, api_helper, name),
                )

    def update(self, value):
        """Updates this object with the provided dictionary."""
        for name, val in value.items():
            o = self[name]
            o.update(val)

    def get_root(self, obj=None):
        """Returns the top-most parent object."""
        obj = self if obj is None else obj
        parent = obj
        if getattr(obj, "_parent", None):
            parent = self.get_root(obj._parent)
        return parent

    def get_session(self, obj=None):
        """Returns the session object."""
        root = self.get_root(obj)
        return root.session

    def get_path(self):
        """Path to the current object."""
        if getattr(self, "_parent", None):
            return self._parent.get_path() + "/" + self._name
        return self._name

    @property
    def path(self):
        """Path to the current object."""
        return self.get_path()

    @property
    def session(self):
        """Returns the session object."""
        return self.get_session()

    def get_session_handle(self, obj=None):
        """Returns the session-handle object."""
        root = self.get_root(obj)
        return getattr(root, "session_handle", None)

    @property
    def session_handle(self):
        """Returns the session-handle object."""
        return self.get_session_handle()

    def __iter__(self):
        return iter(self.__collection)

    def __len__(self):
        return len(self.__collection)

    def __getitem__(self, name):
        o = self.__collection.get(name, None)
        if not o:
            o = self.__collection[name] = self.__object_class(
                name, self, self.__api_helper
            )
            on_create = getattr(self._PyLocalContainer__object_class, "on_create", None)
            if on_create:
                on_create(self, name)
        return o

    def __setitem__(self, name, value):
        o = self[name]
        o.update(value)

    def __delitem__(self, name):
        del self.__collection[name]
        on_delete = getattr(self._PyLocalContainer__object_class, "on_delete", None)
        if on_delete:
            on_delete(self, name)

    def _get_unique_chid_name(self):
        children = list(self)
        index = 0
        while True:
            unique_name = (
                f"{self._PyLocalContainer__object_class.__name__.lower()}-{index}"
            )
            if unique_name not in children:
                break
            index += 1
        return unique_name

    class Delete(metaclass=PyLocalCommandMeta):
        """Local delete command."""

        def _exe_cmd(self, names):
            for item in names:
                self._parent.__delitem__(item)

        class names(metaclass=PyLocalPropertyMeta):
            """Local names property."""

            value: List[str] = []

            @Attribute
            def allowed_values(self):
                """Get allowed values."""
                return list(self._parent._parent)

    class Create(metaclass=PyLocalCommandMeta):
        """Local create command."""

        def _exe_cmd(self, name=None):
            if name is None:
                name = self._parent._get_unique_chid_name()
            new_object = self._parent.__getitem__(name)
            return new_object._name

        class name(metaclass=PyLocalPropertyMeta):
            """Local name property."""

            value: str = None
