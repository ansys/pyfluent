.. _ref_file_session:

File Session
============

The FileSession class provides an interface to expose field info and
field data from a case and data file.

Sample usage
------------

You can use the FileSession by passing the case and data file information by using
the CaseReader (:ref:`ref_case_reader`) and DataReader (:ref:`ref_data_reader`).
This example shows adding case and data file information to FileSession. Then,
field info is extracted followed by adding a transaction request and extracting
field data. One can either run a single or multi-phase case. In that respect, the example
covers both single and multi-phase cases.

Single phase
------------

.. code-block:: python

  >>> from ansys.fluent.core import examples
  >>> from ansys.fluent.core.file_session import FileSession

  >>> case_filepath = examples.download_file("elbow1.cas.h5", "pyfluent/file_session")
  >>> data_filepath = examples.download_file("elbow1.dat.h5", "pyfluent/file_session")
  >>> file_session = FileSession()
  >>> file_session.read_case(case_filepath)
  >>> file_session.read_data(data_filepath)

  >>> file_session.field_info.get_scalar_field_range("SV_T")
  [293.1446694544748, 313.1515948109515]
  >>> file_session.field_info.get_surfaces_info()
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
  >>> file_session.field_info.get_scalar_fields_info()
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
   >>> file_session.field_info.get_vector_fields_info()
   {'velocity': {'x-component': 'SV_U',
    'y-component': 'SV_V',
    'z-component': 'SV_W'}}
   >>> transaction = file_session.field_data.new_transaction()
   >>> transaction.add_surfaces_request([3, 4])
   >>> transaction.add_scalar_fields_request("SV_T", [3, 4])
   >>> transaction.add_vector_fields_request("velocity", [3, 4])
   >>> transaction.get_fields()
   {(('type', 'scalar-field'),
     ('dataLocation', 1),
     ('boundaryValues',
      False)): {3: {'SV_T': array([293.14999, 293.14999, 293.14999, ..., 293.14999, 293.14999,
             293.14999])}, 4: {'SV_T': array([293.14999, 293.14999, 293.14999, ..., 293.14999, 293.14999,
             293.14999])}},
    (('type',
      'vector-field'),): {3: {'velocity': array([0., 0., 0., ..., 0., 0., 0.]), 'vector-scale': array([0.1])},
     4: {'velocity': array([ 3.32643010e-01,  6.64311343e-03,  0.00000000e+00, ...,
              4.56052223e-01,  2.45034248e-01, -1.24726618e-15]),
      'vector-scale': array([0.1])}},
    (('type',
      'surface-data'),): {3: {'faces': array([   4,    3,    2, ...,  727,  694, 3809], dtype=uint32), 'vertices': array([ 0.        , -0.1016    ,  0.        , ...,  0.00620755,
             -0.19304685,  0.03033731])},
     4: {'faces': array([   4,  295,  294, ...,  265, 1482, 2183], dtype=uint32),
      'vertices': array([ 0.        , -0.1016    ,  0.        , ...,  0.06435075,
             -0.08779959,  0.        ])}}
   >>> from ansys.fluent.core.services.field_data import SurfaceDataType
   >>> file_session.field_data.get_surface_data(SurfaceDataType.Vertices, [3, 4])[3].size
   3810
   >>> file_session.field_data.get_surface_data(SurfaceDataType.Vertices, [3, 4])[3][1500].x
   0.12405861914157867
   >>> file_session.field_data.get_scalar_field_data("SV_T", surface_name="wall").size
   3630
   >>> file_session.field_data.get_scalar_field_data("SV_T", surface_name="wall")[1500].scalar_data
   293.18071329432047
   >>> file_session.field_data.get_vector_field_data("velocity", surface_name="symmetry").size
   2018
   >>> file_session.field_data.get_vector_field_data("velocity", surface_name="symmetry")[1000].x
   0.001690600193527586


Multi phase
-----------

.. code-block:: python

  >>> from ansys.fluent.core import examples
  >>> from ansys.fluent.core.file_session import FileSession

  >>> case_filepath = examples.download_file("mixing_elbow_mul_ph.cas.h5", "pyfluent/file_session")
  >>> data_filepath = examples.download_file("mixing_elbow_mul_ph.dat.h5", "pyfluent/file_session")
  >>> file_session = FileSession()
  >>> file_session.read_case(case_filepath)
  >>> file_session.read_data(data_filepath)

  >>> file_session.field_info.get_scalar_field_range("phase-2:SV_P")
  [0.0, 1.5435200335871788e-11]
  >>> file_session.field_info.get_scalar_fields_info()
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
   >>> file_session.field_info.get_vector_fields_info()
   {'phase-1:velocity': {'x-component': 'phase-1: SV_U',
    'y-component': 'phase-1: SV_V',
    'z-component': 'phase-1: SV_W'},
    .....
    'phase-4:velocity': {'x-component': 'phase-4: SV_U',
    'y-component': 'phase-4: SV_V',
    'z-component': 'phase-4: SV_W'}}
   >>> transaction = file_session.field_data.new_transaction()
   >>> transaction.add_scalar_fields_request("phase-1:SV_DENSITY", [30])
   >>> transaction.add_vector_fields_request("phase-1:velocity", [30])
   >>> transaction.get_fields()
   {(('type', 'scalar-field'),
     ('dataLocation', 1),
     ('boundaryValues',
      False)): {30: {'phase-1:SV_DENSITY': array([1.225, .....          1.225])}},
    (('type',
      'vector-field'),): {30: {'phase-1:velocity': array([0., ..... 0.]),
      'vector-scale': array([0.1])}}}
   >>> from ansys.fluent.core.services.field_data import SurfaceDataType
   >>> file_session.field_data.get_surface_data(SurfaceDataType.Vertices, [30])[30].size
   79
   >>> ffile_session.field_data.get_surface_data(SurfaceDataType.Vertices, [30])[30][50].x
   0.14896461503555408
   >>> file_session.field_data.get_scalar_field_data("phase-1:SV_P", surface_name="wall-elbow").size
   2168
   >>> file_session.field_data.get_scalar_field_data("phase-1:SV_P", surface_name="wall-elbow")[1100].scalar_data
   1.4444035696104466e-11
   >>> file_session.field_data.get_vector_field_data("phase-2:velocity", surface_name="wall-elbow").size
   2168
   >>> file_session.field_data.get_vector_field_data("phase-2:velocity", surface_name="wall-elbow")[1000].x
   0.0


Sample usage
------------

You can use the Graphics toolbar to display the mesh, contour and vector data respectively.


.. code-block:: python

  >>> from ansys.fluent.visualization import set_config
  >>> set_config(blocking=True, set_view_on_display="isometric")
  >>> import ansys.fluent.core as pyfluent
  >>> from ansys.fluent.core import examples
  >>> from ansys.fluent.visualization.matplotlib import Plots
  >>> from ansys.fluent.visualization.pyvista import Graphics
  >>> from ansys.fluent.core.file_session  import FileSession
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


.. automodule:: ansys.fluent.core.filereader.data_file
   :members:
   :show-inheritance:
   :undoc-members:
   :exclude-members: __weakref__, __dict__
   :special-members: __init__
   :autosummary:
