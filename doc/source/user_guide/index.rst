.. _ref_user_guide:

==========
User guide
==========
Anyone who wants to use PyFluent can import its Python modules develop
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
The function :func:`launch_fluent() <ansys.fluent.core.launcher.launcher.launch_fluent>`
launches an instance of Fluent, running it as a server in the background. You can launch 
Fluent in solution mode with no arguments:

.. code:: python

    from ansys.fluent.core import launch_fluent

    solver_session = launch_fluent()

You can launch Fluent in meshing mode with: 

.. code:: python

    from ansys.fluent.core import launch_fluent

    meshing_session = launch_fluent(meshing_mode=True)

Setting the ``meshing_mode`` argument to ``False`` launches Fluent in solution mode. 

For more information, see :ref:`ref_user_guide_launch` 
and the API topic :ref:`ref_launcher_launcher`.

PyFluent can create and initialize multiple, independent session objects. Each session
object providings full access to Fluent capabilities relevant to the session's current
mode (solution or meshing).

Solution mode session
---------------------
A solution mode session has an active ``solver`` object, which provides two
distinct interfaces to the solver. The ``solver`` object has a ``tui`` object,
which is a complete Python exposure of the Fluent solver's TUI (text 
user interface). This interface allows straightforward execution of commands and 
modification of settings in a manner that is familiar to existing Fluent 
users:

.. code:: python

    tui = solver_session.solver.tui

    tui.file.read_case(case_file_name="pipe.cas.h5")

    tui.define.models.energy("yes")

For the full hierarchy under the ``tui`` object, see :ref:`ref_solver_tui_commands`.
For general guidance on programming in terms of this interface, see :ref:`ref_user_guide_tui_commands`. 

The same ``solver`` object also has a ``root`` object, which provides a 
different interface to the Fluent solver. The ``root`` object exposes most of the
solver capabilities covered by the ``tui`` object, while providing significant 
additional interface features that are not possible via the ``tui`` object:

.. code:: python

    root = solver_session.solver.root

    root.file.read(file_type="case", file_name="pipe.cas.h5")

    root.setup.models.energy.enabled = True

    energy_is_enabled = root.setup.models.energy.enabled()

For more information, see :ref:`ref_settings`. For the full hierarchy under the ``root``
object, see the API topic :ref:`ref_solver_tui`.

For general guidance on using both the  ``tui`` and ``root`` objects, see
:ref:`ref_user_guide_solver_settings`.

Meshing mode session
--------------------
A meshing mode session has an active ``meshing`` object, which provides
three interfaces to the mesher.

Like the ``solver`` object, the ``meshing`` object has a ``tui`` object, which
is a complete Python exposure of meshing's TUI (text user interface). Again, 
straightforward and familiar command and settings interactions are available:

.. code:: python

    tui = meshing_session.meshing.tui

    tui.mesh.prepare_for_solve("yes")

    tui.file.write_case("pipe.cas.h5")
    
For the full hierarchy under the ``tui`` object, see :ref:`ref_meshing_tui`.
As mentioned earlier, for general guidance, see :ref:`ref_user_guide_tui_commands`. 

In addition, the ``meshing`` object has ``meshing`` and ``workflow`` properties,
which together provide access to Fluent's `meshing workflows`. This interface
is consistent with the Python meshing workflow interface that Fluent meshing
exposes directly:

.. code:: python

    workflow = meshing_session.meshing.workflow

    workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")

    import_geometry = workflow.TaskObject["Import Geometry"]

    import_geometry.Arguments = {"FileName":"pipe.scdoc.pmdb"}

    import_geometry.Execute()

    meshing = meshing_session.meshing.meshing

    meshing.GlobalSettings.LengthUnit.setState("mm")

For additional examples, see :ref:`ref_user_guide_meshing_workflows`.
For information on the full interface, see :ref:`ref_meshing_datamodel`.

Session object
--------------
A session object in either the solution or meshing mode provides a more direct
interaction via its ``scheme_eval`` attribute. Consider this example:

.. code:: python

    unsteady = solver_session.scheme_eval.scheme_eval("(rp-unsteady?)")

The argument to ``scheme_eval`` is a string that contains any scheme
code that can be executed in Fluent for the current mode. Surface field
and mesh data services are available in solution mode only via
the ``field_data`` object attribute of the session object:

.. code:: python

    surface_data = solver_session.field_data.get_fields()

For more information about ``field_data``, see :ref:`ref_field_data`.

The connection status of any session can be verified with:

.. code:: python

    health = solver_session.check_health()

``"SERVING"`` is returned if and only if the connection is healthy.

Streaming
---------
Streaming of the Fluent transcript is automatically started by default.
You can stop it and start it manually with:
 
.. code:: python

    solver_session.stop_transcript()

    solver_session.start_transcript()

You can enable and disable the streaming of events pertaining to various,
specific solver event types via the ``events_manager`` attribute of a solution-mode session:

.. code:: python

    solver_session.events_manager.start()

For more information on event management, see :ref:`ref_events`.

Global logging
--------------
You can control the global logging level at any time with:

.. code:: python

    import ansys.fluent.core as pyfluent
    pyfluent.set_log_level('DEBUG') # by default, only errors are shown

