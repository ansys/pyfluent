.. _ref_new_meshing_workflows_guide:

Meshing workflow
================

PyFluent provides access to Fluent's meshing workflows. A new, enhanced meshing workflow
has existed for prior releases; in Fluent 26R1 the API was further refined and extended.
This refinement is referred to as ``enhanced_api_261`` and is the default in Fluent 26R1
and later.

- To use the legacy workflow interface in Fluent 26R1 and later,
  pass ``legacy=True`` when initializing a workflow.

  For example:

    **Initializing a legacy watertight workflow with Fluent version 26R1:**

    ``watertight = meshing.watertight(legacy=True)``

- Most functionality remains backward compatible; some APIs have updated names or structure.
  Differences are noted in the relevant sections below.


Terminology and versioning
--------------------------

- ``enhanced_api_261``: The Fluent 26R1 enhancement of the enhanced workflow, offering
  clearer task organization, improved traversal, and updated object names.

- Legacy workflow: The pre-26R1 interface. Use ``legacy=True`` to opt in on 26R1+.


Watertight geometry meshing workflow
------------------------------------
Use the **Watertight Geometry** workflow for watertight CAD geometries that
require little cleanup. This is useful for clean geometries that have already
been prepped in another software, such as Ansys SpaceClaim.
The following example shows how to use the Watertight Geometry workflow.

Import geometry
~~~~~~~~~~~~~~~

.. code:: python

    import ansys.fluent.core as pyfluent
    from ansys.fluent.core import examples

    import_file_name = examples.download_file('mixing_elbow.pmdb', 'pyfluent/mixing_elbow')
    meshing_session = pyfluent.launch_fluent(
        mode=pyfluent.FluentMode.MESHING, precision=pyfluent.Precision.DOUBLE, processor_count=2
    )
    watertight = meshing_session.watertight()
    watertight.import_geometry.file_name.set_state(import_file_name)
    watertight.import_geometry.length_unit.set_state("in")
    watertight.import_geometry()

.. Note::
   Fluent 26R1 and later use ``enhanced_api_261`` by default. To use the legacy interface:

   .. code:: python

       watertight = meshing_session.watertight(legacy=True)


Add local sizing
~~~~~~~~~~~~~~~~

.. code:: python

    watertight.add_local_sizing_wtm.add_child_to_task()
    watertight.add_local_sizing_wtm()

Generate surface mesh
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    watertight.create_surface_mesh.cfd_surface_mesh_controls.max_size.set_state(0.3)
    watertight.create_surface_mesh()

Describe geometry
~~~~~~~~~~~~~~~~~

.. code:: python

    watertight.describe_geometry.update_child_tasks(setup_type_changed=False)
    watertight.describe_geometry.setup_type = "fluids"
    watertight.describe_geometry.update_child_tasks(setup_type_changed=True)
    watertight.describe_geometry()

Update boundaries
~~~~~~~~~~~~~~~~~

.. code:: python

    watertight.update_boundaries.boundary_zone_list.set_state(["wall-inlet"])
    watertight.update_boundaries.boundary_label_list.set_state(["wall-inlet"])
    watertight.update_boundaries.boundary_label_type_list.set_state(["wall"])
    watertight.update_boundaries.old_boundary_label_list.set_state(["wall-inlet"])
    watertight.update_boundaries.old_boundary_label_type_list.set_state(["velocity-inlet"])
    watertight.update_boundaries()

Update regions
~~~~~~~~~~~~~~

.. code:: python

    watertight.update_regions()

Add boundary layers
~~~~~~~~~~~~~~~~~~~

.. code:: python

    watertight.add_boundary_layers.add_child_to_task()
    watertight.add_boundary_layers.bl_control_name.set_state("smooth-transition_1")
    watertight.add_boundary_layers.insert_compound_child_task()
    watertight.add_boundary_layers_child_1()

Generate volume mesh
~~~~~~~~~~~~~~~~~~~~

.. code:: python

    watertight.create_volume_mesh_wtm.volume_fill.set_state("poly-hexcore")
    watertight.create_volume_mesh_wtm.volume_fill_controls.hex_max_cell_length.set_state(0.3)
    watertight.create_volume_mesh_wtm()

