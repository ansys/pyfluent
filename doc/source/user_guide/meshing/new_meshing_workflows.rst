.. _ref_new_meshing_workflows_guide:

Meshing workflows
=================

PyFluent provides access to Fluent’s meshing workflows.

Overview
--------
A meshing workflow is a structured collection of meshing tasks that you organize, execute, and reuse.
PyFluent provides pre-built workflows (Watertight Geometry, Fault-tolerant, and 2D meshing) for common use cases,
as well as the ability to create custom workflows. You can insert and duplicate tasks, save your workflow to file,
and load previously saved workflows for reuse.

Watertight geometry workflow
----------------------------
Use the **Watertight Geometry** workflow for watertight CAD geometries that
require little cleanup. This is useful for clean geometries prepared in CAD tools
such as Ansys SpaceClaim.

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
    import_geometry = watertight.import_geometry
    import_geometry.file_name = import_file_name
    import_geometry.length_unit = "in"
    import_geometry()

Add local sizing
~~~~~~~~~~~~~~~~

.. code:: python

    add_local_sizing = watertight.add_local_sizing_wtm
    add_local_sizing.add_child_to_task()
    add_local_sizing()

Generate surface mesh
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    create_surface_mesh = watertight.create_surface_mesh
    create_surface_mesh.cfd_surface_mesh_controls.max_size = 0.3
    create_surface_mesh()

Describe geometry
~~~~~~~~~~~~~~~~~

.. code:: python

    describe_geometry = watertight.describe_geometry
    describe_geometry.update_child_tasks(setup_type_changed=False)
    describe_geometry.setup_type = "fluid"
    describe_geometry.update_child_tasks(setup_type_changed=True)
    describe_geometry()

Update boundaries
~~~~~~~~~~~~~~~~~

.. code:: python

    update_boundaries = watertight.update_boundaries
    update_boundaries.boundary_zone_list = ["wall-inlet"]
    update_boundaries.boundary_label_list = ["wall-inlet"]
    update_boundaries.boundary_label_type_list = ["wall"]
    update_boundaries.old_boundary_label_list = ["wall-inlet"]
    update_boundaries.old_boundary_label_type_list = ["velocity-inlet"]
    update_boundaries()

Update regions
~~~~~~~~~~~~~~

.. code:: python

    watertight.update_regions()

Add boundary layers
~~~~~~~~~~~~~~~~~~~

.. code:: python

    add_boundary_layers = watertight.add_boundary_layers
    add_boundary_layers.control_name = "smooth-transition_1"
    add_boundary_layers.insert_compound_child_task()
    watertight.add_boundary_layers_child_1()

Generate volume mesh
~~~~~~~~~~~~~~~~~~~~

.. code:: python

    create_volume_mesh = watertight.create_volume_mesh_wtm
    create_volume_mesh.volume_fill = "poly-hexcore"
    create_volume_mesh.volume_fill_controls.hex_max_cell_length = 0.3
    create_volume_mesh()

Switch to solution mode
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    solver_session = meshing_session.switch_to_solver()

Fault-tolerant workflow
-----------------------
Use the **Fault-tolerant** workflow for complex CAD geometries that need
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
    fault_tolerant.parts.object_setting["DefaultObjectSetting"].one_zone_per = "part"

    fault_tolerant.import_cad_and_part_management.context = 0
    fault_tolerant.import_cad_and_part_management.create_object_per = "Custom"
    fault_tolerant.import_cad_and_part_management.fmd_file_name = import_file_name
    fault_tolerant.import_cad_and_part_management.file_loaded = True
    fault_tolerant.import_cad_and_part_management.object_setting = "DefaultObjectSetting"
    fault_tolerant.import_cad_and_part_management()

Describe geometry and flow
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    describe_geometry = fault_tolerant.describe_geometry_and_flow
    describe_geometry.add_enclosure = False
    describe_geometry.close_caps = True
    geom_options = describe_geometry.describe_geometry_and_flow_options
    geom_options.advanced_options = True
    geom_options.extract_edge_features = True
    describe_geometry.flow_type = "Internal flow through the object"
    describe_geometry.update_child_tasks(setup_type_changed=False)
    describe_geometry()

