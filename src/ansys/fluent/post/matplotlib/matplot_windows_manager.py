"""Module for matplotlib windows management."""
import itertools
import multiprocessing as mp
from typing import List, Optional, Union

from ansys.fluent.core.session import Session
from ansys.fluent.core.utils.generic import AbstractSingletonMeta, in_notebook
from ansys.fluent.post import get_config
from ansys.fluent.post.matplotlib.plotter_defns import Plotter, ProcessPlotter
from ansys.fluent.post.post_data_extractor import XYPlotDataExtractor
from ansys.fluent.post.post_object_defns import MonitorDefn, PlotDefn, XYPlotDefn
from ansys.fluent.post.post_windows_manager import PostWindow, PostWindowsManager


class _ProcessPlotterHandle:
    """Class for process plotter handle."""

    def __init__(
        self,
        window_id,
        curves=[],
        title="XY Plot",
        xlabel="position",
        ylabel="",
    ):
        self._closed = False
        self.plot_pipe, plotter_pipe = mp.Pipe()
        self.plotter = ProcessPlotter(window_id, curves, title, xlabel, ylabel)
        self.plot_process = mp.Process(
            target=self.plotter, args=(plotter_pipe,), daemon=True
        )
        self.plot_process.start()
        Session._monitor_thread.cbs.append(self.close)

    def plot(self, data):
        self.plot_pipe.send(data)

    def set_properties(self, properties):
        self.plot_pipe.send({"properties": properties})

    def save_graphic(self, name: str):
        self.plot_pipe.send({"save_graphic": name})

    def is_closed(self):
        if self._closed:
            return True
        try:
            self.plot_pipe.send({})
        except (BrokenPipeError, AttributeError):
            self._closed = True
        return self._closed

    def close(self):
        if self._closed:
            return
        self._closed = True
        try:
            self.plot_pipe.send(None)
        except (BrokenPipeError, AttributeError):
            pass


class MatplotWindow(PostWindow):
    """Class for MatplotWindow."""

    def __init__(self, id: str, post_object: PlotDefn):
        """Instantiate a MatplotWindow.

        Parameters
        ----------
        id : str
            Window id.
        post_object : PlotDefn
            Object to plot.
        """
        self.id: str = id
        self.post_object = None
        self.plotter: Union[_ProcessPlotterHandle, Plotter] = self._get_plotter()
        self.close: bool = False
        self.refresh: bool = False

    def plot(self):
        """Draw plot."""
        if self.post_object is not None:
            plot = (
                _XYPlot(self.post_object, self.plotter)
                if self.post_object.__class__.__name__ == "XYPlot"
                else _MonitorPlot(self.post_object, self.plotter)
            )
            plot()

    # private methods
    def _get_plotter(self):
        return (
            Plotter(self.id)
            if in_notebook() or get_config()["blocking"]
            else _ProcessPlotterHandle(self.id)
        )


class _XYPlot:
    """Class for XYPlot."""

    def __init__(
        self, post_object: XYPlotDefn, plotter: Union[_ProcessPlotterHandle, Plotter]
    ):
        """Instantiate XYPlot.

        Parameters
        ----------
        post_object : XYPlotDefn
            Object to plot.
        plotter: Union[_ProcessPlotterHandle, Plotter]
            Plotter to plot data.
        """
        self.post_object: XYPlotDefn = post_object
        self.plotter: Union[_ProcessPlotterHandle, Plotter] = plotter

    def __call__(self):
        """Draw XY plot."""
        if not self.post_object:
            return
        properties = {
            "curves": self.post_object.surfaces_list(),
            "title": "XY Plot",
            "xlabel": "position",
            "ylabel": self.post_object.y_axis_function(),
        }
        xy_data = XYPlotDataExtractor(self.post_object).fetch_data()
        if in_notebook() or get_config()["blocking"]:
            self.plotter.set_properties(properties)
        else:
            try:
                self.plotter.set_properties(properties)
            except BrokenPipeError:
                self.plotter: Union[
                    _ProcessPlotterHandle, Plotter
                ] = self._get_plotter()
                self.plotter.set_properties(properties)
        self.plotter.plot(xy_data)


class _MonitorPlot:
    """Class MonitorPlot."""

    def __init__(
        self, post_object: MonitorDefn, plotter: Union[_ProcessPlotterHandle, Plotter]
    ):
        """Instantiate MonitorPlot.

        Parameters
        ----------
        post_object : MonitorDefn
            Object to plot.
        plotter: Union[_ProcessPlotterHandle, Plotter]
            Plotter to plot data.
        """
        self.post_object: MonitorDefn = post_object
        self.plotter: Union[_ProcessPlotterHandle, Plotter] = plotter

    def __call__(self):
        """Draw Monitor plot."""
        if not self.post_object:
            return
        monitors_manager = self.post_object._data_extractor.monitors_manager()
        indices, columns_data = monitors_manager.get_monitor_set_data(
            self.post_object.monitor_set_name()
        )
        xy_data = {}
        for column_name, column_data in columns_data.items():
            xy_data[column_name] = {"xvalues": indices, "yvalues": column_data}
        monitor_set_name = self.post_object.monitor_set_name()
        properties = {
            "curves": list(xy_data.keys()),
            "title": monitor_set_name,
            "xlabel": monitors_manager.get_monitor_set_prop(monitor_set_name, "xlabel"),
            "ylabel": monitors_manager.get_monitor_set_prop(monitor_set_name, "ylabel"),
            "yscale": "log" if monitor_set_name == "residual" else "linear",
        }

        if in_notebook() or get_config()["blocking"]:
            self.plotter.set_properties(properties)
        else:
            try:
                self.plotter.set_properties(properties)
            except BrokenPipeError:
                self.plotter: Union[
                    _ProcessPlotterHandle, Plotter
                ] = self._get_plotter()
                self.plotter.set_properties(properties)
        if xy_data:
            self.plotter.plot(xy_data)


