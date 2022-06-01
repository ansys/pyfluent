Applying General Settings
=========================
PyFluent allows you to access Fluent General Settings options using 
the traditional Text User Interface (TUI) command-based infrastructure.

Text User Interface (TUI) API
-----------------------------
The following example demonstrates how you can define units using
the TUI API:

.. code:: python

    session.solver.tui.define.units("length", "in")