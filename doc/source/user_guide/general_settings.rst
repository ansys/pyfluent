Applying general settings
=========================
PyFluent supports applying general settings using :ref:`ref_solver_tui_commands` and 
:ref:`ref_settings`.

The following examples shows how you use solver meshing commands
and set up units using :ref:`ref_solver_tui_commands`.

Checking the mesh
-----------------
The ``mesh.check`` TUI performs various mesh consistency checks and displays a
report in the console that lists domain extents, volume statistics,
face area statistics, any warnings, and information about various check and mesh
failures. THe level of information shown depends on the setting specified for
``mesh.check-verbosity``.

.. code:: python

    import ansys.fluent.core as pyfluent
    session = pyfluent.launch_fluent(precision='double', processor_count=2)
    session.solver.tui.file.read_case(case_file_name='file.cas.h5')
    session.solver.tui.mesh.check()

Reporting mesh quality
----------------------
The ``mesh.quality`` TUI displays information about the quality of the mesh in the
console, including the minimum orthogonal quality and maximum aspect ratio.
The level of information that is shown depends on the setting specified for
``mesh.check-verbosity``.

.. code:: python

    session.solver.tui.mesh.quality()

Scaling mesh
------------
The ``mesh.scale`` TUI prompts for the scaling factors in each of the active Cartesian
coordinate directions.

.. code:: python

    session.solver.tui.mesh.scale(1,1,1)

Defining units
--------------
The ``define.units`` TUI sets unit conversion factors.

.. code:: python

    session.solver.tui.define.units('length', 'in')