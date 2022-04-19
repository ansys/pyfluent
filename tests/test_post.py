from pathlib import Path
import pickle
from typing import Dict, List, Optional

import pytest

from ansys.fluent.post.matplotlib import Plots
from ansys.fluent.post.pyvista import Graphics


@pytest.fixture(autouse=True)
def patch_mock_data_extractor(mocker) -> None:
    mocker.patch(
        "ansys.fluent.core.meta.LocalObjectDataExtractor",
        MockLocalObjectDataExtractor,
    )


class MockFieldData:
    def __init__(self, solver_data):
        self._session_data = solver_data
        self._request_to_serve = {"surf": [], "scalar": [], "vector": []}

    def add_get_surfaces_request(
        self,
        surface_ids: List[int],
        overset_mesh: bool = False,
        provide_vertices=True,
        provide_faces=True,
        provide_faces_centroid=False,
        provide_faces_normal=False,
    ) -> None:
        self._request_to_serve["surf"].append(
            (
                surface_ids,
                overset_mesh,
                provide_vertices,
                provide_faces,
                provide_faces_centroid,
                provide_faces_normal,
            )
        )

    def add_get_scalar_fields_request(
        self,
        surface_ids: List[int],
        field_name: str,
        node_value: Optional[bool] = True,
        boundary_value: Optional[bool] = False,
    ) -> None:
        self._request_to_serve["scalar"].append(
            (surface_ids, field_name, node_value, boundary_value)
        )

    def add_get_vector_fields_request(
        self,
        surface_ids: List[int],
        vector_field: Optional[str] = "velocity",
    ) -> None:
        self._request_to_serve["vector"].append((surface_ids, vector_field))

    def get_fields(self) -> Dict[int, Dict]:
        fields = {}
        for request_type, requests in self._request_to_serve.items():
            for request in requests:
                if request_type == "surf":
                    tag_id = 0
                if request_type == "scalar":
                    location_tag = 4 if request[2] else 2
                    boundary_tag = 8 if request[3] else 0
                    tag_id = location_tag | boundary_tag
                if request_type == "vector":
                    tag_id = 0

                field_requests = fields.get(tag_id)
                if not field_requests:
                    field_requests = fields[tag_id] = {}
                surf_ids = request[0]
                for surf_id in surf_ids:
                    surface_requests = field_requests.get(surf_id)
                    if not surface_requests:
                        surface_requests = field_requests[surf_id] = {}
                    surface_requests.update(
                        self._session_data["fields"][tag_id][surf_id]
                    )
        return fields


class MockFieldInfo:
    def __init__(self, solver_data):
        self._session_data = solver_data

    def get_range(
        self, field: str, node_value: bool = False, surface_ids: List[int] = []
    ) -> List[float]:
        if not surface_ids:
            surface_ids = [
                v["surface_id"][0]
                for k, v in self._session_data["surfaces_info"].items()
            ]
        minimum, maximum = None, None
        for surface_id in surface_ids:
            range = self._session_data["range"][field][surface_id][
                "node_value" if node_value else "cell_value"
            ]
            minimum = min(range[0], minimum) if minimum else range[0]
            maximum = max(range[1], maximum) if maximum else range[1]
        return [minimum, maximum]

    def get_fields_info(self) -> dict:
        return self._session_data["scalar_fields_info"]

    def get_vector_fields_info(self) -> dict:
        return self._session_data["vector_fields_info"]

    def get_surfaces_info(self) -> dict:
        return self._session_data["surfaces_info"]


class MockLocalObjectDataExtractor:
    _session_data = None
    _session_dump = "tests//session.dump"

    def __init__(self, obj=None):
        if not MockLocalObjectDataExtractor._session_data:
            with open(
                str(
                    Path(MockLocalObjectDataExtractor._session_dump).resolve()
                ),
                "rb",
            ) as pickle_obj:
                MockLocalObjectDataExtractor._session_data = pickle.load(
                    pickle_obj
                )
        self.field_info = lambda: MockFieldInfo(
            MockLocalObjectDataExtractor._session_data
        )
        self.field_data = lambda: MockFieldData(
            MockLocalObjectDataExtractor._session_data
        )
        self.id = lambda: 1


def test_field_api():
    pyvista_graphics = Graphics(session=None)
    contour1 = pyvista_graphics.Contours["contour-1"]
    field_info = contour1._data_extractor.field_info()
    field_data = contour1._data_extractor.field_data()

    surfaces_id = [
        v["surface_id"][0] for k, v in field_info.get_surfaces_info().items()
    ]

    field_data.add_get_surfaces_request(
        surfaces_id[:1],
        provide_vertices=True,
        provide_faces_centroid=True,
        provide_faces=False,
    )
    field_data.add_get_scalar_fields_request(
        surfaces_id[:1], "temperature", True
    )
    field_data.add_get_scalar_fields_request(
        surfaces_id[:1], "temperature", False
    )
    fields = field_data.get_fields()

    surface_tag = 0
    vertices = fields[surface_tag][surfaces_id[0]]["vertices"]
    centroid = fields[surface_tag][surfaces_id[0]]["centroid"]

    node_location_tag = 4
    node_data = fields[node_location_tag][surfaces_id[0]]["temperature"]
    element_location_tag = 2
    element_data = fields[element_location_tag][surfaces_id[0]]["temperature"]

    assert len(vertices) == len(node_data) * 3
    assert len(centroid) == len(element_data) * 3


