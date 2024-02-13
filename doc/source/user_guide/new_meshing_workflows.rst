.. _ref_user_guide_new_meshing_workflows:

Using meshing workflows
=======================
PyFluent supports accessing all Fluent meshing functionalities, including
guided meshing workflows.

Watertight geometry meshing workflow
------------------------------------
This simple example shows how to use the watertight geometry meshing workflow.

Import geometry
~~~~~~~~~~~~~~~

.. code:: python

    import ansys.fluent.core as pyfluent
    from ansys.fluent.core import examples

    import_file_name = examples.download_file('mixing_elbow.pmdb', 'pyfluent/mixing_elbow')
    meshing = pyfluent.launch_fluent(
        mode="meshing", precision='double', processor_count=2
    )
    watertight = meshing.watertight()
    watertight.import_geometry.FileName.set_state(import_file_name)
    watertight.import_geometry.LengthUnit.set_state('in')
    watertight.import_geometry()

Add local sizing
~~~~~~~~~~~~~~~~

.. code:: python

    watertight.add_local_sizing.AddChildToTask()
    watertight.add_local_sizing()

Generate surface mesh
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    watertight.create_surface_mesh.CFDSurfaceMeshControls.MaxSize.set_state(0.3)
    watertight.create_surface_mesh()

Describe geometry
~~~~~~~~~~~~~~~~~

.. code:: python

    watertight.describe_geometry.UpdateChildTasks(SetupTypeChanged=False)
    watertight.describe_geometry.SetupType.set_state("The geometry consists of only fluid regions with no voids")
    watertight.describe_geometry.UpdateChildTasks(SetupTypeChanged=True)
    watertight.describe_geometry()

Update boundaries
~~~~~~~~~~~~~~~~~

.. code:: python

    watertight.update_boundaries.BoundaryLabelList.set_state(["wall-inlet"])
    watertight.update_boundaries.BoundaryLabelTypeList.set_state(["wall"])
    watertight.update_boundaries.OldBoundaryLabelList.set_state(["wall-inlet"])
    watertight.update_boundaries.OldBoundaryLabelTypeList.set_state(["velocity-inlet"])
    watertight.update_boundaries()

Update regions
~~~~~~~~~~~~~~

.. code:: python

    watertight.update_regions()

Add boundary layers
~~~~~~~~~~~~~~~~~~~

.. code:: python

    watertight.add_boundary_layer.AddChildToTask()
    watertight.add_boundary_layer.InsertCompoundChildTask()
    watertight.task("smooth-transition_1").arguments = {
        "BLControlName": "smooth-transition_1",
    }
    watertight.add_boundary_layer.arguments = {}
    watertight.task("smooth-transition_1")()

Generate volume mesh
~~~~~~~~~~~~~~~~~~~~

.. code:: python

    watertight.create_volume_mesh.VolumeFill.set_state("poly-hexcore")
    watertight.create_volume_mesh.VolumeFillControls.HexMaxCellLength.set_state(0.3)
    watertight.create_volume_mesh()

Switch to solution mode
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    solver = meshing.switch_to_solver()

Fault-tolerant meshing workflow
-------------------------------
This simple example shows how to use the fault-tolerant meshing workflow.

