# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
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

from ansys.fluent.core.utils.fluent_version import FluentVersion, since

# {<class name>: (<kind>, <path>)}
DATA = {
    "Setup": ("Singleton", "setup"),
    "General": ("Singleton", "setup.general"),
    "Models": ("Singleton", "setup.models"),
    "Multiphase": ("Singleton", "setup.models.multiphase"),
    "Energy": ("Singleton", "setup.models.energy"),
    "Viscous": ("Singleton", "setup.models.viscous"),
    "Radiation": ("Singleton", "setup.models.radiation"),
    "Species": ("Singleton", "setup.models.species"),
    "DiscretePhase": ("Singleton", "setup.models.discrete_phase"),
    "Injections": ("Singleton", "setup.models.discrete_phase.injections"),
    "Injection": ("NamedObject", "setup.models.discrete_phase.injections"),
    "VirtualBladeModel": ("Singleton", "setup.models.virtual_blade_model"),
    "Optics": ("Singleton", "setup.models.optics"),
    "Structure": ("Singleton", "setup.models.structure"),
    "Ablation": ("Singleton", "setup.models.ablation"),
    "EChemistry": ("Singleton", "setup.models.echemistry"),
    "Battery": ("Singleton", "setup.models.battery"),
    "SystemCoupling": ("Singleton", "setup.models.system_coupling"),
    "Sofc": ("Singleton", "setup.models.sofc"),
    "Pemfc": ("Singleton", "setup.models.pemfc"),
    "Materials": ("Singleton", "setup.materials"),
    "FluidMaterials": ("Singleton", "setup.materials.fluid"),
    "FluidMaterial": ("NamedObject", "setup.materials.fluid"),
    "SolidMaterials": ("Singleton", "setup.materials.solid"),
    "SolidMaterial": ("NamedObject", "setup.materials.solid"),
    "MixtureMaterials": ("Singleton", "setup.materials.mixture"),
    "MixtureMaterial": ("NamedObject", "setup.materials.mixture"),
    "ParticleMixtureMaterials": ("Singleton", "setup.materials.particle_mixture"),
    "ParticleMixtureMaterial": ("NamedObject", "setup.materials.particle_mixture"),
    "CellZoneConditions": ("Singleton", "setup.cell_zone_conditions"),
    "CellZoneCondition": ("NamedObject", "setup.cell_zone_conditions"),
    "FluidCellZones": ("Singleton", "setup.cell_zone_conditions.fluid"),
    "FluidCellZone": ("NamedObject", "setup.cell_zone_conditions.fluid"),
    "SolidCellZones": ("Singleton", "setup.cell_zone_conditions.solid"),
    "SolidCellZone": ("NamedObject", "setup.cell_zone_conditions.solid"),
    "BoundaryConditions": ("Singleton", "setup.boundary_conditions"),
    "BoundaryCondition": ("NamedObject", "setup.boundary_conditions"),
    "AxisBoundaries": ("Singleton", "setup.boundary_conditions.axis"),
    "AxisBoundary": ("NamedObject", "setup.boundary_conditions.axis"),
    "DegassingBoundaries": ("Singleton", "setup.boundary_conditions.degassing"),
    "DegassingBoundary": ("NamedObject", "setup.boundary_conditions.degassing"),
    "ExhaustFanBoundaries": ("Singleton", "setup.boundary_conditions.exhaust_fan"),
    "ExhaustFanBoundary": ("NamedObject", "setup.boundary_conditions.exhaust_fan"),
    "FanBoundaries": ("Singleton", "setup.boundary_conditions.fan"),
    "FanBoundary": ("NamedObject", "setup.boundary_conditions.fan"),
    "GeometryBoundaries": ("Singleton", "setup.boundary_conditions.geometry"),
    "GeometryBoundary": ("NamedObject", "setup.boundary_conditions.geometry"),
    "InletVentBoundaries": ("Singleton", "setup.boundary_conditions.inlet_vent"),
    "InletVentBoundary": ("NamedObject", "setup.boundary_conditions.inlet_vent"),
    "IntakeFanBoundaries": ("Singleton", "setup.boundary_conditions.intake_fan"),
    "IntakeFanBoundary": ("NamedObject", "setup.boundary_conditions.intake_fan"),
    "InterfaceBoundaries": ("Singleton", "setup.boundary_conditions.interface"),
    "InterfaceBoundary": ("NamedObject", "setup.boundary_conditions.interface"),
    "InteriorBoundaries": ("Singleton", "setup.boundary_conditions.interior"),
    "InteriorBoundary": ("NamedObject", "setup.boundary_conditions.interior"),
    "MassFlowInlets": ("Singleton", "setup.boundary_conditions.mass_flow_inlet"),
    "MassFlowInlet": ("NamedObject", "setup.boundary_conditions.mass_flow_inlet"),
    "MassFlowOutlets": ("Singleton", "setup.boundary_conditions.mass_flow_outlet"),
    "MassFlowOutlet": ("NamedObject", "setup.boundary_conditions.mass_flow_outlet"),
    "NetworkBoundaries": ("Singleton", "setup.boundary_conditions.network"),
    "NetworkBoundary": ("NamedObject", "setup.boundary_conditions.network"),
    "NetworkEndBoundaries": ("Singleton", "setup.boundary_conditions.network_end"),
    "NetworkEndBoundary": ("NamedObject", "setup.boundary_conditions.network_end"),
    "OutflowBoundaries": ("Singleton", "setup.boundary_conditions.outflow"),
    "OutflowBoundary": ("NamedObject", "setup.boundary_conditions.outflow"),
    "OutletVentBoundaries": ("Singleton", "setup.boundary_conditions.outlet_vent"),
    "OutletVentBoundary": ("NamedObject", "setup.boundary_conditions.outlet_vent"),
    "OversetBoundaries": ("Singleton", "setup.boundary_conditions.overset"),
    "OversetBoundary": ("NamedObject", "setup.boundary_conditions.overset"),
    "PeriodicBoundaries": ("Singleton", "setup.boundary_conditions.periodic"),
    "PeriodicBoundary": ("NamedObject", "setup.boundary_conditions.periodic"),
    "PorousJumpBoundaries": ("Singleton", "setup.boundary_conditions.porous_jump"),
    "PorousJumpBoundary": ("NamedObject", "setup.boundary_conditions.porous_jump"),
    "PressureFarFieldBoundaries": (
        "Singleton",
        "setup.boundary_conditions.pressure_far_field",
    ),
    "PressureFarFieldBoundary": (
        "NamedObject",
        "setup.boundary_conditions.pressure_far_field",
    ),
    "PressureInlets": ("Singleton", "setup.boundary_conditions.pressure_inlet"),
    "PressureInlet": ("NamedObject", "setup.boundary_conditions.pressure_inlet"),
    "PressureOutlets": ("Singleton", "setup.boundary_conditions.pressure_outlet"),
    "PressureOutlet": ("NamedObject", "setup.boundary_conditions.pressure_outlet"),
    "RadiatorBoundaries": ("Singleton", "setup.boundary_conditions.radiator"),
    "RadiatorBoundary": ("NamedObject", "setup.boundary_conditions.radiator"),
    "RansLesInterfaceBoundaries": (
        "Singleton",
        "setup.boundary_conditions.rans_les_interface",
    ),
    "RansLesInterfaceBoundary": (
        "NamedObject",
        "setup.boundary_conditions.rans_les_interface",
    ),
    "RecirculationInlets": (
        "Singleton",
        "setup.boundary_conditions.recirculation_inlet",
    ),
    "RecirculationInlet": (
        "NamedObject",
        "setup.boundary_conditions.recirculation_inlet",
    ),
    "RecirculationOutlets": (
        "Singleton",
        "setup.boundary_conditions.recirculation_outlet",
    ),
    "RecirculationOutlet": (
        "NamedObject",
        "setup.boundary_conditions.recirculation_outlet",
    ),
    "ShadowBoundaries": ("Singleton", "setup.boundary_conditions.shadow"),
    "ShadowBoundary": ("NamedObject", "setup.boundary_conditions.shadow"),
    "SymmetryBoundaries": ("Singleton", "setup.boundary_conditions.symmetry"),
    "SymmetryBoundary": ("NamedObject", "setup.boundary_conditions.symmetry"),
    "VelocityInlets": ("Singleton", "setup.boundary_conditions.velocity_inlet"),
    "VelocityInlet": ("NamedObject", "setup.boundary_conditions.velocity_inlet"),
    "WallBoundaries": ("Singleton", "setup.boundary_conditions.wall"),
    "WallBoundary": ("NamedObject", "setup.boundary_conditions.wall"),
    "NonReflectingBoundary": (
        "Singleton",
        "setup.boundary_conditions.non_reflecting_bc",
    ),
    "PerforatedWallBoundary": (
        "Singleton",
        "setup.boundary_conditions.perforated_wall",
    ),
    "MeshInterfaces": (
        "Singleton",
        "setup.mesh_interfaces",
    ),
    "DynamicMesh": (
        "Singleton",
        {
            since(FluentVersion.v251): "setup.dynamic_mesh",
        },
    ),
    "ReferenceValues": ("Singleton", "setup.reference_values"),
    "ReferenceFrames": (
        "Singleton",
        "setup.reference_frames",
    ),
    "ReferenceFrame": (
        "NamedObject",
        "setup.reference_frames",
    ),
    "NamedExpressions": (
        "Singleton",
        "setup.named_expressions",
    ),
    "NamedExpression": (
        "NamedObject",
        "setup.named_expressions",
    ),
    "Solution": ("Singleton", "solution"),
    "Methods": ("Singleton", "solution.methods"),
    "Controls": ("Singleton", "solution.controls"),
    "ReportDefinitions": ("Singleton", "solution.report_definitions"),
    "Monitor": (
        "Singleton",
        "solution.monitor",
    ),
    "Residual": (
        "Singleton",
        "solution.monitor.residual",
    ),
    "ReportFiles": (
        "Singleton",
        "solution.monitor.report_files",
    ),
    "ReportFile": (
        "NamedObject",
        "solution.monitor.report_files",
    ),
    "ReportPlots": (
        "Singleton",
        "solution.monitor.report_plots",
    ),
    "ReportPlot": (
        "NamedObject",
        "solution.monitor.report_plots",
    ),
    "ConvergenceConditions": (
        "Singleton",
        "solution.monitor.convergence_conditions",
    ),
    "CellRegisters": (
        "Singleton",
        "solution.cell_registers",
    ),
    "CellRegister": (
        "NamedObject",
        "solution.cell_registers",
    ),
    "Initialization": ("Singleton", "solution.initialization"),
    "CalculationActivity": (
        "Singleton",
        "solution.calculation_activity",
    ),
    "ExecuteCommands": (
        "Singleton",
        "solution.calculation_activity.execute_commands",
    ),
    "CaseModification": (
        "Singleton",
        "solution.calculation_activity.case_modification",
    ),
    "RunCalculation": ("Singleton", "solution.run_calculation"),
    "Results": ("Singleton", "results"),
    "Surfaces": ("Singleton", "results.surfaces"),
    "PointSurfaces": (
        "Singleton",
        "results.surfaces.point_surface",
    ),
    "PointSurface": (
        "NamedObject",
        "results.surfaces.point_surface",
    ),
    "LineSurfaces": (
        "Singleton",
        "results.surfaces.line_surface",
    ),
    "LineSurface": (
        "NamedObject",
        "results.surfaces.line_surface",
    ),
    "RakeSurfaces": (
        "Singleton",
        "results.surfaces.rake_surface",
    ),
    "RakeSurface": (
        "NamedObject",
        "results.surfaces.rake_surface",
    ),
    "PlaneSurfaces": ("Singleton", "results.surfaces.plane_surface"),
    "PlaneSurface": ("NamedObject", "results.surfaces.plane_surface"),
    "IsoSurfaces": (
        "Singleton",
        "results.surfaces.iso_surface",
    ),
    "IsoSurface": (
        "NamedObject",
        "results.surfaces.iso_surface",
    ),
    "IsoClips": (
        "Singleton",
        "results.surfaces.iso_clip",
    ),
    "IsoClip": (
        "NamedObject",
        "results.surfaces.iso_clip",
    ),
    "ZoneSurfaces": (
        "Singleton",
        "results.surfaces.zone_surface",
    ),
    "ZoneSurface": (
        "NamedObject",
        "results.surfaces.zone_surface",
    ),
    "PartitionSurfaces": (
        "Singleton",
        "results.surfaces.partition_surface",
    ),
    "PartitionSurface": (
        "NamedObject",
        "results.surfaces.partition_surface",
    ),
    "TransformSurfaces": (
        "Singleton",
        "results.surfaces.transform_surface",
    ),
    "TransformSurface": (
        "NamedObject",
        "results.surfaces.transform_surface",
    ),
    "ImprintSurfaces": (
        "Singleton",
        "results.surfaces.imprint_surface",
    ),
    "ImprintSurface": (
        "NamedObject",
        "results.surfaces.imprint_surface",
    ),
    "PlaneSlices": (
        "Singleton",
        "results.surfaces.plane_slice",
    ),
    "PlaneSlice": (
        "NamedObject",
        "results.surfaces.plane_slice",
    ),
    "SphereSlices": (
        "Singleton",
        "results.surfaces.sphere_slice",
    ),
    "SphereSlice": (
        "NamedObject",
        "results.surfaces.sphere_slice",
    ),
    "QuadricSurfaces": (
        "Singleton",
        "results.surfaces.quadric_surface",
    ),
    "QuadricSurface": (
        "NamedObject",
        "results.surfaces.quadric_surface",
    ),
    "SurfaceCells": (
        "Singleton",
        "results.surfaces.surface_cells",
    ),
    "SurfaceCell": (
        "NamedObject",
        "results.surfaces.surface_cells",
    ),
    "ExpressionVolumes": (
        "Singleton",
        {
            since(FluentVersion.v251): "results.surfaces.expression_volume",
        },
    ),
    "ExpressionVolume": (
        "NamedObject",
        {
            since(FluentVersion.v251): "results.surfaces.expression_volume",
        },
    ),
    "GroupSurfaces": (
        "Singleton",
        {
            since(FluentVersion.v251): "results.surfaces.group_surface",
        },
    ),
    "GroupSurface": (
        "NamedObject",
        {
            since(FluentVersion.v251): "results.surfaces.group_surface",
        },
    ),
    "Graphics": ("Singleton", "results.graphics"),
    "Meshes": ("Singleton", "results.graphics.mesh"),
    "Mesh": ("NamedObject", "results.graphics.mesh"),
    "Contours": ("Singleton", "results.graphics.contour"),
    "Contour": ("NamedObject", "results.graphics.contour"),
    "Vectors": ("Singleton", "results.graphics.vector"),
    "Vector": ("NamedObject", "results.graphics.vector"),
    "Pathlines": (
        "Singleton",
        "results.graphics.pathline",
    ),
    "Pathline": (
        "NamedObject",
        "results.graphics.pathline",
    ),
    "ParticleTracks": (
        "Singleton",
        "results.graphics.particle_track",
    ),
    "ParticleTrack": (
        "NamedObject",
        "results.graphics.particle_track",
    ),
    "LICs": ("Singleton", "results.graphics.lic"),
    "LIC": ("NamedObject", "results.graphics.lic"),
    "Plots": (
        "Singleton",
        "results.plot",
    ),
    "XYPlots": (
        "Singleton",
        "results.plot.xy_plot",
    ),
    "XYPlot": (
        "NamedObject",
        "results.plot.xy_plot",
    ),
    "Histogram": (
        "Singleton",
        "results.plot.histogram",
    ),
    "CumulativePlots": (
        "Singleton",
        "results.plot.cumulative_plot",
    ),
    "CumulativePlot": (
        "NamedObject",
        "results.plot.cumulative_plot",
    ),
    "ProfileData": (
        "Singleton",
        "results.plot.profile_data",
    ),
    "InterpolatedData": (
        "Singleton",
        "results.plot.interpolated_data",
    ),
    "Scenes": (
        "Singleton",
        "results.scene",
    ),
    "Scene": (
        "NamedObject",
        "results.scene",
    ),
    "SceneAnimation": (
        "Singleton",
        "results.animations.scene_animation",
    ),
    "Report": (
        "Singleton",
        "results.report",
    ),
    "DiscretePhaseHistogram": (
        "Singleton",
        "results.report.discrete_phase.histogram",
    ),
    "Fluxes": (
        "Singleton",
        "results.report.fluxes",
    ),
    "SurfaceIntegrals": (
        "Singleton",
        "results.report.surface_integrals",
    ),
    "VolumeIntegrals": (
        "Singleton",
        "results.report.volume_integrals",
    ),
    "InputParameters": (
        "Singleton",
        "parameters.input_parameters",
    ),
    "OutputParameters": (
        "Singleton",
        "parameters.output_parameters",
    ),
    "CustomFieldFunctions": (
        "Singleton",
        {
            since(FluentVersion.v251): "results.custom_field_functions",
        },
    ),
    "CustomFieldFunction": (
        "NamedObject",
        {
            since(FluentVersion.v251): "results.custom_field_functions",
        },
    ),
    "CustomVectors": (
        "Singleton",
        "results.custom_vectors",
    ),
    "CustomVector": (
        "NamedObject",
        "results.custom_vectors",
    ),
    "SimulationReports": (
        "Singleton",
        "results.report.simulation_reports",
    ),
    "ParametricStudies": ("Singleton", "parametric_studies"),
    "ParametricStudy": ("NamedObject", "parametric_studies"),
    "DesignPoints": ("Singleton", "parametric_studies.design_points"),
    "DesignPoint": ("NamedObject", "parametric_studies.design_points"),
    "ReadCase": ("Command", "file.read_case"),
    "ReadData": ("Command", "file.read_data"),
    "ReadCaseData": ("Command", "file.read_case_data"),
    "WriteCase": (
        "Command",
        "file.write_case",
    ),
    "WriteData": (
        "Command",
        "file.write_data",
    ),
    "WriteCaseData": (
        "Command",
        "file.write_case_data",
    ),
    "Initialize": ("Command", "solution.initialization.initialize"),
    "Calculate": ("Command", "solution.run_calculation.calculate"),
    "Iterate": ("Command", "solution.run_calculation.iterate"),
    "DualTimeIterate": ("Command", "solution.run_calculation.dual_time_iterate"),
}
