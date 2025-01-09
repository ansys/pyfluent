import gc
from time import sleep

from google.protobuf.json_format import MessageToDict
import pytest
from util import create_datamodel_root_in_server, create_root_using_datamodelgen

from ansys.api.fluent.v0 import datamodel_se_pb2
from ansys.api.fluent.v0.variant_pb2 import Variant
import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
from ansys.fluent.core.services.datamodel_se import (
    PyMenuGeneric,
    ReadOnlyObjectError,
    _convert_value_to_variant,
    _convert_variant_to_value,
    convert_path_to_se_path,
)
from ansys.fluent.core.streaming_services.datamodel_streaming import DatamodelStream
from ansys.fluent.core.utils.execution import timeout_loop
from ansys.fluent.core.utils.fluent_version import FluentVersion


@pytest.mark.parametrize(
    "value,expected",
    [
        (None, None),
        (False, False),
        (True, True),
        (1, 1),
        (1.0, 1.0),
        ("abc", "abc"),
        ((1, 2, 3), [1, 2, 3]),
        ([1, 2, 3], [1, 2, 3]),
        ({"a": 5}, {"a": 5}),
        ({"a": [1, 2, 3]}, {"a": [1, 2, 3]}),
        ({"a": {"b": 5}}, {"a": {"b": 5}}),
    ],
)
def test_convert_value_to_variant_to_value(value, expected):
    variant = Variant()
    _convert_value_to_variant(value, variant)
    assert expected == _convert_variant_to_value(variant)


@pytest.mark.fluent_version(">=23.2")
@pytest.mark.codegen_required
def test_event_subscription(new_meshing_session):
    session = new_meshing_session
    session.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")
    tags = [
        "/workflow/created/TaskObject",
        "/workflow/modified/TaskObject:TaskObject1/Arguments",
        "/workflow/deleted/TaskObject:TaskObject1",
        "/workflow/affected/TaskObject:TaskObject1",
        "/workflow/affected/TaskObject",
        "/workflow/attribute_changed/TaskObject:TaskObject1/TaskList/isActive",
        "/workflow/command_attribute_changed/InitializeWorkflow/arguments",
    ]
    version = session.get_fluent_version()
    if version < FluentVersion.v252:
        tags.append("/workflow/command_executed/InitializeWorkflow")
    else:
        # TODO: path should be appended to the tag
        tags.append("/workflow/command_executed")
    request = datamodel_se_pb2.SubscribeEventsRequest()
    e1 = request.eventrequest.add(rules="workflow")
    e1.createdEventRequest.parentpath = ""
    e1.createdEventRequest.childtype = "TaskObject"
    e2 = request.eventrequest.add(rules="workflow")
    e2.modifiedEventRequest.path = "TaskObject:TaskObject1/Arguments"
    e3 = request.eventrequest.add(rules="workflow")
    e3.deletedEventRequest.path = "TaskObject:TaskObject1"
    e4 = request.eventrequest.add(rules="workflow")
    e4.affectedEventRequest.path = "TaskObject:TaskObject1"
    e5 = request.eventrequest.add(rules="workflow")
    e5.affectedEventRequest.path = ""
    e5.affectedEventRequest.subtype = "TaskObject"
    e6 = request.eventrequest.add(rules="workflow")
    e6.attributeChangedEventRequest.path = "TaskObject:TaskObject1/TaskList"
    e6.attributeChangedEventRequest.attribute = "isActive"
    e7 = request.eventrequest.add(rules="workflow")
    e7.commandAttributeChangedEventRequest.path = ""
    e7.commandAttributeChangedEventRequest.command = "InitializeWorkflow"
    e7.commandAttributeChangedEventRequest.attribute = "arguments"
    e8 = request.eventrequest.add(rules="workflow")
    e8.commandExecutedEventRequest.path = ""
    e8.commandExecutedEventRequest.command = "InitializeWorkflow"
    response = session._datamodel_service_se.subscribe_events(MessageToDict(request))
    assert all(
        [
            r["status"] == datamodel_se_pb2.STATUS_SUBSCRIBED and r["tag"] == t
            for r, t in zip(response, tags)
        ]
    )
    response = session._datamodel_service_se.unsubscribe_events(tags)
    assert all(
        [
            r["status"] == datamodel_se_pb2.STATUS_UNSUBSCRIBED and r["tag"] == t
            for r, t in zip(response, tags)
        ]
    )


