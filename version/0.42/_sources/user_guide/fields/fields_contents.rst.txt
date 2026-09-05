.. _ref_fields_guide:

.. vale Google.Spacing = NO

Fields
======

PyFluent provides several services that allow you to access field data in different ways.
Every PyFluent solution and meshing :ref:`Session <ref_session_guide>` object contains a
``fields`` object. In both solution and meshing modes, the ``fields`` object contains
``field_data`` and ``field_data_streaming`` children. In
:obj:`solution <ansys.fluent.core.session_solver.Solver>` mode, the ``fields`` object
also has ``reduction``, ``solution_variable_data`` and ``solution_variable_info`` children.

To help decide between using ``field_data`` and ``solution_variable_data``, refer to the
:ref:`dedicated comparison guide <field_data_vs_solution_variable_data>`.

This guide explains:

- The surface-centric vs. zone-centric perspectives.
- Read vs. read/write capabilities.
- Typical use cases for each API.
- Performance and scope considerations.

.. toctree::
   :maxdepth: 1
   :hidden:

   field_vs_svars_data
   field_data
   reduction
   solution_data
