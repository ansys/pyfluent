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
The ``solve.set.p_v_coupling`` TUI command selects which pressure-velocity coupling scheme to use.
Five schemes (Index-Model) are available: 20-SIMPLE, 21-SIMPLEC, 22-PISO, 24-Coupled,
and 25-Fractional Step.

The ``solve.set/gradient_scheme`` TUI sets the gradient options.

.. code:: python

    import ansys.fluent.core as pyfluent
    session = pyfluent.launch_fluent(precision='double', processor_count=2)
    session.solver.tui.file.read_case(case_file_name='file.cas.h5')
    session.solver.tui.solve.set.p_v_coupling(24) # Coupled
    session.solver.tui.solve.set.gradient_scheme('yes')    # Green-Gauss Node Based
    session.solver.tui.solve.set.gradient_scheme('no','yes') # Least Squares Cell Based
    
Selecting solution controls 
~~~~~~~~~~~~~~~~~~~~~~~~~~~
The ``solve.set.p_v_controls`` TUI sets pressure-velocity controls.

.. code:: python

    session.solver.tui.solve.set.p_v_controls(0.3,0.4) # Momentum and Pressure

Creating report definitions
~~~~~~~~~~~~~~~~~~~~~~~~~~~
The ``solve.report_definitions`` TUI enters the report definitions menu.

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
The ``solve.initialize`` TUI enters the flow initialization menu.

The ``solve.initialize.hyb_initialization`` TUI initializes using the hybrid
initialization method.

The ``solve.iterate`` TUI performs a specified number of iterations.

.. code:: python

    session.solver.tui.solve.initialize.hyb_initialization()
    session.solver.tui.solve.iterate(100)

Using settings objects
----------------------
The following example shows how you apply solution settings
using :ref:`ref_settings`.

.. code:: python

    session.solver.root.solution.initialization.hybrid_initialize()
    session.solver.root.solution.run_calculation.iterate(number_of_iterations=150)
