.. _ref_user_guide_solver_settings:


Specifying Solver Settings
==========================

Text User Interface (TUI) API
-----------------------------
The following example demonstrates how you can define some solver
settings using the TUI API:

Selecting Steady or Transient
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    import ansys.fluent.core as pyfluent
    session = pyfluent.launch_fluent(precision="double", processor_count=2)
    session.solver.tui.file.read_case(case_file_name='file.cas.h5')
    session.solver.tui.define.models.steady('yes')
    session.solver.tui.define.models.unsteady_1st_order('yes')

Selecting Pressure Based or Density Based Solver
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    session.solver.tui.define.models.solver.density_based_explicit('yes')
    session.solver.tui.define.models.solver.density_based_implicit('yes')
    session.solver.tui.define.models.solver.pressure_based('yes')

Defining Gravitational Acceleration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    session.solver.tui.define.operating_conditions.gravity('yes','0','-9.81','0')
