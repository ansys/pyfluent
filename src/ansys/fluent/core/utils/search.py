import os
from typing import Any

# from ansys.fluent.core.session import BaseSession


def get_api_tree_filepath(version: str):
    this_dirname = os.path.dirname(__file__)
    return os.path.normpath(
        os.path.join(
            this_dirname,
            "..",
            "..",
            "..",
            "..",
            "..",
            "data",
            f"api_tree_{version}.pickle",
        )
    )


def search(pattern: str, root: Any = None):
    """_summary_

    Parameters
    ----------
    pattern : str
        The pattern to search for.
    root : Any, optional
        The root object within which the search will be performed,
        can be a session object or any API object within a session,
        by default None in which case it will search everything.
    """
    pass
