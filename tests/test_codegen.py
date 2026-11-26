# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
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

import ast
from copy import deepcopy
import importlib
import importlib.util
from io import StringIO
from pathlib import Path
import pickle
import pydoc
import shutil
import sys
import tempfile
import types
from typing import Generic, TypeVar

import pytest

import ansys.fluent.core as pyfluent
from ansys.fluent.core.codegen import (
    StaticInfoType,
    allapigen,
    get_codegen_datamodel_dir,
    get_codegen_tui_dir,
    settingsgen,
)
from ansys.fluent.core.codegen.api_tree import get_api_tree_file_name
from ansys.fluent.core.codegen.builtin_settingsgen import (
    _generate_pyi_file,
    _get_builtin_settings_paths,
)
from ansys.fluent.core.codegen.datamodelgen import datamodel_file_name_map
from ansys.fluent.core.solver import flobject
from ansys.fluent.core.utils.fluent_version import (
    FluentVersion,
    get_version_for_file_name,
)


def test_builtin_settings_generation_paths_and_imports(monkeypatch, tmp_path):
    monkeypatch.setattr(pyfluent.config, "codegen_outdir", tmp_path)

    py_file, pyi_file = _get_builtin_settings_paths()
    assert py_file == tmp_path / "solver" / "settings_builtin.py"
    assert pyi_file == tmp_path / "solver" / "settings_builtin.pyi"

    _generate_pyi_file(FluentVersion.v271)
    pyi_contents = pyi_file.read_text(encoding="utf-8")
    assert (
        "ansys.fluent.core.generated.v271.solver.settings import root" in pyi_contents
    )


def test_allapigen_files(new_solver_session):
    version = get_version_for_file_name(session=new_solver_session)
    version_dir = pyfluent.codegen.get_codegen_version_dir(
        version, pyfluent.config.codegen_outdir
    )
    importlib.import_module(f"ansys.fluent.core.generated.v{version}.fluent_version")
    importlib.import_module(f"ansys.fluent.core.generated.v{version}.meshing.tui")
    importlib.import_module(f"ansys.fluent.core.generated.v{version}.solver.tui")
    importlib.import_module(f"ansys.fluent.core.generated.v{version}.meshing.meshing")
    importlib.import_module(
        f"ansys.fluent.core.generated.v{version}.object_model.workflow"
    )
    importlib.import_module(
        f"ansys.fluent.core.generated.v{version}.meshing.meshing_utilities"
    )
    importlib.import_module(
        f"ansys.fluent.core.generated.v{version}.object_model.preferences"
    )
    importlib.import_module(
        f"ansys.fluent.core.generated.v{version}.meshing.part_management"
    )
    importlib.import_module(
        f"ansys.fluent.core.generated.v{version}.meshing.pm_file_management"
    )
    importlib.import_module(f"ansys.fluent.core.generated.v{version}.solver.settings")
    assert get_codegen_tui_dir(version_dir, "meshing").name == "meshing"


@pytest.mark.parametrize(
    "module_name,expected_dir",
    [
        ("meshing", "meshing"),
        ("meshing_workflow", "meshing"),
        ("part_management", "meshing"),
        ("pm_file_management", "meshing"),
        ("meshing_utilities", "meshing"),
        ("workflow", "object_model"),
        ("preferences", "object_model"),
    ],
)
def test_codegen_datamodel_directory_routing(tmp_path, module_name, expected_dir):
    assert get_codegen_datamodel_dir(tmp_path, module_name) == tmp_path / expected_dir


def test_api_tree_data_path_is_shared(tmp_path, monkeypatch):
    monkeypatch.setattr(pyfluent.config, "codegen_outdir", tmp_path)
    from ansys.fluent.core.codegen.api_tree import get_api_tree_data_file_path

    assert get_api_tree_data_file_path() == tmp_path / "api_tree" / "api_objects.json"


@pytest.mark.fluent_version(">=26.1")
def test_settings_allowed_values(new_solver_session):
    version = get_version_for_file_name(session=new_solver_session)
    module = importlib.import_module(
        f"ansys.fluent.core.generated.v{version}.solver.settings"
    )

    file_type_1 = getattr(module, "file_type_1")
    assert set(file_type_1._allowed_values) == set(
        ["case", "case-data", "data", "mesh"]
    )

    unit = getattr(module, "unit")
    assert set(unit._allowed_values) == set(["m", "cm", "mm", "in", "ft"])


