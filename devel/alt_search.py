"""Alternative implementation of the search function."""

from collections import deque
import gzip
import pickle
from pprint import pprint

import psutil

from ansys.fluent.core.generated.solver.settings_252 import root
from ansys.fluent.core.solver.flobject import NamedObject


def get_name_components(name: str):
    """
    Given a name like 'abc_def' returns ['abc', 'def']
    """
    return name.split("_")


SearchCache = {}


def build_cache(root_cls):
    """
    Build a trie from the settings module
    """
    print(f"Memory usage before building cache: {get_memory_usage():.2f} MB")

    # A depth-first algorithm is chosen for the following reasons:
    # 1. Show the search results in a depth-first order of the settings API.
    # 2. Can support a `depth` parameter in the search function to limit the depth of the search.
    queue_order = 0
    queue = deque([("", root_cls, "<solver_session>.settings", queue_order)])

    while queue:
        current_name, current_cls, current_path, rank = queue.popleft()
        SearchCache.setdefault(current_name, []).append((current_path, rank))
        for name_component in get_name_components(current_name):
            SearchCache.setdefault(name_component, []).append((current_path, rank))

        if not hasattr(current_cls, "_child_classes"):
            continue

        for k, v in current_cls._child_classes.items():
            if not issubclass(v, NamedObject):
                next_cls = v
                next_path = f"{current_path}.{k}"
            else:
                next_cls = getattr(v, "child_object_type")
                next_path = f'{current_path}.{k}["_name_"]'
            # with open("alt_search.log", "a") as f:
            #     f.write(f"{next_path}\n")
            queue_order += 1
            queue.append((k, next_cls, next_path, queue_order))

    print(f"Memory usage after building cache: {get_memory_usage():.2f} MB")


def search(search_string: str, match_whole_word: bool = False):
    """
    Basic string-based search
    """
    if not SearchCache:
        build_cache(root)
        # with open("alt_search.log", "w") as f:
        #     pprint(SearchCache, stream=f)
    if match_whole_word:
        results = SearchCache.get(search_string, [])
    else:
        results = [
            item for k, v in SearchCache.items() if search_string in k for item in v
        ]
    results.sort(key=lambda x: x[1])
    return [x[0] for x in results]


def get_memory_usage():
    """
    Print the memory usage of the current process.
    """
    process = psutil.Process()
    memory_info = process.memory_info()
    return memory_info.rss / (1024 * 1024)  # Convert bytes to MB


def save_compressed_cache():
    """
    Save the cache to a compressed file.
    """
    with gzip.open("search_cache.pkl.gz", "wb") as f:
        pickle.dump(SearchCache, f)


if __name__ == "__main__":
    # Example usage
    pprint(search("viscous", match_whole_word=True))
    pprint(len(search("viscous", match_whole_word=True)))
    pprint(search("read_case", match_whole_word=True))
    pprint(len(search("read_case", match_whole_word=True)))
    pprint(search("viscous"))
    pprint(len(search("viscous")))
    save_compressed_cache()
