Specifying Solver Settings
==========================
PyFluent allows you to access Fluent Solver Settings options.

Text User Interface (TUI) API
-----------------------------
The following example demonstrates how you can specify solver
settings using the TUI API:

.. code:: python

    session.solver.tui.define.models.unsteady_2nd_order('yes’)​