Enclose fluid regions (capping)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    fault_tolerant.capping.create_patch_preferences.show_in_gui = False

    enclose_fluid_regions = fault_tolerant.capping
    enclose_fluid_regions.patch_name = "inlet-1"
    enclose_fluid_regions.selection_type = "zone"
    enclose_fluid_regions.zone_selection_list = ["inlet.1"]
    enclose_fluid_regions.insert_compound_child_task()
    fault_tolerant.capping_child_1()

    enclose_fluid_regions.patch_name = "inlet-2"
    enclose_fluid_regions.selection_type = "zone"
    enclose_fluid_regions.zone_selection_list = ["inlet.2"]
    enclose_fluid_regions.insert_compound_child_task()
    fault_tolerant.capping_child_2()

    enclose_fluid_regions.patch_name = "inlet-3"
    enclose_fluid_regions.selection_type = "zone"
    enclose_fluid_regions.zone_selection_list = ["inlet"]
    enclose_fluid_regions.insert_compound_child_task()
    fault_tolerant.capping_child_3()

    enclose_fluid_regions.patch_name = "outlet-1"
    enclose_fluid_regions.selection_type = "zone"
    enclose_fluid_regions.zone_selection_list = ["outlet"]
    enclose_fluid_regions.zone_type = "pressure-outlet"
    enclose_fluid_regions.insert_compound_child_task()
    fault_tolerant.capping_child_4()

Extract edge features
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    edge_features = fault_tolerant.extract_edge_features
    edge_features.extract_edges_name = "edge-group-1"
    edge_features.extract_method_type = "Intersection Loops"
    edge_features.object_selection_list = ["flow_pipe", "main"]
    edge_features.insert_compound_child_task()
    fault_tolerant.extract_edge_features_child_1()

Identify regions
~~~~~~~~~~~~~~~~

.. code:: python

    identify_regions = fault_tolerant.identify_regions
    identify_regions.show_coordinates = True
    identify_regions.material_points_name = "fluid-region-1"
    identify_regions.selection_type = "zone"
    identify_regions.x = 377.322045740589
    identify_regions.y = -176.800676988458
    identify_regions.z = -37.0764628583475
    identify_regions.zone_selection_list = ["main.1"]
    identify_regions.insert_compound_child_task()
    fault_tolerant.identify_regions_child_1()

    identify_regions.show_coordinates = True
    identify_regions.material_points_name = "void-region-1"
    identify_regions.new_region_type = "void"
    identify_regions.selection_type = "object"
    identify_regions.object_selection_list = ["inlet-1", "inlet-2", "inlet-3", "main"]
    identify_regions.x = 374.722045740589
    identify_regions.y = -278.9775145640143
    identify_regions.z = -161.1700719416913
    identify_regions.insert_compound_child_task()
    fault_tolerant.identify_regions_child_2()

Define leakage threshold
~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    leakage_threshold = fault_tolerant.define_leakage_threshold
    leakage_threshold.add_child = "yes"
    leakage_threshold.flip_direction = True
    leakage_threshold.leakage_name = "leakage-1"
    leakage_threshold.plane_direction = "X"
    leakage_threshold.region_selection_single = "void-region-1"
    leakage_threshold.insert_compound_child_task()
    fault_tolerant.define_leakage_threshold_child_1()

Update regions settings
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    update_region = fault_tolerant.update_region_settings
    update_region.all_region_filter_categories = ["2"] * 5 + ["1"] * 2
    update_region.all_region_leakage_size_list = ["none"] * 6 + ["6.4"]
    update_region.all_region_linked_construction_surface_list = ["n/a"] * 6 + ["no"]
    update_region.all_region_mesh_method_list = ["none"] * 6 + ["wrap"]
    update_region.all_region_name_list = [
                "main",
                "flow_pipe",
                "outpipe3",
                "object2",
                "object1",
                "void-region-1",
                "fluid-region-1",
            ]
    update_region.all_region_overset_componen_list = ["no"] * 7
    update_region.all_region_source_list = ["object"] * 5 + ["mpt"] * 2
    update_region.all_region_type_list = ["void"] * 6 + ["fluid"]
    update_region.all_region_volume_fill_list = ["none"] * 6 + ["tet"]
    update_region.filter_category = "Identified Regions"
    update_region.all_region_leakage_size_list = [""]
    update_region.all_region_mesh_method_list = ["wrap"]
    update_region.all_region_name_list = ["fluid-region-1"]
    update_region.all_region_overset_componen_list = ["no"]
    update_region.all_region_type_list = ["fluid"]
    update_region.all_region_volume_fill_list = ["hexcore"]
    update_region.all_region_leakage_size_list = [""]
    update_region.all_region_mesh_method_list = ["wrap"]
    update_region.all_region_name_list = ["fluid-region-1"]
    update_region.all_region_overset_componen_list = ["no"]
    update_region.all_region_type_list = ["fluid"]
    update_region.all_region_volume_fill_list = ["tet"]
    update_region()

