.. _getting_started:

===============
Getting Started
===============
To use PyFluent, you will need a locally installed licenced copy of ANSYS to run
Fluent, with the first supported version being Ansys 2022 R2.

Visit `Ansys <https://www.ansys.com/>`_ for more information on
getting a licensed copy of Ansys.

************
Installation
************
The ``ansys-fluent-core`` package currently supports Python 3.7 through Python
3.10 on Windows and Linux.

If you want to use PyFluent please install the latest release package from
`PyFluent GitHub <https://github.com/pyansys/pyfluent/issues>`_ via:

.. code:: console

   pip install git+https://github.com/pyansys/pyfluent.git

****************
Launching Fluent
****************

You can launch Fluent from Python using the ``launch_fluent`` function:

.. code:: python

  import ansys.fluent.core as pyfluent
  pyfluent.set_log_level('DEBUG') # for development, by default only errors are shown
  session = pyfluent.launch_fluent()
  session.check_health()
  session.start_transcript() # Streaming the transcript locally

Fluent is now active and you can send commands to it as a genuine Python class.
For example, if we wanted to read a case file, update a setting and iterate the
solver:

.. code:: python

  session.tui.solver.file.read_case(case_file_name='elbow.cas.h5')
  session.tui.solver.define.models.unsteady_2nd_order("yes")
  session.tui.solver.solve.initialize.initialize_flow()
  session.tui.solver.solve.dual_time_iterate(2, 3)

In addition to all TUI commands being available there are the ``parametric`` and
``post`` packages.  The ``parametric`` package provides access to Fluent's
design point capability and the ``post`` package provides integrations with both
``pyvista`` and ``matplotlib``.

If you want to interact with the Fluent graphical user interface, set the
following environment variable:

.. code::

		    set PYFLUENT_SHOW_SERVER_GUI=1    # Windows
        export PYFLUENT_SHOW_SERVER_GUI=1 # Linux (bash)

