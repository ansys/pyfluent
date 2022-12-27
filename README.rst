PyFluent
========
|pyansys| |pypi| |GH-CI| |codecov| |MIT| |black|

.. |pyansys| image:: https://img.shields.io/badge/Py-Ansys-ffc107.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC
   :target: https://docs.pyansys.com/
   :alt: PyAnsys

.. |pypi| image:: https://img.shields.io/pypi/v/ansys-fluent-core.svg?logo=python&logoColor=white
   :target: https://pypi.org/project/ansys-fluent-core
   :alt: PyPI

.. |GH-CI| image:: https://github.com/pyansys/pyfluent/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/pyansys/pyfluent/actions/workflows/ci.yml
   :alt: GH-CI

.. |codecov| image:: https://codecov.io/gh/pyansys/pymapdl/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/pyansys/pymapdl

.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: MIT

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat
   :target: https://github.com/psf/black
   :alt: Black

Overview
--------
PyFluent provides Pythonic access to Ansys Fluent. Its features enable the seamless use of
Fluent within the Python ecosystem and broad access to native Fluent features, including the
ability to:

- Launch Fluent using a local Ansys installation
- Use Fluent's TUI (text user interface) commands for both meshing and solver features
- Use Fluent's built-in postprocessing capabilities

Documentation and issues
------------------------
For comprehesive information on PyFluent, see the latest release
`documentation <https://fluent.docs.pyansys.com>`_.

On the `PyFluent Issues <https://github.com/pyansys/pyfluent/issues>`_ page, you can create
issues to submit questions, report bugs, and request new features. To reach
the PyAnsys support team, email `pyansys.support@ansys.com <pyansys.support@ansys.com>`_.

Installation
------------
The ``ansys-fluent-core`` package supports Python 3.7 through Python
3.10 on Windows and Linux.

Install the latest release from `PyPI
<https://pypi.org/project/ansys-fluent-core/>`_ with:

.. code:: console

   pip install ansys-fluent-core

If you plan on doing local *development* of PyFluent with Git, install
the latest release with:

.. code:: console

   git clone https://github.com/pyansys/pyfluent.git
   cd pyfluent
   pip install pip -U
   pip install -e .
   python codegen/allapigen.py  # Generates the API files

Dependencies
------------
You must have a licensed copy of Ansys Fluent installed locally. PyFluent
supports Fluent 2022 R2 and later.

Getting started
---------------

Launching Fluent
~~~~~~~~~~~~~~~~
To launch Fluent from Python, use the ``launch_fluent`` method:

.. code:: python

  import ansys.fluent.core as pyfluent
  solver_session = pyfluent.launch_fluent(mode="solver")
  solver_session.health_check_service.is_serving

On Windows systems the environment variable ``AWP_ROOT<ver>``, is configured
when Fluent is installed, where ``<ver>`` is the Fluent release number such as
``232`` for release 2022 R2.  PyFluent automatically uses this environment
variable to locate the Fluent installation. On Linux systems configure
``AWP_ROOT<ver>`` to point to the absolute path of an Ansys installation such as
``/apps/ansys_inc/v232``.

To use a non-default installation location set ``AWP_ROOT<ver>`` or set the
``PYFLUENT_FLUENT_ROOT`` environment variable to the ``<install
location>/<version>/fluent`` directory, where ``<version>`` is the Fluent
release that you would like to use. For example, ``v232`` uses release 2022 R2.

Basic Usage
~~~~~~~~~~~
You can use the ``solver_session.tui`` interface to run all Fluent TUI commands:

.. code:: python

  solver_session.tui.file.read_case('elbow.cas.h5')
  solver_session.tui.define.models.unsteady_2nd_order("yes")
  solver_session.tui.solve.initialize.initialize_flow()
  solver_session.tui.solve.dual_time_iterate(2, 3)

You can also install and use these PyFluent libraries:

- `PyFluent Parametric <https://fluentparametric.docs.pyansys.com/>`_, which provides
  access to Fluent's parametric workflows.
- `PyFluent Visualization <https://fluentvisualization.docs.pyansys.com/>`_, which
  provides postprocessing and visualization capabilities using the `pyvista <https://docs.pyvista.org/>`_
  and `matplotlib <https://matplotlib.org/>`_ packages.

License and acknowledgments
---------------------------
PyFluent is licensed under the MIT license.

PyFluent makes no commercial claim over Ansys whatsoever. This library
extends the functionality of Ansys Fluent by adding a Python interface
to Fluent without changing the core behavior or license of the original
software. The use of the interactive Fluent control of PyFluent requires a
legally licensed local copy of Fluent.

For more information on Fluent, see the `Ansys Fluent <https://www.ansys.com/products/fluids/ansys-fluent>`_
page on the Ansys website.