Choose mesh control options
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    mesh_control = fault_tolerant.setup_size_controls
    mesh_control.local_settings_name = "default-curvature"
    mesh_control.local_size_control_parameters.sizing_type = "curvature"
    mesh_control.object_selection_list = [
        "inlet-1",
        "inlet-2",
        "inlet-3",
    ]
    mesh_control.add_child_and_update(defer_update=False)
    mesh_control.local_settings_name = "default-proximity"
    mesh_control.local_size_control_parameters.sizing_type = "proximity"
    mesh_control.object_selection_list = [
        "inlet-1",
        "inlet-2",
        "inlet-3",
    ]
    mesh_control.add_child_and_update(defer_update=False)
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

    add_boundary_layer = fault_tolerant.add_boundary_layers
    add_boundary_layer.control_name = "aspect-ratio_1"
    add_boundary_layer.insert_compound_child_task()
    fault_tolerant.add_boundary_layers_child_1()

Generate volume mesh
~~~~~~~~~~~~~~~~~~~~

.. code:: python

    create_volume_mesh = fault_tolerant.create_volume_mesh_ftm
    create_volume_mesh.all_region_name_list = [
                "main",
                "flow_pipe",
                "outpipe3",
                "object2",
                "object1",
                "void-region-1",
                "fluid-region-1",
            ]
    create_volume_mesh.all_region_size_list = ["11.33375"] * 7
    create_volume_mesh.all_region_volume_fill_list = ["none"] * 6 + ["tet"]
    create_volume_mesh()

Switch to solution mode
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    solver_session = meshing_session.switch_to_solver()

2D workflow
-----------
Use the **2D*** workflow to perform common meshing operations on two-dimensional geometries.

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

    load_cad = two_dim_mesh.load_cad_geometry
    load_cad.file_name = import_file_name
    load_cad.length_unit = "mm"
    load_cad.refaceting.refacet = False
    load_cad()

Set regions and boundaries
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    update_boundaries = two_dim_mesh.update_boundaries
    update_boundaries.selection_type = "zone"
    update_boundaries()

Define global sizing
~~~~~~~~~~~~~~~~~~~~

.. code:: python

    global_sizing = two_dim_mesh.define_global_sizing
    global_sizing.curvature_normal_angle = 20
    global_sizing.max_size = 2000.0
    global_sizing.min_size = 5.0
    global_sizing.size_functions = "Curvature"
    global_sizing()

Adding BOI
~~~~~~~~~~

.. code:: python

    add_local_sizing = two_dim_mesh.add_local_sizing_wtm
    add_local_sizing.add_child = "yes"
    add_local_sizing.boi_control_name = "boi_1"
    add_local_sizing.boi_execution = "Body Of Influence"
    add_local_sizing.boi_face_label_list = ["boi"]
    add_local_sizing.boi_size = 50.0
    add_local_sizing.boi_zoneor_label = "label"
    add_local_sizing.draw_size_control = True
    add_local_sizing.add_child_and_update(defer_update=False)

Set edge sizing
~~~~~~~~~~~~~~~

.. code:: python

    add_local_sizing.add_child = "yes"
    add_local_sizing.boi_control_name = "edgesize_1"
    add_local_sizing.boi_execution = "Edge Size"
    add_local_sizing.boi_size = 5.0
    add_local_sizing.boi_zoneor_label = "label"
    add_local_sizing.draw_size_control = True
    add_local_sizing.edge_label_list = ["airfoil-te"]
    add_local_sizing.add_child_and_update(defer_update=False)

