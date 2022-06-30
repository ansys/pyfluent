PyFluent Documentation |version|
================================

.. toctree::
   :hidden:
   :maxdepth: 2

   getting_started/index
   user_guide/index
   api/index
   examples/index
   contributing

Introduction
------------
Ansys Fluent is a state-of-the-art computational fluid dynamics (CFD) software
package for modeling fluid flow, heat transfer, and chemical reactions in
complex geometries.

Ansys Fluent provides complete mesh flexibility, including the ability to solve
your flow problems using unstructured meshes that can be generated about complex
geometries with relative ease. Supported mesh types include 2D
triangular/quadrilateral, 3D tetrahedral/hexahedral/pyramid/wedge/polyhedral,
and mixed (hybrid) meshes. Ansys Fluent also enables you to refine or coarsen
your mesh based on the flow solution.

You can read your mesh into Ansys Fluent, or, for 3D geometries, create your
mesh using the meshing mode of Fluent. All other operations are performed within
the solution mode of Fluent, including setting boundary conditions, defining
fluid properties, executing the solution, refining the mesh, running a parametric study, 
and postprocessing and viewing the results.

What is PyFluent?
-----------------

PyFluent is part of the `PyAnsys <https://docs.pyansys.com>`_ ecosystem that
lets you use Ansys Fluent within or alongside any other Python environment,
whether it is in conjunction with other Ansys Python libraries and packages or
with other external Python products.

PyFluent implements a client-server architecture.  PyFluent launches or connects
with a running Fluent process as a server using Google remote procedure calls, 
or gRPC interfaces, but all you need to interact with is the Python interface.

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
- and more...

Documentation and Issues
------------------------

In addition to installation, usage, and contribution information, the PyFluent
documentation provides API documentation, examples, and code guidelines.

On the PyFluent Issues page, you can create issues to submit questions,
report bugs, and request new features. To reach the project support team,
email pyansys.support@ansys.com.

License
-------
PyFluent is licensed under the MIT license.

This module makes no commercial claim over Ansys whatsoever. PyFluent extends
the functionality of Ansys Fluent by adding an additional Python interface to
Ansys Fluent without changing the core behavior or license of the original
software. The use of the interactive control of PyFluent requires a legally
licensed local copy of Ansys Fluent. For more information about Ansys Fluent,
visit the Ansys Fluent page on the Ansys website.

Project Index
-------------

* :ref:`genindex`
