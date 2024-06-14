Boundary conditions
===================
The examples in this section show how you use :ref:`ref_settings` to interact with
boundary conditions.

Boundary conditions
~~~~~~~~~~~~~~~~~~~

**Python code**

.. code:: python

    boundary_conditions = solver.setup.boundary_conditions
    velocity_inlet = boundary_conditions.velocity_inlet
    velocity_inlet["cold-inlet"].vmag = {
        "option": "constant or expression",
        "constant": 0.4,
    }
    velocity_inlet[
        "cold-inlet"
    ].ke_spec = "Intensity and Hydraulic Diameter"
    velocity_inlet["cold-inlet"].turb_intensity = 5
    velocity_inlet[
        "cold-inlet"
    ].turb_hydraulic_diam = "4 [in]"
    velocity_inlet["cold-inlet"].t = {
        "option": "constant or expression",
        "constant": 293.15,
    }

Cell zone conditions
~~~~~~~~~~~~~~~~~~~~

**Python code**

.. code:: python

    # Enabling Laminar Zone
    solver.setup.cell_zone_conditions.fluid["elbow-fluid"] = {"laminar": True}
