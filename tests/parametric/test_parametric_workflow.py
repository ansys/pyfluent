import os
from pathlib import Path, PurePosixPath
import tempfile

import pytest
from test_utils import pytest_approx

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
from ansys.fluent.core.utils.file_transfer_service import RemoteFileTransferStrategy
from ansys.fluent.core.utils.fluent_version import FluentVersion


@pytest.mark.nightly
@pytest.mark.fluent_version("latest")
def test_parametric_workflow():
    # parent path needs to exist for mkdtemp
    Path(pyfluent.EXAMPLES_PATH).mkdir(parents=True, exist_ok=True)
    tmp_save_path = tempfile.mkdtemp(dir=pyfluent.EXAMPLES_PATH)
    if pyfluent.USE_FILE_TRANSFER_SERVICE:
        file_transfer_service = RemoteFileTransferStrategy(mount_source=tmp_save_path)
    import_file_name = examples.download_file(
        "Static_Mixer_main.cas.h5", "pyfluent/static_mixer", save_path=tmp_save_path
    )
    if os.getenv("PYFLUENT_LAUNCH_CONTAINER") == "1":
        inside_container = True
        config_dict = {}
        config_dict.update(mount_source=tmp_save_path)
        if pyfluent.USE_FILE_TRANSFER_SERVICE:
            solver_session = pyfluent.launch_fluent(
                processor_count=2,
                container_dict=config_dict,
                file_transfer_service=file_transfer_service,
            )
        else:
            solver_session = pyfluent.launch_fluent(
                processor_count=2,
                container_dict=config_dict,
            )
        container_workdir = PurePosixPath(pyfluent.CONTAINER_MOUNT_TARGET)
    else:
        inside_container = False
        solver_session = pyfluent.launch_fluent(processor_count=2, cwd=tmp_save_path)
    solver_session.file.read_case(file_name=import_file_name)
    solver_session.solution.run_calculation.iter_count = 100
    solver_session.tui.define.parameters.enable_in_TUI("yes")

    velocity_inlet = solver_session.tui.define.boundary_conditions.set.velocity_inlet
    velocity_inlet("inlet1", (), "vmag", "yes", "inlet1_vel", 1, "quit")
    velocity_inlet("inlet1", (), "temperature", "yes", "inlet1_temp", 300, "quit")
    velocity_inlet("inlet2", (), "vmag", "yes", "no", "inlet2_vel", 1, "quit")
    velocity_inlet("inlet2", (), "temperature", "yes", "no", "inlet2_temp", 350, "quit")

    solver_session.solution.report_definitions.surface["outlet-temp-avg"] = {}
    outlet_temp_avg = solver_session.solution.report_definitions.surface[
        "outlet-temp-avg"
    ]
    outlet_temp_avg.report_type = "surface-areaavg"
    outlet_temp_avg.field = "temperature"
    outlet_temp_avg.surface_names = ["outlet"]

    solver_session.solution.report_definitions.surface["outlet-vel-avg"] = {}
    outlet_vel_avg = solver_session.solution.report_definitions.surface[
        "outlet-vel-avg"
    ]
    outlet_vel_avg.report_type = "surface-areaavg"
    outlet_vel_avg.field = "velocity-magnitude"
    outlet_vel_avg.surface_names = ["outlet"]

    create_output_param = solver_session.tui.define.parameters.output_parameters.create
    create_output_param("report-definition", "outlet-temp-avg")
    create_output_param("report-definition", "outlet-vel-avg")

    solver_session.tui.solve.monitors.residual.criterion_type("0")

    case_path = Path(tmp_save_path) / "Static_Mixer_Parameters.cas.h5"
    if inside_container:
        write_case_path = str(container_workdir / "Static_Mixer_Parameters.cas.h5")
    else:
        write_case_path = str(case_path)
    solver_session.file.write(file_type="case", file_name=write_case_path)

    assert case_path.exists()
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
    assert base_dp.output_parameters["outlet-temp-avg-op"]() == pytest_approx(
        333.348727
    )
    assert base_dp.output_parameters["outlet-vel-avg-op"]() == pytest_approx(1.506855)
    dp_names = set([*study1.design_points.keys()])
    if solver_session.get_fluent_version() < FluentVersion.v251:
        study1.design_points.create_1()
        dp1_name = set([*study1.design_points.keys()]).difference(dp_names).pop()
        dp1 = study1.design_points[dp1_name]
    else:
        dp1 = study1.design_points.create()
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
    assert base_dp.output_parameters["outlet-temp-avg-op"]() == pytest_approx(
        333.348727
    )
    assert base_dp.output_parameters["outlet-vel-avg-op"]() == pytest_approx(1.506855)
    assert dp1.output_parameters["outlet-temp-avg-op"]() == pytest_approx(425.004045)
    assert dp1.output_parameters["outlet-vel-avg-op"]() == pytest_approx(2.029792)
    assert dp2.output_parameters["outlet-temp-avg-op"]() == pytest_approx(425.004045)
    assert dp2.output_parameters["outlet-vel-avg-op"]() == pytest_approx(2.029792)

    design_point_table = Path(tmp_save_path) / "design_point_table_study_1.csv"
    if inside_container:
        write_design_table = str(container_workdir / "design_point_table_study_1.csv")
    else:
        write_design_table = str(design_point_table)
    solver_session.parametric_studies.export_design_table(filepath=write_design_table)
    assert design_point_table.exists()

    study1.design_points.delete_design_points(design_points=[dp1.obj_name])
    assert len(study1.design_points) == 2
    study_names = set([*solver_session.parametric_studies.keys()])
    solver_session.parametric_studies.duplicate()
    assert len(solver_session.parametric_studies) == 2
    study2_name = (
        set([*solver_session.parametric_studies.keys()]).difference(study_names).pop()
    )
    study2 = solver_session.parametric_studies[study2_name]
    assert len(study2.design_points) == 2
    solver_session.parametric_studies[study2_name].rename("New Study")
    assert "New Study" in solver_session.parametric_studies
    del solver_session.parametric_studies[study1_name]
    assert len(solver_session.parametric_studies) == 1

    project_file_name = Path(tmp_save_path) / "static_mixer_study.flprj"
    if inside_container:
        write_project_file_name = str(container_workdir / "static_mixer_study.flprj")
    else:
        write_project_file_name = str(project_file_name)

    solver_session.file.parametric_project.save_as(
        project_filename=write_project_file_name
    )
    assert project_file_name.exists()
    solver_session.exit()

    if inside_container:
        if pyfluent.USE_FILE_TRANSFER_SERVICE:
            solver_session = pyfluent.launch_fluent(
                processor_count=2,
                container_dict=config_dict,
                file_transfer_service=file_transfer_service,
            )
        else:
            solver_session = pyfluent.launch_fluent(
                processor_count=2,
                container_dict=config_dict,
            )
    else:
        solver_session = pyfluent.launch_fluent(processor_count=2, cwd=tmp_save_path)

    solver_session.file.parametric_project.open(
        project_filename=write_project_file_name
    )
    solver_session.file.parametric_project.save()
    project_save_as_name = Path(tmp_save_path) / "static_mixer_study_save_as.flprj"
    if inside_container:
        write_project_save_as_name = str(
            container_workdir / "static_mixer_study_save_as.flprj"
        )
    else:
        write_project_save_as_name = str(project_save_as_name)

    solver_session.file.parametric_project.save_as(
        project_filename=write_project_save_as_name
    )
    assert project_save_as_name.exists()

    project_save_as_copy_name = (
        Path(tmp_save_path) / "static_mixer_study_save_copy_as.flprj"
    )
    if inside_container:
        write_project_save_as_copy_name = str(
            container_workdir / "static_mixer_study_save_copy_as.flprj"
        )
    else:
        write_project_save_as_copy_name = str(project_save_as_copy_name)
    solver_session.file.parametric_project.save_as_copy(
        project_filename=write_project_save_as_copy_name
    )
    assert project_save_as_copy_name.exists()

    archive_name = Path(tmp_save_path) / "static_mixer_study.flprz"
    if inside_container:
        write_archive_name = str(container_workdir / "static_mixer_study.flprz")
    else:
        write_archive_name = str(archive_name)
    solver_session.file.parametric_project.archive(archive_name=write_archive_name)
    assert archive_name.exists()
    solver_session.exit()