@pytest.mark.fluent_version(">=23.2")
@pytest.mark.codegen_required
def test_add_on_child_created(new_meshing_session):
    meshing = new_meshing_session
    child_paths = []
    subscription = meshing.workflow.add_on_child_created(
        "TaskObject", lambda obj: child_paths.append(convert_path_to_se_path(obj.path))
    )
    assert child_paths == []
    meshing.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")
    sleep(5)
    assert len(child_paths) > 0
    child_paths.clear()
    subscription.unsubscribe()
    meshing.workflow.InitializeWorkflow(WorkflowType="Fault-tolerant Meshing")
    sleep(5)
    assert child_paths == []


@pytest.mark.fluent_version(">=23.2")
@pytest.mark.codegen_required
def test_add_on_deleted(new_meshing_session):
    meshing = new_meshing_session
    meshing.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")
    data = []
    _ = meshing.workflow.TaskObject["Import Geometry"].add_on_deleted(
        lambda: data.append(True)
    )
    assert data == []
    meshing.workflow.InitializeWorkflow(WorkflowType="Fault-tolerant Meshing")
    sleep(5)
    assert len(data) > 0


@pytest.mark.fluent_version(">=23.2")
@pytest.mark.codegen_required
def test_add_on_changed(new_meshing_session):
    meshing = new_meshing_session
    task_list = meshing.workflow.Workflow.TaskList
    assert isinstance(task_list(), list)
    assert len(task_list()) == 0
    data = []
    subscription = task_list.add_on_changed(lambda obj: data.append(True))
    assert data == []
    meshing.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")
    sleep(5)
    assert len(data) > 0
    assert len(task_list()) > 0
    data.clear()
    subscription.unsubscribe()
    meshing.workflow.InitializeWorkflow(WorkflowType="Fault-tolerant Meshing")
    sleep(5)
    assert data == []


@pytest.mark.fluent_version(">=23.2")
@pytest.mark.codegen_required
def test_add_on_affected(new_meshing_session):
    meshing = new_meshing_session
    data = []
    subscription = meshing.workflow.Workflow.add_on_affected(
        lambda obj: data.append(True)
    )
    assert data == []
    wt = meshing.watertight()
    sleep(5)
    assert len(data) > 0
    assert data[0]

    calls = []
    subscription2 = meshing.workflow.add_on_affected(lambda obj: calls.append(True))
    geom = examples.download_file(
        file_name="mixing_elbow.pmdb", directory="pyfluent/mixing_elbow"
    )
    import_geom = meshing.workflow.TaskObject["Import Geometry"]
    assert "FileName" not in import_geom.Arguments()
    assert wt.import_geometry.command_arguments()["FileName"] is None
    import_geom.Arguments = {"FileName": geom}
    assert import_geom.Arguments()["FileName"] == geom
    assert wt.import_geometry.command_arguments()["FileName"] == geom
    sleep(1)
    assert calls == [True]
    import_geom.Arguments = {"FileName": "dummy"}
    sleep(1)
    assert calls == 2 * [True]
    import_geom.Arguments = {"FileName": geom}
    sleep(1)
    assert calls == 3 * [True]
    execute_state = [meshing.workflow()]
    import_geom.Execute()
    calls_after_execute = []
    loop_count = 10
    for i in range(loop_count):
        sleep(5)
        calls_after_execute.append(list(calls))
        execute_state.append(meshing.workflow())
    assert all(state == execute_state[1] for state in execute_state[2:])
    call_count = sum(map(len, calls_after_execute))
    assert call_count == 6 * loop_count
    assert calls_after_execute == loop_count * [6 * [True]]
    subscription2.unsubscribe()

    data.clear()
    subscription.unsubscribe()
    meshing.workflow.InitializeWorkflow(WorkflowType="Fault-tolerant Meshing")
    sleep(5)
    assert data == []


@pytest.mark.fluent_version(">=23.2")
@pytest.mark.codegen_required
def test_add_on_affected_at_type_path(new_meshing_session):
    meshing = new_meshing_session
    data = []
    subscription = meshing.workflow.add_on_affected_at_type_path(
        "TaskObject", lambda obj: data.append(True)
    )
    assert data == []
    meshing.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")
    sleep(5)
    assert len(data) > 0
    assert data[0]
    data.clear()
    subscription.unsubscribe()
    meshing.workflow.InitializeWorkflow(WorkflowType="Fault-tolerant Meshing")
    sleep(5)
    assert data == []


