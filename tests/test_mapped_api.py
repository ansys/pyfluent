import pytest
from util import create_datamodel_root_in_server

rules_str = (
    "RULES:\n"
    "  STRING: X\n"
    "    allowedValues = yes, no\n"
    "    logicalMapping = True, False\n"
    "  END\n"
    "  STRING: Y\n"
    '    allowedValues = \\"1\\", \\"2\\", \\"3\\"\n'
    '    default = \\"2\\"\n'
    "    isNumerical = True\n"
    "  END\n"
    "  INTEGER: Z\n"
    "  END\n"
    "  SINGLETON: ROOT\n"
    "    members = A\n"
    "    commands = C, D\n"
    "    SINGLETON: A\n"
    "      members = X, Y, Z\n"
    "    END\n"
    "    COMMAND: C\n"
    "      arguments = X\n"
    "      functionName = CFunc\n"
    "    END\n"
    "    COMMAND: D\n"
    "      arguments = X\n"
    "      functionName = CFunc\n"
    "      APIName = dd\n"
    "    END\n"
    "  END\n"
    "END\n"
)

rules_str_caps = (
    "RULES:\n"
    "  STRING: X\n"
    "    allowedValues = Yes, No\n"
    "    default = No\n"
    "    logicalMapping = True, False\n"
    "  END\n"
    "  SINGLETON: ROOT\n"
    "    members = A\n"
    "    SINGLETON: A\n"
    "      members = X\n"
    "    END\n"
    "  END\n"
    "END\n"
)


def get_static_info_value(static_info, type_path):
    for p in type_path.removeprefix("/").split("/"):
        static_info = static_info[p]
    return static_info


def get_state_from_remote_app(session, app_name, type_path):
    return session.scheme_eval.scheme_eval(
        f'(state/object/get-state (state/object/find-child (state/find-root "{app_name}") "{type_path}"))'
    )


def get_error_state_message_from_remote_app(session, app_name, type_path):
    return session.scheme_eval.scheme_eval(
        f'(state/object/get-error-state-message (state/object/find-child (state/find-root "{app_name}") "{type_path}"))'
    )


def test_datamodel_api_bool_for_str_has_correct_type(
    datamodel_api_version_new, new_solver_session
):
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, rules_str, app_name)
    service = solver._se_service
    static_info = service.get_static_info("test")
    assert (
        get_static_info_value(static_info, "/singletons/A/parameters/X/type")
        == "Logical"
    )
    cmd_args = get_static_info_value(static_info, "/commands/C/commandinfo/args")
    arg0 = cmd_args[0]
    assert arg0["type"] == "Logical"


def test_datamodel_api_set_bool_for_str(datamodel_api_version_new, new_solver_session):
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, rules_str, app_name)
    service = solver._se_service
    service.set_state(app_name, "/A/X", "yes")
    assert service.get_state(app_name, "/A/X") is True
    assert get_state_from_remote_app(solver, app_name, "/A/X") == "yes"


def test_datamodel_api_set_bool_nested_for_str(
    datamodel_api_version_new, new_solver_session
):
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, rules_str, app_name)
    service = solver._se_service
    service.set_state(app_name, "/A", {"X": True})
    assert service.get_state(app_name, "/A/X") is True
    assert get_error_state_message_from_remote_app(solver, app_name, "/A/X") is None


def test_datamodel_api_get_set_bool_for_str_with_flexible_strs_no_errors(
    datamodel_api_version_new, new_solver_session
):
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, rules_str_caps, app_name)
    service = solver._se_service
    service.set_state(app_name, "/A/X", True)
    assert service.get_state(app_name, "/A/X") is True
    assert get_error_state_message_from_remote_app(solver, app_name, "/A/X") is None


def test_datamodel_api_get_attrs_bool_for_str(
    datamodel_api_version_new, new_solver_session
):
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, rules_str_caps, app_name)
    service = solver._se_service
    # assert service.get_attribute_value(app_name, "/A/Z", "allowedValues") is None  # TODO: issue in accessing the object
    assert service.get_attribute_value(app_name, "/A/X", "allowedValues") is None


def test_datamodel_api_get_and_set_int_for_str(
    datamodel_api_version_new, new_solver_session
):
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, rules_str, app_name)
    service = solver._se_service
    service.set_state(app_name, "/A/Y", 1)
    assert service.get_state(app_name, "/A/Y") == 1
    assert get_error_state_message_from_remote_app(solver, app_name, "/A/Y") is None


# TODO: what are the equivalent of following tests in Python?
# testPopulateMappingAttrTablePaths
# testMapAPIStateToDM
# testMapDMStateToAPI
# testMapNestedAPIStateToDM
# testUpdateStateDictWithMapping


def test_state_of_command_args_with_mapping(
    datamodel_api_version_new, new_solver_session
):
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, rules_str, app_name)
    service = solver._se_service
    c_name = service.create_command_arguments(app_name, "/", "C")
    with pytest.raises(RuntimeError):
        service.set_state(app_name, f"/C:{c_name}/X", False)
    assert service.get_state(app_name, f"/C:{c_name}") == {"X": None}
    service.set_state(app_name, f"/C:{c_name}", {"X": False})
    assert service.get_state(app_name, f"/C:{c_name}") == {"X": False}
    service.set_state(app_name, f"/C:{c_name}", {"X": True})
    assert service.get_state(app_name, f"/C:{c_name}") == {"X": True}
