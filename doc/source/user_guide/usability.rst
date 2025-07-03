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
   >>> pyfluent.search("load", api_path="<solver_session>.parallel.partition.set")
   <solver_session>.parallel.partition.set.dpm_load_balancing (Object) (similarity: 98.31%)
   <solver_session>.parallel.partition.set.dpm_load_balancing.interval (Parameter) (similarity: 98.31%)
   <solver_session>.parallel.partition.set.dpm_load_balancing.load_balancing (Parameter) (similarity: 98.31%)
   <solver_session>.parallel.partition.set.dpm_load_balancing.threshold (Parameter) (similarity: 98.31%)
   <solver_session>.parallel.partition.set.load_distribution (Parameter) (similarity: 98.31%)
   >>>
   >>> # Spanish semantic search
   >>> pyfluent.search("superficie", language="spa")   # search 'surface' in Spanish
   <meshing_session>.preferences.Appearance.SurfaceEmissivity (Parameter) (similarity: 100.0%)
   <meshing_session>.preferences.Appearance.SurfaceSpecularity (Parameter) (similarity: 100.0%)
   <meshing_session>.preferences.Appearance.SurfaceSpecularityForContours (Parameter) (similarity: 100.0%)
   <meshing_session>.preferences.Graphics.Performance.SurfaceCaching (Parameter) (similarity: 100.0%)
   <meshing_session>.preferences.Graphics.SurfaceGeneralDisplacement (Parameter) (similarity: 100.0%)
   <solver_session>.design.geometry.parameterize_and_explore.design_change.export.stl_surfaces (Command) (similarity: 100.0%)
   <solver_session>.design.geometry.parameterize_and_explore.design_change.history.surfaces (Parameter) (similarity: 100.0%)
   <solver_session>.design.geometry.parameterize_and_explore.design_change.preview.surfaces (Parameter) (similarity: 100.0%)
   ...
   <solver_session>.setup.boundary_conditions.intake_fan["<name>"].multiphase.ht_bottom (Object) (similarity: 88.89%)
   <solver_session>.setup.boundary_conditions.intake_fan["<name>"].multiphase.ht_bottom.field_name (Parameter) (similarity: 88.89%)
   <solver_session>.setup.boundary_conditions.intake_fan["<name>"].multiphase.ht_bottom.option (Parameter) (similarity: 88.89%)
   <solver_session>.setup.boundary_conditions.intake_fan["<name>"].multiphase.ht_bottom.profile_name (Parameter) (similarity: 88.89%)
   <solver_session>.setup.boundary_conditions.intake_fan["<name>"].multiphase.ht_bottom.udf (Parameter) (similarity: 88.89%)
   <solver_session>.setup.boundary_conditions.intake_fan["<name>"].multiphase.ht_bottom.value (Parameter) (similarity: 88.89%)
   ...
   <solver_session>.setup.boundary_conditions.outlet_vent["<name>"].list (Command) (similarity: 85.71%)
   <solver_session>.setup.boundary_conditions.outlet_vent["<name>"].list_properties (Command) (similarity: 85.71%)
   <solver_session>.setup.boundary_conditions.outlet_vent["<name>"].make_a_copy (Command) (similarity: 85.71%)
   <solver_session>.setup.boundary_conditions.outlet_vent["<name>"].momentum (Object) (similarity: 85.71%)
   ...
   <solver_session>.results.graphics.pathline["<name>"].axes.rules.x_axis.major_rule_line_color (Parameter) (similarity: 83.33%)
   <solver_session>.results.graphics.pathline["<name>"].axes.rules.x_axis.major_rule_weight (Parameter) (similarity: 83.33%)
   <solver_session>.results.graphics.pathline["<name>"].axes.rules.x_axis.minor_rule_line_color (Parameter) (similarity: 83.33%)
   <solver_session>.results.graphics.pathline["<name>"].axes.rules.x_axis.minor_rule_weight (Parameter) (similarity: 83.33%)
   <solver_session>.results.graphics.pathline["<name>"].axes.rules.y_axis.major_rule_line_color (Parameter) (similarity: 83.33%)
   <solver_session>.results.graphics.pathline["<name>"].axes.rules.y_axis.major_rule_weight (Parameter) (similarity: 83.33%)
   <solver_session>.results.graphics.pathline["<name>"].axes.rules.y_axis.minor_rule_line_color (Parameter) (similarity: 83.33%)
   ...
   <solver_session>.setup.physics.volumes.solid["<name>"].boundaries.pressure_outlet["<name>"].settings.species.tss_scalar["<name>"].profile_name (Parameter) (similarity: 82.35%)
   <solver_session>.setup.physics.volumes.solid["<name>"].boundaries.pressure_outlet["<name>"].settings.structure.x_disp_boundary_value.profile_name (Parameter) (similarity: 82.35%)
   <solver_session>.setup.physics.volumes.solid["<name>"].boundaries.pressure_outlet["<name>"].settings.structure.y_disp_boundary_value.profile_name (Parameter) (similarity: 82.35%)
   <solver_session>.setup.physics.volumes.solid["<name>"].boundaries.pressure_outlet["<name>"].settings.structure.z_disp_boundary_value.profile_name (Parameter) (similarity: 82.35%)
   <solver_session>.setup.physics.volumes.solid["<name>"].boundaries.pressure_outlet["<name>"].settings.thermal.backflow_total_temperature.profile_name (Parameter) (similarity: 82.35%)
   <solver_session>.setup.physics.volumes.solid["<name>"].boundaries.pressure_outlet["<name>"].settings.turbulence.backflow_intermittency.profile_name (Parameter) (similarity: 82.35%)
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
   >>> pyfluent.search("iter*", api_path="<solver_session>.parallel.multidomain") 
   <solver_session>.parallel.multidomain.conjugate_heat_transfer.set.coupling.iter_per_coupling_count (Parameter)
   <solver_session>.parallel.multidomain.conjugate_heat_transfer.set.coupling.single_session_coupling.iteration (Parameter)
   <solver_session>.parallel.multidomain.solve.dual_time_iterate (Command)
   <solver_session>.parallel.multidomain.solve.iterate (Command)
   >>>
   >>> # Misspelled search
   >>> pyfluent.search("cfb_lma")
   <solver_session>.setup.models.viscous.geko_options.cbf_lam (Parameter)
   <solver_session>.tui.define.models.viscous.geko_options.cbf_lam (Command)
   >>>

