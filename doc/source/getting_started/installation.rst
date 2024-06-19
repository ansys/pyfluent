.. _ref_installation:

============
Installation
============


PyFluent Installation
---------------------

PyFluent supports Python 3.9 through Python 3.12 on Windows, Mac OS and Linux.

PyFluent can be installed, along with all its optional dependencies, using:

.. code:: console
   pip install ansys-fluent-core


Development Installation
------------------------

The PyFluent source repository is available on GitHub. You can clone the repository using:
.. code:: console

   git clone https://github.com/ansys/pyfluent.git

Once you have cloned the repository, you can install PyFluent. Installing with the
-e option overwrites the directory in site-packages with a symbolic link to the repository,
meaning any changes you make to the PyFluent code reflect automatically when you use PyFluent.

.. code:: console

   pip install pip -U
   pip install -e ./pyfluent

The full PyFluent package includes some required API classes that are auto-generated rather than
being maintained under version control, so they are not present amongst the files in your
cloned repository at this point. You run the auto-generation using a script included in the repository,
as specified below. The auto-generation requires an Ansys Fluent installation.

.. code:: console

   python codegen/allapigen.py


Fluent Installation
-------------------

To benefit fully from using PyFluent, you must have a licensed copy of Ansys Fluent installed.
All versions of PyFluent support Fluent 2022 R2 and later. 

The Windows installation of Ansys Fluent automatically sets the required environment variables
so that PyFluent can find the Ansys Fluent installation. Using Fluent 2024 R2 installed in the
default directory as an example, the installer automatically sets the ``AWP_ROOT242`` environment
variable to point to ``C:\Program Files\ANSYS Inc\v242`` by default.

On Linux, the required environment variable is not set automatically, and can be set for the
current user in the current shell session. E.g.:

.. code:: console

    export AWP_ROOT242=/usr/ansys_inc/v242

For this variable to persist between different shell sessions for the current user, the same
export command can instead be added to the user's ``~/.profile`` file.

For information on other ways of specifying the Fluent location for PyFluent, see :ref:`faqs_fluentloc` in :ref:`faqs`.


Additional PyFluent packages
----------------------------
In addition to the ``ansys-fluent-core`` package, you can install and use the
``pyfluent-parameteric`` and ``pyfluent-visualization`` packages:

- The `PyFluent-Parametric <https://parametric.fluent.docs.pyansys.com/>`_ package provides
  access to Fluent's parametric workflows.
- The `PyFluent-Visualization <https://visualization.fluent.docs.pyansys.com/>`_ package
  provides postprocessing and visualization capabilities that use `pyvista <https://docs.pyvista.org/>`_
  and `matplotlib <https://matplotlib.org/>`_ packages.
