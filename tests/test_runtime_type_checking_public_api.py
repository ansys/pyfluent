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

"""Audit that PyFluent's public API is really enforced by ``beartype``.

``beartype.claw`` never fails an import when it cannot decorate a function: it only
emits a ``BeartypeClawDecorWarning`` and leaves the function unchecked. Import-only
tests therefore cannot detect silently unchecked public APIs. This audit runs in a
fresh interpreter with ``beartype_package("ansys.fluent.core")`` applied, and:

1. collects every ``BeartypeClawDecorWarning`` raised while importing the package;
2. for every public function/method, verifies that a ``beartype`` wrapper is
   present and that calling it with an object of the wrong type raises a
   ``BeartypeCallHintViolation`` (never a forward-reference error, never silently
   passing);
3. verifies that classes opting out through ``no_runtime_type_check`` are known.

It can also be run directly: ``python tests/test_runtime_type_checking_public_api.py``.
"""

import json
import subprocess
import sys

import pytest

# Classes intentionally excluded from runtime type-checking (dynamic proxying or
# unresolvable generics). Any other class carrying ``__no_type_check__`` is a failure.
ALLOWED_EXEMPT_CLASSES = {
    "ansys.fluent.core.solver.flobject.Base",
    "ansys.fluent.core.solver.flobject.SettingsBase",
    "ansys.fluent.core.solver.flobject.Group",
    "ansys.fluent.core.solver.flobject.NamedObject",
    "ansys.fluent.core.solver.flobject.ListObject",
    "ansys.fluent.core.solver.flobject.Action",
    "ansys.fluent.core.solver.flobject.WildcardPath",
    "ansys.fluent.core.execution.launcher.slurm_launcher.SlurmFuture",
    "ansys.fluent.core.fields.field_data.abstract_field_data.BaseFieldDataSource",
    "ansys.fluent.core.fields.field_data.abstract_field_data.FieldBatch",
    "ansys.fluent.core.fields.field_data.abstract_field_data.AbstractFieldData",
    "ansys.fluent.core.services.abstract_settings.AbstractSettings",
    "ansys.fluent.core.services.settings.BaseSettings",
    "ansys.fluent.core.connectivity.fluent_connection.FluentConnection",
    "ansys.fluent.core.execution.session.session.BaseSession",
    "ansys.fluent.core.meshing.session.base_meshing.BaseMeshing",
    "ansys.fluent.core.solver.session.solver_aero.SolverAero",
    "ansys.fluent.core.solver.session.solver_icing.SolverIcing",
}

# Functions intentionally excluded because their hints name classes that cannot be
# imported at runtime (circular imports). Other flagged functions are failures.
ALLOWED_EXEMPT_FUNCTIONS = {
    "ansys.fluent.core.execution.session.session.BaseSession.from_install",
    "ansys.fluent.core.execution.session.session.BaseSession.from_container",
    "ansys.fluent.core.execution.session.session.BaseSession.from_pim",
    "ansys.fluent.core.execution.launcher.launch_options._get_argvals_and_session",
    "ansys.fluent.core.execution.launcher.launch_options._get_running_session_mode",
    "ansys.fluent.core.solver.session.solver._set_state_safe",
    "ansys.fluent.core.solver.flobject.get_root",
    "ansys.fluent.core.solver.settings_builtin_bases._get_settings_obj",
}

# Functions that accept wrong types. Must stay empty unless a case is justified here.
ALLOWED_NOT_ENFORCED: set[str] = set()

