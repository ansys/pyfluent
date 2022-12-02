import pytest
from util.solver_workflow import new_solver_session  # noqa: F401

from ansys.fluent.core import examples
from ansys.fluent.core.services.field_data import (
    ScalarFieldNameError,
    ScalarFieldUnavailable,
    SurfaceNameError,
)


def test_field_data_errors(new_solver_session) -> None:
    solver = new_solver_session
    import_filename = examples.download_file(
        "mixing_elbow.msh.h5", "pyfluent/mixing_elbow"
    )

    with pytest.raises(ScalarFieldNameError) as fne:
        solver.field_data.get_scalar_field_data(
            field_name="y-face-area", surface_ids=[0]
        )
    assert fne.value.field_name == "y-face-area"

    with pytest.raises(ScalarFieldNameError) as fne:
        solver.field_data.get_scalar_field_data(
            field_name="partition-neighbors", surface_ids=[0]
        )
    assert fne.value.field_name == "partition-neighbors"

    solver.file.read(file_type="case", file_name=import_filename)

    with pytest.raises(ScalarFieldUnavailable) as fnu:
        solver.field_data.get_scalar_field_data(field_name="density", surface_ids=[0])
    assert fnu.value.field_name == "density"

    y_face_area = solver.field_data.get_scalar_field_data(
        field_name="y-face-area", surface_ids=[0]
    )
    assert y_face_area and isinstance(y_face_area, dict)

    partition_neighbors = solver.field_data.get_scalar_field_data(
        field_name="partition-neighbors", surface_ids=[0]
    )
    assert partition_neighbors and isinstance(partition_neighbors, dict)

    # Initialize flow field
    solver.solution.initialization.hybrid_initialize()

    # Get field data object
    field_data = solver.field_data

    with pytest.raises(SurfaceNameError) as sne:
        solver.field_data.get_scalar_field_data(
            field_name="density", surface_name="bob"
        )
    assert sne.value.surface_name == "bob"

    with pytest.raises(ScalarFieldNameError) as fne:
        solver.field_data.get_scalar_field_data(field_name="xdensity", surface_ids=[0])
    assert fne.value.field_name == "xdensity"
