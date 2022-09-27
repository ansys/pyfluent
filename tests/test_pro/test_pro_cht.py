import os
from pathlib import Path

import pytest
from util.fixture_fluent import download_input_file

import ansys.fluent.core as pyfluent


@pytest.mark.solve
@pytest.mark.fluent_231
def test_pro_cht(launch_fluent_solver_3ddp_t2):
    out = str(Path(pyfluent.EXAMPLES_PATH) / "out")
    if not Path(out).exists():
        Path(out).mkdir(parents=True, exist_ok=False)
    solver = launch_fluent_solver_3ddp_t2
    input_type, input_name = download_input_file(
        "pyfluent/exhaust_manifold", "manifold.msh"
    )
    solver.file.read(file_type=input_type, file_name=input_name)
    assert solver._root.get_attr("active?")
    assert solver.check_health() == "SERVING"
    solver.mesh.check()
    solver.execute_tui(r"""/define/units length mm """)
    solver.setup.models.energy = {"enabled": True}
    assert solver.setup.models.energy.enabled()
    solver.execute_tui(r"""/define/models/viscous/kw-sst? yes """)
    assert solver.setup.models.viscous.model() == "k-omega"
    solver.execute_tui(
        r"""/define/materials/change-create aluminum cast-iron yes constant 7150 yes constant 460 yes constant 50 yes """
    )
    assert "cast-iron" in solver.setup.cell_zone_conditions.solid["solid_up"].material()
    solver.setup.boundary_conditions.velocity_inlet["inlet"] = {
        "vmag": 10.0,
        "t": 925.0,
        "ke_spec": "Intensity and Hydraulic Diameter",
        "turb_intensity": 0.1,
        "turb_hydraulic_diam": 0.04,
    }
    assert solver.setup.boundary_conditions.velocity_inlet["inlet"].vmag() == {
        "option": "value",
        "value": 10.0,
    }
    assert solver.setup.boundary_conditions.velocity_inlet["inlet"].t() == {
        "option": "value",
        "value": 925.0,
    }
    assert (
        solver.setup.boundary_conditions.velocity_inlet["inlet"].turb_intensity() == 0.1
    )
    solver.execute_tui(
        r"""/define/boundary-conditions/copy-bc inlet inlet1 inlet2 () """
    )
    assert (
        solver.setup.boundary_conditions.velocity_inlet["inlet"].vmag()
        == solver.setup.boundary_conditions.velocity_inlet["inlet1"].vmag()
    )
    assert (
        solver.setup.boundary_conditions.velocity_inlet["inlet"].t()
        == solver.setup.boundary_conditions.velocity_inlet["inlet1"].t()
    )
    assert (
        solver.setup.boundary_conditions.velocity_inlet["inlet"].turb_hydraulic_diam()
        == solver.setup.boundary_conditions.velocity_inlet[
            "inlet1"
        ].turb_hydraulic_diam()
    )
    assert (
        solver.setup.boundary_conditions.velocity_inlet["inlet"].turb_intensity()
        == solver.setup.boundary_conditions.velocity_inlet["inlet1"].turb_intensity()
    )
    solver.setup.boundary_conditions.pressure_outlet["outlet"] = {
        "ke_spec": "Intensity and Hydraulic Diameter",
        "turb_intensity": 0.1,
        "turb_hydraulic_diam": 0.04,
    }
    assert (
        solver.setup.boundary_conditions.pressure_outlet["outlet"].ke_spec()
        == "Intensity and Hydraulic Diameter"
    )
    assert (
        solver.setup.boundary_conditions.pressure_outlet["outlet"].turb_intensity()
        == 0.1
    )
    solver.setup.boundary_conditions.wall["solid_up:1"] = {
        "thermal_bc": "Convection",
        "h": 10.0,
    }
    assert (
        solver.setup.boundary_conditions.wall["solid_up:1"].thermal_bc() == "Convection"
    )
    assert solver.setup.boundary_conditions.wall["solid_up:1"].h() == {
        "option": "value",
        "value": 10.0,
    }
    solver.execute_tui(
        r"""/define/boundary-conditions/copy-bc solid_up:1 in1 in2 in3 out1 () """
    )
    solver.solution.methods.p_v_coupling.flow_scheme = "Coupled"
    assert solver.solution.methods.p_v_coupling.flow_scheme() == "Coupled"
    solver.solution.report_definitions.surface["point-vel"] = {}
    solver.solution.report_definitions.surface[
        "point-vel"
    ].report_type = "surface-facetmax"
    solver.solution.report_definitions.surface["point-vel"] = {
        "surface_names": ["outlet"],
        "field": "velocity-magnitude",
    }
    assert solver.solution.report_definitions.surface["point-vel"]() == {
        "field": "velocity-magnitude",
        "report_type": "surface-facetmax",
        "average_over": 1,
        "per_surface": False,
        "surface_names": ["outlet"],
    }
    solver.solution.monitor.report_files["point-vel-rfile"] = {}
    solver.solution.monitor.report_files["point-vel-rfile"] = {
        "print": True,
        "report_defs": ["point-vel"],
        "file_name": os.path.join(out, "point-vel-rfile.out"),
    }
    solver.solution.monitor.report_plots["point-vel-rplot"] = {}
    solver.solution.monitor.report_plots["point-vel-rplot"] = {
        "print": True,
        "report_defs": ["point-vel"],
    }
    assert solver.solution.monitor.report_plots["point-vel-rplot"].report_defs() == [
        "point-vel"
    ]
    assert Path(
        solver.solution.monitor.report_files["point-vel-rfile"].file_name()
    ) == Path(out, "point-vel-rfile.out")
    solver.solution.report_definitions.flux["mass-in"] = {}
    solver.solution.report_definitions.flux["mass-in"].report_type = "flux-massflow"
    solver.solution.report_definitions.flux["mass-in"] = {
        "zone_names": ["in1", "in2", "in3", "inlet2", "inlet1", "inlet"]
    }
    assert solver.solution.report_definitions.flux["mass-in"].zone_names() == [
        "in1",
        "in2",
        "in3",
        "inlet2",
        "inlet1",
        "inlet",
    ]
    solver.solution.monitor.report_files["mass-in-rfile"] = {}
    solver.solution.monitor.report_files["mass-in-rfile"] = {
        "print": True,
        "report_defs": ["mass-in"],
        "file_name": os.path.join(out, "mass-in-rfile.out"),
    }
    solver.solution.monitor.report_plots["mass-in-rplot"] = {}
    solver.solution.monitor.report_plots["mass-in-rplot"] = {
        "print": True,
        "report_defs": ["mass-in"],
    }
    solver.solution.report_definitions.flux["mass-tot"] = {}
    solver.solution.report_definitions.flux["mass-tot"].report_type = "flux-massflow"
    solver.solution.report_definitions.flux["mass-tot"] = {
        "zone_names": [
            "outlet",
            "inlet2",
            "inlet1",
            "inlet",
            "solid_up:1",
            "out1",
            "in3",
            "in2",
            "in1",
            "solid_up:002",
            "solid_up:002-shadow",
            "interior--fluid1",
            "interior--solid_up",
        ]
    }
    solver.solution.monitor.report_files["mass-tot-rfile"] = {}
    solver.solution.monitor.report_files["mass-tot-rfile"] = {
        "print": True,
        "report_defs": ["mass-tot"],
        "file_name": os.path.join(out, "mass-tot-rfile.out"),
    }
    solver.solution.monitor.report_plots["mass-tot-rplot"] = {}
    solver.solution.monitor.report_plots["mass-tot-rplot"] = {
        "print": True,
        "report_defs": ["mass-tot"],
    }
    assert solver.solution.monitor.report_plots["mass-tot-rplot"].report_defs() == [
        "mass-tot"
    ]
    solver.solution.initialization.standard_initialize()
    solver.execute_tui(r"""/solve/set/pseudo-transient yes yes 1 5 0 yes 1. """)
    solver.solution.run_calculation.iterate(iter_count=100)
    solver.results.report.report_menu.fluxes.mass_flow(
        all_bndry_zones=False,
        zone_list=["outlet", "inlet2", "inlet1", "inlet"],
        write_to_file=True,
        file_name=os.path.join(out, "mass_flow.flp"),
    )
    solver.results.graphics.pathline["pathlines-1"] = {}
    solver.results.graphics.pathline["pathlines-1"] = {
        "field": "time",
        "skip": 5,
        "surfaces_list": ["inlet", "inlet1", "inlet2"],
    }
    solver.results.graphics.pathline.display(object_name="pathlines-1")
    solver.execute_tui(
        r"""/surface/iso-clip x-coordinate clip-x-coordinate solid_up:1 -362.7150356769562 -174.6281 """
    )
    solver.execute_tui(
        r"""/surface/iso-clip z-coordinate clip-z-coordinate solid_up:1 -101.8218025565147 -44. """
    )
    assert solver.results.graphics.pathline["pathlines-1"].surfaces_list() == [
        "inlet",
        "inlet1",
        "inlet2",
    ]
    solver.results.graphics.mesh["mesh-1"] = {}
    solver.results.graphics.mesh["mesh-1"] = {"surfaces_list": ["clip-x-coordinate"]}
    assert solver.results.graphics.mesh["mesh-1"].surfaces_list() == [
        "clip-x-coordinate"
    ]
    solver.results.scene["scene-1"] = {}
    solver.results.scene["scene-1"].graphics_objects["mesh-1"] = {}
    solver.results.scene["scene-1"].graphics_objects["pathlines-1"] = {}
    solver.results.scene["scene-1"] = {
        "graphics_objects": {"mesh-1": {"transparency": 50}, "pathlines-1": {}}
    }
    solver.results.scene.display(object_name="scene-1")
    solver.results.graphics.contour["contour-velocity"] = {}
    solver.results.graphics.contour["contour-velocity"] = {
        "field": "velocity-magnitude",
        "surfaces_list": ["outlet"],
        "node_values": False,
    }
    assert (
        solver.results.graphics.contour["contour-velocity"].field()
        == "velocity-magnitude"
    )
    solver.execute_tui(r"""/display/zone-mesh out1 () """)
    solver.results.graphics.contour.add_to_graphics(object_name="contour-velocity")
    solver.execute_tui(
        r"""/surface/iso-surface axial-coordinate mid-plane-z () fluid1 solid_up* () -44. () """
    )
    solver.results.graphics.contour["contour-temperature"] = {}
    solver.results.graphics.contour["contour-temperature"] = {
        "field": "temperature",
        "surfaces_list": ["inlet", "inlet1", "inlet2", "mid-plane-z", "outlet", "out1"],
    }
    surface_list = solver.results.graphics.contour[
        "contour-temperature"
    ].surfaces_list()
    surface_list.sort()
    assert surface_list == [
        "inlet",
        "inlet1",
        "inlet2",
        "mid-plane-z",
        "out1",
        "outlet",
    ]
    solver.execute_tui(r"""/display/surface-mesh clip-z-coordinate () """)
    solver.results.graphics.contour.add_to_graphics(object_name="contour-temperature")
    solver.results.graphics.contour["contour-temperature-manifold"] = {}
    solver.results.graphics.contour["contour-temperature-manifold"] = {
        "field": "temperature",
        "surfaces_list": [
            "in1",
            "in2",
            "in3",
            "out1",
            "solid_up:002-shadow",
            "solid_up:002",
            "solid_up:1",
        ],
    }
    assert (
        solver.results.graphics.contour["contour-temperature-manifold"].field()
        == "temperature"
    )
    solver.results.graphics.contour.display(object_name="contour-temperature-manifold")
    solver.file.write(
        file_type="case-data", file_name=os.path.join(out, "manifold_solution.cas.h5")
    )
    solver.execute_tui(r"""(proc-stats)  """)
    solver.execute_tui(r"""(display "testing finished")  """)
    solver.exit()
