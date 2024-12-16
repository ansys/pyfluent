"""Module to manage datamodel cache."""

from collections import abc, defaultdict
from contextlib import contextmanager
import copy
from enum import Enum
from threading import RLock
from typing import Any, Dict, List, Optional

from ansys.api.fluent.v0.variant_pb2 import Variant
from ansys.fluent.core.utils.fluent_version import FluentVersion

StateType = (
    bool
    | int
    | float
    | str
    | List[bool]
    | List[int]
    | List[float]
    | List[str]
    | List["StateType"]
    | Dict[str, "StateType"]
)


class NameKey(Enum):
    """Name key."""

    INTERNAL = "__iname__"
    DISPLAY = "_name_"

    def __invert__(self):
        lst = list(NameKey)
        return lst[~lst.index(self)]


class _CacheImpl:
    def __init__(self, name_key: NameKey):
        self.name_key = name_key

    @staticmethod
    def add_missing_name_keys(k: str, v: dict[str, Any]):
        """Add missing name keys in dict."""
        if ":" in k:
            name_in_key = k.split(":")[1]
            if NameKey.DISPLAY.value in v and v[NameKey.DISPLAY.value] != name_in_key:
                v[NameKey.INTERNAL.value] = name_in_key
            if NameKey.INTERNAL.value in v and v[NameKey.INTERNAL.value] != name_in_key:
                v[NameKey.DISPLAY.value] = name_in_key

    def find(self, d: dict[str, Any], key: str, default: Any) -> tuple[str, Any]:
        """Find in dict."""
        if key in d:
            return key, d[key]
        if ":" in key:
            type_, name = key.split(":")
            for k, v in d.items():
                if (
                    isinstance(v, abc.Mapping)
                    and ":" in k
                    and type_ == k.split(":")[0]
                    and name == v.get((~self.name_key).value, None)
                ):
                    return k, v
            return None, default
        return key, default

    def transform(self, d_in: dict[str, Any], add_missing_name_keys=False):
        """Transform dict."""
        d_out = {}
        for k_in, v_in in d_in.items():
            if isinstance(v_in, abc.Mapping):
                k_out = (
                    f'{k_in.split(":")[0]}:{v_in[(~self.name_key).value]}'
                    if ":" in k_in
                    else k_in
                )
                v_out = self.transform(v_in, add_missing_name_keys)
                if add_missing_name_keys:
                    _CacheImpl.add_missing_name_keys(k_in, v_out)
                d_out[k_out] = v_out
            else:
                d_out[k_in] = v_in
        return d_out

    def update(self, d: dict[str, Any], d1: dict[str, Any]):
        """Update dict."""
        for k1, v1 in d1.items():
            k, v = self.find(d, k1, None)
            if isinstance(v, abc.Mapping) and isinstance(v1, abc.Mapping):
                self.update(v, v1)
            else:
                if isinstance(v1, abc.Mapping):
                    k = (
                        f'{k1.split(":")[0]}:{v1.get(self.name_key.value, k1.split(":")[1])}'
                        if ":" in k1
                        else k1
                    )
                    v1 = _CacheImpl(~self.name_key).transform(v1, True)
                    _CacheImpl.add_missing_name_keys(k1, v1)
                d[k] = v1


def _is_dict_parameter_type(version: FluentVersion, rules: str, rules_path: str):
    """Check if a parameter is a dict type."""
    from ansys.fluent.core import CODEGEN_OUTDIR
    from ansys.fluent.core.services.datamodel_se import (
        PyDictionary,
        PyNamedObjectContainer,
        PyParameter,
    )
    from ansys.fluent.core.utils import load_module

    try:
        module = load_module(
            rules, CODEGEN_OUTDIR / f"datamodel_{version.number}" / f"{rules}.py"
        )
    except FileNotFoundError:  # no codegen or during codegen
        return False
    cls = module.Root
    comps = rules_path.split("/")
    for i, comp in enumerate(comps):
        if hasattr(cls, comp):
            cls = getattr(cls, comp)
            if issubclass(cls, PyParameter) and i < len(comps) - 1:
                return False
            if issubclass(cls, PyNamedObjectContainer):
                cls = getattr(cls, f"_{comp}")
    return issubclass(cls, PyDictionary)


