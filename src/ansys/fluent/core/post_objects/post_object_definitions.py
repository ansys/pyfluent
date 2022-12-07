"""Module providing visualization objects definition."""
from abc import abstractmethod
from typing import List, NamedTuple, Optional
import warnings

from ansys.fluent.core.meta import (
    Attribute,
    PyLocalNamedObjectMetaAbstract,
    PyLocalObjectMeta,
    PyLocalPropertyMeta,
)


class BasePostObjectDefn:
    """Base class for visualization objects."""

    def _pre_display(self):
        local_surfaces_provider = self._get_top_most_parent()._local_surfaces_provider()
        for surf_name in self.surfaces_list():
            if surf_name in list(local_surfaces_provider):
                surf_obj = local_surfaces_provider[surf_name]
                surf_api = surf_obj._api_helper.surface_api
                surf_api.create_surface_on_server()

    def _post_display(self):
        local_surfaces_provider = self._get_top_most_parent()._local_surfaces_provider()
        for surf_name in self.surfaces_list():
            if surf_name in list(local_surfaces_provider):
                surf_obj = local_surfaces_provider[surf_name]
                surf_api = surf_obj._api_helper.surface_api
                surf_api.delete_surface_on_server()


class GraphicsDefn(BasePostObjectDefn, metaclass=PyLocalNamedObjectMetaAbstract):
    """Abstract base class for graphics objects."""

    @abstractmethod
    def display(self, plotter_id: Optional[str] = None):
        """Display graphics.

        Parameters
        ----------
        window_id : str, optional
            Window id. If not specified unique id is used.
        """
        pass


class PlotDefn(BasePostObjectDefn, metaclass=PyLocalNamedObjectMetaAbstract):
    """Abstract base class for plot objects."""

    @abstractmethod
    def plot(self, plotter_id: Optional[str] = None):
        """Draw plot.

        Parameters
        ----------
        window_id : str, optional
            Window id. If not specified unique id is used.
        """
        pass


class Vector(NamedTuple):
    """Class for vector definition."""

    x: float
    y: float
    z: float


class MonitorDefn(PlotDefn):
    """Monitor Definition."""

    PLURAL = "Monitors"

    class monitor_set_name(metaclass=PyLocalPropertyMeta):
        """Monitor set name."""

        value: str

        @Attribute
        def allowed_values(self):
            """Monitor set allowed values."""
            return self._api_helper.monitors_manager().get_monitor_set_names()


class XYPlotDefn(PlotDefn):
    """XYPlot Definition."""

    PLURAL = "XYPlots"

    class node_values(metaclass=PyLocalPropertyMeta):
        """Plot nodal values."""

        value: bool = True

    class boundary_values(metaclass=PyLocalPropertyMeta):
        """Plot Boundary values."""

        value: bool = True

    class direction_vector(metaclass=PyLocalPropertyMeta):
        """Direction Vector."""

        value: Vector = [1, 0, 0]

    class y_axis_function(metaclass=PyLocalPropertyMeta):
        """Y Axis Function."""

        value: str

        @Attribute
        def allowed_values(self):
            """Y axis function allowed values."""
            return list(self._api_helper.field_info().get_fields_info())

    class x_axis_function(metaclass=PyLocalPropertyMeta):
        """X Axis Function."""

        value: str = "direction-vector"

        @Attribute
        def allowed_values(self):
            """X axis function allowed values."""
            return ["direction-vector"]

    class surfaces_list(metaclass=PyLocalPropertyMeta):
        """List of surfaces for plotting."""

        value: List[str]

        @Attribute
        def allowed_values(self):
            """Surface list allowed values."""
            return list(
                self._api_helper.field_info().get_surfaces_info().keys()
            ) + list(self._get_top_most_parent()._local_surfaces_provider())


