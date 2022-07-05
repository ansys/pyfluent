Applying General Settings
=========================
PyFluent supports defining general settings using the :ref:`ref_solver_tui_commands` and 
:ref:`ref_settings`.

Solver TUI Commands
-------------------
The following examples demonstrate how you can use solver meshing commands
and setup units using
:ref:`ref_solver_tui_commands`:

Checking Mesh
~~~~~~~~~~~~~
mesh/check TUI: Performs various mesh consistency checks and displays a
report in the console that lists the domain extents, the volume statistics,
the face area statistics, and any warnings, as well as details about the
various checks and mesh failures (depending on the setting specified for
mesh/check-verbosity).

.. code:: python

    import ansys.fluent.core as pyfluent
    session = pyfluent.launch_fluent(precision='double', processor_count=2)
    session.solver.tui.file.read_case(case_file_name='file.cas.h5')
    session.solver.tui.mesh.check()

Reporting Mesh Quality
~~~~~~~~~~~~~~~~~~~~~~
mesh/quality TUI: Displays information about the quality of the mesh in the
console, including the minimum orthogonal quality and the maximum aspect ratio.
The level of detail displayed depends on the setting specified for
mesh/check-verbosity.

.. code:: python

    session.solver.tui.mesh.quality()

Scaling Mesh
~~~~~~~~~~~~
mesh/scale TUI: Prompts for the scaling factors in each of the active Cartesian
coordinate directions.

.. code:: python

    session.solver.tui.mesh.scale(1,1,1)

Defining Units
~~~~~~~~~~~~~~
define/units TUI: Sets unit conversion factors.

.. code:: python

    session.solver.tui.define.units('length', 'in')