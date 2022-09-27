.. _ref_field_data:

Field data
==========

You can use field data objects to access Fluent surface field data, both 
scalar and vector.

Accessing field data objects
----------------------------

Launch the Fluent solver, e.g.:

.. code-block:: python

  >>> import ansys.fluent.core as pyfluent
  >>> solver = pyfluent.launch_fluent(mode="solver")
  >>> solver.file.read(file_type="case", file_name=case_path)
  >>> solver.solution.initialization.hybrid_initialize()
  >>> solver.solution.run_calculation.iterate()


The field data object is an attribute of the solver object:

.. code-block:: python

  >>> field_data = solver.field_data


Simple requests
---------------

Request surface vertices. Each key in the returned dictionary is a surface ID, 
and each value holds the corresponding vertices in a numpy array:

.. code-block:: python

  >>> from ansys.fluent.core.services.field_data import SurfaceDataType

  >>> field_data.get_surface_data(surface_name="wall-elbow", data_type=SurfaceDataType.Vertices)
  {0: array([ 0.1509247 , -0.1312225 ,  0.        , ..., -0.00996254,
      -0.10107055,  0.00970755], dtype=float32)}


Make a similar request for surface face normals:

.. code-block:: python

  >>> field_data.get_surface_data(surface_name="wall-elbow", data_type=SurfaceDataType.FacesNormal)
  {0: array([ 1.3146671e-06, -1.1612752e-06,  5.7278072e-08, ...,
       -2.6233408e-08,  1.6844007e-05,  1.0690871e-06], dtype=float32)}


For the same surface, request temperature field data:

.. code-block:: python

  >>> field_data.get_scalar_field_data(surface_name="wall-elbow", field_name="temperature")
  {0: array([0., 0., 0., ..., 0., 0., 0.], dtype=float32)}


Request velocity field data:

.. code-block:: python

  >>> field_data.get_vector_field_data(surface_name="wall-elbow", vector_field="velocity")
  {0: (array([0., 0., 0., ..., 0., 0., 0.], dtype=float32), 1.0)}


THe above example employs a separate method for requesting each type of field:

- ``get_surface_data`` for surface data.
- ``get_scalar_field_data`` for scalar field data.
- ``get_vector_field_data`` for vector field data.

For a surface or scalar field request, the response contains a dictoinary of surface IDs to numpy array of 
the requested field. 

``surface_id [int] -> field[numpy.array]``
  
For a vector field request, the response is a dictionary of surface IDs to a tuple containing a
numpy array of ``vector field`` and ``vector-scale``. 

``surface_id [int] -> (vector field [numpy.array],  vector-scale [float])``

.. note:: 
   In Fluent, you can associate a surface name with multiple surface IDs.
   Thus, a response can contain a surface ID as a key of the returned dictionary. 


Making multiple requests in a single transaction
------------------------------------------------

Add some field data requests

.. code-block::

  >>> field_data.add_get_surfaces_request(surface_ids=[1], provide_vertices=True, 
                                        provide_faces=False, provide_faces_centroid=True
                                       )

  >>> field_data.add_get_surfaces_request(surface_ids=[2], provide_vertices=True, 
                                       provide_faces=True
                                       )

  >>> field_data.add_get_scalar_fields_request(surface_ids=[1,2], field_name="temperature",
                                            node_value=True, boundary_value=True
                                            )


Temperature data for the following request will be returned in tag_id 4.

.. code-block::

  >>> field_data.add_get_scalar_fields_request(surface_ids=[3], field_name="temperature",
                                             node_value=True, boundary_value=False
                                             )


Pressure data for the following request will be returned in tag_id 2. 

.. code-block::

  >>> field_data.add_get_scalar_fields_request(surface_ids=[1,4], field_name="pressure",
                                            node_value=False, boundary_value=False
                                            )


Make the query to get the data for all these requests. ``payload_data`` is a dictionary with 
the following order (see below to find out about ``tag id``s):
  `tag_id [int]-> surface_id [int] -> field_name [str] -> field_data [numpy.array]`

.. code-block::

>>> payload_data = field_data.get_fields()


Building requests for multiple data
-----------------------------------
In the above examples, you can get data for multiple fields in a single request
and see the data for all of these fields in a single response.

**Request**

The ``add_get_<items>_request`` methods combine requests for multiple fields in a single request: 

- ``add_get_surfaces_request`` adds a surfaces request.
- ``add_get_scalar_fields_request`` adds a scalar fields request.
- ``add_get_vector_fields_request`` adds a vector fields request. 

**Response**
The ``get_fields`` method returns all requested fields in a single response. It provides 
a dictionary containing the requested fields as a numpy array in the following order:

``tag_id [int]-> surface_id [int] -> field_name [str] -> field_data[numpy.array]``


Tag ID
------ 
A tag ID is generated by applying ```bitwise or``` on all tags for a request. Here is a list
of supported tags and their values:   
 
*  OVERSET_MESH: 1,
*  ELEMENT_LOCATION: 2,
*  NODE_LOCATION: 4,
*  BOUNDARY_VALUES: 8,

For example, if you request the scalar field data for element location[2], in the
dictionary,  ``tag_id`` is ``2``. Similarly, if you request the boundary values[8] for 
node location[4], ``tag_id`` is ``(4|8)``, or 12.

Surface ID
----------
The surface ID is the same one that is passed in the request.

Field name
----------
A request returns multiple fields. The number of fields depends on the request type.

Surface request 
~~~~~~~~~~~~~~~
The response to a surface request contains any of the following fields, depending on the
request arguments:

- ``faces``, which contain face connectivity    
- ``vertices``, which contain node coordinates
- ``centroid``, which contains face centroids    
- ``face-normal``, which contains face normals


Scalar field request
~~~~~~~~~~~~~~~~~~~~
The response to a scalar field request contains a single field with the same name as the
scalar field name passed in the request.

Vector field request
~~~~~~~~~~~~~~~~~~~~
The response to a vector field request contains two fields:

- ``vector field``, with the same name as the vector field name that is passed in the request 
- ``vector-scale``, a float value indicating the vector scale.


.. currentmodule:: ansys.fluent.core.services

.. autosummary::
   :toctree: _autosummary


.. automethod:: ansys.fluent.core.services.field_data.FieldData.add_get_surfaces_request
.. automethod:: ansys.fluent.core.services.field_data.FieldData.add_get_scalar_fields_request
.. automethod:: ansys.fluent.core.services.field_data.FieldData.add_get_vector_fields_request
.. automethod:: ansys.fluent.core.services.field_data.FieldData.get_fields

.. automethod:: ansys.fluent.core.services.field_data.FieldData.get_surface_data
.. automethod:: ansys.fluent.core.services.field_data.FieldData.get_scalar_field_data
.. automethod:: ansys.fluent.core.services.field_data.FieldData.get_vector_field_data