def test_graphics_operations():
    pyvista_graphics1 = Graphics(session=None)
    pyvista_graphics2 = Graphics(session=None)
    contour1 = pyvista_graphics1.Contours["contour-1"]
    contour2 = pyvista_graphics2.Contours["contour-2"]

    # create
    assert pyvista_graphics1 is not pyvista_graphics2
    assert pyvista_graphics1.Contours is pyvista_graphics2.Contours
    assert list(pyvista_graphics1.Contours) == ["contour-1", "contour-2"]

    contour2.field = "temperature"
    contour2.surfaces_list = contour2.surfaces_list.allowed_values

    contour1.field = "pressure"
    contour1.surfaces_list = contour2.surfaces_list.allowed_values[0]

    # copy
    pyvista_graphics2.Contours["contour-3"] = contour1()
    contour3 = pyvista_graphics2.Contours["contour-3"]
    assert contour3() == contour1()

    # update
    contour3.update(contour2())
    assert contour3() == contour2()

    # del
    assert list(pyvista_graphics1.Contours) == [
        "contour-1",
        "contour-2",
        "contour-3",
    ]
    del pyvista_graphics1.Contours["contour-3"]
    assert list(pyvista_graphics1.Contours) == ["contour-1", "contour-2"]


def test_contour_object():

    pyvista_graphics = Graphics(session=None)
    contour1 = pyvista_graphics.Contours["contour-1"]
    field_info = contour1._data_extractor.field_info()

    # Surfaces allowed values should be all surfaces.
    assert contour1.surfaces_list.allowed_values == list(
        field_info.get_surfaces_info().keys()
    )

    # Invalid surface should raise exception.
    with pytest.raises(ValueError) as value_error:
        contour1.surfaces_list = "surface_does_not_exist"

    # Invalid surface should raise exception.
    with pytest.raises(ValueError) as value_error:
        contour1.surfaces_list = ["surface_does_not_exist"]

    # Should accept all valid surface.
    contour1.surfaces_list = contour1.surfaces_list.allowed_values

    # Field allowed values should be all fields.
    assert contour1.field.allowed_values == [
        v["solver_name"] for k, v in field_info.get_fields_info().items()
    ]

    # Important. Because there is no type checking so following passes.
    contour1.field = [contour1.field.allowed_values[0]]

    # Should accept all valid fields.
    contour1.field = contour1.field.allowed_values[0]

    # Invalid field should raise exception.
    with pytest.raises(ValueError) as value_error:
        contour1.field = "field_does_not_exist"

    # Important. Because there is no type checking so following test passes.
    contour1.node_values = "value should be boolean"

    # changing filled to False or setting clip_to_range should set node_value
    # to True.
    contour1.node_values = False
    assert contour1.node_values() == False
    contour1.filled = False
    assert contour1.node_values() == True
    # node value can not be set to False because Filled is False
    contour1.node_values = False
    assert contour1.node_values() == True

    contour1.filled = True
    contour1.node_values = False
    assert contour1.node_values() == False
    contour1.range.option = "auto-range-off"
    contour1.range.auto_range_off.clip_to_range = True
    assert contour1.node_values() == True

    contour1.range.option = "auto-range-on"
    assert contour1.range.auto_range_off is None

    contour1.range.option = "auto-range-off"
    assert contour1.range.auto_range_on is None

    # Range should adjust to min/max of node field values.
    contour1.node_values = True
    contour1.field = "temperature"
    surfaces_id = [
        v["surface_id"][0]
        for k, v in field_info.get_surfaces_info().items()
        if k in contour1.surfaces_list()
    ]

    range = field_info.get_range(
        contour1.field(), contour1.node_values(), surfaces_id
    )
    assert range[0] == pytest.approx(contour1.range.auto_range_off.minimum())
    assert range[1] == pytest.approx(contour1.range.auto_range_off.maximum())

    # Range should adjust to min/max of cell field values.
    contour1.node_values = False
    range = field_info.get_range(
        contour1.field(), contour1.node_values(), surfaces_id
    )
    assert range[0] == pytest.approx(contour1.range.auto_range_off.minimum())
    assert range[1] == pytest.approx(contour1.range.auto_range_off.maximum())

    # Range should adjust to min/max of node field values
    contour1.field = "pressure"
    range = field_info.get_range(
        contour1.field(), contour1.node_values(), surfaces_id
    )
    assert range[0] == pytest.approx(contour1.range.auto_range_off.minimum())
    assert range[1] == pytest.approx(contour1.range.auto_range_off.maximum())


