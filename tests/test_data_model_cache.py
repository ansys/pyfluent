import pytest
from util.meshing_workflow import (  # noqa: F401
    new_mesh_session,
    new_watertight_workflow_session,
)

from ansys.api.fluent.v0.variant_pb2 import Variant
from ansys.fluent.core.data_model_cache import DataModelCache, NameKey
from ansys.fluent.core.services.datamodel_se import _convert_value_to_variant


class Fake:
    def __init__(self, path):
        if isinstance(path, str):
            self.path = [
                comp.split(":") if ":" in comp else [comp, ""]
                for comp in path.split("/")
            ]
        else:
            self.path = path


def test_data_model_cache():
    DataModelCache.set_state("x", Fake([("A", ""), ("x", "")]), 42.0)
    assert 42.0 == DataModelCache.get_state("x", Fake([("A", ""), ("x", "")]))
    assert dict(x=42.0) == DataModelCache.get_state("x", Fake([("A", "")]))
    assert DataModelCache.Empty == DataModelCache.get_state("x", Fake([("B", "")]))
    assert DataModelCache.Empty == DataModelCache.get_state("y", Fake([]))


@pytest.mark.parametrize(
    "initial_cache,rules,state,deleted_paths,final_cache",
    [
        (
            {"r1": {"A": {"B": "ab", "C": {}, "D:D-1": {"__iname__": "D1"}}}},
            "r1",
            None,
            ["X/D:D1", "A/D:Y1", "A/D:D1"],
            {"r1": {"A": {"B": "ab", "C": {}}}},
        ),
        ({"r1": {}}, "r1", {"A": True}, [], {"r1": {"A": True}}),
        ({"r1": {}}, "r1", {"A": 5}, [], {"r1": {"A": 5}}),
        ({"r1": {}}, "r1", {"A": 3.0}, [], {"r1": {"A": 3.0}}),
        ({"r1": {}}, "r1", {"A": "ab"}, [], {"r1": {"A": "ab"}}),
        ({"r1": {}}, "r1", {"A": [False, True]}, [], {"r1": {"A": [False, True]}}),
        ({"r1": {}}, "r1", {"A": [5, 10]}, [], {"r1": {"A": [5, 10]}}),
        ({"r1": {}}, "r1", {"A": [3.0, 6.0]}, [], {"r1": {"A": [3.0, 6.0]}}),
        ({"r1": {}}, "r1", {"A": ["ab", "cd"]}, [], {"r1": {"A": ["ab", "cd"]}}),
        ({"r1": {"A": {}}}, "r1", {"A": {"B": 5}}, [], {"r1": {"A": {"B": 5}}}),
        ({"r1": {"A": 5}}, "r1", {"A": {}}, [], {"r1": {"A": None}}),
        (
            {"r1": {"A": {}}},
            "r1",
            {"A": {"B": {"C": 5}}},
            [],
            {"r1": {"A": {"B": {"C": 5}}}},
        ),
        (
            {"r1": {"A": {}}},
            "r1",
            {"A": {"B:B1": {"_name_": "B-1", "C": 5.0}}},
            [],
            {"r1": {"A": {"B:B-1": {"__iname__": "B1", "_name_": "B-1", "C": 5.0}}}},
        ),
        (
            {"r1": {"A": {"B:B-1": {"__iname__": "B1", "_name_": "B-1", "C": 5.0}}}},
            "r1",
            {"A": {"B:B1": {"C": 7.0}}},
            [],
            {"r1": {"A": {"B:B-1": {"__iname__": "B1", "_name_": "B-1", "C": 7.0}}}},
        ),
        (
            {"r1": {}},
            "r1",
            {"B:B1": {"_name_": "B-1", "C": 5.0}},
            [],
            {"r1": {"B:B-1": {"__iname__": "B1", "_name_": "B-1", "C": 5.0}}},
        ),
        (
            {"r1": {"B:B-1": {"__iname__": "B1", "_name_": "B-1", "C": 5.0}}},
            "r1",
            {"B:B1": {"C": 7.0}},
            [],
            {"r1": {"B:B-1": {"__iname__": "B1", "_name_": "B-1", "C": 7.0}}},
        ),
        (
            {"r1": {}},
            "r1",
            {"A:A1": {"_name_": "A-1", "B:B1": {"_name_": "B-1", "D": 7.0}, "C": 5.0}},
            [],
            {
                "r1": {
                    "A:A-1": {
                        "__iname__": "A1",
                        "_name_": "A-1",
                        "B:B-1": {"__iname__": "B1", "_name_": "B-1", "D": 7.0},
                        "C": 5.0,
                    }
                }
            },
        ),
        (
            {"r1": {"B:B-1": {"__iname__": "B1", "_name_": "B-1", "C": 5.0}}},
            "r1",
            {"B:B1": {"_name_": "B-2", "C": 5.0}},
            ["B:B1"],
            {"r1": {"B:B-2": {"__iname__": "B1", "_name_": "B-2", "C": 5.0}}},
        ),
    ],
)
def test_update_cache_display_names_as_keys(
    initial_cache, rules, state, deleted_paths, final_cache
):
    cache_rules = DataModelCache.rules_str_to_cache
    cache_rules.clear()
    cache_rules.update(initial_cache)
    var = Variant()
    _convert_value_to_variant(state, var)
    DataModelCache.update_cache(rules, var, deleted_paths)
    assert cache_rules == final_cache


