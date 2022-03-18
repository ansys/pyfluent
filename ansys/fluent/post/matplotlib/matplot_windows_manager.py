"""Module for matplotlib windows management."""
import itertools
import multiprocessing as mp
from typing import List, Optional, Union

import numpy as np
from ansys.fluent.core.session import Session
from ansys.fluent.core.utils.generic import AbstractSingletonMeta, in_notebook
from ansys.fluent.post.matplotlib.plotter_defns import Plotter, ProcessPlotter
from ansys.fluent.post.post_object_defns import GraphicsDefn, PlotDefn
from ansys.fluent.post.post_windows_manager import (
    PostWindow,
    PostWindowsManager,
)


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
        self.plotter = ProcessPlotter(
            window_id, curves, title, xlabel, ylabel
        )
        self.plot_process = mp.Process(
            target=self.plotter, args=(plotter_pipe,), daemon=True
        )
        self.plot_process.start()
        Session._monitor_thread.cbs.append(self.close)

    def plot(self, data):
        self.plot_pipe.send(data)

    def set_properties(self, properties):
        self.plot_pipe.send({"properties": properties})

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

    def __init__(self, id: str, post_object: Union[GraphicsDefn, PlotDefn]):
        """
        Instantiate a MatplotWindow.

        Parameters
        ----------
        id : str
            Window id.
        post_object : Union[GraphicsDefn, PlotDefn]
            Object to plot.
        """
        self.post_object: Union[GraphicsDefn, PlotDefn] = post_object
        self.id: str = id
        self.properties: dict = None
        self.plotter: Union[
            _ProcessPlotterHandle, Plotter
        ] = self._get_plotter()
        self.animate: bool = False
        self.close: bool = False
        self.refresh: bool = False
        if in_notebook():
            self.plotter()

    def plot(self):
        """Draw plot."""
        if not self.post_object:
            return
        xy_data = self._get_xy_plot_data()
        if in_notebook():
            self.plotter.set_properties(self.properties)
        else:
            try:
                self.plotter.set_properties(self.properties)
            except BrokenPipeError:
                self.plotter: Union[
                    _ProcessPlotterHandle, Plotter
                ] = self._get_plotter()
                self.plotter.set_properties(self.properties)
        self.plotter.plot(xy_data)

    # private methods
    def _get_plotter(self):
        return (
            Plotter(self.id)
            if in_notebook()
            else _ProcessPlotterHandle(self.id)
        )

    def _get_xy_plot_data(self):
        obj = self.post_object
        field = obj.y_axis_function()
        node_values = obj.node_values()
        boundary_values = obj.boundary_values()
        direction_vector = obj.direction_vector()
        surfaces_list = obj.surfaces_list()
        self.properties = {
            "curves": surfaces_list,
            "title": "XY Plot",
            "xlabel": "position",
            "ylabel": field,
        }
        field_info = obj.field_info()
        field_data = obj.field_data()
        surfaces_info = field_info.get_surfaces_info()
        surface_ids = [
            id
            for surf in obj.surfaces_list()
            for id in surfaces_info[surf]["surface_id"]
        ]
        # get scalar field data
        data = field_data.get_scalar_field(
            surface_ids,
            field,
            True,
            boundary_values,
        )

        # loop over all meshes
        xy_plots_data = {}
        surfaces_list_iter = iter(surfaces_list)
        for surface_id, mesh_data in data.items():
            mesh_data["vertices"].shape = mesh_data["vertices"].size // 3, 3
            faces = mesh_data["faces"]
            y_values = mesh_data[field]
            x_values = np.matmul(mesh_data["vertices"], direction_vector)
            structured_data = np.empty(
                x_values.size,
                dtype={
                    "names": ("xvalues", "yvalues"),
                    "formats": ("f8", "f8"),
                },
            )
            structured_data["xvalues"] = x_values
            structured_data["yvalues"] = y_values
            sort = np.argsort(structured_data, order=["xvalues"])
            surface_name = next(surfaces_list_iter)
            xy_plots_data[surface_name] = structured_data[sort]
        return xy_plots_data


class MatplotWindowsManager(
    PostWindowsManager, metaclass=AbstractSingletonMeta
):
    """Class for matplot windows manager."""

    def __init__(self):
        """Instantiate a windows manager for matplotlib."""
        self._post_windows: Dict[str, MatplotWindow] = {}

    def open_window(self, window_id: Optional[str] = None) -> str:
        """
        Open new window.

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

    def set_object_for_window(
        self, object: Union[PlotDefn, GraphicsDefn], window_id: str
    ) -> None:
        """
        Associate post object with running window instance.

        Parameters
        ----------
        object : Union[GraphicsDefn, PlotDefn]
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
        object: Union[PlotDefn, GraphicsDefn],
        window_id: Optional[str] = None,
    ) -> None:
        """
        Draw plot.

        Parameters
        ----------
        object: Union[GraphicsDefn, PlotDefn]
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

    def refresh_windows(
        self,
        session_id: Optional[str] = "",
        windows_id: Optional[List[str]] = [],
    ) -> None:
        """
        Refresh windows.

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
        """
        Animate windows.

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
        """
        Close windows.

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

    def _open_window(
        self, window_id: str
    ) -> Union[Plotter, _ProcessPlotterHandle]:
        window = self._post_windows.get(window_id)
        plotter = None
        if (
            window
            and not window.plotter.is_closed()
            and (not in_notebook() or window.refresh)
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
                    or session_id
                    == window.graphics_object.session_id()
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
