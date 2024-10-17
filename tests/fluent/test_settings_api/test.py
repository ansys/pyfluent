from ansys.fluent.core.examples import download_file

case_name = download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
solver.settings.file.read_case(file_name=case_name)
viscous_settings = solver.settings.setup.models.viscous
assert viscous_settings.model() == "k-omega"
allowed_values = viscous_settings.model.allowed_values()
assert "k-epsilon" in allowed_values
assert len(allowed_values) > 5
viscous_settings.model = "k-epsilon"
assert viscous_settings.model() == "k-epsilon"
exit()
