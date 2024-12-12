import time

import pytest
from util import create_datamodel_root_in_server

from ansys.fluent.core.services.datamodel_se import (
    PyCommand,
    PyMenu,
    PyNumerical,
    PyTextual,
)
from ansys.fluent.core.utils.execution import timeout_loop

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


# TODO: Generate the class hierarchy via codegen
class rules_cls(PyMenu):
    def __init__(self, service, rules, path):
        self.A = self.__class__.A(service, rules, path + [("A", "")])
        self.C = self.__class__.C(service, rules, path + [("C", "")])
        self.D = self.__class__.D(service, rules, path + [("D", "")])
        super().__init__(service, rules, path)

    class A(PyMenu):
        def __init__(self, service, rules, path):
            self.X = self.__class__.X(service, rules, path + [("X", "")])
            self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
            self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
            super().__init__(service, rules, path)

        class X(PyTextual):
            pass

        class Y(PyTextual):
            pass

        class Z(PyNumerical):
            pass

    class C(PyCommand):
        pass

    class D(PyCommand):
        pass


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


def register_external_function_in_remote_app(session, app_name, func_name):
    session.scheme_eval.scheme_eval(
        f'(state/register-external-fn "{app_name}" "{func_name}" (lambda (obj . args) (car args)) (cons "Variant" (list "ModelObject" "Variant")))'
    )


def test_execute_command_with_args_mapping(
    datamodel_api_version_new, new_solver_session
):
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, rules_str, app_name)
    service = solver._se_service
    register_external_function_in_remote_app(solver, app_name, "CFunc")
    result = service.execute_command(app_name, "/", "C", {"X": True})
    assert result == "yes"


def test_execute_command_with_args_and_path_mapping(
    datamodel_api_version_new, new_solver_session
):
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, rules_str, app_name)
    service = solver._se_service
    register_external_function_in_remote_app(solver, app_name, "CFunc")
    result = service.execute_command(app_name, "/", "dd", {"X": True})
    assert result == "yes"


def test_execute_query_with_args_mapping(datamodel_api_version_new, new_solver_session):
    rules_str = (
        "RULES:\n"
        "  STRING: X\n"
        "    allowedValues = yes, no\n"
        "    logicalMapping = True, False\n"
        "  END\n"
        "  SINGLETON: ROOT\n"
        "    queries = Q\n"
        "    QUERY: Q\n"
        "      arguments = X\n"
        "      functionName = QFunc\n"
        "    END\n"
        "  END\n"
        "END\n"
    )
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, rules_str, app_name)
    service = solver._se_service
    register_external_function_in_remote_app(solver, app_name, "QFunc")
    result = service.execute_query(app_name, "/", "Q", {"X": True})
    assert result == "yes"


def test_get_mapped_attr(datamodel_api_version_new, new_solver_session):
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, rules_str, app_name)
    service = solver._se_service
    assert service.get_attribute_value(app_name, "/A/X", "allowedValues") is None
    assert service.get_attribute_value(app_name, "/A/Y", "allowedValues") is None
    assert service.get_attribute_value(app_name, "/A/Y", "min") == 1
    assert service.get_attribute_value(app_name, "/A/Y", "max") == 3
    assert service.get_attribute_value(app_name, "/A/Y", "default") == 2


def test_get_mapped_attr_defaults(datamodel_api_version_new, new_solver_session):
    rules_str = (
        "RULES:\n"
        "  STRING: X\n"
        "    allowedValues = yes, no\n"
        "    default = no\n"
        "    logicalMapping = True, False\n"
        "  END\n"
        "  STRING: Y\n"
        '    allowedValues = \\"1\\", \\"2\\", \\"3\\"\n'
        '    default = \\"2\\"\n'
        "    isNumerical = True\n"
        "  END\n"
        "  INTEGER: Z\n"
        "    default = 42\n"
        "  END\n"
        "  SINGLETON: ROOT\n"
        "    members = A\n"
        "    SINGLETON: A\n"
        "      members = X, Y, Z\n"
        "    END\n"
        "  END\n"
        "END\n"
    )
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, rules_str, app_name)
    service = solver._se_service
    assert service.get_attribute_value(app_name, "/A/X", "default") is False
    assert service.get_attribute_value(app_name, "/A/Y", "default") == 2
    assert service.get_attribute_value(app_name, "/A/Z", "default") == 42


