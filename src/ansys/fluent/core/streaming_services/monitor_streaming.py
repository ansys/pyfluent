"""Module for monitors management."""

import threading
from typing import Dict, List, Tuple, Union

import numpy as np
import pandas as pd

from ansys.fluent.core.streaming_services.streaming import StreamingService


class MonitorsManager(StreamingService):
    """Manages monitors (Fluent residuals and report definitions monitors).

    Parameters
    ----------
    session_id : str
        Session ID.
    service : MonitorsService
        Monitors streaming service.
    """

    def __init__(self, session_id: str, service):
        super().__init__(
            target=MonitorsManager._process_streaming,
            streaming_service=service,
        )
        self._session_id: str = session_id
        self._lock_refresh: threading.Lock = threading.Lock()
        self._monitors_info = None
        self._data_frames = {}

    def get_monitor_set_names(self) -> List[str]:
        """Get monitor set names.

        Parameters
        ----------
        None

        Returns
        -------
        List[str]
            List of all monitor set names.
        """
        with self._lock:
            return list(self._data_frames)

    def get_monitor_set_prop(self, monitor_set_name: str, property: str) -> str:
        """Get monitor set property.

        Parameters
        ----------
        monitor_set_name : str
            Name of the monitor.
        property : str
            Property of the monitor set. It can be ``title``, ``xlabel``, or ``ylabel``.

        Returns
        -------
        str
            Monitor set property.
        """
        with self._lock:
            return self._monitors_info.get(monitor_set_name, {}).get(property)

    def get_monitor_set_plot(
        self, monitor_set_name, *args, **kwargs
    ) -> Union[None, object]:
        """Get monitor set plot.

        Parameters
        ----------
        monitor_set_name : str
            Name of the monitor.

        Returns
        -------
        Union[None, object]
            Returns ``None`` if the `DataFrame <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.plot.html>`_
            is empty. Otherwise, it returns the plot object, depending on the ``plotting.backend``.
        """
        with self._lock:
            df = self._data_frames[monitor_set_name]["df"]
            return None if df.empty else df.plot(*args, **kwargs)

    def get_monitor_set_data(
        self, monitor_set_name, start_index: int = 0, end_index: int = None
    ) -> Tuple[np.array, Dict[str, np.array]]:
        """Get monitor set data.

        Parameters
        ----------
        monitor_set_name : str
            Name of the monitor set.
        start_index: int, optional
            Start index to provide data.
        end_index: int, optional
            End index to provide data.

        Returns
        -------
        Tuple[np.array, Dict[str, np.array]]
            Tuple containing two elements: a numpy array of x-axis values and a dictionary
            associating monitor names of type ``str`` to numpy arrays of y-axis values.
        """
        with self._lock:
            df_data = self._data_frames[monitor_set_name]
            try:
                df = df_data["df"].iloc[start_index:end_index]
            except IndexError:
                return (np.array([]), {})
            return (
                (np.array([]), {})
                if df.empty
                else (
                    df.index.to_numpy(),
                    {column: df[[column]].to_numpy() for column in df.columns},
                )
            )

    def refresh(self, session_id, event_info) -> None:
        """Refresh plots on-initialized and data-read events.

        This method is registered with the EventsManager and is called
        to refresh plots whenever on-initialized and data-read events occur.

        Parameters
        ----------
        session_id : str
            Name of the monitor set.
        event_info : object
            Event info object.

        Returns
        -------
        None
        """
        with self._lock_refresh:
            self.stop()
            self.start()

    def _prepare(self):
        self._update_dataframe()

    def _process_streaming(self, started_evt):
        """Begin monitors streaming."""
        responses = self._streaming_service.begin_streaming(started_evt)

        while True:
            try:
                data_received = {}
                response = next(responses)
                x_axis_type = response.xaxisdata.xaxistype
                x_axis_index = response.xaxisdata.xaxisindex
                data_received["xvalues"] = x_axis_index
                for y_axis_value in response.yaxisvalues:
                    data_received[y_axis_value.name] = y_axis_value.value
                with self._lock:
                    self._streaming = True
                    for monitor_set_name, df_data in self._data_frames.items():
                        df = df_data["df"]
                        monitors = df_data["monitors"]
                        monitor_data = []
                        for monitor_name in monitors:
                            if monitor_name not in data_received:
                                monitor_data = []
                                break
                            monitor_data.append(data_received[monitor_name])

                        if monitor_data:
                            new_df = pd.DataFrame([monitor_data], columns=monitors)
                            new_df.set_index("xvalues", inplace=True)
                            df_data["df"] = pd.concat([df, new_df])
                            for callback_map in self._service_callbacks.values():
                                callback, args, kwargs = callback_map
                                callback(*args, **kwargs)

            except StopIteration:
                break

    def _update_dataframe(self):
        with self._lock:
            self._monitors_info = self._streaming_service.get_monitors_info()
            self._data_frames = {}
            for monitor_set_name, monitor_set_info in self._monitors_info.items():
                self._data_frames[monitor_set_name] = {}
                monitors_name = list(monitor_set_info["monitors"]) + ["xvalues"]
                df = pd.DataFrame([], columns=monitors_name)
                df.set_index("xvalues", inplace=True)
                self._data_frames[monitor_set_name]["df"] = df
                self._data_frames[monitor_set_name]["monitors"] = monitors_name
