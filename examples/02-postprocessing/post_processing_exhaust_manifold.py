""".. _ref_post_processing_exhaust_manifold:

Post Processing using PyVista and Matplotlib: Exhaust Manifold
----------------------------------------------------------------------
This example demonstrates the postprocessing capabilities of PyFluent
(using PyVista and Matplotlib) using a 3D model
of an exhaust manifold with high temperature flows passing through.
The flow through the manifold is turbulent and
involves conjugate heat transfer.

This example demonstrates how to do the following:

- Create surfaces for the display of 3D data.
- Display filled contours of temperature on several surfaces.
- Display velocity vectors.
- Plot quantitative results using Matplotlib
"""
###############################################################################
import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
from ansys.fluent.post import set_config
from ansys.fluent.post.matplotlib import Plots
from ansys.fluent.post.pyvista import Graphics

set_config(blocking=True, set_view_on_display="isometric")

###############################################################################
# First, download the case and data file and start Fluent as a service with
# Meshing mode, double precision, number of processors: 2

import_case = examples.download_file(
    filename="exhaust_system.cas.h5", directory="pyfluent/exhaust_system"
)

import_data = examples.download_file(
    filename="exhaust_system.dat.h5", directory="pyfluent/exhaust_system"
)

session = pyfluent.launch_fluent(precision="double", processor_count=4)

session.solver.tui.file.read_case(case_file_name=import_case)
session.solver.tui.file.read_data(case_file_name=import_data)

###############################################################################
# Get the graphics object for mesh display

graphics = Graphics(session=session)

###############################################################################
# Create a graphics object for mesh display

mesh1 = graphics.Meshes["mesh-1"]

###############################################################################
# Show edges and faces

mesh1.show_edges = True
mesh1.show_faces = True

###############################################################################
# Get the surfaces list

mesh1.surfaces_list = [
    "in1",
    "in2",
    "in3",
    "out1",
    "solid_up:1",
    "solid_up:1:830",
    "solid_up:1:830-shadow",
]
mesh1.display("window-1")

###############################################################################
# Disable edges and display again

mesh1.show_edges = False
mesh1.display("window-2")

###############################################################################
# Create iso-surface on the outlet plane

surf_outlet_plane = graphics.Surfaces["outlet-plane"]
surf_outlet_plane.surface.type = "iso-surface"
iso_surf1 = surf_outlet_plane.surface.iso_surface
iso_surf1.field = "y-coordinate"
iso_surf1.iso_value = -0.125017
surf_outlet_plane.display("window-3")

###############################################################################
# Create iso-surface on the mid-plane (Issue # 276)

surf_mid_plane_x = graphics.Surfaces["mid-plane-x"]
surf_mid_plane_x.surface.type = "iso-surface"
iso_surf2 = surf_mid_plane_x.surface.iso_surface
iso_surf2.field = "x-coordinate"
iso_surf2.iso_value = -0.174
surf_mid_plane_x.display("window-4")

###############################################################################
# Temperature contour on the mid-plane and the outlet

temperature_contour = graphics.Contours["contour-temperature"]
temperature_contour.field = "temperature"
temperature_contour.surfaces_list = ["mid-plane-x", "outlet-plane"]
temperature_contour.display("window-4")

###############################################################################
# Contour plot of temperature on the manifold

temperature_contour_manifold = graphics.Contours["contour-temperature-manifold"]
temperature_contour_manifold.field = "temperature"
temperature_contour_manifold.surfaces_list = [
    "in1",
    "in2",
    "in3",
    "out1",
    "solid_up:1",
    "solid_up:1:830",
]
temperature_contour_manifold.display("window-5")

###############################################################################
# Vector on the mid-plane
# Currently using outlet-plane since mid-plane is affected by Issue # 276

velocity_vector = graphics.Vectors["velocity-vector"]
velocity_vector.surfaces_list = ["outlet-plane"]
velocity_vector.scale = 1
velocity_vector.display("window-6")

###############################################################################
# Commenting out due to issue #290
# Start the Plot Object for the session
plots_session_1 = Plots(session)

###############################################################################
# Create a default XY-Plot
plot_1 = plots_session_1.XYPlots["plot-1"]

###############################################################################
# Set the surface on which the plot is plotted and the Y-axis function
plot_1.surfaces_list = ["outlet"]
plot_1.y_axis_function = "temperature"

###############################################################################
# Plot the created XY-Plot
plot_1.plot("window-7")
