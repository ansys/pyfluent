Boundary Conditions
====================
PyFluent allows you to define Fluent boundary conditions using the traditional
Text User Interface (TUI) command-based infrastructure and the settings
module (Beta).

TUI based infrastructure
-------------------------
Here’s a simple example defining boundary conditions using the TUI based infrastructure:

.. code:: python

    session.solver.tui.define.boundary_conditions.set.velocity_inlet(
        "cold-inlet", [], "vmag", "no", 0.4, "quit"
    )
    session.solver.tui.define.boundary_conditions.set.velocity_inlet(
        "cold-inlet", [], "ke-spec", "no", "no", "no", "yes", "quit"
    )
    session.solver.tui.define.boundary_conditions.set.velocity_inlet(
        "cold-inlet", [], "turb-intensity", 5, "quit"
    )
    session.solver.tui.define.boundary_conditions.set.velocity_inlet(
        "cold-inlet", [], "turb-hydraulic-diam", 4, "quit"
    )
    session.solver.tui.define.boundary_conditions.set.velocity_inlet(
        "cold-inlet", [], "temperature", "no", 293.15, "quit"
    )

Settings module (Beta)
-------------------------
Here’s a simple example defining boundary conditions using the settings module:

.. code:: python

    session.solver.root.setup.boundary_conditions.velocity_inlet["cold-inlet"].vmag = {
        "option": "constant or expression",
        "constant": 0.4,
    }
    session.solver.root.setup.boundary_conditions.velocity_inlet[
        "cold-inlet"
    ].ke_spec = "Intensity and Hydraulic Diameter"
    session.solver.root.setup.boundary_conditions.velocity_inlet[
        "cold-inlet"
    ].turb_intensity = 5
    session.solver.root.setup.boundary_conditions.velocity_inlet[
        "cold-inlet"
    ].turb_hydraulic_diam = "4 [in]"
    session.solver.root.setup.boundary_conditions.velocity_inlet["cold-inlet"].t = {
        "option": "constant or expression",
        "constant": 293.15,
    }

API Reference
--------------
For more details, please see the API Reference section. 