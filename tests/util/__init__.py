import uuid


def create_datamodel_root_in_server(session, rules_str, root_cls=None) -> None:
    rules_file_name = f"{uuid.uuid4()}.fdl"
    session.scheme_eval.scheme_eval(
        f'(with-output-to-file "{rules_file_name}" (lambda () (format "~a" "{rules_str}")))',
    )
    # TODO: Pass appname via argument
    session.scheme_eval.scheme_eval(
        f'(state/register-new-state-engine "test" "{rules_file_name}")'
    )
    session.scheme_eval.scheme_eval(f'(remove-file "{rules_file_name}")')
    assert session.scheme_eval.scheme_eval('(state/find-root "test")') > 0
    if root_cls:
        return root_cls(session._se_service, "test", [])
