.. _ref_field_data_guide:

.. vale Google.Spacing = NO

Field data
==========

You can use field data objects to access Fluent surface, scalar, vector, and pathlines data.

Accessing field data objects
----------------------------

To work with field data, ensure the Fluent solver is launched and the relevant data is made available.
You can do this either by loading both case and data files or by reading a case file and initializing.

.. code-block:: python

  >>> import ansys.fluent.core as pyfluent
  >>> from ansys.fluent.core.examples import download_file
  >>> solver = pyfluent.launch_fluent()
  >>> case_path = download_file(file_name="exhaust_system.cas.h5", directory="pyfluent/exhaust_system")
  >>> data_path = download_file(file_name="exhaust_system.dat.h5", directory="pyfluent/exhaust_system")
  >>> solver.settings.file.read_case_data(file_name=case_path)

  >>> field_data = solver.fields.field_data  # This creates an instance of the FieldData class.

Simple requests
---------------

To retrieve field data, instantiate a request object based on the data type:

- ``SurfaceFieldDataRequest`` for surface data.
- ``ScalarFieldDataRequest`` for scalar field data.
- ``VectorFieldDataRequest`` for vector field data.
- ``PathlinesFieldDataRequest`` for pathlines field data.

Then, use ``get_field_data`` and pass the request object as an argument to obtain the desired field data.

Retrieving surface data
~~~~~~~~~~~~~~~~~~~~~~~
To obtain surface vertex coordinates for a given surface, create a
``SurfaceFieldDataRequest`` and call the ``get_field_data`` method.

.. code-block:: python

  >>> from ansys.fluent.core.services.field_data import SurfaceDataType, SurfaceFieldDataRequest

  >>> vertices_request = SurfaceFieldDataRequest(
  >>>     surfaces=["inlet"],
  >>>     data_types=[SurfaceDataType.Vertices],
  >>> )
  >>> vertices_data = field_data.get_field_data(vertices_request)

  # Retrieves vertex coordinates as a NumPy array.
  # Shape: (389, 3) - This means 389 vertices, each defined by 3 coordinates (x, y, z).
  >>> vertices_data["inlet"].vertices.shape
  (389, 3)
  >>> vertices_data["inlet"].vertices[5]
  # Example: The 6th vertex (zero-based indexing) has coordinates [-0.3469, 0.0, -0.0386].
  array([-0.34689394,  0.        , -0.03863097], dtype=float32)

To retrieve surface face normals and centroids, include ``FacesNormal`` and ``FacesCentroid``
in the ``data_types`` list.

.. code-block:: python

  >>> faces_normal_and_centroid_request = SurfaceFieldDataRequest(
  >>>     surfaces=["inlet"],
  >>>     data_types=[SurfaceDataType.FacesNormal, SurfaceDataType.FacesCentroid],
  >>> )
  >>> faces_normal_and_centroid_data = field_data.get_field_data(faces_normal_and_centroid_request)

  # FacesNormal shape: (262, 3) - 262 face normals, each with 3 components (x, y, z).
  # FacesCentroid shape: (262, 3) - Centroids for each of the 262 faces, given as (x, y, z).
  >>> faces_normal_and_centroid_data["inlet"].face_normals.shape
  (262, 3)
  >>> faces_normal_and_centroid_data["inlet"].face_centroids[15]
  # Example: The centroid of the 16th face has coordinates [-0.3463, 0.0, -0.0328].
  array([-0.34634298,  0.        , -0.03276413], dtype=float32)

To obtain face connectivity data, specify ``FacesConnectivity`` as the ``data_types`` parameter.

.. code-block:: python

  >>> faces_connectivity_request = SurfaceFieldDataRequest(
  >>>     surfaces=["inlet"], data_types=[SurfaceDataType.FacesConnectivity]
  >>> )
  >>> faces_connectivity_data = field_data.get_field_data(faces_connectivity_request)

  # FacesConnectivity provides indices of vertices for each face. For example:
  # Face 6 is connected to vertices 4, 5, 12, and 11.
  >>> faces_connectivity_data["inlet"].connectivity[5]
  array([ 4,  5, 12, 11])

