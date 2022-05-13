


class StateManager:
    _states = {}

    def __init__(self, user_id, session_id, SessionsManager):
        unique_id = f"{user_id}-{session_id}"
        state = StateManager._states.get(unique_id)
        if not state:
            StateManager._states[unique_id] = self.__dict__ 
            self._user_id = user_id
            self._session_id = session_id
            self._sessions_manager = SessionsManager
            self._session_handle = SessionsManager(user_id, session_id)
            self._var_state = {}
        else:
            self.__dict__ = state
            
    def set_var_value(self, var_name, value):       
        self._var_state[var_name]= value   
                    
    def get_var_value(self, var_name):       
        return self._var_state.get(var_name)          
            
    def copy_from(self, user_id, session_id):
        from post_windows import PlotWindowCollection, GraphicsWindowCollection
        PlotWindowCollection(
            self._user_id, self._session_id, self._sessions_manager
        ).copy_from(user_id, session_id)
        
        GraphicsWindowCollection(
            self._user_id, self._session_id, self._sessions_manager
        ).copy_from(user_id, session_id)

        self._sessions_manager._sessions_state[
            self._session_handle._complete_session_id
        ] = self._sessions_manager._sessions_state[
            self._sessions_manager(user_id, session_id)._complete_session_id
        ]    

  