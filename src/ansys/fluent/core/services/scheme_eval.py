# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
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

"""Wrappers over SchemeEval gRPC service of Fluent.

Example
-------
>>> session.scheme.exec(('(ti-menu-load-string "/report/system/proc-stats")',))
>>> # Returns TUI output string
>>> session.scheme.eval("(+ 2 3)")
5
>>> session.scheme.eval("(rpgetvar 'mom/relax)")
0.7
"""

from typing import Any, Sequence

from deprecated.sphinx import deprecated
import grpc

from ansys.api.fluent.v0 import scheme_eval_pb2 as SchemeEvalProtoModule
from ansys.api.fluent.v0 import scheme_eval_pb2_grpc as SchemeEvalGrpcModule
from ansys.api.fluent.v0.scheme_pointer_pb2 import SchemePointer
from ansys.fluent.core.services.interceptors import (
    BatchInterceptor,
    ErrorStateInterceptor,
    GrpcErrorInterceptor,
    TracingInterceptor,
)
from ansys.fluent.core.utils.fluent_version import FluentVersion


class SchemeEvalService:
    """Class wrapping the SchemeEval gRPC service of Fluent.

    Using the methods from the SchemeEval class is recommended.
    """

    def __init__(
        self, channel: grpc.Channel, metadata: list[tuple[str, str]], fluent_error_state
    ) -> None:
        """__init__ method of SchemeEvalService class."""
        intercept_channel = grpc.intercept_channel(
            channel,
            GrpcErrorInterceptor(),
            ErrorStateInterceptor(fluent_error_state),
            TracingInterceptor(),
            BatchInterceptor(),
        )
        self.__stub = SchemeEvalGrpcModule.SchemeEvalStub(intercept_channel)
        self.__metadata = metadata

    def eval(self, request: SchemePointer) -> SchemePointer:
        """Eval RPC of SchemeEval service."""
        return self.__stub.Eval(request, metadata=self.__metadata)

    def exec(
        self, request: SchemeEvalProtoModule.ExecRequest
    ) -> SchemeEvalProtoModule.ExecResponse:
        """Exec RPC of SchemeEval service."""
        return self.__stub.Exec(request, metadata=self.__metadata)

    def string_eval(
        self, request: SchemeEvalProtoModule.StringEvalRequest
    ) -> SchemeEvalProtoModule.StringEvalResponse:
        """StringEval RPC of SchemeEval service."""
        return self.__stub.StringEval(request, metadata=self.__metadata)

    def scheme_eval(
        self,
        request: SchemeEvalProtoModule.SchemeEvalRequest,
        metadata: list[tuple[str, str]] = None,
    ) -> SchemeEvalProtoModule.SchemeEvalResponse:
        """SchemeEval RPC of SchemeEval service."""
        new_metadata = self.__metadata
        if metadata:
            new_metadata = self.__metadata + metadata
        return self.__stub.SchemeEval(request, metadata=new_metadata)


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


def _convert_pair_to_scheme_pointer(
    val: tuple[Any, Any], p: SchemePointer, version: str
) -> None:
    _convert_py_value_to_scheme_pointer(val[0], p.pair.car, version)
    _convert_py_value_to_scheme_pointer(val[1], p.pair.cdr, version)


def _convert_list_of_pairs_to_scheme_pointer(
    val: list[tuple[Any, Any]], p: SchemePointer, version: str
) -> None:
    if len(val) > 0:
        _convert_pair_to_scheme_pointer(val[0], p.pair.car, version)
        _convert_list_of_pairs_to_scheme_pointer(val[1:], p.pair.cdr, version)


def _convert_py_value_to_scheme_pointer(
    val: Any, p: SchemePointer, version: str
) -> None:
    """Convert Python datatype to Scheme pointer."""
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
        if FluentVersion(version) < FluentVersion.v231:
            if val:
                val = list(val)
                _convert_py_value_to_scheme_pointer(val[0], p.pair.car, version)
                _convert_py_value_to_scheme_pointer(val[1:], p.pair.cdr, version)
        else:
            for item in val:
                _convert_py_value_to_scheme_pointer(item, p.list.item.add(), version)
    elif isinstance(val, dict):
        if FluentVersion(version) < FluentVersion.v231:
            as_list = list(val.items())
            if as_list:
                _convert_pair_to_scheme_pointer(as_list[0], p.pair.car, version)
                _convert_list_of_pairs_to_scheme_pointer(
                    as_list[1:], p.pair.cdr, version
                )
        else:
            for k, v in val.items():
                item = p.list.item.add()
                _convert_py_value_to_scheme_pointer(k, item.pair.car, version)
                _convert_py_value_to_scheme_pointer(v, item.pair.cdr, version)


