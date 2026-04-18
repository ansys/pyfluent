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

"""Wrappers over SchemeEval gRPC service of Fluent (v1 proto API).

All shared logic lives in scheme_eval.py (v0). This module subclasses only
what differs for the v1 protobuf schema.
"""

from typing import Any, Sequence

from ansys.api.fluent.v1 import scheme_eval_pb2 as SchemeEvalProtoModule
from ansys.api.fluent.v1 import scheme_eval_pb2_grpc as SchemeEvalGrpcModule
from ansys.api.fluent.v1.scheme_pointer_pb2 import SchemePointer
from ansys.fluent.core.services.scheme_eval import (
    SchemeEvalService as _SchemeEvalServiceV0,
)
from ansys.fluent.core.services.scheme_eval import (  # noqa: F401 - re-exported for consumers
    Symbol,
)
from ansys.fluent.core.services.scheme_eval import SchemeEval as _SchemeEvalV0


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


class SchemeEvalService(_SchemeEvalServiceV0):
    """Class wrapping the SchemeEval gRPC service of Fluent (v1 proto API)."""

    def _create_stub(self, intercept_channel):
        """Create the v1 gRPC stub."""
        return SchemeEvalGrpcModule.SchemeEvalStub(intercept_channel)


class SchemeEval(_SchemeEvalV0):
    """Class on which Fluent's scheme code can be executed (v1 proto API)."""

    def _eval(self, val: Any, suppress_prompts: bool = True) -> Any:
        """Evaluates a scheme expression represented as a Python datatype."""
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
        """Executes a sequence of scheme commands."""
        request = SchemeEvalProtoModule.ExecRequest()
        request.command.extend(commands)
        request.wait = wait
        request.silent = silent
        response = self.service.exec(request)
        return response.output

    def string_eval(self, input: str) -> str:
        """Evaluates a scheme expression in string format."""
        request = SchemeEvalProtoModule.StringEvalRequest()
        request.input = input
        response = self.service.string_eval(request)
        return response.output
