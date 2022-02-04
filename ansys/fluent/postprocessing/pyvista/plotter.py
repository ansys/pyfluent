import sys
import threading
#import signal
from typing import Optional
import numpy as np
from pyvistaqt import BackgroundPlotter
import pyvista as pv


class Singleton(type):
    __instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super(Singleton, cls).__call__(
                *args, **kwargs
            )
        return cls.__instances[cls]


class _Plotter(metaclass=Singleton):
    """
    Plot the graphics object.

    Properties
    ----------
    background_plotter
        BackgroundPlotter to plot graphics.

    Methods
    -------
    plot_graphics(obj, plotter_id: str)
        Plot graphics.
    """

    __condition = threading.Condition()

    def __init__(self):
        self.__exit = False
        self.__active_plotter = None
        self.__graphics = {}
        self.__plotter_thread = None
        self.__plotters = {}

    def plot_graphics(
        self, obj: object, plotter_id: Optional[str] = None
    ) -> None:
        if self.__exit:
            return
        if not plotter_id:
            plotter_id = obj.session.id
        with self.__condition:
            self.__graphics[plotter_id] = obj
            self.__active_plotter = self.__plotters.get(plotter_id)

        if not self.__plotter_thread:
            self.__plotter_thread = threading.Thread(
                target=self._display, args=(), daemon=True
            )
            self.__plotter_thread.start()

        with self.__condition:
            self.__condition.wait()
            self.__plotters[plotter_id] = self.__active_plotter

    # private methods

    def _exit(self) -> None:
        if self.__plotter_thread:
            with self.__condition:
                self.__exit = True
                self.__condition.wait()
            self.__plotter_thread.join()
            self.__plotter_thread = None

    def _init_properties(self):
        self.__active_plotter.theme.cmap = "jet"
        self.__active_plotter.background_color = "white"
        self.__active_plotter.theme.font.color = "black"

    def _display(self):
        while True:
            with self.__condition:
                if self.__exit:
                    break
                if (
                    not self.__active_plotter or self.__active_plotter._closed
                ) and len(self.__graphics) > 0:
                    plotter_id = next(iter(self.__graphics))
                    self.__active_plotter = BackgroundPlotter(
                        title=f"PyFluent ({plotter_id})"
                    )
                    self._init_properties()
                    self.__active_plotter.add_callback(
                        self._get_refresh_for_plotter(plotter_id),
                        100,
                    )
            self.__active_plotter.app.processEvents()
        with self.__condition:
            for plotter in self.__plotters.values():
                plotter.close()
            self.__active_plotter.app.quit()
            self.__active_plotter = None
            self.__plotters.clear()
            self.__condition.notify()

    def _display_contour(self, obj):
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
        scalar_bar_args = dict(
            title_font_size=20,
            label_font_size=16,
            shadow=True,
            fmt="%.6e",
            font_family="arial",
            vertical=True,
            position_x=0.06,
            position_y=0.3,
        )

        field_data = obj.session.field_data
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
        meta_data = None
        plotter = self.__active_plotter

        # loop over all meshes
        for mesh_data in scalar_field_data:

            topology = "line" if mesh_data["faces"][0][0] == 2 else "face"
            if topology == "line":
                mesh = pv.PolyData(
                    np.array(mesh_data["vertices"]),
                    lines=np.hstack(mesh_data["faces"]),
                )
            else:
                mesh = pv.PolyData(
                    np.array(mesh_data["vertices"]),
                    faces=np.hstack(mesh_data["faces"]),
                )
            if node_values:
                mesh.point_data[field] = np.array(mesh_data["scalar_field"])
            else:
                mesh.cell_data[field] = np.array(mesh_data["scalar_field"])
            if not meta_data:
                meta_data = mesh_data["meta_data"]

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
                            clim=[
                                meta_data.scalarFieldrange.globalmin,
                                meta_data.scalarFieldrange.globalmax,
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

    def _display_iso_surface(self, obj):
        field = obj.surface_type.iso_surface.field()
        if not field:
            raise RuntimeError("Iso surface definition is incomplete.")

        dummy_surface_name = "_dummy_iso_surface_for_pyfluent"
        surfaces_list = list(obj.session.field_data.get_surfaces_info().keys())
        iso_value = obj.surface_type.iso_surface.iso_value()
        if dummy_surface_name in surfaces_list:
            obj.session.tui.solver.surface.delete_surface(dummy_surface_name)

        obj.session.tui.solver.surface.iso_surface(
            field, dummy_surface_name, (), (), iso_value, ()
        )

        from ansys.fluent.postprocessing.pyvista.graphics import Graphics

        surfaces_list = list(obj.session.field_data.get_surfaces_info().keys())
        if not dummy_surface_name in surfaces_list:
            raise RuntimeError("Iso surface creation failed.")
        graphics_session = Graphics(obj.session)
        if obj.surface_type.iso_surface.rendering() == "mesh":
            mesh = graphics_session.Meshes[dummy_surface_name]
            mesh.surfaces_list = [dummy_surface_name]
            mesh.show_edges = True
            self._display_mesh(mesh)
            del graphics_session.Meshes[dummy_surface_name]
        else:
            contour = graphics_session.Contours[dummy_surface_name]
            contour.field = obj.surface_type.iso_surface.field()
            contour.surfaces_list = [dummy_surface_name]
            contour.show_edges = True
            contour.range_option.auto_range_on.global_range = True
            self._display_contour(contour)
            del graphics_session.Contours[dummy_surface_name]
        obj.session.tui.solver.surface.delete_surface(dummy_surface_name)

    def _display_mesh(self, obj):
        if not obj.surfaces_list():
            raise RuntimeError("Mesh definition is incomplete.")
        field_data = obj.session.field_data
        surfaces_info = field_data.get_surfaces_info()
        surface_ids = [
            id
            for surf in obj.surfaces_list()
            for id in surfaces_info[surf]["surface_id"]
        ]
        surfaces_data = field_data.get_surfaces(surface_ids)
        for mesh_data in surfaces_data:
            topology = "line" if mesh_data["faces"][0][0] == 2 else "face"
            if topology == "line":
                mesh = pv.PolyData(
                    np.array(mesh_data["vertices"]),
                    lines=np.hstack(mesh_data["faces"]),
                )
            else:
                mesh = pv.PolyData(
                    np.array(mesh_data["vertices"]),
                    faces=np.hstack(mesh_data["faces"]),
                )
            self.__active_plotter.add_mesh(
                mesh, show_edges=obj.show_edges(), color="lightgrey"
            )

    def _get_refresh_for_plotter(self, plotter_id: str):
        def refresh():
            with self.__condition:
                obj = self.__graphics.get(plotter_id)
                if not obj:
                    self.__condition.notify()
                    return

                del self.__graphics[plotter_id]
                plotter = self.__active_plotter
                plotter.clear()

                camera = plotter.camera.copy()

                if obj.__class__.__name__ == "Mesh":
                    self._display_mesh(obj)
                elif obj.__class__.__name__ == "Surface":
                    if obj.surface_type.surface_type() == "iso-surface":
                        self._display_iso_surface(obj)
                elif obj.__class__.__name__ == "Contour":
                    self._display_contour(obj)

                plotter.camera = camera.copy()
                self.__condition.notify()

        return refresh


plotter = _Plotter()


def signal_handler(sig, frame):
    plotter._exit()
    sys.exit(0)


# Need to associate ctrl+z signal
# signal.signal(signal.SIGINT, signal_handler)
