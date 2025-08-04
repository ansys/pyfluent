# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys

import pytest

import ansys.fluent.core as pyfluent
from ansys.fluent.core.search import (
    _get_api_tree_data,
    _get_capitalize_match_for_word_from_names,
    _get_close_matches_for_word_from_names,
    _get_exact_match_for_word_from_names,
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

    from nltk.corpus import wordnet as wn

    assert wn.langs()


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


@pytest.mark.fluent_version("==26.1")
@pytest.mark.codegen_required
def test_get_wildcard_matches_for_word_from_names():
    api_tree_data = _get_api_tree_data()
    api_object_names = api_tree_data["all_api_object_names"]
    wildcard_matches = _get_wildcard_matches_for_word_from_names(
        "iter*",
        names=api_object_names,
    )
    assert "iter_count" in wildcard_matches
    assert "iterating" in wildcard_matches
    assert "iteration_at_creation_or_edit" in wildcard_matches
    assert "iterations" in wildcard_matches
    assert "iterate" in wildcard_matches
    assert "iterate_steady_2way_fsi" in wildcard_matches
    assert "limiter" not in wildcard_matches


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
    assert (
        "<solver_session>.file.read_surface_mesh (Command) (similarity: 100.0%)"
        in lines
    )

    _search_semantic("フォント", language="jpn", api_tree_data=api_tree_data)
    lines = capsys.readouterr().out.splitlines()
    assert (
        "<solver_session>.tui.preferences.appearance.charts.font (Object) (similarity: 100.0%)"
        in lines
    )


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
    assert "<meshing_session>.tui.preferences.appearance.charts.font (Object)" in lines


@pytest.mark.fluent_version("==24.2")
@pytest.mark.codegen_required
def test_misspelled_search(capsys):
    pyfluent.search("cfb_lma")
    lines = capsys.readouterr().out.splitlines()
    assert (
        "<solver_session>.tui.define.models.viscous.geko_options.cbf_lam (Command)"
        in lines
    )


@pytest.mark.fluent_version("==26.1")
@pytest.mark.codegen_required
def test_wildcard_search(capsys):
    pyfluent.search("local*")
    lines = capsys.readouterr().out.splitlines()
    assert (
        '<solver_session>.setup.mesh_interfaces.interface["<name>"].local_absolute_mapped_tolerance (Parameter)'
        in lines
    )


@pytest.mark.fluent_version("==24.2")
@pytest.mark.codegen_required
def test_chinese_semantic_search(capsys):
    pyfluent.search("读", language="cmn")
    lines = capsys.readouterr().out.splitlines()
    assert "<solver_session>.file.read_case (Command) (similarity: 100.0%)" in lines

    pyfluent.search("写", language="cmn")
    lines = capsys.readouterr().out.splitlines()
    assert "<solver_session>.file.write_case (Command) (similarity: 100.0%)" in lines


@pytest.mark.fluent_version("==24.2")
@pytest.mark.codegen_required
def test_japanese_semantic_search(capsys):
    pyfluent.search("フォント", language="jpn")
    lines = capsys.readouterr().out.splitlines()
    assert (
        "<solver_session>.tui.preferences.appearance.charts.font (Object) (similarity: 100.0%)"
        in lines
    )


def test_match_whole_word(monkeypatch):
    monkeypatch.setattr(pyfluent.config, "print_search_results", False)
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
        "<solver_session>.parent (Object)",
    ]
    assert _search_whole_word("child", api_tree_data=api_tree_data) == [
        "<solver_session>.parent.child (Parameter)",
    ]
    assert pyfluent.search("parent", match_whole_word=True) == [
        "<solver_session>.parent (Object)",
    ]


@pytest.mark.fluent_version("==26.1")
@pytest.mark.codegen_required
def test_solver_api_path():
    import ansys.fluent.core as pyfluent

    pyfluent.config.print_search_results = False
    results = pyfluent.search(search_string="faces_zones", api_path="<solver_session>")
    assert "<meshing_session>" not in results
    assert "<solver_session>.mesh.modify_zones.project_face_zones (Command)" in results
    assert (
        "<solver_session>.tui.mesh.modify_zones.project_face_zones (Command)" in results
    )


