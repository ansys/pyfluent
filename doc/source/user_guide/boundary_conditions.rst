Defining Boundary Conditions
============================
PyFluent supports defining boundary conditions using the :ref:`ref_solver_tui_commands` and :ref:`ref_settings`.

Solver TUI Commands
-------------------
The following example demonstrates how you can define boundary conditions using
:ref:`ref_solver_tui_commands`:

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

Settings Objects
----------------
The following example demonstrates how you can define boundary conditions using
:ref:`ref_settings`:

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