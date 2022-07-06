.. _ref_user_guide_solver_settings:

Specifying Solver Settings
==========================
PyFluent supports specifying solver settings using  both 
:ref:`ref_solver_tui_commands` and :ref:`ref_settings`.

Solver TUI Commands
-------------------
The following examples demonstrate how you can specify solver
settings using the :ref:`ref_solver_tui_commands`:

Selecting Steady or Transient
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
define/models/steady TUI: Enables/disables the steady solution model.

define/models/unsteady-1st-order TUI: Selects the first-order implicit
formulation for transient simulations.

.. code:: python

    import ansys.fluent.core as pyfluent
    session = pyfluent.launch_fluent(precision='double', processor_count=2)
    session.solver.tui.file.read_case(case_file_name='file.cas.h5')
    session.solver.tui.define.models.steady('yes')
    session.solver.tui.define.models.unsteady_1st_order('yes')

Selecting Pressure Based or Density Based Solver
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
define/models/solver/density-based-explicit TUI: Enables/disables the
density-based-explicit solver.

define/models/solver/density-based-implicit TUI: Enables/disables the
density-based-implicit solver.

define/models/solver/pressure-based TUI: Enables/disables the
pressure-based solver.

.. code:: python

    session.solver.tui.define.models.solver.density_based_explicit('yes')
    session.solver.tui.define.models.solver.density_based_implicit('yes')
    session.solver.tui.define.models.solver.pressure_based('yes')

Defining Gravitational Acceleration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
define/operating-conditions/gravity TUI: Sets gravitational acceleration.

.. code:: python

    session.solver.tui.define.operating_conditions.gravity('yes','0','-9.81','0')
