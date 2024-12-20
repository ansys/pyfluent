"""Module providing visualization objects definition."""

from abc import abstractmethod
import logging
from typing import List, NamedTuple

from ansys.fluent.core.post_objects.meta import (
    Attribute,
    PyLocalNamedObjectMetaAbstract,
    PyLocalObjectMeta,
    PyLocalPropertyMeta,
)

logger = logging.getLogger("pyfluent.post_objects")


class BasePostObjectDefn:
    """Base class for visualization objects."""

    def _pre_display(self):
        local_surfaces_provider = self.get_root()._local_surfaces_provider()
        for surf_name in self.surfaces():
            if surf_name in list(local_surfaces_provider):
                surf_obj = local_surfaces_provider[surf_name]
                surf_api = surf_obj._api_helper.surface_api
                surf_api.create_surface_on_server()

    def _post_display(self):
        local_surfaces_provider = self.get_root()._local_surfaces_provider()
        for surf_name in self.surfaces():
            if surf_name in list(local_surfaces_provider):
                surf_obj = local_surfaces_provider[surf_name]
                surf_api = surf_obj._api_helper.surface_api
                surf_api.delete_surface_on_server()


class GraphicsDefn(BasePostObjectDefn, metaclass=PyLocalNamedObjectMetaAbstract):
    """Abstract base class for graphics objects."""

    @abstractmethod
    def display(self, window_id: str | None = None):
        """Display graphics.

        Parameters
        ----------
        window_id : str, optional
            Window ID. If not specified, unique ID is used.
        """
        pass


