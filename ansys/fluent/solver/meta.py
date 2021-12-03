from ansys.fluent.core.core import (
    convertPathCommandPairToGrpcPath,
    PyMenu
)


class PyMenuMeta(type):
    def _createExecuteCommand(path, command):
        @classmethod
        def wrapper(cls, *args, **kwargs):
            return PyMenu.execute(convertPathCommandPairToGrpcPath(path, command), *args, **kwargs)
        return wrapper
    def __new__(cls, name, bases, attrs):
        if 'doc_by_method' in attrs:
            for k, v in attrs['doc_by_method'].items():
                attrs[k] = PyMenuMeta._createExecuteCommand(attrs['__qualname__'].split('.'), k)
                attrs[k].__func__.__doc__ = v # not working
        return super(PyMenuMeta, cls).__new__(
            cls, name, bases, attrs)