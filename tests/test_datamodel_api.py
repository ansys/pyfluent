import time

import pytest
from util import create_datamodel_root_in_server

from ansys.fluent.core.services.datamodel_se import (
    PyCommand,
    PyDictionary,
    PyMenu,
    PyNamedObjectContainer,
    PyTextual,
    SubscribeEventError,
    convert_path_to_se_path,
)
from ansys.fluent.core.utils.execution import timeout_loop

rule_str = (
    "RULES:\n"
    "  STRING: X\n"
    "    default = ijk\n"
    "  END\n"
    "  SINGLETON: ROOT\n"
    "    members = A, B, D, G\n"
    "    commands= C\n"
    "    SINGLETON: A\n"
    "      members = X\n"
    "      x = $./X\n"
    "    END\n"
    "    OBJECT: B\n"
    "      members = X\n"
    "    END\n"
    "    SINGLETON: D\n"
    "      members = E, F, X\n"
    "      SINGLETON: E\n"
    "        members = X\n"
    "      END\n"
    "      SINGLETON: F\n"
    "        members = X\n"
    "      END\n"
    "    END\n"
    "    SINGLETON: G\n"
    "      members = H\n"
    "      DICT: H\n"
    "      END\n"
    "    END\n"
    "    COMMAND: C\n"
    "      arguments = X\n"
    "      x = $/A/X\n"
    "    END\n"
    "  END\n"
    "END\n"
)


class test_root(PyMenu):
    def __init__(self, service, rules, path):
        self.A = self.__class__.A(service, rules, path + [("A", "")])
        self.B = self.__class__.B(service, rules, path + [("B", "")])
        self.C = self.__class__.C(service, rules, path + [("C", "")])
        self.D = self.__class__.D(service, rules, path + [("D", "")])
        self.G = self.__class__.G(service, rules, path + [("G", "")])
        super().__init__(service, rules, path)

    class A(PyMenu):
        def __init__(self, service, rules, path):
            self.X = self.__class__.X(service, rules, path + [("X", "")])
            super().__init__(service, rules, path)

        class X(PyTextual):
            pass

    class B(PyNamedObjectContainer):
        class _B(PyMenu):
            def __init__(self, service, rules, path):
                self.X = self.__class__.X(service, rules, path + [("X", "")])
                super().__init__(service, rules, path)

            class X(PyTextual):
                pass

    class C(PyCommand):
        pass

    class D(PyMenu):
        def __init__(self, service, rules, path):
            self.E = self.__class__.E(service, rules, path + [("E", "")])
            self.F = self.__class__.F(service, rules, path + [("F", "")])
            self.X = self.__class__.X(service, rules, path + [("X", "")])
            super().__init__(service, rules, path)

        class E(PyMenu):
            def __init__(self, service, rules, path):
                self.X = self.__class__.X(service, rules, path + [("X", "")])
                super().__init__(service, rules, path)

            class X(PyTextual):
                pass

        class F(PyMenu):
            def __init__(self, service, rules, path):
                self.X = self.__class__.X(service, rules, path + [("X", "")])
                super().__init__(service, rules, path)

            class X(PyTextual):
                pass

        class X(PyTextual):
            pass

    class G(PyMenu):
        def __init__(self, service, rules, path):
            self.H = self.__class__.H(service, rules, path + [("H", "")])
            super().__init__(service, rules, path)

        class H(PyDictionary):
            pass


@pytest.mark.fluent_version(">=25.2")
def test_env_var_setting(datamodel_api_version, request, new_solver_session):
    solver = new_solver_session
    test_name = request.node.name
    for var in ["REMOTING_NEW_DM_API", "REMOTING_MAPPED_NEW_DM_API"]:
        # TODO: It might be possible to check the param value in the fixture
        # instead of checking the test name here.
        if test_name.endswith("[old]"):
            assert solver.scheme_eval.scheme_eval(f'(getenv "{var}")') is None
        elif test_name.endswith("[new]"):
            assert solver.scheme_eval.scheme_eval(f'(getenv "{var}")') == "1"


