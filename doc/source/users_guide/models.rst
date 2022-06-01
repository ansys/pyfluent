Defining Your Models
====================
PyFluent allows you to access Fluent Models using the traditional
TUI Text User Interface command-based infrastructure and the settings
module (Beta).

Text User Interface (TUI) API
-----------------------------
The following example demonstrates how you can define the energy model
using the TUI API:

.. code:: python

    session.solver.tui.define.models.energy("yes", ", ", ", ", ", ", ", ")

Settings Module (Beta)
----------------------
The following example demonstrates how you can define the energy model
using the settings module (Beta):

.. code:: python

    session.solver.root.setup.models.energy.enabled = True