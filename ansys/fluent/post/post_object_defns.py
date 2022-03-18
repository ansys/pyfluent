"""Module providing post objects definition."""
from abc import abstractmethod
from typing import List, NamedTuple, Optional

from ansys.fluent.core.meta import (
    Attribute,
    PyLocalNamedObjectMetaAbstract,
    PyLocalObjectMeta,
    PyLocalPropertyMeta,
)


class GraphicsDefn(metaclass=PyLocalNamedObjectMetaAbstract):
    """Abstract base class for graphics objects."""

    @abstractmethod
    def display(self, plotter_id: Optional[str] = None):
        """
        Display graphics.

        Parameters
        ----------
        window_id : str, optional
            Window id. If not specified unique id is used.
        """
        pass


class PlotDefn(metaclass=PyLocalNamedObjectMetaAbstract):
    """Abstract base class for plot objects."""

    @abstractmethod
    def plot(self, plotter_id: Optional[str] = None):
        """
        Draw plot.

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


class XYPlotDefn(PlotDefn):
    """XYPlot Definition."""

    class node_values(metaclass=PyLocalPropertyMeta):
        """Show nodal data."""

        value: bool = True

    class boundary_values(metaclass=PyLocalPropertyMeta):
        """Show Boundary values."""

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
            return [
                v["solver_name"]
                for k, v in self.get_session()
                .field_data.get_fields_info()
                .items()
            ]

    class x_axis_function(metaclass=PyLocalPropertyMeta):
        """X Axis Function."""

        value: str = "direction-vector"

        @Attribute
        def allowed_values(self):
            """X axis function allowed values."""
            return ["direction-vector", "curve-length"]

    class surfaces_list(metaclass=PyLocalPropertyMeta):
        """List of surfaces for plotting."""

        value: List[str]

        @Attribute
        def allowed_values(self):
            """Surface list allowed values."""
            return list(
                self.field_data().get_surfaces_info().keys()
            )


class MeshDefn(GraphicsDefn):
    """Mesh graphics."""

    PLURAL = "Meshes"

    class surfaces_list(metaclass=PyLocalPropertyMeta):
        """List of surfaces for mesh graphics."""

        value: List[str]

        @Attribute
        def allowed_values(self):
            """Surface list allowed values."""
            return list(
                (self.field_data().get_surfaces_info().keys())
            )

    class show_edges(metaclass=PyLocalPropertyMeta):
        """Show edges for mesh."""

        value: bool = False


class SurfaceDefn(GraphicsDefn):
    """Surface graphics."""

    PLURAL = "Surfaces"

    class show_edges(metaclass=PyLocalPropertyMeta):
        """Show edges for surface."""

        value: bool = True

    class surface_type(metaclass=PyLocalObjectMeta):
        """Specify surface type."""

        def _availability(self, name):
            if name == "plane_surface":
                return self.surface_type() == "plane-surface"
            if name == "iso_surface":
                return self.surface_type() == "iso-surface"
            return True

        class surface_type(metaclass=PyLocalPropertyMeta):
            """Surface type."""

            value: str = "iso-surface"

            @Attribute
            def allowed_values(self):
                """Surface type allowed values."""
                return ["plane-surface", "iso-surface"]

        class plane_surface(metaclass=PyLocalObjectMeta):
            """Plane surface data."""

        class iso_surface(metaclass=PyLocalObjectMeta):
            """Iso surface data."""

            class field(metaclass=PyLocalPropertyMeta):
                """Iso surface field."""

                value: str

                @Attribute
                def allowed_values(self):
                    """Field allowed values."""
                    field_data = self.field_data()
                    return [
                        v["solver_name"]
                        for k, v in field_data.get_fields_info().items()
                    ]

            class rendering(metaclass=PyLocalPropertyMeta):
                """Iso surface rendering."""

                value: str = "mesh"

                @Attribute
                def allowed_values(self):
                    """Surface rendering allowed values."""
                    return ["mesh", "contour"]

            class iso_value(metaclass=PyLocalPropertyMeta):
                """Iso surface field iso value."""

                _value: float

                def _reset_on_change(self):
                    return [self.parent.field]

                @property
                def value(self):
                    """Iso value property setter."""
                    if getattr(self, "_value", None) is None:
                        range = self.range
                        self._value = range[0] if range else None
                    return self._value

                @value.setter
                def value(self, value):
                    self._value = value

                @Attribute
                def range(self):
                    """Iso value range."""
                    field = self.parent.field()
                    if field:
                        return self.field_data().get_range(
                            field, True
                        )


class ContourDefn(GraphicsDefn):
    """Contour graphics."""

    PLURAL = "Contours"

    class field(metaclass=PyLocalPropertyMeta):
        """Contour field."""

        value: str

        @Attribute
        def allowed_values(self):
            """Field allowed values."""
            field_data = self.field_data()
            return [
                v["solver_name"]
                for k, v in field_data.get_fields_info().items()
            ]

    class surfaces_list(metaclass=PyLocalPropertyMeta):
        """Contour surfaces."""

        value: List[str]

        @Attribute
        def allowed_values(self):
            """Surfaces list allowed values."""
            return list(
                self.field_data().get_surfaces_info().keys()
            )

    class filled(metaclass=PyLocalPropertyMeta):
        """Show filled contour."""

        value: bool = True

    class node_values(metaclass=PyLocalPropertyMeta):
        """Show nodal data."""

        value: bool = True

    class boundary_values(metaclass=PyLocalPropertyMeta):
        """Show boundary values."""

        value: bool = False

    class contour_lines(metaclass=PyLocalPropertyMeta):
        """Show contour lines."""

        value: bool = False

    class show_edges(metaclass=PyLocalPropertyMeta):
        """Show edges."""

        value: bool = False

    class range_option(metaclass=PyLocalObjectMeta):
        """Specify range options."""

        def _availability(self, name):
            if name == "auto_range_on":
                return self.range_option() == "auto-range-on"
            if name == "auto_range_off":
                return self.range_option() == "auto-range-off"
            return True

        class range_option(metaclass=PyLocalPropertyMeta):
            """Range option."""

            value: str = "auto-range-on"

            @Attribute
            def allowed_values(self):
                """Range option allowed values."""
                return ["auto-range-on", "auto-range-off"]

        class auto_range_on(metaclass=PyLocalObjectMeta):
            """Specify auto range on."""

            class global_range(metaclass=PyLocalPropertyMeta):
                """Show global range."""

                value: bool = False

        class auto_range_off(metaclass=PyLocalObjectMeta):
            """Specify auto range off."""

            class clip_to_range(metaclass=PyLocalPropertyMeta):
                """Clip contour within range."""

                value: bool = False

            class minimum(metaclass=PyLocalPropertyMeta):
                """Range minimum."""

                _value: float

                def _reset_on_change(self):
                    return [
                        self.parent.parent.parent.field,
                        self.parent.parent.parent.node_values,
                    ]

                @property
                def value(self):
                    """Range minimum property setter."""
                    if getattr(self, "_value", None) is None:
                        field = self.parent.parent.parent.field()
                        if field:
                            field_data = self.field_data()
                            field_range = field_data.get_range(
                                field, self.parent.parent.parent.node_values()
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
                        self.parent.parent.parent.field,
                        self.parent.parent.parent.node_values,
                    ]

                @property
                def value(self):
                    """Range maximum property setter."""
                    if getattr(self, "_value", None) is None:
                        field = self.parent.parent.parent.field()
                        if field:
                            field_data = self.field_data()
                            field_range = field_data.get_range(
                                field,
                                self.parent.parent.parent.node_values(),
                            )
                            self._value = field_range[1]

                    return self._value

                @value.setter
                def value(self, value):
                    self._value = value


class VectorDefn(GraphicsDefn):
    """Vector graphics."""

    PLURAL = "Vectors"

    class vectors_of(metaclass=PyLocalPropertyMeta):
        """Vector type."""

        value: str = "velocity"

        @Attribute
        def allowed_values(self):
            """Vectors of allowed values."""
            return list(
                self.field_data().get_vector_fields_info().keys()
            )

    class surfaces_list(metaclass=PyLocalPropertyMeta):
        """List of surfaces for vector graphics."""

        value: List[str]

        @Attribute
        def allowed_values(self):
            """Surface list allowed values."""
            return list(
                self.field_data().get_surfaces_info().keys()
            )

    class scale(metaclass=PyLocalPropertyMeta):
        """Vector scale."""

        value: float = 1.0

    class skip(metaclass=PyLocalPropertyMeta):
        """Vector skip."""

        value: int = 0

    class show_edges(metaclass=PyLocalPropertyMeta):
        """Show edges."""

        value: bool = False

    class range_option(metaclass=PyLocalObjectMeta):
        """Specify range options."""

        def _availability(self, name):
            if name == "auto_range_on":
                return self.range_option() == "auto-range-on"
            if name == "auto_range_off":
                return self.range_option() == "auto-range-off"
            return True

        class range_option(metaclass=PyLocalPropertyMeta):
            """Range option."""

            value: str = "auto-range-on"

            @Attribute
            def allowed_values(self):
                """Range option allowed values."""
                return ["auto-range-on", "auto-range-off"]

        class auto_range_on(metaclass=PyLocalObjectMeta):
            """Specify auto range on."""

            class global_range(metaclass=PyLocalPropertyMeta):
                """Show global range."""

                value: bool = False

        class auto_range_off(metaclass=PyLocalObjectMeta):
            """Specify auto range off."""

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
                        field_data = self.self.field_data()
                        field_range = field_data.get_range(
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
                        field_data = self.self.field_data()
                        field_range = field_data.get_range(
                            "velocity-magnitude",
                            False,
                        )
                        self._value = field_range[1]
                    return self._value

                @value.setter
                def value(self, value):
                    self._value = value