@pytest.mark.fluent_version(">=25.2")
def test_datamodel_api_on_child_created(datamodel_api_version, new_solver_session):
    solver = new_solver_session
    root = create_datamodel_root_in_server(solver, rule_str, test_root)
    service = solver._se_service
    called = 0
    created = []

    def cb(obj):
        nonlocal called
        nonlocal created
        called += 1
        created.append(convert_path_to_se_path(obj.path))

    subscription = service.add_on_child_created("test", "/", "B", root, cb)
    assert called == 0
    assert created == []
    service.set_state("test", "/", {"B:b": {"_name_": "b"}})
    timeout_loop(lambda: called == 1, timeout=5)
    assert called == 1
    assert created == ["/B:b"]
    subscription.unsubscribe()


@pytest.mark.fluent_version(">=25.2")
def test_datamodel_api_on_changed(datamodel_api_version, new_solver_session):
    solver = new_solver_session
    root = create_datamodel_root_in_server(solver, rule_str, test_root)
    service = solver._se_service
    called = 0
    state = None
    called_obj = 0
    state_obj = None

    def cb(obj):
        nonlocal called
        nonlocal state
        state = obj()
        called += 1

    def cb_obj(obj):
        nonlocal called_obj
        nonlocal state_obj
        state_obj = obj()
        called_obj += 1

    subscription = service.add_on_changed("test", "/A/X", root.A.X, cb)
    subscription_obj = service.add_on_changed("test", "/A", root.A, cb_obj)
    assert called == 0
    assert state is None
    assert called_obj == 0
    assert state_obj is None
    service.set_state("test", "/A/X", "lmn")
    timeout_loop(lambda: called == 1, timeout=5)
    assert called == 1
    assert state == "lmn"
    assert called_obj == 1
    assert state_obj == {"X": "lmn"}
    service.set_state("test", "/A/X", "abc")
    timeout_loop(lambda: called == 2, timeout=5)
    assert called == 2
    assert state == "abc"
    assert called_obj == 2
    assert state_obj == {"X": "abc"}
    subscription.unsubscribe()
    subscription_obj.unsubscribe()
    service.set_state("test", "/A/X", "xyz")
    time.sleep(5)
    assert called == 2
    assert state == "abc"
    assert called_obj == 2
    assert state_obj == {"X": "abc"}


@pytest.mark.fluent_version(">=25.2")
def test_datamodel_api_on_affected(datamodel_api_version, new_solver_session):
    solver = new_solver_session
    root = create_datamodel_root_in_server(solver, rule_str, test_root)
    service = solver._se_service
    called = 0

    def cb(obj):
        nonlocal called
        called += 1

    subscription = service.add_on_affected("test", "/D", root.D, cb)
    assert called == 0
    service.set_state("test", "/D/X", "lmn")
    timeout_loop(lambda: called == 1, timeout=5)
    assert called == 1
    service.set_state("test", "/D/E/X", "lmn")
    timeout_loop(lambda: called == 2, timeout=5)
    assert called == 2
    service.set_state("test", "/A/X", "lmn")
    time.sleep(5)
    assert called == 2
    subscription.unsubscribe()
    service.set_state("test", "/D/E/X", "pqr")
    time.sleep(5)
    assert called == 2


@pytest.mark.fluent_version(">=25.2")
def test_datamodel_api_on_affected_at_type_path(
    datamodel_api_version, new_solver_session
):
    solver = new_solver_session
    root = create_datamodel_root_in_server(solver, rule_str, test_root)
    service = solver._se_service
    called = 0

    def cb(obj):
        nonlocal called
        called += 1

    subscription = service.add_on_affected_at_type_path("test", "/D", "E", root.D.E, cb)
    assert called == 0
    service.set_state("test", "/D/X", "lmn")
    time.sleep(5)
    assert called == 0
    service.set_state("test", "/D/E/X", "lmn")
    timeout_loop(lambda: called == 1, timeout=5)
    assert called == 1
    service.set_state("test", "/D/F/X", "lmn")
    time.sleep(5)
    assert called == 1
    subscription.unsubscribe()
    service.set_state("test", "/D/E/X", "pqr")
    time.sleep(5)
    assert called == 1


