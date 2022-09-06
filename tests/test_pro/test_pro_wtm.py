from util.fixture_fluent import download_input_file


def test_pro_wtm_tet(new_watertight_workflow_session):
    meshing = new_watertight_workflow_session
    input_type, input_name = download_input_file("pyfluent/cylinder", "cylinder.agdb")
    workflow = meshing.workflow
    # workflow.GlobalSettings.LengthUnit.setState(r'mm')
    # meshing.GlobalSettings.AreaUnit.setState(r'mm^2')
    # meshing.GlobalSettings.VolumeUnit.setState(r'mm^3')
    workflow.TaskObject["Import Geometry"].Arguments.setState(
        {
            r"FileName": r"%s" % input_name,
        }
    )
    workflow.TaskObject["Import Geometry"].Execute()
    workflow.TaskObject["Add Local Sizing"].AddChildAndUpdate()
    workflow.TaskObject["Generate the Surface Mesh"].Arguments.setState(
        {
            r"SeparationRequired": r"Yes",
            r"SurfaceMeshPreferences": {
                r"ShowSurfaceMeshPreferences": False,
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
    assert workflow.TaskObject["Generate the Surface Mesh"].Arguments.getState() == {
        "SeparationRequired": "Yes",
        "SurfaceMeshPreferences": {"ShowSurfaceMeshPreferences": False},
        "OriginalZones": ["solid"],
        "ExecuteShareTopology": "No",
    }
    workflow.TaskObject["Update Boundaries"].Arguments.setState(
        {
            r"BoundaryZoneList": [r"outlet", r"inlet", r"wall"],
            r"BoundaryZoneTypeList": [r"pressure-outlet", r"velocity-inlet", r"wall"],
            r"OldBoundaryZoneList": [r"solid:1:12", r"solid:1:11", r"solid:1"],
            r"OldBoundaryZoneTypeList": [r"wall", r"wall", r"wall"],
        }
    )
    assert workflow.TaskObject["Update Boundaries"].Arguments.getState() == {
        "OldBoundaryZoneTypeList": ["wall", "wall", "wall"],
        "BoundaryZoneTypeList": ["pressure-outlet", "velocity-inlet", "wall"],
        "BoundaryZoneList": ["outlet", "inlet", "wall"],
        "OldBoundaryZoneList": ["solid:1:12", "solid:1:11", "solid:1"],
    }
    workflow.TaskObject["Update Boundaries"].Arguments.setState(
        {
            r"BoundaryZoneList": [r"outlet", r"inlet", r"wall"],
            r"BoundaryZoneTypeList": [r"pressure-outlet", r"velocity-inlet", r"wall"],
            r"OldBoundaryZoneList": [r"solid:1:12", r"solid:1:11", r"solid:1"],
            r"OldBoundaryZoneTypeList": [r"wall", r"wall", r"wall"],
            r"ZoneLocation": [
                r"3",
                r"-1",
                r"-0.998245",
                r"10",
                r"0.99225116",
                r"0.99803305",
                r"10",
                r"solid:1:12",
                r"-1",
                r"-0.998245",
                r"0",
                r"0.99225116",
                r"0.99803305",
                r"0",
                r"solid:1:11",
                r"-1",
                r"-0.99996799",
                r"0",
                r"0.99999988",
                r"0.99995881",
                r"10",
                r"solid:1",
            ],
        }
    )

    workflow.TaskObject["Update Boundaries"].Execute()
    workflow.TaskObject["Update Regions"].Arguments.setState(
        {
            r"OldRegionNameList": [r"solid"],
            r"OldRegionTypeList": [r"fluid"],
            r"RegionNameList": [r"fluid"],
            r"RegionTypeList": [r"fluid"],
        }
    )
    workflow.TaskObject["Update Regions"].Execute()
    assert workflow.TaskObject["Update Regions"].Arguments.getState() == {
        "OldRegionNameList": ["solid"],
        "RegionNameList": ["fluid"],
        "RegionTypeList": ["fluid"],
        "OldRegionTypeList": ["fluid"],
    }
    workflow.TaskObject["Add Boundary Layers"].Arguments.setState(
        {
            r"LocalPrismPreferences": {
                r"Continuous": r"Stair Step",
            },
        }
    )
    workflow.TaskObject["Add Boundary Layers"].AddChildAndUpdate()
    workflow.TaskObject["Generate the Volume Mesh"].Arguments.setState(
        {
            r"VolumeFill": r"tetrahedral",
        }
    )
    workflow.TaskObject["Generate the Volume Mesh"].Execute()
    meshing.execute_tui(r"""/mesh/check-mesh """)
    solver = meshing.switch_to_solver()
    solver.setup.models.energy = {"enabled": True}
    solver.setup.models.viscous.model = "k-epsilon"
    solver.setup.boundary_conditions.velocity_inlet["inlet"] = {"vmag": 1.0}
    solver.mesh.check()
    solver.solution.initialization.hybrid_initialize()
    solver.results.report.report_menu.surface_integrals(
        report_type="area-weighted-avg",
        surface_id=["inlet"],
        cell_report="velocity-magnitude",
        write_to_file=True,
        file_name="wtm_tet_s2.srp",
    )
    solver.solution.run_calculation.iter_count = 10
    solver.solution.run_calculation.iterate(number_of_iterations=10)
    solver.file.write(file_type="case-data", file_name="wtm_tet_s2.cas.h5")
    solver.file.read(file_type="case-data", file_name="wtm_tet_s2.cas.h5")
    solver.execute_tui(r"""(proc-stats)  """)
    solver.execute_tui(r"""(display "testing finished")  """)
    solver.exit()


def test_pro_wtm_hex(new_watertight_workflow_session):
    meshing = new_watertight_workflow_session
    input_type, input_name = download_input_file("pyfluent/cylinder", "cylinder.agdb")
    workflow = meshing.workflow
    workflow.TaskObject["Import Geometry"].Arguments.setState(
        {
            r"FileName": r"%s" % input_name,
        }
    )
    workflow.TaskObject["Import Geometry"].Execute()
    workflow.TaskObject["Add Local Sizing"].AddChildAndUpdate()
    workflow.TaskObject["Generate the Surface Mesh"].Arguments.setState(
        {
            r"SeparationRequired": r"Yes",
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
            r"BoundaryZoneList": [r"outlet", r"inlet", r"wall"],
            r"BoundaryZoneTypeList": [r"pressure-outlet", r"velocity-inlet", r"wall"],
            r"OldBoundaryZoneList": [r"solid:1:12", r"solid:1:11", r"solid:1"],
            r"OldBoundaryZoneTypeList": [r"wall", r"wall", r"wall"],
        }
    )
    workflow.TaskObject["Update Boundaries"].Arguments.setState(
        {
            r"BoundaryZoneList": [r"outlet", r"inlet", r"wall"],
            r"BoundaryZoneTypeList": [r"pressure-outlet", r"velocity-inlet", r"wall"],
            r"OldBoundaryZoneList": [r"solid:1:12", r"solid:1:11", r"solid:1"],
            r"OldBoundaryZoneTypeList": [r"wall", r"wall", r"wall"],
            r"ZoneLocation": [
                r"3",
                r"-1",
                r"-0.998245",
                r"10",
                r"0.99225116",
                r"0.99803305",
                r"10",
                r"solid:1:12",
                r"-1",
                r"-0.998245",
                r"0",
                r"0.99225116",
                r"0.99803305",
                r"0",
                r"solid:1:11",
                r"-1",
                r"-0.99996799",
                r"0",
                r"0.99999988",
                r"0.99995881",
                r"10",
                r"solid:1",
            ],
        }
    )
    workflow.TaskObject["Update Boundaries"].Execute()
    workflow.TaskObject["Update Regions"].Arguments.setState(
        {
            r"OldRegionNameList": [r"solid"],
            r"OldRegionTypeList": [r"fluid"],
            r"RegionNameList": [r"fluid"],
            r"RegionTypeList": [r"fluid"],
        }
    )
    workflow.TaskObject["Update Regions"].Execute()
    workflow.TaskObject["Add Boundary Layers"].Arguments.setState(
        {
            r"LocalPrismPreferences": {
                r"Continuous": r"Stair Step",
            },
        }
    )
    workflow.TaskObject["Add Boundary Layers"].AddChildAndUpdate()
    workflow.TaskObject["Generate the Volume Mesh"].Arguments.setState(
        {
            r"PrismPreferences": {
                r"PrismAdjacentAngle": 80,
            },
            r"VolumeFill": r"hexcore",
        }
    )
    workflow.TaskObject["Generate the Volume Mesh"].Execute()
    meshing.execute_tui(r"""/mesh/check-mesh """)
    solver = meshing.switch_to_solver()
    solver.setup.models.energy = {"enabled": True}
    solver.setup.models.viscous.model = "k-epsilon"
    solver.setup.boundary_conditions.velocity_inlet["inlet"] = {"vmag": 1.0}
    solver.mesh.check()
    solver.solution.initialization.hybrid_initialize()
    solver.results.report.report_menu.surface_integrals(
        report_type="area-weighted-avg",
        surface_id=["inlet"],
        cell_report="velocity-magnitude",
        write_to_file=True,
        file_name="wtm_hex_s4.srp",
    )
    solver.solution.run_calculation.iter_count = 10
    solver.solution.run_calculation.iterate(number_of_iterations=10)
    solver.file.write(file_type="case-data", file_name="wtm_hex_s4.cas.h5")
    solver.file.read(file_type="case-data", file_name="wtm_hex_s4.cas.h5")
    solver.execute_tui(r"""(proc-stats)  """)
    solver.execute_tui(r"""(display "testing finished")  """)
    solver.exit()


def test_pro_wtm_poly(new_watertight_workflow_session):
    meshing = new_watertight_workflow_session
    input_type, input_name = download_input_file("pyfluent/cylinder", "cylinder.agdb")
    workflow = meshing.workflow
    workflow.TaskObject["Import Geometry"].Arguments.setState(
        {
            r"FileName": r"%s" % input_name,
        }
    )
    workflow.TaskObject["Import Geometry"].Execute()
    workflow.TaskObject["Add Local Sizing"].AddChildAndUpdate()
    workflow.TaskObject["Generate the Surface Mesh"].Arguments.setState(
        {
            r"SeparationRequired": r"Yes",
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
            r"BoundaryZoneList": [r"outlet", r"inlet", r"wall"],
            r"BoundaryZoneTypeList": [r"pressure-outlet", r"velocity-inlet", r"wall"],
            r"OldBoundaryZoneList": [r"solid:1:12", r"solid:1:11", r"solid:1"],
            r"OldBoundaryZoneTypeList": [r"wall", r"wall", r"wall"],
        }
    )
    workflow.TaskObject["Update Boundaries"].Arguments.setState(
        {
            r"BoundaryZoneList": [r"outlet", r"inlet", r"wall"],
            r"BoundaryZoneTypeList": [r"pressure-outlet", r"velocity-inlet", r"wall"],
            r"OldBoundaryZoneList": [r"solid:1:12", r"solid:1:11", r"solid:1"],
            r"OldBoundaryZoneTypeList": [r"wall", r"wall", r"wall"],
            r"ZoneLocation": [
                r"3",
                r"-1",
                r"-0.998245",
                r"10",
                r"0.99225116",
                r"0.99803305",
                r"10",
                r"solid:1:12",
                r"-1",
                r"-0.998245",
                r"0",
                r"0.99225116",
                r"0.99803305",
                r"0",
                r"solid:1:11",
                r"-1",
                r"-0.99996799",
                r"0",
                r"0.99999988",
                r"0.99995881",
                r"10",
                r"solid:1",
            ],
        }
    )
    workflow.TaskObject["Update Boundaries"].Execute()
    workflow.TaskObject["Update Regions"].Arguments.setState(
        {
            r"OldRegionNameList": [r"solid"],
            r"OldRegionTypeList": [r"fluid"],
            r"RegionNameList": [r"fluid"],
            r"RegionTypeList": [r"fluid"],
        }
    )
    workflow.TaskObject["Update Regions"].Execute()
    workflow.TaskObject["Add Boundary Layers"].Arguments.setState(
        {
            r"LocalPrismPreferences": {
                r"Continuous": r"Stair Step",
            },
        }
    )
    workflow.TaskObject["Add Boundary Layers"].AddChildAndUpdate()
    workflow.TaskObject["Generate the Volume Mesh"].Execute()
    meshing.execute_tui(r"""/mesh/check-mesh """)
    solver = meshing.switch_to_solver()
    solver.setup.models.energy = {"enabled": True}
    solver.setup.models.viscous.model = "k-epsilon"
    solver.setup.boundary_conditions.velocity_inlet["inlet"] = {"vmag": 1.0}
    solver.mesh.check()
    solver.solution.initialization.hybrid_initialize()
    solver.results.report.report_menu.surface_integrals(
        report_type="area-weighted-avg",
        surface_id=["inlet"],
        cell_report="velocity-magnitude",
        write_to_file=True,
        file_name="wtm_poly_s3.srp",
    )
    solver.solution.run_calculation.iter_count = 10
    solver.solution.run_calculation.iterate(number_of_iterations=10)
    solver.file.write(file_type="case-data", file_name="wtm_poly_s3.cas.h5")
    solver.file.read(file_type="case-data", file_name="wtm_poly_s3.cas.h5")
    solver.execute_tui(r"""(proc-stats)  """)
    solver.execute_tui(r"""(display "testing finished")  """)
    solver.exit()


def test_pro_wtm_polyhexcore(new_watertight_workflow_session):
    meshing = new_watertight_workflow_session
    input_type, input_name = download_input_file("pyfluent/cylinder", "cylinder.agdb")
    workflow = meshing.workflow
    workflow.TaskObject["Import Geometry"].Arguments.setState(
        {
            r"FileName": r"%s" % input_name,
        }
    )
    workflow.TaskObject["Import Geometry"].Execute()
    workflow.TaskObject["Add Local Sizing"].AddChildAndUpdate()
    workflow.TaskObject["Generate the Surface Mesh"].Arguments.setState(
        {
            r"SeparationRequired": r"Yes",
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
            r"BoundaryZoneList": [r"outlet", r"inlet", r"wall"],
            r"BoundaryZoneTypeList": [r"pressure-outlet", r"velocity-inlet", r"wall"],
            r"OldBoundaryZoneList": [r"solid:1:12", r"solid:1:11", r"solid:1"],
            r"OldBoundaryZoneTypeList": [r"wall", r"wall", r"wall"],
        }
    )
    workflow.TaskObject["Update Boundaries"].Arguments.setState(
        {
            r"BoundaryZoneList": [r"outlet", r"inlet", r"wall"],
            r"BoundaryZoneTypeList": [r"pressure-outlet", r"velocity-inlet", r"wall"],
            r"OldBoundaryZoneList": [r"solid:1:12", r"solid:1:11", r"solid:1"],
            r"OldBoundaryZoneTypeList": [r"wall", r"wall", r"wall"],
            r"ZoneLocation": [
                r"3",
                r"-1",
                r"-0.998245",
                r"10",
                r"0.99225116",
                r"0.99803305",
                r"10",
                r"solid:1:12",
                r"-1",
                r"-0.998245",
                r"0",
                r"0.99225116",
                r"0.99803305",
                r"0",
                r"solid:1:11",
                r"-1",
                r"-0.99996799",
                r"0",
                r"0.99999988",
                r"0.99995881",
                r"10",
                r"solid:1",
            ],
        }
    )
    workflow.TaskObject["Update Boundaries"].Execute()
    workflow.TaskObject["Update Regions"].Arguments.setState(
        {
            r"OldRegionNameList": [r"solid"],
            r"OldRegionTypeList": [r"fluid"],
            r"RegionNameList": [r"fluid"],
            r"RegionTypeList": [r"fluid"],
        }
    )
    workflow.TaskObject["Update Regions"].Execute()
    workflow.TaskObject["Add Boundary Layers"].Arguments.setState(
        {
            r"LocalPrismPreferences": {
                r"Continuous": r"Stair Step",
            },
        }
    )
    workflow.TaskObject["Add Boundary Layers"].AddChildAndUpdate()
    workflow.TaskObject["Generate the Volume Mesh"].Arguments.setState(
        {
            r"PrismPreferences": {
                r"ShowPrismPreferences": False,
            },
            r"VolumeFill": r"poly-hexcore",
            r"VolumeMeshPreferences": {
                r"ShowVolumeMeshPreferences": False,
            },
        }
    )
    workflow.TaskObject["Generate the Volume Mesh"].Execute()
    meshing.execute_tui(r"""/mesh/check-mesh """)
    solver = meshing.switch_to_solver()
    solver.setup.models.energy = {"enabled": True}
    solver.setup.models.viscous.model = "k-epsilon"
    solver.setup.boundary_conditions.velocity_inlet["inlet"] = {"vmag": 1.0}
    solver.mesh.check()
    solver.solution.initialization.hybrid_initialize()
    solver.results.report.report_menu.surface_integrals(
        report_type="area-weighted-avg",
        surface_id=["inlet"],
        cell_report="velocity-magnitude",
        write_to_file=True,
        file_name="wtm_poly_hexcore_s1.srp",
    )
    solver.solution.run_calculation.iter_count = 10
    solver.solution.run_calculation.iterate(number_of_iterations=10)
    solver.file.write(file_type="case-data", file_name="wtm_poly_hexcore_s1.cas.h5")
    solver.file.read(file_type="case-data", file_name="wtm_poly_hexcore_s1.cas.h5")
    solver.execute_tui(r"""(proc-stats)  """)
    solver.execute_tui(r"""(display "testing finished")  """)
    solver.exit()
