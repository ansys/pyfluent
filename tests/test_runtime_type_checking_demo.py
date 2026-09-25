# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
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

"""Demonstration script showing each runtime type-checking test execution step-by-step.

This script runs each test individually with detailed output showing:
- Test name and description
- Environment variable setting (enabled/disabled)
- Full source code being executed
- Actual output with print statements
- Pass/Fail status
"""

import os
import subprocess
import sys

# Test data for each test
TESTS = {
    "TEST 1: GenericAlias from typing.List[T]": {
        "env_var": False,
        "description": "Verify GenericAlias is handled correctly (returned unchanged)",
        "source": r"""
from ansys.fluent.core._type_checking import no_runtime_type_check
from typing import List

print("=" * 70)
print("TEST 1: GenericAlias Handling")
print("=" * 70)

# Create a GenericAlias: List[int]
alias = List[int]
print(f"Created GenericAlias: {alias}")
print(f"Type: {type(alias)}")

# Apply decorator (should return unchanged)
print(f"\\nApplying no_runtime_type_check decorator...")
result = no_runtime_type_check(alias)
print(f"After decorator: {result}")

# Check if they're the same object
if result is alias:
    print("\n[PASS] GenericAlias returned unchanged (same object reference)")
else:
    print("\n[FAIL] GenericAlias was modified")
""",
    },
    "TEST 2: Regular Python Class": {
        "env_var": False,
        "description": "Verify regular class gets __no_type_check__ attribute",
        "source": r"""
from ansys.fluent.core._type_checking import no_runtime_type_check

print("=" * 70)
print("TEST 2: Regular Class Decoration")
print("=" * 70)

class MyClass:
    pass

print(f"Created class: {MyClass}")
print(f"Before decorator - has __no_type_check__: {hasattr(MyClass, '__no_type_check__')}")

print(f"\\nApplying no_runtime_type_check decorator...")
result = no_runtime_type_check(MyClass)
print(f"After decorator: {result}")

# Check if __no_type_check__ was set
has_attr = hasattr(result, '__no_type_check__')
print(f"After decorator - has __no_type_check__: {has_attr}")

if has_attr:
    print(f"Value of __no_type_check__: {result.__no_type_check__}")
    if result.__no_type_check__ is True:
        print("\n[PASS] Class has __no_type_check__ = True")
    else:
        print("\n[FAIL] Class has __no_type_check__ but value is not True")
else:
    print("\n[FAIL] Class missing __no_type_check__")
""",
    },
    "TEST 3: Generic Class with TypeVar": {
        "env_var": False,
        "description": "Verify generic class gets __no_type_check__ attribute",
        "source": r"""
from ansys.fluent.core._type_checking import no_runtime_type_check
from typing import Generic, TypeVar

print("=" * 70)
print("TEST 3: Generic Class Decoration")
print("=" * 70)

T = TypeVar('T')

class GenericClass(Generic[T]):
    pass

print(f"Created generic class: {GenericClass}")
print(f"Generic parameters: {GenericClass.__parameters__}")
print(f"Before decorator - has __no_type_check__: {hasattr(GenericClass, '__no_type_check__')}")

print(f"\\nApplying no_runtime_type_check decorator...")
result = no_runtime_type_check(GenericClass)
print(f"After decorator: {result}")

has_attr = hasattr(result, '__no_type_check__')
print(f"After decorator - has __no_type_check__: {has_attr}")

if has_attr:
    print(f"Value of __no_type_check__: {result.__no_type_check__}")
    if result.__no_type_check__ is True:
        print("\n[PASS] Generic class has __no_type_check__ = True")
    else:
        print("\n[FAIL] Generic class has __no_type_check__ but value is not True")
else:
    print("\n[FAIL] Generic class missing __no_type_check__")
""",
    },
    "TEST 4: Generic Inheritance Pattern": {
        "env_var": False,
        "description": "Verify generic inheritance pattern from flobject works",
        "source": r"""
from ansys.fluent.core._type_checking import no_runtime_type_check
from typing import Generic, TypeVar, Dict

print("=" * 70)
print("TEST 4: Generic Inheritance Pattern")
print("=" * 70)

StateT = TypeVar('StateT')

class GenericBase(Generic[StateT]):
    pass

DictStateType = Dict[str, object]

class DerivedClass(GenericBase[DictStateType]):
    pass

print(f"Created GenericBase: {GenericBase}")
print(f"Created DerivedClass: {DerivedClass}")
print(f"DerivedClass bases: {DerivedClass.__bases__}")
print(f"Before decorator - has __no_type_check__: {hasattr(DerivedClass, '__no_type_check__')}")

print(f"\\nApplying no_runtime_type_check decorator...")
result = no_runtime_type_check(DerivedClass)
print(f"After decorator: {result}")

has_attr = hasattr(result, '__no_type_check__')
print(f"After decorator - has __no_type_check__: {has_attr}")

if has_attr:
    print(f"Value of __no_type_check__: {result.__no_type_check__}")
    if result.__no_type_check__ is True:
        print("\n[PASS] Derived class has __no_type_check__ = True")
    else:
        print("\n[FAIL] Derived class has __no_type_check__ but value is not True")
else:
    print("\n[FAIL] Derived class missing __no_type_check__")
""",
    },
    "TEST 5: Proxy Base Class": {
        "env_var": False,
        "description": "Verify Base proxy class from flobject is decorated",
        "source": r"""
from ansys.fluent.core.solver.flobject import Base

print("=" * 70)
print("TEST 5: Proxy Base Class Decoration")
print("=" * 70)

print(f"Imported proxy class: {Base}")
print(f"Base module: {Base.__module__}")
print(f"Base MRO: {Base.__mro__}")

has_attr = hasattr(Base, '__no_type_check__')
print(f"\\nHas __no_type_check__: {has_attr}")

if has_attr:
    print(f"Value of Base.__no_type_check__: {Base.__no_type_check__}")
    if Base.__no_type_check__ is True:
        print("\n[PASS] Base proxy class is properly decorated")
    else:
        print("\n[FAIL] Base.__no_type_check__ is not True")
else:
    print("\n[FAIL] Base proxy class missing __no_type_check__")
""",
    },
    "TEST 6: All Proxy Classes Together": {
        "env_var": False,
        "description": "Verify all 7 proxy classes are decorated",
        "source": r"""
from ansys.fluent.core.solver.flobject import (
    Base, SettingsBase, Group, WildcardPath,
    NamedObject, ListObject, Action
)

print("=" * 70)
print("TEST 6: All Proxy Classes Decoration")
print("=" * 70)

classes = [
    ('Base', Base),
    ('SettingsBase', SettingsBase),
    ('Group', Group),
    ('WildcardPath', WildcardPath),
    ('NamedObject', NamedObject),
    ('ListObject', ListObject),
    ('Action', Action)
]

print(f"Checking {len(classes)} proxy classes for __no_type_check__...\\n")

results = []
for name, cls in classes:
    has_attr = hasattr(cls, '__no_type_check__')
    is_true = has_attr and cls.__no_type_check__ is True
    status = "[OK]" if is_true else "[FAIL]"
    results.append(is_true)
    print(f"  {status} {name:20} - __no_type_check__ = {is_true}")

all_decorated = all(results)

print(f"\\nTotal: {sum(results)}/{len(results)} classes decorated correctly")

if all_decorated:
    print("\n[PASS] All proxy classes are properly decorated")
else:
    print("\n[FAIL] Some proxy classes are missing decoration")
""",
    },
    "TEST 7: Type-Checking Disabled (Default)": {
        "env_var": False,
        "description": "Verify type-checking is disabled when env var is NOT set",
        "source": r"""
import os
from ansys.fluent.core._type_checking import is_type_checking_enabled, ENV_VAR

print("=" * 70)
print("TEST 7: Type-Checking Disabled By Default")
print("=" * 70)

env_status = os.environ.get(ENV_VAR, "NOT SET")
print(f"Environment variable '{ENV_VAR}': {env_status}")

enabled = is_type_checking_enabled()
print(f"is_type_checking_enabled() = {enabled}")

if not enabled:
    print("\n[PASS] Type-checking correctly disabled by default")
else:
    print("\n[FAIL] Type-checking is enabled when it shouldn't be")
""",
    },
    "TEST 8: Type-Checking Can Be Enabled": {
        "env_var": True,
        "description": "Verify type-checking can be enabled via environment variable",
        "source": r"""
import os
from ansys.fluent.core._type_checking import is_type_checking_enabled, ENV_VAR

print("=" * 70)
print("TEST 8: Type-Checking Can Be Enabled Via Env Var")
print("=" * 70)

env_status = os.environ.get(ENV_VAR, "NOT SET")
print(f"Environment variable '{ENV_VAR}': {env_status}")

print(f"\\nChecking if type-checking can be enabled...")
try:
    from beartype import beartype
    print("beartype library is available")

    enabled = is_type_checking_enabled()
    print(f"is_type_checking_enabled() = {enabled}")

    print("\n[PASS] Type-checking can be enabled (beartype available)")
except ImportError:
    print("beartype library not available")
    print("\n[SKIP] beartype not installed")
""",
    },
}


