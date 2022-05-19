"""Module for pyVista windows management."""
import itertools
import threading
from typing import List, Optional, Union

import numpy as np
import pyvista as pv
from pyvistaqt import BackgroundPlotter

from ansys.api.fluent.v0.field_data_pb2 import PayloadTag
from ansys.fluent.core.session import Session
from ansys.fluent.core.utils.generic import AbstractSingletonMeta, in_notebook
from ansys.fluent.post import get_config
from ansys.fluent.post.post_object_defns import GraphicsDefn, PlotDefn
from ansys.fluent.post.post_windows_manager import PostWindow, PostWindowsManager


class DataExtractor:
    def __init__(self, post_object: Union[GraphicsDefn, PlotDefn]):
        self._post_object: Union[GraphicsDefn, PlotDefn] = post_object

    def fetch_data(self):
        if self._post_object.__class__.__name__ == "Mesh":
            return self._fetch_mesh_data(self._post_object)
        elif self._post_object.__class__.__name__ == "Surface":
            return self._fetch_surface_data(self._post_object)
        elif self._post_object.__class__.__name__ == "Contour":
            return self._fetch_contour_data(self._post_object)
        elif self._post_object.__class__.__name__ == "Vector":
            return self._fetch_vector_data(self._post_object)

    def _fetch_mesh_data(self, obj):
        if not obj.surfaces_list():
            raise RuntimeError("Mesh definition is incomplete.")
        obj._pre_display()
        field_info = obj._data_extractor.field_info()
        field_data = obj._data_extractor.field_data()
        surfaces_info = field_info.get_surfaces_info()
        surface_ids = [
            id
            for surf in map(
                obj._data_extractor.remote_surface_name, obj.surfaces_list()
            )
            for id in surfaces_info[surf]["surface_id"]
        ]

        field_data.add_get_surfaces_request(surface_ids)
        surface_tag = 0

        surfaces_data = field_data.get_fields()[surface_tag]
        obj._post_display()
        return surfaces_data

    def _fetch_surface_data(self, obj):
        surface_api = obj._data_extractor.surface_api
        surface_api.create_surface_on_server()
        dummy_object = "dummy_object"
        post_session = obj._get_top_most_parent()
        scalar_field_data = None
        if (
            obj.surface.type() == "iso-surface"
            and obj.surface.iso_surface.rendering() == "contour"
        ):
            contour = post_session.Contours[dummy_object]
            contour.field = obj.surface.iso_surface.field()
            contour.surfaces_list = [obj._name]
            contour.show_edges = True
            contour.range.auto_range_on.global_range = True
            mesh_data, scalar_field_data = self._fetch_contour_data(contour)
            del post_session.Contours[dummy_object]
        else:
            mesh = post_session.Meshes[dummy_object]
            mesh.surfaces_list = [obj._name]
            mesh.show_edges = True
            mesh_data = self._fetch_mesh_data(mesh)
        surface_api.delete_surface_on_server()
        return mesh_data, scalar_field_data

    def _fetch_contour_data(self, obj):
        if not obj.surfaces_list() or not obj.field():
            raise RuntimeError("Contour definition is incomplete.")

        # contour properties
        obj._pre_display()
        field = obj.field()
        range_option = obj.range.option()
        filled = obj.filled()
        contour_lines = obj.contour_lines()
        node_values = obj.node_values()
        boundary_values = obj.boundary_values()

        field_info = obj._data_extractor.field_info()
        field_data = obj._data_extractor.field_data()
        surfaces_info = field_info.get_surfaces_info()
        surface_ids = [
            id
            for surf in map(
                obj._data_extractor.remote_surface_name, obj.surfaces_list()
            )
            for id in surfaces_info[surf]["surface_id"]
        ]
        # get scalar field data
        field_data.add_get_surfaces_request(surface_ids)
        field_data.add_get_scalar_fields_request(
            surface_ids,
            field,
            node_values,
            boundary_values,
        )

        location_tag = (
            field_data._payloadTags[PayloadTag.NODE_LOCATION]
            if node_values
            else field_data._payloadTags[PayloadTag.ELEMENT_LOCATION]
        )
        boundary_value_tag = (
            field_data._payloadTags[PayloadTag.BOUNDARY_VALUES]
            if boundary_values
            else 0
        )
        surface_tag = 0

        scalar_field_payload_data = field_data.get_fields()
        data_tag = location_tag | boundary_value_tag
        scalar_field_data = scalar_field_payload_data[data_tag]
        surface_data = scalar_field_payload_data[surface_tag]
        obj._post_display()
        return surface_data, scalar_field_data

    def _fetch_vector_data(self, obj):

        if not obj.surfaces_list():
            raise RuntimeError("Vector definition is incomplete.")

        obj._pre_display()
        field_info = obj._data_extractor.field_info()
        field_data = obj._data_extractor.field_data()

        # surface ids
        surfaces_info = field_info.get_surfaces_info()
        surface_ids = [
            id
            for surf in map(
                obj._data_extractor.remote_surface_name, obj.surfaces_list()
            )
            for id in surfaces_info[surf]["surface_id"]
        ]

        field_data.add_get_surfaces_request(
            surface_ids, provide_faces_centroid=True, provide_faces_normal=True
        )
        field_data.add_get_vector_fields_request(surface_ids, obj.vectors_of())
        vector_field_tag = 0
        fields = field_data.get_fields()[vector_field_tag]
        obj._post_display()
        return fields


