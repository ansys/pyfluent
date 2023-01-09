
from util.solver_workflow import new_solver_session_no_transcript  # noqa: F401

from ansys.fluent.core.examples import download_file


def test_get_and_set_rp_vars(new_solver_session_no_transcript) -> None:

    case_path = download_file("Static_Mixer_main.cas.h5", "pyfluent/static_mixer")
    solver = new_solver_session_no_transcript
    solver.file.read(file_type="case", file_name=case_path)
    rp_var = solver.rp_var

    # simple integer
    iter_count = 54321
    rp_var(
        "number-of-iterations",
        iter_count
        )
    assert iter_count == rp_var("number-of-iterations")

    # complex list structure
    before_init_mod = rp_var("strategy/solution-strategy/before-init-modification")
    assert before_init_mod[1][1][1] == ("value", False)
    before_init_mod[1][1][1] = ("value", True)
    rp_var(
        "strategy/solution-strategy/before-init-modification",
        before_init_mod
        )
    before_init_mod_2 = rp_var("strategy/solution-strategy/before-init-modification")
    assert before_init_mod_2[1][1][1] == ("value", True)