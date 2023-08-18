import ansys.fluent.core as pyfluent


def test_search(capsys):
    pyfluent.search("display")
    lines = capsys.readouterr().out.splitlines()
    assert "<meshing_session>.tui.display (Object)" in lines
    assert "<meshing_session>.tui.display.update_scene.display (Command)" in lines
    assert (
        "<meshing_session>.preferences.Graphics.MeshingMode.GraphicsWindowDisplayTimeout (Parameter)"
        in lines
    )
    assert "<solver_session>.results.graphics.mesh[<name>].display (Command)" in lines
    assert (
        "<solver_session>.results.graphics.mesh[<name>].display_state_name (Parameter)"
        in lines
    )

    pyfluent.search("display", match_whole_word=True)
    lines = capsys.readouterr().out.splitlines()
    assert "<solver_session>.results.graphics.mesh[<name>].display (Command)" in lines
    assert (
        "<solver_session>.results.graphics.mesh[<name>].display_state_name (Parameter)"
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