Switch to solution mode
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    solver_session = meshing_session.switch_to_solver()

Fault-tolerant meshing workflow
-------------------------------
Use the **Fault-tolerant** meshing workflow for complex CAD geometries that need
cleanup or modification, such as addressing overlaps, intersections, holes, and duplicates.
The following example shows how to use the fault-tolerant workflow.

Import CAD and part management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    import ansys.fluent.core as pyfluent
    from ansys.fluent.core import examples

    import_file_name = examples.download_file(
        "exhaust_system.fmd", "pyfluent/exhaust_system"
    )
    meshing_session = pyfluent.launch_fluent(precision=pyfluent.Precision.DOUBLE, processor_count=2, mode=pyfluent.FluentMode.MESHING)

    fault_tolerant = meshing_session.fault_tolerant()
    meshing_session.PartManagement.InputFileChanged(
        FilePath=import_file_name, IgnoreSolidNames=False, PartPerBody=False
    )
    meshing_session.PMFileManagement.FileManager.LoadFiles()
    meshing_session.PartManagement.Node["Meshing Model"].Copy(
        Paths=[
            "/dirty_manifold-for-wrapper," + "1/dirty_manifold-for-wrapper,1/main,1",
            "/dirty_manifold-for-wrapper," + "1/dirty_manifold-for-wrapper,1/flow-pipe,1",
            "/dirty_manifold-for-wrapper," + "1/dirty_manifold-for-wrapper,1/outpipe3,1",
            "/dirty_manifold-for-wrapper," + "1/dirty_manifold-for-wrapper,1/object2,1",
            "/dirty_manifold-for-wrapper," + "1/dirty_manifold-for-wrapper,1/object1,1",
        ]
    )
    meshing_session.PartManagement.ObjectSetting["DefaultObjectSetting"].OneZonePer.set_state("part")

    fault_tolerant.import_cad_and_part_management.context.set_state(0)
    fault_tolerant.import_cad_and_part_management.create_object_per.set_state("Custom")
    fault_tolerant.import_cad_and_part_management.fmd_file_name.set_state(import_file_name)
    fault_tolerant.import_cad_and_part_management.file_loaded.set_state("yes")
    fault_tolerant.import_cad_and_part_management.object_setting.set_state("DefaultObjectSetting")
    fault_tolerant.import_cad_and_part_management()

.. Note::
   Fluent 26R1 and later use ``enhanced_api_261`` by default. To use the legacy interface:

   .. code:: python

       fault_tolerant = meshing_session.fault_tolerant(legacy=True)

   ``enhanced_api_261`` includes improved naming and organization for ``PartManagement`` and ``PMFileManagement``:

   .. code:: python

       fault_tolerant = meshing_session.fault_tolerant()
       fault_tolerant.parts.input_file_changed(
        file_path=import_file_name, ignore_solid_names=False, part_per_body=False
       )
       fault_tolerant.parts_files.file_manager.load_files()
       fault_tolerant.parts.node["Meshing Model"].copy(
           paths=[
               "/dirty_manifold-for-wrapper," + "1/dirty_manifold-for-wrapper,1/main,1",
               "/dirty_manifold-for-wrapper," + "1/dirty_manifold-for-wrapper,1/flow-pipe,1",
               "/dirty_manifold-for-wrapper," + "1/dirty_manifold-for-wrapper,1/outpipe3,1",
               "/dirty_manifold-for-wrapper," + "1/dirty_manifold-for-wrapper,1/object2,1",
               "/dirty_manifold-for-wrapper," + "1/dirty_manifold-for-wrapper,1/object1,1",
           ]
       )
       fault_tolerant.parts.object_setting["DefaultObjectSetting"].one_zone_per.set_state("part")


