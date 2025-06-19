.. _ref_rpvars_guide:

rpvars
======

Examples
--------

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
