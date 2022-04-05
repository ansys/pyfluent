PyFluent
========
|GH-CI| |MIT|

.. |GH-CI| image:: https://github.com/pyansys/pyfluent/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/pyansys/pyfluent/actions/workflows/ci.yml

.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT

Overview
--------
The PyFluent project provides Pythonic access to Ansys Fluent.  The package
provides features to enable seamless use of Fluent within the Python ecosystem
as well as broad access to Fluent features including:

- Ability to launch Fluent using a local Ansys installation
- Ability to use Fluent TUI commands for both meshing and solver features
- Ability to use Fluent's in-built post processing capabilities

Documentation and Issues
------------------------
See the `Development Documentation <https://dev.fluentdocs.pyansys.com>`_ page
for more details.

Please feel free to post issues and other questions at `PyFluent Issues
<https://github.com/pyansys/pyfluent/issues>`_.  This is the best place
to post questions and code.

Installation
------------
The ``ansys-fluent-core`` package currently supports Python 3.7 through Python
3.10 on Windows and Linux.

If you want to use PyFluent please install the latest from `PyFluent GitHub
<https://github.com/pyansys/pyfluent/issues>`_ via:

.. code:: console

   pip install git+https://github.com/pyansys/pyfluent.git

If you plan on doing local "development" of PyFluent with Git, then install
with:

.. code:: console

  git clone https://github.com/pyansys/pyfluent.git
  cd pyfluent
  pip install -e .

Dependencies
------------
You will need a locally installed licenced copy of ANSYS to run Fluent, with the
first supported version being Ansys 2022 R2.

Getting Started
---------------

Launching Fluent
~~~~~~~~~~~~~~~~
You can launch Fluent from Python using the ``launch_fluent`` function:

.. code:: python

  import ansys.fluent.core as pyfluent
  pyfluent.set_log_level('DEBUG') # for development, by default only errors are shown
  session = pyfluent.launch_fluent()
  session.check_health()
  session.start_transcript() # enable transcript streaming

To use a non-default install location set the ``PYFLUENT_FLUENT_ROOT``
environment variable to the ``<version>/fluent`` directory where ``<version>``
is the Ansys release version you would like to use (eg: v222).

Basic Usage
~~~~~~~~~~~
You can run Fluent TUI commands using the ``session.tui`` interface:

.. code:: python

  session.tui.solver.file.read_case(case_file_name='elbow.cas.gz')
  session.tui.solver.define.models.unsteady_2nd_order("yes")
  session.tui.solver.solve.initialize.initialize_flow()
  session.tui.solver.solve.dual_time_iterate(2, 3)

In addition to all TUI commands being available there are the ``parametric`` and
``post`` packages.  The ``parametric`` package provides access to Fluent's
design point capability and the ``post`` package provides integrations with both
``pyvista`` and ``matplotlib``.

License and Acknowledgments
---------------------------
``PyFluent`` is licensed under the MIT license.

This module, ``ansys-fluent`` makes no commercial claim over Ansys whatsoever.
This tool extends the functionality of ``Fluent`` by adding a Python interface
to the Fluent without changing the core behavior or license of the original
software.  The use of the interactive Fluent control of ``PyFluent`` requires a
legally licensed local copy of Ansys.

To get a copy of Ansys, please visit `Ansys <https://www.ansys.com/>`_.