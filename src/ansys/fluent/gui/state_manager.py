class StateManager:
    _states = {}

    def __init__(self, user_id, session_id, sessions_handle):
        unique_id = f"{user_id}-{session_id}"
        state = StateManager._states.get(unique_id)
        if not state:
            StateManager._states[unique_id] = self.__dict__
            self._user_id = user_id
            self._session_id = session_id
            self._sessions_handle = sessions_handle
            self._session_handle = sessions_handle(user_id, session_id)
            self._var_state = {}
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
        return any(map(lambda x: x == "busy", self._var_state.values()))

    def set_busy(self, var_name):
        print("set_busy", var_name)
        self._var_state[var_name] = "busy"

    def set_free(self, var_name):
        print("set_free", var_name)
        del self._var_state[var_name]

    def copy_from(self, user_id, session_id):
        from post_windows import GraphicsWindowCollection, PlotWindowCollection

        PlotWindowCollection(
            self._user_id, self._session_id, self._sessions_handle
        ).copy_from(user_id, session_id)

        GraphicsWindowCollection(
            self._user_id, self._session_id, self._sessions_handle
        ).copy_from(user_id, session_id)

        self._sessions_handle._sessions_state[
            self._session_handle._complete_session_id
        ] = self._sessions_handle._sessions_state[
            self._sessions_handle(user_id, session_id)._complete_session_id
        ]
