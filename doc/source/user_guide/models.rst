Defining Models
===============

Text User Interface (TUI) API
-----------------------------
The following example demonstrates how you can define some models settings
using the TUI API:

Enabling Energy Model
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    import ansys.fluent.core as pyfluent
    session = pyfluent.launch_fluent(precision="double", processor_count=2)
    session.solver.tui.file.read_case(case_file_name='file.cas.h5')
    session.solver.tui.define.models.energy("yes", "no", "no", "no", "yes")

Enabling Viscous Model
~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    session.solver.tui.define.models.viscous.laminar('yes')
    session.solver.tui.define.models.viscous.kw_sst('yes')
    session.solver.tui.define.models.viscous.ke_standard('yes')

Enabling Radiation Model
~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    session.solver.tui.define.models.radiation.s2s('yes')
    session.solver.tui.define.models.radiation.p1('yes')

Enabling Multiphase Model
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    session.solver.tui.define.models.multiphase.model('vof')
    session.solver.tui.define.models.multiphase.model('eulerian')
    session.solver.tui.define.models.multiphase.model('mixture')
    session.solver.tui.define.models.multiphase.model('wetsteam')

Settings API (Beta)
-----------------------------
The following example demonstrates how you can define some models settings using
:ref:`ref_settings`:

Enabling Energy Model
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    session.solver.root.setup.models.energy.enabled = True

Enabling Viscous Model
~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    session.solver.root.setup.models.viscous.k_epsilon_model.enabled = True
    session.solver.root.setup.models.viscous.k_omega_model.enabled = True