from ansys.fluent.core.session import Session
from local_property_editor import (
    MonitorWindow,
    PlotWindowCollection,
    GraphicsWindowCollection,
)

# from ansys.fluent.core.utils.dash.settings_widgets import SettingsWidget


class SessionsManager:
    _sessions_state = {}
    _windows_per_session = 1

    def __init__(self, app, connection_id, session_id):
        cmplete_session_id = f"session-{session_id}-{connection_id}"
        # print("SessionsManager", session_id)
        session_state = SessionsManager._sessions_state.get(cmplete_session_id)
        MonitorWindow(app, connection_id, session_id, SessionsManager)
        if not session_state:
            SessionsManager._sessions_state[cmplete_session_id] = self.__dict__
            # SettingsWidget(app, connection_id, session_id, SessionsManager)
            for win_id in range(SessionsManager._windows_per_session):
                PlotWindowCollection(app, connection_id, session_id, SessionsManager)
                GraphicsWindowCollection(
                    app, connection_id, session_id, SessionsManager
                )

        else:
            self.__dict__ = session_state

    def add_session(self, session_token):
        # self.session = Session.create_from_server_info_file(file_path, False)
        self.session = Session("10.18.44.30", session_token, cleanup_on_exit=False)
        self.session.monitors_manager.start()
        self.static_info = self.session.get_settings_service().get_static_info()
        self.settings_root = self.session.get_settings_root()
