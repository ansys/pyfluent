"""Provides a module to search a word through the Fluent's object hierarchy.."""

from collections.abc import Mapping
import fnmatch
import functools
import json
import os
from pathlib import Path
import pickle
import re
import sys
from typing import Any
import warnings

from ansys.fluent.core.solver import flobject
from ansys.fluent.core.solver.error_message import closest_allowed_names
from ansys.fluent.core.utils.fluent_version import (
    FluentVersion,
    get_version_for_file_name,
)
from ansys.fluent.core.workflow import (
    BaseTask,
    ClassicWorkflow,
    TaskContainer,
    Workflow,
)


def _get_api_tree_data_file():
    """Get API tree data file."""
    from ansys.fluent.core import CODEGEN_OUTDIR

    return (CODEGEN_OUTDIR / "api_tree" / "api_objects.json").resolve()


def get_api_tree_file_name(version: str) -> Path:
    """Get API tree file name."""
    from ansys.fluent.core import CODEGEN_OUTDIR

    return (CODEGEN_OUTDIR / f"api_tree_{version}.pickle").resolve()


def _match(source: str, word: str, match_whole_word: bool, match_case: bool):
    if not match_case:
        source = source.lower()
        word = word.lower()
    if match_whole_word:
        return source == word
    else:
        return word in source


def _remove_suffix(input: str, suffix):
    if hasattr(input, "removesuffix"):
        return input.removesuffix(suffix)
    else:
        if suffix and input.endswith(suffix):
            return input[: -len(suffix)]
        return input


_meshing_rules = ["workflow", "meshing", "PartManagement", "PMFileManagement"]


def _get_version_path_prefix_from_obj(obj: Any):
    from ansys.fluent.core.services.datamodel_se import PyMenu, PyNamedObjectContainer
    from ansys.fluent.core.services.datamodel_tui import TUIMenu
    from ansys.fluent.core.session_pure_meshing import PureMeshing
    from ansys.fluent.core.session_solver import Solver

    path = None
    version = None
    prefix = None
    if isinstance(obj, PureMeshing):
        path = ["<meshing_session>"]
        version = get_version_for_file_name(obj.get_fluent_version().value)
        prefix = "<search_root>"
    elif isinstance(obj, Solver):
        path = ["<solver_session>"]
        version = get_version_for_file_name(obj.get_fluent_version().value)
        prefix = "<search_root>"
    elif isinstance(obj, TUIMenu):
        module = obj.__class__.__module__
        path = [
            (
                "<meshing_session>"
                if module.startswith("meshing")
                else "<solver_session>"
            ),
            "tui",
        ]
        path.extend(obj._path)
        version = module.rsplit("_", 1)[-1]
        prefix = "<search_root>"
    elif isinstance(obj, (ClassicWorkflow, Workflow)):
        path = ["<meshing_session>", obj.rules]
        module = obj._workflow.__class__.__module__
        version = module.rsplit("_", 1)[-1]
        prefix = "<search_root>"
    elif isinstance(obj, BaseTask):
        path = ["<meshing_session>", obj.rules]
        path.extend([f"{k[0]}:<name>" if k[1] else k[0] for k in obj.path])
        module = obj._workflow.__class__.__module__
        version = module.rsplit("_", 1)[-1]
        prefix = "<search_root>"
    elif isinstance(obj, TaskContainer):
        path = ["<meshing_session>", obj.rules]
        path.extend([f"{k[0]}:<name>" if k[1] else k[0] for k in obj.path])
        path[-1] = f"{path[-1]}:<name>"
        module = obj._container._workflow.__class__.__module__
        version = module.rsplit("_", 1)[-1]
        prefix = '<search_root>["<name>"]'
    elif isinstance(obj, PyMenu):
        rules = obj.rules
        path = ["<meshing_session>" if rules in _meshing_rules else "<solver_session>"]
        path.append(rules)
        path.extend([f"{k[0]}:<name>" if k[1] else k[0] for k in obj.path])
        module = obj.__class__.__module__
        version = module.rsplit("_", 1)[-1]
        prefix = "<search_root>"
    elif isinstance(obj, PyNamedObjectContainer):
        rules = obj.rules
        path = ["<meshing_session>" if rules in _meshing_rules else "<solver_session>"]
        path.append(rules)
        path.extend([f"{k[0]}:<name>" if k[1] else k[0] for k in obj.path])
        path[-1] = f"{path[-1]}:<name>"
        module = obj.__class__.__module__
        version = module.rsplit("_", 1)[-1]
        prefix = '<search_root>["<name>"]'
    elif isinstance(obj, flobject.Group):
        module = obj.__class__.__module__
        try:
            version = module.split(".")[-2].rsplit("_", 1)[-1]
        except IndexError:
            version = None
        prefix = "<search_root>"
        path = ["<solver_session>"]
        # Cannot deduce the whole path without api_tree
    elif isinstance(obj, flobject.NamedObject):
        module = obj.__class__.__module__
        try:
            version = module.split(".")[-2].rsplit("_", 1)[-1]
        except IndexError:
            version = None
        prefix = '<search_root>["<name>"]'
        path = ["<solver_session>"]
        # Cannot deduce the whole path without api_tree
    return version, path, prefix


