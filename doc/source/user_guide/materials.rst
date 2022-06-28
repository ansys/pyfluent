Defining Materials
==================
PyFluent supports defining materials using the TUI API and 
:ref:`ref_settings`.

Text User Interface (TUI) API
-----------------------------
The following example demonstrates how you can define materials using
the TUI API:

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

Settings Objects
----------------
The following example demonstrates how you can define materials using
:ref:`ref_settings`:

.. code:: python

    session.solver.root.setup.materials.copy_database_material_by_name(type="fluid", name="water-liquid")
    session.solver.root.setup.cell_zone_conditions.fluid["elbow-fluid"].material = "water-liquid"