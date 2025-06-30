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
   <solver_session>.setup.physics.volumes.solid["<name>"].solid_motion.solid_motion_velocity[<index>] (Object) (similarity: 98.31%)
   <solver_session>.setup.physics.volumes.solid["<name>"].solid_motion.solid_motion_velocity[<index>].field_name (Parameter) (similarity: 98.31%)
   <solver_session>.setup.physics.volumes.solid["<name>"].solid_motion.solid_motion_velocity[<index>].list_properties (Command) (similarity: 98.31%)
   <solver_session>.setup.physics.volumes.solid["<name>"].solid_motion.solid_motion_velocity[<index>].option (Parameter) (similarity: 98.31%)
   <solver_session>.setup.physics.volumes.solid["<name>"].solid_motion.solid_motion_velocity[<index>].profile_name (Parameter) (similarity: 98.31%)
   <solver_session>.setup.physics.volumes.solid["<name>"].solid_motion.solid_motion_velocity[<index>].resize (Command) (similarity: 98.31%)
   <solver_session>.setup.physics.volumes.solid["<name>"].solid_motion.solid_motion_velocity[<index>].udf (Parameter) (similarity: 98.31%)
   <solver_session>.setup.physics.volumes.solid["<name>"].solid_motion.solid_motion_velocity[<index>].value (Parameter) (similarity: 98.31%)
   <solver_session>.setup.reference_frames["<name>"].motion.constant_velocity (Object) (similarity: 98.31%)
   <solver_session>.setup.reference_frames["<name>"].motion.constant_velocity.linear_velocity (Parameter) (similarity: 98.31%)
   <solver_session>.setup.reference_frames["<name>"].motion.constant_velocity.rotational_velocity (Object) (similarity: 98.31%)
   <solver_session>.setup.reference_frames["<name>"].motion.constant_velocity.rotational_velocity.rotation_axis (Parameter) (similarity: 98.31%)
   <solver_session>.setup.reference_frames["<name>"].motion.constant_velocity.rotational_velocity.speed (Parameter) (similarity: 98.31%)
   <solver_session>.setup.reference_values.velocity (Parameter) (similarity: 98.31%)
   <solver_session>.solution.initialization.hybrid_init_options.general_settings.initialization_options.const_velocity (Parameter) (similarity: 98.31%)
   <solver_session>.solution.methods.expert.physical_velocity_formulation (Parameter) (similarity: 98.31%)
   <solver_session>.solution.methods.expert.velocity_formulation (Parameter) (similarity: 98.31%)
   <solver_session>.solution.methods.high_speed_numerics (Object) (similarity: 98.31%)
   <solver_session>.solution.methods.high_speed_numerics.enable (Parameter) (similarity: 98.31%)
   <solver_session>.solution.methods.high_speed_numerics.expert (Parameter) (similarity: 98.31%)
   <solver_session>.solution.methods.high_speed_numerics.robust_fluxes (Parameter) (similarity: 98.31%)
   <solver_session>.solution.methods.high_speed_numerics.visualize_pressure_discontinuity_sensor (Parameter) (similarity: 98.31%)
   <solver_session>.solution.methods.multiphase_numerics.advanced_stability_controls.hybrid_nita.instability_detector.set_velocity_limit (Parameter) (similarity: 98.31%)
   ...
   >>>
   >>> # Semantic search within a specific API object
   >>> pyfluent.search("speed", api_path="<solver_session>.solution.methods.multiphase_numerics.solution_stabilization")
   <solver_session>.solution.methods.multiphase_numerics.solution_stabilization.velocity_limiting_treatment (Object) (similarity: 98.31%)
   <solver_session>.solution.methods.multiphase_numerics.solution_stabilization.velocity_limiting_treatment.enable_velocity_limiting (Parameter) (similarity: 98.31%)
   <solver_session>.solution.methods.multiphase_numerics.solution_stabilization.velocity_limiting_treatment.set_damping_strength (Parameter) (similarity: 98.31%)    
   <solver_session>.solution.methods.multiphase_numerics.solution_stabilization.velocity_limiting_treatment.set_damping_strengths["<name>"] (Object) (similarity: 98.31%)
   <solver_session>.solution.methods.multiphase_numerics.solution_stabilization.velocity_limiting_treatment.set_damping_strengths["<name>"].create (Command) (similarity: 98.31%)
   <solver_session>.solution.methods.multiphase_numerics.solution_stabilization.velocity_limiting_treatment.set_damping_strengths["<name>"].delete (Command) (similarity: 98.31%)
   <solver_session>.solution.methods.multiphase_numerics.solution_stabilization.velocity_limiting_treatment.set_damping_strengths["<name>"].list (Command) (similarity: 98.31%)
   <solver_session>.solution.methods.multiphase_numerics.solution_stabilization.velocity_limiting_treatment.set_damping_strengths["<name>"].list_properties (Command) (similarity: 98.31%)
   <solver_session>.solution.methods.multiphase_numerics.solution_stabilization.velocity_limiting_treatment.set_damping_strengths["<name>"].make_a_copy (Command) (similarity: 98.31%)
   <solver_session>.solution.methods.multiphase_numerics.solution_stabilization.velocity_limiting_treatment.set_damping_strengths["<name>"].rename (Command) (similarity: 98.31%)
   <solver_session>.solution.methods.multiphase_numerics.solution_stabilization.velocity_limiting_treatment.set_velocity_and_vof_cutoffs["<name>"] (Object) (similarity: 98.31%)
   <solver_session>.solution.methods.multiphase_numerics.solution_stabilization.velocity_limiting_treatment.set_velocity_and_vof_cutoffs["<name>"].create (Command) (similarity: 98.31%)
   <solver_session>.solution.methods.multiphase_numerics.solution_stabilization.velocity_limiting_treatment.set_velocity_and_vof_cutoffs["<name>"].delete (Command) (similarity: 98.31%)
   <solver_session>.solution.methods.multiphase_numerics.solution_stabilization.velocity_limiting_treatment.set_velocity_and_vof_cutoffs["<name>"].list (Command) (similarity: 98.31%)
   <solver_session>.solution.methods.multiphase_numerics.solution_stabilization.velocity_limiting_treatment.set_velocity_and_vof_cutoffs["<name>"].list_properties (Command) (similarity: 98.31%)
   <solver_session>.solution.methods.multiphase_numerics.solution_stabilization.velocity_limiting_treatment.set_velocity_and_vof_cutoffs["<name>"].make_a_copy (Command) (similarity: 98.31%)
   <solver_session>.solution.methods.multiphase_numerics.solution_stabilization.velocity_limiting_treatment.set_velocity_and_vof_cutoffs["<name>"].max_vel_mag (Parameter) (similarity: 98.31%)
   <solver_session>.solution.methods.multiphase_numerics.solution_stabilization.velocity_limiting_treatment.set_velocity_and_vof_cutoffs["<name>"].rename (Command) (similarity: 98.31%)
   <solver_session>.solution.methods.multiphase_numerics.solution_stabilization.velocity_limiting_treatment.set_velocity_and_vof_cutoffs["<name>"].vol_frac_cutoff (Parameter) (similarity: 98.31%)
   <solver_session>.solution.methods.multiphase_numerics.solution_stabilization.velocity_limiting_treatment.set_velocity_cutoff (Parameter) (similarity: 98.31%)     
   <solver_session>.solution.methods.multiphase_numerics.solution_stabilization.velocity_limiting_treatment.verbosity (Parameter) (similarity: 98.31%)
   >>>
   >>> # Chinese semantic search
   >>> pyfluent.search("读", language="cmn")   # search 'read' in Chinese
   <solver_session>.file.convert_hanging_nodes_during_read (Parameter) (similarity: 100.0%)
   <solver_session>.file.import_.read (Command) (similarity: 100.0%)
   <solver_session>.file.interpolate.read_data (Command) (similarity: 100.0%)
   <solver_session>.file.read (Command) (similarity: 100.0%)
   <solver_session>.file.read_case (Command) (similarity: 100.0%)
   <solver_session>.file.read_case_data (Command) (similarity: 100.0%)
   <solver_session>.file.read_case_lightweight (Command) (similarity: 100.0%)
   <solver_session>.file.read_data (Command) (similarity: 100.0%)
   <solver_session>.file.read_field_functions (Command) (similarity: 100.0%)
   <solver_session>.file.read_injections (Command) (similarity: 100.0%)
   <solver_session>.file.read_isat_table (Command) (similarity: 100.0%)
   <solver_session>.file.read_journal (Command) (similarity: 100.0%)
   <solver_session>.file.read_macros (Command) (similarity: 100.0%)
   <solver_session>.file.read_mesh (Command) (similarity: 100.0%)
   <solver_session>.file.read_pdf (Command) (similarity: 100.0%)
   <solver_session>.file.read_profile (Command) (similarity: 100.0%)
   <solver_session>.file.read_settings (Command) (similarity: 100.0%)
   <solver_session>.file.read_surface_mesh (Command) (similarity: 100.0%)
   <solver_session>.file.table_file_manager.read_table_file (Command) (similarity: 100.0%)
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
   >>> pyfluent.search("ApplicationFontSize", match_whole_word=True)
   <meshing_session>.preferences.Appearance.ApplicationFontSize (Parameter)
   <solver_session>.preferences.Appearance.ApplicationFontSize (Parameter)
   <meshing_session>.tui.preferences.appearance.application_font_size (Command)
   <solver_session>.tui.preferences.appearance.application_font_size (Command)
   >>>
   >>> # Whole word search within a specific API object
   >>> pyfluent.search("ApplicationFontSize", match_whole_word=True, api_path="preferences")
   <meshing_session>.preferences.Appearance.ApplicationFontSize (Parameter)
   <solver_session>.preferences.Appearance.ApplicationFontSize (Parameter)
   >>>
   >>> # Wildcard pattern search
   >>> pyfluent.search("local*")
   <solver_session>.solution.controls.advanced.expert.pseudo_time_method_usage.local_dt["<name>"] (Object)
   <solver_session>.solution.controls.advanced.expert.pseudo_time_method_usage.local_dt["<name>"].create (Command)
   <solver_session>.solution.controls.advanced.expert.pseudo_time_method_usage.local_dt["<name>"].delete (Command)
   <solver_session>.solution.controls.advanced.expert.pseudo_time_method_usage.local_dt["<name>"].enable_pseudo_time_method (Parameter)
   <solver_session>.solution.controls.advanced.expert.pseudo_time_method_usage.local_dt["<name>"].implicit_under_relaxation_factor (Parameter)
   <solver_session>.solution.controls.advanced.expert.pseudo_time_method_usage.local_dt["<name>"].list (Command)
   <solver_session>.solution.controls.advanced.expert.pseudo_time_method_usage.local_dt["<name>"].list_properties (Command)
   <solver_session>.solution.controls.advanced.expert.pseudo_time_method_usage.local_dt["<name>"].make_a_copy (Command)
   <solver_session>.solution.controls.advanced.expert.pseudo_time_method_usage.local_dt["<name>"].pseudo_time_scale_factor (Parameter)
   <solver_session>.solution.controls.advanced.expert.pseudo_time_method_usage.local_dt["<name>"].rename (Command)
   ...
   >>>
   >> # Wildcard pattern search within a specific API object
   >>> pyfluent.search("local*", api_path="mesh_interfaces")
   <solver_session>.setup.mesh_interfaces.interface["<name>"].local_absolute_mapped_tolerance (Parameter)
   <solver_session>.setup.mesh_interfaces.interface["<name>"].local_relative_mapped_tolerance (Parameter)
   >>>
   >>> # Misspelled search
   >>> pyfluent.search("cfb_lma")
   <solver_session>.setup.models.viscous.geko_options.cbf_lam (Parameter)
   <solver_session>.tui.define.models.viscous.geko_options.cbf_lam (Command)
   >>>

