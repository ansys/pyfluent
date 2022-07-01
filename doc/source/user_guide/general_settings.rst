Applying General Settings
=========================
PyFluent supports defining general settings using the TUI API and
:ref:`ref_settings`.

Solver TUI Commands
-------------------
The following example demonstrates how you can define units using
:ref:`ref_solver_tui_commands`:

.. code:: python

    session.solver.tui.define.units("length", "in")