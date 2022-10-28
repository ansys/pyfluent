from pathlib import Path

import pytest

import ansys.fluent.core as pyfluent


@pytest.mark.optislang
@pytest.mark.integration
def test_simple_solve(load_mixing_elbow_param_case_dat):

    """
    This optiSLang integration test performs these steps

    - Reads a case file with and without data file
    - Gets input and output parameters and creates dictionary
    - Sets a variation on input parameters
    - Solve
    - Reread data

    This test queries the following using PyTest:
    - Input parameters
    - Output parameters
    """

    # Step 1: Setup logging
    pyfluent.set_log_level("ERROR")

    # Step 2: Launch fluent session and read case file with and without data file
    solver_session = load_mixing_elbow_param_case_dat
    assert solver_session.check_health() == "SERVING"
    case_path = str(Path(pyfluent.EXAMPLES_PATH) / "elbow_param.cas.h5")
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
    if float(solver_session.get_fluent_version()[:-2]) < 23.0:
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
