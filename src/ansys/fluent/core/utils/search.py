"""Provides a module to search a word through the Fluent's object hierarchy.."""

from collections.abc import Mapping
import fnmatch
import os
from pathlib import Path
import pickle
import sys
from typing import Any, Optional
import warnings

from nltk.corpus import wordnet as wn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import ansys.fluent.core as pyfluent
from ansys.fluent.core.services.datamodel_se import PyMenu, PyNamedObjectContainer
from ansys.fluent.core.services.datamodel_tui import TUIMenu
from ansys.fluent.core.session_pure_meshing import PureMeshing
from ansys.fluent.core.session_solver import Solver
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


def get_api_tree_file_name(
    name: Optional[bool] = None,
    text: Optional[bool] = None,
    tui: Optional[bool] = None,
    version: Optional[str] = None,
) -> Path:
    """Get API tree file name."""
    from ansys.fluent.core import CODEGEN_OUTDIR

    text_file_folder = Path(os.path.join(CODEGEN_OUTDIR, "api_tree"))
    if name:
        return (text_file_folder / "api_tree_names.txt").resolve()
    elif text:
        return (text_file_folder / "api_tree.txt").resolve()
    elif tui:
        return (text_file_folder / "api_tree_tui.txt").resolve()
    else:
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
        path = ["<session>", "tui"]
        path.extend(obj._path)
        module = obj.__class__.__module__
        version = module.rsplit("_", 1)[-1]
        prefix = "<search_root>"
    elif isinstance(obj, (ClassicWorkflow, Workflow)):
        path = ["<meshing_session>", obj.rules]
        prefix = "<search_root>"
    elif isinstance(obj, BaseTask):
        path = ["<meshing_session>", obj.rules]
        path.extend([f"{k[0]}:<name>" if k[1] else k[0] for k in obj.path])
        prefix = "<search_root>"
    elif isinstance(obj, TaskContainer):
        path = ["<meshing_session>", obj.rules]
        path.extend([f"{k[0]}:<name>" if k[1] else k[0] for k in obj.path])
        path[-1] = f"{path[-1]}:<name>"
        prefix = '<search_root>["<name>"]'
    elif isinstance(obj, PyMenu):
        rules = obj.rules
        path = ["<meshing_session>" if rules in _meshing_rules else "<solver_session>"]
        path.append(rules)
        path.extend([f"{k[0]}:<name>" if k[1] else k[0] for k in obj.path])
        prefix = "<search_root>"
    elif isinstance(obj, PyNamedObjectContainer):
        rules = obj.rules
        path = ["<meshing_session>" if rules in _meshing_rules else "<solver_session>"]
        path.append(rules)
        path.extend([f"{k[0]}:<name>" if k[1] else k[0] for k in obj.path])
        path[-1] = f"{path[-1]}:<name>"
        prefix = '<search_root>["<name>"]'
    elif isinstance(obj, flobject.Group):
        module = obj.__class__.__module__
        version = module.split(".")[-2].rsplit("_", 1)[-1]
        prefix = "<search_root>"
        path = ["<solver_session>"]
        # Cannot deduce the whole path without api_tree
    elif isinstance(obj, flobject.NamedObject):
        module = obj.__class__.__module__
        version = module.split(".")[-2].rsplit("_", 1)[-1]
        prefix = '<search_root>["<name>"]'
        path = ["<solver_session>"]
        # Cannot deduce the whole path without api_tree
    return version, path, prefix


