from pathlib import Path

import pytest

import ansys.fluent.core as pyfluent
from ansys.fluent.core import FluentVersion, MeshingEvent, SolverEvent, examples
from ansys.fluent.core.warnings import PyFluentDeprecationWarning


def test_receive_events_on_case_loaded(new_solver_session) -> None:

    def on_case_loaded_old(session_id, event_info):
        on_case_loaded_old.loaded = True

    on_case_loaded_old.loaded = False

    def on_case_loaded_old_with_args(x, y, session_id, event_info):
        on_case_loaded_old_with_args.state = dict(x=x, y=y)

    on_case_loaded_old_with_args.state = None

    def on_case_loaded(session, event_info):
        on_case_loaded.loaded = True
        if session.get_fluent_version() >= FluentVersion.v232:
            assert Path(event_info.case_file_name).name == Path(case_file_name).name
            with pytest.warns(PyFluentDeprecationWarning):
                assert Path(event_info.casefilepath).name == Path(case_file_name).name

    on_case_loaded.loaded = False

    def on_case_loaded_with_args_optional_first(x, y, session, event_info):
        on_case_loaded_with_args_optional_first.state = dict(x=x, y=y)

    on_case_loaded_with_args_optional_first.state = None

    def on_case_loaded_with_args(session, event_info, x, y):
        on_case_loaded_with_args.state = dict(x=x, y=y)

    on_case_loaded_with_args.state = None

    solver = new_solver_session

    solver.events.register_callback(SolverEvent.CASE_LOADED, on_case_loaded_old)

    solver.events.register_callback(
        SolverEvent.CASE_LOADED, on_case_loaded_old_with_args, 12, y=42
    )

    solver.events.register_callback(SolverEvent.CASE_LOADED, on_case_loaded)

    solver.events.register_callback(
        SolverEvent.CASE_LOADED, on_case_loaded_with_args_optional_first, 12, y=42
    )

    solver.events.register_callback(
        SolverEvent.CASE_LOADED, on_case_loaded_with_args, 12, y=42
    )

    case_file_name = examples.download_file(
        "mixing_elbow.cas.h5", "pyfluent/mixing_elbow"
    )

    assert not on_case_loaded_old.loaded
    assert not on_case_loaded.loaded
    assert not on_case_loaded_old_with_args.state
    assert not on_case_loaded_with_args_optional_first.state
    assert not on_case_loaded_with_args.state

    try:
        solver.settings.file.read_case(file_name=case_file_name)
    except AttributeError:
        solver.tui.file.read_case(case_file_name)

    assert on_case_loaded_old.loaded
    assert on_case_loaded.loaded
    assert on_case_loaded_old_with_args.state == dict(x=12, y=42)
    assert on_case_loaded_with_args_optional_first.state == dict(x=12, y=42)
    assert on_case_loaded_with_args.state == dict(x=12, y=42)


def test_receive_meshing_events_on_case_loaded(new_meshing_session) -> None:

    case_file_name = examples.download_file(
        "mixing_elbow.cas.h5", "pyfluent/mixing_elbow"
    )

    def on_case_loaded(session, event_info):
        on_case_loaded.loaded = True

    on_case_loaded.loaded = False

    meshing = new_meshing_session

    meshing.events.register_callback(MeshingEvent.CASE_LOADED, on_case_loaded)

    assert not on_case_loaded.loaded

    meshing.tui.file.read_case(case_file_name)

    # this is not working in meshing mode
    # assert on_case_loaded.loaded


@pytest.mark.fluent_version(">=23.1")
def test_iteration_ended_sync_event(static_mixer_case_session):
    solver = static_mixer_case_session
    solver.settings.solution.initialization.hybrid_initialize()
    count = 0

    def cb(session, event_info):
        assert event_info.index == session.scheme_eval.scheme_eval(
            "(get-current-iteration)"
        )
        nonlocal count
        count += 1

    cb_id = solver.events.register_callback(pyfluent.SolverEvent.ITERATION_ENDED, cb)
    solver.settings.solution.run_calculation.iterate(iter_count=10)
    assert count == 10
    solver.events.unregister_callback(cb_id)
    solver.settings.solution.run_calculation.iterate(iter_count=5)
    assert count == 10


@pytest.mark.fluent_version(">=23.1")
def test_iteration_ended_sync_event_multiple_connections(static_mixer_case_session):
    solver1 = static_mixer_case_session
    solver2 = pyfluent.connect_to_fluent(
        ip=solver1.connection_properties.ip,
        port=solver1.connection_properties.port,
        password=solver1.connection_properties.password,
    )
    solver1.settings.solution.initialization.hybrid_initialize()
    solver1_count = 0
    solver2_count = 0

    def solver1_cb(session, event_info):
        assert session == solver1
        if event_info.index % 2 == 0:
            nonlocal solver1_count
            solver1_count += 1

    def solver2_cb(session, event_info):
        assert session == solver2
        if event_info.index % 2 == 1:
            nonlocal solver2_count
            solver2_count += 1

    solver1.events.register_callback(pyfluent.SolverEvent.ITERATION_ENDED, solver1_cb)
    solver2.events.register_callback(pyfluent.SolverEvent.ITERATION_ENDED, solver2_cb)
    solver2.settings.solution.run_calculation.iterate(iter_count=5)
    assert solver1_count == 2
    assert solver2_count == 3


@pytest.mark.fluent_version(">=23.1")
def test_timestep_ended_sync_event(static_mixer_case_session):
    solver = static_mixer_case_session
    solver.settings.setup.general.solver.time = "unsteady-2nd-order"
    solver.settings.solution.initialization.hybrid_initialize()
    count = 0

    def cb(session, event_info):
        assert event_info.index == solver.rp_vars("time-step")
        nonlocal count
        count += 1

    cb_id = solver.events.register_callback(pyfluent.SolverEvent.TIMESTEP_ENDED, cb)
    solver.settings.solution.run_calculation.dual_time_iterate(
        time_step_count=10, max_iter_per_step=2
    )
    assert count == 10
    solver.events.unregister_callback(cb_id)
    solver.settings.solution.run_calculation.dual_time_iterate(
        time_step_count=5, max_iter_per_step=2
    )
    assert count == 10


@pytest.mark.fluent_version(">=23.1")
def test_sync_event_exception_in_callback(static_mixer_case_session, caplog):
    solver = static_mixer_case_session
    solver.settings.solution.initialization.hybrid_initialize()

    def cb(session, event_info):
        raise RuntimeError

    cb_id = solver.events.register_callback(pyfluent.SolverEvent.ITERATION_ENDED, cb)
    with caplog.at_level("ERROR", logger="pyfluent.networking"):
        solver.settings.solution.run_calculation.iterate(iter_count=10)
    assert (
        len(
            [
                record
                for record in caplog.records
                if "Error in callback" in record.message
            ]
        )
        == 10
    )
    caplog.clear()
    solver.events.unregister_callback(cb_id)
    with caplog.at_level("ERROR", logger="pyfluent.networking"):
        solver.settings.solution.run_calculation.iterate(iter_count=5)
    assert (
        len(
            [
                record
                for record in caplog.records
                if "Error in callback" in record.message
            ]
        )
        == 0
    )
