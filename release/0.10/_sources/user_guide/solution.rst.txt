Applying Solution Settings
==========================

PyFluent allows you to apply solution settings, initialize and solve using both 
:ref:`ref_solver_tui_commands` and :ref:`ref_settings`.

Solver TUI Commands
-------------------
The following example demonstrates how you can apply solution settings
using :ref:`ref_solver_tui_commands`:

Selecting Solution Methods 
~~~~~~~~~~~~~~~~~~~~~~~~~~
solve/set/p-v-coupling TUI: Selects which pressure-velocity coupling scheme is to be used.

Five schemes are available: (Index-Model) 20-SIMPLE, 21-SIMPLEC, 22-PISO,
24-Coupled, 25-Fractional Step

solve/set/gradient-scheme: Sets gradient options.

.. code:: python

    import ansys.fluent.core as pyfluent
    session = pyfluent.launch_fluent(precision='double', processor_count=2)
    session.solver.tui.file.read_case(case_file_name='file.cas.h5')
    session.solver.tui.solve.set.p_v_coupling(24) # Coupled
    session.solver.tui.solve.set.gradient_scheme('yes')    # Green-Gauss Node Based
    session.solver.tui.solve.set.gradient_scheme('no','yes') # Least Squares Cell Based
    
Selecting Solution Controls 
~~~~~~~~~~~~~~~~~~~~~~~~~~~
solve/set/p-v-controls TUI: Sets pressure-velocity controls.

.. code:: python

    session.solver.tui.solve.set.p_v_controls(0.3,0.4) # Momentum and Pressure

Creating Report Definition 
~~~~~~~~~~~~~~~~~~~~~~~~~~
solve/report-definitions TUI: Enters the report definitions menu.

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

Initialize and Solve 
~~~~~~~~~~~~~~~~~~~~
solve/initialize TUI: Enters the flow initialization menu.

solve/initialize/hyb-initialization TUI: Initializes using the hybrid
initialization method.

solve/iterate TUI: Performs a specified number of iterations.

.. code:: python

    session.solver.tui.solve.initialize.hyb_initialization()
    session.solver.tui.solve.iterate(100)

Settings Objects
----------------
The following example demonstrates how you can apply solution settings
using the :ref:`ref_settings`:

.. code:: python

    session.solver.root.solution.initialization.hybrid_initialize()
    session.solver.root.solution.run_calculation.iterate(number_of_iterations=150)
