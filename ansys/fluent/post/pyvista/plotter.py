"""Module for graphics windows management."""
import itertools
import threading
from typing import List, Optional, Union
import numpy as np
import pyvista as pv
from pyvistaqt import BackgroundPlotter
from ansys.fluent.core.session import Session
from ansys.fluent.core.utils.generic import in_notebook

class Singleton(type):
    __instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super(Singleton, cls).__call__(
                *args, **kwargs
            )
        return cls.__instances[cls]


class _Plotter(metaclass=Singleton):
    """Class for graphics windows management."""

    _condition = threading.Condition()

    def __init__(self):
        self.__graphics = None
        self.__plotter_id = None
        self.__exit = False
        self.__plotter_thread = None
        self.__plotters = {}
        self.__app = None

    def open_window_in_notebook(
        self, plotter_id: Optional[str] = None
    ) -> None:
        """
        Open blank window in notebook.

        Parameters
        ----------
        plotter_id : str
            Plotter id.
        """
        if in_notebook():
            if not plotter_id:
                plotter_id = self._get_unique_plotter_id()
            self._open_window_notebook(plotter_id)
            return plotter_id

    def set_graphics(self, obj: object, plotter_id: str) -> None:
        """
        Associate graphics object with plotter instance.

        Parameters
        ----------
        plotter_id : str
            Plotter id.
        """
        plotter_data = self.__plotters.get(plotter_id)
        if plotter_data:
            plotter_data["graphics"] = obj

    def plot(self, obj: object, plotter_id: Optional[str] = None) -> None:
        """
        Plot graphics.

        Parameters
        ----------
        obj : object
            Graphics object to plot.

        plotter_id : Optional[str]
            Plotter id. If not specified unique id is used.
        """
        if not plotter_id:
            plotter_id = self._get_unique_plotter_id()
        if in_notebook():
            self._plot_notebook(obj, plotter_id)
        else:
            self._plot_console(obj, plotter_id)

    def refresh(
        self,
        session_id: Optional[str] = "",
        plotters_id: Optional[List[str]] = [],
    ):
        """
        Refresh graphics.

        Parameters
        ----------
        session_id : Optional[str]
           Session id to refresh. If specified, plotters which belong to
           specified session will be refreshed. Otherwise all plotters will
           be refreshed.

        plotters_id : Optional[List[str]]
            Plotters id to refresh. If not specified, all plotters will be
            refreshed.
        """
        with self._condition:
            plotters_id = self._get_plotters_id(session_id, plotters_id)
            for plotter_id in plotters_id:
                plotter_data = self.__plotters.get(plotter_id)
                if plotter_data:
                    plotter_data["refresh"] = True
                    self.plot(plotter_data["graphics"], plotter_id)

    def animate(
        self,
        session_id: Optional[str] = "",
        plotters_id: Optional[List[str]] = [],
    ):
        """
        Animate graphics.

        Parameters
        ----------
        session_id : Optional[str]
           Session id to animate. If specified, plotters which belong to
           specified session will be animated. Otherwise all plotters will
           be animated.

        plotters_id : Optional[List[str]]
            Plotters id to animate. If not specified, all plotters will be
            animated.
        """
        with self._condition:
            plotters_id = self._get_plotters_id(session_id, plotters_id)
            for plotter_id in plotters_id:
                plotter_data = self.__plotters.get(plotter_id)
                if plotter_data:
                    plotter_data["animate"] = True
                    plotter_data["plotter"].open_gif(f"{plotter_id}.gif")

    def close(
        self,
        session_id: Optional[str] = "",
        plotters_id: Optional[List[str]] = [],
    ):
        """
        Close plotters.

        Parameters
        ----------
        session_id : Optional[str]
           Session id to close. If specified, plotters which belong to
           specified session will be closed. Otherwise all plotters will
           be closed.

        plotters_id : Optional[List[str]]
            Plotters id to close. If not specified, all plotters will be
            closed.
        """
        with self._condition:
            plotters_id = self._get_plotters_id(session_id, plotters_id)
            for plotter_id in plotters_id:
                plotter_data = self.__plotters.get(plotter_id)
                if plotter_data:
                    if in_notebook():
                        plotter_data["plotter"].close()
                    plotter_data["close"] = True

    # private methods

    def _get_unique_plotter_id(self) -> str:
        itr_count = itertools.count()
        with self._condition:
            while True:
                plotter_id = f"plotter-{next(itr_count)}"
                if plotter_id not in self.__plotters:
                    return plotter_id

    def _plot_console(self, obj: object, plotter_id: str) -> None:
        if self.__exit:
            return
        with self._condition:
            self.__plotter_id = plotter_id
            self.__graphics = obj

        if not self.__plotter_thread:
            Session._monitor_thread.cbs.append(self._exit)
            self.__plotter_thread = threading.Thread(
                target=self._display, args=()
            )
            self.__plotter_thread.start()

        with self._condition:
            self._condition.wait()

    def _open_window_notebook(self, plotter_id: str) -> pv.Plotter:
        plotter_data = self.__plotters.get(plotter_id)
        plotter = None
        if (
            plotter_data
            and not plotter_data["close"]
            and plotter_data["refresh"]
        ):
            plotter_data["refresh"] = False
        else:
            plotter = pv.Plotter()
            plotter_data = {
                "plotter": plotter,
                "animate": False,
                "close": False,
                "refresh": False,
            }
            self.__plotters[plotter_id] = plotter_data
            self._init_properties(plotter)
            plotter.show()
        return plotter_data

    def _plot_notebook(self, obj: object, plotter_id: str) -> None:
        plotter_data = self._open_window_notebook(plotter_id)
        self.set_graphics(obj, plotter_id)
        plotter = plotter_data["plotter"]
        plotter.clear()
        camera = plotter.camera.copy()
        self._display_object(obj, plotter)
        plotter.camera = camera.copy()
        if plotter_data["animate"]:
            plotter.write_frame()

    def _get_plotters_id(
        self,
        session_id: Optional[str] = "",
        plotters_id: Optional[List[str]] = [],
    ) -> List[str]:
        with self._condition:
            return [
                plotter_id
                for plotter_id in [
                    plotter_id
                    for plotter_id, plotter_data in self.__plotters.items()
                    if not plotter_data["plotter"]._closed
                    and (
                        not session_id
                        or session_id
                        == plotter_data["graphics"].parent.parent.session.id
                    )
                ]
                if not plotters_id or plotter_id in plotters_id
            ]

    def _exit(self) -> None:
        if self.__plotter_thread:
            with self._condition:
                self.__exit = True
                self._condition.wait()
            self.__plotter_thread.join()
            self.__plotter_thread = None

    def _init_properties(self, active_plotter):
        active_plotter.theme.cmap = "jet"
        active_plotter.background_color = "white"
        active_plotter.theme.font.color = "black"

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

    def _display(self) -> None:

        while True:
            with self._condition:
                if self.__exit:
                    break
                if self.__graphics and self.__plotter_id:
                    plotter_data = self.__plotters.get(self.__plotter_id, {})

                    active_plotter = plotter_data.get("plotter")
                    animate = plotter_data.get("animate", False)
                    if not active_plotter or active_plotter._closed:
                        active_plotter = BackgroundPlotter(
                            title=f"PyFluent ({self.__plotter_id})"
                        )
                        self.__app = active_plotter.app
                        self._init_properties(active_plotter)
                        active_plotter.add_callback(
                            self._get_refresh_for_plotter(self.__plotter_id),
                            100,
                        )
                    self.__plotters[self.__plotter_id] = {
                        "plotter": active_plotter,
                        "graphics": self.__graphics,
                        "update": True,
                        "close": False,
                        "animate": animate,
                    }
            self.__app.processEvents()
        with self._condition:
            for plotter_data in self.__plotters.values():
                plotter = plotter_data["plotter"]
                plotter.close()
                plotter.app.quit()
            self.__plotters.clear()
            self._condition.notify()

    def _display_vector(
        self, obj, plotter: Union[BackgroundPlotter, pv.Plotter]
    ):

        if not obj.surfaces_list():
            raise RuntimeError("Vector definition is incomplete.")

        field_data = obj.parent.parent.session.field_data

        # surface ids
        surfaces_info = field_data.get_surfaces_info()
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
            if obj.range_option.range_option() == "auto-range-off":
                auto_range_off = obj.range_option.auto_range_off
                range = [auto_range_off.minimum(), auto_range_off.maximum()]
                if auto_range_off.clip_to_range():
                    velocity_magnitude = np.ma.masked_outside(
                        velocity_magnitude,
                        auto_range_off.minimum(),
                        auto_range_off.maximum(),
                    ).filled(fill_value=0)
            else:
                auto_range_on = obj.range_option.auto_range_on
                if auto_range_on.global_range():
                    range = field_data.get_range(field, False)
                else:
                    range = field_data.get_range(field, False, surface_ids)

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
        range_option = obj.range_option.range_option()
        filled = obj.filled()
        contour_lines = obj.contour_lines()
        node_values = obj.node_values()
        boundary_values = obj.boundary_values()

        # scalar bar properties
        scalar_bar_args = self._scalar_bar_default_properties()

        field_data = obj.parent.parent.session.field_data
        surfaces_info = field_data.get_surfaces_info()
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
                auto_range_off = obj.range_option.auto_range_off
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

                            if (not filled or contour_lines) and (
                                np.min(minimum_above[field])
                                != np.max(minimum_above[field])
                            ):
                                plotter.add_mesh(
                                    minimum_above.contour(isosurfaces=20)
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
                    if (not filled or contour_lines) and (
                        np.min(mesh[field]) != np.max(mesh[field])
                    ):
                        plotter.add_mesh(mesh.contour(isosurfaces=20))
            else:
                auto_range_on = obj.range_option.auto_range_on
                if auto_range_on.global_range():
                    if filled:
                        plotter.add_mesh(
                            mesh,
                            clim=field_data.get_range(field, False),
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

    def _display_iso_surface(
        self, obj, plotter: Union[BackgroundPlotter, pv.Plotter]
    ):
        field = obj.surface_type.iso_surface.field()
        if not field:
            raise RuntimeError("Iso surface definition is incomplete.")

        dummy_surface_name = "_dummy_iso_surface_for_pyfluent"
        field_data = obj.parent.parent.session.field_data
        surfaces_list = list(field_data.get_surfaces_info().keys())
        iso_value = obj.surface_type.iso_surface.iso_value()
        if dummy_surface_name in surfaces_list:
            obj.parent.parent.session.tui.solver.surface.delete_surface(
                dummy_surface_name
            )

        obj.parent.parent.session.tui.solver.surface.iso_surface(
            field, dummy_surface_name, (), (), iso_value, ()
        )

        surfaces_list = list(field_data.get_surfaces_info().keys())
        if not dummy_surface_name in surfaces_list:
            raise RuntimeError("Iso surface creation failed.")
        graphics_session = obj.parent.parent
        if obj.surface_type.iso_surface.rendering() == "mesh":
            mesh = graphics_session.Meshes[dummy_surface_name]
            mesh.surfaces_list = [dummy_surface_name]
            mesh.show_edges = True
            self._display_mesh(mesh, plotter)
            del graphics_session.Meshes[dummy_surface_name]
        else:
            contour = graphics_session.Contours[dummy_surface_name]
            contour.field = obj.surface_type.iso_surface.field()
            contour.surfaces_list = [dummy_surface_name]
            contour.show_edges = True
            contour.range_option.auto_range_on.global_range = True
            self._display_contour(contour, plotter)
            del graphics_session.Contours[dummy_surface_name]
        obj.parent.parent.session.tui.solver.surface.delete_surface(
            dummy_surface_name
        )

    def _display_mesh(
        self, obj, plotter: Union[BackgroundPlotter, pv.Plotter]
    ):
        if not obj.surfaces_list():
            raise RuntimeError("Mesh definition is incomplete.")
        field_data = obj.parent.parent.session.field_data
        surfaces_info = field_data.get_surfaces_info()
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

    def _display_object(
        self, obj, plotter: Union[BackgroundPlotter, pv.Plotter]
    ):
        if obj.__class__.__name__ == "Mesh":
            self._display_mesh(obj, plotter)
        elif obj.__class__.__name__ == "Surface":
            if obj.surface_type.surface_type() == "iso-surface":
                self._display_iso_surface(obj, plotter)
        elif obj.__class__.__name__ == "Contour":
            self._display_contour(obj, plotter)
        elif obj.__class__.__name__ == "Vector":
            self._display_vector(obj, plotter)

    def _get_refresh_for_plotter(self, plotter_id: str):
        def refresh():

            with self._condition:
                plotter_data = self.__plotters[plotter_id]
                plotter = plotter_data["plotter"]
                close_plotter = plotter_data["close"]
                if close_plotter:
                    plotter_data["animate"] = False
                    plotter.close()
                    return
                update_plotter = plotter_data["update"]
                if not update_plotter:
                    return
                obj = plotter_data["graphics"]
                plotter.clear()

                plotter_data["update"] = False
                self.__graphics = None
                camera = plotter.camera.copy()
                try:
                    self._display_object(obj, plotter)
                    if plotter_data["animate"]:
                        plotter.write_frame()
                finally:
                    self._condition.notify()
                plotter.camera = camera.copy()

        return refresh


plotter = _Plotter()
