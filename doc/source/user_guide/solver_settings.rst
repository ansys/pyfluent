.. _ref_user_guide_solver_settings:

Specifying solver settings
==========================
PyFluent supports using :ref:`ref_solver_tui_commands` and :ref:`ref_settings`
to specify solver settings.

The examples in this topic show how you use :ref:`ref_solver_tui_commands` to
specify solver settings.

Set steady or transient solution model
--------------------------------------
This example shows a comparison between the TUI commands and the
Python code for enabling and disabling the steady and unsteady (transient)
solution model.

**TUI command**

.. code:: scheme

    /define/models/steady yes
    /define/models/unsteady_1st_order yes

**Python code**

.. code:: python

    import ansys.fluent.core as pyfluent
    solver = pyfluent.launch_fluent(precision='double', processor_count=2, mode="solver")
    solver.tui.file.read_case('file.cas.h5')
    solver.tui.define.models.steady('yes')
    solver.tui.define.models.unsteady_1st_order('yes')

Set a pressure-based or density-based solver
--------------------------------------------
This example shows a comparison between the TUI commands and the
Python code for enabling and disabling the pressure-based and
density-based solver models.

**TUI command**

.. code:: scheme

    /define/models/solver/density-based-explicit yes 
    /define/models/solver/density-based-implicit yes
    /define/models/solver/pressure-based yes

**Python code**

.. code:: python

    solver.tui.define.models.solver.density_based_explicit('yes')
    solver.tui.define.models.solver.density_based_implicit('yes')
    solver.tui.define.models.solver.pressure_based('yes')

Set gravitational acceleration
------------------------------
This example shows a comparison between the TUI command and the
Python code for setting the gravitational acceleration.

**TUI command**

.. code:: scheme

    /define/operating-conditions/gravity yes 0 -9.81 0

**Python code**

.. code:: python

    solver.tui.define.operating_conditions.gravity('yes','0','-9.81','0')

Sample use of explicit attribute access methods
-----------------------------------------------
This simple example shows how you use the explicit attribute access methods
in a simple solver session.

**Python code**

.. code:: python

    import ansys.fluent.core as pyfluent
    from ansys.fluent.core import examples

    import_filename = examples.download_file("mixing_elbow.msh.h5", "pyfluent/mixing_elbow")
    solver = pyfluent.launch_fluent(mode="solver")

    solver.setup.models.viscous.is_active()
    solver.setup.models.viscous.model.is_read_only()
    solver.setup.models.viscous.model.default_value()
    solver.setup.models.viscous.model.allowed_values()
    solver.setup.models.discrete_phase.tracking.tracking_parameters.max_number_of_steps.min()
    solver.setup.models.discrete_phase.tracking.tracking_parameters.max_number_of_steps.max()
