import os

import pytest
from util.fixture_fluent import download_input_file


@pytest.mark.solve
@pytest.mark.fluent_231
def test_pro_exp(launch_fluent_solver_3ddp_t2):
    if not os.path.exists("out"):
        os.mkdir("out")
    solver = launch_fluent_solver_3ddp_t2
    input_type, input_name = download_input_file("pyfluent/elbow", "elbow.msh.h5")
    solver.file.read(file_type=input_type, file_name=input_name)
    solver.setup.models.energy = {"enabled": True}
    solver.setup.boundary_conditions.velocity_inlet["hot-inlet"] = {
        "vmag": 1.0,
        "t": 350.0,
        "turb_viscosity_ratio": 2,
    }
    solver.setup.boundary_conditions.velocity_inlet["cold-inlet"] = {
        "vmag": 0.5,
        "t": 301.0,
        "turb_viscosity_ratio": 2,
    }
    solver.setup.models.viscous.model = "inviscid"
    solver.solution.initialization.standard_initialize()
    solver.solution.run_calculation.iterate(number_of_iterations=200)
    solver.results.report.report_menu.surface_integrals(
        report_type="area-weighted-avg",
        surface_id=["symmetry-xyplane"],
        cell_report="pressure",
        write_to_file=True,
        file_name="out/pressure1.srp",
    )
    solver.results.graphics.contour["contour-1"] = {}
    solver.results.graphics.contour["contour-1"] = {
        "surfaces_list": ["symmetry-xyplane"],
        "field": "pressure",
    }
    solver.results.graphics.contour.display(object_name="contour-1")
    solver.setup.models.viscous.model = "laminar"
    solver.setup.models.viscous.options.low_pressure_boundary_slip = True
    solver.setup.models.viscous.model = "spalart-allmaras"
    solver.setup.models.viscous.options.corner_flow_correction = True
    solver.setup.models.viscous.options.curvature_correction = True
    solver.execute_tui(
        r"""/define/models/viscous/corner-flow-correction-ccorner yes 0.9 """
    )
    solver.execute_tui(
        r"""/define/models/viscous/curvature-correction-ccurv yes 0.9 """
    )
    solver.solution.initialization.standard_initialize()
    solver.solution.run_calculation.iterate(number_of_iterations=200)
    solver.results.report.report_menu.surface_integrals(
        report_type="area-weighted-avg",
        surface_id=["symmetry-xyplane"],
        cell_report="pressure",
        write_to_file=True,
        file_name="out/pressure2.srp",
    )
    solver.results.graphics.contour["contour-2"] = {}
    solver.results.graphics.contour["contour-2"] = {
        "surfaces_list": ["symmetry-xyplane"],
        "field": "pressure",
    }
    solver.results.graphics.contour.display(object_name="contour-2")
    solver.execute_tui(r"""/define/models/viscous/spalart-allmaras? yes """)
    solver.solution.initialization.standard_initialize()
    solver.solution.run_calculation.iterate(number_of_iterations=200)
    solver.results.report.report_menu.surface_integrals(
        report_type="area-weighted-avg",
        surface_id=["symmetry-xyplane"],
        cell_report="pressure",
        write_to_file=True,
        file_name="out/pressure3.srp",
    )
    solver.results.graphics.contour["contour-3"] = {}
    solver.results.graphics.contour["contour-3"] = {
        "surfaces_list": ["symmetry-xyplane"],
        "field": "pressure",
    }
    solver.results.graphics.contour.display(object_name="contour-3")
    solver.setup.models.viscous.model = "k-omega"
    solver.setup.models.viscous.k_omega_options.kw_low_re_correction = True
    solver.setup.models.viscous.turbulence_expert.kato_launder_model = True
    solver.setup.models.viscous.turbulence_expert.production_limiter.clip_factor = 9
    solver.setup.models.viscous.turbulence_expert.kw_vorticity_based_production = True
    solver.execute_tui(
        r"""/define/models/viscous/turbulence-expert/thermal-p-function? yes """
    )
    solver.setup.models.viscous.turbulence_expert.turb_non_newtonian = True
    solver.solution.initialization.standard_initialize()
    solver.solution.run_calculation.iterate(number_of_iterations=200)
    solver.results.report.report_menu.surface_integrals(
        report_type="area-weighted-avg",
        surface_id=["symmetry-xyplane"],
        cell_report="pressure",
        write_to_file=True,
        file_name="out/pressure4.srp",
    )
    solver.results.graphics.contour["contour-4"] = {}
    solver.results.graphics.contour["contour-4"] = {
        "surfaces_list": ["symmetry-xyplane"],
        "field": "turb-kinetic-energy",
    }
    solver.results.graphics.contour.display(object_name="contour-4")
    solver.setup.models.viscous.model = "k-omega"
    solver.setup.models.viscous.k_omega_model = "sst"
    solver.solution.initialization.standard_initialize()
    solver.solution.run_calculation.iterate(number_of_iterations=200)
    solver.results.report.report_menu.surface_integrals(
        report_type="area-weighted-avg",
        surface_id=["symmetry-xyplane"],
        cell_report="pressure",
        write_to_file=True,
        file_name="out/pressure5.srp",
    )
    solver.results.graphics.contour["contour-5"] = {}
    solver.results.graphics.contour["contour-5"] = {
        "surfaces_list": ["symmetry-xyplane"],
        "field": "turb-kinetic-energy",
    }
    solver.results.graphics.contour.display(object_name="contour-5")
    solver.setup.models.viscous.model = "k-epsilon"
    solver.solution.initialization.standard_initialize()
    solver.solution.run_calculation.iterate(number_of_iterations=200)
    solver.results.report.report_menu.surface_integrals(
        report_type="area-weighted-avg",
        surface_id=["symmetry-xyplane"],
        cell_report="pressure",
        write_to_file=True,
        file_name="out/pressure6.srp",
    )
    solver.results.graphics.contour["contour-6"] = {}
    solver.results.graphics.contour["contour-6"] = {
        "surfaces_list": ["symmetry-xyplane"],
        "field": "turb-kinetic-energy",
    }
    solver.results.graphics.contour.display(object_name="contour-6")
    solver.setup.models.viscous.model = "k-epsilon"
    solver.setup.models.viscous.k_epsilon_model = "realizable"
    solver.setup.models.viscous.turbulence_expert.production_limiter.enable_prod_limiter = (
        True
    )
    solver.setup.models.viscous.turbulence_expert.production_limiter.clip_factor = 0.8
    solver.setup.models.viscous.turbulence_expert.low_re_ke = True
    solver.setup.models.viscous.turbulence_expert.low_re_ke = False
    solver.setup.models.viscous.turbulence_expert.low_re_ke_index = 1
    solver.setup.models.viscous.turbulence_expert.non_newtonian_modification = True
    solver.setup.models.viscous.near_wall_treatment.wall_function = (
        "non-equilibrium-wall-fn"
    )
    solver.solution.initialization.standard_initialize()
    solver.solution.run_calculation.iterate(number_of_iterations=200)
    solver.results.report.report_menu.surface_integrals(
        report_type="area-weighted-avg",
        surface_id=["symmetry-xyplane"],
        cell_report="pressure",
        write_to_file=True,
        file_name="out/pressure7.srp",
    )
    solver.results.graphics.contour["contour-7"] = {}
    solver.results.graphics.contour["contour-7"] = {
        "surfaces_list": ["symmetry-xyplane"],
        "field": "turb-kinetic-energy",
    }
    solver.results.graphics.contour.display(object_name="contour-7")
    solver.execute_tui(r"""(proc-stats)  """)
    solver.execute_tui(r"""(display "testing finished")  """)
    solver.exit()
