.. _ref_settings:

Settings Objects (Beta)
=======================

Introduction
------------

Settings objects provide a natural way to access and modify Fluent settings and
issue commands with a hierarchy of objects.

Top-level Objects
-----------------

The top-level settings object is available as the ``root`` property of session.solver.

.. code-block::

  >>> import ansys.fluent.core as pyfluent
  >>> session = pyfluent.launch_fluent()
  >>> root = session.solver.root

The root object contains attributes such as ``file``, ``setup``,
``solution`` and ``results``.  These objects are also instances of 'settings'
objects and roughly mirror the outline view in Fluent.

Types of Settings Objects
-------------------------

A settings object can be one of the primitive types like ``Integer``, ``Real``,
``String`` and ``Boolean`` or a container object.

There are three types of container objects: ``Group``, ``NamedObject`` and
``ListObject``.

A ``Group`` object is a static container with pre-defined child objects which
can be accessed via attribute access. For example, ``setup.models.energy``
refers to the ``energy`` child of ``models`` child of the ``setup`` object. The
names of the child objects of a group can be accessed with the ``child_names``
attribute of a ``Group`` object.

A ``NamedObject`` is a container holding dynamically created named objects of
its specified child type (accessible via ``child_object_type`` attribute)
similar to a dictionary. A specified named object can be accessed using the
index operator. For example,
``root.setup.boundary_conditions.velocity_inlet['inlet2']`` refers to the
``velocity_object`` object with name ``inlet2``. The current list of named
object children can be accessed with the ``get_object_names()`` function of the
container class.

A ``ListObject`` is a container holding dynamically created unnamed objects of
its specified child type (accessible via ``child_object_type`` attribute) in a
list. Children of ``ListObject`` can be accessed using the index operator. For
example,
``root.setup.cell_zone_conditions.fluid['fluid-1'].source_terms['mass'][2]``
refers to the third (starting from index 0) mass source entry for the fluid zone
named ``fluid-1``. The current number of child objects can be accessed via the
``get_size()`` function.
 

Setting and Modifying State
---------------------------

The state of any object can be accessed by "calling" it. For container objects,
this will return the state of the children as a dictionary (for ``Group`` and
``NamedObject`` types) or a list (for ``ListObject``) types:

.. code-block::

  >>> root.setup.models.viscous.model()
  'k-epsilon-standard'

.. code-block::

  >>> from pprint import pprint
  >>> pprint (root.setup.models.energy())
  {'enabled': True,
   'inlet_diffusion': True,
   'kinetic_energy': False,
   'pressure_work': False,
   'viscous_dissipation': False}
  >>> root.setup.boundary_conditions.velocity_inlet['inlet1'].vmag.constant()
  10.0

To modify the state of any object, you could assign the corresponding attribute
in its parent object. This assignment could be done at any level. For ``Group``
and ``NamedObject`` type objects, the state value will be a dictionary, and for
``ListObject`` type objects, the state value will be a list.

.. code-block::

  >>> root.setup.models.viscous.model = 'laminar'
  >>> root.setup.models.energy = { 'enabled' : False }
  >>> root.setup.boundary_conditions.velocity['inlet1'].vmag.constant = 14

The state of an object can also be accessed via the ``get_state`` method, and
modified via the ``set_state`` method.

The current state can also be printed in a simple text format with the
``print_state`` method. For example, the following

.. code-block::

  >>> root.setup.models.print_state()

gives the following output:
  
.. code-block::

  viscous :
    k_epsilon_model : standard
    near_wall_treatment : standard-wall-fn?
    model : k-epsilon-standard
    options :
      viscous_heating : False
      curvature_correction : False
      production_kato_launder : False
      production_limiter : False
  energy :
    enabled : True
    pressure_work : False
    viscous_dissipation : False
    inlet_diffusion : True
    kinetic_energy : False
  multiphase :
    number_of_phases : 0
    models : none

Commands
--------

Commands are methods of settings objects that are used to modify the state of
the application. For example, the ``hybrid_initialize()`` method of
``solution.initialization`` initializes the solution using the hybrid
initialization method. The ``command_names`` attribute of a settings object
provides the names of its commands.

If needed, commands can be passed keyword arguments, and the list of valid
arguments can be accessed using the ``arguments`` attribute.  If an argument is
not specified, its default value is used. Arguments are also settings objects
and can be either primitive type or container type.

Additional Metadata
-------------------

Settings objects have some additional metadata which can be accessed using the
``get_attr`` and ``get_attrs`` methods. For example, the list of allowed values
at a particular state for the viscous model can be accessed as follows:

.. code-block::

  >>> root.setup.models.viscous.model.get_attr('allowed-values')
  ['inviscid', 'laminar', 'k-epsilon-standard', 'k-omega-standard', 'mixing-length', 'spalart-allmaras', 'k-kl-w', 'transition-sst', 'reynolds-stress', 'scale-adaptive-simulation', 'detached-eddy-simulation', 'large-eddy-simulation']

Attributes are dynamic and the values can change depending on the application
state.

Active Objects and Commands
---------------------------

Objects and commands can be active or inactive based on the application state.
application. The ``is_active()`` method returns ``True`` if an object or command
is active at a particular time. ``get_active_child_names`` returns the list of
active children. ``get_active_command_names`` returns the list of active
commands.

Settings Objects Root
---------------------
:ref:`Settings root<root>`