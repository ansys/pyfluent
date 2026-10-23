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

"""Tests for the guarded inactive-target attribute-access patch.

These verify the reference-counting / idempotency of the patch installer and the
behaviour of the wrapper it builds: a passthrough when no resilient session is
active, and a discover-activate-retry when one is.
"""

import pytest

from ansys.fluent.core.resilient import patch

pytestmark = pytest.mark.resilient


@pytest.fixture(autouse=True)
def _reset_patch_state():
    # Ensure a clean counter around each test (the patch is process-global).
    before = patch.active_session_count()
    yield
    # Drain any sessions this test registered without unregistering.
    while patch.active_session_count() > before:
        patch.unregister_session()


def test_register_unregister_refcount():
    start = patch.active_session_count()
    patch.register_session()
    patch.register_session()
    assert patch.active_session_count() == start + 2
    patch.unregister_session()
    assert patch.active_session_count() == start + 1
    patch.unregister_session()
    assert patch.active_session_count() == start


def test_unregister_never_goes_negative():
    while patch.active_session_count() > 0:
        patch.unregister_session()
    patch.unregister_session()
    assert patch.active_session_count() == 0


class _FakeInactiveError(RuntimeError):
    pass


def _build_wrapper(controller=None, active_error=_FakeInactiveError):
    """Build the wrapper around a synthetic original __getattribute__."""

    def original(self, name):
        # Simulate flobject: raise on 'child' until self._enabled is True.
        if name == "child" and not object.__getattribute__(self, "_enabled"):
            raise active_error("inactive")
        return object.__getattribute__(self, name)

    # Monkeypatch the error class the wrapper catches and the controller lookup.
    import ansys.fluent.core.resilient.patch as p

    p._inactive_object_error_cls = lambda: active_error
    p._controller_for = lambda obj: controller
    return p._make_wrapper(original)


class _Node:
    def __init__(self, enabled, value="ok"):
        object.__setattr__(self, "_enabled", enabled)
        object.__setattr__(self, "child", value)


class _Controller:
    def __init__(self, activator):
        self._resolver = activator


class _Activator:
    """Flips the node's _enabled when asked to activate it."""

    def __init__(self, succeeds):
        self._succeeds = succeeds
        self.called = 0

    def activate_object(self, obj):
        self.called += 1
        if self._succeeds:
            object.__setattr__(obj, "_enabled", True)
            return ["setup.models.energy.enabled"]
        return []


def test_wrapper_passthrough_when_no_resilient_session():
    wrapper = _build_wrapper(controller=_Controller(_Activator(True)))
    # Count is 0 -> pure passthrough -> the original error propagates.
    while patch.active_session_count() > 0:
        patch.unregister_session()
    node = _Node(enabled=False)
    with pytest.raises(_FakeInactiveError):
        wrapper(node, "child")


def test_wrapper_recovers_when_activation_succeeds():
    activator = _Activator(succeeds=True)
    wrapper = _build_wrapper(controller=_Controller(activator))
    patch.register_session()
    node = _Node(enabled=False, value="recovered")
    assert wrapper(node, "child") == "recovered"
    assert activator.called == 1


def test_wrapper_reraises_when_activation_fails():
    activator = _Activator(succeeds=False)
    wrapper = _build_wrapper(controller=_Controller(activator))
    patch.register_session()
    node = _Node(enabled=False)
    with pytest.raises(_FakeInactiveError):
        wrapper(node, "child")
    assert activator.called == 1


# -- __setattr__ wrapper (client-side wrong-type / disallowed-value) --------


from ansys.fluent.core.resilient.types import Fix  # noqa: E402


class _SetattrController:
    def __init__(self, resolver):
        self._resolver = resolver


class _SnapResolver:
    """Proposes a coerce/snap fix from the live child object."""

    def __init__(self, new_value):
        self._new_value = new_value
        self.seen = []

    def propose_for_object(self, obj, value, cls):
        self.seen.append((obj, value, cls.category))
        if self._new_value is None:
            return None
        return Fix(kind="fix", description="repair", new_value=self._new_value)


class _SetattrNode:
    """Simulates a Group whose set rejects bad values until repaired."""

    def __init__(self, resolver, accept):
        object.__setattr__(self, "_resolver", resolver)
        object.__setattr__(self, "_accept", accept)
        object.__setattr__(self, "child", _Child())
        object.__setattr__(self, "applied", None)

    @property
    def _root(self):
        root = type("Root", (), {})()
        root.flproxy = type("Proxy", (), {"_controller": self._resolver_holder})()
        return root


class _Child:
    python_path = "<session>.settings.setup.x"


def _build_setattr_wrapper(resolver, accept_value):
    """Build the __setattr__ wrapper around a synthetic original."""
    import ansys.fluent.core.resilient.patch as p

    state = {}

    def original(self, name, value):
        if name == "child" and value != accept_value:
            raise TypeError("wrong type")
        state[name] = value

    p._controller_for = lambda obj: _SetattrController(resolver)
    p._recoverable_setattr_errors = lambda: (TypeError,)
    return p._make_setattr_wrapper(original), state


def test_setattr_passthrough_when_no_resilient_session():
    resolver = _SnapResolver(new_value=0.05)
    wrapper, _ = _build_setattr_wrapper(resolver, accept_value=0.05)
    while patch.active_session_count() > 0:
        patch.unregister_session()

    class N:
        def __getattribute__(self, n):
            return object.__getattribute__(self, n)

    node = N()
    with pytest.raises(TypeError):
        wrapper(node, "child", "bad")


def test_setattr_recovers_with_coerced_value():
    resolver = _SnapResolver(new_value=0.05)
    wrapper, state = _build_setattr_wrapper(resolver, accept_value=0.05)
    patch.register_session()

    class N:
        child = _Child()

        def __getattribute__(self, n):
            return object.__getattribute__(self, n)

    node = N()
    wrapper(node, "child", "0.05")  # wrong type -> coerced to 0.05 -> accepted
    assert state["child"] == 0.05
    assert resolver.seen  # resolver was consulted


def test_setattr_reraises_when_no_fix():
    resolver = _SnapResolver(new_value=None)  # no fix proposed
    wrapper, _ = _build_setattr_wrapper(resolver, accept_value=0.05)
    patch.register_session()

    class N:
        child = _Child()

        def __getattribute__(self, n):
            return object.__getattribute__(self, n)

    node = N()
    with pytest.raises(TypeError):
        wrapper(node, "child", "bad")
