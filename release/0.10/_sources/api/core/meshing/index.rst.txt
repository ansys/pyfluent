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
    session.meshing.workflow.InitializeWorkflow(WorkflowType='Watertight Geometry')
    session.meshing.workflow.TaskObject['Import Geometry'].Arguments = dict(FileName='cylinder.agdb')
    session.meshing.workflow.TaskObject['Import Geometry'].Execute()
    session.meshing.tui.mesh.check_mesh()
    exit()
	
Existing Fluent meshing workflows journals can also be converted to the
session based PyFluent scripts with some manual modifications.
For example:

Fluent Journal:

.. code-block::

  (%py-exec "workflow.InitializeWorkflow(WorkflowType=r'Watertight Geometry')")
  (%py-exec "workflow.TaskObject['Import Geometry'].Arguments.setState({r'FileName': r'file.pmdb',r'LengthUnit': r'in',})")
  (%py-exec "workflow.TaskObject['Import Geometry'].Execute()")
  (%py-exec "workflow.TaskObject['Add Local Sizing'].AddChildToTask()")
  (%py-exec "workflow.TaskObject['Add Local Sizing'].Execute()")
  (%py-exec "workflow.TaskObject['Generate the Surface Mesh'].Arguments.setState({r'CFDSurfaceMeshControls': {r'MaxSize': 0.3,},})")
  (%py-exec "workflow.TaskObject['Generate the Surface Mesh'].Execute()")
  (%py-exec "workflow.TaskObject['Describe Geometry'].UpdateChildTasks(SetupTypeChanged=False)")
  (%py-exec "workflow.TaskObject['Describe Geometry'].Arguments.setState({r'SetupType': r'The geometry consists of only fluid regions with no voids',})")
  (%py-exec "workflow.TaskObject['Describe Geometry'].UpdateChildTasks(SetupTypeChanged=True)")
  (%py-exec "workflow.TaskObject['Describe Geometry'].Execute()")
  (%py-exec "workflow.TaskObject['Update Boundaries'].Arguments.setState({r'BoundaryLabelList': [r'wall-inlet'],r'BoundaryLabelTypeList': [r'wall'],r'OldBoundaryLabelList': [r'wall-inlet'],r'OldBoundaryLabelTypeList': [r'velocity-inlet'],})")
  (%py-exec "workflow.TaskObject['Update Boundaries'].Execute()")
  (%py-exec "workflow.TaskObject['Update Regions'].Execute()")
  (%py-exec "workflow.TaskObject['Add Boundary Layers'].AddChildToTask()")
  (%py-exec "workflow.TaskObject['Add Boundary Layers'].InsertCompoundChildTask()")
  (%py-exec "workflow.TaskObject['smooth-transition_1'].Arguments.setState({r'BLControlName': r'smooth-transition_1',})")
  (%py-exec "workflow.TaskObject['Add Boundary Layers'].Arguments.setState({})")
  (%py-exec "workflow.TaskObject['smooth-transition_1'].Execute()")
  (%py-exec "workflow.TaskObject['Generate the Volume Mesh'].Arguments.setState({r'VolumeFill': r'poly-hexcore',r'VolumeFillControls': {r'HexMaxCellLength': 0.3,},})")
  (%py-exec "workflow.TaskObject['Generate the Volume Mesh'].Execute()")

Equivalent PyFluent Journal:

.. code:: python

  session.meshing.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")
  session.meshing.workflow.TaskObject["Import Geometry"].Arguments = dict(
      FileName=import_filename, LengthUnit="in"
  )
  session.meshing.workflow.TaskObject["Import Geometry"].Execute()
  session.meshing.workflow.TaskObject["Add Local Sizing"].AddChildToTask()
  session.meshing.workflow.TaskObject["Add Local Sizing"].Execute()
  session.meshing.workflow.TaskObject["Generate the Surface Mesh"].Arguments = {
      "CFDSurfaceMeshControls": {"MaxSize": 0.3}
  }
  session.meshing.workflow.TaskObject["Generate the Surface Mesh"].Execute()
  session.meshing.workflow.TaskObject["Describe Geometry"].UpdateChildTasks(
      SetupTypeChanged=False
  )
  session.meshing.workflow.TaskObject["Describe Geometry"].Arguments = dict(
      SetupType="The geometry consists of only fluid regions with no voids"
  )
  session.meshing.workflow.TaskObject["Describe Geometry"].UpdateChildTasks(
      SetupTypeChanged=True
  )
  session.meshing.workflow.TaskObject["Describe Geometry"].Execute()
  session.meshing.workflow.TaskObject["Update Boundaries"].Arguments = {
      "BoundaryLabelList": ["wall-inlet"],
      "BoundaryLabelTypeList": ["wall"],
      "OldBoundaryLabelList": ["wall-inlet"],
      "OldBoundaryLabelTypeList": ["velocity-inlet"],
  }
  session.meshing.workflow.TaskObject["Update Boundaries"].Execute()
  session.meshing.workflow.TaskObject["Update Regions"].Execute()
  session.meshing.workflow.TaskObject["Add Boundary Layers"].AddChildToTask()
  session.meshing.workflow.TaskObject["Add Boundary Layers"].InsertCompoundChildTask()
  session.meshing.workflow.TaskObject["smooth-transition_1"].Arguments = {
      "BLControlName": "smooth-transition_1",
  }
  session.meshing.workflow.TaskObject["Add Boundary Layers"].Arguments = {}
  session.meshing.workflow.TaskObject["smooth-transition_1"].Execute()
  session.meshing.workflow.TaskObject["Generate the Volume Mesh"].Arguments = {
      "VolumeFill": "poly-hexcore",
      "VolumeFillControls": {
          "HexMaxCellLength": 0.3,
      },
  }
  session.meshing.workflow.TaskObject["Generate the Volume Mesh"].Execute()

TUI Commands Example
--------------------

.. code:: python

    import ansys.fluent.core as pyfluent
    session = pyfluent.launch_fluent(meshing_mode=True)
    session.meshing.tui.file.read_case("elbow.cas.gz")
    session.meshing.tui.switch_to_solution_mode("yes")
    session.solver.tui.define.models.unsteady_2nd_order("yes")
    exit()

.. currentmodule:: ansys.fluent.core.meshing

.. autosummary::
   :toctree: _autosummary

.. toctree::
   :maxdepth: 2
   :hidden:

   tui/index
   datamodel/index