def _search(
    word: str,
    match_whole_word: bool = False,
    match_case: bool = False,
    version: str | None = None,
    search_root: Any | None = None,
    write_api_tree_data: bool | None = False,
):
    """Search for a word through the Fluent's object hierarchy.

    Parameters
    ----------
    word : str
        Word to search for.
    match_whole_word : bool, optional
        Whether to match whole word, by default False
    match_case : bool, optional
        Whether to match case, by default False
    version : str, optional
        Fluent version to search in. The default is ``None``. If ``None``,
        it searches in the latest version for which codegen was run.
    search_root : Any, optional
        The root object within which the search is performed.
        It can be a session object or any API object within a session.
        The default is ``None``. If ``None``, it searches everything.
    write_api_tree_data: bool, optional
        Whether to write the API tree data.

    Examples
    --------
    >>> import ansys.fluent.core as pyfluent
    >>> pyfluent.search("geometry")
    <meshing_session>.tui.file.import_.cad_geometry (Command)
    <meshing_session>.tui.display.update_scene.select_geometry (Command)
    <meshing_session>.meshing.ImportGeometry (Command)
    <meshing_session>.meshing.LoadCADGeometry (Command)
    <solver_session>.tui.solve.initialize.compute_defaults.geometry (Command)
    <solver_session>.tui.report.reference_values.compute.geometry (Command)
    <solver_session>.tui.define.geometry (Command)
    <solver_session>.tui.mesh.geometry (Object)
    <solver_session>.setup.boundary_conditions.geometry["<name>"] (Object)
    <solver_session>.setup.geometry (Object)
    <solver_session>.solution.report_definitions.surface["<name>"].geometry (Parameter)
    <solver_session>.solution.report_definitions.volume["<name>"].geometry (Parameter)
    <solver_session>.results.graphics.mesh["<name>"].geometry (Parameter)
    <solver_session>.results.graphics.contour["<name>"].geometry (Parameter)
    """
    api_objects = []
    api_tui_objects = []
    api_object_names = []
    results = []
    if version:
        version = get_version_for_file_name(version)
    root_version, root_path, prefix = _get_version_path_prefix_from_obj(search_root)
    if search_root and not prefix:
        return
    if not version:
        for fluent_version in FluentVersion:
            version = get_version_for_file_name(fluent_version.value)
            if get_api_tree_file_name(version).exists():
                break
    api_tree_file = get_api_tree_file_name(version)
    with open(api_tree_file, "rb") as f:
        api_tree = pickle.load(f)

    if isinstance(search_root, (flobject.Group, flobject.NamedObject)):
        path = root_path + [
            flobject.to_python_name(x) for x in search_root.path.split("/")
        ]
        root_path = []
        tree = api_tree
        while path:
            p = path.pop(0)
            if p in tree:
                tree = tree[p]
                root_path.append(p)
            elif f"{p}:<name>" in tree:
                tree = tree[f"{p}:<name>"]
                root_path.append(f"{p}:<name>")
                if path:
                    path.pop(0)
            else:
                return

    def inner(tree, path, root_path):
        if root_path:
            path = prefix
        while root_path:
            p = root_path.pop(0)
            if p in tree:
                tree = tree[p]
            else:
                return

        for k, v in tree.items():
            if k in ("<meshing_session>", "<solver_session>"):
                next_path = k
            else:
                if k.endswith(":<name>"):
                    k = _remove_suffix(k, ":<name>")
                    next_path = f'{path}.{k}["<name>"]'
                else:
                    next_path = f"{path}.{k}"
                type_ = "Object" if isinstance(v, Mapping) else v
                api_object_names.append(k)
                if "tui" in next_path:
                    api_tui_objects.append(f"{next_path} ({type_})")
                else:
                    api_objects.append(f"{next_path} ({type_})")
                if _match(k, word, match_whole_word, match_case):
                    results.append(f"{next_path} ({type_})")
            if isinstance(v, Mapping):
                inner(v, next_path, root_path)

    inner(api_tree, "", root_path)

    api_tree_data = dict()
    api_tree_data["api_objects"] = sorted(api_objects)
    api_tree_data["api_tui_objects"] = sorted(api_tui_objects)

    def _write_api_tree_file(api_tree_data: dict, api_object_names: list):
        from nltk.corpus import wordnet as wn

        _download_nltk_data()
        from ansys.fluent.core import CODEGEN_OUTDIR

        json_file_folder = Path(os.path.join(CODEGEN_OUTDIR, "api_tree"))
        json_file_folder.mkdir(parents=True, exist_ok=True)

        all_api_object_name_synsets = dict()
        for name in api_object_names:
            api_object_name_synsets = (
                wn.synsets(name.decode("utf-8"), lang="eng")
                if sys.version_info[0] < 3
                else wn.synsets(name, lang="eng")
            )
            synset_names = []
            for api_object_name_synset in api_object_name_synsets:
                synset_names.append(api_object_name_synset.name().split(".")[0])
            all_api_object_name_synsets[name] = synset_names
        api_tree_data["all_api_object_name_synsets"] = all_api_object_name_synsets

        api_tree_file = _get_api_tree_data_file()
        api_tree_file.touch()
        with open(api_tree_file, "w") as json_file:
            json.dump(api_tree_data, json_file)

    if write_api_tree_data:
        _write_api_tree_file(
            api_tree_data=api_tree_data, api_object_names=list(api_object_names)
        )
    return results


