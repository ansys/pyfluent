Applying General Settings
=========================
PyFluent supports defining general settings using the TUI API and
the Settings API (Beta).

Text User Interface (TUI) API
-----------------------------
The following example demonstrates how you can define units using
the TUI API:

.. code:: python

    session.solver.tui.define.units("length", "in")