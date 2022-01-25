from ansys.fluent.core.core import PyMenu, convert_path_to_grpc_path
from pprint import pformat


class Attribute:
    VALID_NAMES = ["range", "allowed_values"]

    def __init__(self, function):
        self.function = function

    def __set_name__(self, obj, name):
        if not name in self.VALID_NAMES:
            raise ValueError(
                f"Attribute {name} is not allowed."\
                f"Expected values are {self.VALID_NAMES}"
            )
        if not hasattr(obj, "attributes"):
            obj.attributes = set()
        obj.attributes.add(name)

    def __set__(self, obj, value):
        raise AttributeError("Attributes are readonly.")

    def __get__(self, obj, type=None):
        return self.function(obj)


class PyMenuMeta(type):
    @classmethod
    def __create_init(cls):
        def wrapper(self, path, service):
            self.path = path
            self.service = service
            for name, cls in self.__class__.__dict__.items():
                if cls.__class__.__name__ == "PyMenuMeta":
                    setattr(
                        self,
                        name,
                        cls(self.path + [(name, None)], service),
                    )
                if cls.__class__.__name__ == "PyNamedObjectMeta":
                    setattr(
                        self,
                        name,
                        cls(self.path + [(name, None)], None, service),
                    )

        return wrapper

    # pyfluent.results.graphics.objects.contour['contour-1'].color_map.size()
    @classmethod
    def __create_get_state(cls):
        def wrapper(self):
            return PyMenu(self.service).get_state(
                convert_path_to_grpc_path(self.path)
            )

        return wrapper

    # pyfluent.results.graphics.objects.contour['contour-1'].color_map.size.set_state(80.0)
    @classmethod
    def __create_set_state(cls):
        def wrapper(self, value):
            PyMenu(self.service).set_state(
                convert_path_to_grpc_path(self.path), value
            )

        return wrapper

    @classmethod
    def __create_dir(cls):
        def wrapper(self):
            return PyMenu(self.service).get_child_names(
                convert_path_to_grpc_path(self.path)
            )

        return wrapper

    def __new__(cls, name, bases, attrs):
        attrs["__init__"] = cls.__create_init()
        attrs["__dir__"] = cls.__create_dir()
        if "is_extended_tui" in attrs:
            attrs["__call__"] = cls.__create_get_state()
            attrs["set_state"] = cls.__create_set_state()
        return super(PyMenuMeta, cls).__new__(cls, name, bases, attrs)