def _convert_scheme_pointer_to_py_list(p: SchemePointer, version: str) -> dict | list:
    val = []
    val.append(_convert_scheme_pointer_to_py_value(p.pair.car, version))
    if p.pair.cdr.HasField("pair"):
        tail = _convert_scheme_pointer_to_py_list(p.pair.cdr, version)
        val.extend([tail] if isinstance(tail, dict) else tail)
    if all(
        isinstance(x, dict)
        or (
            (isinstance(x, tuple) or isinstance(x, list))
            and x
            and isinstance(x[0], str)
        )
        for x in val
    ):
        d = {}
        for x in val:
            if isinstance(x, dict):
                d.update(x)
            else:
                d[x[0]] = x[1:] if len(x) > 2 else x[1]
        return d
    return val


def _convert_scheme_pointer_to_py_value(p: SchemePointer, version: str) -> Any:
    """Convert Scheme pointer to Python datatype."""
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
        if FluentVersion(version) < FluentVersion.v231:
            if any(
                p.pair.cdr.HasField(x)
                for x in ["b", "fixednum", "flonum", "c", "str", "sym"]
            ):
                return (
                    _convert_scheme_pointer_to_py_value(p.pair.car, version),
                    _convert_scheme_pointer_to_py_value(p.pair.cdr, version),
                )
            else:
                val = _convert_scheme_pointer_to_py_list(p, version)
                return val
        else:
            car = _convert_scheme_pointer_to_py_value(p.pair.car, version)
            cdr = _convert_scheme_pointer_to_py_value(p.pair.cdr, version)
            return (car,) if cdr is None else (car, cdr)
    elif p.HasField("list"):
        is_dict = all(item.HasField("pair") for item in p.list.item)
        if is_dict:
            return {
                _convert_scheme_pointer_to_py_value(
                    item.pair.car, version
                ): _convert_scheme_pointer_to_py_value(item.pair.cdr, version)
                for item in p.list.item
            }
        else:
            return [
                _convert_scheme_pointer_to_py_value(item, version)
                for item in p.list.item
            ]

    return None


class SchemeEval:
    """Class on which Fluent's scheme code can be executed.

    Methods
    -------
    exec(commands, wait, silent)
        Executes a sequence of scheme commands, returns TUI output
        string
    eval(input)
        Evaluates a scheme expression in string format, returns Python
        value
    """

    def __init__(self, service: SchemeEvalService) -> None:
        """__init__ method of SchemeEval class."""
        self.service = service
        try:
            version = self.string_eval("(cx-version)")
            self.version = ".".join(version.strip("()").split())
        except Exception:  # for pypim launch
            self.version = FluentVersion.v231.value

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
        if FluentVersion(self.version) < FluentVersion.v231:
            request = SchemePointer()
            _convert_py_value_to_scheme_pointer(val, request, self.version)
            response = self.service.eval(request)
            return _convert_scheme_pointer_to_py_value(response, self.version)
        else:
            request = SchemeEvalProtoModule.SchemeEvalRequest()
            _convert_py_value_to_scheme_pointer(val, request.input, self.version)
            metadata = []
            if not suppress_prompts:
                metadata.append(("no-suppress-prompts", "1"))
            response = self.service.scheme_eval(request, metadata)
            return _convert_scheme_pointer_to_py_value(response.output, self.version)

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
        request = SchemeEvalProtoModule.ExecRequest()
        request.command.extend(commands)
        request.wait = wait
        request.silent = silent
        response = self.service.exec(request)
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
        request = SchemeEvalProtoModule.StringEvalRequest()
        request.input = input
        response = self.service.string_eval(request)
        return response.output

    @deprecated(version="0.32", reason="Use ``session.scheme``.")
    def scheme_eval(self, scm_input: str, suppress_prompts: bool = True) -> Any:
        """Evaluates a scheme expression in string format."""
        return self.eval(scm_input, suppress_prompts)

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
        return self._eval(val, suppress_prompts)

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
