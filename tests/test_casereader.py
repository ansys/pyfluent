from os.path import dirname, join
import pathlib
import shutil

import pytest

from ansys.fluent.core import examples
from ansys.fluent.core.filereader.casereader import CaseReader, _get_processed_string


def call_casereader(case_filepath: str = None, project_filepath: str = None):

    reader = CaseReader(case_filepath=case_filepath, project_filepath=project_filepath)

    input_parameters = reader.input_parameters()

    assert reader.precision() == 2

    assert reader.num_dimensions() == 3

    assert len(input_parameters) == 4

    input_parameter_dict = {p.name: p.value for p in input_parameters}

    assert input_parameter_dict["inlet1_temp"] == "300 [K]"

    assert input_parameter_dict["inlet1_vel"] == "1 [m/s]"

    assert input_parameter_dict["inlet2_temp"] == "350 [K]"

    assert input_parameter_dict["inlet2_vel"] == "1 [m/s]"

    output_parameters = reader.output_parameters()

    assert len(output_parameters) == 2

    output_parameter_dict = {p.name: p.units for p in output_parameters}
    assert {
        "outlet-temp-avg-op": "K",
        "outlet-vel-avg-op": "m s^-1",
    } == output_parameter_dict


def test_casereader_h5():
    call_casereader(
        case_filepath=examples.download_file(
            "Static_Mixer_Parameters.cas.h5", "pyfluent/static_mixer"
        )
    )


def test_casereader_binary_cas():
    call_casereader(
        case_filepath=examples.download_file(
            "Static_Mixer_Parameters_legacy_binary.cas", "pyfluent/static_mixer"
        )
    )


def test_casereader_binary_gz():
    call_casereader(
        case_filepath=examples.download_file(
            "Static_Mixer_Parameters_legacy_binary.cas.gz", "pyfluent/static_mixer"
        )
    )


def test_casereader_text_cas():
    call_casereader(
        case_filepath=examples.download_file(
            "Static_Mixer_Parameters_legacy_text.cas", "pyfluent/static_mixer"
        )
    )


def test_casereader_text_gz():
    call_casereader(
        case_filepath=examples.download_file(
            "Static_Mixer_Parameters_legacy_text.cas.gz", "pyfluent/static_mixer"
        )
    )


def create_dir_structure_locally(copy_1: bool = False, copy_2: bool = False):
    # Copying from and then creating the entire directory structure locally
    case_file_dir = (
        "Static_Mixer_Parameter_project_file/"
        "Static_Mixer_Parameters.cffdb/Static_Mixer_Parameters-Solve"
    )
    case_filepath = examples.download_file(
        "Static_Mixer_Parameters.cas.h5", "pyfluent/static_mixer/" + case_file_dir
    )
    prj_dir = join(dirname(case_filepath), case_file_dir)
    pathlib.Path(prj_dir).mkdir(parents=True, exist_ok=True)
    if copy_1:
        shutil.copy2(case_filepath, prj_dir)
    if copy_2:
        case_filepath_2 = examples.download_file(
            "Static_Mixer_Parameters_legacy_binary.cas.gz", "pyfluent/static_mixer"
        )
        shutil.copy2(case_filepath_2, prj_dir)
    prj_file_dir = "Static_Mixer_Parameter_project_file"
    prj_file = r"Static_Mixer_Parameters.flprj"
    prj_filepath = examples.download_file(
        prj_file, "pyfluent/static_mixer/" + prj_file_dir
    )
    prj_file_dir = join(dirname(prj_filepath), prj_file_dir)
    shutil.copy2(prj_filepath, prj_file_dir)

    return join(prj_file_dir, prj_file)


def test_casereader_h5_for_project_directory():
    project_filepath = create_dir_structure_locally(copy_1=True)
    call_casereader(project_filepath=project_filepath)
    shutil.rmtree(dirname(project_filepath))


def test_processed_string():
    assert (
        _get_processed_string(b"Hello! World (37 ( Get this part of the string ))")
        == "(37 ( Get this part of the string ))"
    )


def test_casereader_no_file():
    with pytest.raises(RuntimeError):
        call_casereader("no_file.cas.h5")


def test_casereader_with_both_project_and_case_file():
    with pytest.raises(RuntimeError):
        call_casereader(
            case_filepath="case_file.cas.h5", project_filepath="project.flprj"
        )


def test_casereader_for_project_directory_no_case_file():
    project_filepath = create_dir_structure_locally()
    with pytest.raises(RuntimeError):
        call_casereader(project_filepath=project_filepath)
    shutil.rmtree(dirname(project_filepath))


def test_casereader_for_project_directory_dual_case_file():
    project_filepath = create_dir_structure_locally(copy_1=True, copy_2=True)
    with pytest.raises(RuntimeError):
        call_casereader(project_filepath=project_filepath)
    shutil.rmtree(dirname(project_filepath))


def test_casereader_for_project_directory_invalid_project_file():
    with pytest.raises(RuntimeError):
        call_casereader(project_filepath="project.flprx")