class PyLocaPropertyMeta(type):
    @classmethod
    def __create_validate(cls):
        def wrapper(self, value):
            old_value = self()
            if old_value and type(old_value) != type(value):
                raise TypeError(
                    f"Value {value} should be of type {type(old_value)}"
                )
            attrs = hasattr(self, "attributes") and getattr(
                self, "attributes"
            )
            if attrs:
                for attr in attrs:
                    if attr == "range" and (
                        value < self.range[0] or value > self.range[1]
                    ):
                        raise ValueError(
                            f"Value {value} is not within {self.range}."
                        )
                    if attr == "allowed_values":
                        if isinstance(value, list):
                            if not all(
                                v in self.allowed_values for v in value
                            ):
                                raise ValueError(
                                    f"Values {value} are not within "\
                                    f"{self.allowed_values}."
                                )
                        elif not value in self.allowed_values:
                            raise ValueError(
                                f"Value {value} is not within "\
                                f"{self.allowed_values}."
                            )

            return value

        return wrapper

    @classmethod
    def __create_init(cls):
        def wrapper(self, path, session, parent=None):
            self._path = path
            self.session = session
            self.parent = parent
            self._on_change_cbs = []
            reset_on_change = (
                hasattr(self, "_reset_on_change")
                and getattr(self, "_reset_on_change")()
            )
            if reset_on_change:
                for obj in reset_on_change:
                    obj._register_on_change_cb(
                        lambda: setattr(self, "_value", None)
                    )
            for name, cls in self.__class__.__dict__.items():
                if cls.__class__.__name__ == "PyLocaPropertyMeta":
                    setattr(
                        self,
                        name,
                        cls(self._path + [(name, None)], session, self),
                    )
                if cls.__class__.__name__ == "PyLocalNamedObjectMeta":
                    setattr(
                        self,
                        name,
                        cls(
                            self._path + [(name, None)],
                            None,
                            session,
                            self,
                        ),
                    )

        return wrapper

    @classmethod
    def __create_getattribute(cls):
        def wrapper(self, name):
            if name == "availability":
                return object.__getattribute__(self, "availability")
            availability = (
                getattr(self, "availability")(name)
                if hasattr(self, "availability")
                else True
            )
            if availability:
                return object.__getattribute__(self, name)
            else:
                return None

        return wrapper

    @classmethod
    def __create_get_state(cls):
        def wrapper(self, show_attributes=False):
            state = {}
            for name, cls in self.__class__.__dict__.items():
                if cls.__class__.__name__ == "PyLocaPropertyMeta":
                    availability = (
                        getattr(self, "availability")(name)
                        if hasattr(self, "availability")
                        else True
                    )
                    if availability:
                        o = getattr(self, name)
                        state[name] = o(show_attributes)
                        attrs = (
                            show_attributes
                            and hasattr(o, "attributes")
                            and getattr(o, "attributes")
                        )
                        if attrs:
                            for attr in attrs:
                                state[name + "." + attr] = getattr(
                                    o, attr
                                )

            if len(state) > 0:
                return state
            else:
                try:
                    return self.value
                except:
                    return None

        return wrapper

    @classmethod
    def __create_set_state(cls):
        def wrapper(self, value):
            if isinstance(value, dict):
                for k, v in value.items():
                    setattr(self, k, v)
            else:
                self.value = self._validate(value)
            for on_change_cb in self._on_change_cbs:
                on_change_cb()

        return wrapper

    @classmethod
    def __create_setattr(cls):
        def wrapper(self, name, value):
            attr = hasattr(self, name) and getattr(self, name)
            if (
                attr
                and attr.__class__.__class__.__name__
                == "PyLocaPropertyMeta"
            ):
                attr.set_state(value)
            else:
                object.__setattr__(self, name, value)

        return wrapper

    @classmethod
    def __create_register_on_change(cls):
        def wrapper(self, on_change_cb):
            self._on_change_cbs.append(on_change_cb)

        return wrapper

    @classmethod
    def __create_repr(cls):
        def wrapper(self):
            data = self(True)
            if isinstance(data, dict):
                return pformat(data, depth=1, indent=2)
            else:
                return f"{data}"

        return wrapper

    def __new__(cls, name, bases, attrs):
        attrs["__init__"] = cls.__create_init()
        attrs["__call__"] = cls.__create_get_state()
        attrs["__getattribute__"] = cls.__create_getattribute()
        attrs["__setattr__"] = cls.__create_setattr()
        attrs["__repr__"] = cls.__create_repr()
        attrs["_validate"] = cls.__create_validate()
        attrs[
            "_register_on_change_cb"
        ] = cls.__create_register_on_change()
        attrs["set_state"] = cls.__create_set_state()
        attrs["parent"] = None
        return super(PyLocaPropertyMeta, cls).__new__(
            cls, name, bases, attrs
        )


class PyLocalNamedObjectMeta(type):
    @classmethod
    def __create_init(cls):
        def wrapper(self, path, name, session, parent=None):
            self._path = path[:-1] + [(path[-1][0], name)]
            self.session = session
            self.parent = parent
            for name, cls in self.__class__.__dict__.items():
                if cls.__class__.__name__ == "PyLocaPropertyMeta":
                    setattr(
                        self,
                        name,
                        cls(self._path + [(name, None)], session, self),
                    )
                if cls.__class__.__name__ == "PyLocalNamedObjectMeta":
                    setattr(
                        self,
                        name,
                        cls(
                            self._path + [(name, None)],
                            None,
                            session,
                            self,
                        ),
                    )

        return wrapper

    # graphics = ansys.fluent.postprocessing.pyvista.Graphics(session1)
    # c1 = graphics.contour['contour-1']
    @classmethod
    def __create_getitem(cls):
        def wrapper(self, name):
            o = self._collection.get(name, None)
            if not o:
                o = self._collection[name] = self.__class__(
                    self._path, name, self.session, self
                )
            return o

        return wrapper

    # graphics = ansys.fluent.postprocessing.pyvista.Graphics(session1)
    # c1 = graphics.contour['contour-1']
    # c2 = graphics.contour['contour-2']
    # c1.update(c2())
    @classmethod
    def __create_updateitem(cls):
        def wrapper(self, value):
            for name, val in value.items():
                getattr(self, name).set_state(val)

        return wrapper

    # graphics = ansys.fluent.postprocessing.pyvista.Graphics(session1)
    # c1 = graphics.contour['contour-1']
    # graphics.contour['contour-2'] = c1
    @classmethod
    def __create_setitem(cls):
        def wrapper(self, name, value):
            o = self[name]
            o.update(value())

        return wrapper

    # graphics = ansys.fluent.postprocessing.pyvista.Graphics(session1)
    # del graphics.contour['contour-1']
    @classmethod
    def __create_delitem(cls):
        def wrapper(self, name):
            del self._collection[name]

        return wrapper

    # graphics = ansys.fluent.postprocessing.pyvista.Graphics(session1)
    # graphics.contour['contour-1']()
    @classmethod
    def __create_get_state(cls):
        def wrapper(self, show_attributes=False):
            state = {}
            for name, cls in self.__class__.__dict__.items():
                if cls.__class__.__name__ == "PyLocaPropertyMeta":
                    availability = (
                        getattr(self, "availability")(name)
                        if hasattr(self, "availability")
                        else True
                    )
                    if availability:
                        o = getattr(self, name)
                        state[name] = o(show_attributes)
                        attrs = (
                            show_attributes
                            and hasattr(o, "attributes")
                            and getattr(o, "attributes")
                        )
                        if attrs:
                            for attr in attrs:
                                state[name + "." + attr] = getattr(
                                    o, attr
                                )
            return state

        return wrapper

    # graphics = ansys.fluent.postprocessing.pyvista.Graphics(session1)
    # graphics.contour['contour-1'].field  =  "temperature"
    @classmethod
    def __create_setattr(cls):
        def wrapper(self, name, value):
            attr = hasattr(self, name) and getattr(self, name)
            if (
                attr
                and attr.__class__.__class__.__name__
                == "PyLocaPropertyMeta"
            ):
                getattr(self, name).set_state(value)
            else:
                object.__setattr__(self, name, value)

        return wrapper

    @classmethod
    def __create_repr(cls):
        def wrapper(self):
            if self._path[-1][-1]:
                return pformat(self(True), depth=1, indent=2)
            else:
                return object.__repr__(self)

        return wrapper

    def __new__(cls, name, bases, attrs):
        attrs["_path"] = {
            x: None for x in attrs["__qualname__"].split(".")
        }
        attrs["__init__"] = cls.__create_init()
        attrs["__getitem__"] = cls.__create_getitem()
        attrs["__setitem__"] = cls.__create_setitem()
        attrs["__delitem__"] = cls.__create_delitem()
        attrs["__call__"] = cls.__create_get_state()
        attrs["__setattr__"] = cls.__create_setattr()
        attrs["__repr__"] = cls.__create_repr()
        attrs["_collection"] = {}
        attrs["update"] = cls.__create_updateitem()
        attrs["parent"] = None
        return super(PyLocalNamedObjectMeta, cls).__new__(
            cls, name, bases, attrs
        )