@functools.cache
def _get_api_tree_data():
    """Get API tree data."""
    api_tree_data_file = _get_api_tree_data_file()
    if api_tree_data_file.exists():
        json_file = open(api_tree_data_file, "r")
        api_tree_data = json.load(json_file)
        return api_tree_data


def _print_search_results(queries: list, api_tree_data: dict):
    """Print search results.

    Parameters
    ----------
    queries: list
        List of search string to match API object names.
    api_tree_data: dict
        All API object data.
    """
    api_tree_data = api_tree_data if api_tree_data else _get_api_tree_data()
    api_tree_datas = [api_tree_data["api_objects"], api_tree_data["api_tui_objects"]]
    for api_tree_data in api_tree_datas:
        for query in queries:
            for api_object in api_tree_data:
                if query in api_object:
                    print(api_object)


def _get_wildcard_matches_for_word_from_names(word: str, names: list):
    """Get wildcard matches for the given word.

    Parameters
    ----------
    word: str
       Word to search for.
    names: list
        All API object names.

    Returns
    -------
    wildcard_matches: list
        Matched API object names.
    """
    pattern = fnmatch.translate(word)
    regex = re.compile(pattern)
    return [name for name in names if regex.match(name)]


def _search_wildcard(search_string: str, api_tree_data: dict):
    """Perform wildcard search for a word through the Fluent's object hierarchy.

    Parameters
    ----------
    search_string: str
        Word to search for. Semantic search is default.
    api_tree_data: dict
        All API object data.

    Returns
    -------
        List of search string matches.
    """
    api_tree_data = api_tree_data if api_tree_data else _get_api_tree_data()
    queries = _get_wildcard_matches_for_word_from_names(
        search_string, names=list(api_tree_data["all_api_object_name_synsets"].keys())
    )
    if queries:
        _print_search_results(queries, api_tree_data=api_tree_data)


