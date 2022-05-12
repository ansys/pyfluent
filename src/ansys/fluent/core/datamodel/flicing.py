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
            self.Setup = self.__class__.Setup(service, rules, path + [("Setup", "")])
            self.Solution = self.__class__.Solution(service, rules, path + [("Solution", "")])
            self.Streaming = self.__class__.Streaming(service, rules, path + [("Streaming", "")])
            self.Results = self.__class__.Results(service, rules, path + [("Results", "")])
            self.MeshInfo = self.__class__.MeshInfo(service, rules, path + [("MeshInfo", "")])
            self.ResultsInfo = self.__class__.ResultsInfo(service, rules, path + [("ResultsInfo", "")])
            self.App = self.__class__.App(service, rules, path + [("App", "")])
            self.CaseInfo = self.__class__.CaseInfo(service, rules, path + [("CaseInfo", "")])
            self.AuxiliaryInfo = self.__class__.AuxiliaryInfo(service, rules, path + [("AuxiliaryInfo", "")])
            self.AppName = self.__class__.AppName(service, rules, path + [("AppName", "")])
            self.ReadCase = self.__class__.ReadCase(service, rules, "ReadCase", path)
            self.WriteCase = self.__class__.WriteCase(service, rules, "WriteCase", path)
            self.ReadData = self.__class__.ReadData(service, rules, "ReadData", path)
            self.ClearDatamodel = self.__class__.ClearDatamodel(service, rules, "ClearDatamodel", path)
            self.WriteData = self.__class__.WriteData(service, rules, "WriteData", path)
            self.SendCommand = self.__class__.SendCommand(service, rules, "SendCommand", path)
            self.ReadCaseAndData = self.__class__.ReadCaseAndData(service, rules, "ReadCaseAndData", path)
            self.WriteCaseAndData = self.__class__.WriteCaseAndData(service, rules, "WriteCaseAndData", path)
            super().__init__(service, rules, path)

        class Setup(PyMenu):
            """
            Singleton Setup.
            """
            def __init__(self, service, rules, path):
                self.Material = self.__class__.Material(service, rules, path + [("Material", "")])
                self.Boundary = self.__class__.Boundary(service, rules, path + [("Boundary", "")])
                self.CellZone = self.__class__.CellZone(service, rules, path + [("CellZone", "")])
                self.Beta = self.__class__.Beta(service, rules, path + [("Beta", "")])
                super().__init__(service, rules, path)

            class Material(PyNamedObjectContainer):
                class _Material(PyMenu):
                    """
                    Singleton _Material.
                    """
                    def __init__(self, service, rules, path):
                        self.ThermalConductivity = self.__class__.ThermalConductivity(service, rules, path + [("ThermalConductivity", "")])
                        self.Viscosity = self.__class__.Viscosity(service, rules, path + [("Viscosity", "")])
                        self.ThermalExpansionCoefficient = self.__class__.ThermalExpansionCoefficient(service, rules, path + [("ThermalExpansionCoefficient", "")])
                        self.CpSpecificHeat = self.__class__.CpSpecificHeat(service, rules, path + [("CpSpecificHeat", "")])
                        self.Density = self.__class__.Density(service, rules, path + [("Density", "")])
                        self.MolecularWeight = self.__class__.MolecularWeight(service, rules, path + [("MolecularWeight", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        self.FluentName = self.__class__.FluentName(service, rules, path + [("FluentName", "")])
                        self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                        self.LoadFromDatabase = self.__class__.LoadFromDatabase(service, rules, "LoadFromDatabase", path)
                        super().__init__(service, rules, path)

                    class ThermalConductivity(PyMenu):
                        """
                        Singleton ThermalConductivity.
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

                    class ThermalExpansionCoefficient(PyMenu):
                        """
                        Singleton ThermalExpansionCoefficient.
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

                    class Density(PyMenu):
                        """
                        Singleton Density.
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

                    class _name_(PyMenu):
                        """
                        Parameter _name_ of value type str.
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

                    class LoadFromDatabase(PyCommand):
                        """
                        LoadFromDatabase(MaterialName: str) -> None
                        """
                        pass

                def __getitem__(self, key: str) -> _Material:
                    return super().__getitem__(key)

            class Boundary(PyNamedObjectContainer):
                class _Boundary(PyMenu):
                    """
                    Singleton _Boundary.
                    """
                    def __init__(self, service, rules, path):
                        self.Thermal = self.__class__.Thermal(service, rules, path + [("Thermal", "")])
                        self.Flow = self.__class__.Flow(service, rules, path + [("Flow", "")])
                        self.Turbulence = self.__class__.Turbulence(service, rules, path + [("Turbulence", "")])
                        self.BoundaryId = self.__class__.BoundaryId(service, rules, path + [("BoundaryId", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        self.BoundaryType = self.__class__.BoundaryType(service, rules, path + [("BoundaryType", "")])
                        super().__init__(service, rules, path)

                    class Thermal(PyMenu):
                        """
                        Singleton Thermal.
                        """
                        def __init__(self, service, rules, path):
                            self.Temperature = self.__class__.Temperature(service, rules, path + [("Temperature", "")])
                            self.HeatGenerationRate = self.__class__.HeatGenerationRate(service, rules, path + [("HeatGenerationRate", "")])
                            self.ThermalConditions = self.__class__.ThermalConditions(service, rules, path + [("ThermalConditions", "")])
                            self.HeatTransferCoefficient = self.__class__.HeatTransferCoefficient(service, rules, path + [("HeatTransferCoefficient", "")])
                            self.ExternalRadiationTemperature = self.__class__.ExternalRadiationTemperature(service, rules, path + [("ExternalRadiationTemperature", "")])
                            self.WallThickness = self.__class__.WallThickness(service, rules, path + [("WallThickness", "")])
                            self.FreeStreamTemperature = self.__class__.FreeStreamTemperature(service, rules, path + [("FreeStreamTemperature", "")])
                            self.TotalTemperature = self.__class__.TotalTemperature(service, rules, path + [("TotalTemperature", "")])
                            self.HeatFlux = self.__class__.HeatFlux(service, rules, path + [("HeatFlux", "")])
                            self.ExternalEmissivity = self.__class__.ExternalEmissivity(service, rules, path + [("ExternalEmissivity", "")])
                            super().__init__(service, rules, path)

                        class Temperature(PyMenu):
                            """
                            Parameter Temperature of value type float.
                            """
                            pass

                        class HeatGenerationRate(PyMenu):
                            """
                            Parameter HeatGenerationRate of value type float.
                            """
                            pass

                        class ThermalConditions(PyMenu):
                            """
                            Parameter ThermalConditions of value type str.
                            """
                            pass

                        class HeatTransferCoefficient(PyMenu):
                            """
                            Parameter HeatTransferCoefficient of value type float.
                            """
                            pass

                        class ExternalRadiationTemperature(PyMenu):
                            """
                            Parameter ExternalRadiationTemperature of value type float.
                            """
                            pass

                        class WallThickness(PyMenu):
                            """
                            Parameter WallThickness of value type float.
                            """
                            pass

                        class FreeStreamTemperature(PyMenu):
                            """
                            Parameter FreeStreamTemperature of value type float.
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

                        class ExternalEmissivity(PyMenu):
                            """
                            Parameter ExternalEmissivity of value type float.
                            """
                            pass

                    class Flow(PyMenu):
                        """
                        Singleton Flow.
                        """
                        def __init__(self, service, rules, path):
                            self.TranslationalDirection = self.__class__.TranslationalDirection(service, rules, path + [("TranslationalDirection", "")])
                            self.FlowDirection = self.__class__.FlowDirection(service, rules, path + [("FlowDirection", "")])
                            self.Direction = self.__class__.Direction(service, rules, path + [("Direction", "")])
                            self.TranslationalVelocityComponents = self.__class__.TranslationalVelocityComponents(service, rules, path + [("TranslationalVelocityComponents", "")])
                            self.RotationAxisDirection = self.__class__.RotationAxisDirection(service, rules, path + [("RotationAxisDirection", "")])
                            self.VelocityCartesianComponents = self.__class__.VelocityCartesianComponents(service, rules, path + [("VelocityCartesianComponents", "")])
                            self.RotationAxisOrigin = self.__class__.RotationAxisOrigin(service, rules, path + [("RotationAxisOrigin", "")])
                            self.WallVelocitySpecification = self.__class__.WallVelocitySpecification(service, rules, path + [("WallVelocitySpecification", "")])
                            self.MassFlowSpecificationMethod = self.__class__.MassFlowSpecificationMethod(service, rules, path + [("MassFlowSpecificationMethod", "")])
                            self.AverageMassFlux = self.__class__.AverageMassFlux(service, rules, path + [("AverageMassFlux", "")])
                            self.IsRotating = self.__class__.IsRotating(service, rules, path + [("IsRotating", "")])
                            self.RotationalSpeed = self.__class__.RotationalSpeed(service, rules, path + [("RotationalSpeed", "")])
                            self.MassFlowRate = self.__class__.MassFlowRate(service, rules, path + [("MassFlowRate", "")])
                            self.GaugePressure = self.__class__.GaugePressure(service, rules, path + [("GaugePressure", "")])
                            self.DirectionSpecificationMethod = self.__class__.DirectionSpecificationMethod(service, rules, path + [("DirectionSpecificationMethod", "")])
                            self.VelocitySpecification = self.__class__.VelocitySpecification(service, rules, path + [("VelocitySpecification", "")])
                            self.TranslationalVelocityMagnitude = self.__class__.TranslationalVelocityMagnitude(service, rules, path + [("TranslationalVelocityMagnitude", "")])
                            self.SupersonicOrInitialGaugePressure = self.__class__.SupersonicOrInitialGaugePressure(service, rules, path + [("SupersonicOrInitialGaugePressure", "")])
                            self.TranslationalVelocitySpecification = self.__class__.TranslationalVelocitySpecification(service, rules, path + [("TranslationalVelocitySpecification", "")])
                            self.GaugeTotalPressure = self.__class__.GaugeTotalPressure(service, rules, path + [("GaugeTotalPressure", "")])
                            self.MachNumber = self.__class__.MachNumber(service, rules, path + [("MachNumber", "")])
                            self.IsMotionBC = self.__class__.IsMotionBC(service, rules, path + [("IsMotionBC", "")])
                            self.VelocityMagnitude = self.__class__.VelocityMagnitude(service, rules, path + [("VelocityMagnitude", "")])
                            self.MassFlux = self.__class__.MassFlux(service, rules, path + [("MassFlux", "")])
                            super().__init__(service, rules, path)

                        class TranslationalDirection(PyMenu):
                            """
                            Singleton TranslationalDirection.
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

                        class FlowDirection(PyMenu):
                            """
                            Singleton FlowDirection.
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

                        class TranslationalVelocityComponents(PyMenu):
                            """
                            Singleton TranslationalVelocityComponents.
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

                        class RotationAxisDirection(PyMenu):
                            """
                            Singleton RotationAxisDirection.
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

                        class RotationAxisOrigin(PyMenu):
                            """
                            Singleton RotationAxisOrigin.
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

                        class WallVelocitySpecification(PyMenu):
                            """
                            Parameter WallVelocitySpecification of value type str.
                            """
                            pass

                        class MassFlowSpecificationMethod(PyMenu):
                            """
                            Parameter MassFlowSpecificationMethod of value type str.
                            """
                            pass

                        class AverageMassFlux(PyMenu):
                            """
                            Parameter AverageMassFlux of value type float.
                            """
                            pass

                        class IsRotating(PyMenu):
                            """
                            Parameter IsRotating of value type bool.
                            """
                            pass

                        class RotationalSpeed(PyMenu):
                            """
                            Parameter RotationalSpeed of value type float.
                            """
                            pass

                        class MassFlowRate(PyMenu):
                            """
                            Parameter MassFlowRate of value type float.
                            """
                            pass

                        class GaugePressure(PyMenu):
                            """
                            Parameter GaugePressure of value type float.
                            """
                            pass

                        class DirectionSpecificationMethod(PyMenu):
                            """
                            Parameter DirectionSpecificationMethod of value type str.
                            """
                            pass

                        class VelocitySpecification(PyMenu):
                            """
                            Parameter VelocitySpecification of value type str.
                            """
                            pass

                        class TranslationalVelocityMagnitude(PyMenu):
                            """
                            Parameter TranslationalVelocityMagnitude of value type float.
                            """
                            pass

                        class SupersonicOrInitialGaugePressure(PyMenu):
                            """
                            Parameter SupersonicOrInitialGaugePressure of value type float.
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

                        class MachNumber(PyMenu):
                            """
                            Parameter MachNumber of value type float.
                            """
                            pass

                        class IsMotionBC(PyMenu):
                            """
                            Parameter IsMotionBC of value type int.
                            """
                            pass

                        class VelocityMagnitude(PyMenu):
                            """
                            Parameter VelocityMagnitude of value type float.
                            """
                            pass

                        class MassFlux(PyMenu):
                            """
                            Parameter MassFlux of value type float.
                            """
                            pass

                    class Turbulence(PyMenu):
                        """
                        Singleton Turbulence.
                        """
                        def __init__(self, service, rules, path):
                            self.SpecificationMethod = self.__class__.SpecificationMethod(service, rules, path + [("SpecificationMethod", "")])
                            self.TurbulentLengthScale = self.__class__.TurbulentLengthScale(service, rules, path + [("TurbulentLengthScale", "")])
                            self.HydraulicDiameter = self.__class__.HydraulicDiameter(service, rules, path + [("HydraulicDiameter", "")])
                            self.TurbulentViscosityRatio = self.__class__.TurbulentViscosityRatio(service, rules, path + [("TurbulentViscosityRatio", "")])
                            self.TurbulentIntensity = self.__class__.TurbulentIntensity(service, rules, path + [("TurbulentIntensity", "")])
                            super().__init__(service, rules, path)

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

                    class BoundaryType(PyMenu):
                        """
                        Parameter BoundaryType of value type str.
                        """
                        pass

                def __getitem__(self, key: str) -> _Boundary:
                    return super().__getitem__(key)

            class CellZone(PyNamedObjectContainer):
                class _CellZone(PyMenu):
                    """
                    Singleton _CellZone.
                    """
                    def __init__(self, service, rules, path):
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        self.Material = self.__class__.Material(service, rules, path + [("Material", "")])
                        self.CellZoneId = self.__class__.CellZoneId(service, rules, path + [("CellZoneId", "")])
                        super().__init__(service, rules, path)

                    class _name_(PyMenu):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                    class Material(PyMenu):
                        """
                        Parameter Material of value type str.
                        """
                        pass

                    class CellZoneId(PyMenu):
                        """
                        Parameter CellZoneId of value type int.
                        """
                        pass

                def __getitem__(self, key: str) -> _CellZone:
                    return super().__getitem__(key)

            class Beta(PyMenu):
                """
                Parameter Beta of value type bool.
                """
                pass

        class Solution(PyMenu):
            """
            Singleton Solution.
            """
            def __init__(self, service, rules, path):
                self.Monitors = self.__class__.Monitors(service, rules, path + [("Monitors", "")])
                self.Methods = self.__class__.Methods(service, rules, path + [("Methods", "")])
                self.CalculationActivities = self.__class__.CalculationActivities(service, rules, path + [("CalculationActivities", "")])
                self.Controls = self.__class__.Controls(service, rules, path + [("Controls", "")])
                self.State = self.__class__.State(service, rules, path + [("State", "")])
                self.Calculation = self.__class__.Calculation(service, rules, path + [("Calculation", "")])
                super().__init__(service, rules, path)

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
                            self.Frequency = self.__class__.Frequency(service, rules, path + [("Frequency", "")])
                            self.Title = self.__class__.Title(service, rules, path + [("Title", "")])
                            self.IsValid = self.__class__.IsValid(service, rules, path + [("IsValid", "")])
                            self.Active = self.__class__.Active(service, rules, path + [("Active", "")])
                            self.YLabel = self.__class__.YLabel(service, rules, path + [("YLabel", "")])
                            self.XLabel = self.__class__.XLabel(service, rules, path + [("XLabel", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.ReportDefinitions = self.__class__.ReportDefinitions(service, rules, path + [("ReportDefinitions", "")])
                            self.Print = self.__class__.Print(service, rules, path + [("Print", "")])
                            self.UnitInfo = self.__class__.UnitInfo(service, rules, path + [("UnitInfo", "")])
                            self.Name = self.__class__.Name(service, rules, path + [("Name", "")])
                            self.FrequencyOf = self.__class__.FrequencyOf(service, rules, path + [("FrequencyOf", "")])
                            super().__init__(service, rules, path)

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

                        class IsValid(PyMenu):
                            """
                            Parameter IsValid of value type bool.
                            """
                            pass

                        class Active(PyMenu):
                            """
                            Parameter Active of value type bool.
                            """
                            pass

                        class YLabel(PyMenu):
                            """
                            Parameter YLabel of value type str.
                            """
                            pass

                        class XLabel(PyMenu):
                            """
                            Parameter XLabel of value type str.
                            """
                            pass

                        class _name_(PyMenu):
                            """
                            Parameter _name_ of value type str.
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

                        class UnitInfo(PyMenu):
                            """
                            Parameter UnitInfo of value type str.
                            """
                            pass

                        class Name(PyMenu):
                            """
                            Parameter Name of value type str.
                            """
                            pass

                        class FrequencyOf(PyMenu):
                            """
                            Parameter FrequencyOf of value type str.
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
                                self.RelativeCriterion = self.__class__.RelativeCriterion(service, rules, path + [("RelativeCriterion", "")])
                                self.AbsoluteCriterion = self.__class__.AbsoluteCriterion(service, rules, path + [("AbsoluteCriterion", "")])
                                self.IsMonitored = self.__class__.IsMonitored(service, rules, path + [("IsMonitored", "")])
                                self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                                self.CheckConvergence = self.__class__.CheckConvergence(service, rules, path + [("CheckConvergence", "")])
                                super().__init__(service, rules, path)

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

                            class CheckConvergence(PyMenu):
                                """
                                Parameter CheckConvergence of value type bool.
                                """
                                pass

                        def __getitem__(self, key: str) -> _Equation:
                            return super().__getitem__(key)

                    class ConvergenceCriterionType(PyMenu):
                        """
                        Parameter ConvergenceCriterionType of value type str.
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
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.Value = self.__class__.Value(service, rules, path + [("Value", "")])
                            self.AllowedValues = self.__class__.AllowedValues(service, rules, path + [("AllowedValues", "")])
                            self.InternalName = self.__class__.InternalName(service, rules, path + [("InternalName", "")])
                            super().__init__(service, rules, path)

                        class DomainId(PyMenu):
                            """
                            Parameter DomainId of value type int.
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

                        class AllowedValues(PyMenu):
                            """
                            Parameter AllowedValues of value type List[str].
                            """
                            pass

                        class InternalName(PyMenu):
                            """
                            Parameter InternalName of value type str.
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
                            self.RealIndex = self.__class__.RealIndex(service, rules, path + [("RealIndex", "")])
                            self.Sequence = self.__class__.Sequence(service, rules, path + [("Sequence", "")])
                            self.View = self.__class__.View(service, rules, path + [("View", "")])
                            self.Projection = self.__class__.Projection(service, rules, path + [("Projection", "")])
                            self.IntegerIndex = self.__class__.IntegerIndex(service, rules, path + [("IntegerIndex", "")])
                            self.StorageDirectory = self.__class__.StorageDirectory(service, rules, path + [("StorageDirectory", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.WindowId = self.__class__.WindowId(service, rules, path + [("WindowId", "")])
                            self.RecordAfter = self.__class__.RecordAfter(service, rules, path + [("RecordAfter", "")])
                            self.StorageType = self.__class__.StorageType(service, rules, path + [("StorageType", "")])
                            self.Apply = self.__class__.Apply(service, rules, "Apply", path)
                            self.PlayBack = self.__class__.PlayBack(service, rules, "PlayBack", path)
                            self.Delete = self.__class__.Delete(service, rules, "Delete", path)
                            self.Display = self.__class__.Display(service, rules, "Display", path)
                            super().__init__(service, rules, path)

                        class Graphics(PyMenu):
                            """
                            Parameter Graphics of value type str.
                            """
                            pass

                        class RealIndex(PyMenu):
                            """
                            Parameter RealIndex of value type float.
                            """
                            pass

                        class Sequence(PyMenu):
                            """
                            Parameter Sequence of value type int.
                            """
                            pass

                        class View(PyMenu):
                            """
                            Parameter View of value type str.
                            """
                            pass

                        class Projection(PyMenu):
                            """
                            Parameter Projection of value type str.
                            """
                            pass

                        class IntegerIndex(PyMenu):
                            """
                            Parameter IntegerIndex of value type int.
                            """
                            pass

                        class StorageDirectory(PyMenu):
                            """
                            Parameter StorageDirectory of value type str.
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

                        class RecordAfter(PyMenu):
                            """
                            Parameter RecordAfter of value type str.
                            """
                            pass

                        class StorageType(PyMenu):
                            """
                            Parameter StorageType of value type str.
                            """
                            pass

                        class Apply(PyCommand):
                            """
                            Apply() -> bool
                            """
                            pass

                        class PlayBack(PyCommand):
                            """
                            PlayBack() -> bool
                            """
                            pass

                        class Delete(PyCommand):
                            """
                            Delete() -> bool
                            """
                            pass

                        class Display(PyCommand):
                            """
                            Display() -> bool
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
                            self.Value = self.__class__.Value(service, rules, path + [("Value", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.InternalName = self.__class__.InternalName(service, rules, path + [("InternalName", "")])
                            self.DomainId = self.__class__.DomainId(service, rules, path + [("DomainId", "")])
                            super().__init__(service, rules, path)

                        class Value(PyMenu):
                            """
                            Parameter Value of value type float.
                            """
                            pass

                        class _name_(PyMenu):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                        class InternalName(PyMenu):
                            """
                            Parameter InternalName of value type str.
                            """
                            pass

                        class DomainId(PyMenu):
                            """
                            Parameter DomainId of value type int.
                            """
                            pass

                    def __getitem__(self, key: str) -> _UnderRelaxationFactors:
                        return super().__getitem__(key)

                class CourantNumber(PyMenu):
                    """
                    Parameter CourantNumber of value type float.
                    """
                    pass

            class State(PyMenu):
                """
                Singleton State.
                """
                def __init__(self, service, rules, path):
                    self.CaseFileName = self.__class__.CaseFileName(service, rules, path + [("CaseFileName", "")])
                    self.DataId = self.__class__.DataId(service, rules, path + [("DataId", "")])
                    self.AeroOn = self.__class__.AeroOn(service, rules, path + [("AeroOn", "")])
                    self.IcingOn = self.__class__.IcingOn(service, rules, path + [("IcingOn", "")])
                    self.DataValid = self.__class__.DataValid(service, rules, path + [("DataValid", "")])
                    self.CaseValid = self.__class__.CaseValid(service, rules, path + [("CaseValid", "")])
                    self.GridId = self.__class__.GridId(service, rules, path + [("GridId", "")])
                    self.CaseId = self.__class__.CaseId(service, rules, path + [("CaseId", "")])
                    super().__init__(service, rules, path)

                class CaseFileName(PyMenu):
                    """
                    Parameter CaseFileName of value type str.
                    """
                    pass

                class DataId(PyMenu):
                    """
                    Parameter DataId of value type int.
                    """
                    pass

                class AeroOn(PyMenu):
                    """
                    Parameter AeroOn of value type bool.
                    """
                    pass

                class IcingOn(PyMenu):
                    """
                    Parameter IcingOn of value type bool.
                    """
                    pass

                class DataValid(PyMenu):
                    """
                    Parameter DataValid of value type bool.
                    """
                    pass

                class CaseValid(PyMenu):
                    """
                    Parameter CaseValid of value type bool.
                    """
                    pass

                class GridId(PyMenu):
                    """
                    Parameter GridId of value type int.
                    """
                    pass

                class CaseId(PyMenu):
                    """
                    Parameter CaseId of value type int.
                    """
                    pass

            class Calculation(PyMenu):
                """
                Singleton Calculation.
                """
                def __init__(self, service, rules, path):
                    self.AnalysisType = self.__class__.AnalysisType(service, rules, path + [("AnalysisType", "")])
                    self.NumberOfIterations = self.__class__.NumberOfIterations(service, rules, path + [("NumberOfIterations", "")])
                    self.MaxIterationsPerTimeStep = self.__class__.MaxIterationsPerTimeStep(service, rules, path + [("MaxIterationsPerTimeStep", "")])
                    self.NumberOfTimeSteps = self.__class__.NumberOfTimeSteps(service, rules, path + [("NumberOfTimeSteps", "")])
                    self.TimeStepSize = self.__class__.TimeStepSize(service, rules, path + [("TimeStepSize", "")])
                    self.Resume = self.__class__.Resume(service, rules, "Resume", path)
                    self.Calculate = self.__class__.Calculate(service, rules, "Calculate", path)
                    self.Initialize = self.__class__.Initialize(service, rules, "Initialize", path)
                    self.Pause = self.__class__.Pause(service, rules, "Pause", path)
                    self.Interrupt = self.__class__.Interrupt(service, rules, "Interrupt", path)
                    super().__init__(service, rules, path)

                class AnalysisType(PyMenu):
                    """
                    Parameter AnalysisType of value type str.
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

                class NumberOfTimeSteps(PyMenu):
                    """
                    Parameter NumberOfTimeSteps of value type int.
                    """
                    pass

                class TimeStepSize(PyMenu):
                    """
                    Parameter TimeStepSize of value type float.
                    """
                    pass

                class Resume(PyCommand):
                    """
                    Resume() -> bool
                    """
                    pass

                class Calculate(PyCommand):
                    """
                    Calculate() -> bool
                    """
                    pass

                class Initialize(PyCommand):
                    """
                    Initialize() -> bool
                    """
                    pass

                class Pause(PyCommand):
                    """
                    Pause() -> bool
                    """
                    pass

                class Interrupt(PyCommand):
                    """
                    Interrupt() -> bool
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

        class Results(PyMenu):
            """
            Singleton Results.
            """
            def __init__(self, service, rules, path):
                self.View = self.__class__.View(service, rules, path + [("View", "")])
                self.Reports = self.__class__.Reports(service, rules, path + [("Reports", "")])
                self.SurfaceDefs = self.__class__.SurfaceDefs(service, rules, path + [("SurfaceDefs", "")])
                self.Graphics = self.__class__.Graphics(service, rules, path + [("Graphics", "")])
                self.ResultsExternalInfo = self.__class__.ResultsExternalInfo(service, rules, path + [("ResultsExternalInfo", "")])
                self.Plots = self.__class__.Plots(service, rules, path + [("Plots", "")])
                self.CreateMultipleIsosurfaces = self.__class__.CreateMultipleIsosurfaces(service, rules, "CreateMultipleIsosurfaces", path)
                self.CreateCellZoneSurfaces = self.__class__.CreateCellZoneSurfaces(service, rules, "CreateCellZoneSurfaces", path)
                self.CreateMultiplePlanes = self.__class__.CreateMultiplePlanes(service, rules, "CreateMultiplePlanes", path)
                self.GetXYData = self.__class__.GetXYData(service, rules, "GetXYData", path)
                self.GetFieldMinMax = self.__class__.GetFieldMinMax(service, rules, "GetFieldMinMax", path)
                super().__init__(service, rules, path)

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
                            self.Projection = self.__class__.Projection(service, rules, path + [("Projection", "")])
                            self.Width = self.__class__.Width(service, rules, path + [("Width", "")])
                            super().__init__(service, rules, path)

                        class UpVector(PyMenu):
                            """
                            Singleton UpVector.
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

                        class Target(PyMenu):
                            """
                            Singleton Target.
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

                        class Projection(PyMenu):
                            """
                            Parameter Projection of value type str.
                            """
                            pass

                        class Width(PyMenu):
                            """
                            Parameter Width of value type float.
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

            class Reports(PyNamedObjectContainer):
                class _Reports(PyMenu):
                    """
                    Singleton _Reports.
                    """
                    def __init__(self, service, rules, path):
                        self.DensitySpecification = self.__class__.DensitySpecification(service, rules, path + [("DensitySpecification", "")])
                        self.ForEach = self.__class__.ForEach(service, rules, path + [("ForEach", "")])
                        self.VelocityField = self.__class__.VelocityField(service, rules, path + [("VelocityField", "")])
                        self.Volumes = self.__class__.Volumes(service, rules, path + [("Volumes", "")])
                        self.VolumeFractionField = self.__class__.VolumeFractionField(service, rules, path + [("VolumeFractionField", "")])
                        self.DensityConstant = self.__class__.DensityConstant(service, rules, path + [("DensityConstant", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                        self.Quantity = self.__class__.Quantity(service, rules, path + [("Quantity", "")])
                        self.DensityField = self.__class__.DensityField(service, rules, path + [("DensityField", "")])
                        self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                        self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                        self.Expression = self.__class__.Expression(service, rules, path + [("Expression", "")])
                        self.PlotReport = self.__class__.PlotReport(service, rules, "PlotReport", path)
                        self.PrintReport = self.__class__.PrintReport(service, rules, "PrintReport", path)
                        self.SaveReport = self.__class__.SaveReport(service, rules, "SaveReport", path)
                        self.GetReport = self.__class__.GetReport(service, rules, "GetReport", path)
                        super().__init__(service, rules, path)

                    class DensitySpecification(PyMenu):
                        """
                        Parameter DensitySpecification of value type str.
                        """
                        pass

                    class ForEach(PyMenu):
                        """
                        Parameter ForEach of value type bool.
                        """
                        pass

                    class VelocityField(PyMenu):
                        """
                        Parameter VelocityField of value type str.
                        """
                        pass

                    class Volumes(PyMenu):
                        """
                        Parameter Volumes of value type List[str].
                        """
                        pass

                    class VolumeFractionField(PyMenu):
                        """
                        Parameter VolumeFractionField of value type str.
                        """
                        pass

                    class DensityConstant(PyMenu):
                        """
                        Parameter DensityConstant of value type float.
                        """
                        pass

                    class _name_(PyMenu):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                    class Type(PyMenu):
                        """
                        Parameter Type of value type str.
                        """
                        pass

                    class Quantity(PyMenu):
                        """
                        Parameter Quantity of value type str.
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

                    class Field(PyMenu):
                        """
                        Parameter Field of value type str.
                        """
                        pass

                    class Expression(PyMenu):
                        """
                        Parameter Expression of value type str.
                        """
                        pass

                    class PlotReport(PyCommand):
                        """
                        PlotReport(TimestepSelection: Dict[str, Any], Title: str, XAxis: str, XAxisLabel: str, YAxisLabel: str) -> None
                        """
                        pass

                    class PrintReport(PyCommand):
                        """
                        PrintReport(TimestepSelection: Dict[str, Any]) -> None
                        """
                        pass

                    class SaveReport(PyCommand):
                        """
                        SaveReport(Filename: str, TimestepSelection: Dict[str, Any]) -> None
                        """
                        pass

                    class GetReport(PyCommand):
                        """
                        GetReport(TimestepSelection: Dict[str, Any]) -> List[float]
                        """
                        pass

                def __getitem__(self, key: str) -> _Reports:
                    return super().__getitem__(key)

            class SurfaceDefs(PyNamedObjectContainer):
                class _SurfaceDefs(PyMenu):
                    """
                    Singleton _SurfaceDefs.
                    """
                    def __init__(self, service, rules, path):
                        self.IsoClipSettings = self.__class__.IsoClipSettings(service, rules, path + [("IsoClipSettings", "")])
                        self.ZoneSettings = self.__class__.ZoneSettings(service, rules, path + [("ZoneSettings", "")])
                        self.PlaneSettings = self.__class__.PlaneSettings(service, rules, path + [("PlaneSettings", "")])
                        self.LineSettings = self.__class__.LineSettings(service, rules, path + [("LineSettings", "")])
                        self.PointSettings = self.__class__.PointSettings(service, rules, path + [("PointSettings", "")])
                        self.IsosurfaceSettings = self.__class__.IsosurfaceSettings(service, rules, path + [("IsosurfaceSettings", "")])
                        self.RakeSettings = self.__class__.RakeSettings(service, rules, path + [("RakeSettings", "")])
                        self.GroupName = self.__class__.GroupName(service, rules, path + [("GroupName", "")])
                        self.SurfaceId = self.__class__.SurfaceId(service, rules, path + [("SurfaceId", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        self.SurfaceDim = self.__class__.SurfaceDim(service, rules, path + [("SurfaceDim", "")])
                        self.SurfaceType = self.__class__.SurfaceType(service, rules, path + [("SurfaceType", "")])
                        self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                        self.Display = self.__class__.Display(service, rules, "Display", path)
                        self.Ungroup = self.__class__.Ungroup(service, rules, "Ungroup", path)
                        self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                        super().__init__(service, rules, path)

                    class IsoClipSettings(PyMenu):
                        """
                        Singleton IsoClipSettings.
                        """
                        def __init__(self, service, rules, path):
                            self.Minimum = self.__class__.Minimum(service, rules, path + [("Minimum", "")])
                            self.Maximum = self.__class__.Maximum(service, rules, path + [("Maximum", "")])
                            self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                            self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                            self.UpdateMinMax = self.__class__.UpdateMinMax(service, rules, "UpdateMinMax", path)
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

                        class Field(PyMenu):
                            """
                            Parameter Field of value type str.
                            """
                            pass

                        class Surfaces(PyMenu):
                            """
                            Parameter Surfaces of value type List[str].
                            """
                            pass

                        class UpdateMinMax(PyCommand):
                            """
                            UpdateMinMax() -> None
                            """
                            pass

                    class ZoneSettings(PyMenu):
                        """
                        Singleton ZoneSettings.
                        """
                        def __init__(self, service, rules, path):
                            self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                            self.ZId = self.__class__.ZId(service, rules, path + [("ZId", "")])
                            self.ZType = self.__class__.ZType(service, rules, path + [("ZType", "")])
                            self.IdList = self.__class__.IdList(service, rules, path + [("IdList", "")])
                            super().__init__(service, rules, path)

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

                        class ZType(PyMenu):
                            """
                            Parameter ZType of value type str.
                            """
                            pass

                        class IdList(PyMenu):
                            """
                            Parameter IdList of value type List[int].
                            """
                            pass

                    class PlaneSettings(PyMenu):
                        """
                        Singleton PlaneSettings.
                        """
                        def __init__(self, service, rules, path):
                            self.ThirdPoint = self.__class__.ThirdPoint(service, rules, path + [("ThirdPoint", "")])
                            self.SecondPoint = self.__class__.SecondPoint(service, rules, path + [("SecondPoint", "")])
                            self.FirstPoint = self.__class__.FirstPoint(service, rules, path + [("FirstPoint", "")])
                            self.Normal = self.__class__.Normal(service, rules, path + [("Normal", "")])
                            self.CreationMode = self.__class__.CreationMode(service, rules, path + [("CreationMode", "")])
                            self.X = self.__class__.X(service, rules, path + [("X", "")])
                            self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                            self.Bounded = self.__class__.Bounded(service, rules, path + [("Bounded", "")])
                            self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                            super().__init__(service, rules, path)

                        class ThirdPoint(PyMenu):
                            """
                            Singleton ThirdPoint.
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

                        class SecondPoint(PyMenu):
                            """
                            Singleton SecondPoint.
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

                        class Normal(PyMenu):
                            """
                            Singleton Normal.
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

                        class Y(PyMenu):
                            """
                            Parameter Y of value type float.
                            """
                            pass

                    class LineSettings(PyMenu):
                        """
                        Singleton LineSettings.
                        """
                        def __init__(self, service, rules, path):
                            self.StartPoint = self.__class__.StartPoint(service, rules, path + [("StartPoint", "")])
                            self.EndPoint = self.__class__.EndPoint(service, rules, path + [("EndPoint", "")])
                            super().__init__(service, rules, path)

                        class StartPoint(PyMenu):
                            """
                            Singleton StartPoint.
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

                        class EndPoint(PyMenu):
                            """
                            Singleton EndPoint.
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

                    class PointSettings(PyMenu):
                        """
                        Singleton PointSettings.
                        """
                        def __init__(self, service, rules, path):
                            self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                            self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                            self.X = self.__class__.X(service, rules, path + [("X", "")])
                            self.LbClipping = self.__class__.LbClipping(service, rules, path + [("LbClipping", "")])
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

                        class LbClipping(PyMenu):
                            """
                            Parameter LbClipping of value type bool.
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
                            self.IsoValue = self.__class__.IsoValue(service, rules, path + [("IsoValue", "")])
                            self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                            self.Maximum = self.__class__.Maximum(service, rules, path + [("Maximum", "")])
                            self.Zones = self.__class__.Zones(service, rules, path + [("Zones", "")])
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

                        class IsoValue(PyMenu):
                            """
                            Parameter IsoValue of value type float.
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

                        class Zones(PyMenu):
                            """
                            Parameter Zones of value type List[str].
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
                            self.StartPoint = self.__class__.StartPoint(service, rules, path + [("StartPoint", "")])
                            self.EndPoint = self.__class__.EndPoint(service, rules, path + [("EndPoint", "")])
                            self.NumberOfPoints = self.__class__.NumberOfPoints(service, rules, path + [("NumberOfPoints", "")])
                            super().__init__(service, rules, path)

                        class StartPoint(PyMenu):
                            """
                            Singleton StartPoint.
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

                        class EndPoint(PyMenu):
                            """
                            Singleton EndPoint.
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

                        class NumberOfPoints(PyMenu):
                            """
                            Parameter NumberOfPoints of value type int.
                            """
                            pass

                    class GroupName(PyMenu):
                        """
                        Parameter GroupName of value type str.
                        """
                        pass

                    class SurfaceId(PyMenu):
                        """
                        Parameter SurfaceId of value type int.
                        """
                        pass

                    class _name_(PyMenu):
                        """
                        Parameter _name_ of value type str.
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

                    class SaveImage(PyCommand):
                        """
                        SaveImage(FileName: str, Format: str, FileType: str, Coloring: str, Orientation: str, UseWhiteBackground: bool, Resolution: Dict[str, Any]) -> bool
                        """
                        pass

                def __getitem__(self, key: str) -> _SurfaceDefs:
                    return super().__getitem__(key)

            class Graphics(PyMenu):
                """
                Singleton Graphics.
                """
                def __init__(self, service, rules, path):
                    self.LIC = self.__class__.LIC(service, rules, path + [("LIC", "")])
                    self.Mesh = self.__class__.Mesh(service, rules, path + [("Mesh", "")])
                    self.PeriodicInstances = self.__class__.PeriodicInstances(service, rules, path + [("PeriodicInstances", "")])
                    self.Vector = self.__class__.Vector(service, rules, path + [("Vector", "")])
                    self.XYPlot = self.__class__.XYPlot(service, rules, path + [("XYPlot", "")])
                    self.ParticleTracks = self.__class__.ParticleTracks(service, rules, path + [("ParticleTracks", "")])
                    self.Pathlines = self.__class__.Pathlines(service, rules, path + [("Pathlines", "")])
                    self.TransientPlot = self.__class__.TransientPlot(service, rules, path + [("TransientPlot", "")])
                    self.VolumeRender = self.__class__.VolumeRender(service, rules, path + [("VolumeRender", "")])
                    self.Scene = self.__class__.Scene(service, rules, path + [("Scene", "")])
                    self.Contour = self.__class__.Contour(service, rules, path + [("Contour", "")])
                    self.MirrorPlanes = self.__class__.MirrorPlanes(service, rules, path + [("MirrorPlanes", "")])
                    self.GridColors = self.__class__.GridColors(service, rules, path + [("GridColors", "")])
                    self.CameraSettings = self.__class__.CameraSettings(service, rules, path + [("CameraSettings", "")])
                    self.GraphicsCreationCount = self.__class__.GraphicsCreationCount(service, rules, path + [("GraphicsCreationCount", "")])
                    self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                    super().__init__(service, rules, path)

                class LIC(PyNamedObjectContainer):
                    class _LIC(PyMenu):
                        """
                        Singleton _LIC.
                        """
                        def __init__(self, service, rules, path):
                            self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                            self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                            self.TextureSpacing = self.__class__.TextureSpacing(service, rules, path + [("TextureSpacing", "")])
                            self.OrientedLic = self.__class__.OrientedLic(service, rules, path + [("OrientedLic", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.LicNormalize = self.__class__.LicNormalize(service, rules, path + [("LicNormalize", "")])
                            self.ImageFilter = self.__class__.ImageFilter(service, rules, path + [("ImageFilter", "")])
                            self.SyncStatus = self.__class__.SyncStatus(service, rules, path + [("SyncStatus", "")])
                            self.OverlayedMesh = self.__class__.OverlayedMesh(service, rules, path + [("OverlayedMesh", "")])
                            self.IntensityAlpha = self.__class__.IntensityAlpha(service, rules, path + [("IntensityAlpha", "")])
                            self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                            self.TextureSize = self.__class__.TextureSize(service, rules, path + [("TextureSize", "")])
                            self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                            self.LicPixelInterp = self.__class__.LicPixelInterp(service, rules, path + [("LicPixelInterp", "")])
                            self.IntensityFactor = self.__class__.IntensityFactor(service, rules, path + [("IntensityFactor", "")])
                            self.DrawMesh = self.__class__.DrawMesh(service, rules, path + [("DrawMesh", "")])
                            self.GrayScale = self.__class__.GrayScale(service, rules, path + [("GrayScale", "")])
                            self.FastLic = self.__class__.FastLic(service, rules, path + [("FastLic", "")])
                            self.LicColor = self.__class__.LicColor(service, rules, path + [("LicColor", "")])
                            self.ImageToDisplay = self.__class__.ImageToDisplay(service, rules, path + [("ImageToDisplay", "")])
                            self.WindowId = self.__class__.WindowId(service, rules, path + [("WindowId", "")])
                            self.VectorField = self.__class__.VectorField(service, rules, path + [("VectorField", "")])
                            self.LicColorByField = self.__class__.LicColorByField(service, rules, path + [("LicColorByField", "")])
                            self.LicMaxSteps = self.__class__.LicMaxSteps(service, rules, path + [("LicMaxSteps", "")])
                            self.Push = self.__class__.Push(service, rules, "Push", path)
                            self.Pull = self.__class__.Pull(service, rules, "Pull", path)
                            self.SaveAnimation = self.__class__.SaveAnimation(service, rules, "SaveAnimation", path)
                            self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                            self.Display = self.__class__.Display(service, rules, "Display", path)
                            self.Diff = self.__class__.Diff(service, rules, "Diff", path)
                            super().__init__(service, rules, path)

                        class Range(PyMenu):
                            """
                            Singleton Range.
                            """
                            def __init__(self, service, rules, path):
                                self.ClipToRange = self.__class__.ClipToRange(service, rules, path + [("ClipToRange", "")])
                                self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
                                self.MaxValue = self.__class__.MaxValue(service, rules, path + [("MaxValue", "")])
                                self.GlobalRange = self.__class__.GlobalRange(service, rules, path + [("GlobalRange", "")])
                                self.MinValue = self.__class__.MinValue(service, rules, path + [("MinValue", "")])
                                super().__init__(service, rules, path)

                            class ClipToRange(PyMenu):
                                """
                                Parameter ClipToRange of value type bool.
                                """
                                pass

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

                        class ColorMap(PyMenu):
                            """
                            Singleton ColorMap.
                            """
                            def __init__(self, service, rules, path):
                                self.IsLogScale = self.__class__.IsLogScale(service, rules, path + [("IsLogScale", "")])
                                self.Skip = self.__class__.Skip(service, rules, path + [("Skip", "")])
                                self.ShowAll = self.__class__.ShowAll(service, rules, path + [("ShowAll", "")])
                                self.Position = self.__class__.Position(service, rules, path + [("Position", "")])
                                self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                                self.Precision = self.__class__.Precision(service, rules, path + [("Precision", "")])
                                self.Visible = self.__class__.Visible(service, rules, path + [("Visible", "")])
                                self.Size = self.__class__.Size(service, rules, path + [("Size", "")])
                                self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                                super().__init__(service, rules, path)

                            class IsLogScale(PyMenu):
                                """
                                Parameter IsLogScale of value type bool.
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

                            class Position(PyMenu):
                                """
                                Parameter Position of value type str.
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

                            class ColorMap(PyMenu):
                                """
                                Parameter ColorMap of value type str.
                                """
                                pass

                        class TextureSpacing(PyMenu):
                            """
                            Parameter TextureSpacing of value type int.
                            """
                            pass

                        class OrientedLic(PyMenu):
                            """
                            Parameter OrientedLic of value type bool.
                            """
                            pass

                        class _name_(PyMenu):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                        class LicNormalize(PyMenu):
                            """
                            Parameter LicNormalize of value type bool.
                            """
                            pass

                        class ImageFilter(PyMenu):
                            """
                            Parameter ImageFilter of value type str.
                            """
                            pass

                        class SyncStatus(PyMenu):
                            """
                            Parameter SyncStatus of value type str.
                            """
                            pass

                        class OverlayedMesh(PyMenu):
                            """
                            Parameter OverlayedMesh of value type str.
                            """
                            pass

                        class IntensityAlpha(PyMenu):
                            """
                            Parameter IntensityAlpha of value type bool.
                            """
                            pass

                        class Surfaces(PyMenu):
                            """
                            Parameter Surfaces of value type List[str].
                            """
                            pass

                        class TextureSize(PyMenu):
                            """
                            Parameter TextureSize of value type int.
                            """
                            pass

                        class Field(PyMenu):
                            """
                            Parameter Field of value type str.
                            """
                            pass

                        class LicPixelInterp(PyMenu):
                            """
                            Parameter LicPixelInterp of value type bool.
                            """
                            pass

                        class IntensityFactor(PyMenu):
                            """
                            Parameter IntensityFactor of value type int.
                            """
                            pass

                        class DrawMesh(PyMenu):
                            """
                            Parameter DrawMesh of value type bool.
                            """
                            pass

                        class GrayScale(PyMenu):
                            """
                            Parameter GrayScale of value type bool.
                            """
                            pass

                        class FastLic(PyMenu):
                            """
                            Parameter FastLic of value type bool.
                            """
                            pass

                        class LicColor(PyMenu):
                            """
                            Parameter LicColor of value type str.
                            """
                            pass

                        class ImageToDisplay(PyMenu):
                            """
                            Parameter ImageToDisplay of value type str.
                            """
                            pass

                        class WindowId(PyMenu):
                            """
                            Parameter WindowId of value type int.
                            """
                            pass

                        class VectorField(PyMenu):
                            """
                            Parameter VectorField of value type str.
                            """
                            pass

                        class LicColorByField(PyMenu):
                            """
                            Parameter LicColorByField of value type bool.
                            """
                            pass

                        class LicMaxSteps(PyMenu):
                            """
                            Parameter LicMaxSteps of value type int.
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

                        class SaveAnimation(PyCommand):
                            """
                            SaveAnimation(FileName: str, Format: str, FPS: float, AntiAliasingPasses: str, Quality: str, H264: bool, Compression: str, BitRate: int, JPegQuality: int, PPMFormat: str, UseWhiteBackground: bool, Orientation: str, Resolution: Dict[str, Any]) -> None
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

                        class Diff(PyCommand):
                            """
                            Diff() -> bool
                            """
                            pass

                    def __getitem__(self, key: str) -> _LIC:
                        return super().__getitem__(key)

                class Mesh(PyNamedObjectContainer):
                    class _Mesh(PyMenu):
                        """
                        Singleton _Mesh.
                        """
                        def __init__(self, service, rules, path):
                            self.Options = self.__class__.Options(service, rules, path + [("Options", "")])
                            self.EdgeOptions = self.__class__.EdgeOptions(service, rules, path + [("EdgeOptions", "")])
                            self.MeshColoring = self.__class__.MeshColoring(service, rules, path + [("MeshColoring", "")])
                            self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                            self.ShrinkFactor = self.__class__.ShrinkFactor(service, rules, path + [("ShrinkFactor", "")])
                            self.WindowId = self.__class__.WindowId(service, rules, path + [("WindowId", "")])
                            self.SyncStatus = self.__class__.SyncStatus(service, rules, path + [("SyncStatus", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.Diff = self.__class__.Diff(service, rules, "Diff", path)
                            self.AddToViewport = self.__class__.AddToViewport(service, rules, "AddToViewport", path)
                            self.Display = self.__class__.Display(service, rules, "Display", path)
                            self.SaveAnimation = self.__class__.SaveAnimation(service, rules, "SaveAnimation", path)
                            self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                            self.Push = self.__class__.Push(service, rules, "Push", path)
                            self.Pull = self.__class__.Pull(service, rules, "Pull", path)
                            self.DisplayInViewport = self.__class__.DisplayInViewport(service, rules, "DisplayInViewport", path)
                            super().__init__(service, rules, path)

                        class Options(PyMenu):
                            """
                            Singleton Options.
                            """
                            def __init__(self, service, rules, path):
                                self.Partitions = self.__class__.Partitions(service, rules, path + [("Partitions", "")])
                                self.Edges = self.__class__.Edges(service, rules, path + [("Edges", "")])
                                self.Overset = self.__class__.Overset(service, rules, path + [("Overset", "")])
                                self.Nodes = self.__class__.Nodes(service, rules, path + [("Nodes", "")])
                                self.Faces = self.__class__.Faces(service, rules, path + [("Faces", "")])
                                super().__init__(service, rules, path)

                            class Partitions(PyMenu):
                                """
                                Parameter Partitions of value type bool.
                                """
                                pass

                            class Edges(PyMenu):
                                """
                                Parameter Edges of value type bool.
                                """
                                pass

                            class Overset(PyMenu):
                                """
                                Parameter Overset of value type bool.
                                """
                                pass

                            class Nodes(PyMenu):
                                """
                                Parameter Nodes of value type bool.
                                """
                                pass

                            class Faces(PyMenu):
                                """
                                Parameter Faces of value type bool.
                                """
                                pass

                        class EdgeOptions(PyMenu):
                            """
                            Singleton EdgeOptions.
                            """
                            def __init__(self, service, rules, path):
                                self.FeatureAngle = self.__class__.FeatureAngle(service, rules, path + [("FeatureAngle", "")])
                                self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                                super().__init__(service, rules, path)

                            class FeatureAngle(PyMenu):
                                """
                                Parameter FeatureAngle of value type float.
                                """
                                pass

                            class Type(PyMenu):
                                """
                                Parameter Type of value type str.
                                """
                                pass

                        class MeshColoring(PyMenu):
                            """
                            Singleton MeshColoring.
                            """
                            def __init__(self, service, rules, path):
                                self.ColorEdgesBy = self.__class__.ColorEdgesBy(service, rules, path + [("ColorEdgesBy", "")])
                                self.ColorNodesBy = self.__class__.ColorNodesBy(service, rules, path + [("ColorNodesBy", "")])
                                self.Automatic = self.__class__.Automatic(service, rules, path + [("Automatic", "")])
                                self.ColorBy = self.__class__.ColorBy(service, rules, path + [("ColorBy", "")])
                                self.ColorFacesBy = self.__class__.ColorFacesBy(service, rules, path + [("ColorFacesBy", "")])
                                super().__init__(service, rules, path)

                            class ColorEdgesBy(PyMenu):
                                """
                                Parameter ColorEdgesBy of value type str.
                                """
                                pass

                            class ColorNodesBy(PyMenu):
                                """
                                Parameter ColorNodesBy of value type str.
                                """
                                pass

                            class Automatic(PyMenu):
                                """
                                Parameter Automatic of value type bool.
                                """
                                pass

                            class ColorBy(PyMenu):
                                """
                                Parameter ColorBy of value type str.
                                """
                                pass

                            class ColorFacesBy(PyMenu):
                                """
                                Parameter ColorFacesBy of value type str.
                                """
                                pass

                        class Surfaces(PyMenu):
                            """
                            Parameter Surfaces of value type List[str].
                            """
                            pass

                        class ShrinkFactor(PyMenu):
                            """
                            Parameter ShrinkFactor of value type float.
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

                        class Diff(PyCommand):
                            """
                            Diff() -> bool
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

                        class SaveAnimation(PyCommand):
                            """
                            SaveAnimation(FileName: str, Format: str, FPS: float, AntiAliasingPasses: str, Quality: str, H264: bool, Compression: str, BitRate: int, JPegQuality: int, PPMFormat: str, UseWhiteBackground: bool, Orientation: str, Resolution: Dict[str, Any]) -> None
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

                        class DisplayInViewport(PyCommand):
                            """
                            DisplayInViewport(Viewport: str) -> bool
                            """
                            pass

                    def __getitem__(self, key: str) -> _Mesh:
                        return super().__getitem__(key)

                class PeriodicInstances(PyNamedObjectContainer):
                    class _PeriodicInstances(PyMenu):
                        """
                        Singleton _PeriodicInstances.
                        """
                        def __init__(self, service, rules, path):
                            self.TranslationVector = self.__class__.TranslationVector(service, rules, path + [("TranslationVector", "")])
                            self.PointOnAxis = self.__class__.PointOnAxis(service, rules, path + [("PointOnAxis", "")])
                            self.PeriodicType = self.__class__.PeriodicType(service, rules, path + [("PeriodicType", "")])
                            self.NumberOfRepeats = self.__class__.NumberOfRepeats(service, rules, path + [("NumberOfRepeats", "")])
                            self.Angle = self.__class__.Angle(service, rules, path + [("Angle", "")])
                            self.AllSurfaces = self.__class__.AllSurfaces(service, rules, path + [("AllSurfaces", "")])
                            self.NoOfSections = self.__class__.NoOfSections(service, rules, path + [("NoOfSections", "")])
                            self.RotationAxis = self.__class__.RotationAxis(service, rules, path + [("RotationAxis", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
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

                        class PeriodicType(PyMenu):
                            """
                            Parameter PeriodicType of value type str.
                            """
                            pass

                        class NumberOfRepeats(PyMenu):
                            """
                            Parameter NumberOfRepeats of value type int.
                            """
                            pass

                        class Angle(PyMenu):
                            """
                            Parameter Angle of value type float.
                            """
                            pass

                        class AllSurfaces(PyMenu):
                            """
                            Parameter AllSurfaces of value type bool.
                            """
                            pass

                        class NoOfSections(PyMenu):
                            """
                            Parameter NoOfSections of value type int.
                            """
                            pass

                        class RotationAxis(PyMenu):
                            """
                            Parameter RotationAxis of value type str.
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

                    def __getitem__(self, key: str) -> _PeriodicInstances:
                        return super().__getitem__(key)

                class Vector(PyNamedObjectContainer):
                    class _Vector(PyMenu):
                        """
                        Singleton _Vector.
                        """
                        def __init__(self, service, rules, path):
                            self.Scale = self.__class__.Scale(service, rules, path + [("Scale", "")])
                            self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                            self.VectorOptions = self.__class__.VectorOptions(service, rules, path + [("VectorOptions", "")])
                            self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.Skip = self.__class__.Skip(service, rules, path + [("Skip", "")])
                            self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                            self.Style = self.__class__.Style(service, rules, path + [("Style", "")])
                            self.WindowId = self.__class__.WindowId(service, rules, path + [("WindowId", "")])
                            self.SyncStatus = self.__class__.SyncStatus(service, rules, path + [("SyncStatus", "")])
                            self.VectorField = self.__class__.VectorField(service, rules, path + [("VectorField", "")])
                            self.OverlayedMesh = self.__class__.OverlayedMesh(service, rules, path + [("OverlayedMesh", "")])
                            self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                            self.DrawMesh = self.__class__.DrawMesh(service, rules, path + [("DrawMesh", "")])
                            self.Display = self.__class__.Display(service, rules, "Display", path)
                            self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                            self.AddToViewport = self.__class__.AddToViewport(service, rules, "AddToViewport", path)
                            self.Push = self.__class__.Push(service, rules, "Push", path)
                            self.UpdateMinMax = self.__class__.UpdateMinMax(service, rules, "UpdateMinMax", path)
                            self.Pull = self.__class__.Pull(service, rules, "Pull", path)
                            self.SaveAnimation = self.__class__.SaveAnimation(service, rules, "SaveAnimation", path)
                            self.DisplayInViewport = self.__class__.DisplayInViewport(service, rules, "DisplayInViewport", path)
                            self.Diff = self.__class__.Diff(service, rules, "Diff", path)
                            super().__init__(service, rules, path)

                        class Scale(PyMenu):
                            """
                            Singleton Scale.
                            """
                            def __init__(self, service, rules, path):
                                self.Scale = self.__class__.Scale(service, rules, path + [("Scale", "")])
                                self.AutoScale = self.__class__.AutoScale(service, rules, path + [("AutoScale", "")])
                                super().__init__(service, rules, path)

                            class Scale(PyMenu):
                                """
                                Parameter Scale of value type float.
                                """
                                pass

                            class AutoScale(PyMenu):
                                """
                                Parameter AutoScale of value type bool.
                                """
                                pass

                        class ColorMap(PyMenu):
                            """
                            Singleton ColorMap.
                            """
                            def __init__(self, service, rules, path):
                                self.Precision = self.__class__.Precision(service, rules, path + [("Precision", "")])
                                self.IsLogScale = self.__class__.IsLogScale(service, rules, path + [("IsLogScale", "")])
                                self.Position = self.__class__.Position(service, rules, path + [("Position", "")])
                                self.ShowAll = self.__class__.ShowAll(service, rules, path + [("ShowAll", "")])
                                self.Size = self.__class__.Size(service, rules, path + [("Size", "")])
                                self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                                self.Skip = self.__class__.Skip(service, rules, path + [("Skip", "")])
                                self.Visible = self.__class__.Visible(service, rules, path + [("Visible", "")])
                                self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                                super().__init__(service, rules, path)

                            class Precision(PyMenu):
                                """
                                Parameter Precision of value type int.
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

                            class Skip(PyMenu):
                                """
                                Parameter Skip of value type int.
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

                        class VectorOptions(PyMenu):
                            """
                            Singleton VectorOptions.
                            """
                            def __init__(self, service, rules, path):
                                self.InPlane = self.__class__.InPlane(service, rules, path + [("InPlane", "")])
                                self.ZComponent = self.__class__.ZComponent(service, rules, path + [("ZComponent", "")])
                                self.XComponent = self.__class__.XComponent(service, rules, path + [("XComponent", "")])
                                self.FixedLength = self.__class__.FixedLength(service, rules, path + [("FixedLength", "")])
                                self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                self.HeadScale = self.__class__.HeadScale(service, rules, path + [("HeadScale", "")])
                                self.YComponent = self.__class__.YComponent(service, rules, path + [("YComponent", "")])
                                super().__init__(service, rules, path)

                            class InPlane(PyMenu):
                                """
                                Parameter InPlane of value type bool.
                                """
                                pass

                            class ZComponent(PyMenu):
                                """
                                Parameter ZComponent of value type bool.
                                """
                                pass

                            class XComponent(PyMenu):
                                """
                                Parameter XComponent of value type bool.
                                """
                                pass

                            class FixedLength(PyMenu):
                                """
                                Parameter FixedLength of value type bool.
                                """
                                pass

                            class Color(PyMenu):
                                """
                                Parameter Color of value type str.
                                """
                                pass

                            class HeadScale(PyMenu):
                                """
                                Parameter HeadScale of value type float.
                                """
                                pass

                            class YComponent(PyMenu):
                                """
                                Parameter YComponent of value type bool.
                                """
                                pass

                        class Range(PyMenu):
                            """
                            Singleton Range.
                            """
                            def __init__(self, service, rules, path):
                                self.MinValue = self.__class__.MinValue(service, rules, path + [("MinValue", "")])
                                self.MaxValue = self.__class__.MaxValue(service, rules, path + [("MaxValue", "")])
                                self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
                                self.ClipToRange = self.__class__.ClipToRange(service, rules, path + [("ClipToRange", "")])
                                self.GlobalRange = self.__class__.GlobalRange(service, rules, path + [("GlobalRange", "")])
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

                        class _name_(PyMenu):
                            """
                            Parameter _name_ of value type str.
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

                        class Style(PyMenu):
                            """
                            Parameter Style of value type str.
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

                        class AddToViewport(PyCommand):
                            """
                            AddToViewport(Viewport: str) -> bool
                            """
                            pass

                        class Push(PyCommand):
                            """
                            Push() -> bool
                            """
                            pass

                        class UpdateMinMax(PyCommand):
                            """
                            UpdateMinMax() -> None
                            """
                            pass

                        class Pull(PyCommand):
                            """
                            Pull() -> bool
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

                        class Diff(PyCommand):
                            """
                            Diff() -> bool
                            """
                            pass

                    def __getitem__(self, key: str) -> _Vector:
                        return super().__getitem__(key)

                class XYPlot(PyNamedObjectContainer):
                    class _XYPlot(PyMenu):
                        """
                        Singleton _XYPlot.
                        """
                        def __init__(self, service, rules, path):
                            self.Axes = self.__class__.Axes(service, rules, path + [("Axes", "")])
                            self.DirectionVectorInternal = self.__class__.DirectionVectorInternal(service, rules, path + [("DirectionVectorInternal", "")])
                            self.Curves = self.__class__.Curves(service, rules, path + [("Curves", "")])
                            self.YAxisFunction = self.__class__.YAxisFunction(service, rules, path + [("YAxisFunction", "")])
                            self.XAxisFunction = self.__class__.XAxisFunction(service, rules, path + [("XAxisFunction", "")])
                            self.Options = self.__class__.Options(service, rules, path + [("Options", "")])
                            self.UID = self.__class__.UID(service, rules, path + [("UID", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.WindowId = self.__class__.WindowId(service, rules, path + [("WindowId", "")])
                            self.SyncStatus = self.__class__.SyncStatus(service, rules, path + [("SyncStatus", "")])
                            self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                            self.Plot = self.__class__.Plot(service, rules, "Plot", path)
                            self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                            self.Diff = self.__class__.Diff(service, rules, "Diff", path)
                            self.Pull = self.__class__.Pull(service, rules, "Pull", path)
                            self.ExportData = self.__class__.ExportData(service, rules, "ExportData", path)
                            self.Push = self.__class__.Push(service, rules, "Push", path)
                            super().__init__(service, rules, path)

                        class Axes(PyMenu):
                            """
                            Singleton Axes.
                            """
                            def __init__(self, service, rules, path):
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                super().__init__(service, rules, path)

                            class X(PyMenu):
                                """
                                Singleton X.
                                """
                                def __init__(self, service, rules, path):
                                    self.MajorRules = self.__class__.MajorRules(service, rules, path + [("MajorRules", "")])
                                    self.NumberFormat = self.__class__.NumberFormat(service, rules, path + [("NumberFormat", "")])
                                    self.MinorRules = self.__class__.MinorRules(service, rules, path + [("MinorRules", "")])
                                    self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                                    self.Options = self.__class__.Options(service, rules, path + [("Options", "")])
                                    self.Label = self.__class__.Label(service, rules, path + [("Label", "")])
                                    super().__init__(service, rules, path)

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

                                class Options(PyMenu):
                                    """
                                    Singleton Options.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.Log = self.__class__.Log(service, rules, path + [("Log", "")])
                                        self.MajorRules = self.__class__.MajorRules(service, rules, path + [("MajorRules", "")])
                                        self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
                                        self.MinorRules = self.__class__.MinorRules(service, rules, path + [("MinorRules", "")])
                                        super().__init__(service, rules, path)

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

                                    class AutoRange(PyMenu):
                                        """
                                        Parameter AutoRange of value type bool.
                                        """
                                        pass

                                    class MinorRules(PyMenu):
                                        """
                                        Parameter MinorRules of value type bool.
                                        """
                                        pass

                                class Label(PyMenu):
                                    """
                                    Parameter Label of value type str.
                                    """
                                    pass

                            class Y(PyMenu):
                                """
                                Singleton Y.
                                """
                                def __init__(self, service, rules, path):
                                    self.NumberFormat = self.__class__.NumberFormat(service, rules, path + [("NumberFormat", "")])
                                    self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                                    self.MinorRules = self.__class__.MinorRules(service, rules, path + [("MinorRules", "")])
                                    self.MajorRules = self.__class__.MajorRules(service, rules, path + [("MajorRules", "")])
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
                                        self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
                                        self.MajorRules = self.__class__.MajorRules(service, rules, path + [("MajorRules", "")])
                                        self.Log = self.__class__.Log(service, rules, path + [("Log", "")])
                                        self.MinorRules = self.__class__.MinorRules(service, rules, path + [("MinorRules", "")])
                                        super().__init__(service, rules, path)

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

                                    class MinorRules(PyMenu):
                                        """
                                        Parameter MinorRules of value type bool.
                                        """
                                        pass

                                class Label(PyMenu):
                                    """
                                    Parameter Label of value type str.
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
                                    self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                    self.Size = self.__class__.Size(service, rules, path + [("Size", "")])
                                    self.Symbol = self.__class__.Symbol(service, rules, path + [("Symbol", "")])
                                    super().__init__(service, rules, path)

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

                                class Symbol(PyMenu):
                                    """
                                    Parameter Symbol of value type str.
                                    """
                                    pass

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

                        class XAxisFunction(PyMenu):
                            """
                            Singleton XAxisFunction.
                            """
                            def __init__(self, service, rules, path):
                                self.DirectionVector = self.__class__.DirectionVector(service, rules, path + [("DirectionVector", "")])
                                self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                                self.PositionOnCurrentAxis = self.__class__.PositionOnCurrentAxis(service, rules, path + [("PositionOnCurrentAxis", "")])
                                self.XAxisFunctionInternal = self.__class__.XAxisFunctionInternal(service, rules, path + [("XAxisFunctionInternal", "")])
                                super().__init__(service, rules, path)

                            class DirectionVector(PyMenu):
                                """
                                Singleton DirectionVector.
                                """
                                def __init__(self, service, rules, path):
                                    self.YComponent = self.__class__.YComponent(service, rules, path + [("YComponent", "")])
                                    self.XComponent = self.__class__.XComponent(service, rules, path + [("XComponent", "")])
                                    self.ZComponent = self.__class__.ZComponent(service, rules, path + [("ZComponent", "")])
                                    super().__init__(service, rules, path)

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

                                class ZComponent(PyMenu):
                                    """
                                    Parameter ZComponent of value type float.
                                    """
                                    pass

                            class Field(PyMenu):
                                """
                                Parameter Field of value type str.
                                """
                                pass

                            class PositionOnCurrentAxis(PyMenu):
                                """
                                Parameter PositionOnCurrentAxis of value type bool.
                                """
                                pass

                            class XAxisFunctionInternal(PyMenu):
                                """
                                Parameter XAxisFunctionInternal of value type str.
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

                        class ExportData(PyCommand):
                            """
                            ExportData(FileName: str) -> bool
                            """
                            pass

                        class Push(PyCommand):
                            """
                            Push() -> bool
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
                            self.Filter = self.__class__.Filter(service, rules, path + [("Filter", "")])
                            self.Plot = self.__class__.Plot(service, rules, path + [("Plot", "")])
                            self.VectorStyle = self.__class__.VectorStyle(service, rules, path + [("VectorStyle", "")])
                            self.TrackSingleParticleStream = self.__class__.TrackSingleParticleStream(service, rules, path + [("TrackSingleParticleStream", "")])
                            self.Options = self.__class__.Options(service, rules, path + [("Options", "")])
                            self.Style = self.__class__.Style(service, rules, path + [("Style", "")])
                            self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                            self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                            self.DrawMesh = self.__class__.DrawMesh(service, rules, path + [("DrawMesh", "")])
                            self.FreeStreamParticles = self.__class__.FreeStreamParticles(service, rules, path + [("FreeStreamParticles", "")])
                            self.WindowId = self.__class__.WindowId(service, rules, path + [("WindowId", "")])
                            self.OverlayedMesh = self.__class__.OverlayedMesh(service, rules, path + [("OverlayedMesh", "")])
                            self.Skip = self.__class__.Skip(service, rules, path + [("Skip", "")])
                            self.Injections = self.__class__.Injections(service, rules, path + [("Injections", "")])
                            self.TrackPDFParticles = self.__class__.TrackPDFParticles(service, rules, path + [("TrackPDFParticles", "")])
                            self.Coarsen = self.__class__.Coarsen(service, rules, path + [("Coarsen", "")])
                            self.WallFilmParticles = self.__class__.WallFilmParticles(service, rules, path + [("WallFilmParticles", "")])
                            self.SyncStatus = self.__class__.SyncStatus(service, rules, path + [("SyncStatus", "")])
                            self.ParticleTracksField = self.__class__.ParticleTracksField(service, rules, path + [("ParticleTracksField", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.Diff = self.__class__.Diff(service, rules, "Diff", path)
                            self.Pull = self.__class__.Pull(service, rules, "Pull", path)
                            self.Display = self.__class__.Display(service, rules, "Display", path)
                            self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                            self.Push = self.__class__.Push(service, rules, "Push", path)
                            self.SaveAnimation = self.__class__.SaveAnimation(service, rules, "SaveAnimation", path)
                            super().__init__(service, rules, path)

                        class Filter(PyMenu):
                            """
                            Singleton Filter.
                            """
                            def __init__(self, service, rules, path):
                                self.Inside = self.__class__.Inside(service, rules, path + [("Inside", "")])
                                self.MinValue = self.__class__.MinValue(service, rules, path + [("MinValue", "")])
                                self.MaxValue = self.__class__.MaxValue(service, rules, path + [("MaxValue", "")])
                                self.FilterField = self.__class__.FilterField(service, rules, path + [("FilterField", "")])
                                self.Enabled = self.__class__.Enabled(service, rules, path + [("Enabled", "")])
                                super().__init__(service, rules, path)

                            class Inside(PyMenu):
                                """
                                Parameter Inside of value type bool.
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

                            class FilterField(PyMenu):
                                """
                                Parameter FilterField of value type str.
                                """
                                pass

                            class Enabled(PyMenu):
                                """
                                Parameter Enabled of value type bool.
                                """
                                pass

                        class Plot(PyMenu):
                            """
                            Singleton Plot.
                            """
                            def __init__(self, service, rules, path):
                                self.XAxisFunction = self.__class__.XAxisFunction(service, rules, path + [("XAxisFunction", "")])
                                self.Enabled = self.__class__.Enabled(service, rules, path + [("Enabled", "")])
                                super().__init__(service, rules, path)

                            class XAxisFunction(PyMenu):
                                """
                                Parameter XAxisFunction of value type str.
                                """
                                pass

                            class Enabled(PyMenu):
                                """
                                Parameter Enabled of value type bool.
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
                                    self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                    self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                                    self.VectorsOf = self.__class__.VectorsOf(service, rules, path + [("VectorsOf", "")])
                                    self.LengthToHeadRatio = self.__class__.LengthToHeadRatio(service, rules, path + [("LengthToHeadRatio", "")])
                                    self.ConstantColor = self.__class__.ConstantColor(service, rules, path + [("ConstantColor", "")])
                                    self.VariableLength = self.__class__.VariableLength(service, rules, path + [("VariableLength", "")])
                                    self.Length = self.__class__.Length(service, rules, path + [("Length", "")])
                                    self.ScaleFactor = self.__class__.ScaleFactor(service, rules, path + [("ScaleFactor", "")])
                                    super().__init__(service, rules, path)

                                class Color(PyMenu):
                                    """
                                    Parameter Color of value type str.
                                    """
                                    pass

                                class Field(PyMenu):
                                    """
                                    Parameter Field of value type str.
                                    """
                                    pass

                                class VectorsOf(PyMenu):
                                    """
                                    Parameter VectorsOf of value type str.
                                    """
                                    pass

                                class LengthToHeadRatio(PyMenu):
                                    """
                                    Parameter LengthToHeadRatio of value type float.
                                    """
                                    pass

                                class ConstantColor(PyMenu):
                                    """
                                    Parameter ConstantColor of value type bool.
                                    """
                                    pass

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

                                class ScaleFactor(PyMenu):
                                    """
                                    Parameter ScaleFactor of value type float.
                                    """
                                    pass

                            class Style(PyMenu):
                                """
                                Parameter Style of value type str.
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

                        class Style(PyMenu):
                            """
                            Singleton Style.
                            """
                            def __init__(self, service, rules, path):
                                self.Ribbon = self.__class__.Ribbon(service, rules, path + [("Ribbon", "")])
                                self.Sphere = self.__class__.Sphere(service, rules, path + [("Sphere", "")])
                                self.MarkerSize = self.__class__.MarkerSize(service, rules, path + [("MarkerSize", "")])
                                self.Radius = self.__class__.Radius(service, rules, path + [("Radius", "")])
                                self.ArrowSpace = self.__class__.ArrowSpace(service, rules, path + [("ArrowSpace", "")])
                                self.ArrowScale = self.__class__.ArrowScale(service, rules, path + [("ArrowScale", "")])
                                self.LineWidth = self.__class__.LineWidth(service, rules, path + [("LineWidth", "")])
                                self.Style = self.__class__.Style(service, rules, path + [("Style", "")])
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
                                        self.MaxValue = self.__class__.MaxValue(service, rules, path + [("MaxValue", "")])
                                        self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
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

                                    class MinValue(PyMenu):
                                        """
                                        Parameter MinValue of value type float.
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

                            class MarkerSize(PyMenu):
                                """
                                Parameter MarkerSize of value type float.
                                """
                                pass

                            class Radius(PyMenu):
                                """
                                Parameter Radius of value type float.
                                """
                                pass

                            class ArrowSpace(PyMenu):
                                """
                                Parameter ArrowSpace of value type float.
                                """
                                pass

                            class ArrowScale(PyMenu):
                                """
                                Parameter ArrowScale of value type float.
                                """
                                pass

                            class LineWidth(PyMenu):
                                """
                                Parameter LineWidth of value type float.
                                """
                                pass

                            class Style(PyMenu):
                                """
                                Parameter Style of value type str.
                                """
                                pass

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

                        class ColorMap(PyMenu):
                            """
                            Singleton ColorMap.
                            """
                            def __init__(self, service, rules, path):
                                self.Size = self.__class__.Size(service, rules, path + [("Size", "")])
                                self.Precision = self.__class__.Precision(service, rules, path + [("Precision", "")])
                                self.Position = self.__class__.Position(service, rules, path + [("Position", "")])
                                self.ShowAll = self.__class__.ShowAll(service, rules, path + [("ShowAll", "")])
                                self.Skip = self.__class__.Skip(service, rules, path + [("Skip", "")])
                                self.IsLogScale = self.__class__.IsLogScale(service, rules, path + [("IsLogScale", "")])
                                self.Visible = self.__class__.Visible(service, rules, path + [("Visible", "")])
                                self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                                self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                                super().__init__(service, rules, path)

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

                            class IsLogScale(PyMenu):
                                """
                                Parameter IsLogScale of value type bool.
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

                        class DrawMesh(PyMenu):
                            """
                            Parameter DrawMesh of value type bool.
                            """
                            pass

                        class FreeStreamParticles(PyMenu):
                            """
                            Parameter FreeStreamParticles of value type bool.
                            """
                            pass

                        class WindowId(PyMenu):
                            """
                            Parameter WindowId of value type int.
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

                        class Injections(PyMenu):
                            """
                            Parameter Injections of value type List[str].
                            """
                            pass

                        class TrackPDFParticles(PyMenu):
                            """
                            Parameter TrackPDFParticles of value type bool.
                            """
                            pass

                        class Coarsen(PyMenu):
                            """
                            Parameter Coarsen of value type int.
                            """
                            pass

                        class WallFilmParticles(PyMenu):
                            """
                            Parameter WallFilmParticles of value type bool.
                            """
                            pass

                        class SyncStatus(PyMenu):
                            """
                            Parameter SyncStatus of value type str.
                            """
                            pass

                        class ParticleTracksField(PyMenu):
                            """
                            Parameter ParticleTracksField of value type str.
                            """
                            pass

                        class _name_(PyMenu):
                            """
                            Parameter _name_ of value type str.
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

                        class Push(PyCommand):
                            """
                            Push() -> bool
                            """
                            pass

                        class SaveAnimation(PyCommand):
                            """
                            SaveAnimation(FileName: str, Format: str, FPS: float, AntiAliasingPasses: str, Quality: str, H264: bool, Compression: str, BitRate: int, JPegQuality: int, PPMFormat: str, UseWhiteBackground: bool, Orientation: str, Resolution: Dict[str, Any]) -> None
                            """
                            pass

                    def __getitem__(self, key: str) -> _ParticleTracks:
                        return super().__getitem__(key)

                class Pathlines(PyNamedObjectContainer):
                    class _Pathlines(PyMenu):
                        """
                        Singleton _Pathlines.
                        """
                        def __init__(self, service, rules, path):
                            self.Plot = self.__class__.Plot(service, rules, path + [("Plot", "")])
                            self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                            self.Options = self.__class__.Options(service, rules, path + [("Options", "")])
                            self.Style = self.__class__.Style(service, rules, path + [("Style", "")])
                            self.AccuracyControl = self.__class__.AccuracyControl(service, rules, path + [("AccuracyControl", "")])
                            self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                            self.Coarsen = self.__class__.Coarsen(service, rules, path + [("Coarsen", "")])
                            self.OverlayedMesh = self.__class__.OverlayedMesh(service, rules, path + [("OverlayedMesh", "")])
                            self.UID = self.__class__.UID(service, rules, path + [("UID", "")])
                            self.OnZone = self.__class__.OnZone(service, rules, path + [("OnZone", "")])
                            self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                            self.DrawMesh = self.__class__.DrawMesh(service, rules, path + [("DrawMesh", "")])
                            self.VelocityDomain = self.__class__.VelocityDomain(service, rules, path + [("VelocityDomain", "")])
                            self.Skip = self.__class__.Skip(service, rules, path + [("Skip", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.WindowId = self.__class__.WindowId(service, rules, path + [("WindowId", "")])
                            self.SyncStatus = self.__class__.SyncStatus(service, rules, path + [("SyncStatus", "")])
                            self.Step = self.__class__.Step(service, rules, path + [("Step", "")])
                            self.PathlinesField = self.__class__.PathlinesField(service, rules, path + [("PathlinesField", "")])
                            self.Pull = self.__class__.Pull(service, rules, "Pull", path)
                            self.Display = self.__class__.Display(service, rules, "Display", path)
                            self.Push = self.__class__.Push(service, rules, "Push", path)
                            self.Diff = self.__class__.Diff(service, rules, "Diff", path)
                            self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
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

                        class ColorMap(PyMenu):
                            """
                            Singleton ColorMap.
                            """
                            def __init__(self, service, rules, path):
                                self.IsLogScale = self.__class__.IsLogScale(service, rules, path + [("IsLogScale", "")])
                                self.Visible = self.__class__.Visible(service, rules, path + [("Visible", "")])
                                self.Position = self.__class__.Position(service, rules, path + [("Position", "")])
                                self.Skip = self.__class__.Skip(service, rules, path + [("Skip", "")])
                                self.Precision = self.__class__.Precision(service, rules, path + [("Precision", "")])
                                self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                                self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                                self.ShowAll = self.__class__.ShowAll(service, rules, path + [("ShowAll", "")])
                                self.Size = self.__class__.Size(service, rules, path + [("Size", "")])
                                super().__init__(service, rules, path)

                            class IsLogScale(PyMenu):
                                """
                                Parameter IsLogScale of value type bool.
                                """
                                pass

                            class Visible(PyMenu):
                                """
                                Parameter Visible of value type bool.
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

                            class Size(PyMenu):
                                """
                                Parameter Size of value type int.
                                """
                                pass

                        class Options(PyMenu):
                            """
                            Singleton Options.
                            """
                            def __init__(self, service, rules, path):
                                self.NodeValues = self.__class__.NodeValues(service, rules, path + [("NodeValues", "")])
                                self.Reverse = self.__class__.Reverse(service, rules, path + [("Reverse", "")])
                                self.OilFlow = self.__class__.OilFlow(service, rules, path + [("OilFlow", "")])
                                self.Relative = self.__class__.Relative(service, rules, path + [("Relative", "")])
                                super().__init__(service, rules, path)

                            class NodeValues(PyMenu):
                                """
                                Parameter NodeValues of value type bool.
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

                            class Relative(PyMenu):
                                """
                                Parameter Relative of value type bool.
                                """
                                pass

                        class Style(PyMenu):
                            """
                            Singleton Style.
                            """
                            def __init__(self, service, rules, path):
                                self.Ribbon = self.__class__.Ribbon(service, rules, path + [("Ribbon", "")])
                                self.MarkerSize = self.__class__.MarkerSize(service, rules, path + [("MarkerSize", "")])
                                self.ArrowSpace = self.__class__.ArrowSpace(service, rules, path + [("ArrowSpace", "")])
                                self.ArrowScale = self.__class__.ArrowScale(service, rules, path + [("ArrowScale", "")])
                                self.LineWidth = self.__class__.LineWidth(service, rules, path + [("LineWidth", "")])
                                self.Style = self.__class__.Style(service, rules, path + [("Style", "")])
                                self.Radius = self.__class__.Radius(service, rules, path + [("Radius", "")])
                                self.SphereLod = self.__class__.SphereLod(service, rules, path + [("SphereLod", "")])
                                self.SphereSize = self.__class__.SphereSize(service, rules, path + [("SphereSize", "")])
                                super().__init__(service, rules, path)

                            class Ribbon(PyMenu):
                                """
                                Singleton Ribbon.
                                """
                                def __init__(self, service, rules, path):
                                    self.ScaleFactor = self.__class__.ScaleFactor(service, rules, path + [("ScaleFactor", "")])
                                    self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                                    super().__init__(service, rules, path)

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

                            class ArrowScale(PyMenu):
                                """
                                Parameter ArrowScale of value type float.
                                """
                                pass

                            class LineWidth(PyMenu):
                                """
                                Parameter LineWidth of value type float.
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

                            class SphereLod(PyMenu):
                                """
                                Parameter SphereLod of value type int.
                                """
                                pass

                            class SphereSize(PyMenu):
                                """
                                Parameter SphereSize of value type float.
                                """
                                pass

                        class AccuracyControl(PyMenu):
                            """
                            Singleton AccuracyControl.
                            """
                            def __init__(self, service, rules, path):
                                self.AccuracyControlOn = self.__class__.AccuracyControlOn(service, rules, path + [("AccuracyControlOn", "")])
                                self.StepSize = self.__class__.StepSize(service, rules, path + [("StepSize", "")])
                                self.Tolerance = self.__class__.Tolerance(service, rules, path + [("Tolerance", "")])
                                super().__init__(service, rules, path)

                            class AccuracyControlOn(PyMenu):
                                """
                                Parameter AccuracyControlOn of value type bool.
                                """
                                pass

                            class StepSize(PyMenu):
                                """
                                Parameter StepSize of value type float.
                                """
                                pass

                            class Tolerance(PyMenu):
                                """
                                Parameter Tolerance of value type float.
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

                        class Coarsen(PyMenu):
                            """
                            Parameter Coarsen of value type int.
                            """
                            pass

                        class OverlayedMesh(PyMenu):
                            """
                            Parameter OverlayedMesh of value type str.
                            """
                            pass

                        class UID(PyMenu):
                            """
                            Parameter UID of value type str.
                            """
                            pass

                        class OnZone(PyMenu):
                            """
                            Parameter OnZone of value type List[str].
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

                        class VelocityDomain(PyMenu):
                            """
                            Parameter VelocityDomain of value type str.
                            """
                            pass

                        class Skip(PyMenu):
                            """
                            Parameter Skip of value type int.
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

                        class SyncStatus(PyMenu):
                            """
                            Parameter SyncStatus of value type str.
                            """
                            pass

                        class Step(PyMenu):
                            """
                            Parameter Step of value type int.
                            """
                            pass

                        class PathlinesField(PyMenu):
                            """
                            Parameter PathlinesField of value type str.
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

                        class Push(PyCommand):
                            """
                            Push() -> bool
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

                    def __getitem__(self, key: str) -> _Pathlines:
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
                            self.Title = self.__class__.Title(service, rules, path + [("Title", "")])
                            self.YAxisLabel = self.__class__.YAxisLabel(service, rules, path + [("YAxisLabel", "")])
                            self.XAxis = self.__class__.XAxis(service, rules, path + [("XAxis", "")])
                            self.XAxisLabel = self.__class__.XAxisLabel(service, rules, path + [("XAxisLabel", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.Reports = self.__class__.Reports(service, rules, path + [("Reports", "")])
                            self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                            self.Print = self.__class__.Print(service, rules, "Print", path)
                            self.Plot = self.__class__.Plot(service, rules, "Plot", path)
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
                                    self.Label = self.__class__.Label(service, rules, path + [("Label", "")])
                                    self.Filename = self.__class__.Filename(service, rules, path + [("Filename", "")])
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

                                class Label(PyMenu):
                                    """
                                    Parameter Label of value type str.
                                    """
                                    pass

                                class Filename(PyMenu):
                                    """
                                    Parameter Filename of value type str.
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
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                super().__init__(service, rules, path)

                            class X(PyMenu):
                                """
                                Singleton X.
                                """
                                def __init__(self, service, rules, path):
                                    self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                                    self.MajorRules = self.__class__.MajorRules(service, rules, path + [("MajorRules", "")])
                                    self.NumberFormat = self.__class__.NumberFormat(service, rules, path + [("NumberFormat", "")])
                                    self.MinorRules = self.__class__.MinorRules(service, rules, path + [("MinorRules", "")])
                                    self.Options = self.__class__.Options(service, rules, path + [("Options", "")])
                                    self.Label = self.__class__.Label(service, rules, path + [("Label", "")])
                                    super().__init__(service, rules, path)

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

                            class Y(PyMenu):
                                """
                                Singleton Y.
                                """
                                def __init__(self, service, rules, path):
                                    self.MajorRules = self.__class__.MajorRules(service, rules, path + [("MajorRules", "")])
                                    self.Options = self.__class__.Options(service, rules, path + [("Options", "")])
                                    self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                                    self.MinorRules = self.__class__.MinorRules(service, rules, path + [("MinorRules", "")])
                                    self.NumberFormat = self.__class__.NumberFormat(service, rules, path + [("NumberFormat", "")])
                                    self.Label = self.__class__.Label(service, rules, path + [("Label", "")])
                                    super().__init__(service, rules, path)

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
                                        self.MajorRules = self.__class__.MajorRules(service, rules, path + [("MajorRules", "")])
                                        self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
                                        self.Log = self.__class__.Log(service, rules, path + [("Log", "")])
                                        super().__init__(service, rules, path)

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

                                    class Log(PyMenu):
                                        """
                                        Parameter Log of value type bool.
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
                                self.Option = self.__class__.Option(service, rules, path + [("Option", "")])
                                self.End = self.__class__.End(service, rules, path + [("End", "")])
                                self.Begin = self.__class__.Begin(service, rules, path + [("Begin", "")])
                                self.Increment = self.__class__.Increment(service, rules, path + [("Increment", "")])
                                super().__init__(service, rules, path)

                            class Option(PyMenu):
                                """
                                Parameter Option of value type str.
                                """
                                pass

                            class End(PyMenu):
                                """
                                Parameter End of value type float.
                                """
                                pass

                            class Begin(PyMenu):
                                """
                                Parameter Begin of value type float.
                                """
                                pass

                            class Increment(PyMenu):
                                """
                                Parameter Increment of value type float.
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
                                    self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                    self.Symbol = self.__class__.Symbol(service, rules, path + [("Symbol", "")])
                                    self.Size = self.__class__.Size(service, rules, path + [("Size", "")])
                                    super().__init__(service, rules, path)

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
                                    self.Weight = self.__class__.Weight(service, rules, path + [("Weight", "")])
                                    self.Pattern = self.__class__.Pattern(service, rules, path + [("Pattern", "")])
                                    self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                    super().__init__(service, rules, path)

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

                                class Color(PyMenu):
                                    """
                                    Parameter Color of value type str.
                                    """
                                    pass

                        class Title(PyMenu):
                            """
                            Parameter Title of value type str.
                            """
                            pass

                        class YAxisLabel(PyMenu):
                            """
                            Parameter YAxisLabel of value type str.
                            """
                            pass

                        class XAxis(PyMenu):
                            """
                            Parameter XAxis of value type str.
                            """
                            pass

                        class XAxisLabel(PyMenu):
                            """
                            Parameter XAxisLabel of value type str.
                            """
                            pass

                        class _name_(PyMenu):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                        class Reports(PyMenu):
                            """
                            Parameter Reports of value type List[str].
                            """
                            pass

                        class SaveImage(PyCommand):
                            """
                            SaveImage(FileName: str, Format: str, FileType: str, Coloring: str, Orientation: str, UseWhiteBackground: bool, Resolution: Dict[str, Any]) -> bool
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

                        class Export(PyCommand):
                            """
                            Export(FileName: str) -> None
                            """
                            pass

                    def __getitem__(self, key: str) -> _TransientPlot:
                        return super().__getitem__(key)

                class VolumeRender(PyNamedObjectContainer):
                    class _VolumeRender(PyMenu):
                        """
                        Singleton _VolumeRender.
                        """
                        def __init__(self, service, rules, path):
                            self.Grid = self.__class__.Grid(service, rules, path + [("Grid", "")])
                            self.Bound = self.__class__.Bound(service, rules, path + [("Bound", "")])
                            self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                            self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                            self.Volumes = self.__class__.Volumes(service, rules, path + [("Volumes", "")])
                            self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                            self.AlphaScale = self.__class__.AlphaScale(service, rules, path + [("AlphaScale", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.Transparencies = self.__class__.Transparencies(service, rules, path + [("Transparencies", "")])
                            self.Quality = self.__class__.Quality(service, rules, path + [("Quality", "")])
                            self.Display = self.__class__.Display(service, rules, "Display", path)
                            self.SaveAnimation = self.__class__.SaveAnimation(service, rules, "SaveAnimation", path)
                            self.AddToViewport = self.__class__.AddToViewport(service, rules, "AddToViewport", path)
                            self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                            self.DisplayInViewport = self.__class__.DisplayInViewport(service, rules, "DisplayInViewport", path)
                            self.UpdateMinMax = self.__class__.UpdateMinMax(service, rules, "UpdateMinMax", path)
                            super().__init__(service, rules, path)

                        class Grid(PyMenu):
                            """
                            Singleton Grid.
                            """
                            def __init__(self, service, rules, path):
                                self.NZ = self.__class__.NZ(service, rules, path + [("NZ", "")])
                                self.NY = self.__class__.NY(service, rules, path + [("NY", "")])
                                self.NX = self.__class__.NX(service, rules, path + [("NX", "")])
                                super().__init__(service, rules, path)

                            class NZ(PyMenu):
                                """
                                Parameter NZ of value type int.
                                """
                                pass

                            class NY(PyMenu):
                                """
                                Parameter NY of value type int.
                                """
                                pass

                            class NX(PyMenu):
                                """
                                Parameter NX of value type int.
                                """
                                pass

                        class Bound(PyMenu):
                            """
                            Singleton Bound.
                            """
                            def __init__(self, service, rules, path):
                                self.ZMax = self.__class__.ZMax(service, rules, path + [("ZMax", "")])
                                self.YMin = self.__class__.YMin(service, rules, path + [("YMin", "")])
                                self.YMax = self.__class__.YMax(service, rules, path + [("YMax", "")])
                                self.RestrictToBoundingBox = self.__class__.RestrictToBoundingBox(service, rules, path + [("RestrictToBoundingBox", "")])
                                self.ZMin = self.__class__.ZMin(service, rules, path + [("ZMin", "")])
                                self.XMax = self.__class__.XMax(service, rules, path + [("XMax", "")])
                                self.XMin = self.__class__.XMin(service, rules, path + [("XMin", "")])
                                super().__init__(service, rules, path)

                            class ZMax(PyMenu):
                                """
                                Parameter ZMax of value type float.
                                """
                                pass

                            class YMin(PyMenu):
                                """
                                Parameter YMin of value type float.
                                """
                                pass

                            class YMax(PyMenu):
                                """
                                Parameter YMax of value type float.
                                """
                                pass

                            class RestrictToBoundingBox(PyMenu):
                                """
                                Parameter RestrictToBoundingBox of value type bool.
                                """
                                pass

                            class ZMin(PyMenu):
                                """
                                Parameter ZMin of value type float.
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

                        class ColorMap(PyMenu):
                            """
                            Singleton ColorMap.
                            """
                            def __init__(self, service, rules, path):
                                self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                                self.Position = self.__class__.Position(service, rules, path + [("Position", "")])
                                self.Visible = self.__class__.Visible(service, rules, path + [("Visible", "")])
                                self.Size = self.__class__.Size(service, rules, path + [("Size", "")])
                                self.Skip = self.__class__.Skip(service, rules, path + [("Skip", "")])
                                self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                                self.Precision = self.__class__.Precision(service, rules, path + [("Precision", "")])
                                self.IsLogScale = self.__class__.IsLogScale(service, rules, path + [("IsLogScale", "")])
                                self.ShowAll = self.__class__.ShowAll(service, rules, path + [("ShowAll", "")])
                                super().__init__(service, rules, path)

                            class Type(PyMenu):
                                """
                                Parameter Type of value type str.
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

                            class ColorMap(PyMenu):
                                """
                                Parameter ColorMap of value type str.
                                """
                                pass

                            class Precision(PyMenu):
                                """
                                Parameter Precision of value type int.
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

                        class Volumes(PyMenu):
                            """
                            Parameter Volumes of value type List[str].
                            """
                            pass

                        class Field(PyMenu):
                            """
                            Parameter Field of value type str.
                            """
                            pass

                        class AlphaScale(PyMenu):
                            """
                            Parameter AlphaScale of value type float.
                            """
                            pass

                        class _name_(PyMenu):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                        class Transparencies(PyMenu):
                            """
                            Parameter Transparencies of value type List[float].
                            """
                            pass

                        class Quality(PyMenu):
                            """
                            Parameter Quality of value type str.
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

                    def __getitem__(self, key: str) -> _VolumeRender:
                        return super().__getitem__(key)

                class Scene(PyNamedObjectContainer):
                    class _Scene(PyMenu):
                        """
                        Singleton _Scene.
                        """
                        def __init__(self, service, rules, path):
                            self.SyncStatus = self.__class__.SyncStatus(service, rules, path + [("SyncStatus", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.GraphicsObjects = self.__class__.GraphicsObjects(service, rules, path + [("GraphicsObjects", "")])
                            self.WindowId = self.__class__.WindowId(service, rules, path + [("WindowId", "")])
                            self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                            self.Display = self.__class__.Display(service, rules, "Display", path)
                            self.SaveAnimation = self.__class__.SaveAnimation(service, rules, "SaveAnimation", path)
                            self.Pull = self.__class__.Pull(service, rules, "Pull", path)
                            self.Push = self.__class__.Push(service, rules, "Push", path)
                            self.Diff = self.__class__.Diff(service, rules, "Diff", path)
                            super().__init__(service, rules, path)

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

                        class Push(PyCommand):
                            """
                            Push() -> bool
                            """
                            pass

                        class Diff(PyCommand):
                            """
                            Diff() -> bool
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
                            self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                            self.BoundaryValues = self.__class__.BoundaryValues(service, rules, path + [("BoundaryValues", "")])
                            self.NodeValues = self.__class__.NodeValues(service, rules, path + [("NodeValues", "")])
                            self.WindowId = self.__class__.WindowId(service, rules, path + [("WindowId", "")])
                            self.Coloring = self.__class__.Coloring(service, rules, path + [("Coloring", "")])
                            self.ContourLines = self.__class__.ContourLines(service, rules, path + [("ContourLines", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.SyncStatus = self.__class__.SyncStatus(service, rules, path + [("SyncStatus", "")])
                            self.OverlayedMesh = self.__class__.OverlayedMesh(service, rules, path + [("OverlayedMesh", "")])
                            self.Filled = self.__class__.Filled(service, rules, path + [("Filled", "")])
                            self.DrawMesh = self.__class__.DrawMesh(service, rules, path + [("DrawMesh", "")])
                            self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                            self.DisplayInViewport = self.__class__.DisplayInViewport(service, rules, "DisplayInViewport", path)
                            self.UpdateMinMax = self.__class__.UpdateMinMax(service, rules, "UpdateMinMax", path)
                            self.Diff = self.__class__.Diff(service, rules, "Diff", path)
                            self.Display = self.__class__.Display(service, rules, "Display", path)
                            self.SaveAnimation = self.__class__.SaveAnimation(service, rules, "SaveAnimation", path)
                            self.Pull = self.__class__.Pull(service, rules, "Pull", path)
                            self.AddToViewport = self.__class__.AddToViewport(service, rules, "AddToViewport", path)
                            self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                            self.Push = self.__class__.Push(service, rules, "Push", path)
                            super().__init__(service, rules, path)

                        class ColorMap(PyMenu):
                            """
                            Singleton ColorMap.
                            """
                            def __init__(self, service, rules, path):
                                self.Size = self.__class__.Size(service, rules, path + [("Size", "")])
                                self.IsLogScale = self.__class__.IsLogScale(service, rules, path + [("IsLogScale", "")])
                                self.Visible = self.__class__.Visible(service, rules, path + [("Visible", "")])
                                self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                                self.Position = self.__class__.Position(service, rules, path + [("Position", "")])
                                self.Precision = self.__class__.Precision(service, rules, path + [("Precision", "")])
                                self.ShowAll = self.__class__.ShowAll(service, rules, path + [("ShowAll", "")])
                                self.Skip = self.__class__.Skip(service, rules, path + [("Skip", "")])
                                self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
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

                            class Position(PyMenu):
                                """
                                Parameter Position of value type str.
                                """
                                pass

                            class Precision(PyMenu):
                                """
                                Parameter Precision of value type int.
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

                            class ColorMap(PyMenu):
                                """
                                Parameter ColorMap of value type str.
                                """
                                pass

                        class Range(PyMenu):
                            """
                            Singleton Range.
                            """
                            def __init__(self, service, rules, path):
                                self.GlobalRange = self.__class__.GlobalRange(service, rules, path + [("GlobalRange", "")])
                                self.MaxValue = self.__class__.MaxValue(service, rules, path + [("MaxValue", "")])
                                self.MinValue = self.__class__.MinValue(service, rules, path + [("MinValue", "")])
                                self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
                                self.ClipToRange = self.__class__.ClipToRange(service, rules, path + [("ClipToRange", "")])
                                super().__init__(service, rules, path)

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

                            class MinValue(PyMenu):
                                """
                                Parameter MinValue of value type float.
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

                        class Surfaces(PyMenu):
                            """
                            Parameter Surfaces of value type List[str].
                            """
                            pass

                        class BoundaryValues(PyMenu):
                            """
                            Parameter BoundaryValues of value type bool.
                            """
                            pass

                        class NodeValues(PyMenu):
                            """
                            Parameter NodeValues of value type bool.
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

                        class ContourLines(PyMenu):
                            """
                            Parameter ContourLines of value type bool.
                            """
                            pass

                        class _name_(PyMenu):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                        class SyncStatus(PyMenu):
                            """
                            Parameter SyncStatus of value type str.
                            """
                            pass

                        class OverlayedMesh(PyMenu):
                            """
                            Parameter OverlayedMesh of value type str.
                            """
                            pass

                        class Filled(PyMenu):
                            """
                            Parameter Filled of value type bool.
                            """
                            pass

                        class DrawMesh(PyMenu):
                            """
                            Parameter DrawMesh of value type bool.
                            """
                            pass

                        class Field(PyMenu):
                            """
                            Parameter Field of value type str.
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

                        class Push(PyCommand):
                            """
                            Push() -> bool
                            """
                            pass

                    def __getitem__(self, key: str) -> _Contour:
                        return super().__getitem__(key)

                class MirrorPlanes(PyMenu):
                    """
                    Singleton MirrorPlanes.
                    """
                    def __init__(self, service, rules, path):
                        self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                        self.XOrigin = self.__class__.XOrigin(service, rules, path + [("XOrigin", "")])
                        self.YOrigin = self.__class__.YOrigin(service, rules, path + [("YOrigin", "")])
                        self.AllSurfaces = self.__class__.AllSurfaces(service, rules, path + [("AllSurfaces", "")])
                        self.ZOrigin = self.__class__.ZOrigin(service, rules, path + [("ZOrigin", "")])
                        self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                        self.X = self.__class__.X(service, rules, path + [("X", "")])
                        self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                        super().__init__(service, rules, path)

                    class Surfaces(PyMenu):
                        """
                        Parameter Surfaces of value type List[str].
                        """
                        pass

                    class XOrigin(PyMenu):
                        """
                        Parameter XOrigin of value type float.
                        """
                        pass

                    class YOrigin(PyMenu):
                        """
                        Parameter YOrigin of value type float.
                        """
                        pass

                    class AllSurfaces(PyMenu):
                        """
                        Parameter AllSurfaces of value type bool.
                        """
                        pass

                    class ZOrigin(PyMenu):
                        """
                        Parameter ZOrigin of value type float.
                        """
                        pass

                    class Y(PyMenu):
                        """
                        Parameter Y of value type bool.
                        """
                        pass

                    class X(PyMenu):
                        """
                        Parameter X of value type bool.
                        """
                        pass

                    class Z(PyMenu):
                        """
                        Parameter Z of value type bool.
                        """
                        pass

                class GridColors(PyMenu):
                    """
                    Singleton GridColors.
                    """
                    def __init__(self, service, rules, path):
                        self.ColorGridFreeSurface = self.__class__.ColorGridFreeSurface(service, rules, path + [("ColorGridFreeSurface", "")])
                        self.ColorGridInlet = self.__class__.ColorGridInlet(service, rules, path + [("ColorGridInlet", "")])
                        self.ColorGridRansLesInterface = self.__class__.ColorGridRansLesInterface(service, rules, path + [("ColorGridRansLesInterface", "")])
                        self.ColorGridInternal = self.__class__.ColorGridInternal(service, rules, path + [("ColorGridInternal", "")])
                        self.ColorGridWall = self.__class__.ColorGridWall(service, rules, path + [("ColorGridWall", "")])
                        self.ColorSurface = self.__class__.ColorSurface(service, rules, path + [("ColorSurface", "")])
                        self.ColorGridOutlet = self.__class__.ColorGridOutlet(service, rules, path + [("ColorGridOutlet", "")])
                        self.ColorGridAxis = self.__class__.ColorGridAxis(service, rules, path + [("ColorGridAxis", "")])
                        self.ColorGridPeriodic = self.__class__.ColorGridPeriodic(service, rules, path + [("ColorGridPeriodic", "")])
                        self.ColorGridOverset = self.__class__.ColorGridOverset(service, rules, path + [("ColorGridOverset", "")])
                        self.ColorGridInterior = self.__class__.ColorGridInterior(service, rules, path + [("ColorGridInterior", "")])
                        self.ColorGridTraction = self.__class__.ColorGridTraction(service, rules, path + [("ColorGridTraction", "")])
                        self.ColorGridSymmetry = self.__class__.ColorGridSymmetry(service, rules, path + [("ColorGridSymmetry", "")])
                        self.ColorInterface = self.__class__.ColorInterface(service, rules, path + [("ColorInterface", "")])
                        self.ColorGridFar = self.__class__.ColorGridFar(service, rules, path + [("ColorGridFar", "")])
                        super().__init__(service, rules, path)

                    class ColorGridFreeSurface(PyMenu):
                        """
                        Parameter ColorGridFreeSurface of value type str.
                        """
                        pass

                    class ColorGridInlet(PyMenu):
                        """
                        Parameter ColorGridInlet of value type str.
                        """
                        pass

                    class ColorGridRansLesInterface(PyMenu):
                        """
                        Parameter ColorGridRansLesInterface of value type str.
                        """
                        pass

                    class ColorGridInternal(PyMenu):
                        """
                        Parameter ColorGridInternal of value type str.
                        """
                        pass

                    class ColorGridWall(PyMenu):
                        """
                        Parameter ColorGridWall of value type str.
                        """
                        pass

                    class ColorSurface(PyMenu):
                        """
                        Parameter ColorSurface of value type str.
                        """
                        pass

                    class ColorGridOutlet(PyMenu):
                        """
                        Parameter ColorGridOutlet of value type str.
                        """
                        pass

                    class ColorGridAxis(PyMenu):
                        """
                        Parameter ColorGridAxis of value type str.
                        """
                        pass

                    class ColorGridPeriodic(PyMenu):
                        """
                        Parameter ColorGridPeriodic of value type str.
                        """
                        pass

                    class ColorGridOverset(PyMenu):
                        """
                        Parameter ColorGridOverset of value type str.
                        """
                        pass

                    class ColorGridInterior(PyMenu):
                        """
                        Parameter ColorGridInterior of value type str.
                        """
                        pass

                    class ColorGridTraction(PyMenu):
                        """
                        Parameter ColorGridTraction of value type str.
                        """
                        pass

                    class ColorGridSymmetry(PyMenu):
                        """
                        Parameter ColorGridSymmetry of value type str.
                        """
                        pass

                    class ColorInterface(PyMenu):
                        """
                        Parameter ColorInterface of value type str.
                        """
                        pass

                    class ColorGridFar(PyMenu):
                        """
                        Parameter ColorGridFar of value type str.
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

                    class Position(PyMenu):
                        """
                        Singleton Position.
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

            class ResultsExternalInfo(PyMenu):
                """
                Singleton ResultsExternalInfo.
                """
                def __init__(self, service, rules, path):
                    super().__init__(service, rules, path)

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
                        self.XAxisFunction = self.__class__.XAxisFunction(service, rules, path + [("XAxisFunction", "")])
                        self.YAxisFunction = self.__class__.YAxisFunction(service, rules, path + [("YAxisFunction", "")])
                        self.Curves = self.__class__.Curves(service, rules, path + [("Curves", "")])
                        self.Axes = self.__class__.Axes(service, rules, path + [("Axes", "")])
                        self.Filename = self.__class__.Filename(service, rules, path + [("Filename", "")])
                        self.Plot = self.__class__.Plot(service, rules, "Plot", path)
                        super().__init__(service, rules, path)

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

                    class Axes(PyMenu):
                        """
                        Singleton Axes.
                        """
                        def __init__(self, service, rules, path):
                            self.X = self.__class__.X(service, rules, path + [("X", "")])
                            self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                            super().__init__(service, rules, path)

                        class X(PyMenu):
                            """
                            Singleton X.
                            """
                            def __init__(self, service, rules, path):
                                self.MinorRules = self.__class__.MinorRules(service, rules, path + [("MinorRules", "")])
                                self.MajorRules = self.__class__.MajorRules(service, rules, path + [("MajorRules", "")])
                                self.NumberFormat = self.__class__.NumberFormat(service, rules, path + [("NumberFormat", "")])
                                self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                                self.Options = self.__class__.Options(service, rules, path + [("Options", "")])
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

                            class Options(PyMenu):
                                """
                                Singleton Options.
                                """
                                def __init__(self, service, rules, path):
                                    self.Log = self.__class__.Log(service, rules, path + [("Log", "")])
                                    self.MajorRules = self.__class__.MajorRules(service, rules, path + [("MajorRules", "")])
                                    self.MinorRules = self.__class__.MinorRules(service, rules, path + [("MinorRules", "")])
                                    self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
                                    super().__init__(service, rules, path)

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

                            class Label(PyMenu):
                                """
                                Parameter Label of value type str.
                                """
                                pass

                        class Y(PyMenu):
                            """
                            Singleton Y.
                            """
                            def __init__(self, service, rules, path):
                                self.MajorRules = self.__class__.MajorRules(service, rules, path + [("MajorRules", "")])
                                self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                                self.Options = self.__class__.Options(service, rules, path + [("Options", "")])
                                self.NumberFormat = self.__class__.NumberFormat(service, rules, path + [("NumberFormat", "")])
                                self.MinorRules = self.__class__.MinorRules(service, rules, path + [("MinorRules", "")])
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

                            class Label(PyMenu):
                                """
                                Parameter Label of value type str.
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

            class GetXYData(PyCommand):
                """
                GetXYData(Surfaces: List[str], Fields: List[str]) -> None
                """
                pass

            class GetFieldMinMax(PyCommand):
                """
                GetFieldMinMax(Field: str, Surfaces: List[str]) -> List[float]
                """
                pass

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
                    self.YMin = self.__class__.YMin(service, rules, path + [("YMin", "")])
                    self.XMax = self.__class__.XMax(service, rules, path + [("XMax", "")])
                    self.ZMin = self.__class__.ZMin(service, rules, path + [("ZMin", "")])
                    self.ZMax = self.__class__.ZMax(service, rules, path + [("ZMax", "")])
                    self.YMax = self.__class__.YMax(service, rules, path + [("YMax", "")])
                    self.XMin = self.__class__.XMin(service, rules, path + [("XMin", "")])
                    super().__init__(service, rules, path)

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

                class ZMin(PyMenu):
                    """
                    Parameter ZMin of value type float.
                    """
                    pass

                class ZMax(PyMenu):
                    """
                    Parameter ZMax of value type float.
                    """
                    pass

                class YMax(PyMenu):
                    """
                    Parameter YMax of value type float.
                    """
                    pass

                class XMin(PyMenu):
                    """
                    Parameter XMin of value type float.
                    """
                    pass

        class ResultsInfo(PyMenu):
            """
            Singleton ResultsInfo.
            """
            def __init__(self, service, rules, path):
                self.PathlinesFields = self.__class__.PathlinesFields(service, rules, path + [("PathlinesFields", "")])
                self.Fields = self.__class__.Fields(service, rules, path + [("Fields", "")])
                self.DPMInjections = self.__class__.DPMInjections(service, rules, path + [("DPMInjections", "")])
                self.ParticleTracksFields = self.__class__.ParticleTracksFields(service, rules, path + [("ParticleTracksFields", "")])
                self.ParticleVariables = self.__class__.ParticleVariables(service, rules, path + [("ParticleVariables", "")])
                self.DPMParticleVectorFields = self.__class__.DPMParticleVectorFields(service, rules, path + [("DPMParticleVectorFields", "")])
                self.VectorFields = self.__class__.VectorFields(service, rules, path + [("VectorFields", "")])
                super().__init__(service, rules, path)

            class PathlinesFields(PyNamedObjectContainer):
                class _PathlinesFields(PyMenu):
                    """
                    Singleton _PathlinesFields.
                    """
                    def __init__(self, service, rules, path):
                        self.Section = self.__class__.Section(service, rules, path + [("Section", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        self.SolverName = self.__class__.SolverName(service, rules, path + [("SolverName", "")])
                        self.Rank = self.__class__.Rank(service, rules, path + [("Rank", "")])
                        self.Domain = self.__class__.Domain(service, rules, path + [("Domain", "")])
                        self.DisplayName = self.__class__.DisplayName(service, rules, path + [("DisplayName", "")])
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

                def __getitem__(self, key: str) -> _PathlinesFields:
                    return super().__getitem__(key)

            class Fields(PyNamedObjectContainer):
                class _Fields(PyMenu):
                    """
                    Singleton _Fields.
                    """
                    def __init__(self, service, rules, path):
                        self.DisplayName = self.__class__.DisplayName(service, rules, path + [("DisplayName", "")])
                        self.SolverName = self.__class__.SolverName(service, rules, path + [("SolverName", "")])
                        self.Domain = self.__class__.Domain(service, rules, path + [("Domain", "")])
                        self.Rank = self.__class__.Rank(service, rules, path + [("Rank", "")])
                        self.UnitQuantity = self.__class__.UnitQuantity(service, rules, path + [("UnitQuantity", "")])
                        self.Section = self.__class__.Section(service, rules, path + [("Section", "")])
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

                    class Domain(PyMenu):
                        """
                        Parameter Domain of value type str.
                        """
                        pass

                    class Rank(PyMenu):
                        """
                        Parameter Rank of value type int.
                        """
                        pass

                    class UnitQuantity(PyMenu):
                        """
                        Parameter UnitQuantity of value type str.
                        """
                        pass

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

                def __getitem__(self, key: str) -> _Fields:
                    return super().__getitem__(key)

            class DPMInjections(PyNamedObjectContainer):
                class _DPMInjections(PyMenu):
                    """
                    Singleton _DPMInjections.
                    """
                    def __init__(self, service, rules, path):
                        self.DisplayName = self.__class__.DisplayName(service, rules, path + [("DisplayName", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        self.SolverName = self.__class__.SolverName(service, rules, path + [("SolverName", "")])
                        super().__init__(service, rules, path)

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

                def __getitem__(self, key: str) -> _DPMInjections:
                    return super().__getitem__(key)

            class ParticleTracksFields(PyNamedObjectContainer):
                class _ParticleTracksFields(PyMenu):
                    """
                    Singleton _ParticleTracksFields.
                    """
                    def __init__(self, service, rules, path):
                        self.SolverName = self.__class__.SolverName(service, rules, path + [("SolverName", "")])
                        self.Section = self.__class__.Section(service, rules, path + [("Section", "")])
                        self.Domain = self.__class__.Domain(service, rules, path + [("Domain", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        self.DisplayName = self.__class__.DisplayName(service, rules, path + [("DisplayName", "")])
                        super().__init__(service, rules, path)

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

                def __getitem__(self, key: str) -> _ParticleTracksFields:
                    return super().__getitem__(key)

            class ParticleVariables(PyNamedObjectContainer):
                class _ParticleVariables(PyMenu):
                    """
                    Singleton _ParticleVariables.
                    """
                    def __init__(self, service, rules, path):
                        self.DisplayName = self.__class__.DisplayName(service, rules, path + [("DisplayName", "")])
                        self.SolverName = self.__class__.SolverName(service, rules, path + [("SolverName", "")])
                        self.Domain = self.__class__.Domain(service, rules, path + [("Domain", "")])
                        self.Section = self.__class__.Section(service, rules, path + [("Section", "")])
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

                    class Domain(PyMenu):
                        """
                        Parameter Domain of value type str.
                        """
                        pass

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

                def __getitem__(self, key: str) -> _ParticleVariables:
                    return super().__getitem__(key)

            class DPMParticleVectorFields(PyNamedObjectContainer):
                class _DPMParticleVectorFields(PyMenu):
                    """
                    Singleton _DPMParticleVectorFields.
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

                def __getitem__(self, key: str) -> _DPMParticleVectorFields:
                    return super().__getitem__(key)

            class VectorFields(PyNamedObjectContainer):
                class _VectorFields(PyMenu):
                    """
                    Singleton _VectorFields.
                    """
                    def __init__(self, service, rules, path):
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        self.IsCustomVector = self.__class__.IsCustomVector(service, rules, path + [("IsCustomVector", "")])
                        self.ZComponent = self.__class__.ZComponent(service, rules, path + [("ZComponent", "")])
                        self.XComponent = self.__class__.XComponent(service, rules, path + [("XComponent", "")])
                        self.YComponent = self.__class__.YComponent(service, rules, path + [("YComponent", "")])
                        super().__init__(service, rules, path)

                    class _name_(PyMenu):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                    class IsCustomVector(PyMenu):
                        """
                        Parameter IsCustomVector of value type bool.
                        """
                        pass

                    class ZComponent(PyMenu):
                        """
                        Parameter ZComponent of value type str.
                        """
                        pass

                    class XComponent(PyMenu):
                        """
                        Parameter XComponent of value type str.
                        """
                        pass

                    class YComponent(PyMenu):
                        """
                        Parameter YComponent of value type str.
                        """
                        pass

                def __getitem__(self, key: str) -> _VectorFields:
                    return super().__getitem__(key)

        class App(PyMenu):
            """
            Singleton App.
            """
            def __init__(self, service, rules, path):
                self.BC = self.__class__.BC(service, rules, path + [("BC", "")])
                self.Domain = self.__class__.Domain(service, rules, path + [("Domain", "")])
                self.Airflow = self.__class__.Airflow(service, rules, path + [("Airflow", "")])
                self.Particles = self.__class__.Particles(service, rules, path + [("Particles", "")])
                self.Solution = self.__class__.Solution(service, rules, path + [("Solution", "")])
                self.Ice = self.__class__.Ice(service, rules, path + [("Ice", "")])
                self.RunType = self.__class__.RunType(service, rules, path + [("RunType", "")])
                self.Adaptation = self.__class__.Adaptation(service, rules, path + [("Adaptation", "")])
                self.GlobalSettings = self.__class__.GlobalSettings(service, rules, path + [("GlobalSettings", "")])
                self.SetupErrors = self.__class__.SetupErrors(service, rules, path + [("SetupErrors", "")])
                self.IsBusy = self.__class__.IsBusy(service, rules, path + [("IsBusy", "")])
                self.SetupWarnings = self.__class__.SetupWarnings(service, rules, path + [("SetupWarnings", "")])
                self.InProgress = self.__class__.InProgress(service, rules, path + [("InProgress", "")])
                self.SendCommandQuiet = self.__class__.SendCommandQuiet(service, rules, "SendCommandQuiet", path)
                self.ImportMesh = self.__class__.ImportMesh(service, rules, "ImportMesh", path)
                self.SyncDM = self.__class__.SyncDM(service, rules, "SyncDM", path)
                self.InitAddOnAero = self.__class__.InitAddOnAero(service, rules, "InitAddOnAero", path)
                self.InitAddOn = self.__class__.InitAddOn(service, rules, "InitAddOn", path)
                self.CheckSetup = self.__class__.CheckSetup(service, rules, "CheckSetup", path)
                self.SaveCase = self.__class__.SaveCase(service, rules, "SaveCase", path)
                self.SavePostCaseAndData = self.__class__.SavePostCaseAndData(service, rules, "SavePostCaseAndData", path)
                self.SaveCaseAs = self.__class__.SaveCaseAs(service, rules, "SaveCaseAs", path)
                self.InitDM = self.__class__.InitDM(service, rules, "InitDM", path)
                self.LoadCase = self.__class__.LoadCase(service, rules, "LoadCase", path)
                self.SaveCaseAndData = self.__class__.SaveCaseAndData(service, rules, "SaveCaseAndData", path)
                self.ImportCase = self.__class__.ImportCase(service, rules, "ImportCase", path)
                self.LoadCaseAndData = self.__class__.LoadCaseAndData(service, rules, "LoadCaseAndData", path)
                self.ReloadDomain = self.__class__.ReloadDomain(service, rules, "ReloadDomain", path)
                self.SaveData = self.__class__.SaveData(service, rules, "SaveData", path)
                self.ReloadCase = self.__class__.ReloadCase(service, rules, "ReloadCase", path)
                self.IcingImportCase = self.__class__.IcingImportCase(service, rules, "IcingImportCase", path)
                self.IcingImportMesh = self.__class__.IcingImportMesh(service, rules, "IcingImportMesh", path)
                self.WriteAll = self.__class__.WriteAll(service, rules, "WriteAll", path)
                super().__init__(service, rules, path)

            class BC(PyNamedObjectContainer):
                class _BC(PyMenu):
                    """
                    Singleton _BC.
                    """
                    def __init__(self, service, rules, path):
                        self.AirflowWall = self.__class__.AirflowWall(service, rules, path + [("AirflowWall", "")])
                        self.AirflowPressureOutlet = self.__class__.AirflowPressureOutlet(service, rules, path + [("AirflowPressureOutlet", "")])
                        self.AirflowMassFlowInlet = self.__class__.AirflowMassFlowInlet(service, rules, path + [("AirflowMassFlowInlet", "")])
                        self.Common = self.__class__.Common(service, rules, path + [("Common", "")])
                        self.ParticlesInlet = self.__class__.ParticlesInlet(service, rules, path + [("ParticlesInlet", "")])
                        self.AirflowVelocityInlet = self.__class__.AirflowVelocityInlet(service, rules, path + [("AirflowVelocityInlet", "")])
                        self.IceWall = self.__class__.IceWall(service, rules, path + [("IceWall", "")])
                        self.ParticlesWall = self.__class__.ParticlesWall(service, rules, path + [("ParticlesWall", "")])
                        self.AirflowMassFlowOutlet = self.__class__.AirflowMassFlowOutlet(service, rules, path + [("AirflowMassFlowOutlet", "")])
                        self.IsInlet = self.__class__.IsInlet(service, rules, path + [("IsInlet", "")])
                        self.BCType = self.__class__.BCType(service, rules, path + [("BCType", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        self.IsWall = self.__class__.IsWall(service, rules, path + [("IsWall", "")])
                        self.IsExit = self.__class__.IsExit(service, rules, path + [("IsExit", "")])
                        self.RenameBC = self.__class__.RenameBC(service, rules, "RenameBC", path)
                        self.ImportConditions = self.__class__.ImportConditions(service, rules, "ImportConditions", path)
                        self.Display = self.__class__.Display(service, rules, "Display", path)
                        self.RefreshBCs = self.__class__.RefreshBCs(service, rules, "RefreshBCs", path)
                        self.ResetToCustom = self.__class__.ResetToCustom(service, rules, "ResetToCustom", path)
                        self.CopyWallAdiabaticP10 = self.__class__.CopyWallAdiabaticP10(service, rules, "CopyWallAdiabaticP10", path)
                        super().__init__(service, rules, path)

                    class AirflowWall(PyMenu):
                        """
                        Singleton AirflowWall.
                        """
                        def __init__(self, service, rules, path):
                            self.ThermalCondition = self.__class__.ThermalCondition(service, rules, path + [("ThermalCondition", "")])
                            self.HighRoughnessHeight = self.__class__.HighRoughnessHeight(service, rules, path + [("HighRoughnessHeight", "")])
                            self.Roughness = self.__class__.Roughness(service, rules, path + [("Roughness", "")])
                            self.HeatFlux = self.__class__.HeatFlux(service, rules, path + [("HeatFlux", "")])
                            self.Temperature = self.__class__.Temperature(service, rules, path + [("Temperature", "")])
                            super().__init__(service, rules, path)

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

                        class Roughness(PyMenu):
                            """
                            Parameter Roughness of value type str.
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

                    class AirflowPressureOutlet(PyMenu):
                        """
                        Singleton AirflowPressureOutlet.
                        """
                        def __init__(self, service, rules, path):
                            self.AbsolutePressure = self.__class__.AbsolutePressure(service, rules, path + [("AbsolutePressure", "")])
                            self.BCSync = self.__class__.BCSync(service, rules, path + [("BCSync", "")])
                            self.Pressure = self.__class__.Pressure(service, rules, path + [("Pressure", "")])
                            self.Temperature = self.__class__.Temperature(service, rules, path + [("Temperature", "")])
                            self.SettingsVisible = self.__class__.SettingsVisible(service, rules, path + [("SettingsVisible", "")])
                            self.SettingsEditable = self.__class__.SettingsEditable(service, rules, path + [("SettingsEditable", "")])
                            super().__init__(service, rules, path)

                        class AbsolutePressure(PyMenu):
                            """
                            Parameter AbsolutePressure of value type float.
                            """
                            pass

                        class BCSync(PyMenu):
                            """
                            Parameter BCSync of value type str.
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
                            self.SettingsVisible = self.__class__.SettingsVisible(service, rules, path + [("SettingsVisible", "")])
                            self.TurbIntensity = self.__class__.TurbIntensity(service, rules, path + [("TurbIntensity", "")])
                            self.FlowX = self.__class__.FlowX(service, rules, path + [("FlowX", "")])
                            self.MassFlowMode = self.__class__.MassFlowMode(service, rules, path + [("MassFlowMode", "")])
                            self.TurbSpecification = self.__class__.TurbSpecification(service, rules, path + [("TurbSpecification", "")])
                            self.FlowY = self.__class__.FlowY(service, rules, path + [("FlowY", "")])
                            self.BCSync = self.__class__.BCSync(service, rules, path + [("BCSync", "")])
                            self.Temperature = self.__class__.Temperature(service, rules, path + [("Temperature", "")])
                            self.SettingsEditable = self.__class__.SettingsEditable(service, rules, path + [("SettingsEditable", "")])
                            self.TurbViscRatio = self.__class__.TurbViscRatio(service, rules, path + [("TurbViscRatio", "")])
                            self.MassFlow = self.__class__.MassFlow(service, rules, path + [("MassFlow", "")])
                            self.TurbIntermittency = self.__class__.TurbIntermittency(service, rules, path + [("TurbIntermittency", "")])
                            self.FlowZ = self.__class__.FlowZ(service, rules, path + [("FlowZ", "")])
                            self.DirectionMode = self.__class__.DirectionMode(service, rules, path + [("DirectionMode", "")])
                            self.AbsolutePressure = self.__class__.AbsolutePressure(service, rules, path + [("AbsolutePressure", "")])
                            self.Pressure = self.__class__.Pressure(service, rules, path + [("Pressure", "")])
                            super().__init__(service, rules, path)

                        class SettingsVisible(PyMenu):
                            """
                            Parameter SettingsVisible of value type bool.
                            """
                            pass

                        class TurbIntensity(PyMenu):
                            """
                            Parameter TurbIntensity of value type float.
                            """
                            pass

                        class FlowX(PyMenu):
                            """
                            Parameter FlowX of value type float.
                            """
                            pass

                        class MassFlowMode(PyMenu):
                            """
                            Parameter MassFlowMode of value type str.
                            """
                            pass

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

                        class BCSync(PyMenu):
                            """
                            Parameter BCSync of value type str.
                            """
                            pass

                        class Temperature(PyMenu):
                            """
                            Parameter Temperature of value type float.
                            """
                            pass

                        class SettingsEditable(PyMenu):
                            """
                            Parameter SettingsEditable of value type bool.
                            """
                            pass

                        class TurbViscRatio(PyMenu):
                            """
                            Parameter TurbViscRatio of value type float.
                            """
                            pass

                        class MassFlow(PyMenu):
                            """
                            Parameter MassFlow of value type float.
                            """
                            pass

                        class TurbIntermittency(PyMenu):
                            """
                            Parameter TurbIntermittency of value type float.
                            """
                            pass

                        class FlowZ(PyMenu):
                            """
                            Parameter FlowZ of value type float.
                            """
                            pass

                        class DirectionMode(PyMenu):
                            """
                            Parameter DirectionMode of value type str.
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

                    class Common(PyMenu):
                        """
                        Singleton Common.
                        """
                        def __init__(self, service, rules, path):
                            self.DisplayThread = self.__class__.DisplayThread(service, rules, path + [("DisplayThread", "")])
                            self.Hidden = self.__class__.Hidden(service, rules, path + [("Hidden", "")])
                            self.Group = self.__class__.Group(service, rules, path + [("Group", "")])
                            super().__init__(service, rules, path)

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

                        class Group(PyMenu):
                            """
                            Parameter Group of value type str.
                            """
                            pass

                    class ParticlesInlet(PyMenu):
                        """
                        Singleton ParticlesInlet.
                        """
                        def __init__(self, service, rules, path):
                            self.CrystalVelX = self.__class__.CrystalVelX(service, rules, path + [("CrystalVelX", "")])
                            self.CrystalVelY = self.__class__.CrystalVelY(service, rules, path + [("CrystalVelY", "")])
                            self.DropletLWC = self.__class__.DropletLWC(service, rules, path + [("DropletLWC", "")])
                            self.VaporMode = self.__class__.VaporMode(service, rules, path + [("VaporMode", "")])
                            self.DropletVelX = self.__class__.DropletVelX(service, rules, path + [("DropletVelX", "")])
                            self.DropletTemperature = self.__class__.DropletTemperature(service, rules, path + [("DropletTemperature", "")])
                            self.DropletVelY = self.__class__.DropletVelY(service, rules, path + [("DropletVelY", "")])
                            self.VaporRH = self.__class__.VaporRH(service, rules, path + [("VaporRH", "")])
                            self.CrystalVelZ = self.__class__.CrystalVelZ(service, rules, path + [("CrystalVelZ", "")])
                            self.CrystalICC = self.__class__.CrystalICC(service, rules, path + [("CrystalICC", "")])
                            self.DpmNstream = self.__class__.DpmNstream(service, rules, path + [("DpmNstream", "")])
                            self.DpmInjFlag = self.__class__.DpmInjFlag(service, rules, path + [("DpmInjFlag", "")])
                            self.VaporConcentration = self.__class__.VaporConcentration(service, rules, path + [("VaporConcentration", "")])
                            self.DropletVelZ = self.__class__.DropletVelZ(service, rules, path + [("DropletVelZ", "")])
                            self.DropletVelocityFlag = self.__class__.DropletVelocityFlag(service, rules, path + [("DropletVelocityFlag", "")])
                            self.DropletDiameter = self.__class__.DropletDiameter(service, rules, path + [("DropletDiameter", "")])
                            self.CrystalVelocityFlag = self.__class__.CrystalVelocityFlag(service, rules, path + [("CrystalVelocityFlag", "")])
                            self.AutoBC = self.__class__.AutoBC(service, rules, path + [("AutoBC", "")])
                            self.CrystalTemperature = self.__class__.CrystalTemperature(service, rules, path + [("CrystalTemperature", "")])
                            super().__init__(service, rules, path)

                        class CrystalVelX(PyMenu):
                            """
                            Parameter CrystalVelX of value type float.
                            """
                            pass

                        class CrystalVelY(PyMenu):
                            """
                            Parameter CrystalVelY of value type float.
                            """
                            pass

                        class DropletLWC(PyMenu):
                            """
                            Parameter DropletLWC of value type float.
                            """
                            pass

                        class VaporMode(PyMenu):
                            """
                            Parameter VaporMode of value type str.
                            """
                            pass

                        class DropletVelX(PyMenu):
                            """
                            Parameter DropletVelX of value type float.
                            """
                            pass

                        class DropletTemperature(PyMenu):
                            """
                            Parameter DropletTemperature of value type float.
                            """
                            pass

                        class DropletVelY(PyMenu):
                            """
                            Parameter DropletVelY of value type float.
                            """
                            pass

                        class VaporRH(PyMenu):
                            """
                            Parameter VaporRH of value type float.
                            """
                            pass

                        class CrystalVelZ(PyMenu):
                            """
                            Parameter CrystalVelZ of value type float.
                            """
                            pass

                        class CrystalICC(PyMenu):
                            """
                            Parameter CrystalICC of value type float.
                            """
                            pass

                        class DpmNstream(PyMenu):
                            """
                            Parameter DpmNstream of value type int.
                            """
                            pass

                        class DpmInjFlag(PyMenu):
                            """
                            Parameter DpmInjFlag of value type bool.
                            """
                            pass

                        class VaporConcentration(PyMenu):
                            """
                            Parameter VaporConcentration of value type float.
                            """
                            pass

                        class DropletVelZ(PyMenu):
                            """
                            Parameter DropletVelZ of value type float.
                            """
                            pass

                        class DropletVelocityFlag(PyMenu):
                            """
                            Parameter DropletVelocityFlag of value type bool.
                            """
                            pass

                        class DropletDiameter(PyMenu):
                            """
                            Parameter DropletDiameter of value type float.
                            """
                            pass

                        class CrystalVelocityFlag(PyMenu):
                            """
                            Parameter CrystalVelocityFlag of value type bool.
                            """
                            pass

                        class AutoBC(PyMenu):
                            """
                            Parameter AutoBC of value type bool.
                            """
                            pass

                        class CrystalTemperature(PyMenu):
                            """
                            Parameter CrystalTemperature of value type float.
                            """
                            pass

                    class AirflowVelocityInlet(PyMenu):
                        """
                        Singleton AirflowVelocityInlet.
                        """
                        def __init__(self, service, rules, path):
                            self.FlowDirection = self.__class__.FlowDirection(service, rules, path + [("FlowDirection", "")])
                            self.FlowX = self.__class__.FlowX(service, rules, path + [("FlowX", "")])
                            self.FlowXComputed = self.__class__.FlowXComputed(service, rules, path + [("FlowXComputed", "")])
                            self.FlowMagnitude = self.__class__.FlowMagnitude(service, rules, path + [("FlowMagnitude", "")])
                            self.NormalToBoundary = self.__class__.NormalToBoundary(service, rules, path + [("NormalToBoundary", "")])
                            self.Mach = self.__class__.Mach(service, rules, path + [("Mach", "")])
                            self.FlowYComputed = self.__class__.FlowYComputed(service, rules, path + [("FlowYComputed", "")])
                            self.VelocityMode = self.__class__.VelocityMode(service, rules, path + [("VelocityMode", "")])
                            self.TurbIntermittency = self.__class__.TurbIntermittency(service, rules, path + [("TurbIntermittency", "")])
                            self.TurbViscRatio = self.__class__.TurbViscRatio(service, rules, path + [("TurbViscRatio", "")])
                            self.MachComputed = self.__class__.MachComputed(service, rules, path + [("MachComputed", "")])
                            self.SettingsVisible = self.__class__.SettingsVisible(service, rules, path + [("SettingsVisible", "")])
                            self.TurbIntensity = self.__class__.TurbIntensity(service, rules, path + [("TurbIntensity", "")])
                            self.FlowY = self.__class__.FlowY(service, rules, path + [("FlowY", "")])
                            self.TurbSpecification = self.__class__.TurbSpecification(service, rules, path + [("TurbSpecification", "")])
                            self.Temperature = self.__class__.Temperature(service, rules, path + [("Temperature", "")])
                            self.BCSync = self.__class__.BCSync(service, rules, path + [("BCSync", "")])
                            self.FlowZComputed = self.__class__.FlowZComputed(service, rules, path + [("FlowZComputed", "")])
                            self.AngleBeta = self.__class__.AngleBeta(service, rules, path + [("AngleBeta", "")])
                            self.FlowMagnitudeComputed = self.__class__.FlowMagnitudeComputed(service, rules, path + [("FlowMagnitudeComputed", "")])
                            self.SettingsEditable = self.__class__.SettingsEditable(service, rules, path + [("SettingsEditable", "")])
                            self.AngleAlpha = self.__class__.AngleAlpha(service, rules, path + [("AngleAlpha", "")])
                            self.FlowZ = self.__class__.FlowZ(service, rules, path + [("FlowZ", "")])
                            self.AbsolutePressure = self.__class__.AbsolutePressure(service, rules, path + [("AbsolutePressure", "")])
                            self.Pressure = self.__class__.Pressure(service, rules, path + [("Pressure", "")])
                            super().__init__(service, rules, path)

                        class FlowDirection(PyMenu):
                            """
                            Parameter FlowDirection of value type str.
                            """
                            pass

                        class FlowX(PyMenu):
                            """
                            Parameter FlowX of value type float.
                            """
                            pass

                        class FlowXComputed(PyMenu):
                            """
                            Parameter FlowXComputed of value type float.
                            """
                            pass

                        class FlowMagnitude(PyMenu):
                            """
                            Parameter FlowMagnitude of value type float.
                            """
                            pass

                        class NormalToBoundary(PyMenu):
                            """
                            Parameter NormalToBoundary of value type bool.
                            """
                            pass

                        class Mach(PyMenu):
                            """
                            Parameter Mach of value type float.
                            """
                            pass

                        class FlowYComputed(PyMenu):
                            """
                            Parameter FlowYComputed of value type float.
                            """
                            pass

                        class VelocityMode(PyMenu):
                            """
                            Parameter VelocityMode of value type str.
                            """
                            pass

                        class TurbIntermittency(PyMenu):
                            """
                            Parameter TurbIntermittency of value type float.
                            """
                            pass

                        class TurbViscRatio(PyMenu):
                            """
                            Parameter TurbViscRatio of value type float.
                            """
                            pass

                        class MachComputed(PyMenu):
                            """
                            Parameter MachComputed of value type float.
                            """
                            pass

                        class SettingsVisible(PyMenu):
                            """
                            Parameter SettingsVisible of value type bool.
                            """
                            pass

                        class TurbIntensity(PyMenu):
                            """
                            Parameter TurbIntensity of value type float.
                            """
                            pass

                        class FlowY(PyMenu):
                            """
                            Parameter FlowY of value type float.
                            """
                            pass

                        class TurbSpecification(PyMenu):
                            """
                            Parameter TurbSpecification of value type str.
                            """
                            pass

                        class Temperature(PyMenu):
                            """
                            Parameter Temperature of value type float.
                            """
                            pass

                        class BCSync(PyMenu):
                            """
                            Parameter BCSync of value type str.
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

                        class SettingsEditable(PyMenu):
                            """
                            Parameter SettingsEditable of value type bool.
                            """
                            pass

                        class AngleAlpha(PyMenu):
                            """
                            Parameter AngleAlpha of value type float.
                            """
                            pass

                        class FlowZ(PyMenu):
                            """
                            Parameter FlowZ of value type float.
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

                    class IceWall(PyMenu):
                        """
                        Singleton IceWall.
                        """
                        def __init__(self, service, rules, path):
                            self.Icing = self.__class__.Icing(service, rules, path + [("Icing", "")])
                            self.HeatFlux = self.__class__.HeatFlux(service, rules, path + [("HeatFlux", "")])
                            self.HeatFluxFlag = self.__class__.HeatFluxFlag(service, rules, path + [("HeatFluxFlag", "")])
                            super().__init__(service, rules, path)

                        class Icing(PyMenu):
                            """
                            Parameter Icing of value type str.
                            """
                            pass

                        class HeatFlux(PyMenu):
                            """
                            Parameter HeatFlux of value type float.
                            """
                            pass

                        class HeatFluxFlag(PyMenu):
                            """
                            Parameter HeatFluxFlag of value type bool.
                            """
                            pass

                    class ParticlesWall(PyMenu):
                        """
                        Singleton ParticlesWall.
                        """
                        def __init__(self, service, rules, path):
                            self.VaporWetWall = self.__class__.VaporWetWall(service, rules, path + [("VaporWetWall", "")])
                            super().__init__(service, rules, path)

                        class VaporWetWall(PyMenu):
                            """
                            Parameter VaporWetWall of value type bool.
                            """
                            pass

                    class AirflowMassFlowOutlet(PyMenu):
                        """
                        Singleton AirflowMassFlowOutlet.
                        """
                        def __init__(self, service, rules, path):
                            self.BCSync = self.__class__.BCSync(service, rules, path + [("BCSync", "")])
                            self.SettingsEditable = self.__class__.SettingsEditable(service, rules, path + [("SettingsEditable", "")])
                            self.MassFlowMode = self.__class__.MassFlowMode(service, rules, path + [("MassFlowMode", "")])
                            self.MassFlow = self.__class__.MassFlow(service, rules, path + [("MassFlow", "")])
                            self.SettingsVisible = self.__class__.SettingsVisible(service, rules, path + [("SettingsVisible", "")])
                            super().__init__(service, rules, path)

                        class BCSync(PyMenu):
                            """
                            Parameter BCSync of value type str.
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

                        class MassFlow(PyMenu):
                            """
                            Parameter MassFlow of value type float.
                            """
                            pass

                        class SettingsVisible(PyMenu):
                            """
                            Parameter SettingsVisible of value type bool.
                            """
                            pass

                    class IsInlet(PyMenu):
                        """
                        Parameter IsInlet of value type bool.
                        """
                        pass

                    class BCType(PyMenu):
                        """
                        Parameter BCType of value type str.
                        """
                        pass

                    class _name_(PyMenu):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                    class IsWall(PyMenu):
                        """
                        Parameter IsWall of value type bool.
                        """
                        pass

                    class IsExit(PyMenu):
                        """
                        Parameter IsExit of value type bool.
                        """
                        pass

                    class RenameBC(PyCommand):
                        """
                        RenameBC() -> bool
                        """
                        pass

                    class ImportConditions(PyCommand):
                        """
                        ImportConditions() -> bool
                        """
                        pass

                    class Display(PyCommand):
                        """
                        Display() -> bool
                        """
                        pass

                    class RefreshBCs(PyCommand):
                        """
                        RefreshBCs() -> bool
                        """
                        pass

                    class ResetToCustom(PyCommand):
                        """
                        ResetToCustom() -> bool
                        """
                        pass

                    class CopyWallAdiabaticP10(PyCommand):
                        """
                        CopyWallAdiabaticP10() -> bool
                        """
                        pass

                def __getitem__(self, key: str) -> _BC:
                    return super().__getitem__(key)

            class Domain(PyMenu):
                """
                Singleton Domain.
                """
                def __init__(self, service, rules, path):
                    self.Filter = self.__class__.Filter(service, rules, path + [("Filter", "")])
                    self.NodeOrderId = self.__class__.NodeOrderId(service, rules, path + [("NodeOrderId", "")])
                    self.Mode = self.__class__.Mode(service, rules, path + [("Mode", "")])
                    super().__init__(service, rules, path)

                class Filter(PyMenu):
                    """
                    Parameter Filter of value type str.
                    """
                    pass

                class NodeOrderId(PyMenu):
                    """
                    Parameter NodeOrderId of value type str.
                    """
                    pass

                class Mode(PyMenu):
                    """
                    Parameter Mode of value type str.
                    """
                    pass

            class Airflow(PyMenu):
                """
                Singleton Airflow.
                """
                def __init__(self, service, rules, path):
                    self.Conditions = self.__class__.Conditions(service, rules, path + [("Conditions", "")])
                    self.Fluent = self.__class__.Fluent(service, rules, path + [("Fluent", "")])
                    self.AirDirection = self.__class__.AirDirection(service, rules, path + [("AirDirection", "")])
                    self.General = self.__class__.General(service, rules, path + [("General", "")])
                    self.Fensap = self.__class__.Fensap(service, rules, path + [("Fensap", "")])
                    self.Refresh = self.__class__.Refresh(service, rules, "Refresh", path)
                    super().__init__(service, rules, path)

                class Conditions(PyMenu):
                    """
                    Singleton Conditions.
                    """
                    def __init__(self, service, rules, path):
                        self.AdiabaticStagnationTemperature = self.__class__.AdiabaticStagnationTemperature(service, rules, path + [("AdiabaticStagnationTemperature", "")])
                        self.SyncFluent = self.__class__.SyncFluent(service, rules, path + [("SyncFluent", "")])
                        self.Temperature = self.__class__.Temperature(service, rules, path + [("Temperature", "")])
                        self.Velocity = self.__class__.Velocity(service, rules, path + [("Velocity", "")])
                        self.AbsolutePressure = self.__class__.AbsolutePressure(service, rules, path + [("AbsolutePressure", "")])
                        self.Pressure = self.__class__.Pressure(service, rules, path + [("Pressure", "")])
                        self.OperatingPressure = self.__class__.OperatingPressure(service, rules, path + [("OperatingPressure", "")])
                        self.Reynolds = self.__class__.Reynolds(service, rules, path + [("Reynolds", "")])
                        self.Mach = self.__class__.Mach(service, rules, path + [("Mach", "")])
                        self.CharLen = self.__class__.CharLen(service, rules, path + [("CharLen", "")])
                        super().__init__(service, rules, path)

                    class AdiabaticStagnationTemperature(PyMenu):
                        """
                        Parameter AdiabaticStagnationTemperature of value type float.
                        """
                        pass

                    class SyncFluent(PyMenu):
                        """
                        Parameter SyncFluent of value type bool.
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

                    class OperatingPressure(PyMenu):
                        """
                        Parameter OperatingPressure of value type float.
                        """
                        pass

                    class Reynolds(PyMenu):
                        """
                        Parameter Reynolds of value type float.
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

                class Fluent(PyMenu):
                    """
                    Singleton Fluent.
                    """
                    def __init__(self, service, rules, path):
                        self.DiscretizationSchemes = self.__class__.DiscretizationSchemes(service, rules, path + [("DiscretizationSchemes", "")])
                        self.Models = self.__class__.Models(service, rules, path + [("Models", "")])
                        self.Materials = self.__class__.Materials(service, rules, path + [("Materials", "")])
                        self.Solver = self.__class__.Solver(service, rules, path + [("Solver", "")])
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
                                self.AllowedValues = self.__class__.AllowedValues(service, rules, path + [("AllowedValues", "")])
                                self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                                self.InternalName = self.__class__.InternalName(service, rules, path + [("InternalName", "")])
                                self.DomainId = self.__class__.DomainId(service, rules, path + [("DomainId", "")])
                                self.Value = self.__class__.Value(service, rules, path + [("Value", "")])
                                super().__init__(service, rules, path)

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

                            class InternalName(PyMenu):
                                """
                                Parameter InternalName of value type str.
                                """
                                pass

                            class DomainId(PyMenu):
                                """
                                Parameter DomainId of value type int.
                                """
                                pass

                            class Value(PyMenu):
                                """
                                Parameter Value of value type str.
                                """
                                pass

                        def __getitem__(self, key: str) -> _DiscretizationSchemes:
                            return super().__getitem__(key)

                    class Models(PyMenu):
                        """
                        Singleton Models.
                        """
                        def __init__(self, service, rules, path):
                            self.TransitionSSTRoughnessCorrelation = self.__class__.TransitionSSTRoughnessCorrelation(service, rules, path + [("TransitionSSTRoughnessCorrelation", "")])
                            self.KwModel = self.__class__.KwModel(service, rules, path + [("KwModel", "")])
                            self.Turbulence = self.__class__.Turbulence(service, rules, path + [("Turbulence", "")])
                            self.Energy = self.__class__.Energy(service, rules, path + [("Energy", "")])
                            self.TransitionSSTRoughnessConstant = self.__class__.TransitionSSTRoughnessConstant(service, rules, path + [("TransitionSSTRoughnessConstant", "")])
                            self.ViscousHeating = self.__class__.ViscousHeating(service, rules, path + [("ViscousHeating", "")])
                            self.ProductionLimiter = self.__class__.ProductionLimiter(service, rules, path + [("ProductionLimiter", "")])
                            super().__init__(service, rules, path)

                        class TransitionSSTRoughnessCorrelation(PyMenu):
                            """
                            Parameter TransitionSSTRoughnessCorrelation of value type bool.
                            """
                            pass

                        class KwModel(PyMenu):
                            """
                            Parameter KwModel of value type str.
                            """
                            pass

                        class Turbulence(PyMenu):
                            """
                            Parameter Turbulence of value type str.
                            """
                            pass

                        class Energy(PyMenu):
                            """
                            Parameter Energy of value type bool.
                            """
                            pass

                        class TransitionSSTRoughnessConstant(PyMenu):
                            """
                            Parameter TransitionSSTRoughnessConstant of value type float.
                            """
                            pass

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

                    class Materials(PyMenu):
                        """
                        Singleton Materials.
                        """
                        def __init__(self, service, rules, path):
                            self.AirDensityConstant = self.__class__.AirDensityConstant(service, rules, path + [("AirDensityConstant", "")])
                            self.AirViscosity = self.__class__.AirViscosity(service, rules, path + [("AirViscosity", "")])
                            self.SettingsSync = self.__class__.SettingsSync(service, rules, path + [("SettingsSync", "")])
                            self.AirViscosityConstant = self.__class__.AirViscosityConstant(service, rules, path + [("AirViscosityConstant", "")])
                            self.AirCpConstant = self.__class__.AirCpConstant(service, rules, path + [("AirCpConstant", "")])
                            self.AirThermalConductivityConstant = self.__class__.AirThermalConductivityConstant(service, rules, path + [("AirThermalConductivityConstant", "")])
                            self.AirCp = self.__class__.AirCp(service, rules, path + [("AirCp", "")])
                            self.AirDensity = self.__class__.AirDensity(service, rules, path + [("AirDensity", "")])
                            self.AirThermalConductivity = self.__class__.AirThermalConductivity(service, rules, path + [("AirThermalConductivity", "")])
                            super().__init__(service, rules, path)

                        class AirDensityConstant(PyMenu):
                            """
                            Parameter AirDensityConstant of value type float.
                            """
                            pass

                        class AirViscosity(PyMenu):
                            """
                            Parameter AirViscosity of value type str.
                            """
                            pass

                        class SettingsSync(PyMenu):
                            """
                            Parameter SettingsSync of value type str.
                            """
                            pass

                        class AirViscosityConstant(PyMenu):
                            """
                            Parameter AirViscosityConstant of value type float.
                            """
                            pass

                        class AirCpConstant(PyMenu):
                            """
                            Parameter AirCpConstant of value type float.
                            """
                            pass

                        class AirThermalConductivityConstant(PyMenu):
                            """
                            Parameter AirThermalConductivityConstant of value type float.
                            """
                            pass

                        class AirCp(PyMenu):
                            """
                            Parameter AirCp of value type str.
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
                        self.Alpha = self.__class__.Alpha(service, rules, path + [("Alpha", "")])
                        self.Mode = self.__class__.Mode(service, rules, path + [("Mode", "")])
                        self.VelocityY = self.__class__.VelocityY(service, rules, path + [("VelocityY", "")])
                        self.Beta = self.__class__.Beta(service, rules, path + [("Beta", "")])
                        self.VelocityX = self.__class__.VelocityX(service, rules, path + [("VelocityX", "")])
                        self.DragDir = self.__class__.DragDir(service, rules, path + [("DragDir", "")])
                        self.Magnitude = self.__class__.Magnitude(service, rules, path + [("Magnitude", "")])
                        self.VelocityZ = self.__class__.VelocityZ(service, rules, path + [("VelocityZ", "")])
                        self.LiftDir = self.__class__.LiftDir(service, rules, path + [("LiftDir", "")])
                        super().__init__(service, rules, path)

                    class Alpha(PyMenu):
                        """
                        Parameter Alpha of value type float.
                        """
                        pass

                    class Mode(PyMenu):
                        """
                        Parameter Mode of value type str.
                        """
                        pass

                    class VelocityY(PyMenu):
                        """
                        Parameter VelocityY of value type float.
                        """
                        pass

                    class Beta(PyMenu):
                        """
                        Parameter Beta of value type float.
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

                    class Magnitude(PyMenu):
                        """
                        Parameter Magnitude of value type float.
                        """
                        pass

                    class VelocityZ(PyMenu):
                        """
                        Parameter VelocityZ of value type float.
                        """
                        pass

                    class LiftDir(PyMenu):
                        """
                        Parameter LiftDir of value type str.
                        """
                        pass

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

                class Fensap(PyMenu):
                    """
                    Singleton Fensap.
                    """
                    def __init__(self, service, rules, path):
                        self.AV = self.__class__.AV(service, rules, path + [("AV", "")])
                        self.Advanced = self.__class__.Advanced(service, rules, path + [("Advanced", "")])
                        self.Model = self.__class__.Model(service, rules, path + [("Model", "")])
                        self.Turbulence = self.__class__.Turbulence(service, rules, path + [("Turbulence", "")])
                        super().__init__(service, rules, path)

                    class AV(PyMenu):
                        """
                        Singleton AV.
                        """
                        def __init__(self, service, rules, path):
                            self.Order = self.__class__.Order(service, rules, path + [("Order", "")])
                            self.Option = self.__class__.Option(service, rules, path + [("Option", "")])
                            self.CW = self.__class__.CW(service, rules, path + [("CW", "")])
                            super().__init__(service, rules, path)

                        class Order(PyMenu):
                            """
                            Parameter Order of value type float.
                            """
                            pass

                        class Option(PyMenu):
                            """
                            Parameter Option of value type str.
                            """
                            pass

                        class CW(PyMenu):
                            """
                            Parameter CW of value type float.
                            """
                            pass

                    class Advanced(PyMenu):
                        """
                        Singleton Advanced.
                        """
                        def __init__(self, service, rules, path):
                            self.SolverParameters = self.__class__.SolverParameters(service, rules, path + [("SolverParameters", "")])
                            super().__init__(service, rules, path)

                        class SolverParameters(PyMenu):
                            """
                            Parameter SolverParameters of value type str.
                            """
                            pass

                    class Model(PyMenu):
                        """
                        Singleton Model.
                        """
                        def __init__(self, service, rules, path):
                            self.EnergyConservativeFlag = self.__class__.EnergyConservativeFlag(service, rules, path + [("EnergyConservativeFlag", "")])
                            self.EnergyEquation = self.__class__.EnergyEquation(service, rules, path + [("EnergyEquation", "")])
                            self.CoupledFlag = self.__class__.CoupledFlag(service, rules, path + [("CoupledFlag", "")])
                            super().__init__(service, rules, path)

                        class EnergyConservativeFlag(PyMenu):
                            """
                            Parameter EnergyConservativeFlag of value type bool.
                            """
                            pass

                        class EnergyEquation(PyMenu):
                            """
                            Parameter EnergyEquation of value type str.
                            """
                            pass

                        class CoupledFlag(PyMenu):
                            """
                            Parameter CoupledFlag of value type bool.
                            """
                            pass

                    class Turbulence(PyMenu):
                        """
                        Singleton Turbulence.
                        """
                        def __init__(self, service, rules, path):
                            self.CustomFlag = self.__class__.CustomFlag(service, rules, path + [("CustomFlag", "")])
                            self.TransitionSA = self.__class__.TransitionSA(service, rules, path + [("TransitionSA", "")])
                            self.TransitionSST = self.__class__.TransitionSST(service, rules, path + [("TransitionSST", "")])
                            self.Model = self.__class__.Model(service, rules, path + [("Model", "")])
                            super().__init__(service, rules, path)

                        class CustomFlag(PyMenu):
                            """
                            Parameter CustomFlag of value type bool.
                            """
                            pass

                        class TransitionSA(PyMenu):
                            """
                            Parameter TransitionSA of value type str.
                            """
                            pass

                        class TransitionSST(PyMenu):
                            """
                            Parameter TransitionSST of value type str.
                            """
                            pass

                        class Model(PyMenu):
                            """
                            Parameter Model of value type str.
                            """
                            pass

                class Refresh(PyCommand):
                    """
                    Refresh() -> bool
                    """
                    pass

            class Particles(PyMenu):
                """
                Singleton Particles.
                """
                def __init__(self, service, rules, path):
                    self.Crystals = self.__class__.Crystals(service, rules, path + [("Crystals", "")])
                    self.Advanced = self.__class__.Advanced(service, rules, path + [("Advanced", "")])
                    self.Droplets = self.__class__.Droplets(service, rules, path + [("Droplets", "")])
                    self.General = self.__class__.General(service, rules, path + [("General", "")])
                    self.Vapor = self.__class__.Vapor(service, rules, path + [("Vapor", "")])
                    self.Model = self.__class__.Model(service, rules, path + [("Model", "")])
                    self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                    super().__init__(service, rules, path)

                class Crystals(PyMenu):
                    """
                    Singleton Crystals.
                    """
                    def __init__(self, service, rules, path):
                        self.Conditions = self.__class__.Conditions(service, rules, path + [("Conditions", "")])
                        self.ParticlesDistribution = self.__class__.ParticlesDistribution(service, rules, path + [("ParticlesDistribution", "")])
                        super().__init__(service, rules, path)

                    class Conditions(PyMenu):
                        """
                        Singleton Conditions.
                        """
                        def __init__(self, service, rules, path):
                            self.Density = self.__class__.Density(service, rules, path + [("Density", "")])
                            self.AppendixLWCPriorityMode = self.__class__.AppendixLWCPriorityMode(service, rules, path + [("AppendixLWCPriorityMode", "")])
                            self.AppendixTWCFactor = self.__class__.AppendixTWCFactor(service, rules, path + [("AppendixTWCFactor", "")])
                            self.Appendix = self.__class__.Appendix(service, rules, path + [("Appendix", "")])
                            self.ICC = self.__class__.ICC(service, rules, path + [("ICC", "")])
                            self.AR = self.__class__.AR(service, rules, path + [("AR", "")])
                            self.Diameter = self.__class__.Diameter(service, rules, path + [("Diameter", "")])
                            self.CheckAppendixD = self.__class__.CheckAppendixD(service, rules, "CheckAppendixD", path)
                            self.ViewAppendix = self.__class__.ViewAppendix(service, rules, "ViewAppendix", path)
                            super().__init__(service, rules, path)

                        class Density(PyMenu):
                            """
                            Parameter Density of value type float.
                            """
                            pass

                        class AppendixLWCPriorityMode(PyMenu):
                            """
                            Parameter AppendixLWCPriorityMode of value type bool.
                            """
                            pass

                        class AppendixTWCFactor(PyMenu):
                            """
                            Parameter AppendixTWCFactor of value type bool.
                            """
                            pass

                        class Appendix(PyMenu):
                            """
                            Parameter Appendix of value type str.
                            """
                            pass

                        class ICC(PyMenu):
                            """
                            Parameter ICC of value type float.
                            """
                            pass

                        class AR(PyMenu):
                            """
                            Parameter AR of value type float.
                            """
                            pass

                        class Diameter(PyMenu):
                            """
                            Parameter Diameter of value type float.
                            """
                            pass

                        class CheckAppendixD(PyCommand):
                            """
                            CheckAppendixD(UpdateTWC: bool) -> bool
                            """
                            pass

                        class ViewAppendix(PyCommand):
                            """
                            ViewAppendix(Target: str) -> bool
                            """
                            pass

                    class ParticlesDistribution(PyMenu):
                        """
                        Singleton ParticlesDistribution.
                        """
                        def __init__(self, service, rules, path):
                            self.CrystalAspectRatios = self.__class__.CrystalAspectRatios(service, rules, path + [("CrystalAspectRatios", "")])
                            self.CrystalDiameters = self.__class__.CrystalDiameters(service, rules, path + [("CrystalDiameters", "")])
                            self.CrystalDistribution = self.__class__.CrystalDistribution(service, rules, path + [("CrystalDistribution", "")])
                            self.ViewDistribution = self.__class__.ViewDistribution(service, rules, "ViewDistribution", path)
                            self.ExportDistribution = self.__class__.ExportDistribution(service, rules, "ExportDistribution", path)
                            self.ImportDistribution = self.__class__.ImportDistribution(service, rules, "ImportDistribution", path)
                            super().__init__(service, rules, path)

                        class CrystalAspectRatios(PyMenu):
                            """
                            Parameter CrystalAspectRatios of value type str.
                            """
                            pass

                        class CrystalDiameters(PyMenu):
                            """
                            Parameter CrystalDiameters of value type str.
                            """
                            pass

                        class CrystalDistribution(PyMenu):
                            """
                            Parameter CrystalDistribution of value type str.
                            """
                            pass

                        class ViewDistribution(PyCommand):
                            """
                            ViewDistribution(Target: str) -> bool
                            """
                            pass

                        class ExportDistribution(PyCommand):
                            """
                            ExportDistribution(Filename: str) -> bool
                            """
                            pass

                        class ImportDistribution(PyCommand):
                            """
                            ImportDistribution(Filename: str) -> bool
                            """
                            pass

                class Advanced(PyMenu):
                    """
                    Singleton Advanced.
                    """
                    def __init__(self, service, rules, path):
                        self.SolverParameters = self.__class__.SolverParameters(service, rules, path + [("SolverParameters", "")])
                        super().__init__(service, rules, path)

                    class SolverParameters(PyMenu):
                        """
                        Parameter SolverParameters of value type str.
                        """
                        pass

                class Droplets(PyMenu):
                    """
                    Singleton Droplets.
                    """
                    def __init__(self, service, rules, path):
                        self.ParticlesDistribution = self.__class__.ParticlesDistribution(service, rules, path + [("ParticlesDistribution", "")])
                        self.Conditions = self.__class__.Conditions(service, rules, path + [("Conditions", "")])
                        self.Model = self.__class__.Model(service, rules, path + [("Model", "")])
                        super().__init__(service, rules, path)

                    class ParticlesDistribution(PyMenu):
                        """
                        Singleton ParticlesDistribution.
                        """
                        def __init__(self, service, rules, path):
                            self.AppODistribution = self.__class__.AppODistribution(service, rules, path + [("AppODistribution", "")])
                            self.DropletDiameters = self.__class__.DropletDiameters(service, rules, path + [("DropletDiameters", "")])
                            self.Weights = self.__class__.Weights(service, rules, path + [("Weights", "")])
                            self.DPMDropletDistribution = self.__class__.DPMDropletDistribution(service, rules, path + [("DPMDropletDistribution", "")])
                            self.DropletDistribution = self.__class__.DropletDistribution(service, rules, path + [("DropletDistribution", "")])
                            self.ImportDistribution = self.__class__.ImportDistribution(service, rules, "ImportDistribution", path)
                            self.ViewDistribution = self.__class__.ViewDistribution(service, rules, "ViewDistribution", path)
                            self.ExportDistribution = self.__class__.ExportDistribution(service, rules, "ExportDistribution", path)
                            super().__init__(service, rules, path)

                        class AppODistribution(PyMenu):
                            """
                            Parameter AppODistribution of value type str.
                            """
                            pass

                        class DropletDiameters(PyMenu):
                            """
                            Parameter DropletDiameters of value type str.
                            """
                            pass

                        class Weights(PyMenu):
                            """
                            Parameter Weights of value type str.
                            """
                            pass

                        class DPMDropletDistribution(PyMenu):
                            """
                            Parameter DPMDropletDistribution of value type str.
                            """
                            pass

                        class DropletDistribution(PyMenu):
                            """
                            Parameter DropletDistribution of value type str.
                            """
                            pass

                        class ImportDistribution(PyCommand):
                            """
                            ImportDistribution(Filename: str) -> bool
                            """
                            pass

                        class ViewDistribution(PyCommand):
                            """
                            ViewDistribution(Target: str) -> bool
                            """
                            pass

                        class ExportDistribution(PyCommand):
                            """
                            ExportDistribution(Filename: str) -> bool
                            """
                            pass

                    class Conditions(PyMenu):
                        """
                        Singleton Conditions.
                        """
                        def __init__(self, service, rules, path):
                            self.AppendixLWCFactor = self.__class__.AppendixLWCFactor(service, rules, path + [("AppendixLWCFactor", "")])
                            self.LWC = self.__class__.LWC(service, rules, path + [("LWC", "")])
                            self.WaterDensity = self.__class__.WaterDensity(service, rules, path + [("WaterDensity", "")])
                            self.Diameter = self.__class__.Diameter(service, rules, path + [("Diameter", "")])
                            self.AppendixODiameter = self.__class__.AppendixODiameter(service, rules, path + [("AppendixODiameter", "")])
                            self.AppendixEnvironment = self.__class__.AppendixEnvironment(service, rules, path + [("AppendixEnvironment", "")])
                            self.Appendix = self.__class__.Appendix(service, rules, path + [("Appendix", "")])
                            self.AppendixOLWCFactor = self.__class__.AppendixOLWCFactor(service, rules, path + [("AppendixOLWCFactor", "")])
                            self.SLDFlag = self.__class__.SLDFlag(service, rules, path + [("SLDFlag", "")])
                            self.AppendixOEnvironment = self.__class__.AppendixOEnvironment(service, rules, path + [("AppendixOEnvironment", "")])
                            self.CheckAppendixC = self.__class__.CheckAppendixC(service, rules, "CheckAppendixC", path)
                            self.ViewAppendix = self.__class__.ViewAppendix(service, rules, "ViewAppendix", path)
                            self.CheckAppendixO = self.__class__.CheckAppendixO(service, rules, "CheckAppendixO", path)
                            super().__init__(service, rules, path)

                        class AppendixLWCFactor(PyMenu):
                            """
                            Parameter AppendixLWCFactor of value type bool.
                            """
                            pass

                        class LWC(PyMenu):
                            """
                            Parameter LWC of value type float.
                            """
                            pass

                        class WaterDensity(PyMenu):
                            """
                            Parameter WaterDensity of value type float.
                            """
                            pass

                        class Diameter(PyMenu):
                            """
                            Parameter Diameter of value type float.
                            """
                            pass

                        class AppendixODiameter(PyMenu):
                            """
                            Parameter AppendixODiameter of value type int.
                            """
                            pass

                        class AppendixEnvironment(PyMenu):
                            """
                            Parameter AppendixEnvironment of value type int.
                            """
                            pass

                        class Appendix(PyMenu):
                            """
                            Parameter Appendix of value type str.
                            """
                            pass

                        class AppendixOLWCFactor(PyMenu):
                            """
                            Parameter AppendixOLWCFactor of value type bool.
                            """
                            pass

                        class SLDFlag(PyMenu):
                            """
                            Parameter SLDFlag of value type bool.
                            """
                            pass

                        class AppendixOEnvironment(PyMenu):
                            """
                            Parameter AppendixOEnvironment of value type int.
                            """
                            pass

                        class CheckAppendixC(PyCommand):
                            """
                            CheckAppendixC(UpdateLWC: bool) -> bool
                            """
                            pass

                        class ViewAppendix(PyCommand):
                            """
                            ViewAppendix(Target: str) -> bool
                            """
                            pass

                        class CheckAppendixO(PyCommand):
                            """
                            CheckAppendixO() -> bool
                            """
                            pass

                    class Model(PyMenu):
                        """
                        Singleton Model.
                        """
                        def __init__(self, service, rules, path):
                            self.SplashingModel = self.__class__.SplashingModel(service, rules, path + [("SplashingModel", "")])
                            self.Splashing = self.__class__.Splashing(service, rules, path + [("Splashing", "")])
                            self.TurbulentDispersion = self.__class__.TurbulentDispersion(service, rules, path + [("TurbulentDispersion", "")])
                            self.SplashingActivationTrigger = self.__class__.SplashingActivationTrigger(service, rules, path + [("SplashingActivationTrigger", "")])
                            self.DpmDragModel = self.__class__.DpmDragModel(service, rules, path + [("DpmDragModel", "")])
                            self.TerminalVelocity = self.__class__.TerminalVelocity(service, rules, path + [("TerminalVelocity", "")])
                            self.NTries = self.__class__.NTries(service, rules, path + [("NTries", "")])
                            self.DragModel = self.__class__.DragModel(service, rules, path + [("DragModel", "")])
                            self.SplashingDelay = self.__class__.SplashingDelay(service, rules, path + [("SplashingDelay", "")])
                            self.BreakupModel = self.__class__.BreakupModel(service, rules, path + [("BreakupModel", "")])
                            super().__init__(service, rules, path)

                        class SplashingModel(PyMenu):
                            """
                            Parameter SplashingModel of value type str.
                            """
                            pass

                        class Splashing(PyMenu):
                            """
                            Parameter Splashing of value type str.
                            """
                            pass

                        class TurbulentDispersion(PyMenu):
                            """
                            Parameter TurbulentDispersion of value type bool.
                            """
                            pass

                        class SplashingActivationTrigger(PyMenu):
                            """
                            Parameter SplashingActivationTrigger of value type float.
                            """
                            pass

                        class DpmDragModel(PyMenu):
                            """
                            Parameter DpmDragModel of value type str.
                            """
                            pass

                        class TerminalVelocity(PyMenu):
                            """
                            Parameter TerminalVelocity of value type str.
                            """
                            pass

                        class NTries(PyMenu):
                            """
                            Parameter NTries of value type int.
                            """
                            pass

                        class DragModel(PyMenu):
                            """
                            Parameter DragModel of value type str.
                            """
                            pass

                        class SplashingDelay(PyMenu):
                            """
                            Parameter SplashingDelay of value type int.
                            """
                            pass

                        class BreakupModel(PyMenu):
                            """
                            Parameter BreakupModel of value type str.
                            """
                            pass

                class General(PyMenu):
                    """
                    Singleton General.
                    """
                    def __init__(self, service, rules, path):
                        self.UseCaseInjection = self.__class__.UseCaseInjection(service, rules, path + [("UseCaseInjection", "")])
                        self.EnableDPMType = self.__class__.EnableDPMType(service, rules, path + [("EnableDPMType", "")])
                        self.SolverType = self.__class__.SolverType(service, rules, path + [("SolverType", "")])
                        super().__init__(service, rules, path)

                    class UseCaseInjection(PyMenu):
                        """
                        Parameter UseCaseInjection of value type str.
                        """
                        pass

                    class EnableDPMType(PyMenu):
                        """
                        Parameter EnableDPMType of value type bool.
                        """
                        pass

                    class SolverType(PyMenu):
                        """
                        Parameter SolverType of value type str.
                        """
                        pass

                class Vapor(PyMenu):
                    """
                    Singleton Vapor.
                    """
                    def __init__(self, service, rules, path):
                        self.Conditions = self.__class__.Conditions(service, rules, path + [("Conditions", "")])
                        self.Model = self.__class__.Model(service, rules, path + [("Model", "")])
                        super().__init__(service, rules, path)

                    class Conditions(PyMenu):
                        """
                        Singleton Conditions.
                        """
                        def __init__(self, service, rules, path):
                            self.VaporInitialMode = self.__class__.VaporInitialMode(service, rules, path + [("VaporInitialMode", "")])
                            self.VaporRH = self.__class__.VaporRH(service, rules, path + [("VaporRH", "")])
                            self.VaporConcentration = self.__class__.VaporConcentration(service, rules, path + [("VaporConcentration", "")])
                            super().__init__(service, rules, path)

                        class VaporInitialMode(PyMenu):
                            """
                            Parameter VaporInitialMode of value type str.
                            """
                            pass

                        class VaporRH(PyMenu):
                            """
                            Parameter VaporRH of value type float.
                            """
                            pass

                        class VaporConcentration(PyMenu):
                            """
                            Parameter VaporConcentration of value type float.
                            """
                            pass

                    class Model(PyMenu):
                        """
                        Singleton Model.
                        """
                        def __init__(self, service, rules, path):
                            self.TurbSchmidtNumber = self.__class__.TurbSchmidtNumber(service, rules, path + [("TurbSchmidtNumber", "")])
                            super().__init__(service, rules, path)

                        class TurbSchmidtNumber(PyMenu):
                            """
                            Parameter TurbSchmidtNumber of value type float.
                            """
                            pass

                class Model(PyMenu):
                    """
                    Singleton Model.
                    """
                    def __init__(self, service, rules, path):
                        self.ThermalEquation = self.__class__.ThermalEquation(service, rules, path + [("ThermalEquation", "")])
                        super().__init__(service, rules, path)

                    class ThermalEquation(PyMenu):
                        """
                        Parameter ThermalEquation of value type bool.
                        """
                        pass

                class Type(PyMenu):
                    """
                    Singleton Type.
                    """
                    def __init__(self, service, rules, path):
                        self.DropletsFlag = self.__class__.DropletsFlag(service, rules, path + [("DropletsFlag", "")])
                        self.VaporFlag = self.__class__.VaporFlag(service, rules, path + [("VaporFlag", "")])
                        self.CrystalsFlag = self.__class__.CrystalsFlag(service, rules, path + [("CrystalsFlag", "")])
                        super().__init__(service, rules, path)

                    class DropletsFlag(PyMenu):
                        """
                        Parameter DropletsFlag of value type bool.
                        """
                        pass

                    class VaporFlag(PyMenu):
                        """
                        Parameter VaporFlag of value type bool.
                        """
                        pass

                    class CrystalsFlag(PyMenu):
                        """
                        Parameter CrystalsFlag of value type bool.
                        """
                        pass

            class Solution(PyMenu):
                """
                Singleton Solution.
                """
                def __init__(self, service, rules, path):
                    self.RunState = self.__class__.RunState(service, rules, path + [("RunState", "")])
                    self.AdaptationGlobalSettings = self.__class__.AdaptationGlobalSettings(service, rules, path + [("AdaptationGlobalSettings", "")])
                    self.MultishotRun = self.__class__.MultishotRun(service, rules, path + [("MultishotRun", "")])
                    self.GlobalSettings = self.__class__.GlobalSettings(service, rules, path + [("GlobalSettings", "")])
                    self.ParticlesRun = self.__class__.ParticlesRun(service, rules, path + [("ParticlesRun", "")])
                    self.AirflowRun = self.__class__.AirflowRun(service, rules, path + [("AirflowRun", "")])
                    self.IceRun = self.__class__.IceRun(service, rules, path + [("IceRun", "")])
                    self.CHT = self.__class__.CHT(service, rules, path + [("CHT", "")])
                    self.AdaptationRun = self.__class__.AdaptationRun(service, rules, path + [("AdaptationRun", "")])
                    self.Calculate = self.__class__.Calculate(service, rules, "Calculate", path)
                    self.CalculateOG = self.__class__.CalculateOG(service, rules, "CalculateOG", path)
                    self.Interrupt = self.__class__.Interrupt(service, rules, "Interrupt", path)
                    self.ResetMultishot = self.__class__.ResetMultishot(service, rules, "ResetMultishot", path)
                    self.FensapGridSave = self.__class__.FensapGridSave(service, rules, "FensapGridSave", path)
                    self.Reset = self.__class__.Reset(service, rules, "Reset", path)
                    self.ConfigureShots = self.__class__.ConfigureShots(service, rules, "ConfigureShots", path)
                    super().__init__(service, rules, path)

                class RunState(PyMenu):
                    """
                    Singleton RunState.
                    """
                    def __init__(self, service, rules, path):
                        self.ProjectRunIterator = self.__class__.ProjectRunIterator(service, rules, path + [("ProjectRunIterator", "")])
                        self.CurrentStep = self.__class__.CurrentStep(service, rules, path + [("CurrentStep", "")])
                        self.MultishotState = self.__class__.MultishotState(service, rules, path + [("MultishotState", "")])
                        self.RunMode = self.__class__.RunMode(service, rules, path + [("RunMode", "")])
                        self.ClientProcessRunning = self.__class__.ClientProcessRunning(service, rules, path + [("ClientProcessRunning", "")])
                        self.SubStepID = self.__class__.SubStepID(service, rules, path + [("SubStepID", "")])
                        self.ShotID = self.__class__.ShotID(service, rules, path + [("ShotID", "")])
                        super().__init__(service, rules, path)

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

                    class MultishotState(PyMenu):
                        """
                        Parameter MultishotState of value type str.
                        """
                        pass

                    class RunMode(PyMenu):
                        """
                        Parameter RunMode of value type str.
                        """
                        pass

                    class ClientProcessRunning(PyMenu):
                        """
                        Parameter ClientProcessRunning of value type bool.
                        """
                        pass

                    class SubStepID(PyMenu):
                        """
                        Parameter SubStepID of value type int.
                        """
                        pass

                    class ShotID(PyMenu):
                        """
                        Parameter ShotID of value type int.
                        """
                        pass

                class AdaptationGlobalSettings(PyMenu):
                    """
                    Singleton AdaptationGlobalSettings.
                    """
                    def __init__(self, service, rules, path):
                        self.SolutionRestart = self.__class__.SolutionRestart(service, rules, path + [("SolutionRestart", "")])
                        self.NumberLoops = self.__class__.NumberLoops(service, rules, path + [("NumberLoops", "")])
                        self.RunSolver = self.__class__.RunSolver(service, rules, path + [("RunSolver", "")])
                        super().__init__(service, rules, path)

                    class SolutionRestart(PyMenu):
                        """
                        Parameter SolutionRestart of value type str.
                        """
                        pass

                    class NumberLoops(PyMenu):
                        """
                        Parameter NumberLoops of value type int.
                        """
                        pass

                    class RunSolver(PyMenu):
                        """
                        Parameter RunSolver of value type bool.
                        """
                        pass

                class MultishotRun(PyMenu):
                    """
                    Singleton MultishotRun.
                    """
                    def __init__(self, service, rules, path):
                        self.TotalTime = self.__class__.TotalTime(service, rules, path + [("TotalTime", "")])
                        self.ShotRestartStep = self.__class__.ShotRestartStep(service, rules, path + [("ShotRestartStep", "")])
                        self.FirstShotAirflowIterations = self.__class__.FirstShotAirflowIterations(service, rules, path + [("FirstShotAirflowIterations", "")])
                        self.RootFilename = self.__class__.RootFilename(service, rules, path + [("RootFilename", "")])
                        self.FirstShotParticlesIterations = self.__class__.FirstShotParticlesIterations(service, rules, path + [("FirstShotParticlesIterations", "")])
                        self.ShotRestart = self.__class__.ShotRestart(service, rules, path + [("ShotRestart", "")])
                        self.ShotRestartTime = self.__class__.ShotRestartTime(service, rules, path + [("ShotRestartTime", "")])
                        self.SettingsMode = self.__class__.SettingsMode(service, rules, path + [("SettingsMode", "")])
                        self.AirflowRestart = self.__class__.AirflowRestart(service, rules, path + [("AirflowRestart", "")])
                        self.NumberShots = self.__class__.NumberShots(service, rules, path + [("NumberShots", "")])
                        self.IterationSettings = self.__class__.IterationSettings(service, rules, path + [("IterationSettings", "")])
                        self.SaveFiles = self.__class__.SaveFiles(service, rules, path + [("SaveFiles", "")])
                        super().__init__(service, rules, path)

                    class TotalTime(PyMenu):
                        """
                        Parameter TotalTime of value type float.
                        """
                        pass

                    class ShotRestartStep(PyMenu):
                        """
                        Parameter ShotRestartStep of value type str.
                        """
                        pass

                    class FirstShotAirflowIterations(PyMenu):
                        """
                        Parameter FirstShotAirflowIterations of value type int.
                        """
                        pass

                    class RootFilename(PyMenu):
                        """
                        Parameter RootFilename of value type str.
                        """
                        pass

                    class FirstShotParticlesIterations(PyMenu):
                        """
                        Parameter FirstShotParticlesIterations of value type int.
                        """
                        pass

                    class ShotRestart(PyMenu):
                        """
                        Parameter ShotRestart of value type int.
                        """
                        pass

                    class ShotRestartTime(PyMenu):
                        """
                        Parameter ShotRestartTime of value type float.
                        """
                        pass

                    class SettingsMode(PyMenu):
                        """
                        Parameter SettingsMode of value type str.
                        """
                        pass

                    class AirflowRestart(PyMenu):
                        """
                        Parameter AirflowRestart of value type str.
                        """
                        pass

                    class NumberShots(PyMenu):
                        """
                        Parameter NumberShots of value type int.
                        """
                        pass

                    class IterationSettings(PyMenu):
                        """
                        Parameter IterationSettings of value type str.
                        """
                        pass

                    class SaveFiles(PyMenu):
                        """
                        Parameter SaveFiles of value type bool.
                        """
                        pass

                class GlobalSettings(PyMenu):
                    """
                    Singleton GlobalSettings.
                    """
                    def __init__(self, service, rules, path):
                        self.SaveConverg = self.__class__.SaveConverg(service, rules, path + [("SaveConverg", "")])
                        self.AutoSave = self.__class__.AutoSave(service, rules, path + [("AutoSave", "")])
                        self.PlotInterval = self.__class__.PlotInterval(service, rules, path + [("PlotInterval", "")])
                        self.SaveGMRES = self.__class__.SaveGMRES(service, rules, path + [("SaveGMRES", "")])
                        self.MonitorMode = self.__class__.MonitorMode(service, rules, path + [("MonitorMode", "")])
                        self.Verbosity = self.__class__.Verbosity(service, rules, path + [("Verbosity", "")])
                        super().__init__(service, rules, path)

                    class SaveConverg(PyMenu):
                        """
                        Parameter SaveConverg of value type bool.
                        """
                        pass

                    class AutoSave(PyMenu):
                        """
                        Parameter AutoSave of value type bool.
                        """
                        pass

                    class PlotInterval(PyMenu):
                        """
                        Parameter PlotInterval of value type int.
                        """
                        pass

                    class SaveGMRES(PyMenu):
                        """
                        Parameter SaveGMRES of value type bool.
                        """
                        pass

                    class MonitorMode(PyMenu):
                        """
                        Parameter MonitorMode of value type str.
                        """
                        pass

                    class Verbosity(PyMenu):
                        """
                        Parameter Verbosity of value type str.
                        """
                        pass

                class ParticlesRun(PyMenu):
                    """
                    Singleton ParticlesRun.
                    """
                    def __init__(self, service, rules, path):
                        self.SolutionInfo = self.__class__.SolutionInfo(service, rules, path + [("SolutionInfo", "")])
                        self.Output = self.__class__.Output(service, rules, path + [("Output", "")])
                        self.InitConditions = self.__class__.InitConditions(service, rules, path + [("InitConditions", "")])
                        self.Monitors = self.__class__.Monitors(service, rules, path + [("Monitors", "")])
                        self.RunSettings = self.__class__.RunSettings(service, rules, path + [("RunSettings", "")])
                        self.DropletOutputSolution = self.__class__.DropletOutputSolution(service, rules, path + [("DropletOutputSolution", "")])
                        self.CrystalOutputSolution = self.__class__.CrystalOutputSolution(service, rules, path + [("CrystalOutputSolution", "")])
                        self.Solver = self.__class__.Solver(service, rules, path + [("Solver", "")])
                        self.VaporOutputSolution = self.__class__.VaporOutputSolution(service, rules, path + [("VaporOutputSolution", "")])
                        self.ConvergenceAvailable = self.__class__.ConvergenceAvailable(service, rules, path + [("ConvergenceAvailable", "")])
                        self.SolutionAvailable = self.__class__.SolutionAvailable(service, rules, path + [("SolutionAvailable", "")])
                        self.Save = self.__class__.Save(service, rules, "Save", path)
                        self.Calculate = self.__class__.Calculate(service, rules, "Calculate", path)
                        self.LoadParticles = self.__class__.LoadParticles(service, rules, "LoadParticles", path)
                        self.Interrupt = self.__class__.Interrupt(service, rules, "Interrupt", path)
                        self.Reset = self.__class__.Reset(service, rules, "Reset", path)
                        self.SaveDroplets = self.__class__.SaveDroplets(service, rules, "SaveDroplets", path)
                        self.SaveVapor = self.__class__.SaveVapor(service, rules, "SaveVapor", path)
                        self.SaveAs = self.__class__.SaveAs(service, rules, "SaveAs", path)
                        self.SaveCrystals = self.__class__.SaveCrystals(service, rules, "SaveCrystals", path)
                        self.LoadDroplets = self.__class__.LoadDroplets(service, rules, "LoadDroplets", path)
                        self.LoadCrystals = self.__class__.LoadCrystals(service, rules, "LoadCrystals", path)
                        self.Initialize = self.__class__.Initialize(service, rules, "Initialize", path)
                        self.LoadVapor = self.__class__.LoadVapor(service, rules, "LoadVapor", path)
                        super().__init__(service, rules, path)

                    class SolutionInfo(PyMenu):
                        """
                        Singleton SolutionInfo.
                        """
                        def __init__(self, service, rules, path):
                            self.InputSolutionType = self.__class__.InputSolutionType(service, rules, path + [("InputSolutionType", "")])
                            super().__init__(service, rules, path)

                        class InputSolutionType(PyMenu):
                            """
                            Parameter InputSolutionType of value type str.
                            """
                            pass

                    class Output(PyMenu):
                        """
                        Singleton Output.
                        """
                        def __init__(self, service, rules, path):
                            self.NumberedOutput = self.__class__.NumberedOutput(service, rules, path + [("NumberedOutput", "")])
                            self.SaveDelay = self.__class__.SaveDelay(service, rules, path + [("SaveDelay", "")])
                            self.DistributionRestart = self.__class__.DistributionRestart(service, rules, path + [("DistributionRestart", "")])
                            self.AutoSaveDistribution = self.__class__.AutoSaveDistribution(service, rules, path + [("AutoSaveDistribution", "")])
                            super().__init__(service, rules, path)

                        class NumberedOutput(PyMenu):
                            """
                            Parameter NumberedOutput of value type bool.
                            """
                            pass

                        class SaveDelay(PyMenu):
                            """
                            Parameter SaveDelay of value type int.
                            """
                            pass

                        class DistributionRestart(PyMenu):
                            """
                            Parameter DistributionRestart of value type str.
                            """
                            pass

                        class AutoSaveDistribution(PyMenu):
                            """
                            Parameter AutoSaveDistribution of value type bool.
                            """
                            pass

                    class InitConditions(PyMenu):
                        """
                        Singleton InitConditions.
                        """
                        def __init__(self, service, rules, path):
                            self.Magnitude = self.__class__.Magnitude(service, rules, path + [("Magnitude", "")])
                            self.Beta = self.__class__.Beta(service, rules, path + [("Beta", "")])
                            self.VelocityX = self.__class__.VelocityX(service, rules, path + [("VelocityX", "")])
                            self.VelocityZ = self.__class__.VelocityZ(service, rules, path + [("VelocityZ", "")])
                            self.Alpha = self.__class__.Alpha(service, rules, path + [("Alpha", "")])
                            self.VelocityFlag = self.__class__.VelocityFlag(service, rules, path + [("VelocityFlag", "")])
                            self.InitMode = self.__class__.InitMode(service, rules, path + [("InitMode", "")])
                            self.VelocityY = self.__class__.VelocityY(service, rules, path + [("VelocityY", "")])
                            self.DryInit = self.__class__.DryInit(service, rules, path + [("DryInit", "")])
                            super().__init__(service, rules, path)

                        class Magnitude(PyMenu):
                            """
                            Parameter Magnitude of value type float.
                            """
                            pass

                        class Beta(PyMenu):
                            """
                            Parameter Beta of value type float.
                            """
                            pass

                        class VelocityX(PyMenu):
                            """
                            Parameter VelocityX of value type float.
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

                        class VelocityFlag(PyMenu):
                            """
                            Parameter VelocityFlag of value type bool.
                            """
                            pass

                        class InitMode(PyMenu):
                            """
                            Parameter InitMode of value type str.
                            """
                            pass

                        class VelocityY(PyMenu):
                            """
                            Parameter VelocityY of value type float.
                            """
                            pass

                        class DryInit(PyMenu):
                            """
                            Parameter DryInit of value type bool.
                            """
                            pass

                    class Monitors(PyMenu):
                        """
                        Singleton Monitors.
                        """
                        def __init__(self, service, rules, path):
                            self.VaporCondensation = self.__class__.VaporCondensation(service, rules, path + [("VaporCondensation", "")])
                            self.ChangeBeta = self.__class__.ChangeBeta(service, rules, path + [("ChangeBeta", "")])
                            self.TotalBeta = self.__class__.TotalBeta(service, rules, path + [("TotalBeta", "")])
                            self.MassDeficit = self.__class__.MassDeficit(service, rules, path + [("MassDeficit", "")])
                            super().__init__(service, rules, path)

                        class VaporCondensation(PyMenu):
                            """
                            Parameter VaporCondensation of value type bool.
                            """
                            pass

                        class ChangeBeta(PyMenu):
                            """
                            Parameter ChangeBeta of value type bool.
                            """
                            pass

                        class TotalBeta(PyMenu):
                            """
                            Parameter TotalBeta of value type bool.
                            """
                            pass

                        class MassDeficit(PyMenu):
                            """
                            Parameter MassDeficit of value type bool.
                            """
                            pass

                    class RunSettings(PyMenu):
                        """
                        Singleton RunSettings.
                        """
                        def __init__(self, service, rules, path):
                            self.StepLengthFactor = self.__class__.StepLengthFactor(service, rules, path + [("StepLengthFactor", "")])
                            self.StepLengthScale = self.__class__.StepLengthScale(service, rules, path + [("StepLengthScale", "")])
                            self.MaxStepNumber = self.__class__.MaxStepNumber(service, rules, path + [("MaxStepNumber", "")])
                            self.UseStepLengthScale = self.__class__.UseStepLengthScale(service, rules, path + [("UseStepLengthScale", "")])
                            self.NumIterations = self.__class__.NumIterations(service, rules, path + [("NumIterations", "")])
                            self.HighResTrack = self.__class__.HighResTrack(service, rules, path + [("HighResTrack", "")])
                            super().__init__(service, rules, path)

                        class StepLengthFactor(PyMenu):
                            """
                            Parameter StepLengthFactor of value type int.
                            """
                            pass

                        class StepLengthScale(PyMenu):
                            """
                            Parameter StepLengthScale of value type float.
                            """
                            pass

                        class MaxStepNumber(PyMenu):
                            """
                            Parameter MaxStepNumber of value type int.
                            """
                            pass

                        class UseStepLengthScale(PyMenu):
                            """
                            Parameter UseStepLengthScale of value type bool.
                            """
                            pass

                        class NumIterations(PyMenu):
                            """
                            Parameter NumIterations of value type int.
                            """
                            pass

                        class HighResTrack(PyMenu):
                            """
                            Parameter HighResTrack of value type bool.
                            """
                            pass

                    class DropletOutputSolution(PyMenu):
                        """
                        Singleton DropletOutputSolution.
                        """
                        def __init__(self, service, rules, path):
                            self.Filename = self.__class__.Filename(service, rules, path + [("Filename", "")])
                            self.Loaded = self.__class__.Loaded(service, rules, path + [("Loaded", "")])
                            super().__init__(service, rules, path)

                        class Filename(PyMenu):
                            """
                            Parameter Filename of value type str.
                            """
                            pass

                        class Loaded(PyMenu):
                            """
                            Parameter Loaded of value type bool.
                            """
                            pass

                    class CrystalOutputSolution(PyMenu):
                        """
                        Singleton CrystalOutputSolution.
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

                    class Solver(PyMenu):
                        """
                        Singleton Solver.
                        """
                        def __init__(self, service, rules, path):
                            self.CFL = self.__class__.CFL(service, rules, path + [("CFL", "")])
                            self.ResidualCutoff = self.__class__.ResidualCutoff(service, rules, path + [("ResidualCutoff", "")])
                            self.AVCoefficient = self.__class__.AVCoefficient(service, rules, path + [("AVCoefficient", "")])
                            self.ConvergenceBeta = self.__class__.ConvergenceBeta(service, rules, path + [("ConvergenceBeta", "")])
                            super().__init__(service, rules, path)

                        class CFL(PyMenu):
                            """
                            Parameter CFL of value type float.
                            """
                            pass

                        class ResidualCutoff(PyMenu):
                            """
                            Parameter ResidualCutoff of value type float.
                            """
                            pass

                        class AVCoefficient(PyMenu):
                            """
                            Parameter AVCoefficient of value type float.
                            """
                            pass

                        class ConvergenceBeta(PyMenu):
                            """
                            Parameter ConvergenceBeta of value type float.
                            """
                            pass

                    class VaporOutputSolution(PyMenu):
                        """
                        Singleton VaporOutputSolution.
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

                    class ConvergenceAvailable(PyMenu):
                        """
                        Parameter ConvergenceAvailable of value type bool.
                        """
                        pass

                    class SolutionAvailable(PyMenu):
                        """
                        Parameter SolutionAvailable of value type bool.
                        """
                        pass

                    class Save(PyCommand):
                        """
                        Save() -> bool
                        """
                        pass

                    class Calculate(PyCommand):
                        """
                        Calculate() -> bool
                        """
                        pass

                    class LoadParticles(PyCommand):
                        """
                        LoadParticles(Filename: str) -> bool
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

                    class SaveDroplets(PyCommand):
                        """
                        SaveDroplets(Filename: str) -> bool
                        """
                        pass

                    class SaveVapor(PyCommand):
                        """
                        SaveVapor(Filename: str) -> bool
                        """
                        pass

                    class SaveAs(PyCommand):
                        """
                        SaveAs() -> bool
                        """
                        pass

                    class SaveCrystals(PyCommand):
                        """
                        SaveCrystals(Filename: str) -> bool
                        """
                        pass

                    class LoadDroplets(PyCommand):
                        """
                        LoadDroplets(Filename: str) -> bool
                        """
                        pass

                    class LoadCrystals(PyCommand):
                        """
                        LoadCrystals(Filename: str) -> bool
                        """
                        pass

                    class Initialize(PyCommand):
                        """
                        Initialize() -> bool
                        """
                        pass

                    class LoadVapor(PyCommand):
                        """
                        LoadVapor(Filename: str) -> bool
                        """
                        pass

                class AirflowRun(PyMenu):
                    """
                    Singleton AirflowRun.
                    """
                    def __init__(self, service, rules, path):
                        self.FluentCFFPost = self.__class__.FluentCFFPost(service, rules, path + [("FluentCFFPost", "")])
                        self.FluentTimeIntegration = self.__class__.FluentTimeIntegration(service, rules, path + [("FluentTimeIntegration", "")])
                        self.FluentInitSettings = self.__class__.FluentInitSettings(service, rules, path + [("FluentInitSettings", "")])
                        self.FensapOutput = self.__class__.FensapOutput(service, rules, path + [("FensapOutput", "")])
                        self.AirflowFENSAPOutputSolution = self.__class__.AirflowFENSAPOutputSolution(service, rules, path + [("AirflowFENSAPOutputSolution", "")])
                        self.FensapTimeIntegration = self.__class__.FensapTimeIntegration(service, rules, path + [("FensapTimeIntegration", "")])
                        self.AirflowInput = self.__class__.AirflowInput(service, rules, path + [("AirflowInput", "")])
                        self.AirflowFluentOutputSolution = self.__class__.AirflowFluentOutputSolution(service, rules, path + [("AirflowFluentOutputSolution", "")])
                        self.ConvergenceAvailable = self.__class__.ConvergenceAvailable(service, rules, path + [("ConvergenceAvailable", "")])
                        self.SolutionAvailable = self.__class__.SolutionAvailable(service, rules, path + [("SolutionAvailable", "")])
                        self.SaveAs = self.__class__.SaveAs(service, rules, "SaveAs", path)
                        self.Initialize = self.__class__.Initialize(service, rules, "Initialize", path)
                        self.Save = self.__class__.Save(service, rules, "Save", path)
                        self.Interrupt = self.__class__.Interrupt(service, rules, "Interrupt", path)
                        self.Calculate = self.__class__.Calculate(service, rules, "Calculate", path)
                        self.Load = self.__class__.Load(service, rules, "Load", path)
                        self.Reset = self.__class__.Reset(service, rules, "Reset", path)
                        super().__init__(service, rules, path)

                    class FluentCFFPost(PyMenu):
                        """
                        Singleton FluentCFFPost.
                        """
                        def __init__(self, service, rules, path):
                            self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                            self.WriteLevel = self.__class__.WriteLevel(service, rules, path + [("WriteLevel", "")])
                            self.WriteMode = self.__class__.WriteMode(service, rules, path + [("WriteMode", "")])
                            self.Fields = self.__class__.Fields(service, rules, path + [("Fields", "")])
                            self.ReadOnly = self.__class__.ReadOnly(service, rules, path + [("ReadOnly", "")])
                            self.ZoneType = self.__class__.ZoneType(service, rules, path + [("ZoneType", "")])
                            super().__init__(service, rules, path)

                        class Surfaces(PyMenu):
                            """
                            Parameter Surfaces of value type List[str].
                            """
                            pass

                        class WriteLevel(PyMenu):
                            """
                            Parameter WriteLevel of value type str.
                            """
                            pass

                        class WriteMode(PyMenu):
                            """
                            Parameter WriteMode of value type str.
                            """
                            pass

                        class Fields(PyMenu):
                            """
                            Parameter Fields of value type List[str].
                            """
                            pass

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

                    class FluentTimeIntegration(PyMenu):
                        """
                        Singleton FluentTimeIntegration.
                        """
                        def __init__(self, service, rules, path):
                            self.SteeringCourantNumberInitial = self.__class__.SteeringCourantNumberInitial(service, rules, path + [("SteeringCourantNumberInitial", "")])
                            self.TimeTotal = self.__class__.TimeTotal(service, rules, path + [("TimeTotal", "")])
                            self.SteeringRelaxation = self.__class__.SteeringRelaxation(service, rules, path + [("SteeringRelaxation", "")])
                            self.TimeOrder = self.__class__.TimeOrder(service, rules, path + [("TimeOrder", "")])
                            self.TimeStep = self.__class__.TimeStep(service, rules, path + [("TimeStep", "")])
                            self.TimeScaleFactor = self.__class__.TimeScaleFactor(service, rules, path + [("TimeScaleFactor", "")])
                            self.SolutionControl = self.__class__.SolutionControl(service, rules, path + [("SolutionControl", "")])
                            self.SteeringBlending = self.__class__.SteeringBlending(service, rules, path + [("SteeringBlending", "")])
                            self.NumIterations = self.__class__.NumIterations(service, rules, path + [("NumIterations", "")])
                            self.SteeringCourantNumberMax = self.__class__.SteeringCourantNumberMax(service, rules, path + [("SteeringCourantNumberMax", "")])
                            self.CourantNumber = self.__class__.CourantNumber(service, rules, path + [("CourantNumber", "")])
                            super().__init__(service, rules, path)

                        class SteeringCourantNumberInitial(PyMenu):
                            """
                            Parameter SteeringCourantNumberInitial of value type float.
                            """
                            pass

                        class TimeTotal(PyMenu):
                            """
                            Parameter TimeTotal of value type float.
                            """
                            pass

                        class SteeringRelaxation(PyMenu):
                            """
                            Parameter SteeringRelaxation of value type float.
                            """
                            pass

                        class TimeOrder(PyMenu):
                            """
                            Parameter TimeOrder of value type str.
                            """
                            pass

                        class TimeStep(PyMenu):
                            """
                            Parameter TimeStep of value type float.
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

                        class SteeringBlending(PyMenu):
                            """
                            Parameter SteeringBlending of value type float.
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

                        class CourantNumber(PyMenu):
                            """
                            Parameter CourantNumber of value type float.
                            """
                            pass

                    class FluentInitSettings(PyMenu):
                        """
                        Singleton FluentInitSettings.
                        """
                        def __init__(self, service, rules, path):
                            self.InitialVelocityY = self.__class__.InitialVelocityY(service, rules, path + [("InitialVelocityY", "")])
                            self.InitialTurbIntensity = self.__class__.InitialTurbIntensity(service, rules, path + [("InitialTurbIntensity", "")])
                            self.StandardInitSync = self.__class__.StandardInitSync(service, rules, path + [("StandardInitSync", "")])
                            self.Boundaries = self.__class__.Boundaries(service, rules, path + [("Boundaries", "")])
                            self.InitialVelocityX = self.__class__.InitialVelocityX(service, rules, path + [("InitialVelocityX", "")])
                            self.InitializationMethod = self.__class__.InitializationMethod(service, rules, path + [("InitializationMethod", "")])
                            self.InitialVelocityZ = self.__class__.InitialVelocityZ(service, rules, path + [("InitialVelocityZ", "")])
                            self.InitialTemperature = self.__class__.InitialTemperature(service, rules, path + [("InitialTemperature", "")])
                            self.FMGCourantNumber = self.__class__.FMGCourantNumber(service, rules, path + [("FMGCourantNumber", "")])
                            self.InitialPressure = self.__class__.InitialPressure(service, rules, path + [("InitialPressure", "")])
                            self.InitialTurbViscRatio = self.__class__.InitialTurbViscRatio(service, rules, path + [("InitialTurbViscRatio", "")])
                            super().__init__(service, rules, path)

                        class InitialVelocityY(PyMenu):
                            """
                            Parameter InitialVelocityY of value type float.
                            """
                            pass

                        class InitialTurbIntensity(PyMenu):
                            """
                            Parameter InitialTurbIntensity of value type float.
                            """
                            pass

                        class StandardInitSync(PyMenu):
                            """
                            Parameter StandardInitSync of value type str.
                            """
                            pass

                        class Boundaries(PyMenu):
                            """
                            Parameter Boundaries of value type List[str].
                            """
                            pass

                        class InitialVelocityX(PyMenu):
                            """
                            Parameter InitialVelocityX of value type float.
                            """
                            pass

                        class InitializationMethod(PyMenu):
                            """
                            Parameter InitializationMethod of value type str.
                            """
                            pass

                        class InitialVelocityZ(PyMenu):
                            """
                            Parameter InitialVelocityZ of value type float.
                            """
                            pass

                        class InitialTemperature(PyMenu):
                            """
                            Parameter InitialTemperature of value type float.
                            """
                            pass

                        class FMGCourantNumber(PyMenu):
                            """
                            Parameter FMGCourantNumber of value type float.
                            """
                            pass

                        class InitialPressure(PyMenu):
                            """
                            Parameter InitialPressure of value type float.
                            """
                            pass

                        class InitialTurbViscRatio(PyMenu):
                            """
                            Parameter InitialTurbViscRatio of value type float.
                            """
                            pass

                    class FensapOutput(PyMenu):
                        """
                        Singleton FensapOutput.
                        """
                        def __init__(self, service, rules, path):
                            self.MomentY = self.__class__.MomentY(service, rules, path + [("MomentY", "")])
                            self.RefArea = self.__class__.RefArea(service, rules, path + [("RefArea", "")])
                            self.DragY = self.__class__.DragY(service, rules, path + [("DragY", "")])
                            self.MomentX = self.__class__.MomentX(service, rules, path + [("MomentX", "")])
                            self.MomentZ = self.__class__.MomentZ(service, rules, path + [("MomentZ", "")])
                            self.SaveDelay = self.__class__.SaveDelay(service, rules, path + [("SaveDelay", "")])
                            self.MonitorH = self.__class__.MonitorH(service, rules, path + [("MonitorH", "")])
                            self.FensapOutputForces = self.__class__.FensapOutputForces(service, rules, path + [("FensapOutputForces", "")])
                            self.NumberedOutput = self.__class__.NumberedOutput(service, rules, path + [("NumberedOutput", "")])
                            self.LiftAxis = self.__class__.LiftAxis(service, rules, path + [("LiftAxis", "")])
                            self.DragZ = self.__class__.DragZ(service, rules, path + [("DragZ", "")])
                            self.MonitorTotalHeat = self.__class__.MonitorTotalHeat(service, rules, path + [("MonitorTotalHeat", "")])
                            self.FensapOutputEID = self.__class__.FensapOutputEID(service, rules, path + [("FensapOutputEID", "")])
                            self.MonitorMass = self.__class__.MonitorMass(service, rules, path + [("MonitorMass", "")])
                            self.DragX = self.__class__.DragX(service, rules, path + [("DragX", "")])
                            super().__init__(service, rules, path)

                        class MomentY(PyMenu):
                            """
                            Parameter MomentY of value type float.
                            """
                            pass

                        class RefArea(PyMenu):
                            """
                            Parameter RefArea of value type float.
                            """
                            pass

                        class DragY(PyMenu):
                            """
                            Parameter DragY of value type float.
                            """
                            pass

                        class MomentX(PyMenu):
                            """
                            Parameter MomentX of value type float.
                            """
                            pass

                        class MomentZ(PyMenu):
                            """
                            Parameter MomentZ of value type float.
                            """
                            pass

                        class SaveDelay(PyMenu):
                            """
                            Parameter SaveDelay of value type int.
                            """
                            pass

                        class MonitorH(PyMenu):
                            """
                            Parameter MonitorH of value type bool.
                            """
                            pass

                        class FensapOutputForces(PyMenu):
                            """
                            Parameter FensapOutputForces of value type str.
                            """
                            pass

                        class NumberedOutput(PyMenu):
                            """
                            Parameter NumberedOutput of value type bool.
                            """
                            pass

                        class LiftAxis(PyMenu):
                            """
                            Parameter LiftAxis of value type str.
                            """
                            pass

                        class DragZ(PyMenu):
                            """
                            Parameter DragZ of value type float.
                            """
                            pass

                        class MonitorTotalHeat(PyMenu):
                            """
                            Parameter MonitorTotalHeat of value type bool.
                            """
                            pass

                        class FensapOutputEID(PyMenu):
                            """
                            Parameter FensapOutputEID of value type bool.
                            """
                            pass

                        class MonitorMass(PyMenu):
                            """
                            Parameter MonitorMass of value type bool.
                            """
                            pass

                        class DragX(PyMenu):
                            """
                            Parameter DragX of value type float.
                            """
                            pass

                    class AirflowFENSAPOutputSolution(PyMenu):
                        """
                        Singleton AirflowFENSAPOutputSolution.
                        """
                        def __init__(self, service, rules, path):
                            self.HasShear = self.__class__.HasShear(service, rules, path + [("HasShear", "")])
                            self.HasHFlux = self.__class__.HasHFlux(service, rules, path + [("HasHFlux", "")])
                            self.Loaded = self.__class__.Loaded(service, rules, path + [("Loaded", "")])
                            self.Filename = self.__class__.Filename(service, rules, path + [("Filename", "")])
                            super().__init__(service, rules, path)

                        class HasShear(PyMenu):
                            """
                            Parameter HasShear of value type bool.
                            """
                            pass

                        class HasHFlux(PyMenu):
                            """
                            Parameter HasHFlux of value type bool.
                            """
                            pass

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

                    class FensapTimeIntegration(PyMenu):
                        """
                        Singleton FensapTimeIntegration.
                        """
                        def __init__(self, service, rules, path):
                            self.NumIterations = self.__class__.NumIterations(service, rules, path + [("NumIterations", "")])
                            self.RlxIter = self.__class__.RlxIter(service, rules, path + [("RlxIter", "")])
                            self.CFL = self.__class__.CFL(service, rules, path + [("CFL", "")])
                            self.TimeOrder = self.__class__.TimeOrder(service, rules, path + [("TimeOrder", "")])
                            self.VariableRelaxation = self.__class__.VariableRelaxation(service, rules, path + [("VariableRelaxation", "")])
                            self.TimeTotal = self.__class__.TimeTotal(service, rules, path + [("TimeTotal", "")])
                            self.TimeStep = self.__class__.TimeStep(service, rules, path + [("TimeStep", "")])
                            super().__init__(service, rules, path)

                        class NumIterations(PyMenu):
                            """
                            Parameter NumIterations of value type int.
                            """
                            pass

                        class RlxIter(PyMenu):
                            """
                            Parameter RlxIter of value type int.
                            """
                            pass

                        class CFL(PyMenu):
                            """
                            Parameter CFL of value type float.
                            """
                            pass

                        class TimeOrder(PyMenu):
                            """
                            Parameter TimeOrder of value type str.
                            """
                            pass

                        class VariableRelaxation(PyMenu):
                            """
                            Parameter VariableRelaxation of value type bool.
                            """
                            pass

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

                    class AirflowInput(PyMenu):
                        """
                        Singleton AirflowInput.
                        """
                        def __init__(self, service, rules, path):
                            self.RoughnessInput = self.__class__.RoughnessInput(service, rules, path + [("RoughnessInput", "")])
                            super().__init__(service, rules, path)

                        class RoughnessInput(PyMenu):
                            """
                            Parameter RoughnessInput of value type bool.
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

                    class ConvergenceAvailable(PyMenu):
                        """
                        Parameter ConvergenceAvailable of value type bool.
                        """
                        pass

                    class SolutionAvailable(PyMenu):
                        """
                        Parameter SolutionAvailable of value type bool.
                        """
                        pass

                    class SaveAs(PyCommand):
                        """
                        SaveAs(Filename: str) -> bool
                        """
                        pass

                    class Initialize(PyCommand):
                        """
                        Initialize() -> bool
                        """
                        pass

                    class Save(PyCommand):
                        """
                        Save(Filename: str) -> bool
                        """
                        pass

                    class Interrupt(PyCommand):
                        """
                        Interrupt() -> bool
                        """
                        pass

                    class Calculate(PyCommand):
                        """
                        Calculate() -> bool
                        """
                        pass

                    class Load(PyCommand):
                        """
                        Load(Filename: str) -> bool
                        """
                        pass

                    class Reset(PyCommand):
                        """
                        Reset() -> bool
                        """
                        pass

                class IceRun(PyMenu):
                    """
                    Singleton IceRun.
                    """
                    def __init__(self, service, rules, path):
                        self.DisplacementOutputSolution = self.__class__.DisplacementOutputSolution(service, rules, path + [("DisplacementOutputSolution", "")])
                        self.IceOutputSolution = self.__class__.IceOutputSolution(service, rules, path + [("IceOutputSolution", "")])
                        self.IceTime = self.__class__.IceTime(service, rules, path + [("IceTime", "")])
                        self.IceOutput = self.__class__.IceOutput(service, rules, path + [("IceOutput", "")])
                        self.IceRemeshing = self.__class__.IceRemeshing(service, rules, path + [("IceRemeshing", "")])
                        self.IceAdvanced = self.__class__.IceAdvanced(service, rules, path + [("IceAdvanced", "")])
                        self.IceInit = self.__class__.IceInit(service, rules, path + [("IceInit", "")])
                        self.SolutionAvailable = self.__class__.SolutionAvailable(service, rules, path + [("SolutionAvailable", "")])
                        self.SetupRemeshing = self.__class__.SetupRemeshing(service, rules, "SetupRemeshing", path)
                        self.Load = self.__class__.Load(service, rules, "Load", path)
                        self.Calculate = self.__class__.Calculate(service, rules, "Calculate", path)
                        self.SaveAs = self.__class__.SaveAs(service, rules, "SaveAs", path)
                        self.Reset = self.__class__.Reset(service, rules, "Reset", path)
                        self.Save = self.__class__.Save(service, rules, "Save", path)
                        self.Interrupt = self.__class__.Interrupt(service, rules, "Interrupt", path)
                        self.MeshMorph = self.__class__.MeshMorph(service, rules, "MeshMorph", path)
                        super().__init__(service, rules, path)

                    class DisplacementOutputSolution(PyMenu):
                        """
                        Singleton DisplacementOutputSolution.
                        """
                        def __init__(self, service, rules, path):
                            self.Loaded = self.__class__.Loaded(service, rules, path + [("Loaded", "")])
                            super().__init__(service, rules, path)

                        class Loaded(PyMenu):
                            """
                            Parameter Loaded of value type bool.
                            """
                            pass

                    class IceOutputSolution(PyMenu):
                        """
                        Singleton IceOutputSolution.
                        """
                        def __init__(self, service, rules, path):
                            self.Roughness = self.__class__.Roughness(service, rules, path + [("Roughness", "")])
                            self.Filename = self.__class__.Filename(service, rules, path + [("Filename", "")])
                            self.Loaded = self.__class__.Loaded(service, rules, path + [("Loaded", "")])
                            super().__init__(service, rules, path)

                        class Roughness(PyMenu):
                            """
                            Parameter Roughness of value type bool.
                            """
                            pass

                        class Filename(PyMenu):
                            """
                            Parameter Filename of value type str.
                            """
                            pass

                        class Loaded(PyMenu):
                            """
                            Parameter Loaded of value type bool.
                            """
                            pass

                    class IceTime(PyMenu):
                        """
                        Singleton IceTime.
                        """
                        def __init__(self, service, rules, path):
                            self.TimeStep = self.__class__.TimeStep(service, rules, path + [("TimeStep", "")])
                            self.AutoTimeStep = self.__class__.AutoTimeStep(service, rules, path + [("AutoTimeStep", "")])
                            self.TotalTime = self.__class__.TotalTime(service, rules, path + [("TotalTime", "")])
                            super().__init__(service, rules, path)

                        class TimeStep(PyMenu):
                            """
                            Parameter TimeStep of value type float.
                            """
                            pass

                        class AutoTimeStep(PyMenu):
                            """
                            Parameter AutoTimeStep of value type bool.
                            """
                            pass

                        class TotalTime(PyMenu):
                            """
                            Parameter TotalTime of value type float.
                            """
                            pass

                    class IceOutput(PyMenu):
                        """
                        Singleton IceOutput.
                        """
                        def __init__(self, service, rules, path):
                            self.RemeshingMode = self.__class__.RemeshingMode(service, rules, path + [("RemeshingMode", "")])
                            self.MeshingMemoryOptim = self.__class__.MeshingMemoryOptim(service, rules, path + [("MeshingMemoryOptim", "")])
                            self.RemeshingSetup = self.__class__.RemeshingSetup(service, rules, path + [("RemeshingSetup", "")])
                            self.HybridRemeshing = self.__class__.HybridRemeshing(service, rules, path + [("HybridRemeshing", "")])
                            self.RemeshingDelay = self.__class__.RemeshingDelay(service, rules, path + [("RemeshingDelay", "")])
                            super().__init__(service, rules, path)

                        class RemeshingMode(PyMenu):
                            """
                            Parameter RemeshingMode of value type str.
                            """
                            pass

                        class MeshingMemoryOptim(PyMenu):
                            """
                            Parameter MeshingMemoryOptim of value type bool.
                            """
                            pass

                        class RemeshingSetup(PyMenu):
                            """
                            Parameter RemeshingSetup of value type bool.
                            """
                            pass

                        class HybridRemeshing(PyMenu):
                            """
                            Parameter HybridRemeshing of value type bool.
                            """
                            pass

                        class RemeshingDelay(PyMenu):
                            """
                            Parameter RemeshingDelay of value type int.
                            """
                            pass

                    class IceRemeshing(PyMenu):
                        """
                        Singleton IceRemeshing.
                        """
                        def __init__(self, service, rules, path):
                            self.GlobGrowthRate = self.__class__.GlobGrowthRate(service, rules, path + [("GlobGrowthRate", "")])
                            self.RotPeriodicAngle = self.__class__.RotPeriodicAngle(service, rules, path + [("RotPeriodicAngle", "")])
                            self.GlobMaxGeoMinSpan3D = self.__class__.GlobMaxGeoMinSpan3D(service, rules, path + [("GlobMaxGeoMinSpan3D", "")])
                            self.CurvNormalAngle = self.__class__.CurvNormalAngle(service, rules, path + [("CurvNormalAngle", "")])
                            self.Dimension = self.__class__.Dimension(service, rules, path + [("Dimension", "")])
                            self.ProxGrowthRate = self.__class__.ProxGrowthRate(service, rules, path + [("ProxGrowthRate", "")])
                            self.ZSpan = self.__class__.ZSpan(service, rules, path + [("ZSpan", "")])
                            self.RotPeriodicAxis = self.__class__.RotPeriodicAxis(service, rules, path + [("RotPeriodicAxis", "")])
                            self.TransPeriodicZones = self.__class__.TransPeriodicZones(service, rules, path + [("TransPeriodicZones", "")])
                            self.PrismFirstCellAR = self.__class__.PrismFirstCellAR(service, rules, path + [("PrismFirstCellAR", "")])
                            self.GlobRange = self.__class__.GlobRange(service, rules, path + [("GlobRange", "")])
                            self.CurvRange = self.__class__.CurvRange(service, rules, path + [("CurvRange", "")])
                            self.RotPeriodicCenter = self.__class__.RotPeriodicCenter(service, rules, path + [("RotPeriodicCenter", "")])
                            self.WrapResolutionFactor = self.__class__.WrapResolutionFactor(service, rules, path + [("WrapResolutionFactor", "")])
                            self.PrismNLayers = self.__class__.PrismNLayers(service, rules, path + [("PrismNLayers", "")])
                            self.TransPeriodic = self.__class__.TransPeriodic(service, rules, path + [("TransPeriodic", "")])
                            self.Advanced = self.__class__.Advanced(service, rules, path + [("Advanced", "")])
                            self.CellSizingGrowthRate = self.__class__.CellSizingGrowthRate(service, rules, path + [("CellSizingGrowthRate", "")])
                            self.CellSizingType = self.__class__.CellSizingType(service, rules, path + [("CellSizingType", "")])
                            self.RotPeriodicZones = self.__class__.RotPeriodicZones(service, rules, path + [("RotPeriodicZones", "")])
                            self.ProxNCellGap = self.__class__.ProxNCellGap(service, rules, path + [("ProxNCellGap", "")])
                            self.TranslationalPeriodic = self.__class__.TranslationalPeriodic(service, rules, path + [("TranslationalPeriodic", "")])
                            self.MaterialPoint = self.__class__.MaterialPoint(service, rules, path + [("MaterialPoint", "")])
                            self.RotationalPeriodic = self.__class__.RotationalPeriodic(service, rules, path + [("RotationalPeriodic", "")])
                            self.CurvGrowthRate = self.__class__.CurvGrowthRate(service, rules, path + [("CurvGrowthRate", "")])
                            self.PrismGrowthRate = self.__class__.PrismGrowthRate(service, rules, path + [("PrismGrowthRate", "")])
                            self.ProxMin = self.__class__.ProxMin(service, rules, path + [("ProxMin", "")])
                            super().__init__(service, rules, path)

                        class GlobGrowthRate(PyMenu):
                            """
                            Parameter GlobGrowthRate of value type float.
                            """
                            pass

                        class RotPeriodicAngle(PyMenu):
                            """
                            Parameter RotPeriodicAngle of value type float.
                            """
                            pass

                        class GlobMaxGeoMinSpan3D(PyMenu):
                            """
                            Parameter GlobMaxGeoMinSpan3D of value type float.
                            """
                            pass

                        class CurvNormalAngle(PyMenu):
                            """
                            Parameter CurvNormalAngle of value type float.
                            """
                            pass

                        class Dimension(PyMenu):
                            """
                            Parameter Dimension of value type str.
                            """
                            pass

                        class ProxGrowthRate(PyMenu):
                            """
                            Parameter ProxGrowthRate of value type float.
                            """
                            pass

                        class ZSpan(PyMenu):
                            """
                            Parameter ZSpan of value type float.
                            """
                            pass

                        class RotPeriodicAxis(PyMenu):
                            """
                            Parameter RotPeriodicAxis of value type List[float].
                            """
                            pass

                        class TransPeriodicZones(PyMenu):
                            """
                            Parameter TransPeriodicZones of value type str.
                            """
                            pass

                        class PrismFirstCellAR(PyMenu):
                            """
                            Parameter PrismFirstCellAR of value type float.
                            """
                            pass

                        class GlobRange(PyMenu):
                            """
                            Parameter GlobRange of value type List[float].
                            """
                            pass

                        class CurvRange(PyMenu):
                            """
                            Parameter CurvRange of value type List[float].
                            """
                            pass

                        class RotPeriodicCenter(PyMenu):
                            """
                            Parameter RotPeriodicCenter of value type List[float].
                            """
                            pass

                        class WrapResolutionFactor(PyMenu):
                            """
                            Parameter WrapResolutionFactor of value type float.
                            """
                            pass

                        class PrismNLayers(PyMenu):
                            """
                            Parameter PrismNLayers of value type int.
                            """
                            pass

                        class TransPeriodic(PyMenu):
                            """
                            Parameter TransPeriodic of value type List[float].
                            """
                            pass

                        class Advanced(PyMenu):
                            """
                            Parameter Advanced of value type bool.
                            """
                            pass

                        class CellSizingGrowthRate(PyMenu):
                            """
                            Parameter CellSizingGrowthRate of value type float.
                            """
                            pass

                        class CellSizingType(PyMenu):
                            """
                            Parameter CellSizingType of value type str.
                            """
                            pass

                        class RotPeriodicZones(PyMenu):
                            """
                            Parameter RotPeriodicZones of value type str.
                            """
                            pass

                        class ProxNCellGap(PyMenu):
                            """
                            Parameter ProxNCellGap of value type int.
                            """
                            pass

                        class TranslationalPeriodic(PyMenu):
                            """
                            Parameter TranslationalPeriodic of value type bool.
                            """
                            pass

                        class MaterialPoint(PyMenu):
                            """
                            Parameter MaterialPoint of value type List[float].
                            """
                            pass

                        class RotationalPeriodic(PyMenu):
                            """
                            Parameter RotationalPeriodic of value type bool.
                            """
                            pass

                        class CurvGrowthRate(PyMenu):
                            """
                            Parameter CurvGrowthRate of value type float.
                            """
                            pass

                        class PrismGrowthRate(PyMenu):
                            """
                            Parameter PrismGrowthRate of value type float.
                            """
                            pass

                        class ProxMin(PyMenu):
                            """
                            Parameter ProxMin of value type float.
                            """
                            pass

                    class IceAdvanced(PyMenu):
                        """
                        Singleton IceAdvanced.
                        """
                        def __init__(self, service, rules, path):
                            self.EIDDisable = self.__class__.EIDDisable(service, rules, path + [("EIDDisable", "")])
                            super().__init__(service, rules, path)

                        class EIDDisable(PyMenu):
                            """
                            Parameter EIDDisable of value type bool.
                            """
                            pass

                    class IceInit(PyMenu):
                        """
                        Singleton IceInit.
                        """
                        def __init__(self, service, rules, path):
                            self.Restart = self.__class__.Restart(service, rules, path + [("Restart", "")])
                            super().__init__(service, rules, path)

                        class Restart(PyMenu):
                            """
                            Parameter Restart of value type bool.
                            """
                            pass

                    class SolutionAvailable(PyMenu):
                        """
                        Parameter SolutionAvailable of value type bool.
                        """
                        pass

                    class SetupRemeshing(PyCommand):
                        """
                        SetupRemeshing(Filename: str) -> bool
                        """
                        pass

                    class Load(PyCommand):
                        """
                        Load(Filename: str) -> bool
                        """
                        pass

                    class Calculate(PyCommand):
                        """
                        Calculate() -> bool
                        """
                        pass

                    class SaveAs(PyCommand):
                        """
                        SaveAs(Filename: str) -> bool
                        """
                        pass

                    class Reset(PyCommand):
                        """
                        Reset() -> bool
                        """
                        pass

                    class Save(PyCommand):
                        """
                        Save(Filename: str) -> bool
                        """
                        pass

                    class Interrupt(PyCommand):
                        """
                        Interrupt() -> bool
                        """
                        pass

                    class MeshMorph(PyCommand):
                        """
                        MeshMorph() -> bool
                        """
                        pass

                class CHT(PyMenu):
                    """
                    Singleton CHT.
                    """
                    def __init__(self, service, rules, path):
                        self.CHTOutputSolution = self.__class__.CHTOutputSolution(service, rules, path + [("CHTOutputSolution", "")])
                        self.CHTWalls = self.__class__.CHTWalls(service, rules, path + [("CHTWalls", "")])
                        self.SolutionAvailable = self.__class__.SolutionAvailable(service, rules, path + [("SolutionAvailable", "")])
                        self.SaveInterval = self.__class__.SaveInterval(service, rules, path + [("SaveInterval", "")])
                        self.SolverIterations = self.__class__.SolverIterations(service, rules, path + [("SolverIterations", "")])
                        self.NumberLoops = self.__class__.NumberLoops(service, rules, path + [("NumberLoops", "")])
                        self.CalculateICE = self.__class__.CalculateICE(service, rules, "CalculateICE", path)
                        self.Interrupt = self.__class__.Interrupt(service, rules, "Interrupt", path)
                        self.Calculate = self.__class__.Calculate(service, rules, "Calculate", path)
                        self.Load = self.__class__.Load(service, rules, "Load", path)
                        self.Reset = self.__class__.Reset(service, rules, "Reset", path)
                        super().__init__(service, rules, path)

                    class CHTOutputSolution(PyMenu):
                        """
                        Singleton CHTOutputSolution.
                        """
                        def __init__(self, service, rules, path):
                            self.Loaded = self.__class__.Loaded(service, rules, path + [("Loaded", "")])
                            super().__init__(service, rules, path)

                        class Loaded(PyMenu):
                            """
                            Parameter Loaded of value type bool.
                            """
                            pass

                    class CHTWalls(PyMenu):
                        """
                        Parameter CHTWalls of value type List[str].
                        """
                        pass

                    class SolutionAvailable(PyMenu):
                        """
                        Parameter SolutionAvailable of value type bool.
                        """
                        pass

                    class SaveInterval(PyMenu):
                        """
                        Parameter SaveInterval of value type int.
                        """
                        pass

                    class SolverIterations(PyMenu):
                        """
                        Parameter SolverIterations of value type int.
                        """
                        pass

                    class NumberLoops(PyMenu):
                        """
                        Parameter NumberLoops of value type int.
                        """
                        pass

                    class CalculateICE(PyCommand):
                        """
                        CalculateICE() -> bool
                        """
                        pass

                    class Interrupt(PyCommand):
                        """
                        Interrupt() -> bool
                        """
                        pass

                    class Calculate(PyCommand):
                        """
                        Calculate() -> bool
                        """
                        pass

                    class Load(PyCommand):
                        """
                        Load(Filename: str) -> bool
                        """
                        pass

                    class Reset(PyCommand):
                        """
                        Reset() -> bool
                        """
                        pass

                class AdaptationRun(PyMenu):
                    """
                    Singleton AdaptationRun.
                    """
                    def __init__(self, service, rules, path):
                        self.OutputCase = self.__class__.OutputCase(service, rules, path + [("OutputCase", "")])
                        self.Target = self.__class__.Target(service, rules, path + [("Target", "")])
                        self.Options = self.__class__.Options(service, rules, path + [("Options", "")])
                        self.State = self.__class__.State(service, rules, path + [("State", "")])
                        self.Operations = self.__class__.Operations(service, rules, path + [("Operations", "")])
                        self.ViewMesh = self.__class__.ViewMesh(service, rules, "ViewMesh", path)
                        self.ComputeCarpet = self.__class__.ComputeCarpet(service, rules, "ComputeCarpet", path)
                        self.UpdateMesh = self.__class__.UpdateMesh(service, rules, "UpdateMesh", path)
                        self.RunOG = self.__class__.RunOG(service, rules, "RunOG", path)
                        self.Interrupt = self.__class__.Interrupt(service, rules, "Interrupt", path)
                        self.Reset = self.__class__.Reset(service, rules, "Reset", path)
                        super().__init__(service, rules, path)

                    class OutputCase(PyMenu):
                        """
                        Singleton OutputCase.
                        """
                        def __init__(self, service, rules, path):
                            self.Filename = self.__class__.Filename(service, rules, path + [("Filename", "")])
                            self.FilenameIp = self.__class__.FilenameIp(service, rules, path + [("FilenameIp", "")])
                            self.FilenameDat = self.__class__.FilenameDat(service, rules, path + [("FilenameDat", "")])
                            super().__init__(service, rules, path)

                        class Filename(PyMenu):
                            """
                            Parameter Filename of value type str.
                            """
                            pass

                        class FilenameIp(PyMenu):
                            """
                            Parameter FilenameIp of value type str.
                            """
                            pass

                        class FilenameDat(PyMenu):
                            """
                            Parameter FilenameDat of value type str.
                            """
                            pass

                    class Target(PyMenu):
                        """
                        Singleton Target.
                        """
                        def __init__(self, service, rules, path):
                            self.NumNodesChange = self.__class__.NumNodesChange(service, rules, path + [("NumNodesChange", "")])
                            self.NumCellsChange = self.__class__.NumCellsChange(service, rules, path + [("NumCellsChange", "")])
                            self.ErrorValue = self.__class__.ErrorValue(service, rules, path + [("ErrorValue", "")])
                            self.NumCellsRef = self.__class__.NumCellsRef(service, rules, path + [("NumCellsRef", "")])
                            self.NumNodesRef = self.__class__.NumNodesRef(service, rules, path + [("NumNodesRef", "")])
                            self.NumCells = self.__class__.NumCells(service, rules, path + [("NumCells", "")])
                            self.NumNodesMax = self.__class__.NumNodesMax(service, rules, path + [("NumNodesMax", "")])
                            self.NumCellsMax = self.__class__.NumCellsMax(service, rules, path + [("NumCellsMax", "")])
                            self.Mode = self.__class__.Mode(service, rules, path + [("Mode", "")])
                            self.NumNodes = self.__class__.NumNodes(service, rules, path + [("NumNodes", "")])
                            super().__init__(service, rules, path)

                        class NumNodesChange(PyMenu):
                            """
                            Parameter NumNodesChange of value type int.
                            """
                            pass

                        class NumCellsChange(PyMenu):
                            """
                            Parameter NumCellsChange of value type int.
                            """
                            pass

                        class ErrorValue(PyMenu):
                            """
                            Parameter ErrorValue of value type float.
                            """
                            pass

                        class NumCellsRef(PyMenu):
                            """
                            Parameter NumCellsRef of value type int.
                            """
                            pass

                        class NumNodesRef(PyMenu):
                            """
                            Parameter NumNodesRef of value type int.
                            """
                            pass

                        class NumCells(PyMenu):
                            """
                            Parameter NumCells of value type int.
                            """
                            pass

                        class NumNodesMax(PyMenu):
                            """
                            Parameter NumNodesMax of value type int.
                            """
                            pass

                        class NumCellsMax(PyMenu):
                            """
                            Parameter NumCellsMax of value type int.
                            """
                            pass

                        class Mode(PyMenu):
                            """
                            Parameter Mode of value type str.
                            """
                            pass

                        class NumNodes(PyMenu):
                            """
                            Parameter NumNodes of value type int.
                            """
                            pass

                    class Options(PyMenu):
                        """
                        Singleton Options.
                        """
                        def __init__(self, service, rules, path):
                            self.NumberCPUs = self.__class__.NumberCPUs(service, rules, path + [("NumberCPUs", "")])
                            self.SpecifyCPUs = self.__class__.SpecifyCPUs(service, rules, path + [("SpecifyCPUs", "")])
                            super().__init__(service, rules, path)

                        class NumberCPUs(PyMenu):
                            """
                            Parameter NumberCPUs of value type int.
                            """
                            pass

                        class SpecifyCPUs(PyMenu):
                            """
                            Parameter SpecifyCPUs of value type bool.
                            """
                            pass

                    class State(PyMenu):
                        """
                        Singleton State.
                        """
                        def __init__(self, service, rules, path):
                            self.MeshAdapted = self.__class__.MeshAdapted(service, rules, path + [("MeshAdapted", "")])
                            super().__init__(service, rules, path)

                        class MeshAdapted(PyMenu):
                            """
                            Parameter MeshAdapted of value type bool.
                            """
                            pass

                    class Operations(PyMenu):
                        """
                        Singleton Operations.
                        """
                        def __init__(self, service, rules, path):
                            self.NMPost = self.__class__.NMPost(service, rules, path + [("NMPost", "")])
                            self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                            self.MainIter = self.__class__.MainIter(service, rules, path + [("MainIter", "")])
                            self.AdaptCurv = self.__class__.AdaptCurv(service, rules, path + [("AdaptCurv", "")])
                            self.AdjustY = self.__class__.AdjustY(service, rules, path + [("AdjustY", "")])
                            self.NMPre = self.__class__.NMPre(service, rules, path + [("NMPre", "")])
                            self.Mode = self.__class__.Mode(service, rules, path + [("Mode", "")])
                            self.ComputeError = self.__class__.ComputeError(service, rules, path + [("ComputeError", "")])
                            self.Swap = self.__class__.Swap(service, rules, path + [("Swap", "")])
                            super().__init__(service, rules, path)

                        class NMPost(PyMenu):
                            """
                            Parameter NMPost of value type int.
                            """
                            pass

                        class Type(PyMenu):
                            """
                            Parameter Type of value type str.
                            """
                            pass

                        class MainIter(PyMenu):
                            """
                            Parameter MainIter of value type int.
                            """
                            pass

                        class AdaptCurv(PyMenu):
                            """
                            Parameter AdaptCurv of value type bool.
                            """
                            pass

                        class AdjustY(PyMenu):
                            """
                            Parameter AdjustY of value type str.
                            """
                            pass

                        class NMPre(PyMenu):
                            """
                            Parameter NMPre of value type int.
                            """
                            pass

                        class Mode(PyMenu):
                            """
                            Parameter Mode of value type str.
                            """
                            pass

                        class ComputeError(PyMenu):
                            """
                            Parameter ComputeError of value type bool.
                            """
                            pass

                        class Swap(PyMenu):
                            """
                            Parameter Swap of value type int.
                            """
                            pass

                    class ViewMesh(PyCommand):
                        """
                        ViewMesh() -> bool
                        """
                        pass

                    class ComputeCarpet(PyCommand):
                        """
                        ComputeCarpet() -> bool
                        """
                        pass

                    class UpdateMesh(PyCommand):
                        """
                        UpdateMesh() -> bool
                        """
                        pass

                    class RunOG(PyCommand):
                        """
                        RunOG() -> bool
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

                class Calculate(PyCommand):
                    """
                    Calculate() -> bool
                    """
                    pass

                class CalculateOG(PyCommand):
                    """
                    CalculateOG() -> bool
                    """
                    pass

                class Interrupt(PyCommand):
                    """
                    Interrupt() -> bool
                    """
                    pass

                class ResetMultishot(PyCommand):
                    """
                    ResetMultishot() -> bool
                    """
                    pass

                class FensapGridSave(PyCommand):
                    """
                    FensapGridSave(Filename: str) -> bool
                    """
                    pass

                class Reset(PyCommand):
                    """
                    Reset() -> bool
                    """
                    pass

                class ConfigureShots(PyCommand):
                    """
                    ConfigureShots() -> bool
                    """
                    pass

            class Ice(PyMenu):
                """
                Singleton Ice.
                """
                def __init__(self, service, rules, path):
                    self.IceConditions = self.__class__.IceConditions(service, rules, path + [("IceConditions", "")])
                    self.Conditions = self.__class__.Conditions(service, rules, path + [("Conditions", "")])
                    self.IceShedding = self.__class__.IceShedding(service, rules, path + [("IceShedding", "")])
                    self.Advanced = self.__class__.Advanced(service, rules, path + [("Advanced", "")])
                    self.IcingModel = self.__class__.IcingModel(service, rules, path + [("IcingModel", "")])
                    self.Crystals = self.__class__.Crystals(service, rules, path + [("Crystals", "")])
                    super().__init__(service, rules, path)

                class IceConditions(PyMenu):
                    """
                    Singleton IceConditions.
                    """
                    def __init__(self, service, rules, path):
                        self.IcingAirTemperatureFlag = self.__class__.IcingAirTemperatureFlag(service, rules, path + [("IcingAirTemperatureFlag", "")])
                        self.IcingAirTemperature = self.__class__.IcingAirTemperature(service, rules, path + [("IcingAirTemperature", "")])
                        self.RelativeHumidity = self.__class__.RelativeHumidity(service, rules, path + [("RelativeHumidity", "")])
                        self.RecoveryFactor = self.__class__.RecoveryFactor(service, rules, path + [("RecoveryFactor", "")])
                        super().__init__(service, rules, path)

                    class IcingAirTemperatureFlag(PyMenu):
                        """
                        Parameter IcingAirTemperatureFlag of value type bool.
                        """
                        pass

                    class IcingAirTemperature(PyMenu):
                        """
                        Parameter IcingAirTemperature of value type float.
                        """
                        pass

                    class RelativeHumidity(PyMenu):
                        """
                        Parameter RelativeHumidity of value type float.
                        """
                        pass

                    class RecoveryFactor(PyMenu):
                        """
                        Parameter RecoveryFactor of value type float.
                        """
                        pass

                class Conditions(PyMenu):
                    """
                    Singleton Conditions.
                    """
                    def __init__(self, service, rules, path):
                        self.IceDensityType = self.__class__.IceDensityType(service, rules, path + [("IceDensityType", "")])
                        self.IceJonesLEDiameter = self.__class__.IceJonesLEDiameter(service, rules, path + [("IceJonesLEDiameter", "")])
                        self.IceEmissivity = self.__class__.IceEmissivity(service, rules, path + [("IceEmissivity", "")])
                        self.IceConstantDensity = self.__class__.IceConstantDensity(service, rules, path + [("IceConstantDensity", "")])
                        super().__init__(service, rules, path)

                    class IceDensityType(PyMenu):
                        """
                        Parameter IceDensityType of value type str.
                        """
                        pass

                    class IceJonesLEDiameter(PyMenu):
                        """
                        Parameter IceJonesLEDiameter of value type float.
                        """
                        pass

                    class IceEmissivity(PyMenu):
                        """
                        Parameter IceEmissivity of value type float.
                        """
                        pass

                    class IceConstantDensity(PyMenu):
                        """
                        Parameter IceConstantDensity of value type float.
                        """
                        pass

                class IceShedding(PyMenu):
                    """
                    Singleton IceShedding.
                    """
                    def __init__(self, service, rules, path):
                        self.SurfaceInterface = self.__class__.SurfaceInterface(service, rules, path + [("SurfaceInterface", "")])
                        self.CritShedMass = self.__class__.CritShedMass(service, rules, path + [("CritShedMass", "")])
                        self.Flag = self.__class__.Flag(service, rules, path + [("Flag", "")])
                        super().__init__(service, rules, path)

                    class SurfaceInterface(PyMenu):
                        """
                        Parameter SurfaceInterface of value type str.
                        """
                        pass

                    class CritShedMass(PyMenu):
                        """
                        Parameter CritShedMass of value type float.
                        """
                        pass

                    class Flag(PyMenu):
                        """
                        Parameter Flag of value type bool.
                        """
                        pass

                class Advanced(PyMenu):
                    """
                    Singleton Advanced.
                    """
                    def __init__(self, service, rules, path):
                        self.SolverParameters = self.__class__.SolverParameters(service, rules, path + [("SolverParameters", "")])
                        super().__init__(service, rules, path)

                    class SolverParameters(PyMenu):
                        """
                        Parameter SolverParameters of value type str.
                        """
                        pass

                class IcingModel(PyMenu):
                    """
                    Singleton IcingModel.
                    """
                    def __init__(self, service, rules, path):
                        self.Model = self.__class__.Model(service, rules, path + [("Model", "")])
                        self.HeatFlux = self.__class__.HeatFlux(service, rules, path + [("HeatFlux", "")])
                        self.Beading = self.__class__.Beading(service, rules, path + [("Beading", "")])
                        super().__init__(service, rules, path)

                    class Model(PyMenu):
                        """
                        Parameter Model of value type str.
                        """
                        pass

                    class HeatFlux(PyMenu):
                        """
                        Parameter HeatFlux of value type str.
                        """
                        pass

                    class Beading(PyMenu):
                        """
                        Parameter Beading of value type bool.
                        """
                        pass

                class Crystals(PyMenu):
                    """
                    Singleton Crystals.
                    """
                    def __init__(self, service, rules, path):
                        self.Erosion = self.__class__.Erosion(service, rules, path + [("Erosion", "")])
                        self.BouncingModel = self.__class__.BouncingModel(service, rules, path + [("BouncingModel", "")])
                        super().__init__(service, rules, path)

                    class Erosion(PyMenu):
                        """
                        Parameter Erosion of value type bool.
                        """
                        pass

                    class BouncingModel(PyMenu):
                        """
                        Parameter BouncingModel of value type str.
                        """
                        pass

            class RunType(PyMenu):
                """
                Singleton RunType.
                """
                def __init__(self, service, rules, path):
                    self.Ice = self.__class__.Ice(service, rules, path + [("Ice", "")])
                    self.CHT = self.__class__.CHT(service, rules, path + [("CHT", "")])
                    self.Airflow = self.__class__.Airflow(service, rules, path + [("Airflow", "")])
                    self.Particles = self.__class__.Particles(service, rules, path + [("Particles", "")])
                    self.Adapt = self.__class__.Adapt(service, rules, path + [("Adapt", "")])
                    super().__init__(service, rules, path)

                class Ice(PyMenu):
                    """
                    Parameter Ice of value type bool.
                    """
                    pass

                class CHT(PyMenu):
                    """
                    Parameter CHT of value type bool.
                    """
                    pass

                class Airflow(PyMenu):
                    """
                    Parameter Airflow of value type bool.
                    """
                    pass

                class Particles(PyMenu):
                    """
                    Parameter Particles of value type bool.
                    """
                    pass

                class Adapt(PyMenu):
                    """
                    Parameter Adapt of value type bool.
                    """
                    pass

            class Adaptation(PyMenu):
                """
                Singleton Adaptation.
                """
                def __init__(self, service, rules, path):
                    self.State = self.__class__.State(service, rules, path + [("State", "")])
                    self.Constraints = self.__class__.Constraints(service, rules, path + [("Constraints", "")])
                    self.Input = self.__class__.Input(service, rules, path + [("Input", "")])
                    self.Boundaries = self.__class__.Boundaries(service, rules, path + [("Boundaries", "")])
                    self.GenerateCAD = self.__class__.GenerateCAD(service, rules, "GenerateCAD", path)
                    self.EditCAD = self.__class__.EditCAD(service, rules, "EditCAD", path)
                    self.ResetCAD = self.__class__.ResetCAD(service, rules, "ResetCAD", path)
                    super().__init__(service, rules, path)

                class State(PyMenu):
                    """
                    Singleton State.
                    """
                    def __init__(self, service, rules, path):
                        self.CADLoaded = self.__class__.CADLoaded(service, rules, path + [("CADLoaded", "")])
                        super().__init__(service, rules, path)

                    class CADLoaded(PyMenu):
                        """
                        Parameter CADLoaded of value type bool.
                        """
                        pass

                class Constraints(PyMenu):
                    """
                    Singleton Constraints.
                    """
                    def __init__(self, service, rules, path):
                        self.Mode = self.__class__.Mode(service, rules, path + [("Mode", "")])
                        self.HasPrism = self.__class__.HasPrism(service, rules, path + [("HasPrism", "")])
                        self.PrismWarpage = self.__class__.PrismWarpage(service, rules, path + [("PrismWarpage", "")])
                        self.HexaWarpage = self.__class__.HexaWarpage(service, rules, path + [("HexaWarpage", "")])
                        self.FaceAngle = self.__class__.FaceAngle(service, rules, path + [("FaceAngle", "")])
                        self.PrismAspectRatio = self.__class__.PrismAspectRatio(service, rules, path + [("PrismAspectRatio", "")])
                        self.MaxEdgeRef = self.__class__.MaxEdgeRef(service, rules, path + [("MaxEdgeRef", "")])
                        self.DegAnisotropy = self.__class__.DegAnisotropy(service, rules, path + [("DegAnisotropy", "")])
                        self.TetraAspectRatio = self.__class__.TetraAspectRatio(service, rules, path + [("TetraAspectRatio", "")])
                        self.HasPyra = self.__class__.HasPyra(service, rules, path + [("HasPyra", "")])
                        self.DihedralAngle = self.__class__.DihedralAngle(service, rules, path + [("DihedralAngle", "")])
                        self.MaxCoarseningCurvature = self.__class__.MaxCoarseningCurvature(service, rules, path + [("MaxCoarseningCurvature", "")])
                        self.HasHexa = self.__class__.HasHexa(service, rules, path + [("HasHexa", "")])
                        self.MinEdge = self.__class__.MinEdge(service, rules, path + [("MinEdge", "")])
                        self.HexaDeterminant = self.__class__.HexaDeterminant(service, rules, path + [("HexaDeterminant", "")])
                        self.MinEdgeRef = self.__class__.MinEdgeRef(service, rules, path + [("MinEdgeRef", "")])
                        self.MaxEdge = self.__class__.MaxEdge(service, rules, path + [("MaxEdge", "")])
                        self.HasTetra = self.__class__.HasTetra(service, rules, path + [("HasTetra", "")])
                        super().__init__(service, rules, path)

                    class Mode(PyMenu):
                        """
                        Parameter Mode of value type str.
                        """
                        pass

                    class HasPrism(PyMenu):
                        """
                        Parameter HasPrism of value type bool.
                        """
                        pass

                    class PrismWarpage(PyMenu):
                        """
                        Parameter PrismWarpage of value type float.
                        """
                        pass

                    class HexaWarpage(PyMenu):
                        """
                        Parameter HexaWarpage of value type float.
                        """
                        pass

                    class FaceAngle(PyMenu):
                        """
                        Parameter FaceAngle of value type float.
                        """
                        pass

                    class PrismAspectRatio(PyMenu):
                        """
                        Parameter PrismAspectRatio of value type float.
                        """
                        pass

                    class MaxEdgeRef(PyMenu):
                        """
                        Parameter MaxEdgeRef of value type float.
                        """
                        pass

                    class DegAnisotropy(PyMenu):
                        """
                        Parameter DegAnisotropy of value type float.
                        """
                        pass

                    class TetraAspectRatio(PyMenu):
                        """
                        Parameter TetraAspectRatio of value type float.
                        """
                        pass

                    class HasPyra(PyMenu):
                        """
                        Parameter HasPyra of value type bool.
                        """
                        pass

                    class DihedralAngle(PyMenu):
                        """
                        Parameter DihedralAngle of value type float.
                        """
                        pass

                    class MaxCoarseningCurvature(PyMenu):
                        """
                        Parameter MaxCoarseningCurvature of value type float.
                        """
                        pass

                    class HasHexa(PyMenu):
                        """
                        Parameter HasHexa of value type bool.
                        """
                        pass

                    class MinEdge(PyMenu):
                        """
                        Parameter MinEdge of value type float.
                        """
                        pass

                    class HexaDeterminant(PyMenu):
                        """
                        Parameter HexaDeterminant of value type float.
                        """
                        pass

                    class MinEdgeRef(PyMenu):
                        """
                        Parameter MinEdgeRef of value type float.
                        """
                        pass

                    class MaxEdge(PyMenu):
                        """
                        Parameter MaxEdge of value type float.
                        """
                        pass

                    class HasTetra(PyMenu):
                        """
                        Parameter HasTetra of value type bool.
                        """
                        pass

                class Input(PyMenu):
                    """
                    Singleton Input.
                    """
                    def __init__(self, service, rules, path):
                        self.VarList = self.__class__.VarList(service, rules, path + [("VarList", "")])
                        self.ScalarVariableSelect = self.__class__.ScalarVariableSelect(service, rules, path + [("ScalarVariableSelect", "")])
                        self.Deconvolution = self.__class__.Deconvolution(service, rules, path + [("Deconvolution", "")])
                        self.VariablesPost = self.__class__.VariablesPost(service, rules, path + [("VariablesPost", "")])
                        self.Convolution = self.__class__.Convolution(service, rules, path + [("Convolution", "")])
                        self.Expression = self.__class__.Expression(service, rules, path + [("Expression", "")])
                        self.ScalarVariableList = self.__class__.ScalarVariableList(service, rules, path + [("ScalarVariableList", "")])
                        self.PostDeconvolution = self.__class__.PostDeconvolution(service, rules, path + [("PostDeconvolution", "")])
                        self.CADFile = self.__class__.CADFile(service, rules, path + [("CADFile", "")])
                        self.Mode = self.__class__.Mode(service, rules, path + [("Mode", "")])
                        self.ScalarVariableTranslation = self.__class__.ScalarVariableTranslation(service, rules, path + [("ScalarVariableTranslation", "")])
                        self.Variables = self.__class__.Variables(service, rules, path + [("Variables", "")])
                        self.Smoothing = self.__class__.Smoothing(service, rules, path + [("Smoothing", "")])
                        self.ScalarVariable = self.__class__.ScalarVariable(service, rules, path + [("ScalarVariable", "")])
                        super().__init__(service, rules, path)

                    class VarList(PyMenu):
                        """
                        Singleton VarList.
                        """
                        def __init__(self, service, rules, path):
                            self.Var = self.__class__.Var(service, rules, path + [("Var", "")])
                            super().__init__(service, rules, path)

                        class Var(PyNamedObjectContainer):
                            class _Var(PyMenu):
                                """
                                Singleton _Var.
                                """
                                def __init__(self, service, rules, path):
                                    self.Name = self.__class__.Name(service, rules, path + [("Name", "")])
                                    self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                                    super().__init__(service, rules, path)

                                class Name(PyMenu):
                                    """
                                    Parameter Name of value type str.
                                    """
                                    pass

                                class _name_(PyMenu):
                                    """
                                    Parameter _name_ of value type str.
                                    """
                                    pass

                            def __getitem__(self, key: str) -> _Var:
                                return super().__getitem__(key)

                    class ScalarVariableSelect(PyMenu):
                        """
                        Parameter ScalarVariableSelect of value type str.
                        """
                        pass

                    class Deconvolution(PyMenu):
                        """
                        Parameter Deconvolution of value type int.
                        """
                        pass

                    class VariablesPost(PyMenu):
                        """
                        Parameter VariablesPost of value type List[str].
                        """
                        pass

                    class Convolution(PyMenu):
                        """
                        Parameter Convolution of value type int.
                        """
                        pass

                    class Expression(PyMenu):
                        """
                        Parameter Expression of value type str.
                        """
                        pass

                    class ScalarVariableList(PyMenu):
                        """
                        Parameter ScalarVariableList of value type str.
                        """
                        pass

                    class PostDeconvolution(PyMenu):
                        """
                        Parameter PostDeconvolution of value type int.
                        """
                        pass

                    class CADFile(PyMenu):
                        """
                        Parameter CADFile of value type str.
                        """
                        pass

                    class Mode(PyMenu):
                        """
                        Parameter Mode of value type str.
                        """
                        pass

                    class ScalarVariableTranslation(PyMenu):
                        """
                        Parameter ScalarVariableTranslation of value type str.
                        """
                        pass

                    class Variables(PyMenu):
                        """
                        Parameter Variables of value type List[str].
                        """
                        pass

                    class Smoothing(PyMenu):
                        """
                        Parameter Smoothing of value type str.
                        """
                        pass

                    class ScalarVariable(PyMenu):
                        """
                        Parameter ScalarVariable of value type str.
                        """
                        pass

                class Boundaries(PyMenu):
                    """
                    Singleton Boundaries.
                    """
                    def __init__(self, service, rules, path):
                        self.YFamilies = self.__class__.YFamilies(service, rules, path + [("YFamilies", "")])
                        self.DeadZones = self.__class__.DeadZones(service, rules, path + [("DeadZones", "")])
                        super().__init__(service, rules, path)

                    class YFamilies(PyMenu):
                        """
                        Parameter YFamilies of value type List[str].
                        """
                        pass

                    class DeadZones(PyMenu):
                        """
                        Parameter DeadZones of value type List[str].
                        """
                        pass

                class GenerateCAD(PyCommand):
                    """
                    GenerateCAD() -> bool
                    """
                    pass

                class EditCAD(PyCommand):
                    """
                    EditCAD() -> bool
                    """
                    pass

                class ResetCAD(PyCommand):
                    """
                    ResetCAD() -> bool
                    """
                    pass

            class GlobalSettings(PyMenu):
                """
                Singleton GlobalSettings.
                """
                def __init__(self, service, rules, path):
                    self.AdvancedFlag = self.__class__.AdvancedFlag(service, rules, path + [("AdvancedFlag", "")])
                    self.BetaFlag = self.__class__.BetaFlag(service, rules, path + [("BetaFlag", "")])
                    self.CFFOutput = self.__class__.CFFOutput(service, rules, path + [("CFFOutput", "")])
                    self.BetaOrAdvancedFlag = self.__class__.BetaOrAdvancedFlag(service, rules, path + [("BetaOrAdvancedFlag", "")])
                    self.PlotInterval = self.__class__.PlotInterval(service, rules, path + [("PlotInterval", "")])
                    super().__init__(service, rules, path)

                class AdvancedFlag(PyMenu):
                    """
                    Parameter AdvancedFlag of value type bool.
                    """
                    pass

                class BetaFlag(PyMenu):
                    """
                    Parameter BetaFlag of value type bool.
                    """
                    pass

                class CFFOutput(PyMenu):
                    """
                    Parameter CFFOutput of value type bool.
                    """
                    pass

                class BetaOrAdvancedFlag(PyMenu):
                    """
                    Parameter BetaOrAdvancedFlag of value type bool.
                    """
                    pass

                class PlotInterval(PyMenu):
                    """
                    Parameter PlotInterval of value type int.
                    """
                    pass

            class SetupErrors(PyMenu):
                """
                Parameter SetupErrors of value type str.
                """
                pass

            class IsBusy(PyMenu):
                """
                Parameter IsBusy of value type bool.
                """
                pass

            class SetupWarnings(PyMenu):
                """
                Parameter SetupWarnings of value type str.
                """
                pass

            class InProgress(PyMenu):
                """
                Parameter InProgress of value type bool.
                """
                pass

            class SendCommandQuiet(PyCommand):
                """
                SendCommandQuiet(Command: str) -> bool
                """
                pass

            class ImportMesh(PyCommand):
                """
                ImportMesh(Filename: str) -> bool
                """
                pass

            class SyncDM(PyCommand):
                """
                SyncDM() -> bool
                """
                pass

            class InitAddOnAero(PyCommand):
                """
                InitAddOnAero() -> bool
                """
                pass

            class InitAddOn(PyCommand):
                """
                InitAddOn() -> bool
                """
                pass

            class CheckSetup(PyCommand):
                """
                CheckSetup() -> str
                """
                pass

            class SaveCase(PyCommand):
                """
                SaveCase(FileName: str) -> bool
                """
                pass

            class SavePostCaseAndData(PyCommand):
                """
                SavePostCaseAndData(FileName: str) -> bool
                """
                pass

            class SaveCaseAs(PyCommand):
                """
                SaveCaseAs(FileName: str) -> bool
                """
                pass

            class InitDM(PyCommand):
                """
                InitDM() -> bool
                """
                pass

            class LoadCase(PyCommand):
                """
                LoadCase(FileName: str) -> bool
                """
                pass

            class SaveCaseAndData(PyCommand):
                """
                SaveCaseAndData(FileName: str) -> bool
                """
                pass

            class ImportCase(PyCommand):
                """
                ImportCase(Filename: str) -> bool
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

            class SaveData(PyCommand):
                """
                SaveData(FileName: str) -> bool
                """
                pass

            class ReloadCase(PyCommand):
                """
                ReloadCase(Filename: str) -> bool
                """
                pass

            class IcingImportCase(PyCommand):
                """
                IcingImportCase(Filename: str) -> bool
                """
                pass

            class IcingImportMesh(PyCommand):
                """
                IcingImportMesh(Filename: str) -> bool
                """
                pass

            class WriteAll(PyCommand):
                """
                WriteAll(FileName: str) -> bool
                """
                pass

        class CaseInfo(PyMenu):
            """
            Singleton CaseInfo.
            """
            def __init__(self, service, rules, path):
                self.HostName = self.__class__.HostName(service, rules, path + [("HostName", "")])
                self.Dimension = self.__class__.Dimension(service, rules, path + [("Dimension", "")])
                self.IsEduOnlyLogo = self.__class__.IsEduOnlyLogo(service, rules, path + [("IsEduOnlyLogo", "")])
                self.Configuration = self.__class__.Configuration(service, rules, path + [("Configuration", "")])
                self.CaseFileNameDirStripped = self.__class__.CaseFileNameDirStripped(service, rules, path + [("CaseFileNameDirStripped", "")])
                self.IsStudentOnly = self.__class__.IsStudentOnly(service, rules, path + [("IsStudentOnly", "")])
                self.CaseFileName = self.__class__.CaseFileName(service, rules, path + [("CaseFileName", "")])
                self.SolverName = self.__class__.SolverName(service, rules, path + [("SolverName", "")])
                super().__init__(service, rules, path)

            class HostName(PyMenu):
                """
                Parameter HostName of value type str.
                """
                pass

            class Dimension(PyMenu):
                """
                Parameter Dimension of value type str.
                """
                pass

            class IsEduOnlyLogo(PyMenu):
                """
                Parameter IsEduOnlyLogo of value type bool.
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

            class IsStudentOnly(PyMenu):
                """
                Parameter IsStudentOnly of value type bool.
                """
                pass

            class CaseFileName(PyMenu):
                """
                Parameter CaseFileName of value type str.
                """
                pass

            class SolverName(PyMenu):
                """
                Parameter SolverName of value type str.
                """
                pass

        class AuxiliaryInfo(PyMenu):
            """
            Singleton AuxiliaryInfo.
            """
            def __init__(self, service, rules, path):
                self.IsCourantNumberActive = self.__class__.IsCourantNumberActive(service, rules, path + [("IsCourantNumberActive", "")])
                self.DefaultField = self.__class__.DefaultField(service, rules, path + [("DefaultField", "")])
                self.IsSgPDFTransport = self.__class__.IsSgPDFTransport(service, rules, path + [("IsSgPDFTransport", "")])
                self.FluentBoundaryZones = self.__class__.FluentBoundaryZones(service, rules, path + [("FluentBoundaryZones", "")])
                self.IsPVCouplingActive = self.__class__.IsPVCouplingActive(service, rules, path + [("IsPVCouplingActive", "")])
                self.MultiPhaseDomainList = self.__class__.MultiPhaseDomainList(service, rules, path + [("MultiPhaseDomainList", "")])
                self.IsDPMWallFilmBC = self.__class__.IsDPMWallFilmBC(service, rules, path + [("IsDPMWallFilmBC", "")])
                self.IsOversetReadOnly = self.__class__.IsOversetReadOnly(service, rules, path + [("IsOversetReadOnly", "")])
                self.MultiPhaseModel = self.__class__.MultiPhaseModel(service, rules, path + [("MultiPhaseModel", "")])
                self.TimeStepSpecification = self.__class__.TimeStepSpecification(service, rules, path + [("TimeStepSpecification", "")])
                self.DefaultVectorField = self.__class__.DefaultVectorField(service, rules, path + [("DefaultVectorField", "")])
                self.IsUnsteadyParticleTracking = self.__class__.IsUnsteadyParticleTracking(service, rules, path + [("IsUnsteadyParticleTracking", "")])
                super().__init__(service, rules, path)

            class IsCourantNumberActive(PyMenu):
                """
                Parameter IsCourantNumberActive of value type bool.
                """
                pass

            class DefaultField(PyMenu):
                """
                Parameter DefaultField of value type str.
                """
                pass

            class IsSgPDFTransport(PyMenu):
                """
                Parameter IsSgPDFTransport of value type bool.
                """
                pass

            class FluentBoundaryZones(PyMenu):
                """
                Parameter FluentBoundaryZones of value type List[str].
                """
                pass

            class IsPVCouplingActive(PyMenu):
                """
                Parameter IsPVCouplingActive of value type bool.
                """
                pass

            class MultiPhaseDomainList(PyMenu):
                """
                Parameter MultiPhaseDomainList of value type List[str].
                """
                pass

            class IsDPMWallFilmBC(PyMenu):
                """
                Parameter IsDPMWallFilmBC of value type bool.
                """
                pass

            class IsOversetReadOnly(PyMenu):
                """
                Parameter IsOversetReadOnly of value type bool.
                """
                pass

            class MultiPhaseModel(PyMenu):
                """
                Parameter MultiPhaseModel of value type str.
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

            class IsUnsteadyParticleTracking(PyMenu):
                """
                Parameter IsUnsteadyParticleTracking of value type bool.
                """
                pass

        class AppName(PyMenu):
            """
            Parameter AppName of value type str.
            """
            pass

        class ReadCase(PyCommand):
            """
            ReadCase(FileName: str) -> bool
            """
            pass

        class WriteCase(PyCommand):
            """
            WriteCase(FileName: str, Binary: bool, Overwrite: bool) -> bool
            """
            pass

        class ReadData(PyCommand):
            """
            ReadData(FileName: str) -> bool
            """
            pass

        class ClearDatamodel(PyCommand):
            """
            ClearDatamodel() -> None
            """
            pass

        class WriteData(PyCommand):
            """
            WriteData(FileName: str, Binary: bool, Overwrite: bool) -> bool
            """
            pass

        class SendCommand(PyCommand):
            """
            SendCommand(Command: str) -> bool
            """
            pass

        class ReadCaseAndData(PyCommand):
            """
            ReadCaseAndData(FileName: str) -> bool
            """
            pass

        class WriteCaseAndData(PyCommand):
            """
            WriteCaseAndData(FileName: str, Binary: bool, Overwrite: bool) -> bool
            """
            pass

