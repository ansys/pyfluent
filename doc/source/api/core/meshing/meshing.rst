Meshing TUI and workflow example
================================

.. code:: python

    import ansys.fluent.core as pyfluent
    session = pyfluent.launch_fluent(meshing_mode=True)
    session.start_transcript()
    session.workflow.InitializeWorkflow(WorkflowType='Watertight Geometry')
    session.workflow.TaskObject['Import Geometry'].Arguments = dict(FileName='cylinder.agdb')
    session.workflow.TaskObject['Import Geometry'].Execute()
    session.tui.meshing.mesh.check_mesh()
    exit()


.. code:: python

    import ansys.fluent.core as pyfluent
    session = pyfluent.launch_fluent(meshing_mode=True)
    session.tui.meshing.file.read_case("elbow.cas.gz")
    session.tui.meshing.switch_to_solution_mode("yes")
    session.tui.solver.define.models.unsteady_2nd_order("yes")
    exit()