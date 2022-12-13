import ansys.fluent.core as pyfluent
from ansys.fluent.core._stand_alone_datamodel_client._datamodel_client import (
    close_server,
    run_datamodel_server,
)


def test_preferences_client():
    preferences = run_datamodel_server(
        r"C:\ANSYSDev\PyFluent_Dev_01\pyfluent-datamodel-server\launch_server\launch_datamodel_server.bat",
        "preferences",
    )

    assert preferences.Appearance.ColorTheme.get_state() == "Default"
    assert preferences.Appearance.GraphicsColorTheme.get_state() == "Gray Gradient"

    preferences.Appearance.ColorTheme.set_state("Dark")

    assert preferences.Appearance.ColorTheme.get_state() == "Dark"
    assert preferences.Appearance.GraphicsColorTheme.get_state() == "Dark"

    assert preferences.Appearance.AnsysLogo.Color.get_attr("allowedValues") == [
        "White",
        "Black",
    ]
    close_server()


def test_dummy_client():
    dummy = run_datamodel_server(
        r"C:\ANSYSDev\PyFluent_Dev_01\pyfluent-datamodel-server\launch_server\launch_datamodel_server.bat",
        "dummy",
    )

    dict_to_merge = {
        "Parent_1": {"child_1": True, "child_2": "Child of Parent_1"},
        "Parent_2": {"child_3": 3.0},
    }

    assert dummy.Member_1()["Sample_Dict_1"] is None
    dummy.Member_1.Sample_Dict_1.update_dict(dict_to_merge)
    assert dummy.Member_1()["Sample_Dict_1"] == dict_to_merge

    close_server()


def test_preferences_updates_in_fluent():
    preferences = run_datamodel_server(
        r"C:\ANSYSDev\PyFluent_Dev_01\pyfluent-datamodel-server\launch_server\launch_datamodel_server.bat",
        "preferences",
    )

    assert preferences.Appearance.ColorTheme.get_state() == "Default"
    preferences.Appearance.ColorTheme.set_state("Dark")

    updated_preferences_dict = preferences.get_state()

    close_server()

    session = pyfluent.launch_fluent(mode="solver")

    assert session.preferences.Appearance.ColorTheme() == "Default"
    session.preferences.set_state(updated_preferences_dict)
    assert session.preferences.Appearance.ColorTheme() == "Dark"
    session.preferences.Appearance.ColorTheme.set_state("Default")
    session.exit()
