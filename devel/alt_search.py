"""Alternative implementation of the search function."""

from collections import deque
from pprint import pprint

import psutil

from ansys.fluent.core.generated.solver.settings_252 import root
from ansys.fluent.core.solver.flobject import NamedObject


class TrieNode:
    """
    A node in the Trie data structure.
    """

    def __init__(self):
        self.children = {}
        self.results = []


class Trie:
    """
    A Trie (prefix tree) data structure for storing and searching search results."
    """

    def __init__(self):
        self._root = TrieNode()

    def insert(self, word, result):
        """
        Inserts a word into the Trie and associates it with the given results.
        """
        node = self._root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.results.append(result)

    def search(self, word):
        """
        Searches all results in the Trie for the given word.
        """
        node = self._root
        for char in word:
            if char not in node.children:
                return []
            node = node.children[char]

        return node.results


def get_name_components(name: str):
    """
    Given a name like 'abc_def' returns ['abc', 'def']
    """
    return name.split("_")


def build_trie(root_cls):
    """
    Build a trie from the settings module
    """
    print(f"Memory usage before building trie: {get_memory_usage():.2f} MB")

    # A depth-first algorithm is chosen for the following reasons:
    # 1. Show the search results in a depth-first order of the settings API.
    # 2. Can support a `depth` parameter in the search function to limit the depth of the search.
    queue = deque([("", root_cls, "<solver_session>.settings")])

    while queue:
        current_name, current_cls, current_path = queue.popleft()
        for component in get_name_components(current_name):
            for substring in get_all_substrings(component):
                SettingsTrie.insert(substring, current_path)

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
            queue.append((k, next_cls, next_path))

    print(f"Memory usage after building trie: {get_memory_usage():.2f} MB")


def get_all_substrings(name_component: str):
    """
    Given a name component like 'abc' returns all substrings of length > 1
    """
    if len(name_component) < 2:
        return []
    return [
        name_component[i:j]
        for i in range(len(name_component))
        for j in range(i + 2, len(name_component) + 1)
    ]


SettingsTrie = Trie()


def search(search_term):
    """
    Basic substring search
    """
    results = SettingsTrie.search(search_term)
    return results


def get_memory_usage():
    """
    Print the memory usage of the current process.
    """
    process = psutil.Process()
    memory_info = process.memory_info()
    return memory_info.rss / (1024 * 1024)  # Convert bytes to MB


if __name__ == "__main__":
    build_trie(root)
    # Example usage
    pprint(search("viscous"))
    pprint(search("isco"))
    pprint(len(search("viscous")))
    pprint(len(search("isco")))