def test_get_mapped_enum_attr(datamodel_api_version_new, new_solver_session):
    rules_str = (
        "RULES:\n"
        "  STRING: X\n"
        "    allowedValues = ijk, lmn\n"
        "    default = lmn\n"
        "    enum = green, yellow\n"
        "  END\n"
        "  SINGLETON: ROOT\n"
        "    members = A\n"
        "    SINGLETON: A\n"
        "      members = X\n"
        "    END\n"
        "  END\n"
        "END\n"
    )
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, rules_str, app_name)
    service = solver._se_service
    assert service.get_attribute_value(app_name, "/A/X", "allowedValues") == [
        "green",
        "yellow",
    ]
    assert service.get_attribute_value(app_name, "/A/X", "default") == "yellow"


def test_get_mapped_dynamic_enum_attr(datamodel_api_version_new, new_solver_session):
    rules_str = (
        "RULES:\n"
        "  LOGICAL: B\n"
        "    default = True\n"
        "  END\n"
        "  STRING: X\n"
        '    allowedValues = IF($../B, (\\"ijk\\", \\"lmn\\"), (\\"ijk\\", \\"lmn\\", \\"opq\\"))\n'
        "    default = lmn\n"
        '    enum = IF($../B, (\\"green\\", \\"yellow\\"), (\\"green\\", \\"yellow\\", \\"blue\\"))\n'
        "  END\n"
        "  SINGLETON: ROOT\n"
        "    members = A\n"
        "    SINGLETON: A\n"
        "      members = B, X\n"
        "    END\n"
        "  END\n"
        "END\n"
    )
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, rules_str, app_name)
    service = solver._se_service
    assert service.get_attribute_value(app_name, "/A/X", "allowedValues") == [
        "green",
        "yellow",
    ]
    assert service.get_attribute_value(app_name, "/A/X", "default") == "yellow"


def test_get_mapped_command_attr(datamodel_api_version_new, new_solver_session):
    rules_str = (
        "RULES:\n"
        "  STRING: X\n"
        "    allowedValues = yes, no\n"
        "    default = no\n"
        "    logicalMapping = True, False\n"
        "  END\n"
        "  STRING: Y\n"
        '    allowedValues = \\"1\\", \\"2\\", \\"3\\"\n'
        '    default = \\"2\\"\n'
        "    isNumerical = True\n"
        "  END\n"
        "  INTEGER: Z\n"
        "    default = 42\n"
        "  END\n"
        "  SINGLETON: ROOT\n"
        "    commands = C\n"
        "    COMMAND: C\n"
        "      arguments = X, Y, Z\n"
        "    END\n"
        "  END\n"
        "END\n"
    )
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, rules_str, app_name)
    service = solver._se_service
    c_name = service.create_command_arguments(app_name, "/", "C")
    # TODO: Attribute query at command argument level is not working
    assert (
        service.get_attribute_value(app_name, f"/C:{c_name}", "X/allowedValues") is None
    )
    assert (
        service.get_attribute_value(app_name, f"/C:{c_name}", "Y/allowedValues") is None
    )
    assert service.get_attribute_value(app_name, f"/C:{c_name}", "Y/min") == 1
    assert service.get_attribute_value(app_name, f"/C:{c_name}", "Y/max") == 3
    assert service.get_attribute_value(app_name, f"/C:{c_name}", "X/default") is False
    assert service.get_attribute_value(app_name, f"/C:{c_name}", "Y/default") == 2
    assert service.get_attribute_value(app_name, f"/C:{c_name}", "Z/default") == 42


def test_on_changed_is_mapped(datamodel_api_version_new, new_solver_session):
    solver = new_solver_session
    app_name = "test"
    root = create_datamodel_root_in_server(solver, rules_str, app_name, rules_cls)
    service = solver._se_service

    called = 0
    state = None
    called_obj = 0
    state_obj = None

    def on_changed(value):
        nonlocal called
        nonlocal state
        state = value()
        called += 1

    def on_changed_obj(value):
        nonlocal called_obj
        nonlocal state_obj
        state_obj = value()
        called_obj += 1

    subscription = service.add_on_changed(app_name, "/A/X", root.A.X, on_changed)
    subscription_obj = service.add_on_changed(app_name, "/A", root.A, on_changed_obj)

    assert called == 0
    assert state is None
    assert called_obj == 0
    assert state_obj is None

    service.set_state(app_name, "/A/X", True)
    timeout_loop(lambda: called == 1, timeout=5)
    assert called == 1
    assert state is True
    assert called_obj == 1
    assert state_obj == {"X": True, "Y": 2, "Z": None}

    service.set_state(app_name, "/A/X", False)
    timeout_loop(lambda: called == 2, timeout=5)
    assert called == 2
    assert state is False
    assert called_obj == 2
    assert state_obj == {"X": False, "Y": 2, "Z": None}

    subscription.unsubscribe()
    subscription_obj.unsubscribe()

    service.set_state(app_name, "/A/X", True)
    time.sleep(5)
    assert called == 2
    assert state is False
    assert called_obj == 2
    assert state_obj == {"X": False, "Y": 2, "Z": None}


