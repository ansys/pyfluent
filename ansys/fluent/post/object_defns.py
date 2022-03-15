from abc import abstractmethod
from typing import List, Optional, NamedTuple
from ansys.fluent.core.meta import (
    Attribute,
    PyLocalNamedObjectMetaAbstract,
    PyLocalObjectMeta,
    PyLocalPropertyMeta,
)


class Vector(NamedTuple):
    x: float
    y: float
    z: float


class XYPlotDefn(metaclass=PyLocalNamedObjectMetaAbstract):
    """XYPlot Definition."""

    @abstractmethod
    def plot(self, plotter_id: Optional[str] = None):
        pass

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
            return [
                v["solver_name"]
                for k, v in self.get_session().
                field_data.get_fields_info().items()
            ]

    class x_axis_function(metaclass=PyLocalPropertyMeta):
        """X Axis Function."""

        value: str = "direction-vector"

        @Attribute
        def allowed_values(self):
            return ["direction-vector", "curve-length"]

    class surfaces_list(metaclass=PyLocalPropertyMeta):
        """List of surfaces for plotting."""

        value: List[str]

        @Attribute
        def allowed_values(self):
            return list(
                self.get_session().
                field_data.get_surfaces_info().keys()
            )


class MeshDefn(metaclass=PyLocalNamedObjectMetaAbstract):
    """Mesh graphics."""

    PLURAL = "Meshes"

    @abstractmethod
    def display(self, plotter_id: Optional[str] = None):
        pass

    class surfaces_list(metaclass=PyLocalPropertyMeta):
        """List of surfaces for mesh graphics."""

        value: List[str]

        @Attribute
        def allowed_values(self):
            return list(
                (
                    self.get_session().
                    field_data.get_surfaces_info().keys()
                )
            )

    class show_edges(metaclass=PyLocalPropertyMeta):
        """Show edges for mesh."""

        value: bool = False


class SurfaceDefn(metaclass=PyLocalNamedObjectMetaAbstract):
    """Surface graphics."""

    PLURAL = "Surfaces"

    @abstractmethod
    def display(self, plotter_id: Optional[str] = None):
        pass

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
            value: str = "iso-surface"

            @Attribute
            def allowed_values(self):
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
                    field_data = (
                        self.get_session().
                        field_data
                    )
                    return [
                        v["solver_name"]
                        for k, v in field_data.get_fields_info().items()
                    ]

            class rendering(metaclass=PyLocalPropertyMeta):
                """Iso surface rendering."""

                value: str = "mesh"

                @Attribute
                def allowed_values(self):
                    return ["mesh", "contour"]

            class iso_value(metaclass=PyLocalPropertyMeta):
                """Iso surface iso value."""

                _value: float

                def _reset_on_change(self):
                    return [self.parent.field]

                @property
                def value(self):
                    if getattr(self, "_value", None) == None:
                        range = self.range
                        self._value = range[0] if range else None
                    return self._value

                @value.setter
                def value(self, value):
                    self._value = value

                @Attribute
                def range(self):
                    field = self.parent.field()
                    if field:
                        return (self.get_session().
                        field_data.get_range(
                            field, True
                        ))


class ContourDefn(metaclass=PyLocalNamedObjectMetaAbstract):
    """Contour graphics."""

    PLURAL = "Contours"

    @abstractmethod
    def display(self, plotter_id: Optional[str] = None):
        pass

    class field(metaclass=PyLocalPropertyMeta):
        """Contour field."""

        value: str

        @Attribute
        def allowed_values(self):
            field_data = self.get_session().field_data
            return [
                v["solver_name"]
                for k, v in field_data.get_fields_info().items()
            ]

    class surfaces_list(metaclass=PyLocalPropertyMeta):
        """Contour surfaces."""

        value: List[str]

        @Attribute
        def allowed_values(self):
            return list(
                self.get_session().
                field_data.get_surfaces_info().keys()
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

            value: str = "auto-range-on"

            @Attribute
            def allowed_values(self):
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
                    if getattr(self, "_value", None) == None:
                        field = self.parent.parent.parent.field()
                        if field:
                            field_data = (
                                self.get_session().
                                field_data
                            )
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
                    if getattr(self, "_value", None) == None:
                        field = self.parent.parent.parent.field()
                        if field:
                            field_data = (
                                self.get_session().
                                field_data
                            )
                            field_range = field_data.get_range(
                                field,
                                self.parent.parent.parent.node_values(),
                            )
                            self._value = field_range[1]

                    return self._value

                @value.setter
                def value(self, value):
                    self._value = value


class VectorDefn(metaclass=PyLocalNamedObjectMetaAbstract):
    """Vector graphics."""

    PLURAL = "Vectors"

    @abstractmethod
    def display(self, plotter_id: Optional[str] = None):
        pass

    class vectors_of(metaclass=PyLocalPropertyMeta):
        """Vector type."""

        value: str = "velocity"

        @Attribute
        def allowed_values(self):
            return list(
                self.get_session().
                field_data.get_vector_fields_info().keys()
            )

    class surfaces_list(metaclass=PyLocalPropertyMeta):
        """List of surfaces for vector graphics."""

        value: List[str]

        @Attribute
        def allowed_values(self):
            return list(
                self.get_session().
                field_data.get_surfaces_info().keys()
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

            value: str = "auto-range-on"

            @Attribute
            def allowed_values(self):
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
                    if getattr(self, "_value", None) == None:
                        field_data = (
                            self.self.get_session().
                            field_data
                        )
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
                    if getattr(self, "_value", None) == None:
                        field_data = (
                            self.self.get_session().
                            field_data
                        )
                        field_range = field_data.get_range(
                            "velocity-magnitude",
                            False,
                        )
                        self._value = field_range[1]
                    return self._value

                @value.setter
                def value(self, value):
                    self._value = value
