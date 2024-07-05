Boundary conditions
===================
The examples in this section show how you use :ref:`ref_settings` to interact with
boundary conditions.

Boundary conditions
~~~~~~~~~~~~~~~~~~~

.. code:: python

    >>> cold_inlet = solver.settings.setup.boundary_conditions.velocity_inlet["cold-inlet"]
    >>> cold_inlet.momentum.velocity.set_state(0.4)
    >>> inlet_turbulence = cold_inlet.turbulence
    >>> turbulence_specification = inlet_turbulence.turbulence_specification
    >>> turbulence_specification.allowed_values()
    ['K and Omega', 'Intensity and Length Scale', 'Intensity and Viscosity Ratio', 'Intensity and Hydraulic Diameter']
    >>> turbulence_specification.set_state("Intensity and Hydraulic Diameter")
    >>> turbulent_intensity = inlet_turbulence.turbulent_intensity
    >>> turbulent_intensity.min(), turbulent_intensity.max()
    (0, 1)
    >>> turbulent_intensity.set_state(0.5)
    >>> inlet_turbulence.hydraulic_diameter.set_state("4 [in]")
    >>> cold_inlet.thermal.temperature.set_state(293.15)


Cell zone conditions
~~~~~~~~~~~~~~~~~~~~

.. code:: python

    >>> solver.settings.setup.cell_zone_conditions.fluid["elbow-fluid"].laminar.set_state(True)
