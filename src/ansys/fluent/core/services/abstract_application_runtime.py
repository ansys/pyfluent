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

"""Abstract application runtime wrapper."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any

from ansys.fluent.core.utils.fluent_version import FluentVersion


@dataclass
class ProcessInfo:
    """Hold process information."""

    process_id: int
    hostname: str
    working_directory: str


@dataclass
class BuildInfo:
    """Hold build information."""

    build_time: str
    build_id: str
    vcs_revision: str
    vcs_branch: str


class AbstractApplicationRuntime(ABC):
    """Abstract base class for the Application runtime."""

    @abstractmethod
    def get_product_version(self) -> FluentVersion:
        """Get product version."""
        pass

    @abstractmethod
    def get_build_info(self) -> BuildInfo:
        """Get build info."""
        pass

    @abstractmethod
    def get_controller_process_info(self) -> ProcessInfo:
        """Get controller process info."""
        pass

    @abstractmethod
    def get_solver_process_info(self) -> ProcessInfo:
        """Get solver process info."""
        pass

    @abstractmethod
    def get_app_mode(self) -> Enum:
        """Get app mode."""
        pass

    @abstractmethod
    def start_python_journal(self, journal_name: str | None = None) -> int:
        """Start python journal."""
        pass

    @abstractmethod
    def stop_python_journal(self, journal_id: str | None = None) -> str:
        """Stop python journal."""
        pass

    @abstractmethod
    def is_beta_enabled(self) -> bool:
        """Return whether beta features are enabled."""
        pass

    @abstractmethod
    def enable_beta(self) -> None:
        """Enable beta features."""
        pass

    @abstractmethod
    def exit(self) -> None:
        """Exit the server."""
        pass

    @abstractmethod
    def set_working_directory(self, path: Any) -> None:
        """Change the client cortex working directory."""
        pass
