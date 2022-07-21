Defining Materials
==================
PyFluent supports defining materials using :ref:`ref_solver_tui_commands` and 
:ref:`ref_settings`.

Using solver TUI commands
-------------------------
This example shows how you define materials using
:ref:`ref_solver_tui_commands`.

The ``define.materials`` TUI enters the materials menu.

.. code:: python

    import ansys.fluent.core as pyfluent
    session = pyfluent.launch_fluent(precision='double', processor_count=2)
    session.solver.tui.file.read_case(case_file_name='file.cas.h5')
    session.solver.tui.define.materials.copy('fluid', 'water-liquid')
    session.solver.tui.define.boundary_conditions.fluid(
        'elbow-fluid',
        'yes',
        'water-liquid',
        'no',
        'no',
        'no',
        'no',
        '0',
        'no',
        '0',
        'no',
        '0',
        'no',
        '0',
        'no',
        '0',
        'no',
        '1',
        'no',
        'no',
        'no',
        'no',
        'no',
    )

Using Settings objects
----------------------
This example shows how you define materials using
:ref:`ref_settings`.

.. code:: python

    session.solver.root.setup.materials.copy_database_material_by_name(type='fluid', name='water-liquid')
    session.solver.root.setup.cell_zone_conditions.fluid['elbow-fluid'].material = 'water-liquid'