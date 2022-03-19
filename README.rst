Overview
========
Fluent's Solver and Meshing capabilities exposed in Python

Installation
------------
For a local "development" version, install with:

.. code:: console

  git clone https://github.com/pyansys/pyfluent.git
  cd pyfluent
  pip install -e .

Usage
-----
1) Normally Fluent should be installed from the latest daily build but to use a
   non-default install location set the PYFLUENT_FLUENT_ROOT environment
   variable to the ``<version>/fluent`` directory where ``<version>`` is the
   Ansys release version you would like to use (eg: v222).
2) Within a Python 3 console, execute:

.. code:: python

  import ansys.fluent.core as pyfluent
  pyfluent.set_log_level('DEBUG') # for development, by default only errors are shown
  session = pyfluent.launch_fluent()
  session.check_health()
  session.start_transcript() # enable transcript streaming
  session.tui.solver.file.read_case(case_file_name='elbow.cas.gz')
  session.tui.solver.define.models.unsteady_2nd_order("yes")
  session.tui.solver.solve.initialize.initialize_flow()
  session.tui.solver.solve.dual_time_iterate(2, 3)

Documentation and Issues
------------------------
See the `Development Documentation <https://dev.fluentdocs.pyansys.com>`_ page
for more details.

Please feel free to post issues and other questions at `PyFluent Issues
<https://github.com/pyansys/pyfluent/issues>`_.  This is the best place
to post questions and code.