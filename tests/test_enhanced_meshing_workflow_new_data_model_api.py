import time

import pytest

from ansys.fluent.core import examples

"""
                # enum = IF(LEN(@./allowedValues) == 4, ("none", "right", "left", "in"), ("none", "right", "left", "in", "out"))
Basic interactive test
======================

This checks the backend's mapped data model values directly

import ansys.fluent.core as pf
import time
from ansys.fluent.core import examples
meshing = pf.launch_fluent(mode="meshing", py=True, show_gui=True, start_transcript=False, enable_data_model_api_upgrades=True)
wt = meshing.watertight()
import_file_name = examples.download_file(
    "mixing_elbow.pmdb", "pyfluent/mixing_elbow"
)

wt.import_geometry.file_name.set_state(import_file_name)

assert wt.describe_geometry.setup_type.allowed_values() == ['fluid', 'fluid_solid_voids', 'solid']
wt.describe_geometry.multizone.set_state(True)
wt.describe_geometry()
add_multizone_controls = None

while add_multizone_controls is None:
    try:
        add_multizone_controls = wt.add_multizone_controls
        print(f"got add_multizone_controls {add_multizone_controls}")
    except AttributeError:
        print("Caught AttributeError")
        time.sleep(1)

bias_method = add_multizone_controls.bias_method

# assert bias_method.allowed_values() == ["none", "right", "left", "in"]
bias_method.set_state("right")
assert bias_method.get_state() == "right"


In UI:
meshing.workflow.TaskObject["Describe Geometry"].Arguments.get_state()
{'Multizone': 'Yes'}

Version without latest API update:
=================================

import ansys.fluent.core as pf
import time
from ansys.fluent.core import examples
meshing = pf.launch_fluent(mode="meshing", py=True, show_gui=True, start_transcript=False, enable_data_model_api_upgrades=True)
wt = meshing.watertight()
import_file_name = examples.download_file(
    "mixing_elbow.pmdb", "pyfluent/mixing_elbow"
)

wt.import_geometry.file_name.set_state(import_file_name)

wt.describe_geometry.multizone.set_state("Yes")
wt.describe_geometry()
add_multizone_controls = None

while add_multizone_controls is None:
    try:
        add_multizone_controls = wt.add_multizone_controls
        print(f"got add_multizone_controls {add_multizone_controls}")
    except AttributeError:
        print("Caught AttributeError")
        time.sleep(1)



"""


# @pytest.mark.skip("Pending server availability.")
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

    wt = meshing.watertight()

    import_file_name = examples.download_file(
        "mixing_elbow.pmdb", "pyfluent/mixing_elbow"
    )

    wt.import_geometry.file_name.set_state(import_file_name)

    assert wt.describe_geometry.setup_type.allowed_values() == [
        "fluid",
        "fluid_solid_voids",
        "solid",
    ]

    wt.describe_geometry.multizone.set_state(True)

    wt.describe_geometry()

    add_multizone_controls = None

    while add_multizone_controls is None:
        try:
            add_multizone_controls = wt.add_multizone_controls
            print(f"got add_multizone_controls {add_multizone_controls}")
        except AttributeError:
            print("Caught AttributeError")
            time.sleep(1)
