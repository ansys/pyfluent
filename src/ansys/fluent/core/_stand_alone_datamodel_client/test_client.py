# TODO: Later move this to test directory.
import ansys.fluent.core as pyfluent
from ansys.fluent.core._stand_alone_datamodel_client._dummy_client import _DummyClient
from ansys.fluent.core._stand_alone_datamodel_client._preferences_client import (
    _PreferencesClient,
)


def test_preferences_client():
    p_c = _PreferencesClient()
    p_c.run_server(
        r"C:\ANSYSDev\PyFluent_Dev_01\pyfluent-datamodel-server\launch_server\launch_datamodel_server.bat"
    )

    assert p_c.get_state("Appearance/ColorTheme") == "Default"
    assert p_c.get_state("Appearance/GraphicsColorTheme") == "Gray Gradient"

    p_c.set_state(path="Appearance/ColorTheme", state="Dark")

    assert p_c.get_state("Appearance/ColorTheme") == "Dark"
    assert p_c.get_state("Appearance/GraphicsColorTheme") == "Dark"

    assert p_c.get_attrib_value("Appearance/AnsysLogo/Color", "allowedValues") == [
        "White",
        "Black",
    ]

    p_c.close_server()


def test_dummy_client():
    d_c = _DummyClient()
    d_c.run_server(
        r"C:\ANSYSDev\PyFluent_Dev_01\pyfluent-datamodel-server\launch_server\launch_datamodel_server.bat"
    )

    dict_to_merge = {
        "Parent_1": {"child_1": True, "child_2": "Child of Parent_1"},
        "Parent_2": {"child_3": 3.0},
    }

    assert d_c.get_state("Member_1/Sample_Dict_1") is None
    d_c.update_dict("dummy", "Member_1/Sample_Dict_1", dict_to_merge)
    assert d_c.get_state("Member_1/Sample_Dict_1") == dict_to_merge

    d_c.close_server()


def test_preferences_updates_in_fluent():
    p_c = _PreferencesClient()
    p_c.run_server(
        r"C:\ANSYSDev\PyFluent_Dev_01\pyfluent-datamodel-server\launch_server\launch_datamodel_server.bat"
    )

    assert p_c.get_state("Appearance/ColorTheme") == "Default"
    p_c.set_state(path="Appearance/ColorTheme", state="Dark")

    updated_preferences_dict = p_c.get_state(".")

    p_c.close_server()

    session = pyfluent.launch_fluent(mode="solver")

    assert session.preferences.Appearance.ColorTheme() == "Default"
    session.preferences.set_state(updated_preferences_dict)
    assert session.preferences.Appearance.ColorTheme() == "Dark"
    session.preferences.Appearance.ColorTheme.set_state("Default")
    session.exit()