Describe geometry and flow
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    fault_tolerant.describe_geometry_and_flow.add_enclosure.set_state("No")
    fault_tolerant.describe_geometry_and_flow.close_caps.set_state("Yes")
    fault_tolerant.describe_geometry_and_flow.describe_geometry_and_flow_options.advanced_options.set_state(True)
    fault_tolerant.describe_geometry_and_flow.describe_geometry_and_flow_options.extract_edge_features.set_state("Yes")
    fault_tolerant.describe_geometry_and_flow.flow_type.set_state("Internal flow through the object")
    fault_tolerant.describe_geometry_and_flow.update_child_tasks(setup_type_changed=False)
    fault_tolerant.describe_geometry_and_flow()

Enclose fluid regions (capping)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    fault_tolerant.capping.create_patch_preferences.show_in_gui.set_state(False)

    fault_tolerant.enclose_fluid_regions_fault.patch_name.set_state("inlet-1")
    fault_tolerant.enclose_fluid_regions_fault.selection_type.set_state("zone")
    fault_tolerant.enclose_fluid_regions_fault.zone_selection_list.set_state(["inlet.1"])
    fault_tolerant.enclose_fluid_regions_fault.insert_compound_child_task()
    fault_tolerant.enclose_fluid_regions_fault_child_1()

    fault_tolerant.enclose_fluid_regions_fault.patch_name.set_state("inlet-2")
    fault_tolerant.enclose_fluid_regions_fault.selection_type.set_state("zone")
    fault_tolerant.enclose_fluid_regions_fault.zone_selection_list.set_state(["inlet.2"])
    fault_tolerant.enclose_fluid_regions_fault.insert_compound_child_task()
    fault_tolerant.enclose_fluid_regions_fault_child_2()

    fault_tolerant.enclose_fluid_regions_fault.patch_name.set_state("inlet-3")
    fault_tolerant.enclose_fluid_regions_fault.selection_type.set_state("zone")
    fault_tolerant.enclose_fluid_regions_fault.zone_selection_list.set_state(["inlet"])
    fault_tolerant.enclose_fluid_regions_fault.insert_compound_child_task()
    fault_tolerant.enclose_fluid_regions_fault_child_3()

    fault_tolerant.enclose_fluid_regions_fault.patch_name.set_state("outlet-1")
    fault_tolerant.enclose_fluid_regions_fault.selection_type.set_state("zone")
    fault_tolerant.enclose_fluid_regions_fault.zone_selection_list.set_state(["outlet"])
    fault_tolerant.enclose_fluid_regions_fault.zone_type.set_state("pressure-outlet")
    fault_tolerant.enclose_fluid_regions_fault.insert_compound_child_task()
    fault_tolerant.enclose_fluid_regions_fault_child_4()

Extract edge features
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    fault_tolerant.extract_edge_features.extract_edges_name.set_state("edge-group-1")
    fault_tolerant.extract_edge_features.extract_method_type.set_state("Intersection Loops")
    fault_tolerant.extract_edge_features.object_selection_list.set_state(["flow_pipe", "main"])
    fault_tolerant.extract_edge_features.insert_compound_child_task()
    fault_tolerant.extract_edge_features_child_1()

Identify regions
~~~~~~~~~~~~~~~~

.. code:: python

    fault_tolerant.identify_regions.show_coordinates = True
    fault_tolerant.identify_regions.material_points_name.set_state("fluid-region-1")
    fault_tolerant.identify_regions.selection_type.set_state("zone")
    fault_tolerant.identify_regions.x.set_state(377.322045740589)
    fault_tolerant.identify_regions.y.set_state(-176.800676988458)
    fault_tolerant.identify_regions.z.set_state(-37.0764628583475)
    fault_tolerant.identify_regions.zone_selection_list.set_state(["main.1"])
    fault_tolerant.identify_regions.insert_compound_child_task()
    fault_tolerant.identify_regions_child_1()

    fault_tolerant.identify_regions.show_coordinates = True
    fault_tolerant.identify_regions.material_points_name.set_state("void-region-1")
    fault_tolerant.identify_regions.new_region_type.set_state("void")
    fault_tolerant.identify_regions.object_selection_list.set_state(["inlet-1", "inlet-2", "inlet-3", "main"])
    fault_tolerant.identify_regions.x.set_state(374.722045740589)
    fault_tolerant.identify_regions.y.set_state(-278.9775145640143)
    fault_tolerant.identify_regions.z.set_state(-161.1700719416913)
    fault_tolerant.identify_regions.insert_compound_child_task()
    fault_tolerant.identify_regions_child_2()

