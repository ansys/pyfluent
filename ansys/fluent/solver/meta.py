from ansys.fluent.core.core import (
    convert_path_command_pair_to_grpc_path,
    PyMenu
)


class PyMenuMeta(type):

    def __create_execute_command(path, command):
        @classmethod
        def wrapper(cls, *args, **kwargs):
            return PyMenu.execute(
                convert_path_command_pair_to_grpc_path(path, command), *args, **kwargs)
        return wrapper

    def __new__(cls, name, bases, attrs):
        if 'doc_by_method' in attrs:
            for k, v in attrs['doc_by_method'].items():
                attrs[k] = PyMenuMeta.__create_execute_command(attrs['__qualname__'].split('.'), k)
                attrs[k].__func__.__doc__ = v # not working
        return super(PyMenuMeta, cls).__new__(
            cls, name, bases, attrs)