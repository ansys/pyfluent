import grpc

from ansys.api.fluent.v0 import datamodel_pb2_grpc as DataModelGrpcModule
from ansys.fluent.core.core import DatamodelService, parse_server_info_file

class Session:
    def __init__(self, address, password):
        self.__channel = grpc.insecure_channel(address)
        datamodel_stub = DataModelGrpcModule.DataModelStub(self.__channel)
        self.service = DatamodelService(datamodel_stub, password)
        self.tui = Session.tui(self.service)

    def stop(self):
        if self.__channel:
            self.__channel.close()

    class tui:
        __application_modules = []
        def __init__(self, service):
            self.__service = service
            for mod in self.__class__.__application_modules:
                for name, cls in mod.__dict__.items():
                    if cls.__class__.__name__ == 'PyMenuMeta':
                        setattr(self, name, cls([(name, None)], service))
                    if cls.__class__.__name__ in 'PyNamedObjectMeta':
                        setattr(self, name, cls([(name, None)], None, service))

        @classmethod
        def register_module(cls, mod):
            cls.__application_modules.append(mod)

def start(server_info_file):
    address, password = parse_server_info_file(server_info_file)
    return Session(address, password)