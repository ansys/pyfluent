from collections.abc import Mapping
from pathlib import Path
import pickle
from typing import Any

# from ansys.fluent.core.session import BaseSession
from ansys.fluent.core.launcher.launcher import FluentVersion
from ansys.fluent.core.utils.fluent_version import get_version_for_filepath


def get_api_tree_filepath(version: str) -> Path:
    return Path(__file__) / ".." / ".." / "data" / f"api_tree_{version}.pickle"


def _match(source: str, word: str, match_whole_word: bool, match_case: bool):
    if not match_case:
        source = source.lower()
        word = word.lower()
    if match_whole_word:
        return source == word
    else:
        return word in source


def search(
    word: str,
    match_whole_word: bool = False,
    match_case: bool = False,
    version: str = None,
    root: Any = None,
):
    """
    Search for a word through the API object hierarchy.

    Parameters
    ----------
    word : str
        The word to search for.
    match_whole_word : bool, optional
        _description_, by default False
    match_case : bool, optional
        _description_, by default False
    version : str, optional
        Fluent version to search in, by default None in which case
        it will search in the latest released version.
    root : Any, optional
        The root object within which the search will be performed,
        can be a session object or any API object within a session,
        by default None in which case it will search everything.
    """
    if not version:
        version = str(list(FluentVersion)[1])
    version = get_version_for_filepath(version)
    api_tree_file = get_api_tree_filepath(version)
    with open(api_tree_file, "rb") as f:
        api_tree = pickle.load(f)

    def inner(tree, path=""):
        for k, v in tree.items():
            if k in ("<meshing_session>", "<solver_session>"):
                next_path = k
            else:
                if k.endswith(":<name>"):
                    k = k.removesuffix(":<name>")
                    next_path = f"{path}.{k}[<name>]"
                else:
                    next_path = f"{path}.{k}"
                if _match(k, word, match_whole_word, match_case):
                    type_ = "Object" if isinstance(v, Mapping) else v
                    print(f"{next_path} ({type_})")
            if isinstance(v, Mapping):
                inner(v, next_path)

    inner(api_tree)
