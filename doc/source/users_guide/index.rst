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
   tui_api
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
launches an instance of Ansys Fluent, running it as a server in the background.
:ref:`ref_user_guide_launch` provides a more detailed overview of the usage of
that function. The simplest scenario is to call it without arguments:

.. code:: python

    from ansys.fluent.core import launch_fluent

    solver_session = launch_fluent()

which starts Fluent in solution mode, while 

.. code:: python

    from ansys.fluent.core import launch_fluent

    meshing_session = launch_fluent(meshing_mode=True)

starts Fluent in meshing mode. If the ``meshing_mode`` argument were set to 
``False``, Fluent would be launched in solution mode, exactly equivalent to 
the first example. For the many other arguments that can be passed to 
``launch_fluent()``, see :ref:`ref_launcher_launcher` and
:ref:`ref_user_guide_launch`.

PyFluent can hold multiple, independent session objects, each providing full
access to Ansys Fluent capabilities relevant to its current mode (solution or
meshing).

A solution mode session has an active ``solver`` property, which provides two
distinct interfaces to the solver. The ``solver`` object has a ``tui`` property,
which is a complete Python exposure of the Fluent solver's actual Text 
User Interface. This interface allows straightforward execution of commands and 
modification of settings in a manner that will be familiar to existing Fluent 
users:

.. code:: python

    tui = solver_session.solver.tui

    tui.file.read_case(case_file_name="pipe.cas.h5")

    tui.define.models.energy("yes")

See :ref:`ref_solver_tui` for details of the full hierarchical API
(the Fluent solver _TUI_ API) under the ``tui`` object. Some guidance on programming
in terms of that API is provided here: :ref:`ref_user_guide_tui_api`. 

The same ``solver`` object also has a ``root`` property, which provides a 
different interface to the Fluent solver. The ``root`` object exposes most of the
solver capabilities covered by the ``tui`` object, while providing significant 
additional interface features that are not possible via ``tui``:

.. code:: python

    root = solver_session.solver.root

    root.file.read(file_type="case", file_name="pipe.cas.h5")

    root.setup.models.energy.enabled = True

    energy_is_enabled = root.setup.models.energy.enabled()

See :ref:`ref_settings` for details of the full hierarchical API
(the Fluent solver _settings_ API) under the ``root`` object. 
:ref:_ref_user_guide_solver_settings provides additional
guidance on using both `tui` and `root`.

A meshing mode session has an active ``meshing`` property, which provides
three interfaces to the mesher.

Like the ``solver`` object, the ``meshing`` object has a ``tui`` property, which
is a complete Python exposure of meshing's Text User Interface. Again, 
straightforward and familiar command and settings interactions are available:

.. code:: python

    tui = meshing_session.meshing.tui

    tui.mesh.prepare_for_solve("yes")

    tui.file.write_case("pipe.cas.h5")
    
See :ref:`ref_meshing_tui` for details of the full hierarchical API under the
``tui`` object.

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
interaction via the ``scheme_eval`` property. The argument
to string_eval in the following example is a string that contains any Scheme
code that could be executed in Fluent for the current mode:

.. code:: python

    unsteady = solver_session.scheme_eval.string_eval("(rp-unsteady?)")​

Surface field and mesh data services are available in solution mode only via
the ``field_data`` session property (something to link to) (check if correct):

.. code:: python

    surface_data = solver_session.field_data.get_fields()

See here: :ref:`ref_field_data` for more details about ``field_data``.

The connection status of any session can be verified as follows
("SERVING" is returned if and only if the connection is healthy):

.. code:: python

    health = solver_session.check_health()​​

Streaming of the Fluent transcript can be stopped/started as follows (it is 
automatically started by default):
 
.. code:: python

    solver_session.stop_transcript()​​

    solver_session.start_transcript()​​

Streaming of events pertaining to various, specific solver event types can be
enabled/disabled via the ``events_manager`` property of a solution-mode session:

.. code:: python

    solver_session.events_manager.start()

Event management is detailed further here: :ref:`ref_events`.

The global logging level can be controlled at any time:

.. code:: python

    import ansys.fluent.core as pyfluent
    pyfluent.set_log_level('DEBUG') # by default, only errors are shown


