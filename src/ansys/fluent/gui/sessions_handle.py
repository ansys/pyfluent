import threading

from dash import dcc, html
from objects_handle import LocalObjectsHandle
from state_manager import StateManager

from ansys.fluent.core.session import Session


class SessionsHandle:
    _sessions_state = {}

    def __init__(self, user_id, session_id):

        complete_session_id = f"{user_id}:{session_id}"

        session_state = SessionsHandle._sessions_state.get(complete_session_id)

        if not session_state:
            SessionsHandle._sessions_state[complete_session_id] = self.__dict__
            self.session = None
            self._complete_session_id = complete_session_id
            self._events_info_map = {}
            self._lock = threading.Lock()
            self._user_id = user_id
            self._session_id = session_id
            self._state_manager = StateManager(user_id, session_id, SessionsHandle)
        else:
            self.__dict__ = session_state

    @classmethod
    def get_sessions(cls, user_id):
        return map(
            lambda x: x.split(":")[1],
            [
                session_name
                for session_name, session_state in cls._sessions_state.items()
                if session_name.startswith(user_id)
            ],
        )

    def add_session(self, session_token, user_name_to_session_map):
        session_token = session_token.strip()
        if len(session_token.split(":")) == 1:
            self.session = Session(
                "localhost", int(session_token), cleanup_on_exit=False
            )
            self.session.monitors_manager.start()
            # self.static_info = self.session.solver._settings_service.get_static_info()
            self.settings_root = self.session.solver.root
            self.static_info = self.settings_root._static_info
            self.register_events()
            LocalObjectsHandle(SessionsHandle).add_outline_mesh(
                self._user_id, self._session_id
            )
        else:
            user_id, uuid_id = session_token.split(":")
            id_uuid_list = user_name_to_session_map[user_id]
            session_id = list(filter(lambda x: x[1] == session_token, id_uuid_list))[0][
                0
            ]
            self._state_manager.copy_from(user_id, session_id)

    def get_event_info(self, event_name):
        with self._lock:
            return self._events_info_map.get(event_name)

    def register_events(self):
        def store_info(event_name, event_info):
            with self._lock:
                self._events_info_map[event_name] = event_info
                if event_name == "CalculationsEndedEvent":
                    if "ProgressEvent" in self._events_info_map:
                        del self._events_info_map["ProgressEvent"]
                    if "CalculationsStartedEvent" in self._events_info_map:
                        del self._events_info_map["CalculationsStartedEvent"]
                if event_name == "InitializedEvent":
                    itrEndedEvent = self._events_info_map.get("IterationEndedEvent")
                    if itrEndedEvent:
                        itrEndedEvent.index = 0

        self.session.events_manager.register_callback(
            "IterationEndedEvent",
            lambda session_id, event_info: store_info(
                "IterationEndedEvent", event_info
            ),
        )
        self.session.events_manager.register_callback(
            "CalculationsStartedEvent",
            lambda session_id, event_info: store_info(
                "CalculationsStartedEvent", event_info
            ),
        )
        self.session.events_manager.register_callback(
            "TimestepEndedEvent",
            lambda session_id, event_info: store_info("TimestepEndedEvent", event_info),
        )

        self.session.events_manager.register_callback(
            "ProgressEvent",
            lambda session_id, event_info: store_info("ProgressEvent", event_info),
        )

        self.session.events_manager.register_callback(
            "CalculationsEndedEvent",
            lambda session_id, event_info: store_info(
                "CalculationsEndedEvent", event_info
            ),
        )

        self.session.events_manager.register_callback(
            "InitializedEvent",
            lambda session_id, event_info: store_info("InitializedEvent", event_info),
        )
