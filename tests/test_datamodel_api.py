import time

import pytest
from util import create_datamodel_root_in_server, create_root_using_datamodelgen

from ansys.fluent.core.services.datamodel_se import (
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


@pytest.mark.fluent_version(">=25.2")
def test_env_var_setting(datamodel_api_version_all, request, new_solver_session):
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
def test_datamodel_api_on_child_created(datamodel_api_version_all, new_solver_session):
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, rule_str, app_name)
    service = solver._se_service
    root = create_root_using_datamodelgen(service, app_name)

    called = 0
    created = []

    def cb(obj):
        nonlocal called
        nonlocal created
        called += 1
        created.append(convert_path_to_se_path(obj.path))

    subscription = service.add_on_child_created(app_name, "/", "B", root, cb)
    assert called == 0
    assert created == []
    service.set_state(app_name, "/", {"B:b": {"_name_": "b"}})
    timeout_loop(lambda: called == 1, timeout=5)
    assert called == 1
    assert created == ["/B:b"]
    subscription.unsubscribe()


@pytest.mark.fluent_version(">=25.2")
def test_datamodel_api_on_changed(datamodel_api_version_all, new_solver_session):
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, rule_str, app_name)
    service = solver._se_service
    root = create_root_using_datamodelgen(service, app_name)
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

    subscription = service.add_on_changed(app_name, "/A/X", root.A.X, cb)
    subscription_obj = service.add_on_changed(app_name, "/A", root.A, cb_obj)
    assert called == 0
    assert state is None
    assert called_obj == 0
    assert state_obj is None
    service.set_state(app_name, "/A/X", "lmn")
    timeout_loop(lambda: called == 1, timeout=5)
    assert called == 1
    assert state == "lmn"
    assert called_obj == 1
    assert state_obj == {"X": "lmn"}
    service.set_state(app_name, "/A/X", "abc")
    timeout_loop(lambda: called == 2, timeout=5)
    assert called == 2
    assert state == "abc"
    assert called_obj == 2
    assert state_obj == {"X": "abc"}
    subscription.unsubscribe()
    subscription_obj.unsubscribe()
    service.set_state(app_name, "/A/X", "xyz")
    time.sleep(5)
    assert called == 2
    assert state == "abc"
    assert called_obj == 2
    assert state_obj == {"X": "abc"}


@pytest.mark.fluent_version(">=25.2")
def test_datamodel_api_on_affected(datamodel_api_version_all, new_solver_session):
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, rule_str, app_name)
    service = solver._se_service
    root = create_root_using_datamodelgen(service, app_name)
    called = 0

    def cb(obj):
        nonlocal called
        called += 1

    subscription = service.add_on_affected(app_name, "/D", root.D, cb)
    assert called == 0
    service.set_state(app_name, "/D/X", "lmn")
    timeout_loop(lambda: called == 1, timeout=5)
    assert called == 1
    service.set_state(app_name, "/D/E/X", "lmn")
    timeout_loop(lambda: called == 2, timeout=5)
    assert called == 2
    service.set_state(app_name, "/A/X", "lmn")
    time.sleep(5)
    assert called == 2
    subscription.unsubscribe()
    service.set_state(app_name, "/D/E/X", "pqr")
    time.sleep(5)
    assert called == 2


@pytest.mark.fluent_version(">=25.2")
def test_datamodel_api_on_affected_at_type_path(
    datamodel_api_version_all, new_solver_session
):
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, rule_str, app_name)
    service = solver._se_service
    root = create_root_using_datamodelgen(service, app_name)
    called = 0

    def cb(obj):
        nonlocal called
        called += 1

    subscription = service.add_on_affected_at_type_path(
        app_name, "/D", "E", root.D.E, cb
    )
    assert called == 0
    service.set_state(app_name, "/D/X", "lmn")
    time.sleep(5)
    assert called == 0
    service.set_state(app_name, "/D/E/X", "lmn")
    timeout_loop(lambda: called == 1, timeout=5)
    assert called == 1
    service.set_state(app_name, "/D/F/X", "lmn")
    time.sleep(5)
    assert called == 1
    subscription.unsubscribe()
    service.set_state(app_name, "/D/E/X", "pqr")
    time.sleep(5)
    assert called == 1