Define leakage threshold
~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    fault_tolerant.define_leakage_threshold.add_child.set_state("yes")
    fault_tolerant.define_leakage_threshold.flip_direction.set_state(True)
    fault_tolerant.define_leakage_threshold.plane_direction.set_state("X")
    fault_tolerant.define_leakage_threshold.region_selection_single.set_state("void-region-1")
    fault_tolerant.define_leakage_threshold.add_child = "yes"
    fault_tolerant.define_leakage_threshold.flip_direction = True
    fault_tolerant.define_leakage_threshold.leakage_name = "leakage-1"
    fault_tolerant.define_leakage_threshold.plane_direction = "X"
    fault_tolerant.define_leakage_threshold.region_selection_single = "void-region-1"
    fault_tolerant.define_leakage_threshold.insert_compound_child_task()
    fault_tolerant.define_leakage_threshold_child_1()

Update regions settings
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    fault_tolerant.update_region_settings.all_region_filter_categories.set_state(["2"] * 5 + ["1"] * 2)
    fault_tolerant.update_region_settings.all_region_leakage_size_list.set_state(["none"] * 6 + ["6.4"])
    fault_tolerant.update_region_settings.all_region_linked_construction_surface_list.set_state(["n/a"] * 6 + ["no"])
    fault_tolerant.update_region_settings.all_region_mesh_method_list.set_state(["none"] * 6 + ["wrap"])
    fault_tolerant.update_region_settings.all_region_name_list.set_state([
                "main",
                "flow_pipe",
                "outpipe3",
                "object2",
                "object1",
                "void-region-1",
                "fluid-region-1",
            ])
    fault_tolerant.update_region_settings.all_region_overset_componen_list.set_state(["no"] * 7)
    fault_tolerant.update_region_settings.all_region_source_list.set_state(["object"] * 5 + ["mpt"] * 2)
    fault_tolerant.update_region_settings.all_region_type_list.set_state(["void"] * 6 + ["fluid"])
    fault_tolerant.update_region_settings.all_region_volume_fill_list.set_state(["none"] * 6 + ["tet"])
    fault_tolerant.update_region_settings.filter_category.set_state("Identified Regions")
    fault_tolerant.update_region_settings.all_region_leakage_size_list.set_state([""])
    fault_tolerant.update_region_settings.all_region_mesh_method_list.set_state(["wrap"])
    fault_tolerant.update_region_settings.all_region_name_list.set_state(["fluid-region-1"])
    fault_tolerant.update_region_settings.all_region_overset_componen_list.set_state(["no"])
    fault_tolerant.update_region_settings.all_region_type_list.set_state(["fluid"])
    fault_tolerant.update_region_settings.all_region_volume_fill_list.set_state(["hexcore"])
    fault_tolerant.update_region_settings.all_region_leakage_size_list.set_state([""])
    fault_tolerant.update_region_settings.all_region_mesh_method_list.set_state(["wrap"])
    fault_tolerant.update_region_settings.all_region_name_list.set_state(["fluid-region-1"])
    fault_tolerant.update_region_settings.all_region_overset_componen_list.set_state(["no"])
    fault_tolerant.update_region_settings.all_region_type_list.set_state(["fluid"])
    fault_tolerant.update_region_settings.all_region_volume_fill_list.set_state(["tet"])
    fault_tolerant.update_region_settings()

Choose mesh control options
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    fault_tolerant.setup_size_controls.local_settings_name = "default-curvature"
    fault_tolerant.setup_size_controls.local_size_control_parameters.sizing_type = (
        "curvature"
    )
    fault_tolerant.setup_size_controls.object_selection_list = [
        "inlet-1",
        "inlet-2",
        "inlet-3",
    ]
    fault_tolerant.setup_size_controls.add_child_and_update(defer_update=False)
    fault_tolerant.setup_size_controls.local_settings_name = "default-proximity"
    fault_tolerant.setup_size_controls.local_size_control_parameters.sizing_type = (
        "proximity"
    )
    fault_tolerant.setup_size_controls.object_selection_list = [
        "inlet-1",
        "inlet-2",
        "inlet-3",
    ]
    fault_tolerant.setup_size_controls.add_child_and_update(defer_update=False)

