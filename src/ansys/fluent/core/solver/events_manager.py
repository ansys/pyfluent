"""Module for events management."""
from functools import partial
import itertools
import threading
from typing import Callable, List

from ansys.api.fluent.v0 import events_pb2 as EventsProtoModule


class EventsManager:
    """Manages the server side events.

    Allows client to register/unregister callbacks with server events.

    Parameters
    ----------
    session_id : str
        Session id.
    service :
        Event streaming service.

    Properties
    ----------
    events_list : List[str]
        List of supported events.
    """

    def __init__(self, session_id: str, service):
        self.__session_id: str = session_id
        self.__events_service = service
        self.__events_to_callbacks_map: dict = {}
        self.__id_iter = itertools.count()
        self.__lock: threading.Lock = threading.Lock()
        self.__events_list: List[str] = [
            attr for attr in dir(EventsProtoModule) if attr.endswith("Event")
        ]
        self.__events_thread: threading.Thread = threading.Thread(
            target=EventsManager.__listen_events, args=(self,)
        )
        self.__events_thread.start()

    def __listen_events(self):
        responses = self.__events_service.begin_streaming()
        while True:
            try:
                response = next(responses)
                event_name = response.WhichOneof("as")
                with self.__lock:
                    callbacks_map = self.__events_to_callbacks_map.get(event_name, {})
                    for call_back in callbacks_map.values():
                        call_back(
                            session_id=self.__session_id,
                            event_info=getattr(response, event_name),
                        )
            except StopIteration:
                break

    @property
    def events_list(self) -> List[str]:
        return self.__events_list

    def register_callback(
        self, event_name: str, call_back: Callable, *args, **kwargs
    ) -> str:
        """Register Callback.

        Parameters
        ----------
        event_name : str
            Event name to which callback should be registered.

        call_back : Callable
            Callback to register.

        Raises
        ------
        RuntimeError
            If event name is not valid.

        Returns
        -------
        str
            Registered callback Id.
        """
        if not event_name in self.events_list:
            raise RuntimeError(f"{event_name} is not a valid event.")
        with self.__lock:
            event_name = event_name.lower()
            id = f"{event_name}-{next(self.__id_iter)}"
            callbacks_map = self.__events_to_callbacks_map.get(event_name)
            if callbacks_map:
                callbacks_map.update({id: partial(call_back, *args, **kwargs)})
            else:
                self.__events_to_callbacks_map[event_name] = {
                    id: partial(call_back, *args, **kwargs)
                }
            return id

    def unregister_callback(self, callback_id: str):
        """Unregister Callback.

        Parameters
        ----------
        callback_id : str
            Registered callback Id.
        """
        with self.__lock:
            for callbacks_map in self.__events_to_callbacks_map.values():
                if callback_id in callbacks_map:
                    del callbacks_map[callback_id]

    def stop(self):
        """Stop Events manager."""
        self.__events_service.end_streaming()