Import CAD and part management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    import ansys.fluent.core as pyfluent
    from ansys.fluent.core import examples

    import_file_name = examples.download_file(
        "exhaust_system.fmd", "pyfluent/exhaust_system"
    )
    meshing = pyfluent.launch_fluent(precision="double", processor_count=2, mode="meshing")
    fault_tolerant = meshing.fault_tolerant()
    meshing.PartManagement.InputFileChanged(
        FilePath=import_file_name, IgnoreSolidNames=False, PartPerBody=False
    )
    meshing.PMFileManagement.FileManager.LoadFiles()
    meshing.PartManagement.Node["Meshing Model"].Copy(
        Paths=[
            "/dirty_manifold-for-wrapper," + "1/dirty_manifold-for-wrapper,1/main,1",
            "/dirty_manifold-for-wrapper," + "1/dirty_manifold-for-wrapper,1/flow-pipe,1",
            "/dirty_manifold-for-wrapper," + "1/dirty_manifold-for-wrapper,1/outpipe3,1",
            "/dirty_manifold-for-wrapper," + "1/dirty_manifold-for-wrapper,1/object2,1",
            "/dirty_manifold-for-wrapper," + "1/dirty_manifold-for-wrapper,1/object1,1",
        ]
    )
    meshing.PartManagement.ObjectSetting["DefaultObjectSetting"].OneZonePer.set_state("part")
    fault_tolerant.import_cad_and_part_management.Context.set_state(0)
    fault_tolerant.import_cad_and_part_management.CreateObjectPer.set_state("Custom")
    fault_tolerant.import_cad_and_part_management.FMDFileName.set_state(import_file_name)
    fault_tolerant.import_cad_and_part_management.FileLoaded.set_state("yes")
    fault_tolerant.import_cad_and_part_management.ObjectSetting.set_state("DefaultObjectSetting")
    fault_tolerant.import_cad_and_part_management.Options.Line.set_state(False)
    fault_tolerant.import_cad_and_part_management.Options.Solid.set_state(False)
    fault_tolerant.import_cad_and_part_management.Options.Surface.set_state(False)
    fault_tolerant.import_cad_and_part_management()

Describe geometry and flow
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    fault_tolerant.describe_geometry_and_flow.AddEnclosure.set_state("No")
    fault_tolerant.describe_geometry_and_flow.CloseCaps.set_state("Yes")
    fault_tolerant.describe_geometry_and_flow.FlowType.set_state("Internal flow through the object")
    fault_tolerant.describe_geometry_and_flow.UpdateChildTasks(SetupTypeChanged=False)

    fault_tolerant.describe_geometry_and_flow.AddEnclosure.set_state("No")
    fault_tolerant.describe_geometry_and_flow.CloseCaps.set_state("Yes")
    fault_tolerant.describe_geometry_and_flow.DescribeGeometryAndFlowOptions.AdvancedOptions.set_state(True)
    fault_tolerant.describe_geometry_and_flow.DescribeGeometryAndFlowOptions.ExtractEdgeFeatures.set_state("Yes")
    fault_tolerant.describe_geometry_and_flow.FlowType.set_state("Internal flow through the object")
    fault_tolerant.describe_geometry_and_flow.UpdateChildTasks(SetupTypeChanged=False)
    fault_tolerant.describe_geometry_and_flow()

