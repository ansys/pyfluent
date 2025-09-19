import ansys.fluent.core as pyfluent

meshing = pyfluent.launch_fluent(mode="meshing")
print(meshing.file)
