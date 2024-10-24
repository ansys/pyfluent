.. _ref_field_data_guide:

.. vale Google.Spacing = NO

Field data
==========

You can use field data objects to access Fluent surface, scalar, vector, and
pathlines data.

Accessing field data objects
----------------------------

In order to access field data, launch the fluent solver, and make field data
available (for example, either by reading a case file and then initializing as in the following code, or
by reading case and data files).

.. code-block:: python

  >>> import ansys.fluent.core as pyfluent
  >>> from ansys.fluent.core import examples
  >>> import_file_name = examples.download_file("mixing_elbow.msh.h5", "pyfluent/mixing_elbow")
  >>> solver = pyfluent.launch_fluent(mode=pyfluent.FluentMode.SOLVER)
  >>> solver.settings.file.read(file_type="case", file_name=import_file_name)
  >>> solver.settings.solution.initialization.hybrid_initialize()

The field data object is an attribute of the :obj:`~ansys.fluent.core.session_solver.Solver` object:

.. code-block:: python

  >>> field_data = solver.fields.field_data


Simple requests
---------------

Here are the methods for requesting each type of field:

- ``get_surface_data`` for surface data.
- ``get_scalar_field_data`` for scalar field data.
- ``get_vector_field_data`` for vector field data
- ``get_pathlines_field_data`` for vector field data

Get surface data
~~~~~~~~~~~~~~~~
You can request surface vertices for a given surface name by calling
the ``get_surface_data`` method and specifying ``Vertices`` for ``data_types``.

.. code-block:: python

  >>> from ansys.fluent.core.services.field_data import SurfaceDataType

  >>> vertices_data = field_data.get_surface_data(surfaces=["cold-inlet"], data_types=[SurfaceDataType.Vertices])
  >>> vertices_data["cold-inlet"][SurfaceDataType.Vertices].shape
  (241, 3)
  >>> vertices_data["cold-inlet"][SurfaceDataType.Vertices][5]
  array([-0.2       , -0.10167995,  0.00362008], dtype=float32)

You can call the same method to get the corresponding surface face normals and centroids.
For ``data_types``, specifying ``FacesNormal`` and ``FacesCentroid`` respectively.

.. code-block:: python

  >>> faces_normal_and_centroid_data = field_data.get_surface_data(
  >>>     data_types=[SurfaceDataType.FacesNormal, SurfaceDataType.FacesCentroid], surfaces=["cold-inlet"]
  >>> )

  >>> faces_normal_and_centroid_data["cold-inlet"][SurfaceDataType.FacesNormal].shape
  (152, 3)
  >>> faces_normal_and_centroid_data["cold-inlet"][SurfaceDataType.FacesCentroid][15]
  array([-0.2       , -0.11418786,  0.03345207], dtype=float32)

You can request face connectivity data for given ``surfaces`` by calling
the ``get_surface_data`` method and specifying ``FacesConnectivity`` for ``data_types``.

.. code-block:: python

  >>> faces_connectivity_data = field_data.get_surface_data(
  >>>     data_types=[SurfaceDataType.FacesConnectivity], surfaces=["cold-inlet"]
  >>> )
  >>> faces_connectivity_data["cold-inlet"][SurfaceDataType.FacesConnectivity][5]
  array([12, 13, 17, 16])


If a single surface is provided as input, the response contains face vertices, connectivity data, and normal or centroid data.
If multiple surfaces are provided as input, the response is a dictionary containing a map of surface IDs to face
vertices, connectivity data, and normal or centroid data.

Get scalar field data
~~~~~~~~~~~~~~~~~~~~~
You can call the ``get_scalar_field_data`` method to get scalar field data, such as absolute pressure:

.. code-block:: python

  >>> abs_press_data = field_data.get_scalar_field_data(field_name="absolute-pressure", surfaces=["cold-inlet"])
  >>> abs_press_data["cold-inlet"].shape
  (241,)
  >>> abs_press_data["cold-inlet"][120]
  101325.0

If a single surface is provided as input, scalar field data is returned.
If multiple surfaces are provided as input, a dictionary containing a map of surface IDs to scalar field data is returned.

Get vector field data
~~~~~~~~~~~~~~~~~~~~~
You can call the ``get_vector_field_data`` method to get vector field data.

.. code-block:: python

  >>> velocity_vector_data = field_data.get_vector_field_data(field_name="velocity", surfaces=["cold-inlet"])
  >>> velocity_vector_data["cold-inlet"].shape
  (152, 3)

If a single surface is provided as input, vector field data is returned.
If multiple surfaces are provided as input, a dictionary containing a map of surface IDs to vector field data is returned.

Get pathlines field data
~~~~~~~~~~~~~~~~~~~~~~~~
You can call the ``get_pathlines_field_data`` method to get pathlines field data.

.. code-block:: python

  >>> path_lines_data = field_data.get_pathlines_field_data(field_name="velocity", surfaces=["cold-inlet"])
  >>> path_lines_data["cold-inlet"]["vertices"].shape
  (76152, 3)
  >>> len(path_lines_data["cold-inlet"]["lines"])
  76000
  >>> path_lines_data["cold-inlet"]["velocity"].shape
  (76152, )
  >>> path_lines_data["cold-inlet"]["lines"][100]
  array([100, 101])

Dictionary containing a map of surface IDs to the path-line data is returned.
For example, pathlines connectivity, vertices, and field.


.. note::
   In Fluent, a surface name can be associated with multiple surface IDs.
   Thus, a response contains a surface ID as a key of the returned dictionary.