@pytest.mark.fluent_version(">=25.2")
def test_datamodel_api_on_deleted(
    datamodel_api_version_all, request, new_solver_session
):
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, rule_str, app_name)
    service = solver._se_service
    root = create_root_using_datamodelgen(service, app_name)
    called = False
    called_obj = False

    def cb():
        nonlocal called
        called = True

    def cb_obj():
        nonlocal called_obj
        called_obj = True

    service.set_state(app_name, "/", {"B:b": {"_name_": "b"}})
    subscription = service.add_on_deleted(app_name, "/B:b/X", root.B["b"].X, cb)
    subscription_obj = service.add_on_deleted(app_name, "/B:b", root.B["b"], cb_obj)
    assert not called
    assert not called_obj
    service.delete_object(app_name, "/B:b")
    time.sleep(5)
    test_name = request.node.name
    # TODO: Note comment in StateEngine test testDataModelAPIOnDeleted
    if test_name.endswith("[old]"):
        assert called
    elif test_name.endswith("[new]"):
        assert not called
    assert called_obj
    subscription.unsubscribe()
    subscription_obj.unsubscribe()


@pytest.mark.fluent_version(">=25.2")
def test_datamodel_api_on_attribute_changed(
    datamodel_api_version_all, new_solver_session
):
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, rule_str, app_name)
    service = solver._se_service
    root = create_root_using_datamodelgen(service, app_name)
    called = 0
    value = None

    def cb(val):
        nonlocal called
        nonlocal value
        value = val
        called += 1

    subscription = service.add_on_attribute_changed(app_name, "/A", "x", root.A, cb)
    assert called == 0
    assert value is None
    service.set_state(app_name, "/A/X", "cde")
    timeout_loop(lambda: called == 1, timeout=5)
    assert called == 1
    assert value == "cde"
    service.set_state(app_name, "/A/X", "xyz")
    timeout_loop(lambda: called == 2, timeout=5)
    assert called == 2
    assert value == "xyz"
    subscription.unsubscribe()
    service.set_state(app_name, "/A/X", "abc")
    time.sleep(5)
    assert called == 2
    assert value == "xyz"


@pytest.mark.fluent_version(">=25.2")
def test_datamodel_api_on_command_attribute_changed(
    datamodel_api_version_all, new_solver_session
):
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, rule_str, app_name)
    service = solver._se_service
    root = create_root_using_datamodelgen(service, app_name)
    called = 0
    value = None

    def cb(val):
        nonlocal called
        nonlocal value
        value = val
        called += 1

    subscription = service.add_on_command_attribute_changed(
        app_name, "/", "C", "x", root.C, cb
    )
    assert called == 0
    assert value is None
    service.set_state(app_name, "/A/X", "cde")
    timeout_loop(lambda: called == 1, timeout=5)
    assert called == 1
    assert value == "cde"
    service.set_state(app_name, "/A/X", "xyz")
    timeout_loop(lambda: called == 2, timeout=5)
    assert called == 2
    # TODO: value is still "cde" in both old and new API
    # assert value == "xyz"
    subscription.unsubscribe()
    service.set_state(app_name, "/A/X", "abc")
    time.sleep(5)
    assert called == 2
    # Commented out because of the issue above
    # assert value == "xyz"


@pytest.mark.fluent_version(">=25.2")
def test_datamodel_api_on_command_executed(
    datamodel_api_version_all, new_solver_session
):
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, rule_str, app_name)
    service = solver._se_service
    root = create_root_using_datamodelgen(service, app_name)
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
    subscription = service.add_on_command_executed(app_name, "/", root, cb)
    assert executed == 0
    assert command is None
    assert arguments is None
    service.execute_command(app_name, "/", "C", dict(X="abc"))
    timeout_loop(lambda: executed == 1, timeout=5)
    assert executed == 1
    assert command == "C"
    assert arguments == {"X": "abc"}
    subscription.unsubscribe()
    service.execute_command(app_name, "/", "C", dict(X="uvw"))
    time.sleep(5)
    assert executed == 1
    assert command == "C"
    assert arguments == {"X": "abc"}


