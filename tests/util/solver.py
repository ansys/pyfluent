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
