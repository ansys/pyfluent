import atexit
from threading import Lock, Thread

import grpc
from ansys.fluent.core import LOG

from ansys.fluent.services.datamodel_se import (
    DatamodelService as DatamodelService_SE,
)
from ansys.fluent.services.datamodel_se import PyMenu as PyMenu_SE
from ansys.fluent.services.datamodel_tui import (
    DatamodelService as DatamodelService_TUI,
)
from ansys.fluent.services.datamodel_tui import PyMenu as PyMenu_TUI
from ansys.fluent.services.health_check import HealthCheckService
from ansys.fluent.services.transcript import TranscriptService
from ansys.fluent.services.field_data import FieldDataService, FieldData
from ansys.fluent.services.settings import SettingsService
from ansys.fluent.solver import flobject


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
    setup: flobject.Group
        Instance of flobject.Group object from which setup related
        settings can be accessed or modified.
    solution: flobject.Group
        Instance of flobject.Group object from which solution related
        settings can be accessed or modified.
    results: flobject.Group
        Instance of flobject.Group object from which results related
        settings can be accessed or modified.

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

        self.__datamodel_service_tui = DatamodelService_TUI(
            self.__channel, self.__metadata
        )

        self.__field_data_service = FieldDataService(
            self.__channel, self.__metadata
        )
        self.field_data = FieldData(self.__field_data_service)
        self.tui = Session.Tui(self.__datamodel_service_tui)

        self.__datamodel_service_se = DatamodelService_SE(
            self.__channel, self.__metadata
            )
        self.meshing = PyMenu_SE(self.__datamodel_service_se, "meshing")
        self.workflow = PyMenu_SE(self.__datamodel_service_se, "workflow")

        self.__health_check_service = HealthCheckService(
            self.__channel, self.__metadata
        )

        Session.__all_sessions.append(self)

    def setup_settings_objects(self):
        proxy = SettingsService(self.__channel, self.__metadata)
        r = flobject.get_root(flproxy=proxy)
        for k in r.member_names:
            setattr(self, k, getattr(r, k))
        self.root = r

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
            target=Session.__log_transcript, args=(self,), daemon=True
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
            self.tui.solver.exit()
            self.stop_transcript()
            self.__channel.close()
            self.__channel = None
            Session.__all_sessions.remove(self)

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
        def __init__(self, service):
            self.meshing = Session.MeshingTui(service)
            self.solver = Session.SolverTui(service)

    class TuiMode:
        def __init__(self, service):
            self.service = service
            for mod in self.__class__.application_modules:
                for name, cls in mod.__dict__.items():
                    if cls.__class__.__name__ == "PyMenuMeta":
                        setattr(self, name, cls([(name, None)], service))
                    if cls.__class__.__name__ in "PyNamedObjectMeta":
                        setattr(self, name, cls([(name, None)], None, service))

        @classmethod
        def register_module(cls, mod):
            cls.application_modules.append(mod)
            for name, obj in mod.__dict__.items():
                if callable(obj):
                    setattr(cls, name, obj)

        def __dir__(self):
            return PyMenu_TUI(self.service).get_child_names("")

    class MeshingTui(TuiMode):
        application_modules = []

    class SolverTui(TuiMode):
        application_modules = []


atexit.register(Session.exit_all)
