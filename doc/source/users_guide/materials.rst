Materials
=========
PyFluent allows you to access Fluent Materials using the traditional
Text User Interface (TUI) command-based infrastructure and the settings
module (Beta).

TUI based infrastructure
-------------------------
Here’s a simple example defining materials using the TUI based infrastructure:

.. code:: python

    session.solver.tui.define.materials.copy("fluid", "water-liquid")
    session.solver.tui.define.boundary_conditions.fluid(
        "elbow-fluid",
        "yes",
        "water-liquid",
        "no",
        "no",
        "no",
        "no",
        "0",
        "no",
        "0",
        "no",
        "0",
        "no",
        "0",
        "no",
        "0",
        "no",
        "1",
        "no",
        "no",
        "no",
        "no",
        "no",
    )

Settings module (Beta)
-------------------------
Here’s a simple example defining materials using the settings module:

.. code:: python

    session.solver.root.setup.materials.copy_database_material_by_name(type="fluid", name="water-liquid")
    session.solver.root.setup.cell_zone_conditions.fluid["elbow-fluid"].material = "water-liquid"

API Reference
--------------
For more details, please see the API Reference section. 