def test_mapped_on_attribute_changed(datamodel_api_version_new, new_solver_session):
    rules_str = (
        "RULES:\n"
        "  STRING: X\n"
        "    allowedValues = yes, no\n"
        "    default = $../Y\n"
        "    logicalMapping = True, False\n"
        "  END\n"
        "  STRING: Y\n"
        "  END\n"
        "  SINGLETON: ROOT\n"
        "    members = A\n"
        "    commands = C\n"
        "    SINGLETON: A\n"
        "      members = X, Y\n"
        "    END\n"
        "    COMMAND: C\n"
        "      arguments = X, Y\n"
        "    END\n"
        "  END\n"
        "END\n"
    )

    class root_cls(PyMenu):
        def __init__(self, service, rules, path):
            self.A = self.__class__.A(service, rules, path + [("A", "")])
            self.C = self.__class__.C(service, rules, path + [("C", "")])
            super().__init__(service, rules, path)

        class A(PyMenu):
            def __init__(self, service, rules, path):
                self.X = self.__class__.X(service, rules, path + [("X", "")])
                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                super().__init__(service, rules, path)

            class X(PyTextual):
                pass

            class Y(PyTextual):
                pass

        class C(PyCommand):
            pass

    solver = new_solver_session
    app_name = "test"
    root = create_datamodel_root_in_server(solver, rules_str, app_name, root_cls)
    service = solver._se_service
    called = 0
    value = None

    def cb(val):
        nonlocal called
        nonlocal value
        value = val
        called += 1

    subscription = service.add_on_attribute_changed(
        app_name, "/A/X", "default", root.A.X, cb
    )
    assert called == 0
    assert value is None

    service.set_state(app_name, "/A/Y", "no")
    timeout_loop(lambda: called == 1, timeout=5)
    assert called == 1
    assert value is False

    service.set_state(app_name, "/A/Y", "yes")
    timeout_loop(lambda: called == 2, timeout=5)
    assert called == 2
    assert value is True

    subscription.unsubscribe()
    service.set_state(app_name, "/A/Y", "no")
    time.sleep(5)
    assert called == 2
    assert value is True


def test_datamodel_api_on_command_executed_mapped_args(
    datamodel_api_version_new, new_solver_session
):
    solver = new_solver_session
    app_name = "test"
    root = create_datamodel_root_in_server(solver, rules_str, app_name, rules_cls)
    service = solver._se_service
    register_external_function_in_remote_app(solver, app_name, "CFunc")
    executed = False
    command = None
    arguments = None

    def cb(obj, cmd, args):
        nonlocal executed
        nonlocal command
        nonlocal arguments
        command = cmd
        arguments = args
        executed = True

    subscription = service.add_on_command_executed(app_name, "/", "C", root, cb)
    assert not executed
    assert command is None
    assert arguments is None

    service.execute_command(app_name, "/", "C", {"X": True})
    timeout_loop(lambda: executed, timeout=5)
    assert executed
    assert command == "C"
    assert arguments == {"X": True}

    executed = False
    command = None
    arguments = None

    subscription.unsubscribe()
    service.execute_command(app_name, "/", "C", {"X": False})
    time.sleep(5)
    assert not executed
    assert command is None
    assert arguments is None


api_name_rules_str = (
    "RULES:\n"
    "  STRING: __X\n"
    "    allowedValues = yes, no\n"
    "    logicalMapping = True, False\n"
    "    attr1 = 42.0\n"
    "    APIName = xxx\n"
    "  END\n"
    "  STRING: __Y\n"
    '    allowedValues = \\"1\\", \\"2\\", \\"3\\"\n'
    '    default = \\"2\\"\n'
    "    isNumerical = True\n"
    "    APIName = yyy\n"
    "  END\n"
    "  INTEGER: Z\n"
    "  END\n"
    "  SINGLETON: ROOT\n"
    "    members = __A, B, __E\n"
    "    commands = __C, D\n"
    "    SINGLETON: __A\n"
    "      members = __X\n"
    "      APIName = aaa\n"
    "    END\n"
    "    OBJECT: B\n"
    "      members = __Y, Z\n"
    "    END\n"
    "    OBJECT: __E\n"
    "      members = __Y\n"
    "      APIName = eee\n"
    "    END\n"
    "    COMMAND: __C\n"
    "      arguments = __X\n"
    "      functionName = CFunc\n"
    "      APIName = ccc\n"
    "    END\n"
    "    COMMAND: D\n"
    "      arguments = __X\n"
    "      functionName = CFunc\n"
    "    END\n"
    "  END\n"
    "END\n"
)


