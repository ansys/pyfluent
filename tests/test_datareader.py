from ansys.fluent.core import examples
from ansys.fluent.core.filereader.case_file import CaseFile
from ansys.fluent.core.filereader.data_file import DataFile


def test_data_reader_for_single_phase():
    case_file_name = examples.download_file(
        "elbow1.cas.h5", "pyfluent/file_session", return_without_path=False
    )

    data_file_name = examples.download_file(
        "elbow1.dat.h5", "pyfluent/file_session", return_without_path=False
    )

    reader = DataFile(
        data_file_name=data_file_name,
        case_file_handle=CaseFile(case_file_name=case_file_name),
    )

    assert reader.case_file == "elbow1.cas.h5"

    assert len(reader.variables()) == 80

    assert reader.get_phases() == ["phase-1"]

    assert len(reader.get_face_variables("phase-1")) == 30

    assert len(reader.get_cell_variables("phase-1")) == 14

    assert reader.get_cell_variables("phase-1") == [
        "SV_BF_V",
        "SV_D",
        "SV_DENSITY",
        "SV_H",
        "SV_K",
        "SV_LORENTZ_FORCE",
        "SV_MU_LAM",
        "SV_MU_T",
        "SV_P",
        "SV_T",
        "SV_U",
        "SV_V",
        "SV_W",
        "",
    ]

    assert len(reader.get_face_scalar_field_data("phase-1", "SV_DENSITY", 3)) == 3630

    assert len(reader.get_face_vector_field_data("phase-1", 3)) == 10890


def test_data_reader_for_multi_phase():
    case_file_name = examples.download_file(
        "mixing_elbow_mul_ph.cas.h5",
        "pyfluent/file_session",
        return_without_path=False,
    )
    data_file_name = examples.download_file(
        "mixing_elbow_mul_ph.dat.h5",
        "pyfluent/file_session",
        return_without_path=False,
    )

    reader = DataFile(
        data_file_name=data_file_name,
        case_file_handle=CaseFile(case_file_name=case_file_name),
    )  # Instantiate a DataFile class

    assert reader.case_file == "mixing_elbow_mul_ph.cas.h5"

    assert len(reader.variables()) == 80

    assert reader.get_phases() == [
        "phase-1",
        "phase-2",
        "phase-3",
        "phase-4",
    ]

    assert len(reader.get_face_variables("phase-1")) == 23

    assert len(reader.get_face_variables("phase-3")) == 13

    assert len(reader.get_cell_variables("phase-2")) == 14

    assert reader.get_cell_variables("phase-2") == [
        "SV_BF_V",
        "SV_DENSITY",
        "SV_DENSITY_M1",
        "SV_MU_LAM",
        "SV_MU_T",
        "SV_U",
        "SV_U_M1",
        "SV_V",
        "SV_VOF",
        "SV_VOF_M1",
        "SV_V_M1",
        "SV_W",
        "SV_W_M1",
        "",
    ]

    assert len(reader.get_face_scalar_field_data("phase-1", "SV_DENSITY", 33)) == 268
