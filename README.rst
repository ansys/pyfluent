PyFluent
========
Fluent's SolverAPI exposed in Python

Installation
------------
For a local "development" version, install with:

.. code:: console

  git clone https://github.com/pyansys/pyfluent.git
  cd pyfluent
  pip install grpc\ansys-api-fluent-v0-0.0.1.tar.gz
  pip install -e .

We need to install the grpc package as it is not yet in PyPI.

Usage
-----
1) Fluent should be installed from the latest daily build. PyFluent determines the Fluent launch path from AWP_ROOT222 environment variable. That environment variable can be modified to use a custom Fluent build.
2) Within a Python 3 console, execute:

.. code:: python

  import ansys.fluent.solver as pyfluent
  import logging
  pyfluent.setLogLevel(logging.DEBUG) # for development, by default only errors are shown
  session = pyfluent.launch_fluent()
  session.health_check()
  session.tui.file.read_case(case_file_name='elbow.cas.gz')
  session.tui.define.models.unsteady_2nd_order("yes")
  session.tui.solve.initialize.initialize_flow()
  session.tui.solve.dual_time_iterate(number_of_time_steps=2, maximum_number_of_iterations_per_time_step=3)
  
Post Processing
---------------

In Fluent(server)  
-----------------
  session.tui.display.objects.contour['contour-1'] = {'boundary_values': True, 'color_map': {'color': 'field-velocity', 'font_automatic': True, 'font_name': 'Helvetica', 'font_size': 0.032, 'format': '%0.2e', 'length': 0.54, 'log_scale': False, 'position': 1, 'show_all': True, 'size': 100, 'user_skip': 9, 'visible': True, 'width': 6.0}, 'coloring': {'smooth': False}, 'contour_lines': False, 'display_state_name': 'None', 'draw_mesh': False, 'field': 'pressure', 'filled': True, 'mesh_object': '', 'node_values': True, 'range_option': {'auto_range_on': {'global_range': True}}, 'surfaces_list': [2, 5]}
  session.tui.display.objects.contour['contour-1']()
  session.tui.display.objects.contour['contour-1'].field.set_state('velocity-magnitude')
  session.tui.display.objects.contour['contour-1'].field()
  session.tui.display.objects.contour['contour-1'].color_map.size.set_state(80.0)
  session.tui.display.objects.contour['contour-1'].color_map.size()
  session.tui.display.objects.contour['contour-1'].rename('my-contour')
  del session.tui.display.objects.contour['my-contour']
  
PyVista (client)  
-----------------  
  #import module
  import ansys.fluent.postprocessing.pyvista as pv

  #get the graphics objects for the session
  
  graphics_session1 = pv.Graphics(session)
  mesh1 = graphics_session1.mesh["mesh-1"]
  contour1 = graphics_session1.contour["contour-1"]
  contour2 = graphics_session1.contour["contour-2"]
  surface1 = graphics_session1.surface["surface-1"]

  #set graphics objects properties
  
  #mesh
  mesh1.draw_mesh = True
  mesh1.surfaces_list = ['symmetry']

  #contour
  contour1.field = "velocity-magnitude"
  contour1.surfaces_list = ['symmetry']

  contour2.field = "temperature"
  contour2.surfaces_list = ['symmetry', 'wall']

  #iso surface
  surface1.surface_type.iso_surface.field= "velocity-magnitude"
  surface1.surface_type.iso_surface.rendering= "contour"

  #display
  contour1.display()
  mesh1.display()
  surface1.display()
  
  session.exit()

