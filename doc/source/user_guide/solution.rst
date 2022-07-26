Applying solution settings
==========================

PyFluent allows you to apply solution settings, initialize, and solve using 
:ref:`ref_solver_tui_commands` and :ref:`ref_settings`.

Using solver TUI commands
-------------------------
The following examples show how you apply solution settings
using :ref:`ref_solver_tui_commands`.

Selecting solution methods 
~~~~~~~~~~~~~~~~~~~~~~~~~~
The following example shows a comparison between the TUI command and the
Python code for selecting the pressure velocity coupling scheme and setting
the gradient options. Five solution methods (Index-Model) are available:
20-SIMPLE, 21-SIMPLEC, 22-PISO, 24-Coupled, and 25-Fractional Step.

**TUI command**

.. code:: scheme

    /solve/set/p-v-coupling 24
    /solve/set/gradient-scheme yes
    /solve/set/gradient-scheme no yes 

**Python code**

.. code:: python

    import ansys.fluent.core as pyfluent
    session = pyfluent.launch_fluent(precision='double', processor_count=2)
    session.solver.tui.file.read_case(case_file_name='file.cas.h5')
    session.solver.tui.solve.set.p_v_coupling(24) # Coupled
    session.solver.tui.solve.set.gradient_scheme('yes')    # Green-Gauss Node Based
    session.solver.tui.solve.set.gradient_scheme('no','yes') # Least Squares Cell Based
    
Selecting solution controls 
~~~~~~~~~~~~~~~~~~~~~~~~~~~
The following example shows a comparison between the TUI command and the
Python code for selecting the pressure velocity controls.

**TUI command**

.. code:: scheme

    /solve/set/p-v-controls 0.3 0.4

**Python code**

.. code:: python

    session.solver.tui.solve.set.p_v_controls(0.3,0.4) # Momentum and Pressure

Creating report definitions
~~~~~~~~~~~~~~~~~~~~~~~~~~~
The following example shows a comparison between the TUI command and the
Python code for creating report definitions.

**TUI command**

.. code:: scheme

    /solve/report-definitions outlet-temp-avg surface-massavg field temperature surface-names outlet () quit

**Python code**

.. code:: python

    session.solver.tui.solve.report_definitions.add(
        'outlet-temp-avg',
        'surface-massavg',
        'field',
        'temperature',
        'surface-names',
        'outlet',
        '()',
        'quit',
    )

Initializing and solving 
~~~~~~~~~~~~~~~~~~~~~~~~
The following example shows a comparison between the TUI command and the
Python code for initializing and performing a specified number of iterations.

**TUI command**

.. code:: scheme

    /solve/initialize/hyb-initialization
    /solve/iterate 100

**Python code**

.. code:: python

    session.solver.tui.solve.initialize.hyb_initialization()
    session.solver.tui.solve.iterate(100)

Using settings objects
----------------------
The following example shows how you apply solution settings
using :ref:`ref_settings`.

**Python code**

.. code:: python

    session.solver.root.solution.initialization.hybrid_initialize()
    session.solver.root.solution.run_calculation.iterate(number_of_iterations=150)
