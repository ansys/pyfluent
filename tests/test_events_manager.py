from util.solver_workflow import new_solver_session  # noqa: F401

from ansys.fluent.core import examples
from ansys.fluent.core.streaming_services.events_streaming import Event


def test_receive_event_on_case_loaded(new_solver_session) -> None:

    def on_case_loaded(_1, _2):
        on_case_loaded.loaded = True

    on_case_loaded.loaded = False

    new_solver_session.events.register_callback(Event.CASE_LOADED, on_case_loaded)

    case_file_name = examples.download_file(
        "mixing_elbow_mul_ph.cas.h5",
        "pyfluent/file_session",
        return_without_path=False,
    )

    assert not on_case_loaded.loaded

    new_solver_session.file.read_case(file_name=case_file_name)

    assert on_case_loaded.loaded
