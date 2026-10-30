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
   >>> pyfluent.search("font")
   <meshing_session>.meshing_utilities.count_marked_faces (Query) (similarity: 98.31%)
   <meshing_session>.meshing_utilities.delete_marked_faces_in_zones (Command) (similarity: 98.31%)
   <meshing_session>.meshing_utilities.get_free_faces_count (Query) (similarity: 98.31%)
   <meshing_session>.meshing_utilities.get_multi_faces_count (Query) (similarity: 98.31%)
   <meshing_session>.meshing_utilities.get_zones_with_free_faces_for_given_face_zones (Query) (similarity: 98.31%)
   <meshing_session>.meshing_utilities.get_zones_with_marked_faces_for_given_face_zones (Query) (similarity: 98.31%)
   <meshing_session>.meshing_utilities.get_zones_with_multi_faces_for_given_face_zones (Query) (similarity: 98.31%)
   <meshing_session>.meshing_utilities.mark_bad_quality_faces (Query) (similarity: 98.31%)
   <meshing_session>.meshing_utilities.mark_duplicate_faces (Query) (similarity: 98.31%)
   <meshing_session>.meshing_utilities.mark_faces_by_quality (Query) (similarity: 98.31%)
   <meshing_session>.meshing_utilities.mark_faces_deviating_from_size_field (Query) (similarity: 98.31%)
   <meshing_session>.meshing_utilities.mark_faces_in_self_proximity (Query) (similarity: 98.31%)
   <meshing_session>.meshing_utilities.mark_faces_using_node_degree (Query) (similarity: 98.31%)
   <meshing_session>.meshing_utilities.mark_free_faces (Query) (similarity: 98.31%)
   <meshing_session>.meshing_utilities.mark_island_faces (Query) (similarity: 98.31%)
   <meshing_session>.meshing_utilities.mark_multi_faces (Query) (similarity: 98.31%)
   <meshing_session>.meshing_utilities.mark_self_intersecting_faces (Query) (similarity: 98.31%)
   <meshing_session>.meshing_utilities.mark_sliver_faces (Query) (similarity: 98.31%)
   <meshing_session>.meshing_utilities.refine_marked_faces_in_zones (Query) (similarity: 98.31%)
   <meshing_session>.preferences.Appearance.Charts.Font (Object) (similarity: 98.31%)
   <meshing_session>.preferences.Appearance.Charts.Font.Axes (Parameter) (similarity: 98.31%)
   <meshing_session>.preferences.Appearance.Charts.Font.AxesTitles (Parameter) (similarity: 98.31%)
   <meshing_session>.preferences.Appearance.Charts.Font.Legend (Parameter) (similarity: 98.31%)
   <meshing_session>.preferences.Appearance.Charts.Font.Title (Parameter) (similarity: 98.31%)
   ...
   <solver_session>.mesh.swap_mesh_faces (Command) (similarity: 98.31%)
   <solver_session>.preferences.Appearance.Charts.Font (Object) (similarity: 98.31%)
   <solver_session>.preferences.Appearance.Charts.Font.Axes (Parameter) (similarity: 98.31%)
   <solver_session>.preferences.Appearance.Charts.Font.AxesTitles (Parameter) (similarity: 98.31%)
   <solver_session>.preferences.Appearance.Charts.Font.Legend (Parameter) (similarity: 98.31%)
   <solver_session>.preferences.Appearance.Charts.Font.Title (Parameter) (similarity: 98.31%)
   ...
   >>>
   >>> # Semantic search within a specific API object
   >>> pyfluent.search("font", api_path="<solver_session>.results.annotation")
   <solver_session>.results.annotation["<name>"].font_color (Parameter) (similarity: 98.31%)
   <solver_session>.results.annotation["<name>"].font_name (Parameter) (similarity: 98.31%)
   <solver_session>.results.annotation["<name>"].font_size (Parameter) (similarity: 98.31%)
   <solver_session>.results.annotation["<name>"].font_slant (Parameter) (similarity: 98.31%)
   <solver_session>.results.annotation["<name>"].font_weight (Parameter) (similarity: 98.31%)
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

