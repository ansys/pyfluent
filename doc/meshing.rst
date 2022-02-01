Meshing TUI and workflow example
================================

.. code:: python

    import ansys.fluent as pyfluent
    session = pyfluent.launch_fluent(meshing_mode=True)
    session.workflow.initialize_workflow(workflow_type='Watertight Geometry')
    session.workflow.task_object['Import Geometry'].arguments = dict(file_name='cylinder.agdb')
    session.workflow.task_object['Import Geometry'].execute()
    session.tui.meshing.mesh.check_mesh()
    exit()


.. code:: python

    import ansys.fluent as pyfluent
    session = pyfluent.launch_fluent(meshing_mode=True)
    session.tui.meshing.file.read_case("elbow.cas.gz")
    session.tui.meshing.switch_to_solution_mode("yes")
    session.tui.solver.define.models.unsteady_2nd_order("yes")
    exit()