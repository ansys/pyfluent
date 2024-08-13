import pytest

import ansys.fluent.core as pyfluent
from ansys.fluent.core.search import (
    _get_api_tree_data,
    _get_capitalize_match_for_word_from_names,
    _get_close_matches_for_word_from_names,
    _get_exact_match_for_word_from_names,
    _get_match_case_for_word_from_names,
    _get_version_path_prefix_from_obj,
    _get_wildcard_matches_for_word_from_names,
    _search,
    _search_semantic,
    _search_whole_word,
    _search_wildcard,
)


@pytest.mark.fluent_version("==24.2")
def test_nltk_data_download():
    import nltk

    packages = ["wordnet", "omw-1.4"]
    for package in packages:
        nltk.download(package, quiet=True)

    api_tree_data = _get_api_tree_data()
    _search_semantic("读", language="cmn", api_tree_data=api_tree_data)


@pytest.mark.fluent_version("==24.2")
@pytest.mark.codegen_required
def test_get_exact_match_for_word_from_names():
    api_tree_data = _get_api_tree_data()
    api_object_names = list(api_tree_data["all_api_object_name_synsets"].keys())
    exact_match = _get_exact_match_for_word_from_names(
        "VideoResoutionY",
        names=api_object_names,
    )
    assert "VideoResoutionY" in exact_match
    assert len(exact_match) == 1


@pytest.mark.fluent_version("==24.2")
@pytest.mark.codegen_required
def test_get_capitalize_match_for_word_from_names():
    api_tree_data = _get_api_tree_data()
    api_object_names = list(api_tree_data["all_api_object_name_synsets"].keys())
    capitalize_match_cases = _get_capitalize_match_for_word_from_names(
        "font",
        names=api_object_names,
    )
    assert "font" not in capitalize_match_cases
    assert set(capitalize_match_cases) == set(
        [
            "TextFontAutomaticHorizontalSize",
            "TextFontName",
            "TextFontFixedHorizontalSize",
            "TextFontFixedSize",
            "TextFontAutomaticSize",
            "TextFontFixedVerticalSize",
            "TextFontAutomaticVerticalSize",
            "ApplicationFontSize",
            "TextFontFixedUnits",
            "TextFontAutomaticUnits",
            "Font",
        ]
    )


@pytest.mark.fluent_version("==24.2")
@pytest.mark.codegen_required
def test_get_match_case_for_word_from_names():
    api_tree_data = _get_api_tree_data()
    api_object_names = list(api_tree_data["all_api_object_name_synsets"].keys())
    match_cases = _get_match_case_for_word_from_names(
        "font",
        names=api_object_names,
    )
    for match_case in match_cases:
        assert "Font" not in match_case
        assert "font" in match_case
    assert set(match_cases) == set(
        [
            "text_font_fixed_units",
            "text_font_automatic_horizontal_size",
            "font_name",
            "font_size",
            "text_font_fixed_size",
            "label_font",
            "text_font_fixed_vertical_size",
            "text_font_automatic_vertical_size",
            "text_font_automatic_units",
            "font",
            "text_font_automatic_size",
            "text_font_fixed_horizontal_size",
            "application_font_size",
            "font_automatic",
            "text_font_name",
        ]
    )


@pytest.mark.fluent_version("==24.2")
@pytest.mark.codegen_required
def test_get_wildcard_matches_for_word_from_names():
    api_tree_data = _get_api_tree_data()
    api_object_names = list(api_tree_data["all_api_object_name_synsets"].keys())
    wildcard_matches = _get_wildcard_matches_for_word_from_names(
        "iter*",
        names=api_object_names,
    )
    assert set(wildcard_matches) == set(
        [
            "iter_count",
            "iterating",
            "iter_per_coupling_count",
            "iteration_at_creation_or_edit",
            "iteration_interval",
            "iteration_number_of_samples_or_levels",
            "iterations",
            "iterate",
            "iterate_steady_2way_fsi",
            "iteration",
            "iteration_sampling_type",
            "iteration_count",
            "iteration_parameters",
        ]
    )