Choose mesh control options
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    fault_tolerant.choose_mesh_control_options()

Generate surface mesh
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    fault_tolerant.generate_surface_mesh()

Update boundaries
~~~~~~~~~~~~~~~~~

.. code:: python

    fault_tolerant.update_boundaries()

Add boundary layers
~~~~~~~~~~~~~~~~~~~

.. code:: python

    fault_tolerant.add_boundary_layer_ftm.bl_control_name.set_state("aspect-ratio_1")
    fault_tolerant.add_boundary_layer_ftm.insert_compound_child_task()
    fault_tolerant.add_boundary_layer_ftm_child_1()

Generate volume mesh
~~~~~~~~~~~~~~~~~~~~

.. code:: python

    fault_tolerant.create_volume_mesh_ftm.all_region_name_list.set_state([
                "main",
                "flow_pipe",
                "outpipe3",
                "object2",
                "object1",
                "void-region-1",
                "fluid-region-1",
            ])
    fault_tolerant.create_volume_mesh_ftm.all_region_size_list.set_state(["11.33375"] * 7)
    fault_tolerant.create_volume_mesh_ftm.all_region_volume_fill_list.set_state(["none"] * 6 + ["tet"])
    fault_tolerant.create_volume_mesh_ftm()

Switch to solution mode
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    solver_session = meshing_session.switch_to_solver()


2D meshing workflow
-------------------
Use the **2D** meshing workflow to mesh specific two-dimensional geometries.
The example below demonstrates the workflow.

Import geometry
~~~~~~~~~~~~~~~

.. code:: python

    import ansys.fluent.core as pyfluent
    from ansys.fluent.core import examples

    import_file_name = examples.download_file('NACA0012.fmd', 'pyfluent/airfoils')
    meshing_session = pyfluent.launch_fluent(
        mode=pyfluent.FluentMode.MESHING, precision=pyfluent.Precision.DOUBLE, processor_count=2
    )
    two_dim_mesh = meshing_session.two_dimensional_meshing()

    two_dim_mesh.load_cad_geometry.file_name = import_file_name
    two_dim_mesh.load_cad_geometry.length_unit = "mm"
    two_dim_mesh.load_cad_geometry.refaceting.refacet = False
    two_dim_mesh.load_cad_geometry()

.. Note::
   Fluent 26R1 and later use ``enhanced_api_261`` by default. To use the legacy interface:

   .. code:: python

       two_dim_mesh = meshing_session.two_dimensional_meshing(legacy=True)

Set regions and boundaries
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    two_dim_mesh.update_boundaries.selection_type = "zone"
    two_dim_mesh.update_boundaries()

Define global sizing
~~~~~~~~~~~~~~~~~~~~

.. code:: python

    two_dim_mesh.define_global_sizing.curvature_normal_angle = 20
    two_dim_mesh.define_global_sizing.max_size = 2000.0
    two_dim_mesh.define_global_sizing.min_size = 5.0
    two_dim_mesh.define_global_sizing.size_functions = "Curvature"
    two_dim_mesh.define_global_sizing()

Adding BOI
~~~~~~~~~~

.. code:: python

    two_dim_mesh.add_local_sizing_wtm.add_child = "yes"
    two_dim_mesh.add_local_sizing_wtm.boi_control_name = "boi_1"
    two_dim_mesh.add_local_sizing_wtm.boi_execution = "Body Of Influence"
    two_dim_mesh.add_local_sizing_wtm.boi_face_label_list = ["boi"]
    two_dim_mesh.add_local_sizing_wtm.boi_size = 50.0
    two_dim_mesh.add_local_sizing_wtm.boi_zoneor_label = "label"
    two_dim_mesh.add_local_sizing_wtm.draw_size_control = True
    two_dim_mesh.add_local_sizing_wtm.add_child_and_update(defer_update=False)