@pytest.mark.fluent_version("==26.1")
@pytest.mark.codegen_required
def test_meshing_api_path():
    import ansys.fluent.core as pyfluent

    pyfluent.config.print_search_results = False
    results = pyfluent.search(search_string="faces_zones", api_path="<meshing_session>")
    assert "<solver_session>" not in results
    assert "<meshing_session>.tui.mesh.manage.adjacent_face_zones (Command)" in results
    assert "<meshing_session>.meshing_utilities.merge_face_zones (Command)" in results


@pytest.mark.fluent_version("==26.1")
@pytest.mark.codegen_required
def test_solver_specific_api_path():
    import ansys.fluent.core as pyfluent

    pyfluent.config.print_search_results = False
    results = pyfluent.search(search_string="font", api_path="contour")
    assert "<meshing_session>" not in results
    assert (
        '<solver_session>.results.graphics.contour["<name>"].color_map.font_automatic (Parameter) (similarity: 98.31%)'
        in results
    )


@pytest.mark.fluent_version("==26.1")
@pytest.mark.codegen_required
def test_match_whole_word_with_api_path():
    import ansys.fluent.core as pyfluent

    pyfluent.config.print_search_results = False
    results = pyfluent.search(
        "ApplicationFontSize", match_whole_word=True, api_path="<meshing_session>"
    )
    assert "<solver_session>" not in results
    assert (
        "<meshing_session>.preferences.Appearance.ApplicationFontSize (Parameter)"
        in results
    )


@pytest.mark.fluent_version("==26.1")
@pytest.mark.codegen_required
def test_wildcard_with_api_path():
    import ansys.fluent.core as pyfluent

    pyfluent.config.print_search_results = False
    results = pyfluent.search("local*", api_path="<solver_session>.setup")
    assert "<meshing_session>" not in results
    assert (
        '<solver_session>.setup.mesh_interfaces.interface["<name>"].local_absolute_mapped_tolerance (Parameter)'
        in results
    )


@pytest.mark.fluent_version("==26.1")
@pytest.mark.codegen_required
def test_wildcard_with_api_object():
    import ansys.fluent.core as pyfluent

    pyfluent.config.print_search_results = False
    results = pyfluent.search("local*", api_path="mesh_interfaces")
    assert "<meshing_session>" not in results
    assert (
        '<solver_session>.setup.mesh_interfaces.interface["<name>"].local_absolute_mapped_tolerance (Parameter)'
        in results
    )


@pytest.mark.fluent_version("==26.1")
@pytest.mark.codegen_required
def test_match_whole_word_with_api_object_2():
    import ansys.fluent.core as pyfluent

    pyfluent.config.print_search_results = False
    results = pyfluent.search(
        "ApplicationFontSize", match_whole_word=True, api_path="Appearance"
    )
    assert "<solver_session>" not in results
    assert (
        "<meshing_session>.preferences.Appearance.ApplicationFontSize (Parameter)"
        in results
    )


@pytest.mark.fluent_version("==26.1")
@pytest.mark.codegen_required
def test_semantic_search_read():
    import ansys.fluent.core as pyfluent

    pyfluent.config.print_search_results = False
    results = pyfluent.search("读", language="cmn")
    for result in results:
        assert "thread" not in result
    assert (
        "<solver_session>.file.convert_hanging_nodes_during_read (Parameter) (similarity: 100.0%)"
        in results
    )


@pytest.mark.fluent_version("==26.1")
@pytest.mark.codegen_required
def test_multiple_words():
    import ansys.fluent.core as pyfluent

    pyfluent.config.print_search_results = False
    # TODO: Support semantic search with multiple words
    results = pyfluent.search("remove empty face zones")
    assert "<meshing_session>.tui.mesh.cavity.remove_zones (Command)" in results


@pytest.mark.fluent_version("==26.1")
@pytest.mark.codegen_required
def test_multiple_words_2():
    import ansys.fluent.core as pyfluent

    pyfluent.config.print_search_results = False
    # TODO: Support semantic search with multiple words
    results = pyfluent.search("remove, empty, face, zones")
    assert (
        "<meshing_session>.meshing_utilities.delete_empty_face_zones (Command)"
        in results
    )
