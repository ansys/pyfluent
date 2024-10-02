from ansys.fluent.core.examples import download_file

geometry_file = download_file("mixing_elbow.pmdb", "pyfluent/mixing_elbow")
watertight = meshing.watertight()
watertight.import_geometry.file_name.set_state(geometry_file)
assert watertight.import_geometry.length_unit() == "mm"
watertight.import_geometry.length_unit = "in"
assert watertight.import_geometry.length_unit() == "in"
assert watertight.import_geometry.cad_import_options.feature_angle() == 40.0
watertight.import_geometry.cad_import_options.feature_angle.set_state(25.0)
assert watertight.import_geometry.cad_import_options.feature_angle() == 25.0
assert watertight.import_geometry.cad_import_options.one_zone_per.allowed_values() == [
    "body",
    "face",
    "object",
]
assert watertight.import_geometry.cad_import_options.one_zone_per() == "body"
watertight.import_geometry.cad_import_options.one_zone_per = "face"
assert watertight.import_geometry.cad_import_options.one_zone_per() == "face"
watertight.import_geometry()
exit()
