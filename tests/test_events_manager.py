from util.solver_workflow import new_solver_session  # noqa: F401

from ansys.fluent.core import examples
from ansys.fluent.core.streaming_services.events_streaming import Event


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

    new_solver_session.events.register_callback(Event.CASE_LOADED, on_case_loaded_old)

    new_solver_session.events.register_callback(
        Event.CASE_LOADED, on_case_loaded_old_with_args, 12, y=42
    )

    new_solver_session.events.register_callback(Event.CASE_LOADED, on_case_loaded)

    new_solver_session.events.register_callback(
        Event.CASE_LOADED, on_case_loaded_with_args, 12, y=42
    )

    case_file_name = examples.download_file(
        "mixing_elbow_mul_ph.cas.h5",
        "pyfluent/file_session",
        return_without_path=False,
    )

    assert not on_case_loaded_old.loaded
    assert not on_case_loaded.loaded
    assert not on_case_loaded_old_with_args.state
    assert not on_case_loaded_with_args.state

    new_solver_session.file.read_case(file_name=case_file_name)

    assert on_case_loaded_old.loaded
    assert on_case_loaded.loaded
    assert on_case_loaded_old_with_args.state == dict(x=12, y=42)
    assert on_case_loaded_with_args.state == dict(x=12, y=42)
