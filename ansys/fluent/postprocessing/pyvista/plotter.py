import numpy as np
import pyvista as pv
from ansys.fluent.core.core import FieldData
from pyvistaqt import BackgroundPlotter
import threading, copy


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
    Plots the graphics.

    Properties
    ----------
    background_plotter
        BackgroundPlotter to plot graphics

    Methods
    -------
    set_graphics(obj)
        sets the graphics to be plotted.

    close(obj)
        closes the background_plotter.
    """

    __lock = threading.Lock()

    def __init__(self):
        self.__exit = False
        self.__background_plotter = None
        self.__graphics = None
        self.__plotted_graphics_properties = None

    @property
    def background_plotter(self):
        return self.__background_plotter

    def close(self) -> None:
        with self.__lock:
            self.__exit = True

    def set_graphics(self, obj: object) -> None:
        background_plotter = None
        with self.__lock:
            self.__graphics = obj
            background_plotter = self.__background_plotter

        if not background_plotter:
            thread = threading.Thread(target=self._display, args=())
            thread.start()

    # private methods
    def _init_properties(self):
        self.__background_plotter.theme.cmap = "jet"
        self.__background_plotter.background_color = "white"
        self.__background_plotter.theme.font.color = "black"

    def _display(self):
        self.__background_plotter = BackgroundPlotter(title="PyFluent")
        self._init_properties()
        self.refresh()
        self.__background_plotter.add_callback(self.refresh, 100)
        self.__background_plotter.app.exec_()

    def _display_contour(self, obj):
        if not obj.surfaces_list() or not obj.field():
            return

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

        field_data = FieldData(obj.session.field_service)
        surfaces_info = field_data.get_surfaces_info()
        surface_ids = [
            id
            for surf in obj.surfaces_list()
            for id in surfaces_info.get(surf, {}).get("surface_id", [])
        ]
        # get scalar field data
        scalar_field_data = field_data.get_scalar_field(
            surface_ids,
            field,
            node_values,
            boundary_values,
        )
        meta_data = None
        plotter = self.__background_plotter

        # loop over all meshes
        for mesh_data in scalar_field_data:
            try:

                topology = (
                    "line" if mesh_data["faces"][0][0] == 2 else "face"
                )
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
                    mesh.point_data[field] = np.array(
                        mesh_data["scalar_field"]
                    )
                else:
                    mesh.cell_data[field] = np.array(
                        mesh_data["scalar_field"]
                    )
                if not meta_data:
                    meta_data = mesh_data["meta_data"]

                if range_option == "auto-range-off":
                    auto_range_off = obj.range_option.auto_range_off
                    if auto_range_off.clip_to_range():
                        if (
                            np.min(mesh[field])
                            < auto_range_off.maximum()
                        ):
                            maximum_below = mesh.clip_scalar(
                                scalars=field,
                                value=auto_range_off.maximum(),
                            )
                            if (
                                np.max(maximum_below[field])
                                > auto_range_off.minimum()
                            ):
                                minimum_above = (
                                    maximum_below.clip_scalar(
                                        scalars=field,
                                        invert=False,
                                        value=auto_range_off.minimum(),
                                    )
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
                                        minimum_above.contour(
                                            isosurfaces=20
                                        )
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
                            plotter.add_mesh(
                                mesh.contour(isosurfaces=20)
                            )
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
                            plotter.add_mesh(
                                mesh.contour(isosurfaces=20)
                            )

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
                            plotter.add_mesh(
                                mesh.contour(isosurfaces=20)
                            )
            except Exception as e:
                print(e)
                pass

    def _display_iso_surface(self, obj):
        field = obj.surface_type.iso_surface.field()
        if not field:
            return

        surfaces_list = list(
            FieldData(obj.session.field_service)
            .get_surfaces_info()
            .keys()
        )
        iso_value = obj.surface_type.iso_surface.iso_value()
        if "dummy" in surfaces_list:
            obj.session.tui.surface.edit_surface(
                "dummy",
                obj.surface_type.iso_surface.field(),
                "dummy",
                (),
                (),
                obj.surface_type.iso_surface.iso_value(),
                (),
            )
        else:
            obj.session.tui.surface.iso_surface(
                field, "dummy", (), (), iso_value, ()
            )

        from ansys.fluent.postprocessing.pyvista.graphics import (
            Graphics,
        )

        surfaces_list = list(
            FieldData(obj.session.field_service)
            .get_surfaces_info()
            .keys()
        )
        if not "dummy" in surfaces_list:
            raise RuntimeError(f"Iso surface creation failed.")
        graphics_session = Graphics(obj.session)
        if obj.surface_type.iso_surface.rendering() == "mesh":
            mesh = graphics_session.mesh["dummy"]
            mesh.surfaces_list = ["dummy"]
            mesh.show_edges = True
            self._display_mesh(mesh)
            del graphics_session.mesh["dummy"]
        else:
            cont = graphics_session.contour["dummy"]
            cont.field = obj.surface_type.iso_surface.field()
            cont.surfaces_list = ["dummy"]
            cont.show_edges = True
            cont.range_option.auto_range_on.global_range = True
            self._display_contour(cont)
            del graphics_session.contour["dummy"]
        obj.session.tui.surface.delete_surface("dummy")

    def _display_mesh(self, obj):
        if not obj.surfaces_list():
            return
        field_data = FieldData(obj.session.field_service)
        surfaces_info = field_data.get_surfaces_info()
        surface_ids = [
            id
            for surf in obj.surfaces_list()
            for id in surfaces_info.get(surf, {}).get("surface_id", [])
        ]
        surfaces_data = field_data.get_surfaces(surface_ids)
        for mesh_data in surfaces_data:
            topology = (
                "line" if mesh_data["faces"][0][0] == 2 else "face"
            )
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
            self.__background_plotter.add_mesh(
                mesh, show_edges=obj.show_edges(), color="lightgrey"
            )

    def refresh(self):
        with self.__lock:
            obj = self.__graphics
            if not obj:
                return
            if self.__exit:
                self.__background_plotter.close()
                return
            if self.__plotted_graphics_properties == obj():
                return

            self.__plotted_graphics_properties = copy.deepcopy(obj())
            plotter = self.__background_plotter
            plotter.clear()

            camera = plotter.camera.copy()

            if obj.__class__.__name__ == "mesh":
                self._display_mesh(obj)
            elif obj.__class__.__name__ == "surface":
                if obj.surface_type.surface_type() == "iso-surface":
                    self._display_iso_surface(obj)
            elif obj.__class__.__name__ == "contour":
                self._display_contour(obj)

            plotter.camera = camera.copy()


plotter = _Plotter()