@pytest.mark.fluent_version(">=23.2")
@pytest.mark.codegen_required
def test_add_on_command_executed(new_meshing_session):
    meshing = new_meshing_session
    data = []
    version = meshing.get_fluent_version()
    if version < FluentVersion.v252:
        subscription = meshing.meshing.add_on_command_executed_old(
            "ImportGeometry", lambda obj, command, args: data.append(True)
        )
    else:
        subscription = meshing.meshing.add_on_command_executed(
            lambda obj, command, args: data.append(True)
        )
    assert data == []
    meshing.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")
    import_file_name = examples.download_file(
        "mixing_elbow.pmdb", "pyfluent/mixing_elbow"
    )
    meshing.meshing.ImportGeometry(FileName=import_file_name)
    sleep(5)
    assert len(data) > 0
    assert data[0]
    data.clear()
    subscription.unsubscribe()
    meshing.meshing.ImportGeometry(FileName=import_file_name)
    sleep(5)
    assert data == []


@pytest.mark.skip("https://github.com/ansys/pyfluent/issues/2999")
@pytest.mark.fluent_version(">=23.2")
@pytest.mark.codegen_required
def test_datamodel_streaming_full_diff_state(
    disable_datamodel_cache, new_meshing_session
):
    meshing = new_meshing_session
    datamodel_service_se = meshing._datamodel_service_se
    stream = DatamodelStream(datamodel_service_se)
    stream.start(rules="meshing", no_commands_diff_state=False)

    def cb(state, deleted_paths):
        if state:
            state = _convert_variant_to_value(state)
        cb.states.append(state)

    cb.states = []

    stream.register_callback(cb)

    meshing.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")
    import_file_name = examples.download_file(
        "mixing_elbow.pmdb", "pyfluent/mixing_elbow"
    )
    meshing.meshing.ImportGeometry(FileName=import_file_name)
    sleep(5)
    assert "ImportGeometry:ImportGeometry1" in (y for x in cb.states for y in x)


@pytest.mark.fluent_version(">=23.2")
@pytest.mark.codegen_required
def test_datamodel_streaming_no_commands_diff_state(
    disable_datamodel_cache, new_meshing_session
):
    meshing = new_meshing_session
    datamodel_service_se = meshing._datamodel_service_se
    stream = DatamodelStream(datamodel_service_se)
    stream.start(rules="meshing", no_commands_diff_state=True)

    def cb(state, deleted_paths):
        if state:
            state = _convert_variant_to_value(state)
        cb.states.append(state)

    cb.states = []

    stream.register_callback(cb)

    meshing.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")
    import_file_name = examples.download_file(
        "mixing_elbow.pmdb", "pyfluent/mixing_elbow"
    )
    meshing.meshing.ImportGeometry(FileName=import_file_name)
    sleep(5)
    assert "ImportGeometry:ImportGeometry1" not in (y for x in cb.states for y in x)


@pytest.mark.fluent_version(">=24.2")
@pytest.mark.codegen_required
def test_get_object_names_wtm(new_meshing_session):
    meshing = new_meshing_session

    assert not meshing.workflow.TaskObject.get_object_names()

    meshing.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")

    child_object_names = [
        "Import Geometry",
        "Add Local Sizing",
        "Generate the Surface Mesh",
        "Describe Geometry",
        "Apply Share Topology",
        "Enclose Fluid Regions (Capping)",
        "Update Boundaries",
        "Create Regions",
        "Update Regions",
        "Add Boundary Layers",
        "Generate the Volume Mesh",
    ]

    assert meshing.workflow.TaskObject.get_object_names() == child_object_names


