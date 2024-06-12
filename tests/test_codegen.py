import importlib
from pathlib import Path
import pickle
import shutil
import tempfile

import pytest
from util.solver_workflow import new_solver_session  # noqa: F401

import ansys.fluent.core as pyfluent
from ansys.fluent.core.codegen import StaticInfoType, allapigen
from ansys.fluent.core.utils.fluent_version import get_version_for_file_name
from ansys.fluent.core.utils.search import get_api_tree_file_name


@pytest.mark.codegen_required
def test_allapigen_files(new_solver_session):
    version = get_version_for_file_name(session=new_solver_session)
    importlib.import_module(f"ansys.fluent.core.generated.fluent_version_{version}")
    importlib.import_module(f"ansys.fluent.core.generated.meshing.tui_{version}")
    importlib.import_module(f"ansys.fluent.core.generated.solver.tui_{version}")
    importlib.import_module(f"ansys.fluent.core.generated.datamodel_{version}.meshing")
    importlib.import_module(f"ansys.fluent.core.generated.datamodel_{version}.workflow")
    importlib.import_module(
        f"ansys.fluent.core.generated.datamodel_{version}.preferences"
    )
    importlib.import_module(
        f"ansys.fluent.core.generated.datamodel_{version}.PartManagement"
    )
    importlib.import_module(
        f"ansys.fluent.core.generated.datamodel_{version}.PMFileManagement"
    )
    importlib.import_module(
        f"ansys.fluent.core.generated.solver.settings_{version}.root"
    )


def test_codegen_with_no_static_info(monkeypatch):
    codegen_outdir = Path(tempfile.mkdtemp())
    monkeypatch.setattr(pyfluent, "CODEGEN_OUTDIR", codegen_outdir)
    version = "251"
    allapigen.generate(version, {})
    generated_paths = list(codegen_outdir.iterdir())
    assert len(generated_paths) == 1
    assert set(p.name for p in generated_paths) == {f"api_tree_{version}.pickle"}
    api_tree_file = get_api_tree_file_name(version)
    with open(api_tree_file, "rb") as f:
        api_tree = pickle.load(f)
    assert api_tree == {"<meshing_session>": {}, "<solver_session>": {}}


def _get_nth_tui_command_static_info(n):
    return {f"C{n}": {"menus": {}, "commands": {}, "help": f"C{n} help"}}


def _get_nth_tui_menu_static_info(n, menus_static_info, commands_static_info):
    return {
        f"M{n}": {
            "menus": menus_static_info,
            "commands": commands_static_info,
            "help": f"M{n} help",
        }
    }


def _get_expected_tui_api_output(mode):
    return f'''"""Fluent {mode} TUI commands"""
#
# This is an auto-generated file.  DO NOT EDIT!
#
# pylint: disable=line-too-long

from ansys.fluent.core.services.datamodel_tui import PyMenu, TUIMenu, TUIMethod



class main_menu(TUIMenu):
    """
    Fluent {mode} main menu.
    """
    def __init__(self, service, version, mode, path):
        self.M1 = self.__class__.M1(service, version, mode, path + ["M1"])
        self.C1 = self.__class__.C1(service, version, mode, path + ["C1"])
        super().__init__(service, version, mode, path)
    class C1(TUIMethod):
        """
        C1 help.
        """

    class M1(TUIMenu):
        """
        M1 help.
        """
        def __init__(self, service, version, mode, path):
            self.M2 = self.__class__.M2(service, version, mode, path + ["M2"])
            self.C2 = self.__class__.C2(service, version, mode, path + ["C2"])
            super().__init__(service, version, mode, path)
        class C2(TUIMethod):
            """
            C2 help.
            """

        class M2(TUIMenu):
            """
            M2 help.
            """
            def __init__(self, service, version, mode, path):
                self.C3 = self.__class__.C3(service, version, mode, path + ["C3"])
                super().__init__(service, version, mode, path)
            class C3(TUIMethod):
                """
                C3 help.
                """'''