class MeshDefn(GraphicsDefn):
    """Mesh graphics definition."""

    PLURAL = "Meshes"

    class surfaces_list(metaclass=PyLocalPropertyMeta):
        """List of surfaces for mesh graphics."""

        value: List[str]

        @Attribute
        def allowed_values(self):
            """Surface list allowed values."""
            return list(
                (self._api_helper.field_info().get_surfaces_info().keys())
            ) + list(self._get_top_most_parent()._local_surfaces_provider())

    class show_edges(metaclass=PyLocalPropertyMeta):
        """Show edges for mesh."""

        value: bool = False


class PathlinesDefn(GraphicsDefn):
    """Pathlines definition."""

    PLURAL = "Pathlines"

    class field(metaclass=PyLocalPropertyMeta):
        """Pathlines field."""

        value: str

        @Attribute
        def allowed_values(self):
            """Field allowed values."""
            return list(self._api_helper.field_info().get_fields_info())

    class surfaces_list(metaclass=PyLocalPropertyMeta):
        """List of surfaces for pathlines."""

        value: List[str]

        @Attribute
        def allowed_values(self):
            """Surface list allowed values."""
            return list(
                (self._api_helper.field_info().get_surfaces_info().keys())
            ) + list(self._get_top_most_parent()._local_surfaces_provider())


class SurfaceDefn(GraphicsDefn):
    """Surface graphics definition."""

    PLURAL = "Surfaces"

    class show_edges(metaclass=PyLocalPropertyMeta):
        """Show edges for surface."""

        value: bool = True

    class definition(metaclass=PyLocalObjectMeta):
        """Specify surface definition type."""

        def _availability(self, name):
            if name == "plane_surface":
                return self.type() == "plane-surface"
            if name == "iso_surface":
                return self.type() == "iso-surface"
            return True

        class type(metaclass=PyLocalPropertyMeta):
            """Surface type."""

            value: str = "iso-surface"

            @Attribute
            def allowed_values(self):
                """Surface type allowed values."""
                return ["plane-surface", "iso-surface"]

        class plane_surface(metaclass=PyLocalObjectMeta):
            """Plane surface definition."""

            def _availability(self, name):
                if name == "xy_plane":
                    return self.creation_method() == "xy-plane"
                if name == "yz_plane":
                    return self.creation_method() == "yz-plane"
                if name == "zx_plane":
                    return self.creation_method() == "zx-plane"
                return True

            class creation_method(metaclass=PyLocalPropertyMeta):
                """Creation Method."""

                value: str = "xy-plane"

                @Attribute
                def allowed_values(self):
                    """Surface type allowed values."""
                    return ["xy-plane", "yz-plane", "zx-plane"]

            class xy_plane(metaclass=PyLocalObjectMeta):
                """XY Plane definition."""

                class z(metaclass=PyLocalPropertyMeta):
                    """Z value."""

                    value: float = 0

                    @Attribute
                    def range(self):
                        """Z value range."""
                        return self._api_helper.field_info().get_range(
                            "z-coordinate", True
                        )

            class yz_plane(metaclass=PyLocalObjectMeta):
                """YZ Plane definition."""

                class x(metaclass=PyLocalPropertyMeta):
                    """X value."""

                    value: float = 0

                    @Attribute
                    def range(self):
                        """X value range."""
                        return self._api_helper.field_info().get_range(
                            "x-coordinate", True
                        )

            class zx_plane(metaclass=PyLocalObjectMeta):
                """ZX Plane definition."""

                class y(metaclass=PyLocalPropertyMeta):
                    """Y value."""

                    value: float = 0

                    @Attribute
                    def range(self):
                        """Y value range."""
                        return self._api_helper.field_info().get_range(
                            "y-coordinate", True
                        )

        class iso_surface(metaclass=PyLocalObjectMeta):
            """Iso surface definition."""

            class field(metaclass=PyLocalPropertyMeta):
                """Iso surface field."""

                value: str

                @Attribute
                def allowed_values(self):
                    """Field allowed values."""
                    return list(self._api_helper.field_info().get_fields_info())

            class rendering(metaclass=PyLocalPropertyMeta):
                """Iso surface rendering."""

                value: str = "mesh"

                @Attribute
                def allowed_values(self):
                    """Surface rendering allowed values."""
                    return ["mesh", "contour"]

            class iso_value(metaclass=PyLocalPropertyMeta):
                """Iso value for field."""

                _value: float

                def _reset_on_change(self):
                    return [self._parent.field]

                @property
                def value(self):
                    """Iso value property setter."""
                    if getattr(self, "_value", None) is None:
                        range = self.range
                        self._value = (range[0] + range[1]) / 2.0 if range else None
                    return self._value

                @value.setter
                def value(self, value):
                    self._value = value

                @Attribute
                def range(self):
                    """Iso value range."""
                    field = self._parent.field()
                    if field:
                        return self._api_helper.field_info().get_range(field, True)