class MatplotWindowsManager(PostWindowsManager, metaclass=AbstractSingletonMeta):
    """Class for matplot windows manager."""

    def __init__(self):
        """Instantiate a windows manager for matplotlib."""
        self._post_windows: Dict[str, MatplotWindow] = {}

    def open_window(self, window_id: Optional[str] = None) -> str:
        """Open new window.

        Parameters
        ----------
        window_id : str, optional
            Id for new window. If not specified unique id is used.

        Returns
        -------
        str
            Window id.
        """
        if not window_id:
            window_id = self._get_unique_window_id()
        self._open_window(window_id)
        return window_id

    def set_object_for_window(self, object: PlotDefn, window_id: str) -> None:
        """Associate post object with running window instance.

        Parameters
        ----------
        object : PlotDefn
            Post object to associate with window.

        window_id : str
            Window id to associate.

        Raises
        ------
        RuntimeError
            If window does not support object.
        """
        if not isinstance(object, PlotDefn):
            raise RuntimeError("object not implemented.")
        window = self._post_windows.get(window_id)
        if window:
            window.post_object = object

    def plot(
        self,
        object: PlotDefn,
        window_id: Optional[str] = None,
    ) -> None:
        """Draw plot.

        Parameters
        ----------
        object: PlotDefn
            Object to plot.

        window_id : str, optional
            Window id for plot. If not specified unique id is used.

        Raises
        ------
        RuntimeError
            If window does not support object.
        """
        if not isinstance(object, PlotDefn):
            raise RuntimeError("object not implemented.")
        if not window_id:
            window_id = self._get_unique_window_id()
        window = self._open_window(window_id)
        window.post_object = object
        window.plot()

    def save_graphic(
        self,
        window_id: str,
        format: str,
    ) -> None:
        """Save graphics.

        Parameters
        ----------
        window_id : str
            Window id for which graphic should be saved.
        format : str
            Graphic format. Supported formats are eps, jpeg, jpg,
            pdf, pgf, png, ps, raw, rgba, svg, svgz, tif and tiff.

        Raises
        ------
        ValueError
            If window does not support specified format.
        """
        window = self._post_windows.get(window_id)
        if window:
            window.plotter.save_graphic(f"{window_id}.{format}")

    def refresh_windows(
        self,
        session_id: Optional[str] = "",
        windows_id: Optional[List[str]] = [],
    ) -> None:
        """Refresh windows.

        Parameters
        ----------
        session_id : str, optional
           Session id to refresh. If specified, all windows which belong to
           specified session will be refreshed. Otherwise windows for all
           sessions will be refreshed.

        windows_id : List[str], optional
            Windows id to refresh. If not specified, all windows will be
            refreshed.
        """
        windows_id = self._get_windows_id(session_id, windows_id)
        for window_id in windows_id:
            window = self._post_windows.get(window_id)
            if window:
                window.refresh = True
                self.plot(window.post_object, window.id)

    def animate_windows(
        self,
        session_id: Optional[str] = "",
        windows_id: Optional[List[str]] = [],
    ) -> None:
        """Animate windows.

        Parameters
        ----------
        session_id : str, optional
           Session id to animate. If specified, animation will be created
           for windows which belong to specified session. Otherwise
           animation will be created for all windows.

        windows_id : List[str], optional
            Windows id to animate. If not specified, animation will be
            created for all windows.

        Raises
        ------
        NotImplementedError
            If not implemented.
        """
        raise NotImplementedError("animate_windows not implemented.")

    def close_windows(
        self,
        session_id: Optional[str] = "",
        windows_id: Optional[List[str]] = [],
    ) -> None:
        """Close windows.

        Parameters
        ----------
        session_id : str, optional
           Session id to close. If specified, windows which belong to
           specified session will be closed. Otherwise windows for all
           sessions will be closed.

        windows_id : List[str], optional
            Windows id to close. If not specified, all windows will be
            closed.
        """
        windows_id = self._get_windows_id(session_id, windows_id)
        for window_id in windows_id:
            window = self._post_windows.get(window_id)
            if window:
                window.plotter.close()
                window.close = True

    # private methods

    def _open_window(self, window_id: str) -> Union[Plotter, _ProcessPlotterHandle]:
        window = self._post_windows.get(window_id)
        plotter = None
        if (
            window
            and not window.plotter.is_closed()
            and (not (in_notebook() or get_config()["blocking"]) or window.refresh)
        ):
            window.refresh = False
        else:
            window = MatplotWindow(window_id, None)
            self._post_windows[window_id] = window
            if in_notebook():
                window.plotter()
        return window

    def _get_windows_id(
        self,
        session_id: Optional[str] = "",
        windows_id: Optional[List[str]] = [],
    ) -> List[str]:

        return [
            window_id
            for window_id in [
                window_id
                for window_id, window in self._post_windows.items()
                if not window.plotter.is_closed()
                and (
                    not session_id
                    or session_id == window.post_object._data_extractor.id()
                )
            ]
            if not windows_id or window_id in windows_id
        ]

    def _get_unique_window_id(self) -> str:
        itr_count = itertools.count()
        while True:
            window_id = f"window-{next(itr_count)}"
            if window_id not in self._post_windows:
                return window_id


matplot_windows_manager = MatplotWindowsManager()