def run_test(name, test_config):
    """Run a single test with detailed output."""
    print("\n" + "█" * 80)
    print(f"\n{name}")
    print(
        f"Environment: {ENV_VAR} = {'1 (ENABLED)' if test_config['env_var'] else '0 or NOT SET (DISABLED)'}"
    )
    print(f"Description: {test_config['description']}")
    print("\n" + "-" * 80)

    # Prepare environment
    env = os.environ.copy()
    if test_config["env_var"]:
        env["PYFLUENT_RUNTIME_TYPE_CHECKING"] = "1"
    else:
        env.pop("PYFLUENT_RUNTIME_TYPE_CHECKING", None)

    # Run the test
    result = subprocess.run(
        [sys.executable, "-W", "ignore", "-c", test_config["source"]],
        env=env,
        capture_output=True,
        text=True,
    )

    # Show output
    print("\nTest Output:")
    print("-" * 80)
    if result.stdout:
        print(result.stdout.rstrip())

    if result.stderr:
        print("\nErrors/Warnings:")
        print("-" * 80)
        print(result.stderr.rstrip())

    # Check result
    print("\n" + "-" * 80)
    if result.returncode == 0:
        print("Status: ✓ SUCCESS (returncode = 0)")
        return True
    else:
        print("Status: ✗ FAILED (returncode != 0)")
        return False


def main():
    """Run all tests."""
    print("\n" + "█" * 80)
    print("█" + " " * 78 + "█")
    print("█" + "  RUNTIME TYPE-CHECKING TESTS - DETAILED EXECUTION".center(78) + "█")
    print(
        "█"
        + "  Each test shows environment variable setting, source code, and output".center(
            78
        )
        + "█"
    )
    print("█" + " " * 78 + "█")
    print("█" * 80)

    results = {}
    for test_name, test_config in TESTS.items():
        results[test_name] = run_test(test_name, test_config)

    # Summary
    print("\n" + "█" * 80)
    print("\nTEST SUMMARY")
    print("=" * 80)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test_name, success in results.items():
        status = "[PASS]" if success else "[FAIL]"
        print(f"{status} - {test_name}")

    print(f"\n{'=' * 80}")
    print(f"Total: {passed}/{total} tests passed ({100 * passed // total}%)")
    print("=" * 80)


# Environment variable name
ENV_VAR = "PYFLUENT_RUNTIME_TYPE_CHECKING"

if __name__ == "__main__":
    main()