class ContourDefn(GraphicsDefn):
    """Contour graphics definition."""

    PLURAL = "Contours"

    class field(metaclass=PyLocalPropertyMeta):
        """Contour field."""

        value: str

        @Attribute
        def allowed_values(self):
            """Field allowed values."""
            return list(self._api_helper.field_info().get_fields_info())

    class surfaces_list(metaclass=PyLocalPropertyMeta):
        """Contour surfaces."""

        value: List[str]

        @Attribute
        def allowed_values(self):
            """Surfaces list allowed values."""
            return list(
                self._api_helper.field_info().get_surfaces_info().keys()
            ) + list(self._get_top_most_parent()._local_surfaces_provider())

    class filled(metaclass=PyLocalPropertyMeta):
        """Draw filled contour."""

        value: bool = True

    class node_values(metaclass=PyLocalPropertyMeta):
        """Draw nodal data."""

        _value: bool = True

        @property
        def value(self):
            """Node value property setter."""
            filled = self._get_parent_by_type(ContourDefn).filled()
            auto_range_off = self._get_parent_by_type(ContourDefn).range.auto_range_off
            if not filled or (auto_range_off and auto_range_off.clip_to_range()):
                warnings.warn(
                    "For unfilled and clipped contours node values are diaplyed."
                )
                self._value = True
            return self._value

        @value.setter
        def value(self, value):
            self._value = value

    class boundary_values(metaclass=PyLocalPropertyMeta):
        """Draw boundary values."""

        value: bool = False

    class contour_lines(metaclass=PyLocalPropertyMeta):
        """Draw contour lines."""

        value: bool = False

    class show_edges(metaclass=PyLocalPropertyMeta):
        """Show edges."""

        value: bool = False

    class range(metaclass=PyLocalObjectMeta):
        """Range definition."""

        def _availability(self, name):
            if name == "auto_range_on":
                return self.option() == "auto-range-on"
            if name == "auto_range_off":
                return self.option() == "auto-range-off"
            return True

        class option(metaclass=PyLocalPropertyMeta):
            """Range option."""

            value: str = "auto-range-on"

            @Attribute
            def allowed_values(self):
                """Range option allowed values."""
                return ["auto-range-on", "auto-range-off"]

        class auto_range_on(metaclass=PyLocalObjectMeta):
            """Auto range on definition."""

            class global_range(metaclass=PyLocalPropertyMeta):
                """Show global range."""

                value: bool = False

        class auto_range_off(metaclass=PyLocalObjectMeta):
            """Auto range off definition."""

            class clip_to_range(metaclass=PyLocalPropertyMeta):
                """Clip contour within range."""

                value: bool = False

            class minimum(metaclass=PyLocalPropertyMeta):
                """Range minimum."""

                _value: float

                def _reset_on_change(self):
                    return [
                        self._get_parent_by_type(ContourDefn).field,
                        self._get_parent_by_type(ContourDefn).node_values,
                    ]

                @property
                def value(self):
                    """Range minimum property setter."""
                    if getattr(self, "_value", None) is None:
                        field = self._get_parent_by_type(ContourDefn).field()
                        if field:
                            field_info = self._api_helper.field_info()
                            field_range = field_info.get_range(
                                field,
                                self._get_parent_by_type(ContourDefn).node_values(),
                            )
                            self._value = field_range[0]
                    return self._value

                @value.setter
                def value(self, value):
                    self._value = value

            class maximum(metaclass=PyLocalPropertyMeta):
                """Range maximum."""

                _value: float

                def _reset_on_change(self):
                    return [
                        self._get_parent_by_type(ContourDefn).field,
                        self._get_parent_by_type(ContourDefn).node_values,
                    ]

                @property
                def value(self):
                    """Range maximum property setter."""
                    if getattr(self, "_value", None) is None:
                        field = self._get_parent_by_type(ContourDefn).field()
                        if field:
                            field_info = self._api_helper.field_info()
                            field_range = field_info.get_range(
                                field,
                                self._get_parent_by_type(ContourDefn).node_values(),
                            )
                            self._value = field_range[1]

                    return self._value

                @value.setter
                def value(self, value):
                    self._value = value