@pytest.mark.fluent_version("==24.2")
@pytest.mark.codegen_required
def test_get_close_matches_for_word_from_names():
    api_tree_data = _get_api_tree_data()
    api_object_names = list(api_tree_data["all_api_object_name_synsets"].keys())
    close_matches = _get_close_matches_for_word_from_names(
        "font",
        names=api_object_names,
    )
    assert "font" in close_matches

    close_matches = _get_close_matches_for_word_from_names(
        "fnt",
        names=api_object_names,
    )
    assert "font" in close_matches

    close_matches = _get_close_matches_for_word_from_names(
        "solve_flow",
        names=api_object_names,
    )
    assert "solve_flow_last" in close_matches

    close_matches = _get_close_matches_for_word_from_names(
        "sunshine",
        names=api_object_names,
    )
    assert "sunshine_factor" in close_matches


@pytest.mark.fluent_version("==24.2")
@pytest.mark.codegen_required
def test_search_wildcard(capsys):
    api_tree_data = _get_api_tree_data()
    _search_wildcard(
        "max*",
        api_tree_data=api_tree_data,
    )
    lines = capsys.readouterr().out.splitlines()
    assert (
        "<solver_session>.solution.run_calculation.cfl_based_adaptive_time_stepping.max_fixed_time_step (Parameter)"
        in lines
    )

    _search_wildcard(
        "min*",
        api_tree_data=api_tree_data,
    )
    lines = capsys.readouterr().out.splitlines()
    assert "<solver_session>.solution.controls.limits.min_des_tke (Parameter)" in lines


@pytest.mark.fluent_version("==24.2")
@pytest.mark.codegen_required
def test_search_whole_word(capsys):
    api_tree_data = _get_api_tree_data()
    _search_whole_word(
        "RemovePartitionLinesTolerance",
        match_case=False,
        api_tree_data=api_tree_data,
    )
    lines = capsys.readouterr().out.splitlines()
    assert (
        "<meshing_session>.preferences.Graphics.RemovePartitionLinesTolerance (Parameter)"
        in lines
    )

    _search_whole_word(
        "k0_sei",
        match_case=False,
        api_tree_data=api_tree_data,
    )
    lines = capsys.readouterr().out.splitlines()
    assert (
        "<solver_session>.setup.models.battery.tool_kits.standalone_echem_model.k0_sei (Parameter)"
        in lines
    )


@pytest.mark.fluent_version("==24.2")
@pytest.mark.codegen_required
def test_search_semantic(capsys):
    api_tree_data = _get_api_tree_data()
    _search_semantic("读", language="cmn", api_tree_data=api_tree_data)
    lines = capsys.readouterr().out.splitlines()
    assert "<solver_session>.file.read_surface_mesh (Command)" in lines

    _search_semantic("フォント", language="jpn", api_tree_data=api_tree_data)
    lines = capsys.readouterr().out.splitlines()
    assert "<solver_session>.tui.preferences.appearance.charts.font (Object)" in lines


@pytest.mark.fluent_version("==24.2")
@pytest.mark.codegen_required
def test_whole_word_search(capsys):
    pyfluent.search("Font", match_whole_word=True)
    lines = capsys.readouterr().out.splitlines()
    assert "font" not in lines
    assert "<meshing_session>.preferences.Appearance.Charts.Font (Object)" in lines
    assert (
        "<solver_session>.preferences.Graphics.ColormapSettings.TextFontAutomaticUnits (Parameter)"
        in lines
    )


@pytest.mark.fluent_version("==24.2")
@pytest.mark.codegen_required
def test_match_case_search(capsys):
    pyfluent.search("font", match_whole_word=True, match_case=True)
    lines = capsys.readouterr().out.splitlines()
    for line in lines:
        assert "Font" not in line
        assert "font" in line
    assert (
        '<solver_session>.results.graphics.pathline["<name>"].color_map.font_name (Parameter)'
        in lines
    )
    assert (
        '<solver_session>.results.graphics.vector["<name>"].color_map.font_automatic (Parameter)'
        in lines
    )


@pytest.mark.fluent_version("==24.2")
@pytest.mark.codegen_required
def test_match_whole_word_and_case_search(capsys):
    pyfluent.search("font", match_whole_word=True, match_case=True)
    lines = capsys.readouterr().out.splitlines()
    for line in lines:
        assert "font" in line
        assert "Font" not in line
    assert "<meshing_session>.preferences.Appearance.Charts.Font (Object)" not in lines
    assert (
        "<solver_session>.preferences.Graphics.ColormapSettings.TextFontAutomaticUnits (Parameter)"
        not in lines
    )
    assert (
        '<solver_session>.results.graphics.lic["<name>"].color_map.font_name (Parameter)'
        in lines
    )