def _get_exact_match_for_word_from_names(
    word: str,
    names: list,
):
    """Get exact match for the given word.

    Parameters
    ----------
    word: str
        Word to search for.
    names: list
        All API object names.

    Returns
    -------
        List of exact match.
    """
    return [name for name in names if word == name]


def _get_capitalize_match_for_word_from_names(
    word: str,
    names: list,
):
    """Get API object name if capitalize case of the given word is present in the API
    object name.

    Parameters
    ----------
    word: str
        Word to search for.
    names: list
        All API object names.

    Returns
    -------
        List of API object names containing capitalize case of the given word.
    """
    return [name for name in names if word.capitalize() in name]


def _get_match_case_for_word_from_names(
    word: str,
    names: list,
):
    """Get API object name if the given word is present in the API object name.

    Parameters
    ----------
    word: str
        Word to search for.
    names: list
        All API object names.

    Returns
    -------
        List of API object names containing the given word.
    """
    return [name for name in names if word in name]


def _get_close_matches_for_word_from_names(
    word: str,
    names: list,
):
    """Get close matches for the given word.

    Parameters
    ----------
    word: str
        Word to search for.
    names: list
        All API object names.

    Returns
    -------
    valid_close_matches: list
        List of valid close matches.
    """
    close_matches = closest_allowed_names(word, names)
    valid_close_matches = [
        close_match for close_match in close_matches if close_match in names
    ]
    return valid_close_matches


def _search_whole_word(
    search_string: str,
    match_case: bool = False,
    match_whole_word: bool = False,
    api_tree_data: dict = None,
):
    """Perform exact search for a word through the Fluent's object hierarchy.

    Parameters
    ----------
    search_string: str
        Word to search for. Semantic search is default.
    match_case: bool
        Whether to match case. The default is ``False``.
        If ``True``, it matches the given word.
    match_whole_word: bool
        Whether to match whole word. The default is ``False``.
        If ``True``, it matches the given word, and it's capitalize case.
    api_tree_data: dict
        All API object data.

    Returns
    -------
        List of search string matches.
    """
    api_tree_data = api_tree_data if api_tree_data else _get_api_tree_data()
    queries = []
    if match_case and match_whole_word:
        queries.extend(
            _get_exact_match_for_word_from_names(
                search_string,
                names=list(api_tree_data["all_api_object_name_synsets"].keys()),
            )
        )
    elif match_case:
        queries.extend(
            _get_match_case_for_word_from_names(
                search_string,
                names=list(api_tree_data["all_api_object_name_synsets"].keys()),
            )
        )
    elif match_whole_word:
        for word in [search_string, search_string.capitalize()]:
            queries.extend(
                _get_exact_match_for_word_from_names(
                    word,
                    names=list(api_tree_data["all_api_object_name_synsets"].keys()),
                )
            )
    elif not match_case and not match_whole_word:
        queries.extend(
            _get_capitalize_match_for_word_from_names(
                search_string,
                names=list(api_tree_data["all_api_object_name_synsets"].keys()),
            )
        )
        queries.extend(
            _get_match_case_for_word_from_names(
                search_string,
                names=list(api_tree_data["all_api_object_name_synsets"].keys()),
            )
        )
    if queries:
        _print_search_results(queries, api_tree_data=api_tree_data)


def _download_nltk_data():
    """Download NLTK data on demand."""
    import ssl

    import nltk

    try:
        _create_unverified_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_context

    packages = ["wordnet", "omw-1.4"]
    for package in packages:
        nltk.download(
            package,
            quiet=True,
            raise_on_error=True,
        )