Making multiple requests in a single transaction
------------------------------------------------
You can get data for multiple fields in a single transaction.

First create transaction object for field data.

.. code-block:: python

  >>> transaction = solver.fields.field_data.new_transaction()

Then combine requests for multiple fields using ``add_<items>_request`` methods in a single transaction:

- ``add_surfaces_request`` adds a surfaces request.
- ``add_scalar_fields_request`` adds a scalar fields request.
- ``add_vector_fields_request`` adds a vector fields request.
- ``add_pathlines_fields_request`` adds a pathlines fields request.

Following code demonstrate adding multiple requests to a single transaction.

.. code-block::

  >>> transaction.add_surfaces_request(
  >>>     surfaces=[1], data_types = [SurfaceDataType.Vertices, SurfaceDataType.FacesCentroid],
  >>> )
  >>> transaction.add_surfaces_request(
  >>>     surfaces=[2], data_types = [SurfaceDataType.Vertices, SurfaceDataType.FacesConnectivity],
  >>> )
  >>> transaction.add_scalar_fields_request(
  >>>     surfaces=[1,2], field_name="pressure", node_value=True, boundary_value=True
  >>> )
  >>> transaction.add_vector_fields_request(surfaces=[1,2], field_name="velocity")
  >>> transaction.add_pathlines_fields_request(surfaces=[1,2], field_name="temperature")


You can call the ``get_fields`` method to get the data for all these requests. This call also
clears all requests, so that subsequent calls to the ``get_fields`` method yield nothing until
more requests are added.

.. code-block::

  >>> payload_data = transaction.get_fields()

``payload_data`` is a dictionary containing the requested fields as a numpy array in the following order:

``tag -> surface_id [int] -> field_name [str] -> field_data[np.array]``


Tag
---

Fluent versions earlier than 2023 R1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A tag is int, generated by applying ``bitwise or`` on all tags for a request. Here is a list
of supported tags and their values:

*  OVERSET_MESH: 1,
*  ELEMENT_LOCATION: 2,
*  NODE_LOCATION: 4,
*  BOUNDARY_VALUES: 8,

For example, if you request the scalar field data for element location[2], in the
dictionary, ``tag`` is ``2``. Similarly, if you request the boundary values[8] for
node location[4], ``tag`` is ``(4|8)`` or 12.

Fluent versions 2023 R1 and later
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A tag is tuple of input, value pairs for which field data is generated.

For example, if you request the scalar field data for element location, in the
dictionary, ``tag`` is ``(('type','scalar-field'), ('dataLocation', 1), ('boundaryValues',False))``.
Similarly, if you request the boundary values for node location, ``tag`` is
``(('type','scalar-field'), ('dataLocation', 0), ('boundaryValues',True)``.

Surface ID
----------
The surface ID is the same one that is passed in the request.

Field name
----------
A request returns multiple fields. The number of fields depends on the request
type.

Surface request
~~~~~~~~~~~~~~~
The response to a surface request contains any of the following fields,
depending on the request arguments:

- ``faces``, which contain face connectivity
- ``vertices``, which contain node coordinates
- ``centroid``, which contains face centroids
- ``face-normal``, which contains face normals


Scalar field request
~~~~~~~~~~~~~~~~~~~~
The response to a scalar field request contains a single field with the same
name as the scalar field name passed in the request.

Vector field request
~~~~~~~~~~~~~~~~~~~~
The response to a vector field request contains two fields:

- ``vector field``, with the same name as the vector field name that is passed
 in the request
- ``vector-scale``, a float value indicating the vector scale.

Pathlines field request
~~~~~~~~~~~~~~~~~~~~~~~
The response to a pathlines field request contains the following fields:

- ``pathlines-count``, which contains pathlines count.
- ``lines``, which contain pathlines connectivity.
- ``vertices``, which contain node coordinates.
- ``field name``, which contains pathlines field. field name is the same name as
  the scalar field name passed in the request.
- ``particle-time``, which contains particle time, if requested.
- ``additional field name``, which contains additional field, if requested.
  additional field name is the same name as the additional field name passed in
  the request.

Allowed values
--------------
Additionally there is an ``allowed_values`` method provided on all of
``field_name``, ``surface_name`` and ``surface_ids`` which tells you what object
names are accessible.

Some sample use cases are demonstrated below:

.. code-block:: python

  >>> field_data.get_scalar_field_data.field_name.allowed_values()
  ['abs-angular-coordinate', 'absolute-pressure', 'angular-coordinate',
  'anisotropic-adaption-cells', 'axial-coordinate', 'axial-velocity',
  'boundary-cell-dist', 'boundary-layer-cells', 'boundary-normal-dist', ...]

  >>> transaction = field_data.new_transaction()
  >>> transaction.add_scalar_fields_request.field_name.allowed_values()
  ['abs-angular-coordinate', 'absolute-pressure', 'angular-coordinate',
  'anisotropic-adaption-cells', 'axial-coordinate', 'axial-velocity',
  'boundary-cell-dist', 'boundary-layer-cells', 'boundary-normal-dist', ...]

  >>> field_data.get_scalar_field_data.surface_name.allowed_values()
  ['cold-inlet', 'hot-inlet', 'outlet', 'symmetry-xyplane', 'wall-elbow', 'wall-inlet']

  >>> field_data.get_surface_data.surface_ids.allowed_values()
  [0, 1, 2, 3, 4, 5]
