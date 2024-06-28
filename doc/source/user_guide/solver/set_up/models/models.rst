.. _ref_models_guide:

Physics models
==============

Energy model
~~~~~~~~~~~~

The examples in this section show how you use :ref:`ref_settings` to
define models.

Enable energy model
~~~~~~~~~~~~~~~~~~~

**Python code**

.. code:: python

    energy = solver.setup.models.energy
    energy.enabled = True

Enable viscous model
~~~~~~~~~~~~~~~~~~~~

**Python code**

.. code:: python

    viscous = solver.setup.models.viscous
    viscous.k_epsilon_model.enabled = True
    viscous.k_omega_model.enabled = True
