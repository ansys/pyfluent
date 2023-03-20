import pytest

import ansys.fluent.core as pyfluent


@pytest.mark.dev
@pytest.mark.fluent_231
def test_icing_session(with_launching_container):
    icing_session = pyfluent.launch_fluent(mode=pyfluent.LaunchMode.SOLVER_ICING)
    assert "icing" in dir(icing_session)
