from ansys.fluent.services.datamodel_tui import (
    PyMenu,
    convert_path_to_grpc_path
    )


class PyMenuMeta(type):
    @classmethod
    def __create_init(cls):
        def wrapper(self, path, service):
            self.path = path
            self.service = service
            for name, cls in self.__class__.__dict__.items():
                if cls.__class__.__name__ == "PyMenuMeta":
                    setattr(
                        self, name, cls(self.path + [(name, None)], service)
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


class PyNamedObjectMeta(type):
    @classmethod
    def __create_init(cls):
        def wrapper(self, path, name, service):
            self.path = path[:-1] + [(path[-1][0], name)]
            self.service = service
            for name, cls in self.__class__.__dict__.items():
                if cls.__class__.__name__ == "PyMenuMeta":
                    setattr(
                        self, name, cls(self.path + [(name, None)], service)
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
            PyMenu(self.service).del_item(convert_path_to_grpc_path(o.path))

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
        attrs["path"] = {x: None for x in attrs["__qualname__"].split(".")}
        attrs["__init__"] = cls.__create_init()
        attrs["__getitem__"] = cls.__create_getitem()
        attrs["__setitem__"] = cls.__create_setitem()
        attrs["__delitem__"] = cls.__create_delitem()
        attrs["__call__"] = cls.__create_get_state()
        attrs["rename"] = cls.__create_rename()
        return super(PyNamedObjectMeta, cls).__new__(cls, name, bases, attrs)
