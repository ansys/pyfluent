"""Provides a module to search a word through the Fluent's object hierarchy.."""

from collections.abc import Mapping
import fnmatch
import functools
import json
import os
from pathlib import Path
import pickle
import re
import warnings

import ansys.fluent.core as pyfluent
from ansys.fluent.core.solver.error_message import closest_allowed_names
from ansys.fluent.core.utils.fluent_version import (
    FluentVersion,
    get_version_for_file_name,
)


def _get_api_tree_data_file_path():
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


def _generate_api_data(
    version: str | None = None,
):
    """Generate API tree data.

    Parameters
    ----------
    version : str, optional
        Fluent version to search in. The default is ``None``. If ``None``,
        it searches in the latest version for which codegen was run.
    write_api_tree_data: bool, optional
        Whether to write the API tree data.
    """
    api_objects = set()
    api_tui_objects = set()
    api_object_names = set()
    if version:
        version = get_version_for_file_name(version)
    if not version:
        for fluent_version in FluentVersion:
            version = get_version_for_file_name(fluent_version.value)
            if get_api_tree_file_name(version).exists():
                break
    api_tree_file = get_api_tree_file_name(version)
    with open(api_tree_file, "rb") as f:
        api_tree = pickle.load(f)

    def inner(tree, path):
        for k, v in tree.items():
            if k in ("<meshing_session>", "<solver_session>"):
                next_path = k
            else:
                if k.endswith(":<name>"):
                    k = _remove_suffix(k, ":<name>")
                    next_path = f'{path}.{k}["<name>"]'
                elif k.endswith(":<index>"):
                    k = _remove_suffix(k, ":<index>")
                    next_path = f"{path}.{k}[<index>]"
                else:
                    next_path = f"{path}.{k}"
                type_ = "Object" if isinstance(v, Mapping) else v
                api_object_names.add(k)
                if "tui" in next_path:
                    api_tui_objects.add(f"{next_path} ({type_})")
                else:
                    api_objects.add(f"{next_path} ({type_})")
            if isinstance(v, Mapping):
                inner(v, next_path)

    inner(api_tree, "")

    api_tree_data = dict()
    api_tree_data["api_objects"] = sorted(list(api_objects))
    api_tree_data["api_tui_objects"] = sorted(list(api_tui_objects))
    api_tree_data["all_api_object_names"] = sorted(list(api_object_names))

    def _write_api_tree_file(api_tree_data: dict, api_object_names: list):
        from nltk.corpus import wordnet as wn

        _download_nltk_data()
        from ansys.fluent.core import CODEGEN_OUTDIR

        json_file_folder = Path(os.path.join(CODEGEN_OUTDIR, "api_tree"))
        json_file_folder.mkdir(parents=True, exist_ok=True)

        all_api_object_name_synsets = dict()
        for name in api_object_names:
            api_object_name_synsets = wn.synsets(name, lang="eng")
            synset_names = set()
            for api_object_name_synset in api_object_name_synsets:
                synset_names.add(api_object_name_synset.name())
            if synset_names:
                all_api_object_name_synsets[name] = sorted(list(synset_names))
        api_tree_data["all_api_object_name_synsets"] = all_api_object_name_synsets

        api_tree_file_path = _get_api_tree_data_file_path()
        api_tree_file_path.touch()
        with open(api_tree_file_path, "w") as json_file:
            json.dump(api_tree_data, json_file)

    _write_api_tree_file(
        api_tree_data=api_tree_data, api_object_names=list(api_object_names)
    )
    api_tree_file.unlink()


@functools.cache
def _get_api_tree_data():
    """Get API tree data."""
    api_tree_data_file_path = _get_api_tree_data_file_path()
    if api_tree_data_file_path.exists():
        json_file = open(api_tree_data_file_path, "r")
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
    results = []
    api_tree_data = api_tree_data if api_tree_data else _get_api_tree_data()
    api_tree_datas = [api_tree_data["api_objects"], api_tree_data["api_tui_objects"]]

    def _get_results(api_tree_data):
        results = []
        for query in queries:
            for api_object in api_tree_data:
                if api_object.split()[0].endswith(query):
                    results.append(api_object)
        return results

    settings_results = _get_results(api_tree_datas[0])
    tui_results = _get_results(api_tree_datas[1])

    settings_results.sort()
    tui_results.sort()

    results.extend(settings_results)
    results.extend(tui_results)

    if pyfluent.PRINT_SEARCH_RESULTS:
        for result in results:
            print(result)
    elif results:
        return results


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
        search_string, names=api_tree_data["all_api_object_names"]
    )
    if queries:
        return _print_search_results(queries, api_tree_data=api_tree_data)


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
    return list({name for name in names if word == name or word in name})


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
    match_whole_word: bool = True,
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
    if not match_case and not match_whole_word:
        queries.extend(
            _get_capitalize_match_for_word_from_names(
                search_string,
                names=api_tree_data["all_api_object_names"],
            )
        )
        queries.extend(
            _get_match_case_for_word_from_names(
                search_string,
                names=api_tree_data["all_api_object_names"],
            )
        )
    elif match_case and match_whole_word:
        queries.extend(
            _get_exact_match_for_word_from_names(
                search_string,
                names=api_tree_data["all_api_object_names"],
            )
        )
    elif match_case:
        queries.extend(
            _get_match_case_for_word_from_names(
                search_string,
                names=api_tree_data["all_api_object_names"],
            )
        )
    elif match_whole_word:
        for word in [search_string, search_string.capitalize()]:
            queries.extend(
                _get_exact_match_for_word_from_names(
                    word,
                    names=api_tree_data["all_api_object_names"],
                )
            )
    if queries:
        return _print_search_results(queries, api_tree_data=api_tree_data)


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
            halt_on_error=False,
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
    search_string_synsets = set(wn.synsets(search_string, lang=language))
    for api_object_name, api_object_synset_names in list(
        api_tree_data["all_api_object_name_synsets"].items()
    ):
        api_object_synsets = {
            wn.synset(api_object_synset_name)
            for api_object_synset_name in api_object_synset_names
        }
        if search_string_synsets & api_object_synsets:
            similar_keys.add(api_object_name + "*")
    if similar_keys:
        results = []
        for key in similar_keys:
            result = _search_wildcard(key, api_tree_data)
            if result:
                results.extend(result)
        if results:
            return results
    else:
        queries = _get_close_matches_for_word_from_names(
            search_string,
            names=api_tree_data["all_api_object_names"],
        )
        if queries:
            return _print_search_results(queries, api_tree_data=api_tree_data)


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

    api_tree_data = _get_api_tree_data()

    if wildcard:
        return _search_wildcard(
            search_string,
            api_tree_data=api_tree_data,
        )
    elif match_whole_word:
        if not match_case:
            return _search_whole_word(
                search_string, match_whole_word=True, api_tree_data=api_tree_data
            )
        else:
            return _search_whole_word(
                search_string,
                match_case=True,
                match_whole_word=True,
                api_tree_data=api_tree_data,
            )
    else:
        try:
            return _search_semantic(
                search_string, language, api_tree_data=api_tree_data
            )
        except ModuleNotFoundError:
            pass
        except LookupError:
            _download_nltk_data()
            return _search_semantic(
                search_string, language, api_tree_data=api_tree_data
            )
