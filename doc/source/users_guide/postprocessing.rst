Analyzing Your Results
======================
PyFluent postprocessing supports graphics and plotting.

Rendering Graphics Objects
--------------------------
The post package library is used for rendering graphics objects.
The following graphics operations are supported.

Displaying Mesh Objects
~~~~~~~~~~~~~~~~~~~~~~~
The following example demonstrates how you can display the mesh object:

.. code:: python

    import ansys.fluent.core as pyfluent
    from ansys.fluent.core import examples
    from ansys.fluent.post import set_config
    from ansys.fluent.post.matplotlib import Plots
    from ansys.fluent.post.pyvista import Graphics

    set_config(blocking=True, set_view_on_display="isometric")

    import_case = examples.download_file(
        filename="exhaust_system.cas.h5", directory="pyfluent/exhaust_system"
    )

    import_data = examples.download_file(
        filename="exhaust_system.dat.h5", directory="pyfluent/exhaust_system"
    )

    session = pyfluent.launch_fluent(precision="double", processor_count=2)

    session.solver.tui.file.read_case(case_file_name=import_case)
    session.solver.tui.file.read_data(case_file_name=import_data)

    graphics = Graphics(session=session)
    mesh1 = graphics.Meshes["mesh-1"]
    mesh1.show_edges = True
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

Displaying Iso-Surfaces
~~~~~~~~~~~~~~~~~~~~~~~
The following example demonstrates how you can display the iso-surface:

.. code:: python

    surf_outlet_plane = graphics.Surfaces["outlet-plane"]
    surf_outlet_plane.surface.type = "iso-surface"
    iso_surf1 = surf_outlet_plane.surface.iso_surface
    iso_surf1.field = "y-coordinate"
    iso_surf1.iso_value = -0.125017
    surf_outlet_plane.display("window-2")

Displaying Contours
~~~~~~~~~~~~~~~~~~~
The following example demonstrates how you can display the contour object:

.. code:: python

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
    temperature_contour_manifold.display("window-3")

Displaying Vectors
~~~~~~~~~~~~~~~~~~
The following example demonstrates how you can display the vector object:

.. code:: python

    velocity_vector = graphics.Vectors["velocity-vector"]
    velocity_vector.surfaces_list = ["outlet-plane"]
    velocity_vector.scale = 1
    velocity_vector.display("window-4")

Plotting Your Data
------------------
The following plotting operations are supported.

Displaying XY Plots
~~~~~~~~~~~~~~~~~~~
The following example demonstrates how you can display the xy plot:

.. code:: python

    plots_session_1 = Plots(session)
    plot_1 = plots_session_1.XYPlots["plot-1"]
    plot_1.surfaces_list = ["outlet"]
    plot_1.y_axis_function = "temperature"
    plot_1.plot("window-5")