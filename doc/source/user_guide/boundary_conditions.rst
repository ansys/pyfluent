Boundary conditions
===================
The examples in this section show how you use :ref:`ref_settings` to interact with
boundary conditions.

Boundary conditions
~~~~~~~~~~~~~~~~~~~

**Python code**

.. code:: python

    >>> cold_inlet = solver.setup.boundary_conditions.velocity_inlet["cold-inlet"]
    >>> cold_inlet.momentum.velocity = 0.4
    >>> cold_inlet.turbulence.turbulence_specification = "Intensity and Hydraulic Diameter"
    >>> cold_inlet.turbulence.turbulent_intensity= 5
    >>> cold_inlet.turbulence.hydraulic_diameter= "4 [in]"
    >>> cold_inlet.thermal.temperature= 293.15

Cell zone conditions
~~~~~~~~~~~~~~~~~~~~

**Python code**

.. code:: python

    # Enabling Laminar Zone
    >>> solver.setup.cell_zone_conditions.fluid["elbow-fluid"] = {"laminar": True}
