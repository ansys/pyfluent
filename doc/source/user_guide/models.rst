Defining Models
===============
PyFluent supports defining models using :ref:`ref_solver_tui_commands` and :ref:`ref_settings`.

Solver TUI Commands
-------------------
The following example demonstrates how you can define the energy model
using :ref:`ref_solver_tui_commands`:

.. code:: python

    session.solver.tui.define.models.energy("yes", ", ", ", ", ", ", ", ")

Settings Objects
----------------
The following example demonstrates how you can define the energy model
using :ref:`ref_settings`:

.. code:: python

    session.solver.root.setup.models.energy.enabled = True