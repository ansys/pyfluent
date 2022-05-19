"""Module providing session handle."""

import threading
from typing import List

from ansys.fluent.core.session import Session
from ansys.fluent.gui.components import objects_handle, state_manager


class SessionsHandle:
    """Sessions  handle."""

    _objects = {}

    def __init__(self, user_id, session_id):

        unique_id = f"{user_id}:{session_id}"

        session_state = SessionsHandle._objects.get(unique_id)

        if not session_state:
            SessionsHandle._objects[unique_id] = self.__dict__
            self.session = None
            self._unique_id = unique_id
            self._events_info_map = {}
            self._lock = threading.Lock()
            self._user_id = user_id
            self._session_id = session_id
            self._state_manager = state_manager.StateManager(
                user_id, session_id, SessionsHandle
            )
        else:
            self.__dict__ = session_state

    @classmethod
    def get_sessions(cls, user_id: str) -> List[str]:
        """Get sessions for a user_id.
        Parameters
        ----------
        user_id : str
            User ID.

        Returns
        --------
        List[str]
            List containing session IDs for user id.
        """
        return list(
            filter(
                lambda x: x != "None",
                map(
                    lambda x: x.split(":")[1],
                    [
                        session_name
                        for session_name in cls._objects.keys()
                        if session_name.startswith(user_id)
                    ],
                ),
            )
        )

    def connect(self, session_token: str) -> None:
        """Connect to remote session.
        Parameters
        ----------
        session_token : str
            Token for connection. It can be port number or a string containing
            hostname and port number separated by ':'.

        Returns
        --------
        None
        """
        session_token = session_token.strip()
        server_info = session_token.split(":")
        if len(server_info) == 1:
            self.session = Session(
                "localhost", int(session_token), cleanup_on_exit=False
            )
        if len(server_info) == 2:
            self.session = Session(
                server_info[0], int(server_info[1]), cleanup_on_exit=False
            )
        self.session.monitors_manager.refresh(None, None)
        self.settings_root = self.session.solver.root
        self.static_info = self.settings_root._static_info
        self._register_events()
        objects_handle.LocalObjectsHandle().add_outline_mesh(
            self._user_id, self._session_id
        )

    def get_event_info(self, event_name: str) -> object:
        """Get event info.
        Parameters
        ----------
        event_name : str
            Event name.

        Returns
        --------
        object
            Event info object.
        """
        with self._lock:
            return self._events_info_map.get(event_name)

    def _register_events(self):
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

        for event_name in [
            "IterationEndedEvent",
            "CalculationsStartedEvent",
            "TimestepEndedEvent",
            "ProgressEvent",
            "CalculationsEndedEvent",
            "InitializedEvent",
        ]:
            self.session.events_manager.register_callback(
                event_name,
                lambda session_id, event_info, event_name=event_name: store_info(
                    event_name, event_info
                ),
            )
