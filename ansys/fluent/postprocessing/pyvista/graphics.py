import sys
from ansys.fluent.postprocessing.pyvista.plotter import plotter
from ansys.fluent.session import Session
from ansys.fluent.solver.meta import (
    Attribute,
    PyLocalNamedObjectMeta,
    PyLocalPropertyMeta,
)


class Graphics:
    """
    Graphics objects provider.
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


class Mesh(metaclass=PyLocalNamedObjectMeta):
    """
    Mesh graphics.
    """

    def display(self):
        """
        Display mesh graphics.
        """
        plotter.set_graphics(self)

    class surfaces_list(metaclass=PyLocalPropertyMeta):
        """
        List of surfaces for mesh graphics.
        """

        @Attribute
        def allowed_values(self):
            return list(self.session.field_data.get_surfaces_info().keys())

    class show_edges(metaclass=PyLocalPropertyMeta):
        """
        Show edges for mesh.
        """

        value = False


class Surface(metaclass=PyLocalNamedObjectMeta):
    """
    Surface graphics.
    """

    def display(self):
        """
        Display contour graphics.
        """
        plotter.set_graphics(self)

    class show_edges(metaclass=PyLocalPropertyMeta):
        """
        Show edges for surface.
        """

        value = True

    class surface_type(metaclass=PyLocalPropertyMeta):
        """
        Specify surface type.
        """

        def availability(self, name):
            if name == "plane_surface":
                return self.surface_type() == "plane-surface"
            if name == "iso_surface":
                return self.surface_type() == "iso-surface"
            return True

        class surface_type(metaclass=PyLocalPropertyMeta):
            value = "iso-surface"

            @Attribute
            def allowed_values(self):
                return ["plane_surface", "iso_surface"]

        class plane_surface(metaclass=PyLocalPropertyMeta):
            """
            Plane surface data.
            """

        class iso_surface(metaclass=PyLocalPropertyMeta):
            """
            Iso surface data.
            """

            class field(metaclass=PyLocalPropertyMeta):
                """
                Iso surface field.
                """

                @Attribute
                def allowed_values(self):
                    return [
                        v["solver_name"]
                        for k, v in self.session.field_data
                        .get_fields_info().items()
                    ]

            class rendering(metaclass=PyLocalPropertyMeta):
                """
                Iso surface rendering.
                """

                value = "mesh"

                @Attribute
                def allowed_values(self):
                    return ["mesh", "contour"]

            class iso_value(metaclass=PyLocalPropertyMeta):
                """
                Iso surface iso value.
                """

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
                        return self.session.field_data.get_range(field)


class Contour(metaclass=PyLocalNamedObjectMeta):
    """
    Contour graphics.
    """

    def display(self):
        """
        Display Contour graphics.
        """
        plotter.set_graphics(self)

    class field(metaclass=PyLocalPropertyMeta):
        """
        Contour field.
        """

        @Attribute
        def allowed_values(self):
            return [
                v["solver_name"]
                for k, v in self.session.field_data.get_fields_info().items()
            ]

    class surfaces_list(metaclass=PyLocalPropertyMeta):
        """
        Contour surfaces.
        """

        @Attribute
        def allowed_values(self):
            return list(self.session.field_data.get_surfaces_info().keys())

    class filled(metaclass=PyLocalPropertyMeta):
        """
        Show filled contour.
        """

        value = True

    class node_values(metaclass=PyLocalPropertyMeta):
        """
        Show nodal data.
        """

        value = True

    class boundary_values(metaclass=PyLocalPropertyMeta):
        """
        Show boundary values.
        """

        value = False

    class contour_lines(metaclass=PyLocalPropertyMeta):
        """
        Show contour lines.
        """

        value = False

    class show_edges(metaclass=PyLocalPropertyMeta):
        """
        Show edges.
        """

        value = False

    class range_option(metaclass=PyLocalPropertyMeta):
        """
        Specify range options.
        """

        def availability(self, name):
            if name == "auto_range_on":
                return self.range_option() == "auto-range-on"
            if name == "auto_range_off":
                return self.range_option() == "auto-range-off"
            return True

        class range_option(metaclass=PyLocalPropertyMeta):

            value = "auto-range-on"

            @Attribute
            def allowed_values(self):
                return ["auto-range-on", "auto-range-off"]

        class auto_range_on(metaclass=PyLocalPropertyMeta):
            """
            Specify auto range on.
            """

            class global_range(metaclass=PyLocalPropertyMeta):
                """
                Show global range.
                """

                value = False

        class auto_range_off(metaclass=PyLocalPropertyMeta):
            """
            Specify auto range off.
            """

            class clip_to_range(metaclass=PyLocalPropertyMeta):
                """
                Clip contour within range.
                """

                value = False

            class minimum(metaclass=PyLocalPropertyMeta):
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
                    if getattr(self, "_value", None) == None:
                        field = self.parent.parent.parent.field()
                        if field:
                            field_range = self.session.field_data.get_range(
                                field,
                                self.parent.parent.parent.node_values(),
                            )
                            self._value = field_range[0]
                    return self._value

                @value.setter
                def value(self, value):
                    self._value = value

            class maximum(metaclass=PyLocalPropertyMeta):
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
                    if getattr(self, "_value", None) == None:
                        field = self.parent.parent.parent.field()
                        if field:
                            field_range = self.session.field_data.get_range(
                                field,
                                self.parent.parent.parent.node_values(),
                            )
                            self._value = field_range[1]

                    return self._value

                @value.setter
                def value(self, value):
                    self._value = value
