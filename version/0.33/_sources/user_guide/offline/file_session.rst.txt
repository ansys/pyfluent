.. _ref_file_session_guide:

.. vale Google.Spacing = NO

File Session
============

The :obj:`~ansys.fluent.core.file_session.FileSession` class mimics the functionality of :ref:`live session objects <ref_session_guide>`, allowing you
to access field data and other relevant information without a live Fluent session.
You command :obj:`~ansys.fluent.core.file_session.FileSession` objects to read your input files before you access the data through
the :obj:`~ansys.fluent.core.file_session.FileSession` object methods. 

Sample usage
------------

The following examples cover both single-phase and multiphase cases. After case and data files are
loaded, field information is accessed and some field data is extracted. Here, the extraction uses two approaches:
a transaction-based approach where multiple data requests are bundled into each transaction and a direct approach
where a sequence of separate requests are made.

Single-phase
~~~~~~~~~~~~

.. code-block:: python

  >>> from ansys.fluent.core.file_session import FileSession
  >>> from ansys.fluent.core import (
  >>>   examples,
  >>>   ScalarFieldDataRequest,
  >>>   SurfaceDataType,
  >>>   SurfaceFieldDataRequest,
  >>>   VectorFieldDataRequest,
  >>> )

  >>> case_file_name = examples.download_file("elbow1.cas.h5", "pyfluent/file_session")
  >>> data_file_name = examples.download_file("elbow1.dat.h5", "pyfluent/file_session")
  >>> file_session = FileSession(case_file_name, data_file_name)

  >>> file_session.fields.field_info.get_scalar_field_range("SV_T")
  [0.0, 313.1515948109515]
  >>> file_session.fields.field_info.get_surfaces_info()
  {'wall': {'surface_id': [3],
   'zone_id': -1,
   'zone_type': 'wall',
   'type': 'plane'},
   'symmetry': {'surface_id': [4],
   'zone_id': -1,
   'zone_type': 'wall',
   'type': 'plane'},
    .....
   'default-interior': {'surface_id': [9],
   'zone_id': -1,
   'zone_type': 'wall',
   'type': 'plane'}}
  >>> file_session.fields.field_info.get_scalar_fields_info()
  {'SV_ARTIFICIAL_WALL_FLAG': {'display_name': 'SV_ARTIFICIAL_WALL_FLAG',
   'section': 'field-data',
   'domain': 'phase-1'},
   'SV_D': {'display_name': 'SV_D',
   'section': 'field-data',
   'domain': 'phase-1'},
   .....
   'SV_WALL_YPLUS_UTAU': {'display_name': 'SV_WALL_YPLUS_UTAU',
   'section': 'field-data',
   'domain': 'phase-1'}}
   >>> file_session.fields.field_info.get_vector_fields_info()
   {'velocity': {'x-component': 'SV_U',
    'y-component': 'SV_V',
    'z-component': 'SV_W'}}
   >>> transaction = file_session.fields.field_data.new_transaction()
   >>> vertices_and_faces_connectivity_request = SurfaceFieldDataRequest(
   >>>      data_types=[SurfaceDataType.Vertices, SurfaceDataType.FacesConnectivity],
   >>>      surfaces=[3, 4],
   >>> )
   >>> solution_variable_temperature_request = ScalarFieldDataRequest(field_name="SV_T", surfaces=[3, 4], node_value=False, boundary_value=False)
   >>> velocity_request = VectorFieldDataRequest(field_name="velocity", surfaces=[3, 4])
   >>> transaction.add_requests(vertices_and_faces_connectivity_request, solution_variable_temperature_request, velocity_request)
   >>> data = transaction.get_response()
   >>> data.get_field_data(vertices_and_faces_connectivity_request)[3][SurfaceDataType.Vertices]
   array([[ 0.        , -0.1016    ,  0.        ],
       [-0.00635   , -0.1016    ,  0.        ],
       [-0.00634829, -0.10203364,  0.00662349],
       ...,
       [ 0.01857703, -0.19223897,  0.03035362],
       [ 0.0124151 , -0.19273971,  0.03034735],
       [ 0.00620755, -0.19304685,  0.03033731]])
   >>> data.get_field_data(solution_variable_temperature_request)[4]
   array([293.14999, 293.14999, 293.14999, ..., 293.14999, 293.14999,
       293.14999])
   >>> data.get_field_data(velocity_request).keys()
   dict_keys([3, 4]
   >>> data.get_field_data(velocity_request)[4].shape
   (2018, 3)

   >>> vertices_request = SurfaceFieldDataRequest(data_types=[SurfaceDataType.Vertices], surfaces=[3, 4])
   >>> file_session.fields.field_data.get_field_data(vertices_request)[3].shape
   (3810, 3)
   >>> file_session.fields.field_data.get_field_data(vertices_request)[3][1500][0]
   0.12405861914157867
   >>> file_session.fields.field_data.get_field_data(ScalarFieldDataRequest(field_name="SV_T", surfaces=["wall"]))["wall"].shape
   (3630,)
   >>> file_session.fields.field_data.get_field_data(ScalarFieldDataRequest(field_name="SV_T", surfaces=["wall"]))["wall"][1500]
   293.18071329432047
   >>> velocity_request = VectorFieldDataRequest(field_name="velocity", surfaces=["symmetry"])
   >>> file_session.fields.field_data.get_field_data(velocity_request)["symmetry"].shape
   (2018, 3)
   >>> file_session.fields.field_data.get_field_data(velocity_request)["symmetry"][1000][0]
   0.001690600193527586


Multiphase
~~~~~~~~~~~

.. code-block:: python

  >>> from ansys.fluent.core.file_session import FileSession
  >>> from ansys.fluent.core import (
  >>>   examples,
  >>>   ScalarFieldDataRequest,
  >>>   SurfaceDataType,
  >>>   SurfaceFieldDataRequest,
  >>>   VectorFieldDataRequest,
  >>> )

  >>> case_file_name = examples.download_file("mixing_elbow_mul_ph.cas.h5", "pyfluent/file_session")
  >>> data_file_name = examples.download_file("mixing_elbow_mul_ph.dat.h5", "pyfluent/file_session")
  >>> file_session = FileSession()
  >>> file_session.read_case(case_file_name)
  >>> file_session.read_data(data_file_name)

  >>> file_session.fields.field_info.get_scalar_field_range("phase-2:SV_P")
  [0.0, 1.5435200335871788e-11]
  >>> file_session.fields.field_info.get_scalar_fields_info()
  {'phase-1:SV_ARTIFICIAL_WALL_FLAG': {'display_name': 'SV_ARTIFICIAL_WALL_FLAG',
   'section': 'field-data',
   'domain': 'phase-1'},
   'phase-1:SV_DENSITY': {'display_name': 'SV_DENSITY',
   'section': 'field-data',
   'domain': 'phase-1'},
   .....
   'phase-4:': {'display_name': '',
   'section': 'field-data',
   'domain': 'phase-4'}}
   >>> file_session.fields.field_info.get_vector_fields_info()
   {'phase-1:velocity': {'x-component': 'phase-1: SV_U',
    'y-component': 'phase-1: SV_V',
    'z-component': 'phase-1: SV_W'},
    .....
    'phase-4:velocity': {'x-component': 'phase-4: SV_U',
    'y-component': 'phase-4: SV_V',
    'z-component': 'phase-4: SV_W'}}
   >>> transaction = file_session.fields.field_data.new_transaction()
   >>> ph1_density_request = ScalarFieldDataRequest(field_name="phase-1:SV_DENSITY", surfaces=[30], node_value=False, boundary_value=False)
   >>> ph1_velocity_request = VectorFieldDataRequest(field_name="phase-1:velocity", surfaces=[30])
   >>> transaction.add_requests(ph1_density_request, ph1_velocity_request)
   >>> data = transaction.get_response()
   >>> data.get_field_data(ph1_density_request)[30]
   array([1.225, 1.225, 1.225, 1.225, 1.225, 1.225, 1.225, 1.225, 1.225,
       1.225, 1.225, 1.225, 1.225, 1.225, 1.225, 1.225, 1.225, 1.225,
       1.225, 1.225, 1.225, 1.225, 1.225, 1.225, 1.225, 1.225, 1.225,
       1.225, 1.225, 1.225, 1.225, 1.225, 1.225, 1.225, 1.225, 1.225,
       1.225, 1.225, 1.225, 1.225, 1.225, 1.225, 1.225, 1.225, 1.225,
       1.225, 1.225, 1.225, 1.225, 1.225, 1.225, 1.225, 1.225, 1.225,
       1.225])
   >>> data.get_field_data(ph1_velocity_request)[30].shape
   (55, 3)

   >>> vertices_data_request = SurfaceFieldDataRequest(data_types=[SurfaceDataType.Vertices], surfaces=[30])
   >>> file_session.fields.field_data.get_field_data(vertices_data_request)[30].shape
   (79, 3)
   >>> file_session.fields.field_data.get_field_data(vertices_data_request)[30][50][0]
   0.14896461503555408
   >>> ph1_pressure_request = ScalarFieldDataRequest(field_name="phase-1:SV_P", surfaces=["wall-elbow"])
   >>> file_session.fields.field_data.get_field_data(ph1_pressure_request)["wall-elbow"].shape
   (2168,)
   >>> file_session.fields.field_data.get_field_data(ph1_pressure_request)["wall-elbow"][1100]
   1.4444035696104466e-11
   >>> ph2_velocity_request = VectorFieldDataRequest(field_name="phase-2:velocity", surfaces=["wall-elbow"])
   >>> file_session.fields.field_data.get_field_data(ph2_velocity_request)["wall-elbow"].shape
   (2168, 3)
   >>> file_session.fields.field_data.get_field_data(ph2_velocity_request)["wall-elbow"][1000][0]
   0.0


Visualization sample usage
--------------------------

You can use the `ansys-fluent-visualization <https://visualization.fluent.docs.pyansys.com/version/stable/>`_ package to display the
mesh and to visualize results via contours, vectors and other
post-processing objects.


.. code-block:: python

  >>> from ansys.fluent.visualization import set_config
  >>> set_config(blocking=True, set_view_on_display="isometric")
  >>> import ansys.fluent.core as pyfluent
  >>> from ansys.fluent.core import examples
  >>> from ansys.fluent.visualization.matplotlib import Plots
  >>> from ansys.fluent.visualization.pyvista import Graphics
  >>> from ansys.fluent.core.file_session import FileSession
  >>> fileSession=FileSession()
  >>> fileSession.read_case("elbow1.cas.h5")
  >>> fileSession.read_data("elbow1.dat.h5")
  >>> graphics = Graphics(session=fileSession)

Display mesh at wall.

.. code-block:: python

  >>> mesh1 = graphics.Meshes["mesh-1"]
  >>> mesh1.show_edges = True
  >>> mesh1.surfaces_list = [ "wall"]
  >>> mesh1.display("w1")

Display temperature contour at symmetry.

.. code-block:: python

  >>> contour1 = graphics.Contours["mesh-1"]
  >>> contour1.node_values = False
  >>> contour1.field = "SV_T"
  >>> contour1.surfaces_list = ['symmetry']
  >>> contour1.display('w2')

Display velocity vector data at symmetry and wall.

.. code-block:: python

  >>> velocity_vector = graphics.Vectors["velocity-vector"]
  >>> velocity_vector.field = "SV_T"
  >>> velocity_vector.surfaces_list = ['symmetry', 'wall']
  >>> velocity_vector.display("w3")