@pytest.mark.fluent_version(">=23.2")
@pytest.mark.codegen_required
def test_get_and_set_state_for_command_arg_instance(new_meshing_session):
    meshing = new_meshing_session

    meshing.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")

    x = meshing.meshing.ImportGeometry.create_instance()

    assert x.LengthUnit() == "mm"

    assert x.LengthUnit.allowed_values() == ["m", "cm", "mm", "in", "ft", "um", "nm"]

    x.LengthUnit.set_state("ft")

    assert x.LengthUnit.get_state() == "ft"

    assert x.CadImportOptions.ExtractFeatures()

    x.CadImportOptions.ExtractFeatures.set_state(False)

    assert not x.CadImportOptions.ExtractFeatures()

    x.set_state({"FileName": "dummy_file_name.dummy_extn"})

    assert x.FileName() == "dummy_file_name.dummy_extn"


def _is_internal_name(name: str, prefix: str) -> bool:
    return name.startswith(prefix) and name.removeprefix(prefix).isdigit()


@pytest.mark.codegen_required
def test_task_object_keys_are_display_names(new_meshing_session):
    meshing = new_meshing_session
    meshing.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")
    task_object_state = meshing.workflow.TaskObject()
    assert len(task_object_state) > 0
    assert not any(_is_internal_name(x, "TaskObject:") for x in task_object_state)


def test_generic_datamodel(new_solver_session):
    solver = new_solver_session
    solver.scheme_eval.scheme_eval("(init-flserver)")
    flserver = PyMenuGeneric(solver._datamodel_service_se, "flserver")
    assert flserver.Case.Solution.Calculation.TimeStepSize() == 1.0


@pytest.mark.fluent_version(">=24.2")
def test_named_object_specific_methods_using_flserver(new_solver_session):
    import_file_name = examples.download_file(
        "mixing_elbow.cas.h5", "pyfluent/mixing_elbow"
    )
    solver = new_solver_session
    solver.file.read(file_type="case", file_name=import_file_name)
    solver.solution.initialization.hybrid_initialize()
    solver.solution.run_calculation.iterate(iter_count=10)
    solver.tui.display.objects.create(
        "contour",
        "contour-z1",
        "field",
        "velocity-magnitude",
        "surfaces-list",
        "cold-inlet",
    )
    solver.tui.display.objects.create(
        "contour",
        "contour-z2",
        "field",
        "velocity-magnitude",
        "surfaces-list",
        "hot-inlet",
    )
    solver.tui.display.objects.create(
        "contour",
        "contour-z3",
        "field",
        "velocity-magnitude",
        "surfaces-list",
        "outlet",
    )
    solver.tui.display.objects.create(
        "contour",
        "contour-z4",
        "field",
        "velocity-magnitude",
        "surfaces-list",
        "wall-elbow",
    )
    solver.tui.display.objects.create(
        "contour",
        "contour-z5",
        "field",
        "velocity-magnitude",
        "surfaces-list",
        "wall-inlet",
    )

    flserver = PyMenuGeneric(solver._datamodel_service_se, "flserver")

    assert set(flserver.Case.Results.Graphics.Contour.get_object_names()) == {
        "contour-z1",
        "contour-z2",
        "contour-z3",
        "contour-z4",
        "contour-z5",
    }

    assert "contour-x1" not in flserver.Case.Results.Graphics.Contour.get_object_names()

    flserver.Case.Results.Graphics.Contour["contour-z1"].rename("contour-x1")

    assert "contour-x1" in flserver.Case.Results.Graphics.Contour.get_object_names()

    flserver.Case.Results.Graphics.delete_child_objects(
        "Contour", ["contour-x1", "contour-z2"]
    )

    assert set(flserver.Case.Results.Graphics.Contour.get_object_names()) == {
        "contour-z3",
        "contour-z4",
        "contour-z5",
    }

    flserver.Case.Results.Graphics.delete_all_child_objects("Contour")

    assert not flserver.Case.Results.Graphics.Contour.get_object_names()


@pytest.mark.fluent_version(">=24.2")
def test_named_object_specific_methods(new_meshing_session):
    meshing = new_meshing_session
    meshing.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")

    assert set(meshing.workflow.TaskObject.get_object_names()) == {
        "Import Geometry",
        "Add Local Sizing",
        "Generate the Surface Mesh",
        "Describe Geometry",
        "Apply Share Topology",
        "Enclose Fluid Regions (Capping)",
        "Update Boundaries",
        "Create Regions",
        "Update Regions",
        "Add Boundary Layers",
        "Generate the Volume Mesh",
    }

    assert "xyz" not in meshing.workflow.TaskObject.get_object_names()

    meshing.workflow.TaskObject["Import Geometry"].rename("xyz")

    assert "xyz" in meshing.workflow.TaskObject.get_object_names()

    meshing.workflow.delete_all_child_objects("TaskObject")

    assert not meshing.workflow.TaskObject.get_object_names()

    # test availability of different ways to get container state:
    TaskObject = meshing.workflow.TaskObject
    assert TaskObject.get_state() == TaskObject.getState() == TaskObject()


