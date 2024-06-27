.. _ref_user_guide_interface:


============================
Using the PyFluent interface
============================

In this section, we explore some of the feature and usage patterns of PyFluent interface so that you can get a better understanding of how
to use the library in general.

You can start to use the PyFluent interface by importing and calling either :func:`launch_fluent()
<ansys.fluent.core.launcher.launcher.launch_fluent>` or :func:`connect_to_fluent() <ansys.fluent.core.launcher.launcher.connect_to_fluent>`. 


.. code:: python

  >>> import ansys.fluent.core as pyfluent
  >>> from ansys.fluent.core.examples import download_file
  >>> case_file_name = download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
  >>> data_file_name = download_file("mixing_elbow.dat.h5", "pyfluent/mixing_elbow")
  >>> solver = pyfluent.launch_fluent(case_data_file_name=case_file_name)


Note: You can find out more about using :ref:`ref_user_guide_session`, and :ref:`ref_user_guide_launch`.

The above `solver` session object contains a variety of Python objects that provide access to Fluent data and functions. Each object adopts a
specific responsibility that is reflected in its interface. However, PyFluent adopts a consistent style that is consistent across much of
the interface.

.. code:: python

  >>> viscous = settings.setup.models.viscous
  >>> viscous_state = viscous.get_state()
  >>> viscous.model.get_state()
	'k-omega'
  >>> from pprint import pprint
  >>> pprint(viscous.model.allowed_values())
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
  >>> viscous.model.set_state("laminar")
  >>> viscous.model.get_state()
    'laminar'
  >>> discrete_phase = settings.setup.models.discrete_phase
  >>> discrete_phase.is_active()
    True
  >>> max_num_refinements = discrete_phase.numerics.tracking.accuracy_control.max_num_refinements
  >>> max_num_refinements.get_state()
	20
  >>> max_num_refinements.min(), max_num_refinements.max()
   (0, 1000000)
  >>> solver.preferences.Appearance.ColorTheme.allowed_values()
['Fluent R19.2', 'Default', 'SpaceClaim 2016', 'Classic Dark', 'Dark']
  

  >>> field_data = solver.fields.field_data
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



.. code:: python

  >>> import ansys.fluent.core as pyfluent
  >>> meshing = pyfluent.launch_fluent(mode=pyfluent.FluentMode.MESHING)
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

