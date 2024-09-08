import pytest

import ansys.fluent.core as pyfluent


@pytest.mark.fluent_version(">=24.2")
def test_icing_session():
    aero_session = pyfluent.launch_fluent(mode=pyfluent.FluentMode.SOLVER_AERO)
    assert "aero" in dir(aero_session)