class PlotDefn(BasePostObjectDefn, metaclass=PyLocalNamedObjectMetaAbstract):
    """Abstract base class for plot objects."""

    @abstractmethod
    def plot(self, window_id: str | None = None):
        """Draw plot.

        Parameters
        ----------
        window_id : str, optional
            Window ID. If not specified, unique ID is used.
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

        value: str = None

        @Attribute
        def allowed_values(self):
            """Monitor set allowed values."""
            return self._api_helper.monitors.get_monitor_set_names()


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

        value: str = None

        @Attribute
        def allowed_values(self):
            """Y axis function allowed values."""
            return list(self._api_helper.field_info().get_scalar_fields_info())

    class x_axis_function(metaclass=PyLocalPropertyMeta):
        """X Axis Function."""

        value: str = "direction-vector"

        @Attribute
        def allowed_values(self):
            """X axis function allowed values."""
            return ["direction-vector"]

    class surfaces(metaclass=PyLocalPropertyMeta):
        """List of surfaces for plotting."""

        value: List[str] = []

        @Attribute
        def allowed_values(self):
            """Surface list allowed values."""
            return list(
                self._api_helper.field_info().get_surfaces_info().keys()
            ) + list(self.get_root()._local_surfaces_provider())


class MeshDefn(GraphicsDefn):
    """Mesh graphics definition."""

    PLURAL = "Meshes"

    class surfaces(metaclass=PyLocalPropertyMeta):
        """List of surfaces for mesh graphics."""

        value: List[str] = []

        @Attribute
        def allowed_values(self):
            """Surface list allowed values."""
            return list(
                (self._api_helper.field_info().get_surfaces_info().keys())
            ) + list(self.get_root()._local_surfaces_provider())

    class show_edges(metaclass=PyLocalPropertyMeta):
        """Show edges for mesh."""

        value: bool = False

    class show_nodes(metaclass=PyLocalPropertyMeta):
        """Show nodes for mesh."""

        value: bool = False

    class show_faces(metaclass=PyLocalPropertyMeta):
        """Show faces for mesh."""

        value: bool = True


class PathlinesDefn(GraphicsDefn):
    """Pathlines definition."""

    PLURAL = "Pathlines"

    class field(metaclass=PyLocalPropertyMeta):
        """Pathlines field."""

        value: str = None

        @Attribute
        def allowed_values(self):
            """Field allowed values."""
            return list(self._api_helper.field_info().get_scalar_fields_info())

    class surfaces(metaclass=PyLocalPropertyMeta):
        """List of surfaces for pathlines."""

        value: List[str] = []

        @Attribute
        def allowed_values(self):
            """Surface list allowed values."""
            return list(
                (self._api_helper.field_info().get_surfaces_info().keys())
            ) + list(self.get_root()._local_surfaces_provider())


class SurfaceDefn(GraphicsDefn):
    """Surface graphics definition."""

    PLURAL = "Surfaces"

    @property
    def name(self) -> str:
        """Return name of the surface."""
        return self._name

    class show_edges(metaclass=PyLocalPropertyMeta):
        """Show edges for surface."""

        value: bool = True

    class definition(metaclass=PyLocalObjectMeta):
        """Specify surface definition type."""

        class type(metaclass=PyLocalPropertyMeta):
            """Surface type."""

            value: str = "iso-surface"

            @Attribute
            def allowed_values(self):
                """Surface type allowed values."""
                return ["plane-surface", "iso-surface"]

        class plane_surface(metaclass=PyLocalObjectMeta):
            """Plane surface definition."""

            @Attribute
            def is_active(self):
                """Check whether current object is active or not."""
                return self._parent.type() == "plane-surface"

            class creation_method(metaclass=PyLocalPropertyMeta):
                """Creation Method."""

                value: str = "xy-plane"

                @Attribute
                def allowed_values(self):
                    """Surface type allowed values."""
                    return ["xy-plane", "yz-plane", "zx-plane"]

            class xy_plane(metaclass=PyLocalObjectMeta):
                """XY Plane definition."""

                @Attribute
                def is_active(self):
                    """Check whether current object is active or not."""
                    return self._parent.creation_method() == "xy-plane"

                class z(metaclass=PyLocalPropertyMeta):
                    """Z value."""

                    value: float = 0

                    @Attribute
                    def range(self):
                        """Z value range."""
                        return self._api_helper.field_info().get_scalar_field_range(
                            "z-coordinate", True
                        )

            class yz_plane(metaclass=PyLocalObjectMeta):
                """YZ Plane definition."""

                @Attribute
                def is_active(self):
                    """Check whether current object is active or not."""
                    return self._parent.creation_method() == "yz-plane"

                class x(metaclass=PyLocalPropertyMeta):
                    """X value."""

                    value: float = 0

                    @Attribute
                    def range(self):
                        """X value range."""
                        return self._api_helper.field_info().get_scalar_field_range(
                            "x-coordinate", True
                        )

            class zx_plane(metaclass=PyLocalObjectMeta):
                """ZX Plane definition."""

                @Attribute
                def is_active(self):
                    """Check whether current object is active or not."""
                    return self._parent.creation_method() == "zx-plane"

                class y(metaclass=PyLocalPropertyMeta):
                    """Y value."""

                    value: float = 0

                    @Attribute
                    def range(self):
                        """Y value range."""
                        return self._api_helper.field_info().get_scalar_field_range(
                            "y-coordinate", True
                        )

        class iso_surface(metaclass=PyLocalObjectMeta):
            """Iso surface definition."""

            @Attribute
            def is_active(self):
                """Check whether current object is active or not."""
                return self._parent.type() == "iso-surface"

            class field(metaclass=PyLocalPropertyMeta):
                """Iso surface field."""

                value: str = None

                @Attribute
                def allowed_values(self):
                    """Field allowed values."""
                    return list(self._api_helper.field_info().get_scalar_fields_info())

            class rendering(metaclass=PyLocalPropertyMeta):
                """Iso surface rendering."""

                value: str = "mesh"

                @Attribute
                def allowed_values(self):
                    """Surface rendering allowed values."""
                    return ["mesh", "contour"]

            class iso_value(metaclass=PyLocalPropertyMeta):
                """Iso value for field."""

                _value: float = None

                def _reset_on_change(self):
                    return [self._parent.field]

                @property
                def value(self):
                    """Iso value property setter."""
                    if getattr(self, "_value", None) is None:
                        rnge = self.range
                        self._value = (rnge[0] + rnge[1]) / 2.0 if rnge else None
                    return self._value

                @value.setter
                def value(self, value):
                    self._value = value

                @Attribute
                def range(self):
                    """Iso value range."""
                    field = self._parent.field()
                    if field:
                        return self._api_helper.field_info().get_scalar_field_range(
                            field, True
                        )


class ContourDefn(GraphicsDefn):
    """Contour graphics definition."""

    PLURAL = "Contours"

    class field(metaclass=PyLocalPropertyMeta):
        """Contour field."""

        value: str = None

        @Attribute
        def allowed_values(self):
            """Field allowed values."""
            return list(self._api_helper.field_info().get_scalar_fields_info())

    class surfaces(metaclass=PyLocalPropertyMeta):
        """Contour surfaces."""

        value: List[str] = []

        @Attribute
        def allowed_values(self):
            """Surfaces list allowed values."""
            return list(
                self._api_helper.field_info().get_surfaces_info().keys()
            ) + list(self.get_root()._local_surfaces_provider())

    class filled(metaclass=PyLocalPropertyMeta):
        """Draw filled contour."""

        value: bool = True

    class node_values(metaclass=PyLocalPropertyMeta):
        """Draw nodal data."""

        _value: bool = True

        @property
        def value(self):
            """Node value property setter."""
            filled = self.get_ancestors_by_type(ContourDefn).filled()
            auto_range_off = self.get_ancestors_by_type(
                ContourDefn
            ).range.auto_range_off
            if not filled or (auto_range_off and auto_range_off.clip_to_range()):
                logger.warning(
                    "For unfilled and clipped contours node values are displayed."
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

        class option(metaclass=PyLocalPropertyMeta):
            """Range option."""

            value: str = "auto-range-on"

            @Attribute
            def allowed_values(self):
                """Range option allowed values."""
                return ["auto-range-on", "auto-range-off"]

        class auto_range_on(metaclass=PyLocalObjectMeta):
            """Auto range on definition."""

            @Attribute
            def is_active(self):
                """Check whether current object is active or not."""
                return self._parent.option() == "auto-range-on"

            class global_range(metaclass=PyLocalPropertyMeta):
                """Show global range."""

                value: bool = False

        class auto_range_off(metaclass=PyLocalObjectMeta):
            """Auto range off definition."""

            @Attribute
            def is_active(self):
                """Check whether current object is active or not."""
                return self._parent.option() == "auto-range-off"

            class clip_to_range(metaclass=PyLocalPropertyMeta):
                """Clip contour within range."""

                value: bool = False

            class minimum(metaclass=PyLocalPropertyMeta):
                """Range minimum."""

                _value: float = None

                def _reset_on_change(self):
                    return [
                        self.get_ancestors_by_type(ContourDefn).field,
                        self.get_ancestors_by_type(ContourDefn).node_values,
                    ]

                @property
                def value(self):
                    """Range minimum property setter."""
                    if getattr(self, "_value", None) is None:
                        field = self.get_ancestors_by_type(ContourDefn).field()
                        if field:
                            field_info = self._api_helper.field_info()
                            field_range = field_info.get_scalar_field_range(
                                field,
                                self.get_ancestors_by_type(ContourDefn).node_values(),
                            )
                            self._value = field_range[0]
                    return self._value

                @value.setter
                def value(self, value):
                    self._value = value

            class maximum(metaclass=PyLocalPropertyMeta):
                """Range maximum."""

                _value: float = None

                def _reset_on_change(self):
                    return [
                        self.get_ancestors_by_type(ContourDefn).field,
                        self.get_ancestors_by_type(ContourDefn).node_values,
                    ]

                @property
                def value(self):
                    """Range maximum property setter."""
                    if getattr(self, "_value", None) is None:
                        field = self.get_ancestors_by_type(ContourDefn).field()
                        if field:
                            field_info = self._api_helper.field_info()
                            field_range = field_info.get_scalar_field_range(
                                field,
                                self.get_ancestors_by_type(ContourDefn).node_values(),
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
            if hasattr(self._api_helper.field_info(), "get_vector_fields_info"):
                return list(self._api_helper.field_info().get_vector_fields_info())
            return list(self._api_helper.get_vector_fields())

    class field(metaclass=PyLocalPropertyMeta):
        """Vector color field."""

        value: str = None

        @Attribute
        def allowed_values(self):
            """Field allowed values."""
            return list(self._api_helper.field_info().get_scalar_fields_info())

    class surfaces(metaclass=PyLocalPropertyMeta):
        """List of surfaces for vector graphics."""

        value: List[str] = []

        @Attribute
        def allowed_values(self):
            """Surface list allowed values."""
            return list(
                self._api_helper.field_info().get_surfaces_info().keys()
            ) + list(self.get_root()._local_surfaces_provider())

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

        class option(metaclass=PyLocalPropertyMeta):
            """Range option."""

            value: str = "auto-range-on"

            @Attribute
            def allowed_values(self):
                """Range option allowed values."""
                return ["auto-range-on", "auto-range-off"]

        class auto_range_on(metaclass=PyLocalObjectMeta):
            """Auto range on definition."""

            @Attribute
            def is_active(self):
                """Check whether current object is active or not."""
                return self._parent.option() == "auto-range-on"

            class global_range(metaclass=PyLocalPropertyMeta):
                """Show global range."""

                value: bool = False

        class auto_range_off(metaclass=PyLocalObjectMeta):
            """Auto range off definition."""

            @Attribute
            def is_active(self):
                """Check whether current object is active or not."""
                return self._parent.option() == "auto-range-off"

            class clip_to_range(metaclass=PyLocalPropertyMeta):
                """Clip vector within range."""

                value: bool = False

            class minimum(metaclass=PyLocalPropertyMeta):
                """Range minimum."""

                _value: float = None

                @property
                def value(self):
                    """Range minimum property setter."""
                    if getattr(self, "_value", None) is None:
                        field_info = self._api_helper.field_info()
                        field_range = field_info.get_scalar_field_range(
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

                _value: float = None

                @property
                def value(self):
                    """Range maximum property setter."""
                    if getattr(self, "_value", None) is None:
                        field_info = self._api_helper.field_info()
                        field_range = field_info.get_scalar_field_range(
                            "velocity-magnitude",
                            False,
                        )
                        self._value = field_range[1]
                    return self._value

                @value.setter
                def value(self, value):
                    self._value = value
