.. _ref_solution_variable_data_guide:

Solution variable data
======================

A solution variable is an array variable that holds the data for a particular
solved field (such as pressure or velocity). You can use solution_variable_info
and solution_variable_data objects to access Fluent solution variable info and data respectively.

Accessing solution variable objects
-----------------------------------

Launch the fluent solver, and make solution variable objects available 
(for example, by reading case and data files):

.. code-block:: python

  >>> import ansys.fluent.core as pyfluent
  >>> from ansys.fluent.core import examples
  >>> from ansys.units import VariableCatalog
  >>> import_file_name = examples.download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
  >>> examples.download_file("mixing_elbow.dat.h5", "pyfluent/mixing_elbow")
  >>> solver_session = pyfluent.launch_fluent()
  >>> solver_session.settings.file.read_case_data(file_name=import_file_name)


The ``solution_variable_info`` and ``solution_variable_data`` objects are attributes of the ``solver_session.fields`` object:

.. code-block:: python

  >>> solution_variable_info = solver_session.fields.solution_variable_info
  >>> solution_variable_data = solver_session.fields.solution_variable_data


Solution variable info
----------------------
Solution variable metadata information can be accessed via the following solution_variable_info methods:

- ``get_zones_info`` for zone information.
- ``get_variables_info`` for solution variable information.

Get zone information
~~~~~~~~~~~~~~~~~~~~
You can access zone information by calling the ``get_zones_info`` method.

.. code-block:: python
  
  >>> zones_info = solution_variable_info.get_zones_info()
  >>> zones_info.domains
  ['mixture']  
  >>>
  >>> zones_info.zone_names
  ['symmetry-xyplane', 'hot-inlet', 'cold-inlet', 'outlet', 'wall-inlet', 'wall-elbow', 'elbow-fluid', 'interior--elbow-fluid']
  >>>
  >>> zone_info = zones_info['wall-inlet']
  >>>
  >>> zone_info
  name:wall-inlet count: 268 zone_id:33 zone_type:wall threadType:Face 0. 268[2169:2436]
  >>>
  >>> zone_info.name 
  'wall-inlet'   
  >>>
  >>> zone_info.count 
  268 
  >>>
  >>> zone_info.zone_id 
  33
  >>>
  >>> zone_info.zone_type 
  'wall'  
  
Get solution variable information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You can request solution variables information for a given ``domain_name`` and list of ``zone_names``
by calling the ``get_variables_info`` method.

.. code-block:: python

  >>> wall_fluid_info = solution_variable_info.get_variables_info(zone_names=["wall-elbow", "elbow-fluid"], domain_name="mixture")
  >>>
  >>> wall_fluid_info.solution_variables
  ['SV_ADS_0', 'SV_ADS_1', 'SV_CENTROID', 'SV_H', 'SV_K', 'SV_O', 'SV_P', 'SV_T', 'SV_U', 'SV_V', 'SV_W']
  >>>
  >>> solution_variable_info_centroid = wall_fluid_info["SV_CENTROID"]
  >>>
  >>> solution_variable_info_centroid
  name:SV_CENTROID dimension:3 field_type:<class 'numpy.float64'>
  >>>
  >>> solution_variable_info_centroid.name 
  'SV_CENTROID'
  >>>
  >>> solution_variable_info_centroid.dimension 
  3
  >>>
  >>> solution_variable_info_centroid.field_type 
  <class 'numpy.float64'> 
  
Solution variable data
----------------------
solution variable data can be extracted and modified via the following solution_variable_data methods:

- ``get_data`` to get solution variable data.
- ``set_data`` to set solution variable data.


Get solution variable data
~~~~~~~~~~~~~~~~~~~~~~~~~~
You can request solution variable data for a given ``domain_name`` and multiple ``zone_names`` by calling
the ``get_data`` method and passing the particular ``variable_name``.

.. code-block:: python
  
    >>> sv_p_wall_fluid = solution_variable_data.get_data(variable_name=VariableCatalog.PRESSURE, zone_names=["elbow-fluid", "wall-elbow"], domain_name="mixture")
    >>>
    >>> sv_p_wall_fluid.domain
    'mixture'
    >>>
    >>> sv_p_wall_fluid.zone_names
    ['wall-elbow', 'elbow-fluid']
    >>>
    >>> fluid_press = sv_p_wall_fluid["elbow-fluid"]
    >>>
    >>> fluid_press.size
    17822
    >>>
    >>> fluid_press.dtype
    'float64'
    >>>
    >>> fluid_press
    array([0.01635187, 0.35772967, 0.40971006, ..., 0.40919935, 0.39503292, 0.41322547], shape=(17822,))
  
Set solution variable data
~~~~~~~~~~~~~~~~~~~~~~~~~~
You can set solution variable data for a given ``domain_name`` by calling the ``set_data``
method and passing required ``variable_name`` and dictionary of ``zone_name``
to NumPy array of ``solution_variable_data``

Additionally solution_variable_data object also supports ``create_empty_array`` method. This method can be used to 
generate ``numpy zeros array`` for a given ``domain_name``, ``zone_name`` and 
``variable_name``. This array can be populated and passed to ``set_data``.

.. code-block:: python
  
    >>> wall_press_array = solution_variable_data.create_empty_array(VariableCatalog.PRESSURE, "wall-elbow", "mixture")
    >>> fluid_press_array = solution_variable_data.create_empty_array(VariableCatalog.PRESSURE, "elbow-fluid", "mixture")
    >>> wall_press_array[:] = 500
    >>> fluid_press_array[:] = 600
    >>> zone_names_to_solution_variable_data = {"wall-elbow": wall_press_array, "elbow-fluid": fluid_press_array}
    >>> solution_variable_data.set_data(variable_name=VariableCatalog.PRESSURE, zone_names_to_data=zone_names_to_solution_variable_data, domain_name="mixture")