Set curvature sizing
~~~~~~~~~~~~~~~~~~~~

.. code:: python

    add_local_sizing.add_child = "yes"
    add_local_sizing.boi_control_name = "curvature_1"
    add_local_sizing.boi_curvature_normal_angle = 10
    add_local_sizing.boi_execution = "Curvature"
    add_local_sizing.boi_max_size = 2
    add_local_sizing.boi_min_size = 1.5
    add_local_sizing.boi_scope_to = "edges"
    add_local_sizing.boi_zoneor_label = "label"
    add_local_sizing.draw_size_control = True
    add_local_sizing.edge_label_list = ["airfoil"]
    add_local_sizing.add_child_and_update(defer_update=False)

Add boundary layer
~~~~~~~~~~~~~~~~~~

.. code:: python

    add_boundary_layers = two_dim_mesh.add_2d_boundary_layers
    add_boundary_layers.add_child = "yes"
    add_boundary_layers.control_name = "aspect-ratio_1"
    add_boundary_layers.number_of_layers = 4
    add_boundary_layers.offset_method_type = "aspect-ratio"
    add_boundary_layers.add_child_and_update(defer_update=False)

Generate surface mesh
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    # NOTE: Setting `show_advanced_options = True` is required to configure advanced preferences.
    # This dependency may be removed in a future release as the API evolves.
    generate_surface_mesh = two_dim_mesh.generate_initial_surface_mesh
    mesh_preferences = two_dim_mesh.generate_initial_surface_mesh.surface_2d_preferences
    mesh_preferences.show_advanced_options = True
    mesh_preferences.merge_edge_zones_based_on_labels = "no"
    mesh_preferences.merge_face_zones_based_on_labels = "no"
    generate_surface_mesh()

    two_dim_mesh.add_2d_boundary_layers_child_1.revert()
    two_dim_mesh.add_2d_boundary_layers_child_1.add_child = "yes"
    two_dim_mesh.add_2d_boundary_layers_child_1.control_name = "uniform_1"
    two_dim_mesh.add_2d_boundary_layers_child_1.first_layer_height = 2
    two_dim_mesh.add_2d_boundary_layers_child_1.number_of_layers = 4
    two_dim_mesh.add_2d_boundary_layers_child_1.offset_method_type = "uniform"
    two_dim_mesh.add_2d_boundary_layers_child_1()


    # NOTE: Setting `show_advanced_options = True` is required to configure advanced preferences.
    # This dependency may be removed in a future release as the API evolves.
    mesh_preferences.show_advanced_options = True
    mesh_preferences.merge_edge_zones_based_on_labels = "no"
    mesh_preferences.merge_face_zones_based_on_labels = "no"
    generate_surface_mesh()

Switch to solution mode
~~~~~~~~~~~~~~~~~~~~~~~

Switching to solver is not allowed in 2D Meshing mode.

Creating a new workflow
-----------------------
The following example shows you how to use ``create_workflow()`` to build a custom workflow.

Create workflow
~~~~~~~~~~~~~~~

.. code:: python

    import ansys.fluent.core as pyfluent
    from ansys.fluent.core import examples

    import_file_name = examples.download_file('mixing_elbow.pmdb', 'pyfluent/mixing_elbow')
    meshing_session = pyfluent.launch_fluent(
        mode=pyfluent.FluentMode.MESHING, precision=pyfluent.Precision.DOUBLE, processor_count=2
    )
    custom_workflow = meshing_session.create_workflow()

Insert first task
~~~~~~~~~~~~~~~~~

.. code:: python

    custom_workflow.insertable_tasks.import_geometry.insert()
    custom_workflow.import_geometry.file_name = import_file_name
    custom_workflow.import_geometry.length_unit = 'in'
    custom_workflow.import_geometry()

Saving a workflow
-----------------

The following example shows you how to use ``save_workflow()`` to persist the
current workflow definition to a ``.wft`` file for later reuse.

Save workflow
~~~~~~~~~~~~~

.. code:: python

    custom_workflow.save_workflow(file_path="full_path_to_the_file.wft")



