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

"""Unit tests for the ansys.solver.core platform contracts (no Fluent needed)."""

import pytest

from ansys.framework.services import NotSupported, ServiceRegistry
from ansys.framework.transport import ErrorState, Transport


def test_service_registry_lazy_resolution_and_caching():
    calls = []

    def build_settings():
        calls.append("settings")
        return object()

    registry = ServiceRegistry()
    registry.register("settings", build_settings)

    assert registry.has("settings")
    assert not registry.has("field_data")
    assert calls == []  # not built until requested

    first = registry.get("settings")
    second = registry.get("settings")
    assert first is second  # cached
    assert calls == ["settings"]  # factory called exactly once


def test_service_registry_missing_capability_raises_not_supported():
    registry = ServiceRegistry()
    with pytest.raises(NotSupported) as exc_info:
        registry.get("field_data")
    assert exc_info.value.capability == "field_data"


def test_service_registry_capabilities_set():
    registry = ServiceRegistry()
    registry.register("settings", lambda: 1)
    registry.register("field_data", lambda: 2)
    assert registry.capabilities() == frozenset({"settings", "field_data"})


def test_transport_protocol_is_runtime_checkable():
    class _ErrorState:
        name = ""
        details = ""

        def set(self, name, details):
            pass

        def clear(self):
            pass

    class _Transport:
        metadata = [("password", "secret")]
        error_state = _ErrorState()
        is_serving = True

        def connect(self):
            pass

        def close(self):
            pass

    transport = _Transport()
    assert isinstance(transport.error_state, ErrorState)
    assert isinstance(transport, Transport)
    assert not isinstance(object(), Transport)
