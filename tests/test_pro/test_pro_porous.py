import pytest
from util.fixture_fluent import download_input_file


@pytest.mark.solve
@pytest.mark.fluent_231
def test_pro_porous(launch_fluent_solver_3ddp_t2):
    solver = launch_fluent_solver_3ddp_t2
    input_type, input_name = download_input_file(
        "pyfluent/catalytic_converter", "catalytic_converter.msh.h5"
    )
    solver.execute_tui(r"""/file/set-tui-version "23.1" """)
    solver.file.read(file_type=input_type, file_name=input_name)
    solver.mesh.size_info()
    solver.execute_tui(r"""/define/units length mm """)
    solver.setup.models.energy = {"enabled": True, "inlet_diffusion": False}
    solver.execute_tui(r"""/define/materials/copy fluid nitrogen """)
    solver.execute_tui(r"""/define/materials/copy fluid hydrogen """)
    solver.execute_tui(
        r"""/define/materials/change-create nitrogen nit yes constant 1.2 no yes constant 0.1 no no no no no """
    )
    solver.setup.cell_zone_conditions.fluid["fluid:0"] = {"material": "nitrogen"}
    solver.execute_tui(
        r"""/define/boundary-conditions/copy-bc fluid:0 fluid:1 fluid:3 () """
    )
    solver.setup.cell_zone_conditions.fluid["fluid:substrate:1"] = {
        "material": "nitrogen",
        "porous": True,
    }
    solver.execute_tui(
        r"""/define/boundary-conditions/copy-bc fluid:substrate:1 fluid:substrate:2 () """
    )
    solver.setup.boundary_conditions.velocity_inlet["inlet"] = {
        "vmag": 125.0,
        "t": 800.0,
        "ke_spec": "Intensity and Hydraulic Diameter",
        "turb_hydraulic_diam": 0.5,
    }
    solver.setup.boundary_conditions.pressure_outlet["outlet"] = {
        "t0": 800.0,
        "ke_spec": "Intensity and Hydraulic Diameter",
        "turb_hydraulic_diam": 0.5,
    }
    assert solver.setup.boundary_conditions.velocity_inlet["inlet"].vmag() == {
        "option": "value",
        "value": 125.0,
    }
    solver.execute_tui(r"""/solve/initialize/compute-defaults/velocity-inlet inlet """)
    solver.solution.initialization.standard_initialize()
    solver.solution.run_calculation.iter_count = 2
    solver.solution.run_calculation.iterate(number_of_iterations=2)
    solver.results.report.report_menu.fluxes.mass_flow(
        all_bndry_zones=False,
        zone_list=["outlet"],
        write_to_file=True,
        file_name="mass_flow_rate.flp",
    )
    # solver.setup.cell_zone_conditions.fluid['fluid:substrate:1'] = {'material': 'hydrogen', 'dir_spec_cond': 'Conical'}
    # solver.execute_tui(r'''/define/boundary-conditions/copy-bc fluid:substrate:1 fluid:substrate:2 () ''')
    # solver.solution.initialization.standard_initialize()
    # solver.solution.run_calculation.iterate(number_of_iterations=2)
    # solver.execute_tui(r'''/define/curvilinear-coordinate-system/new "curve-coordinate-0" fluid:1 () "Base_Vector" 1 0 0 "Vector_Projection" 0 1 0 ''')
    # solver.execute_tui(r'''/define/curvilinear-coordinate-system/calculation-settings 30 1e-08 ''')
    # solver.setup.cell_zone_conditions.fluid['fluid:1'] = {"material": "nit", "porous": True, "dir_spec_cond": "Curvilinear Coordinate System", "cursys_name": "curve-coordinate-0"}
    # solver.file.write(file_type="case-data", file_name="catalytic_converter_final.cas.h5")
    # solver.execute_tui(r'''(proc-stats)  ''')
    # solver.execute_tui(r'''(display "testing finished")  ''')
    solver.exit()
