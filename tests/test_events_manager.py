from ansys.fluent.core import MeshingEvent, SolverEvent, examples


def test_receive_events_on_case_loaded(new_solver_session) -> None:

    def on_case_loaded_old(session_id, event_info):
        on_case_loaded_old.loaded = True

    on_case_loaded_old.loaded = False

    def on_case_loaded_old_with_args(x, y, session_id, event_info):
        on_case_loaded_old_with_args.state = dict(x=x, y=y)

    on_case_loaded_old_with_args.state = None

    def on_case_loaded(session, event_info):
        on_case_loaded.loaded = True

    on_case_loaded.loaded = False

    def on_case_loaded_with_args(x, y, session, event_info):
        on_case_loaded_with_args.state = dict(x=x, y=y)

    on_case_loaded_with_args.state = None

    solver = new_solver_session

    solver.events.register_callback(SolverEvent.CASE_LOADED, on_case_loaded_old)

    solver.events.register_callback(
        SolverEvent.CASE_LOADED, on_case_loaded_old_with_args, 12, y=42
    )

    solver.events.register_callback(SolverEvent.CASE_LOADED, on_case_loaded)

    solver.events.register_callback(
        SolverEvent.CASE_LOADED, on_case_loaded_with_args, 12, y=42
    )

    case_file_name = examples.download_file(
        "mixing_elbow.cas.h5", "pyfluent/mixing_elbow"
    )

    assert not on_case_loaded_old.loaded
    assert not on_case_loaded.loaded
    assert not on_case_loaded_old_with_args.state
    assert not on_case_loaded_with_args.state

    try:
        solver.settings.file.read_case(file_name=case_file_name)
    except AttributeError:
        solver.tui.file.read_case(case_file_name)

    assert on_case_loaded_old.loaded
    assert on_case_loaded.loaded
    assert on_case_loaded_old_with_args.state == dict(x=12, y=42)
    assert on_case_loaded_with_args.state == dict(x=12, y=42)


def test_receive_meshing_events_on_case_loaded(new_meshing_session) -> None:

    def on_case_loaded(session, event_info):
        on_case_loaded.loaded = True

    on_case_loaded.loaded = False

    meshing = new_meshing_session

    meshing.events.register_callback(MeshingEvent.CASE_LOADED, on_case_loaded)

    case_file_name = examples.download_file(
        "mixing_elbow.cas.h5", "pyfluent/mixing_elbow"
    )

    assert not on_case_loaded.loaded

    meshing.tui.file.read_case(case_file_name)

    # this is not working in meshing mode
    # assert on_case_loaded.loaded
