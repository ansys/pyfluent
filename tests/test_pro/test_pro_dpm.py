import os

from util.fixture_fluent import download_input_file


def test_pro_dpm(launch_fluent_solver_3ddp_t2):
    if not os.path.exists("out"):
        os.mkdir("out")
    solver = launch_fluent_solver_3ddp_t2
    input_type, input_name = download_input_file(
        "pyfluent/simple_duct", "simple-duct.msh.h5"
    )
    solver.file.read(file_type=input_type, file_name=input_name)
    assert solver._root.get_attr("active?")
    assert solver.check_health() == "SERVING"
    solver.setup.boundary_conditions.velocity_inlet["inlet"].vmag = 1.0
    assert solver.setup.boundary_conditions.velocity_inlet["inlet"].vmag() == {
        "option": "value",
        "value": 1.0,
    }
    solver.execute_tui(
        r"""/define/models/dpm/injections/create-injection single no no no no no no no -4.5 0. 0. 1 0. 0. 0.0001 1e-10 """
    )
    solver.execute_tui(
        r"""/define/models/dpm/injections/create-injection group no yes group no 2 no no no no no -4.5 -4.5 0. 0. -0.2 0.2 1 1 0. 0. 0. 0. 0.0001 0.0001 1e-10 1e-10 """
    )
    solver.execute_tui(
        r"""/define/models/dpm/injections/create-injection surface no yes surface no inlet () no yes no no no no no 0.0001 1 1e-10 """
    )
    solver.execute_tui(
        r"""/define/models/dpm/injections/create-injection cone no yes cone no 4 no no no no no -4.5 0. 0. 0.0001 0. 360 1 0 0 1 45 0. 0 4e-10 """
    )
    solver.execute_tui(r"""/solve/initialize/compute-defaults/velocity-inlet inlet """)
    solver.solution.initialization.standard_initialize()
    solver.execute_tui(
        r"""/display/particle-tracks/plot-write-xy-plot x-coordinate single () time -5 5 yes "out/single.xy" """
    )
    solver.execute_tui(
        r"""/display/particle-tracks/plot-write-xy-plot x-coordinate group () time -5 5 yes "out/group_x.xy" """
    )
    solver.execute_tui(
        r"""/display/particle-tracks/plot-write-xy-plot z-coordinate group () time -5 5 yes "out/group_z.xy" """
    )
    solver.execute_tui(
        r"""/display/particle-tracks/plot-write-xy-plot x-coordinate surface () time -5 5 yes "out/surface.xy" """
    )
    solver.execute_tui(
        r"""/display/particle-tracks/plot-write-xy-plot x-coordinate cone () time -5 5 yes "out/cone_x.xy" """
    )
    solver.execute_tui(
        r"""/display/particle-tracks/plot-write-xy-plot y-coordinate cone () time -5 5 yes "out/cone_y.xy" """
    )
    solver.execute_tui(
        r"""/display/particle-tracks/plot-write-xy-plot z-coordinate cone () time -5 5 yes "out/cone_z.xy" """
    )
    solver.execute_tui(r"""(proc-stats)  """)
    solver.execute_tui(r"""(display "testing finished")  """)
    solver.exit()
