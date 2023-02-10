import ansys.fluent.core as pyfluent

pyfluent.USE_LIGHT_IO = True
solver = pyfluent.launch_fluent(show_gui=True)
solver.read_case(file_name="elbow.cas.h5")
solver.setup.models.energy.enabled = False