def _search(
    word: str,
    match_whole_word: bool = False,
    match_case: bool = False,
    version: Optional[str] = None,
    search_root: Optional[Any] = None,
):
    """Search for a word through the Fluent's object hierarchy.

    Parameters
    ----------
    word : str
        The word to search for.
    match_whole_word : bool, optional
        Whether to match whole word, by default False
    match_case : bool, optional
        Whether to match case, by default False
    version : str, optional
        Fluent version to search in, by default None in which case
        it will search in the latest version for which codegen was run.
    search_root : Any, optional
        The root object within which the search will be performed,
        can be a session object or any API object within a session,
        by default None in which case it will search everything.

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
    api_object_names = set()
    if version:
        version = get_version_for_file_name(version)
    root_version, root_path, prefix = _get_version_path_prefix_from_obj(search_root)
    if search_root and not prefix:
        return
    if not version:
        version = root_version
    if not version:
        for fluent_version in FluentVersion:
            version = get_version_for_file_name(fluent_version.value)
            if get_api_tree_file_name(version=version).exists():
                break
    api_tree_file = get_api_tree_file_name(version=version)
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
            # With the dynamic loading of generated api modules, we loose the filepath information
            # from which we were extracting the solver/meshing mode of the given object.
            # Anyway, we are planning to remove search_root in the newer version of search function.
            if p == "<session>":
                p = "<solver_session>"
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
                api_object_names.add(k)
                if "tui" in next_path:
                    api_tui_objects.append(f"{next_path} ({type_})")
                else:
                    api_objects.append(f"{next_path} ({type_})")
                if _match(k, word, match_whole_word, match_case):
                    print(f"{next_path} ({type_})")
            if isinstance(v, Mapping):
                inner(v, next_path, root_path)

    inner(api_tree, "", root_path)

    def _write_api_tree_file(
        api_objects: list,
        name: Optional[bool] = None,
        text: Optional[bool] = False,
        tui: Optional[bool] = False,
    ):
        api_tree_file = get_api_tree_file_name(text=text, name=name, tui=tui)
        api_tree_file.touch()
        with open(api_tree_file, "w") as file:
            for api_object in api_objects:
                file.write(f"{api_object}")
                file.write("\n")

    text_file_folder = Path(os.path.join(pyfluent.CODEGEN_OUTDIR, "api_tree"))
    text_file_folder.mkdir(parents=True, exist_ok=True)

    _write_api_tree_file(api_objects=api_objects, text=True)
    _write_api_tree_file(api_objects=api_tui_objects, tui=True)
    _write_api_tree_file(api_objects=api_object_names, name=True)


def _get_api_object_names():
    """Get API object names."""
    return [
        line.rstrip("\n")
        for line in open(get_api_tree_file_name(name=True), "r", encoding="utf-8")
    ]


def _print_search_results(queries: list, wildcard: bool):
    """Print search results.

    Parameters
    ----------
    queries: list
        List of search string to matche API object names.
    wildcard: bool
        Whether to use wildcard search.
    """
    api_tree = get_api_tree_file_name(text=True)
    api_tui_tree = get_api_tree_file_name(tui=True)
    text_files = [api_tree, api_tui_tree]
    for text_file in text_files:
        api_objects = [
            line.rstrip("\n") for line in open(text_file, "r", encoding="utf-8")
        ]
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(api_objects)
        for query in queries:
            query_vector = tfidf_vectorizer.transform([query])
            cosine_similarities = cosine_similarity(query_vector, tfidf_matrix)
            if wildcard:
                most_similar_api_object_index = cosine_similarities.argmax()
                if query in api_objects[most_similar_api_object_index]:
                    print(api_objects[most_similar_api_object_index])
            else:
                most_similar_api_object_indices = cosine_similarities.argsort()
                for most_similar_api_object_index in reversed(
                    most_similar_api_object_indices[0][-3:]
                ):
                    if query in api_objects[most_similar_api_object_index]:
                        print(api_objects[most_similar_api_object_index])


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
    wildcard_matches = [name for name in names if fnmatch.fnmatch(name, word)]
    valid_wildcard_matches = [
        wildcard_match for wildcard_match in wildcard_matches if wildcard_match in names
    ]
    return valid_wildcard_matches


def _search_wildcard(search_string: str):
    """Perform wildcard search for a word through the Fluent's object hierarchy.

    Parameters
    ----------
    search_string: str
        The word to search for. Semantic search is default.

    Returns
    -------
        List of search string matches.
    """
    names = _get_api_object_names()
    queries = _get_wildcard_matches_for_word_from_names(search_string, names)
    if queries:
        _print_search_results(queries, wildcard=True)


def _get_exact_match_for_word_from_names(
    word: str,
    names: list,
):
    """Get exact match for the given word.

    Parameters
    ----------
    word: str
        The word to search for.
    names: list
        All API object names.

    Returns
    -------
    exact_matche: list
        List of exact match.
    """
    return [name for name in names if word == name]


def _get_close_matches_for_word_from_names(
    word: str,
    names: list,
):
    """Get close matches for the given word.

    Parameters
    ----------
    word: str
        The word to search for.
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


