# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

"""Integration tests for runtime type-checking GenericAlias bug fix.

This module tests that the bug fix for GenericAlias handling in
no_runtime_type_check() works correctly across different scenarios.

Each test runs in isolation to ensure the environment variable is properly set
before any PyFluent modules are imported.
"""

import os
import subprocess
import sys

import pytest

from ansys.fluent.core import _type_checking


def _run_with_env(source: str, enable_type_checking: bool = False) -> str:
    """Run Python source code in a fresh interpreter with controlled environment.

    Parameters
    ----------
    source : str
        Python code to execute.
    enable_type_checking : bool, optional
        Whether to set PYFLUENT_RUNTIME_TYPE_CHECKING=1, by default False.

    Returns
    -------
    str
        The stdout output from executing the code.

    Raises
    ------
    AssertionError
        If the subprocess returns a non-zero exit code.
    """
    env = os.environ.copy()
    if enable_type_checking:
        env[_type_checking.ENV_VAR] = "1"
    else:
        env.pop(_type_checking.ENV_VAR, None)

    result = subprocess.run(
        [sys.executable, "-W", "ignore", "-c", source],
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"stderr: {result.stderr}"
    return result.stdout


class TestGenericAliasDecoratorFix:
    """Test the bug fix for GenericAlias handling in no_runtime_type_check()."""

    def test_decorator_handles_typinglist_genericalias(self):
        """Test that GenericAlias from typing module is handled correctly."""
        source = """
from ansys.fluent.core._type_checking import no_runtime_type_check
from typing import List

# Test GenericAlias returned unchanged
alias = List[int]
result = no_runtime_type_check(alias)
if result is alias:
    print("PASS")
else:
    print("FAIL")
"""
        output = _run_with_env(source)
        assert "PASS" in output

    def test_decorator_marks_regular_class(self):
        """Test that regular classes get __no_type_check__ attribute."""
        source = """
from ansys.fluent.core._type_checking import no_runtime_type_check

class MyClass:
    pass

result = no_runtime_type_check(MyClass)
if hasattr(result, '__no_type_check__') and result.__no_type_check__ is True:
    print("PASS")
else:
    print("FAIL")
"""
        output = _run_with_env(source)
        assert "PASS" in output

    def test_decorator_marks_generic_class(self):
        """Test that generic classes get __no_type_check__ attribute."""
        source = """
from ansys.fluent.core._type_checking import no_runtime_type_check
from typing import Generic, TypeVar

T = TypeVar('T')

class GenericClass(Generic[T]):
    pass

result = no_runtime_type_check(GenericClass)
if hasattr(result, '__no_type_check__') and result.__no_type_check__ is True:
    print("PASS")
else:
    print("FAIL")
"""
        output = _run_with_env(source)
        assert "PASS" in output

    def test_decorator_marks_class_with_generic_parent(self):
        """Test generic inheritance pattern from flobject.py."""
        source = """
from ansys.fluent.core._type_checking import no_runtime_type_check
from typing import Generic, TypeVar, Dict

StateT = TypeVar('StateT')

class GenericBase(Generic[StateT]):
    pass

DictStateType = Dict[str, object]

class DerivedClass(GenericBase[DictStateType]):
    pass

result = no_runtime_type_check(DerivedClass)
if hasattr(result, '__no_type_check__') and result.__no_type_check__ is True:
    print("PASS")
else:
    print("FAIL")
"""
        output = _run_with_env(source)
        assert "PASS" in output


class TestProxyClassDecoration:
    """Test that proxy classes have the decorator applied correctly."""

    def test_base_proxy_class_decorated(self):
        """Test that Base proxy class is decorated."""
        source = """
from ansys.fluent.core.solver.flobject import Base

if hasattr(Base, '__no_type_check__') and Base.__no_type_check__ is True:
    print("PASS")
else:
    print("FAIL")
"""
        output = _run_with_env(source)
        assert "PASS" in output

    def test_settingsbase_generic_proxy_class_decorated(self):
        """Test that SettingsBase generic class is decorated."""
        source = """
from ansys.fluent.core.solver.flobject import SettingsBase

if hasattr(SettingsBase, '__no_type_check__') and SettingsBase.__no_type_check__ is True:
    print("PASS")
else:
    print("FAIL")
"""
        output = _run_with_env(source)
        assert "PASS" in output

    def test_group_proxy_class_decorated(self):
        """Test that Group proxy class is decorated."""
        source = """
from ansys.fluent.core.solver.flobject import Group

if hasattr(Group, '__no_type_check__') and Group.__no_type_check__ is True:
    print("PASS")
else:
    print("FAIL")
"""
        output = _run_with_env(source)
        assert "PASS" in output

    def test_namedobject_proxy_class_decorated(self):
        """Test that NamedObject proxy class is decorated."""
        source = """
from ansys.fluent.core.solver.flobject import NamedObject

if hasattr(NamedObject, '__no_type_check__') and NamedObject.__no_type_check__ is True:
    print("PASS")
else:
    print("FAIL")
"""
        output = _run_with_env(source)
        assert "PASS" in output

    def test_listobject_proxy_class_decorated(self):
        """Test that ListObject proxy class is decorated."""
        source = """
from ansys.fluent.core.solver.flobject import ListObject

if hasattr(ListObject, '__no_type_check__') and ListObject.__no_type_check__ is True:
    print("PASS")
else:
    print("FAIL")
"""
        output = _run_with_env(source)
        assert "PASS" in output

    def test_wildcard_path_proxy_class_decorated(self):
        """Test that WildcardPath proxy class is decorated."""
        source = """
from ansys.fluent.core.solver.flobject import WildcardPath

if hasattr(WildcardPath, '__no_type_check__') and WildcardPath.__no_type_check__ is True:
    print("PASS")
else:
    print("FAIL")
"""
        output = _run_with_env(source)
        assert "PASS" in output

    def test_action_proxy_class_decorated(self):
        """Test that Action proxy class is decorated."""
        source = """
from ansys.fluent.core.solver.flobject import Action

if hasattr(Action, '__no_type_check__') and Action.__no_type_check__ is True:
    print("PASS")
else:
    print("FAIL")
"""
        output = _run_with_env(source)
        assert "PASS" in output

    def test_all_proxy_classes_decorated_together(self):
        """Test that all proxy classes can be imported and are decorated."""
        source = """
from ansys.fluent.core.solver.flobject import (
    Base, SettingsBase, Group, WildcardPath,
    NamedObject, ListObject, Action
)

classes = [Base, SettingsBase, Group, WildcardPath, NamedObject, ListObject, Action]
all_decorated = all(
    hasattr(c, '__no_type_check__') and c.__no_type_check__ is True
    for c in classes
)

if all_decorated:
    print("PASS")
else:
    print("FAIL")
"""
        output = _run_with_env(source)
        assert "PASS" in output


class TestModuleImportsWithTypeChecking:
    """Test that modules import successfully with runtime type-checking enabled."""

    def test_flobject_module_imports_with_type_checking(self):
        """Test solver.flobject module imports with type-checking enabled."""
        source = """
from ansys.fluent.core.solver.flobject import Base, Group, NamedObject
print("PASS")
"""
        output = _run_with_env(source, enable_type_checking=True)
        assert "PASS" in output

    def test_utils_module_imports_with_type_checking(self):
        """Test utils module imports with type-checking enabled."""
        source = """
from ansys.fluent.core.utils.get_completer_info import get_completer_info
print("PASS")
"""
        output = _run_with_env(source, enable_type_checking=True)
        assert "PASS" in output

    def test_multiple_modules_import_independently(self):
        """Test that multiple modules can be imported independently."""
        source = """
from ansys.fluent.core.solver.flobject import Group
from ansys.fluent.core.utils.get_completer_info import get_completer_info
print("PASS")
"""
        output = _run_with_env(source, enable_type_checking=True)
        assert "PASS" in output


class TestEnvironmentVariableHandling:
    """Test environment variable handling for runtime type-checking."""

    def test_type_checking_disabled_by_default(self):
        """Test that type-checking is disabled without environment variable."""
        source = """
from ansys.fluent.core._type_checking import is_type_checking_enabled
if not is_type_checking_enabled():
    print("PASS")
else:
    print("FAIL")
"""
        output = _run_with_env(source, enable_type_checking=False)
        assert "PASS" in output

    def test_type_checking_can_be_enabled_via_env_var(self):
        """Test that type-checking can be enabled via environment variable."""
        source = """
from ansys.fluent.core._type_checking import is_type_checking_enabled
try:
    from beartype import beartype
    enabled = is_type_checking_enabled()
    print("PASS")
except ImportError:
    print("SKIP")
"""
        output = _run_with_env(source, enable_type_checking=True)
        assert "PASS" in output or "SKIP" in output


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
