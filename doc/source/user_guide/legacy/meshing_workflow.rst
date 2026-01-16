.. _ref_legacy_meshing_workflow:

Legacy meshing workflows (prior to Ansys Fluent 2026 R1)
========================================================

This page documents the legacy meshing workflow interface that existed in PyFluent
versions prior to using Ansys Fluent 2026 R1. Use the enhanced workflow for all new scripts.
If you need to keep older scripts working without changes, you can initialize a workflow
with legacy semantics by passing ``legacy=True``.

Portability note
----------------
You can pass ``legacy=True`` unconditionally in PyFluent using any Fluent version, including
Ansys Fluent 2026 R1 and later. This lets you avoid version checks and keep scripts
written for earlier releases working as-is.

For the enhanced workflow and examples, see :ref:`ref_new_meshing_workflows_guide`.


Fault-tolerant meshing workflow
-------------------------------
In the legacy fault-tolerant workflow, Part and File Management use camel-case
attributes and methods accessed directly on the meshing session like
``meshing_session.PartManagement.*``,  ``meshing_session.PMFileManagement.FileManager.*``,
``InputFileChanged`` and ``LoadFiles``.

.. Note::
   Backward compatible: These camel-case Part/File Management entries are still
   supported in Ansys Fluent 2026 R1 for legacy scripts. The recommended approach
   in 2026 R1 and later is to use the enhanced workflow attributes, for example
   ``fault_tolerant.parts.*`` and ``fault_tolerant.parts_files.file_manager.*``.


Import CAD and part management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    import ansys.fluent.core as pyfluent
    from ansys.fluent.core import examples

    import_file_name = examples.download_file(
        "exhaust_system.fmd", "pyfluent/exhaust_system"
    )
    meshing_session = pyfluent.launch_fluent(precision=pyfluent.Precision.DOUBLE, processor_count=2, mode=pyfluent.FluentMode.MESHING)

    fault_tolerant = meshing_session.fault_tolerant(legacy=True)
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


Renaming tasks in workflow
--------------------------
In the legacy workflow, renaming a task updates its Python attribute path.
Access the task by the new name.

.. Note::
   Not backward compatible: In the enhanced workflow (Ansys Fluent 2026 R1 and later),
   changing a task’s display name does not change its Python attribute path. Update
   scripts to the new access pattern or pass ``legacy=True`` to preserve legacy
   rename behavior.

.. code:: python

    watertight.import_geometry.rename(new_name="import_geom_wtm")
    assert watertight.import_geom_wtm


Deleting tasks from workflow
----------------------------
In the legacy workflow, you delete tasks by passing their Python attribute
names as strings in ``list_of_tasks``.

.. Note::
   Partly backward compatible: In the enhanced workflow (Ansys Fluent 2026 R1 and later),
   delete-by-name has been replaced by passing task objects to ``list_of_tasks``
   (for example, ``watertight.delete_tasks(list_of_tasks=[watertight.create_volume_mesh_wtm, watertight.add_boundary_layers])``).
   Calling ``task.delete()`` on a task object still works.


.. code:: python

    watertight.delete_tasks(list_of_tasks=["create_volume_mesh_wtm", "add_boundary_layers"])
    watertight.update_regions.delete()