class PyNamedObjectMeta(type):
    @classmethod
    def __create_init(cls):
        def wrapper(self, path, name, service):
            self.path = path[:-1] + [(path[-1][0], name)]
            self.service = service
            for name, cls in self.__class__.__dict__.items():
                if cls.__class__.__name__ == "PyMenuMeta":
                    setattr(
                        self,
                        name,
                        cls(self.path + [(name, None)], service),
                    )
                if cls.__class__.__name__ == "PyNamedObjectMeta":
                    setattr(
                        self,
                        name,
                        cls(self.path + [(name, None)], None, service),
                    )

        return wrapper

    # pyfluent.results.graphics.objects.contour['contour-1']
    @classmethod
    def __create_getitem(cls):
        def wrapper(self, name):
            return self.__class__(self.path, name, self.service)

        return wrapper

    # pyfluent.results.graphics.objects.contour['contour-1'] = {...}
    @classmethod
    def __create_setitem(cls):
        def wrapper(self, name, value):
            o = self.__class__(self.path, name, self.service)
            PyMenu(self.service).set_state(
                convert_path_to_grpc_path(o.path), value
            )

        return wrapper

    # del pyfluent.results.graphics.objects.contour['contour-1']
    @classmethod
    def __create_delitem(cls):
        def wrapper(self, name):
            o = self.__class__(self.path, name, self.service)
            PyMenu(self.service).del_item(
                convert_path_to_grpc_path(o.path)
            )

        return wrapper

    # pyfluent.results.graphics.objects.contour['contour-1']()
    @classmethod
    def __create_get_state(cls):
        def wrapper(self):
            return PyMenu(self.service).get_state(
                convert_path_to_grpc_path(self.path)
            )

        return wrapper

    # pyfluent.results.graphics.objects.contour['contour-1'].rename('my-contour')
    @classmethod
    def __create_rename(cls):
        def wrapper(self, new_name):
            PyMenu(self.service).rename(
                convert_path_to_grpc_path(self.path), new_name
            )

        return wrapper

    def __new__(cls, name, bases, attrs):
        attrs["path"] = {
            x: None for x in attrs["__qualname__"].split(".")
        }
        attrs["__init__"] = cls.__create_init()
        attrs["__getitem__"] = cls.__create_getitem()
        attrs["__setitem__"] = cls.__create_setitem()
        attrs["__delitem__"] = cls.__create_delitem()
        attrs["__call__"] = cls.__create_get_state()
        attrs["rename"] = cls.__create_rename()
        return super(PyNamedObjectMeta, cls).__new__(
            cls, name, bases, attrs
        )
