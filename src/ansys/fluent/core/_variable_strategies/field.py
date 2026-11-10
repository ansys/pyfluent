# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
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
Provides a ConversionStrategy for mapping VariableDescriptor to names used in Fluent's field data API.
"""

from ansys.variable_descriptor import (
    MappingConversionStrategy,
    VariableCatalog,
)


class FluentFieldDataNamingStrategy(MappingConversionStrategy):
    """This strategy handles conversion of selected
    VariableCatalog into Fluent's server-side field variable naming conventions.
    """

    _c = VariableCatalog

    _mapping = {
        # pressure
        _c.PRESSURE: "pressure",
        _c.STATIC_PRESSURE: "pressure",
        _c.ABSOLUTE_PRESSURE: "absolute-pressure",
        _c.DYNAMIC_PRESSURE: "dynamic-pressure",
        _c.TOTAL_PRESSURE: "total-pressure",
        _c.PRESSURE_COEFFICIENT: "pressure-coefficient",
        # velocity
        _c.AXIAL_VELOCITY: "axial-velocity",
        _c.CONVECTIVE_COURANT_NUMBER: "cell-convective-courant-number",
        _c.CELL_REYNOLDS_NUMBER: "cell-reynolds-number",
        _c.HYDRODYNAMICAL_HELICITY: "helicity",
        _c.LAMBDA_2_CRITERION: "raw-q-criterion",  # ???
        _c.MESH_VELOCITY: "mesh-velocity",  # ?
        _c.MESH_VELOCITY_X: "mesh-x-velocity",  # TODO
        _c.MESH_VELOCITY_Y: "mesh-y-velocity",  # TODO
        _c.MESH_VELOCITY_Z: "mesh-z-velocity",  # TODO
        _c.MESH_VELOCITY_MAGNITUDE: "MeshVelocityMagnitude",  # TODO
        _c.NORMALIZED_Q_CRITERION: "q-criterion",
        _c.Q_CRITERION: "raw-q-criterion",
        _c.RADIAL_VELOCITY: "radial-velocity",
        _c.TANGENTIAL_VELOCITY: "tangential-velocity",
        _c.VELOCITY: "velocity",
        _c.VELOCITY_X: "x-velocity",
        _c.VELOCITY_Y: "y-velocity",
        _c.VELOCITY_Z: "z-velocity",
        _c.VELOCITY_MAGNITUDE: "velocity-magnitude",
        _c.VELOCITY_ANGLE: "xxx",  # eliminate altogether
        _c.VORTICITY: "vorticity",
        _c.VORTICITY_X: "x-vorticity",
        _c.VORTICITY_Y: "y-vorticity",
        _c.VORTICITY_Z: "z-vorticity",
        _c.VORTICITY_MAGNITUDE: "vorticity-mag",
        # density
        _c.DENSITY: "density",
        _c.MIXTURE_DENSITY: "density-all",
        # "properties"
        _c.DYNAMIC_VISCOSITY: "viscosity-lam",
        _c.PRANDTL_NUMBER: "prandtl-number-lam",
        _c.SPECIFIC_HEAT_CAPACITY: "specific-heat-cp",
        _c.THERMAL_CONDUCTIVITY: "thermal-conductivity",
        # turbulence
        _c.EFFECTIVE_PRANDTL_NUMBER: "prandtl-number-eff",
        _c.EFFECTIVE_THERMAL_CONDUCTIVITY: "thermal-conductivity-eff",
        _c.EFFECTIVE_VISCOSITY: "viscosity-eff",
        _c.PRODUCTION_OF_TURBULENT_KINETIC_ENERGY: "production-of-k",
        _c.SPECIFIC_DISSIPATION_RATE: "specific-diss-rate",
        _c.TURBULENT_DISSIPATION_RATE: "turb-diss-rate",
        _c.TURBULENT_INTENSITY: "turb-intensity",
        _c.TURBULENT_VISCOSITY: "viscosity-turb",
        _c.TURBULENT_VISCOSITY_RATIO: "viscosity-ratio",
        _c.TURBULENT_KINETIC_ENERGY: "turb-kinetic-energy",
        _c.TURBULENT_REYNOLDS_NUMBER: "turb-reynolds-number-rey",
        _c.WALL_Y_PLUS: "y-plus",
        _c.WALL_Y_STAR: "y-star",
        # wall fluxes
        _c.SURFACE_HEAT_TRANSFER_COEFFICIENT: "heat-transfer-coef",
        _c.SKIN_FRICTION_COEFFICIENT: "skin-friction-coef",
        _c.SURFACE_HEAT_FLUX: "heat-flux",
        _c.SURFACE_HEAT_TRANSFER_COEFFICIENT: "heat-transfer-coef-wall",
        _c.SURFACE_NUSSELT_NUMBER: "nusselt-number",
        _c.SURFACE_STANTON_NUMBER: "stanton-number",
        _c.WALL_ADJACENT_HEAT_TRANSFER_COEFFICIENT: "heat-transfer-coef-wall-adj",
        _c.WALL_SHEAR_STRESS: "wall-shear",
        _c.WALL_SHEAR_STRESS_X: "x-wall-shear",
        _c.WALL_SHEAR_STRESS_Y: "y-wall-shear",
        _c.WALL_SHEAR_STRESS_Z: "z-wall-shear",
        # _c.WALL_SHEAR_STRESS_MAGNITUDE: "WallShearStressVector.mag",
        _c.Y_PLUS_BASED_HEAT_TRANSFER_COEFFICIENT: "heat-transfer-coef-yplus",
        # residuals
        _c.MASS_IMBALANCE: "mass-imbalance",
        # derivatives
        _c.PRESSURE_HESSIAN_INDICATOR: "pressure-hessian-indicator",
        _c.STRAIN_RATE: "strain-rate-mag",
        # _c.DVELOCITY_DX: "dVelocitydx",
        _c.DVELOCITY_DX_X: "dx-velocity-dx",
        _c.DVELOCITY_DX_Y: "dy-velocity-dx",
        _c.DVELOCITY_DX_Z: "dz-velocity-dx",
        # _c.DVELOCITY_DX_MAGNITUDE: "dVelocitydx.mag",
        # _c.DVELOCITY_DY: "dVelocitydy",
        _c.DVELOCITY_DY_X: "dx-velocity-dy",
        _c.DVELOCITY_DY_Y: "dy-velocity-dy",
        _c.DVELOCITY_DY_Z: "dz-velocity-dy",
        # _c.DVELOCITY_DY_MAGNITUDE: "dVelocitydy.mag",
        # _c.DVELOCITY_DZ: "dVelocitydz",
        _c.DVELOCITY_DZ_X: "dx-velocity-dz",
        _c.DVELOCITY_DZ_Y: "dy-velocity-dz",
        _c.DVELOCITY_DZ_Z: "dz-velocity-dz",
        # _c.DVELOCITY_DZ_MAGNITUDE: "dVelocitydz.mag",
        # temperature
        _c.SPECIFIC_ENTHALPY: "enthalpy",
        _c.SPECIFIC_ENTROPY: "entropy",
        _c.SPECIFIC_INTERNAL_ENERGY: "internal-energy",
        _c.SPECIFIC_TOTAL_ENERGY: "total-energy",
        _c.TEMPERATURE: "temperature",
        _c.SPECIFIC_TOTAL_ENTHALPY: "total-enthalpy",
        _c.TOTAL_ENTHALPY_DEVIATION: "total-enthalpy-deviation",
        _c.TOTAL_TEMPERATURE: "total-temperature",
        _c.WALL_ADJACENT_TEMPERATURE: "wall-adjacent-temperature",
        _c.WALL_TEMPERATURE: "wall-temperature",
        _c.WALL_TEMPERATURE_THIN: "wall-temp-thin",
        _c.Y_PLUS_BASED_HEAT_TRANSFER_COEFFICIENT: "reference-temperature-at-y+",
        # mesh
        _c.MESH_ANISOTROPIC_ADAPTION_CELLS: "anisotropic-adaption-cells",
        _c.MESH_BOUNDARY_CELL_DISTANCE: "boundary-cell-dist",
        _c.MESH_BOUNDARY_LAYER_CELLS: "boundary-layer-cells",
        _c.MESH_BOUNDARY_NORMAL_DISTANCE: "boundary-normal-dist",
        _c.MESH_BOUNDARY_VOLUME_DISTANCE: "boundary-volume-dist",
        _c.MESH_CELL_EQUIANGLE_SKEW: "cell-equiangle-skew",
        _c.MESH_CELL_EQUIVOLUME_SKEW: "cell-equivolume-skew",
        _c.MESH_CELL_PARENT_INDEX: "cell-parent-index",
        _c.MESH_CELL_REFINE_LEVEL: "cell-refine-level",
        _c.MESH_CELL_VOLUME: "cell-volume",
        _c.MESH_CELL_VOLUME_CHANGE: "cell-volume-change",
        _c.MESH_ELEMENT_ASPECT_RATIO: "aspect-ratio",
        _c.MESH_ELEMENT_WALL_DISTANCE: "cell-wall-distance",
        _c.MESH_FACE_AREA_MAGNITUDE: "face-area-magnitude",
        _c.MESH_FACE_HANDEDNESS: "face-handedness",
        _c.MESH_INTERFACE_OVERLAP_FRACTION: "interface-overlap-fraction",
        _c.MESH_MARK_POOR_ELEMENTS: "mark-poor-elements",
        # _c.POSITION: "Position", ???
        _c.POSITION_X: "x-coordinate",
        _c.POSITION_Y: "y-coordinate",
        _c.POSITION_Z: "z-coordinate",
        # _c.POSITION_MAGNITUDE: "Position.mag", ???
        _c.MESH_SMOOTHED_CELL_REFINE_LEVEL: "smoothed-cell-refine-level",
        _c.MESH_X_FACE_AREA: "x-face-area",
        _c.MESH_Y_FACE_AREA: "y-face-area",
        _c.MESH_Z_FACE_AREA: "z-face-area",
        _c.MESH_ACTIVE_CELL_PARTITION: "cell-partition-active",
        _c.MESH_CELL_ELEMENT_TYPE: "cell-element-type",
        _c.MESH_CELL_ID: "cell-id",
        _c.MESH_CELL_WEIGHT: "cell-weight",
        _c.MESH_CELL_ZONE_INDEX: "cell-zone",
        _c.MESH_CELL_ZONE_TYPE: "cell-type",
        _c.MESH_PARTITION_NEIGHBOURS: "partition-neighbors",
        _c.MESH_STORED_CELL_PARTITION: "cell-partition-stored",
    }