def test_datamodel_api_with_mapped_names(datamodel_api_version_new, new_solver_session):
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, api_name_rules_str, app_name)
    service = solver._se_service
    static_info = service.get_static_info(app_name)
    assert (
        get_static_info_value(static_info, "/singletons/aaa/parameters/xxx/type")
        == "Logical"
    )
    assert (
        get_static_info_value(static_info, "/namedobjects/B/parameters/yyy/type")
        == "Integer"
    )
    assert (
        get_static_info_value(static_info, "/namedobjects/B/parameters/Z/type")
        == "Integer"
    )

    command_args = [
        {
            "helpstring": "",
            "name": "xxx",
            "type": "Logical",
        }
    ]
    command_args = [sorted(x.items()) for x in command_args]
    ccc_args = get_static_info_value(  # noqa: F841
        static_info, "/commands/ccc/commandinfo/args"
    )
    # TODO: helpstring is not being set
    # assert command_args == [sorted(x.items()) for x in ccc_args]
    d_args = get_static_info_value(  # noqa: F841
        static_info, "/commands/D/commandinfo/args"
    )
    # TODO: helpstring is not being returned
    # assert command_args == [sorted(x.items()) for x in d_args]


# TODO: what are the equivalent of following tests in Python?
# testMapperMapDataModelPathToAPIPath
# testMapperMapAPIPathToDataModelPath
# testMapperMapDMValueToAPI


def test_datamodel_api_root_get_and_set_state_with_mapped_names(
    datamodel_api_version_new, new_solver_session
):
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, api_name_rules_str, app_name)
    service = solver._se_service
    assert service.get_state(app_name, "/") == {"aaa": {"xxx": None}}
    service.set_state(app_name, "/__A/__X", "yes")
    assert service.get_state(app_name, "/") == {"aaa": {"xxx": True}}
    service.set_state(app_name, "/", {"aaa": {"xxx": False}})
    assert service.get_state(app_name, "/") == {"aaa": {"xxx": False}}


def test_datamodel_api_root_get_attrs_with_mapped_names(
    datamodel_api_version_new, new_solver_session
):
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, api_name_rules_str, app_name)
    service = solver._se_service
    assert service.get_attribute_value(app_name, "/aaa/xxx", "attr1") == 42.0
    service.set_state(app_name, "/", {"B:b": {}})
    assert service.get_attribute_value(app_name, "/B:b/yyy", "default") == 2


def test_datamodel_api_cmd_args_op_with_mapped_names(
    datamodel_api_version_new, new_solver_session
):
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, api_name_rules_str, app_name)
    service = solver._se_service
    c_name = service.create_command_arguments(app_name, "/", "ccc")
    x_path_str = f"/__C:{c_name}/xxx"  # noqa: F841
    # TODO: issue
    # service.set_state(app_name, x_path_str, True)
    service.set_state(app_name, f"/__C:{c_name}", {"xxx": True})
    assert service.get_state(app_name, f"/__C:{c_name}") == {"xxx": True}
    assert service.get_attribute_value(app_name, f"/__C:{c_name}", "xxx/attr1") == 42.0


def test_datamodel_api_rename_with_mapped_names(
    datamodel_api_version_new, new_solver_session
):
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, api_name_rules_str, app_name)
    service = solver._se_service
    service.set_state(app_name, "/", {"B:b": {}})
    service.rename(app_name, "/B:b", "c")
    service.set_state(app_name, "/", {"eee:e": {}})
    assert service.get_state(app_name, "/B:c/yyy") == 2
    service.rename(app_name, "/eee:e", "x")
    assert service.get_state(app_name, "/eee:x/yyy") == 2


def test_datamodel_api_delete_object_with_mapped_names(
    datamodel_api_version_new, new_solver_session
):
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, api_name_rules_str, app_name)
    service = solver._se_service
    service.set_state(app_name, "/", {"B:b": {}})
    service.delete_object(app_name, "/B:b")
