from os.path import dirname, join
import pathlib
import shutil

import pytest

from ansys.fluent.core import examples
from ansys.fluent.core.filereader import lispy
from ansys.fluent.core.filereader.casereader import (
    CaseReader,
    InputParameter,
    _get_processed_string,
)


def call_casereader(
    case_filepath: str = None, project_filepath: str = None, expected: dict = None
):
    reader = CaseReader(case_filepath=case_filepath, project_filepath=project_filepath)
    if expected is not None:
        assert reader.precision() == expected["precision"]
        assert reader.num_dimensions() == expected["num_dimensions"]
        assert reader.iter_count() == expected["iter_count"]
        assert {
            p.name: (p.numeric_value, p.units) for p in reader.input_parameters()
        } == expected["input_parameters"]
        assert {p.name: p.units for p in reader.output_parameters()} == expected[
            "output_parameters"
        ]


def call_casereader_static_mixer(
    case_filepath: str = None, project_filepath: str = None
):
    call_casereader(
        case_filepath=case_filepath,
        project_filepath=project_filepath,
        expected=dict(
            precision=2,
            num_dimensions=3,
            iter_count=100,
            input_parameters=dict(
                inlet1_temp=(300, "K"),
                inlet1_vel=(1, "m/s"),
                inlet2_temp=(350, "K"),
                inlet2_vel=(1, "m/s"),
            ),
            output_parameters={
                "outlet-temp-avg-op": "K",
                "outlet-vel-avg-op": "m s^-1",
            },
        ),
    )


def static_mixer_file():
    return examples.download_file(
        "Static_Mixer_Parameters.cas.h5", "pyfluent/static_mixer"
    )


def test_casereader_static_mixer_h5():
    call_casereader_static_mixer(case_filepath=static_mixer_file())


def test_casereader_static_mixer_binary_cas():
    call_casereader_static_mixer(
        case_filepath=examples.download_file(
            "Static_Mixer_Parameters_legacy_binary.cas", "pyfluent/static_mixer"
        )
    )


def test_casereader_static_mixer_binary_gz():
    call_casereader_static_mixer(
        case_filepath=examples.download_file(
            "Static_Mixer_Parameters_legacy_binary.cas.gz", "pyfluent/static_mixer"
        )
    )


def test_casereader_static_mixer_text_cas():
    call_casereader_static_mixer(
        case_filepath=examples.download_file(
            "Static_Mixer_Parameters_legacy_text.cas", "pyfluent/static_mixer"
        )
    )


def test_casereader_static_mixer_text_gz():
    call_casereader_static_mixer(
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


def test_processed_string():
    assert (
        _get_processed_string(b"Hello! World (37 ( Get this part of the string ))")
        == "(37 ( Get this part of the string ))"
    )


def test_casereader_no_file():
    with pytest.raises(FileNotFoundError):
        call_casereader("no_file.cas.h5")


def test_casereader_with_both_project_and_case_file():
    with pytest.raises(RuntimeError):
        call_casereader(
            case_filepath="case_file.cas.h5", project_filepath="project.flprj"
        )


def test_casereader_for_project_directory_invalid_project_file():
    with pytest.raises(FileNotFoundError):
        call_casereader(project_filepath="project.flprx")


def test_case_reader_with_bad_data_to_be_skipped_and_input_parameters_labeled_differently():
    call_casereader(
        case_filepath=examples.download_file(
            "mixer-ran_2019r3.cas.gz", "pyfluent/optislang"
        ),
        expected=dict(
            precision=1,
            num_dimensions=3,
            iter_count=25,
            input_parameters=dict(
                swirl_max_hot=(0.1, "m s^-1"),
                vel_hot=(0.1, "m s^-1"),
                vel_cold=(0.1, "m s^-1"),
                swirl_max_cold=(0.1, "m s^-1"),
            ),
            output_parameters={
                "p2-op": "kg m^-1 s^-2",
                "t-dev-op": "K",
                "p1-op": "kg m^-1 s^-2",
                "ave_temp_out": "K",
            },
        ),
    )


def test_case_reader_get_rp_and_config_vars():
    reader = CaseReader(case_filepath=static_mixer_file())
    rp_vars = reader.rp_vars()
    assert rp_vars
    assert hasattr(rp_vars, "__getitem__")
    config_vars = reader.config_vars()
    assert config_vars
    assert hasattr(config_vars, "__getitem__")
    assert config_vars["rp-3d?"] is True
    assert reader.config_var("rp-3d?") is True
    assert reader.config_var.rp_3d__q() is True
    assert reader.rp_var.smooth_mesh.niter() == 4
    assert reader.rp_var.pressure.output_dpdt__q() is True
    assert len(reader.rp_var.context.map_r17__plus()) == 53
    assert reader.rp_var.defaults.pre_r19__dot0_early__q() is False
    with pytest.raises(BaseException):
        reader.rp_var.defaults.pre_r19__dot0_early()

    with pytest.raises(ValueError) as msg:
        reader.config_var("rp-3d")

    assert (
        msg.value.args[0] == "rp-3d is not an allowed config-vars name.\n"
        "The most similar names are: rp-3d?, rp-des?."
    )


def test_case_reader_input_parameter():
    number = InputParameter(raw_data=(("name", "n"), ("definition", "12.4")))

    assert number.name == "n"
    assert number.units == ""
    assert number.numeric_value == 12.4
    assert number.value == "12.4"

    length = InputParameter(raw_data=(("name", "x"), ("definition", "12.4 [m]")))

    assert length.name == "x"
    assert length.units == "m"
    assert length.numeric_value == 12.4
    assert length.value == "12.4 [m]"

    momentum = InputParameter(
        raw_data=(("name", "p"), ("definition", "12.4 [kg m s^-1]"))
    )

    assert momentum.name == "p"
    assert momentum.units == "kg m s^-1"
    assert momentum.numeric_value == 12.4
    assert momentum.value == "12.4 [kg m s^-1]"

    velocity = InputParameter(raw_data=(("name", "v"), ("definition", "2[m/s]")))

    assert velocity.name == "v"
    assert velocity.units == "m/s"
    assert velocity.numeric_value == 2
    assert velocity.value == "2 [m/s]"


def test_lispy_for_multiline_string():
    assert lispy.parse('(define x "abc\ndef")') == ["define", "x", '"abc\ndef"']
