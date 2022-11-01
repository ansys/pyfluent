.. _ref_field_data:

Field data
==========

You can use field data objects to access Fluent surface, scalar, vector, and pathlines data.

Accessing field data objects
----------------------------

In order to access field data, launch the fluent solver, and make field
data available (for example, by reading case and data files):

.. code-block:: python

  >>> import ansys.fluent.core as pyfluent
  >>> solver = pyfluent.launch_fluent(mode="solver")
  >>> solver.file.read(file_type="case-dats", file_name=mixing_elbow_case_path)


The field data object is an attribute of the solver object:

.. code-block:: python

  >>> field_data = solver.field_data


Simple requests
---------------

Here are the methods for requesting each type of field:

- ``get_surface_data`` for surface data.
- ``get_scalar_field_data`` for scalar field data.
- ``get_vector_field_data`` for vector field data
- ``get_pathlines_field_data`` for vector field data

Get surface data
~~~~~~~~~~~~~~~~
You can request surface vertices for a given ``surface_name`` by calling
the ``get_surface_data`` method and specifying ``Vertices`` for ``data_type``.

.. code-block:: python

  >>> from ansys.fluent.core.services.field_data import SurfaceDataType

  >>> field_data.get_surface_data(surface_name="inlet", data_type=SurfaceDataType.Vertices)
  {4: array([-0.34760258,  0.        , -0.04240644, ..., -0.2953132 ,
        0.        , -0.06207064], dtype=float32)}


You can call the same method to get the corresponding surface face connectivity, normals, and centroids
by specifying ``FacesConnectivity``, ``FacesNormal`` and ``FacesCentroid`` respectively for ``data_type``.

.. code-block:: python

  >>> field_data.get_surface_data(surface_name="inlet", data_type=SurfaceDataType.FacesConnectivity)
  {4: array([  4,   3,   2, ..., 379, 382, 388])}

  >>> field_data.get_surface_data(surface_name="inlet", data_type=SurfaceDataType.FacesNormal)
  {4: array([ 0.0000000e+00,  2.5835081e-06,  ...,
          2.7459005e-06,  0.0000000e+00,  0.0000000e+00,  3.0340884e-06], dtype=float32)}
  
  >>> field_data.get_surface_data(surface_name="inlet", data_type=SurfaceDataType.FacesCentroid)
  {4: array([-0.34724122,  0.        , -0.0442204 , -0.34724477, ...,
         -0.04050309, -0.34645557,  0.        , -0.04421487, -0.34646705], dtype=float32)}
       
Response contains a dictionary of surface IDs to numpy array of the requested field. 

Get scalar field data
~~~~~~~~~~~~~~~~~~~~~
You can call the ``get_scalar_field_data`` method to get scalar field data, such as temperature:

.. code-block:: python

  >>> field_data.get_scalar_field_data(surface_name="inlet", field_name="temperature")
  {4: array([922.6778 , 923.7954 , 923.791  , 922.67017, 922.88135,  ...,
         924.94556, 924.9451 , 924.9536 , 923.87366, 922.8334 , 922.82434], dtype=float32)}
         
The response contains a dictionary of surface IDs to a numpy array of the requested field.          

Get vector field data
~~~~~~~~~~~~~~~~~~~~~
You can call the ``get_vector_field_data`` method to get vector field data. 

.. code-block:: python

  >>> field_data.get_vector_field_data(surface_name="inlet", vector_field="velocity")
  {4: (array([ 5.81938386e-01, -1.01187916e+01,  3.14891455e-03,  ...,
        -6.49216697e-02,  1.44923580e+00, -1.04387817e+01], dtype=float32), 0.00012235096)}
  
Response is a dictionary of surface IDs to a tuple containing a numpy array of ``vector field`` and ``vector-scale``. 

Get pathlines field data
~~~~~~~~~~~~~~~~~~~~~~~~  
You can call the ``get_pathlines_field_data`` method to get pathlines field data. 

