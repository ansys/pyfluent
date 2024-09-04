import pytest

from tests.conftest import new_meshing_session_new_api_enabled  # noqa: F401


@pytest.mark.skip("Pending server availability.")
@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=25.1")
def test_enhanced_meshing_workflow_new_data_model_api(
    new_meshing_session_new_api_enabled,
):
    meshing = new_meshing_session_new_api_enabled
    ft = meshing.fault_tolerant()
    import_cad = ft.import_cad_and_part_management
    assert import_cad.jt_lod.get_state() == 1
    assert import_cad.jt_lod.min() == 1
    assert import_cad.jt_lod.max() == 10
    with pytest.raises(AttributeError):
        import_cad.jt_lod.allowed_values()
    import_cad.jt_lod.set_state(7)
    assert import_cad.jt_lod.get_state() == 7
    assert import_cad.length_unit.allowed_values() == [
        "m",
        "cm",
        "mm",
        "ft",
        "in",
        "um",
        "nm",
    ]
    assert import_cad.jt_lod_append() == 1
    assert import_cad.jt_lod_append.min() == 1
    assert import_cad.jt_lod_append.max() == 10
    assert import_cad.jt_lod_append.is_active() is False
    assert import_cad.part_per_body.is_active()
    assert import_cad.file_loaded() is False
    with pytest.raises(AttributeError):
        import_cad.file_loaded.allowed_values()

    # This command-state subscription testing only
    # works given server-side changes, implemented
    # for the "new" service.

    def on_param_changed(obj):
        on_param_changed.changed = True

    on_param_changed.changed = False

    import_cad.jt_lod.add_on_changed(on_param_changed)
    assert on_param_changed.changed is False
    import_cad.jt_lod.set_state(7)
    assert on_param_changed.changed is False
    import_cad.jt_lod.set_state(6)
    assert on_param_changed.changed is True

    def on_cmd_changed(obj):
        on_cmd_changed.changed = True

    on_cmd_changed.changed = False

    import_cad.add_on_changed(on_cmd_changed)
    import_cad.jt_lod.set_state(4)
    assert on_cmd_changed.changed is True

    # I can't see how on_affected is working without
    # the equivalent changes that were done for on_changed
    def on_affected(obj):
        on_affected.changed = True

    on_affected.changed = False

    import_cad.add_on_affected(on_affected)
    import_cad.jt_lod.set_state(2)
    assert on_affected.changed is True

    # for parameters, on_changed can always be called
    # def on_param_affected(obj):
    #    on_param_affected.changed = True
    # on_param_affected.changed = False

    # import_cad.jt_lod.add_on_affected(on_param_affected)
    # import_cad.jt_lod.set_state(3)
    # assert on_param_affected.changed is True
