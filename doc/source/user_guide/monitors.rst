.. _ref_monitors_guide:

Using monitors
==============

Monitors allow you to observe the convergence of your solution dynamically
by checking the values of solution variables and residuals.

The following example queries what monitors exist and then registers a callback
function which tabulates monitored values per iteration:

.. code-block:: python

    import ansys.fluent.core as pyfluent
    from ansys.fluent.core import examples
    import pandas as pd
    from tabulate import tabulate
    solver = pyfluent.launch_fluent(start_transcript=False)
    import_case = examples.download_file(
        file_name="exhaust_system.cas.h5", directory="pyfluent/exhaust_system"
    )
    import_data = examples.download_file(
        file_name="exhaust_system.dat.h5", directory="pyfluent/exhaust_system"
    )
    solver.file.read_case_data(file_name=import_case)
    sorted(solver.settings.solution.monitor.report_plots())
    [
        "mass-bal-rplot",
        "mass-in-rplot",
        "mass-tot-rplot",
        "point-vel-rplot",
    ]
    solver.solution.initialization.hybrid_initialize()
    sorted(solver.monitors.get_monitor_set_names())
    [
        "mass-bal-rplot",
        "mass-in-rplot",
        "mass-tot-rplot",
        "point-vel-rplot",
        "residual"
    ]

    def display_monitor_table(monitor_set_name="mass-bal-rplot"):
        def display_table():
            data = solver.monitors.get_monitor_set_data(monitor_set_name=monitor_set_name)
            iterations = data[0]
            if len(iterations) > display_table.iter_count:
                display_table.iter_count = len(iterations)
                results = data[1]
                df = pd.DataFrame(results, index=iterations)
                df.index.name = 'Iteration'
                df.reset_index(inplace=True)
                df = df.drop_duplicates(subset='Iteration')
                print(tabulate(df, headers='keys', tablefmt='psql'))
        display_table.iter_count = 0
        return display_table
    

    register_id = solver.monitors.register_callback(display_monitor_table())

    solver.solution.run_calculation.iterate(iter_count=10)
