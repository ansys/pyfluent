PyFluent
========
|pyansys| |pypi| |GH-CI| |MIT| |black|

.. |pyansys| image:: https://img.shields.io/badge/Py-Ansys-ffc107.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC
   :target: https://docs.pyansys.com/
   :alt: PyAnsys

.. |pypi| image:: https://img.shields.io/pypi/v/ansys-fluent-core.svg?logo=python&logoColor=white
   :target: https://pypi.org/project/ansys-fluent-core
   :alt: PyPI

.. |GH-CI| image:: https://github.com/pyansys/pyfluent/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/pyansys/pyfluent/actions/workflows/ci.yml
   :alt: GH-CI

.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: MIT

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat
   :target: https://github.com/psf/black
   :alt: Black

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
Please see the latest release `documentation <https://fluentdocs.pyansys.com>`_
page for more details.

Please feel free to post issues and other questions at `PyFluent Issues
<https://github.com/pyansys/pyfluent/issues>`_.  This is the best place
to post questions and code.

Installation
------------
The ``ansys-fluent-core`` package currently supports Python 3.7 through Python
3.10 on Windows and Linux.

Install the latest release from `PyPI
<https://pypi.org/project/ansys-fluent-core/>`_ with:

.. code:: console

   pip install ansys-fluent-core

Alternatively, install the latest from `PyFluent GitHub
<https://github.com/pyansys/pyfluent>`_ via:

.. code:: console

   pip install git+https://github.com/pyansys/pyfluent.git

If you plan on doing local "development" of PyFluent with Git, then install
with:

.. code:: console

   git clone https://github.com/pyansys/pyfluent.git
   cd pyfluent
   pip install pip -U
   pip install -e .
   python codegen/allapigen.py  # Generates the API files, requires Fluent

Dependencies
------------
You will need a locally installed licensed copy of ANSYS to run Fluent, with the
first supported version being Ansys 2022 R2.

Getting Started
---------------

Launching Fluent
~~~~~~~~~~~~~~~~
You can launch Fluent from Python using the ``launch_fluent`` function:

.. code:: python

  import ansys.fluent.core as pyfluent
  session = pyfluent.launch_fluent()
  session.check_health()

To use a non-default install location set the ``PYFLUENT_FLUENT_ROOT``
environment variable to the ``<version>/fluent`` directory where ``<version>``
is the Ansys release version you would like to use (eg: v222).

Basic Usage
~~~~~~~~~~~
You can run Fluent TUI commands using the ``session.tui`` interface:

.. code:: python

  session.solver.tui.file.read_case(case_file_name='elbow.cas.h5')
  session.solver.tui.define.models.unsteady_2nd_order("yes")
  session.solver.tui.solve.initialize.initialize_flow()
  session.solver.tui.solve.dual_time_iterate(2, 3)

In addition to all TUI commands being available there are the
`PyFluent Parametric <https://fluentparametric.docs.pyansys.com/>`_ and
`PyFluent Visualization <https://fluentvisualization.docs.pyansys.com/>`_ packages.
The PyFluent Parametric package provides access to Fluent's parametric workflows and
the PyFluent Visualization package provides post-processing and visualization
capabilities using `pyvista <https://docs.pyvista.org/>`_ and
`matplotlib <https://matplotlib.org/>`_.

License and Acknowledgments
---------------------------
``PyFluent`` is licensed under the MIT license.

This module, ``ansys-fluent`` makes no commercial claim over Ansys whatsoever.
This tool extends the functionality of ``Fluent`` by adding a Python interface
to the Fluent without changing the core behavior or license of the original
software.  The use of the interactive Fluent control of ``PyFluent`` requires a
legally licensed local copy of Ansys.

To get a copy of Ansys, please visit `Ansys <https://www.ansys.com/>`_.
