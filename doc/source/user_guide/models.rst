Defining models
===============
PyFluent supports defining models using :ref:`ref_solver_tui_commands` and :ref:`ref_settings`.

Using solver TUI commands
-------------------------
The following examples show how you define models using :ref:`ref_solver_tui_commands`.

Enabling the energy model
~~~~~~~~~~~~~~~~~~~~~~~~~
The following example shows a comparison between the TUI command and the
Python code for enabling and disabling the energy model.

**TUI command**

.. code:: scheme

    /define/models/energy yes no no no yes

**Python code**

.. code:: python

    import ansys.fluent.core as pyfluent
    session = pyfluent.launch_fluent(precision='double', processor_count=2)
    session.solver.tui.file.read_case(case_file_name='file.cas.h5')
    session.solver.tui.define.models.energy('yes', 'no', 'no', 'no', 'yes')

Enabling the viscous model
~~~~~~~~~~~~~~~~~~~~~~~~~~
The following example shows a comparison between the TUI command and the
Python code for enabling and disabling the various viscous models.

**TUI command**

.. code:: scheme

    /define/models/viscous/laminar yes
    /define/models/viscous/kw-sst yes
    /define/models/viscous/ke-standard yes

**Python code**

.. code:: python

    session.solver.tui.define.models.viscous.laminar('yes')
    session.solver.tui.define.models.viscous.kw_sst('yes')
    session.solver.tui.define.models.viscous.ke_standard('yes')

Enabling the radiation model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The following example shows a comparison between the TUI command and the
Python code for selecting different radiation models.

**TUI command**

.. code:: scheme

    /define/models/radiation/s2s yes
    /define/models/radiation/p1 yes

**Python code**

.. code:: python

    session.solver.tui.define.models.radiation.s2s('yes')
    session.solver.tui.define.models.radiation.p1('yes')

Enabling the multiphase model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The following example shows a comparison between the TUI command and the
Python code for selecting different multiphase models.

**TUI command**

.. code:: scheme

    /define/models/multiphase/model vof
    /define/models/multiphase/model eulerian
    /define/models/multiphase/model mixture
    /define/models/multiphase/model wetsteam

**Python code**

.. code:: python

    session.solver.tui.define.models.multiphase.model('vof')
    session.solver.tui.define.models.multiphase.model('eulerian')
    session.solver.tui.define.models.multiphase.model('mixture')
    session.solver.tui.define.models.multiphase.model('wetsteam')

Using settings objects
----------------------
The following examples show how you define models using :ref:`ref_settings`.

Enabling the energy model
~~~~~~~~~~~~~~~~~~~~~~~~~

**Python code**

.. code:: python

    session.solver.root.setup.models.energy.enabled = True

Enabling the viscous model
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Python code**

.. code:: python

    session.solver.root.setup.models.viscous.k_epsilon_model.enabled = True
    session.solver.root.setup.models.viscous.k_omega_model.enabled = True