Set edge sizing
~~~~~~~~~~~~~~~

.. code:: python

    two_dim_mesh.add_local_sizing_wtm.add_child = "yes"
    two_dim_mesh.add_local_sizing_wtm.boi_control_name = "edgesize_1"
    two_dim_mesh.add_local_sizing_wtm.boi_execution = "Edge Size"
    two_dim_mesh.add_local_sizing_wtm.boi_size = 5.0
    two_dim_mesh.add_local_sizing_wtm.boi_zoneor_label = "label"
    two_dim_mesh.add_local_sizing_wtm.draw_size_control = True
    two_dim_mesh.add_local_sizing_wtm.edge_label_list = ["airfoil-te"]
    two_dim_mesh.add_local_sizing_wtm.add_child_and_update(defer_update=False)

Set curvature sizing
~~~~~~~~~~~~~~~~~~~~

.. code:: python

    two_dim_mesh.add_local_sizing_wtm.add_child = "yes"
    two_dim_mesh.add_local_sizing_wtm.boi_control_name = "curvature_1"
    two_dim_mesh.add_local_sizing_wtm.boi_curvature_normal_angle = 10
    two_dim_mesh.add_local_sizing_wtm.boi_execution = "Curvature"
    two_dim_mesh.add_local_sizing_wtm.boi_max_size = 2
    two_dim_mesh.add_local_sizing_wtm.boi_min_size = 1.5
    two_dim_mesh.add_local_sizing_wtm.boi_scope_to = "edges"
    two_dim_mesh.add_local_sizing_wtm.boi_zoneor_label = "label"
    two_dim_mesh.add_local_sizing_wtm.draw_size_control = True
    two_dim_mesh.add_local_sizing_wtm.edge_label_list = ["airfoil"]
    two_dim_mesh.add_local_sizing_wtm.add_child_and_update(defer_update=False)

Add boundary layer
~~~~~~~~~~~~~~~~~~

.. code:: python

    two_dim_mesh.add_2d_boundary_layers.add_child = "yes"
    two_dim_mesh.add_2d_boundary_layers.bl_control_name = "aspect-ratio_1"
    two_dim_mesh.add_2d_boundary_layers.number_of_layers = 4
    two_dim_mesh.add_2d_boundary_layers.offset_method_type = "aspect-ratio"
    two_dim_mesh.add_2d_boundary_layers.add_child_and_update(defer_update=False)

Generate surface mesh
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    # NOTE: Setting `show_advanced_options = True` is required to configure advanced preferences.
    # This dependency may be removed in a future release as the API evolves.
    two_dim_mesh.generate_initial_surface_mesh.surface_2d_preferences.show_advanced_options = True
    two_dim_mesh.generate_initial_surface_mesh.surface_2d_preferences.merge_edge_zones_based_on_labels = "no"
    two_dim_mesh.generate_initial_surface_mesh.surface_2d_preferences.merge_face_zones_based_on_labels = "no"
    two_dim_mesh.generate_initial_surface_mesh()

    two_dim_mesh.add_2d_boundary_layers_child_1.revert()
    two_dim_mesh.add_2d_boundary_layers_child_1.add_child = "yes"
    two_dim_mesh.add_2d_boundary_layers_child_1.bl_control_name = "uniform_1"
    two_dim_mesh.add_2d_boundary_layers_child_1.first_layer_height = 2
    two_dim_mesh.add_2d_boundary_layers_child_1.number_of_layers = 4
    two_dim_mesh.add_2d_boundary_layers_child_1.offset_method_type = "uniform"
    two_dim_mesh.add_2d_boundary_layers_child_1()


    # NOTE: Setting `show_advanced_options = True` is required to configure advanced preferences.
    # This dependency may be removed in a future release as the API evolves.
    two_dim_mesh.generate_initial_surface_mesh.surface_2d_preferences.show_advanced_options = True
    two_dim_mesh.generate_initial_surface_mesh.surface_2d_preferences.merge_edge_zones_based_on_labels = "no"
    two_dim_mesh.generate_initial_surface_mesh.surface_2d_preferences.merge_face_zones_based_on_labels = "no"
    two_dim_mesh.generate_initial_surface_mesh()