class VectorDefn(GraphicsDefn):
    """Vector graphics definition."""

    PLURAL = "Vectors"

    class vectors_of(metaclass=PyLocalPropertyMeta):
        """Vector type."""

        value: str = "velocity"

        @Attribute
        def allowed_values(self):
            """Vectors of allowed values."""
            return list(self._api_helper.get_vector_fields())

    class field(metaclass=PyLocalPropertyMeta):
        """Vector color field."""

        value: str

        @Attribute
        def allowed_values(self):
            """Field allowed values."""
            return list(self._api_helper.field_info().get_fields_info())

    class surfaces_list(metaclass=PyLocalPropertyMeta):
        """List of surfaces for vector graphics."""

        value: List[str]

        @Attribute
        def allowed_values(self):
            """Surface list allowed values."""
            return list(
                self._api_helper.field_info().get_surfaces_info().keys()
            ) + list(self._get_top_most_parent()._local_surfaces_provider())

    class scale(metaclass=PyLocalPropertyMeta):
        """Vector scale."""

        value: float = 1.0

    class skip(metaclass=PyLocalPropertyMeta):
        """Vector skip."""

        value: int = 0

    class show_edges(metaclass=PyLocalPropertyMeta):
        """Show edges."""

        value: bool = False

    class range(metaclass=PyLocalObjectMeta):
        """Range definition."""

        def _availability(self, name):
            if name == "auto_range_on":
                return self.option() == "auto-range-on"
            if name == "auto_range_off":
                return self.option() == "auto-range-off"
            return True

        class option(metaclass=PyLocalPropertyMeta):
            """Range option."""

            value: str = "auto-range-on"

            @Attribute
            def allowed_values(self):
                """Range option allowed values."""
                return ["auto-range-on", "auto-range-off"]

        class auto_range_on(metaclass=PyLocalObjectMeta):
            """Auto range on definition."""

            class global_range(metaclass=PyLocalPropertyMeta):
                """Show global range."""

                value: bool = False

        class auto_range_off(metaclass=PyLocalObjectMeta):
            """Auto range off definition."""

            class clip_to_range(metaclass=PyLocalPropertyMeta):
                """Clip vector within range."""

                value: bool = False

            class minimum(metaclass=PyLocalPropertyMeta):
                """Range minimum."""

                _value: float

                @property
                def value(self):
                    """Range minimum property setter."""
                    if getattr(self, "_value", None) is None:
                        field_info = self._api_helper.field_info()
                        field_range = field_info.get_range(
                            "velocity-magnitude",
                            False,
                        )
                        self._value = field_range[0]
                    return self._value

                @value.setter
                def value(self, value):
                    self._value = value

            class maximum(metaclass=PyLocalPropertyMeta):
                """Range maximum."""

                _value: float

                @property
                def value(self):
                    """Range maximum property setter."""
                    if getattr(self, "_value", None) is None:
                        field_info = self._api_helper.field_info()
                        field_range = field_info.get_range(
                            "velocity-magnitude",
                            False,
                        )
                        self._value = field_range[1]
                    return self._value

                @value.setter
                def value(self, value):
                    self._value = value
