.. _ref_solution_variable_data:

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
  >>> import_filename = examples.download_file("mixing_elbow.msh.h5", "pyfluent/mixing_elbow")
  >>> solver = pyfluent.launch_fluent(mode="solver")
  >>> solver.file.read(file_type="case", file_name=import_filename)


The solution_variable_info and solution_variable_data objects are attributes of the solver object:

.. code-block:: python

  >>> solution_variable_info = solver.solution_variable_info
  >>> solution_variable_data = solver.solution_variable_data


Solution variable info
----------------------
Solution variable metadata information can be accessed via the following solution_variable_info methods:

- ``get_zones_info`` for zone information.
- ``get_solution_variables_info`` for solution variable information.

Get zone information
~~~~~~~~~~~~~~~~~~~~
You can access zone information by calling the ``get_zones_info`` method.

.. code-block:: python
  
  >>> zones_info = solution_variable_info.get_zones_info()
  >>> zones_info.domains
  ['mixture']  
  >>>
  >>> zones_info.zones
  ['fluid', 'wall', 'symmetry', 'pressure-outlet-7', 'velocity-inlet-6', 'velocity-inlet-5', 'default-interior']
  >>>
  >>> zone_info = zones_info['wall']
  >>>
  >>> zone_info
  name:wall count: 3630 zone_id:3 zone_type:wall thread_type:Face
  >>>
  >>> zone_info.name 
  'wall'   
  >>>
  >>> zone_info.count 
  3630 
  >>>
  >>> zone_info.zone_id 
  3
  >>>
  >>> zone_info.zone_type 
  'wall'  
  
Get solution variable information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You can request solution variables information for a given ``domain_name`` and list of ``zone_names``
by calling the ``get_solution_variables_info`` method.

.. code-block:: python

  >>> solution_variables_info_wall_fluid = solution_variable_info.get_solution_variables_info(zone_names=['wall' , "fluid"], domain_name="mixture")
  >>>
  >>> solution_variables_info_wall_fluid.solution_variables
  ['SV_CENTROID', 'SV_D', 'SV_H', 'SV_K', 'SV_P', 'SV_T', 'SV_U', 'SV_V', 'SV_W']
  >>>
  >>> solution_variable_info_centroid = solution_variables_info_wall_fluid['SV_CENTROID']
  >>>
  >>> solution_variable_info_centroid
  name:SV_CENTROID dimension:3 field_type:<class 'numpy.float64'>
  >>>
  >>>solution_variable_info_centroid.name 
  'SV_CENTROID'
  >>>
  >>>solution_variable_info_centroid.dimension 
  >>>3
  >>>
  >>>solution_variable_info_centroid.field_type 
  <class 'numpy.float64'> 
  
Solution variable data
----------------------
solution variable data can be extracted and modified via the following solution_variable_data object methods:

- ``get_solution_variable_data`` to get solution variable data.
- ``set_solution_variable_data`` to set solution variable data.


Get solution variable data
~~~~~~~~~~~~~~~~~~~~~~~~~~
You can request solution variable data for a given ``domain_name`` and multiple ``zone_names`` by calling
the ``get_solution_variable_data`` method and passing the particular ``solution_variable_name``.

.. code-block:: python
  
    >>> sv_t_wall_fluid= solution_variable_data.get_solution_variable_data(solution_variable_name="SV_T", zone_names=["fluid", "wall"], domain_name="mixture")
    >>>
    >>> sv_t_wall_fluid.domain
    'mixture'
    >>>
    >>> sv_t_wall_fluid.zones
    ['fluid', 'wall']
    >>>
    >>> fluid_temp = sv_t_wall_fluid['fluid']
    >>>
    >>> fluid_temp.size
    13852
    >>>
    >>> fluid_temp.dtype
    'float64'
    >>>
    >>> fluid_temp
    array([600., 600., 600., ..., 600., 600., 600.])
  
Set solution variable data
~~~~~~~~~~~~~~~~~~~~~~~~~~
You can set solution variable data for a given ``domain_name`` by calling the ``set_solution_variable_data``
method and passing required ``solution_variable_name`` and dictionary of ``zone_name`` 
to numpy array of ``solution_variable_data``

Additionally solution_variable_data object also supports ``get_array`` method. This method can be used to 
generate ``numpy zeros array`` for a given ``domain_name``, ``zone_name`` and 
``solution_variable_name``. This array can be populated and passed to ``set_solution_variable_data``.

.. code-block:: python
  
    >>> wall_temp_array = solution_variable_data.get_array("SV_T", "wall", "mixture")
    >>> fluid_temp_array = solution_variable_data.get_array("SV_T", "fluid", "mixture")
    >>> wall_temp_array[:] = 500
    >>> fluid_temp_array[:] = 600
    >>> zone_names_to_solution_variable_data = {'wall':wall_temp_array, 'fluid':fluid_temp_array}
    >>> solution_variable_data.set_solution_variable_data(solution_variable_name="SV_T", zone_names_to_solution_variable_data=zone_names_to_solution_variable_data, domain_name="mixture")

.. currentmodule:: ansys.fluent.core.services

.. autosummary::
    :toctree: _autosummary
    :template: flobject-class-template.rst
    :recursive:

    solution_variables.SolutionVariableInfo
    solution_variables.SolutionVariableData
   