# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Data for for builtin setting classes."""

from collections.abc import Mapping

from ansys.fluent.core.utils.fluent_version import (
    FluentVersion,
    FluentVersionSet,
    since,
)

# {<class name>: (<kind>, <path>, <reciprocal?>)}
DATA: Mapping[str, tuple[str, str | dict[FluentVersionSet, str], str | None]] = {
    "Setup": ("Singleton", "setup", None),
    "General": ("Singleton", "setup.general", None),
    "Models": ("Singleton", "setup.models", None),
    "Multiphase": ("Singleton", "setup.models.multiphase", None),
    "Energy": ("Singleton", "setup.models.energy", None),
    "Viscous": ("Singleton", "setup.models.viscous", None),
    "Radiation": ("Singleton", "setup.models.radiation", None),
    "Species": ("Singleton", "setup.models.species", None),
    "DiscretePhase": ("Singleton", "setup.models.discrete_phase", None),
    "Injections": ("Singleton", "setup.models.discrete_phase.injections", "Injection"),
    "Injection": (
        "NamedObject",
        "setup.models.discrete_phase.injections",
        "Injections",
    ),
    "VirtualBladeModel": ("Singleton", "setup.models.virtual_blade_model", None),
    "Optics": ("Singleton", "setup.models.optics", None),
    "Structure": ("Singleton", "setup.models.structure", None),
    "Ablation": ("Singleton", "setup.models.ablation", None),
    "EChemistry": ("Singleton", "setup.models.echemistry", None),
    "Battery": ("Singleton", "setup.models.battery", None),
    "SystemCoupling": ("Singleton", "setup.models.system_coupling", None),
    "Sofc": ("Singleton", "setup.models.sofc", None),
    "Pemfc": ("Singleton", "setup.models.pemfc", None),
    "Materials": ("Singleton", "setup.materials", None),
    "FluidMaterials": ("Singleton", "setup.materials.fluid", "FluidMaterial"),
    "FluidMaterial": ("NamedObject", "setup.materials.fluid", "FluidMaterials"),
    "SolidMaterials": ("Singleton", "setup.materials.solid", "SolidMaterial"),
    "SolidMaterial": ("NamedObject", "setup.materials.solid", "SolidMaterials"),
    "MixtureMaterials": ("Singleton", "setup.materials.mixture", "MixtureMaterial"),
    "MixtureMaterial": ("NamedObject", "setup.materials.mixture", "MixtureMaterials"),
    "ParticleMixtureMaterials": (
        "Singleton",
        "setup.materials.particle_mixture",
        "ParticleMixtureMaterial",
    ),
    "ParticleMixtureMaterial": (
        "NamedObject",
        "setup.materials.particle_mixture",
        "ParticleMixtureMaterials",
    ),
    "CellZoneConditions": (
        "Singleton",
        "setup.cell_zone_conditions",
        "CellZoneCondition",
    ),
    "CellZoneCondition": (
        "NamedObject",
        "setup.cell_zone_conditions",
        "CellZoneConditions",
    ),
    "FluidCellZones": (
        "Singleton",
        "setup.cell_zone_conditions.fluid",
        "FluidCellZone",
    ),
    "FluidCellZone": (
        "NamedObject",
        "setup.cell_zone_conditions.fluid",
        "FluidCellZones",
    ),
    "SolidCellZones": (
        "Singleton",
        "setup.cell_zone_conditions.solid",
        "SolidCellZone",
    ),
    "SolidCellZone": (
        "NamedObject",
        "setup.cell_zone_conditions.solid",
        "SolidCellZones",
    ),
    "BoundaryConditions": (
        "Singleton",
        "setup.boundary_conditions",
        "BoundaryCondition",
    ),
    "BoundaryCondition": (
        "NamedObject",
        "setup.boundary_conditions",
        "BoundaryConditions",
    ),
    "AxisBoundaries": ("Singleton", "setup.boundary_conditions.axis", "AxisBoundary"),
    "AxisBoundary": ("NamedObject", "setup.boundary_conditions.axis", "AxisBoundaries"),
    "DegassingBoundaries": (
        "Singleton",
        "setup.boundary_conditions.degassing",
        "DegassingBoundary",
    ),
    "DegassingBoundary": (
        "NamedObject",
        "setup.boundary_conditions.degassing",
        "DegassingBoundaries",
    ),
    "ExhaustFanBoundaries": (
        "Singleton",
        "setup.boundary_conditions.exhaust_fan",
        "ExhaustFanBoundary",
    ),
    "ExhaustFanBoundary": (
        "NamedObject",
        "setup.boundary_conditions.exhaust_fan",
        "ExhaustFanBoundaries",
    ),
    "FanBoundaries": ("Singleton", "setup.boundary_conditions.fan", "FanBoundary"),
    "FanBoundary": ("NamedObject", "setup.boundary_conditions.fan", "FanBoundaries"),
    "GeometryBoundaries": (
        "Singleton",
        "setup.boundary_conditions.geometry",
        "GeometryBoundary",
    ),
    "GeometryBoundary": (
        "NamedObject",
        "setup.boundary_conditions.geometry",
        "GeometryBoundaries",
    ),
    "InletVentBoundaries": (
        "Singleton",
        "setup.boundary_conditions.inlet_vent",
        "InletVentBoundary",
    ),
    "InletVentBoundary": (
        "NamedObject",
        "setup.boundary_conditions.inlet_vent",
        "InletVentBoundaries",
    ),
    "IntakeFanBoundaries": (
        "Singleton",
        "setup.boundary_conditions.intake_fan",
        "IntakeFanBoundary",
    ),
    "IntakeFanBoundary": (
        "NamedObject",
        "setup.boundary_conditions.intake_fan",
        "IntakeFanBoundaries",
    ),
    "InterfaceBoundaries": (
        "Singleton",
        "setup.boundary_conditions.interface",
        "InterfaceBoundary",
    ),
    "InterfaceBoundary": (
        "NamedObject",
        "setup.boundary_conditions.interface",
        "InterfaceBoundaries",
    ),
    "InteriorBoundaries": (
        "Singleton",
        "setup.boundary_conditions.interior",
        "InteriorBoundary",
    ),
    "InteriorBoundary": (
        "NamedObject",
        "setup.boundary_conditions.interior",
        "InteriorBoundaries",
    ),
    "MassFlowInlets": (
        "Singleton",
        "setup.boundary_conditions.mass_flow_inlet",
        "MassFlowInlet",
    ),
    "MassFlowInlet": (
        "NamedObject",
        "setup.boundary_conditions.mass_flow_inlet",
        "MassFlowInlets",
    ),
    "MassFlowOutlets": (
        "Singleton",
        "setup.boundary_conditions.mass_flow_outlet",
        "MassFlowOutlet",
    ),
    "MassFlowOutlet": (
        "NamedObject",
        "setup.boundary_conditions.mass_flow_outlet",
        "MassFlowOutlets",
    ),
    "NetworkBoundaries": (
        "Singleton",
        "setup.boundary_conditions.network",
        "NetworkBoundary",
    ),
    "NetworkBoundary": (
        "NamedObject",
        "setup.boundary_conditions.network",
        "NetworkBoundaries",
    ),
    "NetworkEndBoundaries": (
        "Singleton",
        "setup.boundary_conditions.network_end",
        "NetworkEndBoundary",
    ),
    "NetworkEndBoundary": (
        "NamedObject",
        "setup.boundary_conditions.network_end",
        "NetworkEndBoundaries",
    ),
    "OutflowBoundaries": (
        "Singleton",
        "setup.boundary_conditions.outflow",
        "OutflowBoundary",
    ),
    "OutflowBoundary": (
        "NamedObject",
        "setup.boundary_conditions.outflow",
        "OutflowBoundaries",
    ),
    "OutletVentBoundaries": (
        "Singleton",
        "setup.boundary_conditions.outlet_vent",
        "OutletVentBoundary",
    ),
    "OutletVentBoundary": (
        "NamedObject",
        "setup.boundary_conditions.outlet_vent",
        "OutletVentBoundaries",
    ),
    "OversetBoundaries": (
        "Singleton",
        "setup.boundary_conditions.overset",
        "OversetBoundary",
    ),
    "OversetBoundary": (
        "NamedObject",
        "setup.boundary_conditions.overset",
        "OversetBoundaries",
    ),
    "PeriodicBoundaries": (
        "Singleton",
        "setup.boundary_conditions.periodic",
        "PeriodicBoundary",
    ),
    "PeriodicBoundary": (
        "NamedObject",
        "setup.boundary_conditions.periodic",
        "PeriodicBoundaries",
    ),
    "PorousJumpBoundaries": (
        "Singleton",
        "setup.boundary_conditions.porous_jump",
        "PorousJumpBoundary",
    ),
    "PorousJumpBoundary": (
        "NamedObject",
        "setup.boundary_conditions.porous_jump",
        "PorousJumpBoundaries",
    ),
    "PressureFarFieldBoundaries": (
        "Singleton",
        "setup.boundary_conditions.pressure_far_field",
        "PressureFarFieldBoundary",
    ),
    "PressureFarFieldBoundary": (
        "NamedObject",
        "setup.boundary_conditions.pressure_far_field",
        "PressureFarFieldBoundaries",
    ),
    "PressureInlets": (
        "Singleton",
        "setup.boundary_conditions.pressure_inlet",
        "PressureInlet",
    ),
    "PressureInlet": (
        "NamedObject",
        "setup.boundary_conditions.pressure_inlet",
        "PressureInlets",
    ),
    "PressureOutlets": (
        "Singleton",
        "setup.boundary_conditions.pressure_outlet",
        "PressureOutlet",
    ),
    "PressureOutlet": (
        "NamedObject",
        "setup.boundary_conditions.pressure_outlet",
        "PressureOutlets",
    ),
    "RadiatorBoundaries": (
        "Singleton",
        "setup.boundary_conditions.radiator",
        "RadiatorBoundary",
    ),
    "RadiatorBoundary": (
        "NamedObject",
        "setup.boundary_conditions.radiator",
        "RadiatorBoundaries",
    ),
    "RansLesInterfaceBoundaries": (
        "Singleton",
        "setup.boundary_conditions.rans_les_interface",
        "RansLesInterfaceBoundary",
    ),
    "RansLesInterfaceBoundary": (
        "NamedObject",
        "setup.boundary_conditions.rans_les_interface",
        "RansLesInterfaceBoundaries",
    ),
    "RecirculationInlets": (
        "Singleton",
        "setup.boundary_conditions.recirculation_inlet",
        "RecirculationInlet",
    ),
    "RecirculationInlet": (
        "NamedObject",
        "setup.boundary_conditions.recirculation_inlet",
        "RecirculationInlets",
    ),
    "RecirculationOutlets": (
        "Singleton",
        "setup.boundary_conditions.recirculation_outlet",
        "RecirculationOutlet",
    ),
    "RecirculationOutlet": (
        "NamedObject",
        "setup.boundary_conditions.recirculation_outlet",
        "RecirculationOutlets",
    ),
    "ShadowBoundaries": (
        "Singleton",
        "setup.boundary_conditions.shadow",
        "ShadowBoundary",
    ),
    "ShadowBoundary": (
        "NamedObject",
        "setup.boundary_conditions.shadow",
        "ShadowBoundaries",
    ),
    "SymmetryBoundaries": (
        "Singleton",
        "setup.boundary_conditions.symmetry",
        "SymmetryBoundary",
    ),
    "SymmetryBoundary": (
        "NamedObject",
        "setup.boundary_conditions.symmetry",
        "SymmetryBoundaries",
    ),
    "VelocityInlets": (
        "Singleton",
        "setup.boundary_conditions.velocity_inlet",
        "VelocityInlet",
    ),
    "VelocityInlet": (
        "NamedObject",
        "setup.boundary_conditions.velocity_inlet",
        "VelocityInlets",
    ),
    "WallBoundaries": ("Singleton", "setup.boundary_conditions.wall", "WallBoundary"),
    "WallBoundary": ("NamedObject", "setup.boundary_conditions.wall", "WallBoundaries"),
    "NonReflectingBoundary": (
        "Singleton",
        "setup.boundary_conditions.non_reflecting_bc",
        None,
    ),
    "PerforatedWallBoundary": (
        "Singleton",
        "setup.boundary_conditions.perforated_wall",
        None,
    ),
    "MeshInterfaces": (
        "Singleton",
        "setup.mesh_interfaces",
        None,
    ),
    "DynamicMesh": (
        "Singleton",
        {
            since(FluentVersion.v251): "setup.dynamic_mesh",
        },
        None,
    ),
    "ReferenceValues": ("Singleton", "setup.reference_values", None),
    "ReferenceFrames": (
        "Singleton",
        "setup.reference_frames",
        "ReferenceFrame",
    ),
    "ReferenceFrame": (
        "NamedObject",
        "setup.reference_frames",
        "ReferenceFrames",
    ),
    "NamedExpressions": (
        "Singleton",
        "setup.named_expressions",
        "NamedExpression",
    ),
    "NamedExpression": (
        "NamedObject",
        "setup.named_expressions",
        "NamedExpressions",
    ),
    "Solution": ("Singleton", "solution", None),
    "Methods": ("Singleton", "solution.methods", None),
    "Controls": ("Singleton", "solution.controls", None),
    "ReportDefinitions": ("Singleton", "solution.report_definitions", None),
    "Monitor": (
        "Singleton",
        "solution.monitor",
        None,
    ),
    "Residual": (
        "Singleton",
        "solution.monitor.residual",
        None,
    ),
    "ReportFiles": (
        "Singleton",
        "solution.monitor.report_files",
        "ReportFile",
    ),
    "ReportFile": (
        "NamedObject",
        "solution.monitor.report_files",
        "ReportFiles",
    ),
    "ReportPlots": (
        "Singleton",
        "solution.monitor.report_plots",
        "ReportPlot",
    ),
    "ReportPlot": (
        "NamedObject",
        "solution.monitor.report_plots",
        "ReportPlots",
    ),
    "ConvergenceConditions": (
        "Singleton",
        "solution.monitor.convergence_conditions",
        None,
    ),
    "CellRegisters": (
        "Singleton",
        "solution.cell_registers",
        "CellRegister",
    ),
    "CellRegister": (
        "NamedObject",
        "solution.cell_registers",
        "CellRegisters",
    ),
    "Initialization": ("Singleton", "solution.initialization", None),
    "CalculationActivity": (
        "Singleton",
        "solution.calculation_activity",
        None,
    ),
    "ExecuteCommands": (
        "Singleton",
        "solution.calculation_activity.execute_commands",
        None,
    ),
    "CaseModification": (
        "Singleton",
        "solution.calculation_activity.case_modification",
        None,
    ),
    "RunCalculation": ("Singleton", "solution.run_calculation", None),
    "Results": ("Singleton", "results", None),
    "Surfaces": ("Singleton", "results.surfaces", None),
    "PointSurfaces": (
        "Singleton",
        "results.surfaces.point_surface",
        "PointSurface",
    ),
    "PointSurface": (
        "NamedObject",
        "results.surfaces.point_surface",
        "PointSurfaces",
    ),
    "LineSurfaces": (
        "Singleton",
        "results.surfaces.line_surface",
        "LineSurface",
    ),
    "LineSurface": (
        "NamedObject",
        "results.surfaces.line_surface",
        "LineSurfaces",
    ),
    "RakeSurfaces": (
        "Singleton",
        "results.surfaces.rake_surface",
        "RakeSurface",
    ),
    "RakeSurface": (
        "NamedObject",
        "results.surfaces.rake_surface",
        "RakeSurfaces",
    ),
    "PlaneSurfaces": ("Singleton", "results.surfaces.plane_surface", None),
    "PlaneSurface": ("NamedObject", "results.surfaces.plane_surface", None),
    "IsoSurfaces": (
        "Singleton",
        "results.surfaces.iso_surface",
        None,
    ),
    "IsoSurface": (
        "NamedObject",
        "results.surfaces.iso_surface",
        None,
    ),
    "IsoClips": (
        "Singleton",
        "results.surfaces.iso_clip",
        "IsoClip",
    ),
    "IsoClip": (
        "NamedObject",
        "results.surfaces.iso_clip",
        "IsoClips",
    ),
    "ZoneSurfaces": (
        "Singleton",
        "results.surfaces.zone_surface",
        "ZoneSurface",
    ),
    "ZoneSurface": (
        "NamedObject",
        "results.surfaces.zone_surface",
        "ZoneSurfaces",
    ),
    "PartitionSurfaces": (
        "Singleton",
        "results.surfaces.partition_surface",
        "PartitionSurface",
    ),
    "PartitionSurface": (
        "NamedObject",
        "results.surfaces.partition_surface",
        "PartitionSurfaces",
    ),
    "TransformSurfaces": (
        "Singleton",
        "results.surfaces.transform_surface",
        "TransformSurface",
    ),
    "TransformSurface": (
        "NamedObject",
        "results.surfaces.transform_surface",
        "TransformSurfaces",
    ),
    "ImprintSurfaces": (
        "Singleton",
        "results.surfaces.imprint_surface",
        "ImprintSurface",
    ),
    "ImprintSurface": (
        "NamedObject",
        "results.surfaces.imprint_surface",
        "ImprintSurfaces",
    ),
    "PlaneSlices": (
        "Singleton",
        "results.surfaces.plane_slice",
        "PlaneSlice",
    ),
    "PlaneSlice": (
        "NamedObject",
        "results.surfaces.plane_slice",
        "PlaneSlices",
    ),
    "SphereSlices": (
        "Singleton",
        "results.surfaces.sphere_slice",
        "SphereSlice",
    ),
    "SphereSlice": (
        "NamedObject",
        "results.surfaces.sphere_slice",
        "SphereSlices",
    ),
    "QuadricSurfaces": (
        "Singleton",
        "results.surfaces.quadric_surface",
        "QuadricSurface",
    ),
    "QuadricSurface": (
        "NamedObject",
        "results.surfaces.quadric_surface",
        "QuadricSurfaces",
    ),
    "SurfaceCells": (
        "Singleton",
        "results.surfaces.surface_cells",
        "SurfaceCell",
    ),
    "SurfaceCell": (
        "NamedObject",
        "results.surfaces.surface_cells",
        "SurfaceCells",
    ),
    "ExpressionVolumes": (
        "Singleton",
        {
            since(FluentVersion.v251): "results.surfaces.expression_volume",
        },
        "ExpressionVolume",
    ),
    "ExpressionVolume": (
        "NamedObject",
        {
            since(FluentVersion.v251): "results.surfaces.expression_volume",
        },
        "ExpressionVolumes",
    ),
    "GroupSurfaces": (
        "Singleton",
        {
            since(FluentVersion.v251): "results.surfaces.group_surface",
        },
        "GroupSurface",
    ),
    "GroupSurface": (
        "NamedObject",
        {
            since(FluentVersion.v251): "results.surfaces.group_surface",
        },
        "GroupSurfaces",
    ),
    "Graphics": ("Singleton", "results.graphics", None),
    "Meshes": ("Singleton", "results.graphics.mesh", "Mesh"),
    "Mesh": ("NamedObject", "results.graphics.mesh", "Meshes"),
    "Contours": ("Singleton", "results.graphics.contour", "Contour"),
    "Contour": ("NamedObject", "results.graphics.contour", "Contours"),
    "Vectors": ("Singleton", "results.graphics.vector", None),
    "Vector": ("NamedObject", "results.graphics.vector", None),
    "Pathlines": (
        "Singleton",
        "results.graphics.pathline",
        None,
    ),
    "Pathline": (
        "NamedObject",
        "results.graphics.pathline",
        None,
    ),
    "ParticleTracks": (
        "Singleton",
        "results.graphics.particle_track",
        "ParticleTrack",
    ),
    "ParticleTrack": (
        "NamedObject",
        "results.graphics.particle_track",
        "ParticleTracks",
    ),
    "LICs": ("Singleton", "results.graphics.lic", None),
    "LIC": ("NamedObject", "results.graphics.lic", None),
    "Plots": (
        "Singleton",
        "results.plot",
        None,
    ),
    "XYPlots": (
        "Singleton",
        "results.plot.xy_plot",
        "XYPlot",
    ),
    "XYPlot": (
        "NamedObject",
        "results.plot.xy_plot",
        "XYPlots",
    ),
    "Histogram": (
        "Singleton",
        "results.plot.histogram",
        None,
    ),
    "CumulativePlots": (
        "Singleton",
        "results.plot.cumulative_plot",
        "CumulativePlot",
    ),
    "CumulativePlot": (
        "NamedObject",
        "results.plot.cumulative_plot",
        "CumulativePlots",
    ),
    "ProfileData": (
        "Singleton",
        "results.plot.profile_data",
        None,
    ),
    "InterpolatedData": (
        "Singleton",
        "results.plot.interpolated_data",
        None,
    ),
    "Scenes": (
        "Singleton",
        "results.scene",
        "Scene",
    ),
    "Scene": (
        "NamedObject",
        "results.scene",
        "Scenes",
    ),
    "SceneAnimation": (
        "Singleton",
        "results.animations.scene_animation",
        None,
    ),
    "Report": (
        "Singleton",
        "results.report",
        None,
    ),
    "DiscretePhaseHistogram": (
        "Singleton",
        "results.report.discrete_phase.histogram",
        None,
    ),
    "Fluxes": (
        "Singleton",
        "results.report.fluxes",
        None,
    ),
    "SurfaceIntegrals": (
        "Singleton",
        "results.report.surface_integrals",
        None,
    ),
    "VolumeIntegrals": (
        "Singleton",
        "results.report.volume_integrals",
        None,
    ),
    "InputParameters": (
        "Singleton",
        "parameters.input_parameters",
        None,
    ),
    "OutputParameters": (
        "Singleton",
        "parameters.output_parameters",
        None,
    ),
    "CustomFieldFunctions": (
        "Singleton",
        {
            since(FluentVersion.v251): "results.custom_field_functions",
        },
        "CustomFieldFunction",
    ),
    "CustomFieldFunction": (
        "NamedObject",
        {
            since(FluentVersion.v251): "results.custom_field_functions",
        },
        "CustomFieldFunctions",
    ),
    "CustomVectors": (
        "Singleton",
        "results.custom_vectors",
        "CustomVector",
    ),
    "CustomVector": (
        "NamedObject",
        "results.custom_vectors",
        "CustomVectors",
    ),
    "SimulationReports": (
        "Singleton",
        "results.report.simulation_reports",
        None,
    ),
    "ParametricStudies": ("Singleton", "parametric_studies", None),
    "ParametricStudy": ("NamedObject", "parametric_studies", None),
    "DesignPoints": ("Singleton", "parametric_studies.design_points", None),
    "DesignPoint": ("NamedObject", "parametric_studies.design_points", None),
    "ReadCase": ("Command", "file.read_case", None),
    "read_case": ("Command", "file.read_case", None),
    "ReadData": ("Command", "file.read_data", None),
    "read_data": ("Command", "file.read_data", None),
    "ReadCaseData": ("Command", "file.read_case_data", None),
    "read_case_data": ("Command", "file.read_case_data", None),
    "WriteCase": (
        "Command",
        "file.write_case",
        None,
    ),
    "write_case": (
        "Command",
        "file.write_case",
        None,
    ),
    "WriteData": (
        "Command",
        "file.write_data",
        None,
    ),
    "write_data": (
        "Command",
        "file.write_data",
        None,
    ),
    "WriteCaseData": (
        "Command",
        "file.write_case_data",
        None,
    ),
    "write_case_data": (
        "Command",
        "file.write_case_data",
        None,
    ),
    "Initialize": ("Command", "solution.initialization.initialize", None),
    "initialize": ("Command", "solution.initialization.initialize", None),
    "Calculate": ("Command", "solution.run_calculation.calculate", None),
    "calculate": ("Command", "solution.run_calculation.calculate", None),
    "Iterate": ("Command", "solution.run_calculation.iterate", None),
    "iterate": ("Command", "solution.run_calculation.iterate", None),
    "DualTimeIterate": ("Command", "solution.run_calculation.dual_time_iterate", None),
    "dual_time_iterate": (
        "Command",
        "solution.run_calculation.dual_time_iterate",
        None,
    ),
}
