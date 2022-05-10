from ansys.fluent.core.session import Session
from local_property_editor import (
    MonitorWindow,
    PlotWindowCollection,
    GraphicsWindowCollection,
    PostWindowCollection,
)
import threading
from ansys.fluent.post.pyvista import Graphics

# from ansys.fluent.core.utils.dash.settings_widgets import SettingsWidget
from local_property_editor import LocalPropertyEditor


class SessionsManager:
    _sessions_state = {}

    def __init__(self, app, connection_id, session_id):

        complete_session_id = f"{connection_id}-{session_id}"

        session_state = SessionsManager._sessions_state.get(complete_session_id)

        if not session_state:
            SessionsManager._sessions_state[complete_session_id] = self.__dict__
            MonitorWindow(app, connection_id, session_id, SessionsManager)
            PlotWindowCollection(app, connection_id, session_id, SessionsManager)
            GraphicsWindowCollection(app, connection_id, session_id, SessionsManager)
            self._app = app
            self._complete_session_id = complete_session_id
            self._events_info_map = {}
            self._lock = threading.Lock()
            self._connection_id = connection_id
            self._session_id = session_id
        else:
            self.__dict__ = session_state

    def add_session(self, session_token, user_name_to_session_map):
        session_token = session_token.strip()
        if len(session_token.split(":")) == 1:

            self.session = Session(
                "10.18.44.30", int(session_token), cleanup_on_exit=False
            )
            self.session.monitors_manager.start()
            outline_mesh = LocalPropertyEditor(self._app, SessionsManager)._get_object(
                self._connection_id, self._session_id, "Mesh", "outline"
            )
            outline_mesh.update(Graphics(self.session).add_outline_mesh()())
            outline_mesh.show_edges = True
            self.static_info = self.session.get_settings_service().get_static_info()
            self.settings_root = self.session.get_settings_root()
            self.register_events()
            PostWindowCollection._show_outline = True
        else:
            user_id, uuid_id = session_token.split(":")
            id_uuid_list = user_name_to_session_map[user_id]
            session_id = list(filter(lambda x: x[1] == session_token, id_uuid_list))[0][
                0
            ]
            PlotWindowCollection(
                self._app, self._connection_id, self._session_id, SessionsManager
            ).copy_from(user_id, session_id)
            GraphicsWindowCollection(
                self._app, self._connection_id, self._session_id, SessionsManager
            ).copy_from(user_id, session_id)

            SessionsManager._sessions_state[
                self._complete_session_id
            ] = SessionsManager._sessions_state[
                SessionsManager(self._app, user_id, session_id)._complete_session_id
            ]

    def get_event_info(self, event_name):
        with self._lock:
            return self._events_info_map.get(event_name)

    def register_events(self):
        def store_info(event_name, event_info):
            with self._lock:
                self._events_info_map[event_name] = event_info
                if event_name == "CalculationsEndedEvent":
                    del self._events_info_map["ProgressEvent"]
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
