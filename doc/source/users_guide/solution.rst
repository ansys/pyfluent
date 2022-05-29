Solution
=========
PyFluent allows you to initialize and solve using the traditional
Text User Interface (TUI) command-based infrastructure and the settings
module (Beta).

TUI based infrastructure
-------------------------
Here’s a simple example of initialization using the TUI based infrastructure:

.. code:: python

    session.solver.tui.solve.initialize.hyb_initialization()
    session.solver.tui.solve.iterate(100)

Settings module (Beta)
-------------------------
Here’s a simple example of initialization using the settings module:

.. code:: python

    session.solver.root.solution.initialization.hybrid_initialize()
    session.solver.root.solution.run_calculation.iterate(number_of_iterations=150)

API Reference
--------------
For more details, please see the API Reference section. 