@pytest.mark.fluent_version("==24.2")
@pytest.mark.codegen_required
def test_misspelled_search(capsys):
    pyfluent.search("cfb_lma")
    lines = capsys.readouterr().out.splitlines()
    assert (
        "<solver_session>.tui.define.models.viscous.geko_options.cbf_lam (Command)"
        in lines
    )


@pytest.mark.fluent_version("==24.2")
@pytest.mark.codegen_required
def test_wildcard_search(capsys):
    pyfluent.search("iter*", wildcard=True)
    lines = capsys.readouterr().out.splitlines()
    assert "<solver_session>.solution.run_calculation.iter_count (Parameter)" in lines
    assert "<solver_session>.solution.run_calculation.iterating (Query)" in lines


@pytest.mark.fluent_version("==24.2")
@pytest.mark.codegen_required
def test_chinese_semantic_search(capsys):
    pyfluent.search("读", language="cmn")
    lines = capsys.readouterr().out.splitlines()
    assert "<solver_session>.file.read_case (Command)" in lines

    pyfluent.search("写", language="cmn")
    lines = capsys.readouterr().out.splitlines()
    assert "<solver_session>.file.write_case (Command)" in lines


@pytest.mark.fluent_version("==24.2")
@pytest.mark.codegen_required
def test_japanese_semantic_search(capsys):
    pyfluent.search("フォント", language="jpn")
    lines = capsys.readouterr().out.splitlines()
    assert "<solver_session>.tui.preferences.appearance.charts.font (Object)" in lines


@pytest.mark.codegen_required
def test_search():
    results = _search("display")
    assert "<meshing_session>.tui.display (Object)" in results
    assert "<meshing_session>.tui.display.update_scene.display (Command)" in results
    assert (
        "<meshing_session>.preferences.Graphics.MeshingMode.GraphicsWindowDisplayTimeout (Parameter)"
        in results
    )
    assert (
        '<solver_session>.results.graphics.mesh["<name>"].display (Command)' in results
    )
    assert (
        '<solver_session>.results.graphics.mesh["<name>"].display_state_name (Parameter)'
        in results
    )

    results = _search("display", match_whole_word=True)
    assert (
        '<solver_session>.results.graphics.mesh["<name>"].display (Command)' in results
    )
    assert (
        '<solver_session>.results.graphics.mesh["<name>"].display_state_name (Parameter)'
        not in results
    )

    results = _search("Display", match_case=True)
    assert "<meshing_session>.tui.display (Object)" not in results
    assert (
        "<meshing_session>.preferences.Graphics.MeshingMode.GraphicsWindowDisplayTimeout (Parameter)"
        in results
    )

    results = _search(
        "GraphicsWindowDisplayTimeout", match_whole_word=True, match_case=True
    )
    assert (
        "<meshing_session>.preferences.Graphics.MeshingMode.GraphicsWindowDisplayTimeout (Parameter)"
        in results
    )
    assert (
        "<solver_session>.preferences.Graphics.MeshingMode.GraphicsWindowDisplayTimeoutValue (Parameter)"
        not in results
    )


