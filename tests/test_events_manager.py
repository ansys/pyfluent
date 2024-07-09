from util.solver_workflow import new_solver_session  # noqa: F401

from ansys.fluent.core import examples
from ansys.fluent.core.streaming_services.events_streaming import Event


def test_receive_events_on_case_loaded(new_solver_session) -> None:

    def on_case_loaded_old(session_id, event_info):
        on_case_loaded_old.loaded = True

    on_case_loaded_old.loaded = False

    def on_case_loaded(session, event_info):
        on_case_loaded.loaded = True

    on_case_loaded.loaded = False

    new_solver_session.events.register_callback(Event.CASE_LOADED, on_case_loaded_old)

    new_solver_session.events.register_callback(
        Event.CASE_LOADED, on_case_loaded, callback_has_new_signature=True
    )

    case_file_name = examples.download_file(
        "mixing_elbow_mul_ph.cas.h5",
        "pyfluent/file_session",
        return_without_path=False,
    )

    assert not on_case_loaded_old.loaded
    assert not on_case_loaded.loaded

    new_solver_session.file.read_case(file_name=case_file_name)

    assert on_case_loaded_old.loaded
    assert on_case_loaded.loaded