_WORKER = r"""
import importlib, inspect, json, pkgutil, sys, typing, warnings

from beartype import roar
from beartype.claw import beartype_package
from beartype.door import is_bearable

ROOT = "ansys.fluent.core"
beartype_package(ROOT)

class _Wrong:
    pass

WRONG = _Wrong()
out = {
    "decor_failures": [], "import_failures": [], "exempt": [], "exempt_functions": [],
    "not_wrapped": [], "unannotated": [], "forward_ref": [], "not_enforced": [],
    "unexpected": [], "unresolvable_hints": [], "checked": 0,
}

def _is_bt(f):
    code = getattr(f, "__code__", None)
    return bool(code and code.co_filename.startswith("<@beartype"))

def _layer(f):
    for _ in range(20):
        if f is None:
            return None
        if _is_bt(f):
            return f
        f = getattr(f, "__wrapped__", None)
    return None

with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    import ansys.fluent.core as pf
    modules = []
    all_modules = []
    for info in pkgutil.walk_packages(pf.__path__, ROOT + "."):
        parts = info.name.split(".")[3:]
        if any(p in ("generated", "ui", "codegen") for p in parts):
            continue
        try:
            module = importlib.import_module(info.name)
        except BaseException as exc:
            out["import_failures"].append(f"{info.name}: {type(exc).__name__}: {str(exc)[:120]}")
            continue
        all_modules.append(module)
        if not any(p.startswith("_") for p in parts):
            modules.append(module)

seen = set()
for w in caught:
    if type(w.message).__name__ == "BeartypeClawDecorWarning":
        text = str(w.message)
        head = text.split(" in file")[0].split(" not decoratable")[0].strip()
        cause = [l.strip() for l in text.splitlines() if l.strip().startswith(("TypeError", "AttributeError", "NameError"))]
        item = head + (" -> " + cause[-1][:140] if cause else "")
        if item not in seen:
            seen.add(item)
            out["decor_failures"].append(item)

def _public_members(mod):
    names = getattr(mod, "__all__", None) or [n for n in vars(mod) if not n.startswith("_")]
    for name in names:
        obj = getattr(mod, name, None)
        if getattr(obj, "__module__", None) == mod.__name__:
            yield name, obj

def _targets(mod):
    for name, obj in _public_members(mod):
        qual = f"{mod.__name__}.{name}"
        if inspect.isfunction(obj):
            yield qual, obj, None
        elif inspect.isclass(obj):
            if obj.__dict__.get("__no_type_check__"):
                out["exempt"].append(qual)
                continue
            for mname, member in list(obj.__dict__.items()):
                if mname.startswith("_") and mname != "__init__":
                    continue
                if isinstance(member, (staticmethod, classmethod)):
                    member = member.__func__
                if inspect.isfunction(member) and member.__qualname__.startswith(
                    obj.__qualname__ + "."
                ):
                    yield f"{qual}.{mname}", member, obj

for mod in modules:
    for qual, func, owner in _targets(mod):
        out["checked"] += 1
        if getattr(func, "__no_type_check__", False) is True:
            out["exempt_functions"].append(qual)
            continue
        layer = _layer(func)
        original = inspect.unwrap(func)
        sig = inspect.signature(original)
        params = [
            p for p in sig.parameters.values()
            if p.name not in ("self", "cls") and p.kind not in (p.VAR_POSITIONAL, p.VAR_KEYWORD)
        ]
        annotated = [p for p in params if p.annotation is not p.empty]
        if params and not annotated:
            out["unannotated"].append(qual)
            continue
        if not annotated:
            continue
        try:
            hints = typing.get_type_hints(original, include_extras=True)
            accepts_anything = all(
                is_bearable(WRONG, hints[p.name]) for p in annotated if p.name in hints
            )
        except Exception:
            accepts_anything = False  # unresolvable hints: the call below surfaces it.
        if accepts_anything:
            continue  # every hint accepts anything; nothing to enforce.
        if layer is None:
            out["not_wrapped"].append(qual)
            continue
        args, kwargs = [], {}
        for p in sig.parameters.values():
            if p.kind in (p.VAR_POSITIONAL, p.VAR_KEYWORD):
                continue
            if p.name in ("self", "cls"):
                args.append(owner if p.name == "cls" else WRONG)
            elif p.kind == p.POSITIONAL_ONLY:
                args.append(WRONG)
            else:
                kwargs[p.name] = WRONG
        try:
            result = layer(*args, **kwargs)
            # Generator functions (incl. @contextmanager) are only checked once started.
            if inspect.isgenerator(result):
                next(result)
            elif hasattr(result, "__enter__") and hasattr(result, "__exit__"):
                result.__enter__()
            out["not_enforced"].append(qual)
        except roar.BeartypeCallHintForwardRefException as exc:
            out["forward_ref"].append(f"{qual}: {str(exc).splitlines()[0][:160]}")
        except roar.BeartypeCallHintViolation:
            pass
        except BaseException as exc:
            out["unexpected"].append(f"{qual}: {type(exc).__name__}: {str(exc)[:120]}")

def _all_functions(mod):
    for name, obj in list(vars(mod).items()):
        if getattr(obj, "__module__", None) != mod.__name__:
            continue
        qual = f"{mod.__name__}.{name}"
        if inspect.isfunction(obj):
            yield qual, obj
        elif inspect.isclass(obj) and not obj.__dict__.get("__no_type_check__"):
            for mname, member in list(vars(obj).items()):
                if isinstance(member, (staticmethod, classmethod)):
                    member = member.__func__
                if inspect.isfunction(member):
                    yield f"{qual}.{mname}", member

# Private helpers are called by public APIs, so their hints must resolve too.
for mod in all_modules:
    for qual, func in _all_functions(mod):
        if getattr(func, "__no_type_check__", False) is True or _layer(func) is None:
            continue
        try:
            typing.get_type_hints(inspect.unwrap(func), include_extras=True)
        except Exception as exc:
            out["unresolvable_hints"].append(f"{qual}: {type(exc).__name__}: {str(exc)[:100]}")

print("__AUDIT__" + json.dumps(out))
"""


