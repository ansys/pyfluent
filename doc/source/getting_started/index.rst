.. _getting_started:

===============
Getting Started
===============
To run PyFluent, you must have a local licenced copy of Ansys Fluent. 
PyFluent supports Ansys Fluent versions 2022 R2 or newer.

Visit `Ansys <https://www.ansys.com/>`_ for more information on
getting a licensed copy of Ansys Fluent.

************
Installation
************

Python Module
~~~~~~~~~~~~~
The ``ansys-fluent-core`` package currently supports Python 3.7 through
Python 3.10 on Windows and Linux.

Install the latest release from `PyPi
<https://pypi.org/project/ansys-fluent-core/>`_ with:

.. code::

   pip install ansys-fluent-core

Alternatively, install the latest from `PyFluent GitHub
<https://github.com/pyansys/pyfluent/issues>`_ via:

.. code::

   pip install git+https://github.com/pyansys/pyfluent.git


For a local "development" version, install with:

.. code::

   git clone https://github.com/pyansys/pyfluent.git
   cd pyfluent
   pip install -e .

(Remove this section when PyFluent project goes public) 
Until PyFluent project goes public, install the latest release from
the artifactory.

.. code::

   python -m pip install --extra-index-url http://conanreader:conanreader@canartifactory.ansys.com:8080/artifactory/api/pypi/pypi/simple --trusted-host canartifactory.ansys.com ansys-fluent-solver

This will allow you to install the PyFluent ``ansys-fluent-core`` module
and modify it locally and have the changes reflected in your setup
after restarting the Python kernel.

****************
Launching Fluent
****************

You can launch Fluent from Python using the ``launch_fluent`` function:

.. code:: python

  import ansys.fluent.core as pyfluent
  session = pyfluent.launch_fluent(precision="double", processor_count=2)
  session.check_health()
  session.start_transcript() # Streaming the transcript locally

Fluent is now active and you can send commands to it as a genuine Python class.
For example, if we wanted to read a case file, update a setting and iterate the
solver:

.. code:: python

  session.solver.tui.file.read_case(case_file_name='elbow.cas.h5')
  session.solver.tui.define.models.unsteady_2nd_order("yes")
  session.solver.tui.solve.initialize.initialize_flow()
  session.solver.tui.solve.dual_time_iterate(2, 3)

In addition to all TUI commands being available there are the ``parametric`` and
``post`` packages.  The ``parametric`` package provides access to Fluent's
design point capability and the ``post`` package provides integrations with both
``pyvista`` and ``matplotlib``.

If you want to interact with the Fluent graphical user interface, set the
following environment variable:

.. code::

  set PYFLUENT_SHOW_SERVER_GUI=1    # Windows
  export PYFLUENT_SHOW_SERVER_GUI=1 # Linux (bash)

If you want to print the debug information for development, set the following
environment variable:

.. code:: python

  pyfluent.set_log_level('DEBUG') # for development, by default only errors are shown