class PyVistaWindow(PostWindow):
    """Class for PyVista window."""

    def __init__(self, id: str, post_object: Union[GraphicsDefn, PlotDefn]):
        """Instantiate a PyVistaWindow.

        Parameters
        ----------
        id : str
            Window id.
        post_object : Union[GraphicsDefn, PlotDefn]
            Object to draw.
        """
        self.post_object: Union[GraphicsDefn, PlotDefn] = post_object
        self.id: str = id
        self.plotter: Union[BackgroundPlotter, pv.Plotter] = (
            pv.Plotter(title=f"PyFluent ({self.id})")
            if in_notebook() or get_config()["blocking"]
            else BackgroundPlotter(title=f"PyFluent ({self.id})")
        )
        self.animate: bool = False
        self.close: bool = False
        self.refresh: bool = False
        self.update: bool = False
        self._visible: bool = False
        self._init_properties()

    def plot(self):
        """Plot graphics."""
        if not self.post_object:
            return
        obj = self.post_object
        plotter = self.plotter
        camera = plotter.camera.copy()
        if in_notebook() and self.plotter.theme._jupyter_backend == "pythreejs":
            plotter.remove_actor(plotter.renderer.actors.copy())
        else:
            plotter.clear()
        if obj.__class__.__name__ == "Mesh":
            self._display_mesh(obj, plotter)
        elif obj.__class__.__name__ == "Surface":
            self._display_surface(obj, plotter)
        elif obj.__class__.__name__ == "Contour":
            self._display_contour(obj, plotter)
        elif obj.__class__.__name__ == "Vector":
            self._display_vector(obj, plotter)
        if self.animate:
            plotter.write_frame()
        view = get_config()["set_view_on_display"]
        view_fun = {
            "xy": plotter.view_xy,
            "xz": plotter.view_xz,
            "yx": plotter.view_yx,
            "yz": plotter.view_yz,
            "zx": plotter.view_zx,
            "zy": plotter.view_zy,
            "isometric": plotter.view_isometric,
        }.get(view)
        if view_fun:
            view_fun()
        else:
            plotter.camera = camera.copy()
        if not self._visible:
            plotter.show()
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

    def _display_vector(self, obj, plotter: Union[BackgroundPlotter, pv.Plotter]):

        vector_field_data = DataExtractor(obj).fetch_data()
        field_info = obj._data_extractor.field_info()

        # surface ids
        surfaces_info = field_info.get_surfaces_info()
        surface_ids = [
            id
            for surf in map(
                obj._data_extractor.remote_surface_name, obj.surfaces_list()
            )
            for id in surfaces_info[surf]["surface_id"]
        ]

        # scalar bar properties
        scalar_bar_args = self._scalar_bar_default_properties()

        # field
        field = "velocity-magnitude"

        for surface_id, mesh_data in vector_field_data.items():
            mesh_data["vertices"].shape = mesh_data["vertices"].size // 3, 3
            mesh_data[obj.vectors_of()].shape = (
                mesh_data[obj.vectors_of()].size // 3,
                3,
            )
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
            mesh.cell_data["vectors"] = mesh_data[obj.vectors_of()]
            velocity_magnitude = np.linalg.norm(mesh_data[obj.vectors_of()], axis=1)
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

    def _display_contour(self, obj, plotter: Union[BackgroundPlotter, pv.Plotter]):
        # contour properties
        field = obj.field()
        range_option = obj.range.option()
        filled = obj.filled()
        contour_lines = obj.contour_lines()
        node_values = obj.node_values()
        boundary_values = obj.boundary_values()

        # scalar bar properties
        scalar_bar_args = self._scalar_bar_default_properties()
        surface_data, scalar_field_data = DataExtractor(obj).fetch_data()

        # loop over all meshes
        for surface_id, mesh_data in surface_data.items():
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
                mesh.point_data[field] = scalar_field_data[surface_id][field]
            else:
                mesh.cell_data[field] = scalar_field_data[surface_id][field]
            if range_option == "auto-range-off":
                auto_range_off = obj.range.auto_range_off
                if auto_range_off.clip_to_range():
                    if np.min(mesh[field]) < auto_range_off.maximum():
                        maximum_below = mesh.clip_scalar(
                            scalars=field,
                            value=auto_range_off.maximum(),
                        )
                        if np.max(maximum_below[field]) > auto_range_off.minimum():
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

                            if (not filled or contour_lines) and (
                                np.min(minimum_above[field])
                                != np.max(minimum_above[field])
                            ):
                                plotter.add_mesh(minimum_above.contour(isosurfaces=20))
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
                    if (not filled or contour_lines) and (
                        np.min(mesh[field]) != np.max(mesh[field])
                    ):
                        plotter.add_mesh(mesh.contour(isosurfaces=20))
            else:
                auto_range_on = obj.range.auto_range_on
                if auto_range_on.global_range():
                    if filled:
                        field_info = obj._data_extractor.field_info()
                        plotter.add_mesh(
                            mesh,
                            clim=field_info.get_range(field, False),
                            scalars=field,
                            show_edges=obj.show_edges(),
                            scalar_bar_args=scalar_bar_args,
                        )
                    if (not filled or contour_lines) and (
                        np.min(mesh[field]) != np.max(mesh[field])
                    ):
                        plotter.add_mesh(mesh.contour(isosurfaces=20))

                else:
                    if filled:
                        plotter.add_mesh(
                            mesh,
                            scalars=field,
                            show_edges=obj.show_edges(),
                            scalar_bar_args=scalar_bar_args,
                        )
                    if (not filled or contour_lines) and (
                        np.min(mesh[field]) != np.max(mesh[field])
                    ):
                        plotter.add_mesh(mesh.contour(isosurfaces=20))

    def _display_surface(self, obj, plotter: Union[BackgroundPlotter, pv.Plotter]):
        surface_api = obj._data_extractor.surface_api
        surface_api.create_surface_on_server()
        dummy_object = "dummy_object"
        post_session = obj._get_top_most_parent()
        if (
            obj.surface.type() == "iso-surface"
            and obj.surface.iso_surface.rendering() == "contour"
        ):
            contour = post_session.Contours[dummy_object]
            contour.field = obj.surface.iso_surface.field()
            contour.surfaces_list = [obj._name]
            contour.show_edges = True
            contour.range.auto_range_on.global_range = True
            self._display_contour(contour, plotter)
            del post_session.Contours[dummy_object]
        else:
            mesh = post_session.Meshes[dummy_object]
            mesh.surfaces_list = [obj._name]
            mesh.show_edges = True
            self._display_mesh(mesh, plotter)
            del post_session.Meshes[dummy_object]
        surface_api.delete_surface_on_server()

    def _display_mesh(self, obj, plotter: Union[BackgroundPlotter, pv.Plotter]):

        surfaces_data = DataExtractor(obj).fetch_data()
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
            plotter.add_mesh(mesh, show_edges=obj.show_edges(), color="lightgrey")

    def _get_refresh_for_plotter(self, window: "PyVistaWindow"):
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