@pytest.mark.codegen_required
@pytest.mark.fluent_version("latest")
def test_get_version_path_prefix_from_obj(
    watertight_workflow_session, new_solver_session
):
    meshing = watertight_workflow_session
    solver = new_solver_session
    version = solver._version
    assert _get_version_path_prefix_from_obj(meshing) == (
        version,
        ["<meshing_session>"],
        "<search_root>",
    )
    assert _get_version_path_prefix_from_obj(solver) == (
        version,
        ["<solver_session>"],
        "<search_root>",
    )
    assert _get_version_path_prefix_from_obj(meshing.tui.file.import_) == (
        version,
        ["<meshing_session>", "tui", "file", "import_"],
        "<search_root>",
    )
    assert _get_version_path_prefix_from_obj(meshing.tui.file.read_case) == (
        None,
        None,
        None,
    )
    assert _get_version_path_prefix_from_obj(meshing.meshing) == (
        version,
        ["<meshing_session>", "meshing"],
        "<search_root>",
    )
    assert _get_version_path_prefix_from_obj(meshing.workflow) == (
        version,
        ["<meshing_session>", "workflow"],
        "<search_root>",
    )
    assert _get_version_path_prefix_from_obj(solver.workflow) == (
        version,
        ["<meshing_session>", "workflow"],
        "<search_root>",
    )
    assert _get_version_path_prefix_from_obj(meshing.workflow.TaskObject) == (
        version,
        ["<meshing_session>", "workflow", "TaskObject:<name>"],
        '<search_root>["<name>"]',
    )
    assert _get_version_path_prefix_from_obj(
        meshing.workflow.TaskObject["Import Geometry"]
    ) == (
        version,
        ["<meshing_session>", "workflow", "TaskObject:<name>"],
        "<search_root>",
    )
    assert _get_version_path_prefix_from_obj(meshing.preferences.Appearance.Charts) == (
        version,
        ["<solver_session>", "preferences", "Appearance", "Charts"],
        "<search_root>",
    )
    assert _get_version_path_prefix_from_obj(solver.setup.models) == (
        version,
        ["<solver_session>"],
        "<search_root>",
    )
    assert _get_version_path_prefix_from_obj(solver.file.cff_files) == (
        None,
        None,
        None,
    )


@pytest.mark.codegen_required
@pytest.mark.fluent_version("latest")
def test_search_from_root(watertight_workflow_session):
    meshing = watertight_workflow_session
    results = _search("display", search_root=meshing)
    assert "<search_root>.tui.display (Object)" in results
    results = _search("display", search_root=meshing.tui)
    assert "<search_root>.display (Object)" in results
    results = _search("display", search_root=meshing.tui.display)
    assert "<search_root>.update_scene.display (Command)" in results
    assert "<search_root>.display_states (Object)" in results
    results = _search("cad", search_root=meshing.meshing)
    assert "<search_root>.GlobalSettings.EnableCleanCAD (Parameter)" in results
    assert "<search_root>.LoadCADGeometry (Command)" in results
    results = _search("next", search_root=meshing.workflow)
    assert '<search_root>.TaskObject["<name>"].InsertNextTask (Command)' in results
    results = _search("next", search_root=meshing.workflow.TaskObject)
    assert '<search_root>["<name>"].InsertNextTask (Command)' in results
    results = _search(
        "next", search_root=meshing.workflow.TaskObject["Import Geometry"]
    )
    assert "<search_root>.InsertNextTask (Command)" in results
    results = _search("timeout", search_root=meshing.preferences)
    assert "<search_root>.General.IdleTimeout (Parameter)" in results
    results = _search("timeout", search_root=meshing.preferences.General)
    assert "<search_root>.IdleTimeout (Parameter)" in results


@pytest.mark.skip("Results are varying each time.")
@pytest.mark.codegen_required
@pytest.mark.fluent_version("==23.2")
def test_search_settings_from_root(capsys, static_mixer_settings_session):
    solver = static_mixer_settings_session
    results = _search("conduction", search_root=solver)
    assert "<search_root>.tui.define.models.shell_conduction (Object)" in results
    assert (
        '<search_root>.setup.boundary_conditions.wall["<name>"].phase["<name>"].thermal.enable_shell_conduction (Parameter)'
        in results
    )
    results = _search("conduction", search_root=solver.setup.boundary_conditions)
    assert (
        '<search_root>.wall["<name>"].phase["<name>"].shell_conduction["<name>"] (Object)'
        in results
    )
    results = _search("conduction", search_root=solver.setup.boundary_conditions.wall)
    assert (
        '<search_root>["<name>"].phase["<name>"].shell_conduction["<name>"] (Object)'
        in results
    )
    results = _search(
        "conduction", search_root=solver.setup.boundary_conditions.wall["wall"]
    )
    assert (
        '<search_root>.phase["<name>"].shell_conduction["<name>"] (Object)' in results
    )
    results = _search(
        "conduction", search_root=solver.setup.boundary_conditions.wall["wall"].phase
    )
    assert '<search_root>["<name>"].shell_conduction["<name>"] (Object)' in results