Enclose fluid regions (capping)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    fault_tolerant.enclose_fluid_regions_fault.CreatePatchPreferences.ShowCreatePatchPreferences.set_state(False)
    fault_tolerant.enclose_fluid_regions_fault.PatchName.set_state("inlet-1")
    fault_tolerant.enclose_fluid_regions_fault.SelectionType.set_state("zone")
    fault_tolerant.enclose_fluid_regions_fault.ZoneSelectionList.set_state(["inlet.1"])

    fault_tolerant.enclose_fluid_regions_fault.CreatePatchPreferences.ShowCreatePatchPreferences.set_state(False)
    fault_tolerant.enclose_fluid_regions_fault.PatchName.set_state("inlet-1")
    fault_tolerant.enclose_fluid_regions_fault.SelectionType.set_state("zone")
    fault_tolerant.enclose_fluid_regions_fault.ZoneLocation.set_state([
                "1",
                "351.68205",
                "-361.34322",
                "-301.88668",
                "396.96205",
                "-332.84759",
                "-266.69751",
                "inlet.1",
            ])
    fault_tolerant.enclose_fluid_regions_fault.ZoneSelectionList.set_state(["inlet.1"])
    fault_tolerant.enclose_fluid_regions_fault.AddChildToTask()
    fault_tolerant.enclose_fluid_regions_fault.InsertCompoundChildTask()
    fault_tolerant.enclose_fluid_regions_fault.arguments.set_state({})
    fault_tolerant.task("inlet-1")()

    fault_tolerant.enclose_fluid_regions_fault.PatchName.set_state("inlet-2")
    fault_tolerant.enclose_fluid_regions_fault.SelectionType.set_state("zone")
    fault_tolerant.enclose_fluid_regions_fault.ZoneSelectionList.set_state(["inlet.2"])

    fault_tolerant.enclose_fluid_regions_fault.PatchName.set_state("inlet-2")
    fault_tolerant.enclose_fluid_regions_fault.SelectionType.set_state("zone")
    fault_tolerant.enclose_fluid_regions_fault.ZoneLocation.set_state([
                "1",
                "441.68205",
                "-361.34322",
                "-301.88668",
                "486.96205",
                "-332.84759",
                "-266.69751",
                "inlet.2",
            ])
    fault_tolerant.enclose_fluid_regions_fault.ZoneSelectionList.set_state(["inlet.2"])
    fault_tolerant.enclose_fluid_regions_fault.AddChildToTask()
    fault_tolerant.enclose_fluid_regions_fault.InsertCompoundChildTask()
    fault_tolerant.enclose_fluid_regions_fault.arguments.set_state({})
    fault_tolerant.task("inlet-2")()

    fault_tolerant.enclose_fluid_regions_fault.PatchName.set_state("inlet-3")
    fault_tolerant.enclose_fluid_regions_fault.SelectionType.set_state("zone")
    fault_tolerant.enclose_fluid_regions_fault.ZoneSelectionList.set_state(["inlet"])

    fault_tolerant.enclose_fluid_regions_fault.PatchName.set_state("inlet-3")
    fault_tolerant.enclose_fluid_regions_fault.SelectionType.set_state("zone")
    fault_tolerant.enclose_fluid_regions_fault.ZoneLocation.set_state([
                "1",
                "261.68205",
                "-361.34322",
                "-301.88668",
                "306.96205",
                "-332.84759",
                "-266.69751",
                "inlet",
            ])
    fault_tolerant.enclose_fluid_regions_fault.ZoneSelectionList.set_state(["inlet"])
    fault_tolerant.enclose_fluid_regions_fault.AddChildToTask()
    fault_tolerant.enclose_fluid_regions_fault.InsertCompoundChildTask()
    fault_tolerant.enclose_fluid_regions_fault.arguments.set_state({})
    fault_tolerant.task("inlet-3")()

    fault_tolerant.enclose_fluid_regions_fault.PatchName.set_state("outlet-1")
    fault_tolerant.enclose_fluid_regions_fault.SelectionType.set_state("zone")
    fault_tolerant.enclose_fluid_regions_fault.ZoneSelectionList.set_state(["outlet"])
    fault_tolerant.enclose_fluid_regions_fault.ZoneType.set_state("pressure-outlet")

    fault_tolerant.enclose_fluid_regions_fault.PatchName.set_state("outlet-1")
    fault_tolerant.enclose_fluid_regions_fault.SelectionType.set_state("zone")
    fault_tolerant.enclose_fluid_regions_fault.ZoneLocation.set_state([
                "1",
                "352.22702",
                "-197.8957",
                "84.102381",
                "394.41707",
                "-155.70565",
                "84.102381",
                "outlet",
            ])
    fault_tolerant.enclose_fluid_regions_fault.ZoneSelectionList.set_state(["outlet"])
    fault_tolerant.enclose_fluid_regions_fault.ZoneType.set_state("pressure-outlet")
    fault_tolerant.enclose_fluid_regions_fault.AddChildToTask()
    fault_tolerant.enclose_fluid_regions_fault.InsertCompoundChildTask()
    fault_tolerant.enclose_fluid_regions_fault.arguments.set_state({})
    fault_tolerant.task("outlet-1")()

Extract edge features
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    fault_tolerant.extract_edge_features.ExtractMethodType.set_state("Intersection Loops")
    fault_tolerant.extract_edge_features.ObjectSelectionList.set_state(["flow_pipe", "main"])
    fault_tolerant.extract_edge_features.AddChildToTask()
    fault_tolerant.extract_edge_features.InsertCompoundChildTask()

    fault_tolerant.extract_edge_features.ExtractEdgesName.set_state("edge-group-1")
    fault_tolerant.extract_edge_features.ExtractMethodType.set_state("Intersection Loops")
    fault_tolerant.extract_edge_features.ObjectSelectionList.set_state(["flow_pipe", "main"])

    fault_tolerant.extract_edge_features.arguments.set_state({})
    fault_tolerant.task("edge-group-1")()