class PyVistaWindowsManager(PostWindowsManager, metaclass=AbstractSingletonMeta):
    """Class for PyVista windows manager."""

    _condition = threading.Condition()

    def __init__(self):
        """Instantiate WindowManager for PyVista."""
        self._post_windows: Dict[str:PyVistaWindow] = {}
        self._plotter_thread: threading.Thread = None
        self._post_object: Union[GraphicsDefn, PlotDefn] = None
        self._window_id: str = None
        self._exit_thread: bool = False
        self._app = None

    def get_plotter(self, window_id: str) -> Union[BackgroundPlotter, pv.Plotter]:
        """Get PyVista Plotter.

        Parameters
        ----------
        window_id : str
            Window Id for plotter.

        Returns
        -------
        Union[BackgroundPlotter, pv.Plotter]
            PyVista Plotter.
        """
        with self._condition:
            return self._post_windows[window_id].plotter

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
        with self._condition:
            if not window_id:
                window_id = self._get_unique_window_id()
            if in_notebook() or get_config()["blocking"]:
                self._open_window_notebook(window_id)
            else:
                self._open_and_plot_console(None, window_id)
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
            raise RuntimeError("Object type currently not supported.")
        with self._condition:
            window = self._post_windows.get(window_id)
            if window:
                window.post_object = object

    def plot(
        self, object: Union[GraphicsDefn, PlotDefn], window_id: Optional[str] = None
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
            raise RuntimeError("Object type currently not supported.")
        with self._condition:
            if not window_id:
                window_id = self._get_unique_window_id()
            if in_notebook() or get_config()["blocking"]:
                self._plot_notebook(object, window_id)
            else:
                self._open_and_plot_console(object, window_id)

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
                if self._window_id:
                    window = self._post_windows.get(self._window_id)
                    plotter = window.plotter if window else None
                    animate = window.animate if window else False
                    if not plotter or plotter._closed:
                        window = PyVistaWindow(self._window_id, self._post_object)
                        plotter = window.plotter
                        self._app = plotter.app
                        plotter.add_callback(
                            window._get_refresh_for_plotter(window),
                            100,
                        )
                    window.post_object = self._post_object
                    window.animate = animate
                    window.update = True
                    self._post_windows[self._window_id] = window
                    self._post_object = None
                    self._window_id = None
            self._app.processEvents()
        with self._condition:
            for window in self._post_windows.values():
                plotter = window.plotter
                plotter.close()
                plotter.app.quit()
            self._post_windows.clear()
            self._condition.notify()

    def _open_and_plot_console(self, obj: object, window_id: str) -> None:
        if self._exit_thread:
            return
        with self._condition:
            self._window_id = window_id
            self._post_object = obj

        if not self._plotter_thread:
            if Session._monitor_thread:
                Session._monitor_thread.cbs.append(self._exit)
            self._plotter_thread = threading.Thread(target=self._display, args=())
            self._plotter_thread.start()

        with self._condition:
            self._condition.wait()

    def _open_window_notebook(self, window_id: str) -> pv.Plotter:
        window = self._post_windows.get(window_id)
        plotter = None
        if window and not window.close and window.refresh:
            window.refresh = False
        else:
            window = PyVistaWindow(window_id, None)
            self._post_windows[window_id] = window
        return window

    def _plot_notebook(self, obj: object, window_id: str) -> None:
        window = self._open_window_notebook(window_id)
        window.post_object = obj
        plotter = window.plotter
        window.plot()

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
                        or session_id == window.post_object._data_extractor.id()
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
