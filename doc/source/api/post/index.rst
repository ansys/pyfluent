.. _ref_postprocessing:

Postprocessing
==============

Post processing Fluent results can be done with either Fluent in-built post
processing capabilities or with the PyVista/MatplotLib integration.

Fluent
------

Here visualization objects are constructed within Fluent.  Graphics can be
written to a file using standard Fluent commands.

.. code:: python

  session.solver.tui.display.objects.contour['contour-1'] = {'boundary_values': True, 'color_map': {'color': 'field-velocity', 'font_automatic': True, 'font_name': 'Helvetica', 'font_size': 0.032, 'format': '%0.2e', 'length': 0.54, 'log_scale': False, 'position': 1, 'show_all': True, 'size': 100, 'user_skip': 9, 'visible': True, 'width': 6.0}, 'coloring': {'smooth': False}, 'contour_lines': False, 'display_state_name': 'None', 'draw_mesh': False, 'field': 'pressure', 'filled': True, 'mesh_object': '', 'node_values': True, 'range_option': {'auto_range_on': {'global_range': True}}, 'surfaces_list': [2, 5]}
  session.solver.tui.display.objects.contour['contour-1']()
  session.solver.tui.display.objects.contour['contour-1'].field.set_state('velocity-magnitude')
  session.solver.tui.display.objects.contour['contour-1'].field()
  session.solver.tui.display.objects.contour['contour-1'].color_map.size.set_state(80.0)
  session.solver.tui.display.objects.contour['contour-1'].color_map.size()
  session.solver.tui.display.objects.contour['contour-1'].rename('my-contour')
  del session.solver.tui.display.objects.contour['my-contour']

PyVista Example (Graphics)
--------------------------

Here the field data is extracted from the Fluent session into the Python
environment and PyVista is used to visualze the extracted data.

.. code:: python

  # import module
  from ansys.fluent.post.pyvista import Graphics

  # get the graphics objects for the session

  graphics_session1 = Graphics(session)
  mesh1 = graphics_session1.Meshes["mesh-1"]
  contour1 = graphics_session1.Contours["contour-1"]
  contour2 = graphics_session1.Contours["contour-2"]
  surface1 = graphics_session1.Surfaces["surface-1"]

  # set graphics objects properties

  # mesh
  mesh1.show_edges = True
  mesh1.surfaces_list = ['symmetry']

  # contour
  contour1.field = "velocity-magnitude"
  contour1.surfaces_list = ['symmetry']

  contour2.field = "temperature"
  contour2.surfaces_list = ['symmetry', 'wall']

  # copy
  graphics_session1.Contours["contour-3"] = contour2()

  # update
  contour3 = graphics_session1.Contours["contour-3"]
  contour3.update(contour1())

  # delete
  del graphics_session1.Contours["contour-3"] 

  # loop
  for name, _ in graphics_session1.Contours.items():
      print(name)

  # iso surface
  surface1.surface.iso_surface.field= "velocity-magnitude"
  surface1.surface.iso_surface.rendering= "contour"

  # display 
  contour1.display()
  mesh1.display()
  surface1.display()
  
  # To display in specific window e.g. window-2
  contour1.display("window-2")
  
MatplotLib Example (XYPlots)
----------------------------

Here the plot data is extracted from the Fluent session into the Python
environment and data is plotted in MatplotLib.

.. code:: python

  # import module
  from ansys.fluent.post.matplotlib import Plots

  # get the plots object for the session
  plots_session1 = Plots(session)
  
  #get xyplot object
  plot1=plots_session1.XYPlots["plot-1"]
  
  #set properties
  plot1.surfaces_list = ["symmetry"]
  plot1.y_axis_function = "temperature"
  
  #Draw plot
  plot1.plot("window-1")

  session.exit()

.. currentmodule:: ansys.fluent.post

.. autosummary::
   :toctree: _autosummary

.. toctree::
   :maxdepth: 2
   :hidden:
   
   pyvista_objects
