import os

import pytest
from util.fixture_fluent import download_input_file


@pytest.mark.solve
@pytest.mark.fluent_231
def test_pro_exp(launch_fluent_solver_3ddp_t2):
    solver = launch_fluent_solver_3ddp_t2
    _THIS_DIR = os.path.dirname(__file__)
    _EXP_FILE = os.path.join(_THIS_DIR, "inlet_exp.tsv")
    input_type, input_name = download_input_file(
        "pyfluent/exhaust_manifold", "manifold_expressions.cas.gz"
    )
    solver.execute_tui(r"""/file/start-transcript "prolic_exp_s1.trn" """)
    solver.file.read(file_type=input_type, file_name=input_name)
    assert solver._root.get_attr("active?")
    assert solver.check_health() == "SERVING"
    solver.execute_tui(r"""/print-license-usage """)
    solver.execute_tui(
        r'''/define/named-expressions/import-from-tsv "%s"''' % _EXP_FILE
    )
    solver.setup.named_expressions["temp_inlet_1"] = {}
    solver.setup.named_expressions["temp_inlet_1"] = {"definition": "-1 [C]"}
    assert solver.setup.named_expressions["temp_inlet_1"].definition() == "-1 [C]"
    solver.setup.boundary_conditions.velocity_inlet["inlet2"] = {
        "vmag": "IF(Maximum(TotalTemperature,['interior-part-heatsource'])> 310 [K], 1 [m/s], 0.01[m/s])",
        "t": 300.0,
        "turb_intensity": 0.04999999888241,
    }
    solver.setup.boundary_conditions.velocity_inlet["inlet1"] = {
        "vmag": "IF(avg_vel_inlet2>=0.5 [m/s], 1 [m/s], 0.2 [m/s])",
        "t": "temp_inlet_1",
        "turb_intensity": 0.04999999888241,
    }
    assert solver.setup.boundary_conditions.velocity_inlet["inlet2"].vmag() == {
        "option": "value",
        "value": "IF(Maximum(TotalTemperature,['interior-part-heatsource'])> 310 [K], 1 [m/s], 0.01[m/s])",
    }
    assert solver.setup.boundary_conditions.velocity_inlet["inlet1"].vmag() == {
        "option": "value",
        "value": "IF(avg_vel_inlet2>=0.5 [m/s], 1 [m/s], 0.2 [m/s])",
    }
    solver.setup.boundary_conditions.velocity_inlet["inlet3"] = {
        "vmag": "IF(AND((Maximum(TotalTemperature,['interior-part-heatsource'])> 310 [K]),(Average(VelocityMagnitude,['inlet1'])== 1 [m/s])), 1 [m/s], 0.2 [m/s])",
        "turb_intensity": 0.04999999888241,
    }
    assert solver.setup.boundary_conditions.velocity_inlet["inlet3"].vmag() == {
        "option": "value",
        "value": "IF(AND((Maximum(TotalTemperature,['interior-part-heatsource'])> 310 [K]),(Average(VelocityMagnitude,['inlet1'])== 1 [m/s])), 1 [m/s], 0.2 [m/s])",
    }
    solver.solution.initialization.standard_initialize()
    solver.solution.run_calculation.iterate(number_of_iterations=150)
    solver.results.report.report_menu.surface_integrals(
        report_type="area-weighted-avg",
        surface_id=["inlet1"],
        cell_report="temperature",
        write_to_file=True,
        file_name="temp_inlet_2.srp",
    )
    solver.file.write(file_type="case-data", file_name="exp_manifold_reduction")
    solver.mesh.check()
    solver.mesh.quality()
    solver.execute_tui(r"""/define/set-unit-system si """)
    solver.execute_tui(r"""/define/units length m """)
    solver.mesh.size_info()
    solver.execute_tui(r"""/define/models/steady? """)
    solver.setup.general.solver.type = "pressure-based"
    solver.execute_tui(r"""(proc-stats)  """)
    solver.execute_tui(r"""(display "testing finished")  """)
    solver.exit()
