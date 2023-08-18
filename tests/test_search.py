import pytest
from util.fixture_fluent import load_static_mixer_case  # noqa: F401
from util.meshing_workflow import new_watertight_workflow_session  # noqa: F401
from util.solver_workflow import new_solver_session  # noqa: F401

import ansys.fluent.core as pyfluent
from ansys.fluent.core.utils.search import _get_version_path_prefix_from_obj


def test_search(capsys):
    pyfluent.search("display")
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

    pyfluent.search("display", match_whole_word=True)
    lines = capsys.readouterr().out.splitlines()
    assert '<solver_session>.results.graphics.mesh["<name>"].display (Command)' in lines
    assert (
        '<solver_session>.results.graphics.mesh["<name>"].display_state_name (Parameter)'
        not in lines
    )

    pyfluent.search("Display", match_case=True)
    lines = capsys.readouterr().out.splitlines()
    assert "<meshing_session>.tui.display (Object)" not in lines
    assert (
        "<meshing_session>.preferences.Graphics.MeshingMode.GraphicsWindowDisplayTimeout (Parameter)"
        in lines
    )

    pyfluent.search(
        "GraphicsWindowDisplayTimeout", match_whole_word=True, match_case=True
    )
    lines = capsys.readouterr().out.splitlines()
    assert (
        "<meshing_session>.preferences.Graphics.MeshingMode.GraphicsWindowDisplayTimeout (Parameter)"
        in lines
    )
    assert (
        "<solver_session>.preferences.Graphics.MeshingMode.GraphicsWindowDisplayTimeoutValue (Parameter)"
        not in lines
    )


@pytest.mark.fluent_version("latest")
def test_get_version_path_prefix_from_obj(
    new_watertight_workflow_session, new_solver_session
):
    meshing = new_watertight_workflow_session
    solver = new_solver_session
    version = solver.version
    assert _get_version_path_prefix_from_obj(meshing) == (
        version,
        ["<meshing_session>"],
        "<root>",
    )
    assert _get_version_path_prefix_from_obj(solver) == (
        version,
        ["<solver_session>"],
        "<root>",
    )
    assert _get_version_path_prefix_from_obj(meshing.tui.file.import_) == (
        version,
        ["<meshing_session>", "tui", "file", "import_"],
        "<root>",
    )
    assert _get_version_path_prefix_from_obj(meshing.tui.file.read_case) == (
        None,
        None,
        None,
    )
    assert _get_version_path_prefix_from_obj(meshing.meshing) == (
        version,
        ["<meshing_session>", "meshing"],
        "<root>",
    )
    assert _get_version_path_prefix_from_obj(meshing.workflow) == (
        version,
        ["<meshing_session>", "workflow"],
        "<root>",
    )
    assert _get_version_path_prefix_from_obj(solver.workflow) == (
        version,
        ["<meshing_session>", "workflow"],
        "<root>",
    )
    assert _get_version_path_prefix_from_obj(meshing.workflow.TaskObject) == (
        version,
        ["<meshing_session>", "workflow", "TaskObject:<name>"],
        '<root>["<name>"]',
    )
    assert _get_version_path_prefix_from_obj(
        meshing.workflow.TaskObject["Import Geometry"]
    ) == (version, ["<meshing_session>", "workflow", "TaskObject:<name>"], "<root>")
    assert _get_version_path_prefix_from_obj(meshing.preferences.Appearance.Charts) == (
        version,
        ["<solver_session>", "preferences", "Appearance", "Charts"],
        "<root>",
    )
    assert _get_version_path_prefix_from_obj(solver.setup.models) == (
        version,
        ["<solver_session>"],
        "<root>",
    )
    assert _get_version_path_prefix_from_obj(solver.file.cff_files) == (
        None,
        None,
        None,
    )


@pytest.mark.fluent_version("latest")
def test_search_from_root(capsys, new_watertight_workflow_session):
    meshing = new_watertight_workflow_session
    pyfluent.search("display", root=meshing)
    lines = capsys.readouterr().out.splitlines()
    assert "<root>.tui.display (Object)" in lines
    pyfluent.search("display", root=meshing.tui)
    lines = capsys.readouterr().out.splitlines()
    assert "<root>.display (Object)" in lines
    pyfluent.search("display", root=meshing.tui.display)
    lines = capsys.readouterr().out.splitlines()
    assert "<root>.update_scene.display (Command)" in lines
    assert "<root>.display_states (Object)" in lines
    pyfluent.search("cad", root=meshing.meshing)
    lines = capsys.readouterr().out.splitlines()
    assert "<root>.GlobalSettings.EnableCleanCAD (Parameter)" in lines
    assert "<root>.LoadCADGeometry (Command)" in lines
    pyfluent.search("next", root=meshing.workflow)
    lines = capsys.readouterr().out.splitlines()
    assert '<root>.TaskObject["<name>"].InsertNextTask (Command)' in lines
    pyfluent.search("next", root=meshing.workflow.TaskObject)
    lines = capsys.readouterr().out.splitlines()
    assert '<root>["<name>"].InsertNextTask (Command)' in lines
    pyfluent.search("next", root=meshing.workflow.TaskObject["Import Geometry"])
    lines = capsys.readouterr().out.splitlines()
    assert "<root>.InsertNextTask (Command)" in lines
    pyfluent.search("timeout", root=meshing.preferences)
    lines = capsys.readouterr().out.splitlines()
    assert "<root>.General.IdleTimeout (Parameter)" in lines
    pyfluent.search("timeout", root=meshing.preferences.General)
    lines = capsys.readouterr().out.splitlines()
    assert "<root>.IdleTimeout (Parameter)" in lines


@pytest.mark.fluent_version("latest")
def test_search_settings_from_root(capsys, load_static_mixer_case):
    solver = load_static_mixer_case
    pyfluent.search("conduction", root=solver)
    lines = capsys.readouterr().out.splitlines()
    assert "<root>.tui.define.models.shell_conduction (Object)" in lines
    assert (
        '<root>.setup.boundary_conditions.wall["<name>"].phase["<name>"].shell_conduction["<name>"] (Object)'
        in lines
    )
    pyfluent.search("conduction", root=solver.setup.boundary_conditions)
    lines = capsys.readouterr().out.splitlines()
    assert (
        '<root>.wall["<name>"].phase["<name>"].shell_conduction["<name>"] (Object)'
        in lines
    )
    pyfluent.search("conduction", root=solver.setup.boundary_conditions.wall)
    lines = capsys.readouterr().out.splitlines()
    assert (
        '<root>["<name>"].phase["<name>"].shell_conduction["<name>"] (Object)' in lines
    )
    pyfluent.search("conduction", root=solver.setup.boundary_conditions.wall["wall"])
    lines = capsys.readouterr().out.splitlines()
    assert '<root>.phase["<name>"].shell_conduction["<name>"] (Object)' in lines
    pyfluent.search(
        "conduction", root=solver.setup.boundary_conditions.wall["wall"].phase
    )
    lines = capsys.readouterr().out.splitlines()
    assert '<root>["<name>"].shell_conduction["<name>"] (Object)' in lines
