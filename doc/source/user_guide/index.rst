.. _ref_user_guide:

==========
User guide
==========
Anyone who wants to use PyFluent can import its Python modules and develop
Python code to control and monitor Ansys Fluent. 

..
   This toctree must be a top level index to get it to show up in
   pydata_sphinx_theme

.. toctree::
   :maxdepth: 1
   :hidden:

   launching_ansys_fluent
   tui_commands
   meshing_workflows
   general_settings
   solver_settings
   models
   materials
   boundary_conditions
   solution


Overview
--------
You use the :func:`launch_fluent() <ansys.fluent.core.launcher.launcher.launch_fluent>` method
to launch an instance of Fluent that runs as a server in the background.

You can launch Fluent in solution mode with:

.. code:: python

    from ansys.fluent.core import launch_fluent

    solver = launch_fluent(mode="solver")

You can launch Fluent in meshing mode with: 

.. code:: python

    from ansys.fluent.core import launch_fluent

    meshing = launch_fluent(mode="meshing")


For more information, see :ref:`ref_user_guide_launch` 
and :ref:`ref_launcher_launcher`.

You can use PyFluent to create and initialize multiple, independent session
objects. Each session object provides full access to the Fluent components
relevant to the session's current mode (solution or meshing).

Solution mode session
---------------------
A solution mode session has an active ``solver`` object that provides two
distinct interfaces to the solver:

- ``tui`` object
- ``root`` object

For general guidance on using these two objects, see
:ref:`ref_user_guide_solver_settings`.

Solver ``tui`` object
~~~~~~~~~~~~~~~~~~~~~
The solver ``tui`` object is a complete Python exposure of the Fluent solver TUI
(text user interface). This object allows straightforward execution of solver
commands and modification of solve settings in a manner that is familiar to
existing Fluent users:

.. code:: python

    tui = solver.tui

    tui.file.read_case("pipe.cas.h5")

    tui.define.models.energy("yes")

For the full hierarchy under the solver ``tui`` object, see :ref:`ref_solver_tui_commands`.
For general guidance on using TUI commands, see :ref:`ref_user_guide_tui_commands`. 

Solver ``root`` object
~~~~~~~~~~~~~~~~~~~~~~
The solver ``root`` object exposes most of the solver capabilities covered by
the solver ``tui`` object and provides significant additional interface features
that are not possible via the ``tui`` object:

.. code:: python

    solver.file.read(file_type="case", file_name="pipe.cas.h5")

    solver.setup.models.energy.enabled = True

    energy_is_enabled = solver.setup.models.energy.enabled()

For the full hierarchy under the solver ``root`` object, see :ref:`ref_solver_tui`.
For additional interface features, see :ref:`ref_settings`.

Meshing mode session
--------------------
A meshing mode session has an active ``meshing`` object that provides two
distinct interfaces to the mesher:

- ``tui`` object
- meshing workflow, which consists of ``meshing`` and ``workflow`` properties and the
  ``PartManagement`` and ``PMFileMangement`` classes

Meshing ``tui`` object
~~~~~~~~~~~~~~~~~~~~~~
The meshing ``tui`` object is a complete Python exposure of the Fluent meshing
TUI (text user interface). This object allows straightforward execution of
meshing commands and modification of meshing settings in a manner that is
familiar to existing Fluent users:

.. code:: python

    tui = meshing_session.tui

    tui.mesh.prepare_for_solve("yes")

    tui.file.write_case("pipe.cas.h5")
    
For the full hierarchy under the meshing ``tui`` object, see
:ref:`ref_meshing_tui`. For general guidance on using TUI commands, see
:ref:`ref_user_guide_tui_commands`. 

``Meshing`` and ``Workflow`` properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The ``meshing`` object has ``meshing`` and ``workflow`` properties that together
provide access to Fluent's meshing workflows. This interface is consistent with
the Python meshing workflow interface that Fluent meshing exposes directly:

.. code:: python

    workflow = meshing_session.workflow

    workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")

    import_geometry = workflow.TaskObject["Import Geometry"]

    import_geometry.Arguments = {"FileName":"pipe.scdoc.pmdb"}

    import_geometry.Execute()

    meshing = meshing_session.meshing

    meshing.GlobalSettings.LengthUnit.set_state("mm")

For additional examples, see :ref:`ref_user_guide_meshing_workflows`.
For information on the full interface, see :ref:`ref_meshing_datamodel`.

Session object
--------------
In either a solution or meshing mode session, the ``session`` object provides a
more direct interaction via its ``scheme_eval`` attribute:

.. code:: python

    unsteady = solver.scheme_eval.scheme_eval("(rp-unsteady?)")

The argument to ``scheme_eval`` is a string that contains any scheme code that
can be executed in Fluent for the current mode.

Surface field and mesh data services are available in solution mode only via the
``field_data`` object attribute of the session object:

.. code:: python

    surface_data = solver.field_data.get_fields()

For more information, see :ref:`ref_field_data`.

The connection status of any session can be verified with:

.. code:: python

    health = solver.check_health()

``"SERVING"`` is returned if and only if the connection is healthy.

Streaming
---------
Streaming of a Fluent transcript is automatically started by default. You can
stop and start the streaming of a transcript manually with:
 
.. code:: python

    solver.stop_transcript()

    solver.start_transcript()

You can enable and disable the streaming of events pertaining to various solver
event types via the ``events_manager`` attribute of a solution mode session:

.. code:: python

    solver.events_manager.start()

For more information, see :ref:`ref_events`.

Global logging
--------------
You can control the global logging level at any time with:

.. code:: python

    import ansys.fluent.core as pyfluent
    pyfluent.set_log_level("DEBUG") # by default, only errors are shown