Identify regions
~~~~~~~~~~~~~~~~

.. code:: python

    fault_tolerant.identify_regions.SelectionType.set_state("zone")
    fault_tolerant.identify_regions.X.set_state(377.322045740589)
    fault_tolerant.identify_regions.Y.set_state(-176.800676988458)
    fault_tolerant.identify_regions.Z.set_state(-37.0764628583475)
    fault_tolerant.identify_regions.ZoneSelectionList.set_state(["main.1"])

    fault_tolerant.identify_regions.SelectionType.set_state("zone")
    fault_tolerant.identify_regions.X.set_state(377.322045740589)
    fault_tolerant.identify_regions.Y.set_state(-176.800676988458)
    fault_tolerant.identify_regions.Z.set_state(-37.0764628583475)
    fault_tolerant.identify_regions.ZoneLocation.set_state([
                "1",
                "213.32205",
                "-225.28068",
                "-158.25531",
                "541.32205",
                "-128.32068",
                "84.102381",
                "main.1",
            ])
    fault_tolerant.identify_regions.ZoneSelectionList.set_state(["main.1"])
    fault_tolerant.identify_regions.AddChildToTask()
    fault_tolerant.identify_regions.InsertCompoundChildTask()

    fault_tolerant.task("fluid-region-1").arguments.set_state(
        {
            "MaterialPointsName": "fluid-region-1",
            "SelectionType": "zone",
            "X": 377.322045740589,
            "Y": -176.800676988458,
            "Z": -37.0764628583475,
            "ZoneLocation": [
                "1",
                "213.32205",
                "-225.28068",
                "-158.25531",
                "541.32205",
                "-128.32068",
                "84.102381",
                "main.1",
            ],
            "ZoneSelectionList": ["main.1"],
        }
    )
    fault_tolerant.identify_regions.arguments.set_state({})
    fault_tolerant.task("fluid-region-1")()

    fault_tolerant.identify_regions.MaterialPointsName.set_state("void-region-1")
    fault_tolerant.identify_regions.NewRegionType.set_state("void")
    fault_tolerant.identify_regions.ObjectSelectionList.set_state(["inlet-1", "inlet-2", "inlet-3", "main"])
    fault_tolerant.identify_regions.X.set_state(374.722045740589)
    fault_tolerant.identify_regions.Y.set_state(-278.9775145640143)
    fault_tolerant.identify_regions.Z.set_state(-161.1700719416913)
    fault_tolerant.identify_regions.AddChildToTask()
    fault_tolerant.identify_regions.InsertCompoundChildTask()
    fault_tolerant.identify_regions.arguments.set_state({})
    fault_tolerant.task("void-region-1")()

Define leakage threshold
~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    fault_tolerant.define_leakage_threshold.AddChild.set_state("yes")
    fault_tolerant.define_leakage_threshold.FlipDirection.set_state(True)
    fault_tolerant.define_leakage_threshold.PlaneDirection.set_state("X")
    fault_tolerant.define_leakage_threshold.RegionSelectionSingle.set_state("void-region-1")
    fault_tolerant.define_leakage_threshold.AddChildToTask()
    fault_tolerant.define_leakage_threshold.InsertCompoundChildTask()


    fault_tolerant.task("leakage-1").arguments.set_state(
        {
            "AddChild": "yes",
            "FlipDirection": True,
            "LeakageName": "leakage-1",
            "PlaneDirection": "X",
            "RegionSelectionSingle": "void-region-1",
        }
    )

    fault_tolerant.define_leakage_threshold.AddChild.set_state("yes")

    fault_tolerant.task("leakage-1")()

