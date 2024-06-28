.. _ref_user_guide:

==========
User guide
==========

..
   This toctree must be a top level index to get it to show up in
   pydata_sphinx_theme

.. toctree::
   :maxdepth: 1
   :hidden:

   launching_ansys_fluent
   specify_file_paths
   tui_commands
   meshing_workflow/index
   general_settings
   solver_settings
   models
   materials
   boundary_conditions
   solution


PyFluent User Guide
-------------------
Welcome to the PyFluent User Guide. This guide helps you understand how to use PyFluent to leverage the power of Ansys Fluent for your CFD simulations.


A Simple Example
----------------

.. code:: python

  >>> import ansys.fluent.core as pyfluent
  >>> meshing = pyfluent.launch_fluent(mode=pyfluent.FluentMode.MESHING, product_version=pyfluent.FluentVersion.v242)
  >>> watertight = meshing.watertight()
  >>> watertight.import_geometry.file_name = pyfluent.examples.download_file("mixing_elbow.pmdb","pyfluent/mixing_elbow")
  >>> watertight.import_geometry()
  >>> watertight.create_volume_mesh()
  >>> meshing.switch_to_solver()
  >>> solver.setup.boundary_conditions.set_zone_type(zone_list=["cold-inlet", "hot-inlet"], new_type="velocity-inlet")
  >>> solver.setup.boundary_conditions.set_zone_type(zone_list=["outlet"], new_type="pressure-outlet")
  >>> solver.setup.cell_zone_conditions.set_zone_type(zone_list="elbow-fluid", new_type="fluid")
  >>> solver.solution.initialization.hybrid_initialize()
  >>> solver.solution.run_calculation.iterate(iter_count=100)
  >>> velocity_data = solver.field_data.get_vector_field_data(field_name="velocity", surface_name="cold-inlet")


Key Features
------------

Launching Fluent from PyFluent
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:ref:`Start a Fluent session <ref_launch_guide>` locally or remotely with a variety of launch options, or connect
to an existing session. Interact with Fluent through the session object returned by the launch
or connect methods.

Guided Meshing Workflows
~~~~~~~~~~~~~~~~~~~~~~~~
Leverage intuitive, :ref:`guided workflows <ref_meshing_workflow>` to create high-quality meshes.

Solution Mode and Settings Objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Utilize :ref:`settings objects <ref_settings>` to configure and control your simulation.

Data Extraction
~~~~~~~~~~~~~~~
Extract solution and mesh data for analysis and post-processing.


Use Cases
---------
Some example use cases are given in this user guide.

Physics Models
~~~~~~~~~~~~~~
.. _ref_models_guide:



