from collections.abc import Mapping
from pathlib import Path
import pickle
from typing import Any

from ansys.fluent.core.launcher.launcher import FluentVersion
from ansys.fluent.core.services.datamodel_se import PyMenu, PyNamedObjectContainer
from ansys.fluent.core.services.datamodel_tui import TUIMenu
from ansys.fluent.core.session_pure_meshing import PureMeshing
from ansys.fluent.core.session_solver import Solver
from ansys.fluent.core.solver import flobject
from ansys.fluent.core.utils.fluent_version import get_version_for_filepath
from ansys.fluent.core.workflow import BaseTask, TaskContainer, WorkflowWrapper


def get_api_tree_filepath(version: str) -> Path:
    return (
        Path(__file__) / ".." / ".." / "data" / f"api_tree_{version}.pickle"
    ).resolve()


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
        version = get_version_for_filepath(obj.get_fluent_version())
        prefix = "<root>"
    elif isinstance(obj, Solver):
        path = ["<solver_session>"]
        version = get_version_for_filepath(obj.get_fluent_version())
        prefix = "<root>"
    elif isinstance(obj, TUIMenu):
        module = obj.__class__.__module__
        path = [
            "<meshing_session>"
            if module.startswith("ansys.fluent.core.meshing")
            else "<solver_session>",
            "tui",
        ]
        path.extend(obj.path)
        version = module.rsplit("_", 1)[-1]
        prefix = "<root>"
    elif isinstance(obj, WorkflowWrapper):
        path = ["<meshing_session>", obj.rules]
        module = obj._workflow.__class__.__module__
        module = _remove_suffix(module, ".workflow")
        version = module.rsplit("_", 1)[-1]
        prefix = "<root>"
    elif isinstance(obj, BaseTask):
        path = ["<meshing_session>", obj.rules]
        path.extend([f"{k[0]}:<name>" if k[1] else k[0] for k in obj.path])
        module = obj._workflow.__class__.__module__
        module = _remove_suffix(module, ".workflow")
        version = module.rsplit("_", 1)[-1]
        prefix = "<root>"
    elif isinstance(obj, TaskContainer):
        path = ["<meshing_session>", obj.rules]
        path.extend([f"{k[0]}:<name>" if k[1] else k[0] for k in obj.path])
        path[-1] = f"{path[-1]}:<name>"
        module = obj._container._workflow.__class__.__module__
        module = _remove_suffix(module, ".workflow")
        version = module.rsplit("_", 1)[-1]
        prefix = '<root>["<name>"]'
    elif isinstance(obj, PyMenu):
        rules = obj.rules
        path = ["<meshing_session>" if rules in _meshing_rules else "<solver_session>"]
        path.append(rules)
        path.extend([f"{k[0]}:<name>" if k[1] else k[0] for k in obj.path])
        module = obj.__class__.__module__
        module = _remove_suffix(module, f".{rules}")
        version = module.rsplit("_", 1)[-1]
        prefix = "<root>"
    elif isinstance(obj, PyNamedObjectContainer):
        rules = obj.rules
        path = ["<meshing_session>" if rules in _meshing_rules else "<solver_session>"]
        path.append(rules)
        path.extend([f"{k[0]}:<name>" if k[1] else k[0] for k in obj.path])
        path[-1] = f"{path[-1]}:<name>"
        module = obj.__class__.__module__
        module = _remove_suffix(module, f".{rules}")
        version = module.rsplit("_", 1)[-1]
        prefix = '<root>["<name>"]'
    elif isinstance(obj, flobject.Group):
        module = obj.__class__.__module__
        version = module.split(".")[-2].rsplit("_", 1)[-1]
        prefix = "<root>"
        path = ["<solver_session>"]
        # Cannot deduce the whole path without api_tree
    elif isinstance(obj, flobject.NamedObject):
        module = obj.__class__.__module__
        version = module.split(".")[-2].rsplit("_", 1)[-1]
        prefix = '<root>["<name>"]'
        path = ["<solver_session>"]
        # Cannot deduce the whole path without api_tree
    return version, path, prefix


def search(
    word: str,
    match_whole_word: bool = False,
    match_case: bool = False,
    version: str = None,
    root: Any = None,
):
    """
    Search for a word through the Fluent's object hierarchy.

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
    root : Any, optional
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
    if version:
        version = get_version_for_filepath(version)
    root_version, root_path, prefix = _get_version_path_prefix_from_obj(root)
    if root and not prefix:
        return
    if not version:
        version = root_version
    if not version:
        for fluent_version in FluentVersion:
            version = get_version_for_filepath(str(fluent_version))
            if get_api_tree_filepath(version).exists():
                break
    api_tree_file = get_api_tree_filepath(version)
    with open(api_tree_file, "rb") as f:
        api_tree = pickle.load(f)

    if isinstance(root, (flobject.Group, flobject.NamedObject)):
        path = root_path + [flobject.to_python_name(x) for x in root.path.split("/")]
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
                if _match(k, word, match_whole_word, match_case):
                    type_ = "Object" if isinstance(v, Mapping) else v
                    print(f"{next_path} ({type_})")
            if isinstance(v, Mapping):
                inner(v, next_path, root_path)

    inner(api_tree, "", root_path)
