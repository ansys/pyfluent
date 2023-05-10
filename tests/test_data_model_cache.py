import pytest

from ansys.api.fluent.v0.variant_pb2 import Variant
from ansys.fluent.core.data_model_cache import DataModelCache
from ansys.fluent.core.services.datamodel_se import _convert_value_to_variant


class Fake:
    def __init__(self, path):
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
    DataModelCache.rules_str_to_cache.clear()
    DataModelCache.rules_str_to_cache.update(initial_cache)
    var = Variant()
    _convert_value_to_variant(state, var)
    DataModelCache.update_cache(rules, var, deleted_paths)
    assert DataModelCache.rules_str_to_cache == final_cache


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
    DataModelCache.set_config("r1", "internal_names_as_keys", True)
    DataModelCache.rules_str_to_cache.clear()
    DataModelCache.rules_str_to_cache.update(initial_cache)
    var = Variant()
    _convert_value_to_variant(state, var)
    DataModelCache.update_cache(rules, var, deleted_paths)
    assert DataModelCache.rules_str_to_cache == final_cache


@pytest.mark.dev
@pytest.mark.fluent_231
@pytest.mark.fluent_232
def test_get_cached_values_in_command_arguments(new_mesh_session):
    new_mesh_session.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")
    new_mesh_session.workflow.TaskObject["Import Geometry"].Arguments = dict(
        FileName="Bob"
    )
    new_mesh_session.workflow.TaskObject["Import Geometry"].Arguments = dict(
        FileName=None
    )
    assert (
        "FileName"
        in new_mesh_session.workflow.TaskObject["Import Geometry"].CommandArguments()
    )
    assert (
        new_mesh_session.workflow.TaskObject["Import Geometry"].CommandArguments()[
            "FileName"
        ]
        is None
    )
