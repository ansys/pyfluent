
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
    rp_vars(
        "number-of-iterations",
        iter_count
        )
    assert iter_count == rp_vars("number-of-iterations")

    # complex list structure
    before_init_mod = rp_vars("strategy/solution-strategy/before-init-modification")
    assert before_init_mod[1][1][1] == ("value", False)
    before_init_mod[1][1][1] = ("value", True)
    rp_vars(
        "strategy/solution-strategy/before-init-modification",
        before_init_mod
        )
    before_init_mod_2 = rp_vars("strategy/solution-strategy/before-init-modification")
    assert before_init_mod_2[1][1][1] == ("value", True)

    # all vars
    all_vars = rp_vars()
    assert len(all_vars) == pytest.approx(9000, 10)

    # refresh
    solver.file.write(file_type="case", file_name=case_path)
    solver.file.read(file_type="case", file_name=case_path)

    # all vars again
    all_vars = rp_vars()
    assert len(all_vars) == pytest.approx(9000, 20)

    # case reader comparison
    case = CaseReader(case_filepath=case_path)
    case_vars = case.rp_vars()
    assert len(case_vars) == pytest.approx(9000, 450)