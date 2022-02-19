PyFluent
========
Fluent's Solver and Meshing capabilities exposed in Python

Installation
------------
For a local "development" version, install with:

.. code:: console

  git clone https://github.com/pyansys/pyfluent.git
  cd pyfluent
  pip install -e .

Usage
-----
1) Fluent should be installed from the latest daily build. Set AWP_ROOT environment variable to vXXX directory to use a custom Fluent build.
2) Within a Python 3 console, execute:

.. code:: python

  import ansys.fluent as pyfluent
  pyfluent.set_log_level('DEBUG') # for development, by default only errors are shown
  session = pyfluent.launch_fluent()
  session.check_health()
  session.tui.solver.file.read_case(case_file_name='elbow.cas.gz')
  session.tui.solver.define.models.unsteady_2nd_order("yes")
  session.tui.solver.solve.initialize.initialize_flow()  
  session.tui.solver.solve.dual_time_iterate(number_of_time_steps=2, maximum_number_of_iterations_per_time_step=3)


Meshing TUI and workflow
************************
TUI and meshing workflows from Fluent meshing are exposed. Please check `meshing <https://github.com/pyansys/pyfluent/blob/main/doc/source/api/meshing.rst>`_ for example usage.

Settings access
***************
The settings objects provide a natural way to access and modify settings. The
top-level settings object for a session can be accessed with the ``get_root()``
method of the session object. More information can be found at 
`settings <https://github.com/pyansys/pyfluent/blob/main/doc/source/api/settings.rst>`_.


Post Processing
***************

In Fluent (server)
^^^^^^^^^^^^^^^^^^

.. code:: python

  session.tui.solver.display.objects.contour['contour-1'] = {'boundary_values': True, 'color_map': {'color': 'field-velocity', 'font_automatic': True, 'font_name': 'Helvetica', 'font_size': 0.032, 'format': '%0.2e', 'length': 0.54, 'log_scale': False, 'position': 1, 'show_all': True, 'size': 100, 'user_skip': 9, 'visible': True, 'width': 6.0}, 'coloring': {'smooth': False}, 'contour_lines': False, 'display_state_name': 'None', 'draw_mesh': False, 'field': 'pressure', 'filled': True, 'mesh_object': '', 'node_values': True, 'range_option': {'auto_range_on': {'global_range': True}}, 'surfaces_list': [2, 5]}
  session.tui.solver.display.objects.contour['contour-1']()
  session.tui.solver.display.objects.contour['contour-1'].field.set_state('velocity-magnitude')
  session.tui.solver.display.objects.contour['contour-1'].field()
  session.tui.solver.display.objects.contour['contour-1'].color_map.size.set_state(80.0)
  session.tui.solver.display.objects.contour['contour-1'].color_map.size()
  session.tui.solver.display.objects.contour['contour-1'].rename('my-contour')
  del session.tui.solver.display.objects.contour['my-contour']

PyVista (client)
^^^^^^^^^^^^^^^^

.. code:: python

  #import module
  import ansys.fluent.postprocessing.pyvista as pv

  #get the graphics objects for the session

  graphics_session1 = pv.Graphics(session)
  mesh1 = graphics_session1.Meshes["mesh-1"]
  contour1 = graphics_session1.Contours["contour-1"]
  contour2 = graphics_session1.Contours["contour-2"]
  surface1 = graphics_session1.Surfaces["surface-1"]

  #set graphics objects properties

  #mesh
  mesh1.show_edges = True
  mesh1.surfaces_list = ['symmetry']

  #contour
  contour1.field = "velocity-magnitude"
  contour1.surfaces_list = ['symmetry']

  contour2.field = "temperature"
  contour2.surfaces_list = ['symmetry', 'wall']

  #copy
  graphics_session1.Contours["contour-3"] = contour2()

  #update
  contour3 = graphics_session1.Contours["contour-3"]
  contour3.update(contour1())

  #delete
  del graphics_session1.Contours["contour-3"] 

  #loop
  for name, _ in graphics_session1.Contours.items():
      print(name)

  #iso surface
  surface1.surface_type.iso_surface.field= "velocity-magnitude"
  surface1.surface_type.iso_surface.rendering= "contour"

  #display in default plotter
  contour1.display()
  mesh1.display()
  surface1.display()
  
  #display in seprate plotter e.g. plotter-2
  contour1.display("plotter-2")

  session.exit()


.. include:: doc/source/api/settings.rst