def _search_semantic(search_string: str, language: str, api_tree_data: dict):
    """Perform semantic search for a word through the Fluent's object hierarchy.

    Parameters
    ----------
    search_string: str
        Word to search for. Semantic search is the default.
    language: str
        ISO 639-3 code for the language to use for the semantic search.
        The default is ``eng`` for English. For the list of supported languages,
        see `OMW Version 1 <https://omwn.org/omw1.html>`_.
    api_tree_data: dict
        All API object data.

    Returns
    -------
    queries: list
        List of search string matches.
    """
    from nltk.corpus import wordnet as wn

    api_tree_data = api_tree_data if api_tree_data else _get_api_tree_data()
    similar_keys = set()
    search_string_synsets = (
        wn.synsets(search_string.decode("utf-8"), lang=language)
        if sys.version_info[0] < 3
        else wn.synsets(search_string, lang=language)
    )
    for api_object_name, api_object_synset_names in list(
        api_tree_data["all_api_object_name_synsets"].items()
    ):
        for search_string_synset in search_string_synsets:
            for api_object_synset_name in api_object_synset_names:
                search_string_synset_name = search_string_synset.name().split(".")[0]
                if (
                    search_string in api_object_synset_name
                    or search_string_synset_name in api_object_synset_name
                ):
                    similar_keys.add(api_object_synset_name + "*")
    if similar_keys:
        for key in similar_keys:
            _search_wildcard(key, api_tree_data)
    else:
        queries = _get_close_matches_for_word_from_names(
            search_string,
            names=list(api_tree_data["all_api_object_name_synsets"].keys()),
        )
        if queries:
            _print_search_results(queries, api_tree_data=api_tree_data)


def search(
    search_string: str,
    language: str | None = "eng",
    wildcard: bool | None = False,
    match_whole_word: bool = False,
    match_case: bool | None = True,
):
    """Search for a word through the Fluent's object hierarchy.

    Parameters
    ----------
    search_string: str
        Word to search for. Semantic search is the default.
    language: str
        ISO 639-3 code for the language to use for the semantic search.
        The default is ``eng`` for English. For the list of supported languages,
        see `OMW Version 1 <https://omwn.org/omw1.html>`_.
    wildcard: bool, optional
        Whether to use the wildcard pattern. The default is ``False``. If ``True``, the
        wildcard pattern is based on the ``fnmatch`` module and semantic matching
        is turned off.
    match_whole_word: bool, optional
        Whether to find only exact matches. The default is ``False``. If ``True``,
        only exact matches are found and semantic matching is turned off.
    match_case: bool, optional
        Whether to match case. The default is ``True``. If ``False``, the search is case-insensitive.

    Examples
    --------
    >>> import ansys.fluent.core as pyfluent
    >>> pyfluent.search("font", match_whole_word=True)
    >>> pyfluent.search("Font")
    >>> pyfluent.search("iter*", wildcard=True)
    >>> pyfluent.search("读", language="cmn")   # search 'read' in Chinese
    The most similar API objects are:
    <solver_session>.file.read (Command)
    <solver_session>.file.import_.read (Command)
    <solver_session>.mesh.surface_mesh.read (Command)
    <solver_session>.tui.display.display_states.read (Command)
    <meshing_session>.tui.display.display_states.read (Command)
    """
    if (wildcard and match_whole_word) or (wildcard and match_case):
        warnings.warn(
            "``wildcard=True`` matches wildcard pattern.",
            UserWarning,
        )
    elif language and wildcard:
        warnings.warn(
            "``wildcard=True`` matches wildcard pattern.",
            UserWarning,
        )
    elif language and match_whole_word:
        warnings.warn(
            "``match_whole_word=True`` matches the whole word (case insensitive).",
            UserWarning,
        )
    elif match_whole_word:
        warnings.warn(
            "``match_whole_word=True`` matches the whole word (case insensitive).",
            UserWarning,
        )
    elif match_case:
        warnings.warn(
            "``match_case=True`` matches the whole word (case sensitive).",
            UserWarning,
        )

    api_tree_data = _get_api_tree_data()

    try:
        _search_semantic(search_string, language, api_tree_data=api_tree_data)
    except ModuleNotFoundError:
        pass
    except LookupError:
        _download_nltk_data()
        _search_semantic(search_string, language, api_tree_data=api_tree_data)

    if wildcard:
        _search_wildcard(
            search_string,
            api_tree_data=api_tree_data,
        )
    elif match_whole_word:
        if not match_case:
            _search_whole_word(
                search_string, match_whole_word=True, api_tree_data=api_tree_data
            )
        else:
            _search_whole_word(
                search_string, match_case=True, api_tree_data=api_tree_data
            )
    else:
        _search_whole_word(
            search_string, match_whole_word=True, api_tree_data=api_tree_data
        )