class DataModelCache:
    """Class to manage datamodel cache."""

    use_display_name = False

    def __init__(self):
        """Initialize datamodel cache."""
        self.rules_str_to_cache = defaultdict(dict)
        self.rules_str_to_config = {}
        self._locks = {}

    @contextmanager
    def _with_lock(self, rules: str):
        if rules not in self._locks:
            self._locks[rules] = RLock()
        with self._locks[rules]:
            yield

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

    def get_config(self, rules: str, name: str) -> Any:
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
        return self.rules_str_to_config.get(rules, {}).get(name, False)

    def set_config(self, rules: str, name: str, value: Any):
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
        if rules not in self.rules_str_to_config:
            self.rules_str_to_config[rules] = {}
        self.rules_str_to_config[rules][name] = value

    def _update_cache_from_variant_state(
        self,
        rules: str,
        source: Dict[str, StateType],
        key: str,
        state: Variant,
        updater_fn,
        rules_str: str,
        version,
    ):
        # Helper function to update the source with the state value
        def update_source_with_state(state_field):
            if state.HasField(state_field):
                updater_fn(source, key, getattr(state, state_field))
                return True
            return False

        # Check for basic state types
        for state_type in [
            "bool_state",
            "int64_state",
            "double_state",
            "string_state",
            "bool_vector_state",
            "int64_vector_state",
            "double_vector_state",
            "string_vector_state",
        ]:
            if update_source_with_state(state_type):
                return

        # Handle variant vector state
        if state.HasField("variant_vector_state"):
            updater_fn(source, key, [])
            for item in state.variant_vector_state.item:
                self._update_cache_from_variant_state(
                    rules,
                    source,
                    key,
                    item,
                    lambda d, k, v: d[k].append(v),
                    rules_str + "/" + key.split(":", maxsplit=1)[0],
                    version,
                )
            return

        # Handle variant map state
        if state.HasField("variant_map_state"):
            internal_names_as_keys = (
                self.get_config(rules, "name_key") == NameKey.INTERNAL
            )

            # Determine the appropriate key
            if ":" in key:
                type_, iname = key.split(":", maxsplit=1)
                key = self._determine_key(
                    source, internal_names_as_keys, key, state, type_, iname
                )
            else:
                if key not in source:
                    source[key] = {}

            if version and _is_dict_parameter_type(version, rules, rules_str):
                source[key] = {}

            # Update the source with items from the variant map state
            if state.variant_map_state.item:
                source = source[key]
                for k, v in state.variant_map_state.item.items():
                    self._update_cache_from_variant_state(
                        rules,
                        source,
                        k,
                        v,
                        dict.__setitem__,
                        rules_str + "/" + k.split(":", maxsplit=1)[0],
                        version,
                    )
            else:
                source[key] = {}

        # Default case when no fields are matched
        else:
            updater_fn(source, key, None)

    def _determine_key(
        self,
        source: Dict[str, StateType],
        internal_names_as_keys: bool,
        key: str,
        state: Variant,
        type_: str,
        iname: str,
    ) -> str:
        """Determine the appropriate key based on internal naming conventions."""
        for k1, v1 in source.items():
            if (internal_names_as_keys and k1 == key) or (
                (not internal_names_as_keys)
                and isinstance(v1, dict)
                and v1.get(NameKey.INTERNAL.value) == iname
            ):
                return k1  # Found a matching key

        # If no match found and internal naming is used
        if internal_names_as_keys:
            source[key] = {}
            return key

        # If no match found and external naming is used
        name = state.variant_map_state.item[NameKey.DISPLAY.value].string_state
        new_key = f"{type_}:{name}"
        source[new_key] = {NameKey.INTERNAL.value: iname}

        return new_key

    def update_cache(
        self, rules: str, state: Variant, deleted_paths: List[str], version=None
    ):
        """Update datamodel cache from streamed state.

        Parameters
        ----------
        rules : str
            datamodel rules
        state : Variant
            streamed state
        deleted_paths : List[str]
            list of deleted paths
        version : FluentVersion, optional
            Fluent version
        """
        cache = self.rules_str_to_cache[rules]

        with self._with_lock(rules):
            internal_names_as_keys = (
                self.get_config(rules, "name_key") == NameKey.INTERNAL
            )

            # Process deleted paths
            self._process_deleted_paths(cache, deleted_paths, internal_names_as_keys)

            # Update cache with new state items
            for k, v in state.variant_map_state.item.items():
                self._update_cache_from_variant_state(
                    rules,
                    cache,
                    k,
                    v,
                    dict.__setitem__,
                    k.split(":", maxsplit=1)[0],
                    version,
                )

    def _process_deleted_paths(
        self,
        cache: Dict[str, Any],
        deleted_paths: List[str],
        internal_names_as_keys: bool,
    ):
        """Process and delete paths from the cache based on the deleted paths list."""
        for deleted_path in deleted_paths:
            comps = [x for x in deleted_path.split("/") if x]
            self._delete_from_cache(cache, comps, internal_names_as_keys)

    def _delete_from_cache(
        self, sub_cache: Dict[str, Any], comps: List[str], internal_names_as_keys: bool
    ):
        """Recursively delete components from the cache."""
        for i, comp in enumerate(comps):
            if ":" in comp:
                _, iname = comp.split(":", maxsplit=1)
                key_to_del = self._find_key_to_delete(
                    sub_cache, comp, iname, i == len(comps) - 1, internal_names_as_keys
                )
                if key_to_del:
                    del sub_cache[key_to_del]
                    return  # Exit after deletion
            else:
                if comp in sub_cache:
                    sub_cache = sub_cache[comp]
                else:
                    break

    def _find_key_to_delete(
        self,
        sub_cache: Dict[str, Any],
        comp: str,
        iname: str,
        is_last_component: bool,
        internal_names_as_keys: bool,
    ) -> Optional[str]:
        """Find the key to delete from the sub-cache."""
        for k, v in sub_cache.items():
            if (internal_names_as_keys and k == comp) or (
                (not internal_names_as_keys)
                and isinstance(v, dict)
                and v.get(NameKey.INTERNAL.value) == iname
            ):
                return (
                    k if is_last_component else None
                )  # Return key if it's the last component
        return None  # No key found to delete

    @staticmethod
    def _dm_path_comp(comp):
        return ":".join(comp) if comp[1] else comp[0]

    @staticmethod
    def _dm_path_comp_list(obj):
        return [DataModelCache._dm_path_comp(comp) for comp in obj.path]

    def get_state(
        self, rules: str, obj: object, name_key: NameKey | None = None
    ) -> Any:
        """Retrieve state from datamodel cache.

        Parameters
        ----------
        rules : str
            datamodel rules
        obj : object
            datamodel object, optional
        name_key : NameKey, optional
            if NameKey.INTERNAL, the returned state will contain internal names in keys.
            if NameKey.DISPLAY, the returned state will contain display names in keys.
            Default value is picked from configuration.

        Returns
        -------
        Any
            cached state
        """
        name_key_in_config = self.get_config(rules, "name_key")
        if name_key is None:
            name_key = name_key_in_config
        cache = self.rules_str_to_cache[rules]
        with self._with_lock(rules):
            if not len(cache):
                return DataModelCache.Empty
            comps = DataModelCache._dm_path_comp_list(obj)
            for comp in comps:
                if name_key == name_key_in_config:
                    cache = cache.get(comp, None)
                else:
                    _, cache = _CacheImpl(name_key_in_config).find(cache, comp, None)
                if cache is None:
                    return DataModelCache.Empty

            if not isinstance(cache, abc.Mapping) or name_key == name_key_in_config:
                return copy.deepcopy(cache)
            else:
                if not cache:
                    return DataModelCache.Empty
                return _CacheImpl(name_key_in_config).transform(cache)

    def set_state(self, rules: str, obj: object, value: Any):
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
        name_key_in_config = self.get_config(rules, "name_key")
        cache = self.rules_str_to_cache[rules]
        with self._with_lock(rules):
            comps = DataModelCache._dm_path_comp_list(obj)
            for i, comp in enumerate(comps):
                key, next_cache = _CacheImpl(name_key_in_config).find(cache, comp, None)
                if i == len(comps) - 1 and not isinstance(value, abc.Mapping):
                    cache[key] = value
                    return
                if isinstance(next_cache, abc.Mapping):
                    cache = next_cache
                else:
                    cache[key] = {}
                    cache = cache[key]
            _CacheImpl(name_key_in_config).update(cache, value)
