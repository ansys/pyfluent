#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .species import species
from .reactions import reactions
from .reaction_mechs import reaction_mechs
from .density import density
from .specific_heat import specific_heat
from .thermal_conductivity import thermal_conductivity
from .viscosity import viscosity
from .molecular_weight import molecular_weight
from .mass_diffusivity import mass_diffusivity
from .thermal_diffusivity import thermal_diffusivity
from .formation_enthalpy import formation_enthalpy
from .formation_entropy import formation_entropy
from .characteristic_vibrational_temperature import characteristic_vibrational_temperature
from .reference_temperature import reference_temperature
from .lennard_jones_length import lennard_jones_length
from .lennard_jones_energy import lennard_jones_energy
from .thermal_accom_coefficient import thermal_accom_coefficient
from .velocity_accom_coefficient import velocity_accom_coefficient
from .absorption_coefficient import absorption_coefficient
from .scattering_coefficient import scattering_coefficient
from .scattering_phase_function import scattering_phase_function
from .therm_exp_coeff import therm_exp_coeff
from .premix_unburnt_density import premix_unburnt_density
from .premix_unburnt_temp import premix_unburnt_temp
from .premix_adiabatic_temp import premix_adiabatic_temp
from .premix_unburnt_cp import premix_unburnt_cp
from .premix_heat_trans_coeff import premix_heat_trans_coeff
from .premix_laminar_speed import premix_laminar_speed
from .premix_laminar_thickness import premix_laminar_thickness
from .premix_critical_strain import premix_critical_strain
from .premix_heat_of_comb import premix_heat_of_comb
from .premix_unburnt_fuel_mf import premix_unburnt_fuel_mf
from .refractive_index import refractive_index
from .latent_heat import latent_heat
from .thermophoretic_co import thermophoretic_co
from .vaporization_temperature import vaporization_temperature
from .boiling_point import boiling_point
from .volatile_fraction import volatile_fraction
from .binary_diffusivity import binary_diffusivity
from .diffusivity_reference_pressure import diffusivity_reference_pressure
from .vapor_pressure import vapor_pressure
from .degrees_of_freedom import degrees_of_freedom
from .emissivity import emissivity
from .scattering_factor import scattering_factor
from .heat_of_pyrolysis import heat_of_pyrolysis
from .swelling_coefficient import swelling_coefficient
from .burn_stoichiometry import burn_stoichiometry
from .combustible_fraction import combustible_fraction
from .burn_hreact import burn_hreact
from .burn_hreact_fraction import burn_hreact_fraction
from .devolatilization_model import devolatilization_model
from .combustion_model import combustion_model
from .averaging_coefficient_t import averaging_coefficient_t
from .averaging_coefficient_y import averaging_coefficient_y
from .vaporization_model import vaporization_model
from .thermolysis_model import thermolysis_model
from .melting_heat import melting_heat
from .tsolidus import tsolidus
from .tliqidus import tliqidus
from .tmelt import tmelt
from .liquidus_slope import liquidus_slope
from .partition_coeff import partition_coeff
from .eutectic_mf import eutectic_mf
from .eutectic_temp import eutectic_temp
from .solut_exp_coeff import solut_exp_coeff
from .solid_diffusion import solid_diffusion
from .uds_diffusivity import uds_diffusivity
from .dpm_surften import dpm_surften
from .electric_conductivity import electric_conductivity
from .dual_electric_conductivity import dual_electric_conductivity
from .lithium_diffusivity import lithium_diffusivity
from .magnetic_permeability import magnetic_permeability
from .charge_density import charge_density
from .charge import charge
from .speed_of_sound import speed_of_sound
from .species_phase import species_phase
from .vp_equilib import vp_equilib
from .critical_temperature import critical_temperature
from .critical_pressure import critical_pressure
from .critical_volume import critical_volume
from .acentric_factor import acentric_factor
from .saturation_pressure import saturation_pressure
from .struct_youngs_modulus import struct_youngs_modulus
from .struct_poisson_ratio import struct_poisson_ratio
from .struct_start_temperature import struct_start_temperature
from .struct_thermal_expansion import struct_thermal_expansion
from .atomic_number import atomic_number
from .struct_damping_alpha import struct_damping_alpha
from .struct_damping_beta import struct_damping_beta
from .mixture_species import mixture_species
class mixture_child(Group):
    """
    'child_object_type' of mixture
    """

    fluent_name = "child-object-type"

    child_names = \
        ['species', 'reactions', 'reaction_mechs', 'density', 'specific_heat',
         'thermal_conductivity', 'viscosity', 'molecular_weight',
         'mass_diffusivity', 'thermal_diffusivity', 'formation_enthalpy',
         'formation_entropy', 'characteristic_vibrational_temperature',
         'reference_temperature', 'lennard_jones_length',
         'lennard_jones_energy', 'thermal_accom_coefficient',
         'velocity_accom_coefficient', 'absorption_coefficient',
         'scattering_coefficient', 'scattering_phase_function',
         'therm_exp_coeff', 'premix_unburnt_density', 'premix_unburnt_temp',
         'premix_adiabatic_temp', 'premix_unburnt_cp',
         'premix_heat_trans_coeff', 'premix_laminar_speed',
         'premix_laminar_thickness', 'premix_critical_strain',
         'premix_heat_of_comb', 'premix_unburnt_fuel_mf', 'refractive_index',
         'latent_heat', 'thermophoretic_co', 'vaporization_temperature',
         'boiling_point', 'volatile_fraction', 'binary_diffusivity',
         'diffusivity_reference_pressure', 'vapor_pressure',
         'degrees_of_freedom', 'emissivity', 'scattering_factor',
         'heat_of_pyrolysis', 'swelling_coefficient', 'burn_stoichiometry',
         'combustible_fraction', 'burn_hreact', 'burn_hreact_fraction',
         'devolatilization_model', 'combustion_model',
         'averaging_coefficient_t', 'averaging_coefficient_y',
         'vaporization_model', 'thermolysis_model', 'melting_heat',
         'tsolidus', 'tliqidus', 'tmelt', 'liquidus_slope', 'partition_coeff',
         'eutectic_mf', 'eutectic_temp', 'solut_exp_coeff', 'solid_diffusion',
         'uds_diffusivity', 'dpm_surften', 'electric_conductivity',
         'dual_electric_conductivity', 'lithium_diffusivity',
         'magnetic_permeability', 'charge_density', 'charge',
         'speed_of_sound', 'species_phase', 'vp_equilib',
         'critical_temperature', 'critical_pressure', 'critical_volume',
         'acentric_factor', 'saturation_pressure', 'struct_youngs_modulus',
         'struct_poisson_ratio', 'struct_start_temperature',
         'struct_thermal_expansion', 'atomic_number', 'struct_damping_alpha',
         'struct_damping_beta', 'mixture_species']

    species: species = species
    """
    species child of mixture_child
    """
    reactions: reactions = reactions
    """
    reactions child of mixture_child
    """
    reaction_mechs: reaction_mechs = reaction_mechs
    """
    reaction_mechs child of mixture_child
    """
    density: density = density
    """
    density child of mixture_child
    """
    specific_heat: specific_heat = specific_heat
    """
    specific_heat child of mixture_child
    """
    thermal_conductivity: thermal_conductivity = thermal_conductivity
    """
    thermal_conductivity child of mixture_child
    """
    viscosity: viscosity = viscosity
    """
    viscosity child of mixture_child
    """
    molecular_weight: molecular_weight = molecular_weight
    """
    molecular_weight child of mixture_child
    """
    mass_diffusivity: mass_diffusivity = mass_diffusivity
    """
    mass_diffusivity child of mixture_child
    """
    thermal_diffusivity: thermal_diffusivity = thermal_diffusivity
    """
    thermal_diffusivity child of mixture_child
    """
    formation_enthalpy: formation_enthalpy = formation_enthalpy
    """
    formation_enthalpy child of mixture_child
    """
    formation_entropy: formation_entropy = formation_entropy
    """
    formation_entropy child of mixture_child
    """
    characteristic_vibrational_temperature: characteristic_vibrational_temperature = characteristic_vibrational_temperature
    """
    characteristic_vibrational_temperature child of mixture_child
    """
    reference_temperature: reference_temperature = reference_temperature
    """
    reference_temperature child of mixture_child
    """
    lennard_jones_length: lennard_jones_length = lennard_jones_length
    """
    lennard_jones_length child of mixture_child
    """
    lennard_jones_energy: lennard_jones_energy = lennard_jones_energy
    """
    lennard_jones_energy child of mixture_child
    """
    thermal_accom_coefficient: thermal_accom_coefficient = thermal_accom_coefficient
    """
    thermal_accom_coefficient child of mixture_child
    """
    velocity_accom_coefficient: velocity_accom_coefficient = velocity_accom_coefficient
    """
    velocity_accom_coefficient child of mixture_child
    """
    absorption_coefficient: absorption_coefficient = absorption_coefficient
    """
    absorption_coefficient child of mixture_child
    """
    scattering_coefficient: scattering_coefficient = scattering_coefficient
    """
    scattering_coefficient child of mixture_child
    """
    scattering_phase_function: scattering_phase_function = scattering_phase_function
    """
    scattering_phase_function child of mixture_child
    """
    therm_exp_coeff: therm_exp_coeff = therm_exp_coeff
    """
    therm_exp_coeff child of mixture_child
    """
    premix_unburnt_density: premix_unburnt_density = premix_unburnt_density
    """
    premix_unburnt_density child of mixture_child
    """
    premix_unburnt_temp: premix_unburnt_temp = premix_unburnt_temp
    """
    premix_unburnt_temp child of mixture_child
    """
    premix_adiabatic_temp: premix_adiabatic_temp = premix_adiabatic_temp
    """
    premix_adiabatic_temp child of mixture_child
    """
    premix_unburnt_cp: premix_unburnt_cp = premix_unburnt_cp
    """
    premix_unburnt_cp child of mixture_child
    """
    premix_heat_trans_coeff: premix_heat_trans_coeff = premix_heat_trans_coeff
    """
    premix_heat_trans_coeff child of mixture_child
    """
    premix_laminar_speed: premix_laminar_speed = premix_laminar_speed
    """
    premix_laminar_speed child of mixture_child
    """
    premix_laminar_thickness: premix_laminar_thickness = premix_laminar_thickness
    """
    premix_laminar_thickness child of mixture_child
    """
    premix_critical_strain: premix_critical_strain = premix_critical_strain
    """
    premix_critical_strain child of mixture_child
    """
    premix_heat_of_comb: premix_heat_of_comb = premix_heat_of_comb
    """
    premix_heat_of_comb child of mixture_child
    """
    premix_unburnt_fuel_mf: premix_unburnt_fuel_mf = premix_unburnt_fuel_mf
    """
    premix_unburnt_fuel_mf child of mixture_child
    """
    refractive_index: refractive_index = refractive_index
    """
    refractive_index child of mixture_child
    """
    latent_heat: latent_heat = latent_heat
    """
    latent_heat child of mixture_child
    """
    thermophoretic_co: thermophoretic_co = thermophoretic_co
    """
    thermophoretic_co child of mixture_child
    """
    vaporization_temperature: vaporization_temperature = vaporization_temperature
    """
    vaporization_temperature child of mixture_child
    """
    boiling_point: boiling_point = boiling_point
    """
    boiling_point child of mixture_child
    """
    volatile_fraction: volatile_fraction = volatile_fraction
    """
    volatile_fraction child of mixture_child
    """
    binary_diffusivity: binary_diffusivity = binary_diffusivity
    """
    binary_diffusivity child of mixture_child
    """
    diffusivity_reference_pressure: diffusivity_reference_pressure = diffusivity_reference_pressure
    """
    diffusivity_reference_pressure child of mixture_child
    """
    vapor_pressure: vapor_pressure = vapor_pressure
    """
    vapor_pressure child of mixture_child
    """
    degrees_of_freedom: degrees_of_freedom = degrees_of_freedom
    """
    degrees_of_freedom child of mixture_child
    """
    emissivity: emissivity = emissivity
    """
    emissivity child of mixture_child
    """
    scattering_factor: scattering_factor = scattering_factor
    """
    scattering_factor child of mixture_child
    """
    heat_of_pyrolysis: heat_of_pyrolysis = heat_of_pyrolysis
    """
    heat_of_pyrolysis child of mixture_child
    """
    swelling_coefficient: swelling_coefficient = swelling_coefficient
    """
    swelling_coefficient child of mixture_child
    """
    burn_stoichiometry: burn_stoichiometry = burn_stoichiometry
    """
    burn_stoichiometry child of mixture_child
    """
    combustible_fraction: combustible_fraction = combustible_fraction
    """
    combustible_fraction child of mixture_child
    """
    burn_hreact: burn_hreact = burn_hreact
    """
    burn_hreact child of mixture_child
    """
    burn_hreact_fraction: burn_hreact_fraction = burn_hreact_fraction
    """
    burn_hreact_fraction child of mixture_child
    """
    devolatilization_model: devolatilization_model = devolatilization_model
    """
    devolatilization_model child of mixture_child
    """
    combustion_model: combustion_model = combustion_model
    """
    combustion_model child of mixture_child
    """
    averaging_coefficient_t: averaging_coefficient_t = averaging_coefficient_t
    """
    averaging_coefficient_t child of mixture_child
    """
    averaging_coefficient_y: averaging_coefficient_y = averaging_coefficient_y
    """
    averaging_coefficient_y child of mixture_child
    """
    vaporization_model: vaporization_model = vaporization_model
    """
    vaporization_model child of mixture_child
    """
    thermolysis_model: thermolysis_model = thermolysis_model
    """
    thermolysis_model child of mixture_child
    """
    melting_heat: melting_heat = melting_heat
    """
    melting_heat child of mixture_child
    """
    tsolidus: tsolidus = tsolidus
    """
    tsolidus child of mixture_child
    """
    tliqidus: tliqidus = tliqidus
    """
    tliqidus child of mixture_child
    """
    tmelt: tmelt = tmelt
    """
    tmelt child of mixture_child
    """
    liquidus_slope: liquidus_slope = liquidus_slope
    """
    liquidus_slope child of mixture_child
    """
    partition_coeff: partition_coeff = partition_coeff
    """
    partition_coeff child of mixture_child
    """
    eutectic_mf: eutectic_mf = eutectic_mf
    """
    eutectic_mf child of mixture_child
    """
    eutectic_temp: eutectic_temp = eutectic_temp
    """
    eutectic_temp child of mixture_child
    """
    solut_exp_coeff: solut_exp_coeff = solut_exp_coeff
    """
    solut_exp_coeff child of mixture_child
    """
    solid_diffusion: solid_diffusion = solid_diffusion
    """
    solid_diffusion child of mixture_child
    """
    uds_diffusivity: uds_diffusivity = uds_diffusivity
    """
    uds_diffusivity child of mixture_child
    """
    dpm_surften: dpm_surften = dpm_surften
    """
    dpm_surften child of mixture_child
    """
    electric_conductivity: electric_conductivity = electric_conductivity
    """
    electric_conductivity child of mixture_child
    """
    dual_electric_conductivity: dual_electric_conductivity = dual_electric_conductivity
    """
    dual_electric_conductivity child of mixture_child
    """
    lithium_diffusivity: lithium_diffusivity = lithium_diffusivity
    """
    lithium_diffusivity child of mixture_child
    """
    magnetic_permeability: magnetic_permeability = magnetic_permeability
    """
    magnetic_permeability child of mixture_child
    """
    charge_density: charge_density = charge_density
    """
    charge_density child of mixture_child
    """
    charge: charge = charge
    """
    charge child of mixture_child
    """
    speed_of_sound: speed_of_sound = speed_of_sound
    """
    speed_of_sound child of mixture_child
    """
    species_phase: species_phase = species_phase
    """
    species_phase child of mixture_child
    """
    vp_equilib: vp_equilib = vp_equilib
    """
    vp_equilib child of mixture_child
    """
    critical_temperature: critical_temperature = critical_temperature
    """
    critical_temperature child of mixture_child
    """
    critical_pressure: critical_pressure = critical_pressure
    """
    critical_pressure child of mixture_child
    """
    critical_volume: critical_volume = critical_volume
    """
    critical_volume child of mixture_child
    """
    acentric_factor: acentric_factor = acentric_factor
    """
    acentric_factor child of mixture_child
    """
    saturation_pressure: saturation_pressure = saturation_pressure
    """
    saturation_pressure child of mixture_child
    """
    struct_youngs_modulus: struct_youngs_modulus = struct_youngs_modulus
    """
    struct_youngs_modulus child of mixture_child
    """
    struct_poisson_ratio: struct_poisson_ratio = struct_poisson_ratio
    """
    struct_poisson_ratio child of mixture_child
    """
    struct_start_temperature: struct_start_temperature = struct_start_temperature
    """
    struct_start_temperature child of mixture_child
    """
    struct_thermal_expansion: struct_thermal_expansion = struct_thermal_expansion
    """
    struct_thermal_expansion child of mixture_child
    """
    atomic_number: atomic_number = atomic_number
    """
    atomic_number child of mixture_child
    """
    struct_damping_alpha: struct_damping_alpha = struct_damping_alpha
    """
    struct_damping_alpha child of mixture_child
    """
    struct_damping_beta: struct_damping_beta = struct_damping_beta
    """
    struct_damping_beta child of mixture_child
    """
    mixture_species: mixture_species = mixture_species
    """
    mixture_species child of mixture_child
    """