@pytest.mark.parametrize("mode", ["solver", "meshing"])
def test_codegen_with_tui_solver_static_info(mode, monkeypatch):
    codegen_outdir = Path(tempfile.mkdtemp())
    monkeypatch.setattr(pyfluent, "CODEGEN_OUTDIR", codegen_outdir)
    version = "251"
    static_infos = {}
    static_info_type = (
        StaticInfoType.TUI_SOLVER if mode == "solver" else StaticInfoType.TUI_MESHING
    )
    static_infos[static_info_type] = {
        "menus": _get_nth_tui_menu_static_info(
            1,
            _get_nth_tui_menu_static_info(2, {}, _get_nth_tui_command_static_info(3)),
            _get_nth_tui_command_static_info(2),
        ),
        "commands": _get_nth_tui_command_static_info(1),
        "help": "Root",
    }
    allapigen.generate(version, static_infos)
    generated_paths = list(codegen_outdir.iterdir())
    assert len(generated_paths) == 2
    assert set(p.name for p in generated_paths) == {f"api_tree_{version}.pickle", mode}
    solver_paths = list((codegen_outdir / mode).iterdir())
    assert len(solver_paths) == 1
    assert set(p.name for p in solver_paths) == {f"tui_{version}.py"}
    with open(codegen_outdir / mode / f"tui_{version}.py", "r") as f:
        assert f.read().strip() == _get_expected_tui_api_output(mode)
    api_tree_file = get_api_tree_file_name(version)
    with open(api_tree_file, "rb") as f:
        api_tree = pickle.load(f)
    tui_tree = {
        "tui": {"M1": {"M2": {"C3": "Command"}, "C2": "Command"}, "C1": "Command"}
    }
    api_tree_expected = {"<meshing_session>": {}, "<solver_session>": {}}
    api_tree_expected[f"<{mode}_session>"] = tui_tree
    assert api_tree == api_tree_expected
    shutil.rmtree(str(codegen_outdir))


_static_info_type_by_rules = {
    "workflow": StaticInfoType.DATAMODEL_WORKFLOW,
    "meshing": StaticInfoType.DATAMODEL_MESHING,
    "PartManagement": StaticInfoType.DATAMODEL_PART_MANAGEMENT,
    "PMFileManagement": StaticInfoType.DATAMODEL_PM_FILE_MANAGEMENT,
    "flicing": StaticInfoType.DATAMODEL_FLICING,
    "preferences": StaticInfoType.DATAMODEL_PREFERENCES,
    "solverworkflow": StaticInfoType.DATAMODEL_SOLVER_WORKFLOW,
    "MeshingUtilities": StaticInfoType.DATAMODEL_MESHING_UTILITIES,
}


def _get_datamodel_entity_static_info(
    name, singletons, namedobjects, commands, parameters
):
    return {
        name: {
            "singletons": singletons,
            "namedobjects": namedobjects,
            "commands": commands,
            "parameters": parameters,
        }
    }


def _get_datamodel_command_static_info(name, args, returntype):
    args = [{"name": arg[0], "type": arg[1]} for arg in args]
    return {name: {"commandinfo": {"args": args, "returntype": returntype}}}


_expected_datamodel_api_output = '''#
# This is an auto-generated file.  DO NOT EDIT!
#
# pylint: disable=line-too-long

from ansys.fluent.core.services.datamodel_se import (
    PyMenu,
    PyParameter,
    PyTextual,
    PyNumerical,
    PyDictionary,
    PyNamedObjectContainer,
    PyCommand,
    PyQuery
)


class Root(PyMenu):
    """
    Singleton Root.
    """
    def __init__(self, service, rules, path):
        self.N1 = self.__class__.N1(service, rules, path + [("N1", "")])
        self.S1 = self.__class__.S1(service, rules, path + [("S1", "")])
        self.P1 = self.__class__.P1(service, rules, path + [("P1", "")])
        self.C1 = self.__class__.C1(service, rules, "C1", path)
        super().__init__(service, rules, path)

    class N1(PyNamedObjectContainer):
        """
        .
        """
        class _N1(PyMenu):
            """
            Singleton _N1.
            """
            def __init__(self, service, rules, path):
                self.S3 = self.__class__.S3(service, rules, path + [("S3", "")])
                super().__init__(service, rules, path)

            class S3(PyMenu):
                """
                Singleton S3.
                """
                def __init__(self, service, rules, path):
                    super().__init__(service, rules, path)

        def __getitem__(self, key: str) -> _N1:
            return super().__getitem__(key)

    class S1(PyMenu):
        """
        Singleton S1.
        """
        def __init__(self, service, rules, path):
            self.S2 = self.__class__.S2(service, rules, path + [("S2", "")])
            self.P2 = self.__class__.P2(service, rules, path + [("P2", "")])
            self.C2 = self.__class__.C2(service, rules, "C2", path)
            super().__init__(service, rules, path)

        class S2(PyMenu):
            """
            Singleton S2.
            """
            def __init__(self, service, rules, path):
                super().__init__(service, rules, path)

        class P2(PyNumerical):
            """
            Parameter P2 of value type float.
            """
            pass

        class C2(PyCommand):
            """
            Command C2.

            Parameters
            ----------
            A2 : float

            Returns
            -------
            bool
            """
            pass

    class P1(PyTextual):
        """
        Parameter P1 of value type str.
        """
        pass

    class C1(PyCommand):
        """
        Command C1.

        Parameters
        ----------
        A1 : str

        Returns
        -------
        bool
        """
        pass'''


@pytest.mark.parametrize(
    "rules",
    [
        "workflow",
        "meshing",
        "PartManagement",
        "PMFileManagement",
        "preferences",
        "solverworkflow",
        "MeshingUtilities",
    ],
)
def test_codegen_with_datamodel_static_info(monkeypatch, rules):
    codegen_outdir = Path(tempfile.mkdtemp())
    monkeypatch.setattr(pyfluent, "CODEGEN_OUTDIR", codegen_outdir)
    version = "251"
    static_infos = {}
    static_info_type = _static_info_type_by_rules[rules]
    static_infos[static_info_type] = {
        "singletons": _get_datamodel_entity_static_info(
            "S1",
            _get_datamodel_entity_static_info("S2", {}, {}, {}, {}),
            {},
            _get_datamodel_command_static_info("C2", [("A2", "Real")], "Logical"),
            {"P2": {"type": "Real"}},
        ),
        "namedobjects": _get_datamodel_entity_static_info(
            "N1", _get_datamodel_entity_static_info("S3", {}, {}, {}, {}), {}, {}, {}
        ),
        "commands": _get_datamodel_command_static_info(
            "C1", [("A1", "String")], "Logical"
        ),
        "parameters": {"P1": {"type": "String"}},
        "help": "Root",
    }
    allapigen.generate(version, static_infos)
    generated_paths = list(codegen_outdir.iterdir())
    assert len(generated_paths) == 2
    assert set(p.name for p in generated_paths) == {
        f"api_tree_{version}.pickle",
        f"datamodel_{version}",
    }
    datamodel_paths = list((codegen_outdir / f"datamodel_{version}").iterdir())
    assert len(datamodel_paths) == 1
    assert set(p.name for p in datamodel_paths) == {f"{rules}.py"}
    with open(codegen_outdir / f"datamodel_{version}" / f"{rules}.py", "r") as f:
        assert f.read().strip() == _expected_datamodel_api_output
    api_tree_file = get_api_tree_file_name(version)
    with open(api_tree_file, "rb") as f:
        api_tree = pickle.load(f)
    datamodel_tree = {
        rules: {
            "C1": "Command",
            "N1:<name>": {"S3": {}},
            "P1": "Parameter",
            "S1": {"C2": "Command", "P2": "Parameter", "S2": {}},
        }
    }
    api_tree_expected = {"<meshing_session>": {}, "<solver_session>": {}}
    if rules in [
        "workflow",
        "meshing",
        "PartManagement",
        "PMFileManagement",
        "preferences",
        "MeshingUtilities",
    ]:
        api_tree_expected["<meshing_session>"] = datamodel_tree
    if rules in ["workflow", "flicing", "preferences", "solverworkflow"]:
        api_tree_expected["<solver_session>"] = datamodel_tree
    assert api_tree == api_tree_expected
    shutil.rmtree(str(codegen_outdir))


def _get_group_settings_static_info(name, children, commands, queries):
    return {
        name: {
            "children": children,
            "commands": commands,
            "queries": queries,
            "type": "group",
            "help": f"{name} help",
        }
    }


def _get_named_object_settings_static_info(name, object_type, children):
    return {
        name: {
            "object-type": object_type,
            "children": children,
            "type": "named-object",
            "help": f"{name} help",
        }
    }


def _get_parameter_settings_static_info(name, type_):
    return {name: {"type": type_, "help": f"{name} help"}}


def _get_command_settings_static_info(name, args):
    args = {arg[0]: {"type": arg[1], "help": f"{arg[0]} help"} for arg in args}
    return {name: {"arguments": args, "type": "command", "help": f"{name} help"}}


def _get_query_settings_static_info(name, args):
    args = {arg[0]: {"type": arg[1], "help": f"{arg[0]} help"} for arg in args}
    return {name: {"arguments": args, "type": "query", "help": f"{name} help"}}


_settings_static_info = {
    "children": (
        _get_group_settings_static_info(
            "G1",
            (
                (
                    _get_group_settings_static_info(
                        "G2",
                        _get_parameter_settings_static_info("P3", "integer"),
                        {},
                        {},
                    )
                )
                | _get_parameter_settings_static_info("P2", "real")
            ),
            _get_command_settings_static_info("C2", [("A2", "real")]),
            _get_query_settings_static_info("Q2", [("A2", "real")]),
        )
        | _get_parameter_settings_static_info("P1", "string")
        | _get_named_object_settings_static_info(
            "N1",
            _get_group_settings_static_info("G3", {}, {}, {})["G3"],
            _get_parameter_settings_static_info("P4", "string"),
        )
    ),
    "commands": _get_command_settings_static_info("C1", [("A1", "string")]),
    "queries": _get_query_settings_static_info("Q1", [("A1", "string")]),
    "type": "group",
}


_expected_init_settings_api_output = '''#
# This is an auto-generated file.  DO NOT EDIT!
#

"""A package providing Fluent's Settings Objects in Python."""
from ansys.fluent.core.solver.flobject import *

SHASH = "3e6d76a4601701388ea8258912d145b7b7c436699a50b6c7fe9a29f41eeff194"
from .root import root'''


_expected_root_settings_api_output = '''#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import (
    _ChildNamedObjectAccessorMixin,
    CreatableNamedObjectMixin,
    _NonCreatableNamedObjectMixin,
    AllowedValuesMixin,
    _InputFile,
    _OutputFile,
    _InOutFile,
)

from .G1 import G1 as G1_cls
from .P1 import P1 as P1_cls
from .N1 import N1 as N1_cls
from .C1 import C1 as C1_cls
from .Q1 import Q1 as Q1_cls

class root(Group):
    """
    'root' object.
    """

    fluent_name = ""

    child_names = \\
        ['G1', 'P1', 'N1']

    command_names = \\
        ['C1']

    query_names = \\
        ['Q1']

    _child_classes = dict(
        G1=G1_cls,
        P1=P1_cls,
        N1=N1_cls,
        C1=C1_cls,
        Q1=Q1_cls,
    )'''


_expected_A1_settings_api_output = '''#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import (
    _ChildNamedObjectAccessorMixin,
    CreatableNamedObjectMixin,
    _NonCreatableNamedObjectMixin,
    AllowedValuesMixin,
    _InputFile,
    _OutputFile,
    _InOutFile,
)


class A1(String):
    """
    A1 help.
    """

    fluent_name = "A1"'''


_expected_C1_settings_api_output = '''#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import (
    _ChildNamedObjectAccessorMixin,
    CreatableNamedObjectMixin,
    _NonCreatableNamedObjectMixin,
    AllowedValuesMixin,
    _InputFile,
    _OutputFile,
    _InOutFile,
)

from .A1 import A1 as A1_cls

class C1(Command):
    """
    C1 help.
    
    Parameters
    ----------
        A1 : str
            A1 help.
    
    """

    fluent_name = "C1"

    argument_names = \\
        ['A1']

    _child_classes = dict(
        A1=A1_cls,
    )'''  # noqa: W293


_expected_G1_settings_api_output = '''#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import (
    _ChildNamedObjectAccessorMixin,
    CreatableNamedObjectMixin,
    _NonCreatableNamedObjectMixin,
    AllowedValuesMixin,
    _InputFile,
    _OutputFile,
    _InOutFile,
)

from .G2 import G2 as G2_cls
from .P2 import P2 as P2_cls
from .C2 import C2 as C2_cls
from .Q2 import Q2 as Q2_cls

class G1(Group):
    """
    G1 help.
    """

    fluent_name = "G1"

    child_names = \\
        ['G2', 'P2']

    command_names = \\
        ['C2']

    query_names = \\
        ['Q2']

    _child_classes = dict(
        G2=G2_cls,
        P2=P2_cls,
        C2=C2_cls,
        Q2=Q2_cls,
    )'''


_expected_N1_settings_api_output = '''#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import (
    _ChildNamedObjectAccessorMixin,
    CreatableNamedObjectMixin,
    _NonCreatableNamedObjectMixin,
    AllowedValuesMixin,
    _InputFile,
    _OutputFile,
    _InOutFile,
)

from .P4 import P4 as P4_cls
from .N1_child import N1_child


class N1(NamedObject[N1_child], _NonCreatableNamedObjectMixin[N1_child]):
    """
    N1 help.
    """

    fluent_name = "N1"

    child_names = \\
        ['P4']

    _child_classes = dict(
        P4=P4_cls,
    )

    child_object_type: N1_child = N1_child
    """
    child_object_type of N1.
    """'''


_expected_N1_child_settings_api_output = '''#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import (
    _ChildNamedObjectAccessorMixin,
    CreatableNamedObjectMixin,
    _NonCreatableNamedObjectMixin,
    AllowedValuesMixin,
    _InputFile,
    _OutputFile,
    _InOutFile,
)


class N1_child(Group):
    """
    'child_object_type' of N1.
    """

    fluent_name = "child-object-type"'''


_expected_P1_settings_api_output = '''#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import (
    _ChildNamedObjectAccessorMixin,
    CreatableNamedObjectMixin,
    _NonCreatableNamedObjectMixin,
    AllowedValuesMixin,
    _InputFile,
    _OutputFile,
    _InOutFile,
)


class P1(String):
    """
    P1 help.
    """

    fluent_name = "P1"'''


_expected_Q1_settings_api_output = '''#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import (
    _ChildNamedObjectAccessorMixin,
    CreatableNamedObjectMixin,
    _NonCreatableNamedObjectMixin,
    AllowedValuesMixin,
    _InputFile,
    _OutputFile,
    _InOutFile,
)

from .A1 import A1 as A1_cls

class Q1(Query):
    """
    Q1 help.
    
    Parameters
    ----------
        A1 : str
            A1 help.
    
    """

    fluent_name = "Q1"

    argument_names = \\
        ['A1']

    _child_classes = dict(
        A1=A1_cls,
    )'''  # noqa: W293


def test_codegen_with_settings_static_info(monkeypatch):
    codegen_outdir = Path(tempfile.mkdtemp())
    monkeypatch.setattr(pyfluent, "CODEGEN_OUTDIR", codegen_outdir)
    version = "251"
    static_infos = {}
    static_infos[StaticInfoType.SETTINGS] = _settings_static_info
    allapigen.generate(version, static_infos)
    generated_paths = list(codegen_outdir.iterdir())
    assert len(generated_paths) == 2
    assert set(p.name for p in generated_paths) == {
        f"api_tree_{version}.pickle",
        "solver",
    }
    solver_paths = list((codegen_outdir / "solver").iterdir())
    assert len(solver_paths) == 1
    assert set(p.name for p in solver_paths) == {f"settings_{version}"}
    settings_paths = list((codegen_outdir / "solver" / f"settings_{version}").iterdir())
    filenames = [
        "root",
        "A1",
        "A2",
        "C1",
        "C2",
        "G1",
        "G2",
        "N1",
        "N1_child",
        "P1",
        "P2",
        "P3",
        "P4",
        "Q1",
        "Q2",
    ]
    filenames = (
        ["__init__.py"]
        + [f"{f}.py" for f in filenames]
        + [f"{f}.pyi" for f in filenames]
    )
    assert set(p.name for p in settings_paths) == set(filenames)
    with open(
        codegen_outdir / "solver" / f"settings_{version}" / "__init__.py", "r"
    ) as f:
        assert f.read().strip() == _expected_init_settings_api_output
    with open(codegen_outdir / "solver" / f"settings_{version}" / "root.py", "r") as f:
        assert f.read().strip() == _expected_root_settings_api_output
    with open(codegen_outdir / "solver" / f"settings_{version}" / "A1.py", "r") as f:
        assert f.read().strip() == _expected_A1_settings_api_output
    with open(codegen_outdir / "solver" / f"settings_{version}" / "C1.py", "r") as f:
        assert f.read().strip() == _expected_C1_settings_api_output
    with open(codegen_outdir / "solver" / f"settings_{version}" / "G1.py", "r") as f:
        assert f.read().strip() == _expected_G1_settings_api_output
    with open(codegen_outdir / "solver" / f"settings_{version}" / "N1.py", "r") as f:
        assert f.read().strip() == _expected_N1_settings_api_output
    with open(
        codegen_outdir / "solver" / f"settings_{version}" / "N1_child.py", "r"
    ) as f:
        assert f.read().strip() == _expected_N1_child_settings_api_output
    with open(codegen_outdir / "solver" / f"settings_{version}" / "P1.py", "r") as f:
        assert f.read().strip() == _expected_P1_settings_api_output
    with open(codegen_outdir / "solver" / f"settings_{version}" / "Q1.py", "r") as f:
        assert f.read().strip() == _expected_Q1_settings_api_output
    api_tree_file = get_api_tree_file_name(version)
    with open(api_tree_file, "rb") as f:
        api_tree = pickle.load(f)
    settings_tree = {
        "C1": "Command",
        "G1": {
            "C2": "Command",
            "G2": {"P3": "Parameter"},
            "P2": "Parameter",
            "Q2": "Query",
        },
        "N1:<name>": {"P4": "Parameter"},
        "P1": "Parameter",
        "Q1": "Query",
    }
    api_tree_expected = {}
    api_tree_expected[f"<meshing_session>"] = {}
    api_tree_expected[f"<solver_session>"] = settings_tree
    assert api_tree == api_tree_expected
    shutil.rmtree(str(codegen_outdir))


def test_codegen_with_zipped_settings_static_info(monkeypatch):
    codegen_outdir = Path(tempfile.mkdtemp())
    monkeypatch.setattr(pyfluent, "CODEGEN_OUTDIR", codegen_outdir)
    monkeypatch.setattr(pyfluent, "CODEGEN_ZIP_SETTINGS", True)
    version = "251"
    static_infos = {}
    static_infos[StaticInfoType.SETTINGS] = _settings_static_info
    allapigen.generate(version, static_infos)
    generated_paths = list(codegen_outdir.iterdir())
    assert len(generated_paths) == 2
    assert set(p.name for p in generated_paths) == {
        f"api_tree_{version}.pickle",
        "solver",
    }
    solver_paths = list((codegen_outdir / "solver").iterdir())
    assert len(solver_paths) == 1
    assert set(p.name for p in solver_paths) == {f"settings_{version}.zip"}
    shutil.rmtree(str(codegen_outdir))
