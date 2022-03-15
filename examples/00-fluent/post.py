#import module
import ansys.fluent.postprocessing.pyvista as pv


#get the graphics objects for the session


graphics_session1 = pv.Graphics(session)
mesh1 = graphics_session1.Meshes["mesh-1"]
vector1 = graphics_session1.Vectors["vector-1"]
contour1 = graphics_session1.Contours["contour-1"]
contour2 = graphics_session1.Contours["contour-2"]
surface1 = graphics_session1.Surfaces["surface-1"]
from ansys.fluent.postprocessing.pyvista.plotter import plotter
#set graphics objects properties


#mesh
mesh1.show_edges = True
mesh1.surfaces_list = ['symmetry']


#contour
contour1.field = "velocity-magnitude"
contour1.surfaces_list = ['symmetry']


contour2.field = "temperature"
contour2.surfaces_list = ['symmetry', 'wall']


#copy
graphics_session1.Contours["contour-3"] = contour2()


#update
contour3 = graphics_session1.Contours["contour-3"]
contour3.update(contour1())


vector1.surfaces_list = ['symmetry']
vector1.scale = 1.0


#delete
del graphics_session1.Contours["contour-3"]


#loop
for name, _ in graphics_session1.Contours.items():
print(name)


#iso surface
surface1.surface_type.iso_surface.field= "velocity-magnitude"
surface1.surface_type.iso_surface.rendering= "contour"


#display in default plotter
contour1.display()
mesh1.display("plotter-1")
surface1.display("plotter-2")
vector1.display("plotter-3")
