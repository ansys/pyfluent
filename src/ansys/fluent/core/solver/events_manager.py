"""Module for events management."""
from functools import partial
import itertools
import threading
from typing import Callable, List

from ansys.api.fluent.v0 import events_pb2 as EventsProtoModule


class EventsManager:
    """Manages server-side events.

    This class allows the client to register and unregister callbacks with server events.

    Parameters
    ----------
    session_id : str
        Session ID.
    service :
        Event streaming service.

    Attributes
    ----------
    events_list : List[str]
        List of supported events.
    """

    def __init__(self, session_id: str, service):
        self._session_id: str = session_id
        self._events_service = service
        self._events_to_callbacks_map: dict = {}
        self._id_iter = itertools.count()
        self._lock: threading.Lock = threading.Lock()
        self._events_thread = None
        self._events_list: List[str] = [
            attr for attr in dir(EventsProtoModule) if attr.endswith("Event")
        ]

    def _listen_events(self, started_evt):
        responses = self._events_service.begin_streaming(started_evt)
        while True:
            try:
                response = next(responses)
                event_name = response.WhichOneof("as")
                with self._lock:
                    callbacks_map = self._events_to_callbacks_map.get(event_name, {})
                    for call_back in callbacks_map.values():
                        call_back(
                            session_id=self._session_id,
                            event_info=getattr(response, event_name),
                        )
            except StopIteration:
                break

    @property
    def events_list(self) -> List[str]:
        """Get a list of supported events.

        Parameters
        ----------
        None

        Returns
        -------
        List[str]
            List of supported events.
        """
        return self._events_list

    def register_callback(
        self, event_name: str, call_back: Callable, *args, **kwargs
    ) -> str:
        """Register the callback.

        Parameters
        ----------
        event_name : str
            Event name to register the callback to.

        call_back : Callable
            Callback to register.

        Returns
        -------
        str
            Registered callback ID.

        Raises
        ------
        RuntimeError
            If event name is not valid.
        """
        if not event_name in self.events_list:
            raise RuntimeError(f"{event_name} is not a valid event.")
        with self._lock:
            event_name = event_name.lower()
            id = f"{event_name}-{next(self._id_iter)}"
            callbacks_map = self._events_to_callbacks_map.get(event_name)
            if callbacks_map:
                callbacks_map.update({id: partial(call_back, *args, **kwargs)})
            else:
                self._events_to_callbacks_map[event_name] = {
                    id: partial(call_back, *args, **kwargs)
                }
            return id

    def unregister_callback(self, callback_id: str):
        """Unregister the callback.

        Parameters
        ----------
        callback_id : str
            ID of the registered callback.
        """
        with self._lock:
            for callbacks_map in self._events_to_callbacks_map.values():
                if callback_id in callbacks_map:
                    del callbacks_map[callback_id]

    def start(self):
        """Start EventsManager.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        if self._events_thread is None:
            started_evt = threading.Event()
            self._events_thread: threading.Thread = threading.Thread(
                target=EventsManager._listen_events, args=(self, started_evt)
            )
            self._events_thread.start()
            started_evt.wait()

    def stop(self):
        """Stop EventsManager.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        if self._events_thread:
            self._events_service.end_streaming()
            self._events_thread.join()
            self._events_thread = None
