from ansys.api.fluent.v0 import datamodel_pb2 as DataModelProtoModule
from ansys.fluent.core.core import (
    convertPathCommandPairToGrpcPath,
    convertValueToGValue,
    convertGValueToValue,
    getDataModelService
)


class PyMenuMeta(type):
    def _createExecuteCommand(path, command, doc):
        @classmethod
        def wrapper(cls, *args, **kwargs):
            request = DataModelProtoModule.ExecuteCommandRequest()
            request.path = convertPathCommandPairToGrpcPath(path, command)
            if kwargs:
                for k, v in kwargs.items():
                    convertValueToGValue(v, request.args.fields[k])
            else:
                convertValueToGValue(args, request.args.fields['tui_args'])
            ret = getDataModelService().executeCommand(request)
            return convertGValueToValue(ret.result)
        return wrapper
    def __new__(cls, name, bases, attrs):
        if 'doc_by_method' in attrs:
            for k, v in attrs['doc_by_method'].items():
                attrs[k] = PyMenuMeta._createExecuteCommand(attrs['__qualname__'].split('.'), k, v)
                attrs[k].__func__.__doc__ = v # not working
        return super(PyMenuMeta, cls).__new__(
            cls, name, bases, attrs)