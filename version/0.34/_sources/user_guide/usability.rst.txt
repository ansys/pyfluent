.. _ref_usability_features:


Usability features
==================

API search
----------

The :ref:`API search <ref_search>` allows you to search for a word throughout Fluent's object hierarchy. It provides results
based on supported features, including semantic matching, wildcard pattern matching, whole word matching, and misspelled
word correction. Semantic search is the default, with English (``eng``) as the default language. For
a list of supported languages, see `OMW Version 1 <https://omwn.org/omw1.html>`_.

Examples
--------

.. code-block:: python

   >>> import ansys.fluent.core as pyfluent
   >>>
   >>> # Semantic search
   >>> pyfluent.search("speed")
   ...
   <solver_session>.setup.boundary_conditions.wall["<name>"].turbulence.free_stream_velocity (Parameter) (similarity: 98.31%)
   <solver_session>.setup.boundary_conditions.wall["<name>"].wall_film.relative_initial_film_velocity (Parameter) (similarity: 98.31%)
   <solver_session>.setup.boundary_conditions.wall["<name>"].wall_film.upper_deposition_limit_offset (Parameter) (similarity: 98.31%)
   <solver_session>.setup.cell_zone_conditions.fluid["<name>"].disabled.solid_motion_velocity[<index>] (Object) (similarity: 98.31%)
   <solver_session>.setup.cell_zone_conditions.fluid["<name>"].mesh_motion.moving_mesh_velocity[<index>] (Object) (similarity: 98.31%)
   <solver_session>.setup.cell_zone_conditions.fluid["<name>"].phase["<name>"].disabled.solid_motion_velocity[<index>] (Object) (similarity: 98.31%)
   <solver_session>.setup.cell_zone_conditions.fluid["<name>"].phase["<name>"].mesh_motion.moving_mesh_velocity[<index>] (Object) (similarity: 98.31%)
   <solver_session>.setup.cell_zone_conditions.fluid["<name>"].phase["<name>"].reference_frame.reference_frame_velocity[<index>] (Object) (similarity: 98.31%)
   <solver_session>.setup.cell_zone_conditions.fluid["<name>"].reference_frame.reference_frame_velocity[<index>] (Object) (similarity: 98.31%)
   <solver_session>.setup.cell_zone_conditions.solid["<name>"].mesh_motion.moving_mesh_velocity[<index>] (Object) (similarity: 98.31%)
   <solver_session>.setup.cell_zone_conditions.solid["<name>"].phase["<name>"].mesh_motion.moving_mesh_velocity[<index>] (Object) (similarity: 98.31%)
   <solver_session>.setup.cell_zone_conditions.solid["<name>"].phase["<name>"].reference_frame.reference_frame_velocity[<index>] (Object) (similarity: 98.31%)
   <solver_session>.setup.cell_zone_conditions.solid["<name>"].phase["<name>"].solid_motion.solid_motion_velocity[<index>] (Object) (similarity: 98.31%)
   <solver_session>.setup.cell_zone_conditions.solid["<name>"].reference_frame.reference_frame_velocity[<index>] (Object) (similarity: 98.31%)
   <solver_session>.setup.cell_zone_conditions.solid["<name>"].solid_motion.solid_motion_velocity[<index>] (Object) (similarity: 98.31%)
   <solver_session>.setup.dynamic_mesh.dynamic_zones["<name>"].motion.rigid_body_properties.angular_velocity (Parameter) (similarity: 98.31%)
   <solver_session>.setup.dynamic_mesh.dynamic_zones["<name>"].motion.rigid_body_properties.cg_velocity (Parameter) (similarity: 98.31%)
   <solver_session>.setup.dynamic_mesh.options.in_cylinder.crank_shaft_speed (Parameter) (similarity: 98.31%)
   <solver_session>.setup.general.solver.velocity_formulation (Parameter) (similarity: 98.31%)
   <solver_session>.setup.materials.fluid["<name>"].premix_laminar_speed (Object) (similarity: 98.31%)
   <solver_session>.setup.materials.fluid["<name>"].speed_of_sound (Object) (similarity: 98.31%)
   <solver_session>.setup.materials.fluid["<name>"].velocity_accom_coefficient (Object) (similarity: 98.31%)
   <solver_session>.setup.materials.mixture["<name>"].premix_laminar_speed (Object) (similarity: 98.31%)
   ...
   >>>
   >>> # Semantic search within a specific API object
   >>> pyfluent.search("load", api_path="<solver_session>.parallel.partition.set")
   <solver_session>.parallel.partition.set.dpm_load_balancing (Object) (similarity: 98.31%)
   <solver_session>.parallel.partition.set.dpm_load_balancing.load_balancing (Parameter) (similarity: 98.31%)
   <solver_session>.parallel.partition.set.load_distribution (Parameter) (similarity: 98.31%)
   >>>
   >>> # Spanish semantic search
   >>> pyfluent.search("superficie", language="spa")   # search 'surface' in Spanish
   <meshing_session>.PMFileManagement.File["<name>"].Options.Surface (Parameter) (similarity: 100.0%)
   <meshing_session>.meshing_utilities.get_face_zone_area (Query) (similarity: 100.0%)
   <meshing_session>.meshing_utilities.get_face_zones_by_zone_area (Query) (similarity: 100.0%)
   <meshing_session>.meshing_utilities.get_minsize_face_zone_by_area (Query) (similarity: 100.0%)
   <meshing_session>.preferences.Appearance.SurfaceEmissivity (Parameter) (similarity: 100.0%)
   <meshing_session>.preferences.Appearance.SurfaceSpecularity (Parameter) (similarity: 100.0%)
   <meshing_session>.preferences.Appearance.SurfaceSpecularityForContours (Parameter) (similarity: 100.0%)
   <meshing_session>.preferences.Graphics.Performance.SurfaceCaching (Parameter) (similarity: 100.0%)
   <meshing_session>.preferences.Graphics.SurfaceGeneralDisplacement (Parameter) (similarity: 100.0%)
   <solver_session>.design.geometry.parameterize_and_explore.design_change.export.stl_surfaces (Command) (similarity: 100.0%)
   <solver_session>.design.geometry.parameterize_and_explore.design_change.history.surfaces (Parameter) (similarity: 100.0%)
   <solver_session>.design.geometry.parameterize_and_explore.design_change.preview.surfaces (Parameter) (similarity: 100.0%)
   ...
   <solver_session>.mesh.modify_zones.create_periodic_interface (Command) (similarity: 94.12%)
   <solver_session>.mesh.polyhedra.options.preserve_interior_zones (Parameter) (similarity: 94.12%)
   <solver_session>.results.graphics.colors.interface_faces (Parameter) (similarity: 94.12%)
   <solver_session>.results.graphics.colors.interior_faces (Parameter) (similarity: 94.12%)
   <solver_session>.results.graphics.colors.rans_les_interface_faces (Parameter) (similarity: 94.12%)
   <solver_session>.results.graphics.particle_track["<name>"].filter_settings.options.inside (Parameter) (similarity: 94.12%)
   <solver_session>.results.graphics.particle_track["<name>"].filter_settings.options.outside (Parameter) (similarity: 94.12%)
   <solver_session>.results.surfaces.partition_surface["<name>"].interior_cell_faces (Parameter) (similarity: 94.12%)
   <solver_session>.setup.boundary_conditions.interface["<name>"] (Object) (similarity: 94.12%)
   ...
   <solver_session>.setup.boundary_conditions.exhaust_fan["<name>"].structure.x_disp_boundary_condition (Parameter) (similarity: 85.71%)
   <solver_session>.setup.boundary_conditions.exhaust_fan["<name>"].structure.x_disp_boundary_value (Object) (similarity: 85.71%)
   <solver_session>.setup.boundary_conditions.exhaust_fan["<name>"].structure.y_disp_boundary_condition (Parameter) (similarity: 85.71%)
   <solver_session>.setup.boundary_conditions.exhaust_fan["<name>"].structure.y_disp_boundary_value (Object) (similarity: 85.71%)
   <solver_session>.setup.boundary_conditions.exhaust_fan["<name>"].structure.z_disp_boundary_condition (Parameter) (similarity: 85.71%)
   <solver_session>.setup.boundary_conditions.exhaust_fan["<name>"].structure.z_disp_boundary_value (Object) (similarity: 85.71%)
   ...
   <solver_session>.results.graphics.pathline["<name>"].style_attributes.range_sphere (Object) (similarity: 83.33%)
   <solver_session>.results.graphics.pathline["<name>"].style_attributes.sphere_detail_lod (Parameter) (similarity: 83.33%)
   <solver_session>.results.graphics.pathline["<name>"].style_attributes.sphere_lod (Parameter) (similarity: 83.33%)
   <solver_session>.results.graphics.pathline["<name>"].style_attributes.sphere_scale (Parameter) (similarity: 83.33%)
   <solver_session>.results.graphics.pathline["<name>"].style_attributes.sphere_size (Parameter) (similarity: 83.33%)
   ...
   <solver_session>.setup.profiles.display_profile_point_cloud_data (Command) (similarity: 82.35%)
   <solver_session>.setup.profiles.display_profile_surface (Command) (similarity: 82.35%)
   <solver_session>.setup.profiles.list_profile_fields (Command) (similarity: 82.35%)
   <solver_session>.setup.profiles.list_profile_parameters (Command) (similarity: 82.35%)
   <solver_session>.setup.profiles.list_profile_parameters_with_value (Command) (similarity: 82.35%)
   <solver_session>.setup.profiles.list_profiles (Command) (similarity: 82.35%)
   ...
   >>>
   >>> # Chinese semantic search within a specific API object
   >>> pyfluent.search("读", language="cmn", api_path="results")   # search 'read' in Chinese
   <solver_session>.results.animations.playback.read_animation_file (Command) (similarity: 100.0%)
   <solver_session>.results.animations.scene_animation.read_animation (Command) (similarity: 100.0%)
   <solver_session>.results.graphics.views.display_states["<name>"].read (Command) (similarity: 100.0%)
   <solver_session>.results.graphics.views.read_views (Command) (similarity: 100.0%)
   <solver_session>.results.plot.xy_plot["<name>"].read_from_file (Command) (similarity: 100.0%)
   <solver_session>.results.report.discrete_phase.histogram.read_sample_file (Command) (similarity: 100.0%)
   <solver_session>.results.report.simulation_reports.read_simulation_report_template_file (Command) (similarity: 100.0%)
   <solver_session>.tui.results.animations.playback.read_animation_file (Command) (similarity: 100.0%)
   <solver_session>.tui.results.animations.scene_animation.read_animation (Command) (similarity: 100.0%)
   <solver_session>.tui.results.graphics.views.display_states.read (Command) (similarity: 100.0%)
   <solver_session>.tui.results.graphics.views.read_views (Command) (similarity: 100.0%)
   <solver_session>.tui.results.report.discrete_phase.histogram.read_sample_file (Command) (similarity: 100.0%)
   <solver_session>.tui.results.report.simulation_reports.read_simulation_report_template_file (Command) (similarity: 100.0%)
   >>>
   >>> # Whole word search
   >>> pyfluent.search("iteration_at_creation_or_edit", match_whole_word=True) 
   <solver_session>.solution.monitor.convergence_conditions.convergence_reports["<name>"].iteration_at_creation_or_edit (Parameter)
   >>>
   >>> # Whole word search within a specific API object
   >>> pyfluent.search("ApplicationFontSize", match_whole_word=True, api_path="preferences")
   <meshing_session>.preferences.Appearance.ApplicationFontSize (Parameter)
   <solver_session>.preferences.Appearance.ApplicationFontSize (Parameter)
   >>>
   >>> # Wildcard pattern search
   >>> pyfluent.search("local*")
   <solver_session>.setup.dynamic_mesh.methods.smoothing.radial_settings.local_smoothing (Parameter)
   <solver_session>.setup.mesh_interfaces.interface["<name>"].local_absolute_mapped_tolerance (Parameter)
   <solver_session>.setup.mesh_interfaces.interface["<name>"].local_relative_mapped_tolerance (Parameter)
   <solver_session>.setup.models.species.nox.turbulence_interaction.local_tmax_factor (Parameter)
   <solver_session>.solution.controls.pseudo_time_explicit_relaxation_factor.local_dt_dualts_relax["<name>"] (Object)
   <solver_session>.solution.controls.zonal_pbns_solution_controls.local_dt_verbosity (Parameter)
   <solver_session>.solution.initialization.localized_turb_init (Object)
   <meshing_session>.tui.boundary.modify.local_remesh (Command)
   <meshing_session>.tui.boundary.refine.local_regions (Object)
   <meshing_session>.tui.boundary.separate.local_regions (Object)
   <meshing_session>.tui.mesh.hexcore.local_regions (Object)
   <meshing_session>.tui.mesh.poly.local_regions (Object)
   <meshing_session>.tui.mesh.separate.local_regions (Object)
   <meshing_session>.tui.mesh.tet.local_regions (Object)
   <meshing_session>.tui.preferences.simulation.local_residual_scaling (Command)
   ...
   >>>
   >> # Wildcard pattern search within a specific API object
   >>> pyfluent.search("iter*", api_path="<solver_session>.parallel.multidomain") 
   <solver_session>.parallel.multidomain.conjugate_heat_transfer.set.coupling.iter_per_coupling_count (Parameter)
   <solver_session>.parallel.multidomain.conjugate_heat_transfer.set.coupling.single_session_coupling.iteration (Parameter)
   <solver_session>.parallel.multidomain.solve.dual_time_iterate (Command)
   <solver_session>.parallel.multidomain.solve.iterate (Command)
   >>>
   >>> # Misspelled search
   >>> pyfluent.search("cfb_lma")
   <solver_session>.setup.models.viscous.geko.auxiliary_constants.cbf_lam (Parameter)
   <solver_session>.tui.define.models.viscous.geko_options.cbf_lam (Command)
   >>>

