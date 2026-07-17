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

"""High-level scheme interpreter wrappers.

This module owns the business-logic layer on top of the SchemeInterpreter gRPC
service. The grpc service implementation lives in:

* ``ansys.fluent.core._grpc_services.scheme_interpreter_service`` (v1 proto API)
* ``ansys.fluent.core._grpc_services.scheme_interpreter_service_v0`` (v0 proto API)

Class hierarchy
---------------
``SchemeInterpreter``
    gRPC-based implementation (v1 and v0 proto API).

Example
-------
>>> session.scheme.exec(('(ti-menu-load-string "/report/system/proc-stats")',))
>>> # Returns TUI output string
>>> session.scheme.eval("(+ 2 3)")
5
>>> session.scheme.eval("(rpgetvar 'mom/relax)")
0.7
"""

from collections.abc import Sequence
from typing import Any

from deprecated.sphinx import deprecated

from ansys.fluent.core.services.abstract_scheme_interpreter import (
    AbstractSchemeInterpreter,
)
from ansys.fluent.core.utils.fluent_version import FluentVersion


class SchemeInterpreter(AbstractSchemeInterpreter):
    """SchemeInterpreter backed by the SchemeInterpreter gRPC service."""

    def __init__(self, service) -> None:
        """Initialize SchemeInterpreter."""
        self.service = service
        try:
            version = self.string_eval("(cx-version)")
            self.version = ".".join(version.strip("()").split())
        except Exception:  # for pypim launch
            self.version = FluentVersion.v252.value

    def _eval(self, val: Any, suppress_prompts: bool = True) -> Any:
        """Evaluates a scheme expression.

        Parameters
        ----------
        val : Any
            Input scheme expression represented as Python datatype

        suppress_prompts : bool, optional
            Whether to suppress prompts in Fluent, by default True

        Returns
        -------
        Any
            Output scheme value represented as Python datatype
        """
        return self.service.scheme_eval(val=val, suppress_prompts=suppress_prompts)

    def exec(
        self,
        commands: Sequence[str],
        wait: bool = True,
        silent: bool = True,
    ) -> str:
        """Executes a sequence of scheme commands.

        Parameters
        ----------
        commands : Sequence[str]
            Sequence of scheme commands in string format
        wait : bool, optional
            Specifies whether to wait until execution completes, by
            default True
        silent : bool, optional
            Specifies whether to execute silently, by default True

        Returns
        -------
        str
           Output as string
        """
        return self.service.exec(commands=commands, wait=wait, silent=silent)

    def string_eval(self, input: str) -> str:
        """Evaluates a scheme expression in string format.

        Parameters
        ----------
        input : str
            Input scheme expression in string format

        Returns
        -------
        str
            Output scheme value in string format
        """
        return self.service.string_eval(input=input)

    @deprecated(version="0.32", reason="Use ``session.scheme``.")
    def scheme_eval(self, scm_input: str, suppress_prompts: bool = True) -> Any:
        """Evaluates a scheme expression in string format."""
        return self.service.eval(scm_input, suppress_prompts)

    def is_defined(self, symbol: str) -> bool:
        """Check if a symbol is defined in the scheme environment.

        Parameters
        ----------
        symbol : str
            Name of the symbol

        Returns
        -------
        bool
            True if symbol is defined, False otherwise
        """
        return not self.eval(
            f"(lexical-unreferenceable? user-initial-environment '{symbol})"
        )

    def eval(self, scm_input: str, suppress_prompts: bool = True) -> Any:
        """Evaluates a scheme expression in string format.

        Parameters
        ----------
        scm_input : str
            Input scheme expression in string format

        suppress_prompts : bool, optional
            Whether to suppress prompts in Fluent, by default True

        Returns
        -------
        Any
            Output scheme value represented as Python datatype
        """
        return self.service.eval(scm_input, suppress_prompts)
