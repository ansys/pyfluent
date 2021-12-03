from ansys.fluent.core.core import (
    convert_path_to_grpc_path,
    PyMenu
)


class PyMenuMeta(type):

    @classmethod
    def __create_execute_command(cls, command):
        @classmethod
        def wrapper(cls_, *args, **kwargs):
            command_path = dict(cls_.path)
            command_path[command] = None
            return PyMenu.execute(convert_path_to_grpc_path(command_path), *args, **kwargs)
        return wrapper

    @classmethod
    def __create_get_state(cls):
        @classmethod
        def wrapper(cls_):
            return PyMenu.get_state(convert_path_to_grpc_path(cls_.path))
        return wrapper

    @classmethod
    def __create_set_state(cls):
        @classmethod
        def wrapper(cls_, value):
            return PyMenu.set_state(convert_path_to_grpc_path(cls_.path), value)
        return wrapper

    def __new__(cls, name, bases, attrs):
        attrs['path'] = { x : None for x in attrs['__qualname__'].split('.') }
        if 'doc_by_method' in attrs:
            for k, v in attrs['doc_by_method'].items():
                attrs[k] = cls.__create_execute_command(k)
                attrs[k].__func__.__doc__ = v
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

    def __getitem__(cls, name):
        return cls(name)

    @classmethod
    def __create_get_state(cls):
        @classmethod
        def wrapper(cls_):
            return PyMenu.get_state(convert_path_to_grpc_path(cls_.path))
        return wrapper

    @classmethod
    def __create_set_state(cls):
        @classmethod
        def wrapper(cls_, value):
            return PyMenu.set_state(convert_path_to_grpc_path(cls_.path), value)
        return wrapper

    def __new__(cls, name, bases, attrs):
        attrs['path'] = { x : None for x in attrs['__qualname__'].split('.') }
        if 'is_container' in attrs:
            attrs['__init__'] = cls.__create_init(name, attrs)
        if 'is_extended_tui' in attrs:
            attrs['get_state'] = cls.__create_get_state()
            attrs['set_state'] = cls.__create_set_state()
        return super(PyNamedObjectMeta, cls).__new__(
            cls, name, bases, attrs)
