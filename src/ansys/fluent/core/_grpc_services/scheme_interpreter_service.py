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

"""Wrapper over the scheme interpreter gRPC service of Fluent (v1 proto API)."""

from collections.abc import Sequence
from typing import Any

import grpc

from ansys.api.fluent.v1 import scheme_interpreter_pb2, scheme_interpreter_pb2_grpc
from ansys.api.fluent.v1.scheme_pointer_pb2 import SchemePointer
from ansys.fluent.core.services._protocols import ServiceProtocol
from ansys.fluent.core.services.interceptors import (
    BatchInterceptor,
    ErrorStateInterceptor,
    GrpcErrorInterceptor,
    TracingInterceptor,
)


class SchemeInterpreterService(ServiceProtocol):
    """SchemeInterpreter gRPC service wrapper (v1 proto API)."""

    def __init__(
        self, channel: grpc.Channel, metadata: list[tuple[str, str]], fluent_error_state
    ) -> None:
        """Initialize SchemeInterpreterService."""
        intercept_channel = grpc.intercept_channel(
            channel,
            GrpcErrorInterceptor(),
            ErrorStateInterceptor(fluent_error_state),
            TracingInterceptor(),
            BatchInterceptor(),
        )
        self._stub = scheme_interpreter_pb2_grpc.SchemeInterpreterStub(
            intercept_channel
        )
        self._metadata = metadata

    @property
    def version(self) -> str:
        """Gets the version of the server."""
        return ".".join(self.string_eval("(cx-version)").strip("()").split())

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
        request = scheme_interpreter_pb2.ExecRequest()
        request.commands.extend(commands)
        request.wait = wait
        request.silent = silent
        response = self._stub.Exec(request, metadata=self._metadata)
        return response.output

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
        request = scheme_interpreter_pb2.StringEvalRequest()
        request.input = input
        response = self._stub.StringEval(request, metadata=self._metadata)
        return response.output

    def scheme_eval(self, val: Any, suppress_prompts: bool = True) -> Any:
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
        request = scheme_interpreter_pb2.SchemeEvalRequest()
        _convert_py_value_to_scheme_pointer(val, request.input, self.version)
        metadata = []
        if not suppress_prompts:
            metadata.append(("no-suppress-prompts", "1"))
        new_metadata = self._metadata
        if metadata:
            new_metadata = self._metadata + metadata
        response = self._stub.SchemeEval(request, metadata=new_metadata)
        return _convert_scheme_pointer_to_py_value(response.output, self.version)

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
        S = Symbol  # noqa N806
        val = (
            S("eval"),
            (S("with-input-from-string"), scm_input, S("read")),
            S("user-initial-environment"),
        )
        return self.scheme_eval(val=val, suppress_prompts=suppress_prompts)


class Symbol:
    """Class representing the symbol datatype in Fluent.

    Attributes
    ----------
    str : str
        Underlying string representation
    """

    def __init__(self, str: str) -> None:
        """__init__ method of Symbol class."""
        self.str = str

    def __repr__(self) -> str:
        return self.str


def _convert_py_value_to_scheme_pointer(
    val: Any, p: SchemePointer, version: str
) -> None:
    """Convert Python datatype to Scheme pointer for v1 proto."""
    if isinstance(val, bool):
        p.b = val
    elif isinstance(val, int):
        p.fixednum = val
    elif isinstance(val, float):
        p.flonum = val
    elif isinstance(val, str):
        p.str = val
    elif isinstance(val, Symbol):
        p.sym = val.str
    elif isinstance(val, tuple) and len(val) == 2:
        _convert_py_value_to_scheme_pointer(val[0], p.pair.car, version)
        _convert_py_value_to_scheme_pointer(val[1], p.pair.cdr, version)
    elif isinstance(val, list) or isinstance(val, tuple):
        for item in val:
            _convert_py_value_to_scheme_pointer(item, p.list.items.add(), version)
    elif isinstance(val, dict):
        for k, v in val.items():
            item = p.list.items.add()
            _convert_py_value_to_scheme_pointer(k, item.pair.car, version)
            _convert_py_value_to_scheme_pointer(v, item.pair.cdr, version)


def _convert_scheme_pointer_to_py_value(p: SchemePointer, version: str) -> Any:
    """Convert Scheme pointer to Python datatype for v1 proto."""
    if p.HasField("b"):
        return p.b
    elif p.HasField("fixednum"):
        return p.fixednum
    elif p.HasField("flonum"):
        return p.flonum
    elif p.HasField("c"):
        return p.c
    elif p.HasField("str"):
        return p.str
    elif p.HasField("sym"):
        return Symbol(p.sym)
    elif p.HasField("pair"):
        car = _convert_scheme_pointer_to_py_value(p.pair.car, version)
        cdr = _convert_scheme_pointer_to_py_value(p.pair.cdr, version)
        return (car,) if cdr is None else (car, cdr)
    elif p.HasField("list"):
        is_dict = all(item.HasField("pair") for item in p.list.items)
        if is_dict:
            return {
                _convert_scheme_pointer_to_py_value(
                    item.pair.car, version
                ): _convert_scheme_pointer_to_py_value(item.pair.cdr, version)
                for item in p.list.items
            }
        else:
            return [
                _convert_scheme_pointer_to_py_value(item, version)
                for item in p.list.items
            ]

    return None