def _search_whole_word(search_string: str, match_case: bool):
    """Perform exact search for a word through the Fluent's object hierarchy.

    Parameters
    ----------
    search_string: str
        The word to search for. Semantic search is default.
    match_case: bool
        Whether to match case. If ``True`` will match case-insensitive case.

    Returns
    -------
        List of search string matches.
    """
    names = _get_api_object_names()
    if match_case:
        search_string = search_string + "*"
        _search_wildcard(search_string, names)
    else:
        queries = _get_exact_match_for_word_from_names(search_string, names)
        if queries:
            _print_search_results(queries, wildcard=False)


def _download_nltk_data():
    """Download NLTK data on-demand."""
    import nltk

    packages = ["wordnet", "omw-1.4"]
    for package in packages:
        nltk.download(package, quiet=True)


def _search_semantic(search_string: str, language: str):
    """Perform semantic search for a word through the Fluent's object hierarchy.

    Parameters
    ----------
    search_string: str
        The word to search for. Semantic search is default.
    language: str
        The language for the semantic search.
        English is default for the semantic search.
        ISO 639-3 code of the language to be used for semantic search.
        See `https://omwn.org/omw1.html` for the list of supported languages.
        The default value is `eng` for English language.

    Returns
    -------
    queries: list
        List of search string matches.
    """
    names = _get_api_object_names()
    similar_keys = set()
    search_string_synsets = (
        wn.synsets(search_string.decode("utf-8"), lang=language)
        if sys.version_info[0] < 3
        else wn.synsets(search_string, lang=language)
    )
    for name in names:
        api_object_name_synsets = (
            wn.synsets(name.decode("utf-8"), lang=language)
            if sys.version_info[0] < 3
            else wn.synsets(name, lang="eng")
        )
        for search_string_synset in search_string_synsets:
            for api_object_name_synset in api_object_name_synsets:
                search_string_synset_name = search_string_synset.name().split(".")[0]
                api_object_synset_name = api_object_name_synset.name().split(".")[0]
                if (
                    search_string in api_object_synset_name
                    or search_string_synset_name in api_object_synset_name
                ):
                    similar_keys.add(api_object_synset_name + "*")
    if similar_keys:
        for key in similar_keys:
            _search_wildcard(key)
    else:
        queries = _get_close_matches_for_word_from_names(search_string, names)
        if queries:
            _print_search_results(queries, wildcard=True)


def search(
    search_string: str,
    language: Optional[str] = "eng",
    wildcard: Optional[bool] = False,
    match_whole_word: Optional[bool] = False,
    match_case: Optional[bool] = False,
):
    """Search for a word through the Fluent's object hierarchy.

    Parameters
    ----------
    search_string: str
        The word to search for. Semantic search is default.
    language: str
        The language for the semantic search.
        English is default for the semantic search.
        ISO 639-3 code of the language to be used for semantic search.
        See `https://omwn.org/omw1.html` for the list of supported languages.
        The default value is `eng` for English language.
    wildcard: bool
        Whether to use wildcard pattern. If ``True`` will match wildcard pattern based on ``fnmatch`` module and
        will turn off semantic matching.
    match_whole_word: bool
        Whether to get exact match. If ``True`` will match exact string and will turn off semantic matching.
    match_case: bool
        Whether to match case. If ``True`` will match case-insensitive case.

    Raises
    ------
    ValueError
        If both ``wildcard`` and ``match_whole_word`` are ``True``.

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
    if wildcard and match_whole_word:
        raise ValueError(
            "``wildcard`` cannot be ``True`` when ``match_whole_word`` is ``True``."
        )
    elif language and match_whole_word:
        warnings.warn(
            "``match_whole_word=True`` will match exact string and will turn off semantic matching.",
            UserWarning,
        )
    elif match_whole_word:
        warnings.warn(
            "``match_whole_word=True`` will turn off wildcard matching.",
            UserWarning,
        )

    if wildcard:
        _search_wildcard(search_string)
    elif match_whole_word:
        _search_whole_word(search_string, match_case)
    else:
        try:
            _search_semantic(search_string, language)
        except Exception:
            _download_nltk_data()
            _search_semantic(search_string, language)
