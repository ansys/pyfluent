from pathlib import Path
import tempfile
import time

import pytest

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples


@pytest.mark.fluent_232
def test_parametric_workflow():
    save_path = tempfile.mkdtemp(dir=pyfluent.EXAMPLES_PATH)
    import_filename = examples.download_file(
        "Static_Mixer_main.cas.h5", "pyfluent/static_mixer", save_path=save_path
    )
    solver_session = pyfluent.launch_fluent(processor_count=2, cwd=save_path)
    solver_session.file.read_case(file_name=import_filename)
    solver_session.solution.run_calculation.iter_count = 100
    solver_session.tui.define.parameters.enable_in_TUI("yes")
    solver_session.tui.define.boundary_conditions.set.velocity_inlet(
        "inlet1", (), "vmag", "yes", "inlet1_vel", 1, "quit"
    )
    solver_session.tui.define.boundary_conditions.set.velocity_inlet(
        "inlet1", (), "temperature", "yes", "inlet1_temp", 300, "quit"
    )
    solver_session.tui.define.boundary_conditions.set.velocity_inlet(
        "inlet2", (), "vmag", "yes", "no", "inlet2_vel", 1, "quit"
    )
    solver_session.tui.define.boundary_conditions.set.velocity_inlet(
        "inlet2", (), "temperature", "yes", "no", "inlet2_temp", 350, "quit"
    )
    solver_session.solution.report_definitions.surface["outlet-temp-avg"] = {}
    solver_session.solution.report_definitions.surface[
        "outlet-temp-avg"
    ].report_type = "surface-areaavg"
    solver_session.solution.report_definitions.surface[
        "outlet-temp-avg"
    ].field = "temperature"
    solver_session.solution.report_definitions.surface[
        "outlet-temp-avg"
    ].surface_names = ["outlet"]
    solver_session.solution.report_definitions.surface["outlet-vel-avg"] = {}
    solver_session.solution.report_definitions.surface[
        "outlet-vel-avg"
    ].report_type = "surface-areaavg"
    solver_session.solution.report_definitions.surface[
        "outlet-vel-avg"
    ].field = "velocity-magnitude"
    solver_session.solution.report_definitions.surface[
        "outlet-vel-avg"
    ].surface_names = ["outlet"]
    solver_session.tui.define.parameters.output_parameters.create(
        "report-definition", "outlet-temp-avg"
    )
    solver_session.tui.define.parameters.output_parameters.create(
        "report-definition", "outlet-vel-avg"
    )
    solver_session.tui.solve.monitors.residual.criterion_type("0")
    case_path = str(Path(save_path) / "Static_Mixer_Parameters.cas.h5")
    solver_session.file.write(file_type="case", file_name=case_path)
    assert (Path(save_path) / "Static_Mixer_Parameters.cas.h5").exists()
    assert len(solver_session.parametric_studies) == 0
    solver_session.parametric_studies.initialize()
    assert len(solver_session.parametric_studies) == 1
    study1_name = "Static_Mixer_main-Solve"
    assert study1_name in solver_session.parametric_studies
    study1 = solver_session.parametric_studies[study1_name]
    assert len(study1.design_points) == 1
    base_dp_name = "Base DP"
    assert "Base DP" in study1.design_points
    base_dp = study1.design_points[base_dp_name]
    base_dp.input_parameters["inlet1_vel"] = 0.5
    assert base_dp.input_parameters["inlet1_vel"]() == 0.5
    assert base_dp.input_parameters["inlet2_temp"]() == 350.0
    assert base_dp.input_parameters["inlet2_vel"]() == 1.0
    assert base_dp.input_parameters["inlet1_temp"]() == 300.0
    study1.design_points.update_current()
    assert len(study1.design_points) == 1
    assert base_dp.output_parameters["outlet-temp-avg-op"]() == pytest.approx(
        333.348727
    )
    assert base_dp.output_parameters["outlet-vel-avg-op"]() == pytest.approx(1.506855)
    dp1_name = study1.design_points.create_1()
    dp1 = study1.design_points[dp1_name]
    dp1.input_parameters["inlet1_temp"] = 500
    dp1.input_parameters["inlet1_vel"] = 1
    dp1.input_parameters["inlet2_vel"] = 1
    assert len(study1.design_points) == 2
    assert dp1.input_parameters["inlet1_temp"]() == 500
    assert dp1.input_parameters["inlet1_vel"]() == 1
    assert dp1.input_parameters["inlet2_vel"]() == 1
    assert dp1.input_parameters["inlet2_temp"]() == 350.0
    dp_names = set([*study1.design_points.keys()])
    study1.design_points.duplicate(design_point=dp1.obj_name)
    dp2_name = set([*study1.design_points.keys()]).difference(dp_names).pop()
    dp2 = study1.design_points[dp2_name]
    assert dp1.input_parameters() == dp2.input_parameters()
    assert len(study1.design_points) == 3
    assert study1.current_design_point() == base_dp_name
    study1.design_points.set_as_current(design_point=dp2_name)
    assert study1.current_design_point() == dp2_name
    study1.design_points.update_all()
    assert len(study1.design_points) == 3
    assert base_dp.output_parameters["outlet-temp-avg-op"]() == pytest.approx(
        333.348727
    )
    assert base_dp.output_parameters["outlet-vel-avg-op"]() == pytest.approx(1.506855)
    assert dp1.output_parameters["outlet-temp-avg-op"]() == pytest.approx(425.004045)
    assert dp1.output_parameters["outlet-vel-avg-op"]() == pytest.approx(2.029792)
    assert dp2.output_parameters["outlet-temp-avg-op"]() == pytest.approx(425.004045)
    assert dp2.output_parameters["outlet-vel-avg-op"]() == pytest.approx(2.029792)
    design_point_table = str(Path(save_path) / "design_point_table_study_1.csv")
    solver_session.parametric_studies.export_design_table(filepath=design_point_table)
    study1.design_points.delete_design_points(design_points=[dp1_name])
    assert len(study1.design_points) == 2
    study_names = set([*solver_session.parametric_studies.keys()])
    solver_session.parametric_studies.duplicate()
    assert len(solver_session.parametric_studies) == 2
    study2_name = (
        set([*solver_session.parametric_studies.keys()]).difference(study_names).pop()
    )
    study2 = solver_session.parametric_studies[study2_name]
    assert len(study2.design_points) == 2
    solver_session.parametric_studies.rename("New Study", study2_name)
    assert "New Study" in solver_session.parametric_studies
    del solver_session.parametric_studies[study1_name]
    assert len(solver_session.parametric_studies) == 1
    project_filename = Path(save_path) / "static_mixer_study.flprj"
    solver_session.file.parametric_project.save_as(
        project_filename=str(project_filename)
    )
    assert project_filename.exists()
    solver_session.exit()
    time.sleep(10)
    solver_session = pyfluent.launch_fluent(processor_count=2, cwd=save_path)
    solver_session.file.parametric_project.open(project_filename=str(project_filename))
    solver_session.file.parametric_project.save()
    project_save_as_name = Path(save_path) / "static_mixer_study_save_as.flprj"
    solver_session.file.parametric_project.save_as(
        project_filename=str(project_save_as_name)
    )
    assert project_save_as_name.exists()
    project_save_as_copy_name = (
        Path(save_path) / "static_mixer_study_save_copy_as.flprj"
    )
    solver_session.file.parametric_project.save_as(
        project_filename=str(project_save_as_copy_name)
    )
    assert project_save_as_copy_name.exists()
    archive_name = Path(save_path) / "static_mixer_study.flprz"
    solver_session.file.parametric_project.archive(archive_name=str(archive_name))
    assert archive_name.exists()
    solver_session.exit()