Update regions settings
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    fault_tolerant.update_region_settings.AllRegionFilterCategories.set_state(["2"] * 5 + ["1"] * 2)
    fault_tolerant.update_region_settings.AllRegionLeakageSizeList.set_state(["none"] * 6 + ["6.4"])
    fault_tolerant.update_region_settings.AllRegionLinkedConstructionSurfaceList.set_state(["n/a"] * 6 + ["no"])
    fault_tolerant.update_region_settings.AllRegionMeshMethodList.set_state(["none"] * 6 + ["wrap"])
    fault_tolerant.update_region_settings.AllRegionNameList.set_state([
                "main",
                "flow_pipe",
                "outpipe3",
                "object2",
                "object1",
                "void-region-1",
                "fluid-region-1",
            ])
    fault_tolerant.update_region_settings.AllRegionOversetComponenList.set_state(["no"] * 7)
    fault_tolerant.update_region_settings.AllRegionSourceList.set_state(["object"] * 5 + ["mpt"] * 2)
    fault_tolerant.update_region_settings.AllRegionTypeList.set_state(["void"] * 6 + ["fluid"])
    fault_tolerant.update_region_settings.AllRegionVolumeFillList.set_state(["none"] * 6 + ["tet"])
    fault_tolerant.update_region_settings.FilterCategory.set_state("Identified Regions")
    fault_tolerant.update_region_settings.OldRegionLeakageSizeList.set_state([""])
    fault_tolerant.update_region_settings.OldRegionMeshMethodList.set_state(["wrap"])
    fault_tolerant.update_region_settings.OldRegionNameList.set_state(["fluid-region-1"])
    fault_tolerant.update_region_settings.OldRegionOversetComponenList.set_state(["no"])
    fault_tolerant.update_region_settings.OldRegionTypeList.set_state(["fluid"])
    fault_tolerant.update_region_settings.OldRegionVolumeFillList.set_state(["hexcore"])
    fault_tolerant.update_region_settings.RegionLeakageSizeList.set_state([""])
    fault_tolerant.update_region_settings.RegionMeshMethodList.set_state(["wrap"])
    fault_tolerant.update_region_settings.RegionNameList.set_state(["fluid-region-1"])
    fault_tolerant.update_region_settings.RegionOversetComponenList.set_state(["no"])
    fault_tolerant.update_region_settings.RegionTypeList.set_state(["fluid"])
    fault_tolerant.update_region_settings.RegionVolumeFillList.set_state(["tet"])
    fault_tolerant.update_region_settings()

Choose mesh control options
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    fault_tolerant.choose_mesh_control_options()

Generate surface mesh
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    fault_tolerant.generate_the_surface_mesh()

Update boundaries
~~~~~~~~~~~~~~~~~

.. code:: python

    fault_tolerant.update_boundaries_ftm()

Add boundary layers
~~~~~~~~~~~~~~~~~~~

.. code:: python

    fault_tolerant.add_boundary_layer_ftm.AddChildToTask()
    fault_tolerant.add_boundary_layer_ftm.InsertCompoundChildTask()
    fault_tolerant.task("aspect-ratio_1").arguments.set_state(
        {
            "BLControlName": "aspect-ratio_1",
        }
    )
    fault_tolerant.add_boundary_layer_ftm.arguments.set_state({})
    fault_tolerant.task("aspect-ratio_1")()

Generate volume mesh
~~~~~~~~~~~~~~~~~~~~

.. code:: python

    fault_tolerant.generate_the_volume_mesh.AllRegionNameList.set_state([
                "main",
                "flow_pipe",
                "outpipe3",
                "object2",
                "object1",
                "void-region-1",
                "fluid-region-1",
            ])
    fault_tolerant.generate_the_volume_mesh.AllRegionSizeList.set_state(["11.33375"] * 7)
    fault_tolerant.generate_the_volume_mesh.AllRegionVolumeFillList.set_state(["none"] * 6 + ["tet"])
    fault_tolerant.generate_the_volume_mesh.EnableParallel.set_state(True)
    fault_tolerant.generate_the_volume_mesh()

Switch to solution mode
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    solver = meshing.switch_to_solver()
