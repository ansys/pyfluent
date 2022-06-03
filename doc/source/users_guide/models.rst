Defining Your Models
====================
PyFluent supports defining models using the TUI API and the 
Settings API (Beta).

Text User Interface (TUI) API
-----------------------------
The following example demonstrates how you can define the energy model
using the TUI API:

.. code:: python

    session.solver.tui.define.models.energy("yes", ", ", ", ", ", ", ", ")

Settings API (Beta)
----------------------
The following example demonstrates how you can define the energy model
using the settings module (Beta):

.. code:: python

    session.solver.root.setup.models.energy.enabled = True