.. code-block:: python

  >>> field_data.get_pathlines_field_data(surface_name="inlet", field_name="temperature")
  {4: {'faces': array([    2,     0,     1, ...,     2, 28828, 28829]), 'vertices': array([-0.34724122,  0.        , -0.0442204 , ..., -0.19877256,
         -0.1250188 , -0.0621446 ], dtype=float32), 'temperature': array([879.25073, 828.8636 , 861.65686, ..., 892.1276 , 894.6389 ,
         897.95325], dtype=float32)}}

Pathlines data is returned as line surface. So response is a dictionary of surface IDs to a information about line surface. 


.. note:: 
   In Fluent, a surface name can be associated with multiple surface IDs.
   Thus, a response contain a surface ID as a key of the returned dictionary. 


Making multiple requests in a single transaction
------------------------------------------------
You can get data for multiple fields in a single transaction.

First create transaction object for field data.

.. code-block:: python

  >>> transaction = solver.field_data.new_transaction()

Then combine requests for multiple fields using ``add_<items>_request`` methods in a single transaction: 

- ``add_surfaces_request`` adds a surfaces request.
- ``add_scalar_fields_request`` adds a scalar fields request.
- ``add_vector_fields_request`` adds a vector fields request. 
- ``add_pathlines_fields_request`` adds a pathlines fields request.

Following code demonstrate adding multiple requests to a single transaction.

.. code-block::

>>> transaction.add_surfaces_request(surface_ids=[1], provide_vertices=True, 
                                        provide_faces=False, provide_faces_centroid=True
                                       )
>>> transaction.add_surfaces_request(surface_ids=[2], provide_vertices=True, 
                                       provide_faces=True
                                       )
>>> transaction.add_scalar_fields_request(surface_ids=[1,2], field_name="temperature",
                                            node_value=True, boundary_value=True
                                            )                                            
>>> transaction.add_vector_fields_request(surface_ids=[1,2])
>>> transaction.add_pathlines_fields_request(surface_ids=[1,2], field_name="temperature"                                           
                                            )                                            

                                            
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
dictionary,  ``tag`` is ``2``. Similarly, if you request the boundary values[8] for 
node location[4], ``tag`` is ``(4|8)`` or 12.

Fluent versions 2023 R1 and later
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A tag is tuple of input, value pairs for which field data is generated.

For example, if you request the scalar field data for element location, in the
dictionary,  ``tag`` is ``(('type','scalar-field'), ('dataLocation', 1), ('boundaryValues',False))``. 
Similarly, if you request the boundary values for node location, ``tag`` is 
``(('type','scalar-field'), ('dataLocation', 0), ('boundaryValues',True)``.

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
 
Pathlines field request
~~~~~~~~~~~~~~~~~~~~~~~
The response to a pathlines field request contains the following fields:

- ``pathlines-count``, pathlines count. 

For each pathline, the following fields are returned:

- ``pathlines-<pathlines-counter>-line-data``, pathlines connectivity.
- ``pathlines-<pathlines-counter>-position-data``, pathlines positions.
- ``pathlines-<pathlines-counter>-field-data``, pathlines field.
- ``pathlines-<pathlines-counter>-additional-field-data``, pathlines additional field if requested.
- ``pathlines-<pathlines-counter>-particle-time-field-data``, pathlines particle time if requested.


.. currentmodule:: ansys.fluent.core.services

.. autosummary::
   :toctree: _autosummary


.. automethod:: ansys.fluent.core.services.field_data.FieldTransaction.add_surfaces_request
.. automethod:: ansys.fluent.core.services.field_data.FieldTransaction.add_scalar_fields_request
.. automethod:: ansys.fluent.core.services.field_data.FieldTransaction.add_vector_fields_request
.. automethod:: ansys.fluent.core.services.field_data.FieldTransaction.add_pathlines_fields_request
.. automethod:: ansys.fluent.core.services.field_data.FieldTransaction.get_fields

.. automethod:: ansys.fluent.core.services.field_data.FieldData.get_surface_data
.. automethod:: ansys.fluent.core.services.field_data.FieldData.get_scalar_field_data
.. automethod:: ansys.fluent.core.services.field_data.FieldData.get_vector_field_data
.. automethod:: ansys.fluent.core.services.field_data.FieldData.get_pathlines_field_data