@pytest.mark.fluent_version(">=24.2")
def test_parameters_list_function(static_mixer_settings_session):
    solver = static_mixer_settings_session
    solver.tui.define.parameters.enable_in_TUI("yes")

    velocity_inlet = solver.tui.define.boundary_conditions.set.velocity_inlet
    velocity_inlet("inlet1", (), "vmag", "yes", "inlet1_vel", 1, "quit")
    velocity_inlet("inlet1", (), "temperature", "yes", "inlet1_temp", 300, "quit")
    velocity_inlet("inlet2", (), "vmag", "yes", "no", "inlet2_vel", 1, "quit")
    velocity_inlet("inlet2", (), "temperature", "yes", "no", "inlet2_temp", 350, "quit")

    solver.solution.report_definitions.surface["outlet-temp-avg"] = {}
    outlet_temp_avg = solver.solution.report_definitions.surface["outlet-temp-avg"]
    outlet_temp_avg.report_type = "surface-areaavg"
    outlet_temp_avg.field = "temperature"
    outlet_temp_avg.surface_names = ["outlet"]

    solver.solution.report_definitions.surface["outlet-vel-avg"] = {}
    outlet_vel_avg = solver.solution.report_definitions.surface["outlet-vel-avg"]
    outlet_vel_avg.report_type = "surface-areaavg"
    outlet_vel_avg.field = "velocity-magnitude"
    outlet_vel_avg.surface_names = ["outlet"]

    create_output_param = solver.tui.define.parameters.output_parameters.create
    create_output_param("report-definition", "outlet-temp-avg")
    create_output_param("report-definition", "outlet-vel-avg")

    # Create a unitless output parameter
    unitless_quantity = solver.settings.solution.report_definitions.surface.create(
        "temp-outlet-uniformity"
    )
    unitless_quantity.report_type = "surface-masswtui"
    unitless_quantity.field = "temperature"
    unitless_quantity.surface_names = ["outlet"]
    unitless_quantity.output_parameter = True

    input_parameters_list = solver.parameters.input_parameters.list()
    output_parameters_list = solver.parameters.output_parameters.list()
    assert input_parameters_list == {
        "inlet1_temp": [300.0, "K"],
        "inlet1_vel": [1.0, "m/s"],
        "inlet2_temp": [350.0, "K"],
        "inlet2_vel": [1.0, "m/s"],
    }
    assert output_parameters_list == {
        "outlet-temp-avg-op": [0.0, "K"],
        "outlet-vel-avg-op": [0.0, "m/s"],
        "temp-outlet-uniformity-op": [0.0, ""],
    }
