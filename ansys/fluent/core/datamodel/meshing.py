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
        self.GlobalSettings = self.__class__.GlobalSettings(service, rules, path + [("GlobalSettings", "")])
        self.Capping = self.__class__.Capping(service, rules, "Capping", path)
        self.GenerateTheSurfaceMeshFTM = self.__class__.GenerateTheSurfaceMeshFTM(service, rules, "GenerateTheSurfaceMeshFTM", path)
        self.CreateRegions = self.__class__.CreateRegions(service, rules, "CreateRegions", path)
        self.IdentifyDeviatedFaces = self.__class__.IdentifyDeviatedFaces(service, rules, "IdentifyDeviatedFaces", path)
        self.PartManagement = self.__class__.PartManagement(service, rules, "PartManagement", path)
        self.LocalScopedSizingForPartReplacement = self.__class__.LocalScopedSizingForPartReplacement(service, rules, "LocalScopedSizingForPartReplacement", path)
        self.GenerateTheMultiZoneMesh = self.__class__.GenerateTheMultiZoneMesh(service, rules, "GenerateTheMultiZoneMesh", path)
        self.ManageZones = self.__class__.ManageZones(service, rules, "ManageZones", path)
        self.DefineLeakageThreshold = self.__class__.DefineLeakageThreshold(service, rules, "DefineLeakageThreshold", path)
        self.RunCustomJournal = self.__class__.RunCustomJournal(service, rules, "RunCustomJournal", path)
        self.PartReplacementSettings = self.__class__.PartReplacementSettings(service, rules, "PartReplacementSettings", path)
        self.CreateContactPatch = self.__class__.CreateContactPatch(service, rules, "CreateContactPatch", path)
        self.SetupBoundaryLayers = self.__class__.SetupBoundaryLayers(service, rules, "SetupBoundaryLayers", path)
        self.ShareTopology = self.__class__.ShareTopology(service, rules, "ShareTopology", path)
        self.CreateBackgroundMesh = self.__class__.CreateBackgroundMesh(service, rules, "CreateBackgroundMesh", path)
        self.ComputeSizeField = self.__class__.ComputeSizeField(service, rules, "ComputeSizeField", path)
        self.CreatePorousRegions = self.__class__.CreatePorousRegions(service, rules, "CreatePorousRegions", path)
        self.ExtrudeVolumeMesh = self.__class__.ExtrudeVolumeMesh(service, rules, "ExtrudeVolumeMesh", path)
        self.CreateExternalFlowBoundaries = self.__class__.CreateExternalFlowBoundaries(service, rules, "CreateExternalFlowBoundaries", path)
        self.AddLocalSizingFTM = self.__class__.AddLocalSizingFTM(service, rules, "AddLocalSizingFTM", path)
        self.GenerateTheVolumeMeshFTM = self.__class__.GenerateTheVolumeMeshFTM(service, rules, "GenerateTheVolumeMeshFTM", path)
        self.GenerateTheSurfaceMeshWTM = self.__class__.GenerateTheSurfaceMeshWTM(service, rules, "GenerateTheSurfaceMeshWTM", path)
        self.CreateOversetInterfaces = self.__class__.CreateOversetInterfaces(service, rules, "CreateOversetInterfaces", path)
        self.AddThickness = self.__class__.AddThickness(service, rules, "AddThickness", path)
        self.ComplexMeshingRegions = self.__class__.ComplexMeshingRegions(service, rules, "ComplexMeshingRegions", path)
        self.CreateComponentMesh = self.__class__.CreateComponentMesh(service, rules, "CreateComponentMesh", path)
        self.GeneratePrisms = self.__class__.GeneratePrisms(service, rules, "GeneratePrisms", path)
        self.DescribeOversetFeatures = self.__class__.DescribeOversetFeatures(service, rules, "DescribeOversetFeatures", path)
        self.UpdateTheVolumeMesh = self.__class__.UpdateTheVolumeMesh(service, rules, "UpdateTheVolumeMesh", path)
        self.AddBoundaryLayersForPartReplacement = self.__class__.AddBoundaryLayersForPartReplacement(service, rules, "AddBoundaryLayersForPartReplacement", path)
        self.AddMultiZoneControls = self.__class__.AddMultiZoneControls(service, rules, "AddMultiZoneControls", path)
        self.SetUpPeriodicBoundaries = self.__class__.SetUpPeriodicBoundaries(service, rules, "SetUpPeriodicBoundaries", path)
        self.CloseLeakage = self.__class__.CloseLeakage(service, rules, "CloseLeakage", path)
        self.LinearMeshPattern = self.__class__.LinearMeshPattern(service, rules, "LinearMeshPattern", path)
        self.AddLocalSizingWTM = self.__class__.AddLocalSizingWTM(service, rules, "AddLocalSizingWTM", path)
        self.CreateGapCover = self.__class__.CreateGapCover(service, rules, "CreateGapCover", path)
        self.UpdateBoundaries = self.__class__.UpdateBoundaries(service, rules, "UpdateBoundaries", path)
        self.SizeControlsTable = self.__class__.SizeControlsTable(service, rules, "SizeControlsTable", path)
        self.DescribeGeometryAndFlow = self.__class__.DescribeGeometryAndFlow(service, rules, "DescribeGeometryAndFlow", path)
        self.IdentifyRegions = self.__class__.IdentifyRegions(service, rules, "IdentifyRegions", path)
        self.ExtractEdges = self.__class__.ExtractEdges(service, rules, "ExtractEdges", path)
        self.RemeshSurface = self.__class__.RemeshSurface(service, rules, "RemeshSurface", path)
        self.CreateLocalRefinementRegions = self.__class__.CreateLocalRefinementRegions(service, rules, "CreateLocalRefinementRegions", path)
        self.WrapMain = self.__class__.WrapMain(service, rules, "WrapMain", path)
        self.IdentifyConstructionSurfaces = self.__class__.IdentifyConstructionSurfaces(service, rules, "IdentifyConstructionSurfaces", path)
        self.ImportGeometry = self.__class__.ImportGeometry(service, rules, "ImportGeometry", path)
        self.AddBoundaryType = self.__class__.AddBoundaryType(service, rules, "AddBoundaryType", path)
        self.SeparateContacts = self.__class__.SeparateContacts(service, rules, "SeparateContacts", path)
        self.UpdateRegions = self.__class__.UpdateRegions(service, rules, "UpdateRegions", path)
        self.GenerateTheVolumeMeshWTM = self.__class__.GenerateTheVolumeMeshWTM(service, rules, "GenerateTheVolumeMeshWTM", path)
        self.ModifyMeshRefinement = self.__class__.ModifyMeshRefinement(service, rules, "ModifyMeshRefinement", path)
        self.ImportBodyOfInfluenceGeometry = self.__class__.ImportBodyOfInfluenceGeometry(service, rules, "ImportBodyOfInfluenceGeometry", path)
        self.ChoosePartReplacementOptions = self.__class__.ChoosePartReplacementOptions(service, rules, "ChoosePartReplacementOptions", path)
        self.UpdateRegionSettings = self.__class__.UpdateRegionSettings(service, rules, "UpdateRegionSettings", path)
        self.ImproveSurfaceMesh = self.__class__.ImproveSurfaceMesh(service, rules, "ImproveSurfaceMesh", path)
        self.ChooseMeshControlOptions = self.__class__.ChooseMeshControlOptions(service, rules, "ChooseMeshControlOptions", path)
        self.AddBoundaryLayers = self.__class__.AddBoundaryLayers(service, rules, "AddBoundaryLayers", path)
        self.GeometrySetup = self.__class__.GeometrySetup(service, rules, "GeometrySetup", path)
        self.ImproveVolumeMesh = self.__class__.ImproveVolumeMesh(service, rules, "ImproveVolumeMesh", path)
        self.TransformVolumeMesh = self.__class__.TransformVolumeMesh(service, rules, "TransformVolumeMesh", path)
        self.CreateCollarMesh = self.__class__.CreateCollarMesh(service, rules, "CreateCollarMesh", path)
        self.IdentifyOrphans = self.__class__.IdentifyOrphans(service, rules, "IdentifyOrphans", path)
        self.MeshFluidDomain = self.__class__.MeshFluidDomain(service, rules, "MeshFluidDomain", path)
        super().__init__(service, rules, path)

    class GlobalSettings(PyMenu):
        """
        Singleton GlobalSettings.
        """
        def __init__(self, service, rules, path):
            self.FTMRegionData = self.__class__.FTMRegionData(service, rules, path + [("FTMRegionData", "")])
            self.EnableCleanCAD = self.__class__.EnableCleanCAD(service, rules, path + [("EnableCleanCAD", "")])
            self.EnableComplexMeshing = self.__class__.EnableComplexMeshing(service, rules, path + [("EnableComplexMeshing", "")])
            self.InitialVersion = self.__class__.InitialVersion(service, rules, path + [("InitialVersion", "")])
            self.LengthUnit = self.__class__.LengthUnit(service, rules, path + [("LengthUnit", "")])
            self.EnableOversetMeshing = self.__class__.EnableOversetMeshing(service, rules, path + [("EnableOversetMeshing", "")])
            self.VolumeUnit = self.__class__.VolumeUnit(service, rules, path + [("VolumeUnit", "")])
            self.AreaUnit = self.__class__.AreaUnit(service, rules, path + [("AreaUnit", "")])
            self.NormalMode = self.__class__.NormalMode(service, rules, path + [("NormalMode", "")])
            super().__init__(service, rules, path)

        class FTMRegionData(PyMenu):
            """
            Singleton FTMRegionData.
            """
            def __init__(self, service, rules, path):
                self.AllRegionMeshMethodList = self.__class__.AllRegionMeshMethodList(service, rules, path + [("AllRegionMeshMethodList", "")])
                self.AllRegionOversetComponenList = self.__class__.AllRegionOversetComponenList(service, rules, path + [("AllRegionOversetComponenList", "")])
                self.AllOversetSizeList = self.__class__.AllOversetSizeList(service, rules, path + [("AllOversetSizeList", "")])
                self.AllOversetVolumeFillList = self.__class__.AllOversetVolumeFillList(service, rules, path + [("AllOversetVolumeFillList", "")])
                self.AllRegionNameList = self.__class__.AllRegionNameList(service, rules, path + [("AllRegionNameList", "")])
                self.AllRegionFilterCategories = self.__class__.AllRegionFilterCategories(service, rules, path + [("AllRegionFilterCategories", "")])
                self.AllRegionSourceList = self.__class__.AllRegionSourceList(service, rules, path + [("AllRegionSourceList", "")])
                self.AllRegionVolumeFillList = self.__class__.AllRegionVolumeFillList(service, rules, path + [("AllRegionVolumeFillList", "")])
                self.AllOversetTypeList = self.__class__.AllOversetTypeList(service, rules, path + [("AllOversetTypeList", "")])
                self.AllRegionLinkedConstructionSurfaceList = self.__class__.AllRegionLinkedConstructionSurfaceList(service, rules, path + [("AllRegionLinkedConstructionSurfaceList", "")])
                self.AllRegionLeakageSizeList = self.__class__.AllRegionLeakageSizeList(service, rules, path + [("AllRegionLeakageSizeList", "")])
                self.AllRegionTypeList = self.__class__.AllRegionTypeList(service, rules, path + [("AllRegionTypeList", "")])
                self.AllOversetNameList = self.__class__.AllOversetNameList(service, rules, path + [("AllOversetNameList", "")])
                self.AllRegionSizeList = self.__class__.AllRegionSizeList(service, rules, path + [("AllRegionSizeList", "")])
                super().__init__(service, rules, path)

            class AllRegionMeshMethodList(PyMenu):
                """
                Parameter AllRegionMeshMethodList of value type List[str].
                """
                pass

            class AllRegionOversetComponenList(PyMenu):
                """
                Parameter AllRegionOversetComponenList of value type List[str].
                """
                pass

            class AllOversetSizeList(PyMenu):
                """
                Parameter AllOversetSizeList of value type List[str].
                """
                pass

            class AllOversetVolumeFillList(PyMenu):
                """
                Parameter AllOversetVolumeFillList of value type List[str].
                """
                pass

            class AllRegionNameList(PyMenu):
                """
                Parameter AllRegionNameList of value type List[str].
                """
                pass

            class AllRegionFilterCategories(PyMenu):
                """
                Parameter AllRegionFilterCategories of value type List[str].
                """
                pass

            class AllRegionSourceList(PyMenu):
                """
                Parameter AllRegionSourceList of value type List[str].
                """
                pass

            class AllRegionVolumeFillList(PyMenu):
                """
                Parameter AllRegionVolumeFillList of value type List[str].
                """
                pass

            class AllOversetTypeList(PyMenu):
                """
                Parameter AllOversetTypeList of value type List[str].
                """
                pass

            class AllRegionLinkedConstructionSurfaceList(PyMenu):
                """
                Parameter AllRegionLinkedConstructionSurfaceList of value type List[str].
                """
                pass

            class AllRegionLeakageSizeList(PyMenu):
                """
                Parameter AllRegionLeakageSizeList of value type List[str].
                """
                pass

            class AllRegionTypeList(PyMenu):
                """
                Parameter AllRegionTypeList of value type List[str].
                """
                pass

            class AllOversetNameList(PyMenu):
                """
                Parameter AllOversetNameList of value type List[str].
                """
                pass

            class AllRegionSizeList(PyMenu):
                """
                Parameter AllRegionSizeList of value type List[str].
                """
                pass

        class EnableCleanCAD(PyMenu):
            """
            Parameter EnableCleanCAD of value type bool.
            """
            pass

        class EnableComplexMeshing(PyMenu):
            """
            Parameter EnableComplexMeshing of value type bool.
            """
            pass

        class InitialVersion(PyMenu):
            """
            Parameter InitialVersion of value type str.
            """
            pass

        class LengthUnit(PyMenu):
            """
            Parameter LengthUnit of value type str.
            """
            pass

        class EnableOversetMeshing(PyMenu):
            """
            Parameter EnableOversetMeshing of value type bool.
            """
            pass

        class VolumeUnit(PyMenu):
            """
            Parameter VolumeUnit of value type str.
            """
            pass

        class AreaUnit(PyMenu):
            """
            Parameter AreaUnit of value type str.
            """
            pass

        class NormalMode(PyMenu):
            """
            Parameter NormalMode of value type bool.
            """
            pass

    class Capping(PyCommand):
        """
        Capping(PatchName: str, ZoneType: str, PatchType: str, SelectionType: str, LabelSelectionList: List[str], ZoneSelectionList: List[str], TopologyList: List[str], CreatePatchPreferences: Dict[str, Any], ObjectAssociation: str, NewObjectName: str, PatchObjectName: str, CapLabels: List[str], ZoneLocation: List[str], CompleteZoneSelectionList: List[str], CompleteLabelSelectionList: List[str], CompleteTopologyList: List[str]) -> bool
        """
        pass

    class GenerateTheSurfaceMeshFTM(PyCommand):
        """
        GenerateTheSurfaceMeshFTM(SurfaceQuality: float, SaveSurfaceMesh: bool, AdvancedOptions: bool, SaveIntermediateFiles: str, IntermediateFileName: str, SeparateSurface: str, AutoPairing: str, ParallelSerialOption: str, NumberOfSessions: int, MaxIslandFace: int, SpikeRemovalAngle: float, DihedralMinAngle: float, AutoAssignZoneTypes: str, AdvancedInnerWrap: str, ExcludeGapCoverZoneRecovery: str, GlobalMin: float, ShowSubTasks: str) -> bool
        """
        pass

    class CreateRegions(PyCommand):
        """
        CreateRegions(NumberOfFlowVolumes: int, MeshObject: str) -> bool
        """
        pass

    class IdentifyDeviatedFaces(PyCommand):
        """
        IdentifyDeviatedFaces(DisplayGridName: str, SelectionType: str, ObjectSelectionList: List[str], ZoneSelectionList: List[str], ZoneLocation: List[str], AdvancedOptions: bool, DeviationMinValue: float, DeviationMaxValue: float, Overlay: str) -> bool
        """
        pass

    class PartManagement(PyCommand):
        """
        PartManagement(FileLoaded: str, FMDFileName: str, AppendFileName: str, Append: bool, LengthUnit: str, CreateObjectPer: str, FileLengthUnit: str, FileLengthUnitAppend: str, Route: str, RouteAppend: str, JtLOD: str, JtLODAppend: str, PartPerBody: bool, FeatureAngle: float, OneZonePer: str, Refaceting: Dict[str, Any], IgnoreSolidNames: bool, IgnoreSolidNamesAppend: bool, Options: Dict[str, Any], EdgeExtraction: str, Context: int, ObjectSetting: str) -> bool
        """
        pass

    class LocalScopedSizingForPartReplacement(PyCommand):
        """
        LocalScopedSizingForPartReplacement(LocalSettingsName: str, SelectionType: str, ObjectSelectionList: List[str], LabelSelectionList: List[str], ZoneSelectionList: List[str], ZoneLocation: List[str], EdgeSelectionList: List[str], LocalSizeControlParameters: Dict[str, Any], ValueChanged: str, CompleteZoneSelectionList: List[str], CompleteLabelSelectionList: List[str], CompleteObjectSelectionList: List[str], CompleteEdgeSelectionList: List[str]) -> bool
        """
        pass

    class GenerateTheMultiZoneMesh(PyCommand):
        """
        GenerateTheMultiZoneMesh(OrtogonalQualityLimit: float, RegionScope: List[str], CFDSurfaceMeshControls: Dict[str, Any], CompleteRegionScope: List[str]) -> bool
        """
        pass

    class ManageZones(PyCommand):
        """
        ManageZones(Type: str, ZoneFilter: str, SizeFilter: str, Area: float, Volume: float, EqualRange: float, ZoneOrLabel: str, LabelList: List[str], ManageFaceZoneList: List[str], ManageCellZoneList: List[str], BodyLabelList: List[str], Operation: str, OperationName: str, MZChildName: str, AddPrefixName: str, FaceMerge: str, Angle: float, ZoneList: List[str], ZoneLocation: List[str]) -> bool
        """
        pass

    class DefineLeakageThreshold(PyCommand):
        """
        DefineLeakageThreshold(AddChild: str, LeakageName: str, SelectionType: str, DeadRegionsList: List[str], RegionSelectionSingle: List[str], DeadRegionsSize: float, PlaneClippingValue: int, PlaneDirection: str, FlipDirection: bool) -> bool
        """
        pass

    class RunCustomJournal(PyCommand):
        """
        RunCustomJournal(JournalString: str) -> bool
        """
        pass

    class PartReplacementSettings(PyCommand):
        """
        PartReplacementSettings(PartReplacementName: str, ManagementMethod: str, CreationMethod: str, OldObjectSelectionList: List[str], NewObjectSelectionList: List[str], AdvancedOptions: bool, ScalingFactor: float, MptMethodType: str, GraphicalSelection: bool, ShowCoordinates: bool, X: float, Y: float, Z: float) -> bool
        """
        pass

    class CreateContactPatch(PyCommand):
        """
        CreateContactPatch(ContactPatchName: str, SelectionType: str, ZoneSelectionList: List[str], ZoneLocation: List[str], ObjectSelectionList: List[str], LabelSelectionList: List[str], GroundZoneSelectionList: List[str], Distance: float, FeatureAngle: float, PatchHole: bool, FlipDirection: bool) -> bool
        """
        pass

    class SetupBoundaryLayers(PyCommand):
        """
        SetupBoundaryLayers(AddChild: str, PrismsSettingsName: str, AspectRatio: float, GrowthRate: float, OffsetMethodType: str, LastRatioPercentage: float, FirstHeight: float, PrismLayers: int, RegionSelectionList: List[str]) -> bool
        """
        pass

    class ShareTopology(PyCommand):
        """
        ShareTopology(GapDistance: float, GapDistanceConnect: float, STMinSize: float, InterfaceSelect: str, ShareTopologyPreferences: Dict[str, Any], SMImprovePreferences: Dict[str, Any], SurfaceMeshPreferences: Dict[str, Any]) -> bool
        """
        pass

    class CreateBackgroundMesh(PyCommand):
        """
        CreateBackgroundMesh(RefinementRegionsName: str, CreationMethod: str, BOIMaxSize: float, BOISizeName: str, SelectionType: str, ZoneSelectionList: List[str], ZoneLocation: List[str], LabelSelectionList: List[str], ObjectSelectionList: List[str], ZoneSelectionSingle: List[str], ObjectSelectionSingle: List[str], BoundingBoxObject: Dict[str, Any], OffsetObject: Dict[str, Any], CylinderObject: Dict[str, Any]) -> bool
        """
        pass

    class ComputeSizeField(PyCommand):
        """
        ComputeSizeField(ComputeSizeFieldControl: str) -> bool
        """
        pass

    class CreatePorousRegions(PyCommand):
        """
        CreatePorousRegions(InputMethod: str, PorousRegionName: str, FileName: str, Location: str, CellSizeP1P2: float, CellSizeP1P3: float, CellSizeP1P4: float, BufferSizeRatio: float, P1: List[float], P2: List[float], P3: List[float], P4: List[float], NonRectangularParameters: Dict[str, Any]) -> bool
        """
        pass

    class ExtrudeVolumeMesh(PyCommand):
        """
        ExtrudeVolumeMesh(MExControlName: str, Method: str, ExternalBoundaryZoneList: List[str], TotalHeight: float, FirstHeight: float, NumberofLayers: int, GrowthRate: float, VMExtrudePreferences: Dict[str, Any], ZoneLocation: List[str]) -> bool
        """
        pass

    class CreateExternalFlowBoundaries(PyCommand):
        """
        CreateExternalFlowBoundaries(ExternalBoundariesName: str, CreationMethod: str, ExtractionMethod: str, SelectionType: str, ObjectSelectionList: List[str], ZoneSelectionList: List[str], ZoneLocation: List[str], LabelSelectionList: List[str], ObjectSelectionSingle: List[str], ZoneSelectionSingle: List[str], LabelSelectionSingle: List[str], OriginalObjectName: str, BoundingBoxObject: Dict[str, Any]) -> bool
        """
        pass

    class AddLocalSizingFTM(PyCommand):
        """
        AddLocalSizingFTM(LocalSettingsName: str, SelectionType: str, ObjectSelectionList: List[str], LabelSelectionList: List[str], ZoneSelectionList: List[str], ZoneLocation: List[str], EdgeSelectionList: List[str], LocalSizeControlParameters: Dict[str, Any], ValueChanged: str, CompleteZoneSelectionList: List[str], CompleteLabelSelectionList: List[str], CompleteObjectSelectionList: List[str], CompleteEdgeSelectionList: List[str]) -> bool
        """
        pass

    class GenerateTheVolumeMeshFTM(PyCommand):
        """
        GenerateTheVolumeMeshFTM(MeshQuality: float, OrthogonalQuality: float, EnableParallel: bool, SaveVolumeMesh: bool, EditVolumeSettings: bool, RegionNameList: List[str], RegionVolumeFillList: List[str], RegionSizeList: List[str], OldRegionNameList: List[str], OldRegionVolumeFillList: List[str], OldRegionSizeList: List[str], AllRegionNameList: List[str], AllRegionVolumeFillList: List[str], AllRegionSizeList: List[str], AdvancedOptions: bool, SpikeRemovalAngle: float, DihedralMinAngle: float, AvoidHangingNodes: str, ShowSubTasks: str) -> bool
        """
        pass

    class GenerateTheSurfaceMeshWTM(PyCommand):
        """
        GenerateTheSurfaceMeshWTM(CFDSurfaceMeshControls: Dict[str, Any], SeparationRequired: str, SeparationAngle: float, RemeshSelectionType: str, RemeshZoneList: List[str], RemeshLabelList: List[str], SurfaceMeshPreferences: Dict[str, Any], ImportType: str, AppendMesh: bool, CadFacetingFileName: str, Directory: str, Pattern: str, LengthUnit: str, TesselationMethod: str, OriginalZones: List[str], ExecuteShareTopology: str, CADFacetingControls: Dict[str, Any], CadImportOptions: Dict[str, Any], ShareTopologyPreferences: Dict[str, Any], PreviewSizeToggle: bool) -> bool
        """
        pass

    class CreateOversetInterfaces(PyCommand):
        """
        CreateOversetInterfaces(OversetInterfacesName: str, ObjectSelectionList: List[str]) -> bool
        """
        pass

    class AddThickness(PyCommand):
        """
        AddThickness(ZeroThicknessName: str, SelectionType: str, ZoneSelectionList: List[str], ZoneLocation: List[str], ObjectSelectionList: List[str], LabelSelectionList: List[str], Distance: float) -> bool
        """
        pass

    class ComplexMeshingRegions(PyCommand):
        """
        ComplexMeshingRegions(ComplexMeshingRegionsOption: bool) -> bool
        """
        pass

    class CreateComponentMesh(PyCommand):
        """
        CreateComponentMesh(RefinementRegionsName: str, CreationMethod: str, BOIMaxSize: float, BOISizeName: str, SelectionType: str, ZoneSelectionList: List[str], ZoneLocation: List[str], LabelSelectionList: List[str], ObjectSelectionList: List[str], ZoneSelectionSingle: List[str], ObjectSelectionSingle: List[str], BoundingBoxObject: Dict[str, Any], OffsetObject: Dict[str, Any], CylinderObject: Dict[str, Any], VolumeFill: str) -> bool
        """
        pass

    class GeneratePrisms(PyCommand):
        """
        GeneratePrisms(GeneratePrismsOption: bool) -> bool
        """
        pass

    class DescribeOversetFeatures(PyCommand):
        """
        DescribeOversetFeatures(AdvancedOptions: bool, ComponentGrid: str, CollarGrid: str, BackgroundMesh: str, OversetInterfaces: str) -> bool
        """
        pass

    class UpdateTheVolumeMesh(PyCommand):
        """
        UpdateTheVolumeMesh(EnableParallel: bool) -> bool
        """
        pass

    class AddBoundaryLayersForPartReplacement(PyCommand):
        """
        AddBoundaryLayersForPartReplacement(AddChild: str, ReadPrismControlFile: str, BLControlName: str, OffsetMethodType: str, NumberOfLayers: int, FirstAspectRatio: float, TransitionRatio: float, Rate: float, FirstHeight: float, FaceScope: Dict[str, Any], RegionScope: List[str], BlLabelList: List[str], ZoneSelectionList: List[str], ZoneLocation: List[str], LocalPrismPreferences: Dict[str, Any], BLZoneList: List[str], BLRegionList: List[str], CompleteRegionScope: List[str], CompleteBlLabelList: List[str], CompleteBLZoneList: List[str], CompleteBLRegionList: List[str], CompleteZoneSelectionList: List[str], CompleteLabelSelectionList: List[str]) -> bool
        """
        pass

    class AddMultiZoneControls(PyCommand):
        """
        AddMultiZoneControls(ControlType: str, MultiZName: str, MeshMethod: str, FillWith: str, UseSweepSize: str, MaxSweepSize: float, RegionScope: List[str], SourceMethod: str, ParallelSelection: bool, LabelSourceList: List[str], ZoneSourceList: List[str], AssignSizeUsing: str, Intervals: int, Size: float, BiasMethod: str, GrowthMethod: str, GrowthRate: float, LastFirstRatio: float, EdgeLabelList: List[str], CFDSurfaceMeshControls: Dict[str, Any], CompleteRegionScope: List[str]) -> bool
        """
        pass

    class SetUpPeriodicBoundaries(PyCommand):
        """
        SetUpPeriodicBoundaries(MeshObject: str, Type: str, Method: str, PeriodicityAngle: float, LCSOrigin: Dict[str, Any], LCSVector: Dict[str, Any], TransShift: Dict[str, Any], SelectionType: str, ZoneList: List[str], LabelList: List[str], RemeshBoundariesOption: str, ZoneLocation: List[str], ListAllLabelToggle: bool) -> bool
        """
        pass

    class CloseLeakage(PyCommand):
        """
        CloseLeakage(CloseLeakageOption: bool) -> bool
        """
        pass

    class LinearMeshPattern(PyCommand):
        """
        LinearMeshPattern(ChildName: str, ObjectList: List[str], AutoPopulateVector: str, PatternVector: Dict[str, Any], Pitch: float, NumberOfUnits: int, CheckOverlappingFaces: str, BatteryModelingOptions: Dict[str, Any]) -> bool
        """
        pass

    class AddLocalSizingWTM(PyCommand):
        """
        AddLocalSizingWTM(AddChild: str, BOIControlName: str, BOIGrowthRate: float, BOIExecution: str, BOISize: float, BOIMinSize: float, BOIMaxSize: float, BOICurvatureNormalAngle: float, BOICellsPerGap: float, BOIScopeTo: str, IgnoreOrientation: str, BOIZoneorLabel: str, BOIFaceLabelList: List[str], BOIFaceZoneList: List[str], EdgeLabelList: List[str], TopologyList: List[str], BOIPatchingtoggle: bool, DrawSizeControl: bool, ZoneLocation: List[str], CompleteFaceZoneList: List[str], CompleteFaceLabelList: List[str], CompleteEdgeLabelList: List[str], CompleteTopologyList: List[str]) -> bool
        """
        pass

    class CreateGapCover(PyCommand):
        """
        CreateGapCover(GapCoverName: str, SizingMethod: str, GapSizeRatio: float, GapSize: float, SelectionType: str, ZoneSelectionList: List[str], ZoneLocation: List[str], LabelSelectionList: List[str], ObjectSelectionList: List[str]) -> bool
        """
        pass

    class UpdateBoundaries(PyCommand):
        """
        UpdateBoundaries(MeshObject: str, SelectionType: str, BoundaryLabelList: List[str], BoundaryLabelTypeList: List[str], BoundaryZoneList: List[str], BoundaryZoneTypeList: List[str], OldBoundaryLabelList: List[str], OldBoundaryLabelTypeList: List[str], OldBoundaryZoneList: List[str], OldBoundaryZoneTypeList: List[str], OldLabelZoneList: List[str], ListAllBoundariesToggle: bool, ZoneLocation: List[str]) -> bool
        """
        pass

    class SizeControlsTable(PyCommand):
        """
        SizeControlsTable(GlobalMin: float, GlobalMax: float, TargetGrowthRate: float, DrawSizeControl: bool, InitialSizeControl: bool, TargetSizeControl: bool, SizeControlInterval: float, SizeControlParameters: Dict[str, Any]) -> bool
        """
        pass

    class DescribeGeometryAndFlow(PyCommand):
        """
        DescribeGeometryAndFlow(FlowType: str, GeometryOptions: bool, AddEnclosure: str, CloseCaps: str, LocalRefinementRegions: str, DescribeGeometryAndFlowOptions: Dict[str, Any]) -> bool
        """
        pass

    class IdentifyRegions(PyCommand):
        """
        IdentifyRegions(AddChild: str, MaterialPointsName: str, MptMethodType: str, NewRegionType: str, LinkConstruction: str, SelectionType: str, ZoneSelectionList: List[str], ZoneLocation: List[str], LabelSelectionList: List[str], ObjectSelectionList: List[str], GraphicalSelection: bool, ShowCoordinates: bool, X: float, Y: float, Z: float, OffsetX: float, OffsetY: float, OffsetZ: float) -> bool
        """
        pass

    class ExtractEdges(PyCommand):
        """
        ExtractEdges(ExtractEdgesName: str, ExtractMethodType: str, SelectionType: str, ObjectSelectionList: List[str], GeomObjectSelectionList: List[str], ZoneSelectionList: List[str], ZoneLocation: List[str], LabelSelectionList: List[str], FeatureAngleLocal: int, IndividualCollective: str, SharpAngle: int, CompleteObjectSelectionList: List[str], CompleteGeomObjectSelectionList: List[str], NonExtractedObjects: List[str]) -> bool
        """
        pass

    class RemeshSurface(PyCommand):
        """
        RemeshSurface(RemeshSurfaceOption: bool) -> bool
        """
        pass

    class CreateLocalRefinementRegions(PyCommand):
        """
        CreateLocalRefinementRegions(RefinementRegionsName: str, CreationMethod: str, BOIMaxSize: float, BOISizeName: str, SelectionType: str, ZoneSelectionList: List[str], ZoneLocation: List[str], LabelSelectionList: List[str], ObjectSelectionList: List[str], ZoneSelectionSingle: List[str], ObjectSelectionSingle: List[str], BoundingBoxObject: Dict[str, Any], OffsetObject: Dict[str, Any], CylinderObject: Dict[str, Any], VolumeFill: str) -> bool
        """
        pass

    class WrapMain(PyCommand):
        """
        WrapMain(WrapRegionsName: str) -> bool
        """
        pass

    class IdentifyConstructionSurfaces(PyCommand):
        """
        IdentifyConstructionSurfaces(MRFName: str, CreationMethod: str, SelectionType: str, ObjectSelectionSingle: List[str], ZoneSelectionSingle: List[str], LabelSelectionSingle: List[str], ObjectSelectionList: List[str], ZoneSelectionList: List[str], ZoneLocation: List[str], LabelSelectionList: List[str], DefeaturingSize: float, OffsetHeight: float, Pivot: Dict[str, Any], Axis: Dict[str, Any], Rotation: Dict[str, Any], CylinderObject: Dict[str, Any], BoundingBoxObject: Dict[str, Any]) -> bool
        """
        pass

    class ImportGeometry(PyCommand):
        """
        ImportGeometry(FileFormat: str, LengthUnit: str, MeshUnit: str, ImportCadPreferences: Dict[str, Any], FileName: str, MeshFileName: str, NumParts: float, ImportType: str, AppendMesh: bool, Directory: str, Pattern: str, CadImportOptions: Dict[str, Any]) -> bool
        """
        pass

    class AddBoundaryType(PyCommand):
        """
        AddBoundaryType(MeshObject: str, NewBoundaryLabelName: str, NewBoundaryType: str, BoundaryFaceZoneList: List[str], Merge: str, ZoneLocation: List[str]) -> bool
        """
        pass

    class SeparateContacts(PyCommand):
        """
        SeparateContacts(SeparateContactsOption: bool) -> bool
        """
        pass

    class UpdateRegions(PyCommand):
        """
        UpdateRegions(MeshObject: str, RegionNameList: List[str], RegionTypeList: List[str], OldRegionNameList: List[str], OldRegionTypeList: List[str], RegionInternals: List[str], RegionInternalTypes: List[str]) -> bool
        """
        pass

    class GenerateTheVolumeMeshWTM(PyCommand):
        """
        GenerateTheVolumeMeshWTM(VolumeFill: str, MeshSolidRegions: bool, SizingMethod: str, VolumeFillControls: Dict[str, Any], RegionBasedPreferences: bool, ReMergeZones: str, ParallelMeshing: bool, VolumeMeshPreferences: Dict[str, Any], PrismPreferences: Dict[str, Any], InvokePrimsControl: str, OffsetMethodType: str, NumberOfLayers: int, FirstAspectRatio: float, TransitionRatio: float, Rate: float, FirstHeight: float, MeshObject: str, MeshDeadRegions: bool, BodyLabelList: List[str], PrismLayers: bool, QuadTetTransition: str, MergeCellZones: bool, FaceScope: Dict[str, Any], RegionTetNameList: List[str], RegionTetMaxCellLengthList: List[str], RegionTetGrowthRateList: List[str], RegionHexNameList: List[str], RegionHexMaxCellLengthList: List[str], OldRegionTetMaxCellLengthList: List[str], OldRegionTetGrowthRateList: List[str], OldRegionHexMaxCellLengthList: List[str], CFDSurfaceMeshControls: Dict[str, Any]) -> bool
        """
        pass

    class ModifyMeshRefinement(PyCommand):
        """
        ModifyMeshRefinement(MeshObject: str, RemeshExecution: str, RemeshControlName: str, LocalSize: float, FaceZoneOrLabel: str, RemeshFaceZoneList: List[str], RemeshFaceLabelList: List[str], SizingType: str, LocalMinSize: float, LocalMaxSize: float, RemeshGrowthRate: float, RemeshCurvatureNormalAngle: float, RemeshCellsPerGap: float, CFDSurfaceMeshControls: Dict[str, Any], RemeshPreferences: Dict[str, Any]) -> bool
        """
        pass

    class ImportBodyOfInfluenceGeometry(PyCommand):
        """
        ImportBodyOfInfluenceGeometry(LengthUnit: str, Type: str, GeometryFileName: str, MeshFileName: str, ImportedObjects: List[str], CadImportOptions: Dict[str, Any]) -> bool
        """
        pass

    class ChoosePartReplacementOptions(PyCommand):
        """
        ChoosePartReplacementOptions(AddPartManagement: str, AddPartReplacement: str, AddLocalSizing: str, AddBoundaryLayer: str, AddUpdateTheVolumeMesh: str) -> bool
        """
        pass

    class UpdateRegionSettings(PyCommand):
        """
        UpdateRegionSettings(MainFluidRegion: str, FilterCategory: str, RegionNameList: List[str], RegionMeshMethodList: List[str], RegionTypeList: List[str], RegionVolumeFillList: List[str], RegionLeakageSizeList: List[str], RegionOversetComponenList: List[str], OldRegionNameList: List[str], OldRegionMeshMethodList: List[str], OldRegionTypeList: List[str], OldRegionVolumeFillList: List[str], OldRegionLeakageSizeList: List[str], OldRegionOversetComponenList: List[str], AllRegionNameList: List[str], AllRegionMeshMethodList: List[str], AllRegionTypeList: List[str], AllRegionVolumeFillList: List[str], AllRegionLeakageSizeList: List[str], AllRegionOversetComponenList: List[str], AllRegionLinkedConstructionSurfaceList: List[str], AllRegionSourceList: List[str], AllRegionFilterCategories: List[str]) -> bool
        """
        pass

    class ImproveSurfaceMesh(PyCommand):
        """
        ImproveSurfaceMesh(MeshObject: str, FaceQualityLimit: float, SQMinSize: float, SMImprovePreferences: Dict[str, Any]) -> bool
        """
        pass

    class ChooseMeshControlOptions(PyCommand):
        """
        ChooseMeshControlOptions(ReadOrCreate: str, SizeControlFileName: str, WrapSizeControlFileName: str, CreationMethod: str, ViewOption: str, GlobalMin: float, GlobalMax: float, GlobalGrowthRate: float, MeshControlOptions: Dict[str, Any]) -> bool
        """
        pass

    class AddBoundaryLayers(PyCommand):
        """
        AddBoundaryLayers(AddChild: str, ReadPrismControlFile: str, BLControlName: str, OffsetMethodType: str, NumberOfLayers: int, FirstAspectRatio: float, TransitionRatio: float, Rate: float, FirstHeight: float, FaceScope: Dict[str, Any], RegionScope: List[str], BlLabelList: List[str], ZoneSelectionList: List[str], ZoneLocation: List[str], LocalPrismPreferences: Dict[str, Any], BLZoneList: List[str], BLRegionList: List[str], CompleteRegionScope: List[str], CompleteBlLabelList: List[str], CompleteBLZoneList: List[str], CompleteBLRegionList: List[str], CompleteZoneSelectionList: List[str], CompleteLabelSelectionList: List[str]) -> bool
        """
        pass

    class GeometrySetup(PyCommand):
        """
        GeometrySetup(SetupType: str, CappingRequired: str, WallToInternal: str, InvokeShareTopology: str, NonConformal: str, Multizone: str, SetupInternals: List[str], SetupInternalTypes: List[str], OldZoneList: List[str], OldZoneTypeList: List[str], RegionList: List[str], SMImprovePreferences: Dict[str, Any]) -> bool
        """
        pass

    class ImproveVolumeMesh(PyCommand):
        """
        ImproveVolumeMesh(CellQualityLimit: float, VMImprovePreferences: Dict[str, Any]) -> bool
        """
        pass

    class TransformVolumeMesh(PyCommand):
        """
        TransformVolumeMesh(MTControlName: str, Type: str, Method: str, CellZoneList: List[str], LCSOrigin: Dict[str, Any], LCSVector: Dict[str, Any], TransShift: Dict[str, Any], Angle: float, Copy: str, NumOfCopies: int, Merge: str, Rename: str) -> bool
        """
        pass

    class CreateCollarMesh(PyCommand):
        """
        CreateCollarMesh(RefinementRegionsName: str, CreationMethod: str, BOIMaxSize: float, BOISizeName: str, SelectionType: str, ZoneSelectionList: List[str], ZoneLocation: List[str], LabelSelectionList: List[str], ObjectSelectionList: List[str], ZoneSelectionSingle: List[str], ObjectSelectionSingle: List[str], BoundingBoxObject: Dict[str, Any], OffsetObject: Dict[str, Any], CylinderObject: Dict[str, Any], VolumeFill: str) -> bool
        """
        pass

    class IdentifyOrphans(PyCommand):
        """
        IdentifyOrphans(NumberOfOrphans: str, ObjectSelectionList: List[str], DonorPriorityMethod: str, OverlapBoundaries: str) -> bool
        """
        pass

    class MeshFluidDomain(PyCommand):
        """
        MeshFluidDomain(MeshFluidDomainOption: bool) -> bool
        """
        pass