@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=24.1")
def test_command_creation_inside_singleton(new_meshing_session):
    meshing = new_meshing_session
    read_mesh = meshing.meshing.File.ReadMesh.create_instance()
    assert read_mesh.FileName is not None


@pytest.mark.codegen_required
def test_read_only_set_state(new_meshing_session):
    meshing = new_meshing_session
    meshing.preferences.MeshingWorkflow.SaveCheckpointFiles = True
    assert meshing.preferences.MeshingWorkflow.CheckpointingOption.is_read_only()
    with pytest.raises(ReadOnlyObjectError):
        meshing.preferences.MeshingWorkflow.CheckpointingOption = "Write into memory"

    assert "set_state" not in dir(
        meshing.preferences.MeshingWorkflow.CheckpointingOption
    )


test_rules = (
    "RULES:\n"
    "    SINGLETON: ROOT\n"
    "        members = A\n"
    "        OBJECT: A\n"
    "            members = B, X\n"
    "            commands = C\n"
    "            isABC = $./X == ABC\n"
    "            OBJECT: B\n"
    "            END\n"
    "            STRING: X\n"
    "                default = IJK\n"
    "            END\n"
    "            COMMAND: C\n"
    "                returnType = Logical\n"
    "                functionName = S_C\n"
    "                isABC = $../X == ABC\n"
    "            END\n"
    "        END\n"
    "     END\n"
    "END\n"
)


@pytest.mark.fluent_version(">=24.2")
def test_on_child_created_lifetime(new_solver_session):
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, test_rules, app_name)
    root = create_root_using_datamodelgen(solver._se_service, app_name)
    root.A["A1"] = {}
    data = []
    _ = root.A["A1"].add_on_child_created("B", lambda _: data.append(1))
    root.A["A1"].add_on_child_created("B", lambda _: data.append(2))
    gc.collect()
    assert "/test/created/A:A1/B" in solver._se_service.subscriptions
    assert "/test/created/A:A1/B-1" in solver._se_service.subscriptions
    root.A["A1"].B["B1"] = {}
    assert timeout_loop(lambda: data == [1, 2], 5)
    del root.A["A1"]
    assert "/test/created/A:A1/B" not in solver._se_service.subscriptions
    assert "/test/created/A:A1/B-1" not in solver._se_service.subscriptions


@pytest.mark.fluent_version(">=24.2")
def test_on_deleted_lifetime(new_solver_session):
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, test_rules, app_name)
    root = create_root_using_datamodelgen(solver._se_service, app_name)
    root.A["A1"] = {}
    data = []
    _ = root.A["A1"].add_on_deleted(lambda: data.append(1))
    root.A["A1"].add_on_deleted(lambda: data.append(2))
    gc.collect()
    assert "/test/deleted/A:A1" in solver._se_service.subscriptions
    assert "/test/deleted/A:A1-1" in solver._se_service.subscriptions
    del root.A["A1"]
    assert timeout_loop(lambda: data == [1, 2], 5)
    assert timeout_loop(
        lambda: "/test/deleted/A:A1" not in solver._se_service.subscriptions, 5
    )
    assert timeout_loop(
        lambda: "/test/deleted/A:A1-1" not in solver._se_service.subscriptions, 5
    )


@pytest.mark.fluent_version(">=24.2")
def test_on_changed_lifetime(new_solver_session):
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, test_rules, app_name)
    root = create_root_using_datamodelgen(solver._se_service, app_name)
    root.A["A1"] = {}
    data = []
    _ = root.A["A1"].X.add_on_changed(lambda _: data.append(1))
    root.A["A1"].X.add_on_changed(lambda _: data.append(2))
    gc.collect()
    assert "/test/modified/A:A1/X" in solver._se_service.subscriptions
    assert "/test/modified/A:A1/X-1" in solver._se_service.subscriptions
    root.A["A1"].X = "ABC"
    assert timeout_loop(lambda: data == [1, 2], 5)
    del root.A["A1"]
    assert "/test/modified/A:A1/X" not in solver._se_service.subscriptions
    assert "/test/modified/A:A1/X-1" not in solver._se_service.subscriptions


