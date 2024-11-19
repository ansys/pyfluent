PyFluent
========
|pyansys| |python| |pypi| |GH-CI| |codecov| |MIT| |black| |pre-commit|

.. |pyansys| image:: https://img.shields.io/badge/Py-Ansys-ffc107.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC
   :target: https://docs.pyansys.com/
   :alt: PyAnsys

.. |python| image:: https://img.shields.io/pypi/pyversions/ansys-fluent-core?logo=pypi
   :target: https://pypi.org/project/ansys-fluent-core/
   :alt: Python

.. |pypi| image:: https://img.shields.io/pypi/v/ansys-fluent-core.svg?logo=python&logoColor=white
   :target: https://pypi.org/project/ansys-fluent-core
   :alt: PyPI

.. |GH-CI| image:: https://github.com/ansys/pyfluent/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/ansys/pyfluent/actions/workflows/ci.yml
   :alt: GH-CI

.. |codecov| image:: https://codecov.io/gh/ansys/pyfluent/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/ansys/pyfluent

.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: MIT

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat
   :target: https://github.com/psf/black
   :alt: Black

.. |pre-commit| image:: https://results.pre-commit.ci/badge/github/ansys/pyfluent/main.svg
   :target: https://results.pre-commit.ci/latest/github/ansys/pyfluent/main
   :alt: pre-commit.ci status

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
Documentation for the latest stable release of PyFluent is hosted at
`PyFluent documentation <https://fluent.docs.pyansys.com/version/stable/>`_.

In the upper right corner of the documentation's title bar, there is an option for switching from
viewing the documentation for the latest stable release to viewing the documentation for the
development version or previously released versions.

You can also `view <https://cheatsheets.docs.pyansys.com/pyfluent_cheat_sheet.png>`_ or
`download <https://cheatsheets.docs.pyansys.com/pyfluent_cheat_sheet.pdf>`_ the
PyFluent cheat sheet. This one-page reference provides syntax rules and commands
for using PyFluent.

On the `PyFluent Issues <https://github.com/ansys/pyfluent/issues>`_ page, you can create
issues to report bugs and request new features. On the `PyFluent Discussions
<https://github.com/ansys/pyfluent/discussions>`_ page or the `Discussions <https://discuss.ansys.com/>`_
page on the Ansys Developer portal, you can post questions, share ideas, and get community feedback.

To reach the project support team, email `pyansys.core@ansys.com <pyansys.core@ansys.com>`_.

Installation
------------
The ``ansys-fluent-core`` package supports Python 3.9 through Python
3.13 on Windows and Linux.

Install the latest release from `PyPI
<https://pypi.org/project/ansys-fluent-core/>`_ with:

.. code:: console

   pip install ansys-fluent-core

For developers
--------------
If you plan on doing local *development* of PyFluent with Git, install
the latest release with:

.. code:: console

   git clone https://github.com/ansys/pyfluent.git
   cd pyfluent
   pip install pip -U
   pip install -e .
   python codegen/allapigen.py  # Generates the API files

Dependencies
------------
You must have a licensed copy of Ansys Fluent installed locally. PyFluent
supports Fluent 2022 R2 and later. The Windows installation of Ansys Fluent automatically
sets the required environment variables so that PyFluent can find the Ansys Fluent
installation. Using Fluent 2023 R2 (or 23.2) installed in the default directory as an
example, the installer automatically sets the ``AWP_ROOT232`` environment variable to point
to ``C:\Program Files\ANSYS Inc\v232``.

On Linux, the required environment variable is not set automatically, and can be set for the
current user in the current shell session, using Fluent 2023 R2 in the default installation
directory as an example, before running PyFluent, with:

.. code:: console

    export AWP_ROOT232=/usr/ansys_inc/v232

For this setting to persist between different shell sessions for the current user, the same
export command can instead be added to the user's ``~/.profile`` file.

Getting started
---------------

Launching Fluent
~~~~~~~~~~~~~~~~
To launch Fluent from Python, use the ``launch_fluent`` function:

.. code:: python

  import ansys.fluent.core as pyfluent
  solver_session = pyfluent.launch_fluent(mode="solver")
  solver_session.health_check.is_serving

Basic usage
~~~~~~~~~~~
You can use the ``solver_session.tui`` interface to run all Fluent TUI commands:

.. code:: python

  solver_session.tui.file.read_case('elbow.cas.h5')
  solver_session.tui.define.models.unsteady_2nd_order("yes")
  solver_session.tui.solve.initialize.initialize_flow()
  solver_session.tui.solve.dual_time_iterate(2, 3)

You can also install and use these PyFluent libraries:

- `PyFluent Parametric <https://parametric.fluent.docs.pyansys.com/>`_, which provides
  access to Fluent's parametric workflows.
- `PyFluent Visualization <https://visualization.fluent.docs.pyansys.com/>`_, which
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
