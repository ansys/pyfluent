import os
from pathlib import Path

import pytest
from util.fixture_fluent import download_input_file

import ansys.fluent.core as pyfluent


@pytest.mark.solve
@pytest.mark.fluent_231
def test_pro_post(launch_fluent_solver_3ddp_t2):
    out = str(Path(pyfluent.EXAMPLES_PATH) / "out")
    if not Path(out).exists():
        Path(out).mkdir(parents=True, exist_ok=False)
    solver = launch_fluent_solver_3ddp_t2
    input_type, input_name = download_input_file("pyfluent/box", "poly.msh")
    solver.file.read(file_type=input_type, file_name=input_name)
    solver.mesh.check()
    solver.execute_tui(r"""/file/show-configuration """)
    solver.setup.models.viscous.model = "laminar"
    assert solver.setup.models.viscous.model() == "laminar"
    solver.execute_tui(r"""/define/units velocity "m/s" """)
    solver.execute_tui(r"""/define/units pressure "Pa" """)
    solver.execute_tui(r"""/define/units temperature "K" """)
    solver.execute_tui(
        r"""/define/materials/change-create air air yes constant 1 no no yes constant 0.001 no no no """
    )
    solver.setup.boundary_conditions.wall["top"] = {
        "motion_bc": "Moving Wall",
        "vmag": 1.0,
    }
    solver.solution.methods.p_v_coupling.flow_scheme = "Coupled"
    assert solver.solution.methods.p_v_coupling.flow_scheme() == "Coupled"
    solver.execute_tui(r"""/solve/monitors/residual/scale-by-coefficient? yes no """)
    solver.execute_tui(
        r"""/solve/monitors/residual/convergence-criteria 1e-05 1e-05 1e-05 1e-05 """
    )
    solver.execute_tui(r"""/solve/monitors/residual/plot? no """)
    solver.solution.initialization.hybrid_initialize()
    solver.file.write(
        file_type="case-data", file_name=os.path.join(out, "pro_poly_ini")
    )
    solver.mesh.check()
    solver.execute_tui(
        r"""/file/write-profile "%s" symmetry bottom front left right top () pressure velocity-magnitude x-wall-shear pressure-coefficient x-velocity quit """
        % os.path.join(out, "test1")
    )
    solver.mesh.check()
    solver.execute_tui(r"""/define/reference-frames/list """)
    solver.execute_tui(r"""/define/reference-frames/list-properties "global" """)
    solver.execute_tui(r"""/define/reference-frames/display "global" """)
    solver.execute_tui(r"""/define/reference-frames/hide "global" """)
    solver.execute_tui(
        r"""/define/materials/change-create air air yes ideal-gas yes constant 1006.43 no no no yes 0. no """
    )
    solver.execute_tui(r"""/define/materials/list-materials """)
    solver.execute_tui(
        r"""/define/materials/change-create air air yes boussinesq 0.05 no no no no no no """
    )
    solver.setup.boundary_conditions.wall["bottom"].thermal_bc = "Temperature"
    solver.setup.boundary_conditions.wall["front"].thermal_bc = "Temperature"
    solver.setup.boundary_conditions.wall["left"].thermal_bc = "Temperature"
    solver.setup.boundary_conditions.wall["right"].thermal_bc = "Temperature"
    solver.setup.boundary_conditions.wall["bottom"].t = 500.0
    solver.setup.boundary_conditions.wall["front"].t = 500.0
    solver.setup.boundary_conditions.wall["left"].t = 500.0
    solver.setup.boundary_conditions.wall["right"].t = 500.0
    solver.setup.cell_zone_conditions.fluid["fluid"].mrf_motion = True
    solver.setup.cell_zone_conditions.fluid["fluid"].reference_frame_axis_direction = [
        {"value": 0.5, "option": "value"},
        {"value": 0, "option": "value"},
        {"value": 1, "option": "value"},
    ]
    solver.setup.cell_zone_conditions.fluid["fluid"].mrf_omega = 5.0
    solver.execute_tui(r"""/define/boundary-conditions/set/symmetry symmetry () """)
    solver.setup.boundary_conditions.wall["front"].thermal_bc = "Temperature"
    solver.setup.boundary_conditions.wall["left"].thermal_bc = "Temperature"
    solver.setup.boundary_conditions.wall["right"].thermal_bc = "Temperature"
    solver.setup.boundary_conditions.wall["top"].thermal_bc = "Temperature"
    solver.setup.boundary_conditions.wall["bottom"].t = 1000.0
    solver.setup.boundary_conditions.wall["front"].t = 1000.0
    solver.setup.boundary_conditions.wall["left"].t = 1000.0
    solver.setup.boundary_conditions.wall["right"].t = 1000.0
    solver.setup.boundary_conditions.wall["top"].t = 1000.0
    solver.setup.cell_zone_conditions.fluid["fluid"] = {
        "sources": True,
        "source_terms": {
            "mass": [10.0],
            "x-momentum": [],
            "y-momentum": [],
            "z-momentum": [],
            "energy": [],
        },
        "fixed": True,
        "fixes": {
            "x-velocity": 0.0,
            "y-velocity": 0.0,
            "z-velocity": 0.0,
            "temperature": 0.0,
        },
    }
    solver.execute_tui(r"""/define/boundary-conditions/list-zones """)
    solver.execute_tui(r"""/define/boundary-conditions/zone-name top top """)
    solver.execute_tui(r"""/define/boundary-conditions/zone-type top wall """)
    solver.execute_tui(
        r"""/define/materials/change-create air air yes boussinesq 0.05 no no no no no no """
    )
    solver.execute_tui(r"""/define/materials/list-materials """)
    solver.execute_tui(r"""/define/materials/list-properties air """)
    solver.execute_tui(r"""/solve/monitors/residual/plot? no """)
    solver.execute_tui(
        r"""/solve/monitors/residual/check-convergence? yes yes yes yes yes """
    )
    solver.execute_tui(r"""/solve/monitors/residual/criterion-type 0 """)
    solver.execute_tui(r"""/solve/monitors/residual/print? yes """)
    solver.execute_tui(r"""/solve/monitors/residual/reset? yes """)
    solver.solution.report_definitions.force["report-def-0"] = {}
    solver.solution.report_definitions.force["report-def-0"] = {
        "thread_names": ["top", "bottom", "front", "left", "right"],
        "force_vector": [1, 1, 1],
        "per_zone": True,
    }
    solver.solution.report_definitions.compute(report_defs=["report-def-0"])
    solver.solution.monitor.report_plots["report-plot-0"] = {}
    solver.solution.monitor.report_plots["report-plot-0"] = {
        "report_defs": ["report-def-0"],
        "print": True,
    }
    solver.solution.monitor.report_files["report-file-0"] = {}
    solver.solution.monitor.report_files["report-file-0"] = {
        "file_name": os.path.join(out, "force-rep.out"),
        "report_defs": ["report-def-0"],
    }
    solver.execute_tui(r"""/solve/report-files/list """)
    solver.execute_tui(r"""/solve/report-files/list-properties "report-file-0" """)
    solver.execute_tui(r"""/solve/report-files/clear-data () """)
    solver.solution.report_definitions.surface["report-def-1"] = {}
    solver.solution.report_definitions.surface[
        "report-def-1"
    ].report_type = "surface-integral"
    solver.solution.report_definitions.surface["report-def-1"] = {
        "surface_names": ["top", "bottom", "front", "left", "right"],
        "field": "pressure",
        "per_surface": True,
    }
    solver.solution.monitor.report_files["report-file-1"] = {}
    solver.solution.monitor.report_files["report-file-1"] = {
        "file_name": os.path.join(out, "surface-rep.out"),
        "report_defs": ["report-def-1"],
    }
    solver.solution.monitor.report_plots["report-plot-1"] = {}
    solver.solution.monitor.report_plots["report-plot-1"] = {
        "report_defs": ["report-def-1"]
    }
    solver.solution.report_definitions.volume["report-def-2"] = {}
    solver.solution.report_definitions.volume[
        "report-def-2"
    ].report_type = "volume-average"
    solver.solution.report_definitions.volume["report-def-2"] = {
        "field": "pressure",
        "zone_names": ["fluid"],
        "per_zone": True,
    }
    solver.solution.monitor.report_plots["report-plot-2"] = {}
    solver.solution.monitor.report_plots["report-plot-2"] = {
        "report_defs": ["report-def-2"]
    }
    solver.execute_tui(r"""/solve/report-plots/list """)
    solver.solution.monitor.report_files["report-file-2"] = {}
    solver.solution.monitor.report_files["report-file-2"] = {
        "file_name": os.path.join(out, "vol-rep.out"),
        "report_defs": ["report-def-2"],
        "print": True,
    }
    solver.execute_tui(
        r"""/define/materials/change-create air air yes ideal-gas no no no no no no """
    )
    solver.execute_tui(r"""/solve/set/equations/flow yes """)
    solver.solution.run_calculation.data_sampling.data_sampling = True
    solver.solution.initialization.standard_initialize()
    solver.execute_tui(r"""it 5 """)
    solver.mesh.check()
    solver.results.graphics.mesh["mesh-1"] = {}
    solver.results.graphics.mesh["mesh-1"] = {
        "surfaces_list": ["top", "bottom", "left", "right", "front"],
        "options": {
            "nodes": False,
            "edges": True,
            "faces": True,
            "partitions": False,
            "overset": False,
        },
    }
    assert solver.results.graphics.mesh["mesh-1"].options() == {
        "nodes": False,
        "edges": True,
        "faces": True,
        "partitions": False,
        "overset": False,
    }
    assert solver.results.graphics.mesh["mesh-1"].surfaces_list() == [
        "top",
        "bottom",
        "left",
        "right",
        "front",
    ]
    solver.results.graphics.mesh.add_to_graphics(object_name="mesh-1")
    solver.results.graphics.mesh.display(object_name="mesh-1")
    solver.execute_tui(r"""/display/set/rendering-options/driver quit """)
    solver.results.graphics.contour["contour-1"] = {}
    solver.results.graphics.contour["contour-1"] = {
        "surfaces_list": [
            "left",
            "front",
            "bottom",
            "default-interior",
            "top",
            "symmetry",
            "right",
        ],
        "field": "pressure",
    }
    assert solver.results.graphics.contour["contour-1"].surfaces_list() == [
        "left",
        "front",
        "bottom",
        "default-interior",
        "top",
        "symmetry",
        "right",
    ]
    assert solver.results.graphics.contour["contour-1"].field() == "pressure"
    solver.results.graphics.contour.add_to_graphics(object_name="contour-1")
    solver.file.read(file_type="case-data", file_name=os.path.join(out, "pro_poly_ini"))
    solver.execute_tui(r"""it 500 """)
    solver.execute_tui(r"""/surface/point-array point-array-7 10 0. 0. 0. 1 0. 0. """)
    solver.execute_tui(r"""/surface/point-surface point-8 0. 0. 0. """)
    solver.execute_tui(r"""/surface/line-surface line-9 0. 0. 0. 1 0.5 1 """)
    solver.execute_tui(
        r"""/surface/iso-surface pressure pressure-10 top bottom () () () """
    )
    solver.execute_tui(r"""/surface/plane-surface plane-11 yz-plane 0.5 """)
    solver.execute_tui(
        r"""/surface/multiple-iso-surfaces pressure pressure-12 top bottom () () 0. 11 0.01 """
    )
    solver.execute_tui(
        r"""/surface/multiple-plane-surfaces plane-23 yz-plane 0.5 10 0.01 """
    )
    solver.execute_tui(r"""/surface/list-surfaces """)
    solver.execute_tui(r"""/surface/rake-surface rake-33 0. 0. 0. 1 0. 0. 10 """)
    solver.results.graphics.mesh["mesh-1"] = {}
    solver.results.graphics.mesh["mesh-1"] = {
        "surfaces_list": ["top", "bottom", "left", "right", "front"],
        "options": {
            "nodes": False,
            "edges": True,
            "faces": True,
            "partitions": False,
            "overset": False,
        },
        "shrink_factor": 0.5,
    }
    assert solver.results.graphics.mesh["mesh-1"].surfaces_list() == [
        "top",
        "bottom",
        "left",
        "right",
        "front",
    ]
    assert solver.results.graphics.mesh["mesh-1"].options() == {
        "nodes": False,
        "edges": True,
        "faces": True,
        "partitions": False,
        "overset": False,
    }
    solver.results.graphics.mesh.display(object_name="mesh-1")
    solver.results.graphics.contour["contour-1"] = {}
    solver.results.graphics.contour["contour-1"] = {"field": "pressure"}
    assert solver.results.graphics.contour["contour-1"].field() == "pressure"
    solver.results.graphics.contour.add_to_graphics(object_name="contour-1")
    solver.results.graphics.contour.display(object_name="contour-1")
    solver.results.graphics.vector["vector-1"] = {}
    solver.results.graphics.vector["vector-1"] = {"skip": 2}
    assert solver.results.graphics.vector["vector-1"].skip() == 2
    solver.results.graphics.vector.display(object_name="vector-1")
    solver.results.graphics.pathline["pathlines-1"] = {}
    solver.results.graphics.pathline["pathlines-1"] = {
        "surfaces_list": ["top", "bottom", "front", "left", "right"]
    }
    solver.results.graphics.pathline.display(object_name="pathlines-1")
    assert solver.results.graphics.pathline["pathlines-1"].surfaces_list() == [
        "top",
        "bottom",
        "front",
        "left",
        "right",
    ]
    solver.results.plot.xy_plot["xy-plot-1"] = {}
    solver.results.plot.xy_plot["xy-plot-1"] = {
        "surfaces_list": ["top", "bottom", "left", "right", "front"]
    }
    assert solver.results.plot.xy_plot["xy-plot-1"].surfaces_list() == [
        "top",
        "bottom",
        "left",
        "right",
        "front",
    ]
    solver.results.plot.xy_plot.display(object_name="xy-plot-1")
    solver.results.scene["scene-1"] = {}
    solver.results.scene["scene-1"].graphics_objects["contour-1"] = {}
    solver.results.scene["scene-1"].graphics_objects["mesh-1"] = {}
    solver.results.scene["scene-1"].graphics_objects["vector-1"] = {}
    solver.results.scene["scene-1"] = {
        "graphics_objects": {
            "contour-1": {"transparency": 50},
            "mesh-1": {"transparency": 55},
            "vector-1": {},
        }
    }
    solver.results.scene.display(object_name="scene-1")
    assert solver.results.scene["scene-1"].graphics_objects["contour-1"]() == {
        "transparency": 50
    }
    assert solver.results.scene["scene-1"].graphics_objects["mesh-1"]() == {
        "transparency": 55
    }
    solver.results.scene.copy(from_name="scene-1", new_name="scene-2")
    solver.results.scene["scene-2"] = {"graphics_objects": {}}
    solver.results.scene.display(object_name="scene-2")
    solver.execute_tui(
        r"""/plot/histogram pressure -0.4653678834438324 1.225927948951721 10 no top bottom left right front () """
    )
    solver.execute_tui(
        r"""/plot/cumulative-plot/add "cumulative-plot-1" option cumulative-force zones top bottom left right front () split-direction 1. 1 1 force-direction 1. 1 1 number-of-divisions 15 quit """
    )
    solver.execute_tui(r"""/plot/cumulative-plot/plot "cumulative-plot-1" """)
    solver.execute_tui(r"""/plot/cumulative-plot/list """)
    solver.execute_tui(
        r"""/plot/cumulative-plot/list-properties "cumulative-plot-1" """
    )
    solver.execute_tui(r"""/plot/cumulative-plot/print "cumulative-plot-1" """)
    solver.execute_tui(
        r"""/plot/cumulative-plot/write "cumulative-plot-1" "%s" """
        % os.path.join(out, "cum-force.xy")
    )
    solver.results.report.report_menu.fluxes.mass_flow(
        all_bndry_zones=False,
        zone_list=["front", "right", "left", "bottom", "top"],
        write_to_file=True,
        file_name=os.path.join(out, "mfr"),
    )
    solver.execute_tui(
        r"""/report/forces/pressure-center yes no yes 0.5 yes "%s" """
        % os.path.join(out, "forces")
    )
    solver.execute_tui(
        r"""/report/forces/wall-forces yes 1 1 1 yes "%s" """
        % os.path.join(out, "wall-forces")
    )
    solver.execute_tui(
        r"""/report/forces/wall-moments yes 1 1 1 1 0 0 yes "%s" """
        % os.path.join(out, "wall-mon")
    )
    solver.results.report.report_menu.projected_surface_area(
        surface_id_val=[2, 1, 5, 4, 6],
        min_feature_size=0.01,
        proj_plane_norm_comp=[1, 0, 0],
    )
    solver.results.report.report_menu.surface_integrals(
        report_type="vertex-max",
        surface_id=["top", "bottom", "left", "right", "front"],
        cell_report="pressure",
        write_to_file=True,
        file_name=os.path.join(out, "vertex-max-pressure"),
    )
    solver.results.report.report_menu.volume_integrals(
        report_type="mass", thread_id_list=["fluid"], write_to_file=False
    )
    solver.results.report.report_menu.volume_integrals(
        report_type="sum",
        thread_id_list=["fluid"],
        cell_function="pressure",
        write_to_file=True,
        file_name=os.path.join(out, "sum"),
    )
    solver.results.report.report_menu.summary(
        write_to_file=True, file_name=os.path.join(out, "summary")
    )
    solver.execute_tui(r"""/report/reference-values/pressure 0. """)
    solver.execute_tui(r"""/report/reference-values/density 1.225 """)
    solver.results.report.report_menu.system.sys_statistics()
    solver.results.report.report_menu.system.time_statistics()
    solver.execute_tui(r"""it 5 """)
    solver.file.write(
        file_type="case-data", file_name=os.path.join(out, "pro_poly-final_s1")
    )
    solver.execute_tui(r"""(proc-stats)  """)
    solver.execute_tui(r"""(display "testing finished")  """)
    solver.exit()