@pytest.mark.fluent_version(">=24.2")
def test_on_affected_lifetime(new_solver_session):
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, test_rules, app_name)
    root = create_root_using_datamodelgen(solver._se_service, app_name)
    root.A["A1"] = {}
    data = []
    _ = root.A["A1"].add_on_affected(lambda _: data.append(1))
    root.A["A1"].add_on_affected(lambda _: data.append(2))
    gc.collect()
    assert "/test/affected/A:A1" in solver._se_service.subscriptions
    assert "/test/affected/A:A1-1" in solver._se_service.subscriptions
    root.A["A1"].X = "ABC"
    assert timeout_loop(lambda: data == [1, 2], 5)
    del root.A["A1"]
    assert "/test/affected/A:A1" not in solver._se_service.subscriptions
    assert "/test/affected/A:A1-1" not in solver._se_service.subscriptions


@pytest.mark.fluent_version(">=24.2")
def test_on_affected_at_type_path_lifetime(new_solver_session):
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, test_rules, app_name)
    root = create_root_using_datamodelgen(solver._se_service, app_name)
    root.A["A1"] = {}
    data = []
    _ = root.A["A1"].add_on_affected_at_type_path("B", lambda _: data.append(1))
    root.A["A1"].add_on_affected_at_type_path("B", lambda _: data.append(2))
    gc.collect()
    assert "/test/affected/A:A1/B" in solver._se_service.subscriptions
    assert "/test/affected/A:A1/B-1" in solver._se_service.subscriptions
    root.A["A1"].B["B1"] = {}
    assert timeout_loop(lambda: data == [1, 2], 5)
    del root.A["A1"]
    assert "/test/affected/A:A1/B" not in solver._se_service.subscriptions
    assert "/test/affected/A:A1/B-1" not in solver._se_service.subscriptions


@pytest.mark.fluent_version(">=24.2")
def test_on_command_executed_lifetime(new_solver_session):
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, test_rules, app_name)
    root = create_root_using_datamodelgen(solver._se_service, app_name)
    root.A["A1"] = {}
    data = []
    version = solver.get_fluent_version()
    if version < FluentVersion.v252:
        _ = root.A["A1"].add_on_command_executed_old("C", lambda *args: data.append(1))
        root.A["A1"].add_on_command_executed_old("C", lambda *args: data.append(2))
        tags = ["/test/command_executed/A:A1/C", "/test/command_executed/A:A1/C-1"]
    else:
        _ = root.A["A1"].add_on_command_executed(lambda *args: data.append(1))
        root.A["A1"].add_on_command_executed(lambda *args: data.append(2))
        tags = ["/test/command_executed/A:A1", "/test/command_executed/A:A1-1"]
    gc.collect()
    for tag in tags:
        assert tag in solver._se_service.subscriptions
    root.A["A1"].C()
    assert timeout_loop(lambda: data == [1, 2], 5)
    del root.A["A1"]
    for tag in tags:
        assert tag not in solver._se_service.subscriptions


@pytest.mark.fluent_version(">=24.2")
def test_on_attribute_changed_lifetime(new_solver_session):
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, test_rules, app_name)
    root = create_root_using_datamodelgen(solver._se_service, app_name)
    root.A["A1"] = {}
    data = []
    _ = root.A["A1"].add_on_attribute_changed("isABC", lambda _: data.append(1))
    root.A["A1"].add_on_attribute_changed("isABC", lambda _: data.append(2))
    gc.collect()
    assert "/test/attribute_changed/A:A1/isABC" in solver._se_service.subscriptions
    assert "/test/attribute_changed/A:A1/isABC-1" in solver._se_service.subscriptions
    root.A["A1"].X = "ABC"
    assert timeout_loop(lambda: data == [1, 2], 5)
    del root.A["A1"]
    assert "/test/attribute_changed/A:A1/isABC" not in solver._se_service.subscriptions
    assert (
        "/test/attribute_changed/A:A1/isABC-1" not in solver._se_service.subscriptions
    )


