Applying general settings
=========================
PyFluent supports applying general settings using :ref:`ref_solver_tui_commands` and 
:ref:`ref_settings`.

The following examples shows how you use solver meshing commands
and set up units using :ref:`ref_solver_tui_commands`.

Checking the mesh
-----------------
The following example shows a comparison between the TUI command and the
Python code for performing mesh consistency checks and displaying a
report in the console that lists domain extents, volume statistics,
face area statistics, any warnings, and information about failures.
The level of information shown depends on the setting specified for
the verbosity (level 0 to 3).

**TUI command**

.. code:: scheme

    /mesh/check
    /mesh/check-verbosity 1

**Python code**

.. code:: python

    import ansys.fluent.core as pyfluent
    session = pyfluent.launch_fluent(precision='double', processor_count=2)
    session.solver.tui.file.read_case(case_file_name='file.cas.h5')
    session.solver.tui.mesh.check()

Reporting mesh quality
----------------------
The following example shows a comparison between the TUI command and the
Python code for displaying information about the quality of the mesh in the
console, including the minimum orthogonal quality and maximum aspect ratio.

**TUI command**

.. code:: scheme

    /mesh/quality

**Python code**

.. code:: python

    session.solver.tui.mesh.quality()

Scaling mesh
------------
The following example shows a comparison between the TUI command and the
Python code for the scaling the mesh in each of the active Cartesian
coordinate directions.

**TUI command**

.. code:: scheme

    /mesh/scale 1 1 1

**Python code**

.. code:: python

    session.solver.tui.mesh.scale(1,1,1)

Defining units
--------------
The following example shows a comparison between the TUI command and the
Python code for setting the unit conversion factors.

**TUI command**

.. code:: scheme

    /define/units length 'in'

**Python code**

.. code:: python

    session.solver.tui.define.units('length', 'in')