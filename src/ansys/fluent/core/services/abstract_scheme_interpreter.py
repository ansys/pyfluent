# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
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

"""Abstract scheme interpreter wrapper."""

from abc import ABC, abstractmethod
from typing import Any, Sequence


class AbstractSchemeInterpreter(ABC):
    """Abstract base class for the scheme interpreter."""

    @abstractmethod
    def _eval(self, val: Any, suppress_prompts: bool = True) -> Any:
        """Evaluates a scheme expression."""
        pass

    @abstractmethod
    def exec(
        self,
        commands: Sequence[str],
        wait: bool = True,
        silent: bool = True,
    ) -> str:
        """Executes a sequence of scheme commands."""
        pass

    @abstractmethod
    def string_eval(self, input: str) -> str:
        """Evaluates a scheme expression in string format."""
        pass

    @abstractmethod
    def eval(self, scm_input: str, suppress_prompts: bool = True) -> Any:
        """Evaluates a scheme expression in string format."""
        pass
