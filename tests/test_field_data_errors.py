import pytest
from util.solver_workflow import new_solver_session  # noqa: F401

from ansys.fluent.core import examples
from ansys.fluent.core.services.field_data import FieldNameError, SurfaceNameError


def test_field_data_errors(new_solver_session) -> None:
    solver = new_solver_session
    import_filename = examples.download_file(
        "mixing_elbow.msh.h5", "pyfluent/mixing_elbow"
    )
    solver.file.read(file_type="case", file_name=import_filename)

    # Initialize flow field
    solver.solution.initialization.hybrid_initialize()

    # Get field data object
    field_data = solver.field_data

    with pytest.raises(SurfaceNameError) as sne:
        solver.field_data.get_scalar_field_data(
            field_name="entropy", surface_name="bob"
        )
    assert sne.value.surface_name == "bob"

    with pytest.raises(FieldNameError) as fne:
        solver.field_data.get_scalar_field_data(field_name="bentropy", surface_ids=[0])
    assert fne.value.field_name == "bentropy"
