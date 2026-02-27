.. _ref_rpvars_guide:

rpvars
======

Examples
--------

Accessing and modifying existing rpvars
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   >>> import ansys.fluent.core as pyfluent
   >>> solver_session = pyfluent.launch_fluent()
   >>> iter_count = 100
   >>> solver_session.rp_vars("number-of-iterations", iter_count)
   'number-of-iterations'
   >>> solver_session.rp_vars("number-of-iterations")
   100
   >>> # Get dictionary of all available rpvars:
   >>> solver_session.rp_vars()
   {'sg-swirl?': False, 'rp-seg?': True, 'rf-energy?': False, 'rp-inviscid?': False, ...
   'number-of-iterations': 100, ...}


Creating rpvars
~~~~~~~~~~~~~~~

You can create custom user-defined rpvars with specific types using the ``create`` method.
The ``var_type`` parameter accepts either Python types (``int``, ``float``, ``bool``, ``str``)
or ``RPVarType`` enum values. Use ``None`` to create a custom-typed rpvars
that can hold any value type.

.. code-block:: python

   >>> import ansys.fluent.core as pyfluent
   >>> from ansys.fluent.core.rpvars import RPVarType
   >>> solver_session = pyfluent.launch_fluent()
   
   >>> # Create integer rpvars using Python type
   >>> solver_session.rp_vars.create(name="my-int-var", value=55, var_type=int)
   >>> solver_session.rp_vars("my-int-var")
   55
   >>> solver_session.rp_vars("my-int-var", 60)
   >>> solver_session.rp_vars("my-int-var")
   60
   
   >>> # Create string rpvars using RPVarType enum
   >>> solver_session.rp_vars.create(name="my-str-var", value="my-string", var_type=RPVarType.STRING)
   >>> solver_session.rp_vars("my-str-var")
   '"my-string"'
   >>> solver_session.rp_vars("my-str-var", "new-str")
   >>> solver_session.rp_vars("my-str-var")
   '"new-str"'
   
   >>> # Create custom-typed rpvars that accepts any type
   >>> solver_session.rp_vars.create(name="my-custom-var", value=100, var_type=None)
   >>> solver_session.rp_vars("my-custom-var")
   100
   >>> solver_session.rp_vars("my-custom-var", "any-str")
   >>> solver_session.rp_vars("my-custom-var")
   '"any-str"'


**Type validation:**

When creating typed rpvars, the initial value must match the specified type. Type-checking 
is enforced to prevent mismatches:

.. code-block:: python

   >>> # This raises TypeError: value type mismatch
   >>> solver_session.rp_vars.create(name="my-int-var", value=55.5, var_type=int)
   TypeError: Value type mismatch: expected <class 'int'>, got float
   
   >>> # This raises NameError: rpvars already exists
   >>> solver_session.rp_vars.create(name="my-int-var", value=55, var_type=int)
   NameError: 'my-int-var' already exists as an rpvar.

**Note:** Custom-typed rpvars (created with ``var_type=None``) do not enforce type restrictions 
and can be reassigned to any value type.