def test_codegen_with_no_static_info(monkeypatch):
    codegen_outdir = Path(tempfile.mkdtemp())
    monkeypatch.setattr(pyfluent.config, "codegen_outdir", codegen_outdir)
    version = "252"
    allapigen.generate(version, {})
    generated_paths = list(codegen_outdir.iterdir())
    assert len(generated_paths) == 1
    assert set(p.name for p in generated_paths) == {f"v{version}"}
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

from ansys.fluent.core.services.text_interface import PyMenu, TUIMenu, TUIMethod



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
    monkeypatch.setattr(pyfluent.config, "codegen_outdir", codegen_outdir)
    version = "252"
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
    version_dir = codegen_outdir / f"v{version}"
    generated_paths = list(version_dir.iterdir())
    assert len(generated_paths) == 2
    output_dir = mode
    assert set(p.name for p in generated_paths) == {"api_tree.pickle", output_dir}
    solver_paths = list((version_dir / output_dir).iterdir())
    assert len(solver_paths) == 1
    assert set(p.name for p in solver_paths) == {"tui.py"}
    with open(version_dir / output_dir / "tui.py", "r") as f:
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
    "meshing_workflow": StaticInfoType.DATAMODEL_MESHING_WORKFLOW,
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

from ansys.fluent.core.services.object_model import (
    PyMenu,
    PyNamedObject,
    PyParameter,
    PyTextual,
    PyNumerical,
    PyDictionary,
    PyNamedObjectContainer,
    PyCommand,
    PyQuery,
    PyArguments,
    PyArgumentsTextualSubItem,
    PyArgumentsNumericalSubItem,
    PyArgumentsDictionarySubItem,
    PyArgumentsParameterSubItem,
    PyArgumentsSingletonSubItem
)


