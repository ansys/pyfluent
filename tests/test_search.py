import pytest
from util.fixture_fluent import load_static_mixer_case  # noqa: F401
from util.meshing_workflow import new_watertight_workflow_session  # noqa: F401
from util.solver_workflow import new_solver_session  # noqa: F401

import ansys.fluent.core as pyfluent
from ansys.fluent.core.utils.search import (
    _get_api_object_names,
    _get_close_matches_for_word_from_names,
    _get_version_path_prefix_from_obj,
    _get_wildcard_matches_for_word_from_names,
    _search,
    _search_semantic,
    _search_whole_word,
    _search_wildcard,
)


def test_nltk_data_download():
    import os
    from pathlib import Path

    import nltk
    import platformdirs

    packages = ["wordnet", "omw-1.4"]
    for package in packages:
        nltk.download(package, quiet=True)

    with pytest.raises(LookupError):
        _search_semantic("读", language="cmn")

    user_data_path = Path(platformdirs.user_data_dir()).resolve()
    nltk.data.path.append(user_data_path)
    os.environ["NLTK_DATA"] = user_data_path
    for package in packages:
        nltk.download(package, download_dir=user_data_path, quiet=True)

    with not pytest.raises(LookupError):
        _search_semantic("读", language="cmn")


@pytest.mark.fluent_version("==24.2")
@pytest.mark.codegen_required
def test_get_wildcard_matches_for_word_from_names():
    names = _get_api_object_names()
    wildcard_matches = _get_wildcard_matches_for_word_from_names("iter*", names)
    assert "iterating" in wildcard_matches
    assert "iterate_steady_2way_fsi" in wildcard_matches


@pytest.mark.fluent_version("==24.2")
@pytest.mark.codegen_required
def test_get_close_matches_for_word_from_names():
    names = _get_api_object_names()
    close_matches = _get_close_matches_for_word_from_names("font", names)
    assert "font" in close_matches

    close_matches = _get_close_matches_for_word_from_names("fnt", names)
    assert "font" in close_matches

    close_matches = _get_close_matches_for_word_from_names("solve_flow", names)
    assert "solve_flow_last" in close_matches

    close_matches = _get_close_matches_for_word_from_names("sunshine", names)
    assert "sunshine_factor" in close_matches


@pytest.mark.fluent_version("==24.2")
@pytest.mark.codegen_required
def test_search_wildcard(capsys):
    _search_wildcard("max*")
    lines = capsys.readouterr().out.splitlines()
    assert (
        "<solver_session>.solution.run_calculation.cfl_based_adaptive_time_stepping.max_fixed_time_step (Parameter)"
        in lines
    )

    _search_wildcard("min*")
    lines = capsys.readouterr().out.splitlines()
    assert "<solver_session>.solution.controls.limits.min_des_tke (Parameter)" in lines


@pytest.mark.fluent_version("==24.2")
@pytest.mark.codegen_required
def test_search_whole_word(capsys):
    _search_whole_word("RemovePartitionLinesTolerance", match_case=False)
    lines = capsys.readouterr().out.splitlines()
    assert (
        "<meshing_session>.preferences.Graphics.RemovePartitionLinesTolerance (Parameter)"
        in lines
    )

    _search_whole_word("k0_sei", match_case=False)
    lines = capsys.readouterr().out.splitlines()
    assert (
        "<solver_session>.setup.models.battery.tool_kits.standalone_echem_model.k0_sei (Parameter)"
        in lines
    )


@pytest.mark.fluent_version("==24.2")
@pytest.mark.codegen_required
def test_search_semantic(capsys):
    _search_semantic("读", language="cmn")
    lines = capsys.readouterr().out.splitlines()
    assert "<solver_session>.file.read_surface_mesh (Command)" in lines
    assert "<meshing_session>.meshing.File.ReadJournal (Command)" in lines

    _search_semantic("フォント", language="jpn")
    lines = capsys.readouterr().out.splitlines()
    assert "<solver_session>.tui.preferences.appearance.charts.font (Object)" in lines
    assert "<solver_session>.preferences.Appearance.Charts.Font (Object)" in lines


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
    pyfluent.search("font", match_case=True)
    lines = capsys.readouterr().out.splitlines()
    for line in lines:
        assert "Font" in line
        assert "font" not in line
    assert "<meshing_session>.preferences.Appearance.Charts.Font (Object)" in lines
    assert (
        "<solver_session>.preferences.Graphics.ColormapSettings.TextFontAutomaticUnits (Parameter)"
        in lines
    )