Get scalar field data
~~~~~~~~~~~~~~~~~~~~~
To retrieve scalar field data, such as absolute pressure, use ``ScalarFieldDataRequest``:

.. code-block:: python

  >>> from ansys.fluent.core.services.field_data import ScalarFieldDataRequest
  >>> absolute_pressure_request = ScalarFieldDataRequest(field_name="absolute-pressure", surfaces=["inlet"])
  >>> absolute_pressure_data = field_data.get_field_data(absolute_pressure_request)

  # Shape: (389,) - A single scalar value (e.g., pressure) for each of the 389 vertices.
  >>> absolute_pressure_data["inlet"].shape
  (389,)
  >>> absolute_pressure_data["inlet"][120]
  # Example: The absolute pressure at the 121st vertex is 102031.4 Pascals.
  102031.4

Get vector field data
~~~~~~~~~~~~~~~~~~~~~
To obtain vector field data, such as velocity vectors, use ``VectorFieldDataRequest``:

.. code-block:: python

  >>> from ansys.fluent.core.services.field_data import VectorFieldDataRequest
  >>> velocity_request = VectorFieldDataRequest(field_name="velocity", surfaces=["inlet", "inlet1"])
  >>> velocity_vector_data = field_data.get_field_data(velocity_request)
  # Shape: (262, 3) - Velocity vectors for 262 faces, each with components (vx, vy, vz) for 'inlet'.
  >>> velocity_vector_data["inlet"].shape
  (262, 3)
  # Shape: (265, 3) - Velocity vectors for 265 faces, each with components (vx, vy, vz) for 'inlet1'.
  >>> velocity_vector_data["inlet1"].shape
  (265, 3)

Get pathlines field data
~~~~~~~~~~~~~~~~~~~~~~~~
To obtain pathlines field data, use ``PathlinesFieldDataRequest``:

.. code-block:: python

  >>> from ansys.fluent.core.services.field_data import PathlinesFieldDataRequest
  >>> velocity_pathlines_request = PathlinesFieldDataRequest(field_name="x-velocity", surfaces=["inlet"])
  >>> velocity_path_lines_data = field_data.get_field_data(velocity_pathlines_request)

  # Vertices shape: (29565, 3) - 29565 pathline points, each with coordinates (x, y, z).
  # Lines: A list where each entry contains indices of vertices forming a pathline.
  # Velocity shape: (29565,) - Scalar velocity values at each pathline point.
  >>> velocity_path_lines_data["inlet"].vertices.shape
  (29565, 3)
  >>> len(velocity_path_lines_data["inlet"].lines)
  29303
  >>> velocity_path_lines_data["inlet"].scalar_field.shape
  (29565,)
  >>> velocity_path_lines_data["inlet"].lines[100]
  # Example: Pathline 101 connects vertices 100 and 101.
  array([100, 101])

Making multiple requests in a single transaction
------------------------------------------------
To retrieve multiple field data types in a single transaction, create a transaction object:

.. code-block:: python

  >>> transaction = solver.fields.field_data.new_transaction()
  # This creates a new transaction object for batching multiple requests.

Add multiple requests using ``add_requests`` and access the data with ``get_response``:

.. code-block:: python

  >>> vertices_and_centroid_request = SurfaceFieldDataRequest(surfaces=[1], data_types=[SurfaceDataType.Vertices, SurfaceDataType.FacesCentroid])
  >>> pressure_request = ScalarFieldDataRequest(surfaces=[1, 2], field_name="pressure", node_value=True, boundary_value=True)
  >>> velocity_request = VectorFieldDataRequest(surfaces=[1, 2], field_name="velocity")

  >>> payload_data = transaction.add_requests(vertices_and_centroid_request, pressure_request, velocity_request).get_response()

Retrieve data using ``get_field_data``, either by reusing or modifying request objects:

