from ansys.fluent.core.session import Session
from ansys.fluent.core.utils.dash.post_widgets import (
    GraphicsWidget,
    PlotWidget,
)
from ansys.fluent.core.utils.dash.settings_widgets import SettingsWidget


class SessionsManager:
    _sessions_state = {}
    _windows_per_session = 20

    def __init__(self, app, connection_id, session_id):
        cmplete_session_id = f"session-{session_id}-{connection_id}"
        print("SessionsManager", session_id)
        session_state = SessionsManager._sessions_state.get(cmplete_session_id)
        if not session_state:
            SessionsManager._sessions_state[cmplete_session_id] = self.__dict__
            SettingsWidget(app, connection_id, session_id, SessionsManager)
            for win_id in range(SessionsManager._windows_per_session):
                GraphicsWidget(
                    app, connection_id, session_id, win_id, SessionsManager
                )
                PlotWidget(
                    app, connection_id, session_id, win_id, SessionsManager
                )

        else:
            self.__dict__ = session_state

    def add_session(self, file_path):
        self.session = Session.create_from_server_info_file(file_path, False)
        self.static_info = (
            self.session.get_settings_service().get_static_info()
        )
        self.settings_root = self.session.get_settings_root()
