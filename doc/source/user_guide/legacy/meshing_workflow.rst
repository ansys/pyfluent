.. _ref_legacy_meshing_workflow:

Legacy meshing interface (opt-in)
=================================

This page documents the legacy PyFluent meshing interface. It remains available when using
PyFluent with Ansys Fluent 2026 R1 and later (for example, Ansys Fluent 2027 R1). Use it to
run existing scripts without changes.

.. Note::
    This page documents the legacy PyFluent meshing interface for the API-based meshing infrastructure.
    It is distinct from PyFluent’s classic meshing workflow. See :ref:`ref_meshing_workflows_guide`.

Scope of this page
------------------
- What this page covers: how to opt in to the legacy interface and behaviors that differ from the enhanced workflow.
- What this page does not cover: an overview or migration guide. See :ref:`ref_new_meshing_workflows_guide` for the enhanced workflow.

Opt in to the legacy interface
------------------------------
Pass ``legacy=True`` to the workflow initializer to use the legacy interface:

.. code:: python

    watertight = meshing_session.watertight(legacy=True)
    fault_tolerant = meshing_session.fault_tolerant(legacy=True)
    # ...use the workflow as shown in the examples ...

Portability note
----------------
You can pass ``legacy=True`` unconditionally when using PyFluent with any Fluent version,
including PyFluent with Ansys Fluent 2026 R1 and later. This avoids version checks and keeps
scripts written for earlier releases working as-is.

Terminology
-----------
Historically, this interface was sometimes referred to as “enhanced.” In this documentation,
“legacy interface” means the pre–Ansys Fluent 2026 R1 PyFluent meshing API.

Fault-tolerant meshing workflow
-------------------------------
In the legacy fault-tolerant workflow, PartManagement and PMFileManagement are accessed
directly from the meshing session. Use these objects and their methods as shown below:

- meshing_session.PartManagement.InputFileChanged(...)
- meshing_session.PMFileManagement.FileManager.LoadFiles()
- meshing_session.PartManagement.Node["Meshing Model"].Copy(...)
- meshing_session.PartManagement.ObjectSetting["DefaultObjectSetting"].OneZonePer.set_state(...)

.. Note::
   Backward compatible: These entries are still supported in PyFLuent using
   Ansys Fluent 2026 R1 for legacy scripts.


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
   delete-by-name has been replaced by passing task objects to ``list_of_tasks``.
   Calling ``task.delete()`` on a task object still works.


.. code:: python

    watertight.delete_tasks(list_of_tasks=["create_volume_mesh_wtm", "add_boundary_layers"])
    watertight.update_regions.delete()