class Root(PyMenu):
    """
    Root group.
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
        class _N1(PyNamedObject):
            """
            _N1 group.
            """
            def __init__(self, service, rules, path):
                self.S3 = self.__class__.S3(service, rules, path + [("S3", "")])
                super().__init__(service, rules, path)

            class S3(PyMenu):
                """
                S3 group.
                """
                def __init__(self, service, rules, path):
                    super().__init__(service, rules, path)

        def __getitem__(self, key: str) -> _N1:
            return super().__getitem__(key)

    class S1(PyMenu):
        """
        S1 group.
        """
        def __init__(self, service, rules, path):
            self.S2 = self.__class__.S2(service, rules, path + [("S2", "")])
            self.P2 = self.__class__.P2(service, rules, path + [("P2", "")])
            self.C2 = self.__class__.C2(service, rules, "C2", path)
            super().__init__(service, rules, path)

        class S2(PyMenu):
            """
            S2 group.
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
            C2 command.


            Parameters
            ----------
            A2 : float

            Returns
            -------
            bool
            """
            class _C2Arguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)
                    self.A2 = self._A2(self, "A2", service, rules, path)

                class _A2(PyArgumentsNumericalSubItem):
                    """
                    Argument A2.
                    """

            def create(self) -> _C2Arguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._create_arguments_instance(*args)

    class P1(PyTextual):
        """
        Parameter P1 of value type str.
        """
        pass

    class C1(PyCommand):
        """
        C1 command.


        Parameters
        ----------
        A1 : str

        Returns
        -------
        bool
        """
        class _C1Arguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.A1 = self._A1(self, "A1", service, rules, path)

            class _A1(PyArgumentsTextualSubItem):
                """
                Argument A1.
                """

        def create(self) -> _C1Arguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._create_arguments_instance(*args)'''


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
    monkeypatch.setattr(pyfluent.config, "codegen_outdir", codegen_outdir)
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
    version_dir = codegen_outdir / f"v{version}"
    output_dir = get_codegen_datamodel_dir(version_dir, datamodel_file_name_map[rules])
    generated_paths = list(version_dir.iterdir())
    assert len(generated_paths) == 2
    assert set(p.name for p in generated_paths) == {
        "api_tree.pickle",
        output_dir.name,
    }
    datamodel_paths = list(output_dir.iterdir())
    assert len(datamodel_paths) == 1 or 2
    assert set(p.name for p in datamodel_paths) == {
        f"{datamodel_file_name_map[rules]}.py"
    } or {f"{datamodel_file_name_map[rules]}.pyi"}
    with open(
        codegen_outdir
        / f"v{version}"
        / output_dir.name
        / f"{datamodel_file_name_map[rules]}.py",
        "r",
    ) as f:
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
        "meshing_workflow",
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
            "api_exposure_level": "alpha",
            "help": f"{name} help",
        }
    }


def _get_named_object_settings_static_info(name, object_type, children):
    return {
        name: {
            "object_type": object_type,
            "children": children,
            "type": "named-object",
            "help": f"{name} help",
        }
    }


def _get_parameter_settings_static_info(name, type_):
    return {
        name: {"type": type_, "api_exposure_level": "stable", "help": f"{name} help"}
    }


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


_expected_settings_api_output = '''#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import (
    ExposureLevel,
    _ChildNamedObjectAccessorMixin,
    _NonCreatableNamedObjectMixin,
    _NamedObjectCommandBase,
    _merge_named_object_child_classes,
    _merge_named_object_command_names,
    _InputFile,
    _OutputFile,
    _InOutFile,
    _FlStringConstant,
)

class P3(Integer):
    """
    P3 help.
    """
    _version = '251'
    exposure_level = ExposureLevel.ALPHA
    fluent_name = 'P3'
    _python_name = 'P3'

class G2(Group):
    """
    G2 help.
    """
    _version = '251'
    exposure_level = ExposureLevel.ALPHA
    fluent_name = 'G2'
    _python_name = 'G2'
    child_names = ['P3']
    _child_classes = dict(
        P3=P3,
    )

class P2(Real):
    """
    P2 help.
    """
    _version = '251'
    exposure_level = ExposureLevel.ALPHA
    fluent_name = 'P2'
    _python_name = 'P2'

class A2(Real):
    """
    A2 help.
    """
    _version = '251'
    exposure_level = ExposureLevel.ALPHA
    fluent_name = 'A2'
    _python_name = 'A2'

class C2(Command):
    """
    C2 help.
    
    Parameters
    ----------
        A2 : real
            A2 help.
    """
    _version = '251'
    exposure_level = ExposureLevel.ALPHA
    fluent_name = 'C2'
    _python_name = 'C2'
    argument_names = ['A2']
    _child_classes = dict(
        A2=A2,
    )

class Q2(Query):
    """
    Q2 help.
    
    Parameters
    ----------
        A2 : real
            A2 help.
    """
    _version = '251'
    exposure_level = ExposureLevel.ALPHA
    fluent_name = 'Q2'
    _python_name = 'Q2'
    argument_names = ['A2']
    _child_classes = dict(
        A2=A2,
    )

class G1(Group):
    """
    G1 help.
    """
    _version = '251'
    exposure_level = ExposureLevel.ALPHA
    fluent_name = 'G1'
    _python_name = 'G1'
    child_names = ['G2', 'P2']
    command_names = ['C2']
    query_names = ['Q2']
    _child_classes = dict(
        G2=G2,
        P2=P2,
        C2=C2,
        Q2=Q2,
    )

class P1(String):
    """
    P1 help.
    """
    _version = '251'
    exposure_level = ExposureLevel.STABLE
    fluent_name = 'P1'
    _python_name = 'P1'

class P4(String):
    """
    P4 help.
    """
    _version = '251'
    exposure_level = ExposureLevel.STABLE
    fluent_name = 'P4'
    _python_name = 'P4'

class N1_item(Group):
    """
    'child_object_type' of N1.
    """
    _version = '251'
    exposure_level = ExposureLevel.ALPHA
    fluent_name = 'child-object-type'
    _python_name = 'N1_item'

class N1(NamedObject[N1_item], _NonCreatableNamedObjectMixin[N1_item]):
    """
    N1 help.
    """
    _version = '251'
    exposure_level = ExposureLevel.STABLE
    fluent_name = 'N1'
    _python_name = 'N1'
    child_names = ['P4']
    _child_classes = dict(
        P4=P4,
    )
    child_object_type = N1_item

class A1(String):
    """
    A1 help.
    """
    _version = '251'
    exposure_level = ExposureLevel.STABLE
    fluent_name = 'A1'
    _python_name = 'A1'

class C1(Command):
    """
    C1 help.
    
    Parameters
    ----------
        A1 : str
            A1 help.
    """
    _version = '251'
    exposure_level = ExposureLevel.STABLE
    fluent_name = 'C1'
    _python_name = 'C1'
    argument_names = ['A1']
    _child_classes = dict(
        A1=A1,
    )

class Q1(Query):
    """
    Q1 help.
    
    Parameters
    ----------
        A1 : str
            A1 help.
    """
    _version = '251'
    exposure_level = ExposureLevel.STABLE
    fluent_name = 'Q1'
    _python_name = 'Q1'
    argument_names = ['A1']
    _child_classes = dict(
        A1=A1,
    )

class root(Group):
    """
    'root' object.
    """
    _version = '251'
    exposure_level = ExposureLevel.STABLE
    fluent_name = ''
    _python_name = 'root'
    child_names = ['G1', 'P1', 'N1']
    command_names = ['C1']
    query_names = ['Q1']
    _child_classes = dict(
        G1=G1,
        P1=P1,
        N1=N1,
        C1=C1,
        Q1=Q1,
    )'''  # noqa: W293


def test_codegen_with_settings_static_info(monkeypatch):
    codegen_outdir = Path(tempfile.mkdtemp())
    monkeypatch.setattr(pyfluent.config, "codegen_outdir", codegen_outdir)
    version = "251"
    static_infos = {}
    static_infos[StaticInfoType.SETTINGS] = _settings_static_info
    allapigen.generate(version, static_infos)
    version_dir = codegen_outdir / f"v{version}"
    generated_paths = list(version_dir.iterdir())
    assert len(generated_paths) == 2
    assert set(p.name for p in generated_paths) == {
        "api_tree.pickle",
        "solver",
    }
    assert {p.name for p in (version_dir / "solver").glob("*.py*")} == {
        "settings.py",
        "settings.pyi",
    }
    with open(version_dir / "solver" / "settings.py", "r") as f:
        expected_settings_api_output = _expected_settings_api_output
        assert f.read().strip() == expected_settings_api_output
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
    api_tree_expected["<meshing_session>"] = {}
    api_tree_expected["<solver_session>"] = settings_tree
    assert api_tree == api_tree_expected
    shutil.rmtree(str(codegen_outdir))


def test_settings_command_stub_generates_command_objects(monkeypatch, tmp_path):
    monkeypatch.setattr(pyfluent.config, "codegen_outdir", tmp_path)
    settings_static_info = {
        "children": _get_group_settings_static_info(
            "file",
            {},
            _get_command_settings_static_info(
                "read_case",
                [("file_name", "file"), ("pdf_file_name", "file")],
            )
            | _get_command_settings_static_info(
                "rename", [("old", "string"), ("new", "string")]
            ),
            _get_query_settings_static_info("status", [("name", "string")]),
        ),
        "commands": {},
        "queries": {},
        "type": "group",
    }

    settingsgen.generate("271", {StaticInfoType.SETTINGS: settings_static_info})
    stub = (tmp_path / "v271" / "solver" / "settings.pyi").read_text(encoding="utf-8")
    ast.parse(stub)

    assert "class read_case(Command):" in stub
    assert "    file_name: file_name\n" in stub
    assert "    pdf_file_name: pdf_file_name\n" in stub
    assert (
        "    def __call__(self, *, file_name: str = ..., "
        "pdf_file_name: str = ...) -> StateType | None: ...\n"
    ) in stub
    assert "class rename(CommandWithPositionalArgs):" in stub
    assert (
        "    def __call__(self, old: str = ..., new: str = ...) "
        "-> StateType | None: ...\n"
    ) in stub
    assert "    read_case: read_case\n" in stub
    assert "    rename: rename\n" in stub
    assert "    def status(self, name: str):\n" in stub


@pytest.mark.parametrize("version", ["242", "251", "261"])
def test_named_object_commands_share_generated_bases(
    monkeypatch, tmp_path, mocker, version
):
    monkeypatch.setattr(pyfluent.config, "codegen_outdir", tmp_path)
    commands = (
        _get_command_settings_static_info("create", [("name", "string")])
        | _get_command_settings_static_info("delete", [("name-list", "string-list")])
        | _get_command_settings_static_info(
            "rename", [("old", "string"), ("new", "string")]
        )
        | _get_command_settings_static_info("list", [])
        | _get_command_settings_static_info(
            "list-properties", [("object-name", "string")]
        )
        | _get_command_settings_static_info(
            "make-a-copy", [("from", "string"), ("to", "string")]
        )
    )

    def named_object(commands, creatable=True):
        return {
            "type": "named-object",
            "user_creatable": creatable,
            "object_type": {"type": "group"},
            "commands": deepcopy(commands),
        }

    special_commands = commands | _get_command_settings_static_info("display", [])
    variant_commands = commands | _get_command_settings_static_info(
        "create", [("name", "string"), ("volume", "string")]
    )
    non_prefix_commands = _get_command_settings_static_info("display", []) | commands
    hidden_commands = deepcopy(commands)
    hidden_commands["make-a-copy"]["api_exposure_level"] = "beta"
    static_info = {
        "type": "group",
        "children": {
            "first": named_object(commands),
            "second": named_object(special_commands),
            "variant": named_object(variant_commands),
            "fixed": named_object(commands, creatable=False),
            "non-prefix": named_object(non_prefix_commands),
            "hidden": named_object(hidden_commands),
        },
    }
    static_info["children"]["non-prefix"]["children"] = {"detail": {"type": "string"}}
    static_info["children"]["non-prefix"]["queries"] = _get_query_settings_static_info(
        "status", []
    )
    dynamic_root, _ = flobject.get_cls("", deepcopy(static_info), version=version)
    settingsgen.generate(version, {StaticInfoType.SETTINGS: deepcopy(static_info)})
    directory = tmp_path / f"v{version}" / "solver"
    source = (directory / "settings.py").read_text(encoding="utf-8")
    stub = (directory / "settings.pyi").read_text(encoding="utf-8")
    ast.parse(source)
    ast.parse(stub)
    spec = importlib.util.spec_from_file_location(
        "test_generated_settings", directory / "settings.py"
    )
    generated = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(generated)

    first = generated.root._child_classes["first"]
    second = generated.root._child_classes["second"]
    variant = generated.root._child_classes["variant"]
    fixed = generated.root._child_classes["fixed"]
    assert first.__bases__[0] is second.__bases__[0]
    assert variant.__bases__[0] is not first.__bases__[0]
    assert fixed.__bases__[0] is not first.__bases__[0]
    for root_cls in (dynamic_root, generated.root):
        for container_name in ("first", "second", "fixed", "variant"):
            container = root_cls._child_classes[container_name]
            command_base = container.__bases__[0]
            assert issubclass(command_base, flobject._NamedObjectCommandBase)
            for name in command_base.command_names:
                assert name not in vars(container)
                assert vars(command_base)[name] is container._child_classes[name]
        assert "create" not in vars(root_cls._child_classes["fixed"].__bases__[0])
    class_node = next(
        node
        for node in ast.parse(source).body
        if isinstance(node, ast.ClassDef) and node.name == first.__name__
    )
    assigned = {
        target.id
        for node in class_node.body
        if isinstance(node, ast.Assign)
        for target in node.targets
        if isinstance(target, ast.Name)
    }
    assert "command_names" not in assigned
    assert "_child_classes" not in assigned
    assert first.command_names is not second.command_names
    assert first._child_classes is not second._child_classes
    subclass = type("subclass", (first,), {})
    assert subclass.command_names is first.command_names
    assert subclass._child_classes is first._child_classes
    assert "display" in vars(second)["_child_classes"]
    assert "create" not in fixed.command_names
    create_name = next(
        name
        for name in variant.command_names
        if variant._child_classes[name].fluent_name == "create"
    )
    assert variant._child_classes[create_name].argument_names == ["name", "volume"]
    non_prefix = generated.root._child_classes["non_prefix"]
    assert non_prefix.__bases__[0] is first.__bases__[0]
    assert non_prefix.command_names[0] == "display"
    assert list(non_prefix._child_classes) == [
        "detail",
        *non_prefix.command_names,
        "status",
    ]

    for root_cls in (dynamic_root, generated.root):
        root = root_cls()
        proxy = mocker.Mock()
        proxy.get_attrs.return_value = {}
        proxy.get_object_names.return_value = []
        proxy.execute_cmd.return_value = None
        proxy.is_interactive_mode.return_value = False
        root.set_flproxy(proxy)
        obj = root.second
        assert obj.command_names == list(obj._child_classes)
        assert obj.get_active_command_names() == obj.command_names
        if version == "242":
            assert obj.create("created").obj_name == "created"
            proxy.create.assert_called_with("second", "created")
        else:
            obj.create("created")
            proxy.execute_cmd.assert_called_with("second", "create", name="created")
        obj.rename("old-name", "new-name")
        proxy.execute_cmd.assert_called_with(
            "second", "rename", old="old-name", new="new-name"
        )
        obj.display()
        proxy.execute_cmd.assert_called_with("second", "display")
        obj.delete(["old-name"])
        proxy.execute_cmd.assert_called_with(
            "second", "delete", **{"name-list": ["old-name"]}
        )
        obj.list()
        proxy.execute_cmd.assert_called_with("second", "list")
        obj.list_properties(object_name="old-name")
        proxy.execute_cmd.assert_called_with(
            "second", "list-properties", **{"object-name": "old-name"}
        )
        obj.make_a_copy(from_="old-name", to="new-name")
        proxy.execute_cmd.assert_called_with(
            "second", "make-a-copy", **{"from": "old-name", "to": "new-name"}
        )
        assert "make_a_copy" not in root.hidden.get_active_command_names()
        with pytest.raises(AttributeError):
            root.hidden.make_a_copy

    if version == "251":
        monkeypatch.syspath_prepend(str(Path(__file__).parents[1] / "doc"))
        settings_rstgen = importlib.import_module("settings_rstgen")
        monkeypatch.setattr(settings_rstgen, "rst_list", [])
        monkeypatch.setattr(settings_rstgen, "parents_dict", {})
        rst_dir = tmp_path / "rst"
        rst_dir.mkdir()
        settings_rstgen._populate_parents_list(generated.root)
        settings_rstgen._populate_rst_from_settings(rst_dir, generated.root, version)
        container_page = (rst_dir / f"{second.__name__}.rst").read_text()
        base_page = (rst_dir / f"{second.__bases__[0].__name__}.rst").read_text()
        assert ":show-inheritance:" in container_page
        assert ".. rubric:: Base class" not in container_page
        assert ":ref:`display <" in container_page
        assert ":ref:`create <" not in container_page
        assert ":ref:`delete <" not in container_page
        assert ":ref:`create <" in base_page
        assert ":ref:`delete <" in base_page
        assert ":ref:`display <" not in base_page


def test_named_object_command_base_rendered_docs(monkeypatch, tmp_path):
    sphinx = pytest.importorskip("sphinx.application")
    monkeypatch.setattr(pyfluent.config, "codegen_outdir", tmp_path)
    monkeypatch.syspath_prepend(str(Path(__file__).parents[1] / "doc"))
    settings_rstgen = importlib.import_module("settings_rstgen")
    monkeypatch.setattr(settings_rstgen, "rst_list", [])
    monkeypatch.setattr(settings_rstgen, "parents_dict", {})
    commands = (
        _get_command_settings_static_info("create", [("name", "string")])
        | _get_command_settings_static_info("delete", [("name", "string")])
        | _get_command_settings_static_info("display", [])
    )
    info = {
        "type": "group",
        "children": {
            "container": {
                "type": "named-object",
                "user_creatable": True,
                "object_type": {"type": "group"},
                "commands": commands,
            }
        },
    }
    settingsgen.generate("271", {StaticInfoType.SETTINGS: info})
    module_name = "ansys.fluent.core.generated.v271.solver.settings"
    parent = pyfluent
    for package_name in (
        "ansys.fluent.core.generated",
        "ansys.fluent.core.generated.v271",
        "ansys.fluent.core.generated.v271.solver",
    ):
        package = types.ModuleType(package_name)
        package.__path__ = []
        monkeypatch.setitem(sys.modules, package_name, package)
        monkeypatch.setattr(
            parent, package_name.rsplit(".", 1)[-1], package, raising=False
        )
        parent = package
    spec = importlib.util.spec_from_file_location(
        module_name, tmp_path / "v271" / "solver" / "settings.py"
    )
    generated = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, module_name, generated)
    monkeypatch.setattr(parent, "settings", generated, raising=False)
    spec.loader.exec_module(generated)
    container = generated.root._child_classes["container"]
    child_type = container.child_object_type
    child_type.__name__ = "container_1_item"
    generated.container_1_item = child_type
    source = tmp_path / "docs"
    source.mkdir()
    settings_rstgen._populate_parents_list(generated.root)
    settings_rstgen._populate_rst_from_settings(source, generated.root, "271")
    container_rst = (source / f"{container.__name__}.rst").read_text()
    assert (
        "organised like a Python dictionary holding objects of type "
        ":ref:`container_item <container_1_item>` by name."
    ) in container_rst
    (source / "conf.py").write_text(
        "extensions = ['sphinx.ext.autodoc']\nmaster_doc = 'index'\n",
        encoding="utf-8",
    )
    pages = sorted(path.stem for path in source.glob("*.rst"))
    (source / "index.rst").write_text(
        "Test\n====\n\n.. toctree::\n\n" + "".join(f"   {page}\n" for page in pages),
        encoding="utf-8",
    )
    warnings = StringIO()
    app = sphinx.Sphinx(
        str(source),
        str(source),
        str(tmp_path / "html"),
        str(tmp_path / "doctrees"),
        "html",
        status=StringIO(),
        warning=warnings,
        warningiserror=True,
        freshenv=True,
    )
    app.connect("autodoc-process-bases", settings_rstgen._process_autodoc_bases)
    app.build()
    assert app.statuscode == 0, warnings.getvalue()
    base = container.__bases__[0]
    container_html = (tmp_path / "html" / f"{container.__name__}.html").read_text(
        encoding="utf-8"
    )
    base_html = (tmp_path / "html" / f"{base.__name__}.html").read_text(
        encoding="utf-8"
    )
    container_html = container_html.split('role="main">', 1)[1].split("</section>", 1)[
        0
    ]
    base_html = base_html.split('role="main">', 1)[1].split("</section>", 1)[0]
    bases_line = container_html.split("Bases:", 1)[1].split("</p>", 1)[0]
    assert '<span class="pre">NamedObject</span>' in bases_line
    assert '<span class="pre">CreatableNamedObjectMixin</span>' in bases_line
    assert '<span class="pre">container_item</span>' in bases_line
    assert '<span class="pre">container_1_item</span>' not in bases_line
    assert "container_1_item.html" in bases_line
    assert "display.html" in container_html
    assert "create.html" not in container_html
    assert "delete.html" not in container_html
    assert "create.html" in base_html
    assert "delete.html" in base_html


def test_process_autodoc_bases_uses_short_names(monkeypatch):
    monkeypatch.syspath_prepend(str(Path(__file__).parents[1] / "doc"))
    settings_rstgen = importlib.import_module("settings_rstgen")
    item_type = TypeVar("item_type")

    class Item:
        _python_name = "named_item"

    class NamedObject(Generic[item_type]):
        pass

    class Container:
        child_object_type = Item

    bases = [NamedObject[Item]]
    settings_rstgen._process_autodoc_bases(None, "", Container, None, bases)

    assert bases == [
        f":py:class:`NamedObject <{NamedObject.__module__}.{NamedObject.__qualname__}>`\\ "
        f"[:py:class:`named_item <{Item.__module__}.{Item.__name__}>`\\ ]"
    ]


def test_settings_codegen_argument_docs_use_callable_names(monkeypatch, tmp_path):
    from ansys.fluent.core.solver import flobject

    monkeypatch.setattr(pyfluent.config, "codegen_outdir", tmp_path)
    monkeypatch.setattr(flobject, "_bases_by_class", {})
    static_info = {
        "type": "group",
        "commands": {
            "write-case": {
                "type": "command",
                "help": "Write a case.",
                "arguments": {"file-name": {"type": "file", "file_purpose": "output"}},
            },
            "read-case": {
                "type": "command",
                "help": "Read a case.",
                "arguments": {
                    "file-name": {"type": "file", "file_purpose": "input"},
                    "part-2": {"type": "string"},
                },
            },
        },
    }

    settingsgen.generate("271", {StaticInfoType.SETTINGS: static_info})
    path = tmp_path / "v271" / "solver" / "settings.py"
    module = pyfluent.utils.load_module("test_settings_argument_docs", path)
    command = module.root._child_classes["read_case"]

    assert command.argument_names == ["file_name", "part_2"]
    assert command._child_classes["file_name"].__name__ != "file_name"
    assert "    file_name : str\n" in command.__doc__
    assert "    file_name_1 : str\n" not in command.__doc__
    assert "    part_2 : str\n" in command.__doc__
    help_text = pydoc.render_doc(command, renderer=pydoc.plaintext)
    assert "file_name : str" in help_text
    assert "file_name_1 : str" not in help_text


_settings_static_info_duplicate_parameters = {
    "children": (
        _get_group_settings_static_info(
            "G1",
            (
                (
                    _get_group_settings_static_info(
                        "G2",
                        _get_parameter_settings_static_info("P1", "string"),
                        {},
                        {},
                    )
                )
                | _get_parameter_settings_static_info("P1", "string")
            ),
            {},
            {},
        )
    ),
    "commands": {},
    "queries": {},
    "type": "group",
}

_settings_static_info_different_parameters_with_same_name = {
    "children": (
        _get_group_settings_static_info(
            "G1",
            (
                (
                    _get_group_settings_static_info(
                        "G2",
                        _get_parameter_settings_static_info("P1", "real"),
                        {},
                        {},
                    )
                )
                | _get_parameter_settings_static_info("P1", "string")
            ),
            {},
            {},
        )
    ),
    "commands": {},
    "queries": {},
    "type": "group",
}


_settings_static_info_combined_case = {
    "children": (
        _get_group_settings_static_info(
            "G1",
            (
                (
                    _get_group_settings_static_info(
                        "G2",
                        (
                            _get_parameter_settings_static_info("P1", "real")
                            | _get_parameter_settings_static_info("P2", "string")
                        ),
                        {},
                        {},
                    )
                )
                | _get_parameter_settings_static_info("P1", "string")
                | _get_parameter_settings_static_info("P2", "string")
            ),
            {},
            {},
        )
    ),
    "commands": {},
    "queries": {},
    "type": "group",
}


@pytest.mark.parametrize(
    "settings_static_info,class_names",
    [
        (_settings_static_info_duplicate_parameters, ["P1", "G2", "G1", "root"]),
        (
            _settings_static_info_different_parameters_with_same_name,
            ["P1_1", "G2", "P1", "G1", "root"],
        ),
        (_settings_static_info_combined_case, ["P1_1", "P2", "G2", "P1", "G1", "root"]),
    ],
)
def test_codegen_with_settings_static_info_edge_cases(
    monkeypatch, settings_static_info, class_names
):

    codegen_outdir = Path(tempfile.mkdtemp())
    monkeypatch.setattr(pyfluent.config, "codegen_outdir", codegen_outdir)
    version = "251"
    static_infos = {}
    static_infos[StaticInfoType.SETTINGS] = settings_static_info
    allapigen.generate(version, static_infos)
    with open(codegen_outdir / f"v{version}" / "solver" / "settings.py", "r") as f:
        module_def = ast.parse(f.read())
        class_names_from_file = [
            x.name for x in module_def.body if isinstance(x, ast.ClassDef)
        ]
        # The order of classes is important.
        assert class_names_from_file == class_names
    shutil.rmtree(str(codegen_outdir))
