import atexit
from threading import Lock, Thread

import grpc
from ansys.fluent.core import LOG
from ansys.fluent.services.health_check import HealthCheckService
from ansys.fluent.services.transcript import TranscriptService
from ansys.fluent.services.tui_datamodel import DatamodelService, PyMenu
from ansys.fluent.services.field_data import FieldDataService, FieldData

def parse_server_info_file(filename: str):
    with open(filename, "rb") as f:
        lines = f.readlines()
    return lines[0].strip(), lines[1].strip()


class Session:
    """
    Encapsulates a Fluent connection.

    Attributes
    ----------
    tui : Session.Tui
        Instance of Session.Tui on which Fluent's TUI methods can be
        executed.

    Methods
    -------
    start_transcript()
        Start streaming of Fluent transcript

    stop_transcript()
        Stop streaming of Fluent transcript

    check_health()
        Check health of Fluent connection

    exit()
        Close the Fluent connection and exit Fluent.

    """

    __all_sessions = []
    __on_exit_cbs = []

    def __init__(self, server_info_filepath):
        address, password = parse_server_info_file(server_info_filepath)
        self.__channel = grpc.insecure_channel(address)
        self.__metadata = [("password", password)]

        self.__transcript_service: TranscriptService = None
        self.__transcript_thread: Thread = None
        self.__lock = Lock()
        self.__is_transcript_stopping = False
        self.start_transcript()

        self.__datamodel_service = DatamodelService(
            self.__channel, self.__metadata
            )
        self.tui = Session.Tui(self.__datamodel_service)
        self.__field_data_service = FieldDataService(
            self.__channel, self.__metadata
            )
        self.field_data =  FieldData(self.__field_data_service)
        self.__health_check_service = HealthCheckService(
            self.__channel, self.__metadata
            )
        Session.__all_sessions.append(self)

    def __log_transcript(self):
        responses = self.__transcript_service.begin_streaming()
        transcript = ""
        while True:
            with self.__lock:
                if self.__is_transcript_stopping:
                    LOG.debug(transcript)
                    break
            try:
                response = next(responses)
                transcript += response.transcript
                if transcript[-1] == "\n":
                    LOG.debug(transcript[0:-1])
                    transcript = ""
            except StopIteration:
                break

    def start_transcript(self):
        """Start streaming of Fluent transcript"""
        self.__transcript_service = TranscriptService(
            self.__channel, self.__metadata
            )
        self.__transcript_thread = Thread(
            target=Session.__log_transcript, args=(self,)
            )
        self.__transcript_thread.start()

    def stop_transcript(self):
        """Stop streaming of Fluent transcript"""
        with self.__lock:
            self.__is_transcript_stopping = True
        if self.__transcript_thread:
            self.__transcript_thread.join()

    def check_health(self):
        """Check health of Fluent connection"""
        if self.__channel:
            return self.__health_check_service.check_health()
        else:
            return HealthCheckService.Status.NOT_SERVING.name

    def exit(self):
        """Close the Fluent connection and exit Fluent."""
        if self.__channel:
            self.tui.exit()
            self.stop_transcript()
            self.__channel.close()
            self.__channel = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.exit()

    @classmethod
    def register_on_exit(cls, callback):
        cls.__on_exit_cbs.append(callback)

    @staticmethod
    def exit_all():
        for session in Session.__all_sessions:
            session.exit()
        for cb in Session.__on_exit_cbs:
            cb()

    class Tui:
        __application_modules = []

        def __init__(self, service):
            self.service = service
            for mod in self.__class__.__application_modules:
                for name, cls in mod.__dict__.items():
                    if cls.__class__.__name__ == "PyMenuMeta":
                        setattr(self, name, cls([(name, None)], service))
                    if cls.__class__.__name__ in "PyNamedObjectMeta":
                        setattr(self, name, cls([(name, None)], None, service))

        @classmethod
        def register_module(cls, mod):
            cls.__application_modules.append(mod)
            for name, obj in mod.__dict__.items():
                if callable(obj):
                    setattr(cls, name, obj)

        def __dir__(self):
            return PyMenu(self.service).get_child_names("")


atexit.register(Session.exit_all)
