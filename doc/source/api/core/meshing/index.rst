.. _ref_meshing:

Meshing
=======
This module allows you to use Fluent meshing capabilities from Python.  Both
the meshing workflows and meshing TUI commands are available.

Workflow Example
----------------

.. code:: python

    import ansys.fluent.core as pyfluent
    session = pyfluent.launch_fluent(meshing_mode=True)
    session.start_transcript()
    session.workflow.InitializeWorkflow(WorkflowType='Watertight Geometry')
    session.workflow.TaskObject['Import Geometry'].Arguments = dict(FileName='cylinder.agdb')
    session.workflow.TaskObject['Import Geometry'].Execute()
    session.tui.meshing.mesh.check_mesh()
    exit()

TUI Commands Example
--------------------

.. code:: python

    import ansys.fluent.core as pyfluent
    session = pyfluent.launch_fluent(meshing_mode=True)
    session.tui.meshing.file.read_case("elbow.cas.gz")
    session.tui.meshing.switch_to_solution_mode("yes")
    session.tui.solver.define.models.unsteady_2nd_order("yes")
    exit()

.. currentmodule:: ansys.fluent.core.meshing

.. autosummary::
   :toctree: _autosummary

.. toctree::
   :maxdepth: 2
   :hidden:

   tui