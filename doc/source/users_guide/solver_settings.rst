Specifying Solver Settings
==========================
PyFluent supports specifying solver settings using the TUI API and the
Settings Module (Beta).

Text User Interface (TUI) API
-----------------------------
The following example demonstrates how you can specify solver
settings using the TUI API:

.. code:: python

    session.solver.tui.define.models.unsteady_2nd_order('yes’)​