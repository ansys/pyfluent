from ansys.fluent.core.services.scheme_eval import SchemeEval, SchemeEvalService


class ApiUpgradeAdvisor:
    def __init__(self, channel, metadata, fluent_error_state, version, mode):
        self._scheme_eval = SchemeEval(
            SchemeEvalService(channel, metadata, fluent_error_state)
        ).scheme_eval
        self._version = version
        self._mode = mode

    def __enter__(self):
        if self._version >= "23.1" and self._mode == "solver":
            self._scheme_eval("(define journal-str-port (open-output-string))")
            self._scheme_eval("(api-echo-python-port journal-str-port)")
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self._version >= "23.1" and self._mode == "solver":
            self._scheme_eval("(api-unecho-python-port journal-str-port)")
            journal_str = self._scheme_eval(
                "(close-output-port journal-str-port)"
            ).strip()
            if (
                journal_str.startswith("solver.")
                and not journal_str.startswith("solver.tui")
                and not journal_str.startswith("solver.execute_tui")
            ):
                print(
                    "The following settings API could also be used to execute the above command:"
                )
                print(f"<solver_session>.{journal_str.removeprefix('solver.')}")
