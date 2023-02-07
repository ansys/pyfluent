import ansys.fluent.core as pyfluent

solver_light = pyfluent.launch_fluent(show_gui=True)
solver_light.file.read(file_type="case", file_name="elbow.cas.h5", lightweight_setup=True)
solver_light.setup.models.energy.enabled = False
print(solver_light.setup.models.energy())
state = solver_light._root.get_state()

solver = pyfluent.launch_fluent(show_gui=True)
solver.file.read(file_type="case", file_name="elbow.cas.h5")
solver_light.build_from_fluent_connection(solver.fluent_connection)
solver_light._root.set_state(state)