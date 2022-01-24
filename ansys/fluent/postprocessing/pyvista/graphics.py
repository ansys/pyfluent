from ansys.fluent.solver.meta import (
    PyLocaPropertyMeta,
    PyLocalNamedObjectMeta,
    Attribute,
)
from ansys.fluent.core.core import FieldData
from ansys.fluent.postprocessing.pyvista.plotter import plotter
from ansys.fluent.session import Session
import sys


class Graphics:
    """
    Instantiate the graphics objects.
    """

    def __init__(self, session):
        self.session = session
        self._init_module(self, sys.modules[__name__])

    def _init_module(self, obj, mod):
        for name, cls in mod.__dict__.items():
            if cls.__class__.__name__ == "module":
                module = mod.__dict__[name]
                cls_obj = type(name, (), {})()
                setattr(obj, name, cls_obj)
                self._init_module(cls_obj, module)
            if cls.__class__.__name__ == "PyLocalNamedObjectMeta":
                setattr(
                    obj,
                    name,
                    cls([(name, None)], None, self.session, obj),
                )


Session.register_on_exit(lambda: plotter.close())


class mesh(metaclass=PyLocalNamedObjectMeta):
    """
    Mesh graphics.
    """

    def display(self):
        """
        Displays mesh graphics.
        """
        plotter.set_graphics(self)

    class surfaces_list(metaclass=PyLocaPropertyMeta):
        """
        List of surfaces for mesh graphics.
        """

        @Attribute
        def allowed_values(self):
            return list(
                FieldData(self.session.field_service)
                .get_surfaces_info()
                .keys()
            )

    class show_edges(metaclass=PyLocaPropertyMeta):
        """
        Show edges for mesh.
        """

        value = False


class surface(metaclass=PyLocalNamedObjectMeta):
    """
    Surface graphics.
    """

    def display(self):
        """
        Displays contour graphics.
        """
        plotter.set_graphics(self)

    class show_edges(metaclass=PyLocaPropertyMeta):
        """
        Show edges for surface.
        """

        value = True

    class surface_type(metaclass=PyLocaPropertyMeta):
        """
        Specify surface type.
        """

        def availability(self, name):
            if name == "plane_surface":
                return self.surface_type() == "plane-surface"
            if name == "iso_surface":
                return self.surface_type() == "iso-surface"
            return True

        class surface_type(metaclass=PyLocaPropertyMeta):
            value = "iso-surface"

            @Attribute
            def allowed_values(self):
                return ["plane_surface", "iso_surface"]

        class plane_surface(metaclass=PyLocaPropertyMeta):
            """
            Plane surface data.
            """

        class iso_surface(metaclass=PyLocaPropertyMeta):
            """
            Iso surface data.
            """

            class field(metaclass=PyLocaPropertyMeta):
                """
                Iso surface field.
                """

                @Attribute
                def allowed_values(self):
                    return [
                        v["solver_name"]
                        for k, v in FieldData(
                            self.session.field_service
                        )
                        .get_fields_info()
                        .items()
                    ]

            class rendering(metaclass=PyLocaPropertyMeta):
                """
                Iso surface rendering.
                """

                value = "mesh"

                @Attribute
                def allowed_values(self):
                    return ["mesh", "contour"]

            class iso_value(metaclass=PyLocaPropertyMeta):
                """
                Iso surface iso value.
                """

                def _reset_on_change(self):
                    return [self.parent.field]

                @property
                def value(self):
                    if (
                        not hasattr(self, "_value")
                        or self._value == None
                    ):
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
                        return FieldData(
                            self.session.field_service
                        ).get_range(field)


class contour(metaclass=PyLocalNamedObjectMeta):
    """
    Contour graphics.
    """

    def display(self):
        """
        Displays Contour graphics.
        """
        plotter.set_graphics(self)

    class field(metaclass=PyLocaPropertyMeta):
        """
        Contour field.
        """

        @Attribute
        def allowed_values(self):
            return [
                v["solver_name"]
                for k, v in FieldData(self.session.field_service)
                .get_fields_info()
                .items()
            ]

    class surfaces_list(metaclass=PyLocaPropertyMeta):
        """
        Contour surfaces.
        """

        @Attribute
        def allowed_values(self):
            return list(
                FieldData(self.session.field_service)
                .get_surfaces_info()
                .keys()
            )

    class filled(metaclass=PyLocaPropertyMeta):
        """
        Show filled contour.
        """

        value = True

    class node_values(metaclass=PyLocaPropertyMeta):
        """
        Show nodal data.
        """

        value = True

    class boundary_values(metaclass=PyLocaPropertyMeta):
        """
        Show boundary values.
        """

        value = False

    class contour_lines(metaclass=PyLocaPropertyMeta):
        """
        Show contour lines.
        """

        value = False

    class show_edges(metaclass=PyLocaPropertyMeta):
        """
        Show edges.
        """

        value = False

    class range_option(metaclass=PyLocaPropertyMeta):
        """
        Specify range options.
        """

        def availability(self, name):
            if name == "auto_range_on":
                return self.range_option() == "auto-range-on"
            if name == "auto_range_off":
                return self.range_option() == "auto-range-off"
            return True

        class range_option(metaclass=PyLocaPropertyMeta):
            __doc__ = ""
            value = "auto-range-on"

            @Attribute
            def allowed_values(self):
                return ["auto-range-on", "auto-range-off"]

        class auto_range_on(metaclass=PyLocaPropertyMeta):
            class global_range(metaclass=PyLocaPropertyMeta):
                """
                Show global range.
                """

                value = False

        class auto_range_off(metaclass=PyLocaPropertyMeta):
            __doc__ = ""

            class clip_to_range(metaclass=PyLocaPropertyMeta):
                """
                Clip contour within range.
                """

                value = False

            class minimum(metaclass=PyLocaPropertyMeta):
                """
                Range minimum.
                """

                def _reset_on_change(self):
                    return [
                        self.parent.parent.parent.field,
                        self.parent.parent.parent.node_values,
                    ]

                @property
                def value(self):
                    if (
                        not hasattr(self, "_value")
                        or self._value == None
                    ):
                        field = self.parent.parent.parent.field()
                        if field:
                            field_range = FieldData(
                                self.session.field_service
                            ).get_range(
                                field,
                                self.parent.parent.parent.node_values(),
                            )
                            self._value = field_range[0]
                    return self._value

                @value.setter
                def value(self, value):
                    self._value = value

            class maximum(metaclass=PyLocaPropertyMeta):
                """
                Range maximum.
                """

                def _reset_on_change(self):
                    return [
                        self.parent.parent.parent.field,
                        self.parent.parent.parent.node_values,
                    ]

                @property
                def value(self):
                    if (
                        not hasattr(self, "_value")
                        or self._value == None
                    ):
                        field = self.parent.parent.parent.field()
                        if field:
                            field_range = FieldData(
                                self.session.field_service
                            ).get_range(
                                field,
                                self.parent.parent.parent.node_values(),
                            )
                            self._value = field_range[1]

                    return self._value

                @value.setter
                def value(self, value):
                    self._value = value
