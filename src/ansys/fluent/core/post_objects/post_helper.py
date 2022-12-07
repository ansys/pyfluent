import re


class PostAPIHelper:
    """Class providing helper API for post objects."""

    class _SurfaceAPI:
        """Class providing APIs for surface operations."""

        def __init__(self, obj):
            self.obj = obj
            self._surface_name_on_server = self.surface_name_on_server(obj._name)

        @staticmethod
        def surface_name_on_server(local_surface_name):
            return "_dummy_surface_for_pyfluent:" + local_surface_name.lower()

        def _get_api_handle(self):
            return self.obj._get_top_most_parent().session.tui.surface

        def _delete_if_exist_on_server(self):
            field_info = self.obj._api_helper.field_info()
            surfaces_list = list(field_info.get_surfaces_info().keys())
            if self._surface_name_on_server in surfaces_list:
                self.delete_surface_on_server()

        def create_surface_on_server(self):
            if self.obj.definition.type() == "iso-surface":
                iso_surface = self.obj.definition.iso_surface
                field = iso_surface.field()
                iso_value = iso_surface.iso_value()
                if not field:
                    raise RuntimeError("Iso surface definition is incomplete.")
                self._delete_if_exist_on_server()
                phases = self.obj._api_helper._get_phases()
                unit_quantity = self.obj._api_helper._field_unit_quantity(field)
                unit_info = self.obj._api_helper._fluent_unit_info(unit_quantity)
                if phases:
                    phases = list(filter(field.startswith, phases))
                    if phases:
                        domain, field = (
                            field[0 : len(phases[0])],
                            field[len(phases[0]) + 1 :],
                        )
                    else:
                        domain = "mixture"
                    self._get_api_handle().iso_surface(
                        domain,
                        field,
                        self._surface_name_on_server,
                        (),
                        (),
                        (iso_value / unit_info[1]) - unit_info[2],
                        (),
                    )
                else:
                    self._get_api_handle().iso_surface(
                        field,
                        self._surface_name_on_server,
                        (),
                        (),
                        (iso_value / unit_info[1]) - unit_info[2],
                        (),
                    )
            elif self.obj.definition.type() == "plane-surface":
                plane_surface = self.obj.definition.plane_surface
                xy_plane = plane_surface.xy_plane
                yz_plane = plane_surface.yz_plane
                zx_plane = plane_surface.zx_plane
                self._delete_if_exist_on_server()
                unit_info = self.obj._api_helper._fluent_unit_info("length")
                self._get_api_handle().plane_surface(
                    self._surface_name_on_server,
                    "xy-plane" if xy_plane else "yz-plane" if yz_plane else "zx-plane",
                    (xy_plane.z() / unit_info[1]) - unit_info[2]
                    if xy_plane
                    else (yz_plane.x() / unit_info[1]) - unit_info[2]
                    if yz_plane
                    else (zx_plane.y() / unit_info[1]) - unit_info[2],
                )
            field_info = self.obj._api_helper.field_info()
            surfaces_list = list(field_info.get_surfaces_info().keys())
            if self._surface_name_on_server not in surfaces_list:
                raise RuntimeError("Surface creation failed.")

        def delete_surface_on_server(self):
            self._get_api_handle().delete_surface(self._surface_name_on_server)

    def __init__(self, obj):
        self.obj = obj
        self.field_info = lambda: obj._get_top_most_parent().session.field_info
        self.field_data = lambda: obj._get_top_most_parent().session.field_data
        self.monitors_manager = (
            lambda: obj._get_top_most_parent().session.monitors_manager
        )
        self.id = lambda: obj._get_top_most_parent().session.id
        if obj.__class__.__name__ == "Surface":
            self.surface_api = PostAPIHelper._SurfaceAPI(obj)

    def remote_surface_name(self, local_surface_name):
        local_surfaces_provider = (
            self.obj._get_top_most_parent()._local_surfaces_provider()
        )
        if local_surface_name in list(local_surfaces_provider):
            return PostAPIHelper._SurfaceAPI.surface_name_on_server(local_surface_name)
        else:
            return local_surface_name

    # Following functions will be deprecated in future.
    def get_vector_fields(self):
        scheme_eval_str = "(map car (apply append (map client-inquire-cell-vector-functions (inquire-domain-for-cell-functions))))"  # noqa: E501
        return self._scheme_str_to_py_list(scheme_eval_str)

    def get_field_unit(self, field):
        quantity = self._field_unit_quantity(field)
        if quantity == "*null*":
            return ""
        scheme_eval_str = f"(units/get-pretty-wb-units-from-dimension (units/inquire-dimension '{quantity}))"  # noqa: E501
        return " ".join(self._scheme_str_to_py_list(scheme_eval_str))

    def _get_phases(self):
        scheme_eval_str = "(map domain-name (get-phase-domains))"
        return self._scheme_str_to_py_list(scheme_eval_str)

    def _field_unit_quantity(self, field):
        scheme_eval_str = f"(cdr (assq 'units (%fill-render-info '{field})))"
        return self._scheme_str_to_py_list(scheme_eval_str)[0]

    def _fluent_unit_info(self, unit_quantity):
        def to_float(number):
            try:
                return float(number)
            except ValueError:
                return number

        scheme_eval_str = (
            f"(units/inquire-label-scale-offset-for-quantity '{unit_quantity})"
        )
        unit_info = [
            to_float(data) for data in self._scheme_str_to_py_list(scheme_eval_str)
        ]
        if len(unit_info) == 2:
            unit_info.insert(0, "")
        return unit_info

    def _scheme_str_to_py_list(self, scheme_eval_str):
        session = self.obj._get_top_most_parent().session
        str = session.scheme_eval.string_eval(scheme_eval_str)
        return list(filter(None, re.split(r'[\s()"\']', str)))
