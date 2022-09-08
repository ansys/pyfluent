import pytest
from util.fixture_fluent import download_input_file


@pytest.mark.solve
@pytest.mark.fluent_231
def test_pro_ht(new_watertight_workflow_session):
    meshing = new_watertight_workflow_session
    input_type, input_name = download_input_file(
        "pyfluent/mixing_elbow", "elbow.scdoc.pmdb"
    )
    workflow = meshing.workflow
    workflow.TaskObject["Import Geometry"].Arguments.setState(
        {
            r"FileName": r"%s" % input_name,
            r"LengthUnit": r"in",
        }
    )
    workflow.TaskObject["Import Geometry"].Execute()
    workflow.TaskObject["Add Local Sizing"].AddChildToTask()
    workflow.TaskObject["Add Local Sizing"].Execute()
    workflow.TaskObject["Generate the Surface Mesh"].Arguments.setState(
        {
            r"CFDSurfaceMeshControls": {
                r"MaxSize": 0.3,
            },
        }
    )
    workflow.TaskObject["Generate the Surface Mesh"].Execute()
    workflow.TaskObject["Describe Geometry"].UpdateChildTasks(SetupTypeChanged=False)
    workflow.TaskObject["Describe Geometry"].Arguments.setState(
        {
            r"SetupType": r"The geometry consists of only fluid regions with no voids",
        }
    )
    workflow.TaskObject["Describe Geometry"].UpdateChildTasks(SetupTypeChanged=True)
    workflow.TaskObject["Describe Geometry"].Execute()
    workflow.TaskObject["Update Boundaries"].Arguments.setState(
        {
            r"BoundaryLabelList": [r"wall-inlet"],
            r"BoundaryLabelTypeList": [r"wall"],
            r"OldBoundaryLabelList": [r"wall-inlet"],
            r"OldBoundaryLabelTypeList": [r"velocity-inlet"],
        }
    )
    workflow.TaskObject["Update Boundaries"].Execute()
    workflow.TaskObject["Update Regions"].Execute()
    workflow.TaskObject["Add Boundary Layers"].AddChildToTask()
    workflow.TaskObject["Add Boundary Layers"].InsertCompoundChildTask()
    workflow.TaskObject["smooth-transition_1"].Arguments.setState(
        {
            r"BLControlName": r"smooth-transition_1",
        }
    )
    workflow.TaskObject["Add Boundary Layers"].Arguments.setState({})
    workflow.TaskObject["smooth-transition_1"].Execute()
    workflow.TaskObject["Generate the Volume Mesh"].Arguments.setState(
        {
            r"VolumeFill": r"poly-hexcore",
            r"VolumeFillControls": {
                r"HexMaxCellLength": 0.3,
            },
        }
    )
    workflow.TaskObject["Generate the Volume Mesh"].Execute()
    meshing.execute_tui(r"""/mesh/check-mesh """)
    meshing.execute_tui(r"""/file/write-mesh "elbow.msh.h5" """)
    solver = meshing.switch_to_solver()
    solver.mesh.check()
    solver.execute_tui(r"""/define/units length in """)
    solver.mesh.check()
    solver.execute_tui(r"""/file/show-configuration """)
    assert not solver.setup.models.energy.enabled()
    solver.setup.models.energy = {"enabled": True}
    assert solver.setup.models.energy.enabled()
    solver.execute_tui(r"""/define/materials/copy fluid water-liquid """)
    solver.setup.cell_zone_conditions.fluid["fluid"] = {"material": "water-liquid"}
    assert "water-liquid" in solver.setup.cell_zone_conditions.fluid["fluid"].material()
    solver.setup.boundary_conditions.velocity_inlet["cold-inlet"] = {
        "vmag": 0.4,
        "t": 293.15,
        "ke_spec": "Intensity and Hydraulic Diameter",
        "turb_hydraulic_diam": 0.1016,
    }
    solver.setup.boundary_conditions.velocity_inlet["hot-inlet"] = {
        "vmag": 1.2,
        "t": 313.15,
        "ke_spec": "Intensity and Hydraulic Diameter",
        "turb_hydraulic_diam": 0.0254,
    }
    solver.setup.boundary_conditions.pressure_outlet["outlet"] = {
        "ke_spec": "Intensity and Hydraulic Diameter",
        "turb_hydraulic_diam": 0.1016,
    }
    assert solver.setup.boundary_conditions.velocity_inlet["cold-inlet"].vmag() == {
        "option": "value",
        "value": 0.4,
    }
    assert solver.setup.boundary_conditions.velocity_inlet["cold-inlet"].t() == {
        "option": "value",
        "value": 293.15,
    }
    assert (
        solver.setup.boundary_conditions.velocity_inlet["hot-inlet"].ke_spec()
        == "Intensity and Hydraulic Diameter"
    )
    solver.execute_tui(r"""/solve/monitors/residual/plot? no """)
    solver.solution.report_definitions.surface["outlet-temp-avg"] = {}
    solver.solution.report_definitions.surface[
        "outlet-temp-avg"
    ].report_type = "surface-massavg"
    assert (
        solver.solution.report_definitions.surface["outlet-temp-avg"].report_type()
        == "surface-massavg"
    )
    solver.solution.report_definitions.surface["outlet-temp-avg"] = {
        "field": "temperature",
        "surface_names": ["outlet"],
    }
    solver.solution.monitor.report_files["outlet-temp-avg-rfile"] = {}
    solver.solution.monitor.report_files["outlet-temp-avg-rfile"] = {
        "report_defs": ["outlet-temp-avg"],
        "file_name": r"out\\outlet-temp-avg-rfile.out",
        "print": True,
        "frequency": 3,
    }
    solver.solution.monitor.convergence_conditions.convergence_reports[
        "con-outlet-temp-avg"
    ] = {}
    solver.solution.monitor.convergence_conditions = {
        "convergence_reports": {
            "con-outlet-temp-avg": {
                "initial_values_to_ignore": 20,
                "previous_values_to_consider": 15,
                "print": True,
                "report_defs": "outlet-temp-avg",
                "stop_criterion": 1e-05,
            }
        },
        "frequency": 3,
    }
    solver.solution.initialization.hybrid_initialize()
    solver.solution.run_calculation.iterate(number_of_iterations=150)
    solver.results.graphics.contour["contour-vel"] = {}
    solver.results.graphics.contour["contour-vel"] = {
        "field": "velocity-magnitude",
        "surfaces_list": ["symmetry-xyplane"],
        "coloring": {"option": "banded", "banded": []},
    }
    solver.results.graphics.contour["contour-temp"] = {}
    solver.results.graphics.contour["contour-temp"] = {
        "field": "velocity-magnitude",
        "surfaces_list": ["symmetry-xyplane"],
    }
    assert (
        solver.results.graphics.contour["contour-temp"].field() == "velocity-magnitude"
    )
    assert solver.results.graphics.contour["contour-temp"].surfaces_list() == [
        "symmetry-xyplane"
    ]
    solver.results.graphics.contour.display(object_name="contour-temp")
    solver.results.graphics.vector["vector-vel"] = {}
    solver.results.graphics.vector["vector-vel"] = {
        "style": "arrow",
        "surfaces_list": ["symmetry-xyplane"],
        "scale": {"auto_scale": True, "scale_f": 4},
        "skip": 2,
    }
    solver.results.graphics.vector.display(object_name="vector-vel")
    solver.results.report.report_menu.fluxes.mass_flow(
        all_bndry_zones=False,
        zone_list=["outlet", "hot-inlet", "cold-inlet"],
        write_to_file=True,
        file_name="mass-flux1.flp",
    )
    solver.execute_tui(
        r"""/surface/iso-surface z-coordinate z=0_outlet outlet () () 0 () """
    )
    solver.execute_tui(r"""/plot/solution-set/plot-to-file "temp-1.xy" """)
    solver.execute_tui(r"""/plot/solution temperature yes () z=0_outlet () """)
    solver.file.write(file_type="case-data", file_name="elbow1.cas.h5")
    solver.execute_tui(r"""(proc-stats)  """)
    solver.execute_tui(r"""(display "testing finished")  """)
    solver.exit()
