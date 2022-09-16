import os

import pytest
from util.fixture_fluent import download_input_file


@pytest.mark.solve
@pytest.mark.fluent_231
def test_pro_exp(launch_fluent_solver_3ddp_t2):
    if not os.path.exists("out"):
        os.mkdir("out")
    solver = launch_fluent_solver_3ddp_t2
    input_type, input_name = download_input_file("pyfluent/nozzle", "nozzle_3d.msh")
    solver.file.read(file_type=input_type, file_name=input_name)
    solver.mesh.check()
    solver.execute_tui(r"""/file/show-configuration """)
    solver.setup.models.energy = {"enabled": True}
    assert solver.setup.models.energy.enabled()
    solver.setup.models.viscous.model = "laminar"
    assert solver.setup.models.viscous.model() == "laminar"
    solver.execute_tui(
        r"""/define/materials/change-create air air yes ideal-gas yes constant 1006.43 yes constant 0.0242 yes constant 1.7894e-05 yes 28.966 no no """
    )
    solver.setup.boundary_conditions.pressure_inlet["inlet"] = {
        "p0": 200000.0,
        "supersonic_or_initial_gauge_pressure": 190000.0,
        "t0": 500.0,
    }
    assert solver.setup.boundary_conditions.pressure_inlet["inlet"].p0() == {
        "option": "value",
        "value": 200000.0,
    }
    assert solver.setup.boundary_conditions.pressure_inlet[
        "inlet"
    ].supersonic_or_initial_gauge_pressure() == {"option": "value", "value": 190000.0}
    solver.setup.boundary_conditions.pressure_outlet["outlet"] = {"p": 75000.0}
    assert solver.setup.boundary_conditions.pressure_outlet["outlet"].p() == {
        "option": "value",
        "value": 75000.0,
    }
    solver.setup.boundary_conditions.wall["top"] = {
        "thermal_bc": "Temperature",
        "t": 328.0,
    }
    assert solver.setup.boundary_conditions.wall["top"].t() == {
        "option": "value",
        "value": 328.0,
    }
    solver.setup.boundary_conditions.wall["bottom"] = {
        "thermal_bc": "Temperature",
        "t": 328.0,
    }
    assert (
        solver.setup.boundary_conditions.wall["top"].t()
        == solver.setup.boundary_conditions.wall["bottom"].t()
    )
    solver.execute_tui(r"""/define/operating-conditions/operating-pressure 101325 """)
    solver.execute_tui(
        r"""/solve/monitors/residual/convergence-criteria 1e-05 1e-05 1e-05 1e-05 1e-05 """
    )
    solver.execute_tui(r"""/solve/monitors/residual/plot? no """)
    solver.file.write(file_type="case", file_name="out/nozzle3d-ini")
    solver.solution.initialization.hybrid_initialize()
    solver.execute_tui(r"""/solve/set/equations/flow yes """)
    solver.execute_tui(r"""/solve/set/equations/temperature yes """)
    solver.setup.models.viscous.model = "k-epsilon"
    solver.execute_tui(r"""/solve/set/equations/ke yes """)
    solver.solution.methods.gradient_scheme = "least-square-cell-based"
    assert solver.solution.methods.gradient_scheme() == "least-square-cell-based"
    solver.solution.methods.discretization_scheme = {"pressure": "standard"}
    assert solver.solution.methods.discretization_scheme["pressure"]() == "standard"
    solver.solution.methods.discretization_scheme = {"pressure": "presto!"}
    assert solver.solution.methods.discretization_scheme["pressure"]() == "presto!"
    solver.solution.methods.discretization_scheme = {"density": "first-order-upwind"}
    assert (
        solver.solution.methods.discretization_scheme["density"]()
        == "first-order-upwind"
    )
    solver.solution.methods.discretization_scheme = {"density": "quick"}
    assert solver.solution.methods.discretization_scheme["density"]() == "quick"
    solver.solution.methods.discretization_scheme = {"mom": "first-order-upwind"}
    assert (
        solver.solution.methods.discretization_scheme["mom"]() == "first-order-upwind"
    )
    solver.solution.methods.discretization_scheme = {"mom": "quick"}
    assert solver.solution.methods.discretization_scheme["mom"]() == "quick"
    solver.solution.methods.discretization_scheme = {
        "temperature": "first-order-upwind"
    }
    assert (
        solver.solution.methods.discretization_scheme["temperature"]()
        == "first-order-upwind"
    )
    solver.solution.methods.discretization_scheme = {"temperature": "quick"}
    assert solver.solution.methods.discretization_scheme["temperature"]() == "quick"
    solver.solution.methods.discretization_scheme = {
        "temperature": "second-order-upwind"
    }
    assert (
        solver.solution.methods.discretization_scheme["temperature"]()
        == "second-order-upwind"
    )
    solver.solution.methods.discretization_scheme = {"k": "second-order-upwind"}
    assert solver.solution.methods.discretization_scheme["k"]() == "second-order-upwind"
    solver.solution.methods.discretization_scheme = {"epsilon": "second-order-upwind"}
    solver.execute_tui(
        r"""/solve/set/limits 1. 50000000000. 1. 5000. 1e-14 9.999999999999999e-21 100000. """
    )
    solver.solution.methods.p_v_coupling.flow_scheme = "Coupled"
    assert solver.solution.methods.p_v_coupling.flow_scheme() == "Coupled"
    solver.solution.controls.p_v_controls.explicit_momentum_under_relaxation = 0.5
    assert (
        solver.solution.controls.p_v_controls.explicit_momentum_under_relaxation()
        == 0.5
    )
    solver.solution.controls.p_v_controls.explicit_pressure_under_relaxation = 0.4
    assert (
        solver.solution.controls.p_v_controls.explicit_pressure_under_relaxation()
        == 0.4
    )
    solver.solution.controls.limits.min_temperature = 2.0
    assert solver.solution.controls.limits.min_temperature() == 2.0
    solver.solution.methods.expert.numerics_pbns.velocity_formulation = "absolute"
    assert (
        solver.solution.methods.expert.numerics_pbns.velocity_formulation()
        == "absolute"
    )
    solver.execute_tui(r"""/solve/set/expert no no no no """)
    solver.solution.methods.set_solution_methods_to_default()
    solver.solution.controls.set_controls_to_default.solution_controls()
    solver.execute_tui(r"""/solve/monitors/residual/plot? no """)
    solver.execute_tui(r"""/solve/monitors/residual/print? yes """)
    solver.execute_tui(r"""/solve/monitors/residual/reset? yes """)
    solver.execute_tui(
        r"""/solve/monitors/residual/monitor? yes yes yes yes yes yes yes """
    )
    solver.execute_tui(r"""/solve/monitors/residual/n-display 1000 """)
    solver.execute_tui(r"""/solve/monitors/residual/criterion-type 0 """)
    solver.execute_tui(
        r"""/solve/monitors/residual/convergence-criteria 1e-05 1e-05 1e-05 1e-05 1e-05 0.001 0.001 """
    )
    solver.execute_tui(
        r"""/solve/monitors/residual/check-convergence? yes yes yes yes yes yes yes """
    )
    solver.execute_tui(r"""/solve/monitors/residual/n-maximize-norms 5 """)
    solver.execute_tui(r"""/solve/monitors/residual/n-save 1000 """)
    solver.execute_tui(r"""/solve/monitors/residual/normalize? yes """)
    solver.execute_tui(
        r"""/solve/monitors/residual/normalization-factors 0.5 0.5 0.5 0.5 0.5 0.5 0.5 """
    )
    solver.execute_tui(r"""/solve/monitors/residual/re-normalize """)
    solver.execute_tui(
        r"""/solve/monitors/residual/scale-by-coefficient? yes yes yes """
    )
    solver.execute_tui(
        r"""/solve/set/previous-defaults/undo-2022r1-default-changes? no no no """
    )
    solver.solution.methods.expert.numerics_pbns.velocity_formulation = "absolute"
    assert (
        solver.solution.methods.expert.numerics_pbns.velocity_formulation()
        == "absolute"
    )
    solver.solution.initialization.hybrid_initialize()
    solver.solution.initialization.list_defaults()
    solver.execute_tui(r"""/solve/initialize/init-turb-vel-fluctuations """)
    solver.solution.initialization.hybrid_init_options.general_settings.iter_count = 5
    assert (
        solver.solution.initialization.hybrid_init_options.general_settings.iter_count()
        == 5
    )
    solver.solution.initialization.hybrid_init_options.general_settings.external_aero = (
        True
    )
    assert (
        solver.solution.initialization.hybrid_init_options.general_settings.external_aero()
        == True
    )
    solver.execute_tui(
        r"""/solve/initialize/set-hyb-initializationturbulent-settings/ yes """
    )
    solver.solution.initialization.hybrid_init_options.turbulent_setting.averaged_turbulent_parameters = (
        False
    )
    assert (
        solver.solution.initialization.hybrid_init_options.turbulent_setting.averaged_turbulent_parameters()
        == False
    )
    solver.file.read(file_type="case", file_name="out/nozzle3d-ini")
    solver.solution.initialization.standard_initialize()
    solver.execute_tui(r"""(benchmark '(iterate 500))  """)
    solver.execute_tui(r"""/surface/line-surface center-line 0 0 0 2 0 0 """)
    solver.file.write(file_type="case-data", file_name="out/nozzle-3d-supsonic_r1.cas")
    solver.execute_tui(
        r"""/plot/plot no "out/temp.xy" no no no temperature yes 1 0 0 center-line () """
    )
    solver.execute_tui(
        r"""/plot/plot no "out/mach.xy" no no no mach-number no no x-coordinate center-line () """
    )
    solver.execute_tui(r"""(proc-stats)  """)
    solver.execute_tui(r"""/solve/monitors/residual/plot? yes """)
    solver.execute_tui(
        r"""/plot/residuals-set/plot-to-file "out/nozzle-settings_s1.res" """
    )
    solver.execute_tui(r"""it 0 """)
    solver.execute_tui(
        r"""(define port (open-output-file "out/nozzle-settings_s1_no.conv"))  """
    )
    solver.execute_tui(r"""(write (%iterate 0) port)  """)
    solver.execute_tui(r"""(close-output-port port)  """)
    solver.execute_tui(r"""(display "testing finished")  """)
    solver.exit()
