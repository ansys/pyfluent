from os.path import dirname, join
import pathlib
import shutil

from ansys.fluent.core import examples
from ansys.fluent.core.filereader.casereader import CaseReader, _get_processed_string


def call_casereader(case_filepath: str):

    reader = CaseReader(case_filepath=case_filepath)

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
        examples.download_file(
            "Static_Mixer_Parameters.cas.h5", "pyfluent/static_mixer"
        )
    )


def test_casereader_binary_cas():
    call_casereader(
        examples.download_file(
            "Static_Mixer_Parameters_legacy_binary.cas", "pyfluent/static_mixer"
        )
    )


def test_casereader_binary_gz():
    call_casereader(
        examples.download_file(
            "Static_Mixer_Parameters_legacy_binary.cas.gz", "pyfluent/static_mixer"
        )
    )


def test_casereader_text_cas():
    call_casereader(
        examples.download_file(
            "Static_Mixer_Parameters_legacy_text.cas", "pyfluent/static_mixer"
        )
    )


def test_casereader_text_gz():
    call_casereader(
        examples.download_file(
            "Static_Mixer_Parameters_legacy_text.cas.gz", "pyfluent/static_mixer"
        )
    )


def test_casereader_h5_for_project_directory():

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
    shutil.copy(case_filepath, prj_dir)
    prj_file_dir = "Static_Mixer_Parameter_project_file"
    prj_file = r"Static_Mixer_Parameters.flprj"
    prj_filepath = examples.download_file(
        prj_file, "pyfluent/static_mixer/" + prj_file_dir
    )
    prj_file_dir = join(dirname(prj_filepath), prj_file_dir)
    shutil.copy(prj_filepath, prj_file_dir)

    call_casereader(join(prj_file_dir, prj_file))


def test_processed_string():
    assert (
        _get_processed_string(b"Hello! World (37 ( Get this part of the string ))")
        == "(37 ( Get this part of the string ))"
    )


def test_casereader_no_file():
    throws = False
    try:
        call_casereader("no_file.cas.h5")
    except RuntimeError:
        throws = True
    assert throws