def test_vector_object():

    pyvista_graphics = Graphics(session=None)
    vector1 = pyvista_graphics.Vectors["contour-1"]
    field_info = vector1._data_extractor.field_info()

    assert vector1.surfaces_list.allowed_values == list(
        field_info.get_surfaces_info().keys()
    )

    with pytest.raises(ValueError) as value_error:
        vector1.surfaces_list = "surface_does_not_exist"

    with pytest.raises(ValueError) as value_error:
        vector1.surfaces_list = ["surface_does_not_exist"]

    vector1.surfaces_list = vector1.surfaces_list.allowed_values

    vector1.range.option = "auto-range-on"
    assert vector1.range.auto_range_off is None

    vector1.range.option = "auto-range-off"
    assert vector1.range.auto_range_on is None

    surfaces_id = [
        v["surface_id"][0]
        for k, v in field_info.get_surfaces_info().items()
        if k in vector1.surfaces_list()
    ]

    range = field_info.get_range("velocity-magnitude", False)
    assert range == pytest.approx(
        [
            vector1.range.auto_range_off.minimum(),
            vector1.range.auto_range_off.maximum(),
        ]
    )


def test_surface_object():

    pyvista_graphics = Graphics(session=None)
    surf1 = pyvista_graphics.Surfaces["surf-1"]
    field_info = surf1._data_extractor.field_info()

    surf1.surface.type = "iso-surface"
    assert surf1.surface.plane_surface is None
    surf1.surface.type = "plane-surface"
    assert surf1.surface.iso_surface is None

    surf1.surface.plane_surface.creation_method = "xy-plane"
    assert surf1.surface.plane_surface.yz_plane is None
    assert surf1.surface.plane_surface.zx_plane is None

    surf1.surface.type = "iso-surface"
    iso_surf = surf1.surface.iso_surface

    assert iso_surf.field.allowed_values == [
        v["solver_name"] for k, v in field_info.get_fields_info().items()
    ]

    # Important. Because there is no type checking so following test passes.
    iso_surf.field = [iso_surf.field.allowed_values[0]]

    # Incorrect field should throw exception
    with pytest.raises(ValueError) as value_error:
        iso_surf.field = "field_does_not_exist"

    # Iso surface value should automatically update upon change in field.
    iso_surf.field = "temperature"
    range = field_info.get_range(iso_surf.field(), True)
    assert range[0] == pytest.approx(iso_surf.iso_value())

    # Setting out of range should throw exception
    with pytest.raises(ValueError) as value_error:
        iso_surf.iso_value = range[1] + 0.001

    with pytest.raises(ValueError) as value_error:
        iso_surf.iso_value = range[0] - 0.001

    # Iso surface value should automatically update upon change in field.
    iso_surf.field = "pressure"
    range = field_info.get_range(iso_surf.field(), True)
    assert range[0] == pytest.approx(iso_surf.iso_value())

    # New surface should be in allowed values for graphics.
    cont1 = pyvista_graphics.Contours["surf-1"]
    assert "surf-1" in cont1.surfaces_list.allowed_values

    # New surface is not available in allowed values for plots.
    matplotlib_plots = Plots(session=None)
    p1 = matplotlib_plots.XYPlots["p-1"]
    assert "surf-1" not in p1.surfaces_list.allowed_values

    # With local surface provider it becomes available.
    local_surfaces_provider = Graphics(session=None).Surfaces
    matplotlib_plots = Plots(
        session=None, local_surfaces_provider=local_surfaces_provider
    )
    assert "surf-1" in p1.surfaces_list.allowed_values


def test_create_plot_objects():
    matplotlib_plots1 = Plots(session=None)
    matplotlib_plots2 = Plots(session=None)
    matplotlib_plots1.XYPlots["p-1"]
    matplotlib_plots2.XYPlots["p-2"]

    assert matplotlib_plots1 is not matplotlib_plots2
    assert matplotlib_plots1.XYPlots is matplotlib_plots2.XYPlots
    assert list(matplotlib_plots1.XYPlots) == ["p-1", "p-2"]


def test_xyplot_object():

    matplotlib_plots = Plots(session=None)
    p1 = matplotlib_plots.XYPlots["p-1"]
    field_info = p1._data_extractor.field_info()

    assert p1.surfaces_list.allowed_values == list(
        field_info.get_surfaces_info().keys()
    )

    with pytest.raises(ValueError) as value_error:
        p1.surfaces_list = "surface_does_not_exist"

    with pytest.raises(ValueError) as value_error:
        p1.surfaces_list = ["surface_does_not_exist"]

    p1.surfaces_list = p1.surfaces_list.allowed_values

    assert p1.y_axis_function.allowed_values == [
        v["solver_name"] for k, v in field_info.get_fields_info().items()
    ]

    # Important. Because there is no type checking so following passes.
    p1.y_axis_function = [p1.y_axis_function.allowed_values[0]]

    p1.y_axis_function = p1.y_axis_function.allowed_values[0]

    with pytest.raises(ValueError) as value_error:
        p1.y_axis_function = "field_does_not_exist"