@pytest.mark.parametrize(
    "initial_cache,rules,state,deleted_paths,final_cache",
    [
        (
            {"r1": {"A": {"B": "ab", "C": {}, "D:D1": {}}}},
            "r1",
            None,
            ["X/D:D1", "A/D:Y1", "A/D:D1"],
            {"r1": {"A": {"B": "ab", "C": {}}}},
        ),
        ({"r1": {}}, "r1", {"A": True}, [], {"r1": {"A": True}}),
        ({"r1": {}}, "r1", {"A": 5}, [], {"r1": {"A": 5}}),
        ({"r1": {}}, "r1", {"A": 3.0}, [], {"r1": {"A": 3.0}}),
        ({"r1": {}}, "r1", {"A": "ab"}, [], {"r1": {"A": "ab"}}),
        ({"r1": {}}, "r1", {"A": [False, True]}, [], {"r1": {"A": [False, True]}}),
        ({"r1": {}}, "r1", {"A": [5, 10]}, [], {"r1": {"A": [5, 10]}}),
        ({"r1": {}}, "r1", {"A": [3.0, 6.0]}, [], {"r1": {"A": [3.0, 6.0]}}),
        ({"r1": {}}, "r1", {"A": ["ab", "cd"]}, [], {"r1": {"A": ["ab", "cd"]}}),
        ({"r1": {"A": {}}}, "r1", {"A": {"B": 5}}, [], {"r1": {"A": {"B": 5}}}),
        (
            {"r1": {"A": {}}},
            "r1",
            {"A": {"B": {"C": 5}}},
            [],
            {"r1": {"A": {"B": {"C": 5}}}},
        ),
        (
            {"r1": {"A": {}}},
            "r1",
            {"A": {"B:B1": {"_name_": "B-1", "C": 5.0}}},
            [],
            {"r1": {"A": {"B:B1": {"_name_": "B-1", "C": 5.0}}}},
        ),
        (
            {"r1": {"A": {"B:B1": {"_name_": "B-1", "C": 5.0}}}},
            "r1",
            {"A": {"B:B1": {"C": 7.0}}},
            [],
            {"r1": {"A": {"B:B1": {"_name_": "B-1", "C": 7.0}}}},
        ),
        (
            {"r1": {}},
            "r1",
            {"B:B1": {"_name_": "B-1", "C": 5.0}},
            [],
            {"r1": {"B:B1": {"_name_": "B-1", "C": 5.0}}},
        ),
        (
            {"r1": {"B:B1": {"_name_": "B-1", "C": 5.0}}},
            "r1",
            {"B:B1": {"C": 7.0}},
            [],
            {"r1": {"B:B1": {"_name_": "B-1", "C": 7.0}}},
        ),
        (
            {"r1": {}},
            "r1",
            {"A:A1": {"_name_": "A-1", "B:B1": {"_name_": "B-1", "D": 7.0}, "C": 5.0}},
            [],
            {
                "r1": {
                    "A:A1": {
                        "_name_": "A-1",
                        "B:B1": {"_name_": "B-1", "D": 7.0},
                        "C": 5.0,
                    }
                }
            },
        ),
        (
            {"r1": {"B:B1": {"_name_": "B-1", "C": 5.0}}},
            "r1",
            {"B:B1": {"_name_": "B-2", "C": 5.0}},
            ["B:B1"],
            {"r1": {"B:B1": {"_name_": "B-2", "C": 5.0}}},
        ),
    ],
)
def test_update_cache_internal_names_as_keys(
    initial_cache, rules, state, deleted_paths, final_cache
):
    DataModelCache.set_config("r1", "name_key", NameKey.INTERNAL)
    cache_rules = DataModelCache.rules_str_to_cache
    cache_rules.clear()
    cache_rules.update(initial_cache)
    var = Variant()
    _convert_value_to_variant(state, var)
    DataModelCache.update_cache(rules, var, deleted_paths)
    assert cache_rules == final_cache


