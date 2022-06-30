Applying Solution Settings
==========================

Text User Interface (TUI) API
-----------------------------
The following example demonstrates how you can apply some solution 
settings using the TUI API:

Selecting Solution Methods 
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    import ansys.fluent.core as pyfluent
    session = pyfluent.launch_fluent(precision="double", processor_count=2)
    session.solver.tui.file.read_case(case_file_name='file.cas.h5')
    session.solver.tui.solve.set.p_v_coupling(20) # Coupled
    session.solver.tui.solve.set.gradient_scheme('yes')    # Green-Gauss Node Based
    session.solver.tui.solve.set.gradient_scheme('no','yes') # Least Squares Cell Based
    
Selecting Solution Controls 
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    session.solver.tui.solve.set.p_v_controls(0.3,0.4) # Momentum and Pressure

Creating Report Definition 
~~~~~~~~~~~~~~~~~~~~~~~~~~

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
