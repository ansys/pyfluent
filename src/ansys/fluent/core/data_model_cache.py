"""Module to manage datamodel cache."""


from collections import defaultdict
from typing import Any, Dict, List, Union

from ansys.api.fluent.v0.variant_pb2 import Variant

StateType = Union[
    bool,
    int,
    float,
    str,
    List[bool],
    List[int],
    List[float],
    List[str],
    List["StateType"],
    Dict[str, "StateType"],
]


class DataModelCache:
    """Class to manage datamodel cache."""

    class Empty:
        """Class representing unassigned cached state."""

    @staticmethod
    def is_unassigned(state: Any) -> bool:
        """Check whether a cached state is unassigned.

        Parameters
        ----------
        state : Any
            state

        Returns
        -------
        bool
            whether a cached state is unassigned
        """
        return state is DataModelCache.Empty

    rules_str_to_cache = defaultdict(dict)
    rules_str_to_config = {}

    @staticmethod
    def get_config(rules: str, name: str) -> Any:
        """Get datamodel cache configuration value.

        Parameters
        ----------
        rules : str
            datamodel rules
        name : str
            configuration name

        Returns
        -------
        Any
            configuration value
        """
        return DataModelCache.rules_str_to_config.get(rules, {}).get(name, False)

    @staticmethod
    def set_config(rules: str, name: str, value: Any):
        """Set datamodel cache configuration value.

        Parameters
        ----------
        rules : str
            datamodel rules
        name : str
            configuration name
        value : Any
            configuration value
        """
        if rules not in DataModelCache.rules_str_to_config:
            DataModelCache.rules_str_to_config[rules] = {}
        DataModelCache.rules_str_to_config[rules][name] = value

    @staticmethod
    def _update_cache_from_variant_state(
        rules: str, source: Dict[str, StateType], key: str, state: Variant, updaterFn
    ):
        if state.HasField("bool_state"):
            updaterFn(source, key, state.bool_state)
        elif state.HasField("int64_state"):
            updaterFn(source, key, state.int64_state)
        elif state.HasField("double_state"):
            updaterFn(source, key, state.double_state)
        elif state.HasField("string_state"):
            updaterFn(source, key, state.string_state)
        elif state.HasField("bool_vector_state"):
            updaterFn(source, key, state.bool_vector_state.item)
        elif state.HasField("int64_vector_state"):
            updaterFn(source, key, state.int64_vector_state.item)
        elif state.HasField("double_vector_state"):
            updaterFn(source, key, state.double_vector_state.item)
        elif state.HasField("string_vector_state"):
            updaterFn(source, key, state.string_vector_state.item)
        elif state.HasField("variant_vector_state"):
            updaterFn(source, key, [])
            for item in state.variant_vector_state.item:
                DataModelCache._update_cache_from_variant_state(
                    rules, source, key, item, lambda d, k, v: d[k].append(v)
                )
        elif state.HasField("variant_map_state"):
            internal_names_as_keys = DataModelCache.get_config(
                rules, "internal_names_as_keys"
            )
            if ":" in key:
                type_, iname = key.split(":", maxsplit=1)
                for k1, v1 in source.items():
                    if (internal_names_as_keys and k1 == key) or (
                        (not internal_names_as_keys)
                        and isinstance(v1, dict)
                        and v1.get("__iname__") == iname
                    ):
                        key = k1
                        break
                else:  # new named object
                    if internal_names_as_keys:
                        source[key] = {}
                    else:
                        name = state.variant_map_state.item["_name_"].string_state
                        key = f"{type_}:{name}"
                        source[key] = {"__iname__": iname}
            else:
                if key not in source:
                    source[key] = {}
            source = source[key]
            for k, v in state.variant_map_state.item.items():
                DataModelCache._update_cache_from_variant_state(
                    rules, source, k, v, dict.__setitem__
                )

    @staticmethod
    def update_cache(rules: str, state: Variant, deleted_paths: List[str]):
        """Update datamodel cache from streamed state.

        Parameters
        ----------
        rules : str
            datamodel rules
        state : Variant
            streamed state
        deleted_paths : List[str]
            list of deleted paths
        """
        cache = DataModelCache.rules_str_to_cache[rules]
        internal_names_as_keys = DataModelCache.get_config(
            rules, "internal_names_as_keys"
        )
        for deleted_path in deleted_paths:
            comps = [x for x in deleted_path.split("/") if x]
            sub_cache = cache
            for i, comp in enumerate(comps):
                if ":" in comp:
                    _, iname = comp.split(":", maxsplit=1)
                    key_to_del = None
                    for k, v in sub_cache.items():
                        if (internal_names_as_keys and k == comp) or (
                            (not internal_names_as_keys)
                            and isinstance(v, dict)
                            and v.get("__iname__") == iname
                        ):
                            if i == len(comps) - 1:
                                key_to_del = k
                            else:
                                sub_cache = v
                            break
                    else:
                        break
                    if key_to_del:
                        del sub_cache[key_to_del]
                else:
                    if comp in sub_cache:
                        sub_cache = sub_cache[comp]
                    else:
                        break
        for k, v in state.variant_map_state.item.items():
            DataModelCache._update_cache_from_variant_state(
                rules, cache, k, v, dict.__setitem__
            )

    @staticmethod
    def _dm_path_comp(comp):
        return ":".join(comp if comp[1] else comp[0])

    @staticmethod
    def _dm_path_comp_list(obj):
        return [DataModelCache._dm_path_comp(comp) for comp in obj.path]

    @staticmethod
    def get_state(rules: str, obj: object) -> Any:
        """Retrieve state from datamodel cache

        Parameters
        ----------
        rules : str
            datamodel rules
        obj : object
            datamodel object

        Returns
        -------
        _type_
            _description_
        """
        cache = DataModelCache.rules_str_to_cache[rules]
        if not len(cache):
            return DataModelCache.Empty
        path_components = DataModelCache._dm_path_comp_list(obj)
        for path_component in path_components:
            cache = cache.get(path_component, None)
            if not cache:
                return DataModelCache.Empty
        return cache

    @staticmethod
    def _set_state_at_path(cache, path, value):
        if len(path) == 0:
            return
        path_component = path[0]
        if len(path) == 1:
            cache[path_component] = value
        else:
            next_cache = cache.get(path_component, None)
            if not next_cache:
                next_cache = cache[path_component] = dict()
            DataModelCache._set_state_at_path(next_cache, path[1:], value)

    @staticmethod
    def set_state(rules: str, obj: object, value: Any):
        """Set datamodel cache state

        Parameters
        ----------
        rules : str
            datamodel rules
        obj : object
            datamodel object
        value : Any
            state
        """
        DataModelCache._set_state_at_path(
            DataModelCache.rules_str_to_cache[rules],
            DataModelCache._dm_path_comp_list(obj),
            value,
        )