.. code-block:: python

  >>> pressure_data = payload_data.get_field_data(pressure_request)
  >>> pressure_data.keys()
  dict_keys([1, 2])
  >>> pressure_request = pressure_request._replace(surfaces=[1])
  >>> update_pressure_data = payload_data.get_field_data(pressure_request)
  >>> update_pressure_data.keys()
  dict_keys([1])

.. note::
  ``PathlinesFieldDataRequest`` allows only one unique ``field_name`` per transaction.

Allowed values
--------------
Additionally there is an ``allowed_values`` method provided on all of
``field_name``, ``surface_name`` and ``surface_ids`` which tells you what object
names are accessible.

Some sample use cases are demonstrated below:

.. code-block:: python

  >>> field_data.get_scalar_field_data.field_name.allowed_values()
  ['abs-angular-coordinate', 'absolute-pressure', 'angular-coordinate',
  'anisotropic-adaption-cells', 'aspect-ratio', 'axial-coordinate', 'axial-velocity',
  'boundary-cell-dist', 'boundary-layer-cells', 'boundary-normal-dist', ...]

  >>> transaction = field_data.new_transaction()
  >>> transaction.add_scalar_fields_request.field_name.allowed_values()
  ['abs-angular-coordinate', 'absolute-pressure', 'angular-coordinate',
  'anisotropic-adaption-cells', 'aspect-ratio', 'axial-coordinate', 'axial-velocity',
  'boundary-cell-dist', 'boundary-layer-cells', 'boundary-normal-dist', ...]

  >>> field_data.get_scalar_field_data.surface_name.allowed_values()
  ['in1', 'in2', 'in3', 'inlet', 'inlet1', 'inlet2', 'out1', 'outlet', 'solid_up:1', 'solid_up:1:830', 'solid_up:1:830-shadow']

  >>> field_data.get_surface_data.surface_ids.allowed_values()
  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


Field data streaming
--------------------

PyFluent's field data streaming service allows you to dynamically observe changes
in field data by tracking its values in real time. You can integrate PyFluent's
field data streaming callback mechanism with visualization
tools from the Python ecosystem, making it easy to visualize the data of interest.

.. note::
   In **Meshing mode**, only 'field_data_streaming' provides a valid interface as of now.
   Other methods currently return an empty array when used in Meshing mode.

   The 'field_data_streaming' is available only for the **Meshing mode**.

The following example demonstrates how to update mesh data in **Meshing mode**
using the field data streaming mechanism:

.. code-block:: python

  >>> import ansys.fluent.core as pyfluent
  >>> from ansys.fluent.core import examples

  >>> # Download example geometry file
  >>> import_file_name = examples.download_file(
  >>>     "mixing_elbow.pmdb", "pyfluent/mixing_elbow"
  >>> )

  >>> # Launch Fluent in Meshing mode
  >>> meshing = pyfluent.launch_fluent(mode=pyfluent.FluentMode.MESHING)

  >>> # Dictionary to store mesh data
  >>> mesh_data = {}

  >>> # Define a callback function to process streamed field data
  >>> def plot_mesh(index, field_name, data):
  >>>     if data is not None:
  >>>         if index in mesh_data:
  >>>             mesh_data[index].update({field_name: data})
  >>>         else:
  >>>             mesh_data[index] = {field_name: data}

  >>> # Register the callback function
  >>> meshing.fields.field_data_streaming.register_callback(plot_mesh)

  >>> # Start field data streaming with byte stream and chunk size
  >>> meshing.fields.field_data_streaming.start(provideBytesStream=True, chunkSize=1024)

  >>> # Initialize the Meshing workflow
  >>> meshing.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")

  >>> # Import the geometry into the workflow
  >>> meshing.workflow.TaskObject["Import Geometry"].Arguments = {
  >>>    "FileName": import_file_name,
  >>>    "LengthUnit": "in",
  >>> }

  >>> meshing.workflow.TaskObject["Import Geometry"].Execute()
