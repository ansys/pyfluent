Defining Boundary Conditions
============================

Text User Interface (TUI) API
-----------------------------
The following example demonstrates how you can define boundary conditions using
the TUI API:

Defining Boundary Conditions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    import ansys.fluent.core as pyfluent
    session = pyfluent.launch_fluent(precision="double", processor_count=2)
    session.solver.tui.file.read_case(case_file_name='file.cas.h5')
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

Copying Boundary Conditions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    session.solver.tui.define.boundary_conditions.copy_bc("cold-inlet","hot-inlet","()")

Listing Zones
~~~~~~~~~~~~~

.. code:: python

    session.solver.tui.define.boundary_conditions.list_zones()

Modifying Cellzone Conditions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    #Enabling Laminar Zone
    session.solver.tui.define.boundary_conditions.fluid('elbow-fluid','no','no','no','no','no',0,'no',0,'no',0,'no',0,'no',0,'no',1,'no','yes','yes','no','no','no')

Settings Objects
----------------
The following example demonstrates how you can define boundary conditions using
:ref:`ref_settings`:

Defining Boundary Conditions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

Modifying Cellzone Conditions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    #Enabling Laminar Zone
    session.solver.root.setup.cell_zone_conditions.fluid['elbow-fluid'] = {"laminar" : True}