@pytest.mark.fluent_version(">=25.2")
def test_datamodel_api_on_deleted(datamodel_api_version, request, new_solver_session):
    solver = new_solver_session
    root = create_datamodel_root_in_server(solver, rule_str, test_root)
    service = solver._se_service
    called = False
    called_obj = False

    def cb():
        nonlocal called
        called = True

    def cb_obj():
        nonlocal called_obj
        called_obj = True

    service.set_state("test", "/", {"B:b": {"_name_": "b"}})
    subscription = service.add_on_deleted("test", "/B:b/X", root.B["b"].X, cb)
    subscription_obj = service.add_on_deleted("test", "/B:b", root.B["b"], cb_obj)
    assert not called
    assert not called_obj
    service.delete_object("test", "/B:b")
    timeout_loop(lambda: called_obj, timeout=5)
    test_name = request.node.name
    # Note comment in StateEngine test testDataModelAPIOnDeleted
    if test_name.endswith("[old]"):
        assert called
    elif test_name.endswith("[new]"):
        assert not called
    assert called_obj
    subscription.unsubscribe()
    subscription_obj.unsubscribe()


@pytest.mark.fluent_version(">=25.2")
def test_datamodel_api_on_attribute_changed(datamodel_api_version, new_solver_session):
    solver = new_solver_session
    root = create_datamodel_root_in_server(solver, rule_str, test_root)
    service = solver._se_service
    called = 0
    value = None

    def cb(val):
        nonlocal called
        nonlocal value
        value = val
        called += 1

    subscription = service.add_on_attribute_changed("test", "/A", "x", root.A, cb)
    assert called == 0
    assert value is None
    service.set_state("test", "/A/X", "cde")
    timeout_loop(lambda: called == 1, timeout=5)
    assert called == 1
    assert value == "cde"
    service.set_state("test", "/A/X", "xyz")
    timeout_loop(lambda: called == 2, timeout=5)
    assert called == 2
    assert value == "xyz"
    subscription.unsubscribe()
    service.set_state("test", "/A/X", "abc")
    time.sleep(5)
    assert called == 2
    assert value == "xyz"


@pytest.mark.fluent_version(">=25.2")
def test_datamodel_api_on_command_attribute_changed(
    datamodel_api_version, new_solver_session
):
    solver = new_solver_session
    root = create_datamodel_root_in_server(solver, rule_str, test_root)
    service = solver._se_service
    called = 0
    value = None

    def cb(val):
        nonlocal called
        nonlocal value
        value = val
        called += 1

    subscription = service.add_on_command_attribute_changed(
        "test", "/", "C", "x", root.C, cb
    )
    assert called == 0
    assert value is None
    service.set_state("test", "/A/X", "cde")
    timeout_loop(lambda: called == 1, timeout=5)
    assert called == 1
    assert value == "cde"
    service.set_state("test", "/A/X", "xyz")
    timeout_loop(lambda: called == 2, timeout=5)
    assert called == 2
    # TODO: value is still "cde" in both old and new API
    # assert value == "xyz"
    subscription.unsubscribe()
    service.set_state("test", "/A/X", "abc")
    time.sleep(5)
    assert called == 2
    # Commented out because of the issue above
    # assert value == "xyz"


@pytest.mark.fluent_version(">=25.2")
def test_datamodel_api_on_command_executed(datamodel_api_version, new_solver_session):
    solver = new_solver_session
    root = create_datamodel_root_in_server(solver, rule_str, test_root)
    service = solver._se_service
    executed = 0
    command = None
    arguments = None

    def cb(obj, cmd, args):
        nonlocal executed
        nonlocal command
        nonlocal arguments
        command = cmd
        arguments = args
        executed += 1

    # TODO: In C++ API, we don't need to pass the command name
    subscription = service.add_on_command_executed("test", "/", "C", root, cb)
    assert executed == 0
    assert command is None
    assert arguments is None
    service.execute_command("test", "/", "C", dict(X="abc"))
    timeout_loop(lambda: executed == 1, timeout=5)
    assert executed == 1
    assert command == "C"
    assert arguments == {"X": "abc"}
    subscription.unsubscribe()
    service.execute_command("test", "/", "C", dict(X="uvw"))
    time.sleep(5)
    assert executed == 1
    assert command == "C"
    assert arguments == {"X": "abc"}


