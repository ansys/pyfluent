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
        self.ObjectSetting = self.__class__.ObjectSetting(service, rules, path + [("ObjectSetting", "")])
        self.Node = self.__class__.Node(service, rules, path + [("Node", "")])
        self.AssemblyNode = self.__class__.AssemblyNode(service, rules, path + [("AssemblyNode", "")])
        self.Transform = self.__class__.Transform(service, rules, path + [("Transform", "")])
        self.Refaceting = self.__class__.Refaceting(service, rules, path + [("Refaceting", "")])
        self.MeshingOperations = self.__class__.MeshingOperations(service, rules, path + [("MeshingOperations", "")])
        self.ObjectSettingOperations = self.__class__.ObjectSettingOperations(service, rules, path + [("ObjectSettingOperations", "")])
        self.GlobalSettings = self.__class__.GlobalSettings(service, rules, path + [("GlobalSettings", "")])
        self.TransformOperations = self.__class__.TransformOperations(service, rules, path + [("TransformOperations", "")])
        self.RefacetingOperations = self.__class__.RefacetingOperations(service, rules, path + [("RefacetingOperations", "")])
        self.Delete = self.__class__.Delete(service, rules, "Delete", path)
        self.ResetTemplate = self.__class__.ResetTemplate(service, rules, "ResetTemplate", path)
        self.LoadTemplate = self.__class__.LoadTemplate(service, rules, "LoadTemplate", path)
        self.MoveToObject = self.__class__.MoveToObject(service, rules, "MoveToObject", path)
        self.ChangeFileLengthUnit = self.__class__.ChangeFileLengthUnit(service, rules, "ChangeFileLengthUnit", path)
        self.MoveCADComponentsToNewObject = self.__class__.MoveCADComponentsToNewObject(service, rules, "MoveCADComponentsToNewObject", path)
        self.SaveFmdFile = self.__class__.SaveFmdFile(service, rules, "SaveFmdFile", path)
        self.InitializeTemplate = self.__class__.InitializeTemplate(service, rules, "InitializeTemplate", path)
        self.DeletePaths = self.__class__.DeletePaths(service, rules, "DeletePaths", path)
        self.CreateObjects = self.__class__.CreateObjects(service, rules, "CreateObjects", path)
        self.UndoAllTransforms = self.__class__.UndoAllTransforms(service, rules, "UndoAllTransforms", path)
        self.CreateObjForEachPart = self.__class__.CreateObjForEachPart(service, rules, "CreateObjForEachPart", path)
        self.LoadFmdFile = self.__class__.LoadFmdFile(service, rules, "LoadFmdFile", path)
        self.InputFileChanged = self.__class__.InputFileChanged(service, rules, "InputFileChanged", path)
        self.RedoAllTransforms = self.__class__.RedoAllTransforms(service, rules, "RedoAllTransforms", path)
        self.ListMeshingOperations = self.__class__.ListMeshingOperations(service, rules, "ListMeshingOperations", path)
        self.SaveTemplate = self.__class__.SaveTemplate(service, rules, "SaveTemplate", path)
        self.AppendFmdFiles = self.__class__.AppendFmdFiles(service, rules, "AppendFmdFiles", path)
        self.ChangeLengthUnit = self.__class__.ChangeLengthUnit(service, rules, "ChangeLengthUnit", path)
        super().__init__(service, rules, path)

    class ObjectSetting(PyNamedObjectContainer):
        class _ObjectSetting(PyMenu):
            """
            Singleton _ObjectSetting.
            """
            def __init__(self, service, rules, path):
                self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                self.EdgeExtraction = self.__class__.EdgeExtraction(service, rules, path + [("EdgeExtraction", "")])
                self.Name = self.__class__.Name(service, rules, path + [("Name", "")])
                self.Context = self.__class__.Context(service, rules, path + [("Context", "")])
                self.PrefixObjectName = self.__class__.PrefixObjectName(service, rules, path + [("PrefixObjectName", "")])
                self.Children = self.__class__.Children(service, rules, path + [("Children", "")])
                self.OneZonePer = self.__class__.OneZonePer(service, rules, path + [("OneZonePer", "")])
                self.FeatureAngle = self.__class__.FeatureAngle(service, rules, path + [("FeatureAngle", "")])
                self.MergeChildren = self.__class__.MergeChildren(service, rules, path + [("MergeChildren", "")])
                self.Rename = self.__class__.Rename(service, rules, "Rename", path)
                super().__init__(service, rules, path)

            class _name_(PyMenu):
                """
                Parameter _name_ of value type str.
                """
                pass

            class EdgeExtraction(PyMenu):
                """
                Parameter EdgeExtraction of value type str.
                """
                pass

            class Name(PyMenu):
                """
                Parameter Name of value type str.
                """
                pass

            class Context(PyMenu):
                """
                Parameter Context of value type int.
                """
                pass

            class PrefixObjectName(PyMenu):
                """
                Parameter PrefixObjectName of value type bool.
                """
                pass

            class Children(PyMenu):
                """
                Parameter Children of value type List[str].
                """
                pass

            class OneZonePer(PyMenu):
                """
                Parameter OneZonePer of value type str.
                """
                pass

            class FeatureAngle(PyMenu):
                """
                Parameter FeatureAngle of value type float.
                """
                pass

            class MergeChildren(PyMenu):
                """
                Parameter MergeChildren of value type bool.
                """
                pass

            class Rename(PyCommand):
                """
                Rename(NewName: str) -> bool
                """
                pass

        def __getitem__(self, key: str) -> _ObjectSetting:
            return super().__getitem__(key)

    class Node(PyNamedObjectContainer):
        class _Node(PyMenu):
            """
            Singleton _Node.
            """
            def __init__(self, service, rules, path):
                self.Updated = self.__class__.Updated(service, rules, path + [("Updated", "")])
                self.KeyId = self.__class__.KeyId(service, rules, path + [("KeyId", "")])
                self.Children = self.__class__.Children(service, rules, path + [("Children", "")])
                self.RefacetOperation = self.__class__.RefacetOperation(service, rules, path + [("RefacetOperation", "")])
                self.Transformations = self.__class__.Transformations(service, rules, path + [("Transformations", "")])
                self.Parent = self.__class__.Parent(service, rules, path + [("Parent", "")])
                self.ObjectSetting = self.__class__.ObjectSetting(service, rules, path + [("ObjectSetting", "")])
                self.Name = self.__class__.Name(service, rules, path + [("Name", "")])
                self.Context = self.__class__.Context(service, rules, path + [("Context", "")])
                self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                self.Rename = self.__class__.Rename(service, rules, "Rename", path)
                self.CreateChild = self.__class__.CreateChild(service, rules, "CreateChild", path)
                self.Copy = self.__class__.Copy(service, rules, "Copy", path)
                self.Move = self.__class__.Move(service, rules, "Move", path)
                super().__init__(service, rules, path)

            class Updated(PyMenu):
                """
                Parameter Updated of value type bool.
                """
                pass

            class KeyId(PyMenu):
                """
                Parameter KeyId of value type int.
                """
                pass

            class Children(PyMenu):
                """
                Parameter Children of value type List[str].
                """
                pass

            class RefacetOperation(PyMenu):
                """
                Parameter RefacetOperation of value type str.
                """
                pass

            class Transformations(PyMenu):
                """
                Parameter Transformations of value type List[str].
                """
                pass

            class Parent(PyMenu):
                """
                Parameter Parent of value type str.
                """
                pass

            class ObjectSetting(PyMenu):
                """
                Parameter ObjectSetting of value type str.
                """
                pass

            class Name(PyMenu):
                """
                Parameter Name of value type str.
                """
                pass

            class Context(PyMenu):
                """
                Parameter Context of value type int.
                """
                pass

            class _name_(PyMenu):
                """
                Parameter _name_ of value type str.
                """
                pass

            class Rename(PyCommand):
                """
                Rename(NewName: str) -> bool
                """
                pass

            class CreateChild(PyCommand):
                """
                CreateChild(ChildName: str) -> bool
                """
                pass

            class Copy(PyCommand):
                """
                Copy(Paths: List[str]) -> bool
                """
                pass

            class Move(PyCommand):
                """
                Move(Paths: List[str]) -> bool
                """
                pass

        def __getitem__(self, key: str) -> _Node:
            return super().__getitem__(key)

    class AssemblyNode(PyNamedObjectContainer):
        class _AssemblyNode(PyMenu):
            """
            Singleton _AssemblyNode.
            """
            def __init__(self, service, rules, path):
                self.Refaceting = self.__class__.Refaceting(service, rules, path + [("Refaceting", "")])
                self.Transformations = self.__class__.Transformations(service, rules, path + [("Transformations", "")])
                self.Context = self.__class__.Context(service, rules, path + [("Context", "")])
                self.FeatureAngle = self.__class__.FeatureAngle(service, rules, path + [("FeatureAngle", "")])
                self.KeyId = self.__class__.KeyId(service, rules, path + [("KeyId", "")])
                self.RefacetOperation = self.__class__.RefacetOperation(service, rules, path + [("RefacetOperation", "")])
                self.Children = self.__class__.Children(service, rules, path + [("Children", "")])
                self.EdgeExtraction = self.__class__.EdgeExtraction(service, rules, path + [("EdgeExtraction", "")])
                self.OneZonePer = self.__class__.OneZonePer(service, rules, path + [("OneZonePer", "")])
                self.PrefixObjectName = self.__class__.PrefixObjectName(service, rules, path + [("PrefixObjectName", "")])
                self.MergeChildren = self.__class__.MergeChildren(service, rules, path + [("MergeChildren", "")])
                self.Parent = self.__class__.Parent(service, rules, path + [("Parent", "")])
                self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                self.Name = self.__class__.Name(service, rules, path + [("Name", "")])
                self.IsChildrenSettingsChanged = self.__class__.IsChildrenSettingsChanged(service, rules, path + [("IsChildrenSettingsChanged", "")])
                self.ReFacetNow = self.__class__.ReFacetNow(service, rules, "ReFacetNow", path)
                self.Move = self.__class__.Move(service, rules, "Move", path)
                self.ReFacet = self.__class__.ReFacet(service, rules, "ReFacet", path)
                self.Rename = self.__class__.Rename(service, rules, "Rename", path)
                self.ChangeChildrenSettings = self.__class__.ChangeChildrenSettings(service, rules, "ChangeChildrenSettings", path)
                self.CreateChild = self.__class__.CreateChild(service, rules, "CreateChild", path)
                self.Copy = self.__class__.Copy(service, rules, "Copy", path)
                super().__init__(service, rules, path)

            class Refaceting(PyMenu):
                """
                Singleton Refaceting.
                """
                def __init__(self, service, rules, path):
                    self.NormalAngle = self.__class__.NormalAngle(service, rules, path + [("NormalAngle", "")])
                    self.Refacet = self.__class__.Refacet(service, rules, path + [("Refacet", "")])
                    self.Deviation = self.__class__.Deviation(service, rules, path + [("Deviation", "")])
                    self.MaxSize = self.__class__.MaxSize(service, rules, path + [("MaxSize", "")])
                    super().__init__(service, rules, path)

                class NormalAngle(PyMenu):
                    """
                    Parameter NormalAngle of value type float.
                    """
                    pass

                class Refacet(PyMenu):
                    """
                    Parameter Refacet of value type bool.
                    """
                    pass

                class Deviation(PyMenu):
                    """
                    Parameter Deviation of value type float.
                    """
                    pass

                class MaxSize(PyMenu):
                    """
                    Parameter MaxSize of value type float.
                    """
                    pass

            class Transformations(PyMenu):
                """
                Parameter Transformations of value type List[str].
                """
                pass

            class Context(PyMenu):
                """
                Parameter Context of value type int.
                """
                pass

            class FeatureAngle(PyMenu):
                """
                Parameter FeatureAngle of value type float.
                """
                pass

            class KeyId(PyMenu):
                """
                Parameter KeyId of value type int.
                """
                pass

            class RefacetOperation(PyMenu):
                """
                Parameter RefacetOperation of value type str.
                """
                pass

            class Children(PyMenu):
                """
                Parameter Children of value type List[str].
                """
                pass

            class EdgeExtraction(PyMenu):
                """
                Parameter EdgeExtraction of value type str.
                """
                pass

            class OneZonePer(PyMenu):
                """
                Parameter OneZonePer of value type str.
                """
                pass

            class PrefixObjectName(PyMenu):
                """
                Parameter PrefixObjectName of value type bool.
                """
                pass

            class MergeChildren(PyMenu):
                """
                Parameter MergeChildren of value type bool.
                """
                pass

            class Parent(PyMenu):
                """
                Parameter Parent of value type str.
                """
                pass

            class _name_(PyMenu):
                """
                Parameter _name_ of value type str.
                """
                pass

            class Name(PyMenu):
                """
                Parameter Name of value type str.
                """
                pass

            class IsChildrenSettingsChanged(PyMenu):
                """
                Parameter IsChildrenSettingsChanged of value type bool.
                """
                pass

            class ReFacetNow(PyCommand):
                """
                ReFacetNow() -> bool
                """
                pass

            class Move(PyCommand):
                """
                Move(Paths: List[str]) -> bool
                """
                pass

            class ReFacet(PyCommand):
                """
                ReFacet(Deviation: float, NormalAngle: float, MaxSize: float) -> bool
                """
                pass

            class Rename(PyCommand):
                """
                Rename(NewName: str) -> bool
                """
                pass

            class ChangeChildrenSettings(PyCommand):
                """
                ChangeChildrenSettings() -> bool
                """
                pass

            class CreateChild(PyCommand):
                """
                CreateChild(ChildName: str) -> bool
                """
                pass

            class Copy(PyCommand):
                """
                Copy(Paths: List[str]) -> bool
                """
                pass

        def __getitem__(self, key: str) -> _AssemblyNode:
            return super().__getitem__(key)

    class Transform(PyNamedObjectContainer):
        class _Transform(PyMenu):
            """
            Singleton _Transform.
            """
            def __init__(self, service, rules, path):
                self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                self.Name = self.__class__.Name(service, rules, path + [("Name", "")])
                self.Applied = self.__class__.Applied(service, rules, path + [("Applied", "")])
                self.Context = self.__class__.Context(service, rules, path + [("Context", "")])
                self.TranslateX = self.__class__.TranslateX(service, rules, path + [("TranslateX", "")])
                self.TranslateY = self.__class__.TranslateY(service, rules, path + [("TranslateY", "")])
                self.RotateZ = self.__class__.RotateZ(service, rules, path + [("RotateZ", "")])
                self.RotateX = self.__class__.RotateX(service, rules, path + [("RotateX", "")])
                self.RotateY = self.__class__.RotateY(service, rules, path + [("RotateY", "")])
                self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                self.TranslateZ = self.__class__.TranslateZ(service, rules, path + [("TranslateZ", "")])
                self.Children = self.__class__.Children(service, rules, path + [("Children", "")])
                self.Global = self.__class__.Global(service, rules, path + [("Global", "")])
                self.Undo = self.__class__.Undo(service, rules, "Undo", path)
                self.Apply = self.__class__.Apply(service, rules, "Apply", path)
                self.Delete = self.__class__.Delete(service, rules, "Delete", path)
                self.Update = self.__class__.Update(service, rules, "Update", path)
                self.Rename = self.__class__.Rename(service, rules, "Rename", path)
                super().__init__(service, rules, path)

            class _name_(PyMenu):
                """
                Parameter _name_ of value type str.
                """
                pass

            class Name(PyMenu):
                """
                Parameter Name of value type str.
                """
                pass

            class Applied(PyMenu):
                """
                Parameter Applied of value type bool.
                """
                pass

            class Context(PyMenu):
                """
                Parameter Context of value type int.
                """
                pass

            class TranslateX(PyMenu):
                """
                Parameter TranslateX of value type float.
                """
                pass

            class TranslateY(PyMenu):
                """
                Parameter TranslateY of value type float.
                """
                pass

            class RotateZ(PyMenu):
                """
                Parameter RotateZ of value type float.
                """
                pass

            class RotateX(PyMenu):
                """
                Parameter RotateX of value type float.
                """
                pass

            class RotateY(PyMenu):
                """
                Parameter RotateY of value type float.
                """
                pass

            class Type(PyMenu):
                """
                Parameter Type of value type str.
                """
                pass

            class TranslateZ(PyMenu):
                """
                Parameter TranslateZ of value type float.
                """
                pass

            class Children(PyMenu):
                """
                Parameter Children of value type List[str].
                """
                pass

            class Global(PyMenu):
                """
                Parameter Global of value type str.
                """
                pass

            class Undo(PyCommand):
                """
                Undo() -> bool
                """
                pass

            class Apply(PyCommand):
                """
                Apply() -> bool
                """
                pass

            class Delete(PyCommand):
                """
                Delete(Path: str) -> bool
                """
                pass

            class Update(PyCommand):
                """
                Update() -> bool
                """
                pass

            class Rename(PyCommand):
                """
                Rename(NewName: str) -> bool
                """
                pass

        def __getitem__(self, key: str) -> _Transform:
            return super().__getitem__(key)

    class Refaceting(PyNamedObjectContainer):
        class _Refaceting(PyMenu):
            """
            Singleton _Refaceting.
            """
            def __init__(self, service, rules, path):
                self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                self.MaxSize = self.__class__.MaxSize(service, rules, path + [("MaxSize", "")])
                self.Deviation = self.__class__.Deviation(service, rules, path + [("Deviation", "")])
                self.Name = self.__class__.Name(service, rules, path + [("Name", "")])
                self.NormalAngle = self.__class__.NormalAngle(service, rules, path + [("NormalAngle", "")])
                self.Applied = self.__class__.Applied(service, rules, path + [("Applied", "")])
                self.Children = self.__class__.Children(service, rules, path + [("Children", "")])
                self.Context = self.__class__.Context(service, rules, path + [("Context", "")])
                self.Apply = self.__class__.Apply(service, rules, "Apply", path)
                self.Edit = self.__class__.Edit(service, rules, "Edit", path)
                self.Rename = self.__class__.Rename(service, rules, "Rename", path)
                self.Delete = self.__class__.Delete(service, rules, "Delete", path)
                super().__init__(service, rules, path)

            class _name_(PyMenu):
                """
                Parameter _name_ of value type str.
                """
                pass

            class MaxSize(PyMenu):
                """
                Parameter MaxSize of value type float.
                """
                pass

            class Deviation(PyMenu):
                """
                Parameter Deviation of value type float.
                """
                pass

            class Name(PyMenu):
                """
                Parameter Name of value type str.
                """
                pass

            class NormalAngle(PyMenu):
                """
                Parameter NormalAngle of value type float.
                """
                pass

            class Applied(PyMenu):
                """
                Parameter Applied of value type bool.
                """
                pass

            class Children(PyMenu):
                """
                Parameter Children of value type List[str].
                """
                pass

            class Context(PyMenu):
                """
                Parameter Context of value type int.
                """
                pass

            class Apply(PyCommand):
                """
                Apply() -> bool
                """
                pass

            class Edit(PyCommand):
                """
                Edit() -> bool
                """
                pass

            class Rename(PyCommand):
                """
                Rename(NewName: str) -> bool
                """
                pass

            class Delete(PyCommand):
                """
                Delete() -> bool
                """
                pass

        def __getitem__(self, key: str) -> _Refaceting:
            return super().__getitem__(key)

    class MeshingOperations(PyMenu):
        """
        Singleton MeshingOperations.
        """
        def __init__(self, service, rules, path):
            self.Children = self.__class__.Children(service, rules, path + [("Children", "")])
            self.Name = self.__class__.Name(service, rules, path + [("Name", "")])
            self.UpdateAllOperations = self.__class__.UpdateAllOperations(service, rules, "UpdateAllOperations", path)
            self.DeleteAllOperations = self.__class__.DeleteAllOperations(service, rules, "DeleteAllOperations", path)
            super().__init__(service, rules, path)

        class Children(PyMenu):
            """
            Parameter Children of value type List[str].
            """
            pass

        class Name(PyMenu):
            """
            Parameter Name of value type str.
            """
            pass

        class UpdateAllOperations(PyCommand):
            """
            UpdateAllOperations() -> bool
            """
            pass

        class DeleteAllOperations(PyCommand):
            """
            DeleteAllOperations() -> bool
            """
            pass

    class ObjectSettingOperations(PyMenu):
        """
        Singleton ObjectSettingOperations.
        """
        def __init__(self, service, rules, path):
            self.Name = self.__class__.Name(service, rules, path + [("Name", "")])
            self.Children = self.__class__.Children(service, rules, path + [("Children", "")])
            self.CreateObjectSetting = self.__class__.CreateObjectSetting(service, rules, "CreateObjectSetting", path)
            self.DeleteAllObjectSetting = self.__class__.DeleteAllObjectSetting(service, rules, "DeleteAllObjectSetting", path)
            self.DeleteObjectSetting = self.__class__.DeleteObjectSetting(service, rules, "DeleteObjectSetting", path)
            super().__init__(service, rules, path)

        class Name(PyMenu):
            """
            Parameter Name of value type str.
            """
            pass

        class Children(PyMenu):
            """
            Parameter Children of value type List[str].
            """
            pass

        class CreateObjectSetting(PyCommand):
            """
            CreateObjectSetting(Paths: List[str]) -> bool
            """
            pass

        class DeleteAllObjectSetting(PyCommand):
            """
            DeleteAllObjectSetting() -> bool
            """
            pass

        class DeleteObjectSetting(PyCommand):
            """
            DeleteObjectSetting(Paths: List[str]) -> bool
            """
            pass

    class GlobalSettings(PyMenu):
        """
        Singleton GlobalSettings.
        """
        def __init__(self, service, rules, path):
            self.LengthUnit = self.__class__.LengthUnit(service, rules, path + [("LengthUnit", "")])
            self.CurrentNode = self.__class__.CurrentNode(service, rules, path + [("CurrentNode", "")])
            self.CurrentContext = self.__class__.CurrentContext(service, rules, path + [("CurrentContext", "")])
            super().__init__(service, rules, path)

        class LengthUnit(PyMenu):
            """
            Parameter LengthUnit of value type str.
            """
            pass

        class CurrentNode(PyMenu):
            """
            Parameter CurrentNode of value type str.
            """
            pass

        class CurrentContext(PyMenu):
            """
            Parameter CurrentContext of value type int.
            """
            pass

    class TransformOperations(PyMenu):
        """
        Singleton TransformOperations.
        """
        def __init__(self, service, rules, path):
            self.Name = self.__class__.Name(service, rules, path + [("Name", "")])
            self.Children = self.__class__.Children(service, rules, path + [("Children", "")])
            self.CreateTransform = self.__class__.CreateTransform(service, rules, "CreateTransform", path)
            self.DeleteTransform = self.__class__.DeleteTransform(service, rules, "DeleteTransform", path)
            self.DeleteAllTransforms = self.__class__.DeleteAllTransforms(service, rules, "DeleteAllTransforms", path)
            self.UpdateAllTransforms = self.__class__.UpdateAllTransforms(service, rules, "UpdateAllTransforms", path)
            super().__init__(service, rules, path)

        class Name(PyMenu):
            """
            Parameter Name of value type str.
            """
            pass

        class Children(PyMenu):
            """
            Parameter Children of value type List[str].
            """
            pass

        class CreateTransform(PyCommand):
            """
            CreateTransform(Paths: List[str]) -> bool
            """
            pass

        class DeleteTransform(PyCommand):
            """
            DeleteTransform(Paths: List[str]) -> bool
            """
            pass

        class DeleteAllTransforms(PyCommand):
            """
            DeleteAllTransforms() -> bool
            """
            pass

        class UpdateAllTransforms(PyCommand):
            """
            UpdateAllTransforms() -> bool
            """
            pass

    class RefacetingOperations(PyMenu):
        """
        Singleton RefacetingOperations.
        """
        def __init__(self, service, rules, path):
            self.Children = self.__class__.Children(service, rules, path + [("Children", "")])
            self.Name = self.__class__.Name(service, rules, path + [("Name", "")])
            self.UpdateAllRefacets = self.__class__.UpdateAllRefacets(service, rules, "UpdateAllRefacets", path)
            self.DeleteRefacet = self.__class__.DeleteRefacet(service, rules, "DeleteRefacet", path)
            self.CreateRefacet = self.__class__.CreateRefacet(service, rules, "CreateRefacet", path)
            self.DeleteAllRefacets = self.__class__.DeleteAllRefacets(service, rules, "DeleteAllRefacets", path)
            super().__init__(service, rules, path)

        class Children(PyMenu):
            """
            Parameter Children of value type List[str].
            """
            pass

        class Name(PyMenu):
            """
            Parameter Name of value type str.
            """
            pass

        class UpdateAllRefacets(PyCommand):
            """
            UpdateAllRefacets() -> bool
            """
            pass

        class DeleteRefacet(PyCommand):
            """
            DeleteRefacet(Paths: List[str]) -> bool
            """
            pass

        class CreateRefacet(PyCommand):
            """
            CreateRefacet(Paths: List[str]) -> bool
            """
            pass

        class DeleteAllRefacets(PyCommand):
            """
            DeleteAllRefacets() -> bool
            """
            pass

    class Delete(PyCommand):
        """
        Delete(Path: str) -> bool
        """
        pass

    class ResetTemplate(PyCommand):
        """
        ResetTemplate() -> bool
        """
        pass

    class LoadTemplate(PyCommand):
        """
        LoadTemplate(FilePath: str) -> bool
        """
        pass

    class MoveToObject(PyCommand):
        """
        MoveToObject(Paths: List[str]) -> bool
        """
        pass

    class ChangeFileLengthUnit(PyCommand):
        """
        ChangeFileLengthUnit(LengthUnit: str) -> bool
        """
        pass

    class MoveCADComponentsToNewObject(PyCommand):
        """
        MoveCADComponentsToNewObject(Paths: List[str]) -> bool
        """
        pass

    class SaveFmdFile(PyCommand):
        """
        SaveFmdFile(FilePath: str) -> bool
        """
        pass

    class InitializeTemplate(PyCommand):
        """
        InitializeTemplate(templateType: str) -> bool
        """
        pass

    class DeletePaths(PyCommand):
        """
        DeletePaths(Paths: List[str]) -> bool
        """
        pass

    class CreateObjects(PyCommand):
        """
        CreateObjects() -> bool
        """
        pass

    class UndoAllTransforms(PyCommand):
        """
        UndoAllTransforms() -> bool
        """
        pass

    class CreateObjForEachPart(PyCommand):
        """
        CreateObjForEachPart(Paths: List[str]) -> bool
        """
        pass

    class LoadFmdFile(PyCommand):
        """
        LoadFmdFile(FilePath: str, FileUnit: str, Route: str, JtLOD: str, PartPerBody: bool, IgnoreSolidNames: bool, Options: Dict[str, Any]) -> bool
        """
        pass

    class InputFileChanged(PyCommand):
        """
        InputFileChanged(FilePath: str, PartPerBody: bool, IgnoreSolidNames: bool) -> bool
        """
        pass

    class RedoAllTransforms(PyCommand):
        """
        RedoAllTransforms() -> bool
        """
        pass

    class ListMeshingOperations(PyCommand):
        """
        ListMeshingOperations(Path: str) -> bool
        """
        pass

    class SaveTemplate(PyCommand):
        """
        SaveTemplate(FilePath: str) -> bool
        """
        pass

    class AppendFmdFiles(PyCommand):
        """
        AppendFmdFiles(FilePath: List[str], AssemblyParentNode: int, FileUnit: str, Route: str, JtLOD: str, PartPerBody: bool, IgnoreSolidNamesAppend: bool, Options: Dict[str, Any]) -> bool
        """
        pass

    class ChangeLengthUnit(PyCommand):
        """
        ChangeLengthUnit(LengthUnit: str) -> bool
        """
        pass

