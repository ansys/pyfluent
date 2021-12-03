# This is an auto-generated file.  DO NOT EDIT!

from ansys.fluent.solver.meta import PyMenuMeta, PyNamedObjectMeta


doc_by_method = {
    'adjoint' : 'Adjoint.',
    'file' : 'Enter the file menu.',
    'icing' : 'FENSAP-ICE options',
    'mesh' : 'Enter the mesh menu.',
    'parameters__and__customization' : 'Enter Parameters and custom menu.',
    'parallel' : 'Enter the parallel processing menu.',
    'preferences' : 'Set preferences',
    'solution' : 'Enter solution menu.',
    'setup' : 'Enter setup menu.',
    'simulation_reports' : 'Enter the simulation reports menu.',
    'server' : 'Enter the server menu.',
    'turbo_post' : 'Enter the turbo menu.',
    'close_fluent' : 'Exit program.',
    'exit' : 'Exit program.',
    'switch_to_meshing_mode' : 'Switch to meshing mode.',
    'print_license_usage' : 'Print license usage information',
    'parametric_study' : 'Enter the parametric study menu',
    'turbo_workflow' : 'Enter the turbo workflow menu',
}

class results(metaclass=PyMenuMeta):
    __doc__ = 'Enter results menu.'

    class animate(metaclass=PyMenuMeta):
        __doc__ = 'Enter the animation menu.'

        class playback(metaclass=PyMenuMeta):
            __doc__ = 'Enter animation playback menu.'
            doc_by_method = {
                'read' : 'Read new animation from file or already-defined animations.',
                'play' : 'Play the selected animation.',
                'write' : 'Write animation sequence to the file.',
                'delete' : 'Delete animation sequence.',
                'stored_view' : 'Play the 3D animation sequence using the view stored in the sequence.',
                'set_custom_frames' : 'Set custom frames start, end, skip frames for video export',
            }

            class video(metaclass=PyMenuMeta):
                __doc__ = 'Set options for exporting video file menu.'
                doc_by_method = {
                    'fps' : 'Set the Frame Per Sec(FPS) for exporting video file.',
                    'format' : 'Set format for exporting video file.',
                    'quality' : 'Set quality for exporting video file.',
                    'name' : 'Exporting video file name',
                    'use_original_resolution' : 'enable original resolution',
                    'scale' : 'Set scale by which video resolution will expand.',
                    'set_standard_resolution' : 'Select from pre-defined resolution list.',
                    'width' : 'Set the width for exporting video file.',
                    'height' : 'Set the height for exporting video file.',
                }

                class advance_quality(metaclass=PyMenuMeta):
                    __doc__ = 'Advance Quality setting'
                    doc_by_method = {
                        'bitrate_scale' : 'Mp4 bitrate scale - Best-64000 High-32000 Medium-16000 Low-8000',
                        'enable_h264' : 'H264 encoding flag',
                        'bitrate' : 'Set video bitrate(kbits/sec) for exporting video file.',
                        'compression_method' : 'Compression methode for Microsoft AVI movie',
                        'keyframe' : 'Set video keyframe rate for exporting video file.',
                    }

    class graphics(metaclass=PyMenuMeta):
        __doc__ = 'Enter graphics menu.'
        doc_by_method = {
            'annotate' : 'Add a text annotation string to the active graphics window.',
            'clear_annotations' : 'Delete all annotation text.',
            'color_map' : 'Enter the color-map menu.',
            'hsf_file' : 'Display hoops stream file data to active graphics window.',
        }

        class expert(metaclass=PyMenuMeta):
            __doc__ = 'Enter expert menu.'
            doc_by_method = {
                'add_custom_vector' : 'Add new custom vector definition.',
                'contour' : 'Display contours of a flow variable.',
                'display_custom_vector' : 'Display custom vector.',
                'graphics_window_layout' : 'Arrange the graphics window layout.',
                'mesh' : 'Display the mesh.',
                'mesh_outline' : 'Display the mesh boundaries.',
                'mesh_partition_boundary' : 'Display mesh partition boundaries.',
                'multigrid_coarsening' : 'Display a coarse mesh level from the last multigrid coarsening.',
                'profile' : 'Display profiles of a flow variable.',
                'reacting_channel_curves' : 'Plot/Report the reacting channel variables.',
                're_render' : 'Re-render the last contour, profile, or velocity vector plot\n     with updated surfaces, meshes, lights, colormap, rendering options, etc.,\n     without recalculating the contour data.',
                're_scale' : 'Re-render the last contour, profile, or velocity vector plot\n     with updated scale, surfaces, meshes, lights, colormap, rendering options, etc.,\n     without recalculating the field data.',
                'set_list_tree_separator' : 'Set the separator character for list tree.',
                'surface_cells' : 'Draw the cells on the specified surfaces.',
                'surface_mesh' : 'Draw the mesh defined by the specified surfaces.',
                'vector' : 'Display space vectors.',
                'velocity_vector' : 'Display velocity vectors.',
                'zone_mesh' : 'Draw the mesh defined by specified face zones.',
            }

            class flamelet_data(metaclass=PyMenuMeta):
                __doc__ = 'Display flamelet data.'
                doc_by_method = {
                    'draw_number_box' : 'Enable/disable display of the numbers box.',
                    'plot_1d_slice' : 'Enable/disable plot of the 1D-slice.',
                    'write_to_file' : 'Enable/disable writing the 1D-slice to file instead of plot.',
                    'carpet_plot' : 'Enable/disable display of carpet plot of a property.',
                }

            class particle_tracks(metaclass=PyMenuMeta):
                __doc__ = 'Enter the particle tracks menu.'
                doc_by_method = {
                    'particle_tracks' : 'Calculate and display particle tracks from defined injections.',
                    'plot_write_xy_plot' : 'Plot or write XY plot of particle tracks.',
                }

            class path_lines(metaclass=PyMenuMeta):
                __doc__ = 'Enter the pathlines menu.'
                doc_by_method = {
                    'path_lines' : 'Display pathlines from a surface.',
                    'plot_write_xy_plot' : 'Plot or write XY plot of pathline.',
                    'write_to_files' : 'Write Pathlines to a File.',
                }

            class pdf_data(metaclass=PyMenuMeta):
                __doc__ = 'Enter the PDF data menu.'
                doc_by_method = {
                    'draw_number_box' : 'Enable/disable the display of the numbers box.',
                    'plot_1d_slice' : 'Enable/disable a plot of the 1D-slice.',
                    'write_to_file' : 'Enable/disable writing the 1D-slice to file instead of plot.',
                    'carpet_plot' : 'Enable/disable the display of a carpet plot of a property.',
                }

            class set(metaclass=PyMenuMeta):
                __doc__ = 'Enter the set menu to set display parameters.'
                doc_by_method = {
                    'color_map' : 'Enter the color-map menu.',
                    'element_shrink' : 'Set percentage to shrink elements.',
                    'filled_mesh' : 'Enable/disable the filled mesh option.',
                    'mesh_level' : 'Set coarse mesh level to be drawn.',
                    'mesh_partitions' : 'Enable/disable drawing of the mesh partition boundaries.',
                    'mesh_surfaces' : 'Set surface IDs to be drawn as mesh',
                    'mesh_zones' : 'Set zone IDs to be drawn as mesh',
                    'line_weight' : 'Set the line-weight factor for the window.',
                    'marker_size' : 'Set the size of markers used to represent points.',
                    'marker_symbol' : 'Set the type of markers used to represent points.',
                    'mesh_display_configuration' : 'Set mesh display configuration',
                    'mirror_zones' : 'Set zones to mirror the domain about.',
                    'n_stream_func' : 'Set the number of iterations used in computing stream function.',
                    'nodewt_based_interp' : 'Use more accurate node-weight based interpolation for postprocessing',
                    'overlays' : 'Enable/disable overlays.',
                    'periodic_instancing' : 'Set periodic instancing.',
                    'proximity_zones' : 'Set zones to be used for boundary cell distance and boundary proximity.',
                    'render_mesh' : 'Enable/disable rendering the mesh on top of contours, vectors, etc.',
                    'reset_graphics' : 'Reset the graphics system.',
                    'zero_angle_dir' : 'Set the vector having zero angular coordinates.',
                    'duplicate_node_display' : 'Set flag to remove duplicate nodes in mesh display.',
                }

                class colors(metaclass=PyMenuMeta):
                    __doc__ = 'Enter the color options menu.'
                    doc_by_method = {
                        'background' : 'Set the background (window) color.',
                        'color_by_type' : 'Determine whether to color meshes by type or by surface (ID).',
                        'foreground' : 'Set the foreground (text and window frame) color.',
                        'far_field_faces' : 'Set the color of far field faces.',
                        'inlet_faces' : 'Set the color of inlet faces.',
                        'interior_faces' : 'Set the color of interior faces.',
                        'internal_faces' : 'Set the color of internal interface faces',
                        'outlet_faces' : 'Set the color of outlet faces.',
                        'overset_faces' : 'Set the color of overset faces.',
                        'periodic_faces' : 'Set the color of periodic faces.',
                        'rans_les_interface_faces' : 'Set the color of RANS/LES interface faces.',
                        'reset_user_colors' : 'Reset all user colors',
                        'show_user_colors' : 'List currently defined user colors',
                        'symmetry_faces' : 'Set the color of symmetric faces.',
                        'axis_faces' : 'Set the color of axisymmetric faces.',
                        'free_surface_faces' : 'Set the color of free-surface faces.',
                        'traction_faces' : 'Set the color of traction faces.',
                        'user_color' : 'Explicitly set color of display zone',
                        'wall_faces' : 'Set the color of wall faces.',
                        'interface_faces' : 'Set the color of mesh Interfaces.',
                        'list' : 'List available colors.',
                        'reset_colors' : 'Reset individual mesh surface colors to the defaults.',
                        'surface' : 'Set the color of surfaces.',
                        'skip_label' : 'Set the number of labels to be skipped in the colopmap scale.',
                        'automatic_skip' : 'Determine whether to skip labels in the colopmap scale automatically.',
                        'graphics_color_theme' : 'Enter the graphics color theme menu.',
                    }

                    class by_type(metaclass=PyMenuMeta):
                        __doc__ = 'Enter the zone type color and material assignment menu.'
                        doc_by_method = {
                            'only_list_case_boundaries' : 'Only list the boundary types that are assigned in this case.',
                            'reset' : 'To reset colors and/or materials to the defaults.',
                        }

                        class type_name(metaclass=PyMenuMeta):
                            __doc__ = 'Select the boundary type to specify colors and/or materials.'

                            class axis(metaclass=PyMenuMeta):
                                __doc__ = 'Set the material and/or color for the selected boundary type.'
                                doc_by_method = {
                                    'color' : 'Set a color for the selected boundary type.',
                                    'material' : 'Set a material for the selected boundary type.',
                                }

                            class far_field(metaclass=PyMenuMeta):
                                __doc__ = 'Set the material and/or color for the selected boundary type.'
                                doc_by_method = {
                                    'color' : 'Set a color for the selected boundary type.',
                                    'material' : 'Set a material for the selected boundary type.',
                                }

                            class free_surface(metaclass=PyMenuMeta):
                                __doc__ = 'Set the material and/or color for the selected boundary type.'
                                doc_by_method = {
                                    'color' : 'Set a color for the selected boundary type.',
                                    'material' : 'Set a material for the selected boundary type.',
                                }

                            class inlet(metaclass=PyMenuMeta):
                                __doc__ = 'Set the material and/or color for the selected boundary type.'
                                doc_by_method = {
                                    'color' : 'Set a color for the selected boundary type.',
                                    'material' : 'Set a material for the selected boundary type.',
                                }

                            class interface(metaclass=PyMenuMeta):
                                __doc__ = 'Set the material and/or color for the selected boundary type.'
                                doc_by_method = {
                                    'color' : 'Set a color for the selected boundary type.',
                                    'material' : 'Set a material for the selected boundary type.',
                                }

                            class interior(metaclass=PyMenuMeta):
                                __doc__ = 'Set the material and/or color for the selected boundary type.'
                                doc_by_method = {
                                    'color' : 'Set a color for the selected boundary type.',
                                    'material' : 'Set a material for the selected boundary type.',
                                }

                            class internal(metaclass=PyMenuMeta):
                                __doc__ = 'Set the material and/or color for the selected boundary type.'
                                doc_by_method = {
                                    'color' : 'Set a color for the selected boundary type.',
                                    'material' : 'Set a material for the selected boundary type.',
                                }

                            class outlet(metaclass=PyMenuMeta):
                                __doc__ = 'Set the material and/or color for the selected boundary type.'
                                doc_by_method = {
                                    'color' : 'Set a color for the selected boundary type.',
                                    'material' : 'Set a material for the selected boundary type.',
                                }

                            class overset(metaclass=PyMenuMeta):
                                __doc__ = 'Set the material and/or color for the selected boundary type.'
                                doc_by_method = {
                                    'color' : 'Set a color for the selected boundary type.',
                                    'material' : 'Set a material for the selected boundary type.',
                                }

                            class periodic(metaclass=PyMenuMeta):
                                __doc__ = 'Set the material and/or color for the selected boundary type.'
                                doc_by_method = {
                                    'color' : 'Set a color for the selected boundary type.',
                                    'material' : 'Set a material for the selected boundary type.',
                                }

                            class rans_les_interface(metaclass=PyMenuMeta):
                                __doc__ = 'Set the material and/or color for the selected boundary type.'
                                doc_by_method = {
                                    'color' : 'Set a color for the selected boundary type.',
                                    'material' : 'Set a material for the selected boundary type.',
                                }

                            class surface(metaclass=PyMenuMeta):
                                __doc__ = 'Set the material and/or color for the selected boundary type.'
                                doc_by_method = {
                                    'color' : 'Set a color for the selected boundary type.',
                                    'material' : 'Set a material for the selected boundary type.',
                                }

                            class symmetry(metaclass=PyMenuMeta):
                                __doc__ = 'Set the material and/or color for the selected boundary type.'
                                doc_by_method = {
                                    'color' : 'Set a color for the selected boundary type.',
                                    'material' : 'Set a material for the selected boundary type.',
                                }

                            class traction(metaclass=PyMenuMeta):
                                __doc__ = 'Set the material and/or color for the selected boundary type.'
                                doc_by_method = {
                                    'color' : 'Set a color for the selected boundary type.',
                                    'material' : 'Set a material for the selected boundary type.',
                                }

                            class wall(metaclass=PyMenuMeta):
                                __doc__ = 'Set the material and/or color for the selected boundary type.'
                                doc_by_method = {
                                    'color' : 'Set a color for the selected boundary type.',
                                    'material' : 'Set a material for the selected boundary type.',
                                }

                class contours(metaclass=PyMenuMeta):
                    __doc__ = 'Enter the contour options menu.'
                    doc_by_method = {
                        'auto_range' : 'Enable/disable auto-computation of range for contours.',
                        'clip_to_range' : 'Enable/disable the clip to range option for filled contours.',
                        'surfaces' : 'Set surfaces to be contoured.',
                        'filled_contours' : 'Enable/disable the filled contour option.',
                        'global_range' : 'Enable/disable the global range for contours option.',
                        'line_contours' : 'Enable/disable the filled contour option.',
                        'log_scale' : 'Enable/disable the use of a log scale.',
                        'n_contour' : 'Set the number of contour levels.',
                        'node_values' : 'Enable/disable the plot of node values.',
                        'render_mesh' : 'Determine whether or not to render the mesh on top of contours, vectors, etc.',
                        'coloring' : 'Select coloring option',
                    }

                class picture(metaclass=PyMenuMeta):
                    __doc__ = 'Enter the hardcopy/save-picture options menu.'
                    doc_by_method = {
                        'invert_background' : 'Exchange foreground/background colors for hardcopy.',
                        'landscape' : 'Plot hardcopies in landscape or portrait orientation.',
                        'preview' : 'Display a preview image of a hardcopy.',
                        'x_resolution' : 'Set the width of raster-formatted images in pixels (0 implies current window size).',
                        'y_resolution' : 'Set the height of raster-formatted images in pixels (0 implies current window size).',
                        'dpi' : 'Set the DPI for EPS and Postscript files, specifies the resolution in dots per inch (DPI) instead of setting the width and height',
                        'use_window_resolution' : "Use the currently active window's resolution for hardcopy (ignores the x-resolution and y-resolution in this case).",
                        'set_standard_resolution' : 'Select from pre-defined resolution list.',
                        'jpeg_hardcopy_quality' : 'To set jpeg hardcopy quality.',
                    }

                    class color_mode(metaclass=PyMenuMeta):
                        __doc__ = 'Enter the hardcopy color mode menu.'
                        doc_by_method = {
                            'color' : 'Plot hardcopies in color.',
                            'gray_scale' : 'Convert color to grayscale for hardcopy.',
                            'mono_chrome' : 'Convert color to monochrome (black and white) for hardcopy.',
                            'list' : 'Display the current hardcopy color mode.',
                        }

                    class driver(metaclass=PyMenuMeta):
                        __doc__ = 'Enter the set hardcopy driver menu.'
                        doc_by_method = {
                            'dump_window' : 'Set the command used to dump the graphics window to a file.',
                            'eps' : 'Produce encapsulated PostScript (EPS) output for hardcopies.',
                            'jpeg' : 'Produce JPEG output for hardcopies.',
                            'post_script' : 'Produce PostScript output for hardcopies.',
                            'ppm' : 'Produce PPM output for hardcopies.',
                            'tiff' : 'Use TIFF output for hardcopies.',
                            'png' : 'Use PNG output for hardcopies.',
                            'hsf' : 'Use HSF output for hardcopies.',
                            'avz' : 'Use AVZ output for hardcopies.',
                            'glb' : 'Use GLB output for hardcopies.',
                            'vrml' : 'Use VRML output for hardcopies.',
                            'list' : 'List the current hardcopy driver.',
                            'options' : 'Set the hardcopy options. Available options are:\n\\\\n               \t"no gamma correction", disables gamma correction of colors,\n\\\\n               \t"physical size = (width,height)", where width and height\n          are the actual measurements of the printable area of the page\n          in centimeters.\n\\\\n               \t"subscreen = (left,right,bottom,top)", where left,right,\n          bottom, and top are numbers in [-1,1] describing a subwindow on\n          the page in which to place the hardcopy.\n\n\\\\n          The options may be combined by separating them with commas.',
                        }

                        class post_format(metaclass=PyMenuMeta):
                            __doc__ = 'Enter the PostScript driver format menu.'
                            doc_by_method = {
                                'fast_raster' : 'Use the new raster format.',
                                'raster' : 'Use the original raster format.',
                                'rle_raster' : 'Use the run-length encoded raster format.',
                                'vector' : 'Use vector format.',
                            }

                class lights(metaclass=PyMenuMeta):
                    __doc__ = 'Enter the lights menu.'
                    doc_by_method = {
                        'lights_on' : 'Turn all active lighting on/off.',
                        'set_ambient_color' : 'Set the ambient light color for the scene.',
                        'set_light' : 'Add or modify a directional, colored light.',
                        'headlight_on' : 'Turn the light that moves with the camera on or off.',
                    }

                    class lighting_interpolation(metaclass=PyMenuMeta):
                        __doc__ = 'Set lighting interpolation method.'
                        doc_by_method = {
                            'automatic' : 'Choose Automatic to automatically select the best lighting method for a given graphics object.',
                            'flat' : 'Use flat shading for meshes and polygons.',
                            'gouraud' : 'Use Gouraud shading to calculate the color at each vertex of a polygon and interpolate it in the interior.',
                            'phong' : 'Use Phong shading to interpolate the normals for each pixel of a polygon and compute a color at every pixel.',
                        }

                class particle_tracks(metaclass=PyMenuMeta):
                    __doc__ = 'Enter the particle-tracks menu to set parameters for display of particle tracks.'
                    doc_by_method = {
                        'display' : 'Determine whether particle tracks will be displayed or only tracked.',
                        'history_filename' : 'Specify the name of the particle history file.',
                        'report_to' : 'Specify the destination for the report (console, file, none).',
                        'report_type' : 'Set the report type for particle tracks.',
                        'report_variables' : 'Set the report variables.',
                        'report_default_variables' : 'Set the report variables to default.',
                        'track_single_particle_stream' : 'Specify the stream ID to be tracked.',
                        'arrow_scale' : 'Set the scale factor for arrows drawn on particle tracks.',
                        'arrow_space' : 'Set the spacing factor for arrows drawn on particle tracks.',
                        'coarsen_factor' : 'Set the particle tracks coarsening factor.',
                        'line_width' : 'Set the width for particle track.',
                        'marker_size' : 'Set the marker size for particle drawing.',
                        'radius' : 'Set the radius for particle track (ribbons/cylinder only) cross-section.',
                        'style' : 'Set the display style for particle track (line/ribbon/cylinder/sphere).',
                        'twist_factor' : 'Set the scale factor for twisting (ribbons only).',
                        'sphere_attrib' : 'Specify size and number of slices to be used in drawing spheres.',
                        'particle_skip' : 'Specify how many particle tracks should be displayed.',
                    }

                    class sphere_settings(metaclass=PyMenuMeta):
                        __doc__ = 'Provide sphere specific input.'
                        doc_by_method = {
                            'vary_diameter' : 'Specify whether the spheres can vary with another variable.',
                            'diameter' : 'Diameter of the spheres when vary-diameter? is disabled.',
                            'auto_range' : 'Specify whether displayed spheres should include auto range of variable to size spheres.',
                            'minimum' : 'Set the minimum value of the sphere to be displayed.',
                            'maximum' : 'Set the maximum value of the sphere to be displayed.',
                            'smooth_parameter' : 'Specify number of slices to be used in drawing spheres.',
                            'scale_factor' : 'Specify a scale factor to enlarge/reduce the size of spheres.',
                            'size_variable' : 'Select a particle variable to size the spheres.',
                        }

                    class vector_settings(metaclass=PyMenuMeta):
                        __doc__ = 'Set vector specific input.'
                        doc_by_method = {
                            'style' : 'Enable and set the display style for particle vectors (none/vector/centered-vector/centered-cylinder).',
                            'vector_length' : 'Specify the length of constant vectors.',
                            'vector_length_variable' : 'Select a particle variable to specify the length of vectors.',
                            'scale_factor' : 'Specify a scale factor to enlarge/reduce the length of vectors.',
                            'length_variable' : 'Specify whether the displayed vectors have length varying with another variable.',
                            'length_to_head_ratio' : 'Specify ratio of length to head for vectors and length to diameter for cylinders.',
                            'constant_color' : 'Specify a constant color for the vectors.',
                            'color_variable' : 'Specify whether the vectors should be colored by variable specified in /display/particle-track/particle-track (if false use a constant color).',
                            'vector_variable' : 'Select a particle vector function to specify vector direction.',
                        }

                    class filter_settings(metaclass=PyMenuMeta):
                        __doc__ = 'Set filter for particle display.'
                        doc_by_method = {
                            'enable_filtering' : 'Specify whether particle display is filtered.',
                            'inside' : 'Specify whether filter variable needs to be inside min/max to be displayed (else outside min/max).',
                            'filter_variable' : 'Select a variable used for filtering of particles.',
                            'minimum' : 'Specify the lower bound for the filter variable.',
                            'maximum' : 'Specify the upper bound for the filter variable.',
                        }

                class path_lines(metaclass=PyMenuMeta):
                    __doc__ = 'Enter the path-lines menu to set parameters for the display of pathlines.'
                    doc_by_method = {
                        'arrow_scale' : 'Set the scale factor for arrows drawn on pathlines.',
                        'arrow_space' : 'Set the spacing factor for arrows drawn on pathlines.',
                        'display_steps' : 'Set the display stepping for pathlines.',
                        'error_control' : 'Set error control during pathline computation.',
                        'line_width' : 'Set the width for pathlines.',
                        'marker_size' : 'Set the marker size for particle drawing.',
                        'maximum_steps' : 'Set the maximum number of steps to take for pathlines.',
                        'maximum_error' : 'Set the maximum error allowed while computing the pathlines.',
                        'radius' : 'Set the radius for pathline (ribbons/cylinder only) cross-section.',
                        'relative_pathlines' : 'Enable/disable the tracking of pathlines in a relative coordinate system.',
                        'style' : 'Set display style for pathlines (line/ribbon/cylinder).',
                        'twist_factor' : 'Set the scale factor for twisting (ribbons only).',
                        'step_size' : 'Set the step length between particle positions for path-lines.',
                        'reverse' : 'Enable/disable the direction of path tracking.',
                        'sphere_attrib' : 'Specify size and no. of slices to be used in drawing sphere for sphere-style.',
                        'track_in_phase' : 'Assign phase to display pathlines in.',
                    }

                class rendering_options(metaclass=PyMenuMeta):
                    __doc__ = 'Enter the rendering options menu.'
                    doc_by_method = {
                        'auto_spin' : 'Enable/disable mouse view rotations to continue to spin the display after the button is released.',
                        'device_info' : 'List information for the graphics device.',
                        'double_buffering' : 'Enable/disable double-buffering.',
                        'driver' : 'Change the current graphics driver.',
                        'hidden_surfaces' : 'Enable/disable hidden surface removal.',
                        'hidden_surface_method' : 'Specify the method to perform hidden line and hidden surface rendering.',
                        'outer_face_cull' : 'Enable/disable discarding outer faces during display.',
                        'surface_edge_visibility' : 'Set edge visibility flags for surfaces.',
                        'animation_option' : 'Using Wireframe / All option during animation',
                        'color_map_alignment' : 'Set the color bar alignment.',
                        'help_text_color' : 'Set the color of screen help text.',
                        'face_displacement' : 'Set face displacement value in Z-buffer units along the Camera Z-axis.',
                        'set_rendering_options' : 'Set the rendering options.',
                        'show_colormap' : 'Enable/Disable colormap.',
                    }

                class titles(metaclass=PyMenuMeta):
                    __doc__ = 'Set problem title.'
                    doc_by_method = {
                        'left_top' : 'Set the title text for left top in title segment',
                        'left_bottom' : 'Set the title text for left bottom in title segment',
                        'right_top' : 'Set the title text for right top in title segment',
                        'right_middle' : 'Set the title text for right middle in title segment',
                        'right_bottom' : 'Set the title text for right bottom in title segment',
                    }

                class velocity_vectors(metaclass=PyMenuMeta):
                    __doc__ = 'Enter the menu to set parameters for display of velocity vectors.'
                    doc_by_method = {
                        'auto_scale' : 'Enable/disable auto-scale of all vectors so that vector overlap is minimal.',
                        'color' : 'Set the color used for all vectors. Set color to the null string to use the color map.',
                        'component_x' : 'Enable/disable use of x-component of vectors.',
                        'component_y' : 'Enable/disable use of y-component of vectors.',
                        'component_z' : 'Enable/disable use of z-component of vectors.',
                        'constant_length' : 'Enable/disable setting all vectors to have the same length.',
                        'color_levels' : 'Set the number of colors used from the color map.',
                        'global_range' : 'Enable/disable the global range for vectors option.',
                        'in_plane' : 'Toggle the display of in-plane velocity vectors.',
                        'log_scale' : 'Enable/disable the use of a log scale.',
                        'node_values' : 'Enable/disable plotting node values. Cell values will be plotted if "no".',
                        'relative' : 'Enable/disable the display of relative velocity vectors.',
                        'render_mesh' : 'Enable/disable rendering the mseh on top of contours, vectors, etc.',
                        'scale' : 'Set the value by which the vector length will be scaled.',
                        'scale_head' : 'Set the value by which the vector head will be scaled.',
                        'style' : 'Set the style with which the vectors will be drawn.',
                        'surfaces' : 'Set surfaces on which vectors are drawn.',
                    }

                class windows(metaclass=PyMenuMeta):
                    __doc__ = 'Enter the window options menu.'
                    doc_by_method = {
                        'aspect_ratio' : 'Set the aspect ratio of the active window.',
                        'logo' : 'Enable/disable visibility of the logo in graphics window.',
                        'ruler' : 'Enable/disable ruler visibility.',
                        'logo_color' : 'Set logo color to white/black.',
                    }

                    class axes(metaclass=PyMenuMeta):
                        __doc__ = 'Enter the axes window options menu.'
                        doc_by_method = {
                            'border' : 'Enable/disable drawing of a border around the axes window.',
                            'bottom' : 'Set the bottom boundary of the axes window.',
                            'clear' : 'Set the transparency of the axes window.',
                            'right' : 'Set the right boundary of the axes window.',
                            'visible' : 'Enable/disable axes visibility.',
                        }

                    class main(metaclass=PyMenuMeta):
                        __doc__ = 'Enter the main view window options menu.'
                        doc_by_method = {
                            'border' : 'Enable/disable drawing of borders around the main viewing window.',
                            'bottom' : 'Set the bottom boundary of the main viewing window.',
                            'left' : 'Set the left boundary of the main viewing window.',
                            'right' : 'Set the right boundary of the main viewing window.',
                            'top' : 'Set the top boundary of the main viewing window.',
                            'visible' : 'Enable/disable visibility of the main viewing window.',
                        }

                    class scale(metaclass=PyMenuMeta):
                        __doc__ = 'Enter the color scale window options menu.'
                        doc_by_method = {
                            'border' : 'Enable/disable drawing of borders around the color scale window.',
                            'bottom' : 'Set the bottom boundary of the color scale window.',
                            'clear' : 'Set the transparency of the scale window.',
                            'format' : 'Set the number format of the color scale window (e.g. %0.2e).',
                            'font_size' : 'Set the font size of the color scale window.',
                            'left' : 'Set the left boundary of the color scale window.',
                            'margin' : 'Set the margin of the color scale window.',
                            'right' : 'Set the right boundary of the color scale window.',
                            'top' : 'Set the top boundary of the color scale window.',
                            'visible' : 'Enable/disable visibility of the color scale window.',
                            'alignment' : 'Set colormap to bottom/left/top/right',
                        }

                    class text(metaclass=PyMenuMeta):
                        __doc__ = 'Enter the text window options menu.'
                        doc_by_method = {
                            'application' : 'Enable/disable the application name in the picture.',
                            'border' : 'Enable/disable drawing of borders around the text window.',
                            'bottom' : 'Set the bottom boundary of the text window.',
                            'clear' : 'Enable/disable text window transparency.',
                            'company' : 'Enable/disable the company name in the picture.',
                            'date' : 'Enable/disable the date in the picture.',
                            'left' : 'Set the left boundary of the text window.',
                            'right' : 'Set the right boundary of the text window.',
                            'top' : 'Set the top boundary of the text window.',
                            'visible' : 'Enable/disable text window transparency.',
                        }

                    class video(metaclass=PyMenuMeta):
                        __doc__ = 'Enter the video window options menu.'
                        doc_by_method = {
                            'background' : 'Set the background color in the video picture.',
                            'color_filter' : 'Set the color filter options for the picture.',
                            'foreground' : 'Set the foreground color in the video picture.',
                            'on' : 'Enable/disable video picture settings.',
                            'pixel_size' : 'Set the window size in pixels.',
                        }

                    class xy(metaclass=PyMenuMeta):
                        __doc__ = 'Enter the X-Y plot window options menu.'
                        doc_by_method = {
                            'border' : 'Enable/disable drawing of a border around the X-Y plotter window.',
                            'bottom' : 'Set the bottom boundary of the X-Y plotter window.',
                            'left' : 'Set the left boundary of the X-Y plotter window.',
                            'right' : 'Set the right boundary of the X-Y plotter window.',
                            'top' : 'Set the top boundary of the X-Y plotter window.',
                            'visible' : 'Enable/disable X-Y plotter window visibility.',
                        }

        class lights(metaclass=PyMenuMeta):
            __doc__ = 'Enter the lights menu.'
            doc_by_method = {
                'lights_on' : 'Turn all active lighting on/off.',
                'set_ambient_color' : 'Set the ambient light color for the scene.',
                'set_light' : 'Add or modify a directional, colored light.',
                'headlight_on' : 'Turn the light that moves with the camera on or off.',
            }

            class lighting_interpolation(metaclass=PyMenuMeta):
                __doc__ = 'Set lighting interpolation method.'
                doc_by_method = {
                    'automatic' : 'Choose Automatic to automatically select the best lighting method for a given graphics object.',
                    'flat' : 'Use flat shading for meshes and polygons.',
                    'gouraud' : 'Use Gouraud shading to calculate the color at each vertex of a polygon and interpolate it in the interior.',
                    'phong' : 'Use Phong shading to interpolate the normals for each pixel of a polygon and compute a color at every pixel.',
                }

        class objects(metaclass=PyMenuMeta):
            __doc__ = 'Enter to add, edit, delete or display graphics objects'
            is_extended_tui = True
            doc_by_method = {
                'create' : 'Create new graphics object.',
                'edit' : 'Edit graphics object.',
                'copy' : 'Copy graphics object.',
                'delete' : 'Delete graphics object.',
                'display' : 'Display graphics object.',
                'add_to_graphics' : 'Add graphics object to existing graphics.',
            }

            class mesh(metaclass=PyNamedObjectMeta):
                __doc__ = ''
                is_container = True
                is_extended_tui = True

                class name(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class options(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                    class nodes(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class edges(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class faces(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class partitions(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class overset(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class gap(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                class edge_type(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                    class all(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class feature(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                        class feature_angle(metaclass=PyMenuMeta):
                            __doc__ = ''
                            is_extended_tui = True

                    class outline(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                class shrink_factor(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class surfaces_list(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class coloring(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                    class automatic(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                        class type(metaclass=PyMenuMeta):
                            __doc__ = ''
                            is_extended_tui = True

                        class id(metaclass=PyMenuMeta):
                            __doc__ = ''
                            is_extended_tui = True

                        class normal(metaclass=PyMenuMeta):
                            __doc__ = ''
                            is_extended_tui = True

                        class partition(metaclass=PyMenuMeta):
                            __doc__ = ''
                            is_extended_tui = True

                    class manual(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                        class faces(metaclass=PyMenuMeta):
                            __doc__ = ''
                            is_extended_tui = True

                        class edges(metaclass=PyMenuMeta):
                            __doc__ = ''
                            is_extended_tui = True

                        class nodes(metaclass=PyMenuMeta):
                            __doc__ = ''
                            is_extended_tui = True

                        class material_color(metaclass=PyMenuMeta):
                            __doc__ = ''
                            is_extended_tui = True

                class display_state_name(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

            class contour(metaclass=PyNamedObjectMeta):
                __doc__ = ''
                is_container = True
                is_extended_tui = True

                class name(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class field(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class filled(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class boundary_values(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class contour_lines(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class node_values(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class surfaces_list(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class range_option(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                    class auto_range_on(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                        class global_range(metaclass=PyMenuMeta):
                            __doc__ = ''
                            is_extended_tui = True

                    class auto_range_off(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                        class clip_to_range(metaclass=PyMenuMeta):
                            __doc__ = ''
                            is_extended_tui = True

                        class minimum(metaclass=PyMenuMeta):
                            __doc__ = ''
                            is_extended_tui = True

                        class maximum(metaclass=PyMenuMeta):
                            __doc__ = ''
                            is_extended_tui = True

                class coloring(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                    class smooth(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class banded(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                class color_map(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                    class visible(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class size(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class color(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class log_scale(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class format(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class user_skip(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class show_all(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class position(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class font_name(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class font_automatic(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class font_size(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class length(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class width(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                class draw_mesh(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class mesh_object(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class display_state_name(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

            class vector(metaclass=PyNamedObjectMeta):
                __doc__ = ''
                is_container = True
                is_extended_tui = True

                class name(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class field(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class vector_field(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class surfaces_list(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class scale(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                    class auto_scale(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class scale_f(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                class style(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class skip(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class vector_opt(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                    class in_plane(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class fixed_length(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class x_comp(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class y_comp(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class z_comp(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class scale_head(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class color(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                class range_option(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                    class auto_range_on(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                        class global_range(metaclass=PyMenuMeta):
                            __doc__ = ''
                            is_extended_tui = True

                    class auto_range_off(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                        class clip_to_range(metaclass=PyMenuMeta):
                            __doc__ = ''
                            is_extended_tui = True

                        class minimum(metaclass=PyMenuMeta):
                            __doc__ = ''
                            is_extended_tui = True

                        class maximum(metaclass=PyMenuMeta):
                            __doc__ = ''
                            is_extended_tui = True

                class color_map(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                    class visible(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class size(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class color(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class log_scale(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class format(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class user_skip(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class show_all(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class position(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class font_name(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class font_automatic(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class font_size(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class length(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                    class width(metaclass=PyMenuMeta):
                        __doc__ = ''
                        is_extended_tui = True

                class draw_mesh(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class mesh_object(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

                class display_state_name(metaclass=PyMenuMeta):
                    __doc__ = ''
                    is_extended_tui = True

        class rendering_options(metaclass=PyMenuMeta):
            __doc__ = 'Enter the rendering options menu.'
            doc_by_method = {
                'auto_spin' : 'Enable/disable mouse view rotations to continue to spin the display after the button is released.',
                'device_info' : 'List information for the graphics device.',
                'double_buffering' : 'Enable/disable double-buffering.',
                'driver' : 'Change the current graphics driver.',
                'hidden_surfaces' : 'Enable/disable hidden surface removal.',
                'hidden_surface_method' : 'Specify the method to perform hidden line and hidden surface rendering.',
                'outer_face_cull' : 'Enable/disable discarding outer faces during display.',
                'surface_edge_visibility' : 'Set edge visibility flags for surfaces.',
                'animation_option' : 'Using Wireframe / All option during animation',
                'color_map_alignment' : 'Set the color bar alignment.',
                'help_text_color' : 'Set the color of screen help text.',
                'face_displacement' : 'Set face displacement value in Z-buffer units along the Camera Z-axis.',
                'set_rendering_options' : 'Set the rendering options.',
                'show_colormap' : 'Enable/Disable colormap.',
            }

        class update_scene(metaclass=PyMenuMeta):
            __doc__ = 'Enter the scene options menu.'
            doc_by_method = {
                'select_geometry' : 'Select geometry to be updated.',
                'overlays' : 'Enable/disable the overlays option.',
                'draw_frame' : 'Enable/disable drawing of the bounding frame.',
                'delete' : 'Delete selected geometries.',
                'display' : 'Display selected geometries.',
                'transform' : 'Apply transformation matrix on selected geometries.',
                'pathline' : 'Change pathline attributes.',
                'iso_sweep' : 'Change iso-sweep values.',
                'time' : 'Change time-step value.',
                'set_frame' : 'Change frame options.',
            }

    class plot(metaclass=PyMenuMeta):
        __doc__ = 'Enter the XY plot menu.'
        doc_by_method = {
            'circum_avg_axial' : 'Compute iso-axial band surfaces and plot data vs axial coordinate on them.',
            'circum_avg_radial' : 'Compute iso-radial band surfaces and plot data vs radius on them.',
            'change_fft_ref_pressure' : 'Change acoustic reference pressure.',
            'fft' : 'Plot FFT of file data.',
            'fft_set' : 'Enter the menu to set histogram plot parameters.',
            'file' : 'Plot data from file.',
            'datasources' : 'Enter the menu to set data sources.',
            'display_profile_data' : 'Plot profile data.',
            'file_list' : 'Plot data from multiple files.',
            'file_set' : 'Enter the menu to set file plot parameters.',
            'histogram' : 'Plot a histogram of a specified scalar quantity.',
            'histogram_set' : 'Enter the menu to set histogram plot parameters.',
            'plot' : 'Plot solution on surfaces.',
            'plot_direction' : 'Set plot direction for xy plot.',
            'residuals' : 'Plot equation residual history.',
            'residuals_set' : 'Enter the menu to set residual plot parameters.',
            'solution' : 'Plot solution on surfaces and/or zones.',
            'solution_set' : 'Enter the menu to set solution plot parameters.',
            'set_boundary_val_off' : 'Set boundary value off when node values off for XY/Solution Plot.\n       \n Note: This setting is valid for current Fluent session only.',
            'label_alignment' : 'Set the alignment of xy plot label to horizontal or axis aligned.',
        }

        class ansys_sound_analysis(metaclass=PyMenuMeta):
            __doc__ = 'Ansys Sound analysis and specification.'
            doc_by_method = {
                'write_files' : 'write Ansys Sound out files',
                'print_indicators' : 'print Ansys Sound indicators',
            }

        class cumulative_plot(metaclass=PyMenuMeta):
            __doc__ = 'Plot Cumulative Force and Moments'
            doc_by_method = {
                'add' : 'Add a new object',
                'axes' : 'Set axes options of an object.',
                'curves' : 'Set curves options of an object.',
                'edit' : 'Edit an object',
                'delete' : 'Delete an object',
                'list' : 'List objects',
                'list_properties' : 'List properties of an object',
                'plot' : 'Plot the Cumulative Forces/Moments',
                'print' : 'Print the Cumulative Forces/Moments',
                'write' : 'Write the Cumulative Forces/Moments',
            }

        class flamelet_curves(metaclass=PyMenuMeta):
            __doc__ = 'Plot flamelet curves.'
            doc_by_method = {
                'write_to_file' : 'Write curve to a file instead of plot.',
                'plot_curves' : 'Plot of a property.',
            }

    class report(metaclass=PyMenuMeta):
        __doc__ = 'Enter the report menu.'
        doc_by_method = {
            'dpm_summary' : 'Print discrete phase summary report of particle fates.',
            'dpm_extended_summary' : 'Print extended discrete phase summary report of particle fates, with options',
            'dpm_zone_summaries_per_injection' : 'Enable per-injection zone DPM summaries',
            'dpm_sample' : 'Sample trajectories at boundaries and lines/planes.',
            'dpm_sample_output_udf' : 'Set the DPM sampling output UDF',
            'dpm_sample_sort_file' : 'Enable writing of sorted DPM sample files.',
            'particle_summary' : 'Print summary report for all current particles',
            'path_line_summary' : 'Print path-line-summary report.',
            'print_histogram' : 'Print a histogram of a scalar quantity.',
            'write_histogram' : '',
            'projected_surface_area' : 'Print total area of the projection of a group of surfaces to a plane.',
            'species_mass_flow' : 'Print list of species mass flow rates at boundaries.',
            'element_mass_flow' : 'Print list of element mass flow rates at boundaries.',
            'summary' : 'Print report summary.',
            'uds_flow' : 'Print list of UDS flow rate at boundaries.',
            'mphase_summary' : 'Multiphase Summary and Recommendations',
        }

        class dpm_histogram(metaclass=PyMenuMeta):
            __doc__ = 'Enter the DPM histogram menu.'
            doc_by_method = {
                'compute_sample' : 'Compute minimum/maximum of a sample variable.',
                'delete_sample' : 'Delete a sample from loaded sample list.',
                'list_samples' : 'Show all samples in loaded sample list.',
                'plot_sample' : 'Plot a histogram of a loaded sample.',
                'read_sample' : 'Read a sample file and add it to the sample list.',
                'write_sample' : 'Write a histogram of a loaded sample into a file.',
                'pick_sample_to_reduce' : 'Pick a sample for which to first set-up and then perform the data reduction.',
                'reduce_picked_sample' : 'Reduce a sample after first picking it and setting up all data-reduction options and parameters.',
            }

            class set(metaclass=PyMenuMeta):
                __doc__ = 'Enter the settings menu for the histogram.'
                doc_by_method = {
                    'auto_range' : 'Automatically compute range of sampling variable for histogram plots.',
                    'correlation' : 'Compute correlation of sampling variable with other variable.',
                    'cumulation_curve' : 'Compute a cumulative curve for sampling variable or correlation variable when correlation? was specified.',
                    'diameter_statistics' : 'Compute Rosin Rammler parameters, Sauter and other mean diameters.\nRequires specification of diameter as sampling variable.',
                    'histogram_mode' : 'Use bars for histogram plot or xy-style.',
                    'minimum' : 'Specify mimimum value of x-axis variable for histogram plots.',
                    'maximum' : 'Specify maximum value of x-axis variable for histogram plots.',
                    'number_of_bins' : 'Specify the number of bins.',
                    'percentage' : 'Use percentages of bins to be computed.',
                    'variable_power_3' : 'Use the cubic of the cumulation variable during computation of the cumulative curve.\nWhen the particle mass was not sampled, the diameter can be used instead.',
                    'logarithmic' : 'Use logarithmic scaling on the abscissa (variable axis)? -- Will not work unless all values are positive.',
                    'weighting' : 'Use weighting with additional variable when sorting data into samples.',
                }

            class setup_reduction(metaclass=PyMenuMeta):
                __doc__ = 'Set up the sample data reduction by specifying all relevant options and setting parameters as desired.'
                doc_by_method = {
                    'use_weighting' : 'Specify whether to use any weighting in the averaging that is done in each bin in the data reduction.',
                    'weighting_variable' : 'Choose the weighting variable for the averaging in each bin in the data reduction.',
                    'make_steady_from_unsteady_file' : 'Specify whether the unsteady sample is to be reduced into a steady-state injection file.',
                    'reset_min_and_max' : 'Reset the min and max values of the range to be considered for a specific variable in the data reduction.',
                    'minimum' : 'Set the minimum value of the range to be considered for a specific variable in the data reduction.',
                    'maximum' : 'Set the maximum value of the range to be considered for a specific variable in the data reduction.',
                    'logarithmic' : 'Switch on or off logarithmic scaling to be used for a specific variable in the data reduction.',
                    'number_of_bins' : 'Set the number of bins to be used for a specific variable in the data reduction.',
                    'all_variables_number_of_bins' : 'Set the number of bins to be used for ALL variables in the data reduction.',
                    'list_settings' : 'List all user inputs for the sample picked for data reduction.',
                }

        class fluxes(metaclass=PyMenuMeta):
            __doc__ = 'Flux report menu.'
            doc_by_method = {
                'mass_flow' : 'Print mass flow rate at inlets and outlets.',
                'heat_transfer' : 'Print heat transfer rate at boundaries.',
                'heat_transfer_sensible' : 'Print sensible heat transfer rate at boundaries.',
                'rad_heat_trans' : 'Print radiation heat transfer rate at boundaries.',
                'film_mass_flow' : 'Print film mass flow rate at boundaries.',
                'film_heat_transfer' : 'Print film heat transfer rate at boundaries.',
                'pressure_work' : 'Print pressure work rate at moving boundaries.',
                'viscous_work' : 'Print viscous work rate at boundaries.',
            }

        class forces(metaclass=PyMenuMeta):
            __doc__ = 'Force report menu.'
            doc_by_method = {
                'wall_forces' : 'Print integrated pressure and viscous forces on wall zones.',
                'wall_moments' : 'Print integrated pressure and viscous moments on wall zones.',
                'pressure_center' : 'Print center of pressure on wall zones.',
            }

        class reference_values(metaclass=PyMenuMeta):
            __doc__ = 'Reference value menu.'
            doc_by_method = {
                'area' : 'Set reference area for normalization.',
                'depth' : 'Set reference depth for volume calculation.',
                'density' : 'Set reference density for normalization.',
                'enthalpy' : 'Set reference enthalpy for enthalpy damping and normalization.',
                'length' : 'Set reference length for normalization.',
                'pressure' : 'Set reference pressure for normalization.',
                'temperature' : 'Set reference temperature for normalization.',
                'yplus' : 'Set reference yplus for normalization.',
                'velocity' : 'Set reference velocity for normalization.',
                'viscosity' : 'Set reference viscosity for normalization.',
                'zone' : 'Set reference zone.',
                'list' : 'List current reference values.',
            }

            class compute(metaclass=PyMenuMeta):
                __doc__ = 'Enter the compute menu.'
                doc_by_method = {
                    'axis' : 'Compute reference values from a zone of this type.',
                    'degassing' : 'Compute reference values from a zone of this type.',
                    'dummy_entry' : '',
                    'exhaust_fan' : 'Compute reference values from a zone of this type.',
                    'fan' : 'Compute reference values from a zone of this type.',
                    'fluid' : 'Compute reference values from a zone of this type.',
                    'inlet_vent' : 'Compute reference values from a zone of this type.',
                    'intake_fan' : 'Compute reference values from a zone of this type.',
                    'interface' : 'Compute reference values from a zone of this type.',
                    'interior' : 'Compute reference values from a zone of this type.',
                    'mass_flow_inlet' : 'Compute reference values from a zone of this type.',
                    'mass_flow_outlet' : 'Compute reference values from a zone of this type.',
                    'network' : 'Compute reference values from a zone of this type.',
                    'network_end' : 'Compute reference values from a zone of this type.',
                    'outflow' : 'Compute reference values from a zone of this type.',
                    'outlet_vent' : 'Compute reference values from a zone of this type.',
                    'overset' : 'Compute reference values from a zone of this type.',
                    'periodic' : 'Compute reference values from a zone of this type.',
                    'porous_jump' : 'Compute reference values from a zone of this type.',
                    'pressure_far_field' : 'Compute reference values from a zone of this type.',
                    'pressure_inlet' : 'Compute reference values from a zone of this type.',
                    'pressure_outlet' : 'Compute reference values from a zone of this type.',
                    'radiator' : 'Compute reference values from a zone of this type.',
                    'rans_les_interface' : 'Compute reference values from a zone of this type.',
                    'recirculation_inlet' : 'Compute reference values from a zone of this type.',
                    'recirculation_outlet' : 'Compute reference values from a zone of this type.',
                    'shadow' : 'Compute reference values from a zone of this type.',
                    'solid' : 'Compute reference values from a zone of this type.',
                    'symmetry' : 'Compute reference values from a zone of this type.',
                    'velocity_inlet' : 'Compute reference values from a zone of this type.',
                    'wall' : 'Compute reference values from a zone of this type.',
                }

        class surface_integrals(metaclass=PyMenuMeta):
            __doc__ = 'Surface Integral menu.'
            doc_by_method = {
                'area' : 'Print total area of surfaces.',
                'area_weighted_avg' : 'Print area-weighted average of scalar on surfaces.',
                'facet_avg' : 'Print average of scalar at facet centroids of the surfaces.',
                'facet_max' : 'Print maximum of scalar at facet centroids of the surfaces.',
                'facet_min' : 'Print minimum of scalar at facet centroids of the surfaces.',
                'flow_rate' : 'Print flow rate of scalar through surfaces.',
                'integral' : 'Print integral of scalar over surfaces.',
                'mass_flow_rate' : 'Print mass flow rate through surfaces.',
                'mass_weighted_avg' : 'Print mass-average of scalar over surfaces.',
                'standard_deviation' : 'Print standard deviation of scalar',
                'sum' : 'Print sum of scalar at facet centroids of the surfaces.',
                'uniformity_index_area_weighted' : 'Print uniformity index of scalar over surfaces.',
                'uniformity_index_mass_weighted' : 'Print uniformity index of scalar over surfaces.',
                'vector_based_flux' : 'Print custom vector based flux',
                'vector_flux' : 'Print custom vector flux',
                'vector_weighted_average' : 'Print custom vector weighted average',
                'vertex_avg' : 'Print average of scalar at vertices of the surfaces.',
                'vertex_max' : 'Print maximkum of scalar at vertices of the surfaces.',
                'vertex_min' : 'Print minimum of scalar at vertices of the surfaces.',
                'volume_flow_rate' : 'Print volume flow rate through surfaces.',
            }

        class volume_integrals(metaclass=PyMenuMeta):
            __doc__ = 'Volume Integral menu.'
            doc_by_method = {
                'mass' : 'Print total mass of specified cell zones.',
                'mass_avg' : 'Print mass-average of scalar over cell zones.',
                'mass_integral' : 'Print mass-weighted integral of scalar over cell zones.',
                'maximum' : 'Print maximum of scalar over all cell zones.',
                'minimum' : 'Print minimum of scalar over all cell zones.',
                'sum' : 'Print sum of scalar over all cell zones.',
                'twopisum' : 'Print sum of scalar over all cell zones multiplied by 2*Pi.',
                'volume' : 'Print total volume of specified cell zones.',
                'volume_avg' : 'Print volume-weighted average of scalar over cell zones.',
                'volume_integral' : 'Print integral of scalar over cell zones.',
            }

        class modified_setting(metaclass=PyMenuMeta):
            __doc__ = 'Enter the menu for setting up the Modified Settings Summary table.'
            doc_by_method = {
                'modified_setting' : 'Specify which settings will be checked for non-default status for generating the Modified Settings Summary table.',
                'write_user_setting' : 'Write the contents of the Modified Settings Summary table to a file.',
            }

        class population_balance(metaclass=PyMenuMeta):
            __doc__ = 'Population Balance menu.'
            doc_by_method = {
                'moments' : 'Set moments for population balance.',
                'number_density' : 'Set number density functions.',
            }

        class heat_exchanger(metaclass=PyMenuMeta):
            __doc__ = 'Enter the heat exchanger menu.'
            doc_by_method = {
                'computed_heat_rejection' : 'Print total heat rejection.',
                'inlet_temperature' : 'Print inlet temperature.',
                'outlet_temperature' : 'Print outlet temperature.',
                'mass_flow_rate' : 'Print mass flow rate.',
                'specific_heat' : "Print fluid's specific heat.",
            }

        class system(metaclass=PyMenuMeta):
            __doc__ = 'Sytem menu.'
            doc_by_method = {
                'proc_stats' : 'Fluent process information.',
                'sys_stats' : 'System information.',
                'gpgpu_stats' : 'GPGPU information.',
                'time_stats' : 'Time usage information.',
            }

        class simulation_reports(metaclass=PyMenuMeta):
            __doc__ = 'Enter the simulation reports menu.'
            doc_by_method = {
                'list_simulation_reports' : 'List all report names.',
                'generate_simulation_report' : 'Generate a new simulation report or regenerate an existing simulation report with the provided name.',
                'view_simulation_report' : "View a simulation report that has already been generated. In batch mode this will print the report's URL.",
                'export_simulation_report_as_pdf' : 'Export the provided simulation report as a PDF file.',
                'export_simulation_report_as_html' : 'Export the provided simulation report as HTML.',
                'write_report_names_to_file' : 'Write the list of currently generated report names to a txt file.',
                'rename_simulation_report' : 'Rename a report which has already been generated.',
                'duplicate_simulation_report' : 'Duplicate a report and all of its settings to a new report.',
                'reset_report_to_defaults' : 'Reset all report settings to default for the provided simulation report.',
                'delete_simulation_report' : 'Delete the provided simulation report.',
                'write_simulation_report_template_file' : "Write a JSON template file with this case's Simulation Report settings.",
                'read_simulation_report_template_file' : 'Read a JSON template file with existing Simulation Report settings.',
            }

    class surface(metaclass=PyMenuMeta):
        __doc__ = 'Enter the data surface manipulation menu.'
        doc_by_method = {
            'circle_slice' : 'Extract a circular slice.',
            'delete_surface' : 'Remove a defined data surface.',
            'group_surfaces' : 'Group a set of surfaces',
            'ungroup_surface' : 'Ungroup the surface(if grouped)',
            'iso_clip' : 'Clip a data surface (surface, curve, or point) between two iso-values.',
            'iso_surface' : 'Extract an iso-surface (surface, curve, or point) from the curent data field.',
            'expression_volume' : 'Create volume with boolean expression',
            'multiple_iso_surfaces' : 'Create multiple iso-surfaces from the data field at specified spacing.',
            'line_slice' : 'Extract a linear slice.',
            'line_surface' : 'Define a "line" surface by specifying the two endpoint coordinates.',
            'list_surfaces' : 'List the number of facets in the defined surfaces.',
            'mouse_line' : 'Define a line surface using the mouse to select two points.',
            'mouse_plane' : 'Define a plane surface using the mouse to select three points.',
            'mouse_rake' : 'Define a "rake" surface using the mouse to select the end points.',
            'partition_surface' : 'Define a data surface on mesh faces on the partition boundary.',
            'plane' : 'Create a plane given 3 points bounded by the domain.',
            'plane_surface' : 'Create a plane from a coordinate plane, point and normal, or three points.',
            'multiple_plane_surfaces' : 'Create multiple plane surfaces at specified spacing.',
            'plane_slice' : 'Extract a planar slice.',
            'point_array' : 'Extract a rectangular array of data points.',
            'point_surface' : 'Define a "point" surface by specifying the coordinates.',
            'structural_point_surface' : 'Define a "structural point" surface by specifying the coordinates.',
            'quadric_slice' : 'Extract a quadric slice.',
            'rake_surface' : 'Define a "rake" surface by specifying the end points.',
            'rename_surface' : 'Rename a defined data surface.',
            'sphere_slice' : 'Extract a spherical slice.',
            'ellipsoid_slice' : 'Extract a ellipsoid slice.',
            'cone_slice' : 'Extract a cone slice.',
            'surface_cells' : 'Extract all cells intersected by a data surface.',
            'transform_surface' : 'Transform surface.',
            'create_imprint_surface' : 'Imprint surface.',
            'zone_surface' : 'Define a data surface on a mesh zone.',
            'reset_zone_surfaces' : 'Reset case surface list',
            'multiple_zone_surfaces' : 'Create multiple data surfaces at a time.',
            'edit_surface' : 'Edit a defined data surface.',
        }

        class query(metaclass=PyMenuMeta):
            __doc__ = 'Enter surface query menu.'
            doc_by_method = {
                'delete_query' : 'Delete saved query.',
                'list_surfaces' : 'List surfaces.',
                'named_surface_list' : 'Create named list of surfaces.',
                'list_named_selection' : 'List named selection of surface type',
                'list_queries' : 'List all saved queries',
            }

    class graphics_window(metaclass=PyMenuMeta):
        __doc__ = 'Enter graphics window menu'
        doc_by_method = {
            'close_window' : 'Close a user graphics window.',
            'close_window_by_name' : 'Close a reserved graphics window by its name.',
            'open_window' : 'Open a user graphics window.',
            'save_picture' : 'Generate a "hardcopy" of the active window.',
            'set_window' : 'Set a user graphics window to be the active window.',
            'set_window_by_name' : 'Set a reserved graphics window to be the active window by its name.',
            'update_layout' : 'update the fluent layout',
        }

        class embedded_windows(metaclass=PyMenuMeta):
            __doc__ = 'Enter to embed, close, move-out embedded windows'
            doc_by_method = {
                'close' : 'Close an embedded window.',
                'close_all' : 'Close all embedded windows for given parent window.',
                'embed_in' : 'Embed Window into another window',
                'move_out' : 'Move out an embedded window',
                'move_out_all' : 'Move out all embedded windows for given parent window.',
            }

        class picture(metaclass=PyMenuMeta):
            __doc__ = 'Enter the hardcopy/save-picture options menu.'
            doc_by_method = {
                'invert_background' : 'Exchange foreground/background colors for hardcopy.',
                'landscape' : 'Plot hardcopies in landscape or portrait orientation.',
                'preview' : 'Display a preview image of a hardcopy.',
                'x_resolution' : 'Set the width of raster-formatted images in pixels (0 implies current window size).',
                'y_resolution' : 'Set the height of raster-formatted images in pixels (0 implies current window size).',
                'dpi' : 'Set the DPI for EPS and Postscript files, specifies the resolution in dots per inch (DPI) instead of setting the width and height',
                'use_window_resolution' : "Use the currently active window's resolution for hardcopy (ignores the x-resolution and y-resolution in this case).",
                'set_standard_resolution' : 'Select from pre-defined resolution list.',
                'jpeg_hardcopy_quality' : 'To set jpeg hardcopy quality.',
            }

            class color_mode(metaclass=PyMenuMeta):
                __doc__ = 'Enter the hardcopy color mode menu.'
                doc_by_method = {
                    'color' : 'Plot hardcopies in color.',
                    'gray_scale' : 'Convert color to grayscale for hardcopy.',
                    'mono_chrome' : 'Convert color to monochrome (black and white) for hardcopy.',
                    'list' : 'Display the current hardcopy color mode.',
                }

            class driver(metaclass=PyMenuMeta):
                __doc__ = 'Enter the set hardcopy driver menu.'
                doc_by_method = {
                    'dump_window' : 'Set the command used to dump the graphics window to a file.',
                    'eps' : 'Produce encapsulated PostScript (EPS) output for hardcopies.',
                    'jpeg' : 'Produce JPEG output for hardcopies.',
                    'post_script' : 'Produce PostScript output for hardcopies.',
                    'ppm' : 'Produce PPM output for hardcopies.',
                    'tiff' : 'Use TIFF output for hardcopies.',
                    'png' : 'Use PNG output for hardcopies.',
                    'hsf' : 'Use HSF output for hardcopies.',
                    'avz' : 'Use AVZ output for hardcopies.',
                    'glb' : 'Use GLB output for hardcopies.',
                    'vrml' : 'Use VRML output for hardcopies.',
                    'list' : 'List the current hardcopy driver.',
                    'options' : 'Set the hardcopy options. Available options are:\n\\\\n               \t"no gamma correction", disables gamma correction of colors,\n\\\\n               \t"physical size = (width,height)", where width and height\n          are the actual measurements of the printable area of the page\n          in centimeters.\n\\\\n               \t"subscreen = (left,right,bottom,top)", where left,right,\n          bottom, and top are numbers in [-1,1] describing a subwindow on\n          the page in which to place the hardcopy.\n\n\\\\n          The options may be combined by separating them with commas.',
                }

                class post_format(metaclass=PyMenuMeta):
                    __doc__ = 'Enter the PostScript driver format menu.'
                    doc_by_method = {
                        'fast_raster' : 'Use the new raster format.',
                        'raster' : 'Use the original raster format.',
                        'rle_raster' : 'Use the run-length encoded raster format.',
                        'vector' : 'Use vector format.',
                    }

        class windows(metaclass=PyMenuMeta):
            __doc__ = 'Enter the window options menu.'
            doc_by_method = {
                'aspect_ratio' : 'Set the aspect ratio of the active window.',
                'logo' : 'Enable/disable visibility of the logo in graphics window.',
                'ruler' : 'Enable/disable ruler visibility.',
                'logo_color' : 'Set logo color to white/black.',
            }

            class axes(metaclass=PyMenuMeta):
                __doc__ = 'Enter the axes window options menu.'
                doc_by_method = {
                    'border' : 'Enable/disable drawing of a border around the axes window.',
                    'bottom' : 'Set the bottom boundary of the axes window.',
                    'clear' : 'Set the transparency of the axes window.',
                    'right' : 'Set the right boundary of the axes window.',
                    'visible' : 'Enable/disable axes visibility.',
                }

            class main(metaclass=PyMenuMeta):
                __doc__ = 'Enter the main view window options menu.'
                doc_by_method = {
                    'border' : 'Enable/disable drawing of borders around the main viewing window.',
                    'bottom' : 'Set the bottom boundary of the main viewing window.',
                    'left' : 'Set the left boundary of the main viewing window.',
                    'right' : 'Set the right boundary of the main viewing window.',
                    'top' : 'Set the top boundary of the main viewing window.',
                    'visible' : 'Enable/disable visibility of the main viewing window.',
                }

            class scale(metaclass=PyMenuMeta):
                __doc__ = 'Enter the color scale window options menu.'
                doc_by_method = {
                    'border' : 'Enable/disable drawing of borders around the color scale window.',
                    'bottom' : 'Set the bottom boundary of the color scale window.',
                    'clear' : 'Set the transparency of the scale window.',
                    'format' : 'Set the number format of the color scale window (e.g. %0.2e).',
                    'font_size' : 'Set the font size of the color scale window.',
                    'left' : 'Set the left boundary of the color scale window.',
                    'margin' : 'Set the margin of the color scale window.',
                    'right' : 'Set the right boundary of the color scale window.',
                    'top' : 'Set the top boundary of the color scale window.',
                    'visible' : 'Enable/disable visibility of the color scale window.',
                    'alignment' : 'Set colormap to bottom/left/top/right',
                }

            class text(metaclass=PyMenuMeta):
                __doc__ = 'Enter the text window options menu.'
                doc_by_method = {
                    'application' : 'Enable/disable the application name in the picture.',
                    'border' : 'Enable/disable drawing of borders around the text window.',
                    'bottom' : 'Set the bottom boundary of the text window.',
                    'clear' : 'Enable/disable text window transparency.',
                    'company' : 'Enable/disable the company name in the picture.',
                    'date' : 'Enable/disable the date in the picture.',
                    'left' : 'Set the left boundary of the text window.',
                    'right' : 'Set the right boundary of the text window.',
                    'top' : 'Set the top boundary of the text window.',
                    'visible' : 'Enable/disable text window transparency.',
                }

            class video(metaclass=PyMenuMeta):
                __doc__ = 'Enter the video window options menu.'
                doc_by_method = {
                    'background' : 'Set the background color in the video picture.',
                    'color_filter' : 'Set the color filter options for the picture.',
                    'foreground' : 'Set the foreground color in the video picture.',
                    'on' : 'Enable/disable video picture settings.',
                    'pixel_size' : 'Set the window size in pixels.',
                }

            class xy(metaclass=PyMenuMeta):
                __doc__ = 'Enter the X-Y plot window options menu.'
                doc_by_method = {
                    'border' : 'Enable/disable drawing of a border around the X-Y plotter window.',
                    'bottom' : 'Set the bottom boundary of the X-Y plotter window.',
                    'left' : 'Set the left boundary of the X-Y plotter window.',
                    'right' : 'Set the right boundary of the X-Y plotter window.',
                    'top' : 'Set the top boundary of the X-Y plotter window.',
                    'visible' : 'Enable/disable X-Y plotter window visibility.',
                }

        class titles(metaclass=PyMenuMeta):
            __doc__ = 'Set problem title.'
            doc_by_method = {
                'left_top' : 'Set the title text for left top in title segment',
                'left_bottom' : 'Set the title text for left bottom in title segment',
                'right_top' : 'Set the title text for right top in title segment',
                'right_middle' : 'Set the title text for right middle in title segment',
                'right_bottom' : 'Set the title text for right bottom in title segment',
            }

        class views(metaclass=PyMenuMeta):
            __doc__ = 'Enter the view manipulation menu.'
            doc_by_method = {
                'auto_scale' : 'Scale and center the current scene.',
                'default_view' : 'Reset view to front and center.',
                'delete_view' : 'Remove a view from the list.',
                'last_view' : 'Return to the camera position before the last manipulation.',
                'next_view' : 'Return to the camera position after the current position in the stack.',
                'list_views' : 'List predefined and saved views.',
                'restore_view' : 'Use a saved view.',
                'read_views' : 'Read views from a view file.',
                'save_view' : 'Save the current view to the view list.',
                'write_views' : 'Write selected views to a view file.',
            }

            class camera(metaclass=PyMenuMeta):
                __doc__ = 'Enter the camera menu to modify the current viewing parameters.'
                doc_by_method = {
                    'dolly_camera' : 'Adjust the camera position and target.',
                    'field' : 'Set the field of view (width and height).',
                    'orbit_camera' : 'Adjust the camera position without modifying the target.',
                    'pan_camera' : 'Adjust the camera target without modifying the position.',
                    'position' : 'Set the camera position.',
                    'projection' : 'Set the camera projection type.',
                    'roll_camera' : 'Adjust the camera up-vector.',
                    'target' : 'Set the point to be the center of the camera view.',
                    'up_vector' : 'Set the camera up-vector.',
                    'zoom_camera' : 'Adjust the camera field of view.',
                }

        class display_states(metaclass=PyMenuMeta):
            __doc__ = 'Enter the display state manipulation menu.'
            doc_by_method = {
                'list' : 'Print the names of the available display states to the console.',
                'apply' : 'Apply a display state to the active window.',
                'delete' : 'Delete a display state.',
                'use_active' : "Update an existing display state's settings to match those of the active graphics window.",
                'copy' : 'Create a new display state with settings copied from an existing display state.',
                'read' : 'Read display states from a file.',
                'write' : 'Write display states to a file.',
                'edit' : 'Edit a particular display state setting.',
                'create' : 'Create a new display state.',
            }

        class view_sync(metaclass=PyMenuMeta):
            __doc__ = 'Enter the display state manipulation menu.'
            doc_by_method = {
                'list' : 'Print window ids of open windows.',
                'start' : 'Start view synchronization',
                'stop' : 'Stop view synchronization',
                'remove_all' : 'Unsynchronize all windows.',
                'add_all' : 'Synchronize all windows.',
                'add' : 'Add list of window ids for synchronization.',
                'remove' : 'Remove list of window ids from synchronization.',
            }
