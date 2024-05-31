.. _ref_user_guide:

==========
User guide
==========
Anyone who wants to use PyFluent can import its Python modules and develop
Python code to control and monitor Ansys Fluent.

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
Welcome to the PyFluent User Guide. This guide will help you understand how to use PyFluent to leverage the power of ANSYS Fluent for your CFD simulations.


A Simple Example
----------------
.. code-block:: python
	>>> import ansys.fluent.core as pf
	>>> meshing = pf.launch_fluent(mode=pf.FluentMode.MESHING_MODE, product_version=pf.FluentVersion.v242)
	>>> wt = meshing.watertight()
	>>> wt.import_geometry.file_name = pf.examples.download_file("mixing_elbow.pmdb","pyfluent/mixing_elbow")
	>>> wt.import_geometry()
	>>> wt.create_volume_mesh()
	>>> meshing.switch_to_solver()
	>>> solver.setup.boundary_conditions.set_zone_type(zone_list=["cold-inlet", "hot-inlet"], new_type="velocity-inlet")
	>>> solver.setup.boundary_conditions.set_zone_type(zone_list=["outlet"], new_type="pressure-outlet")
	>>> solver.setup.cell_zone_conditions.set_zone_type(zone_list="elbow-fluid", new_type="fluid")
	>>> solver.solution.initialization.hybrid_initialize()
	>>> solver.solution.run_calculation.iterate(iter_count=100)
	>>> velocity_data = solver.field_data.get_vector_field_data(field_name="velocity", surface_name="cold-inlet")


Key Features
------------

Guided Meshing Workflows
------------------------
Leverage intuitive, guided workflows to create high-quality meshes.

Solution Mode and Settings Objects
----------------------------------
Utilize settings objects to configure and control your simulation.

Data Extraction
---------------
Easily extract solution and mesh data for analysis and post-processing.

