"""Module for events management."""
import itertools
from typing import Callable, List

from ansys.api.fluent.v0 import events_pb2 as EventsProtoModule
from ansys.fluent.core.streaming_services.streaming_services import StreamingService


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
            target=EventsManager._listen_events,
            streaming_service=service,
        )
        self._session_id: str = session_id
        self._id_iter = itertools.count()
        self._events_list: List[str] = [
            attr for attr in dir(EventsProtoModule) if attr.endswith("Event")
        ]

    def _listen_events(self, started_evt):
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
        if not event_name in self.events_list:
            raise RuntimeError(f"{event_name} is not a valid event.")
        return super().register_callback(
            service_name=event_name, call_back=call_back, *args, **kwargs
        )
