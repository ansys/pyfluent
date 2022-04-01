from typing import Dict, List, Optional
import pickle
import pytest
from pathlib import Path
from ansys.fluent.post.pyvista import Graphics
from ansys.fluent.post.matplotlib import Plots


@pytest.fixture(autouse=True)
def patch_mock_data_extractor(mocker) -> None:
    mocker.patch(
        "ansys.fluent.core.meta.LocalObjectDataExtractor",
        MockLocalObjectDataExtractor,
    )


class MockFieldData:
    def __init__(self, solver_data):
        self._session_data = solver_data

    def get_scalar_field(
        self,
        surface_ids: List[int],
        scalar_field: str,
        node_value: Optional[bool] = True,
        boundary_value: Optional[bool] = False,
    ) -> Dict[int, Dict]:
        return {
            surface_id: self._session_data["scalar-field"][scalar_field][
                surface_id
            ]["node_value" if node_value else "cell_value"]
            for surface_id in surface_ids
        }

    def get_vector_field(
        self,
        surface_ids: List[int],
        vector_field: Optional[str] = "velocity",
        scalar_field: Optional[str] = "",
        node_value: Optional[bool] = False,
    ) -> Dict[int, Dict]:
        return {
            surface_id: self._session_data["vector-field"][surface_id]
            for surface_id in surface_ids
        }

    def get_surfaces(
        self, surface_ids: List[int], overset_mesh: bool = False
    ) -> Dict[int, Dict]:
        return {
            surface_id: self._session_data["surfaces"][surface_id]
            for surface_id in surface_ids
        }


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
            pickle_obj = open(
                str(
                    Path(MockLocalObjectDataExtractor._session_dump).resolve()
                ),
                "rb",
            )
            MockLocalObjectDataExtractor._session_data = pickle.load(
                pickle_obj
            )
            pickle_obj.close()
        self.field_info = lambda: MockFieldInfo(
            MockLocalObjectDataExtractor._session_data
        )
        self.field_data = lambda: MockFieldData(
            MockLocalObjectDataExtractor._session_data
        )
        self.id = lambda: 1


def test_create_graphics_objects():
    pyvista_graphics1 = Graphics(session=None)
    pyvista_graphics2 = Graphics(session=None)
    pyvista_graphics1.Contours["contour-1"]
    pyvista_graphics2.Contours["contour-2"]

    assert pyvista_graphics1 is not pyvista_graphics2
    assert pyvista_graphics1.Contours is pyvista_graphics2.Contours
    assert list(pyvista_graphics1.Contours) == ["contour-1", "contour-2"]


def test_contour_object():

    pyvista_graphics = Graphics(session=None)
    contour1 = pyvista_graphics.Contours["contour-1"]
    field_info = contour1._data_extractor.field_info()

    assert contour1.surfaces_list.allowed_values == list(
        field_info.get_surfaces_info().keys()
    )

    with pytest.raises(ValueError) as value_error:
        contour1.surfaces_list = "surface_does_not_exist"

    with pytest.raises(ValueError) as value_error:
        contour1.surfaces_list = ["surface_does_not_exist"]
    contour1.surfaces_list = contour1.surfaces_list.allowed_values

    assert contour1.field.allowed_values == [
        v["solver_name"] for k, v in field_info.get_fields_info().items()
    ]

    # Important. Because there is no type checking so following passes.
    contour1.field = [contour1.field.allowed_values[0]]

    contour1.field = contour1.field.allowed_values[0]
    with pytest.raises(ValueError) as value_error:
        contour1.field = "field_does_not_exist"

    # Important. Because there is no type checking so following passes.
    contour1.node_values = "value should be boolean"

    contour1.range.option = "auto-range-on"
    assert contour1.range.auto_range_off is None

    contour1.range.option = "auto-range-off"
    assert contour1.range.auto_range_on is None

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

    contour1.node_values = False
    range = field_info.get_range(
        contour1.field(), contour1.node_values(), surfaces_id
    )
    assert range[0] == pytest.approx(contour1.range.auto_range_off.minimum())
    assert range[1] == pytest.approx(contour1.range.auto_range_off.maximum())

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
    iso_surf = surf1.surface.iso_surface

    assert iso_surf.field.allowed_values == [
        v["solver_name"] for k, v in field_info.get_fields_info().items()
    ]

    # Important. Because there is no type checking so following passes.
    iso_surf.field = [iso_surf.field.allowed_values[0]]

    with pytest.raises(ValueError) as value_error:
        iso_surf.field = "field_does_not_exist"

    iso_surf.field = "temperature"
    range = field_info.get_range(iso_surf.field(), True)
    assert range[0] == pytest.approx(iso_surf.iso_value())

    with pytest.raises(ValueError) as value_error:
        iso_surf.iso_value = range[1] + 0.001

    with pytest.raises(ValueError) as value_error:
        iso_surf.iso_value = range[0] - 0.001

    iso_surf.field = "pressure"
    range = field_info.get_range(iso_surf.field(), True)
    assert range[0] == pytest.approx(iso_surf.iso_value())

    cont1 = pyvista_graphics.Contours["surf-1"]
    assert "surf-1" in cont1.surfaces_list.allowed_values

    matplotlib_plots = Plots(session=None)
    p1 = matplotlib_plots.XYPlots["p-1"]
    assert "surf-1" not in p1.surfaces_list.allowed_values

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
