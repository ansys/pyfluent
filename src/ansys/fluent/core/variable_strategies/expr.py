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

"""
Provides a ConversionStrategy for mapping VariableDescriptor to variable names used in Fluent expressions.
"""

from ansys.units.variable_descriptor import (
    MappingConversionStrategy,
    VariableCatalog,
)


class FluentExprNamingStrategy(MappingConversionStrategy):
    """This strategy handles conversion of selected VariableCatalog into Fluent's
    server-side expression variable naming conventions.
    """

    _c = VariableCatalog

    _mapping = {
        # pressure
        _c.PRESSURE: "StaticPressure",
        _c.STATIC_PRESSURE: "StaticPressure",
        _c.ABSOLUTE_PRESSURE: "AbsolutePressure",
        _c.DYNAMIC_PRESSURE: "DynamicPressure",
        _c.TOTAL_PRESSURE: "TotalPressure",
        _c.PRESSURE_COEFFICIENT: "PressureCoefficient",
        # velocity
        _c.AXIAL_VELOCITY: "AxialVelocity",
        _c.CONVECTIVE_COURANT_NUMBER: "ElementConvectionCourantNumber",
        _c.CELL_REYNOLDS_NUMBER: "ElementReynoldsNumber",
        _c.fluent.HELICITY: "Helicity",
        _c.fluent.LAMBDA_2_CRITERION: "Lambda2Criterion",
        _c.MESH_VELOCITY: "MeshVelocity",
        _c.MESH_VELOCITY_X: "MeshVelocity.x",
        _c.MESH_VELOCITY_Y: "MeshVelocity.y",
        _c.MESH_VELOCITY_Z: "MeshVelocity.z",
        _c.MESH_VELOCITY_MAGNITUDE: "MeshVelocityMagnitude",
        _c.NORMALIZED_Q_CRITERION: "QCriterionNormalized",
        _c.Q_CRITERION: "QCriterionRaw",
        _c.RADIAL_VELOCITY: "RadialVelocity",
        _c.TANGENTIAL_VELOCITY: "TangentialVelocity",
        _c.VELOCITY: "Velocity",
        _c.VELOCITY_X: "Velocity.x",
        _c.VELOCITY_Y: "Velocity.y",
        _c.VELOCITY_Z: "Velocity.z",
        _c.VELOCITY_MAGNITUDE: "VelocityMagnitude",
        _c.fluent.VELOCITY_ANGLE: "VelocityAngle",
        _c.VORTICITY: "Vorticity",
        _c.VORTICITY_X: "Vorticity.x",
        _c.VORTICITY_Y: "Vorticity.y",
        _c.VORTICITY_Z: "Vorticity.z",
        _c.VORTICITY_MAGNITUDE: "VorticityMagnitude",
        # density
        _c.DENSITY: "Density",
        _c.fluent.DENSITY_ALL: "DensityAll",
        # "properties"
        _c.DYNAMIC_VISCOSITY: "DynamicViscosity",
        _c.PRANDTL_NUMBER: "PrandtlNumber",
        _c.SPECIFIC_HEAT_CAPACITY: "SpecificHeatCapacity",
        _c.THERMAL_CONDUCTIVITY: "ThermalConductivity",
        # turbulence
        _c.EFFECTIVE_PRANDTL_NUMBER: "EffectivePrandtlNumber",
        _c.EFFECTIVE_THERMAL_CONDUCTIVITY: "EffectiveThermalConductivity",
        _c.EFFECTIVE_VISCOSITY: "EffectiveViscosity",
        _c.PRODUCTION_OF_TURBULENT_KINETIC_ENERGY: "Productionofk",
        _c.SPECIFIC_DISSIPATION_RATE: "SpecificDissipationRateOmega",
        _c.TURBULENT_DISSIPATION_RATE: "TurbulenceDissipationRate",
        _c.TURBULENT_INTENSITY: "TurbulenceIntensity",
        _c.TURBULENT_VISCOSITY: "TurbulenceViscosity",
        _c.TURBULENT_VISCOSITY_RATIO: "TurbulenceViscosityRatio",
        _c.TURBULENT_KINETIC_ENERGY: "TurbulentKineticEnergyk",
        _c.TURBULENT_REYNOLDS_NUMBER: "TurbulentReynoldsNumberRe_y",
        _c.WALL_Y_PLUS: "WallYplus",
        _c.WALL_Y_STAR: "WallYstar",
        # wall fluxes
        _c.SURFACE_HEAT_TRANSFER_COEFFICIENT: "HeatTransferCoefficient",
        _c.SKIN_FRICTION_COEFFICIENT: "SkinFrictionCoefficient",
        _c.SURFACE_HEAT_FLUX: "SurfaceHeatFlux",
        _c.SURFACE_HEAT_TRANSFER_COEFFICIENT: "SurfaceHeatTransferCoefficient",
        _c.SURFACE_NUSSELT_NUMBER: "SurfaceNusseltNumber",
        _c.SURFACE_STANTON_NUMBER: "SurfaceStantonNumber",
        _c.WALL_ADJACENT_HEAT_TRANSFER_COEFFICIENT: "WallAdjacentHeatTransferCoef",
        _c.WALL_SHEAR_STRESS: "WallShearStressVector",
        _c.WALL_SHEAR_STRESS_X: "WallShearStressVector.x",
        _c.WALL_SHEAR_STRESS_Y: "WallShearStressVector.y",
        _c.WALL_SHEAR_STRESS_Z: "WallShearStressVector.z",
        _c.WALL_SHEAR_STRESS_MAGNITUDE: "WallShearStressVector.mag",
        _c.fluent.Y_PLUS_BASED_HEAT_TRANSFER_COEFFICIENT: "YplusBasedHeatTranCoef",
        # residuals
        _c.fluent.MASS_IMBALANCE: "MassImbalance",
        # derivatives
        _c.fluent.PRESSURE_HESSIAN_INDICATOR: "PressureHessianIndicator",
        _c.STRAIN_RATE: "StrainRate",
        _c.fluent.DVELOCITY_DX: "dVelocitydx",
        _c.fluent.DVELOCITY_DX_X: "dVelocitydx.x",
        _c.fluent.DVELOCITY_DX_Y: "dVelocitydx.y",
        _c.fluent.DVELOCITY_DX_Z: "dVelocitydx.z",
        _c.fluent.DVELOCITY_DX_MAGNITUDE: "dVelocitydx.mag",
        _c.fluent.DVELOCITY_DY: "dVelocitydy",
        _c.fluent.DVELOCITY_DY_X: "dVelocitydy.x",
        _c.fluent.DVELOCITY_DY_Y: "dVelocitydy.y",
        _c.fluent.DVELOCITY_DY_Z: "dVelocitydy.z",
        _c.fluent.DVELOCITY_DY_MAGNITUDE: "dVelocitydy.mag",
        _c.fluent.DVELOCITY_DZ: "dVelocitydz",
        _c.fluent.DVELOCITY_DZ_X: "dVelocitydz.x",
        _c.fluent.DVELOCITY_DZ_Y: "dVelocitydz.y",
        _c.fluent.DVELOCITY_DZ_Z: "dVelocitydz.z",
        _c.fluent.DVELOCITY_DZ_MAGNITUDE: "dVelocitydz.mag",
        # temperature
        _c.SPECIFIC_ENTHALPY: "SpecificEnthalpy",
        _c.SPECIFIC_ENTROPY: "SpecificEntropy",
        _c.SPECIFIC_INTERNAL_ENERGY: "SpecificInternalEnergy",
        _c.SPECIFIC_TOTAL_ENERGY: "SpecificTotalEnergy",
        _c.TEMPERATURE: "StaticTemperature",
        _c.SPECIFIC_TOTAL_ENTHALPY: "SpecificTotalEnthalpy",
        _c.fluent.TOTAL_ENTHALPY_DEVIATION: "TotalEnthalpyDeviation",
        _c.TOTAL_TEMPERATURE: "TotalTemperature",
        _c.WALL_ADJACENT_TEMPERATURE: "WallAdjacentTemperature",
        _c.WALL_TEMPERATURE: "WallTemperature",
        _c.WALL_TEMPERATURE_THIN: "WallTemperatureThin",
        _c.fluent.Y_PLUS_BASED_HEAT_TRANSFER_COEFFICIENT: "YplusBasedHeatTranRefTemperature",
        # mesh
        _c.mesh.ANISOTROPIC_ADAPTION_CELLS: "AnisotropicAdaptionCells",
        _c.mesh.BOUNDARY_CELL_DISTANCE: "BoundaryCellDistance",
        _c.mesh.BOUNDARY_LAYER_CELLS: "BoundaryLayerCells",
        _c.mesh.BOUNDARY_NORMAL_DISTANCE: "BoundaryNormalDistance",
        _c.mesh.BOUNDARY_VOLUME_DISTANCE: "BoundaryVolumeDistance",
        _c.mesh.CELL_EQUIANGLE_SKEW: "CellEquiangleSkew",
        _c.mesh.CELL_EQUIVOLUME_SKEW: "CellEquivolumeSkew",
        _c.mesh.CELL_PARENT_INDEX: "CellParentIndex",
        _c.mesh.CELL_REFINE_LEVEL: "CellRefineLevel",
        _c.mesh.CELL_VOLUME: "CellVolume",
        _c.mesh.CELL_VOLUME_CHANGE: "CellVolumeChange",
        _c.mesh.ELEMENT_ASPECT_RATIO: "ElementAspectRatio",
        _c.mesh.ELEMENT_WALL_DISTANCE: "ElementWallDistance",
        _c.mesh.FACE_AREA_MAGNITUDE: "FaceAreaMagnitude",
        _c.mesh.FACE_HANDEDNESS: "FaceHandedness",
        _c.mesh.INTERFACE_OVERLAP_FRACTION: "InterfaceOverlapFraction",
        _c.mesh.MARK_POOR_ELEMENTS: "MarkPoorElements",
        _c.POSITION: "Position",
        _c.POSITION_X: "Position.x",
        _c.POSITION_Y: "Position.y",
        _c.POSITION_Z: "Position.z",
        _c.POSITION_MAGNITUDE: "Position.mag",
        _c.mesh.SMOOTHED_CELL_REFINE_LEVEL: "SmoothedCellRefineLevel",
        _c.mesh.X_FACE_AREA: "XFaceArea",
        _c.mesh.Y_FACE_AREA: "YFaceArea",
        _c.mesh.Z_FACE_AREA: "ZFaceArea",
        _c.mesh.ACTIVE_CELL_PARTITION: "ActiveElementPartition",
        _c.mesh.CELL_ELEMENT_TYPE: "CellElementType",
        _c.mesh.CELL_ID: "CellId",
        _c.mesh.CELL_WEIGHT: "CellWeight",
        _c.mesh.CELL_ZONE_INDEX: "CellZoneIndex",
        _c.mesh.CELL_ZONE_TYPE: "CellZoneType",
        _c.mesh.PARTITION_NEIGHBOURS: "PartitionNeighbors",
        _c.mesh.STORED_CELL_PARTITIION: "StoredElementPartition",
    }
