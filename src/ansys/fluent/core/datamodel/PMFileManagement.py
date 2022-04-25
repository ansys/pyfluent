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
        self.File = self.__class__.File(service, rules, path + [("File", "")])
        self.FileManager = self.__class__.FileManager(service, rules, path + [("FileManager", "")])
        super().__init__(service, rules, path)

    class File(PyNamedObjectContainer):
        class _File(PyMenu):
            """
            Singleton _File.
            """
            def __init__(self, service, rules, path):
                self.Options = self.__class__.Options(service, rules, path + [("Options", "")])
                self.IgnoreSolidNames = self.__class__.IgnoreSolidNames(service, rules, path + [("IgnoreSolidNames", "")])
                self.Keys = self.__class__.Keys(service, rules, path + [("Keys", "")])
                self.FileUnit = self.__class__.FileUnit(service, rules, path + [("FileUnit", "")])
                self.Path = self.__class__.Path(service, rules, path + [("Path", "")])
                self.JtLOD = self.__class__.JtLOD(service, rules, path + [("JtLOD", "")])
                self.Dummy = self.__class__.Dummy(service, rules, path + [("Dummy", "")])
                self.ConvertedPath = self.__class__.ConvertedPath(service, rules, path + [("ConvertedPath", "")])
                self.Route = self.__class__.Route(service, rules, path + [("Route", "")])
                self.Updated = self.__class__.Updated(service, rules, path + [("Updated", "")])
                self.PartPerBody = self.__class__.PartPerBody(service, rules, path + [("PartPerBody", "")])
                self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                self.Append = self.__class__.Append(service, rules, path + [("Append", "")])
                self.Name = self.__class__.Name(service, rules, path + [("Name", "")])
                super().__init__(service, rules, path)

            class Options(PyMenu):
                """
                Singleton Options.
                """
                def __init__(self, service, rules, path):
                    self.Solid = self.__class__.Solid(service, rules, path + [("Solid", "")])
                    self.Surface = self.__class__.Surface(service, rules, path + [("Surface", "")])
                    self.Line = self.__class__.Line(service, rules, path + [("Line", "")])
                    super().__init__(service, rules, path)

                class Solid(PyMenu):
                    """
                    Parameter Solid of value type bool.
                    """
                    pass

                class Surface(PyMenu):
                    """
                    Parameter Surface of value type bool.
                    """
                    pass

                class Line(PyMenu):
                    """
                    Parameter Line of value type bool.
                    """
                    pass

            class IgnoreSolidNames(PyMenu):
                """
                Parameter IgnoreSolidNames of value type bool.
                """
                pass

            class Keys(PyMenu):
                """
                Parameter Keys of value type List[int].
                """
                pass

            class FileUnit(PyMenu):
                """
                Parameter FileUnit of value type str.
                """
                pass

            class Path(PyMenu):
                """
                Parameter Path of value type str.
                """
                pass

            class JtLOD(PyMenu):
                """
                Parameter JtLOD of value type str.
                """
                pass

            class Dummy(PyMenu):
                """
                Parameter Dummy of value type bool.
                """
                pass

            class ConvertedPath(PyMenu):
                """
                Parameter ConvertedPath of value type str.
                """
                pass

            class Route(PyMenu):
                """
                Parameter Route of value type str.
                """
                pass

            class Updated(PyMenu):
                """
                Parameter Updated of value type bool.
                """
                pass

            class PartPerBody(PyMenu):
                """
                Parameter PartPerBody of value type bool.
                """
                pass

            class _name_(PyMenu):
                """
                Parameter _name_ of value type str.
                """
                pass

            class Append(PyMenu):
                """
                Parameter Append of value type bool.
                """
                pass

            class Name(PyMenu):
                """
                Parameter Name of value type str.
                """
                pass

        def __getitem__(self, key: str) -> _File:
            return super().__getitem__(key)

    class FileManager(PyMenu):
        """
        Singleton FileManager.
        """
        def __init__(self, service, rules, path):
            self.Children = self.__class__.Children(service, rules, path + [("Children", "")])
            self.Name = self.__class__.Name(service, rules, path + [("Name", "")])
            self.DeleteCadKey = self.__class__.DeleteCadKey(service, rules, "DeleteCadKey", path)
            self.Reload = self.__class__.Reload(service, rules, "Reload", path)
            self.Unload = self.__class__.Unload(service, rules, "Unload", path)
            self.LoadFiles = self.__class__.LoadFiles(service, rules, "LoadFiles", path)
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

        class DeleteCadKey(PyCommand):
            """
            DeleteCadKey(Key: int) -> bool
            """
            pass

        class Reload(PyCommand):
            """
            Reload(FileName: str) -> bool
            """
            pass

        class Unload(PyCommand):
            """
            Unload(FileName: str) -> bool
            """
            pass

        class LoadFiles(PyCommand):
            """
            LoadFiles() -> bool
            """
            pass

