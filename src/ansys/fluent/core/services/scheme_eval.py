"""Wrappers over SchemeEval gRPC service of Fluent.

Example
-------
>>> from ansys.fluent.services.scheme_eval import Symbol as S
>>> session.scheme_eval.eval([S('+'), 2, 3])
5
>>> session.scheme_eval.eval([S('rpgetvar'), [S('string->symbol'), "mom/relax"]])  # noqa: E501
0.7
>>> session.scheme_eval.exec(('(ti-menu-load-string "/report/system/proc-stats")',))  # noqa: E501
>>> # prints Fluent TUI output
>>> session.scheme_eval.string_eval("(+ 2 3)")
'5'
>>> session.scheme_eval.string_eval("(rpgetvar 'mom/relax)")
'0.7'
>>> session.scheme_eval.scheme_eval("(+ 2 3)")
5
>>> session.scheme_eval.scheme_eval("(rpgetvar 'mom/relax)")
0.7
"""

from typing import Any, List, Sequence, Tuple

import grpc

from ansys.api.fluent.v0 import scheme_eval_pb2 as SchemeEvalProtoModule
from ansys.api.fluent.v0 import scheme_eval_pb2_grpc as SchemeEvalGrpcModule
from ansys.api.fluent.v0.scheme_pointer_pb2 import SchemePointer


class SchemeEvalService:
    """Class wrapping the SchemeEval gRPC service of Fluent.

    Using the methods from the SchemeEval class is recommended.
    """

    def __init__(self, channel: grpc.Channel, metadata: List[Tuple[str, str]]):
        self.__stub = SchemeEvalGrpcModule.SchemeEvalStub(channel)
        self.__metadata = metadata

    def eval(self, request: SchemePointer) -> SchemePointer:
        return self.__stub.Eval(request, metadata=self.__metadata)

    def exec(
        self, request: SchemeEvalProtoModule.ExecRequest
    ) -> SchemeEvalProtoModule.ExecResponse:
        return self.__stub.Exec(request, metadata=self.__metadata)

    def string_eval(
        self, request: SchemeEvalProtoModule.StringEvalRequest
    ) -> SchemeEvalProtoModule.StringEvalResponse:
        return self.__stub.StringEval(request, metadata=self.__metadata)


class Symbol:
    """Class representing the symbol datatype in the scheme.

    Attributes
    ----------
    str : str
        Underlying string representation
    """

    def __init__(self, str_: str):
        self.str = str_


def _convert_pair_to_scheme_pointer(val: Tuple[Any, Any], p: SchemePointer):
    _convert_py_value_to_scheme_pointer(val[0], p.pair.car)
    _convert_py_value_to_scheme_pointer(val[1], p.pair.cdr)


def _convert_list_of_pairs_to_scheme_pointer(
    val: List[Tuple[Any, Any]], p: SchemePointer
):
    if len(val) > 0:
        _convert_pair_to_scheme_pointer(val[0], p.pair.car)
        _convert_list_of_pairs_to_scheme_pointer(val[1:], p.pair.cdr)


def _convert_py_value_to_scheme_pointer(val: Any, p: SchemePointer):
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
        _convert_py_value_to_scheme_pointer(val[0], p.pair.car)
        _convert_py_value_to_scheme_pointer(val[1], p.pair.cdr)
    elif isinstance(val, list) or isinstance(val, tuple):
        if val:
            val = list(val)
            _convert_py_value_to_scheme_pointer(val[0], p.pair.car)
            _convert_py_value_to_scheme_pointer(val[1:], p.pair.cdr)
    elif isinstance(val, dict):
        as_list = list(val.items())
        if as_list:
            _convert_pair_to_scheme_pointer(as_list[0], p.pair.car)
            _convert_list_of_pairs_to_scheme_pointer(as_list[1:], p.pair.cdr)


def _convert_scheme_pointer_to_py_list(p: SchemePointer):
    val = []
    val.append(_convert_scheme_pointer_to_py_value(p.pair.car))
    if p.pair.cdr.HasField("pair"):
        tail = _convert_scheme_pointer_to_py_list(p.pair.cdr)
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


def _convert_scheme_pointer_to_py_value(p: SchemePointer):
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
        if any(
            p.pair.cdr.HasField(x)
            for x in ["b", "fixednum", "flonum", "c", "str", "sym"]
        ):
            return (
                _convert_scheme_pointer_to_py_value(p.pair.car),
                _convert_scheme_pointer_to_py_value(p.pair.cdr),
            )
        else:
            val = _convert_scheme_pointer_to_py_list(p)
            return val
    return None


class SchemeEval:
    """Class on which Fluent's scheme code can be executed.

    Methods
    -------
    eval(val)
        Evaluates a scheme expression, returns Python value
    exec(commands, wait, silent)
        Executes a sequence of scheme commands, returns TUI output
        string
    string_eval(input_)
        Evaluates a scheme expression in string format, returns string
    scheme_eval(input_)
        Evaluates a scheme expression in string format, returns Python
        value
    """

    def __init__(self, service: SchemeEvalService):
        self.service = service

    def eval(self, val: Any) -> Any:
        """Evaluates a scheme expression.

        Parameters
        ----------
        val : Any
            Input scheme expression represented as Python datatype

        Returns
        -------
        Any
            Output scheme value represented as Python datatype
        """
        request = SchemePointer()
        _convert_py_value_to_scheme_pointer(val, request)
        response = self.service.eval(request)
        return _convert_scheme_pointer_to_py_value(response)

    def exec(
        self, commands: Sequence[str], wait: bool = True, silent: bool = True
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

    def string_eval(self, input_: str) -> str:
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
        request.input = input_
        response = self.service.string_eval(request)
        return response.output

    def scheme_eval(self, input_: str) -> Any:
        """Evaluates a scheme expression in string format.

        Parameters
        ----------
        input : str
            Input scheme expression in string format

        Returns
        -------
        str
            Output scheme value represented as Python datatype
        """
        request = SchemePointer()
        S = Symbol  # noqa N806
        val = (
            S("eval"),
            (S("with-input-from-string"), input_, S("read")),
            S("user-initial-environment"),
        )
        _convert_py_value_to_scheme_pointer(val, request)
        response = self.service.eval(request)
        return _convert_scheme_pointer_to_py_value(response)
