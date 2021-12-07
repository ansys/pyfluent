from ansys.fluent.core.core import (
    convert_path_to_grpc_path,
    PyMenu
)


class PyMenuMeta(type):

    # pyfluent.results.graphics.objects.contour['contour-1'].color_map.size.get_state()
    @classmethod
    def __create_get_state(cls):
        @classmethod
        def wrapper(cls_):
            return PyMenu.get_state(convert_path_to_grpc_path(cls_.path))
        return wrapper

    # pyfluent.results.graphics.objects.contour['contour-1'].color_map.size.set_state(80.0)
    @classmethod
    def __create_set_state(cls):
        @classmethod
        def wrapper(cls_, value):
            PyMenu.set_state(convert_path_to_grpc_path(cls_.path), value)
        return wrapper

    def __new__(cls, name, bases, attrs):
        attrs['path'] = { x : None for x in attrs['__qualname__'].split('.') }
        if 'is_extended_tui' in attrs:
            attrs['get_state'] = cls.__create_get_state()
            attrs['set_state'] = cls.__create_set_state()
        return super(PyMenuMeta, cls).__new__(
            cls, name, bases, attrs)


class PyNamedObjectMeta(type):

    @classmethod
    def __create_init(cls, cls_name, attrs):
        def update_path(attr, cls_name, name):
            if isinstance(attr, PyMenuMeta) or isinstance(attr, PyNamedObjectMeta):
                getattr(attr, 'path')[cls_name] = name
                for _, v in attr.__dict__.items():
                    update_path(v, cls_name, name)
        def wrapper(self, name):
            getattr(self, 'path')[cls_name] = name
            for _, v in attrs.items():
                update_path(v, cls_name, name)
        return wrapper

    # pyfluent.results.graphics.objects.contour['contour-1']
    def __getitem__(cls, name):
        return cls(name)

    # pyfluent.results.graphics.objects.contour['contour-1'] = {...}
    def __setitem__(cls, name, value):
        PyMenu.set_state(convert_path_to_grpc_path(cls(name).path), value)

    # del pyfluent.results.graphics.objects.contour['contour-1']
    def __delitem__(cls, name):
        PyMenu.del_item(convert_path_to_grpc_path(cls(name).path))

    # pyfluent.results.graphics.objects.contour['contour-1'].field = 'velocity-magnitude'
    @classmethod
    def __create_setattr(cls):
        def wrapper(self, name, value):
            child_path = dict(self.path)
            child_path[name] = None
            PyMenu.set_state(convert_path_to_grpc_path(child_path), value)
        return wrapper

    # pyfluent.results.graphics.objects.contour['contour-1']()
    @classmethod
    def __create_get_state(cls):
        def wrapper(self):
            return PyMenu.get_state(convert_path_to_grpc_path(self.path))
        return wrapper

    # pyfluent.results.graphics.objects.contour['contour-1'].rename('my-contour')
    @classmethod
    def __create_rename(cls):
        def wrapper(self, new_name):
            PyMenu.rename(convert_path_to_grpc_path(self.path), new_name)
        return wrapper

    def __new__(cls, name, bases, attrs):
        attrs['path'] = { x : None for x in attrs['__qualname__'].split('.') }
        attrs['__init__'] = cls.__create_init(name, attrs)
        attrs['__call__'] = cls.__create_get_state()
        attrs['__setattr__'] = cls.__create_setattr()
        attrs['rename'] = cls.__create_rename()
        return super(PyNamedObjectMeta, cls).__new__(
            cls, name, bases, attrs)
