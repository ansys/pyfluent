.. _getting_started:

===============
Getting started
===============
PyFluent provides Pythonic access to Ansys Fluent. 

To run PyFluent, you must have a licensed copy of Ansys Fluent
installed locally. PyFluent supports Fluent 2022 R2 and later.

For more information on Fluent, see the `Ansys Fluent page <https://www.ansys.com/products/fluids/ansys-fluent>`_ 
on the Ansys website.

Install the package
-------------------
The ``ansys-fluent-core`` package supports Python 3.7 through
Python 3.10 on Windows and Linux.

Install the latest release from `PyPi
<https://pypi.org/project/ansys-fluent-core/>`_ with:

.. code::

   pip install ansys-fluent-core

If you plan on doing local *development* of PyFluent with Git, install
the latest release with:

.. code:: console

   git clone https://github.com/pyansys/pyfluent.git
   cd pyfluent
   pip install pip -U
   pip install -e .
   python codegen/allapigen.py  # Generates the API files


Any changes that you make locally are reflected in your setup after you restart
the Python kernel.

Launch Fluent
-------------
To launch Fluent from PyFluent, use the ``launch_fluent`` method:

.. code:: python

  import ansys.fluent.core as pyfluent
  solver_session = pyfluent.launch_fluent(precision="double", processor_count=2, mode="solver")
  solver_session.check_health()

On Windows systems the environment variable ``AWP_ROOT<ver>``, is configured
when Fluent is installed, where ``<ver>`` is the Fluent release number such as
``222`` for release 2022 R2.  PyFluent automatically uses this environment
variable to locate the Fluent installation. On Linux systems configure
``AWP_ROOT<ver>`` to point to the absolute path of an Ansys installation such as
``/apps/ansys_inc/v222``.  

To use a non-default installation location set ``AWP_ROOT<ver>`` or set the
``PYFLUENT_FLUENT_ROOT`` environment variable to the ``<install
location>/<version>/fluent`` directory, where ``<version>`` is the Fluent
release that you would like to use. For example, ``v222`` uses release 2022 R2.
Once Fluent is active, you can use the ``solver_session.tui`` interface to send
Fluent TUI commands to Fluent. For example, you can read a case file, update a
setting, and iterate the solver with:

.. code:: python

  solver_session.tui.file.read_case('elbow.cas.h5')
  solver_session.tui.define.models.unsteady_2nd_order("yes")
  solver_session.tui.solve.initialize.initialize_flow()
  solver_session.tui.solve.dual_time_iterate(2, 3)

If you want to interact with the Fluent graphical user interface, pass ``show_gui=True``
to the ``launch_fluent`` function:

.. code:: python

  session = pyfluent.launch_fluent(precision="double", processor_count=2, show_gui=True, mode="solver")

If you want to print the debug information for development, set the following
environment variable:

.. code:: python

  pyfluent.set_log_level('DEBUG') # for development, by default only errors are shown


Additional PyFluent libraries
-----------------------------
You can also install and use these additional PyFluent libraries:

- `PyFluent Parametric <https://fluentparametric.docs.pyansys.com/>`_, which provides
  access to Fluent's parametric workflows.
- `PyFluent Visualization <https://fluentvisualization.docs.pyansys.com/>`_, which
  provides postprocessing and visualization capabilities using the `pyvista <https://docs.pyvista.org/>`_
  and `matplotlib <https://matplotlib.org/>`_ packages.
