import os

import pytest
from util.fixture_fluent import download_input_file


@pytest.mark.solve
@pytest.mark.fluent_231
def test_pro_parameters(launch_fluent_solver_3ddp_t2):
    if not os.path.exists("out"):
        os.mkdir("out")
    solver = launch_fluent_solver_3ddp_t2
    input_type, input_name = download_input_file(
        "pyfluent/static_mixer", "StaticMixer.msh"
    )
    solver.file.read(file_type=input_type, file_name=input_name)
    solver.setup.models.energy = {"enabled": True}
    solver.setup.models.viscous.model = "k-epsilon"
    assert solver.setup.models.viscous.model() == "k-epsilon"
    solver.setup.models.viscous.k_epsilon_model = "realizable"
    assert solver.setup.models.viscous.k_epsilon_model() == "realizable"
    solver.setup.named_expressions["inlet1_temp"] = {}
    solver.setup.named_expressions["inlet1_temp"] = {"definition": "300 [K]"}
    solver.setup.named_expressions["inlet1_temp"] = {"input_parameter": True}
    assert solver.setup.named_expressions["inlet1_temp"]() == {
        "name": "inlet1_temp",
        "definition": "300 [K]",
        "description": "",
        "input_parameter": True,
        "output_parameter": False,
    }
    solver.setup.named_expressions["inlet2_temp"] = {}
    solver.setup.named_expressions["inlet2_temp"] = {
        "definition": "350 [K]",
        "input_parameter": True,
    }
    solver.setup.named_expressions["inlet1_vel"] = {}
    solver.setup.named_expressions["inlet1_vel"] = {
        "definition": "5 [m/s]",
        "input_parameter": True,
    }
    solver.setup.named_expressions["inlet2_vel"] = {}
    solver.setup.named_expressions["inlet2_vel"] = {
        "definition": "10 [m/s]",
        "input_parameter": True,
    }
    assert solver.setup.named_expressions["inlet2_vel"]() == {
        "name": "inlet2_vel",
        "definition": "10 [m/s]",
        "description": "",
        "input_parameter": True,
        "output_parameter": False,
    }
    solver.execute_tui(r"""/define/boundary-conditions/list-zones """)
    solver.execute_tui(r"""/define/boundary-conditions/zone-type in1 velocity-inlet """)
    solver.execute_tui(r"""/define/boundary-conditions/zone-type in2 velocity-inlet """)
    solver.setup.boundary_conditions.velocity_inlet["in1"] = {
        "vmag": "inlet1_vel",
        "t": "inlet1_temp",
    }
    solver.setup.boundary_conditions.velocity_inlet["in2"] = {
        "vmag": "inlet2_vel",
        "t": "inlet2_temp",
    }
    solver.solution.report_definitions.surface["outlet-temp-avg"] = {}
    solver.solution.report_definitions.surface[
        "outlet-temp-avg"
    ].report_type = "surface-massavg"
    solver.solution.report_definitions.surface["outlet-temp-avg"] = {
        "field": "temperature",
        "surface_names": ["outlet"],
    }
    solver.solution.monitor.report_files["outlet-temp-avg-rfile"] = {}
    solver.solution.monitor.report_files["outlet-temp-avg-rfile"] = {
        "report_defs": ["outlet-temp-avg"],
        "print": True,
        "file_name": r"out\\outlet-temp-avg-rfile.out",
    }
    solver.solution.monitor.report_plots["outlet-temp-avg-rplot"] = {}
    solver.solution.monitor.report_plots["outlet-temp-avg-rplot"] = {
        "report_defs": ["outlet-temp-avg"],
        "print": True,
    }
    solver.execute_tui(
        r"""/define/parameters/output-parameters/create report-definition outlet-temp-avg """
    )
    solver.execute_tui(r"""/solve/initialize/compute-defaults/velocity-inlet in1 """)
    solver.solution.run_calculation.iter_count = 350
    assert solver.solution.run_calculation.iter_count() == 350
    solver.solution.run_calculation.iterate(number_of_iterations=350)
    solver.execute_tui(r"""/display/surface/plane-surface plane-4 xy-plane 1. """)
    solver.results.graphics.lic["lic-temp"] = {}
    solver.results.graphics.lic["lic-temp"] = {
        "field": "temperature",
        "surfaces_list": ["plane-4"],
        "texture_size": 2,
    }
    solver.results.graphics.lic.display(object_name="lic-temp")
    solver.file.write(file_type="case-data", file_name="out/StaticMixer.cas.h5")
    solver.execute_tui(r"""(proc-stats)  """)
    solver.execute_tui(r"""(display "testing finished")  """)
    solver.exit()
