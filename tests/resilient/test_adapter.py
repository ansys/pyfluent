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

"""Tests for the reusable-framework adapter seam.

Verify that the resilient engine is product-agnostic: it works with the Fluent
adapter and with an arbitrary custom adapter, that adapters are resolved
*per-session* (so one process can drive multiple products concurrently), and that
the engine falls back cleanly to the default adapter.
"""

import pytest

from ansys.fluent.core.resilient.adapter import (
    DEFAULT_ADAPTER,
    ErrorClasses,
    ResilientAdapter,
    adapter_for,
)
from ansys.fluent.core.resilient.attach import enable_resilient_mode
from ansys.fluent.core.resilient.fluent_adapter import FluentAdapter
from tests.resilient._fakes import (
    FakeFileGroup,
    FakeGroup,
    FakeLeaf,
    FakeSession,
    FakeSettings,
)

pytestmark = pytest.mark.resilient


def test_default_adapter_for_bare_session():
    # A session with no attached adapter resolves to the generic default.
    assert adapter_for(object()) is DEFAULT_ADAPTER


def test_fluent_adapter_identity_and_classes():
    a = FluentAdapter()
    assert a.product_name == "fluent"
    assert a.checkpoint_kind == "file"
    assert "iterate" in a.irreversible_leaves
    assert a.governing_model_flags()  # non-empty for Fluent


class _OtherAdapter(ResilientAdapter):
    """A minimal custom product adapter (stands in for e.g. CFX)."""

    product_name = "other"
    path_prefixes = ("root.",)
    checkpoint_kind = "native"
    irreversible_leaves = frozenset({"run"})

    def error_classes(self) -> ErrorClasses:
        return ErrorClasses()

    def restore_native(self, session, steps: int = 1) -> None:  # pragma: no cover
        pass


def _session_with_clamp():
    def reject_high(value):
        if isinstance(value, (int, float)) and value > 1.0:
            raise RuntimeError("Value is not in range")

    leaf = FakeLeaf(0.05, minimum=0.0, maximum=1.0, set_raises=reject_high)
    settings = FakeSettings(file_group=FakeFileGroup(), setup=FakeGroup(ti=leaf))
    return FakeSession(settings=settings)


def test_adapter_is_per_session_two_products_coexist():
    # Two sessions, two different adapters, in one process -- must not interfere.
    fluent_sess = _session_with_clamp()
    other_sess = _session_with_clamp()
    enable_resilient_mode(fluent_sess, adapter=FluentAdapter())
    enable_resilient_mode(other_sess, adapter=_OtherAdapter())

    assert adapter_for(fluent_sess).product_name == "fluent"
    assert adapter_for(other_sess).product_name == "other"

    # Recovery works independently on each session with its own adapter.
    fluent_sess._settings_service.set_var("setup.ti", 5.0)
    other_sess._settings_service.set_var("setup.ti", 5.0)
    assert fluent_sess.settings.setup.ti.get_state() == 1.0
    assert other_sess.settings.setup.ti.get_state() == 1.0


def test_custom_adapter_prefixes_and_irreversible():
    a = _OtherAdapter()
    assert a.is_irreversible("root.solution.run")
    assert not a.is_irreversible("root.setup.x")


def test_all_from_methods_expose_resilient_params():
    # Every session-creating from_* entry point on the Solver session must
    # advertise resilient_mode / resilient_config, so resilient mode can be
    # requested at construction time regardless of how the session is created.
    import inspect

    from ansys.fluent.core.solver import Solver

    for name in ("from_install", "from_container", "from_pim", "from_connection"):
        params = inspect.signature(getattr(Solver, name)).parameters
        has_kwargs = any(
            p.kind is inspect.Parameter.VAR_KEYWORD for p in params.values()
        )
        if name == "from_connection":
            # Explicit parameters (no **kwargs): they must be named.
            assert "resilient_mode" in params, name
            assert "resilient_config" in params, name
            assert params["resilient_mode"].default is False, name
            assert params["resilient_config"].default is None, name
        else:
            # kwargs-based entry points accept them via the typed **kwargs.
            assert has_kwargs, name


def test_shared_resilient_helper_is_a_no_op_when_not_requested():
    from ansys.fluent.core.solver import Solver

    session = _session_with_clamp()
    # resilient_mode=False -> returned unchanged, no adapter attached.
    assert Solver._maybe_enable_resilient_mode(session, False, None) is session
    # A session without _settings_service (e.g. a dry-run / meshing result) is
    # also returned unchanged even when resilient_mode=True.
    assert Solver._maybe_enable_resilient_mode(object(), True, None) is not None


def test_shared_resilient_helper_enables_when_requested():
    from ansys.fluent.core.solver import Solver

    session = _session_with_clamp()
    result = Solver._maybe_enable_resilient_mode(session, True, None)
    assert result is session
    assert adapter_for(session).product_name == "fluent"
    # Auto-recovery now works on the session with no extra calls.
    session._settings_service.set_var("setup.ti", 5.0)
    assert session.settings.setup.ti.get_state() == 1.0
