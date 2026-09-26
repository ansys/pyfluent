.. _ref_installation:

============
Installation
============


PyFluent Installation
---------------------

PyFluent supports Python 3.10 through Python 3.14 on Windows, Mac OS and Linux.

PyFluent can be installed, along with all its optional dependencies, using:

.. code:: console

   pip install ansys-fluent-core


Using a virtual environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is recommended to use a `virtual environment <https://docs.python.org/3/tutorial/venv.html>`_ when installing PyFluent to avoid conflicts with other Python packages.
A virtual environment can be created and activated with the following commands:

.. code:: console

   python -m venv .venv


On Windows:

.. code:: console

   .venv\Scripts\activate


On Linux and Mac OS:

.. code:: console

   source .venv/bin/activate


Then, install PyFluent in the virtual environment with:

.. code:: console

   python -m pip install ansys-fluent-core


Development Installation
------------------------
The PyFluent source repository is available on GitHub. Clone it and set up a virtual
environment as described above, then install PyFluent in editable mode:

.. code:: console

   git clone https://github.com/ansys/pyfluent.git
   cd pyfluent
   pip install pip -U
   pip install -e .
   python codegen/allapigen.py     # Generates the API files or
   python codegen/allapigen.py -v  # Pass -v or --verbose to display the paths of the generated API files

Installing with the ``-e`` option (editable mode) creates a symbolic link to the repository in
your Python installation's ``site-packages`` directory, so changes to the PyFluent source are
reflected immediately without reinstalling. The ``codegen/allapigen.py`` script generates API
classes that aren't tracked under version control; this step requires a licensed Ansys Fluent
installation.

Fluent Installation
-------------------

To benefit fully from using PyFluent, you must have a licensed copy of Ansys Fluent installed.
PyFluent is compatible with the full set of Fluent versions officially supported at its release date.

PyFluent uses an environment variable to locate your Ansys installation.

On Windows, the Ansys installer sets the environment variable. For instance, the Ansys 2025 R2
installer sets the ``AWP_ROOT252`` environment variable to point to ``C:\Program Files\ANSYS Inc\v252``
if you accept the default installation location.

**On Linux, the environment variable is not set automatically.** It can be set for the
current user in the current shell session as follows:

.. code:: console

    export AWP_ROOT252=/usr/ansys_inc/v252

For this variable to persist between different shell sessions for the current user, the same
export command can instead be added to the user's ``~/.profile`` file.

For information on other ways of specifying the Fluent location for PyFluent, see :ref:`faqs_fluentloc` in :ref:`faqs`.

.. note::
   Ansys Fluent versions prior to 2024 R2 were supported by PyFluent version 0.37 and earlier.
   These versions are no longer supported in the current PyFluent releases.


Additional PyFluent packages
----------------------------
In addition to the ``ansys-fluent-core`` package, you can install and use the
``pyfluent-parameteric`` and ``pyfluent-visualization`` packages:

- The `PyFluent-Parametric <https://parametric.fluent.docs.pyansys.com/>`_ package provides
  access to Fluent's parametric workflows.
- The `PyFluent-Visualization <https://visualization.fluent.docs.pyansys.com/>`_ package
  provides postprocessing and visualization capabilities that use `pyvista <https://docs.pyvista.org/>`_
  and `matplotlib <https://matplotlib.org/>`_ packages.
