import ansys.fluent.core as pyfluent


def test_icing_session(with_launching_container):
    icing_session = pyfluent.launch_fluent(mode=pyfluent.LaunchModes.SOLVER_ICING)
    assert "icing" in dir(icing_session)
