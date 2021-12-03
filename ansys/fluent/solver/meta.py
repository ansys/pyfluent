from ansys.fluent.core.core import (
    convert_path_command_pair_to_grpc_path,
    PyMenu
)


class PyMenuMeta(type):

    @classmethod
    def __create_execute_command(cls, path, command):
        @classmethod
        def wrapper(_, *args, **kwargs):
            return PyMenu.execute(
                convert_path_command_pair_to_grpc_path(path, command), *args, **kwargs)
        return wrapper

    def __new__(cls, name, bases, attrs):
        if 'doc_by_method' in attrs:
            for k, v in attrs['doc_by_method'].items():
                attrs[k] = cls.__create_execute_command(attrs['__qualname__'].split('.'), k)
                attrs[k].__func__.__doc__ = v
        return super(PyMenuMeta, cls).__new__(
            cls, name, bases, attrs)


class PyNamedObjectMeta(type):

    @classmethod
    def __create_init(cls):
        def wrapper(self, name):
            self.name = name
        return wrapper

    def __getitem__(cls, name):
        return cls(name)

    def __new__(cls, name, bases, attrs):
        if 'is_container' in attrs:
            attrs['__init__'] = cls.__create_init()
        return super(PyNamedObjectMeta, cls).__new__(
            cls, name, bases, attrs)
