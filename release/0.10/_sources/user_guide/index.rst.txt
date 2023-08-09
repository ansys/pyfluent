.. _ref_user_guide:

==========
User Guide
==========
This page introduces the PyFluent library for anyone who wants to
import its Python modules and start to develop Python code to control
and monitor Ansys Fluent. 


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
========
The function, :func:`launch_fluent() <ansys.fluent.core.launcher.launcher.launch_fluent>`
launches an instance of Ansys Fluent, running it as a server in the background. Launching 
in solution mode requires no arguments:

.. code:: python

    from ansys.fluent.core import launch_fluent

    solver_session = launch_fluent()

while: 

.. code:: python

    from ansys.fluent.core import launch_fluent

    meshing_session = launch_fluent(meshing_mode=True)

starts Fluent in meshing mode. If the ``meshing_mode`` argument were set to 
``False``, Fluent would be launched in solution mode, exactly equivalent to 
the first example. You can read more in the user guide on :ref:`ref_user_guide_launch` 
and the API documentation on :ref:`ref_launcher_launcher`.

PyFluent can create and initialize multiple, independent session objects, each providing full
access to Ansys Fluent capabilities relevant to its current mode (solution or
meshing).

A solution mode session has an active ``solver`` object, which provides two
distinct interfaces to the solver. The ``solver`` object has a ``tui`` object,
which is a complete Python exposure of the Fluent solver's actual Text 
User Interface. This interface allows straightforward execution of commands and 
modification of settings in a manner that will be familiar to existing Fluent 
users:

.. code:: python

    tui = solver_session.solver.tui

    tui.file.read_case(case_file_name="pipe.cas.h5")

    tui.define.models.energy("yes")

See :ref:`ref_solver_tui_commands` for details of the full hierarchy
under the ``tui`` object. Some general guidance on 
programming in terms of such an interface can be found in :ref:`ref_user_guide_tui_commands`. 

The same ``solver`` object also has a ``root`` object, which provides a 
different interface to the Fluent solver. The ``root`` object exposes most of the
solver capabilities covered by the ``tui`` object, while providing significant 
additional interface features that are not possible via the ``tui`` object:

.. code:: python

    root = solver_session.solver.root

    root.file.read(file_type="case", file_name="pipe.cas.h5")

    root.setup.models.energy.enabled = True

    energy_is_enabled = root.setup.models.energy.enabled()

See :ref:`ref_settings` Read more about the full hierarchy of :ref:`ref_settings`
under the ``root`` object. :ref:`ref_user_guide_solver_settings` provides additional
guidance on using both the ``tui`` and ``root`` objects.

A meshing mode session has an active ``meshing`` object, which provides
three interfaces to the mesher.

Like the ``solver`` object, the ``meshing`` object has a ``tui`` object, which
is a complete Python exposure of meshing's Text User Interface. Again, 
straightforward and familiar command and settings interactions are available:

.. code:: python

    tui = meshing_session.meshing.tui

    tui.mesh.prepare_for_solve("yes")

    tui.file.write_case("pipe.cas.h5")
    
See :ref:`ref_meshing_tui` for details of the full hierarchy under the
``tui`` object. As mentioned above, :ref:`ref_user_guide_tui_commands` contains
more general guidance. 

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

See :ref:`ref_user_guide_meshing_workflows` for further examples. The full interface
is documented here: :ref:`ref_meshing_datamodel`.

A session object in either solution or meshing mode provides a more direct
interaction via its ``scheme_eval`` attribute. The argument
to string_eval in the following example is a string that contains any Scheme
code that could be executed in Fluent for the current mode:

.. code:: python

    unsteady = solver_session.scheme_eval.scheme_eval("(rp-unsteady?)")

Surface field and mesh data services are available in solution mode only via
the ``field_data`` object attribute of the session object:

.. code:: python

    surface_data = solver_session.field_data.get_fields()

See here: :ref:`ref_field_data` for more details about ``field_data``.

The connection status of any session can be verified as follows
("SERVING" is returned if and only if the connection is healthy):

.. code:: python

    health = solver_session.check_health()

Streaming of the Fluent transcript can be stopped/started as follows (it is 
automatically started by default):
 
.. code:: python

    solver_session.stop_transcript()

    solver_session.start_transcript()

Streaming of events pertaining to various, specific solver event types can be
enabled/disabled via the ``events_manager`` attribute of a solution-mode session:

.. code:: python

    solver_session.events_manager.start()

Event management is detailed further here: :ref:`ref_events`

The global logging level can be controlled at any time:

.. code:: python

    import ansys.fluent.core as pyfluent
    pyfluent.set_log_level('DEBUG') # by default, only errors are shown