Switch to solution mode
~~~~~~~~~~~~~~~~~~~~~~~

Switching to solver is not allowed in 2D Meshing mode.


Creating new meshing workflow
-----------------------------
Use ``create_workflow()`` to build a custom workflow.
The example below demonstrates how to create and populate a workflow.

Create workflow
~~~~~~~~~~~~~~~

.. code:: python

    import ansys.fluent.core as pyfluent
    from ansys.fluent.core import examples

    import_file_name = examples.download_file('mixing_elbow.pmdb', 'pyfluent/mixing_elbow')
    meshing_session = pyfluent.launch_fluent(
        mode=pyfluent.FluentMode.MESHING, precision=pyfluent.Precision.DOUBLE, processor_count=2
    )
    created_workflow = meshing_session.create_workflow()

.. Note::
   Fluent 26R1 and later use ``enhanced_api_261`` by default. To use the legacy interface:

   .. code:: python

       created_workflow = meshing_session.create_workflow(legacy=True)

Insert first task
~~~~~~~~~~~~~~~~~

.. code:: python

    created_workflow.insertable_tasks.import_geometry.insert()
    created_workflow.import_geometry.file_name.set_state(import_file_name)
    created_workflow.import_geometry.length_unit.set_state('in')
    created_workflow.import_geometry()

Insert next task
~~~~~~~~~~~~~~~~

.. code:: python

    created_workflow.import_geometry.insertable_tasks.add_local_sizing.insert()
    created_workflow.add_local_sizing()


Loading a saved meshing workflow
--------------------------------
Use ``load_workflow()`` to load and execute a previously saved workflow.

Load workflow
~~~~~~~~~~~~~

.. code:: python

    import ansys.fluent.core as pyfluent
    from ansys.fluent.core import examples

    saved_workflow_path = examples.download_file(
        "sample_watertight_workflow.wft", "pyfluent/meshing_workflows"
    )
    meshing_session = pyfluent.launch_fluent(
        mode=pyfluent.FluentMode.MESHING, precision=pyfluent.Precision.DOUBLE, processor_count=2
    )
    loaded_workflow = meshing_session.load_workflow(file_path=saved_workflow_path)

.. Note::
   Fluent 26R1 and later use ``enhanced_api_261`` by default. To use the legacy interface:

   .. code:: python

       loaded_workflow = meshing_session.load_workflow(file_path=saved_workflow_path, legacy=True)


Insert new task
---------------
Tasks can be inserted into a workflow using an object-oriented approach.

.. code:: python

    import ansys.fluent.core as pyfluent

    meshing_session = pyfluent.launch_fluent(
        mode=pyfluent.FluentMode.MESHING, precision=pyfluent.Precision.DOUBLE, processor_count=2
    )
    watertight = meshing_session.watertight()
    watertight.import_geometry.insertable_tasks()
    watertight.import_geometry.insertable_tasks.set_up_rotational_periodic_boundaries.insert()

Duplicate tasks
~~~~~~~~~~~~~~~

.. code:: python

    watertight.import_geometry.insertable_tasks.import_boi_geometry.insert()
    watertight.import_geometry.insertable_tasks.import_boi_geometry.insert()
    watertight.import_geometry.insertable_tasks.import_boi_geometry.insert()
    assert watertight.import_boi_geometry.arguments()
    assert watertight.import_boi_geometry_1.arguments()
    assert watertight.import_boi_geometry_2.arguments()

