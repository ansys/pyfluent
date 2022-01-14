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
1) Run Fluent from the latest develop branch.
2) In the Fluent Console (TUI) execute the following Scheme code: (enable-feature 'new-tui)
3) Start the server with server.txt as server-info filename. 
   E.g., from the Fluent UI File Menu, select Applications > Server > Start ... . Enter server.txt in the dialog and select OK.

In Python (client-side):

.. code:: python

  import ansys.fluent.solver as pyfluent
  session = pyfluent.start(r'<path-to-server-file>/server.txt')
  session.tui.file.read_case(case_file_name='tet.cas.gz')
  session.tui.define.models.unsteady_2nd_order("yes")
  session.tui.solve.initialize.initialize_flow()
  session.tui.solve.dual_time_iterate(number_of_total_periods=2, maximum_number_of_iterations_per_time_step=3)
  session.tui.display.objects.contour['contour-1'] = {'boundary_values': True, 'color_map': {'color': 'field-velocity', 'font_automatic': True, 'font_name': 'Helvetica', 'font_size': 0.032, 'format': '%0.2e', 'length': 0.54, 'log_scale': False, 'position': 1, 'show_all': True, 'size': 100, 'user_skip': 9, 'visible': True, 'width': 6.0}, 'coloring': {'smooth': False}, 'contour_lines': False, 'display_state_name': 'None', 'draw_mesh': False, 'field': 'pressure', 'filled': True, 'mesh_object': '', 'node_values': True, 'range_option': {'auto_range_on': {'global_range': True}}, 'surfaces_list': [2, 5]}
  session.tui.display.objects.contour['contour-1']()
  session.tui.display.objects.contour['contour-1'].field.set_state('velocity-magnitude')
  session.tui.display.objects.contour['contour-1'].field()
  session.tui.display.objects.contour['contour-1'].color_map.size.set_state(80.0)
  session.tui.display.objects.contour['contour-1'].color_map.size()
  session.tui.display.objects.contour['contour-1'].rename('my-contour')
  del session.tui.display.objects.contour['my-contour']
  session.stop()

