Models
=======
PyFluent allows you to access Fluent Models using the traditional
TUI Text User Interface command-based infrastructure and the settings
module (Beta).

TUI based infrastructure
-------------------------
Here’s a simple example defining models using the TUI based infrastructure:

.. code:: python

    session.solver.tui.define.models.energy("yes", ", ", ", ", ", ", ", ")

Settings module (Beta)
-------------------------
Here’s a simple example defining models using the settings module:

.. code:: python

    session.solver.root.setup.models.energy.enabled = True

API Reference
--------------
For more details, please see the API Reference section. 