@pytest.mark.fluent_version("==24.2")
@pytest.mark.codegen_required
def test_match_whole_word_and_case_search(capsys):
    pyfluent.search("font", match_whole_word=True, match_case=True)
    lines = capsys.readouterr().out.splitlines()
    for line in lines:
        assert "Font" or "font" in line
    assert "<meshing_session>.preferences.Appearance.Charts.Font (Object)" in lines
    assert (
        "<solver_session>.preferences.Graphics.ColormapSettings.TextFontAutomaticUnits (Parameter)"
        in lines
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
        "<solver_session>.setup.models.viscous.geko_options.cbf_lam (Parameter)"
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
    assert "<meshing_session>.meshing.File.ReadMesh (Command)" in lines

    pyfluent.search("写", language="cmn")
    lines = capsys.readouterr().out.splitlines()
    assert "<solver_session>.file.write_case (Command)" in lines
    assert "<meshing_session>.meshing.File.WriteMesh (Command)" in lines


@pytest.mark.fluent_version("==24.2")
@pytest.mark.codegen_required
def test_japanese_semantic_search(capsys):
    pyfluent.search("フォント", language="jpn")
    lines = capsys.readouterr().out.splitlines()
    assert "<solver_session>.tui.preferences.appearance.charts.font (Object)" in lines
    assert "<solver_session>.preferences.Appearance.Charts.Font (Object)" in lines


@pytest.mark.codegen_required
def test_search(capsys):
    _search("display")
    lines = capsys.readouterr().out.splitlines()
    assert "<meshing_session>.tui.display (Object)" in lines
    assert "<meshing_session>.tui.display.update_scene.display (Command)" in lines
    assert (
        "<meshing_session>.preferences.Graphics.MeshingMode.GraphicsWindowDisplayTimeout (Parameter)"
        in lines
    )
    assert '<solver_session>.results.graphics.mesh["<name>"].display (Command)' in lines
    assert (
        '<solver_session>.results.graphics.mesh["<name>"].display_state_name (Parameter)'
        in lines
    )

    _search("display", match_whole_word=True)
    lines = capsys.readouterr().out.splitlines()
    assert '<solver_session>.results.graphics.mesh["<name>"].display (Command)' in lines
    assert (
        '<solver_session>.results.graphics.mesh["<name>"].display_state_name (Parameter)'
        not in lines
    )

    _search("Display", match_case=True)
    lines = capsys.readouterr().out.splitlines()
    assert "<meshing_session>.tui.display (Object)" not in lines
    assert (
        "<meshing_session>.preferences.Graphics.MeshingMode.GraphicsWindowDisplayTimeout (Parameter)"
        in lines
    )

    _search("GraphicsWindowDisplayTimeout", match_whole_word=True, match_case=True)
    lines = capsys.readouterr().out.splitlines()
    assert (
        "<meshing_session>.preferences.Graphics.MeshingMode.GraphicsWindowDisplayTimeout (Parameter)"
        in lines
    )
    assert (
        "<solver_session>.preferences.Graphics.MeshingMode.GraphicsWindowDisplayTimeoutValue (Parameter)"
        not in lines
    )


@pytest.mark.codegen_required
@pytest.mark.fluent_version("latest")
def test_get_version_path_prefix_from_obj(
    new_watertight_workflow_session, new_solver_session
):
    meshing = new_watertight_workflow_session
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
def test_search_from_root(capsys, new_watertight_workflow_session):
    meshing = new_watertight_workflow_session
    _search("display", search_root=meshing)
    lines = capsys.readouterr().out.splitlines()
    assert "<search_root>.tui.display (Object)" in lines
    _search("display", search_root=meshing.tui)
    lines = capsys.readouterr().out.splitlines()
    assert "<search_root>.display (Object)" in lines
    _search("display", search_root=meshing.tui.display)
    lines = capsys.readouterr().out.splitlines()
    assert "<search_root>.update_scene.display (Command)" in lines
    assert "<search_root>.display_states (Object)" in lines
    _search("cad", search_root=meshing.meshing)
    lines = capsys.readouterr().out.splitlines()
    assert "<search_root>.GlobalSettings.EnableCleanCAD (Parameter)" in lines
    assert "<search_root>.LoadCADGeometry (Command)" in lines
    _search("next", search_root=meshing.workflow)
    lines = capsys.readouterr().out.splitlines()
    assert '<search_root>.TaskObject["<name>"].InsertNextTask (Command)' in lines
    _search("next", search_root=meshing.workflow.TaskObject)
    lines = capsys.readouterr().out.splitlines()
    assert '<search_root>["<name>"].InsertNextTask (Command)' in lines
    _search("next", search_root=meshing.workflow.TaskObject["Import Geometry"])
    lines = capsys.readouterr().out.splitlines()
    assert "<search_root>.InsertNextTask (Command)" in lines
    _search("timeout", search_root=meshing.preferences)
    lines = capsys.readouterr().out.splitlines()
    assert "<search_root>.General.IdleTimeout (Parameter)" in lines
    _search("timeout", search_root=meshing.preferences.General)
    lines = capsys.readouterr().out.splitlines()
    assert "<search_root>.IdleTimeout (Parameter)" in lines


@pytest.mark.codegen_required
@pytest.mark.fluent_version("==23.2")
def test_search_settings_from_root(capsys, load_static_mixer_settings_only):
    solver = load_static_mixer_settings_only
    _search("conduction", search_root=solver)
    lines = capsys.readouterr().out.splitlines()
    assert "<search_root>.tui.define.models.shell_conduction (Object)" in lines
    assert (
        '<search_root>.setup.boundary_conditions.wall["<name>"].phase["<name>"].shell_conduction["<name>"] (Object)'
        in lines
    )
    _search("conduction", search_root=solver.setup.boundary_conditions)
    lines = capsys.readouterr().out.splitlines()
    assert (
        '<search_root>.wall["<name>"].phase["<name>"].shell_conduction["<name>"] (Object)'
        in lines
    )
    _search("conduction", search_root=solver.setup.boundary_conditions.wall)
    lines = capsys.readouterr().out.splitlines()
    assert (
        '<search_root>["<name>"].phase["<name>"].shell_conduction["<name>"] (Object)'
        in lines
    )
    _search("conduction", search_root=solver.setup.boundary_conditions.wall["wall"])
    lines = capsys.readouterr().out.splitlines()
    assert '<search_root>.phase["<name>"].shell_conduction["<name>"] (Object)' in lines
    _search(
        "conduction", search_root=solver.setup.boundary_conditions.wall["wall"].phase
    )
    lines = capsys.readouterr().out.splitlines()
    assert '<search_root>["<name>"].shell_conduction["<name>"] (Object)' in lines