@pytest.mark.fluent_version(">=25.2")
def test_datamodel_api_get_state(datamodel_api_version_all, new_solver_session):
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, rule_str, app_name)
    service = solver._se_service
    assert service.get_state(app_name, "/A/X") == "ijk"


@pytest.mark.fluent_version(">=25.2")
def test_datamodel_api_set_state(datamodel_api_version_all, new_solver_session):
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, rule_str, app_name)
    service = solver._se_service
    service.set_state(app_name, "/A/X", "new_val")
    assert service.get_state(app_name, "/A/X") == "new_val"


@pytest.mark.fluent_version(">=25.2")
def test_datamodel_api_update_dict(datamodel_api_version_all, new_solver_session):
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, rule_str, app_name)
    service = solver._se_service
    service.update_dict(app_name, "/G/H", {"X": "abc"})
    assert service.get_state(app_name, "/G/H") == {"X": "abc"}


@pytest.mark.fluent_version(">=25.2")
def test_datamodel_api_on_bad_input(
    datamodel_api_version_all, request, new_solver_session
):
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, rule_str, app_name)
    service = solver._se_service
    root = create_root_using_datamodelgen(service, app_name)
    test_name = request.node.name
    new_api = test_name.endswith("[new]")
    with pytest.raises(SubscribeEventError):
        service.add_on_child_created(app_name, "", "", root, lambda _: None)
    with pytest.raises(RuntimeError if new_api else SubscribeEventError):  # TODO: issue
        service.add_on_child_created(app_name, "/BB", "B", root, lambda _: None)
    with pytest.raises(SubscribeEventError):
        service.add_on_child_created(app_name, "/", "A", root, lambda _: None)
    with pytest.raises(SubscribeEventError):
        service.add_on_child_created(app_name, "/", "BB", root, lambda _: None)
    with pytest.raises(RuntimeError if new_api else SubscribeEventError):  # TODO: issue
        service.add_on_changed(app_name, "/BB", root, lambda _: None)
    with pytest.raises(RuntimeError if new_api else SubscribeEventError):  # TODO: issue
        service.add_on_deleted(app_name, "/BB", root, lambda: None)
    with pytest.raises(RuntimeError if new_api else SubscribeEventError):  # TODO: issue
        service.add_on_affected(app_name, "/BB", root, lambda _: None)
    with pytest.raises(RuntimeError if new_api else SubscribeEventError):  # TODO: issue
        service.add_on_affected_at_type_path(app_name, "/BB", "B", root, lambda: None)
    # TODO: not raised in the old API - issue
    if new_api:
        with pytest.raises(SubscribeEventError):
            service.add_on_affected_at_type_path(
                app_name, "/", "BB", root, lambda: None
            )
    with pytest.raises(RuntimeError if new_api else SubscribeEventError):  # TODO: issue
        service.add_on_attribute_changed(
            app_name, "/BB", "isActive", root, lambda _: None
        )
    with pytest.raises(SubscribeEventError):
        service.add_on_attribute_changed(app_name, "/A", "", root, lambda _: None)
    with pytest.raises(RuntimeError if new_api else SubscribeEventError):  # TODO: issue
        service.add_on_command_attribute_changed(
            app_name, "/BB", "C", "isActive", root, lambda _: None
        )
    with pytest.raises(SubscribeEventError):
        service.add_on_command_attribute_changed(
            app_name, "/A", "CC", "", root, lambda _: None
        )
    with pytest.raises(SubscribeEventError):
        service.add_on_command_attribute_changed(
            app_name, "/", "CC", "isActive", root, lambda _: None
        )
    with pytest.raises(RuntimeError if new_api else SubscribeEventError):  # TODO: issue
        service.add_on_command_executed(app_name, "/BB", root, lambda _: None)


@pytest.mark.fluent_version(">=25.2")
def test_datamodel_api_static_info(datamodel_api_version_all, new_solver_session):
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, rule_str, app_name)
    service = solver._se_service
    assert service.get_static_info(app_name)
