.. _ref_interface_guide:


==============
Using PyFluent
==============

You can obtain a PyFluent session object by calling either :func:`launch_fluent()
<ansys.fluent.core.launcher.launcher.launch_fluent>` or :func:`connect_to_fluent() <ansys.fluent.core.launcher.launcher.connect_to_fluent>`. 


.. code:: python

  >>> import ansys.fluent.core as pyfluent
  >>> from ansys.fluent.core.examples import download_file
  >>> case_file_name = download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
  >>> data_file_name = download_file("mixing_elbow.dat.h5", "pyfluent/mixing_elbow")
  >>> solver = pyfluent.launch_fluent(case_data_file_name=case_file_name)


Note: You can find out more about using :ref:`ref_session_guide`, and :ref:`ref_launch_guide`.

The above ``solver`` session object contains a variety of Python objects that provide access to the data
and functions of the connected Fluent solver. A consistent interface style is maintained across those objects
and each object adopts a specific responsibility that is reflected in its particular interface. For instance,
this ``solver`` session provides child objects for solver settings and field data access respectively.
You can discover the ``fields`` and ``settings`` attributes by executing ``dir(solver)``. then you can discover
more children within ``fields`` and ``settings``, and so on.  

.. code:: python

  >>> solver_children = dir(solver)
  >>> settings = solver.settings
  >>> from pprint import pprint
  >>> settings_children = dir(settings)
  >>> fields = solver.fields
  >>> fields_children = dir(fields)


You can call the Python ``help()`` function to find out more about each item in PyFluent. 

.. code:: python

  >>> help(solver.settings.file.read_case)


You can create additional PyFluent sessions. The following code creates a meshing mode
session that starts a second Fluent instance and is independent of your PyFluent solver session.

.. code:: python

  >>> import ansys.fluent.core as pyfluent
  >>> meshing = pyfluent.launch_fluent(mode=pyfluent.FluentMode.MESHING)


A uniform interface exists across solver settings objects. For instance,
``get_state()``, ``set_state()`` and ``is-active()`` are ubiquitous methods,
and ``allowed_values()``, ``min()`` and ``max()`` are found on relevant items.
Here are some examples using the ``viscous`` and ``discrete_phase`` models.

.. code:: python

  >>> viscous_model = settings.setup.models.viscous.model
  >>> viscous_model.get_state()
	'k-omega'
  >>> from pprint import pprint
  >>> pprint(viscous_model.allowed_values())
	['inviscid',
	 'laminar',
	 'k-epsilon',
	 'k-omega',
	 'mixing-length',
	 'spalart-allmaras',
	 'k-kl-w',
	 'transition-sst',
	 'reynolds-stress',
	 'scale-adaptive-simulation',
	 'detached-eddy-simulation',
	 'large-eddy-simulation']
  >>> viscous_model.set_state("laminar")
  >>> viscous_model.get_state()
    'laminar'
  >>> discrete_phase = settings.setup.models.discrete_phase
  >>> discrete_phase.is_active()
    True
  >>> max_num_refinements = discrete_phase.numerics.tracking.accuracy_control.max_num_refinements
  >>> max_num_refinements.get_state()
	20
  >>> max_num_refinements.min(), max_num_refinements.max()
   (0, 1000000)
  

Some items in the solver settings object tree are methods:

  >>> solver.settings.solution.run_calculation.iterate(iter_count=100)


Note: You can find out more about solver settings objects here:
:ref:`ref_settings_guide`. 

Objects under ``fields`` provide a similar interface.

  >>> field_data = fields.field_data
  >>> transaction = field_data.new_transaction()
  >>> add_scalar_fields = transaction.add_scalar_fields_request
  >>> allowed_field_names = add_scalar_fields.field_name.allowed_values()
  >>> pprint(allowed_field_names[:min([len(allowed_field_names), 5])])
  ['abs-angular-coordinate',
   'absolute-pressure',
   'angular-coordinate',
   'anisotropic-adaption-cells',
   'aspect-ratio']
  >>> add_scalar_fields.surface_names.allowed_values()
  ['cold-inlet', 'hot-inlet', 'outlet', 'symmetry-xyplane', 'wall-elbow', 'wall-inlet']
  >>> add_scalar_fields(field_name='absolute-pressure', surface_names=['cold-inlet', 'hot-inlet', 'outlet', 'symmetry-xyplane', 'wall-elbow', 'wall-inlet'])
  >>> pressure_fields = transaction.get_fields()
  >>> solver.fields.reduction.sum_if(
  >>>     expression="AbsolutePressure",
  >>>     condition="AbsolutePressure > 0[Pa]",
  >>>     locations=[settings.setup.boundary_conditions.velocity_inlet["cold-inlet"]],
  >>>     weight="Area",
  >>> )
  15401477.28604886


Note that interactions in meshing mode are consistent with solver mode. Here is some
task-based meshing workflow code:

.. code:: python

  >>> watertight = meshing.watertight()
  >>> from ansys.fluent.core.examples import download_file
  >>> import_file_name = examples.download_file('mixing_elbow.pmdb', 'pyfluent/mixing_elbow')
  >>> import_geometry = watertight.import_geometry
  >>> import_geometry.file_name.set_state(import_file_name)
  >>> length_unit = import_geometry.length_unit
  >>> length_unit.get_state()
   "mm"
  >>> length_unit.allowed_values()
   ["m", "cm", "mm", "in", "ft", "um", "nm"]
  >>> length_unit.set_state("mm")
  >>> import_geometry()


Note: You can find out more about meshing workflow here:
:ref:`ref_new_meshing_workflows_guide`. 