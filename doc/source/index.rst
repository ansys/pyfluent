PyFluent Documentation |version|
================================

.. toctree::
   :hidden:
   :maxdepth: 2

   getting_started/index
   users_guide/index
   api/index
   examples/index
   contributing

Introduction
------------
Ansys Fluent is a state-of-the-art computational fluid dynamics (CFD) software
package for modeling fluid flow, heat transfer, and chemical reactions in
complex geometries.

Python is a portable, dynamically typed, interpreted programming language that
is easy to learn, read, and write. It is free to use and distribute and is
supported by a vast support library of thousands of available packages.

PyFluent is part of the growing `PyAnsys <https://docs.pyansys.com>`_ ecosystem
that lets you use Ansys Fluent within or alongside any other Python environment,
whether it is in conjunction with other Ansys Python libraries and packages or
with other external Python products.

PyFluent launches or connects with a running Fluent process as a server using
gRPC interfaces, but all you need to interact with is the Python interface.

You can use PyFluent to programmatically create, interact with and control an
Ansys Fluent session to create your own customized workspace. In addition, you
can use PyFluent to enhance your productivity with highly configurable,
customized scripts.

Features
--------
The primary package, ``ansys-fluent``, provides features such as:

- Scripting of Fluent's meshing capabilities. See the :ref:`ref_meshing` module
  for more information.
- Scripting using Fluent's TUI commands. See the :ref:`ref_solver_tui`  module for
  more information about the available commands.
- Script post processing using Fluent's in-built post processing capabilities.
  See the :ref:`ref_postprocessing` module for more information.
- Plotting of Fluent geometry and meshes using `PyVista
  <https://docs.pyvista.org>`_ from within a Python script or an
  interactive `Jupyter notebook <https://jupyter.org/>`_.
- Access to Fluent surface based field data as Python objects via `NumPy
  <https://numpy.org/>`_ arrays
- and more...
  
Beta Features
-------------
The settings object interface provides a more Pythonic way to access and modify
Fluent settings than the TUI command interface.  These API calls group Fluent
settings into a tree of objects where individal settings for material
properties, boundary conditions are accessible without the need to pass
parameter lists.

More information is available in the :ref:`ref_settings` module documentation.

Project Index
-------------

* :ref:`genindex`
