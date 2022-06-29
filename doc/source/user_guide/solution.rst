Applying Solution Settings
==========================

PyFluent allows you to apply solution settings, initialize and solve using both 
:ref:`ref_solver_tui_commands` and :ref:`ref_settings`.

Solver TUI Commands
-------------------
The following example demonstrates how you can apply solution settings
using :ref:`ref_solver_tui_commands`:

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