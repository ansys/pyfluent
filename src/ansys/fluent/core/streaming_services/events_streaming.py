"""Module for events management."""
from functools import partial
from typing import Callable, List

from ansys.api.fluent.v0 import events_pb2 as EventsProtoModule
from ansys.fluent.core.streaming_services.streaming import StreamingService


class EventsManager(StreamingService):
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
        super().__init__(
            target=EventsManager._process_streaming,
            streaming_service=service,
        )
        self._session_id: str = session_id
        self._events_list: List[str] = [
            attr for attr in dir(EventsProtoModule) if attr.endswith("Event")
        ]

    def _process_streaming(self, started_evt):
        responses = self._streaming_service.begin_streaming(started_evt)
        while True:
            try:
                response = next(responses)
                event_name = response.WhichOneof("as")
                with self._lock:
                    self._streaming = True
                    callbacks_map = self._service_callbacks.get(event_name, {})
                    for call_back in callbacks_map.values():
                        call_back(
                            session_id=self._session_id,
                            event_info=getattr(response, event_name),
                        )
            except StopIteration:
                break

    def register_callback(
        self, event_name: str = None, call_back: Callable = None, *args, **kwargs
    ):
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
        if event_name is None or call_back is None:
            raise RuntimeError(
                "Please provide compulsory arguments : 'event_name' and 'call_back'"
            )

        if event_name not in self.events_list:
            raise RuntimeError(f"{event_name} is not a valid event.")
        with self._lock:
            event_name = event_name.lower()
            callback_id = f"{event_name}-{next(self._service_callback_id)}"
            callbacks_map = self._service_callbacks.get(event_name)
            if callbacks_map:
                callbacks_map.update({callback_id: partial(call_back, *args, **kwargs)})
            else:
                self._service_callbacks[event_name] = {
                    callback_id: partial(call_back, *args, **kwargs)
                }

    def unregister_callback(self, callback_id: str):
        """Unregister the callback.

        Parameters
        ----------
        callback_id : str
            ID of the registered callback.
        """
        with self._lock:
            for callbacks_map in self._service_callbacks.values():
                if callback_id in callbacks_map:
                    del callbacks_map[callback_id]

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
