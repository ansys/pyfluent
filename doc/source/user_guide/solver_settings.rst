.. _ref_user_guide_solver_settings:

Specifying solver settings
==========================
PyFluent supports specifying solver settings using 
:ref:`ref_solver_tui_commands` and :ref:`ref_settings`.

The following examples show how you specify solver
settings using :ref:`ref_solver_tui_commands`:

Selecting steady or transient
-----------------------------
The ``define.models.steady`` TUI enables and disables the steady solution model.

The ``define.models.unsteady.1st_order TUI`` selects the first-order implicit
formulation for a transient simulation.

.. code:: python

    import ansys.fluent.core as pyfluent
    session = pyfluent.launch_fluent(precision='double', processor_count=2)
    session.solver.tui.file.read_case(case_file_name='file.cas.h5')
    session.solver.tui.define.models.steady('yes')
    session.solver.tui.define.models.unsteady_1st_order('yes')

Selecting pressure-based or density-based solver
------------------------------------------------
The ``define.models.solver.density_based_explicit`` TUI enables and disables the
density-based explicit solver.

The ``define.models.solver.density_based-implicit`` TUI enables and disables the
density-based implicit solver.

The ``define.models.solver.pressure_based`` TUI enables and disables the
pressure-based solver.

.. code:: python

    session.solver.tui.define.models.solver.density_based_explicit('yes')
    session.solver.tui.define.models.solver.density_based_implicit('yes')
    session.solver.tui.define.models.solver.pressure_based('yes')

Defining gravitational acceleration
-----------------------------------
The ``define.operating_conditions.gravity`` TUI sets the gravitational acceleration.

.. code:: python

    session.solver.tui.define.operating_conditions.gravity('yes','0','-9.81','0')
