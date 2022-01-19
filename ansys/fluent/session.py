import atexit
import grpc
import threading

from ansys.api.fluent.v0 import datamodel_pb2_grpc as DataModelGrpcModule
from ansys.api.fluent.v0 import transcript_pb2 as TranscriptModule
from ansys.api.fluent.v0 import transcript_pb2_grpc as TranscriptGrpcModule
from ansys.api.fluent.v0 import health_pb2 as HealthModule
from ansys.api.fluent.v0 import health_pb2_grpc as HealthGrpcModule
from ansys.fluent.core.core import DatamodelService, PyMenu

from ansys.fluent.core import LOG

def parse_server_info_file(filename: str):
    with open(filename, "rb") as f:
        lines = f.readlines()
    return lines[0].strip(), lines[1].strip()

class Session:
    """
    Encapsulates a Fluent connection.

    ...

    Attributes
    ----------
    tui : Session.Tui
        Instance of Session.Tui on which Fluent's TUI methods can be
        executed.

    Methods
    -------
    health_check()
        Check health of Fluent connection

    exit()
        Close the Fluent connection and exit Fluent.

    """
    __all_sessions = []

    def __init__(self, server_info_filepath):
        self.__is_exiting = False
        self.lock = threading.Lock()
        address, password = parse_server_info_file(server_info_filepath)
        self.__channel = grpc.insecure_channel(address)

        transcript_stub = TranscriptGrpcModule.TranscriptStub(
            self.__channel)
        request = TranscriptModule.TranscriptRequest()
        responses = transcript_stub.BeginStreaming(
            request, metadata=[('password', password)])
        self.transcript_thread = threading.Thread(
            target=Session.log_transcript, args=(self, responses))
        self.transcript_thread.start()

        datamodel_stub = DataModelGrpcModule.DataModelStub(self.__channel)
        self.service = DatamodelService(datamodel_stub, password)
        self.tui = Session.Tui(self.service)

        health_stub = HealthGrpcModule.HealthStub(self.__channel)
        health_check_request = HealthModule.HealthCheckRequest()
        self.__health_checker = lambda : health_stub.Check(
            health_check_request, metadata=[('password', password)])

        Session.__all_sessions.append(self)

    def log_transcript(self, responses):
        transcript = ''
        while True:
            with self.lock:
                if self.__is_exiting:
                    LOG.debug(transcript)
                    break
            try:
                response = next(responses)
                transcript += response.transcript
                if transcript[-1] == '\n':
                    LOG.debug(transcript[0:-1])
                    transcript = ''
            except StopIteration:
                break

    def health_check(self):
        """Check health of Fluent connection

        """
        response_cls = HealthModule.HealthCheckResponse
        if self.__channel:
            response = self.__health_checker()
            return response_cls.ServingStatus.Name(response.status)
        else:
            return response_cls.ServingStatus.Name(response_cls.NOT_SERVING)

    def exit(self):
        """Close the Fluent connection and exit Fluent.

        """
        with self.lock:
            self.__is_exiting = True
        if self.__channel:
            self.tui.exit()
            if self.transcript_thread:
                self.transcript_thread.join()
            self.__channel.close()
            self.__channel = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.exit()

    @staticmethod
    def exit_all():
        for session in Session.__all_sessions:
            session.exit()

    class Tui:
        __application_modules = []

        def __init__(self, service):
            self.service = service
            for mod in self.__class__.__application_modules:
                for name, cls in mod.__dict__.items():
                    if cls.__class__.__name__ == 'PyMenuMeta':
                        setattr(self, name, cls([(name, None)], service))
                    if cls.__class__.__name__ in 'PyNamedObjectMeta':
                        setattr(self, name, cls([(name, None)], None, service))

        @classmethod
        def register_module(cls, mod):
            cls.__application_modules.append(mod)
            for name, obj in mod.__dict__.items():
                if callable(obj):
                    setattr(cls, name, obj)

        def __dir__(self):
            return PyMenu(self.service).get_child_names('')

atexit.register(Session.exit_all)