Applying solution settings
==========================

PyFluent allows you to use :ref:`ref_settings` to interact with solution settings, and initialize and solve.


Steady or transient solution model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

  >>> setup = pyfluent.solver.Setup(solver_session)
  >>> solver_time = setup.general.solver.time
  >>> solver_time()
  'steady'
  >>> solver_time.all()
  ['steady', 'unsteady-1st-order']
  >>> solver_time.set_state("unsteady-1st-order")


Pressure-based or density-based solver
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

  >>> setup = pyfluent.solver.Setup(solver_session)
  >>> solver = setup.general.solver
  >>> solver.type()
  'pressure-based'
  >>> solver.type.all()
  ['pressure-based', 'density-based-implicit', 'density-based-explicit']
  >>> solver.type = "density-based-explicit"
  >>> solver.type()
  'density-based-explicit'


Velocity coupling scheme and gradient options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

  >>> methods = pyfluent.solver.Methods(solver_session)
  >>> flow_scheme = methods.p_v_coupling.flow_scheme
  >>> flow_scheme.all()
  ['SIMPLE', 'SIMPLEC', 'PISO', 'Coupled']
  >>> flow_scheme.set_state("Coupled")
  >>> gradient_scheme = methods.gradient_scheme
  >>> gradient_scheme.all()
  ['green-gauss-node-based', 'green-gauss-cell-based', 'least-square-cell-based']
  >>> gradient_scheme.set_state("green-gauss-node-based")


Solution controls
~~~~~~~~~~~~~~~~~

.. code:: python

  >>> controls = pyfluent.solver.Controls(solver_session)
  >>> p_v_controls = controls.p_v_controls
  >>> explicit_momentum_under_relaxation = p_v_controls.explicit_momentum_under_relaxation
  >>> explicit_momentum_under_relaxation.min()
  0
  >>> explicit_momentum_under_relaxation.max()
  1
  >>> explicit_momentum_under_relaxation.set_state(0.4)
  >>> flow_courant_number = p_v_controls.flow_courant_number
  >>> flow_courant_number.min()
  0
  >>> flow_courant_number.max()
  >>> flow_courant_number.set_state(0.3)


Create a report definition
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

  >>> rep_defs = pyfluent.solver.ReportDefinitions(solver_session)
  >>> outlet_temperature = rep_defs.surface.create(
  ...     name="outlet-temp-avg",
  ...     report_type="surface-massavg",
  ...     field="temperature",
  ... )


Initialize and solve
~~~~~~~~~~~~~~~~~~~~

.. code:: python

  >>> solution = solver_session.settings.solution
  >>> solution.initialization.hybrid_initialize()
  >>> solution.run_calculation.iterate(iter_count=100)
