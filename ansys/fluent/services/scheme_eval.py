"""
Wrappers over SchemeEval grpc service of Fluent.

Example
-------
>>> from ansys.fluent.services.scheme_eval import Symbol as S
>>> session._Session__scheme_eval.eval([S('+'), 2.0, 3.0])
5.0
>>> session._Session__scheme_eval.eval((S('rpgetvar'), (S('string->symbol'), "smooth-mesh/method")))  # noqa: E501
'quality based'

"""

from typing import Any, List, Tuple

import grpc

from ansys.api.fluent.v0 import scheme_eval_pb2 as SchemeEvalProtoModule
from ansys.api.fluent.v0 import scheme_eval_pb2_grpc as SchemeEvalGrpcModule
from ansys.api.fluent.v0.scheme_pointer_pb2 import SchemePointer


class SchemeEvalService:
    """
    Class wrapping the SchemeEval grpc service of Fluent. It is
    suggested to use the methods from SchemeEval class.
    """

    def __init__(self, channel: grpc.Channel, metadata):
        self.__stub = SchemeEvalGrpcModule.SchemeEvalStub(channel)
        self.__metadata = metadata

    def eval(self, request):
        return self.__stub.Eval(request, metadata=self.__metadata)

    def exec(self, request):
        return self.__stub.Exec(request, metadata=self.__metadata)

    def string_eval(self, request):
        return self.__stub.StringEval(request, metadata=self.__metadata)


class Symbol:
    """
    Class to represent symbol datatype in scheme

    Attributes
    ----------
    str : str
        The underlying string representation
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
    """Convert Python datatype to Scheme pointer"""
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
        p.pair.car.sym = "__map__"
        as_list = list(val.items())
        if as_list:
            _convert_pair_to_scheme_pointer(as_list[0], p.pair.cdr.pair.car)
            _convert_list_of_pairs_to_scheme_pointer(
                as_list[1:], p.pair.cdr.pair.cdr
            )


def _convert_scheme_pointer_to_pair(p: SchemePointer):
    k = _convert_scheme_pointer_to_py_value(p.pair.car)
    v = _convert_scheme_pointer_to_py_value(p.pair.cdr)
    return k, v


def _convert_scheme_pointer_to_list_of_pairs(p: SchemePointer):
    val = []
    if p.HasField("pair"):
        val.append(_convert_scheme_pointer_to_pair(p.pair.car))
        val.extend(_convert_scheme_pointer_to_list_of_pairs(p.pair.cdr))
    return val


def _convert_scheme_pointer_to_py_value(p: SchemePointer):
    """Convert Scheme pointer to Python datatype"""
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
        if p.pair.car.HasField("sym") and p.pair.car.sym == "__map__":
            d = {}
            if p.pair.cdr.HasField("pair"):
                k, v = _convert_scheme_pointer_to_pair(p.pair.cdr.pair.car)
                d[k] = v
                for kv in _convert_scheme_pointer_to_list_of_pairs(
                    p.pair.cdr.pair.cdr
                ):
                    d[kv[0]] = kv[1]
            return d
        elif any(
            p.pair.cdr.HasField(x)
            for x in ["b", "fixednum", "flonum", "c", "str", "sym"]
        ):
            return (
                _convert_scheme_pointer_to_py_value(p.pair.car),
                _convert_scheme_pointer_to_py_value(p.pair.cdr),
            )
        else:
            val = []
            val.append(_convert_scheme_pointer_to_py_value(p.pair.car))
            if p.pair.cdr.HasField("pair"):
                val.extend(_convert_scheme_pointer_to_py_value(p.pair.cdr))
            return val
    return None


class SchemeEval:
    def __init__(self, service: SchemeEvalService):
        self.service = service

    def eval(self, val: Any) -> Any:
        """
        Evaluate a scheme expression

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
        self, commands: List[str], wait: bool = True, silent: bool = True
    ) -> str:
        """
        Execute a sequence of scheme commands

        Parameters
        ----------
        commands : List[str]
            List of scheme commands in string format
        wait : bool, optional
            Whether to wait till execution completes, by default True
        silent : bool, optional
            Whether to execute silently, by default True

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
        """
        Evaluate a string expression in string format

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
