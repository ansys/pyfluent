.. _ref_user_guide_solver_settings:

Specifying Solver Settings
==========================
PyFluent supports specifying solver settings using  both 
:ref:`ref_solver_tui_commands` and :ref:`ref_settings`.

Solver TUI Commands
-------------------
The following example demonstrates how you can specify solver
settings using the :ref:`ref_solver_tui_commands`:

.. code:: python

    session.solver.tui.define.models.unsteady_2nd_order('yes’)​