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

"""Provides a module to search a word through the Fluent's object hierarchy.."""

from collections.abc import Mapping
import fnmatch
import functools
import json
import os
from pathlib import Path
import pickle
import re

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


def _remove_suffix(input: str, suffix):
    if hasattr(input, "removesuffix"):
        return input.removesuffix(suffix)
    else:
        if suffix and input.endswith(suffix):
            return input[: -len(suffix)]
        return input


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
                next_path = (
                    next_path.replace("MeshingUtilities", "meshing_utilities")
                    if "MeshingUtilities" in next_path
                    else next_path
                )
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


def _print_search_results(
    queries: list, api_tree_data: dict, api_path: str | None = None
):
    """Print search results.

    Parameters
    ----------
    queries: list
        List of search string to match API object names.
    api_tree_data: dict
        All API object data.
    api_path: str, optional
        The API path to search in. The default is ``None``. If ``None``, it searches in the whole
        Fluent's object hierarchy.
    """
    results = []
    api_tree_data = api_tree_data if api_tree_data else _get_api_tree_data()
    api_tree_datas = [api_tree_data["api_objects"], api_tree_data["api_tui_objects"]]

    def _get_results(api_data, queries, api_path=None):
        def has_query_in_substrings(query, substrings):
            """Check if the query matches the substring conditions."""
            return any(substring.startswith(query) for substring in substrings)

        def has_query_in_substring_with_underscore(query, substrings):
            """Check if the query appears in a substring with an underscore."""
            return any(
                substring.find("_") != -1
                and (f"_{query}" in substring or f"_{query}_" in substring)
                for substring in substrings
            )

        results = set()

        for api_object in api_data:
            target = api_object

            if api_path:
                start_index = api_object.find(api_path)
                if start_index == -1:
                    continue
                target = api_object[start_index:]

            first_token = target.split()[0]
            substrings = first_token.split(".")

            if isinstance(queries[0], tuple):
                for query in queries:
                    api_name, score = query[0], query[1]
                    if api_name in first_token and (
                        has_query_in_substrings(api_name, substrings)
                        or has_query_in_substring_with_underscore(api_name, substrings)
                    ):
                        results.add((api_object, round(score, 2)))
            else:
                for query in queries:
                    if query in first_token and (
                        has_query_in_substrings(query, substrings)
                        or has_query_in_substring_with_underscore(query, substrings)
                    ):
                        results.add(api_object)

        return list(results)

    if not isinstance(queries[0], tuple):
        settings_results = _get_results(api_tree_datas[0], queries, api_path=api_path)
        tui_results = _get_results(api_tree_datas[1], queries, api_path=api_path)

        settings_results.sort()
        tui_results.sort()

        results.extend(settings_results)
        results.extend(tui_results)
    else:
        settings_results = _get_results(api_tree_datas[0], queries, api_path=api_path)
        tui_results = _get_results(api_tree_datas[1], queries, api_path=api_path)

        settings_results.sort()
        tui_results.sort()

        results.extend(settings_results)
        results.extend(tui_results)

        results = sorted(
            results, key=lambda api_name_score: api_name_score[1], reverse=True
        )
        results = [
            f"{api_name_score[0]} (similarity: {api_name_score[1]}%)"
            for api_name_score in results
        ]

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


def _search_wildcard(
    search_string: str | list[(str, float)],
    api_tree_data: dict,
    api_path: str | None = None,
):
    """Perform wildcard search for a word through the Fluent's object hierarchy.

    Parameters
    ----------
    search_string: str | list[(str, float)]
        Word to search for. Semantic search is default.
    api_tree_data: dict
        All API object data.
    api_path: str, optional
        The API path to search in. The default is ``None``. If ``None``, it searches in the whole
        Fluent's object hierarchy.

    Returns
    -------
        List of search string matches.
    """
    queries = []
    api_tree_data = api_tree_data if api_tree_data else _get_api_tree_data()

    if isinstance(search_string, str):
        queries.extend(
            _get_wildcard_matches_for_word_from_names(
                search_string, names=api_tree_data["all_api_object_names"]
            )
        )
    if isinstance(search_string, list):
        for api_name_score in search_string:
            matches = _get_wildcard_matches_for_word_from_names(
                api_name_score[0], names=api_tree_data["all_api_object_names"]
            )
            if matches:
                queries.extend([(match, api_name_score[1]) for match in matches])

    if queries:
        return _print_search_results(
            queries, api_tree_data=api_tree_data, api_path=api_path
        )


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
    api_path: str | None = None,
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
    api_path: str, optional
        The API path to search in. The default is ``None``. If ``None``, it searches in the whole
        Fluent's object hierarchy.

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
        return _print_search_results(
            queries, api_tree_data=api_tree_data, api_path=api_path
        )


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


