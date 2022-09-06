import os

from util.fixture_fluent import download_input_file


def test_pro_exp(launch_fluent_solver_2ddp_t2):
    if not os.path.exists("out"):
        os.mkdir("out")
    solver = launch_fluent_solver_2ddp_t2
    input_type, input_name = download_input_file("pyfluent/2d_box", "pro_species.cas")
    solver.file.read(file_type=input_type, file_name=input_name)
    solver.setup.models.energy = {"enabled": True}
    solver.setup.models.viscous.model = "k-epsilon"
    solver.setup.models.viscous.k_epsilon_model = "realizable"
    solver.execute_tui(
        r"""/define/models/species/species-transport? yes methane-air """
    )
    solver.execute_tui(
        r"""/define/boundary-conditions/zone-type vi-fuel velocity-inlet """
    )
    solver.execute_tui(
        r"""/define/boundary-conditions/zone-type vi-oxid velocity-inlet """
    )
    solver.execute_tui(r"""/define/boundary-conditions/zone-type po pressure-outlet """)
    solver.setup.boundary_conditions.velocity_inlet["vi-fuel"] = {
        "vmag": 5.0,
        "ke_spec": "Intensity and Hydraulic Diameter",
        "turb_intensity": 0.09999999400000001,
        "turb_hydraulic_diam": 0.009999999799999999,
        "species_in_mole_fractions": True,
        "mf": {"ch4": 0.6144294, "o2": 0, "co2": 0.1119896, "h2o": 0.273581},
    }
    solver.setup.boundary_conditions.velocity_inlet["vi-oxid"] = {
        "vmag": 10.0,
        "ke_spec": "Intensity and Hydraulic Diameter",
        "turb_intensity": 0.09999999400000001,
        "turb_hydraulic_diam": 0.009999999799999999,
        "species_in_mole_fractions": True,
        "mf": {"ch4": 0, "o2": 0.207292, "co2": 0, "h2o": 0},
    }
    solver.setup.boundary_conditions.pressure_outlet["po"] = {
        "ke_spec": "K and Epsilon"
    }
    solver.solution.methods.gradient_scheme = "green-gauss-node-based"
    solver.solution.methods.flux_type.pbns_cases.flux_auto_select = False
    solver.solution.methods.flux_type.pbns_cases.flux_type = 0
    solver.solution.methods.gradient_scheme = "green-gauss-node-based"
    solver.execute_tui(
        r"""/solve/monitors/residual/convergence-criteria 0.001 0.001 0.001 1e-06 1e-06 1e-06 0.001 0.001 0.001 0.001 """
    )
    solver.solution.methods.discretization_scheme = {"pressure": "presto!"}
    solver.solution.methods.discretization_scheme = {"k": "second-order-upwind"}
    solver.solution.methods.discretization_scheme = {"epsilon": "second-order-upwind"}
    solver.solution.report_definitions.surface["mf_co2_outlet"] = {}
    solver.solution.report_definitions.surface[
        "mf_co2_outlet"
    ].report_type = "surface-areaavg"
    solver.solution.report_definitions.surface["mf_co2_outlet"] = {
        "field": "molef-co2",
        "surface_names": ["po"],
    }
    solver.solution.report_definitions.surface["mf_h20_outlet"] = {}
    solver.solution.report_definitions.surface[
        "mf_h20_outlet"
    ].report_type = "surface-areaavg"
    solver.solution.report_definitions.surface["mf_h20_outlet"] = {
        "field": "molef-h2o",
        "surface_names": ["po"],
    }
    solver.solution.report_definitions.surface["mf_temp_outlet"] = {}
    solver.solution.report_definitions.surface[
        "mf_temp_outlet"
    ].report_type = "surface-areaavg"
    solver.solution.report_definitions.surface["mf_temp_outlet"] = {
        "field": "temperature",
        "surface_names": ["po"],
    }
    solver.solution.monitor.report_files["mf_co2_outlet"] = {}
    solver.solution.monitor.report_files["mf_co2_outlet"] = {
        "file_name": r"out\\mf_co2_outlet.out",
        "report_defs": ["mf_co2_outlet"],
        "print": True,
    }
    solver.solution.monitor.report_files["mf_h20_outlet"] = {}
    solver.solution.monitor.report_files["mf_h20_outlet"] = {
        "file_name": r"out\\mf_h20_outlet.out",
        "report_defs": ["mf_h20_outlet"],
        "print": True,
    }
    solver.solution.monitor.report_files["mf_temp_outlet"] = {}
    solver.solution.monitor.report_files["mf_temp_outlet"] = {
        "file_name": r"out\\mf_temp_outlet.out",
        "report_defs": ["mf_temp_outlet"],
        "print": True,
    }
    solver.solution.initialization.hybrid_initialize()
    solver.execute_tui(r"""(benchmark '(iterate 150))  """)
    solver.execute_tui(
        r"""/plot/plot yes "out/mass_ch4_outlet.xy" no no no ch4 yes 0 1 po () """
    )
    solver.execute_tui(
        r"""/plot/plot yes "out/mass_o2_outlet.xy" no no no o2 yes 0 1 po () """
    )
    solver.execute_tui(
        r"""/plot/plot yes "out/mass_co2_outlet.xy" no no no co2 yes 0 1 po () """
    )
    solver.execute_tui(
        r"""/plot/plot yes "out/mass_h2o_outlet.xy" no no no h2o yes 0 1 po () """
    )
    solver.execute_tui(
        r"""/plot/plot yes "out/mass_n2_outlet.xy" no no no n2 yes 0 1 po () """
    )
    solver.execute_tui(
        r"""/plot/plot yes "out/vmag_outlet.xy" no no no velocity-magnitude yes 0 1 po () """
    )
    solver.execute_tui(
        r"""/plot/plot yes "out/k_outlet.xy" no no no turb-kinetic-energy yes 0 1 po () """
    )
    solver.results.graphics.contour["mf_co2"] = {}
    solver.results.graphics.contour["mf_co2"] = {
        "field": "molef-co2",
        "surfaces_list": ["int_fluid"],
    }
    solver.results.graphics.vector["molef_o2"] = {}
    solver.results.graphics.vector["molef_o2"] = {
        "field": "molef-o2",
        "surfaces_list": ["int_fluid"],
    }
    solver.results.graphics.pathline["path_fuel"] = {}
    solver.results.graphics.pathline["path_fuel"] = {"surfaces_list": ["vi-fuel"]}
    solver.results.graphics.pathline["path_oxid"] = {}
    solver.results.graphics.pathline["path_oxid"] = {"surfaces_list": ["vi-oxid"]}
    solver.execute_tui(r"""/solve/monitors/residual/plot? yes """)
    solver.execute_tui(
        r"""/plot/residuals-set/plot-to-file "out/pro_species_s1.res" """
    )
    solver.execute_tui(r"""it 0 """)
    solver.execute_tui(
        r"""(define port (open-output-file "out/pro_species_s1_no.conv"))  """
    )
    solver.execute_tui(r"""(write (%iterate 0) port)  """)
    solver.execute_tui(r"""(close-output-port port)  """)
    solver.execute_tui(r"""(display "testing finished")  """)
    solver.exit()
