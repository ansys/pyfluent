
from util.solver_workflow import new_solver_session_no_transcript  # noqa: F401

from ansys.fluent.core.examples import download_file


def test_rp_var(new_solver_session_no_transcript) -> None:
    case_path = download_file("Static_Mixer_main.cas.h5", "pyfluent/static_mixer")
    solver = new_solver_session_no_transcript
    solver.file.read(file_type="case", file_name=case_path)
    rp_vars = solver.rp_vars
    before_init_mod = rp_vars.get_var("strategy/solution-strategy/before-init-modification")
    assert before_init_mod[1][1][1] == ("value", False)
    before_init_mod[1][1][1] = ("value", True)
    rp_vars.set_var(
        "strategy/solution-strategy/before-init-modification",
        before_init_mod
        )
    before_init_mod_2 = rp_vars.get_var("strategy/solution-strategy/before-init-modification")
    assert before_init_mod_2[1][1][1] == ("value", True)