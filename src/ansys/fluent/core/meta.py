"""Metaclasses used in various explicit classes in PyFluent."""
from abc import ABCMeta
from collections.abc import MutableMapping
import inspect
from pprint import pformat

# pylint: disable=unused-private-member
# pylint: disable=bad-mcs-classmethod-argument


class Attribute:
    VALID_NAMES = ["range", "allowed_values"]

    def __init__(self, function):
        self.function = function

    def __set_name__(self, obj, name):
        if name not in self.VALID_NAMES:
            raise ValueError(
                f"Attribute {name} is not allowed."
                f"Expected values are {self.VALID_NAMES}"
            )
        if not hasattr(obj, "attributes"):
            obj.attributes = set()
        obj.attributes.add(name)

    def __set__(self, obj, value):
        raise AttributeError("Attributes are read only.")

    def __get__(self, obj, objtype=None):
        return self.function(obj)


class Command:

    def __init__(self, method):
        self.arguments_attrs = {}
        args = inspect.signature(method).parameters
        for arg_name in args:
            self.arguments_attrs[arg_name] = {}
        self.command = type(
            'command', (), {
                '__call__': lambda _self, **kwargs: method(self.obj, **kwargs),
                "argument": lambda _self, argument_name, attr_name: self.arguments_attrs[argument_name][attr_name](self.obj),
                "arguments": lambda _self: list(self.arguments_attrs.keys())
            }
        )

    def __set_name__(self, obj, name):
        self.obj = obj
        if not hasattr(obj, "commands"):
            obj.commands = {}
        obj.commands[name] = {}

    def __get__(self, obj, obj_type=None):
        return self.command()


def CommandArgs(command_object, argument_name):
    def wrapper(attribute):
        if argument_name in command_object.arguments_attrs:
            command_object.arguments_attrs[argument_name].update({attribute.__name__: attribute})
        else:
            command_object.arguments_attrs[argument_name] = {attribute.__name__: attribute}
        return attribute

    return wrapper


class PyLocalBaseMeta(type):
    @classmethod
    def __create_get_parent_by_type(cls):
        def wrapper(self, obj_type, obj=None):
            obj = self if obj is None else obj
            parent = None
            if getattr(obj, "_parent", None):
                if isinstance(obj._parent, obj_type):
                    return obj._parent
                parent = self._get_parent_by_type(obj_type, obj._parent)
            return parent

        return wrapper

    @classmethod
    def __create_get_top_most_parent(cls):
        def wrapper(self, obj=None):
            obj = self if obj is None else obj
            parent = obj
            if getattr(obj, "_parent", None):
                parent = self._get_top_most_parent(obj._parent)
            return parent

        return wrapper

    def __new__(cls, name, bases, attrs):
        attrs["_get_parent_by_type"] = cls.__create_get_parent_by_type()
        attrs["_get_top_most_parent"] = cls.__create_get_top_most_parent()
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
                            raise ValueError(
                                f"Value {value}, is not within valid range"
                                f" {self.range}."
                            )
                    elif attr == "allowed_values":
                        if isinstance(value, list):
                            if not all(
                                v is None or v in self.allowed_values for v in value
                            ):
                                raise ValueError(
                                    f"Not all values in {value}, are in the "
                                    "list of allowed values "
                                    f"{self.allowed_values}."
                                )
                        elif value is not None and value not in self.allowed_values:
                            raise ValueError(
                                f"Value {value}, is not in the list of "
                                f"allowed values {self.allowed_values}."
                            )

            return value

        return wrapper

    @classmethod
    def __create_init(cls):
        def wrapper(self, parent, api_helper):
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
            if reset_on_change:
                for obj in reset_on_change:
                    obj._register_on_change_cb(lambda: setattr(self, "_value", None))

        return wrapper

    @classmethod
    def __create_get_state(cls, show_attributes=False):
        def wrapper(self):
            try:
                return self.value
            except AttributeError:
                return None

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


