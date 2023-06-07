import os

os.environ["PYFLUENT_FLUENT_ROOT"] = r"C:\ANSYSDev\ANSYSDev\vNNN\fluent"

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples

import_filename = examples.download_file("mixing_elbow.msh.h5", "pyfluent/mixing_elbow")
solver = pyfluent.launch_fluent(mode="solver")
solver.file.read(file_type="case", file_name=import_filename)

svar_info = solver.svar_info
svar_data = solver.svar_data

zones_info = svar_info.get_zones_info()

assert zones_info.domains == ["mixture"]

assert zones_info.zones == [
    "symmetry-xyplane",
    "hot-inlet",
    "cold-inlet",
    "outlet",
    "wall-inlet",
    "wall-elbow",
    "elbow-fluid",
    "interior--elbow-fluid",
]

zone_info = zones_info["wall-inlet"]

assert zone_info.name == "wall-inlet"

assert zone_info.count == 268

assert zone_info.zone_id == 33

assert zone_info.zone_type == "wall"

svars_info_wall_fluid = svar_info.get_svars_info(
    zone_names=["wall", "fluid"], domain_name="mixture"
)

assert svars_info_wall_fluid.svars == [
    "SV_CENTROID",
    "SV_D",
    "SV_H",
    "SV_K",
    "SV_P",
    "SV_T",
    "SV_U",
    "SV_V",
    "SV_W",
]

svar_info_centroid = svars_info_wall_fluid["SV_CENTROID"]

# svar_info_centroid
# name: SV_CENTROID
# dimension: 3
# field_type: <

assert svar_info_centroid.name == "SV_CENTROID"

assert svar_info_centroid.dimension == 3

# assert svar_info_centroid.field_type == 'numpy.float64'

sv_t_wall_fluid = svar_data.get_svar_data(
    svar_name="SV_T", zone_names=["fluid", "wall"], domain_name="mixture"
)
assert sv_t_wall_fluid.domain == "mixture"

assert sv_t_wall_fluid.zones == ["fluid", "wall"]

fluid_temp = sv_t_wall_fluid["fluid"]
assert fluid_temp.size == 13852
assert fluid_temp.dtype == "float64"
# assert fluid_temp == array([600., 600., 600., ..., 600., 600., 600.])

wall_temp_array = svar_data.get_array("SV_T", "wall", "mixture")
fluid_temp_array = svar_data.get_array("SV_T", "fluid", "mixture")
wall_temp_array[:] = 500
fluid_temp_array[:] = 600
zone_names_to_svar_data = {"wall": wall_temp_array, "fluid": fluid_temp_array}
svar_data.set_svar_data(
    svar_name="SV_T",
    zone_names_to_svar_data=zone_names_to_svar_data,
    domain_name="mixture",
)
