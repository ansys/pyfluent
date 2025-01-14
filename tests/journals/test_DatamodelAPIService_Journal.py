"Test DataModelAPIService through journal."


def create_datamodel_root_in_server(solver) -> None:
    import uuid

    app_name = "test"
    rules_str = (
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
    rules_file_name = f"{uuid.uuid4()}.fdl"
    solver.scheme_eval.scheme_eval(
        f'(with-output-to-file "{rules_file_name}" (lambda () (format "~a" "{rules_str}")))',
    )
    solver.scheme_eval.scheme_eval(
        f'(state/register-new-state-engine "{app_name}" "{rules_file_name}")'
    )
    solver.scheme_eval.scheme_eval(f'(remove-file "{rules_file_name}")')


def test_datamodel_api_on_child_created(solver):
    import time

    create_datamodel_root_in_server(solver)
    app_name = "test"
    service = solver._se_service
    called = 0
    created = []

    def cb(path):
        nonlocal called
        nonlocal created
        called += 1
        created.append(path)

    subscription = service.add_on_child_created(app_name, "/", "B", cb)
    assert called == 0
    assert created == []
    service.set_state(app_name, "/", {"B:b": {"_name_": "b"}})
    time.sleep(6)
    assert called == 1
    assert created == ["/B:b"]
    subscription.unsubscribe()


def test_datamodel_api_on_changed(solver):
    import time

    create_datamodel_root_in_server(solver)
    app_name = "test"
    service = solver._se_service
    called = 0
    changed = None
    called_obj = 0
    changed_obj = None

    def cb(path):
        nonlocal called
        nonlocal changed
        changed = path
        called += 1

    def cb_obj(path):
        nonlocal called_obj
        nonlocal changed_obj
        changed_obj = path
        called_obj += 1

    subscription = service.add_on_changed(app_name, "/A/X", cb)
    subscription_obj = service.add_on_changed(app_name, "/A", cb_obj)
    assert called == 0
    assert changed is None
    assert called_obj == 0
    assert changed_obj is None
    service.set_state(app_name, "/A/X", "lmn")
    time.sleep(5)
    assert called == 1
    assert changed == "lmn"
    assert called_obj == 1
    assert changed_obj == {"X": "lmn"}
    service.set_state(app_name, "/A/X", "abc")
    time.sleep(5)
    assert called == 2
    assert changed == "abc"
    assert called_obj == 2
    assert changed_obj == {"X": "abc"}
    subscription.unsubscribe()
    subscription_obj.unsubscribe()
    service.set_state(app_name, "/A/X", "xyz")
    time.sleep(5)
    assert called == 2
    assert changed == "abc"
    assert called_obj == 2
    assert changed_obj == {"X": "abc"}


def test_datamodel_api_on_attribute_changed(solver):
    import time

    create_datamodel_root_in_server(solver)
    app_name = "test"
    service = solver._se_service
    called = 0
    value = None

    def cb(attribute):
        nonlocal called
        nonlocal value
        value = attribute
        called += 1

    subscription = service.add_on_attribute_changed(app_name, "/A", "x", cb)
    assert called == 0
    assert value is None
    service.set_state(app_name, "/A/X", "cde")
    time.sleep(5)
    assert called == 1
    assert value == "cde"
    service.set_state(app_name, "/A/X", "xyz")
    time.sleep(5)
    assert called == 2
    assert value == "xyz"
    subscription.unsubscribe()
    service.set_state(app_name, "/A/X", "abc")
    time.sleep(5)
    assert called == 2
    assert value == "xyz"


def test_datamodel_api_on_command_attribute_changed(solver):
    import time

    create_datamodel_root_in_server(solver)
    app_name = "test"
    service = solver._se_service
    called = 0
    value = None

    def cb(val):
        nonlocal called
        nonlocal value
        value = val
        called += 1

    subscription = service.add_on_command_attribute_changed(app_name, "/", "C", "x", cb)
    assert called == 0
    assert value is None
    service.set_state(app_name, "/A/X", "cde")
    time.sleep(5)
    assert called == 1
    assert value == "cde"
    service.set_state(app_name, "/A/X", "xyz")
    time.sleep(5)
    assert called == 2
    assert value == "xyz"
    subscription.unsubscribe()
    service.set_state(app_name, "/A/X", "abc")
    time.sleep(5)
    assert called == 2
    assert value == "xyz"


def test_datamodel_api_on_command_executed(solver):
    import time

    create_datamodel_root_in_server(solver)
    app_name = "test"
    service = solver._se_service
    executed = 0
    command = None
    arguments = None

    def cb(cmd, args):
        nonlocal executed
        nonlocal command
        nonlocal arguments
        command = cmd
        arguments = args
        executed += 1

    subscription = service.add_on_command_executed(app_name, "/", cb)
    assert executed == 0
    assert command is None
    assert arguments is None
    service.execute_command(app_name, "/", "C", dict(X="abc"))
    time.sleep(5)
    assert executed == 1
    assert command == "C"
    assert arguments == {"X": "abc"}
    subscription.unsubscribe()
    service.execute_command(app_name, "/", "C", dict(X="uvw"))
    time.sleep(5)
    assert executed == 1
    assert command == "C"
    assert arguments == {"X": "abc"}


def test_datamodel_api_get_state(solver):
    create_datamodel_root_in_server(solver)
    app_name = "test"
    service = solver._se_service
    assert service.get_state(app_name, "/A/X") == "ijk"


def test_datamodel_api_set_state(solver):
    create_datamodel_root_in_server(solver)
    app_name = "test"
    service = solver._se_service
    service.set_state(app_name, "/A/X", "new_val")
    assert service.get_state(app_name, "/A/X") == "new_val"


def test_datamodel_api_update_dict(solver):
    create_datamodel_root_in_server(solver)
    app_name = "test"
    service = solver._se_service
    service.update_dict(app_name, "/G/H", {"X": "abc"})
    assert service.get_state(app_name, "/G/H") == {"X": "abc"}


def test_datamodel_api_static_info(solver):
    create_datamodel_root_in_server(solver)
    app_name = "test"
    service = solver._se_service
    assert service.get_static_info(app_name)


def test_datamodel_api_on_affected(solver):
    import time

    create_datamodel_root_in_server(solver)
    app_name = "test"
    service = solver._se_service
    called = 0

    def cb():
        nonlocal called
        called += 1

    subscription = service.add_on_affected(app_name, "/D", cb)
    assert called == 0
    service.set_state(app_name, "/D/X", "lmn")
    time.sleep(5)
    assert called == 1
    service.set_state(app_name, "/D/E/X", "lmn")
    time.sleep(5)
    assert called == 2
    service.set_state(app_name, "/A/X", "lmn")
    time.sleep(5)
    assert called == 2
    subscription.unsubscribe()
    service.set_state(app_name, "/D/E/X", "pqr")
    time.sleep(5)
    assert called == 2


def test_datamodel_api_on_affected_at_type_path(solver):
    import time

    create_datamodel_root_in_server(solver)
    app_name = "test"
    service = solver._se_service
    called = 0

    def cb():
        nonlocal called
        called += 1

    subscription = service.add_on_affected_at_type_path(app_name, "/D", "E", cb)
    assert called == 0
    service.set_state(app_name, "/D/X", "lmn")
    time.sleep(5)
    assert called == 0
    service.set_state(app_name, "/D/E/X", "lmn")
    time.sleep(5)
    assert called == 1
    service.set_state(app_name, "/D/F/X", "lmn")
    time.sleep(5)
    assert called == 1
    subscription.unsubscribe()
    service.set_state(app_name, "/D/E/X", "pqr")
    time.sleep(5)
    assert called == 1


def test_datamodel_api_on_deleted(solver):
    import time

    create_datamodel_root_in_server(solver)
    app_name = "test"
    service = solver._se_service
    called = False
    called_obj = False

    def cb():
        nonlocal called
        called = True

    def cb_obj():
        nonlocal called_obj
        called_obj = True

    service.set_state(app_name, "/", {"B:b": {"_name_": "b"}})
    subscription = service.add_on_deleted(app_name, "/B:b/X", cb)
    subscription_obj = service.add_on_deleted(app_name, "/B:b", cb_obj)
    assert not called
    assert not called_obj
    service.delete_object(app_name, "/B:b")
    time.sleep(5)
    assert not called
    assert called_obj
    subscription.unsubscribe()
    subscription_obj.unsubscribe()


def test_datamodel_api_rename_and_get_object_names(solver):
    create_datamodel_root_in_server(solver)
    app_name = "test"
    service = solver._se_service

    def cb(path):
        pass

    subscription = service.add_on_child_created(app_name, "/", "B", cb)
    service.set_state(app_name, "/", {"B:b": {"_name_": "b"}})
    service.rename(app_name, "/B:b", "b_new")
    assert service.get_object_names(app_name, "/B:b_new") == ["b_new"]
    subscription.unsubscribe()


create_datamodel_root_in_server(solver)  # noqa: F821
test_datamodel_api_on_child_created(solver)  # noqa: F821
test_datamodel_api_on_changed(solver)  # noqa: F821
test_datamodel_api_on_attribute_changed(solver)  # noqa: F821
test_datamodel_api_on_command_attribute_changed(solver)  # noqa: F821
test_datamodel_api_on_command_executed(solver)  # noqa: F821
test_datamodel_api_get_state(solver)  # noqa: F821
test_datamodel_api_set_state(solver)  # noqa: F821
test_datamodel_api_update_dict(solver)  # noqa: F821
test_datamodel_api_static_info(solver)  # noqa: F821
test_datamodel_api_on_affected(solver)  # noqa: F821
test_datamodel_api_on_affected_at_type_path(solver)  # noqa: F821
test_datamodel_api_on_deleted(solver)  # noqa: F821
test_datamodel_api_rename_and_get_object_names(solver)  # noqa: F821

print("\n Testing finished. All tests passed.\n")
