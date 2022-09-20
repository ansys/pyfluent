import os

import pytest
from util.fixture_fluent import download_input_file


@pytest.mark.solve
@pytest.mark.fluent_231
def test_pro_fan(launch_fluent_solver_3ddp_t2):
    if not os.path.exists("out"):
        os.mkdir("out")
    solver = launch_fluent_solver_3ddp_t2
    input_type, input_name = download_input_file("pyfluent/fan", "fan_bc_vent.msh")
    solver.file.read(file_type=input_type, file_name=input_name)
    assert solver._root.get_attr("active?")
    assert solver.check_health() == "SERVING"
    solver.mesh.check()
    solver.execute_tui(r"""/file/show-configuration """)
    solver.setup.models.viscous.model = "k-epsilon"
    assert solver.setup.models.viscous.model() == "k-epsilon"
    solver.setup.boundary_conditions.inlet_vent["inlet-vent-6"] = {
        "direction_spec": "Direction Vector"
    }
    solver.setup.boundary_conditions.inlet_vent["inlet-vent-6"] = {
        "ke_spec": "K and Epsilon",
        "k": 0.02,
    }
    solver.setup.boundary_conditions.outlet_vent["outlet-vent-7"] = {
        "ke_spec": "K and Epsilon",
        "k": 0.02,
    }
    solver.setup.boundary_conditions.fan["fan-8"] = {
        "average_dp": True,
        "c": {
            "method": "polynomial",
            "number_of_coeff": 2,
            "coefficients": [200.0, -10.0],
        },
        "limit_range": True,
        "v_max": 20.0,
        "swirl_model": True,
        "fr": [0, 0, 20],
        "hub": 0.02,
        "axis_origin": [0.25, 0, 0],
    }
    assert (
        solver.setup.boundary_conditions.inlet_vent["inlet-vent-6"].ke_spec()
        == "K and Epsilon"
    )
    assert solver.setup.boundary_conditions.inlet_vent["inlet-vent-6"].k() == {
        "option": "value",
        "value": 0.02,
    }
    assert (
        solver.setup.boundary_conditions.outlet_vent["outlet-vent-7"].ke_spec()
        == "K and Epsilon"
    )
    assert solver.setup.boundary_conditions.outlet_vent["outlet-vent-7"].k() == {
        "option": "value",
        "value": 0.02,
    }
    assert solver.setup.boundary_conditions.fan["fan-8"].c() == {
        "method": "polynomial",
        "number_of_coeff": 2,
        "coefficients": [200.0, -10.0],
    }
    assert solver.setup.boundary_conditions.fan["fan-8"].axis_origin() == [0.25, 0, 0]
    solver.execute_tui(r"""/solve/set/disable-reconstruction? no """)
    solver.solution.methods.discretization_scheme = {"pressure": "standard"}
    solver.solution.methods.discretization_scheme = {"mom": "first-order-upwind"}
    assert solver.solution.methods.discretization_scheme() == {
        "k": "first-order-upwind",
        "mom": "first-order-upwind",
        "epsilon": "first-order-upwind",
        "pressure": "standard",
    }
    solver.execute_tui(r"""/solve/monitors/residual/normalize? yes """)
    solver.execute_tui(
        r"""/solve/monitors/residual/normalization-factors 0.5231051 3.599108 0.6445935 0.6873757 0.03376108 2.694927 """
    )
    solver.execute_tui(r"""/define/boundary-conditions/list-zones """)
    solver.execute_tui(r"""/solve/monitors/residual/plot? no """)
    solver.solution.initialization.standard_initialize()
    solver.execute_tui(r"""it 1000 """)
    solver.file.write(file_type="case-data", file_name=os.path.join("out", "fan.cas"))
    solver.results.graphics.contour["contour-1"] = {}
    solver.results.graphics.contour["contour-1"] = {
        "field": "pressure",
        "surfaces_list": ["fan-8", "symmetry-9", "wall-2", "wall-3"],
    }
    solver.results.graphics.contour.display(object_name="contour-1")
    solver.results.graphics.mesh["mesh-1"] = {}
    solver.results.graphics.mesh["mesh-1"] = {
        "options": {
            "nodes": False,
            "edges": True,
            "faces": True,
            "partitions": False,
            "overset": False,
        },
        "surfaces_list": [
            "fan-8",
            "wall-2",
            "wall-3",
            "symmetry-9",
            "inlet-vent-6",
            "outlet-vent-7",
        ],
    }
    solver.results.graphics.mesh.display(object_name="mesh-1")
    solver.results.graphics.vector["vector-1"] = {}
    solver.results.graphics.vector["vector-1"] = {
        "surfaces_list": [
            "symmetry-9",
            "fan-8",
            "wall-2",
            "wall-3",
            "inlet-vent-6",
            "outlet-vent-7",
        ]
    }
    solver.results.graphics.vector.display(object_name="vector-1")
    solver.results.plot.xy_plot["xy-plot-1"] = {}
    solver.results.plot.xy_plot["xy-plot-1"] = {"surfaces_list": ["fan-8"]}
    solver.results.plot.xy_plot.display(object_name="xy-plot-1")
    solver.results.plot.xy_plot["xy-plot-1"] = {
        "plot_direction": {
            "option": "direction-vector",
            "direction_vector": {"z_component": 0, "y_component": 1, "x_component": 0},
        }
    }
    solver.results.plot.xy_plot.display(object_name="xy-plot-1")
    solver.results.report.report_menu.fluxes.mass_flow(
        all_bndry_zones=False, zone_list=["fan-8"], write_to_file=False
    )
    solver.results.report.report_menu.fluxes.mass_flow(
        all_bndry_zones=False,
        zone_list=["fan-8"],
        write_to_file=True,
        file_name=os.path.join("out", "mfr-fan.flp"),
    )
    solver.execute_tui(r"""(proc-stats)  """)
    solver.execute_tui(r"""(display "testing finished")  """)
    solver.exit()