def _are_words_semantically_close(query, api_name, language="eng"):
    from nltk.corpus import wordnet as wn

    similarity_threshold = (
        3.2 if language == "eng" else 0.8
    )  # Max values are 3.7 and 1.0 respectively
    max_similarity = 0.0

    synsets1 = wn.synsets(query, lang=language)
    synsets2 = wn.synsets(api_name, lang="eng")

    for syn1 in synsets1:
        for syn2 in synsets2:
            if syn1.pos() == syn2.pos():
                similarity = (
                    syn1.lch_similarity(syn2)  # Leacock–Chodorow similarity
                    if language == "eng"
                    else syn1.wup_similarity(syn2)  # Wu–Palmer similarity
                )
                if similarity is not None:
                    max_similarity = max(max_similarity, similarity)
                    if similarity >= similarity_threshold:
                        score = (
                            (similarity / 3.7) * 100
                            if language == "eng"
                            else similarity * 100
                        )
                        return True, score

    return False, 0


def _search_semantic(
    search_string: str, language: str, api_tree_data: dict, api_path: str | None = None
):
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
    api_tree_data = api_tree_data if api_tree_data else _get_api_tree_data()
    similar_keys = set()
    api_object_names = api_tree_data["all_api_object_names"]
    for api_object_name in api_object_names:
        api_obj_name = (
            api_object_name.replace("_", " ")
            if "_" in api_object_name
            else api_object_name
        )
        is_similar, score = _are_words_semantically_close(
            search_string, api_obj_name, language=language
        )
        if is_similar:
            similar_keys.add((api_object_name + "*", score))
    if similar_keys:
        sorted_similar_keys = sorted(similar_keys)
        results = []
        result = _search_wildcard(sorted_similar_keys, api_tree_data, api_path=api_path)
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
            return _print_search_results(
                queries, api_tree_data=api_tree_data, api_path=api_path
            )


def search(
    search_string: str,
    language: str | None = "eng",
    match_whole_word: bool = False,
    match_case: bool | None = True,
    api_path: str | None = None,
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
    match_whole_word: bool, optional
        Whether to find only exact matches. The default is ``False``. If ``True``,
        only exact matches are found and semantic matching is turned off.
    match_case: bool, optional
        Whether to match case. The default is ``True``. If ``False``, the search is case-insensitive.
    api_path: str, optional
        The API path to search in. The default is ``None``. If ``None``, it searches in the whole
        Fluent's object hierarchy.

    Examples
    --------
    >>> import ansys.fluent.core as pyfluent
    >>> pyfluent.search("font", match_whole_word=True)
    >>> pyfluent.search("Font")
    >>> pyfluent.search("local*", api_path="<solver_session>.setup")
    <solver_session>.setup.dynamic_mesh.methods.smoothing.radial_settings.local_smoothing (Parameter)
    <solver_session>.setup.mesh_interfaces.interface["<name>"].local_absolute_mapped_tolerance (Parameter)
    <solver_session>.setup.mesh_interfaces.interface["<name>"].local_relative_mapped_tolerance (Parameter)
    >>> pyfluent.search("读", language="cmn")   # search 'read' in Chinese
    <solver_session>.file.read (Command)
    <solver_session>.file.import_.read (Command)
    <solver_session>.mesh.surface_mesh.read (Command)
    <solver_session>.tui.display.display_states.read (Command)
    <meshing_session>.tui.display.display_states.read (Command)
    """

    api_tree_data = _get_api_tree_data()

    wildcard_pattern = re.compile(r"[*?\[\]]")

    if bool(wildcard_pattern.search(search_string)):
        return _search_wildcard(
            search_string,
            api_tree_data=api_tree_data,
            api_path=api_path,
        )
    elif match_whole_word:
        if not match_case:
            return _search_whole_word(
                search_string,
                match_whole_word=True,
                api_tree_data=api_tree_data,
                api_path=api_path,
            )
        else:
            return _search_whole_word(
                search_string,
                match_case=True,
                match_whole_word=True,
                api_tree_data=api_tree_data,
                api_path=api_path,
            )
    else:
        try:
            return _search_semantic(
                search_string, language, api_tree_data=api_tree_data, api_path=api_path
            )
        except ModuleNotFoundError:
            pass
        except LookupError:
            _download_nltk_data()
            return _search_semantic(
                search_string, language, api_tree_data=api_tree_data, api_path=api_path
            )