.. Note::
   ``enhanced_api_261`` also supports indexed access to duplicate tasks:

   .. code:: python

       >>> watertight.import_boi_geometry
       task < import_boi_geometry: 0 >
       >>> watertight.import_boi_geometry[0]
       task < import_boi_geometry: 0 >
       >>> watertight.import_boi_geometry[1]
       task < import_boi_geometry: 1 >
       >>> watertight.import_boi_geometry[2]
       task < import_boi_geometry: 2 >

   Index 0 returns the first instance; calling the task or indexing with 0 are equivalent.

   After inserting the tasks above, the workflow contains:

   .. code:: python

       >>> watertight.children()
           [task < import_geometry: 0 >,
            task < import_boi_geometry: 2 >,
            task < import_boi_geometry: 1 >,
            task < import_boi_geometry: 0 >,
            task < add_local_sizing_wtm: 0 >,
            task < create_surface_mesh: 0 >,
            task < describe_geometry: 0 >,
            task < update_regions: 0 >,
            task < add_boundary_layers: 0 >,
            task < create_volume_mesh_wtm: 0 >]


Current meshing workflow
------------------------
Use the ``current_workflow`` property to access the active workflow.

Current workflow
~~~~~~~~~~~~~~~~

.. code:: python

    meshing_session.current_workflow

.. Note::
   ``current_workflow`` raises an attribute error if no workflow has been initialized.


Mark as updated
---------------
Use the ``mark_as_updated()`` to explicitly mark a task as updated.

.. code:: python

    watertight.import_geometry.mark_as_updated()


Renaming tasks in workflow
--------------------------
After a task is renamed, the new display name change its Python attribute name.
Access the task as shown:

.. code:: python

    watertight.import_geometry.rename(new_name="import_geom_wtm")
    assert watertight.import_geom_wtm

.. Note::
   In ``enhanced_api_261`` the display name update is decoupled from the Python attribute access:

   .. code:: python

       >>> watertight.import_geometry.rename(new_name="IG")
       >>> watertight.import_geometry["IG"]
       task < import_geometry: 0 >
       >>> watertight.import_geometry
       task < import_geometry: 0 >
       >>> watertight.import_geometry[0]
       task < import_geometry: 0 >

   This allows non-Pythonic display names (for example, "I-G") without affecting attribute access.


Deleting tasks from workflow
----------------------------
Tasks can be deleted individually or in groups.

.. code:: python

    watertight.delete_tasks(list_of_tasks=["create_volume_mesh_wtm", "add_boundary_layers"])
    watertight.update_regions.delete()

.. Note::
   In ``enhanced_api_261``, pass task objects to ``list_of_tasks``:

   .. code:: python

       watertight.delete_tasks(
            list_of_tasks=[
                watertight.create_volume_mesh_wtm,
                watertight.add_boundary_layers,
             ]
        )
       watertight.update_regions.delete()

   Duplicate tasks can also be deleted via indexing:

   .. code:: python

       watertight.import_geometry.insertable_tasks.import_boi_geometry.insert()
       watertight.import_geometry.insertable_tasks.import_boi_geometry.insert()

       del watertight.import_boi_geometry[1]
       watertight.import_boi_geometry.delete()
       del watertight.create_regions


Workflow navigation enhancements (``enhanced_api_261``)
-------------------------------------------------------

The refined API enables straightforward traversal of tasks within a workflow:

.. code:: python

    watertight = meshing.watertight()

    task_1 = watertight.first_child()
    task_1.has_parent() is True
    task_1.parent().__class__.__name__ == "WatertightMeshingWorkflow"
    task_1.has_previous() is False  # As this is the first task in the workflow
    task_1.has_next() is True
    task_1.first_child() is None  # It is a simple task with no children
    task_1.last_child() is None

    task_2 = task_1.next()
    task_2.name() == "Add Local Sizing"

    task_4 = task_2.next().next()
    task_4.name() == "Describe Geometry"
    task_4_1 = task_4.first_child()  # It is a compound task with children
    task_4_1.name() == "Enclose Fluid Regions (Capping)"

    task_7 = watertight.last_child()
    task_7.name() == "Generate the Volume Mesh"

    task_6 = task_7.previous()
    task_6.name() == "Add Boundary Layers"

This enables navigation without relying on Python attribute names.


Known limitations
-----------------
- In ``enhanced_api_261``, switching between workflows and re-initializing workflows
  within the same session are currently blocked.
- Workaround: start a new session and initialize the required workflow again.

.. Note::

   This is a beta feature; user feedback is welcome.
