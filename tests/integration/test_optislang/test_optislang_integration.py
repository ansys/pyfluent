import os
from pathlib import Path
import shutil

import pytest
from util.meshing_workflow import mixing_elbow_geometry  # noqa: F401

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples


@pytest.mark.nightly
@pytest.mark.codegen_required
@pytest.mark.fluent_version("latest")
def test_simple_solve(load_mixing_elbow_param_case_dat):
    """Use case 1: This optiSLang integration test performs these steps.

    - Reads a case file with and without data file
    - Gets input and output parameters and creates dictionary
    - Sets a variation on input parameters
    - Solve
    - Reread data

    This test queries the following using PyTest:
    - Session health
    - Input parameters
    - Output parameters
    """
    # Step 1: Setup logging
    import logging

    logging.root.setLevel("ERROR")

    # Step 2: Launch fluent session and read case file with and without data file
    solver_session = load_mixing_elbow_param_case_dat
    assert solver_session.health_check_service.is_serving
    case_path = examples.path("elbow_param.cas.h5")
    solver_session.tui.file.read_case_data(case_path)

    # Step 3: Get input and output parameters and create a dictionary
    from ansys.fluent.core.services.scheme_eval import Symbol

    input_parameters = solver_session.scheme_eval.eval(
        (Symbol("list-input-parameters"),)
    )
    output_parameters = solver_session.scheme_eval.eval(
        (Symbol("list-output-parameters"),)
    )
    solver_session.tui.file.read_case(case_path)

    # TODO: Remove the if condition after a stable version of 23.1 is available and update the commands as required.
    if float(solver_session.get_fluent_version().value[:-2]) < 23.0:
        input_parameters = input_parameters["inlet2_temp"]
        output_parameters = output_parameters["outlet_temp-op"]

        # Step 4: Set a variation on these input parameters
        # variations/designs are generated by optiSLang based on
        # algorithm selected
        solver_session.tui.define.parameters.input_parameters.edit(
            "inlet2_temp", "inlet2_temp", 600
        )
        solver_session.tui.file.write_case("design_elbow_param.cas.h5")

        # Step 5: Solve
        solver_session.tui.solve.initialize.initialize_flow()

        # check if solution is steady or transient
        workflow = solver_session.scheme_eval.string_eval("(rp-unsteady?)")

        # iterate workflow
        if workflow == "#t":
            solver_session.tui.solve.dual_time_iterate()
        else:
            solver_session.tui.solve.iterate()

        convergence = solver_session.scheme_eval.string_eval(
            "(rpgetvar 'solution/converged?)"
        )

        # solution output (test conditional statement)
        if convergence == "#f":  # -> let user know
            print("Failed to converge")
        else:
            print("Solution is converged")

        assert convergence == "#t", "Solution failed to converge"

        # Step 6: Read the data again from the case and data file
        solver_session.tui.file.read_case_data(case_path)
        input_parameters2 = solver_session.scheme_eval.eval(
            (Symbol("list-input-parameters"),)
        )
        output_parameters2 = solver_session.scheme_eval.eval(
            (Symbol("list-output-parameters"),)
        )
        input_parameters2 = input_parameters2["inlet2_temp"]
        output_parameters2 = output_parameters2["outlet_temp-op"]
        assert input_parameters[0] == input_parameters2[0]
        assert output_parameters[0] == output_parameters2[0]
        solver_session.exit()


@pytest.mark.nightly
@pytest.mark.codegen_required
@pytest.mark.fluent_version("latest")
def test_generate_read_mesh(mixing_elbow_geometry):
    """Use case 2: This optiSLang integration test performs these steps.

    - Launch Fluent in Meshing Mode
    - Generate mesh with default workflow settings
    - Read created mesh file
    - Switch to solution and write case file

    This test queries the following using PyTest:
    - Session health
    """
    # Step 1: Setup logging
    import logging

    logging.root.setLevel("ERROR")

    # Step 2: Launch fluent session in meshing mode
    meshing = pyfluent.launch_fluent(
        mode="meshing", precision="double", processor_count=2
    )
    assert meshing.health_check_service.is_serving
    temporary_resource_path = os.path.join(
        pyfluent.EXAMPLES_PATH, "test_generate_read_mesh_resources"
    )
    if os.path.exists(temporary_resource_path):
        shutil.rmtree(temporary_resource_path, ignore_errors=True)
    if not os.path.exists(temporary_resource_path):
        os.mkdir(temporary_resource_path)

    # TODO: Remove the if condition after a stable version of 23.1 is available and update the commands as required.
    if float(meshing.get_fluent_version().value[:-2]) < 23.0:
        # Step 3 Generate mesh from geometry with default workflow settings
        meshing.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")
        geo_import = meshing.workflow.TaskObject["Import Geometry"]
        geo_import.Arguments = dict(FileName=mixing_elbow_geometry)
        geo_import.Execute()
        meshing.workflow.TaskObject["Generate the Volume Mesh"].Execute()
        meshing.tui.mesh.check_mesh()
        gz_path = str(Path(temporary_resource_path) / "default_mesh.msh.gz")
        h5_path = str(Path(temporary_resource_path) / "default_mesh.msh.h5")
        meshing.tui.file.write_mesh(gz_path)
        meshing.tui.file.write_mesh(h5_path)
        assert (Path(temporary_resource_path) / "default_mesh.msh.gz").exists() == True
        assert (Path(temporary_resource_path) / "default_mesh.msh.h5").exists() == True

        # Step 4: use created mesh file - .msh.gz/.msh.h5
        meshing.tui.file.read_mesh(gz_path, "ok")
        meshing.tui.file.read_mesh(h5_path, "ok")

        # Step 5: Switch to solution and Write case file
        solver = meshing.switch_to_solver()
        solver.tui.solve.initialize.hyb_initialization()
        gz_path = str(Path(temporary_resource_path) / "default_case.cas.gz")
        h5_path = str(Path(temporary_resource_path) / "default_case.cas.h5")
        write_case = solver.tui.file.write_case
        write_case(gz_path)
        write_case(h5_path)
        assert (Path(temporary_resource_path) / "default_case.cas.gz").exists() == True
        assert (Path(temporary_resource_path) / "default_case.cas.h5").exists() == True
        solver.exit()
        shutil.rmtree(temporary_resource_path, ignore_errors=True)
