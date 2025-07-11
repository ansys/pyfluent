.. _ref_field_info_guide:

.. vale Google.Spacing = NO

Field info
==========

You can use field information objects to access field-related metadata from Fluent.

Accessing field information objects
-----------------------------------

.. code:: python

  >>> from ansys.fluent.core.examples.downloads import download_file
  >>> mixing_elbow_case_path = download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")

  >>> import ansys.fluent.core as pyfluent
  >>> solver_session = pyfluent.launch_fluent()
  >>> solver_session.settings.file.read(file_type="case", file_name=mixing_elbow_case_path)
  >>> solver_session.settings.solution.initialization.hybrid_initialize()


The field information object is available as an attribute of the :obj:`~ansys.fluent.core.session_solver_session.Solver` object:

.. code-block:: python

  >>> field_info = solver_session.fields.field_info

Available methods
-----------------

You can use the following methods to retrieve various types of field metadata:

- ``get_scalar_fields_info`` - Returns information about scalar fields.
- ``get_scalar_field_range`` - Returns the minimum and maximum values for a given scalar field.
- ``get_vector_fields_info`` - Returns information about vector fields.
- ``get_surfaces_info`` - Returns information about available surfaces.

Scalar field information
~~~~~~~~~~~~~~~~~~~~~~~~
To retrieve details about scalar fields (such as field name, domain, and section),
use the ``get_scalar_fields_info`` method:

.. code-block:: python

  >>> field_info.get_scalar_fields_info()
  {'pressure': {'display_name': 'Static Pressure', 'section': 'Pressure...', 'domain': 'mixture'},
   'pressure-coefficient': {'display_name': 'Pressure Coefficient', 'section': 'Pressure...', 'domain': 'mixture'},
   'dynamic-pressure': {'display_name': 'Dynamic Pressure', 'section': 'Pressure...', 'domain': 'mixture'},
   'absolute-pressure': {'display_name': 'Absolute Pressure', 'section': 'Pressure...', 'domain': 'mixture'},
    ...}

Scalar field range
~~~~~~~~~~~~~~~~~~
To get the range (minimum and maximum values) of a specific scalar field, use the ``get_scalar_field_range`` method.
The field name must be one of the keys returned by the ``get_scalar_fields_info`` method.

.. code-block:: python

  >>> field_info.get_scalar_field_range("cell-weight")
  [8.0, 24.0]

Vector field information
~~~~~~~~~~~~~~~~~~~~~~~~~
To retrieve metadata about vector fields, use the ``get_vector_fields_info`` method:

.. code-block:: python

  >>> field_info.get_vector_fields_info()
  {'velocity': {'x-component': 'x-velocity', 'y-component': 'y-velocity', 'z-component': 'z-velocity'},
   'relative-velocity': {'x-component': 'relative-x-velocity', 'y-component': 'relative-y-velocity', 'z-component': 'relative-z-velocity'}}

Get surface information
~~~~~~~~~~~~~~~~~~~~~~~
To get information about available surfaces (including surface ID, zone ID, and zone type),
use the ``get_surfaces_info`` method:
.. code-block:: python

  >>> field_info.get_surfaces_info()
  {'symmetry-xyplane': {'surface_id': [5], 'zone_id': 29, 'zone_type': 'symmetry', 'type': 'zone-surf'},
   'hot-inlet': {'surface_id': [4], 'zone_id': 30, 'zone_type': 'velocity-inlet', 'type': 'zone-surf'},
   'cold-inlet': {'surface_id': [3], 'zone_id': 31, 'zone_type': 'velocity-inlet', 'type': 'zone-surf'},
   'outlet': {'surface_id': [2], 'zone_id': 32, 'zone_type': 'pressure-outlet', 'type': 'zone-surf'},
   'wall-inlet': {'surface_id': [1], 'zone_id': 33, 'zone_type': 'wall', 'type': 'zone-surf'},
   'wall-elbow': {'surface_id': [0], 'zone_id': 34, 'zone_type': 'wall', 'type': 'zone-surf'}}


