Defining Parametric Workflows
=============================
PyFluent supports parametric workflows in Fluent.

Parametric Study
----------------
Here is a simple example:

Creating Input Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~
The following example demonstrates how you can create input parameters:
inlet1_vel, inlet1_temp, inlet2_vel and inlet2_temp

.. code:: python

    from pathlib import Path
    import ansys.fluent.core as pyfluent
    from ansys.fluent.core import examples
    from ansys.fluent.parametric import ParametricProject, ParametricStudy

    session = pyfluent.launch_fluent(precision="double", processor_count=2)
    import_filename = examples.download_file(
        "Static_Mixer_main.cas.h5", "pyfluent/static_mixer"
    )
    session.solver.root.file.read(file_type="case", file_name=import_filename)
    session.solver.root.solution.run_calculation.iterate(number_of_iterations=100)
    session.solver.tui.define.parameters.enable_in_TUI("yes")
    session.solver.tui.define.boundary_conditions.set.velocity_inlet(
        "inlet1", (), "vmag", "yes", "inlet1_vel", 1, "quit"
    )
    session.solver.tui.define.boundary_conditions.set.velocity_inlet(
        "inlet1", (), "temperature", "yes", "inlet1_temp", 300, "quit"
    )
    session.solver.tui.define.boundary_conditions.set.velocity_inlet(
        "inlet2", (), "vmag", "yes", "no", "inlet2_vel", 1, "quit"
    )
    session.solver.tui.define.boundary_conditions.set.velocity_inlet(
        "inlet2", (), "temperature", "yes", "no", "inlet2_temp", 350, "quit"
    )

Creating Output Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~
The following example demonstrates how you can create output parameters:
outlet-temp-avg and outlet-vel-avg

.. code:: python

    session.solver.root.solution.report_definitions.surface["outlet-temp-avg"] = {}
    session.solver.root.solution.report_definitions.surface[
        "outlet-temp-avg"
    ].report_type = "surface-areaavg"
    session.solver.root.solution.report_definitions.surface[
        "outlet-temp-avg"
    ].field = "temperature"
    session.solver.root.solution.report_definitions.surface[
        "outlet-temp-avg"
    ].surface_names = ["outlet"]
    session.solver.root.solution.report_definitions.surface["outlet-vel-avg"] = {}
    session.solver.root.solution.report_definitions.surface[
        "outlet-vel-avg"
    ].report_type = "surface-areaavg"
    session.solver.root.solution.report_definitions.surface[
        "outlet-vel-avg"
    ].field = "velocity-magnitude"
    session.solver.root.solution.report_definitions.surface[
        "outlet-vel-avg"
    ].surface_names = ["outlet"]
    session.solver.tui.define.parameters.enable_in_TUI("yes")
    session.solver.tui.define.parameters.output_parameters.create(
        "report-definition", "outlet-temp-avg"
    )
    session.solver.tui.define.parameters.output_parameters.create(
        "report-definition", "outlet-vel-avg"
    )

Instantiating a parametric study
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The following example demonstrates how you can instantiate a parametric study:

.. code:: python

    study_1 = ParametricStudy(session.solver.root.parametric_studies).initialize()

Accessing and Modifying Input Parameters of the Base Design Point
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The following example demonstrates how you can access and modify input parameters of the base design point:

.. code:: python

    input_parameters_update = study_1.design_points["Base DP"].input_parameters
    input_parameters_update["inlet1_vel"] = 0.5
    study_1.design_points["Base DP"].input_parameters = input_parameters_update

Updating the Current Design Point
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The following example demonstrates how you can update the current design point:

.. code:: python

    study_1.update_current_design_point()

Adding New Design Points
~~~~~~~~~~~~~~~~~~~~~~~~
The following example demonstrates how to add new design points:

.. code:: python

    design_point_1 = study_1.add_design_point()
    design_point_1_input_parameters = study_1.design_points["DP1"].input_parameters
    design_point_1_input_parameters["inlet1_temp"] = 500
    design_point_1_input_parameters["inlet1_vel"] = 1
    design_point_1_input_parameters["inlet2_vel"] = 1
    study_1.design_points["DP1"].input_parameters = design_point_1_input_parameters

Duplicating Design Points
~~~~~~~~~~~~~~~~~~~~~~~~~
The following example demonstrates how you can duplicate a design point:

.. code:: python

    design_point_2 = study_1.duplicate_design_point(design_point_1)

Updating All Design Points
~~~~~~~~~~~~~~~~~~~~~~~~~~
The following example demonstrates how you can update all design points in your study:

.. code:: python

    study_1.update_all_design_points()

Exporting the Design Point Table
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The following example demonstrates how you can export the design point table as a comma separated value (CSV) table:

.. code:: python

    design_point_table = str(
        Path(pyfluent.EXAMPLES_PATH) / "design_point_table_study_1.csv"
    )
    study_1.export_design_table(design_point_table)

Deleting Design Points
~~~~~~~~~~~~~~~~~~~~~~
The following example demonstrates how you can remove design points:

.. code:: python

    study_1.delete_design_points([design_point_1])

Duplicating Design Points
~~~~~~~~~~~~~~~~~~~~~~~~~
The following example demonstrates how you can copy design points:

.. code:: python

    study_2 = study_1.duplicate()

Renaming Studies
~~~~~~~~~~~~~~~~
The following example demonstrates how you can change the name of your study:

.. code:: python

    study_2.rename("New Study")

Deleting Studies
~~~~~~~~~~~~~~~~
The following example demonstrates how you can remove old parametric studies:

.. code:: python

    study_1.delete()

Saving Your Study and Closing Fluent
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The following example demonstrates how you can save your work and close the Fluent instance:

.. code:: python

    project_filepath = str(Path(pyfluent.EXAMPLES_PATH) / "static_mixer_study.flprj")
    session.solver.tui.file.parametric_project.save_as(project_filepath)
    session.exit()

Resuming Your Work
~~~~~~~~~~~~~~~~~~
The following example demonstrates how you can re-start Fluent and read in a previously saved project:

.. code:: python

    session = pyfluent.launch_fluent(precision="double", processor_count=2)
    project_filepath_read = str(Path(pyfluent.EXAMPLES_PATH) / "static_mixer_study.flprj")
    proj = ParametricProject(
        session.solver.root.file.parametric_project,
        session.solver.root.parametric_studies,
        project_filepath_read,
    )

Saving Your Work
~~~~~~~~~~~~~~~~
The following example demonstrates how you can save your current project:

.. code:: python

    proj.save()

Saving Your Work With a Different Name
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The following example demonstrates how you can save your current project to a different file name:

.. code:: python

    project_filepath_save_as = str(
        Path(pyfluent.EXAMPLES_PATH) / "static_mixer_study_save_as.flprj"
    )
    proj.save_as(project_filepath=project_filepath_save_as)

Exporting Your Work
~~~~~~~~~~~~~~~~~~~
The following example demonstrates how you can export the current project:

.. code:: python

    project_filepath_export = str(
        Path(pyfluent.EXAMPLES_PATH) / "static_mixer_study_export.flprj"
    )
    proj.export(project_filepath=project_filepath_export)

Archiving Projects
~~~~~~~~~~~~~~~~~~
The following example demonstrates how you can archive your current project:

.. code:: python

    proj.archive()

Closing Fluent
~~~~~~~~~~~~~~
The following example demonstrates how you can end your Fluent session:

.. code:: python

    session.exit()