@pytest.mark.fluent_version(">=23.1")
@pytest.mark.codegen_required
def test_get_cached_values_in_command_arguments(new_mesh_session):
    new_mesh_session.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")
    geo_import = new_mesh_session.workflow.TaskObject["Import Geometry"]
    geo_import.Arguments = dict(FileName="Bob")
    geo_import.Arguments = dict(FileName=None)
    assert "FileName" in geo_import.command_arguments()
    assert geo_import.command_arguments()["FileName"] is None


@pytest.fixture
def display_names_as_keys_in_cache():
    rules_list = ["workflow", "meshing", "PartManagement", "PMFileManagement"]
    for rules in rules_list:
        DataModelCache.set_config(rules, "name_key", NameKey.DISPLAY)
    yield
    for rules in rules_list:
        DataModelCache.set_config(rules, "name_key", NameKey.INTERNAL)


def test_display_names_as_keys(
    display_names_as_keys_in_cache, new_watertight_workflow_session
):
    assert "TaskObject:Import Geometry" in DataModelCache.rules_str_to_cache["workflow"]
    assert "TaskObject:TaskObject1" not in DataModelCache.rules_str_to_cache["workflow"]


def test_internal_names_as_keys(new_watertight_workflow_session):
    assert (
        "TaskObject:Import Geometry"
        not in DataModelCache.rules_str_to_cache["workflow"]
    )
    assert "TaskObject:TaskObject1" in DataModelCache.rules_str_to_cache["workflow"]


@pytest.mark.parametrize(
    "cache,name_key_in_config,path,name_key,state",
    [
        ({"A": {"B": {"C": 2}}}, NameKey.INTERNAL, "A/B", NameKey.INTERNAL, {"C": 2}),
        (
            {"A": {"B:B1": {"C:C1": {"_name_": "C-1"}, "_name_": "B-1"}}},
            NameKey.INTERNAL,
            "A/B:B-1",
            NameKey.DISPLAY,
            {"C:C-1": {"_name_": "C-1"}, "_name_": "B-1"},
        ),
        (
            {"A": {"B:B1": {"C:C1": {"_name_": "C-1"}, "_name_": "B-1"}}},
            NameKey.INTERNAL,
            "A/B:B1",
            NameKey.DISPLAY,
            {"C:C-1": {"_name_": "C-1"}, "_name_": "B-1"},
        ),
        (
            {"A": {"B:B-1": {"C:C-1": {"__iname__": "C1"}, "__iname__": "B1"}}},
            NameKey.DISPLAY,
            "A/B:B1",
            NameKey.INTERNAL,
            {"C:C1": {"__iname__": "C1"}, "__iname__": "B1"},
        ),
        (
            {"A": {"B:B1": {"C": 2, "_name_": "B-1"}}},
            NameKey.INTERNAL,
            "A/B:B-2",
            NameKey.DISPLAY,
            DataModelCache.Empty,
        ),
    ],
)
def test_cache_get_state(cache, name_key_in_config, path, name_key, state):
    rules = "x"
    DataModelCache.set_config(rules, "name_key", name_key_in_config)
    cache_rules = DataModelCache.rules_str_to_cache
    cache_rules.clear()
    cache_rules[rules] = cache
    assert state == DataModelCache.get_state(rules, Fake(path), name_key)


