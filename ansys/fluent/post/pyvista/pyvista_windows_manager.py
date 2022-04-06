"""Module for pyVista windows management."""
import itertools
import threading
from typing import List, Optional, Union

import numpy as np
import pyvista as pv
from pyvistaqt import BackgroundPlotter

from ansys.fluent.core.session import Session
from ansys.fluent.core.utils.generic import AbstractSingletonMeta, in_notebook
from ansys.fluent.post import get_config
from ansys.fluent.post.post_object_defns import GraphicsDefn, PlotDefn
from ansys.fluent.post.post_windows_manager import (
    PostWindow,
    PostWindowsManager,
)


class PyVistaWindow(PostWindow):
    """Class for PyVista window."""

    def __init__(
        self,
        id: str,
        post_object: Union[GraphicsDefn, PlotDefn],
        *args,
        **kwargs,
    ):
        """
        Instantiate a PyVistaWindow.

        Parameters
        ----------
        id : str
            Window id.
        post_object : Union[GraphicsDefn, PlotDefn]
            Object to draw.
        """
        self.post_object: Union[GraphicsDefn, PlotDefn] = post_object
        self.id: str = id
        if "title" not in kwargs:
            kwargs.update({"title": f"PyFluent ({self.id})"})
        self.plotter: Union[BackgroundPlotter, pv.Plotter] = (
            pv.Plotter(*args, **kwargs)
            if in_notebook() or get_config()["blocking"]
            else BackgroundPlotter(*args, **kwargs)
        )
        self.animate: bool = False
        self.close: bool = False
        self.refresh: bool = False
        self.update: bool = False
        self._visible: bool = False
        self._init_properties()

    def plot(self, *args, **kwargs):
        """Plot graphics."""
        if not self.post_object:
            return
        obj = self.post_object
        plotter = self.plotter
        camera = plotter.camera.copy()
        plotter.clear()
        if obj.__class__.__name__ == "Mesh":
            self._display_mesh(obj, plotter)
        elif obj.__class__.__name__ == "Surface":
            if obj.surface.type() == "iso-surface":
                self._display_iso_surface(obj, plotter)
        elif obj.__class__.__name__ == "Contour":
            self._display_contour(obj, plotter)
        elif obj.__class__.__name__ == "Vector":
            self._display_vector(obj, plotter)
        if self.animate:
            plotter.write_frame()
        plotter.camera = camera.copy()
        if not self._visible:
            plotter.show(*args, **kwargs)
            self._visible = True

    # private methods

    def _init_properties(self):
        self.plotter.theme.cmap = "jet"
        self.plotter.background_color = "white"
        self.plotter.theme.font.color = "black"

    def _scalar_bar_default_properties(self) -> dict:
        return dict(
            title_font_size=20,
            label_font_size=16,
            shadow=True,
            fmt="%.6e",
            font_family="arial",
            vertical=True,
            position_x=0.06,
            position_y=0.3,
        )

    def _display_vector(
        self, obj, plotter: Union[BackgroundPlotter, pv.Plotter]
    ):

        if not obj.surfaces_list():
            raise RuntimeError("Vector definition is incomplete.")

        field_info = obj._data_extractor.field_info()
        field_data = obj._data_extractor.field_data()

        # surface ids
        surfaces_info = field_info.get_surfaces_info()
        surface_ids = [
            id
            for surf in obj.surfaces_list()
            for id in surfaces_info[surf]["surface_id"]
        ]

        # field
        field = "velocity-magnitude"

        # scalar bar properties
        scalar_bar_args = self._scalar_bar_default_properties()

        # get vector field data
        vector_field_data = field_data.get_vector_field(
            surface_ids, obj.vectors_of()
        )
        for surface_id, mesh_data in vector_field_data.items():
            mesh_data["vertices"].shape = mesh_data["vertices"].size // 3, 3
            mesh_data["vector"].shape = mesh_data["vector"].size // 3, 3
            vector_scale = mesh_data["vector-scale"][0]
            topology = "line" if mesh_data["faces"][0] == 2 else "face"
            if topology == "line":
                mesh = pv.PolyData(
                    mesh_data["vertices"],
                    lines=mesh_data["faces"],
                )
            else:
                mesh = pv.PolyData(
                    mesh_data["vertices"],
                    faces=mesh_data["faces"],
                )
            mesh.cell_data["vectors"] = mesh_data["vector"]
            velocity_magnitude = np.linalg.norm(mesh_data["vector"], axis=1)
            if obj.range.option() == "auto-range-off":
                auto_range_off = obj.range.auto_range_off
                range = [auto_range_off.minimum(), auto_range_off.maximum()]
                if auto_range_off.clip_to_range():
                    velocity_magnitude = np.ma.masked_outside(
                        velocity_magnitude,
                        auto_range_off.minimum(),
                        auto_range_off.maximum(),
                    ).filled(fill_value=0)
            else:
                auto_range_on = obj.range.auto_range_on
                if auto_range_on.global_range():
                    range = field_info.get_range(field, False)
                else:
                    range = field_info.get_range(field, False, surface_ids)

            if obj.skip():
                vmag = np.zeros(velocity_magnitude.size)
                vmag[:: obj.skip() + 1] = velocity_magnitude[:: obj.skip() + 1]
                velocity_magnitude = vmag
            mesh.cell_data["Velocity Magnitude"] = velocity_magnitude
            glyphs = mesh.glyph(
                orient="vectors",
                scale="Velocity Magnitude",
                factor=vector_scale * obj.scale(),
                geom=pv.Arrow(),
            )
            plotter.add_mesh(
                glyphs,
                scalar_bar_args=scalar_bar_args,
                clim=range,
            )
            if obj.show_edges():
                plotter.add_mesh(mesh, show_edges=True, color="white")

    def _display_contour(
        self, obj, plotter: Union[BackgroundPlotter, pv.Plotter]
    ):
        if not obj.surfaces_list() or not obj.field():
            raise RuntimeError("Contour definition is incomplete.")

        # contour properties
        field = obj.field()
        range_option = obj.range.option()
        filled = obj.filled()
        node_values = obj.node_values()
        boundary_values = obj.boundary_values()

        # scalar bar properties
        scalar_bar_args = self._scalar_bar_default_properties()

        field_info = obj._data_extractor.field_info()
        field_data = obj._data_extractor.field_data()
        surfaces_info = field_info.get_surfaces_info()
        surface_ids = [
            id
            for surf in obj.surfaces_list()
            for id in surfaces_info[surf]["surface_id"]
        ]
        # get scalar field data
        scalar_field_data = field_data.get_scalar_field(
            surface_ids,
            field,
            node_values,
            boundary_values,
        )
        # loop over all meshes
        for surface_id, mesh_data in scalar_field_data.items():
            mesh_data["vertices"].shape = mesh_data["vertices"].size // 3, 3
            topology = "line" if mesh_data["faces"][0] == 2 else "face"
            if topology == "line":
                mesh = pv.PolyData(
                    mesh_data["vertices"],
                    lines=mesh_data["faces"],
                )
            else:
                mesh = pv.PolyData(
                    mesh_data["vertices"],
                    faces=mesh_data["faces"],
                )
            if node_values:
                mesh.point_data[field] = mesh_data[field]
            else:
                mesh.cell_data[field] = mesh_data[field]
            if range_option == "auto-range-off":
                auto_range_off = obj.range.auto_range_off
                if auto_range_off.clip_to_range():
                    if np.min(mesh[field]) < auto_range_off.maximum():
                        maximum_below = mesh.clip_scalar(
                            scalars=field,
                            value=auto_range_off.maximum(),
                        )
                        if (
                            np.max(maximum_below[field])
                            > auto_range_off.minimum()
                        ):
                            minimum_above = maximum_below.clip_scalar(
                                scalars=field,
                                invert=False,
                                value=auto_range_off.minimum(),
                            )
                            if filled:
                                plotter.add_mesh(
                                    minimum_above,
                                    scalars=field,
                                    show_edges=obj.show_edges(),
                                    scalar_bar_args=scalar_bar_args,
                                )

                            if not filled and (
                                np.min(minimum_above[field])
                                != np.max(minimum_above[field])
                            ):
                                plotter.add_mesh(
                                    minimum_above.contour(isosurfaces=20),
                                    show_edges=obj.show_edges(),
                                )
                else:
                    if filled:
                        plotter.add_mesh(
                            mesh,
                            clim=[
                                auto_range_off.minimum(),
                                auto_range_off.maximum(),
                            ],
                            scalars=field,
                            show_edges=obj.show_edges(),
                            scalar_bar_args=scalar_bar_args,
                        )
                    if not filled and (
                        np.min(mesh[field]) != np.max(mesh[field])
                    ):
                        plotter.add_mesh(
                            mesh.contour(isosurfaces=20),
                            show_edges=obj.show_edges(),
                        )
            else:
                auto_range_on = obj.range.auto_range_on
                if auto_range_on.global_range():
                    if filled:
                        plotter.add_mesh(
                            mesh,
                            clim=field_info.get_range(field, False),
                            scalars=field,
                            show_edges=obj.show_edges(),
                            scalar_bar_args=scalar_bar_args,
                        )
                    if not filled and (
                        np.min(mesh[field]) != np.max(mesh[field])
                    ):
                        plotter.add_mesh(
                            mesh.contour(isosurfaces=20),
                            show_edges=obj.show_edges(),
                        )

                else:
                    if filled:
                        plotter.add_mesh(
                            mesh,
                            scalars=field,
                            show_edges=obj.show_edges(),
                            scalar_bar_args=scalar_bar_args,
                        )
                    if not filled and (
                        np.min(mesh[field]) != np.max(mesh[field])
                    ):
                        plotter.add_mesh(
                            mesh.contour(isosurfaces=20),
                            show_edges=obj.show_edges(),
                        )

    def _display_iso_surface(
        self, obj, plotter: Union[BackgroundPlotter, pv.Plotter]
    ):
        field = obj.surface.iso_surface.field()
        if not field:
            raise RuntimeError("Iso surface definition is incomplete.")

        dummy_surface_name = "_dummy_iso_surface_for_pyfluent"
        field_info = obj._data_extractor.field_info()
        surfaces_list = list(field_info.get_surfaces_info().keys())
        iso_value = obj.surface.iso_surface.iso_value()
        if dummy_surface_name in surfaces_list:
            obj._data_extractor.surface_api().delete_surface(
                dummy_surface_name
            )

        obj._data_extractor.surface_api().iso_surface(
            field, dummy_surface_name, (), (), iso_value, ()
        )

        surfaces_list = list(field_info.get_surfaces_info().keys())
        if dummy_surface_name not in surfaces_list:
            raise RuntimeError("Iso surface creation failed.")
        post_session = obj._get_top_most_parent()
        if obj.surface.iso_surface.rendering() == "mesh":
            mesh = post_session.Meshes[dummy_surface_name]
            mesh.surfaces_list = [dummy_surface_name]
            mesh.show_edges = True
            self._display_mesh(mesh, plotter)
            del post_session.Meshes[dummy_surface_name]
        else:
            contour = post_session.Contours[dummy_surface_name]
            contour.field = obj.surface.iso_surface.field()
            contour.surfaces_list = [dummy_surface_name]
            contour.show_edges = True
            contour.range.auto_range_on.global_range = True
            self._display_contour(contour, plotter)
            del post_session.Contours[dummy_surface_name]
        obj._data_extractor.surface_api().delete_surface(dummy_surface_name)

    def _display_mesh(
        self, obj, plotter: Union[BackgroundPlotter, pv.Plotter]
    ):
        if not obj.surfaces_list():
            raise RuntimeError("Mesh definition is incomplete.")
        field_info = obj._data_extractor.field_info()
        field_data = obj._data_extractor.field_data()
        surfaces_info = field_info.get_surfaces_info()
        surface_ids = [
            id
            for surf in obj.surfaces_list()
            for id in surfaces_info[surf]["surface_id"]
        ]
        surfaces_data = field_data.get_surfaces(surface_ids)
        for surface_id, mesh_data in surfaces_data.items():
            mesh_data["vertices"].shape = mesh_data["vertices"].size // 3, 3
            topology = "line" if mesh_data["faces"][0] == 2 else "face"
            if topology == "line":
                mesh = pv.PolyData(
                    mesh_data["vertices"],
                    lines=mesh_data["faces"],
                )
            else:
                mesh = pv.PolyData(
                    mesh_data["vertices"],
                    faces=mesh_data["faces"],
                )
            plotter.add_mesh(
                mesh, show_edges=obj.show_edges(), color="lightgrey"
            )