@pytest.mark.fluent_version(">=25.2")
def test_datamodel_api_get_state(datamodel_api_version, new_solver_session):
    solver = new_solver_session
    create_datamodel_root_in_server(solver, rule_str, test_root)
    service = solver._se_service
    assert service.get_state("test", "/A/X") == "ijk"


@pytest.mark.fluent_version(">=25.2")
def test_datamodel_api_set_state(datamodel_api_version, new_solver_session):
    solver = new_solver_session
    create_datamodel_root_in_server(solver, rule_str, test_root)
    service = solver._se_service
    service.set_state("test", "/A/X", "new_val")
    assert service.get_state("test", "/A/X") == "new_val"


@pytest.mark.fluent_version(">=25.2")
def test_datamodel_api_update_dict(datamodel_api_version, new_solver_session):
    solver = new_solver_session
    create_datamodel_root_in_server(solver, rule_str, test_root)
    service = solver._se_service
    service.update_dict("test", "/G/H", {"X": "abc"})
    assert service.get_state("test", "/G/H") == {"X": "abc"}


@pytest.mark.fluent_version(">=25.2")
def test_datamodel_api_on_bad_input(datamodel_api_version, request, new_solver_session):
    solver = new_solver_session
    root = create_datamodel_root_in_server(solver, rule_str, test_root)
    service = solver._se_service
    test_name = request.node.name
    new_api = test_name.endswith("[new]")
    with pytest.raises(SubscribeEventError):
        service.add_on_child_created("test", "", "", root, lambda _: None)
    with pytest.raises(RuntimeError if new_api else SubscribeEventError):  # TODO: issue
        service.add_on_child_created("test", "/BB", "B", root, lambda _: None)
    with pytest.raises(SubscribeEventError):
        service.add_on_child_created("test", "/", "A", root, lambda _: None)
    with pytest.raises(SubscribeEventError):
        service.add_on_child_created("test", "/", "BB", root, lambda _: None)
    with pytest.raises(RuntimeError if new_api else SubscribeEventError):  # TODO: issue
        service.add_on_changed("test", "/BB", root, lambda _: None)
    with pytest.raises(RuntimeError if new_api else SubscribeEventError):  # TODO: issue
        service.add_on_deleted("test", "/BB", root, lambda: None)
    with pytest.raises(RuntimeError if new_api else SubscribeEventError):  # TODO: issue
        service.add_on_affected("test", "/BB", root, lambda _: None)
    with pytest.raises(RuntimeError if new_api else SubscribeEventError):  # TODO: issue
        service.add_on_affected_at_type_path("test", "/BB", "B", root, lambda: None)
    # TODO: not raised in the old API - issue
    if new_api:
        with pytest.raises(SubscribeEventError):
            service.add_on_affected_at_type_path("test", "/", "BB", root, lambda: None)
    with pytest.raises(RuntimeError if new_api else SubscribeEventError):  # TODO: issue
        service.add_on_attribute_changed(
            "test", "/BB", "isActive", root, lambda _: None
        )
    with pytest.raises(SubscribeEventError):
        service.add_on_attribute_changed("test", "/A", "", root, lambda _: None)
    with pytest.raises(RuntimeError if new_api else SubscribeEventError):  # TODO: issue
        service.add_on_command_attribute_changed(
            "test", "/BB", "C", "isActive", root, lambda _: None
        )
    with pytest.raises(SubscribeEventError):
        service.add_on_command_attribute_changed(
            "test", "/A", "CC", "", root, lambda _: None
        )
    with pytest.raises(SubscribeEventError):
        service.add_on_command_attribute_changed(
            "test", "/", "CC", "isActive", root, lambda _: None
        )
    with pytest.raises(RuntimeError if new_api else SubscribeEventError):  # TODO: issue
        service.add_on_command_executed("test", "/BB", "C", root, lambda _: None)


@pytest.mark.fluent_version(">=25.2")
def test_datamodel_api_static_info(datamodel_api_version, new_solver_session):
    solver = new_solver_session
    create_datamodel_root_in_server(solver, rule_str, test_root)
    service = solver._se_service
    assert service.get_static_info("test")
