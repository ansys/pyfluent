Defining Models
===============
PyFluent supports defining models using the TUI API and :ref:`ref_settings`.

Text User Interface (TUI) API
-----------------------------
The following example demonstrates how you can define the energy model
using the TUI API:

.. code:: python

    session.solver.tui.define.models.energy("yes", ", ", ", ", ", ", ", ")

Settings Objects
----------------
The following example demonstrates how you can define the energy model
using :ref:`ref_settings`:

.. code:: python

    session.solver.root.setup.models.energy.enabled = True