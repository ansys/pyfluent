Viscous model
=============

**Python code**

.. code:: python

    viscous = solver.settings.setup.models.viscous
    viscous.k_epsilon_model.enabled = True
    viscous.k_omega_model.enabled = True