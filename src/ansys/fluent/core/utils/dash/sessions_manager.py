from ansys.fluent.core.session import Session
from local_property_editor import (
    MonitorWindow,
    PlotWindowCollection,
    GraphicsWindowCollection,
)
import threading

# from ansys.fluent.core.utils.dash.settings_widgets import SettingsWidget


class SessionsManager:
    _sessions_state = {}

    def __init__(self, app, connection_id, session_id):
        cmplete_session_id = f"session-{session_id}-{connection_id}"

        session_state = SessionsManager._sessions_state.get(cmplete_session_id)

        if not session_state:
            SessionsManager._sessions_state[cmplete_session_id] = self.__dict__
            MonitorWindow(app, connection_id, session_id, SessionsManager)
            PlotWindowCollection(app, connection_id, session_id, SessionsManager)
            GraphicsWindowCollection(app, connection_id, session_id, SessionsManager)
            self._events_info_map = {}
            self._lock = threading.Lock()

        else:
            self.__dict__ = session_state

    def add_session(self, session_token):
        # self.session = Session.create_from_server_info_file(file_path, False)
        self.session = Session("10.18.44.30", session_token, cleanup_on_exit=False)
        self.session.monitors_manager.start()

        self.static_info = self.session.get_settings_service().get_static_info()
        self.settings_root = self.session.get_settings_root()
        self.register_events()

    def get_event_info(self, event_name):
        with self._lock:
            return self._events_info_map.get(event_name)

    def register_events(self):
        def store_info(event_name, event_info):
            with self._lock:
                self._events_info_map[event_name] = event_info

        cb_itr_id = self.session.events_manager.register_callback(
            "IterationEndedEvent",
            lambda session_id, event_info: store_info(
                "IterationEndedEvent", event_info
            ),
        )
        cb_time_step_id = self.session.events_manager.register_callback(
            "TimestepEndedEvent",
            lambda session_id, event_info: store_info("TimestepEndedEvent", event_info),
        )
