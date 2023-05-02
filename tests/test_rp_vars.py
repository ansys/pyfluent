import pytest
from util.solver_workflow import new_solver_session_no_transcript  # noqa: F401

from ansys.fluent.core.examples import download_file
from ansys.fluent.core.filereader.casereader import CaseReader


def test_get_and_set_rp_vars(new_solver_session_no_transcript) -> None:
    case_path = download_file("Static_Mixer_main.cas.h5", "pyfluent/static_mixer")
    solver = new_solver_session_no_transcript
    solver.file.read(file_type="case", file_name=case_path)
    rp_vars = solver.rp_vars

    # simple integer
    iter_count = 54321
    rp_vars("number-of-iterations", iter_count)
    assert iter_count == rp_vars("number-of-iterations")

    # complex list structure
    before_init_mod = rp_vars("strategy/solution-strategy/before-init-modification")
    assert before_init_mod[1][1][1] == ("value", False)
    before_init_mod[1][1][1] = ("value", True)
    rp_vars("strategy/solution-strategy/before-init-modification", before_init_mod)
    before_init_mod_2 = rp_vars("strategy/solution-strategy/before-init-modification")
    assert before_init_mod_2[1][1][1] == ("value", True)


@pytest.mark.fluent_231
def test_get_all_rp_vars(new_solver_session_no_transcript) -> None:
    case_path = download_file("Static_Mixer_main.cas.h5", "pyfluent/static_mixer")
    solver = new_solver_session_no_transcript
    solver.file.read(file_type="case", file_name=case_path)
    rp_vars = solver.rp_vars
    # all vars
    all_vars = rp_vars()
    assert len(all_vars) == pytest.approx(9000, 10)

    # refresh
    solver.file.write(file_type="case", file_name=case_path)
    solver.file.read(file_type="case", file_name=case_path)

    # all vars again
    all_vars = rp_vars()
    assert len(all_vars) == pytest.approx(9000, 20)

    # CaseFile comparison
    case = CaseReader(case_filepath=case_path)
    case_vars = case.rp_vars()
    assert len(case_vars) == pytest.approx(9000, 450)


@pytest.mark.dev
@pytest.mark.fluent_232
def test_rp_vars_allowed_values(new_solver_session_no_transcript) -> None:
    solver = new_solver_session_no_transcript
    rp_vars = solver.rp_vars

    assert rp_vars("number-of-iterations") == 0

    with pytest.raises(RuntimeError) as msg:
        rp_vars("number-of-iterat")

    assert (
        msg.value.args[0] == "number-of-iterat is not an allowed rp-vars name.\n"
        "The most similar names are: number-of-iterations, "
        "number-of-time-steps, lb/number-of-timesteps, "
        "number-of-samples, gpuapp/total-number-of-subiterations."
    )

    assert "number-of-iterations" in rp_vars.allowed_values()
