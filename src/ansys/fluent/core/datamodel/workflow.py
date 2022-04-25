#
# This is an auto-generated file.  DO NOT EDIT!
#
# pylint: disable=line-too-long

from ansys.fluent.core.services.datamodel_se import (
    PyMenu,
    PyNamedObjectContainer,
    PyCommand
)


class Root(PyMenu):
    """
    Singleton Root.
    """
    def __init__(self, service, rules, path):
        self.TaskObject = self.__class__.TaskObject(service, rules, path + [("TaskObject", "")])
        self.Workflow = self.__class__.Workflow(service, rules, path + [("Workflow", "")])
        self.InsertNewTask = self.__class__.InsertNewTask(service, rules, "InsertNewTask", path)
        self.SaveWorkflow = self.__class__.SaveWorkflow(service, rules, "SaveWorkflow", path)
        self.InitializeWorkflow = self.__class__.InitializeWorkflow(service, rules, "InitializeWorkflow", path)
        self.LoadState = self.__class__.LoadState(service, rules, "LoadState", path)
        self.CreateCompositeTask = self.__class__.CreateCompositeTask(service, rules, "CreateCompositeTask", path)
        self.ResetWorkflow = self.__class__.ResetWorkflow(service, rules, "ResetWorkflow", path)
        self.LoadWorkflow = self.__class__.LoadWorkflow(service, rules, "LoadWorkflow", path)
        self.CreateNewWorkflow = self.__class__.CreateNewWorkflow(service, rules, "CreateNewWorkflow", path)
        self.DeleteTasks = self.__class__.DeleteTasks(service, rules, "DeleteTasks", path)
        super().__init__(service, rules, path)

    class TaskObject(PyNamedObjectContainer):
        class _TaskObject(PyMenu):
            """
            Singleton _TaskObject.
            """
            def __init__(self, service, rules, path):
                self.TaskType = self.__class__.TaskType(service, rules, path + [("TaskType", "")])
                self.InactiveTaskList = self.__class__.InactiveTaskList(service, rules, path + [("InactiveTaskList", "")])
                self.TaskList = self.__class__.TaskList(service, rules, path + [("TaskList", "")])
                self.ObjectPath = self.__class__.ObjectPath(service, rules, path + [("ObjectPath", "")])
                self.CommandName = self.__class__.CommandName(service, rules, path + [("CommandName", "")])
                self.Warnings = self.__class__.Warnings(service, rules, path + [("Warnings", "")])
                self.Arguments = self.__class__.Arguments(service, rules, path + [("Arguments", "")])
                self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                self.Errors = self.__class__.Errors(service, rules, path + [("Errors", "")])
                self.State = self.__class__.State(service, rules, path + [("State", "")])
                self.UpdateChildTasks = self.__class__.UpdateChildTasks(service, rules, "UpdateChildTasks", path)
                self.Revert = self.__class__.Revert(service, rules, "Revert", path)
                self.InsertCompositeChildTask = self.__class__.InsertCompositeChildTask(service, rules, "InsertCompositeChildTask", path)
                self.SetAsCurrent = self.__class__.SetAsCurrent(service, rules, "SetAsCurrent", path)
                self.ForceUptoDate = self.__class__.ForceUptoDate(service, rules, "ForceUptoDate", path)
                self.AddChildToTask = self.__class__.AddChildToTask(service, rules, "AddChildToTask", path)
                self.InsertCompoundChildTask = self.__class__.InsertCompoundChildTask(service, rules, "InsertCompoundChildTask", path)
                self.ExecuteUpstreamNonExecutedAndThisTask = self.__class__.ExecuteUpstreamNonExecutedAndThisTask(service, rules, "ExecuteUpstreamNonExecutedAndThisTask", path)
                self.Execute = self.__class__.Execute(service, rules, "Execute", path)
                self.GetNextPossibleTasks = self.__class__.GetNextPossibleTasks(service, rules, "GetNextPossibleTasks", path)
                self.InsertNextTask = self.__class__.InsertNextTask(service, rules, "InsertNextTask", path)
                self.Rename = self.__class__.Rename(service, rules, "Rename", path)
                super().__init__(service, rules, path)

            class TaskType(PyMenu):
                """
                Parameter TaskType of value type str.
                """
                pass

            class InactiveTaskList(PyMenu):
                """
                Parameter InactiveTaskList of value type List[str].
                """
                pass

            class TaskList(PyMenu):
                """
                Parameter TaskList of value type List[str].
                """
                pass

            class ObjectPath(PyMenu):
                """
                Parameter ObjectPath of value type str.
                """
                pass

            class CommandName(PyMenu):
                """
                Parameter CommandName of value type str.
                """
                pass

            class Warnings(PyMenu):
                """
                Parameter Warnings of value type List[str].
                """
                pass

            class Arguments(PyMenu):
                """
                Parameter Arguments of value type Dict[str, Any].
                """
                pass

            class _name_(PyMenu):
                """
                Parameter _name_ of value type str.
                """
                pass

            class Errors(PyMenu):
                """
                Parameter Errors of value type List[str].
                """
                pass

            class State(PyMenu):
                """
                Parameter State of value type str.
                """
                pass

            class UpdateChildTasks(PyCommand):
                """
                UpdateChildTasks(SetupTypeChanged: bool) -> bool
                """
                pass

            class Revert(PyCommand):
                """
                Revert() -> bool
                """
                pass

            class InsertCompositeChildTask(PyCommand):
                """
                InsertCompositeChildTask(CommandName: str) -> bool
                """
                pass

            class SetAsCurrent(PyCommand):
                """
                SetAsCurrent() -> bool
                """
                pass

            class ForceUptoDate(PyCommand):
                """
                ForceUptoDate() -> bool
                """
                pass

            class AddChildToTask(PyCommand):
                """
                AddChildToTask() -> bool
                """
                pass

            class InsertCompoundChildTask(PyCommand):
                """
                InsertCompoundChildTask() -> bool
                """
                pass

            class ExecuteUpstreamNonExecutedAndThisTask(PyCommand):
                """
                ExecuteUpstreamNonExecutedAndThisTask() -> bool
                """
                pass

            class Execute(PyCommand):
                """
                Execute(Force: bool) -> bool
                """
                pass

            class GetNextPossibleTasks(PyCommand):
                """
                GetNextPossibleTasks() -> bool
                """
                pass

            class InsertNextTask(PyCommand):
                """
                InsertNextTask(CommandName: str, Select: bool) -> bool
                """
                pass

            class Rename(PyCommand):
                """
                Rename(NewName: str) -> bool
                """
                pass

        def __getitem__(self, key: str) -> _TaskObject:
            return super().__getitem__(key)

    class Workflow(PyMenu):
        """
        Singleton Workflow.
        """
        def __init__(self, service, rules, path):
            self.CurrentTask = self.__class__.CurrentTask(service, rules, path + [("CurrentTask", "")])
            self.TaskList = self.__class__.TaskList(service, rules, path + [("TaskList", "")])
            super().__init__(service, rules, path)

        class CurrentTask(PyMenu):
            """
            Parameter CurrentTask of value type str.
            """
            pass

        class TaskList(PyMenu):
            """
            Parameter TaskList of value type List[str].
            """
            pass

    class InsertNewTask(PyCommand):
        """
        InsertNewTask(CommandName: str) -> bool
        """
        pass

    class SaveWorkflow(PyCommand):
        """
        SaveWorkflow(FilePath: str) -> bool
        """
        pass

    class InitializeWorkflow(PyCommand):
        """
        InitializeWorkflow(WorkflowType: str) -> bool
        """
        pass

    class LoadState(PyCommand):
        """
        LoadState(ListOfRoots: List[str]) -> bool
        """
        pass

    class CreateCompositeTask(PyCommand):
        """
        CreateCompositeTask(ListOfTasks: List[str]) -> bool
        """
        pass

    class ResetWorkflow(PyCommand):
        """
        ResetWorkflow() -> bool
        """
        pass

    class LoadWorkflow(PyCommand):
        """
        LoadWorkflow(FilePath: str) -> bool
        """
        pass

    class CreateNewWorkflow(PyCommand):
        """
        CreateNewWorkflow() -> bool
        """
        pass

    class DeleteTasks(PyCommand):
        """
        DeleteTasks(ListOfTasks: List[str]) -> bool
        """
        pass