@pytest.mark.parametrize(
    "initial_cache,name_key_in_config,path,value,final_cache",
    [
        ({"A": 2}, NameKey.INTERNAL, "A/B", 2, {"A": {"B": 2}}),
        (
            {"A": 2},
            NameKey.INTERNAL,
            "A/B",
            {"C": {"D": 2}},
            {"A": {"B": {"C": {"D": 2}}}},
        ),
        (
            {"A": {"B": 2}},
            NameKey.INTERNAL,
            "A/B",
            {"C": {"D": 2}},
            {"A": {"B": {"C": {"D": 2}}}},
        ),
        (
            {"A": {"B": {"C": 2}}},
            NameKey.INTERNAL,
            "A/B",
            {"C": {"D": 2}},
            {"A": {"B": {"C": {"D": 2}}}},
        ),
        (
            {"A": {"B": {"C": {"D": 1}}}},
            NameKey.INTERNAL,
            "A/B",
            {"C": {"D": 2}},
            {"A": {"B": {"C": {"D": 2}}}},
        ),
        (
            {"A": {"B:B1": {"C:C1": {"_name_": "C-1"}, "_name_": "B-1"}}},
            NameKey.INTERNAL,
            "A/B:B-1",
            {"C:C-1": {"D": 2}},
            {"A": {"B:B1": {"C:C1": {"_name_": "C-1", "D": 2}, "_name_": "B-1"}}},
        ),
        (
            {"A": {"B:B1": {"C:C1": {"_name_": "C-1"}, "_name_": "B-1"}}},
            NameKey.INTERNAL,
            "A/B:B-1",
            {"C:C-1": {"D:D-1": {"__iname__": "D1"}}},
            {
                "A": {
                    "B:B1": {
                        "C:C1": {
                            "_name_": "C-1",
                            "D:D1": {"__iname__": "D1", "_name_": "D-1"},
                        },
                        "_name_": "B-1",
                    }
                }
            },
        ),
        (
            {"A": {"B:B1": {"C:C1": {"_name_": "C-1"}, "_name_": "B-1"}}},
            NameKey.INTERNAL,
            "A/B:B1",
            {"C:C1": {"D:D1": {"_name_": "D-1"}}},
            {
                "A": {
                    "B:B1": {
                        "C:C1": {
                            "_name_": "C-1",
                            "D:D1": {"_name_": "D-1", "__iname__": "D1"},
                        },
                        "_name_": "B-1",
                    }
                }
            },
        ),
        (
            {"A": {"B:B-1": {"C:C-1": {"__iname__": "C1"}, "__iname__": "B1"}}},
            NameKey.DISPLAY,
            "A/B:B1",
            {"C:C1": {"D": 2}},
            {"A": {"B:B-1": {"C:C-1": {"__iname__": "C1", "D": 2}, "__iname__": "B1"}}},
        ),
        (
            {"A": {"B:B-1": {"C:C-1": {"__iname__": "C1"}, "__iname__": "B1"}}},
            NameKey.DISPLAY,
            "A/B:B1",
            {"C:C1": {"D:D1": {"_name_": "D-1"}}},
            {
                "A": {
                    "B:B-1": {
                        "C:C-1": {
                            "__iname__": "C1",
                            "D:D-1": {"_name_": "D-1", "__iname__": "D1"},
                        },
                        "__iname__": "B1",
                    }
                }
            },
        ),
        (
            {"A": {"B:B-1": {"C:C-1": {"__iname__": "C1"}, "__iname__": "B1"}}},
            NameKey.DISPLAY,
            "A/B:B-1",
            {"C:C-1": {"D:D-1": {"__iname__": "D1"}}},
            {
                "A": {
                    "B:B-1": {
                        "C:C-1": {
                            "__iname__": "C1",
                            "D:D-1": {"__iname__": "D1", "_name_": "D-1"},
                        },
                        "__iname__": "B1",
                    }
                }
            },
        ),
    ],
)
def test_cache_set_state(
    initial_cache,
    name_key_in_config,
    path,
    value,
    final_cache,
):
    rules = "x"
    DataModelCache.set_config(rules, "name_key", name_key_in_config)
    cache_rules = DataModelCache.rules_str_to_cache
    cache_rules.clear()
    cache_rules[rules] = initial_cache
    DataModelCache.set_state(rules, Fake(path), value)
    assert final_cache == cache_rules[rules]