class PyVistaBGWindow(PyVistaWindow):
    """Class for PyVista background window."""

    def __init__(
        self,
        id: str,
        post_object: Union[GraphicsDefn, PlotDefn],
        *args,
        **kwargs,
    ):
        super().__init__(id, post_object, *args, **kwargs)

    def _get_refresh_for_bg_plotter(self, window: "PyVistaBGWindow"):
        def refresh():

            with PyVistaWindowsManager._condition:
                plotter = window.plotter
                if window.close:
                    window.animate = False
                    plotter.close()
                    return
                if not window.update:
                    return
                window.update = False
                try:
                    window.plot()
                finally:
                    PyVistaWindowsManager._condition.notify()

        return refresh


class PyVistaWindowsManager(
    PostWindowsManager, metaclass=AbstractSingletonMeta
):
    """Class for PyVista windows manager."""

    _condition = threading.Condition()

    def __init__(self):
        """Instantiate WindowManager for PyVista."""
        self._post_windows: Dict[str:PyVistaWindow] = {}
        self._plotter_thread: threading.Thread = None
        self._background_plotter_data: dict = None
        self._exit_thread: bool = False
        self._app = None

    def open_window(
        self, window_id: Optional[str] = None, *args, **kwargs
    ) -> str:
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
        with self._condition:
            if not window_id:
                window_id = self._get_unique_window_id()
            if in_notebook() or get_config()["blocking"]:
                self._open_window_notebook(window_id, *args, **kwargs)
            else:
                self._background_plotter_data = {
                    "window_id": window_id,
                    "args": args,
                    "kwargs": kwargs,
                }
                self._open_and_plot_console()
            return window_id

    def set_object_for_window(
        self, object: Union[GraphicsDefn, PlotDefn], window_id: str
    ) -> None:
        """Associate post object with running window instance.

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
        if not isinstance(object, GraphicsDefn):
            raise RuntimeError("object not implemented.")
        with self._condition:
            window = self._post_windows.get(window_id)
            if window:
                window.post_object = object

    def plot(
        self,
        object: Union[GraphicsDefn, PlotDefn],
        window_id: Optional[str] = None,
        *args,
        **kwargs,
    ) -> None:
        """Draw plot.

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
        if not isinstance(object, GraphicsDefn):
            raise RuntimeError("object not implemented.")
        with self._condition:
            if not window_id:
                window_id = self._get_unique_window_id()
            if in_notebook() or get_config()["blocking"]:
                self._plot_notebook(object, window_id, *args, **kwargs)
            else:
                self._background_plotter_data = {
                    "window_id": window_id,
                    "post_object": object,
                    "args": args,
                    "kwargs": kwargs,
                }
                self._open_and_plot_console()

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
            Graphic format. Supported formats are svg, eps, ps, pdf and tex.

        Raises
        ------
        ValueError
            If window does not support specified format.
        """
        with self._condition:
            window = self._post_windows.get(window_id)
            if window:
                window.plotter.save_graphic(f"{window_id}.{format}")

    def refresh_windows(
        self,
        session_id: Optional[str] = "",
        windows_id: Optional[List[str]] = [],
        *args,
        **kwargs,
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
        with self._condition:
            windows_id = self._get_windows_id(session_id, windows_id)
            for window_id in windows_id:
                window = self._post_windows.get(window_id)
                if window:
                    window.refresh = True
                    self.plot(window.post_object, window.id, *args, **kwargs)

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
        with self._condition:
            windows_id = self._get_windows_id(session_id, windows_id)
            for window_id in windows_id:
                window = self._post_windows.get(window_id)
                if window:
                    window.animate = True
                    window.plotter.open_gif(f"{window.id}.gif")

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
        with self._condition:
            windows_id = self._get_windows_id(session_id, windows_id)
            for window_id in windows_id:
                window = self._post_windows.get(window_id)
                if window:
                    if in_notebook() or get_config()["blocking"]:
                        window.plotter.close()
                    window.close = True

    # private methods

    def _display(self) -> None:
        while True:
            with self._condition:
                if self._exit_thread:
                    break
                if self._background_plotter_data:
                    window_id = self._background_plotter_data.get("window_id")
                    post_object = self._background_plotter_data.get(
                        "post_object"
                    )
                    args = (
                        self._background_plotter_data.get("args", ())
                        if not post_object
                        else ()
                    )
                    kwargs = (
                        self._background_plotter_data.get("kwargs", {})
                        if not post_object
                        else {}
                    )
                    window = self._post_windows.get(window_id)
                    plotter = window.plotter if window else None
                    animate = window.animate if window else False
                    if not plotter or plotter._closed:
                        try:
                            window = PyVistaBGWindow(
                                window_id, post_object, *args, **kwargs
                            )
                        finally:
                            PyVistaWindowsManager._condition.notify()
                        plotter = window.plotter
                        self._app = plotter.app
                        plotter.add_callback(
                            window._get_refresh_for_bg_plotter(window),
                            100,
                        )
                    window.post_object = self._background_plotter_data.get(
                        "post_object"
                    )
                    window.animate = animate
                    window.update = True
                    self._post_windows[window.id] = window
                    self._background_plotter_data = None

            self._app.processEvents()
        with self._condition:
            for window in self._post_windows.values():
                plotter = window.plotter
                plotter.close()
                plotter.app.quit()
            self._post_windows.clear()
            self._condition.notify()

    def _open_and_plot_console(self) -> None:
        if self._exit_thread:
            return

        if not self._plotter_thread:
            if Session._monitor_thread:
                Session._monitor_thread.cbs.append(self._exit)
            self._plotter_thread = threading.Thread(
                target=self._display, args=()
            )
            self._plotter_thread.start()

        with self._condition:
            self._condition.wait()

    def _open_window_notebook(
        self, window_id: str, *args, **kwargs
    ) -> PyVistaWindow:
        window = self._post_windows.get(window_id)
        plotter = None
        if window and not window.close and window.refresh:
            window.refresh = False
        else:
            window = PyVistaWindow(window_id, None, *args, **kwargs)
            self._post_windows[window_id] = window
        return window

    def _plot_notebook(
        self, obj: object, window_id: str, *args, **kwargs
    ) -> None:
        window = self._open_window_notebook(window_id)
        window.post_object = obj
        plotter = window.plotter
        window.plot(*args, **kwargs)

    def _get_windows_id(
        self,
        session_id: Optional[str] = "",
        windows_id: Optional[List[str]] = [],
    ) -> List[str]:
        with self._condition:
            return [
                window_id
                for window_id in [
                    window_id
                    for window_id, window in self._post_windows.items()
                    if not window.plotter._closed
                    and (
                        not session_id
                        or session_id
                        == window.post_object._data_extractor.id()
                    )
                ]
                if not windows_id or window_id in windows_id
            ]

    def _exit(self) -> None:
        if self._plotter_thread:
            with self._condition:
                self._exit_thread = True
                self._condition.wait()
            self._plotter_thread.join()
            self._plotter_thread = None

    def _get_unique_window_id(self) -> str:
        itr_count = itertools.count()
        with self._condition:
            while True:
                window_id = f"window-{next(itr_count)}"
                if window_id not in self._post_windows:
                    return window_id


pyvista_windows_manager = PyVistaWindowsManager()
