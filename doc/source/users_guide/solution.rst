Applying Solution Settings
==========================
PyFluent supports applying solution settings using the TUI API and the
Settings API (Beta).

PyFluent allows you to initialize and solve using the traditional
Text User Interface (TUI) command-based infrastructure and the settings
module (Beta).

Text User Interface (TUI) API
-----------------------------
The following example demonstrates how you can apply solution settings
using the TUI API:

.. code:: python

    session.solver.tui.solve.initialize.hyb_initialization()
    session.solver.tui.solve.iterate(100)

Settings Module (Beta)
----------------------
The following example demonstrates how you can apply solution settings
using the settings module (Beta):

.. code:: python

    session.solver.root.solution.initialization.hybrid_initialize()
    session.solver.root.solution.run_calculation.iterate(number_of_iterations=150)