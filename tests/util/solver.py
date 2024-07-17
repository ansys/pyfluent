from ansys.fluent.core.utils.fluent_version import FluentVersion


def check_report_definition_result(
    report_definitions, report_definition_name, expected_result
):
    assert (
        report_definitions.compute(report_defs=[report_definition_name])[
            report_definition_name
        ][0]
        == expected_result
    )


def assign_settings_value_from_value_dict(setting, value):
    try:
        setting.set_state({"option": "value", "value": value})
    except RuntimeError:
        setting.set_state({"option": "constant or expression", "constant": value})


class ApiNames:
    def __init__(self, session):
        self.session = session

    @property
    def initial_gauge_pressure(self):
        if self.session.get_fluent_version() == FluentVersion.v222:
            return "p_sup"
        else:
            return "initial_gauge_pressure"


def settings_value_from_value_dict(dict_value) -> bool:
    if "option" in dict_value:
        option = dict_value["option"]
        key = None
        if option == "value":
            key = "value"
        elif option == "constant or expression":
            key = "constant"
        if key:
            return dict_value[key]


def assert_settings_values_equal(left, right):
    assert settings_value_from_value_dict(left) == right


class SettingsValDict:
    def __init__(self, val):
        self._val = val

    def __eq__(self, other):
        return settings_value_from_value_dict(other) == self._val


def copy_database_material(materials, type, name):
    try:
        materials.database.copy_by_name(type=type, name=name)
    except AttributeError:
        materials.copy_database_material_by_name(type=type, name=name)


def get_name_info(allnamesdict, namescheck):
    name_selected = {}
    for names, details in allnamesdict.items():
        if isinstance(details, dict):
            for name in namescheck:
                if name in details.values() or name in details or name in names:
                    name_selected[name] = details
    return name_selected
