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
        self.Case = self.__class__.Case(service, rules, path + [("Case", "")])
        super().__init__(service, rules, path)

    class Case(PyMenu):
        """
        Singleton Case.
        """
        def __init__(self, service, rules, path):
            self.AuxiliaryInfo = self.__class__.AuxiliaryInfo(service, rules, path + [("AuxiliaryInfo", "")])
            self.ResultsInfo = self.__class__.ResultsInfo(service, rules, path + [("ResultsInfo", "")])
            self.MeshInfo = self.__class__.MeshInfo(service, rules, path + [("MeshInfo", "")])
            self.CaseInfo = self.__class__.CaseInfo(service, rules, path + [("CaseInfo", "")])
            self.Solution = self.__class__.Solution(service, rules, path + [("Solution", "")])
            self.Setup = self.__class__.Setup(service, rules, path + [("Setup", "")])
            self.Streaming = self.__class__.Streaming(service, rules, path + [("Streaming", "")])
            self.App = self.__class__.App(service, rules, path + [("App", "")])
            self.Results = self.__class__.Results(service, rules, path + [("Results", "")])
            self.AppName = self.__class__.AppName(service, rules, path + [("AppName", "")])
            self.ReadData = self.__class__.ReadData(service, rules, "ReadData", path)
            self.ReadCaseAndData = self.__class__.ReadCaseAndData(service, rules, "ReadCaseAndData", path)
            self.ClearDatamodel = self.__class__.ClearDatamodel(service, rules, "ClearDatamodel", path)
            self.WriteCaseAndData = self.__class__.WriteCaseAndData(service, rules, "WriteCaseAndData", path)
            self.SendCommand = self.__class__.SendCommand(service, rules, "SendCommand", path)
            self.WriteCase = self.__class__.WriteCase(service, rules, "WriteCase", path)
            self.WriteData = self.__class__.WriteData(service, rules, "WriteData", path)
            self.ReadCase = self.__class__.ReadCase(service, rules, "ReadCase", path)
            super().__init__(service, rules, path)

        class AuxiliaryInfo(PyMenu):
            """
            Singleton AuxiliaryInfo.
            """
            def __init__(self, service, rules, path):
                self.IsSgPDFTransport = self.__class__.IsSgPDFTransport(service, rules, path + [("IsSgPDFTransport", "")])
                self.TimeStepSpecification = self.__class__.TimeStepSpecification(service, rules, path + [("TimeStepSpecification", "")])
                self.DefaultVectorField = self.__class__.DefaultVectorField(service, rules, path + [("DefaultVectorField", "")])
                self.MultiPhaseDomainList = self.__class__.MultiPhaseDomainList(service, rules, path + [("MultiPhaseDomainList", "")])
                self.IsCourantNumberActive = self.__class__.IsCourantNumberActive(service, rules, path + [("IsCourantNumberActive", "")])
                self.IsPVCouplingActive = self.__class__.IsPVCouplingActive(service, rules, path + [("IsPVCouplingActive", "")])
                self.DefaultField = self.__class__.DefaultField(service, rules, path + [("DefaultField", "")])
                self.IsDPMWallFilmBC = self.__class__.IsDPMWallFilmBC(service, rules, path + [("IsDPMWallFilmBC", "")])
                self.IsUnsteadyParticleTracking = self.__class__.IsUnsteadyParticleTracking(service, rules, path + [("IsUnsteadyParticleTracking", "")])
                self.IsOversetReadOnly = self.__class__.IsOversetReadOnly(service, rules, path + [("IsOversetReadOnly", "")])
                self.FluentBoundaryZones = self.__class__.FluentBoundaryZones(service, rules, path + [("FluentBoundaryZones", "")])
                self.MultiPhaseModel = self.__class__.MultiPhaseModel(service, rules, path + [("MultiPhaseModel", "")])
                super().__init__(service, rules, path)

            class IsSgPDFTransport(PyMenu):
                """
                Parameter IsSgPDFTransport of value type bool.
                """
                pass

            class TimeStepSpecification(PyMenu):
                """
                Parameter TimeStepSpecification of value type bool.
                """
                pass

            class DefaultVectorField(PyMenu):
                """
                Parameter DefaultVectorField of value type str.
                """
                pass

            class MultiPhaseDomainList(PyMenu):
                """
                Parameter MultiPhaseDomainList of value type List[str].
                """
                pass

            class IsCourantNumberActive(PyMenu):
                """
                Parameter IsCourantNumberActive of value type bool.
                """
                pass

            class IsPVCouplingActive(PyMenu):
                """
                Parameter IsPVCouplingActive of value type bool.
                """
                pass

            class DefaultField(PyMenu):
                """
                Parameter DefaultField of value type str.
                """
                pass

            class IsDPMWallFilmBC(PyMenu):
                """
                Parameter IsDPMWallFilmBC of value type bool.
                """
                pass

            class IsUnsteadyParticleTracking(PyMenu):
                """
                Parameter IsUnsteadyParticleTracking of value type bool.
                """
                pass

            class IsOversetReadOnly(PyMenu):
                """
                Parameter IsOversetReadOnly of value type bool.
                """
                pass

            class FluentBoundaryZones(PyMenu):
                """
                Parameter FluentBoundaryZones of value type List[str].
                """
                pass

            class MultiPhaseModel(PyMenu):
                """
                Parameter MultiPhaseModel of value type str.
                """
                pass

        class ResultsInfo(PyMenu):
            """
            Singleton ResultsInfo.
            """
            def __init__(self, service, rules, path):
                self.Fields = self.__class__.Fields(service, rules, path + [("Fields", "")])
                self.ParticleVariables = self.__class__.ParticleVariables(service, rules, path + [("ParticleVariables", "")])
                self.DPMParticleVectorFields = self.__class__.DPMParticleVectorFields(service, rules, path + [("DPMParticleVectorFields", "")])
                self.PathlinesFields = self.__class__.PathlinesFields(service, rules, path + [("PathlinesFields", "")])
                self.DPMInjections = self.__class__.DPMInjections(service, rules, path + [("DPMInjections", "")])
                self.VectorFields = self.__class__.VectorFields(service, rules, path + [("VectorFields", "")])
                self.ParticleTracksFields = self.__class__.ParticleTracksFields(service, rules, path + [("ParticleTracksFields", "")])
                super().__init__(service, rules, path)

            class Fields(PyNamedObjectContainer):
                class _Fields(PyMenu):
                    """
                    Singleton _Fields.
                    """
                    def __init__(self, service, rules, path):
                        self.UnitQuantity = self.__class__.UnitQuantity(service, rules, path + [("UnitQuantity", "")])
                        self.Domain = self.__class__.Domain(service, rules, path + [("Domain", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        self.DisplayName = self.__class__.DisplayName(service, rules, path + [("DisplayName", "")])
                        self.Rank = self.__class__.Rank(service, rules, path + [("Rank", "")])
                        self.SolverName = self.__class__.SolverName(service, rules, path + [("SolverName", "")])
                        self.Section = self.__class__.Section(service, rules, path + [("Section", "")])
                        super().__init__(service, rules, path)

                    class UnitQuantity(PyMenu):
                        """
                        Parameter UnitQuantity of value type str.
                        """
                        pass

                    class Domain(PyMenu):
                        """
                        Parameter Domain of value type str.
                        """
                        pass

                    class _name_(PyMenu):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                    class DisplayName(PyMenu):
                        """
                        Parameter DisplayName of value type str.
                        """
                        pass

                    class Rank(PyMenu):
                        """
                        Parameter Rank of value type int.
                        """
                        pass

                    class SolverName(PyMenu):
                        """
                        Parameter SolverName of value type str.
                        """
                        pass

                    class Section(PyMenu):
                        """
                        Parameter Section of value type str.
                        """
                        pass

                def __getitem__(self, key: str) -> _Fields:
                    return super().__getitem__(key)

            class ParticleVariables(PyNamedObjectContainer):
                class _ParticleVariables(PyMenu):
                    """
                    Singleton _ParticleVariables.
                    """
                    def __init__(self, service, rules, path):
                        self.Section = self.__class__.Section(service, rules, path + [("Section", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        self.Domain = self.__class__.Domain(service, rules, path + [("Domain", "")])
                        self.DisplayName = self.__class__.DisplayName(service, rules, path + [("DisplayName", "")])
                        self.SolverName = self.__class__.SolverName(service, rules, path + [("SolverName", "")])
                        super().__init__(service, rules, path)

                    class Section(PyMenu):
                        """
                        Parameter Section of value type str.
                        """
                        pass

                    class _name_(PyMenu):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                    class Domain(PyMenu):
                        """
                        Parameter Domain of value type str.
                        """
                        pass

                    class DisplayName(PyMenu):
                        """
                        Parameter DisplayName of value type str.
                        """
                        pass

                    class SolverName(PyMenu):
                        """
                        Parameter SolverName of value type str.
                        """
                        pass

                def __getitem__(self, key: str) -> _ParticleVariables:
                    return super().__getitem__(key)

            class DPMParticleVectorFields(PyNamedObjectContainer):
                class _DPMParticleVectorFields(PyMenu):
                    """
                    Singleton _DPMParticleVectorFields.
                    """
                    def __init__(self, service, rules, path):
                        self.SolverName = self.__class__.SolverName(service, rules, path + [("SolverName", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        self.DisplayName = self.__class__.DisplayName(service, rules, path + [("DisplayName", "")])
                        super().__init__(service, rules, path)

                    class SolverName(PyMenu):
                        """
                        Parameter SolverName of value type str.
                        """
                        pass

                    class _name_(PyMenu):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                    class DisplayName(PyMenu):
                        """
                        Parameter DisplayName of value type str.
                        """
                        pass

                def __getitem__(self, key: str) -> _DPMParticleVectorFields:
                    return super().__getitem__(key)

            class PathlinesFields(PyNamedObjectContainer):
                class _PathlinesFields(PyMenu):
                    """
                    Singleton _PathlinesFields.
                    """
                    def __init__(self, service, rules, path):
                        self.Section = self.__class__.Section(service, rules, path + [("Section", "")])
                        self.Domain = self.__class__.Domain(service, rules, path + [("Domain", "")])
                        self.DisplayName = self.__class__.DisplayName(service, rules, path + [("DisplayName", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        self.SolverName = self.__class__.SolverName(service, rules, path + [("SolverName", "")])
                        self.Rank = self.__class__.Rank(service, rules, path + [("Rank", "")])
                        super().__init__(service, rules, path)

                    class Section(PyMenu):
                        """
                        Parameter Section of value type str.
                        """
                        pass

                    class Domain(PyMenu):
                        """
                        Parameter Domain of value type str.
                        """
                        pass

                    class DisplayName(PyMenu):
                        """
                        Parameter DisplayName of value type str.
                        """
                        pass

                    class _name_(PyMenu):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                    class SolverName(PyMenu):
                        """
                        Parameter SolverName of value type str.
                        """
                        pass

                    class Rank(PyMenu):
                        """
                        Parameter Rank of value type int.
                        """
                        pass

                def __getitem__(self, key: str) -> _PathlinesFields:
                    return super().__getitem__(key)

            class DPMInjections(PyNamedObjectContainer):
                class _DPMInjections(PyMenu):
                    """
                    Singleton _DPMInjections.
                    """
                    def __init__(self, service, rules, path):
                        self.DisplayName = self.__class__.DisplayName(service, rules, path + [("DisplayName", "")])
                        self.SolverName = self.__class__.SolverName(service, rules, path + [("SolverName", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        super().__init__(service, rules, path)

                    class DisplayName(PyMenu):
                        """
                        Parameter DisplayName of value type str.
                        """
                        pass

                    class SolverName(PyMenu):
                        """
                        Parameter SolverName of value type str.
                        """
                        pass

                    class _name_(PyMenu):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                def __getitem__(self, key: str) -> _DPMInjections:
                    return super().__getitem__(key)

            class VectorFields(PyNamedObjectContainer):
                class _VectorFields(PyMenu):
                    """
                    Singleton _VectorFields.
                    """
                    def __init__(self, service, rules, path):
                        self.XComponent = self.__class__.XComponent(service, rules, path + [("XComponent", "")])
                        self.ZComponent = self.__class__.ZComponent(service, rules, path + [("ZComponent", "")])
                        self.IsCustomVector = self.__class__.IsCustomVector(service, rules, path + [("IsCustomVector", "")])
                        self.YComponent = self.__class__.YComponent(service, rules, path + [("YComponent", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        super().__init__(service, rules, path)

                    class XComponent(PyMenu):
                        """
                        Parameter XComponent of value type str.
                        """
                        pass

                    class ZComponent(PyMenu):
                        """
                        Parameter ZComponent of value type str.
                        """
                        pass

                    class IsCustomVector(PyMenu):
                        """
                        Parameter IsCustomVector of value type bool.
                        """
                        pass

                    class YComponent(PyMenu):
                        """
                        Parameter YComponent of value type str.
                        """
                        pass

                    class _name_(PyMenu):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                def __getitem__(self, key: str) -> _VectorFields:
                    return super().__getitem__(key)

            class ParticleTracksFields(PyNamedObjectContainer):
                class _ParticleTracksFields(PyMenu):
                    """
                    Singleton _ParticleTracksFields.
                    """
                    def __init__(self, service, rules, path):
                        self.Section = self.__class__.Section(service, rules, path + [("Section", "")])
                        self.Domain = self.__class__.Domain(service, rules, path + [("Domain", "")])
                        self.DisplayName = self.__class__.DisplayName(service, rules, path + [("DisplayName", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        self.SolverName = self.__class__.SolverName(service, rules, path + [("SolverName", "")])
                        super().__init__(service, rules, path)

                    class Section(PyMenu):
                        """
                        Parameter Section of value type str.
                        """
                        pass

                    class Domain(PyMenu):
                        """
                        Parameter Domain of value type str.
                        """
                        pass

                    class DisplayName(PyMenu):
                        """
                        Parameter DisplayName of value type str.
                        """
                        pass

                    class _name_(PyMenu):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                    class SolverName(PyMenu):
                        """
                        Parameter SolverName of value type str.
                        """
                        pass

                def __getitem__(self, key: str) -> _ParticleTracksFields:
                    return super().__getitem__(key)

        class MeshInfo(PyMenu):
            """
            Singleton MeshInfo.
            """
            def __init__(self, service, rules, path):
                self.MeshExtents = self.__class__.MeshExtents(service, rules, path + [("MeshExtents", "")])
                super().__init__(service, rules, path)

            class MeshExtents(PyMenu):
                """
                Singleton MeshExtents.
                """
                def __init__(self, service, rules, path):
                    self.YMax = self.__class__.YMax(service, rules, path + [("YMax", "")])
                    self.ZMax = self.__class__.ZMax(service, rules, path + [("ZMax", "")])
                    self.ZMin = self.__class__.ZMin(service, rules, path + [("ZMin", "")])
                    self.YMin = self.__class__.YMin(service, rules, path + [("YMin", "")])
                    self.XMax = self.__class__.XMax(service, rules, path + [("XMax", "")])
                    self.XMin = self.__class__.XMin(service, rules, path + [("XMin", "")])
                    super().__init__(service, rules, path)

                class YMax(PyMenu):
                    """
                    Parameter YMax of value type float.
                    """
                    pass

                class ZMax(PyMenu):
                    """
                    Parameter ZMax of value type float.
                    """
                    pass

                class ZMin(PyMenu):
                    """
                    Parameter ZMin of value type float.
                    """
                    pass

                class YMin(PyMenu):
                    """
                    Parameter YMin of value type float.
                    """
                    pass

                class XMax(PyMenu):
                    """
                    Parameter XMax of value type float.
                    """
                    pass

                class XMin(PyMenu):
                    """
                    Parameter XMin of value type float.
                    """
                    pass

        class CaseInfo(PyMenu):
            """
            Singleton CaseInfo.
            """
            def __init__(self, service, rules, path):
                self.CaseFileName = self.__class__.CaseFileName(service, rules, path + [("CaseFileName", "")])
                self.IsEduOnlyLogo = self.__class__.IsEduOnlyLogo(service, rules, path + [("IsEduOnlyLogo", "")])
                self.IsStudentOnly = self.__class__.IsStudentOnly(service, rules, path + [("IsStudentOnly", "")])
                self.Dimension = self.__class__.Dimension(service, rules, path + [("Dimension", "")])
                self.SolverName = self.__class__.SolverName(service, rules, path + [("SolverName", "")])
                self.Configuration = self.__class__.Configuration(service, rules, path + [("Configuration", "")])
                self.CaseFileNameDirStripped = self.__class__.CaseFileNameDirStripped(service, rules, path + [("CaseFileNameDirStripped", "")])
                self.HostName = self.__class__.HostName(service, rules, path + [("HostName", "")])
                super().__init__(service, rules, path)

            class CaseFileName(PyMenu):
                """
                Parameter CaseFileName of value type str.
                """
                pass

            class IsEduOnlyLogo(PyMenu):
                """
                Parameter IsEduOnlyLogo of value type bool.
                """
                pass

            class IsStudentOnly(PyMenu):
                """
                Parameter IsStudentOnly of value type bool.
                """
                pass

            class Dimension(PyMenu):
                """
                Parameter Dimension of value type str.
                """
                pass

            class SolverName(PyMenu):
                """
                Parameter SolverName of value type str.
                """
                pass

            class Configuration(PyMenu):
                """
                Parameter Configuration of value type str.
                """
                pass

            class CaseFileNameDirStripped(PyMenu):
                """
                Parameter CaseFileNameDirStripped of value type str.
                """
                pass

            class HostName(PyMenu):
                """
                Parameter HostName of value type str.
                """
                pass

        class Solution(PyMenu):
            """
            Singleton Solution.
            """
            def __init__(self, service, rules, path):
                self.CalculationActivities = self.__class__.CalculationActivities(service, rules, path + [("CalculationActivities", "")])
                self.Controls = self.__class__.Controls(service, rules, path + [("Controls", "")])
                self.Methods = self.__class__.Methods(service, rules, path + [("Methods", "")])
                self.Monitors = self.__class__.Monitors(service, rules, path + [("Monitors", "")])
                self.State = self.__class__.State(service, rules, path + [("State", "")])
                self.Calculation = self.__class__.Calculation(service, rules, path + [("Calculation", "")])
                super().__init__(service, rules, path)

            class CalculationActivities(PyMenu):
                """
                Singleton CalculationActivities.
                """
                def __init__(self, service, rules, path):
                    self.SolutionAnimations = self.__class__.SolutionAnimations(service, rules, path + [("SolutionAnimations", "")])
                    super().__init__(service, rules, path)

                class SolutionAnimations(PyNamedObjectContainer):
                    class _SolutionAnimations(PyMenu):
                        """
                        Singleton _SolutionAnimations.
                        """
                        def __init__(self, service, rules, path):
                            self.Graphics = self.__class__.Graphics(service, rules, path + [("Graphics", "")])
                            self.IntegerIndex = self.__class__.IntegerIndex(service, rules, path + [("IntegerIndex", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.WindowId = self.__class__.WindowId(service, rules, path + [("WindowId", "")])
                            self.Projection = self.__class__.Projection(service, rules, path + [("Projection", "")])
                            self.RecordAfter = self.__class__.RecordAfter(service, rules, path + [("RecordAfter", "")])
                            self.Sequence = self.__class__.Sequence(service, rules, path + [("Sequence", "")])
                            self.StorageType = self.__class__.StorageType(service, rules, path + [("StorageType", "")])
                            self.View = self.__class__.View(service, rules, path + [("View", "")])
                            self.StorageDirectory = self.__class__.StorageDirectory(service, rules, path + [("StorageDirectory", "")])
                            self.RealIndex = self.__class__.RealIndex(service, rules, path + [("RealIndex", "")])
                            self.PlayBack = self.__class__.PlayBack(service, rules, "PlayBack", path)
                            self.Display = self.__class__.Display(service, rules, "Display", path)
                            self.Apply = self.__class__.Apply(service, rules, "Apply", path)
                            self.Delete = self.__class__.Delete(service, rules, "Delete", path)
                            super().__init__(service, rules, path)

                        class Graphics(PyMenu):
                            """
                            Parameter Graphics of value type str.
                            """
                            pass

                        class IntegerIndex(PyMenu):
                            """
                            Parameter IntegerIndex of value type int.
                            """
                            pass

                        class _name_(PyMenu):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                        class WindowId(PyMenu):
                            """
                            Parameter WindowId of value type int.
                            """
                            pass

                        class Projection(PyMenu):
                            """
                            Parameter Projection of value type str.
                            """
                            pass

                        class RecordAfter(PyMenu):
                            """
                            Parameter RecordAfter of value type str.
                            """
                            pass

                        class Sequence(PyMenu):
                            """
                            Parameter Sequence of value type int.
                            """
                            pass

                        class StorageType(PyMenu):
                            """
                            Parameter StorageType of value type str.
                            """
                            pass

                        class View(PyMenu):
                            """
                            Parameter View of value type str.
                            """
                            pass

                        class StorageDirectory(PyMenu):
                            """
                            Parameter StorageDirectory of value type str.
                            """
                            pass

                        class RealIndex(PyMenu):
                            """
                            Parameter RealIndex of value type float.
                            """
                            pass

                        class PlayBack(PyCommand):
                            """
                            PlayBack() -> bool
                            """
                            pass

                        class Display(PyCommand):
                            """
                            Display() -> bool
                            """
                            pass

                        class Apply(PyCommand):
                            """
                            Apply() -> bool
                            """
                            pass

                        class Delete(PyCommand):
                            """
                            Delete() -> bool
                            """
                            pass

                    def __getitem__(self, key: str) -> _SolutionAnimations:
                        return super().__getitem__(key)

            class Controls(PyMenu):
                """
                Singleton Controls.
                """
                def __init__(self, service, rules, path):
                    self.UnderRelaxationFactors = self.__class__.UnderRelaxationFactors(service, rules, path + [("UnderRelaxationFactors", "")])
                    self.CourantNumber = self.__class__.CourantNumber(service, rules, path + [("CourantNumber", "")])
                    super().__init__(service, rules, path)

                class UnderRelaxationFactors(PyNamedObjectContainer):
                    class _UnderRelaxationFactors(PyMenu):
                        """
                        Singleton _UnderRelaxationFactors.
                        """
                        def __init__(self, service, rules, path):
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.DomainId = self.__class__.DomainId(service, rules, path + [("DomainId", "")])
                            self.Value = self.__class__.Value(service, rules, path + [("Value", "")])
                            self.InternalName = self.__class__.InternalName(service, rules, path + [("InternalName", "")])
                            super().__init__(service, rules, path)

                        class _name_(PyMenu):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                        class DomainId(PyMenu):
                            """
                            Parameter DomainId of value type int.
                            """
                            pass

                        class Value(PyMenu):
                            """
                            Parameter Value of value type float.
                            """
                            pass

                        class InternalName(PyMenu):
                            """
                            Parameter InternalName of value type str.
                            """
                            pass

                    def __getitem__(self, key: str) -> _UnderRelaxationFactors:
                        return super().__getitem__(key)

                class CourantNumber(PyMenu):
                    """
                    Parameter CourantNumber of value type float.
                    """
                    pass

            class Methods(PyMenu):
                """
                Singleton Methods.
                """
                def __init__(self, service, rules, path):
                    self.DiscretizationSchemes = self.__class__.DiscretizationSchemes(service, rules, path + [("DiscretizationSchemes", "")])
                    self.PVCouplingScheme = self.__class__.PVCouplingScheme(service, rules, path + [("PVCouplingScheme", "")])
                    self.PVCouplingSchemeAllowedValues = self.__class__.PVCouplingSchemeAllowedValues(service, rules, path + [("PVCouplingSchemeAllowedValues", "")])
                    super().__init__(service, rules, path)

                class DiscretizationSchemes(PyNamedObjectContainer):
                    class _DiscretizationSchemes(PyMenu):
                        """
                        Singleton _DiscretizationSchemes.
                        """
                        def __init__(self, service, rules, path):
                            self.DomainId = self.__class__.DomainId(service, rules, path + [("DomainId", "")])
                            self.InternalName = self.__class__.InternalName(service, rules, path + [("InternalName", "")])
                            self.Value = self.__class__.Value(service, rules, path + [("Value", "")])
                            self.AllowedValues = self.__class__.AllowedValues(service, rules, path + [("AllowedValues", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            super().__init__(service, rules, path)

                        class DomainId(PyMenu):
                            """
                            Parameter DomainId of value type int.
                            """
                            pass

                        class InternalName(PyMenu):
                            """
                            Parameter InternalName of value type str.
                            """
                            pass

                        class Value(PyMenu):
                            """
                            Parameter Value of value type str.
                            """
                            pass

                        class AllowedValues(PyMenu):
                            """
                            Parameter AllowedValues of value type List[str].
                            """
                            pass

                        class _name_(PyMenu):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                    def __getitem__(self, key: str) -> _DiscretizationSchemes:
                        return super().__getitem__(key)

                class PVCouplingScheme(PyMenu):
                    """
                    Parameter PVCouplingScheme of value type str.
                    """
                    pass

                class PVCouplingSchemeAllowedValues(PyMenu):
                    """
                    Parameter PVCouplingSchemeAllowedValues of value type List[str].
                    """
                    pass

            class Monitors(PyMenu):
                """
                Singleton Monitors.
                """
                def __init__(self, service, rules, path):
                    self.ReportPlots = self.__class__.ReportPlots(service, rules, path + [("ReportPlots", "")])
                    self.Residuals = self.__class__.Residuals(service, rules, path + [("Residuals", "")])
                    super().__init__(service, rules, path)

                class ReportPlots(PyNamedObjectContainer):
                    class _ReportPlots(PyMenu):
                        """
                        Singleton _ReportPlots.
                        """
                        def __init__(self, service, rules, path):
                            self.Name = self.__class__.Name(service, rules, path + [("Name", "")])
                            self.Frequency = self.__class__.Frequency(service, rules, path + [("Frequency", "")])
                            self.Title = self.__class__.Title(service, rules, path + [("Title", "")])
                            self.XLabel = self.__class__.XLabel(service, rules, path + [("XLabel", "")])
                            self.FrequencyOf = self.__class__.FrequencyOf(service, rules, path + [("FrequencyOf", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.Active = self.__class__.Active(service, rules, path + [("Active", "")])
                            self.UnitInfo = self.__class__.UnitInfo(service, rules, path + [("UnitInfo", "")])
                            self.YLabel = self.__class__.YLabel(service, rules, path + [("YLabel", "")])
                            self.ReportDefinitions = self.__class__.ReportDefinitions(service, rules, path + [("ReportDefinitions", "")])
                            self.Print = self.__class__.Print(service, rules, path + [("Print", "")])
                            self.IsValid = self.__class__.IsValid(service, rules, path + [("IsValid", "")])
                            super().__init__(service, rules, path)

                        class Name(PyMenu):
                            """
                            Parameter Name of value type str.
                            """
                            pass

                        class Frequency(PyMenu):
                            """
                            Parameter Frequency of value type int.
                            """
                            pass

                        class Title(PyMenu):
                            """
                            Parameter Title of value type str.
                            """
                            pass

                        class XLabel(PyMenu):
                            """
                            Parameter XLabel of value type str.
                            """
                            pass

                        class FrequencyOf(PyMenu):
                            """
                            Parameter FrequencyOf of value type str.
                            """
                            pass

                        class _name_(PyMenu):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                        class Active(PyMenu):
                            """
                            Parameter Active of value type bool.
                            """
                            pass

                        class UnitInfo(PyMenu):
                            """
                            Parameter UnitInfo of value type str.
                            """
                            pass

                        class YLabel(PyMenu):
                            """
                            Parameter YLabel of value type str.
                            """
                            pass

                        class ReportDefinitions(PyMenu):
                            """
                            Parameter ReportDefinitions of value type List[str].
                            """
                            pass

                        class Print(PyMenu):
                            """
                            Parameter Print of value type bool.
                            """
                            pass

                        class IsValid(PyMenu):
                            """
                            Parameter IsValid of value type bool.
                            """
                            pass

                    def __getitem__(self, key: str) -> _ReportPlots:
                        return super().__getitem__(key)

                class Residuals(PyMenu):
                    """
                    Singleton Residuals.
                    """
                    def __init__(self, service, rules, path):
                        self.Equation = self.__class__.Equation(service, rules, path + [("Equation", "")])
                        self.ConvergenceCriterionType = self.__class__.ConvergenceCriterionType(service, rules, path + [("ConvergenceCriterionType", "")])
                        super().__init__(service, rules, path)

                    class Equation(PyNamedObjectContainer):
                        class _Equation(PyMenu):
                            """
                            Singleton _Equation.
                            """
                            def __init__(self, service, rules, path):
                                self.CheckConvergence = self.__class__.CheckConvergence(service, rules, path + [("CheckConvergence", "")])
                                self.RelativeCriterion = self.__class__.RelativeCriterion(service, rules, path + [("RelativeCriterion", "")])
                                self.AbsoluteCriterion = self.__class__.AbsoluteCriterion(service, rules, path + [("AbsoluteCriterion", "")])
                                self.IsMonitored = self.__class__.IsMonitored(service, rules, path + [("IsMonitored", "")])
                                self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                                super().__init__(service, rules, path)

                            class CheckConvergence(PyMenu):
                                """
                                Parameter CheckConvergence of value type bool.
                                """
                                pass

                            class RelativeCriterion(PyMenu):
                                """
                                Parameter RelativeCriterion of value type float.
                                """
                                pass

                            class AbsoluteCriterion(PyMenu):
                                """
                                Parameter AbsoluteCriterion of value type float.
                                """
                                pass

                            class IsMonitored(PyMenu):
                                """
                                Parameter IsMonitored of value type bool.
                                """
                                pass

                            class _name_(PyMenu):
                                """
                                Parameter _name_ of value type str.
                                """
                                pass

                        def __getitem__(self, key: str) -> _Equation:
                            return super().__getitem__(key)

                    class ConvergenceCriterionType(PyMenu):
                        """
                        Parameter ConvergenceCriterionType of value type str.
                        """
                        pass

            class State(PyMenu):
                """
                Singleton State.
                """
                def __init__(self, service, rules, path):
                    self.AeroOn = self.__class__.AeroOn(service, rules, path + [("AeroOn", "")])
                    self.CaseValid = self.__class__.CaseValid(service, rules, path + [("CaseValid", "")])
                    self.CaseFileName = self.__class__.CaseFileName(service, rules, path + [("CaseFileName", "")])
                    self.DataValid = self.__class__.DataValid(service, rules, path + [("DataValid", "")])
                    self.CaseId = self.__class__.CaseId(service, rules, path + [("CaseId", "")])
                    self.GridId = self.__class__.GridId(service, rules, path + [("GridId", "")])
                    self.DataId = self.__class__.DataId(service, rules, path + [("DataId", "")])
                    self.IcingOn = self.__class__.IcingOn(service, rules, path + [("IcingOn", "")])
                    super().__init__(service, rules, path)

                class AeroOn(PyMenu):
                    """
                    Parameter AeroOn of value type bool.
                    """
                    pass

                class CaseValid(PyMenu):
                    """
                    Parameter CaseValid of value type bool.
                    """
                    pass

                class CaseFileName(PyMenu):
                    """
                    Parameter CaseFileName of value type str.
                    """
                    pass

                class DataValid(PyMenu):
                    """
                    Parameter DataValid of value type bool.
                    """
                    pass

                class CaseId(PyMenu):
                    """
                    Parameter CaseId of value type int.
                    """
                    pass

                class GridId(PyMenu):
                    """
                    Parameter GridId of value type int.
                    """
                    pass

                class DataId(PyMenu):
                    """
                    Parameter DataId of value type int.
                    """
                    pass

                class IcingOn(PyMenu):
                    """
                    Parameter IcingOn of value type bool.
                    """
                    pass

            class Calculation(PyMenu):
                """
                Singleton Calculation.
                """
                def __init__(self, service, rules, path):
                    self.TimeStepSize = self.__class__.TimeStepSize(service, rules, path + [("TimeStepSize", "")])
                    self.NumberOfTimeSteps = self.__class__.NumberOfTimeSteps(service, rules, path + [("NumberOfTimeSteps", "")])
                    self.NumberOfIterations = self.__class__.NumberOfIterations(service, rules, path + [("NumberOfIterations", "")])
                    self.MaxIterationsPerTimeStep = self.__class__.MaxIterationsPerTimeStep(service, rules, path + [("MaxIterationsPerTimeStep", "")])
                    self.AnalysisType = self.__class__.AnalysisType(service, rules, path + [("AnalysisType", "")])
                    self.Calculate = self.__class__.Calculate(service, rules, "Calculate", path)
                    self.Pause = self.__class__.Pause(service, rules, "Pause", path)
                    self.Resume = self.__class__.Resume(service, rules, "Resume", path)
                    self.Interrupt = self.__class__.Interrupt(service, rules, "Interrupt", path)
                    self.Initialize = self.__class__.Initialize(service, rules, "Initialize", path)
                    super().__init__(service, rules, path)

                class TimeStepSize(PyMenu):
                    """
                    Parameter TimeStepSize of value type float.
                    """
                    pass

                class NumberOfTimeSteps(PyMenu):
                    """
                    Parameter NumberOfTimeSteps of value type int.
                    """
                    pass

                class NumberOfIterations(PyMenu):
                    """
                    Parameter NumberOfIterations of value type int.
                    """
                    pass

                class MaxIterationsPerTimeStep(PyMenu):
                    """
                    Parameter MaxIterationsPerTimeStep of value type int.
                    """
                    pass

                class AnalysisType(PyMenu):
                    """
                    Parameter AnalysisType of value type str.
                    """
                    pass

                class Calculate(PyCommand):
                    """
                    Calculate() -> bool
                    """
                    pass

                class Pause(PyCommand):
                    """
                    Pause() -> bool
                    """
                    pass

                class Resume(PyCommand):
                    """
                    Resume() -> bool
                    """
                    pass

                class Interrupt(PyCommand):
                    """
                    Interrupt() -> bool
                    """
                    pass

                class Initialize(PyCommand):
                    """
                    Initialize() -> bool
                    """
                    pass

        class Setup(PyMenu):
            """
            Singleton Setup.
            """
            def __init__(self, service, rules, path):
                self.Material = self.__class__.Material(service, rules, path + [("Material", "")])
                self.CellZone = self.__class__.CellZone(service, rules, path + [("CellZone", "")])
                self.Boundary = self.__class__.Boundary(service, rules, path + [("Boundary", "")])
                self.Beta = self.__class__.Beta(service, rules, path + [("Beta", "")])
                super().__init__(service, rules, path)

            class Material(PyNamedObjectContainer):
                class _Material(PyMenu):
                    """
                    Singleton _Material.
                    """
                    def __init__(self, service, rules, path):
                        self.Density = self.__class__.Density(service, rules, path + [("Density", "")])
                        self.CpSpecificHeat = self.__class__.CpSpecificHeat(service, rules, path + [("CpSpecificHeat", "")])
                        self.MolecularWeight = self.__class__.MolecularWeight(service, rules, path + [("MolecularWeight", "")])
                        self.ThermalExpansionCoefficient = self.__class__.ThermalExpansionCoefficient(service, rules, path + [("ThermalExpansionCoefficient", "")])
                        self.ThermalConductivity = self.__class__.ThermalConductivity(service, rules, path + [("ThermalConductivity", "")])
                        self.Viscosity = self.__class__.Viscosity(service, rules, path + [("Viscosity", "")])
                        self.FluentName = self.__class__.FluentName(service, rules, path + [("FluentName", "")])
                        self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        self.LoadFromDatabase = self.__class__.LoadFromDatabase(service, rules, "LoadFromDatabase", path)
                        super().__init__(service, rules, path)

                    class Density(PyMenu):
                        """
                        Singleton Density.
                        """
                        def __init__(self, service, rules, path):
                            self.Value = self.__class__.Value(service, rules, path + [("Value", "")])
                            self.Method = self.__class__.Method(service, rules, path + [("Method", "")])
                            super().__init__(service, rules, path)

                        class Value(PyMenu):
                            """
                            Parameter Value of value type float.
                            """
                            pass

                        class Method(PyMenu):
                            """
                            Parameter Method of value type str.
                            """
                            pass

                    class CpSpecificHeat(PyMenu):
                        """
                        Singleton CpSpecificHeat.
                        """
                        def __init__(self, service, rules, path):
                            self.Method = self.__class__.Method(service, rules, path + [("Method", "")])
                            self.Value = self.__class__.Value(service, rules, path + [("Value", "")])
                            super().__init__(service, rules, path)

                        class Method(PyMenu):
                            """
                            Parameter Method of value type str.
                            """
                            pass

                        class Value(PyMenu):
                            """
                            Parameter Value of value type float.
                            """
                            pass

                    class MolecularWeight(PyMenu):
                        """
                        Singleton MolecularWeight.
                        """
                        def __init__(self, service, rules, path):
                            self.Value = self.__class__.Value(service, rules, path + [("Value", "")])
                            self.Method = self.__class__.Method(service, rules, path + [("Method", "")])
                            super().__init__(service, rules, path)

                        class Value(PyMenu):
                            """
                            Parameter Value of value type float.
                            """
                            pass

                        class Method(PyMenu):
                            """
                            Parameter Method of value type str.
                            """
                            pass

                    class ThermalExpansionCoefficient(PyMenu):
                        """
                        Singleton ThermalExpansionCoefficient.
                        """
                        def __init__(self, service, rules, path):
                            self.Value = self.__class__.Value(service, rules, path + [("Value", "")])
                            self.Method = self.__class__.Method(service, rules, path + [("Method", "")])
                            super().__init__(service, rules, path)

                        class Value(PyMenu):
                            """
                            Parameter Value of value type float.
                            """
                            pass

                        class Method(PyMenu):
                            """
                            Parameter Method of value type str.
                            """
                            pass

                    class ThermalConductivity(PyMenu):
                        """
                        Singleton ThermalConductivity.
                        """
                        def __init__(self, service, rules, path):
                            self.Value = self.__class__.Value(service, rules, path + [("Value", "")])
                            self.Method = self.__class__.Method(service, rules, path + [("Method", "")])
                            super().__init__(service, rules, path)

                        class Value(PyMenu):
                            """
                            Parameter Value of value type float.
                            """
                            pass

                        class Method(PyMenu):
                            """
                            Parameter Method of value type str.
                            """
                            pass

                    class Viscosity(PyMenu):
                        """
                        Singleton Viscosity.
                        """
                        def __init__(self, service, rules, path):
                            self.Method = self.__class__.Method(service, rules, path + [("Method", "")])
                            self.Value = self.__class__.Value(service, rules, path + [("Value", "")])
                            super().__init__(service, rules, path)

                        class Method(PyMenu):
                            """
                            Parameter Method of value type str.
                            """
                            pass

                        class Value(PyMenu):
                            """
                            Parameter Value of value type float.
                            """
                            pass

                    class FluentName(PyMenu):
                        """
                        Parameter FluentName of value type str.
                        """
                        pass

                    class Type(PyMenu):
                        """
                        Parameter Type of value type str.
                        """
                        pass

                    class _name_(PyMenu):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                    class LoadFromDatabase(PyCommand):
                        """
                        LoadFromDatabase(MaterialName: str) -> None
                        """
                        pass

                def __getitem__(self, key: str) -> _Material:
                    return super().__getitem__(key)

            class CellZone(PyNamedObjectContainer):
                class _CellZone(PyMenu):
                    """
                    Singleton _CellZone.
                    """
                    def __init__(self, service, rules, path):
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        self.CellZoneId = self.__class__.CellZoneId(service, rules, path + [("CellZoneId", "")])
                        self.Material = self.__class__.Material(service, rules, path + [("Material", "")])
                        super().__init__(service, rules, path)

                    class _name_(PyMenu):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                    class CellZoneId(PyMenu):
                        """
                        Parameter CellZoneId of value type int.
                        """
                        pass

                    class Material(PyMenu):
                        """
                        Parameter Material of value type str.
                        """
                        pass

                def __getitem__(self, key: str) -> _CellZone:
                    return super().__getitem__(key)

            class Boundary(PyNamedObjectContainer):
                class _Boundary(PyMenu):
                    """
                    Singleton _Boundary.
                    """
                    def __init__(self, service, rules, path):
                        self.Flow = self.__class__.Flow(service, rules, path + [("Flow", "")])
                        self.Thermal = self.__class__.Thermal(service, rules, path + [("Thermal", "")])
                        self.Turbulence = self.__class__.Turbulence(service, rules, path + [("Turbulence", "")])
                        self.BoundaryType = self.__class__.BoundaryType(service, rules, path + [("BoundaryType", "")])
                        self.BoundaryId = self.__class__.BoundaryId(service, rules, path + [("BoundaryId", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        super().__init__(service, rules, path)

                    class Flow(PyMenu):
                        """
                        Singleton Flow.
                        """
                        def __init__(self, service, rules, path):
                            self.TranslationalVelocityComponents = self.__class__.TranslationalVelocityComponents(service, rules, path + [("TranslationalVelocityComponents", "")])
                            self.FlowDirection = self.__class__.FlowDirection(service, rules, path + [("FlowDirection", "")])
                            self.RotationAxisOrigin = self.__class__.RotationAxisOrigin(service, rules, path + [("RotationAxisOrigin", "")])
                            self.VelocityCartesianComponents = self.__class__.VelocityCartesianComponents(service, rules, path + [("VelocityCartesianComponents", "")])
                            self.RotationAxisDirection = self.__class__.RotationAxisDirection(service, rules, path + [("RotationAxisDirection", "")])
                            self.Direction = self.__class__.Direction(service, rules, path + [("Direction", "")])
                            self.TranslationalDirection = self.__class__.TranslationalDirection(service, rules, path + [("TranslationalDirection", "")])
                            self.MassFlux = self.__class__.MassFlux(service, rules, path + [("MassFlux", "")])
                            self.MassFlowRate = self.__class__.MassFlowRate(service, rules, path + [("MassFlowRate", "")])
                            self.IsRotating = self.__class__.IsRotating(service, rules, path + [("IsRotating", "")])
                            self.VelocitySpecification = self.__class__.VelocitySpecification(service, rules, path + [("VelocitySpecification", "")])
                            self.DirectionSpecificationMethod = self.__class__.DirectionSpecificationMethod(service, rules, path + [("DirectionSpecificationMethod", "")])
                            self.TranslationalVelocityMagnitude = self.__class__.TranslationalVelocityMagnitude(service, rules, path + [("TranslationalVelocityMagnitude", "")])
                            self.TranslationalVelocitySpecification = self.__class__.TranslationalVelocitySpecification(service, rules, path + [("TranslationalVelocitySpecification", "")])
                            self.GaugeTotalPressure = self.__class__.GaugeTotalPressure(service, rules, path + [("GaugeTotalPressure", "")])
                            self.VelocityMagnitude = self.__class__.VelocityMagnitude(service, rules, path + [("VelocityMagnitude", "")])
                            self.WallVelocitySpecification = self.__class__.WallVelocitySpecification(service, rules, path + [("WallVelocitySpecification", "")])
                            self.SupersonicOrInitialGaugePressure = self.__class__.SupersonicOrInitialGaugePressure(service, rules, path + [("SupersonicOrInitialGaugePressure", "")])
                            self.IsMotionBC = self.__class__.IsMotionBC(service, rules, path + [("IsMotionBC", "")])
                            self.GaugePressure = self.__class__.GaugePressure(service, rules, path + [("GaugePressure", "")])
                            self.AverageMassFlux = self.__class__.AverageMassFlux(service, rules, path + [("AverageMassFlux", "")])
                            self.MassFlowSpecificationMethod = self.__class__.MassFlowSpecificationMethod(service, rules, path + [("MassFlowSpecificationMethod", "")])
                            self.MachNumber = self.__class__.MachNumber(service, rules, path + [("MachNumber", "")])
                            self.RotationalSpeed = self.__class__.RotationalSpeed(service, rules, path + [("RotationalSpeed", "")])
                            super().__init__(service, rules, path)

                        class TranslationalVelocityComponents(PyMenu):
                            """
                            Singleton TranslationalVelocityComponents.
                            """
                            def __init__(self, service, rules, path):
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                super().__init__(service, rules, path)

                            class Y(PyMenu):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class Z(PyMenu):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                            class X(PyMenu):
                                """
                                Parameter X of value type float.
                                """
                                pass

                        class FlowDirection(PyMenu):
                            """
                            Singleton FlowDirection.
                            """
                            def __init__(self, service, rules, path):
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                super().__init__(service, rules, path)

                            class X(PyMenu):
                                """
                                Parameter X of value type float.
                                """
                                pass

                            class Z(PyMenu):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                            class Y(PyMenu):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                        class RotationAxisOrigin(PyMenu):
                            """
                            Singleton RotationAxisOrigin.
                            """
                            def __init__(self, service, rules, path):
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                super().__init__(service, rules, path)

                            class Y(PyMenu):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class Z(PyMenu):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                            class X(PyMenu):
                                """
                                Parameter X of value type float.
                                """
                                pass

                        class VelocityCartesianComponents(PyMenu):
                            """
                            Singleton VelocityCartesianComponents.
                            """
                            def __init__(self, service, rules, path):
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                super().__init__(service, rules, path)

                            class Y(PyMenu):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class Z(PyMenu):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                            class X(PyMenu):
                                """
                                Parameter X of value type float.
                                """
                                pass

                        class RotationAxisDirection(PyMenu):
                            """
                            Singleton RotationAxisDirection.
                            """
                            def __init__(self, service, rules, path):
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                super().__init__(service, rules, path)

                            class Z(PyMenu):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                            class Y(PyMenu):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class X(PyMenu):
                                """
                                Parameter X of value type float.
                                """
                                pass

                        class Direction(PyMenu):
                            """
                            Singleton Direction.
                            """
                            def __init__(self, service, rules, path):
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                super().__init__(service, rules, path)

                            class Z(PyMenu):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                            class X(PyMenu):
                                """
                                Parameter X of value type float.
                                """
                                pass

                            class Y(PyMenu):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                        class TranslationalDirection(PyMenu):
                            """
                            Singleton TranslationalDirection.
                            """
                            def __init__(self, service, rules, path):
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                super().__init__(service, rules, path)

                            class X(PyMenu):
                                """
                                Parameter X of value type float.
                                """
                                pass

                            class Z(PyMenu):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                            class Y(PyMenu):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                        class MassFlux(PyMenu):
                            """
                            Parameter MassFlux of value type float.
                            """
                            pass

                        class MassFlowRate(PyMenu):
                            """
                            Parameter MassFlowRate of value type float.
                            """
                            pass

                        class IsRotating(PyMenu):
                            """
                            Parameter IsRotating of value type bool.
                            """
                            pass

                        class VelocitySpecification(PyMenu):
                            """
                            Parameter VelocitySpecification of value type str.
                            """
                            pass

                        class DirectionSpecificationMethod(PyMenu):
                            """
                            Parameter DirectionSpecificationMethod of value type str.
                            """
                            pass

                        class TranslationalVelocityMagnitude(PyMenu):
                            """
                            Parameter TranslationalVelocityMagnitude of value type float.
                            """
                            pass

                        class TranslationalVelocitySpecification(PyMenu):
                            """
                            Parameter TranslationalVelocitySpecification of value type str.
                            """
                            pass

                        class GaugeTotalPressure(PyMenu):
                            """
                            Parameter GaugeTotalPressure of value type float.
                            """
                            pass

                        class VelocityMagnitude(PyMenu):
                            """
                            Parameter VelocityMagnitude of value type float.
                            """
                            pass

                        class WallVelocitySpecification(PyMenu):
                            """
                            Parameter WallVelocitySpecification of value type str.
                            """
                            pass

                        class SupersonicOrInitialGaugePressure(PyMenu):
                            """
                            Parameter SupersonicOrInitialGaugePressure of value type float.
                            """
                            pass

                        class IsMotionBC(PyMenu):
                            """
                            Parameter IsMotionBC of value type int.
                            """
                            pass

                        class GaugePressure(PyMenu):
                            """
                            Parameter GaugePressure of value type float.
                            """
                            pass

                        class AverageMassFlux(PyMenu):
                            """
                            Parameter AverageMassFlux of value type float.
                            """
                            pass

                        class MassFlowSpecificationMethod(PyMenu):
                            """
                            Parameter MassFlowSpecificationMethod of value type str.
                            """
                            pass

                        class MachNumber(PyMenu):
                            """
                            Parameter MachNumber of value type float.
                            """
                            pass

                        class RotationalSpeed(PyMenu):
                            """
                            Parameter RotationalSpeed of value type float.
                            """
                            pass

                    class Thermal(PyMenu):
                        """
                        Singleton Thermal.
                        """
                        def __init__(self, service, rules, path):
                            self.HeatTransferCoefficient = self.__class__.HeatTransferCoefficient(service, rules, path + [("HeatTransferCoefficient", "")])
                            self.HeatGenerationRate = self.__class__.HeatGenerationRate(service, rules, path + [("HeatGenerationRate", "")])
                            self.WallThickness = self.__class__.WallThickness(service, rules, path + [("WallThickness", "")])
                            self.TotalTemperature = self.__class__.TotalTemperature(service, rules, path + [("TotalTemperature", "")])
                            self.HeatFlux = self.__class__.HeatFlux(service, rules, path + [("HeatFlux", "")])
                            self.Temperature = self.__class__.Temperature(service, rules, path + [("Temperature", "")])
                            self.ExternalEmissivity = self.__class__.ExternalEmissivity(service, rules, path + [("ExternalEmissivity", "")])
                            self.ExternalRadiationTemperature = self.__class__.ExternalRadiationTemperature(service, rules, path + [("ExternalRadiationTemperature", "")])
                            self.FreeStreamTemperature = self.__class__.FreeStreamTemperature(service, rules, path + [("FreeStreamTemperature", "")])
                            self.ThermalConditions = self.__class__.ThermalConditions(service, rules, path + [("ThermalConditions", "")])
                            super().__init__(service, rules, path)

                        class HeatTransferCoefficient(PyMenu):
                            """
                            Parameter HeatTransferCoefficient of value type float.
                            """
                            pass

                        class HeatGenerationRate(PyMenu):
                            """
                            Parameter HeatGenerationRate of value type float.
                            """
                            pass

                        class WallThickness(PyMenu):
                            """
                            Parameter WallThickness of value type float.
                            """
                            pass

                        class TotalTemperature(PyMenu):
                            """
                            Parameter TotalTemperature of value type float.
                            """
                            pass

                        class HeatFlux(PyMenu):
                            """
                            Parameter HeatFlux of value type float.
                            """
                            pass

                        class Temperature(PyMenu):
                            """
                            Parameter Temperature of value type float.
                            """
                            pass

                        class ExternalEmissivity(PyMenu):
                            """
                            Parameter ExternalEmissivity of value type float.
                            """
                            pass

                        class ExternalRadiationTemperature(PyMenu):
                            """
                            Parameter ExternalRadiationTemperature of value type float.
                            """
                            pass

                        class FreeStreamTemperature(PyMenu):
                            """
                            Parameter FreeStreamTemperature of value type float.
                            """
                            pass

                        class ThermalConditions(PyMenu):
                            """
                            Parameter ThermalConditions of value type str.
                            """
                            pass

                    class Turbulence(PyMenu):
                        """
                        Singleton Turbulence.
                        """
                        def __init__(self, service, rules, path):
                            self.TurbulentViscosityRatio = self.__class__.TurbulentViscosityRatio(service, rules, path + [("TurbulentViscosityRatio", "")])
                            self.TurbulentIntensity = self.__class__.TurbulentIntensity(service, rules, path + [("TurbulentIntensity", "")])
                            self.SpecificationMethod = self.__class__.SpecificationMethod(service, rules, path + [("SpecificationMethod", "")])
                            self.TurbulentLengthScale = self.__class__.TurbulentLengthScale(service, rules, path + [("TurbulentLengthScale", "")])
                            self.HydraulicDiameter = self.__class__.HydraulicDiameter(service, rules, path + [("HydraulicDiameter", "")])
                            super().__init__(service, rules, path)

                        class TurbulentViscosityRatio(PyMenu):
                            """
                            Parameter TurbulentViscosityRatio of value type float.
                            """
                            pass

                        class TurbulentIntensity(PyMenu):
                            """
                            Parameter TurbulentIntensity of value type float.
                            """
                            pass

                        class SpecificationMethod(PyMenu):
                            """
                            Parameter SpecificationMethod of value type str.
                            """
                            pass

                        class TurbulentLengthScale(PyMenu):
                            """
                            Parameter TurbulentLengthScale of value type float.
                            """
                            pass

                        class HydraulicDiameter(PyMenu):
                            """
                            Parameter HydraulicDiameter of value type float.
                            """
                            pass

                    class BoundaryType(PyMenu):
                        """
                        Parameter BoundaryType of value type str.
                        """
                        pass

                    class BoundaryId(PyMenu):
                        """
                        Parameter BoundaryId of value type int.
                        """
                        pass

                    class _name_(PyMenu):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                def __getitem__(self, key: str) -> _Boundary:
                    return super().__getitem__(key)

            class Beta(PyMenu):
                """
                Parameter Beta of value type bool.
                """
                pass

        class Streaming(PyMenu):
            """
            Singleton Streaming.
            """
            def __init__(self, service, rules, path):
                self.Ack = self.__class__.Ack(service, rules, path + [("Ack", "")])
                super().__init__(service, rules, path)

            class Ack(PyMenu):
                """
                Parameter Ack of value type bool.
                """
                pass

        class App(PyMenu):
            """
            Singleton App.
            """
            def __init__(self, service, rules, path):
                self.BC = self.__class__.BC(service, rules, path + [("BC", "")])
                self.DP = self.__class__.DP(service, rules, path + [("DP", "")])
                self.RunType = self.__class__.RunType(service, rules, path + [("RunType", "")])
                self.Airflow = self.__class__.Airflow(service, rules, path + [("Airflow", "")])
                self.Solution = self.__class__.Solution(service, rules, path + [("Solution", "")])
                self.AeroWorkflow = self.__class__.AeroWorkflow(service, rules, path + [("AeroWorkflow", "")])
                self.Domain = self.__class__.Domain(service, rules, path + [("Domain", "")])
                self.GlobalSettings = self.__class__.GlobalSettings(service, rules, path + [("GlobalSettings", "")])
                self.SetupErrors = self.__class__.SetupErrors(service, rules, path + [("SetupErrors", "")])
                self.SetupWarnings = self.__class__.SetupWarnings(service, rules, path + [("SetupWarnings", "")])
                self.IsBusy = self.__class__.IsBusy(service, rules, path + [("IsBusy", "")])
                self.InProgress = self.__class__.InProgress(service, rules, path + [("InProgress", "")])
                self.SaveCaseAs = self.__class__.SaveCaseAs(service, rules, "SaveCaseAs", path)
                self.SavePostCaseAndData = self.__class__.SavePostCaseAndData(service, rules, "SavePostCaseAndData", path)
                self.SendCommandQuiet = self.__class__.SendCommandQuiet(service, rules, "SendCommandQuiet", path)
                self.CheckSetup = self.__class__.CheckSetup(service, rules, "CheckSetup", path)
                self.WriteAll = self.__class__.WriteAll(service, rules, "WriteAll", path)
                self.ImportMesh = self.__class__.ImportMesh(service, rules, "ImportMesh", path)
                self.InitAddOn = self.__class__.InitAddOn(service, rules, "InitAddOn", path)
                self.SaveCase = self.__class__.SaveCase(service, rules, "SaveCase", path)
                self.InitAddOnAero = self.__class__.InitAddOnAero(service, rules, "InitAddOnAero", path)
                self.ReloadCase = self.__class__.ReloadCase(service, rules, "ReloadCase", path)
                self.SyncDM = self.__class__.SyncDM(service, rules, "SyncDM", path)
                self.InitDM = self.__class__.InitDM(service, rules, "InitDM", path)
                self.SaveData = self.__class__.SaveData(service, rules, "SaveData", path)
                self.LoadCaseAndData = self.__class__.LoadCaseAndData(service, rules, "LoadCaseAndData", path)
                self.ReloadDomain = self.__class__.ReloadDomain(service, rules, "ReloadDomain", path)
                self.ImportCase = self.__class__.ImportCase(service, rules, "ImportCase", path)
                self.SaveCaseAndData = self.__class__.SaveCaseAndData(service, rules, "SaveCaseAndData", path)
                self.LoadCase = self.__class__.LoadCase(service, rules, "LoadCase", path)
                super().__init__(service, rules, path)

            class BC(PyNamedObjectContainer):
                class _BC(PyMenu):
                    """
                    Singleton _BC.
                    """
                    def __init__(self, service, rules, path):
                        self.AirflowWall = self.__class__.AirflowWall(service, rules, path + [("AirflowWall", "")])
                        self.Common = self.__class__.Common(service, rules, path + [("Common", "")])
                        self.AirflowVelocityInlet = self.__class__.AirflowVelocityInlet(service, rules, path + [("AirflowVelocityInlet", "")])
                        self.AirflowMassFlowOutlet = self.__class__.AirflowMassFlowOutlet(service, rules, path + [("AirflowMassFlowOutlet", "")])
                        self.AirflowPressureOutlet = self.__class__.AirflowPressureOutlet(service, rules, path + [("AirflowPressureOutlet", "")])
                        self.AirflowMassFlowInlet = self.__class__.AirflowMassFlowInlet(service, rules, path + [("AirflowMassFlowInlet", "")])
                        self.ComponentPart = self.__class__.ComponentPart(service, rules, path + [("ComponentPart", "")])
                        self.IsWall = self.__class__.IsWall(service, rules, path + [("IsWall", "")])
                        self.IsInlet = self.__class__.IsInlet(service, rules, path + [("IsInlet", "")])
                        self.IsExit = self.__class__.IsExit(service, rules, path + [("IsExit", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        self.BCType = self.__class__.BCType(service, rules, path + [("BCType", "")])
                        self.ComponentDisplay = self.__class__.ComponentDisplay(service, rules, "ComponentDisplay", path)
                        self.ChangeBCType = self.__class__.ChangeBCType(service, rules, "ChangeBCType", path)
                        self.ManageComponents = self.__class__.ManageComponents(service, rules, "ManageComponents", path)
                        self.MoveBCToGroup = self.__class__.MoveBCToGroup(service, rules, "MoveBCToGroup", path)
                        self.Display = self.__class__.Display(service, rules, "Display", path)
                        self.ReloadResultsCustomTable = self.__class__.ReloadResultsCustomTable(service, rules, "ReloadResultsCustomTable", path)
                        self.RefreshBCs = self.__class__.RefreshBCs(service, rules, "RefreshBCs", path)
                        self.ImportConditions = self.__class__.ImportConditions(service, rules, "ImportConditions", path)
                        self.ResetToCustom = self.__class__.ResetToCustom(service, rules, "ResetToCustom", path)
                        self.ManageOutputs = self.__class__.ManageOutputs(service, rules, "ManageOutputs", path)
                        self.RenameBC = self.__class__.RenameBC(service, rules, "RenameBC", path)
                        super().__init__(service, rules, path)

                    class AirflowWall(PyMenu):
                        """
                        Singleton AirflowWall.
                        """
                        def __init__(self, service, rules, path):
                            self.Temperature = self.__class__.Temperature(service, rules, path + [("Temperature", "")])
                            self.ThermalCondition = self.__class__.ThermalCondition(service, rules, path + [("ThermalCondition", "")])
                            self.HighRoughnessHeight = self.__class__.HighRoughnessHeight(service, rules, path + [("HighRoughnessHeight", "")])
                            self.HeatFlux = self.__class__.HeatFlux(service, rules, path + [("HeatFlux", "")])
                            self.Roughness = self.__class__.Roughness(service, rules, path + [("Roughness", "")])
                            super().__init__(service, rules, path)

                        class Temperature(PyMenu):
                            """
                            Parameter Temperature of value type float.
                            """
                            pass

                        class ThermalCondition(PyMenu):
                            """
                            Parameter ThermalCondition of value type str.
                            """
                            pass

                        class HighRoughnessHeight(PyMenu):
                            """
                            Parameter HighRoughnessHeight of value type float.
                            """
                            pass

                        class HeatFlux(PyMenu):
                            """
                            Parameter HeatFlux of value type float.
                            """
                            pass

                        class Roughness(PyMenu):
                            """
                            Parameter Roughness of value type str.
                            """
                            pass

                    class Common(PyMenu):
                        """
                        Singleton Common.
                        """
                        def __init__(self, service, rules, path):
                            self.Group = self.__class__.Group(service, rules, path + [("Group", "")])
                            self.DisplayThread = self.__class__.DisplayThread(service, rules, path + [("DisplayThread", "")])
                            self.Hidden = self.__class__.Hidden(service, rules, path + [("Hidden", "")])
                            super().__init__(service, rules, path)

                        class Group(PyMenu):
                            """
                            Parameter Group of value type str.
                            """
                            pass

                        class DisplayThread(PyMenu):
                            """
                            Parameter DisplayThread of value type str.
                            """
                            pass

                        class Hidden(PyMenu):
                            """
                            Parameter Hidden of value type bool.
                            """
                            pass

                    class AirflowVelocityInlet(PyMenu):
                        """
                        Singleton AirflowVelocityInlet.
                        """
                        def __init__(self, service, rules, path):
                            self.FlowX = self.__class__.FlowX(service, rules, path + [("FlowX", "")])
                            self.FlowDirection = self.__class__.FlowDirection(service, rules, path + [("FlowDirection", "")])
                            self.TemperatureCustom = self.__class__.TemperatureCustom(service, rules, path + [("TemperatureCustom", "")])
                            self.Pressure = self.__class__.Pressure(service, rules, path + [("Pressure", "")])
                            self.TurbSpecification = self.__class__.TurbSpecification(service, rules, path + [("TurbSpecification", "")])
                            self.NormalToBoundary = self.__class__.NormalToBoundary(service, rules, path + [("NormalToBoundary", "")])
                            self.TemperatureInput = self.__class__.TemperatureInput(service, rules, path + [("TemperatureInput", "")])
                            self.TurbViscRatio = self.__class__.TurbViscRatio(service, rules, path + [("TurbViscRatio", "")])
                            self.Temperature = self.__class__.Temperature(service, rules, path + [("Temperature", "")])
                            self.FlowXComputed = self.__class__.FlowXComputed(service, rules, path + [("FlowXComputed", "")])
                            self.FlowZComputed = self.__class__.FlowZComputed(service, rules, path + [("FlowZComputed", "")])
                            self.AngleBeta = self.__class__.AngleBeta(service, rules, path + [("AngleBeta", "")])
                            self.FlowMagnitudeComputed = self.__class__.FlowMagnitudeComputed(service, rules, path + [("FlowMagnitudeComputed", "")])
                            self.SettingsVisible = self.__class__.SettingsVisible(service, rules, path + [("SettingsVisible", "")])
                            self.FlowMagnitude = self.__class__.FlowMagnitude(service, rules, path + [("FlowMagnitude", "")])
                            self.TurbIntensity = self.__class__.TurbIntensity(service, rules, path + [("TurbIntensity", "")])
                            self.Mach = self.__class__.Mach(service, rules, path + [("Mach", "")])
                            self.MachComputed = self.__class__.MachComputed(service, rules, path + [("MachComputed", "")])
                            self.FlowYComputed = self.__class__.FlowYComputed(service, rules, path + [("FlowYComputed", "")])
                            self.BCSync = self.__class__.BCSync(service, rules, path + [("BCSync", "")])
                            self.TurbIntermittency = self.__class__.TurbIntermittency(service, rules, path + [("TurbIntermittency", "")])
                            self.PressureInput = self.__class__.PressureInput(service, rules, path + [("PressureInput", "")])
                            self.SettingsEditable = self.__class__.SettingsEditable(service, rules, path + [("SettingsEditable", "")])
                            self.PressureCustom = self.__class__.PressureCustom(service, rules, path + [("PressureCustom", "")])
                            self.AbsolutePressure = self.__class__.AbsolutePressure(service, rules, path + [("AbsolutePressure", "")])
                            self.VelocityMode = self.__class__.VelocityMode(service, rules, path + [("VelocityMode", "")])
                            self.FlowZ = self.__class__.FlowZ(service, rules, path + [("FlowZ", "")])
                            self.AngleAlpha = self.__class__.AngleAlpha(service, rules, path + [("AngleAlpha", "")])
                            self.FlowY = self.__class__.FlowY(service, rules, path + [("FlowY", "")])
                            super().__init__(service, rules, path)

                        class FlowX(PyMenu):
                            """
                            Parameter FlowX of value type float.
                            """
                            pass

                        class FlowDirection(PyMenu):
                            """
                            Parameter FlowDirection of value type str.
                            """
                            pass

                        class TemperatureCustom(PyMenu):
                            """
                            Parameter TemperatureCustom of value type str.
                            """
                            pass

                        class Pressure(PyMenu):
                            """
                            Parameter Pressure of value type float.
                            """
                            pass

                        class TurbSpecification(PyMenu):
                            """
                            Parameter TurbSpecification of value type str.
                            """
                            pass

                        class NormalToBoundary(PyMenu):
                            """
                            Parameter NormalToBoundary of value type bool.
                            """
                            pass

                        class TemperatureInput(PyMenu):
                            """
                            Parameter TemperatureInput of value type str.
                            """
                            pass

                        class TurbViscRatio(PyMenu):
                            """
                            Parameter TurbViscRatio of value type float.
                            """
                            pass

                        class Temperature(PyMenu):
                            """
                            Parameter Temperature of value type float.
                            """
                            pass

                        class FlowXComputed(PyMenu):
                            """
                            Parameter FlowXComputed of value type float.
                            """
                            pass

                        class FlowZComputed(PyMenu):
                            """
                            Parameter FlowZComputed of value type float.
                            """
                            pass

                        class AngleBeta(PyMenu):
                            """
                            Parameter AngleBeta of value type float.
                            """
                            pass

                        class FlowMagnitudeComputed(PyMenu):
                            """
                            Parameter FlowMagnitudeComputed of value type float.
                            """
                            pass

                        class SettingsVisible(PyMenu):
                            """
                            Parameter SettingsVisible of value type bool.
                            """
                            pass

                        class FlowMagnitude(PyMenu):
                            """
                            Parameter FlowMagnitude of value type float.
                            """
                            pass

                        class TurbIntensity(PyMenu):
                            """
                            Parameter TurbIntensity of value type float.
                            """
                            pass

                        class Mach(PyMenu):
                            """
                            Parameter Mach of value type float.
                            """
                            pass

                        class MachComputed(PyMenu):
                            """
                            Parameter MachComputed of value type float.
                            """
                            pass

                        class FlowYComputed(PyMenu):
                            """
                            Parameter FlowYComputed of value type float.
                            """
                            pass

                        class BCSync(PyMenu):
                            """
                            Parameter BCSync of value type str.
                            """
                            pass

                        class TurbIntermittency(PyMenu):
                            """
                            Parameter TurbIntermittency of value type float.
                            """
                            pass

                        class PressureInput(PyMenu):
                            """
                            Parameter PressureInput of value type str.
                            """
                            pass

                        class SettingsEditable(PyMenu):
                            """
                            Parameter SettingsEditable of value type bool.
                            """
                            pass

                        class PressureCustom(PyMenu):
                            """
                            Parameter PressureCustom of value type str.
                            """
                            pass

                        class AbsolutePressure(PyMenu):
                            """
                            Parameter AbsolutePressure of value type float.
                            """
                            pass

                        class VelocityMode(PyMenu):
                            """
                            Parameter VelocityMode of value type str.
                            """
                            pass

                        class FlowZ(PyMenu):
                            """
                            Parameter FlowZ of value type float.
                            """
                            pass

                        class AngleAlpha(PyMenu):
                            """
                            Parameter AngleAlpha of value type float.
                            """
                            pass

                        class FlowY(PyMenu):
                            """
                            Parameter FlowY of value type float.
                            """
                            pass

                    class AirflowMassFlowOutlet(PyMenu):
                        """
                        Singleton AirflowMassFlowOutlet.
                        """
                        def __init__(self, service, rules, path):
                            self.MassFlowMode = self.__class__.MassFlowMode(service, rules, path + [("MassFlowMode", "")])
                            self.MassFlowInput = self.__class__.MassFlowInput(service, rules, path + [("MassFlowInput", "")])
                            self.BCSync = self.__class__.BCSync(service, rules, path + [("BCSync", "")])
                            self.MassFlow = self.__class__.MassFlow(service, rules, path + [("MassFlow", "")])
                            self.MassFlowCustom = self.__class__.MassFlowCustom(service, rules, path + [("MassFlowCustom", "")])
                            self.SettingsVisible = self.__class__.SettingsVisible(service, rules, path + [("SettingsVisible", "")])
                            self.SettingsEditable = self.__class__.SettingsEditable(service, rules, path + [("SettingsEditable", "")])
                            super().__init__(service, rules, path)

                        class MassFlowMode(PyMenu):
                            """
                            Parameter MassFlowMode of value type str.
                            """
                            pass

                        class MassFlowInput(PyMenu):
                            """
                            Parameter MassFlowInput of value type str.
                            """
                            pass

                        class BCSync(PyMenu):
                            """
                            Parameter BCSync of value type str.
                            """
                            pass

                        class MassFlow(PyMenu):
                            """
                            Parameter MassFlow of value type float.
                            """
                            pass

                        class MassFlowCustom(PyMenu):
                            """
                            Parameter MassFlowCustom of value type str.
                            """
                            pass

                        class SettingsVisible(PyMenu):
                            """
                            Parameter SettingsVisible of value type bool.
                            """
                            pass

                        class SettingsEditable(PyMenu):
                            """
                            Parameter SettingsEditable of value type bool.
                            """
                            pass

                    class AirflowPressureOutlet(PyMenu):
                        """
                        Singleton AirflowPressureOutlet.
                        """
                        def __init__(self, service, rules, path):
                            self.TemperatureCustom = self.__class__.TemperatureCustom(service, rules, path + [("TemperatureCustom", "")])
                            self.TemperatureInput = self.__class__.TemperatureInput(service, rules, path + [("TemperatureInput", "")])
                            self.AbsolutePressure = self.__class__.AbsolutePressure(service, rules, path + [("AbsolutePressure", "")])
                            self.Pressure = self.__class__.Pressure(service, rules, path + [("Pressure", "")])
                            self.BCSync = self.__class__.BCSync(service, rules, path + [("BCSync", "")])
                            self.PressureCustom = self.__class__.PressureCustom(service, rules, path + [("PressureCustom", "")])
                            self.PressureInput = self.__class__.PressureInput(service, rules, path + [("PressureInput", "")])
                            self.Temperature = self.__class__.Temperature(service, rules, path + [("Temperature", "")])
                            self.SettingsVisible = self.__class__.SettingsVisible(service, rules, path + [("SettingsVisible", "")])
                            self.SettingsEditable = self.__class__.SettingsEditable(service, rules, path + [("SettingsEditable", "")])
                            super().__init__(service, rules, path)

                        class TemperatureCustom(PyMenu):
                            """
                            Parameter TemperatureCustom of value type str.
                            """
                            pass

                        class TemperatureInput(PyMenu):
                            """
                            Parameter TemperatureInput of value type str.
                            """
                            pass

                        class AbsolutePressure(PyMenu):
                            """
                            Parameter AbsolutePressure of value type float.
                            """
                            pass

                        class Pressure(PyMenu):
                            """
                            Parameter Pressure of value type float.
                            """
                            pass

                        class BCSync(PyMenu):
                            """
                            Parameter BCSync of value type str.
                            """
                            pass

                        class PressureCustom(PyMenu):
                            """
                            Parameter PressureCustom of value type str.
                            """
                            pass

                        class PressureInput(PyMenu):
                            """
                            Parameter PressureInput of value type str.
                            """
                            pass

                        class Temperature(PyMenu):
                            """
                            Parameter Temperature of value type float.
                            """
                            pass

                        class SettingsVisible(PyMenu):
                            """
                            Parameter SettingsVisible of value type bool.
                            """
                            pass

                        class SettingsEditable(PyMenu):
                            """
                            Parameter SettingsEditable of value type bool.
                            """
                            pass

                    class AirflowMassFlowInlet(PyMenu):
                        """
                        Singleton AirflowMassFlowInlet.
                        """
                        def __init__(self, service, rules, path):
                            self.TurbSpecification = self.__class__.TurbSpecification(service, rules, path + [("TurbSpecification", "")])
                            self.FlowY = self.__class__.FlowY(service, rules, path + [("FlowY", "")])
                            self.MassFlow = self.__class__.MassFlow(service, rules, path + [("MassFlow", "")])
                            self.AbsolutePressure = self.__class__.AbsolutePressure(service, rules, path + [("AbsolutePressure", "")])
                            self.FlowZ = self.__class__.FlowZ(service, rules, path + [("FlowZ", "")])
                            self.PressureCustom = self.__class__.PressureCustom(service, rules, path + [("PressureCustom", "")])
                            self.Pressure = self.__class__.Pressure(service, rules, path + [("Pressure", "")])
                            self.Temperature = self.__class__.Temperature(service, rules, path + [("Temperature", "")])
                            self.TurbIntensity = self.__class__.TurbIntensity(service, rules, path + [("TurbIntensity", "")])
                            self.SettingsVisible = self.__class__.SettingsVisible(service, rules, path + [("SettingsVisible", "")])
                            self.MassFlowInput = self.__class__.MassFlowInput(service, rules, path + [("MassFlowInput", "")])
                            self.TurbViscRatio = self.__class__.TurbViscRatio(service, rules, path + [("TurbViscRatio", "")])
                            self.DirectionMode = self.__class__.DirectionMode(service, rules, path + [("DirectionMode", "")])
                            self.PressureInput = self.__class__.PressureInput(service, rules, path + [("PressureInput", "")])
                            self.TurbIntermittency = self.__class__.TurbIntermittency(service, rules, path + [("TurbIntermittency", "")])
                            self.FlowX = self.__class__.FlowX(service, rules, path + [("FlowX", "")])
                            self.TemperatureCustom = self.__class__.TemperatureCustom(service, rules, path + [("TemperatureCustom", "")])
                            self.SettingsEditable = self.__class__.SettingsEditable(service, rules, path + [("SettingsEditable", "")])
                            self.MassFlowMode = self.__class__.MassFlowMode(service, rules, path + [("MassFlowMode", "")])
                            self.BCSync = self.__class__.BCSync(service, rules, path + [("BCSync", "")])
                            self.MassFlowCustom = self.__class__.MassFlowCustom(service, rules, path + [("MassFlowCustom", "")])
                            self.TemperatureInput = self.__class__.TemperatureInput(service, rules, path + [("TemperatureInput", "")])
                            super().__init__(service, rules, path)

                        class TurbSpecification(PyMenu):
                            """
                            Parameter TurbSpecification of value type str.
                            """
                            pass

                        class FlowY(PyMenu):
                            """
                            Parameter FlowY of value type float.
                            """
                            pass

                        class MassFlow(PyMenu):
                            """
                            Parameter MassFlow of value type float.
                            """
                            pass

                        class AbsolutePressure(PyMenu):
                            """
                            Parameter AbsolutePressure of value type float.
                            """
                            pass

                        class FlowZ(PyMenu):
                            """
                            Parameter FlowZ of value type float.
                            """
                            pass

                        class PressureCustom(PyMenu):
                            """
                            Parameter PressureCustom of value type str.
                            """
                            pass

                        class Pressure(PyMenu):
                            """
                            Parameter Pressure of value type float.
                            """
                            pass

                        class Temperature(PyMenu):
                            """
                            Parameter Temperature of value type float.
                            """
                            pass

                        class TurbIntensity(PyMenu):
                            """
                            Parameter TurbIntensity of value type float.
                            """
                            pass

                        class SettingsVisible(PyMenu):
                            """
                            Parameter SettingsVisible of value type bool.
                            """
                            pass

                        class MassFlowInput(PyMenu):
                            """
                            Parameter MassFlowInput of value type str.
                            """
                            pass

                        class TurbViscRatio(PyMenu):
                            """
                            Parameter TurbViscRatio of value type float.
                            """
                            pass

                        class DirectionMode(PyMenu):
                            """
                            Parameter DirectionMode of value type str.
                            """
                            pass

                        class PressureInput(PyMenu):
                            """
                            Parameter PressureInput of value type str.
                            """
                            pass

                        class TurbIntermittency(PyMenu):
                            """
                            Parameter TurbIntermittency of value type float.
                            """
                            pass

                        class FlowX(PyMenu):
                            """
                            Parameter FlowX of value type float.
                            """
                            pass

                        class TemperatureCustom(PyMenu):
                            """
                            Parameter TemperatureCustom of value type str.
                            """
                            pass

                        class SettingsEditable(PyMenu):
                            """
                            Parameter SettingsEditable of value type bool.
                            """
                            pass

                        class MassFlowMode(PyMenu):
                            """
                            Parameter MassFlowMode of value type str.
                            """
                            pass

                        class BCSync(PyMenu):
                            """
                            Parameter BCSync of value type str.
                            """
                            pass

                        class MassFlowCustom(PyMenu):
                            """
                            Parameter MassFlowCustom of value type str.
                            """
                            pass

                        class TemperatureInput(PyMenu):
                            """
                            Parameter TemperatureInput of value type str.
                            """
                            pass

                    class ComponentPart(PyMenu):
                        """
                        Parameter ComponentPart of value type str.
                        """
                        pass

                    class IsWall(PyMenu):
                        """
                        Parameter IsWall of value type bool.
                        """
                        pass

                    class IsInlet(PyMenu):
                        """
                        Parameter IsInlet of value type bool.
                        """
                        pass

                    class IsExit(PyMenu):
                        """
                        Parameter IsExit of value type bool.
                        """
                        pass

                    class _name_(PyMenu):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                    class BCType(PyMenu):
                        """
                        Parameter BCType of value type str.
                        """
                        pass

                    class ComponentDisplay(PyCommand):
                        """
                        ComponentDisplay(GroupName: str) -> bool
                        """
                        pass

                    class ChangeBCType(PyCommand):
                        """
                        ChangeBCType(BCName: str, BCType: str) -> bool
                        """
                        pass

                    class ManageComponents(PyCommand):
                        """
                        ManageComponents() -> bool
                        """
                        pass

                    class MoveBCToGroup(PyCommand):
                        """
                        MoveBCToGroup(BCName: str, GroupName: str) -> bool
                        """
                        pass

                    class Display(PyCommand):
                        """
                        Display() -> bool
                        """
                        pass

                    class ReloadResultsCustomTable(PyCommand):
                        """
                        ReloadResultsCustomTable() -> bool
                        """
                        pass

                    class RefreshBCs(PyCommand):
                        """
                        RefreshBCs() -> bool
                        """
                        pass

                    class ImportConditions(PyCommand):
                        """
                        ImportConditions() -> bool
                        """
                        pass

                    class ResetToCustom(PyCommand):
                        """
                        ResetToCustom() -> bool
                        """
                        pass

                    class ManageOutputs(PyCommand):
                        """
                        ManageOutputs() -> bool
                        """
                        pass

                    class RenameBC(PyCommand):
                        """
                        RenameBC(BCName: str, NewName: str) -> bool
                        """
                        pass

                def __getitem__(self, key: str) -> _BC:
                    return super().__getitem__(key)

            class DP(PyNamedObjectContainer):
                class _DP(PyMenu):
                    """
                    Singleton _DP.
                    """
                    def __init__(self, service, rules, path):
                        self.Inputs = self.__class__.Inputs(service, rules, path + [("Inputs", "")])
                        self.Residuals = self.__class__.Residuals(service, rules, path + [("Residuals", "")])
                        self.Outputs = self.__class__.Outputs(service, rules, path + [("Outputs", "")])
                        self.Solve = self.__class__.Solve(service, rules, path + [("Solve", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        self.DP = self.__class__.DP(service, rules, path + [("DP", "")])
                        self.Status = self.__class__.Status(service, rules, path + [("Status", "")])
                        self.Converged = self.__class__.Converged(service, rules, path + [("Converged", "")])
                        self.StatusBackup = self.__class__.StatusBackup(service, rules, path + [("StatusBackup", "")])
                        self.SaveStringFlag = self.__class__.SaveStringFlag(service, rules, path + [("SaveStringFlag", "")])
                        super().__init__(service, rules, path)

                    class Inputs(PyMenu):
                        """
                        Singleton Inputs.
                        """
                        def __init__(self, service, rules, path):
                            self.ParameterSearch = self.__class__.ParameterSearch(service, rules, path + [("ParameterSearch", "")])
                            self.ComponentInputs = self.__class__.ComponentInputs(service, rules, path + [("ComponentInputs", "")])
                            self.Conditions = self.__class__.Conditions(service, rules, path + [("Conditions", "")])
                            self.CustomInputs = self.__class__.CustomInputs(service, rules, path + [("CustomInputs", "")])
                            super().__init__(service, rules, path)

                        class ParameterSearch(PyMenu):
                            """
                            Singleton ParameterSearch.
                            """
                            def __init__(self, service, rules, path):
                                self.Parameters = self.__class__.Parameters(service, rules, path + [("Parameters", "")])
                                self.Values = self.__class__.Values(service, rules, path + [("Values", "")])
                                super().__init__(service, rules, path)

                            class Parameters(PyMenu):
                                """
                                Parameter Parameters of value type List[str].
                                """
                                pass

                            class Values(PyMenu):
                                """
                                Parameter Values of value type List[float].
                                """
                                pass

                        class ComponentInputs(PyMenu):
                            """
                            Singleton ComponentInputs.
                            """
                            def __init__(self, service, rules, path):
                                self.Parameters = self.__class__.Parameters(service, rules, path + [("Parameters", "")])
                                self.Values = self.__class__.Values(service, rules, path + [("Values", "")])
                                super().__init__(service, rules, path)

                            class Parameters(PyMenu):
                                """
                                Parameter Parameters of value type List[str].
                                """
                                pass

                            class Values(PyMenu):
                                """
                                Parameter Values of value type List[float].
                                """
                                pass

                        class Conditions(PyMenu):
                            """
                            Singleton Conditions.
                            """
                            def __init__(self, service, rules, path):
                                self.Mach = self.__class__.Mach(service, rules, path + [("Mach", "")])
                                self.Altitude = self.__class__.Altitude(service, rules, path + [("Altitude", "")])
                                self.AoA = self.__class__.AoA(service, rules, path + [("AoA", "")])
                                self.Pressure = self.__class__.Pressure(service, rules, path + [("Pressure", "")])
                                self.Temperature = self.__class__.Temperature(service, rules, path + [("Temperature", "")])
                                self.AoS = self.__class__.AoS(service, rules, path + [("AoS", "")])
                                self.TotalPressure = self.__class__.TotalPressure(service, rules, path + [("TotalPressure", "")])
                                self.MassFlow = self.__class__.MassFlow(service, rules, path + [("MassFlow", "")])
                                self.TotalTemperature = self.__class__.TotalTemperature(service, rules, path + [("TotalTemperature", "")])
                                self.TAS = self.__class__.TAS(service, rules, path + [("TAS", "")])
                                self.Reynolds = self.__class__.Reynolds(service, rules, path + [("Reynolds", "")])
                                super().__init__(service, rules, path)

                            class Mach(PyMenu):
                                """
                                Parameter Mach of value type float.
                                """
                                pass

                            class Altitude(PyMenu):
                                """
                                Parameter Altitude of value type float.
                                """
                                pass

                            class AoA(PyMenu):
                                """
                                Parameter AoA of value type float.
                                """
                                pass

                            class Pressure(PyMenu):
                                """
                                Parameter Pressure of value type float.
                                """
                                pass

                            class Temperature(PyMenu):
                                """
                                Parameter Temperature of value type float.
                                """
                                pass

                            class AoS(PyMenu):
                                """
                                Parameter AoS of value type float.
                                """
                                pass

                            class TotalPressure(PyMenu):
                                """
                                Parameter TotalPressure of value type float.
                                """
                                pass

                            class MassFlow(PyMenu):
                                """
                                Parameter MassFlow of value type float.
                                """
                                pass

                            class TotalTemperature(PyMenu):
                                """
                                Parameter TotalTemperature of value type float.
                                """
                                pass

                            class TAS(PyMenu):
                                """
                                Parameter TAS of value type float.
                                """
                                pass

                            class Reynolds(PyMenu):
                                """
                                Parameter Reynolds of value type float.
                                """
                                pass

                        class CustomInputs(PyMenu):
                            """
                            Singleton CustomInputs.
                            """
                            def __init__(self, service, rules, path):
                                self.Parameters = self.__class__.Parameters(service, rules, path + [("Parameters", "")])
                                self.Values = self.__class__.Values(service, rules, path + [("Values", "")])
                                super().__init__(service, rules, path)

                            class Parameters(PyMenu):
                                """
                                Parameter Parameters of value type List[str].
                                """
                                pass

                            class Values(PyMenu):
                                """
                                Parameter Values of value type List[float].
                                """
                                pass

                    class Residuals(PyMenu):
                        """
                        Singleton Residuals.
                        """
                        def __init__(self, service, rules, path):
                            self.Values = self.__class__.Values(service, rules, path + [("Values", "")])
                            self.Parameters = self.__class__.Parameters(service, rules, path + [("Parameters", "")])
                            super().__init__(service, rules, path)

                        class Values(PyMenu):
                            """
                            Parameter Values of value type List[float].
                            """
                            pass

                        class Parameters(PyMenu):
                            """
                            Parameter Parameters of value type List[str].
                            """
                            pass

                    class Outputs(PyMenu):
                        """
                        Singleton Outputs.
                        """
                        def __init__(self, service, rules, path):
                            self.AverageResiduals = self.__class__.AverageResiduals(service, rules, path + [("AverageResiduals", "")])
                            self.CustomOutputs = self.__class__.CustomOutputs(service, rules, path + [("CustomOutputs", "")])
                            self.Forces = self.__class__.Forces(service, rules, path + [("Forces", "")])
                            self.ComponentMonitors = self.__class__.ComponentMonitors(service, rules, path + [("ComponentMonitors", "")])
                            self.CoefficientResiduals = self.__class__.CoefficientResiduals(service, rules, path + [("CoefficientResiduals", "")])
                            self.ComponentOutputs = self.__class__.ComponentOutputs(service, rules, path + [("ComponentOutputs", "")])
                            self.Coefficients = self.__class__.Coefficients(service, rules, path + [("Coefficients", "")])
                            self.ParameterSearch = self.__class__.ParameterSearch(service, rules, path + [("ParameterSearch", "")])
                            super().__init__(service, rules, path)

                        class AverageResiduals(PyMenu):
                            """
                            Singleton AverageResiduals.
                            """
                            def __init__(self, service, rules, path):
                                self.ResidualsAverage = self.__class__.ResidualsAverage(service, rules, path + [("ResidualsAverage", "")])
                                self.CoefficientResidualsAverage = self.__class__.CoefficientResidualsAverage(service, rules, path + [("CoefficientResidualsAverage", "")])
                                super().__init__(service, rules, path)

                            class ResidualsAverage(PyMenu):
                                """
                                Parameter ResidualsAverage of value type float.
                                """
                                pass

                            class CoefficientResidualsAverage(PyMenu):
                                """
                                Parameter CoefficientResidualsAverage of value type float.
                                """
                                pass

                        class CustomOutputs(PyMenu):
                            """
                            Singleton CustomOutputs.
                            """
                            def __init__(self, service, rules, path):
                                self.Values = self.__class__.Values(service, rules, path + [("Values", "")])
                                self.Parameters = self.__class__.Parameters(service, rules, path + [("Parameters", "")])
                                super().__init__(service, rules, path)

                            class Values(PyMenu):
                                """
                                Parameter Values of value type List[float].
                                """
                                pass

                            class Parameters(PyMenu):
                                """
                                Parameter Parameters of value type List[str].
                                """
                                pass

                        class Forces(PyMenu):
                            """
                            Singleton Forces.
                            """
                            def __init__(self, service, rules, path):
                                self.Drag = self.__class__.Drag(service, rules, path + [("Drag", "")])
                                self.MomentRoll = self.__class__.MomentRoll(service, rules, path + [("MomentRoll", "")])
                                self.MomentYaw = self.__class__.MomentYaw(service, rules, path + [("MomentYaw", "")])
                                self.Lift = self.__class__.Lift(service, rules, path + [("Lift", "")])
                                self.MomentPitch = self.__class__.MomentPitch(service, rules, path + [("MomentPitch", "")])
                                super().__init__(service, rules, path)

                            class Drag(PyMenu):
                                """
                                Parameter Drag of value type float.
                                """
                                pass

                            class MomentRoll(PyMenu):
                                """
                                Parameter MomentRoll of value type float.
                                """
                                pass

                            class MomentYaw(PyMenu):
                                """
                                Parameter MomentYaw of value type float.
                                """
                                pass

                            class Lift(PyMenu):
                                """
                                Parameter Lift of value type float.
                                """
                                pass

                            class MomentPitch(PyMenu):
                                """
                                Parameter MomentPitch of value type float.
                                """
                                pass

                        class ComponentMonitors(PyMenu):
                            """
                            Singleton ComponentMonitors.
                            """
                            def __init__(self, service, rules, path):
                                self.Values = self.__class__.Values(service, rules, path + [("Values", "")])
                                self.Parameters = self.__class__.Parameters(service, rules, path + [("Parameters", "")])
                                super().__init__(service, rules, path)

                            class Values(PyMenu):
                                """
                                Parameter Values of value type List[float].
                                """
                                pass

                            class Parameters(PyMenu):
                                """
                                Parameter Parameters of value type List[str].
                                """
                                pass

                        class CoefficientResiduals(PyMenu):
                            """
                            Singleton CoefficientResiduals.
                            """
                            def __init__(self, service, rules, path):
                                self.CoefficientMomentPitchResidual = self.__class__.CoefficientMomentPitchResidual(service, rules, path + [("CoefficientMomentPitchResidual", "")])
                                self.CoefficientMomentRollResidual = self.__class__.CoefficientMomentRollResidual(service, rules, path + [("CoefficientMomentRollResidual", "")])
                                self.CoefficientMomentYawResidual = self.__class__.CoefficientMomentYawResidual(service, rules, path + [("CoefficientMomentYawResidual", "")])
                                self.CoefficientDragResidual = self.__class__.CoefficientDragResidual(service, rules, path + [("CoefficientDragResidual", "")])
                                self.CoefficientLiftResidual = self.__class__.CoefficientLiftResidual(service, rules, path + [("CoefficientLiftResidual", "")])
                                super().__init__(service, rules, path)

                            class CoefficientMomentPitchResidual(PyMenu):
                                """
                                Parameter CoefficientMomentPitchResidual of value type float.
                                """
                                pass

                            class CoefficientMomentRollResidual(PyMenu):
                                """
                                Parameter CoefficientMomentRollResidual of value type float.
                                """
                                pass

                            class CoefficientMomentYawResidual(PyMenu):
                                """
                                Parameter CoefficientMomentYawResidual of value type float.
                                """
                                pass

                            class CoefficientDragResidual(PyMenu):
                                """
                                Parameter CoefficientDragResidual of value type float.
                                """
                                pass

                            class CoefficientLiftResidual(PyMenu):
                                """
                                Parameter CoefficientLiftResidual of value type float.
                                """
                                pass

                        class ComponentOutputs(PyMenu):
                            """
                            Singleton ComponentOutputs.
                            """
                            def __init__(self, service, rules, path):
                                self.Values = self.__class__.Values(service, rules, path + [("Values", "")])
                                self.Parameters = self.__class__.Parameters(service, rules, path + [("Parameters", "")])
                                super().__init__(service, rules, path)

                            class Values(PyMenu):
                                """
                                Parameter Values of value type List[float].
                                """
                                pass

                            class Parameters(PyMenu):
                                """
                                Parameter Parameters of value type List[str].
                                """
                                pass

                        class Coefficients(PyMenu):
                            """
                            Singleton Coefficients.
                            """
                            def __init__(self, service, rules, path):
                                self.CoefficientMomentPitch = self.__class__.CoefficientMomentPitch(service, rules, path + [("CoefficientMomentPitch", "")])
                                self.CoefficientLift = self.__class__.CoefficientLift(service, rules, path + [("CoefficientLift", "")])
                                self.CoefficientDrag = self.__class__.CoefficientDrag(service, rules, path + [("CoefficientDrag", "")])
                                self.CoefficientMomentYaw = self.__class__.CoefficientMomentYaw(service, rules, path + [("CoefficientMomentYaw", "")])
                                self.CoefficientMomentRoll = self.__class__.CoefficientMomentRoll(service, rules, path + [("CoefficientMomentRoll", "")])
                                super().__init__(service, rules, path)

                            class CoefficientMomentPitch(PyMenu):
                                """
                                Parameter CoefficientMomentPitch of value type float.
                                """
                                pass

                            class CoefficientLift(PyMenu):
                                """
                                Parameter CoefficientLift of value type float.
                                """
                                pass

                            class CoefficientDrag(PyMenu):
                                """
                                Parameter CoefficientDrag of value type float.
                                """
                                pass

                            class CoefficientMomentYaw(PyMenu):
                                """
                                Parameter CoefficientMomentYaw of value type float.
                                """
                                pass

                            class CoefficientMomentRoll(PyMenu):
                                """
                                Parameter CoefficientMomentRoll of value type float.
                                """
                                pass

                        class ParameterSearch(PyMenu):
                            """
                            Singleton ParameterSearch.
                            """
                            def __init__(self, service, rules, path):
                                self.Values = self.__class__.Values(service, rules, path + [("Values", "")])
                                self.Parameters = self.__class__.Parameters(service, rules, path + [("Parameters", "")])
                                super().__init__(service, rules, path)

                            class Values(PyMenu):
                                """
                                Parameter Values of value type List[float].
                                """
                                pass

                            class Parameters(PyMenu):
                                """
                                Parameter Parameters of value type List[str].
                                """
                                pass

                    class Solve(PyMenu):
                        """
                        Singleton Solve.
                        """
                        def __init__(self, service, rules, path):
                            self.FluentCFFPost = self.__class__.FluentCFFPost(service, rules, path + [("FluentCFFPost", "")])
                            self.ConvergenceSettings = self.__class__.ConvergenceSettings(service, rules, path + [("ConvergenceSettings", "")])
                            self.JournalsSettings = self.__class__.JournalsSettings(service, rules, path + [("JournalsSettings", "")])
                            self.MaterialsSettings = self.__class__.MaterialsSettings(service, rules, path + [("MaterialsSettings", "")])
                            self.ParameterSearchSettings = self.__class__.ParameterSearchSettings(service, rules, path + [("ParameterSearchSettings", "")])
                            self.ModelsSettings = self.__class__.ModelsSettings(service, rules, path + [("ModelsSettings", "")])
                            self.InitializationSettings = self.__class__.InitializationSettings(service, rules, path + [("InitializationSettings", "")])
                            self.SolutionSettings = self.__class__.SolutionSettings(service, rules, path + [("SolutionSettings", "")])
                            self.ShowAdvanced = self.__class__.ShowAdvanced(service, rules, path + [("ShowAdvanced", "")])
                            self.SolverType = self.__class__.SolverType(service, rules, path + [("SolverType", "")])
                            self.AeroCalculateDP = self.__class__.AeroCalculateDP(service, rules, path + [("AeroCalculateDP", "")])
                            self.Iterations = self.__class__.Iterations(service, rules, path + [("Iterations", "")])
                            self.AeroRunNext = self.__class__.AeroRunNext(service, rules, "AeroRunNext", path)
                            self.AeroInitializeAllDPs = self.__class__.AeroInitializeAllDPs(service, rules, "AeroInitializeAllDPs", path)
                            self.AeroApplySettingsSolver = self.__class__.AeroApplySettingsSolver(service, rules, "AeroApplySettingsSolver", path)
                            self.AeroApplySettingsConvergence = self.__class__.AeroApplySettingsConvergence(service, rules, "AeroApplySettingsConvergence", path)
                            self.AeroInterrupt = self.__class__.AeroInterrupt(service, rules, "AeroInterrupt", path)
                            self.AeroCalculate = self.__class__.AeroCalculate(service, rules, "AeroCalculate", path)
                            self.AeroInitializeCurrentDP = self.__class__.AeroInitializeCurrentDP(service, rules, "AeroInitializeCurrentDP", path)
                            self.AeroSolveUseCaseSettings = self.__class__.AeroSolveUseCaseSettings(service, rules, "AeroSolveUseCaseSettings", path)
                            self.AeroContinue = self.__class__.AeroContinue(service, rules, "AeroContinue", path)
                            self.AeroSolveUseDefaultSettings = self.__class__.AeroSolveUseDefaultSettings(service, rules, "AeroSolveUseDefaultSettings", path)
                            self.AeroSave = self.__class__.AeroSave(service, rules, "AeroSave", path)
                            super().__init__(service, rules, path)

                        class FluentCFFPost(PyMenu):
                            """
                            Singleton FluentCFFPost.
                            """
                            def __init__(self, service, rules, path):
                                self.ReadOnly = self.__class__.ReadOnly(service, rules, path + [("ReadOnly", "")])
                                self.ZoneType = self.__class__.ZoneType(service, rules, path + [("ZoneType", "")])
                                self.WriteLevel = self.__class__.WriteLevel(service, rules, path + [("WriteLevel", "")])
                                self.WriteCase = self.__class__.WriteCase(service, rules, path + [("WriteCase", "")])
                                self.WriteMode = self.__class__.WriteMode(service, rules, path + [("WriteMode", "")])
                                self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                                self.Fields = self.__class__.Fields(service, rules, path + [("Fields", "")])
                                super().__init__(service, rules, path)

                            class ReadOnly(PyMenu):
                                """
                                Parameter ReadOnly of value type bool.
                                """
                                pass

                            class ZoneType(PyMenu):
                                """
                                Parameter ZoneType of value type str.
                                """
                                pass

                            class WriteLevel(PyMenu):
                                """
                                Parameter WriteLevel of value type str.
                                """
                                pass

                            class WriteCase(PyMenu):
                                """
                                Parameter WriteCase of value type str.
                                """
                                pass

                            class WriteMode(PyMenu):
                                """
                                Parameter WriteMode of value type str.
                                """
                                pass

                            class Surfaces(PyMenu):
                                """
                                Parameter Surfaces of value type List[str].
                                """
                                pass

                            class Fields(PyMenu):
                                """
                                Parameter Fields of value type List[str].
                                """
                                pass

                        class ConvergenceSettings(PyMenu):
                            """
                            Singleton ConvergenceSettings.
                            """
                            def __init__(self, service, rules, path):
                                self.OutputParamsPrevVals = self.__class__.OutputParamsPrevVals(service, rules, path + [("OutputParamsPrevVals", "")])
                                self.OutputParamsConvCutoff = self.__class__.OutputParamsConvCutoff(service, rules, path + [("OutputParamsConvCutoff", "")])
                                self.ConvCutoff = self.__class__.ConvCutoff(service, rules, path + [("ConvCutoff", "")])
                                super().__init__(service, rules, path)

                            class OutputParamsPrevVals(PyMenu):
                                """
                                Parameter OutputParamsPrevVals of value type int.
                                """
                                pass

                            class OutputParamsConvCutoff(PyMenu):
                                """
                                Parameter OutputParamsConvCutoff of value type float.
                                """
                                pass

                            class ConvCutoff(PyMenu):
                                """
                                Parameter ConvCutoff of value type float.
                                """
                                pass

                        class JournalsSettings(PyMenu):
                            """
                            Singleton JournalsSettings.
                            """
                            def __init__(self, service, rules, path):
                                self.RunJournalFile = self.__class__.RunJournalFile(service, rules, path + [("RunJournalFile", "")])
                                self.RunJournal = self.__class__.RunJournal(service, rules, path + [("RunJournal", "")])
                                self.DesignPointJournalFile = self.__class__.DesignPointJournalFile(service, rules, path + [("DesignPointJournalFile", "")])
                                self.InitializationJournal = self.__class__.InitializationJournal(service, rules, path + [("InitializationJournal", "")])
                                self.DesignPointJournal = self.__class__.DesignPointJournal(service, rules, path + [("DesignPointJournal", "")])
                                self.InitializationJournalFile = self.__class__.InitializationJournalFile(service, rules, path + [("InitializationJournalFile", "")])
                                super().__init__(service, rules, path)

                            class RunJournalFile(PyMenu):
                                """
                                Parameter RunJournalFile of value type str.
                                """
                                pass

                            class RunJournal(PyMenu):
                                """
                                Parameter RunJournal of value type str.
                                """
                                pass

                            class DesignPointJournalFile(PyMenu):
                                """
                                Parameter DesignPointJournalFile of value type str.
                                """
                                pass

                            class InitializationJournal(PyMenu):
                                """
                                Parameter InitializationJournal of value type str.
                                """
                                pass

                            class DesignPointJournal(PyMenu):
                                """
                                Parameter DesignPointJournal of value type str.
                                """
                                pass

                            class InitializationJournalFile(PyMenu):
                                """
                                Parameter InitializationJournalFile of value type str.
                                """
                                pass

                        class MaterialsSettings(PyMenu):
                            """
                            Singleton MaterialsSettings.
                            """
                            def __init__(self, service, rules, path):
                                self.FluidProperties = self.__class__.FluidProperties(service, rules, path + [("FluidProperties", "")])
                                super().__init__(service, rules, path)

                            class FluidProperties(PyMenu):
                                """
                                Parameter FluidProperties of value type str.
                                """
                                pass

                        class ParameterSearchSettings(PyMenu):
                            """
                            Singleton ParameterSearchSettings.
                            """
                            def __init__(self, service, rules, path):
                                self.InitializeBetweenCycles = self.__class__.InitializeBetweenCycles(service, rules, path + [("InitializeBetweenCycles", "")])
                                self.Method = self.__class__.Method(service, rules, path + [("Method", "")])
                                self.Cycles = self.__class__.Cycles(service, rules, path + [("Cycles", "")])
                                super().__init__(service, rules, path)

                            class InitializeBetweenCycles(PyMenu):
                                """
                                Parameter InitializeBetweenCycles of value type bool.
                                """
                                pass

                            class Method(PyMenu):
                                """
                                Parameter Method of value type str.
                                """
                                pass

                            class Cycles(PyMenu):
                                """
                                Parameter Cycles of value type int.
                                """
                                pass

                        class ModelsSettings(PyMenu):
                            """
                            Singleton ModelsSettings.
                            """
                            def __init__(self, service, rules, path):
                                self.TwoTempModel = self.__class__.TwoTempModel(service, rules, path + [("TwoTempModel", "")])
                                self.TransSSTRoughConst = self.__class__.TransSSTRoughConst(service, rules, path + [("TransSSTRoughConst", "")])
                                self.TurbulenceInflow = self.__class__.TurbulenceInflow(service, rules, path + [("TurbulenceInflow", "")])
                                self.TurbulenceModel = self.__class__.TurbulenceModel(service, rules, path + [("TurbulenceModel", "")])
                                super().__init__(service, rules, path)

                            class TwoTempModel(PyMenu):
                                """
                                Parameter TwoTempModel of value type str.
                                """
                                pass

                            class TransSSTRoughConst(PyMenu):
                                """
                                Parameter TransSSTRoughConst of value type float.
                                """
                                pass

                            class TurbulenceInflow(PyMenu):
                                """
                                Parameter TurbulenceInflow of value type str.
                                """
                                pass

                            class TurbulenceModel(PyMenu):
                                """
                                Parameter TurbulenceModel of value type str.
                                """
                                pass

                        class InitializationSettings(PyMenu):
                            """
                            Singleton InitializationSettings.
                            """
                            def __init__(self, service, rules, path):
                                self.InitializationMethod = self.__class__.InitializationMethod(service, rules, path + [("InitializationMethod", "")])
                                self.FMGAdvancedSettings = self.__class__.FMGAdvancedSettings(service, rules, path + [("FMGAdvancedSettings", "")])
                                self.InitializeBetweenDPs = self.__class__.InitializeBetweenDPs(service, rules, path + [("InitializeBetweenDPs", "")])
                                self.FMGCourantNumber = self.__class__.FMGCourantNumber(service, rules, path + [("FMGCourantNumber", "")])
                                super().__init__(service, rules, path)

                            class InitializationMethod(PyMenu):
                                """
                                Parameter InitializationMethod of value type str.
                                """
                                pass

                            class FMGAdvancedSettings(PyMenu):
                                """
                                Parameter FMGAdvancedSettings of value type bool.
                                """
                                pass

                            class InitializeBetweenDPs(PyMenu):
                                """
                                Parameter InitializeBetweenDPs of value type bool.
                                """
                                pass

                            class FMGCourantNumber(PyMenu):
                                """
                                Parameter FMGCourantNumber of value type float.
                                """
                                pass

                        class SolutionSettings(PyMenu):
                            """
                            Singleton SolutionSettings.
                            """
                            def __init__(self, service, rules, path):
                                self.AutoConvergenceStrategy = self.__class__.AutoConvergenceStrategy(service, rules, path + [("AutoConvergenceStrategy", "")])
                                self.SteeringCourantNumberMax = self.__class__.SteeringCourantNumberMax(service, rules, path + [("SteeringCourantNumberMax", "")])
                                self.SteeringBlending = self.__class__.SteeringBlending(service, rules, path + [("SteeringBlending", "")])
                                self.SteeringCourantNumberInitial = self.__class__.SteeringCourantNumberInitial(service, rules, path + [("SteeringCourantNumberInitial", "")])
                                self.SolverMethods = self.__class__.SolverMethods(service, rules, path + [("SolverMethods", "")])
                                self.CourantNumber = self.__class__.CourantNumber(service, rules, path + [("CourantNumber", "")])
                                self.SteeringRelaxation = self.__class__.SteeringRelaxation(service, rules, path + [("SteeringRelaxation", "")])
                                self.TimeScaleFactor = self.__class__.TimeScaleFactor(service, rules, path + [("TimeScaleFactor", "")])
                                self.SolutionControl = self.__class__.SolutionControl(service, rules, path + [("SolutionControl", "")])
                                self.Solver = self.__class__.Solver(service, rules, path + [("Solver", "")])
                                self.EnhancedCASM = self.__class__.EnhancedCASM(service, rules, path + [("EnhancedCASM", "")])
                                self.FlowRange = self.__class__.FlowRange(service, rules, path + [("FlowRange", "")])
                                super().__init__(service, rules, path)

                            class AutoConvergenceStrategy(PyMenu):
                                """
                                Parameter AutoConvergenceStrategy of value type str.
                                """
                                pass

                            class SteeringCourantNumberMax(PyMenu):
                                """
                                Parameter SteeringCourantNumberMax of value type float.
                                """
                                pass

                            class SteeringBlending(PyMenu):
                                """
                                Parameter SteeringBlending of value type float.
                                """
                                pass

                            class SteeringCourantNumberInitial(PyMenu):
                                """
                                Parameter SteeringCourantNumberInitial of value type float.
                                """
                                pass

                            class SolverMethods(PyMenu):
                                """
                                Parameter SolverMethods of value type str.
                                """
                                pass

                            class CourantNumber(PyMenu):
                                """
                                Parameter CourantNumber of value type float.
                                """
                                pass

                            class SteeringRelaxation(PyMenu):
                                """
                                Parameter SteeringRelaxation of value type float.
                                """
                                pass

                            class TimeScaleFactor(PyMenu):
                                """
                                Parameter TimeScaleFactor of value type float.
                                """
                                pass

                            class SolutionControl(PyMenu):
                                """
                                Parameter SolutionControl of value type str.
                                """
                                pass

                            class Solver(PyMenu):
                                """
                                Parameter Solver of value type str.
                                """
                                pass

                            class EnhancedCASM(PyMenu):
                                """
                                Parameter EnhancedCASM of value type bool.
                                """
                                pass

                            class FlowRange(PyMenu):
                                """
                                Parameter FlowRange of value type str.
                                """
                                pass

                        class ShowAdvanced(PyMenu):
                            """
                            Parameter ShowAdvanced of value type bool.
                            """
                            pass

                        class SolverType(PyMenu):
                            """
                            Parameter SolverType of value type str.
                            """
                            pass

                        class AeroCalculateDP(PyMenu):
                            """
                            Parameter AeroCalculateDP of value type str.
                            """
                            pass

                        class Iterations(PyMenu):
                            """
                            Parameter Iterations of value type int.
                            """
                            pass

                        class AeroRunNext(PyCommand):
                            """
                            AeroRunNext() -> bool
                            """
                            pass

                        class AeroInitializeAllDPs(PyCommand):
                            """
                            AeroInitializeAllDPs() -> bool
                            """
                            pass

                        class AeroApplySettingsSolver(PyCommand):
                            """
                            AeroApplySettingsSolver() -> bool
                            """
                            pass

                        class AeroApplySettingsConvergence(PyCommand):
                            """
                            AeroApplySettingsConvergence() -> bool
                            """
                            pass

                        class AeroInterrupt(PyCommand):
                            """
                            AeroInterrupt() -> bool
                            """
                            pass

                        class AeroCalculate(PyCommand):
                            """
                            AeroCalculate() -> bool
                            """
                            pass

                        class AeroInitializeCurrentDP(PyCommand):
                            """
                            AeroInitializeCurrentDP() -> bool
                            """
                            pass

                        class AeroSolveUseCaseSettings(PyCommand):
                            """
                            AeroSolveUseCaseSettings() -> bool
                            """
                            pass

                        class AeroContinue(PyCommand):
                            """
                            AeroContinue() -> bool
                            """
                            pass

                        class AeroSolveUseDefaultSettings(PyCommand):
                            """
                            AeroSolveUseDefaultSettings() -> bool
                            """
                            pass

                        class AeroSave(PyCommand):
                            """
                            AeroSave() -> bool
                            """
                            pass

                    class _name_(PyMenu):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                    class DP(PyMenu):
                        """
                        Parameter DP of value type int.
                        """
                        pass

                    class Status(PyMenu):
                        """
                        Parameter Status of value type str.
                        """
                        pass

                    class Converged(PyMenu):
                        """
                        Parameter Converged of value type str.
                        """
                        pass

                    class StatusBackup(PyMenu):
                        """
                        Parameter StatusBackup of value type str.
                        """
                        pass

                    class SaveStringFlag(PyMenu):
                        """
                        Parameter SaveStringFlag of value type bool.
                        """
                        pass

                def __getitem__(self, key: str) -> _DP:
                    return super().__getitem__(key)

            class RunType(PyMenu):
                """
                Singleton RunType.
                """
                def __init__(self, service, rules, path):
                    self.Airflow = self.__class__.Airflow(service, rules, path + [("Airflow", "")])
                    super().__init__(service, rules, path)

                class Airflow(PyMenu):
                    """
                    Parameter Airflow of value type bool.
                    """
                    pass

            class Airflow(PyMenu):
                """
                Singleton Airflow.
                """
                def __init__(self, service, rules, path):
                    self.General = self.__class__.General(service, rules, path + [("General", "")])
                    self.Conditions = self.__class__.Conditions(service, rules, path + [("Conditions", "")])
                    self.Fluent = self.__class__.Fluent(service, rules, path + [("Fluent", "")])
                    self.AirDirection = self.__class__.AirDirection(service, rules, path + [("AirDirection", "")])
                    self.Refresh = self.__class__.Refresh(service, rules, "Refresh", path)
                    super().__init__(service, rules, path)

                class General(PyMenu):
                    """
                    Singleton General.
                    """
                    def __init__(self, service, rules, path):
                        self.SolverType = self.__class__.SolverType(service, rules, path + [("SolverType", "")])
                        super().__init__(service, rules, path)

                    class SolverType(PyMenu):
                        """
                        Parameter SolverType of value type str.
                        """
                        pass

                class Conditions(PyMenu):
                    """
                    Singleton Conditions.
                    """
                    def __init__(self, service, rules, path):
                        self.AdiabaticStagnationTemperature = self.__class__.AdiabaticStagnationTemperature(service, rules, path + [("AdiabaticStagnationTemperature", "")])
                        self.Temperature = self.__class__.Temperature(service, rules, path + [("Temperature", "")])
                        self.Velocity = self.__class__.Velocity(service, rules, path + [("Velocity", "")])
                        self.SyncFluent = self.__class__.SyncFluent(service, rules, path + [("SyncFluent", "")])
                        self.Mach = self.__class__.Mach(service, rules, path + [("Mach", "")])
                        self.CharLen = self.__class__.CharLen(service, rules, path + [("CharLen", "")])
                        self.Reynolds = self.__class__.Reynolds(service, rules, path + [("Reynolds", "")])
                        self.Pressure = self.__class__.Pressure(service, rules, path + [("Pressure", "")])
                        self.OperatingPressure = self.__class__.OperatingPressure(service, rules, path + [("OperatingPressure", "")])
                        self.AbsolutePressure = self.__class__.AbsolutePressure(service, rules, path + [("AbsolutePressure", "")])
                        super().__init__(service, rules, path)

                    class AdiabaticStagnationTemperature(PyMenu):
                        """
                        Parameter AdiabaticStagnationTemperature of value type float.
                        """
                        pass

                    class Temperature(PyMenu):
                        """
                        Parameter Temperature of value type float.
                        """
                        pass

                    class Velocity(PyMenu):
                        """
                        Parameter Velocity of value type float.
                        """
                        pass

                    class SyncFluent(PyMenu):
                        """
                        Parameter SyncFluent of value type bool.
                        """
                        pass

                    class Mach(PyMenu):
                        """
                        Parameter Mach of value type float.
                        """
                        pass

                    class CharLen(PyMenu):
                        """
                        Parameter CharLen of value type float.
                        """
                        pass

                    class Reynolds(PyMenu):
                        """
                        Parameter Reynolds of value type float.
                        """
                        pass

                    class Pressure(PyMenu):
                        """
                        Parameter Pressure of value type float.
                        """
                        pass

                    class OperatingPressure(PyMenu):
                        """
                        Parameter OperatingPressure of value type float.
                        """
                        pass

                    class AbsolutePressure(PyMenu):
                        """
                        Parameter AbsolutePressure of value type float.
                        """
                        pass

                class Fluent(PyMenu):
                    """
                    Singleton Fluent.
                    """
                    def __init__(self, service, rules, path):
                        self.DiscretizationSchemes = self.__class__.DiscretizationSchemes(service, rules, path + [("DiscretizationSchemes", "")])
                        self.Materials = self.__class__.Materials(service, rules, path + [("Materials", "")])
                        self.Solver = self.__class__.Solver(service, rules, path + [("Solver", "")])
                        self.Models = self.__class__.Models(service, rules, path + [("Models", "")])
                        self.Refresh = self.__class__.Refresh(service, rules, "Refresh", path)
                        self.SetModel = self.__class__.SetModel(service, rules, "SetModel", path)
                        self.SetAir = self.__class__.SetAir(service, rules, "SetAir", path)
                        super().__init__(service, rules, path)

                    class DiscretizationSchemes(PyNamedObjectContainer):
                        class _DiscretizationSchemes(PyMenu):
                            """
                            Singleton _DiscretizationSchemes.
                            """
                            def __init__(self, service, rules, path):
                                self.DomainId = self.__class__.DomainId(service, rules, path + [("DomainId", "")])
                                self.AllowedValues = self.__class__.AllowedValues(service, rules, path + [("AllowedValues", "")])
                                self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                                self.Value = self.__class__.Value(service, rules, path + [("Value", "")])
                                self.InternalName = self.__class__.InternalName(service, rules, path + [("InternalName", "")])
                                super().__init__(service, rules, path)

                            class DomainId(PyMenu):
                                """
                                Parameter DomainId of value type int.
                                """
                                pass

                            class AllowedValues(PyMenu):
                                """
                                Parameter AllowedValues of value type List[str].
                                """
                                pass

                            class _name_(PyMenu):
                                """
                                Parameter _name_ of value type str.
                                """
                                pass

                            class Value(PyMenu):
                                """
                                Parameter Value of value type str.
                                """
                                pass

                            class InternalName(PyMenu):
                                """
                                Parameter InternalName of value type str.
                                """
                                pass

                        def __getitem__(self, key: str) -> _DiscretizationSchemes:
                            return super().__getitem__(key)

                    class Materials(PyMenu):
                        """
                        Singleton Materials.
                        """
                        def __init__(self, service, rules, path):
                            self.AirThermalConductivityConstant = self.__class__.AirThermalConductivityConstant(service, rules, path + [("AirThermalConductivityConstant", "")])
                            self.SettingsSync = self.__class__.SettingsSync(service, rules, path + [("SettingsSync", "")])
                            self.AirDensity = self.__class__.AirDensity(service, rules, path + [("AirDensity", "")])
                            self.AirThermalConductivity = self.__class__.AirThermalConductivity(service, rules, path + [("AirThermalConductivity", "")])
                            self.AirDensityConstant = self.__class__.AirDensityConstant(service, rules, path + [("AirDensityConstant", "")])
                            self.AirViscosityConstant = self.__class__.AirViscosityConstant(service, rules, path + [("AirViscosityConstant", "")])
                            self.AirCp = self.__class__.AirCp(service, rules, path + [("AirCp", "")])
                            self.AirCpConstant = self.__class__.AirCpConstant(service, rules, path + [("AirCpConstant", "")])
                            self.AirViscosity = self.__class__.AirViscosity(service, rules, path + [("AirViscosity", "")])
                            super().__init__(service, rules, path)

                        class AirThermalConductivityConstant(PyMenu):
                            """
                            Parameter AirThermalConductivityConstant of value type float.
                            """
                            pass

                        class SettingsSync(PyMenu):
                            """
                            Parameter SettingsSync of value type str.
                            """
                            pass

                        class AirDensity(PyMenu):
                            """
                            Parameter AirDensity of value type str.
                            """
                            pass

                        class AirThermalConductivity(PyMenu):
                            """
                            Parameter AirThermalConductivity of value type str.
                            """
                            pass

                        class AirDensityConstant(PyMenu):
                            """
                            Parameter AirDensityConstant of value type float.
                            """
                            pass

                        class AirViscosityConstant(PyMenu):
                            """
                            Parameter AirViscosityConstant of value type float.
                            """
                            pass

                        class AirCp(PyMenu):
                            """
                            Parameter AirCp of value type str.
                            """
                            pass

                        class AirCpConstant(PyMenu):
                            """
                            Parameter AirCpConstant of value type float.
                            """
                            pass

                        class AirViscosity(PyMenu):
                            """
                            Parameter AirViscosity of value type str.
                            """
                            pass

                    class Solver(PyMenu):
                        """
                        Singleton Solver.
                        """
                        def __init__(self, service, rules, path):
                            self.SolverType = self.__class__.SolverType(service, rules, path + [("SolverType", "")])
                            super().__init__(service, rules, path)

                        class SolverType(PyMenu):
                            """
                            Parameter SolverType of value type str.
                            """
                            pass

                    class Models(PyMenu):
                        """
                        Singleton Models.
                        """
                        def __init__(self, service, rules, path):
                            self.ViscousHeating = self.__class__.ViscousHeating(service, rules, path + [("ViscousHeating", "")])
                            self.ProductionLimiter = self.__class__.ProductionLimiter(service, rules, path + [("ProductionLimiter", "")])
                            self.TransitionSSTRoughnessConstant = self.__class__.TransitionSSTRoughnessConstant(service, rules, path + [("TransitionSSTRoughnessConstant", "")])
                            self.KwModel = self.__class__.KwModel(service, rules, path + [("KwModel", "")])
                            self.Energy = self.__class__.Energy(service, rules, path + [("Energy", "")])
                            self.TransitionSSTRoughnessCorrelation = self.__class__.TransitionSSTRoughnessCorrelation(service, rules, path + [("TransitionSSTRoughnessCorrelation", "")])
                            self.Turbulence = self.__class__.Turbulence(service, rules, path + [("Turbulence", "")])
                            super().__init__(service, rules, path)

                        class ViscousHeating(PyMenu):
                            """
                            Parameter ViscousHeating of value type bool.
                            """
                            pass

                        class ProductionLimiter(PyMenu):
                            """
                            Parameter ProductionLimiter of value type bool.
                            """
                            pass

                        class TransitionSSTRoughnessConstant(PyMenu):
                            """
                            Parameter TransitionSSTRoughnessConstant of value type float.
                            """
                            pass

                        class KwModel(PyMenu):
                            """
                            Parameter KwModel of value type str.
                            """
                            pass

                        class Energy(PyMenu):
                            """
                            Parameter Energy of value type bool.
                            """
                            pass

                        class TransitionSSTRoughnessCorrelation(PyMenu):
                            """
                            Parameter TransitionSSTRoughnessCorrelation of value type bool.
                            """
                            pass

                        class Turbulence(PyMenu):
                            """
                            Parameter Turbulence of value type str.
                            """
                            pass

                    class Refresh(PyCommand):
                        """
                        Refresh() -> bool
                        """
                        pass

                    class SetModel(PyCommand):
                        """
                        SetModel() -> bool
                        """
                        pass

                    class SetAir(PyCommand):
                        """
                        SetAir() -> bool
                        """
                        pass

                class AirDirection(PyMenu):
                    """
                    Singleton AirDirection.
                    """
                    def __init__(self, service, rules, path):
                        self.Magnitude = self.__class__.Magnitude(service, rules, path + [("Magnitude", "")])
                        self.VelocityY = self.__class__.VelocityY(service, rules, path + [("VelocityY", "")])
                        self.Mode = self.__class__.Mode(service, rules, path + [("Mode", "")])
                        self.VelocityZ = self.__class__.VelocityZ(service, rules, path + [("VelocityZ", "")])
                        self.Alpha = self.__class__.Alpha(service, rules, path + [("Alpha", "")])
                        self.VelocityX = self.__class__.VelocityX(service, rules, path + [("VelocityX", "")])
                        self.DragDir = self.__class__.DragDir(service, rules, path + [("DragDir", "")])
                        self.LiftDir = self.__class__.LiftDir(service, rules, path + [("LiftDir", "")])
                        self.Beta = self.__class__.Beta(service, rules, path + [("Beta", "")])
                        super().__init__(service, rules, path)

                    class Magnitude(PyMenu):
                        """
                        Parameter Magnitude of value type float.
                        """
                        pass

                    class VelocityY(PyMenu):
                        """
                        Parameter VelocityY of value type float.
                        """
                        pass

                    class Mode(PyMenu):
                        """
                        Parameter Mode of value type str.
                        """
                        pass

                    class VelocityZ(PyMenu):
                        """
                        Parameter VelocityZ of value type float.
                        """
                        pass

                    class Alpha(PyMenu):
                        """
                        Parameter Alpha of value type float.
                        """
                        pass

                    class VelocityX(PyMenu):
                        """
                        Parameter VelocityX of value type float.
                        """
                        pass

                    class DragDir(PyMenu):
                        """
                        Parameter DragDir of value type str.
                        """
                        pass

                    class LiftDir(PyMenu):
                        """
                        Parameter LiftDir of value type str.
                        """
                        pass

                    class Beta(PyMenu):
                        """
                        Parameter Beta of value type float.
                        """
                        pass

                class Refresh(PyCommand):
                    """
                    Refresh() -> bool
                    """
                    pass

            class Solution(PyMenu):
                """
                Singleton Solution.
                """
                def __init__(self, service, rules, path):
                    self.RunState = self.__class__.RunState(service, rules, path + [("RunState", "")])
                    self.AirflowRun = self.__class__.AirflowRun(service, rules, path + [("AirflowRun", "")])
                    self.GlobalSettings = self.__class__.GlobalSettings(service, rules, path + [("GlobalSettings", "")])
                    super().__init__(service, rules, path)

                class RunState(PyMenu):
                    """
                    Singleton RunState.
                    """
                    def __init__(self, service, rules, path):
                        self.ClientProcessRunning = self.__class__.ClientProcessRunning(service, rules, path + [("ClientProcessRunning", "")])
                        self.ProjectRunIterator = self.__class__.ProjectRunIterator(service, rules, path + [("ProjectRunIterator", "")])
                        self.CurrentStep = self.__class__.CurrentStep(service, rules, path + [("CurrentStep", "")])
                        super().__init__(service, rules, path)

                    class ClientProcessRunning(PyMenu):
                        """
                        Parameter ClientProcessRunning of value type bool.
                        """
                        pass

                    class ProjectRunIterator(PyMenu):
                        """
                        Parameter ProjectRunIterator of value type int.
                        """
                        pass

                    class CurrentStep(PyMenu):
                        """
                        Parameter CurrentStep of value type str.
                        """
                        pass

                class AirflowRun(PyMenu):
                    """
                    Singleton AirflowRun.
                    """
                    def __init__(self, service, rules, path):
                        self.FluentTimeIntegration = self.__class__.FluentTimeIntegration(service, rules, path + [("FluentTimeIntegration", "")])
                        self.AirflowFluentOutputSolution = self.__class__.AirflowFluentOutputSolution(service, rules, path + [("AirflowFluentOutputSolution", "")])
                        self.SolutionAvailable = self.__class__.SolutionAvailable(service, rules, path + [("SolutionAvailable", "")])
                        self.ConvergenceAvailable = self.__class__.ConvergenceAvailable(service, rules, path + [("ConvergenceAvailable", "")])
                        self.Initialize = self.__class__.Initialize(service, rules, "Initialize", path)
                        self.SaveAs = self.__class__.SaveAs(service, rules, "SaveAs", path)
                        self.Interrupt = self.__class__.Interrupt(service, rules, "Interrupt", path)
                        self.Reset = self.__class__.Reset(service, rules, "Reset", path)
                        self.Load = self.__class__.Load(service, rules, "Load", path)
                        self.Save = self.__class__.Save(service, rules, "Save", path)
                        self.Calculate = self.__class__.Calculate(service, rules, "Calculate", path)
                        super().__init__(service, rules, path)

                    class FluentTimeIntegration(PyMenu):
                        """
                        Singleton FluentTimeIntegration.
                        """
                        def __init__(self, service, rules, path):
                            self.TimeTotal = self.__class__.TimeTotal(service, rules, path + [("TimeTotal", "")])
                            self.TimeStep = self.__class__.TimeStep(service, rules, path + [("TimeStep", "")])
                            self.CourantNumber = self.__class__.CourantNumber(service, rules, path + [("CourantNumber", "")])
                            self.SteeringBlending = self.__class__.SteeringBlending(service, rules, path + [("SteeringBlending", "")])
                            self.SolutionControl = self.__class__.SolutionControl(service, rules, path + [("SolutionControl", "")])
                            self.NumIterations = self.__class__.NumIterations(service, rules, path + [("NumIterations", "")])
                            self.SteeringCourantNumberMax = self.__class__.SteeringCourantNumberMax(service, rules, path + [("SteeringCourantNumberMax", "")])
                            self.TimeScaleFactor = self.__class__.TimeScaleFactor(service, rules, path + [("TimeScaleFactor", "")])
                            self.TimeOrder = self.__class__.TimeOrder(service, rules, path + [("TimeOrder", "")])
                            self.SteeringCourantNumberInitial = self.__class__.SteeringCourantNumberInitial(service, rules, path + [("SteeringCourantNumberInitial", "")])
                            self.SteeringRelaxation = self.__class__.SteeringRelaxation(service, rules, path + [("SteeringRelaxation", "")])
                            super().__init__(service, rules, path)

                        class TimeTotal(PyMenu):
                            """
                            Parameter TimeTotal of value type float.
                            """
                            pass

                        class TimeStep(PyMenu):
                            """
                            Parameter TimeStep of value type float.
                            """
                            pass

                        class CourantNumber(PyMenu):
                            """
                            Parameter CourantNumber of value type float.
                            """
                            pass

                        class SteeringBlending(PyMenu):
                            """
                            Parameter SteeringBlending of value type float.
                            """
                            pass

                        class SolutionControl(PyMenu):
                            """
                            Parameter SolutionControl of value type str.
                            """
                            pass

                        class NumIterations(PyMenu):
                            """
                            Parameter NumIterations of value type int.
                            """
                            pass

                        class SteeringCourantNumberMax(PyMenu):
                            """
                            Parameter SteeringCourantNumberMax of value type float.
                            """
                            pass

                        class TimeScaleFactor(PyMenu):
                            """
                            Parameter TimeScaleFactor of value type float.
                            """
                            pass

                        class TimeOrder(PyMenu):
                            """
                            Parameter TimeOrder of value type str.
                            """
                            pass

                        class SteeringCourantNumberInitial(PyMenu):
                            """
                            Parameter SteeringCourantNumberInitial of value type float.
                            """
                            pass

                        class SteeringRelaxation(PyMenu):
                            """
                            Parameter SteeringRelaxation of value type float.
                            """
                            pass

                    class AirflowFluentOutputSolution(PyMenu):
                        """
                        Singleton AirflowFluentOutputSolution.
                        """
                        def __init__(self, service, rules, path):
                            self.Loaded = self.__class__.Loaded(service, rules, path + [("Loaded", "")])
                            self.Filename = self.__class__.Filename(service, rules, path + [("Filename", "")])
                            super().__init__(service, rules, path)

                        class Loaded(PyMenu):
                            """
                            Parameter Loaded of value type bool.
                            """
                            pass

                        class Filename(PyMenu):
                            """
                            Parameter Filename of value type str.
                            """
                            pass

                    class SolutionAvailable(PyMenu):
                        """
                        Parameter SolutionAvailable of value type bool.
                        """
                        pass

                    class ConvergenceAvailable(PyMenu):
                        """
                        Parameter ConvergenceAvailable of value type bool.
                        """
                        pass

                    class Initialize(PyCommand):
                        """
                        Initialize() -> bool
                        """
                        pass

                    class SaveAs(PyCommand):
                        """
                        SaveAs(Filename: str) -> bool
                        """
                        pass

                    class Interrupt(PyCommand):
                        """
                        Interrupt() -> bool
                        """
                        pass

                    class Reset(PyCommand):
                        """
                        Reset() -> bool
                        """
                        pass

                    class Load(PyCommand):
                        """
                        Load(Filename: str) -> bool
                        """
                        pass

                    class Save(PyCommand):
                        """
                        Save(Filename: str) -> bool
                        """
                        pass

                    class Calculate(PyCommand):
                        """
                        Calculate() -> bool
                        """
                        pass

                class GlobalSettings(PyMenu):
                    """
                    Singleton GlobalSettings.
                    """
                    def __init__(self, service, rules, path):
                        self.MonitorMode = self.__class__.MonitorMode(service, rules, path + [("MonitorMode", "")])
                        self.AutoSave = self.__class__.AutoSave(service, rules, path + [("AutoSave", "")])
                        super().__init__(service, rules, path)

                    class MonitorMode(PyMenu):
                        """
                        Parameter MonitorMode of value type str.
                        """
                        pass

                    class AutoSave(PyMenu):
                        """
                        Parameter AutoSave of value type bool.
                        """
                        pass

            class AeroWorkflow(PyMenu):
                """
                Singleton AeroWorkflow.
                """
                def __init__(self, service, rules, path):
                    self.Solution = self.__class__.Solution(service, rules, path + [("Solution", "")])
                    self.Setup = self.__class__.Setup(service, rules, path + [("Setup", "")])
                    self.AeroFlags = self.__class__.AeroFlags(service, rules, path + [("AeroFlags", "")])
                    self.Results = self.__class__.Results(service, rules, path + [("Results", "")])
                    self.AeroGetOutParam = self.__class__.AeroGetOutParam(service, rules, "AeroGetOutParam", path)
                    super().__init__(service, rules, path)

                class Solution(PyMenu):
                    """
                    Singleton Solution.
                    """
                    def __init__(self, service, rules, path):
                        self.Solve = self.__class__.Solve(service, rules, path + [("Solve", "")])
                        super().__init__(service, rules, path)

                    class Solve(PyMenu):
                        """
                        Singleton Solve.
                        """
                        def __init__(self, service, rules, path):
                            self.InitializationSettings = self.__class__.InitializationSettings(service, rules, path + [("InitializationSettings", "")])
                            self.SolutionSettings = self.__class__.SolutionSettings(service, rules, path + [("SolutionSettings", "")])
                            self.MaterialsSettings = self.__class__.MaterialsSettings(service, rules, path + [("MaterialsSettings", "")])
                            self.FluentCFFPost = self.__class__.FluentCFFPost(service, rules, path + [("FluentCFFPost", "")])
                            self.ModelsSettings = self.__class__.ModelsSettings(service, rules, path + [("ModelsSettings", "")])
                            self.ConvergenceSettings = self.__class__.ConvergenceSettings(service, rules, path + [("ConvergenceSettings", "")])
                            self.JournalsSettings = self.__class__.JournalsSettings(service, rules, path + [("JournalsSettings", "")])
                            self.ParameterSearchSettings = self.__class__.ParameterSearchSettings(service, rules, path + [("ParameterSearchSettings", "")])
                            self.ShowAdvanced = self.__class__.ShowAdvanced(service, rules, path + [("ShowAdvanced", "")])
                            self.AeroCalculateDP = self.__class__.AeroCalculateDP(service, rules, path + [("AeroCalculateDP", "")])
                            self.Iterations = self.__class__.Iterations(service, rules, path + [("Iterations", "")])
                            self.SolverType = self.__class__.SolverType(service, rules, path + [("SolverType", "")])
                            self.AeroInitializeAllDPs = self.__class__.AeroInitializeAllDPs(service, rules, "AeroInitializeAllDPs", path)
                            self.AeroRunNext = self.__class__.AeroRunNext(service, rules, "AeroRunNext", path)
                            self.AeroCalculate = self.__class__.AeroCalculate(service, rules, "AeroCalculate", path)
                            self.AeroSolveUseCaseSettings = self.__class__.AeroSolveUseCaseSettings(service, rules, "AeroSolveUseCaseSettings", path)
                            self.AeroInterrupt = self.__class__.AeroInterrupt(service, rules, "AeroInterrupt", path)
                            self.AeroContinue = self.__class__.AeroContinue(service, rules, "AeroContinue", path)
                            self.AeroApplySettingsConvergence = self.__class__.AeroApplySettingsConvergence(service, rules, "AeroApplySettingsConvergence", path)
                            self.AeroSolveUseDefaultSettings = self.__class__.AeroSolveUseDefaultSettings(service, rules, "AeroSolveUseDefaultSettings", path)
                            self.AeroSave = self.__class__.AeroSave(service, rules, "AeroSave", path)
                            self.AeroInitializeCurrentDP = self.__class__.AeroInitializeCurrentDP(service, rules, "AeroInitializeCurrentDP", path)
                            self.AeroApplySettingsSolver = self.__class__.AeroApplySettingsSolver(service, rules, "AeroApplySettingsSolver", path)
                            super().__init__(service, rules, path)

                        class InitializationSettings(PyMenu):
                            """
                            Singleton InitializationSettings.
                            """
                            def __init__(self, service, rules, path):
                                self.InitializationMethod = self.__class__.InitializationMethod(service, rules, path + [("InitializationMethod", "")])
                                self.FMGAdvancedSettings = self.__class__.FMGAdvancedSettings(service, rules, path + [("FMGAdvancedSettings", "")])
                                self.FMGCourantNumber = self.__class__.FMGCourantNumber(service, rules, path + [("FMGCourantNumber", "")])
                                self.InitializeBetweenDPs = self.__class__.InitializeBetweenDPs(service, rules, path + [("InitializeBetweenDPs", "")])
                                super().__init__(service, rules, path)

                            class InitializationMethod(PyMenu):
                                """
                                Parameter InitializationMethod of value type str.
                                """
                                pass

                            class FMGAdvancedSettings(PyMenu):
                                """
                                Parameter FMGAdvancedSettings of value type bool.
                                """
                                pass

                            class FMGCourantNumber(PyMenu):
                                """
                                Parameter FMGCourantNumber of value type float.
                                """
                                pass

                            class InitializeBetweenDPs(PyMenu):
                                """
                                Parameter InitializeBetweenDPs of value type bool.
                                """
                                pass

                        class SolutionSettings(PyMenu):
                            """
                            Singleton SolutionSettings.
                            """
                            def __init__(self, service, rules, path):
                                self.AutoConvergenceStrategy = self.__class__.AutoConvergenceStrategy(service, rules, path + [("AutoConvergenceStrategy", "")])
                                self.Solver = self.__class__.Solver(service, rules, path + [("Solver", "")])
                                self.SteeringBlending = self.__class__.SteeringBlending(service, rules, path + [("SteeringBlending", "")])
                                self.CourantNumber = self.__class__.CourantNumber(service, rules, path + [("CourantNumber", "")])
                                self.EnhancedCASM = self.__class__.EnhancedCASM(service, rules, path + [("EnhancedCASM", "")])
                                self.SteeringCourantNumberMax = self.__class__.SteeringCourantNumberMax(service, rules, path + [("SteeringCourantNumberMax", "")])
                                self.SteeringCourantNumberInitial = self.__class__.SteeringCourantNumberInitial(service, rules, path + [("SteeringCourantNumberInitial", "")])
                                self.FlowRange = self.__class__.FlowRange(service, rules, path + [("FlowRange", "")])
                                self.SolutionControl = self.__class__.SolutionControl(service, rules, path + [("SolutionControl", "")])
                                self.SteeringRelaxation = self.__class__.SteeringRelaxation(service, rules, path + [("SteeringRelaxation", "")])
                                self.TimeScaleFactor = self.__class__.TimeScaleFactor(service, rules, path + [("TimeScaleFactor", "")])
                                self.SolverMethods = self.__class__.SolverMethods(service, rules, path + [("SolverMethods", "")])
                                super().__init__(service, rules, path)

                            class AutoConvergenceStrategy(PyMenu):
                                """
                                Parameter AutoConvergenceStrategy of value type str.
                                """
                                pass

                            class Solver(PyMenu):
                                """
                                Parameter Solver of value type str.
                                """
                                pass

                            class SteeringBlending(PyMenu):
                                """
                                Parameter SteeringBlending of value type float.
                                """
                                pass

                            class CourantNumber(PyMenu):
                                """
                                Parameter CourantNumber of value type float.
                                """
                                pass

                            class EnhancedCASM(PyMenu):
                                """
                                Parameter EnhancedCASM of value type bool.
                                """
                                pass

                            class SteeringCourantNumberMax(PyMenu):
                                """
                                Parameter SteeringCourantNumberMax of value type float.
                                """
                                pass

                            class SteeringCourantNumberInitial(PyMenu):
                                """
                                Parameter SteeringCourantNumberInitial of value type float.
                                """
                                pass

                            class FlowRange(PyMenu):
                                """
                                Parameter FlowRange of value type str.
                                """
                                pass

                            class SolutionControl(PyMenu):
                                """
                                Parameter SolutionControl of value type str.
                                """
                                pass

                            class SteeringRelaxation(PyMenu):
                                """
                                Parameter SteeringRelaxation of value type float.
                                """
                                pass

                            class TimeScaleFactor(PyMenu):
                                """
                                Parameter TimeScaleFactor of value type float.
                                """
                                pass

                            class SolverMethods(PyMenu):
                                """
                                Parameter SolverMethods of value type str.
                                """
                                pass

                        class MaterialsSettings(PyMenu):
                            """
                            Singleton MaterialsSettings.
                            """
                            def __init__(self, service, rules, path):
                                self.FluidProperties = self.__class__.FluidProperties(service, rules, path + [("FluidProperties", "")])
                                super().__init__(service, rules, path)

                            class FluidProperties(PyMenu):
                                """
                                Parameter FluidProperties of value type str.
                                """
                                pass

                        class FluentCFFPost(PyMenu):
                            """
                            Singleton FluentCFFPost.
                            """
                            def __init__(self, service, rules, path):
                                self.Fields = self.__class__.Fields(service, rules, path + [("Fields", "")])
                                self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                                self.WriteCase = self.__class__.WriteCase(service, rules, path + [("WriteCase", "")])
                                self.ZoneType = self.__class__.ZoneType(service, rules, path + [("ZoneType", "")])
                                self.WriteMode = self.__class__.WriteMode(service, rules, path + [("WriteMode", "")])
                                self.WriteLevel = self.__class__.WriteLevel(service, rules, path + [("WriteLevel", "")])
                                self.ReadOnly = self.__class__.ReadOnly(service, rules, path + [("ReadOnly", "")])
                                super().__init__(service, rules, path)

                            class Fields(PyMenu):
                                """
                                Parameter Fields of value type List[str].
                                """
                                pass

                            class Surfaces(PyMenu):
                                """
                                Parameter Surfaces of value type List[str].
                                """
                                pass

                            class WriteCase(PyMenu):
                                """
                                Parameter WriteCase of value type str.
                                """
                                pass

                            class ZoneType(PyMenu):
                                """
                                Parameter ZoneType of value type str.
                                """
                                pass

                            class WriteMode(PyMenu):
                                """
                                Parameter WriteMode of value type str.
                                """
                                pass

                            class WriteLevel(PyMenu):
                                """
                                Parameter WriteLevel of value type str.
                                """
                                pass

                            class ReadOnly(PyMenu):
                                """
                                Parameter ReadOnly of value type bool.
                                """
                                pass

                        class ModelsSettings(PyMenu):
                            """
                            Singleton ModelsSettings.
                            """
                            def __init__(self, service, rules, path):
                                self.TurbulenceInflow = self.__class__.TurbulenceInflow(service, rules, path + [("TurbulenceInflow", "")])
                                self.TurbulenceModel = self.__class__.TurbulenceModel(service, rules, path + [("TurbulenceModel", "")])
                                self.TwoTempModel = self.__class__.TwoTempModel(service, rules, path + [("TwoTempModel", "")])
                                self.TransSSTRoughConst = self.__class__.TransSSTRoughConst(service, rules, path + [("TransSSTRoughConst", "")])
                                super().__init__(service, rules, path)

                            class TurbulenceInflow(PyMenu):
                                """
                                Parameter TurbulenceInflow of value type str.
                                """
                                pass

                            class TurbulenceModel(PyMenu):
                                """
                                Parameter TurbulenceModel of value type str.
                                """
                                pass

                            class TwoTempModel(PyMenu):
                                """
                                Parameter TwoTempModel of value type str.
                                """
                                pass

                            class TransSSTRoughConst(PyMenu):
                                """
                                Parameter TransSSTRoughConst of value type float.
                                """
                                pass

                        class ConvergenceSettings(PyMenu):
                            """
                            Singleton ConvergenceSettings.
                            """
                            def __init__(self, service, rules, path):
                                self.ConvCutoff = self.__class__.ConvCutoff(service, rules, path + [("ConvCutoff", "")])
                                self.OutputParamsConvCutoff = self.__class__.OutputParamsConvCutoff(service, rules, path + [("OutputParamsConvCutoff", "")])
                                self.OutputParamsPrevVals = self.__class__.OutputParamsPrevVals(service, rules, path + [("OutputParamsPrevVals", "")])
                                super().__init__(service, rules, path)

                            class ConvCutoff(PyMenu):
                                """
                                Parameter ConvCutoff of value type float.
                                """
                                pass

                            class OutputParamsConvCutoff(PyMenu):
                                """
                                Parameter OutputParamsConvCutoff of value type float.
                                """
                                pass

                            class OutputParamsPrevVals(PyMenu):
                                """
                                Parameter OutputParamsPrevVals of value type int.
                                """
                                pass

                        class JournalsSettings(PyMenu):
                            """
                            Singleton JournalsSettings.
                            """
                            def __init__(self, service, rules, path):
                                self.RunJournalFile = self.__class__.RunJournalFile(service, rules, path + [("RunJournalFile", "")])
                                self.DesignPointJournal = self.__class__.DesignPointJournal(service, rules, path + [("DesignPointJournal", "")])
                                self.RunJournal = self.__class__.RunJournal(service, rules, path + [("RunJournal", "")])
                                self.DesignPointJournalFile = self.__class__.DesignPointJournalFile(service, rules, path + [("DesignPointJournalFile", "")])
                                self.InitializationJournal = self.__class__.InitializationJournal(service, rules, path + [("InitializationJournal", "")])
                                self.InitializationJournalFile = self.__class__.InitializationJournalFile(service, rules, path + [("InitializationJournalFile", "")])
                                super().__init__(service, rules, path)

                            class RunJournalFile(PyMenu):
                                """
                                Parameter RunJournalFile of value type str.
                                """
                                pass

                            class DesignPointJournal(PyMenu):
                                """
                                Parameter DesignPointJournal of value type str.
                                """
                                pass

                            class RunJournal(PyMenu):
                                """
                                Parameter RunJournal of value type str.
                                """
                                pass

                            class DesignPointJournalFile(PyMenu):
                                """
                                Parameter DesignPointJournalFile of value type str.
                                """
                                pass

                            class InitializationJournal(PyMenu):
                                """
                                Parameter InitializationJournal of value type str.
                                """
                                pass

                            class InitializationJournalFile(PyMenu):
                                """
                                Parameter InitializationJournalFile of value type str.
                                """
                                pass

                        class ParameterSearchSettings(PyMenu):
                            """
                            Singleton ParameterSearchSettings.
                            """
                            def __init__(self, service, rules, path):
                                self.InitializeBetweenCycles = self.__class__.InitializeBetweenCycles(service, rules, path + [("InitializeBetweenCycles", "")])
                                self.Method = self.__class__.Method(service, rules, path + [("Method", "")])
                                self.Cycles = self.__class__.Cycles(service, rules, path + [("Cycles", "")])
                                super().__init__(service, rules, path)

                            class InitializeBetweenCycles(PyMenu):
                                """
                                Parameter InitializeBetweenCycles of value type bool.
                                """
                                pass

                            class Method(PyMenu):
                                """
                                Parameter Method of value type str.
                                """
                                pass

                            class Cycles(PyMenu):
                                """
                                Parameter Cycles of value type int.
                                """
                                pass

                        class ShowAdvanced(PyMenu):
                            """
                            Parameter ShowAdvanced of value type bool.
                            """
                            pass

                        class AeroCalculateDP(PyMenu):
                            """
                            Parameter AeroCalculateDP of value type str.
                            """
                            pass

                        class Iterations(PyMenu):
                            """
                            Parameter Iterations of value type int.
                            """
                            pass

                        class SolverType(PyMenu):
                            """
                            Parameter SolverType of value type str.
                            """
                            pass

                        class AeroInitializeAllDPs(PyCommand):
                            """
                            AeroInitializeAllDPs() -> bool
                            """
                            pass

                        class AeroRunNext(PyCommand):
                            """
                            AeroRunNext() -> bool
                            """
                            pass

                        class AeroCalculate(PyCommand):
                            """
                            AeroCalculate() -> bool
                            """
                            pass

                        class AeroSolveUseCaseSettings(PyCommand):
                            """
                            AeroSolveUseCaseSettings() -> bool
                            """
                            pass

                        class AeroInterrupt(PyCommand):
                            """
                            AeroInterrupt() -> bool
                            """
                            pass

                        class AeroContinue(PyCommand):
                            """
                            AeroContinue() -> bool
                            """
                            pass

                        class AeroApplySettingsConvergence(PyCommand):
                            """
                            AeroApplySettingsConvergence() -> bool
                            """
                            pass

                        class AeroSolveUseDefaultSettings(PyCommand):
                            """
                            AeroSolveUseDefaultSettings() -> bool
                            """
                            pass

                        class AeroSave(PyCommand):
                            """
                            AeroSave() -> bool
                            """
                            pass

                        class AeroInitializeCurrentDP(PyCommand):
                            """
                            AeroInitializeCurrentDP() -> bool
                            """
                            pass

                        class AeroApplySettingsSolver(PyCommand):
                            """
                            AeroApplySettingsSolver() -> bool
                            """
                            pass

                class Setup(PyMenu):
                    """
                    Singleton Setup.
                    """
                    def __init__(self, service, rules, path):
                        self.ComponentGroups = self.__class__.ComponentGroups(service, rules, path + [("ComponentGroups", "")])
                        self.SimulationConditions = self.__class__.SimulationConditions(service, rules, path + [("SimulationConditions", "")])
                        self.GeometricProperties = self.__class__.GeometricProperties(service, rules, path + [("GeometricProperties", "")])
                        self.AdvancedWorkflows = self.__class__.AdvancedWorkflows(service, rules, path + [("AdvancedWorkflows", "")])
                        self.ParameterSearch = self.__class__.ParameterSearch(service, rules, path + [("ParameterSearch", "")])
                        super().__init__(service, rules, path)

                    class ComponentGroups(PyMenu):
                        """
                        Singleton ComponentGroups.
                        """
                        def __init__(self, service, rules, path):
                            self.ComponentList = self.__class__.ComponentList(service, rules, path + [("ComponentList", "")])
                            self.OutputComponentList = self.__class__.OutputComponentList(service, rules, path + [("OutputComponentList", "")])
                            self.MonitorComponentList = self.__class__.MonitorComponentList(service, rules, path + [("MonitorComponentList", "")])
                            self.ComponentOutputList = self.__class__.ComponentOutputList(service, rules, path + [("ComponentOutputList", "")])
                            self.ComponentMonitorList = self.__class__.ComponentMonitorList(service, rules, path + [("ComponentMonitorList", "")])
                            self.DeleteComponentGroup = self.__class__.DeleteComponentGroup(service, rules, "DeleteComponentGroup", path)
                            self.RenameComponentGroup = self.__class__.RenameComponentGroup(service, rules, "RenameComponentGroup", path)
                            self.CreateComponentGroup = self.__class__.CreateComponentGroup(service, rules, "CreateComponentGroup", path)
                            self.RemoveFromComponentGroup = self.__class__.RemoveFromComponentGroup(service, rules, "RemoveFromComponentGroup", path)
                            self.AddToComponentGroup = self.__class__.AddToComponentGroup(service, rules, "AddToComponentGroup", path)
                            super().__init__(service, rules, path)

                        class ComponentList(PyMenu):
                            """
                            Parameter ComponentList of value type List[str].
                            """
                            pass

                        class OutputComponentList(PyMenu):
                            """
                            Parameter OutputComponentList of value type List[str].
                            """
                            pass

                        class MonitorComponentList(PyMenu):
                            """
                            Parameter MonitorComponentList of value type List[str].
                            """
                            pass

                        class ComponentOutputList(PyMenu):
                            """
                            Parameter ComponentOutputList of value type List[str].
                            """
                            pass

                        class ComponentMonitorList(PyMenu):
                            """
                            Parameter ComponentMonitorList of value type List[str].
                            """
                            pass

                        class DeleteComponentGroup(PyCommand):
                            """
                            DeleteComponentGroup(GroupName: str) -> bool
                            """
                            pass

                        class RenameComponentGroup(PyCommand):
                            """
                            RenameComponentGroup(CurrentGroupName: str, NewGroupName: str) -> bool
                            """
                            pass

                        class CreateComponentGroup(PyCommand):
                            """
                            CreateComponentGroup(Group: str) -> bool
                            """
                            pass

                        class RemoveFromComponentGroup(PyCommand):
                            """
                            RemoveFromComponentGroup(GroupType: str, GroupName: str, BCName: str) -> bool
                            """
                            pass

                        class AddToComponentGroup(PyCommand):
                            """
                            AddToComponentGroup(GroupType: str, GroupName: str, GroupPart: str, BCName: str) -> bool
                            """
                            pass

                    class SimulationConditions(PyMenu):
                        """
                        Singleton SimulationConditions.
                        """
                        def __init__(self, service, rules, path):
                            self.CustomInputOutput = self.__class__.CustomInputOutput(service, rules, path + [("CustomInputOutput", "")])
                            self.FlightConditions = self.__class__.FlightConditions(service, rules, path + [("FlightConditions", "")])
                            self.DesignPoints = self.__class__.DesignPoints(service, rules, path + [("DesignPoints", "")])
                            self.ShowInputSelectPanel = self.__class__.ShowInputSelectPanel(service, rules, "ShowInputSelectPanel", path)
                            self.FillCustomTableCellString = self.__class__.FillCustomTableCellString(service, rules, "FillCustomTableCellString", path)
                            self.ShowOutputSelectPanel = self.__class__.ShowOutputSelectPanel(service, rules, "ShowOutputSelectPanel", path)
                            self.SetDesignPointsStatus = self.__class__.SetDesignPointsStatus(service, rules, "SetDesignPointsStatus", path)
                            self.RefreshStatusCustomTable = self.__class__.RefreshStatusCustomTable(service, rules, "RefreshStatusCustomTable", path)
                            self.AddTableDP = self.__class__.AddTableDP(service, rules, "AddTableDP", path)
                            self.DeleteTableDP = self.__class__.DeleteTableDP(service, rules, "DeleteTableDP", path)
                            self.TableExportCSV = self.__class__.TableExportCSV(service, rules, "TableExportCSV", path)
                            self.InitCustomTable = self.__class__.InitCustomTable(service, rules, "InitCustomTable", path)
                            self.FillCustomTableCellReal = self.__class__.FillCustomTableCellReal(service, rules, "FillCustomTableCellReal", path)
                            self.ReloadResultsCustomTable = self.__class__.ReloadResultsCustomTable(service, rules, "ReloadResultsCustomTable", path)
                            self.TableImportCSV = self.__class__.TableImportCSV(service, rules, "TableImportCSV", path)
                            super().__init__(service, rules, path)

                        class CustomInputOutput(PyMenu):
                            """
                            Singleton CustomInputOutput.
                            """
                            def __init__(self, service, rules, path):
                                self.CustomOutputList = self.__class__.CustomOutputList(service, rules, path + [("CustomOutputList", "")])
                                self.CustomInputList = self.__class__.CustomInputList(service, rules, path + [("CustomInputList", "")])
                                self.CustomOutput = self.__class__.CustomOutput(service, rules, path + [("CustomOutput", "")])
                                self.ComponentInputsList = self.__class__.ComponentInputsList(service, rules, path + [("ComponentInputsList", "")])
                                self.ComponentInputs = self.__class__.ComponentInputs(service, rules, path + [("ComponentInputs", "")])
                                self.CustomInput = self.__class__.CustomInput(service, rules, path + [("CustomInput", "")])
                                self.SetCustomOutputs = self.__class__.SetCustomOutputs(service, rules, "SetCustomOutputs", path)
                                self.SetCustomInputs = self.__class__.SetCustomInputs(service, rules, "SetCustomInputs", path)
                                self.SetComponentOutputs = self.__class__.SetComponentOutputs(service, rules, "SetComponentOutputs", path)
                                super().__init__(service, rules, path)

                            class CustomOutputList(PyMenu):
                                """
                                Parameter CustomOutputList of value type List[str].
                                """
                                pass

                            class CustomInputList(PyMenu):
                                """
                                Parameter CustomInputList of value type List[str].
                                """
                                pass

                            class CustomOutput(PyMenu):
                                """
                                Parameter CustomOutput of value type bool.
                                """
                                pass

                            class ComponentInputsList(PyMenu):
                                """
                                Parameter ComponentInputsList of value type List[str].
                                """
                                pass

                            class ComponentInputs(PyMenu):
                                """
                                Parameter ComponentInputs of value type bool.
                                """
                                pass

                            class CustomInput(PyMenu):
                                """
                                Parameter CustomInput of value type bool.
                                """
                                pass

                            class SetCustomOutputs(PyCommand):
                                """
                                SetCustomOutputs(OutputList: List[str]) -> bool
                                """
                                pass

                            class SetCustomInputs(PyCommand):
                                """
                                SetCustomInputs(InputList: List[str]) -> bool
                                """
                                pass

                            class SetComponentOutputs(PyCommand):
                                """
                                SetComponentOutputs(OutputComponentList: List[str], MonitorComponentList: List[str]) -> bool
                                """
                                pass

                        class FlightConditions(PyMenu):
                            """
                            Singleton FlightConditions.
                            """
                            def __init__(self, service, rules, path):
                                self.FlowSpeed = self.__class__.FlowSpeed(service, rules, path + [("FlowSpeed", "")])
                                self.FlowDirection = self.__class__.FlowDirection(service, rules, path + [("FlowDirection", "")])
                                self.PresTempInput = self.__class__.PresTempInput(service, rules, path + [("PresTempInput", "")])
                                super().__init__(service, rules, path)

                            class FlowSpeed(PyMenu):
                                """
                                Singleton FlowSpeed.
                                """
                                def __init__(self, service, rules, path):
                                    self.MassFlowMax = self.__class__.MassFlowMax(service, rules, path + [("MassFlowMax", "")])
                                    self.MassFlowMin = self.__class__.MassFlowMin(service, rules, path + [("MassFlowMin", "")])
                                    self.Mach = self.__class__.Mach(service, rules, path + [("Mach", "")])
                                    self.TasNum = self.__class__.TasNum(service, rules, path + [("TasNum", "")])
                                    self.Distribution = self.__class__.Distribution(service, rules, path + [("Distribution", "")])
                                    self.MachMin = self.__class__.MachMin(service, rules, path + [("MachMin", "")])
                                    self.MassFlow = self.__class__.MassFlow(service, rules, path + [("MassFlow", "")])
                                    self.Tas = self.__class__.Tas(service, rules, path + [("Tas", "")])
                                    self.MassFlowNum = self.__class__.MassFlowNum(service, rules, path + [("MassFlowNum", "")])
                                    self.TasMax = self.__class__.TasMax(service, rules, path + [("TasMax", "")])
                                    self.MachNum = self.__class__.MachNum(service, rules, path + [("MachNum", "")])
                                    self.Parameter = self.__class__.Parameter(service, rules, path + [("Parameter", "")])
                                    self.TasMin = self.__class__.TasMin(service, rules, path + [("TasMin", "")])
                                    self.MachMax = self.__class__.MachMax(service, rules, path + [("MachMax", "")])
                                    super().__init__(service, rules, path)

                                class MassFlowMax(PyMenu):
                                    """
                                    Parameter MassFlowMax of value type float.
                                    """
                                    pass

                                class MassFlowMin(PyMenu):
                                    """
                                    Parameter MassFlowMin of value type float.
                                    """
                                    pass

                                class Mach(PyMenu):
                                    """
                                    Parameter Mach of value type float.
                                    """
                                    pass

                                class TasNum(PyMenu):
                                    """
                                    Parameter TasNum of value type int.
                                    """
                                    pass

                                class Distribution(PyMenu):
                                    """
                                    Parameter Distribution of value type str.
                                    """
                                    pass

                                class MachMin(PyMenu):
                                    """
                                    Parameter MachMin of value type float.
                                    """
                                    pass

                                class MassFlow(PyMenu):
                                    """
                                    Parameter MassFlow of value type float.
                                    """
                                    pass

                                class Tas(PyMenu):
                                    """
                                    Parameter Tas of value type float.
                                    """
                                    pass

                                class MassFlowNum(PyMenu):
                                    """
                                    Parameter MassFlowNum of value type int.
                                    """
                                    pass

                                class TasMax(PyMenu):
                                    """
                                    Parameter TasMax of value type float.
                                    """
                                    pass

                                class MachNum(PyMenu):
                                    """
                                    Parameter MachNum of value type int.
                                    """
                                    pass

                                class Parameter(PyMenu):
                                    """
                                    Parameter Parameter of value type str.
                                    """
                                    pass

                                class TasMin(PyMenu):
                                    """
                                    Parameter TasMin of value type float.
                                    """
                                    pass

                                class MachMax(PyMenu):
                                    """
                                    Parameter MachMax of value type float.
                                    """
                                    pass

                            class FlowDirection(PyMenu):
                                """
                                Singleton FlowDirection.
                                """
                                def __init__(self, service, rules, path):
                                    self.Parameter = self.__class__.Parameter(service, rules, path + [("Parameter", "")])
                                    self.AosMax = self.__class__.AosMax(service, rules, path + [("AosMax", "")])
                                    self.Aoa = self.__class__.Aoa(service, rules, path + [("Aoa", "")])
                                    self.DistributionAos = self.__class__.DistributionAos(service, rules, path + [("DistributionAos", "")])
                                    self.AoaNum = self.__class__.AoaNum(service, rules, path + [("AoaNum", "")])
                                    self.AosMin = self.__class__.AosMin(service, rules, path + [("AosMin", "")])
                                    self.AosNum = self.__class__.AosNum(service, rules, path + [("AosNum", "")])
                                    self.ParamSearchInputEnabled = self.__class__.ParamSearchInputEnabled(service, rules, path + [("ParamSearchInputEnabled", "")])
                                    self.AoaMin = self.__class__.AoaMin(service, rules, path + [("AoaMin", "")])
                                    self.Aos = self.__class__.Aos(service, rules, path + [("Aos", "")])
                                    self.AoaMax = self.__class__.AoaMax(service, rules, path + [("AoaMax", "")])
                                    self.DistributionAoa = self.__class__.DistributionAoa(service, rules, path + [("DistributionAoa", "")])
                                    super().__init__(service, rules, path)

                                class Parameter(PyMenu):
                                    """
                                    Parameter Parameter of value type str.
                                    """
                                    pass

                                class AosMax(PyMenu):
                                    """
                                    Parameter AosMax of value type float.
                                    """
                                    pass

                                class Aoa(PyMenu):
                                    """
                                    Parameter Aoa of value type float.
                                    """
                                    pass

                                class DistributionAos(PyMenu):
                                    """
                                    Parameter DistributionAos of value type str.
                                    """
                                    pass

                                class AoaNum(PyMenu):
                                    """
                                    Parameter AoaNum of value type int.
                                    """
                                    pass

                                class AosMin(PyMenu):
                                    """
                                    Parameter AosMin of value type float.
                                    """
                                    pass

                                class AosNum(PyMenu):
                                    """
                                    Parameter AosNum of value type int.
                                    """
                                    pass

                                class ParamSearchInputEnabled(PyMenu):
                                    """
                                    Parameter ParamSearchInputEnabled of value type bool.
                                    """
                                    pass

                                class AoaMin(PyMenu):
                                    """
                                    Parameter AoaMin of value type float.
                                    """
                                    pass

                                class Aos(PyMenu):
                                    """
                                    Parameter Aos of value type float.
                                    """
                                    pass

                                class AoaMax(PyMenu):
                                    """
                                    Parameter AoaMax of value type float.
                                    """
                                    pass

                                class DistributionAoa(PyMenu):
                                    """
                                    Parameter DistributionAoa of value type str.
                                    """
                                    pass

                            class PresTempInput(PyMenu):
                                """
                                Singleton PresTempInput.
                                """
                                def __init__(self, service, rules, path):
                                    self.TotalTemperatureMin = self.__class__.TotalTemperatureMin(service, rules, path + [("TotalTemperatureMin", "")])
                                    self.DistributionTotalPressure = self.__class__.DistributionTotalPressure(service, rules, path + [("DistributionTotalPressure", "")])
                                    self.Temperature = self.__class__.Temperature(service, rules, path + [("Temperature", "")])
                                    self.AltitudeNum = self.__class__.AltitudeNum(service, rules, path + [("AltitudeNum", "")])
                                    self.TotalPressureMin = self.__class__.TotalPressureMin(service, rules, path + [("TotalPressureMin", "")])
                                    self.TotalTemperatureMax = self.__class__.TotalTemperatureMax(service, rules, path + [("TotalTemperatureMax", "")])
                                    self.TotalTemperature = self.__class__.TotalTemperature(service, rules, path + [("TotalTemperature", "")])
                                    self.ReynoldsMin = self.__class__.ReynoldsMin(service, rules, path + [("ReynoldsMin", "")])
                                    self.PressureMax = self.__class__.PressureMax(service, rules, path + [("PressureMax", "")])
                                    self.ReynoldsNum = self.__class__.ReynoldsNum(service, rules, path + [("ReynoldsNum", "")])
                                    self.TemperatureMax = self.__class__.TemperatureMax(service, rules, path + [("TemperatureMax", "")])
                                    self.Pressure = self.__class__.Pressure(service, rules, path + [("Pressure", "")])
                                    self.TemperatureNum = self.__class__.TemperatureNum(service, rules, path + [("TemperatureNum", "")])
                                    self.TotalPressureMax = self.__class__.TotalPressureMax(service, rules, path + [("TotalPressureMax", "")])
                                    self.Parameter = self.__class__.Parameter(service, rules, path + [("Parameter", "")])
                                    self.DistributionReynolds = self.__class__.DistributionReynolds(service, rules, path + [("DistributionReynolds", "")])
                                    self.Reynolds = self.__class__.Reynolds(service, rules, path + [("Reynolds", "")])
                                    self.ReynoldsMax = self.__class__.ReynoldsMax(service, rules, path + [("ReynoldsMax", "")])
                                    self.DistributionTemperature = self.__class__.DistributionTemperature(service, rules, path + [("DistributionTemperature", "")])
                                    self.Distribution = self.__class__.Distribution(service, rules, path + [("Distribution", "")])
                                    self.Altitude = self.__class__.Altitude(service, rules, path + [("Altitude", "")])
                                    self.AltitudeMin = self.__class__.AltitudeMin(service, rules, path + [("AltitudeMin", "")])
                                    self.DistributionPressure = self.__class__.DistributionPressure(service, rules, path + [("DistributionPressure", "")])
                                    self.TotalPressure = self.__class__.TotalPressure(service, rules, path + [("TotalPressure", "")])
                                    self.PressureMin = self.__class__.PressureMin(service, rules, path + [("PressureMin", "")])
                                    self.TotalPressureNum = self.__class__.TotalPressureNum(service, rules, path + [("TotalPressureNum", "")])
                                    self.TotalTemperatureNum = self.__class__.TotalTemperatureNum(service, rules, path + [("TotalTemperatureNum", "")])
                                    self.TemperatureMin = self.__class__.TemperatureMin(service, rules, path + [("TemperatureMin", "")])
                                    self.PressureNum = self.__class__.PressureNum(service, rules, path + [("PressureNum", "")])
                                    self.AltitudeMax = self.__class__.AltitudeMax(service, rules, path + [("AltitudeMax", "")])
                                    self.DistributionTotalTemperature = self.__class__.DistributionTotalTemperature(service, rules, path + [("DistributionTotalTemperature", "")])
                                    super().__init__(service, rules, path)

                                class TotalTemperatureMin(PyMenu):
                                    """
                                    Parameter TotalTemperatureMin of value type float.
                                    """
                                    pass

                                class DistributionTotalPressure(PyMenu):
                                    """
                                    Parameter DistributionTotalPressure of value type str.
                                    """
                                    pass

                                class Temperature(PyMenu):
                                    """
                                    Parameter Temperature of value type float.
                                    """
                                    pass

                                class AltitudeNum(PyMenu):
                                    """
                                    Parameter AltitudeNum of value type int.
                                    """
                                    pass

                                class TotalPressureMin(PyMenu):
                                    """
                                    Parameter TotalPressureMin of value type float.
                                    """
                                    pass

                                class TotalTemperatureMax(PyMenu):
                                    """
                                    Parameter TotalTemperatureMax of value type float.
                                    """
                                    pass

                                class TotalTemperature(PyMenu):
                                    """
                                    Parameter TotalTemperature of value type float.
                                    """
                                    pass

                                class ReynoldsMin(PyMenu):
                                    """
                                    Parameter ReynoldsMin of value type float.
                                    """
                                    pass

                                class PressureMax(PyMenu):
                                    """
                                    Parameter PressureMax of value type float.
                                    """
                                    pass

                                class ReynoldsNum(PyMenu):
                                    """
                                    Parameter ReynoldsNum of value type int.
                                    """
                                    pass

                                class TemperatureMax(PyMenu):
                                    """
                                    Parameter TemperatureMax of value type float.
                                    """
                                    pass

                                class Pressure(PyMenu):
                                    """
                                    Parameter Pressure of value type float.
                                    """
                                    pass

                                class TemperatureNum(PyMenu):
                                    """
                                    Parameter TemperatureNum of value type int.
                                    """
                                    pass

                                class TotalPressureMax(PyMenu):
                                    """
                                    Parameter TotalPressureMax of value type float.
                                    """
                                    pass

                                class Parameter(PyMenu):
                                    """
                                    Parameter Parameter of value type str.
                                    """
                                    pass

                                class DistributionReynolds(PyMenu):
                                    """
                                    Parameter DistributionReynolds of value type str.
                                    """
                                    pass

                                class Reynolds(PyMenu):
                                    """
                                    Parameter Reynolds of value type float.
                                    """
                                    pass

                                class ReynoldsMax(PyMenu):
                                    """
                                    Parameter ReynoldsMax of value type float.
                                    """
                                    pass

                                class DistributionTemperature(PyMenu):
                                    """
                                    Parameter DistributionTemperature of value type str.
                                    """
                                    pass

                                class Distribution(PyMenu):
                                    """
                                    Parameter Distribution of value type str.
                                    """
                                    pass

                                class Altitude(PyMenu):
                                    """
                                    Parameter Altitude of value type float.
                                    """
                                    pass

                                class AltitudeMin(PyMenu):
                                    """
                                    Parameter AltitudeMin of value type float.
                                    """
                                    pass

                                class DistributionPressure(PyMenu):
                                    """
                                    Parameter DistributionPressure of value type str.
                                    """
                                    pass

                                class TotalPressure(PyMenu):
                                    """
                                    Parameter TotalPressure of value type float.
                                    """
                                    pass

                                class PressureMin(PyMenu):
                                    """
                                    Parameter PressureMin of value type float.
                                    """
                                    pass

                                class TotalPressureNum(PyMenu):
                                    """
                                    Parameter TotalPressureNum of value type int.
                                    """
                                    pass

                                class TotalTemperatureNum(PyMenu):
                                    """
                                    Parameter TotalTemperatureNum of value type int.
                                    """
                                    pass

                                class TemperatureMin(PyMenu):
                                    """
                                    Parameter TemperatureMin of value type float.
                                    """
                                    pass

                                class PressureNum(PyMenu):
                                    """
                                    Parameter PressureNum of value type int.
                                    """
                                    pass

                                class AltitudeMax(PyMenu):
                                    """
                                    Parameter AltitudeMax of value type float.
                                    """
                                    pass

                                class DistributionTotalTemperature(PyMenu):
                                    """
                                    Parameter DistributionTotalTemperature of value type str.
                                    """
                                    pass

                        class DesignPoints(PyMenu):
                            """
                            Singleton DesignPoints.
                            """
                            def __init__(self, service, rules, path):
                                self.NumDPs = self.__class__.NumDPs(service, rules, path + [("NumDPs", "")])
                                super().__init__(service, rules, path)

                            class NumDPs(PyMenu):
                                """
                                Parameter NumDPs of value type int.
                                """
                                pass

                        class ShowInputSelectPanel(PyCommand):
                            """
                            ShowInputSelectPanel() -> bool
                            """
                            pass

                        class FillCustomTableCellString(PyCommand):
                            """
                            FillCustomTableCellString(dpi: int, icol: int, val: str) -> bool
                            """
                            pass

                        class ShowOutputSelectPanel(PyCommand):
                            """
                            ShowOutputSelectPanel() -> bool
                            """
                            pass

                        class SetDesignPointsStatus(PyCommand):
                            """
                            SetDesignPointsStatus() -> bool
                            """
                            pass

                        class RefreshStatusCustomTable(PyCommand):
                            """
                            RefreshStatusCustomTable() -> bool
                            """
                            pass

                        class AddTableDP(PyCommand):
                            """
                            AddTableDP() -> bool
                            """
                            pass

                        class DeleteTableDP(PyCommand):
                            """
                            DeleteTableDP() -> bool
                            """
                            pass

                        class TableExportCSV(PyCommand):
                            """
                            TableExportCSV(FileName: str) -> bool
                            """
                            pass

                        class InitCustomTable(PyCommand):
                            """
                            InitCustomTable() -> bool
                            """
                            pass

                        class FillCustomTableCellReal(PyCommand):
                            """
                            FillCustomTableCellReal(dpi: int, icol: int, val: float) -> bool
                            """
                            pass

                        class ReloadResultsCustomTable(PyCommand):
                            """
                            ReloadResultsCustomTable() -> bool
                            """
                            pass

                        class TableImportCSV(PyCommand):
                            """
                            TableImportCSV(FileName: str) -> bool
                            """
                            pass

                    class GeometricProperties(PyMenu):
                        """
                        Singleton GeometricProperties.
                        """
                        def __init__(self, service, rules, path):
                            self.PrjArea = self.__class__.PrjArea(service, rules, path + [("PrjArea", "")])
                            self.MomentCenterZ = self.__class__.MomentCenterZ(service, rules, path + [("MomentCenterZ", "")])
                            self.MomentCenterX = self.__class__.MomentCenterX(service, rules, path + [("MomentCenterX", "")])
                            self.RefLength = self.__class__.RefLength(service, rules, path + [("RefLength", "")])
                            self.MomentCenterY = self.__class__.MomentCenterY(service, rules, path + [("MomentCenterY", "")])
                            self.LiftDir = self.__class__.LiftDir(service, rules, path + [("LiftDir", "")])
                            self.MomentPitchDir = self.__class__.MomentPitchDir(service, rules, path + [("MomentPitchDir", "")])
                            self.RefArea = self.__class__.RefArea(service, rules, path + [("RefArea", "")])
                            self.DragDir = self.__class__.DragDir(service, rules, path + [("DragDir", "")])
                            self.DomainType = self.__class__.DomainType(service, rules, path + [("DomainType", "")])
                            self.PlaneNormalDir = self.__class__.PlaneNormalDir(service, rules, path + [("PlaneNormalDir", "")])
                            self.RefreshBCs = self.__class__.RefreshBCs(service, rules, "RefreshBCs", path)
                            self.GridLoad = self.__class__.GridLoad(service, rules, "GridLoad", path)
                            super().__init__(service, rules, path)

                        class PrjArea(PyMenu):
                            """
                            Parameter PrjArea of value type bool.
                            """
                            pass

                        class MomentCenterZ(PyMenu):
                            """
                            Parameter MomentCenterZ of value type float.
                            """
                            pass

                        class MomentCenterX(PyMenu):
                            """
                            Parameter MomentCenterX of value type float.
                            """
                            pass

                        class RefLength(PyMenu):
                            """
                            Parameter RefLength of value type float.
                            """
                            pass

                        class MomentCenterY(PyMenu):
                            """
                            Parameter MomentCenterY of value type float.
                            """
                            pass

                        class LiftDir(PyMenu):
                            """
                            Parameter LiftDir of value type str.
                            """
                            pass

                        class MomentPitchDir(PyMenu):
                            """
                            Parameter MomentPitchDir of value type str.
                            """
                            pass

                        class RefArea(PyMenu):
                            """
                            Parameter RefArea of value type float.
                            """
                            pass

                        class DragDir(PyMenu):
                            """
                            Parameter DragDir of value type str.
                            """
                            pass

                        class DomainType(PyMenu):
                            """
                            Parameter DomainType of value type str.
                            """
                            pass

                        class PlaneNormalDir(PyMenu):
                            """
                            Parameter PlaneNormalDir of value type str.
                            """
                            pass

                        class RefreshBCs(PyCommand):
                            """
                            RefreshBCs() -> bool
                            """
                            pass

                        class GridLoad(PyCommand):
                            """
                            GridLoad() -> bool
                            """
                            pass

                    class AdvancedWorkflows(PyMenu):
                        """
                        Singleton AdvancedWorkflows.
                        """
                        def __init__(self, service, rules, path):
                            self.ParameterSearch = self.__class__.ParameterSearch(service, rules, path + [("ParameterSearch", "")])
                            super().__init__(service, rules, path)

                        class ParameterSearch(PyMenu):
                            """
                            Parameter ParameterSearch of value type bool.
                            """
                            pass

                    class ParameterSearch(PyMenu):
                        """
                        Singleton ParameterSearch.
                        """
                        def __init__(self, service, rules, path):
                            self.SearchInput = self.__class__.SearchInput(service, rules, path + [("SearchInput", "")])
                            self.SearchObjective = self.__class__.SearchObjective(service, rules, path + [("SearchObjective", "")])
                            super().__init__(service, rules, path)

                        class SearchInput(PyMenu):
                            """
                            Singleton SearchInput.
                            """
                            def __init__(self, service, rules, path):
                                self.ParameterValueInitialDelta = self.__class__.ParameterValueInitialDelta(service, rules, path + [("ParameterValueInitialDelta", "")])
                                self.ParameterValueMax = self.__class__.ParameterValueMax(service, rules, path + [("ParameterValueMax", "")])
                                self.ParameterValueMin = self.__class__.ParameterValueMin(service, rules, path + [("ParameterValueMin", "")])
                                self.ParameterValueInitial = self.__class__.ParameterValueInitial(service, rules, path + [("ParameterValueInitial", "")])
                                self.Parameter = self.__class__.Parameter(service, rules, path + [("Parameter", "")])
                                super().__init__(service, rules, path)

                            class ParameterValueInitialDelta(PyMenu):
                                """
                                Parameter ParameterValueInitialDelta of value type float.
                                """
                                pass

                            class ParameterValueMax(PyMenu):
                                """
                                Parameter ParameterValueMax of value type float.
                                """
                                pass

                            class ParameterValueMin(PyMenu):
                                """
                                Parameter ParameterValueMin of value type float.
                                """
                                pass

                            class ParameterValueInitial(PyMenu):
                                """
                                Parameter ParameterValueInitial of value type float.
                                """
                                pass

                            class Parameter(PyMenu):
                                """
                                Parameter Parameter of value type str.
                                """
                                pass

                        class SearchObjective(PyMenu):
                            """
                            Singleton SearchObjective.
                            """
                            def __init__(self, service, rules, path):
                                self.Tolerance = self.__class__.Tolerance(service, rules, path + [("Tolerance", "")])
                                self.Parameter = self.__class__.Parameter(service, rules, path + [("Parameter", "")])
                                self.Distribution = self.__class__.Distribution(service, rules, path + [("Distribution", "")])
                                self.TargetValue = self.__class__.TargetValue(service, rules, path + [("TargetValue", "")])
                                self.Objective = self.__class__.Objective(service, rules, path + [("Objective", "")])
                                super().__init__(service, rules, path)

                            class Tolerance(PyMenu):
                                """
                                Parameter Tolerance of value type float.
                                """
                                pass

                            class Parameter(PyMenu):
                                """
                                Parameter Parameter of value type str.
                                """
                                pass

                            class Distribution(PyMenu):
                                """
                                Parameter Distribution of value type str.
                                """
                                pass

                            class TargetValue(PyMenu):
                                """
                                Parameter TargetValue of value type float.
                                """
                                pass

                            class Objective(PyMenu):
                                """
                                Parameter Objective of value type str.
                                """
                                pass

                class AeroFlags(PyMenu):
                    """
                    Singleton AeroFlags.
                    """
                    def __init__(self, service, rules, path):
                        self.ContinueFlag = self.__class__.ContinueFlag(service, rules, path + [("ContinueFlag", "")])
                        self.BCtypeChanged = self.__class__.BCtypeChanged(service, rules, path + [("BCtypeChanged", "")])
                        self.SettingsLoaded = self.__class__.SettingsLoaded(service, rules, path + [("SettingsLoaded", "")])
                        self.AeroIsBusy = self.__class__.AeroIsBusy(service, rules, path + [("AeroIsBusy", "")])
                        self.InterruptPressed = self.__class__.InterruptPressed(service, rules, path + [("InterruptPressed", "")])
                        self.InterruptSolver = self.__class__.InterruptSolver(service, rules, path + [("InterruptSolver", "")])
                        self.SolveFlag = self.__class__.SolveFlag(service, rules, path + [("SolveFlag", "")])
                        self.BCnameChanged = self.__class__.BCnameChanged(service, rules, path + [("BCnameChanged", "")])
                        super().__init__(service, rules, path)

                    class ContinueFlag(PyMenu):
                        """
                        Parameter ContinueFlag of value type bool.
                        """
                        pass

                    class BCtypeChanged(PyMenu):
                        """
                        Parameter BCtypeChanged of value type bool.
                        """
                        pass

                    class SettingsLoaded(PyMenu):
                        """
                        Parameter SettingsLoaded of value type bool.
                        """
                        pass

                    class AeroIsBusy(PyMenu):
                        """
                        Parameter AeroIsBusy of value type bool.
                        """
                        pass

                    class InterruptPressed(PyMenu):
                        """
                        Parameter InterruptPressed of value type bool.
                        """
                        pass

                    class InterruptSolver(PyMenu):
                        """
                        Parameter InterruptSolver of value type bool.
                        """
                        pass

                    class SolveFlag(PyMenu):
                        """
                        Parameter SolveFlag of value type bool.
                        """
                        pass

                    class BCnameChanged(PyMenu):
                        """
                        Parameter BCnameChanged of value type bool.
                        """
                        pass

                class Results(PyMenu):
                    """
                    Singleton Results.
                    """
                    def __init__(self, service, rules, path):
                        self.Tables = self.__class__.Tables(service, rules, path + [("Tables", "")])
                        self.Contours = self.__class__.Contours(service, rules, path + [("Contours", "")])
                        self.Graphs = self.__class__.Graphs(service, rules, path + [("Graphs", "")])
                        self.Plots = self.__class__.Plots(service, rules, path + [("Plots", "")])
                        self.CurrentSolution = self.__class__.CurrentSolution(service, rules, path + [("CurrentSolution", "")])
                        super().__init__(service, rules, path)

                    class Tables(PyMenu):
                        """
                        Singleton Tables.
                        """
                        def __init__(self, service, rules, path):
                            self.ExportTables = self.__class__.ExportTables(service, rules, "ExportTables", path)
                            self.ExportStkAero = self.__class__.ExportStkAero(service, rules, "ExportStkAero", path)
                            self.CreateTables = self.__class__.CreateTables(service, rules, "CreateTables", path)
                            self.PostProcUpdate = self.__class__.PostProcUpdate(service, rules, "PostProcUpdate", path)
                            super().__init__(service, rules, path)

                        class ExportTables(PyCommand):
                            """
                            ExportTables() -> bool
                            """
                            pass

                        class ExportStkAero(PyCommand):
                            """
                            ExportStkAero(Type: str) -> bool
                            """
                            pass

                        class CreateTables(PyCommand):
                            """
                            CreateTables() -> bool
                            """
                            pass

                        class PostProcUpdate(PyCommand):
                            """
                            PostProcUpdate() -> bool
                            """
                            pass

                    class Contours(PyMenu):
                        """
                        Singleton Contours.
                        """
                        def __init__(self, service, rules, path):
                            self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                            self.CuttingPlaneNormal = self.__class__.CuttingPlaneNormal(service, rules, path + [("CuttingPlaneNormal", "")])
                            self.CuttingPlanePosition = self.__class__.CuttingPlanePosition(service, rules, path + [("CuttingPlanePosition", "")])
                            self.Solution = self.__class__.Solution(service, rules, path + [("Solution", "")])
                            self.DrawMesh = self.__class__.DrawMesh(service, rules, path + [("DrawMesh", "")])
                            self.CutFields = self.__class__.CutFields(service, rules, path + [("CutFields", "")])
                            self.ComponentGroupFields = self.__class__.ComponentGroupFields(service, rules, path + [("ComponentGroupFields", "")])
                            self.CuttingPlaneMax = self.__class__.CuttingPlaneMax(service, rules, path + [("CuttingPlaneMax", "")])
                            self.RangeMax = self.__class__.RangeMax(service, rules, path + [("RangeMax", "")])
                            self.CuttingPlaneMin = self.__class__.CuttingPlaneMin(service, rules, path + [("CuttingPlaneMin", "")])
                            self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
                            self.RangeMin = self.__class__.RangeMin(service, rules, path + [("RangeMin", "")])
                            self.CuttingPlaneMinMax = self.__class__.CuttingPlaneMinMax(service, rules, path + [("CuttingPlaneMinMax", "")])
                            self.ComponentGroups = self.__class__.ComponentGroups(service, rules, path + [("ComponentGroups", "")])
                            self.ContourSaveFlag = self.__class__.ContourSaveFlag(service, rules, path + [("ContourSaveFlag", "")])
                            self.SelectedSurfacesFields = self.__class__.SelectedSurfacesFields(service, rules, path + [("SelectedSurfacesFields", "")])
                            self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                            self.WallFields = self.__class__.WallFields(service, rules, path + [("WallFields", "")])
                            self.SurfacesGroup = self.__class__.SurfacesGroup(service, rules, path + [("SurfacesGroup", "")])
                            self.PlotCuttingPlane = self.__class__.PlotCuttingPlane(service, rules, "PlotCuttingPlane", path)
                            self.SaveContourImages = self.__class__.SaveContourImages(service, rules, "SaveContourImages", path)
                            self.ContourView = self.__class__.ContourView(service, rules, "ContourView", path)
                            self.PlotSurface = self.__class__.PlotSurface(service, rules, "PlotSurface", path)
                            super().__init__(service, rules, path)

                        class ColorMap(PyMenu):
                            """
                            Singleton ColorMap.
                            """
                            def __init__(self, service, rules, path):
                                self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                                self.Visible = self.__class__.Visible(service, rules, path + [("Visible", "")])
                                self.Skip = self.__class__.Skip(service, rules, path + [("Skip", "")])
                                self.ShowAll = self.__class__.ShowAll(service, rules, path + [("ShowAll", "")])
                                super().__init__(service, rules, path)

                            class ColorMap(PyMenu):
                                """
                                Parameter ColorMap of value type str.
                                """
                                pass

                            class Visible(PyMenu):
                                """
                                Parameter Visible of value type bool.
                                """
                                pass

                            class Skip(PyMenu):
                                """
                                Parameter Skip of value type int.
                                """
                                pass

                            class ShowAll(PyMenu):
                                """
                                Parameter ShowAll of value type bool.
                                """
                                pass

                        class CuttingPlaneNormal(PyMenu):
                            """
                            Parameter CuttingPlaneNormal of value type str.
                            """
                            pass

                        class CuttingPlanePosition(PyMenu):
                            """
                            Parameter CuttingPlanePosition of value type float.
                            """
                            pass

                        class Solution(PyMenu):
                            """
                            Parameter Solution of value type str.
                            """
                            pass

                        class DrawMesh(PyMenu):
                            """
                            Parameter DrawMesh of value type bool.
                            """
                            pass

                        class CutFields(PyMenu):
                            """
                            Parameter CutFields of value type str.
                            """
                            pass

                        class ComponentGroupFields(PyMenu):
                            """
                            Parameter ComponentGroupFields of value type str.
                            """
                            pass

                        class CuttingPlaneMax(PyMenu):
                            """
                            Parameter CuttingPlaneMax of value type float.
                            """
                            pass

                        class RangeMax(PyMenu):
                            """
                            Parameter RangeMax of value type float.
                            """
                            pass

                        class CuttingPlaneMin(PyMenu):
                            """
                            Parameter CuttingPlaneMin of value type float.
                            """
                            pass

                        class AutoRange(PyMenu):
                            """
                            Parameter AutoRange of value type bool.
                            """
                            pass

                        class RangeMin(PyMenu):
                            """
                            Parameter RangeMin of value type float.
                            """
                            pass

                        class CuttingPlaneMinMax(PyMenu):
                            """
                            Parameter CuttingPlaneMinMax of value type List[float].
                            """
                            pass

                        class ComponentGroups(PyMenu):
                            """
                            Parameter ComponentGroups of value type List[str].
                            """
                            pass

                        class ContourSaveFlag(PyMenu):
                            """
                            Parameter ContourSaveFlag of value type bool.
                            """
                            pass

                        class SelectedSurfacesFields(PyMenu):
                            """
                            Parameter SelectedSurfacesFields of value type str.
                            """
                            pass

                        class Surfaces(PyMenu):
                            """
                            Parameter Surfaces of value type List[str].
                            """
                            pass

                        class WallFields(PyMenu):
                            """
                            Parameter WallFields of value type str.
                            """
                            pass

                        class SurfacesGroup(PyMenu):
                            """
                            Parameter SurfacesGroup of value type str.
                            """
                            pass

                        class PlotCuttingPlane(PyCommand):
                            """
                            PlotCuttingPlane() -> bool
                            """
                            pass

                        class SaveContourImages(PyCommand):
                            """
                            SaveContourImages() -> bool
                            """
                            pass

                        class ContourView(PyCommand):
                            """
                            ContourView() -> bool
                            """
                            pass

                        class PlotSurface(PyCommand):
                            """
                            PlotSurface() -> bool
                            """
                            pass

                    class Graphs(PyMenu):
                        """
                        Singleton Graphs.
                        """
                        def __init__(self, service, rules, path):
                            self.AllPlot = self.__class__.AllPlot(service, rules, "AllPlot", path)
                            self.SavePlotCoeffs = self.__class__.SavePlotCoeffs(service, rules, "SavePlotCoeffs", path)
                            self.CoeffsPlot = self.__class__.CoeffsPlot(service, rules, "CoeffsPlot", path)
                            self.plotParametric = self.__class__.plotParametric(service, rules, "plotParametric", path)
                            self.ClCdPlot = self.__class__.ClCdPlot(service, rules, "ClCdPlot", path)
                            self.plotRefCoeffs = self.__class__.plotRefCoeffs(service, rules, "plotRefCoeffs", path)
                            super().__init__(service, rules, path)

                        class AllPlot(PyCommand):
                            """
                            AllPlot() -> bool
                            """
                            pass

                        class SavePlotCoeffs(PyCommand):
                            """
                            SavePlotCoeffs(FileName: str) -> bool
                            """
                            pass

                        class CoeffsPlot(PyCommand):
                            """
                            CoeffsPlot() -> bool
                            """
                            pass

                        class plotParametric(PyCommand):
                            """
                            plotParametric() -> bool
                            """
                            pass

                        class ClCdPlot(PyCommand):
                            """
                            ClCdPlot() -> bool
                            """
                            pass

                        class plotRefCoeffs(PyCommand):
                            """
                            plotRefCoeffs(FileName: str) -> bool
                            """
                            pass

                    class Plots(PyMenu):
                        """
                        Singleton Plots.
                        """
                        def __init__(self, service, rules, path):
                            self.CutNorm = self.__class__.CutNorm(service, rules, path + [("CutNorm", "")])
                            self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                            self.CutMax = self.__class__.CutMax(service, rules, path + [("CutMax", "")])
                            self.SurfacesGroup = self.__class__.SurfacesGroup(service, rules, path + [("SurfacesGroup", "")])
                            self.Solution = self.__class__.Solution(service, rules, path + [("Solution", "")])
                            self.CutPosition = self.__class__.CutPosition(service, rules, path + [("CutPosition", "")])
                            self.CutField = self.__class__.CutField(service, rules, path + [("CutField", "")])
                            self.CutNum = self.__class__.CutNum(service, rules, path + [("CutNum", "")])
                            self.ComponentGroups = self.__class__.ComponentGroups(service, rules, path + [("ComponentGroups", "")])
                            self.CutMin = self.__class__.CutMin(service, rules, path + [("CutMin", "")])
                            self.AeroCutLoadSolution = self.__class__.AeroCutLoadSolution(service, rules, "AeroCutLoadSolution", path)
                            self.plotRefCut = self.__class__.plotRefCut(service, rules, "plotRefCut", path)
                            self.CutPlot = self.__class__.CutPlot(service, rules, "CutPlot", path)
                            self.SavePlotCut = self.__class__.SavePlotCut(service, rules, "SavePlotCut", path)
                            super().__init__(service, rules, path)

                        class CutNorm(PyMenu):
                            """
                            Parameter CutNorm of value type str.
                            """
                            pass

                        class Surfaces(PyMenu):
                            """
                            Parameter Surfaces of value type List[str].
                            """
                            pass

                        class CutMax(PyMenu):
                            """
                            Parameter CutMax of value type float.
                            """
                            pass

                        class SurfacesGroup(PyMenu):
                            """
                            Parameter SurfacesGroup of value type str.
                            """
                            pass

                        class Solution(PyMenu):
                            """
                            Parameter Solution of value type str.
                            """
                            pass

                        class CutPosition(PyMenu):
                            """
                            Parameter CutPosition of value type float.
                            """
                            pass

                        class CutField(PyMenu):
                            """
                            Parameter CutField of value type str.
                            """
                            pass

                        class CutNum(PyMenu):
                            """
                            Parameter CutNum of value type int.
                            """
                            pass

                        class ComponentGroups(PyMenu):
                            """
                            Parameter ComponentGroups of value type List[str].
                            """
                            pass

                        class CutMin(PyMenu):
                            """
                            Parameter CutMin of value type float.
                            """
                            pass

                        class AeroCutLoadSolution(PyCommand):
                            """
                            AeroCutLoadSolution() -> bool
                            """
                            pass

                        class plotRefCut(PyCommand):
                            """
                            plotRefCut(FileName: str) -> bool
                            """
                            pass

                        class CutPlot(PyCommand):
                            """
                            CutPlot() -> bool
                            """
                            pass

                        class SavePlotCut(PyCommand):
                            """
                            SavePlotCut(FileName: str) -> bool
                            """
                            pass

                    class CurrentSolution(PyMenu):
                        """
                        Parameter CurrentSolution of value type int.
                        """
                        pass

                class AeroGetOutParam(PyCommand):
                    """
                    AeroGetOutParam(ParamName: str) -> str
                    """
                    pass

            class Domain(PyMenu):
                """
                Singleton Domain.
                """
                def __init__(self, service, rules, path):
                    self.Filter = self.__class__.Filter(service, rules, path + [("Filter", "")])
                    self.Mode = self.__class__.Mode(service, rules, path + [("Mode", "")])
                    self.NodeOrderId = self.__class__.NodeOrderId(service, rules, path + [("NodeOrderId", "")])
                    super().__init__(service, rules, path)

                class Filter(PyMenu):
                    """
                    Parameter Filter of value type str.
                    """
                    pass

                class Mode(PyMenu):
                    """
                    Parameter Mode of value type str.
                    """
                    pass

                class NodeOrderId(PyMenu):
                    """
                    Parameter NodeOrderId of value type str.
                    """
                    pass

            class GlobalSettings(PyMenu):
                """
                Singleton GlobalSettings.
                """
                def __init__(self, service, rules, path):
                    self.PlotInterval = self.__class__.PlotInterval(service, rules, path + [("PlotInterval", "")])
                    self.BetaFlag = self.__class__.BetaFlag(service, rules, path + [("BetaFlag", "")])
                    self.BetaOrAdvancedFlag = self.__class__.BetaOrAdvancedFlag(service, rules, path + [("BetaOrAdvancedFlag", "")])
                    self.AdvancedFlag = self.__class__.AdvancedFlag(service, rules, path + [("AdvancedFlag", "")])
                    self.CFFOutput = self.__class__.CFFOutput(service, rules, path + [("CFFOutput", "")])
                    super().__init__(service, rules, path)

                class PlotInterval(PyMenu):
                    """
                    Parameter PlotInterval of value type int.
                    """
                    pass

                class BetaFlag(PyMenu):
                    """
                    Parameter BetaFlag of value type bool.
                    """
                    pass

                class BetaOrAdvancedFlag(PyMenu):
                    """
                    Parameter BetaOrAdvancedFlag of value type bool.
                    """
                    pass

                class AdvancedFlag(PyMenu):
                    """
                    Parameter AdvancedFlag of value type bool.
                    """
                    pass

                class CFFOutput(PyMenu):
                    """
                    Parameter CFFOutput of value type bool.
                    """
                    pass

            class SetupErrors(PyMenu):
                """
                Parameter SetupErrors of value type str.
                """
                pass

            class SetupWarnings(PyMenu):
                """
                Parameter SetupWarnings of value type str.
                """
                pass

            class IsBusy(PyMenu):
                """
                Parameter IsBusy of value type bool.
                """
                pass

            class InProgress(PyMenu):
                """
                Parameter InProgress of value type bool.
                """
                pass

            class SaveCaseAs(PyCommand):
                """
                SaveCaseAs(FileName: str) -> bool
                """
                pass

            class SavePostCaseAndData(PyCommand):
                """
                SavePostCaseAndData(FileName: str) -> bool
                """
                pass

            class SendCommandQuiet(PyCommand):
                """
                SendCommandQuiet(Command: str) -> bool
                """
                pass

            class CheckSetup(PyCommand):
                """
                CheckSetup() -> str
                """
                pass

            class WriteAll(PyCommand):
                """
                WriteAll(FileName: str) -> bool
                """
                pass

            class ImportMesh(PyCommand):
                """
                ImportMesh(Filename: str) -> bool
                """
                pass

            class InitAddOn(PyCommand):
                """
                InitAddOn() -> bool
                """
                pass

            class SaveCase(PyCommand):
                """
                SaveCase(FileName: str) -> bool
                """
                pass

            class InitAddOnAero(PyCommand):
                """
                InitAddOnAero() -> bool
                """
                pass

            class ReloadCase(PyCommand):
                """
                ReloadCase(Filename: str) -> bool
                """
                pass

            class SyncDM(PyCommand):
                """
                SyncDM() -> bool
                """
                pass

            class InitDM(PyCommand):
                """
                InitDM() -> bool
                """
                pass

            class SaveData(PyCommand):
                """
                SaveData(FileName: str) -> bool
                """
                pass

            class LoadCaseAndData(PyCommand):
                """
                LoadCaseAndData(FileName: str) -> bool
                """
                pass

            class ReloadDomain(PyCommand):
                """
                ReloadDomain(CheckNodeOrder: bool) -> bool
                """
                pass

            class ImportCase(PyCommand):
                """
                ImportCase(Filename: str) -> bool
                """
                pass

            class SaveCaseAndData(PyCommand):
                """
                SaveCaseAndData(FileName: str) -> bool
                """
                pass

            class LoadCase(PyCommand):
                """
                LoadCase(FileName: str) -> bool
                """
                pass

        class Results(PyMenu):
            """
            Singleton Results.
            """
            def __init__(self, service, rules, path):
                self.Reports = self.__class__.Reports(service, rules, path + [("Reports", "")])
                self.View = self.__class__.View(service, rules, path + [("View", "")])
                self.SurfaceDefs = self.__class__.SurfaceDefs(service, rules, path + [("SurfaceDefs", "")])
                self.ResultsExternalInfo = self.__class__.ResultsExternalInfo(service, rules, path + [("ResultsExternalInfo", "")])
                self.Graphics = self.__class__.Graphics(service, rules, path + [("Graphics", "")])
                self.Plots = self.__class__.Plots(service, rules, path + [("Plots", "")])
                self.CreateMultipleIsosurfaces = self.__class__.CreateMultipleIsosurfaces(service, rules, "CreateMultipleIsosurfaces", path)
                self.CreateCellZoneSurfaces = self.__class__.CreateCellZoneSurfaces(service, rules, "CreateCellZoneSurfaces", path)
                self.CreateMultiplePlanes = self.__class__.CreateMultiplePlanes(service, rules, "CreateMultiplePlanes", path)
                self.GetFieldMinMax = self.__class__.GetFieldMinMax(service, rules, "GetFieldMinMax", path)
                self.GetXYData = self.__class__.GetXYData(service, rules, "GetXYData", path)
                super().__init__(service, rules, path)

            class Reports(PyNamedObjectContainer):
                class _Reports(PyMenu):
                    """
                    Singleton _Reports.
                    """
                    def __init__(self, service, rules, path):
                        self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                        self.Quantity = self.__class__.Quantity(service, rules, path + [("Quantity", "")])
                        self.DensitySpecification = self.__class__.DensitySpecification(service, rules, path + [("DensitySpecification", "")])
                        self.VelocityField = self.__class__.VelocityField(service, rules, path + [("VelocityField", "")])
                        self.DensityConstant = self.__class__.DensityConstant(service, rules, path + [("DensityConstant", "")])
                        self.DensityField = self.__class__.DensityField(service, rules, path + [("DensityField", "")])
                        self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                        self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                        self.Expression = self.__class__.Expression(service, rules, path + [("Expression", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        self.VolumeFractionField = self.__class__.VolumeFractionField(service, rules, path + [("VolumeFractionField", "")])
                        self.ForEach = self.__class__.ForEach(service, rules, path + [("ForEach", "")])
                        self.Volumes = self.__class__.Volumes(service, rules, path + [("Volumes", "")])
                        self.SaveReport = self.__class__.SaveReport(service, rules, "SaveReport", path)
                        self.PrintReport = self.__class__.PrintReport(service, rules, "PrintReport", path)
                        self.PlotReport = self.__class__.PlotReport(service, rules, "PlotReport", path)
                        self.GetReport = self.__class__.GetReport(service, rules, "GetReport", path)
                        super().__init__(service, rules, path)

                    class Field(PyMenu):
                        """
                        Parameter Field of value type str.
                        """
                        pass

                    class Quantity(PyMenu):
                        """
                        Parameter Quantity of value type str.
                        """
                        pass

                    class DensitySpecification(PyMenu):
                        """
                        Parameter DensitySpecification of value type str.
                        """
                        pass

                    class VelocityField(PyMenu):
                        """
                        Parameter VelocityField of value type str.
                        """
                        pass

                    class DensityConstant(PyMenu):
                        """
                        Parameter DensityConstant of value type float.
                        """
                        pass

                    class DensityField(PyMenu):
                        """
                        Parameter DensityField of value type str.
                        """
                        pass

                    class Surfaces(PyMenu):
                        """
                        Parameter Surfaces of value type List[str].
                        """
                        pass

                    class Type(PyMenu):
                        """
                        Parameter Type of value type str.
                        """
                        pass

                    class Expression(PyMenu):
                        """
                        Parameter Expression of value type str.
                        """
                        pass

                    class _name_(PyMenu):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                    class VolumeFractionField(PyMenu):
                        """
                        Parameter VolumeFractionField of value type str.
                        """
                        pass

                    class ForEach(PyMenu):
                        """
                        Parameter ForEach of value type bool.
                        """
                        pass

                    class Volumes(PyMenu):
                        """
                        Parameter Volumes of value type List[str].
                        """
                        pass

                    class SaveReport(PyCommand):
                        """
                        SaveReport(Filename: str, TimestepSelection: Dict[str, Any]) -> None
                        """
                        pass

                    class PrintReport(PyCommand):
                        """
                        PrintReport(TimestepSelection: Dict[str, Any]) -> None
                        """
                        pass

                    class PlotReport(PyCommand):
                        """
                        PlotReport(TimestepSelection: Dict[str, Any], Title: str, XAxis: str, XAxisLabel: str, YAxisLabel: str) -> None
                        """
                        pass

                    class GetReport(PyCommand):
                        """
                        GetReport(TimestepSelection: Dict[str, Any]) -> List[float]
                        """
                        pass

                def __getitem__(self, key: str) -> _Reports:
                    return super().__getitem__(key)

            class View(PyNamedObjectContainer):
                class _View(PyMenu):
                    """
                    Singleton _View.
                    """
                    def __init__(self, service, rules, path):
                        self.Camera = self.__class__.Camera(service, rules, path + [("Camera", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        self.RestoreView = self.__class__.RestoreView(service, rules, "RestoreView", path)
                        super().__init__(service, rules, path)

                    class Camera(PyMenu):
                        """
                        Singleton Camera.
                        """
                        def __init__(self, service, rules, path):
                            self.UpVector = self.__class__.UpVector(service, rules, path + [("UpVector", "")])
                            self.Target = self.__class__.Target(service, rules, path + [("Target", "")])
                            self.Position = self.__class__.Position(service, rules, path + [("Position", "")])
                            self.Height = self.__class__.Height(service, rules, path + [("Height", "")])
                            self.Width = self.__class__.Width(service, rules, path + [("Width", "")])
                            self.Projection = self.__class__.Projection(service, rules, path + [("Projection", "")])
                            super().__init__(service, rules, path)

                        class UpVector(PyMenu):
                            """
                            Singleton UpVector.
                            """
                            def __init__(self, service, rules, path):
                                self.ZComponent = self.__class__.ZComponent(service, rules, path + [("ZComponent", "")])
                                self.YComponent = self.__class__.YComponent(service, rules, path + [("YComponent", "")])
                                self.XComponent = self.__class__.XComponent(service, rules, path + [("XComponent", "")])
                                super().__init__(service, rules, path)

                            class ZComponent(PyMenu):
                                """
                                Parameter ZComponent of value type float.
                                """
                                pass

                            class YComponent(PyMenu):
                                """
                                Parameter YComponent of value type float.
                                """
                                pass

                            class XComponent(PyMenu):
                                """
                                Parameter XComponent of value type float.
                                """
                                pass

                        class Target(PyMenu):
                            """
                            Singleton Target.
                            """
                            def __init__(self, service, rules, path):
                                self.ZComponent = self.__class__.ZComponent(service, rules, path + [("ZComponent", "")])
                                self.XComponent = self.__class__.XComponent(service, rules, path + [("XComponent", "")])
                                self.YComponent = self.__class__.YComponent(service, rules, path + [("YComponent", "")])
                                super().__init__(service, rules, path)

                            class ZComponent(PyMenu):
                                """
                                Parameter ZComponent of value type float.
                                """
                                pass

                            class XComponent(PyMenu):
                                """
                                Parameter XComponent of value type float.
                                """
                                pass

                            class YComponent(PyMenu):
                                """
                                Parameter YComponent of value type float.
                                """
                                pass

                        class Position(PyMenu):
                            """
                            Singleton Position.
                            """
                            def __init__(self, service, rules, path):
                                self.YComponent = self.__class__.YComponent(service, rules, path + [("YComponent", "")])
                                self.ZComponent = self.__class__.ZComponent(service, rules, path + [("ZComponent", "")])
                                self.XComponent = self.__class__.XComponent(service, rules, path + [("XComponent", "")])
                                super().__init__(service, rules, path)

                            class YComponent(PyMenu):
                                """
                                Parameter YComponent of value type float.
                                """
                                pass

                            class ZComponent(PyMenu):
                                """
                                Parameter ZComponent of value type float.
                                """
                                pass

                            class XComponent(PyMenu):
                                """
                                Parameter XComponent of value type float.
                                """
                                pass

                        class Height(PyMenu):
                            """
                            Parameter Height of value type float.
                            """
                            pass

                        class Width(PyMenu):
                            """
                            Parameter Width of value type float.
                            """
                            pass

                        class Projection(PyMenu):
                            """
                            Parameter Projection of value type str.
                            """
                            pass

                    class _name_(PyMenu):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                    class RestoreView(PyCommand):
                        """
                        RestoreView() -> bool
                        """
                        pass

                def __getitem__(self, key: str) -> _View:
                    return super().__getitem__(key)

            class SurfaceDefs(PyNamedObjectContainer):
                class _SurfaceDefs(PyMenu):
                    """
                    Singleton _SurfaceDefs.
                    """
                    def __init__(self, service, rules, path):
                        self.IsoClipSettings = self.__class__.IsoClipSettings(service, rules, path + [("IsoClipSettings", "")])
                        self.RakeSettings = self.__class__.RakeSettings(service, rules, path + [("RakeSettings", "")])
                        self.LineSettings = self.__class__.LineSettings(service, rules, path + [("LineSettings", "")])
                        self.ZoneSettings = self.__class__.ZoneSettings(service, rules, path + [("ZoneSettings", "")])
                        self.IsosurfaceSettings = self.__class__.IsosurfaceSettings(service, rules, path + [("IsosurfaceSettings", "")])
                        self.PointSettings = self.__class__.PointSettings(service, rules, path + [("PointSettings", "")])
                        self.PlaneSettings = self.__class__.PlaneSettings(service, rules, path + [("PlaneSettings", "")])
                        self.GroupName = self.__class__.GroupName(service, rules, path + [("GroupName", "")])
                        self.SurfaceDim = self.__class__.SurfaceDim(service, rules, path + [("SurfaceDim", "")])
                        self.SurfaceType = self.__class__.SurfaceType(service, rules, path + [("SurfaceType", "")])
                        self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        self.SurfaceId = self.__class__.SurfaceId(service, rules, path + [("SurfaceId", "")])
                        self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                        self.Display = self.__class__.Display(service, rules, "Display", path)
                        self.Ungroup = self.__class__.Ungroup(service, rules, "Ungroup", path)
                        super().__init__(service, rules, path)

                    class IsoClipSettings(PyMenu):
                        """
                        Singleton IsoClipSettings.
                        """
                        def __init__(self, service, rules, path):
                            self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                            self.Minimum = self.__class__.Minimum(service, rules, path + [("Minimum", "")])
                            self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                            self.Maximum = self.__class__.Maximum(service, rules, path + [("Maximum", "")])
                            self.UpdateMinMax = self.__class__.UpdateMinMax(service, rules, "UpdateMinMax", path)
                            super().__init__(service, rules, path)

                        class Field(PyMenu):
                            """
                            Parameter Field of value type str.
                            """
                            pass

                        class Minimum(PyMenu):
                            """
                            Parameter Minimum of value type float.
                            """
                            pass

                        class Surfaces(PyMenu):
                            """
                            Parameter Surfaces of value type List[str].
                            """
                            pass

                        class Maximum(PyMenu):
                            """
                            Parameter Maximum of value type float.
                            """
                            pass

                        class UpdateMinMax(PyCommand):
                            """
                            UpdateMinMax() -> None
                            """
                            pass

                    class RakeSettings(PyMenu):
                        """
                        Singleton RakeSettings.
                        """
                        def __init__(self, service, rules, path):
                            self.EndPoint = self.__class__.EndPoint(service, rules, path + [("EndPoint", "")])
                            self.StartPoint = self.__class__.StartPoint(service, rules, path + [("StartPoint", "")])
                            self.NumberOfPoints = self.__class__.NumberOfPoints(service, rules, path + [("NumberOfPoints", "")])
                            super().__init__(service, rules, path)

                        class EndPoint(PyMenu):
                            """
                            Singleton EndPoint.
                            """
                            def __init__(self, service, rules, path):
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                super().__init__(service, rules, path)

                            class Y(PyMenu):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class Z(PyMenu):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                            class X(PyMenu):
                                """
                                Parameter X of value type float.
                                """
                                pass

                        class StartPoint(PyMenu):
                            """
                            Singleton StartPoint.
                            """
                            def __init__(self, service, rules, path):
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                super().__init__(service, rules, path)

                            class X(PyMenu):
                                """
                                Parameter X of value type float.
                                """
                                pass

                            class Y(PyMenu):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class Z(PyMenu):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                        class NumberOfPoints(PyMenu):
                            """
                            Parameter NumberOfPoints of value type int.
                            """
                            pass

                    class LineSettings(PyMenu):
                        """
                        Singleton LineSettings.
                        """
                        def __init__(self, service, rules, path):
                            self.EndPoint = self.__class__.EndPoint(service, rules, path + [("EndPoint", "")])
                            self.StartPoint = self.__class__.StartPoint(service, rules, path + [("StartPoint", "")])
                            super().__init__(service, rules, path)

                        class EndPoint(PyMenu):
                            """
                            Singleton EndPoint.
                            """
                            def __init__(self, service, rules, path):
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                super().__init__(service, rules, path)

                            class Y(PyMenu):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class Z(PyMenu):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                            class X(PyMenu):
                                """
                                Parameter X of value type float.
                                """
                                pass

                        class StartPoint(PyMenu):
                            """
                            Singleton StartPoint.
                            """
                            def __init__(self, service, rules, path):
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                super().__init__(service, rules, path)

                            class X(PyMenu):
                                """
                                Parameter X of value type float.
                                """
                                pass

                            class Z(PyMenu):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                            class Y(PyMenu):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                    class ZoneSettings(PyMenu):
                        """
                        Singleton ZoneSettings.
                        """
                        def __init__(self, service, rules, path):
                            self.ZType = self.__class__.ZType(service, rules, path + [("ZType", "")])
                            self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                            self.ZId = self.__class__.ZId(service, rules, path + [("ZId", "")])
                            self.IdList = self.__class__.IdList(service, rules, path + [("IdList", "")])
                            super().__init__(service, rules, path)

                        class ZType(PyMenu):
                            """
                            Parameter ZType of value type str.
                            """
                            pass

                        class Type(PyMenu):
                            """
                            Parameter Type of value type str.
                            """
                            pass

                        class ZId(PyMenu):
                            """
                            Parameter ZId of value type int.
                            """
                            pass

                        class IdList(PyMenu):
                            """
                            Parameter IdList of value type List[int].
                            """
                            pass

                    class IsosurfaceSettings(PyMenu):
                        """
                        Singleton IsosurfaceSettings.
                        """
                        def __init__(self, service, rules, path):
                            self.RestrictToSpecificZones = self.__class__.RestrictToSpecificZones(service, rules, path + [("RestrictToSpecificZones", "")])
                            self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                            self.Minimum = self.__class__.Minimum(service, rules, path + [("Minimum", "")])
                            self.RestrictToSpecificSurfaces = self.__class__.RestrictToSpecificSurfaces(service, rules, path + [("RestrictToSpecificSurfaces", "")])
                            self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                            self.Zones = self.__class__.Zones(service, rules, path + [("Zones", "")])
                            self.IsoValue = self.__class__.IsoValue(service, rules, path + [("IsoValue", "")])
                            self.Maximum = self.__class__.Maximum(service, rules, path + [("Maximum", "")])
                            self.UpdateMinMax = self.__class__.UpdateMinMax(service, rules, "UpdateMinMax", path)
                            super().__init__(service, rules, path)

                        class RestrictToSpecificZones(PyMenu):
                            """
                            Parameter RestrictToSpecificZones of value type bool.
                            """
                            pass

                        class Field(PyMenu):
                            """
                            Parameter Field of value type str.
                            """
                            pass

                        class Minimum(PyMenu):
                            """
                            Parameter Minimum of value type float.
                            """
                            pass

                        class RestrictToSpecificSurfaces(PyMenu):
                            """
                            Parameter RestrictToSpecificSurfaces of value type bool.
                            """
                            pass

                        class Surfaces(PyMenu):
                            """
                            Parameter Surfaces of value type List[str].
                            """
                            pass

                        class Zones(PyMenu):
                            """
                            Parameter Zones of value type List[str].
                            """
                            pass

                        class IsoValue(PyMenu):
                            """
                            Parameter IsoValue of value type float.
                            """
                            pass

                        class Maximum(PyMenu):
                            """
                            Parameter Maximum of value type float.
                            """
                            pass

                        class UpdateMinMax(PyCommand):
                            """
                            UpdateMinMax() -> None
                            """
                            pass

                    class PointSettings(PyMenu):
                        """
                        Singleton PointSettings.
                        """
                        def __init__(self, service, rules, path):
                            self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                            self.LbClipping = self.__class__.LbClipping(service, rules, path + [("LbClipping", "")])
                            self.X = self.__class__.X(service, rules, path + [("X", "")])
                            self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                            super().__init__(service, rules, path)

                        class Z(PyMenu):
                            """
                            Parameter Z of value type float.
                            """
                            pass

                        class LbClipping(PyMenu):
                            """
                            Parameter LbClipping of value type bool.
                            """
                            pass

                        class X(PyMenu):
                            """
                            Parameter X of value type float.
                            """
                            pass

                        class Y(PyMenu):
                            """
                            Parameter Y of value type float.
                            """
                            pass

                    class PlaneSettings(PyMenu):
                        """
                        Singleton PlaneSettings.
                        """
                        def __init__(self, service, rules, path):
                            self.ThirdPoint = self.__class__.ThirdPoint(service, rules, path + [("ThirdPoint", "")])
                            self.SecondPoint = self.__class__.SecondPoint(service, rules, path + [("SecondPoint", "")])
                            self.Normal = self.__class__.Normal(service, rules, path + [("Normal", "")])
                            self.FirstPoint = self.__class__.FirstPoint(service, rules, path + [("FirstPoint", "")])
                            self.CreationMode = self.__class__.CreationMode(service, rules, path + [("CreationMode", "")])
                            self.X = self.__class__.X(service, rules, path + [("X", "")])
                            self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                            self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                            self.Bounded = self.__class__.Bounded(service, rules, path + [("Bounded", "")])
                            super().__init__(service, rules, path)

                        class ThirdPoint(PyMenu):
                            """
                            Singleton ThirdPoint.
                            """
                            def __init__(self, service, rules, path):
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                super().__init__(service, rules, path)

                            class Y(PyMenu):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class X(PyMenu):
                                """
                                Parameter X of value type float.
                                """
                                pass

                            class Z(PyMenu):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                        class SecondPoint(PyMenu):
                            """
                            Singleton SecondPoint.
                            """
                            def __init__(self, service, rules, path):
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                super().__init__(service, rules, path)

                            class Y(PyMenu):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class X(PyMenu):
                                """
                                Parameter X of value type float.
                                """
                                pass

                            class Z(PyMenu):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                        class Normal(PyMenu):
                            """
                            Singleton Normal.
                            """
                            def __init__(self, service, rules, path):
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                super().__init__(service, rules, path)

                            class Y(PyMenu):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class X(PyMenu):
                                """
                                Parameter X of value type float.
                                """
                                pass

                            class Z(PyMenu):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                        class FirstPoint(PyMenu):
                            """
                            Singleton FirstPoint.
                            """
                            def __init__(self, service, rules, path):
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                super().__init__(service, rules, path)

                            class X(PyMenu):
                                """
                                Parameter X of value type float.
                                """
                                pass

                            class Z(PyMenu):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                            class Y(PyMenu):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                        class CreationMode(PyMenu):
                            """
                            Parameter CreationMode of value type str.
                            """
                            pass

                        class X(PyMenu):
                            """
                            Parameter X of value type float.
                            """
                            pass

                        class Y(PyMenu):
                            """
                            Parameter Y of value type float.
                            """
                            pass

                        class Z(PyMenu):
                            """
                            Parameter Z of value type float.
                            """
                            pass

                        class Bounded(PyMenu):
                            """
                            Parameter Bounded of value type bool.
                            """
                            pass

                    class GroupName(PyMenu):
                        """
                        Parameter GroupName of value type str.
                        """
                        pass

                    class SurfaceDim(PyMenu):
                        """
                        Parameter SurfaceDim of value type List[str].
                        """
                        pass

                    class SurfaceType(PyMenu):
                        """
                        Parameter SurfaceType of value type str.
                        """
                        pass

                    class Surfaces(PyMenu):
                        """
                        Parameter Surfaces of value type List[str].
                        """
                        pass

                    class _name_(PyMenu):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                    class SurfaceId(PyMenu):
                        """
                        Parameter SurfaceId of value type int.
                        """
                        pass

                    class SaveImage(PyCommand):
                        """
                        SaveImage(FileName: str, Format: str, FileType: str, Coloring: str, Orientation: str, UseWhiteBackground: bool, Resolution: Dict[str, Any]) -> bool
                        """
                        pass

                    class Display(PyCommand):
                        """
                        Display() -> bool
                        """
                        pass

                    class Ungroup(PyCommand):
                        """
                        Ungroup() -> bool
                        """
                        pass

                def __getitem__(self, key: str) -> _SurfaceDefs:
                    return super().__getitem__(key)

            class ResultsExternalInfo(PyMenu):
                """
                Singleton ResultsExternalInfo.
                """
                def __init__(self, service, rules, path):
                    super().__init__(service, rules, path)

            class Graphics(PyMenu):
                """
                Singleton Graphics.
                """
                def __init__(self, service, rules, path):
                    self.Mesh = self.__class__.Mesh(service, rules, path + [("Mesh", "")])
                    self.TransientPlot = self.__class__.TransientPlot(service, rules, path + [("TransientPlot", "")])
                    self.Pathlines = self.__class__.Pathlines(service, rules, path + [("Pathlines", "")])
                    self.XYPlot = self.__class__.XYPlot(service, rules, path + [("XYPlot", "")])
                    self.ParticleTracks = self.__class__.ParticleTracks(service, rules, path + [("ParticleTracks", "")])
                    self.Scene = self.__class__.Scene(service, rules, path + [("Scene", "")])
                    self.Contour = self.__class__.Contour(service, rules, path + [("Contour", "")])
                    self.PeriodicInstances = self.__class__.PeriodicInstances(service, rules, path + [("PeriodicInstances", "")])
                    self.VolumeRender = self.__class__.VolumeRender(service, rules, path + [("VolumeRender", "")])
                    self.LIC = self.__class__.LIC(service, rules, path + [("LIC", "")])
                    self.Vector = self.__class__.Vector(service, rules, path + [("Vector", "")])
                    self.GridColors = self.__class__.GridColors(service, rules, path + [("GridColors", "")])
                    self.CameraSettings = self.__class__.CameraSettings(service, rules, path + [("CameraSettings", "")])
                    self.MirrorPlanes = self.__class__.MirrorPlanes(service, rules, path + [("MirrorPlanes", "")])
                    self.GraphicsCreationCount = self.__class__.GraphicsCreationCount(service, rules, path + [("GraphicsCreationCount", "")])
                    self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                    super().__init__(service, rules, path)

                class Mesh(PyNamedObjectContainer):
                    class _Mesh(PyMenu):
                        """
                        Singleton _Mesh.
                        """
                        def __init__(self, service, rules, path):
                            self.MeshColoring = self.__class__.MeshColoring(service, rules, path + [("MeshColoring", "")])
                            self.EdgeOptions = self.__class__.EdgeOptions(service, rules, path + [("EdgeOptions", "")])
                            self.Options = self.__class__.Options(service, rules, path + [("Options", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                            self.WindowId = self.__class__.WindowId(service, rules, path + [("WindowId", "")])
                            self.SyncStatus = self.__class__.SyncStatus(service, rules, path + [("SyncStatus", "")])
                            self.ShrinkFactor = self.__class__.ShrinkFactor(service, rules, path + [("ShrinkFactor", "")])
                            self.DisplayInViewport = self.__class__.DisplayInViewport(service, rules, "DisplayInViewport", path)
                            self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                            self.Display = self.__class__.Display(service, rules, "Display", path)
                            self.AddToViewport = self.__class__.AddToViewport(service, rules, "AddToViewport", path)
                            self.Pull = self.__class__.Pull(service, rules, "Pull", path)
                            self.Diff = self.__class__.Diff(service, rules, "Diff", path)
                            self.SaveAnimation = self.__class__.SaveAnimation(service, rules, "SaveAnimation", path)
                            self.Push = self.__class__.Push(service, rules, "Push", path)
                            super().__init__(service, rules, path)

                        class MeshColoring(PyMenu):
                            """
                            Singleton MeshColoring.
                            """
                            def __init__(self, service, rules, path):
                                self.ColorBy = self.__class__.ColorBy(service, rules, path + [("ColorBy", "")])
                                self.ColorNodesBy = self.__class__.ColorNodesBy(service, rules, path + [("ColorNodesBy", "")])
                                self.ColorEdgesBy = self.__class__.ColorEdgesBy(service, rules, path + [("ColorEdgesBy", "")])
                                self.Automatic = self.__class__.Automatic(service, rules, path + [("Automatic", "")])
                                self.ColorFacesBy = self.__class__.ColorFacesBy(service, rules, path + [("ColorFacesBy", "")])
                                super().__init__(service, rules, path)

                            class ColorBy(PyMenu):
                                """
                                Parameter ColorBy of value type str.
                                """
                                pass

                            class ColorNodesBy(PyMenu):
                                """
                                Parameter ColorNodesBy of value type str.
                                """
                                pass

                            class ColorEdgesBy(PyMenu):
                                """
                                Parameter ColorEdgesBy of value type str.
                                """
                                pass

                            class Automatic(PyMenu):
                                """
                                Parameter Automatic of value type bool.
                                """
                                pass

                            class ColorFacesBy(PyMenu):
                                """
                                Parameter ColorFacesBy of value type str.
                                """
                                pass

                        class EdgeOptions(PyMenu):
                            """
                            Singleton EdgeOptions.
                            """
                            def __init__(self, service, rules, path):
                                self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                                self.FeatureAngle = self.__class__.FeatureAngle(service, rules, path + [("FeatureAngle", "")])
                                super().__init__(service, rules, path)

                            class Type(PyMenu):
                                """
                                Parameter Type of value type str.
                                """
                                pass

                            class FeatureAngle(PyMenu):
                                """
                                Parameter FeatureAngle of value type float.
                                """
                                pass

                        class Options(PyMenu):
                            """
                            Singleton Options.
                            """
                            def __init__(self, service, rules, path):
                                self.Faces = self.__class__.Faces(service, rules, path + [("Faces", "")])
                                self.Partitions = self.__class__.Partitions(service, rules, path + [("Partitions", "")])
                                self.Nodes = self.__class__.Nodes(service, rules, path + [("Nodes", "")])
                                self.Overset = self.__class__.Overset(service, rules, path + [("Overset", "")])
                                self.Edges = self.__class__.Edges(service, rules, path + [("Edges", "")])
                                super().__init__(service, rules, path)

                            class Faces(PyMenu):
                                """
                                Parameter Faces of value type bool.
                                """
                                pass

                            class Partitions(PyMenu):
                                """
                                Parameter Partitions of value type bool.
                                """
                                pass

                            class Nodes(PyMenu):
                                """
                                Parameter Nodes of value type bool.
                                """
                                pass

                            class Overset(PyMenu):
                                """
                                Parameter Overset of value type bool.
                                """
                                pass

                            class Edges(PyMenu):
                                """
                                Parameter Edges of value type bool.
                                """
                                pass

                        class _name_(PyMenu):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                        class Surfaces(PyMenu):
                            """
                            Parameter Surfaces of value type List[str].
                            """
                            pass

                        class WindowId(PyMenu):
                            """
                            Parameter WindowId of value type int.
                            """
                            pass

                        class SyncStatus(PyMenu):
                            """
                            Parameter SyncStatus of value type str.
                            """
                            pass

                        class ShrinkFactor(PyMenu):
                            """
                            Parameter ShrinkFactor of value type float.
                            """
                            pass

                        class DisplayInViewport(PyCommand):
                            """
                            DisplayInViewport(Viewport: str) -> bool
                            """
                            pass

                        class SaveImage(PyCommand):
                            """
                            SaveImage(FileName: str, Format: str, FileType: str, Coloring: str, Orientation: str, UseWhiteBackground: bool, Resolution: Dict[str, Any]) -> bool
                            """
                            pass

                        class Display(PyCommand):
                            """
                            Display() -> bool
                            """
                            pass

                        class AddToViewport(PyCommand):
                            """
                            AddToViewport(Viewport: str) -> bool
                            """
                            pass

                        class Pull(PyCommand):
                            """
                            Pull() -> bool
                            """
                            pass

                        class Diff(PyCommand):
                            """
                            Diff() -> bool
                            """
                            pass

                        class SaveAnimation(PyCommand):
                            """
                            SaveAnimation(FileName: str, Format: str, FPS: float, AntiAliasingPasses: str, Quality: str, H264: bool, Compression: str, BitRate: int, JPegQuality: int, PPMFormat: str, UseWhiteBackground: bool, Orientation: str, Resolution: Dict[str, Any]) -> None
                            """
                            pass

                        class Push(PyCommand):
                            """
                            Push() -> bool
                            """
                            pass

                    def __getitem__(self, key: str) -> _Mesh:
                        return super().__getitem__(key)

                class TransientPlot(PyNamedObjectContainer):
                    class _TransientPlot(PyMenu):
                        """
                        Singleton _TransientPlot.
                        """
                        def __init__(self, service, rules, path):
                            self.ReportFile = self.__class__.ReportFile(service, rules, path + [("ReportFile", "")])
                            self.Axes = self.__class__.Axes(service, rules, path + [("Axes", "")])
                            self.TimestepSelection = self.__class__.TimestepSelection(service, rules, path + [("TimestepSelection", "")])
                            self.Curves = self.__class__.Curves(service, rules, path + [("Curves", "")])
                            self.XAxis = self.__class__.XAxis(service, rules, path + [("XAxis", "")])
                            self.Title = self.__class__.Title(service, rules, path + [("Title", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.XAxisLabel = self.__class__.XAxisLabel(service, rules, path + [("XAxisLabel", "")])
                            self.YAxisLabel = self.__class__.YAxisLabel(service, rules, path + [("YAxisLabel", "")])
                            self.Reports = self.__class__.Reports(service, rules, path + [("Reports", "")])
                            self.Print = self.__class__.Print(service, rules, "Print", path)
                            self.Plot = self.__class__.Plot(service, rules, "Plot", path)
                            self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                            self.Export = self.__class__.Export(service, rules, "Export", path)
                            super().__init__(service, rules, path)

                        class ReportFile(PyNamedObjectContainer):
                            class _ReportFile(PyMenu):
                                """
                                Singleton _ReportFile.
                                """
                                def __init__(self, service, rules, path):
                                    self.SelectedColumns = self.__class__.SelectedColumns(service, rules, path + [("SelectedColumns", "")])
                                    self.ListOfColumns = self.__class__.ListOfColumns(service, rules, path + [("ListOfColumns", "")])
                                    self.Filename = self.__class__.Filename(service, rules, path + [("Filename", "")])
                                    self.Label = self.__class__.Label(service, rules, path + [("Label", "")])
                                    self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                                    super().__init__(service, rules, path)

                                class SelectedColumns(PyMenu):
                                    """
                                    Parameter SelectedColumns of value type List[str].
                                    """
                                    pass

                                class ListOfColumns(PyMenu):
                                    """
                                    Parameter ListOfColumns of value type List[str].
                                    """
                                    pass

                                class Filename(PyMenu):
                                    """
                                    Parameter Filename of value type str.
                                    """
                                    pass

                                class Label(PyMenu):
                                    """
                                    Parameter Label of value type str.
                                    """
                                    pass

                                class _name_(PyMenu):
                                    """
                                    Parameter _name_ of value type str.
                                    """
                                    pass

                            def __getitem__(self, key: str) -> _ReportFile:
                                return super().__getitem__(key)

                        class Axes(PyMenu):
                            """
                            Singleton Axes.
                            """
                            def __init__(self, service, rules, path):
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                super().__init__(service, rules, path)

                            class Y(PyMenu):
                                """
                                Singleton Y.
                                """
                                def __init__(self, service, rules, path):
                                    self.MinorRules = self.__class__.MinorRules(service, rules, path + [("MinorRules", "")])
                                    self.MajorRules = self.__class__.MajorRules(service, rules, path + [("MajorRules", "")])
                                    self.Options = self.__class__.Options(service, rules, path + [("Options", "")])
                                    self.NumberFormat = self.__class__.NumberFormat(service, rules, path + [("NumberFormat", "")])
                                    self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                                    self.Label = self.__class__.Label(service, rules, path + [("Label", "")])
                                    super().__init__(service, rules, path)

                                class MinorRules(PyMenu):
                                    """
                                    Singleton MinorRules.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                        self.Weight = self.__class__.Weight(service, rules, path + [("Weight", "")])
                                        super().__init__(service, rules, path)

                                    class Color(PyMenu):
                                        """
                                        Parameter Color of value type str.
                                        """
                                        pass

                                    class Weight(PyMenu):
                                        """
                                        Parameter Weight of value type float.
                                        """
                                        pass

                                class MajorRules(PyMenu):
                                    """
                                    Singleton MajorRules.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                        self.Weight = self.__class__.Weight(service, rules, path + [("Weight", "")])
                                        super().__init__(service, rules, path)

                                    class Color(PyMenu):
                                        """
                                        Parameter Color of value type str.
                                        """
                                        pass

                                    class Weight(PyMenu):
                                        """
                                        Parameter Weight of value type float.
                                        """
                                        pass

                                class Options(PyMenu):
                                    """
                                    Singleton Options.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.MinorRules = self.__class__.MinorRules(service, rules, path + [("MinorRules", "")])
                                        self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
                                        self.MajorRules = self.__class__.MajorRules(service, rules, path + [("MajorRules", "")])
                                        self.Log = self.__class__.Log(service, rules, path + [("Log", "")])
                                        super().__init__(service, rules, path)

                                    class MinorRules(PyMenu):
                                        """
                                        Parameter MinorRules of value type bool.
                                        """
                                        pass

                                    class AutoRange(PyMenu):
                                        """
                                        Parameter AutoRange of value type bool.
                                        """
                                        pass

                                    class MajorRules(PyMenu):
                                        """
                                        Parameter MajorRules of value type bool.
                                        """
                                        pass

                                    class Log(PyMenu):
                                        """
                                        Parameter Log of value type bool.
                                        """
                                        pass

                                class NumberFormat(PyMenu):
                                    """
                                    Singleton NumberFormat.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.Precision = self.__class__.Precision(service, rules, path + [("Precision", "")])
                                        self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                                        super().__init__(service, rules, path)

                                    class Precision(PyMenu):
                                        """
                                        Parameter Precision of value type int.
                                        """
                                        pass

                                    class Type(PyMenu):
                                        """
                                        Parameter Type of value type str.
                                        """
                                        pass

                                class Range(PyMenu):
                                    """
                                    Singleton Range.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.Minimum = self.__class__.Minimum(service, rules, path + [("Minimum", "")])
                                        self.Maximum = self.__class__.Maximum(service, rules, path + [("Maximum", "")])
                                        super().__init__(service, rules, path)

                                    class Minimum(PyMenu):
                                        """
                                        Parameter Minimum of value type float.
                                        """
                                        pass

                                    class Maximum(PyMenu):
                                        """
                                        Parameter Maximum of value type float.
                                        """
                                        pass

                                class Label(PyMenu):
                                    """
                                    Parameter Label of value type str.
                                    """
                                    pass

                            class X(PyMenu):
                                """
                                Singleton X.
                                """
                                def __init__(self, service, rules, path):
                                    self.NumberFormat = self.__class__.NumberFormat(service, rules, path + [("NumberFormat", "")])
                                    self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                                    self.MajorRules = self.__class__.MajorRules(service, rules, path + [("MajorRules", "")])
                                    self.MinorRules = self.__class__.MinorRules(service, rules, path + [("MinorRules", "")])
                                    self.Options = self.__class__.Options(service, rules, path + [("Options", "")])
                                    self.Label = self.__class__.Label(service, rules, path + [("Label", "")])
                                    super().__init__(service, rules, path)

                                class NumberFormat(PyMenu):
                                    """
                                    Singleton NumberFormat.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                                        self.Precision = self.__class__.Precision(service, rules, path + [("Precision", "")])
                                        super().__init__(service, rules, path)

                                    class Type(PyMenu):
                                        """
                                        Parameter Type of value type str.
                                        """
                                        pass

                                    class Precision(PyMenu):
                                        """
                                        Parameter Precision of value type int.
                                        """
                                        pass

                                class Range(PyMenu):
                                    """
                                    Singleton Range.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.Maximum = self.__class__.Maximum(service, rules, path + [("Maximum", "")])
                                        self.Minimum = self.__class__.Minimum(service, rules, path + [("Minimum", "")])
                                        super().__init__(service, rules, path)

                                    class Maximum(PyMenu):
                                        """
                                        Parameter Maximum of value type float.
                                        """
                                        pass

                                    class Minimum(PyMenu):
                                        """
                                        Parameter Minimum of value type float.
                                        """
                                        pass

                                class MajorRules(PyMenu):
                                    """
                                    Singleton MajorRules.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.Weight = self.__class__.Weight(service, rules, path + [("Weight", "")])
                                        self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                        super().__init__(service, rules, path)

                                    class Weight(PyMenu):
                                        """
                                        Parameter Weight of value type float.
                                        """
                                        pass

                                    class Color(PyMenu):
                                        """
                                        Parameter Color of value type str.
                                        """
                                        pass

                                class MinorRules(PyMenu):
                                    """
                                    Singleton MinorRules.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.Weight = self.__class__.Weight(service, rules, path + [("Weight", "")])
                                        self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                        super().__init__(service, rules, path)

                                    class Weight(PyMenu):
                                        """
                                        Parameter Weight of value type float.
                                        """
                                        pass

                                    class Color(PyMenu):
                                        """
                                        Parameter Color of value type str.
                                        """
                                        pass

                                class Options(PyMenu):
                                    """
                                    Singleton Options.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.MajorRules = self.__class__.MajorRules(service, rules, path + [("MajorRules", "")])
                                        self.MinorRules = self.__class__.MinorRules(service, rules, path + [("MinorRules", "")])
                                        self.Log = self.__class__.Log(service, rules, path + [("Log", "")])
                                        self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
                                        super().__init__(service, rules, path)

                                    class MajorRules(PyMenu):
                                        """
                                        Parameter MajorRules of value type bool.
                                        """
                                        pass

                                    class MinorRules(PyMenu):
                                        """
                                        Parameter MinorRules of value type bool.
                                        """
                                        pass

                                    class Log(PyMenu):
                                        """
                                        Parameter Log of value type bool.
                                        """
                                        pass

                                    class AutoRange(PyMenu):
                                        """
                                        Parameter AutoRange of value type bool.
                                        """
                                        pass

                                class Label(PyMenu):
                                    """
                                    Parameter Label of value type str.
                                    """
                                    pass

                        class TimestepSelection(PyMenu):
                            """
                            Singleton TimestepSelection.
                            """
                            def __init__(self, service, rules, path):
                                self.End = self.__class__.End(service, rules, path + [("End", "")])
                                self.Increment = self.__class__.Increment(service, rules, path + [("Increment", "")])
                                self.Option = self.__class__.Option(service, rules, path + [("Option", "")])
                                self.Begin = self.__class__.Begin(service, rules, path + [("Begin", "")])
                                super().__init__(service, rules, path)

                            class End(PyMenu):
                                """
                                Parameter End of value type float.
                                """
                                pass

                            class Increment(PyMenu):
                                """
                                Parameter Increment of value type float.
                                """
                                pass

                            class Option(PyMenu):
                                """
                                Parameter Option of value type str.
                                """
                                pass

                            class Begin(PyMenu):
                                """
                                Parameter Begin of value type float.
                                """
                                pass

                        class Curves(PyMenu):
                            """
                            Singleton Curves.
                            """
                            def __init__(self, service, rules, path):
                                self.LineStyle = self.__class__.LineStyle(service, rules, path + [("LineStyle", "")])
                                self.MarkerStyle = self.__class__.MarkerStyle(service, rules, path + [("MarkerStyle", "")])
                                super().__init__(service, rules, path)

                            class LineStyle(PyMenu):
                                """
                                Singleton LineStyle.
                                """
                                def __init__(self, service, rules, path):
                                    self.Pattern = self.__class__.Pattern(service, rules, path + [("Pattern", "")])
                                    self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                    self.Weight = self.__class__.Weight(service, rules, path + [("Weight", "")])
                                    super().__init__(service, rules, path)

                                class Pattern(PyMenu):
                                    """
                                    Parameter Pattern of value type str.
                                    """
                                    pass

                                class Color(PyMenu):
                                    """
                                    Parameter Color of value type str.
                                    """
                                    pass

                                class Weight(PyMenu):
                                    """
                                    Parameter Weight of value type float.
                                    """
                                    pass

                            class MarkerStyle(PyMenu):
                                """
                                Singleton MarkerStyle.
                                """
                                def __init__(self, service, rules, path):
                                    self.Size = self.__class__.Size(service, rules, path + [("Size", "")])
                                    self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                    self.Symbol = self.__class__.Symbol(service, rules, path + [("Symbol", "")])
                                    super().__init__(service, rules, path)

                                class Size(PyMenu):
                                    """
                                    Parameter Size of value type float.
                                    """
                                    pass

                                class Color(PyMenu):
                                    """
                                    Parameter Color of value type str.
                                    """
                                    pass

                                class Symbol(PyMenu):
                                    """
                                    Parameter Symbol of value type str.
                                    """
                                    pass

                        class XAxis(PyMenu):
                            """
                            Parameter XAxis of value type str.
                            """
                            pass

                        class Title(PyMenu):
                            """
                            Parameter Title of value type str.
                            """
                            pass

                        class _name_(PyMenu):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                        class XAxisLabel(PyMenu):
                            """
                            Parameter XAxisLabel of value type str.
                            """
                            pass

                        class YAxisLabel(PyMenu):
                            """
                            Parameter YAxisLabel of value type str.
                            """
                            pass

                        class Reports(PyMenu):
                            """
                            Parameter Reports of value type List[str].
                            """
                            pass

                        class Print(PyCommand):
                            """
                            Print() -> None
                            """
                            pass

                        class Plot(PyCommand):
                            """
                            Plot() -> None
                            """
                            pass

                        class SaveImage(PyCommand):
                            """
                            SaveImage(FileName: str, Format: str, FileType: str, Coloring: str, Orientation: str, UseWhiteBackground: bool, Resolution: Dict[str, Any]) -> bool
                            """
                            pass

                        class Export(PyCommand):
                            """
                            Export(FileName: str) -> None
                            """
                            pass

                    def __getitem__(self, key: str) -> _TransientPlot:
                        return super().__getitem__(key)

                class Pathlines(PyNamedObjectContainer):
                    class _Pathlines(PyMenu):
                        """
                        Singleton _Pathlines.
                        """
                        def __init__(self, service, rules, path):
                            self.AccuracyControl = self.__class__.AccuracyControl(service, rules, path + [("AccuracyControl", "")])
                            self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                            self.Options = self.__class__.Options(service, rules, path + [("Options", "")])
                            self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                            self.Style = self.__class__.Style(service, rules, path + [("Style", "")])
                            self.Plot = self.__class__.Plot(service, rules, path + [("Plot", "")])
                            self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                            self.DrawMesh = self.__class__.DrawMesh(service, rules, path + [("DrawMesh", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.UID = self.__class__.UID(service, rules, path + [("UID", "")])
                            self.VelocityDomain = self.__class__.VelocityDomain(service, rules, path + [("VelocityDomain", "")])
                            self.OnZone = self.__class__.OnZone(service, rules, path + [("OnZone", "")])
                            self.Skip = self.__class__.Skip(service, rules, path + [("Skip", "")])
                            self.OverlayedMesh = self.__class__.OverlayedMesh(service, rules, path + [("OverlayedMesh", "")])
                            self.Step = self.__class__.Step(service, rules, path + [("Step", "")])
                            self.SyncStatus = self.__class__.SyncStatus(service, rules, path + [("SyncStatus", "")])
                            self.Coarsen = self.__class__.Coarsen(service, rules, path + [("Coarsen", "")])
                            self.PathlinesField = self.__class__.PathlinesField(service, rules, path + [("PathlinesField", "")])
                            self.WindowId = self.__class__.WindowId(service, rules, path + [("WindowId", "")])
                            self.Push = self.__class__.Push(service, rules, "Push", path)
                            self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                            self.Display = self.__class__.Display(service, rules, "Display", path)
                            self.Pull = self.__class__.Pull(service, rules, "Pull", path)
                            self.Diff = self.__class__.Diff(service, rules, "Diff", path)
                            super().__init__(service, rules, path)

                        class AccuracyControl(PyMenu):
                            """
                            Singleton AccuracyControl.
                            """
                            def __init__(self, service, rules, path):
                                self.AccuracyControlOn = self.__class__.AccuracyControlOn(service, rules, path + [("AccuracyControlOn", "")])
                                self.Tolerance = self.__class__.Tolerance(service, rules, path + [("Tolerance", "")])
                                self.StepSize = self.__class__.StepSize(service, rules, path + [("StepSize", "")])
                                super().__init__(service, rules, path)

                            class AccuracyControlOn(PyMenu):
                                """
                                Parameter AccuracyControlOn of value type bool.
                                """
                                pass

                            class Tolerance(PyMenu):
                                """
                                Parameter Tolerance of value type float.
                                """
                                pass

                            class StepSize(PyMenu):
                                """
                                Parameter StepSize of value type float.
                                """
                                pass

                        class Range(PyMenu):
                            """
                            Singleton Range.
                            """
                            def __init__(self, service, rules, path):
                                self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
                                self.MaxValue = self.__class__.MaxValue(service, rules, path + [("MaxValue", "")])
                                self.MinValue = self.__class__.MinValue(service, rules, path + [("MinValue", "")])
                                super().__init__(service, rules, path)

                            class AutoRange(PyMenu):
                                """
                                Parameter AutoRange of value type bool.
                                """
                                pass

                            class MaxValue(PyMenu):
                                """
                                Parameter MaxValue of value type float.
                                """
                                pass

                            class MinValue(PyMenu):
                                """
                                Parameter MinValue of value type float.
                                """
                                pass

                        class Options(PyMenu):
                            """
                            Singleton Options.
                            """
                            def __init__(self, service, rules, path):
                                self.NodeValues = self.__class__.NodeValues(service, rules, path + [("NodeValues", "")])
                                self.Relative = self.__class__.Relative(service, rules, path + [("Relative", "")])
                                self.Reverse = self.__class__.Reverse(service, rules, path + [("Reverse", "")])
                                self.OilFlow = self.__class__.OilFlow(service, rules, path + [("OilFlow", "")])
                                super().__init__(service, rules, path)

                            class NodeValues(PyMenu):
                                """
                                Parameter NodeValues of value type bool.
                                """
                                pass

                            class Relative(PyMenu):
                                """
                                Parameter Relative of value type bool.
                                """
                                pass

                            class Reverse(PyMenu):
                                """
                                Parameter Reverse of value type bool.
                                """
                                pass

                            class OilFlow(PyMenu):
                                """
                                Parameter OilFlow of value type bool.
                                """
                                pass

                        class ColorMap(PyMenu):
                            """
                            Singleton ColorMap.
                            """
                            def __init__(self, service, rules, path):
                                self.Position = self.__class__.Position(service, rules, path + [("Position", "")])
                                self.Visible = self.__class__.Visible(service, rules, path + [("Visible", "")])
                                self.Size = self.__class__.Size(service, rules, path + [("Size", "")])
                                self.Skip = self.__class__.Skip(service, rules, path + [("Skip", "")])
                                self.IsLogScale = self.__class__.IsLogScale(service, rules, path + [("IsLogScale", "")])
                                self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                                self.Precision = self.__class__.Precision(service, rules, path + [("Precision", "")])
                                self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                                self.ShowAll = self.__class__.ShowAll(service, rules, path + [("ShowAll", "")])
                                super().__init__(service, rules, path)

                            class Position(PyMenu):
                                """
                                Parameter Position of value type str.
                                """
                                pass

                            class Visible(PyMenu):
                                """
                                Parameter Visible of value type bool.
                                """
                                pass

                            class Size(PyMenu):
                                """
                                Parameter Size of value type int.
                                """
                                pass

                            class Skip(PyMenu):
                                """
                                Parameter Skip of value type int.
                                """
                                pass

                            class IsLogScale(PyMenu):
                                """
                                Parameter IsLogScale of value type bool.
                                """
                                pass

                            class Type(PyMenu):
                                """
                                Parameter Type of value type str.
                                """
                                pass

                            class Precision(PyMenu):
                                """
                                Parameter Precision of value type int.
                                """
                                pass

                            class ColorMap(PyMenu):
                                """
                                Parameter ColorMap of value type str.
                                """
                                pass

                            class ShowAll(PyMenu):
                                """
                                Parameter ShowAll of value type bool.
                                """
                                pass

                        class Style(PyMenu):
                            """
                            Singleton Style.
                            """
                            def __init__(self, service, rules, path):
                                self.Ribbon = self.__class__.Ribbon(service, rules, path + [("Ribbon", "")])
                                self.SphereSize = self.__class__.SphereSize(service, rules, path + [("SphereSize", "")])
                                self.Style = self.__class__.Style(service, rules, path + [("Style", "")])
                                self.Radius = self.__class__.Radius(service, rules, path + [("Radius", "")])
                                self.ArrowScale = self.__class__.ArrowScale(service, rules, path + [("ArrowScale", "")])
                                self.MarkerSize = self.__class__.MarkerSize(service, rules, path + [("MarkerSize", "")])
                                self.SphereLod = self.__class__.SphereLod(service, rules, path + [("SphereLod", "")])
                                self.ArrowSpace = self.__class__.ArrowSpace(service, rules, path + [("ArrowSpace", "")])
                                self.LineWidth = self.__class__.LineWidth(service, rules, path + [("LineWidth", "")])
                                super().__init__(service, rules, path)

                            class Ribbon(PyMenu):
                                """
                                Singleton Ribbon.
                                """
                                def __init__(self, service, rules, path):
                                    self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                                    self.ScaleFactor = self.__class__.ScaleFactor(service, rules, path + [("ScaleFactor", "")])
                                    super().__init__(service, rules, path)

                                class Field(PyMenu):
                                    """
                                    Parameter Field of value type str.
                                    """
                                    pass

                                class ScaleFactor(PyMenu):
                                    """
                                    Parameter ScaleFactor of value type float.
                                    """
                                    pass

                            class SphereSize(PyMenu):
                                """
                                Parameter SphereSize of value type float.
                                """
                                pass

                            class Style(PyMenu):
                                """
                                Parameter Style of value type str.
                                """
                                pass

                            class Radius(PyMenu):
                                """
                                Parameter Radius of value type float.
                                """
                                pass

                            class ArrowScale(PyMenu):
                                """
                                Parameter ArrowScale of value type float.
                                """
                                pass

                            class MarkerSize(PyMenu):
                                """
                                Parameter MarkerSize of value type float.
                                """
                                pass

                            class SphereLod(PyMenu):
                                """
                                Parameter SphereLod of value type int.
                                """
                                pass

                            class ArrowSpace(PyMenu):
                                """
                                Parameter ArrowSpace of value type float.
                                """
                                pass

                            class LineWidth(PyMenu):
                                """
                                Parameter LineWidth of value type float.
                                """
                                pass

                        class Plot(PyMenu):
                            """
                            Singleton Plot.
                            """
                            def __init__(self, service, rules, path):
                                self.Enabled = self.__class__.Enabled(service, rules, path + [("Enabled", "")])
                                self.XAxisFunction = self.__class__.XAxisFunction(service, rules, path + [("XAxisFunction", "")])
                                super().__init__(service, rules, path)

                            class Enabled(PyMenu):
                                """
                                Parameter Enabled of value type bool.
                                """
                                pass

                            class XAxisFunction(PyMenu):
                                """
                                Parameter XAxisFunction of value type str.
                                """
                                pass

                        class Surfaces(PyMenu):
                            """
                            Parameter Surfaces of value type List[str].
                            """
                            pass

                        class DrawMesh(PyMenu):
                            """
                            Parameter DrawMesh of value type bool.
                            """
                            pass

                        class _name_(PyMenu):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                        class UID(PyMenu):
                            """
                            Parameter UID of value type str.
                            """
                            pass

                        class VelocityDomain(PyMenu):
                            """
                            Parameter VelocityDomain of value type str.
                            """
                            pass

                        class OnZone(PyMenu):
                            """
                            Parameter OnZone of value type List[str].
                            """
                            pass

                        class Skip(PyMenu):
                            """
                            Parameter Skip of value type int.
                            """
                            pass

                        class OverlayedMesh(PyMenu):
                            """
                            Parameter OverlayedMesh of value type str.
                            """
                            pass

                        class Step(PyMenu):
                            """
                            Parameter Step of value type int.
                            """
                            pass

                        class SyncStatus(PyMenu):
                            """
                            Parameter SyncStatus of value type str.
                            """
                            pass

                        class Coarsen(PyMenu):
                            """
                            Parameter Coarsen of value type int.
                            """
                            pass

                        class PathlinesField(PyMenu):
                            """
                            Parameter PathlinesField of value type str.
                            """
                            pass

                        class WindowId(PyMenu):
                            """
                            Parameter WindowId of value type int.
                            """
                            pass

                        class Push(PyCommand):
                            """
                            Push() -> bool
                            """
                            pass

                        class SaveImage(PyCommand):
                            """
                            SaveImage(FileName: str, Format: str, FileType: str, Coloring: str, Orientation: str, UseWhiteBackground: bool, Resolution: Dict[str, Any]) -> bool
                            """
                            pass

                        class Display(PyCommand):
                            """
                            Display() -> bool
                            """
                            pass

                        class Pull(PyCommand):
                            """
                            Pull() -> bool
                            """
                            pass

                        class Diff(PyCommand):
                            """
                            Diff() -> bool
                            """
                            pass

                    def __getitem__(self, key: str) -> _Pathlines:
                        return super().__getitem__(key)

                class XYPlot(PyNamedObjectContainer):
                    class _XYPlot(PyMenu):
                        """
                        Singleton _XYPlot.
                        """
                        def __init__(self, service, rules, path):
                            self.Options = self.__class__.Options(service, rules, path + [("Options", "")])
                            self.Curves = self.__class__.Curves(service, rules, path + [("Curves", "")])
                            self.DirectionVectorInternal = self.__class__.DirectionVectorInternal(service, rules, path + [("DirectionVectorInternal", "")])
                            self.Axes = self.__class__.Axes(service, rules, path + [("Axes", "")])
                            self.XAxisFunction = self.__class__.XAxisFunction(service, rules, path + [("XAxisFunction", "")])
                            self.YAxisFunction = self.__class__.YAxisFunction(service, rules, path + [("YAxisFunction", "")])
                            self.SyncStatus = self.__class__.SyncStatus(service, rules, path + [("SyncStatus", "")])
                            self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                            self.UID = self.__class__.UID(service, rules, path + [("UID", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.WindowId = self.__class__.WindowId(service, rules, path + [("WindowId", "")])
                            self.Pull = self.__class__.Pull(service, rules, "Pull", path)
                            self.Diff = self.__class__.Diff(service, rules, "Diff", path)
                            self.Push = self.__class__.Push(service, rules, "Push", path)
                            self.Plot = self.__class__.Plot(service, rules, "Plot", path)
                            self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                            self.ExportData = self.__class__.ExportData(service, rules, "ExportData", path)
                            super().__init__(service, rules, path)

                        class Options(PyMenu):
                            """
                            Singleton Options.
                            """
                            def __init__(self, service, rules, path):
                                self.NodeValues = self.__class__.NodeValues(service, rules, path + [("NodeValues", "")])
                                super().__init__(service, rules, path)

                            class NodeValues(PyMenu):
                                """
                                Parameter NodeValues of value type bool.
                                """
                                pass

                        class Curves(PyMenu):
                            """
                            Singleton Curves.
                            """
                            def __init__(self, service, rules, path):
                                self.MarkerStyle = self.__class__.MarkerStyle(service, rules, path + [("MarkerStyle", "")])
                                self.LineStyle = self.__class__.LineStyle(service, rules, path + [("LineStyle", "")])
                                super().__init__(service, rules, path)

                            class MarkerStyle(PyMenu):
                                """
                                Singleton MarkerStyle.
                                """
                                def __init__(self, service, rules, path):
                                    self.Symbol = self.__class__.Symbol(service, rules, path + [("Symbol", "")])
                                    self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                    self.Size = self.__class__.Size(service, rules, path + [("Size", "")])
                                    super().__init__(service, rules, path)

                                class Symbol(PyMenu):
                                    """
                                    Parameter Symbol of value type str.
                                    """
                                    pass

                                class Color(PyMenu):
                                    """
                                    Parameter Color of value type str.
                                    """
                                    pass

                                class Size(PyMenu):
                                    """
                                    Parameter Size of value type float.
                                    """
                                    pass

                            class LineStyle(PyMenu):
                                """
                                Singleton LineStyle.
                                """
                                def __init__(self, service, rules, path):
                                    self.Pattern = self.__class__.Pattern(service, rules, path + [("Pattern", "")])
                                    self.Weight = self.__class__.Weight(service, rules, path + [("Weight", "")])
                                    self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                    super().__init__(service, rules, path)

                                class Pattern(PyMenu):
                                    """
                                    Parameter Pattern of value type str.
                                    """
                                    pass

                                class Weight(PyMenu):
                                    """
                                    Parameter Weight of value type float.
                                    """
                                    pass

                                class Color(PyMenu):
                                    """
                                    Parameter Color of value type str.
                                    """
                                    pass

                        class DirectionVectorInternal(PyMenu):
                            """
                            Singleton DirectionVectorInternal.
                            """
                            def __init__(self, service, rules, path):
                                self.XComponent = self.__class__.XComponent(service, rules, path + [("XComponent", "")])
                                self.YComponent = self.__class__.YComponent(service, rules, path + [("YComponent", "")])
                                self.ZComponent = self.__class__.ZComponent(service, rules, path + [("ZComponent", "")])
                                super().__init__(service, rules, path)

                            class XComponent(PyMenu):
                                """
                                Parameter XComponent of value type float.
                                """
                                pass

                            class YComponent(PyMenu):
                                """
                                Parameter YComponent of value type float.
                                """
                                pass

                            class ZComponent(PyMenu):
                                """
                                Parameter ZComponent of value type float.
                                """
                                pass

                        class Axes(PyMenu):
                            """
                            Singleton Axes.
                            """
                            def __init__(self, service, rules, path):
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                super().__init__(service, rules, path)

                            class Y(PyMenu):
                                """
                                Singleton Y.
                                """
                                def __init__(self, service, rules, path):
                                    self.NumberFormat = self.__class__.NumberFormat(service, rules, path + [("NumberFormat", "")])
                                    self.Options = self.__class__.Options(service, rules, path + [("Options", "")])
                                    self.MinorRules = self.__class__.MinorRules(service, rules, path + [("MinorRules", "")])
                                    self.MajorRules = self.__class__.MajorRules(service, rules, path + [("MajorRules", "")])
                                    self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                                    self.Label = self.__class__.Label(service, rules, path + [("Label", "")])
                                    super().__init__(service, rules, path)

                                class NumberFormat(PyMenu):
                                    """
                                    Singleton NumberFormat.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.Precision = self.__class__.Precision(service, rules, path + [("Precision", "")])
                                        self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                                        super().__init__(service, rules, path)

                                    class Precision(PyMenu):
                                        """
                                        Parameter Precision of value type int.
                                        """
                                        pass

                                    class Type(PyMenu):
                                        """
                                        Parameter Type of value type str.
                                        """
                                        pass

                                class Options(PyMenu):
                                    """
                                    Singleton Options.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
                                        self.Log = self.__class__.Log(service, rules, path + [("Log", "")])
                                        self.MinorRules = self.__class__.MinorRules(service, rules, path + [("MinorRules", "")])
                                        self.MajorRules = self.__class__.MajorRules(service, rules, path + [("MajorRules", "")])
                                        super().__init__(service, rules, path)

                                    class AutoRange(PyMenu):
                                        """
                                        Parameter AutoRange of value type bool.
                                        """
                                        pass

                                    class Log(PyMenu):
                                        """
                                        Parameter Log of value type bool.
                                        """
                                        pass

                                    class MinorRules(PyMenu):
                                        """
                                        Parameter MinorRules of value type bool.
                                        """
                                        pass

                                    class MajorRules(PyMenu):
                                        """
                                        Parameter MajorRules of value type bool.
                                        """
                                        pass

                                class MinorRules(PyMenu):
                                    """
                                    Singleton MinorRules.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.Weight = self.__class__.Weight(service, rules, path + [("Weight", "")])
                                        self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                        super().__init__(service, rules, path)

                                    class Weight(PyMenu):
                                        """
                                        Parameter Weight of value type float.
                                        """
                                        pass

                                    class Color(PyMenu):
                                        """
                                        Parameter Color of value type str.
                                        """
                                        pass

                                class MajorRules(PyMenu):
                                    """
                                    Singleton MajorRules.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                        self.Weight = self.__class__.Weight(service, rules, path + [("Weight", "")])
                                        super().__init__(service, rules, path)

                                    class Color(PyMenu):
                                        """
                                        Parameter Color of value type str.
                                        """
                                        pass

                                    class Weight(PyMenu):
                                        """
                                        Parameter Weight of value type float.
                                        """
                                        pass

                                class Range(PyMenu):
                                    """
                                    Singleton Range.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.Minimum = self.__class__.Minimum(service, rules, path + [("Minimum", "")])
                                        self.Maximum = self.__class__.Maximum(service, rules, path + [("Maximum", "")])
                                        super().__init__(service, rules, path)

                                    class Minimum(PyMenu):
                                        """
                                        Parameter Minimum of value type float.
                                        """
                                        pass

                                    class Maximum(PyMenu):
                                        """
                                        Parameter Maximum of value type float.
                                        """
                                        pass

                                class Label(PyMenu):
                                    """
                                    Parameter Label of value type str.
                                    """
                                    pass

                            class X(PyMenu):
                                """
                                Singleton X.
                                """
                                def __init__(self, service, rules, path):
                                    self.NumberFormat = self.__class__.NumberFormat(service, rules, path + [("NumberFormat", "")])
                                    self.MinorRules = self.__class__.MinorRules(service, rules, path + [("MinorRules", "")])
                                    self.Options = self.__class__.Options(service, rules, path + [("Options", "")])
                                    self.MajorRules = self.__class__.MajorRules(service, rules, path + [("MajorRules", "")])
                                    self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                                    self.Label = self.__class__.Label(service, rules, path + [("Label", "")])
                                    super().__init__(service, rules, path)

                                class NumberFormat(PyMenu):
                                    """
                                    Singleton NumberFormat.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                                        self.Precision = self.__class__.Precision(service, rules, path + [("Precision", "")])
                                        super().__init__(service, rules, path)

                                    class Type(PyMenu):
                                        """
                                        Parameter Type of value type str.
                                        """
                                        pass

                                    class Precision(PyMenu):
                                        """
                                        Parameter Precision of value type int.
                                        """
                                        pass

                                class MinorRules(PyMenu):
                                    """
                                    Singleton MinorRules.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.Weight = self.__class__.Weight(service, rules, path + [("Weight", "")])
                                        self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                        super().__init__(service, rules, path)

                                    class Weight(PyMenu):
                                        """
                                        Parameter Weight of value type float.
                                        """
                                        pass

                                    class Color(PyMenu):
                                        """
                                        Parameter Color of value type str.
                                        """
                                        pass

                                class Options(PyMenu):
                                    """
                                    Singleton Options.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.Log = self.__class__.Log(service, rules, path + [("Log", "")])
                                        self.MinorRules = self.__class__.MinorRules(service, rules, path + [("MinorRules", "")])
                                        self.MajorRules = self.__class__.MajorRules(service, rules, path + [("MajorRules", "")])
                                        self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
                                        super().__init__(service, rules, path)

                                    class Log(PyMenu):
                                        """
                                        Parameter Log of value type bool.
                                        """
                                        pass

                                    class MinorRules(PyMenu):
                                        """
                                        Parameter MinorRules of value type bool.
                                        """
                                        pass

                                    class MajorRules(PyMenu):
                                        """
                                        Parameter MajorRules of value type bool.
                                        """
                                        pass

                                    class AutoRange(PyMenu):
                                        """
                                        Parameter AutoRange of value type bool.
                                        """
                                        pass

                                class MajorRules(PyMenu):
                                    """
                                    Singleton MajorRules.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                        self.Weight = self.__class__.Weight(service, rules, path + [("Weight", "")])
                                        super().__init__(service, rules, path)

                                    class Color(PyMenu):
                                        """
                                        Parameter Color of value type str.
                                        """
                                        pass

                                    class Weight(PyMenu):
                                        """
                                        Parameter Weight of value type float.
                                        """
                                        pass

                                class Range(PyMenu):
                                    """
                                    Singleton Range.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.Maximum = self.__class__.Maximum(service, rules, path + [("Maximum", "")])
                                        self.Minimum = self.__class__.Minimum(service, rules, path + [("Minimum", "")])
                                        super().__init__(service, rules, path)

                                    class Maximum(PyMenu):
                                        """
                                        Parameter Maximum of value type float.
                                        """
                                        pass

                                    class Minimum(PyMenu):
                                        """
                                        Parameter Minimum of value type float.
                                        """
                                        pass

                                class Label(PyMenu):
                                    """
                                    Parameter Label of value type str.
                                    """
                                    pass

                        class XAxisFunction(PyMenu):
                            """
                            Singleton XAxisFunction.
                            """
                            def __init__(self, service, rules, path):
                                self.DirectionVector = self.__class__.DirectionVector(service, rules, path + [("DirectionVector", "")])
                                self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                                self.XAxisFunctionInternal = self.__class__.XAxisFunctionInternal(service, rules, path + [("XAxisFunctionInternal", "")])
                                self.PositionOnCurrentAxis = self.__class__.PositionOnCurrentAxis(service, rules, path + [("PositionOnCurrentAxis", "")])
                                super().__init__(service, rules, path)

                            class DirectionVector(PyMenu):
                                """
                                Singleton DirectionVector.
                                """
                                def __init__(self, service, rules, path):
                                    self.ZComponent = self.__class__.ZComponent(service, rules, path + [("ZComponent", "")])
                                    self.YComponent = self.__class__.YComponent(service, rules, path + [("YComponent", "")])
                                    self.XComponent = self.__class__.XComponent(service, rules, path + [("XComponent", "")])
                                    super().__init__(service, rules, path)

                                class ZComponent(PyMenu):
                                    """
                                    Parameter ZComponent of value type float.
                                    """
                                    pass

                                class YComponent(PyMenu):
                                    """
                                    Parameter YComponent of value type float.
                                    """
                                    pass

                                class XComponent(PyMenu):
                                    """
                                    Parameter XComponent of value type float.
                                    """
                                    pass

                            class Field(PyMenu):
                                """
                                Parameter Field of value type str.
                                """
                                pass

                            class XAxisFunctionInternal(PyMenu):
                                """
                                Parameter XAxisFunctionInternal of value type str.
                                """
                                pass

                            class PositionOnCurrentAxis(PyMenu):
                                """
                                Parameter PositionOnCurrentAxis of value type bool.
                                """
                                pass

                        class YAxisFunction(PyMenu):
                            """
                            Singleton YAxisFunction.
                            """
                            def __init__(self, service, rules, path):
                                self.DirectionVector = self.__class__.DirectionVector(service, rules, path + [("DirectionVector", "")])
                                self.YAxisFunctionInternal = self.__class__.YAxisFunctionInternal(service, rules, path + [("YAxisFunctionInternal", "")])
                                self.PositionOnCurrentAxis = self.__class__.PositionOnCurrentAxis(service, rules, path + [("PositionOnCurrentAxis", "")])
                                self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                                super().__init__(service, rules, path)

                            class DirectionVector(PyMenu):
                                """
                                Singleton DirectionVector.
                                """
                                def __init__(self, service, rules, path):
                                    self.XComponent = self.__class__.XComponent(service, rules, path + [("XComponent", "")])
                                    self.YComponent = self.__class__.YComponent(service, rules, path + [("YComponent", "")])
                                    self.ZComponent = self.__class__.ZComponent(service, rules, path + [("ZComponent", "")])
                                    super().__init__(service, rules, path)

                                class XComponent(PyMenu):
                                    """
                                    Parameter XComponent of value type float.
                                    """
                                    pass

                                class YComponent(PyMenu):
                                    """
                                    Parameter YComponent of value type float.
                                    """
                                    pass

                                class ZComponent(PyMenu):
                                    """
                                    Parameter ZComponent of value type float.
                                    """
                                    pass

                            class YAxisFunctionInternal(PyMenu):
                                """
                                Parameter YAxisFunctionInternal of value type str.
                                """
                                pass

                            class PositionOnCurrentAxis(PyMenu):
                                """
                                Parameter PositionOnCurrentAxis of value type bool.
                                """
                                pass

                            class Field(PyMenu):
                                """
                                Parameter Field of value type str.
                                """
                                pass

                        class SyncStatus(PyMenu):
                            """
                            Parameter SyncStatus of value type str.
                            """
                            pass

                        class Surfaces(PyMenu):
                            """
                            Parameter Surfaces of value type List[str].
                            """
                            pass

                        class UID(PyMenu):
                            """
                            Parameter UID of value type str.
                            """
                            pass

                        class _name_(PyMenu):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                        class WindowId(PyMenu):
                            """
                            Parameter WindowId of value type int.
                            """
                            pass

                        class Pull(PyCommand):
                            """
                            Pull() -> bool
                            """
                            pass

                        class Diff(PyCommand):
                            """
                            Diff() -> bool
                            """
                            pass

                        class Push(PyCommand):
                            """
                            Push() -> bool
                            """
                            pass

                        class Plot(PyCommand):
                            """
                            Plot() -> bool
                            """
                            pass

                        class SaveImage(PyCommand):
                            """
                            SaveImage(FileName: str, Format: str, FileType: str, Coloring: str, Orientation: str, UseWhiteBackground: bool, Resolution: Dict[str, Any]) -> bool
                            """
                            pass

                        class ExportData(PyCommand):
                            """
                            ExportData(FileName: str) -> bool
                            """
                            pass

                    def __getitem__(self, key: str) -> _XYPlot:
                        return super().__getitem__(key)

                class ParticleTracks(PyNamedObjectContainer):
                    class _ParticleTracks(PyMenu):
                        """
                        Singleton _ParticleTracks.
                        """
                        def __init__(self, service, rules, path):
                            self.Plot = self.__class__.Plot(service, rules, path + [("Plot", "")])
                            self.VectorStyle = self.__class__.VectorStyle(service, rules, path + [("VectorStyle", "")])
                            self.Style = self.__class__.Style(service, rules, path + [("Style", "")])
                            self.Filter = self.__class__.Filter(service, rules, path + [("Filter", "")])
                            self.TrackSingleParticleStream = self.__class__.TrackSingleParticleStream(service, rules, path + [("TrackSingleParticleStream", "")])
                            self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                            self.Options = self.__class__.Options(service, rules, path + [("Options", "")])
                            self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                            self.Injections = self.__class__.Injections(service, rules, path + [("Injections", "")])
                            self.WindowId = self.__class__.WindowId(service, rules, path + [("WindowId", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.FreeStreamParticles = self.__class__.FreeStreamParticles(service, rules, path + [("FreeStreamParticles", "")])
                            self.OverlayedMesh = self.__class__.OverlayedMesh(service, rules, path + [("OverlayedMesh", "")])
                            self.ParticleTracksField = self.__class__.ParticleTracksField(service, rules, path + [("ParticleTracksField", "")])
                            self.SyncStatus = self.__class__.SyncStatus(service, rules, path + [("SyncStatus", "")])
                            self.Coarsen = self.__class__.Coarsen(service, rules, path + [("Coarsen", "")])
                            self.Skip = self.__class__.Skip(service, rules, path + [("Skip", "")])
                            self.TrackPDFParticles = self.__class__.TrackPDFParticles(service, rules, path + [("TrackPDFParticles", "")])
                            self.DrawMesh = self.__class__.DrawMesh(service, rules, path + [("DrawMesh", "")])
                            self.WallFilmParticles = self.__class__.WallFilmParticles(service, rules, path + [("WallFilmParticles", "")])
                            self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                            self.SaveAnimation = self.__class__.SaveAnimation(service, rules, "SaveAnimation", path)
                            self.Pull = self.__class__.Pull(service, rules, "Pull", path)
                            self.Diff = self.__class__.Diff(service, rules, "Diff", path)
                            self.Display = self.__class__.Display(service, rules, "Display", path)
                            self.Push = self.__class__.Push(service, rules, "Push", path)
                            super().__init__(service, rules, path)

                        class Plot(PyMenu):
                            """
                            Singleton Plot.
                            """
                            def __init__(self, service, rules, path):
                                self.Enabled = self.__class__.Enabled(service, rules, path + [("Enabled", "")])
                                self.XAxisFunction = self.__class__.XAxisFunction(service, rules, path + [("XAxisFunction", "")])
                                super().__init__(service, rules, path)

                            class Enabled(PyMenu):
                                """
                                Parameter Enabled of value type bool.
                                """
                                pass

                            class XAxisFunction(PyMenu):
                                """
                                Parameter XAxisFunction of value type str.
                                """
                                pass

                        class VectorStyle(PyMenu):
                            """
                            Singleton VectorStyle.
                            """
                            def __init__(self, service, rules, path):
                                self.VectorAttribute = self.__class__.VectorAttribute(service, rules, path + [("VectorAttribute", "")])
                                self.Style = self.__class__.Style(service, rules, path + [("Style", "")])
                                super().__init__(service, rules, path)

                            class VectorAttribute(PyMenu):
                                """
                                Singleton VectorAttribute.
                                """
                                def __init__(self, service, rules, path):
                                    self.VariableLength = self.__class__.VariableLength(service, rules, path + [("VariableLength", "")])
                                    self.Length = self.__class__.Length(service, rules, path + [("Length", "")])
                                    self.LengthToHeadRatio = self.__class__.LengthToHeadRatio(service, rules, path + [("LengthToHeadRatio", "")])
                                    self.VectorsOf = self.__class__.VectorsOf(service, rules, path + [("VectorsOf", "")])
                                    self.ConstantColor = self.__class__.ConstantColor(service, rules, path + [("ConstantColor", "")])
                                    self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                    self.ScaleFactor = self.__class__.ScaleFactor(service, rules, path + [("ScaleFactor", "")])
                                    self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                                    super().__init__(service, rules, path)

                                class VariableLength(PyMenu):
                                    """
                                    Parameter VariableLength of value type bool.
                                    """
                                    pass

                                class Length(PyMenu):
                                    """
                                    Parameter Length of value type float.
                                    """
                                    pass

                                class LengthToHeadRatio(PyMenu):
                                    """
                                    Parameter LengthToHeadRatio of value type float.
                                    """
                                    pass

                                class VectorsOf(PyMenu):
                                    """
                                    Parameter VectorsOf of value type str.
                                    """
                                    pass

                                class ConstantColor(PyMenu):
                                    """
                                    Parameter ConstantColor of value type bool.
                                    """
                                    pass

                                class Color(PyMenu):
                                    """
                                    Parameter Color of value type str.
                                    """
                                    pass

                                class ScaleFactor(PyMenu):
                                    """
                                    Parameter ScaleFactor of value type float.
                                    """
                                    pass

                                class Field(PyMenu):
                                    """
                                    Parameter Field of value type str.
                                    """
                                    pass

                            class Style(PyMenu):
                                """
                                Parameter Style of value type str.
                                """
                                pass

                        class Style(PyMenu):
                            """
                            Singleton Style.
                            """
                            def __init__(self, service, rules, path):
                                self.Ribbon = self.__class__.Ribbon(service, rules, path + [("Ribbon", "")])
                                self.Sphere = self.__class__.Sphere(service, rules, path + [("Sphere", "")])
                                self.Radius = self.__class__.Radius(service, rules, path + [("Radius", "")])
                                self.Style = self.__class__.Style(service, rules, path + [("Style", "")])
                                self.MarkerSize = self.__class__.MarkerSize(service, rules, path + [("MarkerSize", "")])
                                self.ArrowSpace = self.__class__.ArrowSpace(service, rules, path + [("ArrowSpace", "")])
                                self.LineWidth = self.__class__.LineWidth(service, rules, path + [("LineWidth", "")])
                                self.ArrowScale = self.__class__.ArrowScale(service, rules, path + [("ArrowScale", "")])
                                super().__init__(service, rules, path)

                            class Ribbon(PyMenu):
                                """
                                Singleton Ribbon.
                                """
                                def __init__(self, service, rules, path):
                                    self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                                    self.ScaleFactor = self.__class__.ScaleFactor(service, rules, path + [("ScaleFactor", "")])
                                    super().__init__(service, rules, path)

                                class Field(PyMenu):
                                    """
                                    Parameter Field of value type str.
                                    """
                                    pass

                                class ScaleFactor(PyMenu):
                                    """
                                    Parameter ScaleFactor of value type float.
                                    """
                                    pass

                            class Sphere(PyMenu):
                                """
                                Singleton Sphere.
                                """
                                def __init__(self, service, rules, path):
                                    self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                                    self.SphereField = self.__class__.SphereField(service, rules, path + [("SphereField", "")])
                                    self.SphereSize = self.__class__.SphereSize(service, rules, path + [("SphereSize", "")])
                                    self.SphereLod = self.__class__.SphereLod(service, rules, path + [("SphereLod", "")])
                                    self.ScaleFactor = self.__class__.ScaleFactor(service, rules, path + [("ScaleFactor", "")])
                                    self.VariableSize = self.__class__.VariableSize(service, rules, path + [("VariableSize", "")])
                                    super().__init__(service, rules, path)

                                class Range(PyMenu):
                                    """
                                    Singleton Range.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.MinValue = self.__class__.MinValue(service, rules, path + [("MinValue", "")])
                                        self.MaxValue = self.__class__.MaxValue(service, rules, path + [("MaxValue", "")])
                                        self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
                                        super().__init__(service, rules, path)

                                    class MinValue(PyMenu):
                                        """
                                        Parameter MinValue of value type float.
                                        """
                                        pass

                                    class MaxValue(PyMenu):
                                        """
                                        Parameter MaxValue of value type float.
                                        """
                                        pass

                                    class AutoRange(PyMenu):
                                        """
                                        Parameter AutoRange of value type bool.
                                        """
                                        pass

                                class SphereField(PyMenu):
                                    """
                                    Parameter SphereField of value type str.
                                    """
                                    pass

                                class SphereSize(PyMenu):
                                    """
                                    Parameter SphereSize of value type float.
                                    """
                                    pass

                                class SphereLod(PyMenu):
                                    """
                                    Parameter SphereLod of value type int.
                                    """
                                    pass

                                class ScaleFactor(PyMenu):
                                    """
                                    Parameter ScaleFactor of value type float.
                                    """
                                    pass

                                class VariableSize(PyMenu):
                                    """
                                    Parameter VariableSize of value type bool.
                                    """
                                    pass

                            class Radius(PyMenu):
                                """
                                Parameter Radius of value type float.
                                """
                                pass

                            class Style(PyMenu):
                                """
                                Parameter Style of value type str.
                                """
                                pass

                            class MarkerSize(PyMenu):
                                """
                                Parameter MarkerSize of value type float.
                                """
                                pass

                            class ArrowSpace(PyMenu):
                                """
                                Parameter ArrowSpace of value type float.
                                """
                                pass

                            class LineWidth(PyMenu):
                                """
                                Parameter LineWidth of value type float.
                                """
                                pass

                            class ArrowScale(PyMenu):
                                """
                                Parameter ArrowScale of value type float.
                                """
                                pass

                        class Filter(PyMenu):
                            """
                            Singleton Filter.
                            """
                            def __init__(self, service, rules, path):
                                self.Enabled = self.__class__.Enabled(service, rules, path + [("Enabled", "")])
                                self.MinValue = self.__class__.MinValue(service, rules, path + [("MinValue", "")])
                                self.Inside = self.__class__.Inside(service, rules, path + [("Inside", "")])
                                self.MaxValue = self.__class__.MaxValue(service, rules, path + [("MaxValue", "")])
                                self.FilterField = self.__class__.FilterField(service, rules, path + [("FilterField", "")])
                                super().__init__(service, rules, path)

                            class Enabled(PyMenu):
                                """
                                Parameter Enabled of value type bool.
                                """
                                pass

                            class MinValue(PyMenu):
                                """
                                Parameter MinValue of value type float.
                                """
                                pass

                            class Inside(PyMenu):
                                """
                                Parameter Inside of value type bool.
                                """
                                pass

                            class MaxValue(PyMenu):
                                """
                                Parameter MaxValue of value type float.
                                """
                                pass

                            class FilterField(PyMenu):
                                """
                                Parameter FilterField of value type str.
                                """
                                pass

                        class TrackSingleParticleStream(PyMenu):
                            """
                            Singleton TrackSingleParticleStream.
                            """
                            def __init__(self, service, rules, path):
                                self.StreamId = self.__class__.StreamId(service, rules, path + [("StreamId", "")])
                                self.Enabled = self.__class__.Enabled(service, rules, path + [("Enabled", "")])
                                super().__init__(service, rules, path)

                            class StreamId(PyMenu):
                                """
                                Parameter StreamId of value type int.
                                """
                                pass

                            class Enabled(PyMenu):
                                """
                                Parameter Enabled of value type bool.
                                """
                                pass

                        class ColorMap(PyMenu):
                            """
                            Singleton ColorMap.
                            """
                            def __init__(self, service, rules, path):
                                self.Size = self.__class__.Size(service, rules, path + [("Size", "")])
                                self.IsLogScale = self.__class__.IsLogScale(service, rules, path + [("IsLogScale", "")])
                                self.Position = self.__class__.Position(service, rules, path + [("Position", "")])
                                self.Visible = self.__class__.Visible(service, rules, path + [("Visible", "")])
                                self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                                self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                                self.ShowAll = self.__class__.ShowAll(service, rules, path + [("ShowAll", "")])
                                self.Precision = self.__class__.Precision(service, rules, path + [("Precision", "")])
                                self.Skip = self.__class__.Skip(service, rules, path + [("Skip", "")])
                                super().__init__(service, rules, path)

                            class Size(PyMenu):
                                """
                                Parameter Size of value type int.
                                """
                                pass

                            class IsLogScale(PyMenu):
                                """
                                Parameter IsLogScale of value type bool.
                                """
                                pass

                            class Position(PyMenu):
                                """
                                Parameter Position of value type str.
                                """
                                pass

                            class Visible(PyMenu):
                                """
                                Parameter Visible of value type bool.
                                """
                                pass

                            class Type(PyMenu):
                                """
                                Parameter Type of value type str.
                                """
                                pass

                            class ColorMap(PyMenu):
                                """
                                Parameter ColorMap of value type str.
                                """
                                pass

                            class ShowAll(PyMenu):
                                """
                                Parameter ShowAll of value type bool.
                                """
                                pass

                            class Precision(PyMenu):
                                """
                                Parameter Precision of value type int.
                                """
                                pass

                            class Skip(PyMenu):
                                """
                                Parameter Skip of value type int.
                                """
                                pass

                        class Options(PyMenu):
                            """
                            Singleton Options.
                            """
                            def __init__(self, service, rules, path):
                                self.NodeValues = self.__class__.NodeValues(service, rules, path + [("NodeValues", "")])
                                super().__init__(service, rules, path)

                            class NodeValues(PyMenu):
                                """
                                Parameter NodeValues of value type bool.
                                """
                                pass

                        class Range(PyMenu):
                            """
                            Singleton Range.
                            """
                            def __init__(self, service, rules, path):
                                self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
                                self.MinValue = self.__class__.MinValue(service, rules, path + [("MinValue", "")])
                                self.MaxValue = self.__class__.MaxValue(service, rules, path + [("MaxValue", "")])
                                super().__init__(service, rules, path)

                            class AutoRange(PyMenu):
                                """
                                Parameter AutoRange of value type bool.
                                """
                                pass

                            class MinValue(PyMenu):
                                """
                                Parameter MinValue of value type float.
                                """
                                pass

                            class MaxValue(PyMenu):
                                """
                                Parameter MaxValue of value type float.
                                """
                                pass

                        class Injections(PyMenu):
                            """
                            Parameter Injections of value type List[str].
                            """
                            pass

                        class WindowId(PyMenu):
                            """
                            Parameter WindowId of value type int.
                            """
                            pass

                        class _name_(PyMenu):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                        class FreeStreamParticles(PyMenu):
                            """
                            Parameter FreeStreamParticles of value type bool.
                            """
                            pass

                        class OverlayedMesh(PyMenu):
                            """
                            Parameter OverlayedMesh of value type str.
                            """
                            pass

                        class ParticleTracksField(PyMenu):
                            """
                            Parameter ParticleTracksField of value type str.
                            """
                            pass

                        class SyncStatus(PyMenu):
                            """
                            Parameter SyncStatus of value type str.
                            """
                            pass

                        class Coarsen(PyMenu):
                            """
                            Parameter Coarsen of value type int.
                            """
                            pass

                        class Skip(PyMenu):
                            """
                            Parameter Skip of value type int.
                            """
                            pass

                        class TrackPDFParticles(PyMenu):
                            """
                            Parameter TrackPDFParticles of value type bool.
                            """
                            pass

                        class DrawMesh(PyMenu):
                            """
                            Parameter DrawMesh of value type bool.
                            """
                            pass

                        class WallFilmParticles(PyMenu):
                            """
                            Parameter WallFilmParticles of value type bool.
                            """
                            pass

                        class SaveImage(PyCommand):
                            """
                            SaveImage(FileName: str, Format: str, FileType: str, Coloring: str, Orientation: str, UseWhiteBackground: bool, Resolution: Dict[str, Any]) -> bool
                            """
                            pass

                        class SaveAnimation(PyCommand):
                            """
                            SaveAnimation(FileName: str, Format: str, FPS: float, AntiAliasingPasses: str, Quality: str, H264: bool, Compression: str, BitRate: int, JPegQuality: int, PPMFormat: str, UseWhiteBackground: bool, Orientation: str, Resolution: Dict[str, Any]) -> None
                            """
                            pass

                        class Pull(PyCommand):
                            """
                            Pull() -> bool
                            """
                            pass

                        class Diff(PyCommand):
                            """
                            Diff() -> bool
                            """
                            pass

                        class Display(PyCommand):
                            """
                            Display() -> bool
                            """
                            pass

                        class Push(PyCommand):
                            """
                            Push() -> bool
                            """
                            pass

                    def __getitem__(self, key: str) -> _ParticleTracks:
                        return super().__getitem__(key)

                class Scene(PyNamedObjectContainer):
                    class _Scene(PyMenu):
                        """
                        Singleton _Scene.
                        """
                        def __init__(self, service, rules, path):
                            self.GraphicsObjects = self.__class__.GraphicsObjects(service, rules, path + [("GraphicsObjects", "")])
                            self.WindowId = self.__class__.WindowId(service, rules, path + [("WindowId", "")])
                            self.SyncStatus = self.__class__.SyncStatus(service, rules, path + [("SyncStatus", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.SaveAnimation = self.__class__.SaveAnimation(service, rules, "SaveAnimation", path)
                            self.Push = self.__class__.Push(service, rules, "Push", path)
                            self.Pull = self.__class__.Pull(service, rules, "Pull", path)
                            self.Display = self.__class__.Display(service, rules, "Display", path)
                            self.Diff = self.__class__.Diff(service, rules, "Diff", path)
                            self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                            super().__init__(service, rules, path)

                        class GraphicsObjects(PyMenu):
                            """
                            Parameter GraphicsObjects of value type Dict[str, Any].
                            """
                            pass

                        class WindowId(PyMenu):
                            """
                            Parameter WindowId of value type int.
                            """
                            pass

                        class SyncStatus(PyMenu):
                            """
                            Parameter SyncStatus of value type str.
                            """
                            pass

                        class _name_(PyMenu):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                        class SaveAnimation(PyCommand):
                            """
                            SaveAnimation(FileName: str, Format: str, FPS: float, AntiAliasingPasses: str, Quality: str, H264: bool, Compression: str, BitRate: int, JPegQuality: int, PPMFormat: str, UseWhiteBackground: bool, Orientation: str, Resolution: Dict[str, Any]) -> None
                            """
                            pass

                        class Push(PyCommand):
                            """
                            Push() -> bool
                            """
                            pass

                        class Pull(PyCommand):
                            """
                            Pull() -> bool
                            """
                            pass

                        class Display(PyCommand):
                            """
                            Display() -> bool
                            """
                            pass

                        class Diff(PyCommand):
                            """
                            Diff() -> bool
                            """
                            pass

                        class SaveImage(PyCommand):
                            """
                            SaveImage(FileName: str, Format: str, FileType: str, Coloring: str, Orientation: str, UseWhiteBackground: bool, Resolution: Dict[str, Any]) -> bool
                            """
                            pass

                    def __getitem__(self, key: str) -> _Scene:
                        return super().__getitem__(key)

                class Contour(PyNamedObjectContainer):
                    class _Contour(PyMenu):
                        """
                        Singleton _Contour.
                        """
                        def __init__(self, service, rules, path):
                            self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                            self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                            self.Filled = self.__class__.Filled(service, rules, path + [("Filled", "")])
                            self.OverlayedMesh = self.__class__.OverlayedMesh(service, rules, path + [("OverlayedMesh", "")])
                            self.SyncStatus = self.__class__.SyncStatus(service, rules, path + [("SyncStatus", "")])
                            self.NodeValues = self.__class__.NodeValues(service, rules, path + [("NodeValues", "")])
                            self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                            self.DrawMesh = self.__class__.DrawMesh(service, rules, path + [("DrawMesh", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.WindowId = self.__class__.WindowId(service, rules, path + [("WindowId", "")])
                            self.Coloring = self.__class__.Coloring(service, rules, path + [("Coloring", "")])
                            self.BoundaryValues = self.__class__.BoundaryValues(service, rules, path + [("BoundaryValues", "")])
                            self.ContourLines = self.__class__.ContourLines(service, rules, path + [("ContourLines", "")])
                            self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                            self.DisplayInViewport = self.__class__.DisplayInViewport(service, rules, "DisplayInViewport", path)
                            self.Diff = self.__class__.Diff(service, rules, "Diff", path)
                            self.Pull = self.__class__.Pull(service, rules, "Pull", path)
                            self.Push = self.__class__.Push(service, rules, "Push", path)
                            self.Display = self.__class__.Display(service, rules, "Display", path)
                            self.UpdateMinMax = self.__class__.UpdateMinMax(service, rules, "UpdateMinMax", path)
                            self.SaveAnimation = self.__class__.SaveAnimation(service, rules, "SaveAnimation", path)
                            self.AddToViewport = self.__class__.AddToViewport(service, rules, "AddToViewport", path)
                            self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                            super().__init__(service, rules, path)

                        class ColorMap(PyMenu):
                            """
                            Singleton ColorMap.
                            """
                            def __init__(self, service, rules, path):
                                self.Position = self.__class__.Position(service, rules, path + [("Position", "")])
                                self.Size = self.__class__.Size(service, rules, path + [("Size", "")])
                                self.Precision = self.__class__.Precision(service, rules, path + [("Precision", "")])
                                self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                                self.Visible = self.__class__.Visible(service, rules, path + [("Visible", "")])
                                self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                                self.IsLogScale = self.__class__.IsLogScale(service, rules, path + [("IsLogScale", "")])
                                self.ShowAll = self.__class__.ShowAll(service, rules, path + [("ShowAll", "")])
                                self.Skip = self.__class__.Skip(service, rules, path + [("Skip", "")])
                                super().__init__(service, rules, path)

                            class Position(PyMenu):
                                """
                                Parameter Position of value type str.
                                """
                                pass

                            class Size(PyMenu):
                                """
                                Parameter Size of value type int.
                                """
                                pass

                            class Precision(PyMenu):
                                """
                                Parameter Precision of value type int.
                                """
                                pass

                            class Type(PyMenu):
                                """
                                Parameter Type of value type str.
                                """
                                pass

                            class Visible(PyMenu):
                                """
                                Parameter Visible of value type bool.
                                """
                                pass

                            class ColorMap(PyMenu):
                                """
                                Parameter ColorMap of value type str.
                                """
                                pass

                            class IsLogScale(PyMenu):
                                """
                                Parameter IsLogScale of value type bool.
                                """
                                pass

                            class ShowAll(PyMenu):
                                """
                                Parameter ShowAll of value type bool.
                                """
                                pass

                            class Skip(PyMenu):
                                """
                                Parameter Skip of value type int.
                                """
                                pass

                        class Range(PyMenu):
                            """
                            Singleton Range.
                            """
                            def __init__(self, service, rules, path):
                                self.ClipToRange = self.__class__.ClipToRange(service, rules, path + [("ClipToRange", "")])
                                self.GlobalRange = self.__class__.GlobalRange(service, rules, path + [("GlobalRange", "")])
                                self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
                                self.MinValue = self.__class__.MinValue(service, rules, path + [("MinValue", "")])
                                self.MaxValue = self.__class__.MaxValue(service, rules, path + [("MaxValue", "")])
                                super().__init__(service, rules, path)

                            class ClipToRange(PyMenu):
                                """
                                Parameter ClipToRange of value type bool.
                                """
                                pass

                            class GlobalRange(PyMenu):
                                """
                                Parameter GlobalRange of value type bool.
                                """
                                pass

                            class AutoRange(PyMenu):
                                """
                                Parameter AutoRange of value type bool.
                                """
                                pass

                            class MinValue(PyMenu):
                                """
                                Parameter MinValue of value type float.
                                """
                                pass

                            class MaxValue(PyMenu):
                                """
                                Parameter MaxValue of value type float.
                                """
                                pass

                        class Filled(PyMenu):
                            """
                            Parameter Filled of value type bool.
                            """
                            pass

                        class OverlayedMesh(PyMenu):
                            """
                            Parameter OverlayedMesh of value type str.
                            """
                            pass

                        class SyncStatus(PyMenu):
                            """
                            Parameter SyncStatus of value type str.
                            """
                            pass

                        class NodeValues(PyMenu):
                            """
                            Parameter NodeValues of value type bool.
                            """
                            pass

                        class Field(PyMenu):
                            """
                            Parameter Field of value type str.
                            """
                            pass

                        class DrawMesh(PyMenu):
                            """
                            Parameter DrawMesh of value type bool.
                            """
                            pass

                        class _name_(PyMenu):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                        class WindowId(PyMenu):
                            """
                            Parameter WindowId of value type int.
                            """
                            pass

                        class Coloring(PyMenu):
                            """
                            Parameter Coloring of value type str.
                            """
                            pass

                        class BoundaryValues(PyMenu):
                            """
                            Parameter BoundaryValues of value type bool.
                            """
                            pass

                        class ContourLines(PyMenu):
                            """
                            Parameter ContourLines of value type bool.
                            """
                            pass

                        class Surfaces(PyMenu):
                            """
                            Parameter Surfaces of value type List[str].
                            """
                            pass

                        class DisplayInViewport(PyCommand):
                            """
                            DisplayInViewport(Viewport: str) -> bool
                            """
                            pass

                        class Diff(PyCommand):
                            """
                            Diff() -> bool
                            """
                            pass

                        class Pull(PyCommand):
                            """
                            Pull() -> bool
                            """
                            pass

                        class Push(PyCommand):
                            """
                            Push() -> bool
                            """
                            pass

                        class Display(PyCommand):
                            """
                            Display() -> bool
                            """
                            pass

                        class UpdateMinMax(PyCommand):
                            """
                            UpdateMinMax() -> None
                            """
                            pass

                        class SaveAnimation(PyCommand):
                            """
                            SaveAnimation(FileName: str, Format: str, FPS: float, AntiAliasingPasses: str, Quality: str, H264: bool, Compression: str, BitRate: int, JPegQuality: int, PPMFormat: str, UseWhiteBackground: bool, Orientation: str, Resolution: Dict[str, Any]) -> None
                            """
                            pass

                        class AddToViewport(PyCommand):
                            """
                            AddToViewport(Viewport: str) -> bool
                            """
                            pass

                        class SaveImage(PyCommand):
                            """
                            SaveImage(FileName: str, Format: str, FileType: str, Coloring: str, Orientation: str, UseWhiteBackground: bool, Resolution: Dict[str, Any]) -> bool
                            """
                            pass

                    def __getitem__(self, key: str) -> _Contour:
                        return super().__getitem__(key)

                class PeriodicInstances(PyNamedObjectContainer):
                    class _PeriodicInstances(PyMenu):
                        """
                        Singleton _PeriodicInstances.
                        """
                        def __init__(self, service, rules, path):
                            self.TranslationVector = self.__class__.TranslationVector(service, rules, path + [("TranslationVector", "")])
                            self.PointOnAxis = self.__class__.PointOnAxis(service, rules, path + [("PointOnAxis", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                            self.AllSurfaces = self.__class__.AllSurfaces(service, rules, path + [("AllSurfaces", "")])
                            self.NumberOfRepeats = self.__class__.NumberOfRepeats(service, rules, path + [("NumberOfRepeats", "")])
                            self.PeriodicType = self.__class__.PeriodicType(service, rules, path + [("PeriodicType", "")])
                            self.Angle = self.__class__.Angle(service, rules, path + [("Angle", "")])
                            self.RotationAxis = self.__class__.RotationAxis(service, rules, path + [("RotationAxis", "")])
                            self.NoOfSections = self.__class__.NoOfSections(service, rules, path + [("NoOfSections", "")])
                            super().__init__(service, rules, path)

                        class TranslationVector(PyMenu):
                            """
                            Singleton TranslationVector.
                            """
                            def __init__(self, service, rules, path):
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                super().__init__(service, rules, path)

                            class Z(PyMenu):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                            class Y(PyMenu):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class X(PyMenu):
                                """
                                Parameter X of value type float.
                                """
                                pass

                        class PointOnAxis(PyMenu):
                            """
                            Singleton PointOnAxis.
                            """
                            def __init__(self, service, rules, path):
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                super().__init__(service, rules, path)

                            class X(PyMenu):
                                """
                                Parameter X of value type float.
                                """
                                pass

                            class Y(PyMenu):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class Z(PyMenu):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                        class _name_(PyMenu):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                        class Surfaces(PyMenu):
                            """
                            Parameter Surfaces of value type List[str].
                            """
                            pass

                        class AllSurfaces(PyMenu):
                            """
                            Parameter AllSurfaces of value type bool.
                            """
                            pass

                        class NumberOfRepeats(PyMenu):
                            """
                            Parameter NumberOfRepeats of value type int.
                            """
                            pass

                        class PeriodicType(PyMenu):
                            """
                            Parameter PeriodicType of value type str.
                            """
                            pass

                        class Angle(PyMenu):
                            """
                            Parameter Angle of value type float.
                            """
                            pass

                        class RotationAxis(PyMenu):
                            """
                            Parameter RotationAxis of value type str.
                            """
                            pass

                        class NoOfSections(PyMenu):
                            """
                            Parameter NoOfSections of value type int.
                            """
                            pass

                    def __getitem__(self, key: str) -> _PeriodicInstances:
                        return super().__getitem__(key)

                class VolumeRender(PyNamedObjectContainer):
                    class _VolumeRender(PyMenu):
                        """
                        Singleton _VolumeRender.
                        """
                        def __init__(self, service, rules, path):
                            self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                            self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                            self.Grid = self.__class__.Grid(service, rules, path + [("Grid", "")])
                            self.Bound = self.__class__.Bound(service, rules, path + [("Bound", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.Quality = self.__class__.Quality(service, rules, path + [("Quality", "")])
                            self.AlphaScale = self.__class__.AlphaScale(service, rules, path + [("AlphaScale", "")])
                            self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                            self.Transparencies = self.__class__.Transparencies(service, rules, path + [("Transparencies", "")])
                            self.Volumes = self.__class__.Volumes(service, rules, path + [("Volumes", "")])
                            self.UpdateMinMax = self.__class__.UpdateMinMax(service, rules, "UpdateMinMax", path)
                            self.DisplayInViewport = self.__class__.DisplayInViewport(service, rules, "DisplayInViewport", path)
                            self.AddToViewport = self.__class__.AddToViewport(service, rules, "AddToViewport", path)
                            self.Display = self.__class__.Display(service, rules, "Display", path)
                            self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                            self.SaveAnimation = self.__class__.SaveAnimation(service, rules, "SaveAnimation", path)
                            super().__init__(service, rules, path)

                        class Range(PyMenu):
                            """
                            Singleton Range.
                            """
                            def __init__(self, service, rules, path):
                                self.MaxValue = self.__class__.MaxValue(service, rules, path + [("MaxValue", "")])
                                self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
                                self.MinValue = self.__class__.MinValue(service, rules, path + [("MinValue", "")])
                                self.GlobalRange = self.__class__.GlobalRange(service, rules, path + [("GlobalRange", "")])
                                self.ClipToRange = self.__class__.ClipToRange(service, rules, path + [("ClipToRange", "")])
                                super().__init__(service, rules, path)

                            class MaxValue(PyMenu):
                                """
                                Parameter MaxValue of value type float.
                                """
                                pass

                            class AutoRange(PyMenu):
                                """
                                Parameter AutoRange of value type bool.
                                """
                                pass

                            class MinValue(PyMenu):
                                """
                                Parameter MinValue of value type float.
                                """
                                pass

                            class GlobalRange(PyMenu):
                                """
                                Parameter GlobalRange of value type bool.
                                """
                                pass

                            class ClipToRange(PyMenu):
                                """
                                Parameter ClipToRange of value type bool.
                                """
                                pass

                        class ColorMap(PyMenu):
                            """
                            Singleton ColorMap.
                            """
                            def __init__(self, service, rules, path):
                                self.Visible = self.__class__.Visible(service, rules, path + [("Visible", "")])
                                self.Precision = self.__class__.Precision(service, rules, path + [("Precision", "")])
                                self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                                self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                                self.ShowAll = self.__class__.ShowAll(service, rules, path + [("ShowAll", "")])
                                self.IsLogScale = self.__class__.IsLogScale(service, rules, path + [("IsLogScale", "")])
                                self.Position = self.__class__.Position(service, rules, path + [("Position", "")])
                                self.Size = self.__class__.Size(service, rules, path + [("Size", "")])
                                self.Skip = self.__class__.Skip(service, rules, path + [("Skip", "")])
                                super().__init__(service, rules, path)

                            class Visible(PyMenu):
                                """
                                Parameter Visible of value type bool.
                                """
                                pass

                            class Precision(PyMenu):
                                """
                                Parameter Precision of value type int.
                                """
                                pass

                            class Type(PyMenu):
                                """
                                Parameter Type of value type str.
                                """
                                pass

                            class ColorMap(PyMenu):
                                """
                                Parameter ColorMap of value type str.
                                """
                                pass

                            class ShowAll(PyMenu):
                                """
                                Parameter ShowAll of value type bool.
                                """
                                pass

                            class IsLogScale(PyMenu):
                                """
                                Parameter IsLogScale of value type bool.
                                """
                                pass

                            class Position(PyMenu):
                                """
                                Parameter Position of value type str.
                                """
                                pass

                            class Size(PyMenu):
                                """
                                Parameter Size of value type int.
                                """
                                pass

                            class Skip(PyMenu):
                                """
                                Parameter Skip of value type int.
                                """
                                pass

                        class Grid(PyMenu):
                            """
                            Singleton Grid.
                            """
                            def __init__(self, service, rules, path):
                                self.NX = self.__class__.NX(service, rules, path + [("NX", "")])
                                self.NY = self.__class__.NY(service, rules, path + [("NY", "")])
                                self.NZ = self.__class__.NZ(service, rules, path + [("NZ", "")])
                                super().__init__(service, rules, path)

                            class NX(PyMenu):
                                """
                                Parameter NX of value type int.
                                """
                                pass

                            class NY(PyMenu):
                                """
                                Parameter NY of value type int.
                                """
                                pass

                            class NZ(PyMenu):
                                """
                                Parameter NZ of value type int.
                                """
                                pass

                        class Bound(PyMenu):
                            """
                            Singleton Bound.
                            """
                            def __init__(self, service, rules, path):
                                self.XMin = self.__class__.XMin(service, rules, path + [("XMin", "")])
                                self.ZMax = self.__class__.ZMax(service, rules, path + [("ZMax", "")])
                                self.RestrictToBoundingBox = self.__class__.RestrictToBoundingBox(service, rules, path + [("RestrictToBoundingBox", "")])
                                self.YMax = self.__class__.YMax(service, rules, path + [("YMax", "")])
                                self.XMax = self.__class__.XMax(service, rules, path + [("XMax", "")])
                                self.ZMin = self.__class__.ZMin(service, rules, path + [("ZMin", "")])
                                self.YMin = self.__class__.YMin(service, rules, path + [("YMin", "")])
                                super().__init__(service, rules, path)

                            class XMin(PyMenu):
                                """
                                Parameter XMin of value type float.
                                """
                                pass

                            class ZMax(PyMenu):
                                """
                                Parameter ZMax of value type float.
                                """
                                pass

                            class RestrictToBoundingBox(PyMenu):
                                """
                                Parameter RestrictToBoundingBox of value type bool.
                                """
                                pass

                            class YMax(PyMenu):
                                """
                                Parameter YMax of value type float.
                                """
                                pass

                            class XMax(PyMenu):
                                """
                                Parameter XMax of value type float.
                                """
                                pass

                            class ZMin(PyMenu):
                                """
                                Parameter ZMin of value type float.
                                """
                                pass

                            class YMin(PyMenu):
                                """
                                Parameter YMin of value type float.
                                """
                                pass

                        class _name_(PyMenu):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                        class Quality(PyMenu):
                            """
                            Parameter Quality of value type str.
                            """
                            pass

                        class AlphaScale(PyMenu):
                            """
                            Parameter AlphaScale of value type float.
                            """
                            pass

                        class Field(PyMenu):
                            """
                            Parameter Field of value type str.
                            """
                            pass

                        class Transparencies(PyMenu):
                            """
                            Parameter Transparencies of value type List[float].
                            """
                            pass

                        class Volumes(PyMenu):
                            """
                            Parameter Volumes of value type List[str].
                            """
                            pass

                        class UpdateMinMax(PyCommand):
                            """
                            UpdateMinMax() -> None
                            """
                            pass

                        class DisplayInViewport(PyCommand):
                            """
                            DisplayInViewport(Viewport: str) -> bool
                            """
                            pass

                        class AddToViewport(PyCommand):
                            """
                            AddToViewport(Viewport: str) -> bool
                            """
                            pass

                        class Display(PyCommand):
                            """
                            Display() -> bool
                            """
                            pass

                        class SaveImage(PyCommand):
                            """
                            SaveImage(FileName: str, Format: str, FileType: str, Coloring: str, Orientation: str, UseWhiteBackground: bool, Resolution: Dict[str, Any]) -> bool
                            """
                            pass

                        class SaveAnimation(PyCommand):
                            """
                            SaveAnimation(FileName: str, Format: str, FPS: float, AntiAliasingPasses: str, Quality: str, H264: bool, Compression: str, BitRate: int, JPegQuality: int, PPMFormat: str, UseWhiteBackground: bool, Orientation: str, Resolution: Dict[str, Any]) -> None
                            """
                            pass

                    def __getitem__(self, key: str) -> _VolumeRender:
                        return super().__getitem__(key)

                class LIC(PyNamedObjectContainer):
                    class _LIC(PyMenu):
                        """
                        Singleton _LIC.
                        """
                        def __init__(self, service, rules, path):
                            self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                            self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                            self.LicNormalize = self.__class__.LicNormalize(service, rules, path + [("LicNormalize", "")])
                            self.LicPixelInterp = self.__class__.LicPixelInterp(service, rules, path + [("LicPixelInterp", "")])
                            self.LicColorByField = self.__class__.LicColorByField(service, rules, path + [("LicColorByField", "")])
                            self.IntensityAlpha = self.__class__.IntensityAlpha(service, rules, path + [("IntensityAlpha", "")])
                            self.LicMaxSteps = self.__class__.LicMaxSteps(service, rules, path + [("LicMaxSteps", "")])
                            self.VectorField = self.__class__.VectorField(service, rules, path + [("VectorField", "")])
                            self.OverlayedMesh = self.__class__.OverlayedMesh(service, rules, path + [("OverlayedMesh", "")])
                            self.TextureSpacing = self.__class__.TextureSpacing(service, rules, path + [("TextureSpacing", "")])
                            self.FastLic = self.__class__.FastLic(service, rules, path + [("FastLic", "")])
                            self.SyncStatus = self.__class__.SyncStatus(service, rules, path + [("SyncStatus", "")])
                            self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                            self.LicColor = self.__class__.LicColor(service, rules, path + [("LicColor", "")])
                            self.GrayScale = self.__class__.GrayScale(service, rules, path + [("GrayScale", "")])
                            self.DrawMesh = self.__class__.DrawMesh(service, rules, path + [("DrawMesh", "")])
                            self.TextureSize = self.__class__.TextureSize(service, rules, path + [("TextureSize", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.WindowId = self.__class__.WindowId(service, rules, path + [("WindowId", "")])
                            self.ImageFilter = self.__class__.ImageFilter(service, rules, path + [("ImageFilter", "")])
                            self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                            self.ImageToDisplay = self.__class__.ImageToDisplay(service, rules, path + [("ImageToDisplay", "")])
                            self.IntensityFactor = self.__class__.IntensityFactor(service, rules, path + [("IntensityFactor", "")])
                            self.OrientedLic = self.__class__.OrientedLic(service, rules, path + [("OrientedLic", "")])
                            self.Display = self.__class__.Display(service, rules, "Display", path)
                            self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                            self.SaveAnimation = self.__class__.SaveAnimation(service, rules, "SaveAnimation", path)
                            self.Pull = self.__class__.Pull(service, rules, "Pull", path)
                            self.Diff = self.__class__.Diff(service, rules, "Diff", path)
                            self.Push = self.__class__.Push(service, rules, "Push", path)
                            super().__init__(service, rules, path)

                        class ColorMap(PyMenu):
                            """
                            Singleton ColorMap.
                            """
                            def __init__(self, service, rules, path):
                                self.Size = self.__class__.Size(service, rules, path + [("Size", "")])
                                self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                                self.Visible = self.__class__.Visible(service, rules, path + [("Visible", "")])
                                self.Precision = self.__class__.Precision(service, rules, path + [("Precision", "")])
                                self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                                self.IsLogScale = self.__class__.IsLogScale(service, rules, path + [("IsLogScale", "")])
                                self.Position = self.__class__.Position(service, rules, path + [("Position", "")])
                                self.ShowAll = self.__class__.ShowAll(service, rules, path + [("ShowAll", "")])
                                self.Skip = self.__class__.Skip(service, rules, path + [("Skip", "")])
                                super().__init__(service, rules, path)

                            class Size(PyMenu):
                                """
                                Parameter Size of value type int.
                                """
                                pass

                            class ColorMap(PyMenu):
                                """
                                Parameter ColorMap of value type str.
                                """
                                pass

                            class Visible(PyMenu):
                                """
                                Parameter Visible of value type bool.
                                """
                                pass

                            class Precision(PyMenu):
                                """
                                Parameter Precision of value type int.
                                """
                                pass

                            class Type(PyMenu):
                                """
                                Parameter Type of value type str.
                                """
                                pass

                            class IsLogScale(PyMenu):
                                """
                                Parameter IsLogScale of value type bool.
                                """
                                pass

                            class Position(PyMenu):
                                """
                                Parameter Position of value type str.
                                """
                                pass

                            class ShowAll(PyMenu):
                                """
                                Parameter ShowAll of value type bool.
                                """
                                pass

                            class Skip(PyMenu):
                                """
                                Parameter Skip of value type int.
                                """
                                pass

                        class Range(PyMenu):
                            """
                            Singleton Range.
                            """
                            def __init__(self, service, rules, path):
                                self.MinValue = self.__class__.MinValue(service, rules, path + [("MinValue", "")])
                                self.GlobalRange = self.__class__.GlobalRange(service, rules, path + [("GlobalRange", "")])
                                self.MaxValue = self.__class__.MaxValue(service, rules, path + [("MaxValue", "")])
                                self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
                                self.ClipToRange = self.__class__.ClipToRange(service, rules, path + [("ClipToRange", "")])
                                super().__init__(service, rules, path)

                            class MinValue(PyMenu):
                                """
                                Parameter MinValue of value type float.
                                """
                                pass

                            class GlobalRange(PyMenu):
                                """
                                Parameter GlobalRange of value type bool.
                                """
                                pass

                            class MaxValue(PyMenu):
                                """
                                Parameter MaxValue of value type float.
                                """
                                pass

                            class AutoRange(PyMenu):
                                """
                                Parameter AutoRange of value type bool.
                                """
                                pass

                            class ClipToRange(PyMenu):
                                """
                                Parameter ClipToRange of value type bool.
                                """
                                pass

                        class LicNormalize(PyMenu):
                            """
                            Parameter LicNormalize of value type bool.
                            """
                            pass

                        class LicPixelInterp(PyMenu):
                            """
                            Parameter LicPixelInterp of value type bool.
                            """
                            pass

                        class LicColorByField(PyMenu):
                            """
                            Parameter LicColorByField of value type bool.
                            """
                            pass

                        class IntensityAlpha(PyMenu):
                            """
                            Parameter IntensityAlpha of value type bool.
                            """
                            pass

                        class LicMaxSteps(PyMenu):
                            """
                            Parameter LicMaxSteps of value type int.
                            """
                            pass

                        class VectorField(PyMenu):
                            """
                            Parameter VectorField of value type str.
                            """
                            pass

                        class OverlayedMesh(PyMenu):
                            """
                            Parameter OverlayedMesh of value type str.
                            """
                            pass

                        class TextureSpacing(PyMenu):
                            """
                            Parameter TextureSpacing of value type int.
                            """
                            pass

                        class FastLic(PyMenu):
                            """
                            Parameter FastLic of value type bool.
                            """
                            pass

                        class SyncStatus(PyMenu):
                            """
                            Parameter SyncStatus of value type str.
                            """
                            pass

                        class Field(PyMenu):
                            """
                            Parameter Field of value type str.
                            """
                            pass

                        class LicColor(PyMenu):
                            """
                            Parameter LicColor of value type str.
                            """
                            pass

                        class GrayScale(PyMenu):
                            """
                            Parameter GrayScale of value type bool.
                            """
                            pass

                        class DrawMesh(PyMenu):
                            """
                            Parameter DrawMesh of value type bool.
                            """
                            pass

                        class TextureSize(PyMenu):
                            """
                            Parameter TextureSize of value type int.
                            """
                            pass

                        class _name_(PyMenu):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                        class WindowId(PyMenu):
                            """
                            Parameter WindowId of value type int.
                            """
                            pass

                        class ImageFilter(PyMenu):
                            """
                            Parameter ImageFilter of value type str.
                            """
                            pass

                        class Surfaces(PyMenu):
                            """
                            Parameter Surfaces of value type List[str].
                            """
                            pass

                        class ImageToDisplay(PyMenu):
                            """
                            Parameter ImageToDisplay of value type str.
                            """
                            pass

                        class IntensityFactor(PyMenu):
                            """
                            Parameter IntensityFactor of value type int.
                            """
                            pass

                        class OrientedLic(PyMenu):
                            """
                            Parameter OrientedLic of value type bool.
                            """
                            pass

                        class Display(PyCommand):
                            """
                            Display() -> bool
                            """
                            pass

                        class SaveImage(PyCommand):
                            """
                            SaveImage(FileName: str, Format: str, FileType: str, Coloring: str, Orientation: str, UseWhiteBackground: bool, Resolution: Dict[str, Any]) -> bool
                            """
                            pass

                        class SaveAnimation(PyCommand):
                            """
                            SaveAnimation(FileName: str, Format: str, FPS: float, AntiAliasingPasses: str, Quality: str, H264: bool, Compression: str, BitRate: int, JPegQuality: int, PPMFormat: str, UseWhiteBackground: bool, Orientation: str, Resolution: Dict[str, Any]) -> None
                            """
                            pass

                        class Pull(PyCommand):
                            """
                            Pull() -> bool
                            """
                            pass

                        class Diff(PyCommand):
                            """
                            Diff() -> bool
                            """
                            pass

                        class Push(PyCommand):
                            """
                            Push() -> bool
                            """
                            pass

                    def __getitem__(self, key: str) -> _LIC:
                        return super().__getitem__(key)

                class Vector(PyNamedObjectContainer):
                    class _Vector(PyMenu):
                        """
                        Singleton _Vector.
                        """
                        def __init__(self, service, rules, path):
                            self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                            self.Scale = self.__class__.Scale(service, rules, path + [("Scale", "")])
                            self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                            self.VectorOptions = self.__class__.VectorOptions(service, rules, path + [("VectorOptions", "")])
                            self.VectorField = self.__class__.VectorField(service, rules, path + [("VectorField", "")])
                            self.DrawMesh = self.__class__.DrawMesh(service, rules, path + [("DrawMesh", "")])
                            self.SyncStatus = self.__class__.SyncStatus(service, rules, path + [("SyncStatus", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.Style = self.__class__.Style(service, rules, path + [("Style", "")])
                            self.OverlayedMesh = self.__class__.OverlayedMesh(service, rules, path + [("OverlayedMesh", "")])
                            self.Skip = self.__class__.Skip(service, rules, path + [("Skip", "")])
                            self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                            self.WindowId = self.__class__.WindowId(service, rules, path + [("WindowId", "")])
                            self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                            self.Diff = self.__class__.Diff(service, rules, "Diff", path)
                            self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                            self.Push = self.__class__.Push(service, rules, "Push", path)
                            self.Pull = self.__class__.Pull(service, rules, "Pull", path)
                            self.Display = self.__class__.Display(service, rules, "Display", path)
                            self.SaveAnimation = self.__class__.SaveAnimation(service, rules, "SaveAnimation", path)
                            self.DisplayInViewport = self.__class__.DisplayInViewport(service, rules, "DisplayInViewport", path)
                            self.UpdateMinMax = self.__class__.UpdateMinMax(service, rules, "UpdateMinMax", path)
                            self.AddToViewport = self.__class__.AddToViewport(service, rules, "AddToViewport", path)
                            super().__init__(service, rules, path)

                        class ColorMap(PyMenu):
                            """
                            Singleton ColorMap.
                            """
                            def __init__(self, service, rules, path):
                                self.Size = self.__class__.Size(service, rules, path + [("Size", "")])
                                self.Visible = self.__class__.Visible(service, rules, path + [("Visible", "")])
                                self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                                self.IsLogScale = self.__class__.IsLogScale(service, rules, path + [("IsLogScale", "")])
                                self.ShowAll = self.__class__.ShowAll(service, rules, path + [("ShowAll", "")])
                                self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                                self.Position = self.__class__.Position(service, rules, path + [("Position", "")])
                                self.Skip = self.__class__.Skip(service, rules, path + [("Skip", "")])
                                self.Precision = self.__class__.Precision(service, rules, path + [("Precision", "")])
                                super().__init__(service, rules, path)

                            class Size(PyMenu):
                                """
                                Parameter Size of value type int.
                                """
                                pass

                            class Visible(PyMenu):
                                """
                                Parameter Visible of value type bool.
                                """
                                pass

                            class Type(PyMenu):
                                """
                                Parameter Type of value type str.
                                """
                                pass

                            class IsLogScale(PyMenu):
                                """
                                Parameter IsLogScale of value type bool.
                                """
                                pass

                            class ShowAll(PyMenu):
                                """
                                Parameter ShowAll of value type bool.
                                """
                                pass

                            class ColorMap(PyMenu):
                                """
                                Parameter ColorMap of value type str.
                                """
                                pass

                            class Position(PyMenu):
                                """
                                Parameter Position of value type str.
                                """
                                pass

                            class Skip(PyMenu):
                                """
                                Parameter Skip of value type int.
                                """
                                pass

                            class Precision(PyMenu):
                                """
                                Parameter Precision of value type int.
                                """
                                pass

                        class Scale(PyMenu):
                            """
                            Singleton Scale.
                            """
                            def __init__(self, service, rules, path):
                                self.AutoScale = self.__class__.AutoScale(service, rules, path + [("AutoScale", "")])
                                self.Scale = self.__class__.Scale(service, rules, path + [("Scale", "")])
                                super().__init__(service, rules, path)

                            class AutoScale(PyMenu):
                                """
                                Parameter AutoScale of value type bool.
                                """
                                pass

                            class Scale(PyMenu):
                                """
                                Parameter Scale of value type float.
                                """
                                pass

                        class Range(PyMenu):
                            """
                            Singleton Range.
                            """
                            def __init__(self, service, rules, path):
                                self.MaxValue = self.__class__.MaxValue(service, rules, path + [("MaxValue", "")])
                                self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
                                self.ClipToRange = self.__class__.ClipToRange(service, rules, path + [("ClipToRange", "")])
                                self.GlobalRange = self.__class__.GlobalRange(service, rules, path + [("GlobalRange", "")])
                                self.MinValue = self.__class__.MinValue(service, rules, path + [("MinValue", "")])
                                super().__init__(service, rules, path)

                            class MaxValue(PyMenu):
                                """
                                Parameter MaxValue of value type float.
                                """
                                pass

                            class AutoRange(PyMenu):
                                """
                                Parameter AutoRange of value type bool.
                                """
                                pass

                            class ClipToRange(PyMenu):
                                """
                                Parameter ClipToRange of value type bool.
                                """
                                pass

                            class GlobalRange(PyMenu):
                                """
                                Parameter GlobalRange of value type bool.
                                """
                                pass

                            class MinValue(PyMenu):
                                """
                                Parameter MinValue of value type float.
                                """
                                pass

                        class VectorOptions(PyMenu):
                            """
                            Singleton VectorOptions.
                            """
                            def __init__(self, service, rules, path):
                                self.ZComponent = self.__class__.ZComponent(service, rules, path + [("ZComponent", "")])
                                self.FixedLength = self.__class__.FixedLength(service, rules, path + [("FixedLength", "")])
                                self.XComponent = self.__class__.XComponent(service, rules, path + [("XComponent", "")])
                                self.HeadScale = self.__class__.HeadScale(service, rules, path + [("HeadScale", "")])
                                self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                self.YComponent = self.__class__.YComponent(service, rules, path + [("YComponent", "")])
                                self.InPlane = self.__class__.InPlane(service, rules, path + [("InPlane", "")])
                                super().__init__(service, rules, path)

                            class ZComponent(PyMenu):
                                """
                                Parameter ZComponent of value type bool.
                                """
                                pass

                            class FixedLength(PyMenu):
                                """
                                Parameter FixedLength of value type bool.
                                """
                                pass

                            class XComponent(PyMenu):
                                """
                                Parameter XComponent of value type bool.
                                """
                                pass

                            class HeadScale(PyMenu):
                                """
                                Parameter HeadScale of value type float.
                                """
                                pass

                            class Color(PyMenu):
                                """
                                Parameter Color of value type str.
                                """
                                pass

                            class YComponent(PyMenu):
                                """
                                Parameter YComponent of value type bool.
                                """
                                pass

                            class InPlane(PyMenu):
                                """
                                Parameter InPlane of value type bool.
                                """
                                pass

                        class VectorField(PyMenu):
                            """
                            Parameter VectorField of value type str.
                            """
                            pass

                        class DrawMesh(PyMenu):
                            """
                            Parameter DrawMesh of value type bool.
                            """
                            pass

                        class SyncStatus(PyMenu):
                            """
                            Parameter SyncStatus of value type str.
                            """
                            pass

                        class _name_(PyMenu):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                        class Style(PyMenu):
                            """
                            Parameter Style of value type str.
                            """
                            pass

                        class OverlayedMesh(PyMenu):
                            """
                            Parameter OverlayedMesh of value type str.
                            """
                            pass

                        class Skip(PyMenu):
                            """
                            Parameter Skip of value type int.
                            """
                            pass

                        class Field(PyMenu):
                            """
                            Parameter Field of value type str.
                            """
                            pass

                        class WindowId(PyMenu):
                            """
                            Parameter WindowId of value type int.
                            """
                            pass

                        class Surfaces(PyMenu):
                            """
                            Parameter Surfaces of value type List[str].
                            """
                            pass

                        class Diff(PyCommand):
                            """
                            Diff() -> bool
                            """
                            pass

                        class SaveImage(PyCommand):
                            """
                            SaveImage(FileName: str, Format: str, FileType: str, Coloring: str, Orientation: str, UseWhiteBackground: bool, Resolution: Dict[str, Any]) -> bool
                            """
                            pass

                        class Push(PyCommand):
                            """
                            Push() -> bool
                            """
                            pass

                        class Pull(PyCommand):
                            """
                            Pull() -> bool
                            """
                            pass

                        class Display(PyCommand):
                            """
                            Display() -> bool
                            """
                            pass

                        class SaveAnimation(PyCommand):
                            """
                            SaveAnimation(FileName: str, Format: str, FPS: float, AntiAliasingPasses: str, Quality: str, H264: bool, Compression: str, BitRate: int, JPegQuality: int, PPMFormat: str, UseWhiteBackground: bool, Orientation: str, Resolution: Dict[str, Any]) -> None
                            """
                            pass

                        class DisplayInViewport(PyCommand):
                            """
                            DisplayInViewport(Viewport: str) -> bool
                            """
                            pass

                        class UpdateMinMax(PyCommand):
                            """
                            UpdateMinMax() -> None
                            """
                            pass

                        class AddToViewport(PyCommand):
                            """
                            AddToViewport(Viewport: str) -> bool
                            """
                            pass

                    def __getitem__(self, key: str) -> _Vector:
                        return super().__getitem__(key)

                class GridColors(PyMenu):
                    """
                    Singleton GridColors.
                    """
                    def __init__(self, service, rules, path):
                        self.ColorGridWall = self.__class__.ColorGridWall(service, rules, path + [("ColorGridWall", "")])
                        self.ColorGridInternal = self.__class__.ColorGridInternal(service, rules, path + [("ColorGridInternal", "")])
                        self.ColorGridTraction = self.__class__.ColorGridTraction(service, rules, path + [("ColorGridTraction", "")])
                        self.ColorGridInterior = self.__class__.ColorGridInterior(service, rules, path + [("ColorGridInterior", "")])
                        self.ColorGridOutlet = self.__class__.ColorGridOutlet(service, rules, path + [("ColorGridOutlet", "")])
                        self.ColorGridFreeSurface = self.__class__.ColorGridFreeSurface(service, rules, path + [("ColorGridFreeSurface", "")])
                        self.ColorGridRansLesInterface = self.__class__.ColorGridRansLesInterface(service, rules, path + [("ColorGridRansLesInterface", "")])
                        self.ColorGridFar = self.__class__.ColorGridFar(service, rules, path + [("ColorGridFar", "")])
                        self.ColorGridInlet = self.__class__.ColorGridInlet(service, rules, path + [("ColorGridInlet", "")])
                        self.ColorGridSymmetry = self.__class__.ColorGridSymmetry(service, rules, path + [("ColorGridSymmetry", "")])
                        self.ColorGridOverset = self.__class__.ColorGridOverset(service, rules, path + [("ColorGridOverset", "")])
                        self.ColorInterface = self.__class__.ColorInterface(service, rules, path + [("ColorInterface", "")])
                        self.ColorSurface = self.__class__.ColorSurface(service, rules, path + [("ColorSurface", "")])
                        self.ColorGridPeriodic = self.__class__.ColorGridPeriodic(service, rules, path + [("ColorGridPeriodic", "")])
                        self.ColorGridAxis = self.__class__.ColorGridAxis(service, rules, path + [("ColorGridAxis", "")])
                        super().__init__(service, rules, path)

                    class ColorGridWall(PyMenu):
                        """
                        Parameter ColorGridWall of value type str.
                        """
                        pass

                    class ColorGridInternal(PyMenu):
                        """
                        Parameter ColorGridInternal of value type str.
                        """
                        pass

                    class ColorGridTraction(PyMenu):
                        """
                        Parameter ColorGridTraction of value type str.
                        """
                        pass

                    class ColorGridInterior(PyMenu):
                        """
                        Parameter ColorGridInterior of value type str.
                        """
                        pass

                    class ColorGridOutlet(PyMenu):
                        """
                        Parameter ColorGridOutlet of value type str.
                        """
                        pass

                    class ColorGridFreeSurface(PyMenu):
                        """
                        Parameter ColorGridFreeSurface of value type str.
                        """
                        pass

                    class ColorGridRansLesInterface(PyMenu):
                        """
                        Parameter ColorGridRansLesInterface of value type str.
                        """
                        pass

                    class ColorGridFar(PyMenu):
                        """
                        Parameter ColorGridFar of value type str.
                        """
                        pass

                    class ColorGridInlet(PyMenu):
                        """
                        Parameter ColorGridInlet of value type str.
                        """
                        pass

                    class ColorGridSymmetry(PyMenu):
                        """
                        Parameter ColorGridSymmetry of value type str.
                        """
                        pass

                    class ColorGridOverset(PyMenu):
                        """
                        Parameter ColorGridOverset of value type str.
                        """
                        pass

                    class ColorInterface(PyMenu):
                        """
                        Parameter ColorInterface of value type str.
                        """
                        pass

                    class ColorSurface(PyMenu):
                        """
                        Parameter ColorSurface of value type str.
                        """
                        pass

                    class ColorGridPeriodic(PyMenu):
                        """
                        Parameter ColorGridPeriodic of value type str.
                        """
                        pass

                    class ColorGridAxis(PyMenu):
                        """
                        Parameter ColorGridAxis of value type str.
                        """
                        pass

                class CameraSettings(PyMenu):
                    """
                    Singleton CameraSettings.
                    """
                    def __init__(self, service, rules, path):
                        self.Target = self.__class__.Target(service, rules, path + [("Target", "")])
                        self.Position = self.__class__.Position(service, rules, path + [("Position", "")])
                        super().__init__(service, rules, path)

                    class Target(PyMenu):
                        """
                        Singleton Target.
                        """
                        def __init__(self, service, rules, path):
                            self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                            self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                            self.X = self.__class__.X(service, rules, path + [("X", "")])
                            super().__init__(service, rules, path)

                        class Z(PyMenu):
                            """
                            Parameter Z of value type float.
                            """
                            pass

                        class Y(PyMenu):
                            """
                            Parameter Y of value type float.
                            """
                            pass

                        class X(PyMenu):
                            """
                            Parameter X of value type float.
                            """
                            pass

                    class Position(PyMenu):
                        """
                        Singleton Position.
                        """
                        def __init__(self, service, rules, path):
                            self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                            self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                            self.X = self.__class__.X(service, rules, path + [("X", "")])
                            super().__init__(service, rules, path)

                        class Z(PyMenu):
                            """
                            Parameter Z of value type float.
                            """
                            pass

                        class Y(PyMenu):
                            """
                            Parameter Y of value type float.
                            """
                            pass

                        class X(PyMenu):
                            """
                            Parameter X of value type float.
                            """
                            pass

                class MirrorPlanes(PyMenu):
                    """
                    Singleton MirrorPlanes.
                    """
                    def __init__(self, service, rules, path):
                        self.ZOrigin = self.__class__.ZOrigin(service, rules, path + [("ZOrigin", "")])
                        self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                        self.AllSurfaces = self.__class__.AllSurfaces(service, rules, path + [("AllSurfaces", "")])
                        self.YOrigin = self.__class__.YOrigin(service, rules, path + [("YOrigin", "")])
                        self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                        self.XOrigin = self.__class__.XOrigin(service, rules, path + [("XOrigin", "")])
                        self.X = self.__class__.X(service, rules, path + [("X", "")])
                        self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                        super().__init__(service, rules, path)

                    class ZOrigin(PyMenu):
                        """
                        Parameter ZOrigin of value type float.
                        """
                        pass

                    class Surfaces(PyMenu):
                        """
                        Parameter Surfaces of value type List[str].
                        """
                        pass

                    class AllSurfaces(PyMenu):
                        """
                        Parameter AllSurfaces of value type bool.
                        """
                        pass

                    class YOrigin(PyMenu):
                        """
                        Parameter YOrigin of value type float.
                        """
                        pass

                    class Z(PyMenu):
                        """
                        Parameter Z of value type bool.
                        """
                        pass

                    class XOrigin(PyMenu):
                        """
                        Parameter XOrigin of value type float.
                        """
                        pass

                    class X(PyMenu):
                        """
                        Parameter X of value type bool.
                        """
                        pass

                    class Y(PyMenu):
                        """
                        Parameter Y of value type bool.
                        """
                        pass

                class GraphicsCreationCount(PyMenu):
                    """
                    Parameter GraphicsCreationCount of value type int.
                    """
                    pass

                class SaveImage(PyCommand):
                    """
                    SaveImage(FileName: str, Format: str, FileType: str, Coloring: str, Orientation: str, UseWhiteBackground: bool, Resolution: Dict[str, Any]) -> bool
                    """
                    pass

            class Plots(PyMenu):
                """
                Singleton Plots.
                """
                def __init__(self, service, rules, path):
                    self.PlotFromFile = self.__class__.PlotFromFile(service, rules, path + [("PlotFromFile", "")])
                    super().__init__(service, rules, path)

                class PlotFromFile(PyMenu):
                    """
                    Singleton PlotFromFile.
                    """
                    def __init__(self, service, rules, path):
                        self.Axes = self.__class__.Axes(service, rules, path + [("Axes", "")])
                        self.Curves = self.__class__.Curves(service, rules, path + [("Curves", "")])
                        self.XAxisFunction = self.__class__.XAxisFunction(service, rules, path + [("XAxisFunction", "")])
                        self.YAxisFunction = self.__class__.YAxisFunction(service, rules, path + [("YAxisFunction", "")])
                        self.Filename = self.__class__.Filename(service, rules, path + [("Filename", "")])
                        self.Plot = self.__class__.Plot(service, rules, "Plot", path)
                        super().__init__(service, rules, path)

                    class Axes(PyMenu):
                        """
                        Singleton Axes.
                        """
                        def __init__(self, service, rules, path):
                            self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                            self.X = self.__class__.X(service, rules, path + [("X", "")])
                            super().__init__(service, rules, path)

                        class Y(PyMenu):
                            """
                            Singleton Y.
                            """
                            def __init__(self, service, rules, path):
                                self.MajorRules = self.__class__.MajorRules(service, rules, path + [("MajorRules", "")])
                                self.MinorRules = self.__class__.MinorRules(service, rules, path + [("MinorRules", "")])
                                self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                                self.NumberFormat = self.__class__.NumberFormat(service, rules, path + [("NumberFormat", "")])
                                self.Options = self.__class__.Options(service, rules, path + [("Options", "")])
                                self.Label = self.__class__.Label(service, rules, path + [("Label", "")])
                                super().__init__(service, rules, path)

                            class MajorRules(PyMenu):
                                """
                                Singleton MajorRules.
                                """
                                def __init__(self, service, rules, path):
                                    self.Weight = self.__class__.Weight(service, rules, path + [("Weight", "")])
                                    self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                    super().__init__(service, rules, path)

                                class Weight(PyMenu):
                                    """
                                    Parameter Weight of value type float.
                                    """
                                    pass

                                class Color(PyMenu):
                                    """
                                    Parameter Color of value type str.
                                    """
                                    pass

                            class MinorRules(PyMenu):
                                """
                                Singleton MinorRules.
                                """
                                def __init__(self, service, rules, path):
                                    self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                    self.Weight = self.__class__.Weight(service, rules, path + [("Weight", "")])
                                    super().__init__(service, rules, path)

                                class Color(PyMenu):
                                    """
                                    Parameter Color of value type str.
                                    """
                                    pass

                                class Weight(PyMenu):
                                    """
                                    Parameter Weight of value type float.
                                    """
                                    pass

                            class Range(PyMenu):
                                """
                                Singleton Range.
                                """
                                def __init__(self, service, rules, path):
                                    self.Minimum = self.__class__.Minimum(service, rules, path + [("Minimum", "")])
                                    self.Maximum = self.__class__.Maximum(service, rules, path + [("Maximum", "")])
                                    super().__init__(service, rules, path)

                                class Minimum(PyMenu):
                                    """
                                    Parameter Minimum of value type float.
                                    """
                                    pass

                                class Maximum(PyMenu):
                                    """
                                    Parameter Maximum of value type float.
                                    """
                                    pass

                            class NumberFormat(PyMenu):
                                """
                                Singleton NumberFormat.
                                """
                                def __init__(self, service, rules, path):
                                    self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                                    self.Precision = self.__class__.Precision(service, rules, path + [("Precision", "")])
                                    super().__init__(service, rules, path)

                                class Type(PyMenu):
                                    """
                                    Parameter Type of value type str.
                                    """
                                    pass

                                class Precision(PyMenu):
                                    """
                                    Parameter Precision of value type int.
                                    """
                                    pass

                            class Options(PyMenu):
                                """
                                Singleton Options.
                                """
                                def __init__(self, service, rules, path):
                                    self.MinorRules = self.__class__.MinorRules(service, rules, path + [("MinorRules", "")])
                                    self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
                                    self.Log = self.__class__.Log(service, rules, path + [("Log", "")])
                                    self.MajorRules = self.__class__.MajorRules(service, rules, path + [("MajorRules", "")])
                                    super().__init__(service, rules, path)

                                class MinorRules(PyMenu):
                                    """
                                    Parameter MinorRules of value type bool.
                                    """
                                    pass

                                class AutoRange(PyMenu):
                                    """
                                    Parameter AutoRange of value type bool.
                                    """
                                    pass

                                class Log(PyMenu):
                                    """
                                    Parameter Log of value type bool.
                                    """
                                    pass

                                class MajorRules(PyMenu):
                                    """
                                    Parameter MajorRules of value type bool.
                                    """
                                    pass

                            class Label(PyMenu):
                                """
                                Parameter Label of value type str.
                                """
                                pass

                        class X(PyMenu):
                            """
                            Singleton X.
                            """
                            def __init__(self, service, rules, path):
                                self.Options = self.__class__.Options(service, rules, path + [("Options", "")])
                                self.NumberFormat = self.__class__.NumberFormat(service, rules, path + [("NumberFormat", "")])
                                self.MinorRules = self.__class__.MinorRules(service, rules, path + [("MinorRules", "")])
                                self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                                self.MajorRules = self.__class__.MajorRules(service, rules, path + [("MajorRules", "")])
                                self.Label = self.__class__.Label(service, rules, path + [("Label", "")])
                                super().__init__(service, rules, path)

                            class Options(PyMenu):
                                """
                                Singleton Options.
                                """
                                def __init__(self, service, rules, path):
                                    self.MinorRules = self.__class__.MinorRules(service, rules, path + [("MinorRules", "")])
                                    self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
                                    self.MajorRules = self.__class__.MajorRules(service, rules, path + [("MajorRules", "")])
                                    self.Log = self.__class__.Log(service, rules, path + [("Log", "")])
                                    super().__init__(service, rules, path)

                                class MinorRules(PyMenu):
                                    """
                                    Parameter MinorRules of value type bool.
                                    """
                                    pass

                                class AutoRange(PyMenu):
                                    """
                                    Parameter AutoRange of value type bool.
                                    """
                                    pass

                                class MajorRules(PyMenu):
                                    """
                                    Parameter MajorRules of value type bool.
                                    """
                                    pass

                                class Log(PyMenu):
                                    """
                                    Parameter Log of value type bool.
                                    """
                                    pass

                            class NumberFormat(PyMenu):
                                """
                                Singleton NumberFormat.
                                """
                                def __init__(self, service, rules, path):
                                    self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                                    self.Precision = self.__class__.Precision(service, rules, path + [("Precision", "")])
                                    super().__init__(service, rules, path)

                                class Type(PyMenu):
                                    """
                                    Parameter Type of value type str.
                                    """
                                    pass

                                class Precision(PyMenu):
                                    """
                                    Parameter Precision of value type int.
                                    """
                                    pass

                            class MinorRules(PyMenu):
                                """
                                Singleton MinorRules.
                                """
                                def __init__(self, service, rules, path):
                                    self.Weight = self.__class__.Weight(service, rules, path + [("Weight", "")])
                                    self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                    super().__init__(service, rules, path)

                                class Weight(PyMenu):
                                    """
                                    Parameter Weight of value type float.
                                    """
                                    pass

                                class Color(PyMenu):
                                    """
                                    Parameter Color of value type str.
                                    """
                                    pass

                            class Range(PyMenu):
                                """
                                Singleton Range.
                                """
                                def __init__(self, service, rules, path):
                                    self.Maximum = self.__class__.Maximum(service, rules, path + [("Maximum", "")])
                                    self.Minimum = self.__class__.Minimum(service, rules, path + [("Minimum", "")])
                                    super().__init__(service, rules, path)

                                class Maximum(PyMenu):
                                    """
                                    Parameter Maximum of value type float.
                                    """
                                    pass

                                class Minimum(PyMenu):
                                    """
                                    Parameter Minimum of value type float.
                                    """
                                    pass

                            class MajorRules(PyMenu):
                                """
                                Singleton MajorRules.
                                """
                                def __init__(self, service, rules, path):
                                    self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                    self.Weight = self.__class__.Weight(service, rules, path + [("Weight", "")])
                                    super().__init__(service, rules, path)

                                class Color(PyMenu):
                                    """
                                    Parameter Color of value type str.
                                    """
                                    pass

                                class Weight(PyMenu):
                                    """
                                    Parameter Weight of value type float.
                                    """
                                    pass

                            class Label(PyMenu):
                                """
                                Parameter Label of value type str.
                                """
                                pass

                    class Curves(PyMenu):
                        """
                        Singleton Curves.
                        """
                        def __init__(self, service, rules, path):
                            self.MarkerStyle = self.__class__.MarkerStyle(service, rules, path + [("MarkerStyle", "")])
                            self.LineStyle = self.__class__.LineStyle(service, rules, path + [("LineStyle", "")])
                            super().__init__(service, rules, path)

                        class MarkerStyle(PyMenu):
                            """
                            Singleton MarkerStyle.
                            """
                            def __init__(self, service, rules, path):
                                self.Symbol = self.__class__.Symbol(service, rules, path + [("Symbol", "")])
                                self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                self.Size = self.__class__.Size(service, rules, path + [("Size", "")])
                                super().__init__(service, rules, path)

                            class Symbol(PyMenu):
                                """
                                Parameter Symbol of value type str.
                                """
                                pass

                            class Color(PyMenu):
                                """
                                Parameter Color of value type str.
                                """
                                pass

                            class Size(PyMenu):
                                """
                                Parameter Size of value type float.
                                """
                                pass

                        class LineStyle(PyMenu):
                            """
                            Singleton LineStyle.
                            """
                            def __init__(self, service, rules, path):
                                self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                self.Weight = self.__class__.Weight(service, rules, path + [("Weight", "")])
                                self.Pattern = self.__class__.Pattern(service, rules, path + [("Pattern", "")])
                                super().__init__(service, rules, path)

                            class Color(PyMenu):
                                """
                                Parameter Color of value type str.
                                """
                                pass

                            class Weight(PyMenu):
                                """
                                Parameter Weight of value type float.
                                """
                                pass

                            class Pattern(PyMenu):
                                """
                                Parameter Pattern of value type str.
                                """
                                pass

                    class XAxisFunction(PyMenu):
                        """
                        Singleton XAxisFunction.
                        """
                        def __init__(self, service, rules, path):
                            self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                            super().__init__(service, rules, path)

                        class Field(PyMenu):
                            """
                            Parameter Field of value type str.
                            """
                            pass

                    class YAxisFunction(PyMenu):
                        """
                        Singleton YAxisFunction.
                        """
                        def __init__(self, service, rules, path):
                            self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                            super().__init__(service, rules, path)

                        class Field(PyMenu):
                            """
                            Parameter Field of value type str.
                            """
                            pass

                    class Filename(PyMenu):
                        """
                        Parameter Filename of value type str.
                        """
                        pass

                    class Plot(PyCommand):
                        """
                        Plot() -> None
                        """
                        pass

            class CreateMultipleIsosurfaces(PyCommand):
                """
                CreateMultipleIsosurfaces(NameFormat: str, Field: str, SpecifyBy: str, FirstValue: float, Increment: float, Steps: int, LastValue: float) -> None
                """
                pass

            class CreateCellZoneSurfaces(PyCommand):
                """
                CreateCellZoneSurfaces() -> List[int]
                """
                pass

            class CreateMultiplePlanes(PyCommand):
                """
                CreateMultiplePlanes(NameFormat: str, NumberOfPlanes: int, Option: str, NormalSpecification: str, NormalVector: Dict[str, Any], StartPoint: Dict[str, Any], EndPoint: Dict[str, Any], Spacing: float) -> None
                """
                pass

            class GetFieldMinMax(PyCommand):
                """
                GetFieldMinMax(Field: str, Surfaces: List[str]) -> List[float]
                """
                pass

            class GetXYData(PyCommand):
                """
                GetXYData(Surfaces: List[str], Fields: List[str]) -> None
                """
                pass

        class AppName(PyMenu):
            """
            Parameter AppName of value type str.
            """
            pass

        class ReadData(PyCommand):
            """
            ReadData(FileName: str) -> bool
            """
            pass

        class ReadCaseAndData(PyCommand):
            """
            ReadCaseAndData(FileName: str) -> bool
            """
            pass

        class ClearDatamodel(PyCommand):
            """
            ClearDatamodel() -> None
            """
            pass

        class WriteCaseAndData(PyCommand):
            """
            WriteCaseAndData(FileName: str, Binary: bool, Overwrite: bool) -> bool
            """
            pass

        class SendCommand(PyCommand):
            """
            SendCommand(Command: str) -> bool
            """
            pass

        class WriteCase(PyCommand):
            """
            WriteCase(FileName: str, Binary: bool, Overwrite: bool) -> bool
            """
            pass

        class WriteData(PyCommand):
            """
            WriteData(FileName: str, Binary: bool, Overwrite: bool) -> bool
            """
            pass

        class ReadCase(PyCommand):
            """
            ReadCase(FileName: str) -> bool
            """
            pass

