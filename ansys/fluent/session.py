import atexit
import itertools
import threading
from typing import Callable, List, Optional

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
from ansys.fluent.services.field_data import FieldData, FieldDataService
from ansys.fluent.services.health_check import HealthCheckService
from ansys.fluent.services.scheme_eval import SchemeEval, SchemeEvalService
from ansys.fluent.services.settings import SettingsService
from ansys.fluent.services.transcript import TranscriptService
from ansys.fluent.solver.flobject import get_root as settings_get_root
from ansys.fluent.services.events import EventsService
from ansys.fluent.solver.events_manager import EventsManager


def parse_server_info_file(filename: str):
    with open(filename, "rb") as f:
        lines = f.readlines()
    return lines[0].strip(), lines[1].strip()

class MonitorThread(threading.Thread):
    """
    Deamon thread which will ensure cleanup of session objects, shutdown
    of non-deamon threads etc.

    Attributes
    ----------
    cbs : List[Callable]
        Cleanup/shutdown functions
    """

    def __init__(self):
        super().__init__(daemon=True)
        self.cbs: List[Callable] = []

    def run(self):
        main_thread = threading.main_thread()
        main_thread.join()
        for cb in self.cbs:
            cb()


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

    _on_exit_cbs: List[Callable] = []
    _id_iter = itertools.count()
    _monitor_thread: Optional[MonitorThread] = None

    def __init__(self, server_info_filepath):
        address, password = parse_server_info_file(server_info_filepath)
        self.__channel = grpc.insecure_channel(address)
        self.__metadata = [("password", password)]
        self.__id = f"session-{next(Session._id_iter)}"
        self._settings_root = None

        if not Session._monitor_thread:
            Session._monitor_thread = MonitorThread()
            Session._monitor_thread.start()

        self.__transcript_service = TranscriptService(
            self.__channel, self.__metadata
        )
        self.__transcript_thread: threading.Thread = None

        self.__events_service = EventsService(self.__channel, self.__metadata)
        self.events_manager = EventsManager(self.__id, self.__events_service)

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
        self.part_management = PyMenu_SE(self.__datamodel_service_se,
                                         "PartManagement")

        self.__health_check_service = HealthCheckService(
            self.__channel, self.__metadata
        )

        self.__scheme_eval_service = SchemeEvalService(
            self.__channel, self.__metadata
        )
        self.scheme_eval = SchemeEval(self.__scheme_eval_service)

        Session._monitor_thread.cbs.append(self.exit)

    @property
    def id(self):
        return self.__id

    def get_settings_service(self):
        """Return an instance of SettingsService object"""
        return SettingsService(self.__channel, self.__metadata)

    def get_settings_root(self):
        """Return root settings object"""
        if self._settings_root is None:
            LOG.warning("The settings API is currently experimental.")
            self._settings_root = settings_get_root(
                    flproxy = self.get_settings_service()
                    )
        return self._settings_root

    def _process_transcript(self):
        responses = self.__transcript_service.begin_streaming()
        transcript = ""
        while True:
            try:
                response = next(responses)
                transcript += response.transcript
                if transcript[-1] == "\n":
                    print(transcript[0:-1])
                    transcript = ""
            except StopIteration:
                break

    def start_transcript(self):
        """Start streaming of Fluent transcript"""
        self.__transcript_thread = threading.Thread(
            target=Session._process_transcript, args=(self,)
        )

        self.__transcript_thread.start()

    def stop_transcript(self):
        """Stop streaming of Fluent transcript"""
        self.__transcript_service.end_streaming()

    def check_health(self):
        """Check health of Fluent connection"""
        if self.__channel:
            return self.__health_check_service.check_health()
        else:
            return HealthCheckService.Status.NOT_SERVING.name

    def exit(self):
        """Close the Fluent connection and exit Fluent."""
        if self.__channel:
            self.scheme_eval.exec(("(exit-server)",))
            self.__transcript_service.end_streaming()
            self.events_manager.stop()
            self.__channel.close()
            self.__channel = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.exit()

    @classmethod
    def register_on_exit(cls, callback):
        cls._on_exit_cbs.append(callback)

    @staticmethod
    def exit_all():
        for cb in Session._on_exit_cbs:
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