def _run_audit() -> dict:
    result = subprocess.run(
        [sys.executable, "-c", _WORKER],
        capture_output=True,
        text=True,
        check=False,
    )
    for line in reversed(result.stdout.splitlines()):
        if line.startswith("__AUDIT__"):
            return json.loads(line[len("__AUDIT__") :])
    raise RuntimeError(
        f"Audit crashed:\n{result.stdout[-2000:]}\n{result.stderr[-4000:]}"
    )


@pytest.fixture(scope="module")
def audit() -> dict:
    pytest.importorskip("beartype")
    return _run_audit()


def _fail_if(items, message):
    if items:
        listing = "\n  ".join(sorted(items))
        pytest.fail(f"{message} ({len(items)}):\n  {listing}", pytrace=False)


def test_audit_covers_public_api(audit):
    """Guard against the audit silently checking nothing."""
    assert audit["checked"] > 500
    assert not audit["import_failures"], audit["import_failures"]


def test_no_beartype_decoration_failures(audit):
    """``beartype.claw`` must be able to decorate every function in the package."""
    _fail_if(
        audit["decor_failures"],
        "beartype could not decorate these callables (they are silently unchecked)",
    )


def test_public_api_is_wrapped_by_beartype(audit):
    """Public callables with annotations must carry a beartype wrapper."""
    _fail_if(
        audit["not_wrapped"], "Annotated public callables without a beartype wrapper"
    )


def test_public_api_rejects_wrong_types(audit):
    """Calling a public callable with a wrong-typed argument must raise."""
    _fail_if(
        set(audit["not_enforced"]) - ALLOWED_NOT_ENFORCED,
        "Public callables that accepted a wrong-typed argument",
    )
    _fail_if(
        audit["forward_ref"], "Public callables with unresolvable hints at call time"
    )
    _fail_if(audit["unexpected"], "Public callables raising a non-beartype error")


@pytest.mark.xfail(
    reason="Static type hints are tracked separately from runtime checking.",
    strict=False,
)
def test_public_api_parameters_are_annotated(audit):
    """Public callables taking parameters must annotate at least one of them."""
    _fail_if(audit["unannotated"], "Public callables with no parameter annotations")


def test_only_known_classes_opt_out(audit):
    """Only allow-listed classes may use ``no_runtime_type_check``."""
    _fail_if(
        set(audit["exempt"]) - ALLOWED_EXEMPT_CLASSES,
        "Classes opting out of runtime type-checking without being allow-listed",
    )


def test_only_known_functions_opt_out(audit):
    """Only allow-listed functions may use ``no_runtime_type_check``."""
    _fail_if(
        set(audit["exempt_functions"]) - ALLOWED_EXEMPT_FUNCTIONS,
        "Functions opting out of runtime type-checking without being allow-listed",
    )


def test_all_hints_resolve_at_runtime(audit):
    """Hints of every checked function, private ones included, must be resolvable."""
    _fail_if(
        audit["unresolvable_hints"],
        "Functions whose hints cannot be resolved at runtime",
    )


def test_using_context_manager_type_enforcement():
    """``using()`` is a generator context manager: its hints are checked on ``__enter__``."""
    pytest.importorskip("beartype")

    source = """
from beartype import roar
from beartype.claw import beartype_package

beartype_package('ansys.fluent.core')

from ansys.fluent.core.execution.session.session import using

try:
    with using(123):
        print('FAIL:no-raise')
except roar.BeartypeCallHintViolation:
    print('PASS')
"""
    result = subprocess.run(
        [sys.executable, "-W", "ignore", "-c", source],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.stdout.strip() == "PASS", (result.stdout, result.stderr[-2000:])


if __name__ == "__main__":
    report = _run_audit()
    failed = False
    for key, values in report.items():
        if key == "checked":
            print(f"checked callables: {values}")
            continue
        print(f"\n== {key}: {len(values)}")
        for value in sorted(values):
            print(f"   {value}")
        failed = failed or (key not in ("exempt", "exempt_functions") and bool(values))
    sys.exit(1 if failed else 0)
