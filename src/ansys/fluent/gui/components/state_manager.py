"""Module providing state management."""

import threading


class StateManager:
    _objects = {}

    def __init__(self, user_id, session_id, sessions_handle):
        unique_id = f"{user_id}-{session_id}"
        state = StateManager._objects.get(unique_id)
        if not state:
            StateManager._objects[unique_id] = self.__dict__
            self._user_id = user_id
            self._session_id = session_id
            self._sessions_handle = sessions_handle
            self._session_handle = sessions_handle(user_id, session_id)
            self._busy_components = {}
            self._lock: threading.Lock = threading.Lock()
        else:
            self.__dict__ = state

    class BusyWith:
        def __init__(self, user_id, session_id, sessions_handle, index):
            self._user_id = user_id
            self._session_id = session_id
            self._index = index
            self._sessions_handle = sessions_handle

        def __enter__(self):
            StateManager(
                self._user_id, self._session_id, self._sessions_handle
            ).set_busy(self._index)

        def __exit__(self, exc_type, exc_val, exc_tb):
            StateManager(
                self._user_id, self._session_id, self._sessions_handle
            ).set_free(self._index)

    def is_busy(self):
        """Check if any component is busy."""
        with self._lock:
            return any(map(lambda x: x == "busy", self._busy_components.values()))

    def set_busy(self, var_name):
        """Set component state busy."""
        with self._lock:
            self._busy_components[var_name] = "busy"

    def set_free(self, var_name):
        """Set component state free."""
        with self._lock:
            del self._busy_components[var_name]

    def copy_from(self, user_id, session_id):
        """Copy component state."""
        from post_windows import GraphicsWindowCollection, PlotWindowCollection

        PlotWindowCollection(
            self._user_id, self._session_id, self._sessions_handle
        ).copy_from(user_id, session_id)

        GraphicsWindowCollection(
            self._user_id, self._session_id, self._sessions_handle
        ).copy_from(user_id, session_id)

        self._sessions_handle._sessions_state[
            self._session_handle._unique_id
        ] = self._sessions_handle._sessions_state[
            self._sessions_handle(user_id, session_id)._unique_id
        ]
