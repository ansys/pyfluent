import uuid


def create_datamodel_root_in_server(
    session, rules_str, app_name, root_cls=None
) -> None:
    rules_file_name = f"{uuid.uuid4()}.fdl"
    session.scheme_eval.scheme_eval(
        f'(with-output-to-file "{rules_file_name}" (lambda () (format "~a" "{rules_str}")))',
    )
    session.scheme_eval.scheme_eval(
        f'(state/register-new-state-engine "{app_name}" "{rules_file_name}")'
    )
    session.scheme_eval.scheme_eval(f'(remove-file "{rules_file_name}")')
    assert session.scheme_eval.scheme_eval(f'(state/find-root "{app_name}")') > 0
    if root_cls:
        return root_cls(session._se_service, app_name, [])
