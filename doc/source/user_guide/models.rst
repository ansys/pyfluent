Defining models
===============
PyFluent supports defining models using :ref:`ref_solver_tui_commands` and :ref:`ref_settings`.

Using solver TUI commands
-------------------------
The following examples show how you define models using :ref:`ref_solver_tui_commands`.

Enabling the energy model
~~~~~~~~~~~~~~~~~~~~~~~~~
The ``define.models.energy`` TUI enables and disables the energy model.

.. code:: python

    import ansys.fluent.core as pyfluent
    session = pyfluent.launch_fluent(precision='double', processor_count=2)
    session.solver.tui.file.read_case(case_file_name='file.cas.h5')
    session.solver.tui.define.models.energy('yes', 'no', 'no', 'no', 'yes')

Enabling the viscous model
~~~~~~~~~~~~~~~~~~~~~~~~~~
The ``define.models.viscous.laminar`` TUI enables and disables the laminar flow model.

The ``define.models.viscous.kw_sst`` TUI enables and disables the SST-kw turbulence model.

The ``define.models.viscous.ke_standard`` TUI enables and ddisables the standard-ke
turbulence model.

.. code:: python

    session.solver.tui.define.models.viscous.laminar('yes')
    session.solver.tui.define.models.viscous.kw_sst('yes')
    session.solver.tui.define.models.viscous.ke_standard('yes')

Enabling the radiation model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The ``define.models.radiation`` TUI provides options for selecting different radiation models.

.. code:: python

    session.solver.tui.define.models.radiation.s2s('yes')
    session.solver.tui.define.models.radiation.p1('yes')

Enabling the multiphase model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The ``define.models.multiphase`` TUI provides options for selecting different multiphase models.

.. code:: python

    session.solver.tui.define.models.multiphase.model('vof')
    session.solver.tui.define.models.multiphase.model('eulerian')
    session.solver.tui.define.models.multiphase.model('mixture')
    session.solver.tui.define.models.multiphase.model('wetsteam')

Uing Settings objects
---------------------
The following examples show how you define models using :ref:`ref_settings`.

Enabling the energy model
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    session.solver.root.setup.models.energy.enabled = True

Enabling the viscous model
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    session.solver.root.setup.models.viscous.k_epsilon_model.enabled = True
    session.solver.root.setup.models.viscous.k_omega_model.enabled = True