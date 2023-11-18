"""Module to manage datamodel cache."""


import abc
from collections import abc, defaultdict
import copy
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
    def _find_in_internal_name_dict(
        d: dict[str, Any], key: str, default: Any
    ) -> tuple[str, Any]:
        if key in d:
            return key, d[key]
        if ":" in key:
            type_, name = key.split(":")
            return next(
                (
                    (k, v)
                    for k, v in d.items()
                    if type_ == k.split(":")[0] and name == v["_name_"]
                ),
                (None, default),
            )
        return key, default

    @staticmethod
    def _find_in_display_name_dict(
        d: dict[str, Any], key: str, default: Any
    ) -> tuple[str, Any]:
        if key in d:
            return key, d[key]
        if ":" in key:
            type_, name = key.split(":")
            return next(
                (
                    (k, v)
                    for k, v in d.items()
                    if type_ == k.split(":")[0] and name == v["__iname__"]
                ),
                (None, default),
            )
        else:
            return key, default

    @staticmethod
    def _transform_internal_name_dict_by_display_names(d_in: dict[str, Any]):
        d_out = {}
        for k_in, v_in in d_in.items():
            k_out = f'{k_in.split(":")[0]}:{v_in["_name_"]}' if ":" in k_in else k_in
            if isinstance(v_in, abc.Mapping):
                d_out[
                    k_out
                ] = DataModelCache._transform_internal_name_dict_by_display_names(v_in)
            else:
                d_out[k_out] = v_in
        return d_out

    @staticmethod
    def _transform_display_name_dict_by_internal_names(d_in: dict[str, Any]):
        d_out = {}
        for k_in, v_in in d_in.items():
            k_out = f'{k_in.split(":")[0]}:{v_in["__iname__"]}' if ":" in k_in else k_in
            if isinstance(v_in, abc.Mapping):
                d_out[
                    k_out
                ] = DataModelCache._transform_display_name_dict_by_internal_names(v_in)
            else:
                d_out[k_out] = v_in
        return d_out

    @staticmethod
    def _update_internal_name_dict(d: dict[str, Any], d1: dict[str, Any]):
        for k1, v1 in d1.items():
            k, v = DataModelCache._find_in_internal_name_dict(d, k1, None)
            if isinstance(v, abc.Mapping) and isinstance(v1, abc.Mapping):
                DataModelCache._update_internal_name_dict(v, v1)
            else:
                if isinstance(v1, abc.Mapping):
                    k = (
                        f'{k1.split(":")[0]}:{v1.get("__iname__", k1.split(":")[1])}'
                        if ":" in k1
                        else k1
                    )
                    d[
                        k
                    ] = DataModelCache._transform_display_name_dict_by_internal_names(
                        v1
                    )
                else:
                    d[k] = v1

    @staticmethod
    def _update_display_name_dict(d: dict[str, Any], d1: dict[str, Any]):
        for k1, v1 in d1.items():
            k, v = DataModelCache._find_in_display_name_dict(d, k1, None)
            if isinstance(v, abc.Mapping) and isinstance(v1, abc.Mapping):
                DataModelCache._update_display_name_dict(v, v1)
            else:
                if isinstance(v1, abc.Mapping):
                    k = (
                        f'{k1.split(":")[0]}:{v1.get("_name_", k1.split(":")[1])}'
                        if ":" in k1
                        else k1
                    )
                    d[
                        k
                    ] = DataModelCache._transform_internal_name_dict_by_display_names(
                        v1
                    )
                else:
                    d[k] = v1

    @staticmethod
    def get_state(rules: str, obj: object, internal_names_as_keys=None) -> Any:
        """Retrieve state from datamodel cache.

        Parameters
        ----------
        rules : str
            datamodel rules
        obj : object
            datamodel object
        internal_names_as_keys : bool
            if True, returned state will hold internal names as keys

        Returns
        -------
        state : Any
            cached state
        """
        internal_names_as_keys_in_config = DataModelCache.get_config(
            rules, "internal_names_as_keys"
        )
        if internal_names_as_keys == None:
            internal_names_as_keys = internal_names_as_keys_in_config
        cache = DataModelCache.rules_str_to_cache[rules]
        if not len(cache):
            return DataModelCache.Empty
        comps = DataModelCache._dm_path_comp_list(obj)
        for comp in comps:
            if internal_names_as_keys == internal_names_as_keys_in_config:
                cache = cache.get(comp, None)
            elif not internal_names_as_keys and internal_names_as_keys_in_config:
                _, cache = DataModelCache._find_in_internal_name_dict(cache, comp, None)
            else:
                _, cache = DataModelCache._find_in_display_name_dict(cache, comp, None)
            if cache is None:
                return DataModelCache.Empty

        if internal_names_as_keys == internal_names_as_keys_in_config:
            return copy.deepcopy(cache)
        elif not internal_names_as_keys and internal_names_as_keys_in_config:
            return DataModelCache._transform_internal_name_dict_by_display_names(cache)
        else:
            return DataModelCache._transform_display_name_dict_by_internal_names(cache)

    @staticmethod
    def set_state(rules: str, obj: object, value: Any):
        """Set datamodel cache state.

        Parameters
        ----------
        rules : str
            datamodel rules
        obj : object
            datamodel object
        value : Any
            state
        """
        internal_names_as_keys_in_config = DataModelCache.get_config(
            rules, "internal_names_as_keys"
        )
        cache = DataModelCache.rules_str_to_cache[rules]
        comps = DataModelCache._dm_path_comp_list(obj)
        for comp in comps:
            if internal_names_as_keys_in_config:
                (
                    key,
                    next_cache,
                ) = DataModelCache._find_in_internal_name_dict(cache, comp, None)
            else:
                (
                    key,
                    next_cache,
                ) = DataModelCache._find_in_display_name_dict(cache, comp, None)
            if isinstance(next_cache, abc.Mapping):
                cache = next_cache
            else:
                cache[key] = {}
                cache = cache[key]
        if isinstance(value, abc.Mapping):
            if internal_names_as_keys_in_config:
                DataModelCache._update_internal_name_dict(cache, value)
            else:
                DataModelCache._update_display_name_dict(cache, value)
        else:
            cache[key] = value
