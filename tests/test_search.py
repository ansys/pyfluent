import sys

import pytest

import ansys.fluent.core as pyfluent
from ansys.fluent.core.search import (
    _get_api_tree_data,
    _get_capitalize_match_for_word_from_names,
    _get_close_matches_for_word_from_names,
    _get_exact_match_for_word_from_names,
    _get_match_case_for_word_from_names,
    _get_wildcard_matches_for_word_from_names,
    _search_semantic,
    _search_whole_word,
    _search_wildcard,
)


@pytest.mark.codegen_required
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
    api_object_names = api_tree_data["all_api_object_names"]
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
    api_object_names = api_tree_data["all_api_object_names"]
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
    api_object_names = api_tree_data["all_api_object_names"]
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
    api_object_names = api_tree_data["all_api_object_names"]
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
    api_object_names = api_tree_data["all_api_object_names"]
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
    assert "<solver_session>.preferences.Appearance.Charts.Font (Object)" in lines


@pytest.mark.fluent_version("==24.2")
@pytest.mark.codegen_required
def test_match_case_search(capsys):
    pyfluent.search("font", match_whole_word=True, match_case=True)
    lines = capsys.readouterr().out.splitlines()
    for line in lines:
        assert "Font" not in line
        assert "font" in line
    assert "<solver_session>.tui.preferences.appearance.charts.font (Object)" in lines
    assert "<meshing_session>.tui.preferences.appearance.charts.font (Object)" in lines


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
    assert "<meshing_session>.tui.display.set_grid.label_font (Command)" in lines


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


def test_match_whole_word(monkeypatch):
    monkeypatch.setattr(pyfluent, "PRINT_SEARCH_RESULTS", False)
    api_tree_data = {
        "api_objects": [
            "<solver_session>.parent (Object)",
            "<solver_session>.parent.child (Parameter)",
            "<solver_session>.first_last (Object)",
            "<solver_session>.none (Object)",
        ],
        "api_tui_objects": [],
        "all_api_object_name_synsets": {
            "parent": ["parent"],
            "child": ["child"],
            "first_last": ["first_last"],
            "none": ["none"],
        },
        "all_api_object_names": ["parent", "child", "first_last", "none"],
    }

    search_module = sys.modules["ansys.fluent.core.search"]
    monkeypatch.setattr(search_module, "_get_api_tree_data", lambda: api_tree_data)

    assert _search_whole_word("parent", api_tree_data=api_tree_data) == [
        "<solver_session>.parent (Object)"
    ]
    assert _search_whole_word("child", api_tree_data=api_tree_data) == [
        "<solver_session>.parent.child (Parameter)"
    ]
    assert pyfluent.search("parent", match_whole_word=True) == [
        "<solver_session>.parent (Object)"
    ]

    assert pyfluent.search("first", match_whole_word=True) == [
        "<solver_session>.first_last (Object)"
    ]
    assert pyfluent.search("last", match_whole_word=True) == [
        "<solver_session>.first_last (Object)"
    ]

    assert pyfluent.search("first_last", match_whole_word=True) == [
        "<solver_session>.first_last (Object)"
    ]