@pytest.mark.fluent_version(">=24.2")
def test_on_command_attribute_changed_lifetime(new_solver_session):
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, test_rules, app_name)
    root = create_root_using_datamodelgen(solver._se_service, app_name)
    root.A["A1"] = {}
    data = []
    _ = root.A["A1"].add_on_command_attribute_changed(
        "C", "isABC", lambda _: data.append(1)
    )
    root.A["A1"].add_on_command_attribute_changed(
        "C", "isABC", lambda _: data.append(2)
    )
    gc.collect()
    assert (
        "/test/command_attribute_changed/A:A1/C/isABC"
        in solver._se_service.subscriptions
    )
    assert (
        "/test/command_attribute_changed/A:A1/C/isABC-1"
        in solver._se_service.subscriptions
    )
    root.A["A1"].X = "ABC"
    assert timeout_loop(lambda: data == [1, 2], 5)
    del root.A["A1"]
    assert (
        "/test/command_attribute_changed/A:A1/C/isABC"
        not in solver._se_service.subscriptions
    )
    assert (
        "/test/command_attribute_changed/A:A1/C/isABC-1"
        not in solver._se_service.subscriptions
    )


@pytest.mark.fluent_version(">=24.2")
def test_on_affected_lifetime_with_delete_child_objects(new_solver_session):
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, test_rules, app_name)
    root = create_root_using_datamodelgen(solver._se_service, app_name)
    pyfluent.logging.enable()
    root.A["A1"] = {}
    data = []
    _ = root.A["A1"].add_on_affected(lambda _: data.append(1))
    root.A["A1"].add_on_affected(lambda _: data.append(2))
    gc.collect()
    assert "/test/affected/A:A1" in solver._se_service.subscriptions
    assert "/test/affected/A:A1-1" in solver._se_service.subscriptions
    root.A["A1"].X = "ABC"
    assert timeout_loop(lambda: data == [1, 2], 5)
    root.delete_child_objects("A", ["A1"])
    assert "/test/affected/A:A1" not in solver._se_service.subscriptions
    assert "/test/affected/A:A1-1" not in solver._se_service.subscriptions


@pytest.mark.fluent_version(">=24.2")
def test_on_affected_lifetime_with_delete_all_child_objects(new_solver_session):
    solver = new_solver_session
    app_name = "test"
    create_datamodel_root_in_server(solver, test_rules, app_name)
    root = create_root_using_datamodelgen(solver._se_service, app_name)
    pyfluent.logging.enable()
    root.A["A1"] = {}
    data = []
    _ = root.A["A1"].add_on_affected(lambda _: data.append(1))
    root.A["A1"].add_on_affected(lambda _: data.append(2))
    gc.collect()
    assert "/test/affected/A:A1" in solver._se_service.subscriptions
    assert "/test/affected/A:A1-1" in solver._se_service.subscriptions
    root.A["A1"].X = "ABC"
    assert timeout_loop(lambda: data == [1, 2], 5)
    root.delete_all_child_objects("A")
    assert "/test/affected/A:A1" not in solver._se_service.subscriptions
    assert "/test/affected/A:A1-1" not in solver._se_service.subscriptions


@pytest.mark.fluent_version(">=23.2")
def test_set_command_args_and_sub_args(new_meshing_session):
    meshing = new_meshing_session
    ig = meshing.meshing.ImportGeometry.create_instance()

    # Command Arguments
    assert ig.MeshUnit() == "m"
    ig.MeshUnit = "mm"
    assert ig.MeshUnit() == "mm"

    # Command Arguments SubItem
    assert ig.CadImportOptions.OneZonePer() == "body"
    ig.CadImportOptions.OneZonePer = "face"
    assert ig.CadImportOptions.OneZonePer() == "face"


@pytest.mark.fluent_version(">=24.1")
def test_dynamic_dependency(new_meshing_session):
    meshing = new_meshing_session
    ic = meshing.meshing.LoadCADGeometry.create_instance()

    d = ic.Refaceting.Deviation.get_state()
    cd = ic.Refaceting.CustomDeviation.get_state()
    assert d == cd

    ic.Refaceting.Deviation.set_state(1.2)
    d = ic.Refaceting.Deviation.get_state()
    cd = ic.Refaceting.CustomDeviation.get_state()
    assert d == cd