class PyLocalObjectMeta(PyLocalBaseMeta):
    """Metaclass for local object classes."""

    @classmethod
    def __create_init(cls):
        def wrapper(self, parent, api_helper):
            self._parent = parent
            self._api_helper = api_helper(self)
            self.type = "object"

            def update(clss):
                for name, cls in clss.__dict__.items():
                    if cls.__class__.__name__ in (
                        "PyLocalPropertyMeta",
                        "PyLocalObjectMeta",
                    ):
                        setattr(
                            self,
                            name,
                            cls(self, api_helper),
                        )
                    if cls.__class__.__name__ == "PyLocalNamedObjectMeta":
                        setattr(
                            self,
                            cls.PLURAL,
                            PyLocalContainer(self, cls, api_helper),
                        )
                for base_class in clss.__bases__:
                    update(base_class)

            update(self.__class__)

        return wrapper

    @classmethod
    def __create_getattribute(cls):
        def wrapper(self, name):
            if name == "_availability":
                return object.__getattribute__(self, "_availability")
            availability = (
                getattr(self, "_availability")(name)
                if hasattr(self, "_availability")
                else True
            )
            if availability:
                return object.__getattribute__(self, name)
            else:
                return None

        return wrapper

    @classmethod
    def __create_updateitem(cls):
        def wrapper(self, value):
            for name, val in value.items():
                obj = getattr(self, name)
                if obj.__class__.__class__.__name__ == "PyLocalPropertyMeta":
                    obj.set_state(val)
                else:
                    obj.update(val)

        wrapper.__doc__ = "Update object."
        return wrapper

    @classmethod
    def __create_get_state(cls):
        def wrapper(self, show_attributes=False):
            state = {}

            def update_state(clss):
                for name, cls in clss.__dict__.items():

                    availability = (
                        getattr(self, "_availability")(name)
                        if hasattr(self, "_availability")
                        else True
                    )
                    if availability:
                        o = getattr(self, name)
                        if cls.__class__.__name__ == "PyLocalObjectMeta":
                            state[name] = o(show_attributes)

                        if cls.__class__.__name__ == "PyLocalPropertyMeta":
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
        attrs["__call__"] = cls.__create_get_state()
        attrs["__setattr__"] = cls.__create_setattr()
        attrs["__repr__"] = cls.__create_repr()
        attrs["update"] = cls.__create_updateitem()
        return super(PyLocalObjectMeta, cls).__new__(cls, name, bases, attrs)


class PyLocalNamedObjectMeta(PyLocalObjectMeta):
    """Metaclass for local named object classes."""

    @classmethod
    def __create_init(cls):
        def wrapper(self, name, parent, api_helper):
            self._name = name
            self._api_helper = api_helper(self)
            self._parent = parent
            self.type = "object"

            def update(clss):
                for name, cls in clss.__dict__.items():
                    if cls.__class__.__name__ in (
                        "PyLocalPropertyMeta",
                        "PyLocalObjectMeta",
                    ):
                        setattr(
                            self,
                            name,
                            cls(self, api_helper),
                        )
                    if cls.__class__.__name__ == "PyLocalNamedObjectMeta":
                        setattr(
                            self,
                            cls.PLURAL,
                            PyLocalContainer(self, cls, api_helper),
                        )
                for base_class in clss.__bases__:
                    update(base_class)

            update(self.__class__)

        return wrapper

    def __new__(cls, name, bases, attrs):
        attrs["__init__"] = cls.__create_init()
        return super(PyLocalNamedObjectMeta, cls).__new__(cls, name, bases, attrs)


class PyLocalNamedObjectMetaAbstract(ABCMeta, PyLocalNamedObjectMeta):
    pass


class PyLocalContainer(MutableMapping):
    """Local container for named objects."""

    def __init__(self, parent, object_class, api_helper):
        self._parent = parent
        self.__object_class = object_class
        self.__collection: dict = {}
        self.__api_helper = api_helper
        self.type = "named-object"

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
        return o

    def __setitem__(self, name, value):
        o = self[name]
        o.update(value)

    def __delitem__(self, name):
        del self.__collection[name]
