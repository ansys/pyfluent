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

"""Capability-based service registry for the platform layer.

A :class:`ServiceRegistry` maps capability names (for example ``"settings"`` or
``"field_data"``) to lazily constructed service objects. A backend registers
only the capabilities it supports; requesting an unsupported capability raises
:class:`NotSupported` rather than failing deep inside a service call. This lets
the same higher-level code run over different backends (gRPC, REST, a mock),
with each advertising a different capability set.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


class NotSupported(RuntimeError):
    """Raised when a requested service capability is not provided by a backend."""

    def __init__(self, capability: str) -> None:
        """Initialize NotSupported with the missing capability name."""
        self.capability = capability
        super().__init__(f"Service capability '{capability}' is not supported.")


class ServiceRegistry:
    """Lazily resolves backend services by capability name.

    Capabilities are registered with a zero-argument factory. The service is
    built on first request and cached for subsequent requests.
    """

    def __init__(self) -> None:
        """Initialize an empty registry."""
        self._factories: dict[str, Callable[[], Any]] = {}
        self._instances: dict[str, Any] = {}

    def register(self, capability: str, factory: Callable[[], Any]) -> None:
        """Register a factory for a capability.

        Parameters
        ----------
        capability : str
            The capability name.
        factory : Callable[[], Any]
            Zero-argument callable that builds the service on first request.
        """
        self._factories[capability] = factory

    def has(self, capability: str) -> bool:
        """Return whether a capability is registered."""
        return capability in self._factories

    def get(self, capability: str) -> Any:
        """Return the service for a capability, building it on first request.

        Raises
        ------
        NotSupported
            If the capability is not registered.
        """
        if capability not in self._factories:
            raise NotSupported(capability)
        if capability not in self._instances:
            self._instances[capability] = self._factories[capability]()
        return self._instances[capability]

    def capabilities(self) -> frozenset[str]:
        """Return the set of registered capability names."""
        return frozenset(self._factories)
