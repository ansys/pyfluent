from ansys.fluent.core import examples
from ansys.fluent.core.filereader.casereader import CaseReader


def test_casereader():

    case_filepath = examples.download_file(
        "Static_Mixer_Parameters.cas.h5", "pyfluent/static_mixer"
    )

    reader = CaseReader(hdf5_case_filepath=case_filepath)

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

    assert {"outlet-temp-avg-op", "outlet-vel-avg-op"} == {
        p.name for p in output_parameters
    }
