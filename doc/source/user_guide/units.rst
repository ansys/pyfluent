.. _ref_units_guide:

Physical units
==============
By default, you can access and modify PyFluent solver settings according to SI units.
However, PyFluent also allows you to work in arbitrary physical units. Here's an example:

.. code-block:: python

  >>> from ansys.units import Quantity
  >>> hydraulic_diameter = solver_session.settings.setup.boundary_conditions.velocity_inlet["hot-inlet"].turbulence.hydraulic_diameter
  >>> hydraulic_diameter.set_state(.02)
  >>> hydraulic_diameter.get_state()
  0.02
  >>> hydraulic_diameter.state_with_units()
  (0.02, 'm')
  >>> hydraulic_diameter.set_state(Quantity(15, "mm"))
  >>> hydraulic_diameter.state_with_units()
  (0.015, 'm')
  >>> diam = hydraulic_diameter.as_quantity()
  >>> diam
  Quantity (0.015, "m")
  >>> diam = diam * 2
  >>> diam
  Quantity (0.03, "m")
  >>> hydraulic_diameter.set_state(diam)
  >>> hydraulic_diameter.as_quantity()
  Quantity (0.03, "m")


You can find out more about using ``Quantity`` objects and other library features in the 
`PyAnsys Units documentation <https://units.docs.pyansys.com/version/stable/>`_.

.. note::

  While most PyFluent settings commands expect values in SI units, TUI
  commands (e.g., ``solver_session.tui.define.models.energy("yes", True)``)
  work in terms of the current units in Fluent, as specified by the user.
  For example, if the length unit is set to 'mm' in Fluent, any length values
  passed to TUI commands should also be in 'mm'.