Loading a saved workflow
------------------------
The following example shows you how to use ``load_workflow()`` to load a previously saved workflow.

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


Insert new task
---------------
You can insert tasks into a workflow using the workflow object.

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

When you insert the same task multiple times, duplicates are accessible by attribute names with numeric suffixes.

.. code:: python

    ig = watertight.import_geometry
    ig.insertable_tasks.import_boi_geometry.insert()
    ig.insertable_tasks.import_boi_geometry.insert()
    ig.insertable_tasks.import_boi_geometry.insert()
    assert watertight.import_boi_geometry.arguments()
    assert watertight.import_boi_geometry_1.arguments()
    assert watertight.import_boi_geometry_2.arguments()

.. Note::
    You can also access duplicate tasks by index:

   .. code:: python

       >>> watertight.import_boi_geometry
       task < import_boi_geometry: 0 >
       >>> watertight.import_boi_geometry[0]
       task < import_boi_geometry: 0 >
       >>> watertight.import_boi_geometry[1]
       task < import_boi_geometry: 1 >
       >>> watertight.import_boi_geometry[2]
       task < import_boi_geometry: 2 >

   Index 0 returns the first instance; accessing the task without an index is equivalent to indexing with 0.

   After inserting the tasks above, you can call ``children()`` to confirm the task list:

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


Current workflow
----------------
You can use the ``current_workflow`` to access the active workflow.

.. code:: python

    meshing_session.current_workflow

.. Note::
   ``current_workflow`` returns ``None`` if no workflow has been initialized.


Mark as updated
---------------
Use the ``mark_as_updated()`` to explicitly mark a task as updated.

.. code:: python

    watertight.import_geometry.mark_as_updated()


Renaming tasks in workflow
--------------------------
You can rename a task to any display name, including names that are not valid Python identifiers.
The task remains accessible by its original name or by the new display name as a string key.

.. code:: python

   >>> watertight.import_geometry.rename(new_name="I-G")
   >>> watertight.import_geometry["I-G"]
   task < import_geometry: 0 >
   >>> watertight.import_geometry
   task < import_geometry: 0 >




Deleting tasks from workflow
----------------------------
You can delete tasks individually or in groups. To delete multiple tasks at once,
pass task objects to the ``list_of_tasks`` argument of ``delete_tasks()``:

.. Note::
   ``delete_tasks()`` accepts a list of task objects instead of a list of task names.

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

       ig = watertight.import_geometry
       ig.insertable_tasks.import_boi_geometry.insert()
       ig.insertable_tasks.import_boi_geometry.insert()

       del watertight.import_boi_geometry[1]
       watertight.import_boi_geometry.delete()
       del watertight.create_regions


Workflow navigation enhancements
--------------------------------

You can traverse tasks within a workflow using navigation methods such as
``first_child()``, ``last_child()``, ``next()``, ``previous()``, ``parent()``,
and corresponding boolean checks (``has_parent()``, ``has_next()``, etc.):

.. code:: python

    >>> watertight = meshing.watertight()

    >>> task_1 = watertight.first_child()
    >>> task_1.has_parent()
    True
    >>> task_1.parent()
    <ansys.fluent.core.meshing.meshing_workflow_new.WatertightMeshingWorkflow at 0x22931166000>
    >>> task_1.has_previous()
    False  # As this is the first task in the workflow
    >>> task_1.has_next()
    True
    >>> assert task_1.first_child() is None  # It is a simple task with no children
    >>> assert task_1.last_child() is None

    >>> task_2 = task_1.next()
    >>> task_2
    task < add_local_sizing_wtm: 0 >

    >>> task_4 = task_2.next().next()
    >>> task_4
    task < describe_geometry: 0 >
    >>> task_4_1 = task_4.first_child()  # It is a compound task with children
    >>> task_4_1
    task < capping: 0 >

    >>> task_7 = watertight.last_child()
    >>> task_7
    task < create_volume_mesh_wtm: 0 >

    >>> task_7.has_previous()
    True
    >>> task_6 = task_7.previous()
    >>> task_6
    task < add_boundary_layers: 0 >

This enables navigation without relying on attribute names.
