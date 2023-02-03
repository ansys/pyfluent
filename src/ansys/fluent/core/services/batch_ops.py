"""Batch rpc service."""

import inspect
from typing import List, Tuple

import grpc

import ansys.api.fluent.v0 as api
from ansys.api.fluent.v0 import batch_ops_pb2, batch_ops_pb2_grpc, batchable_pb2
from ansys.fluent.core.services.error_handler import catch_grpc_error
from ansys.fluent.core.utils.logging import LOG


class BatchOpsService:
    """Class wrapping methods in batch rpc service."""

    def __init__(self, channel: grpc.Channel, metadata: List[Tuple[str, str]]):
        self._stub = batch_ops_pb2_grpc.BatchOpsStub(channel)
        self._metadata = metadata

    @catch_grpc_error
    def execute(self, request):
        """Call execute rpc."""
        return self._stub.Execute(request,  metadata=self._metadata)


class BatchOps:
    """Class to perform batch operations.

    Examples
    --------
    >>> with pyfluent.BatchOps(solver):
    >>>     solver.tui.file.read_case("elbow.cas.h5")
    >>>     solver.solution.initialization.hybrid_initialize()

    Above will be executed in server through a single grpc call during exiting the with
    block. Only the execute-command like rpc methods are supported. Those methods are
    marked with `batchable` option in .proto files.

    The non-batchable rpc methods within the with block are executed right away. Make
    sure that they do not depend on execution of batchable methods.

    """

    _proto_files = None
    _batchable_desc = None
    _current = None

    @classmethod
    def get_current(cls) -> "BatchOps":
        """
        Get the current instance of BatchOps.

        Returns
        -------
        BatchOps
            Current BatchOps instance
        """
        return cls._current

    class Op:
        """
        Class to create a single batch operation.
        """
        def __init__(self, package: str, service: str, method: str, request_body: bytes):
            self._request = batch_ops_pb2.ExecuteRequest(
                package=package, service=service, method=method, request_body=request_body
            )
            if not BatchOps._proto_files:
                BatchOps._proto_files = [x[1] for x in inspect.getmembers(api, inspect.ismodule) if hasattr(x[1], "DESCRIPTOR")]
            if not BatchOps._batchable_desc:
                BatchOps._batchable_desc = batchable_pb2.DESCRIPTOR.extensions_by_name["batchable"]
            self._supported = False
            self.response_cls = None
            for file in BatchOps._proto_files:
                file_desc = file.DESCRIPTOR
                if file_desc.package == package:
                    service_desc = file_desc.services_by_name.get(service)
                    if service_desc:
                        method_desc = service_desc.methods_by_name.get(method)
                        if method_desc:
                            options = method_desc.GetOptions()
                            if options.HasExtension(BatchOps._batchable_desc) and options.Extensions[BatchOps._batchable_desc]:
                                self._supported = True
                                response_cls_name = method_desc.output_type.name
                                # TODO Get the respnse_cls from message_factory
                                self.response_cls = getattr(file, response_cls_name)
                                break
            if self._supported:
                self._request = batch_ops_pb2.ExecuteRequest(
                    package=package, service=service, method=method, request_body=request_body
                    )
                self._status = None
                self._result = None
            self.queued = False

        def update_result(self, status, data):
            """
            Update results after the batch operation is executed.
            """
            obj = self.response_cls()
            try:
                obj.ParseFromString(data)
            except Exception:
                pass
            self._status = status
            self._result = obj

    def __init__(self, session):
        """Initialize BatchOps."""
        self._service = session._batch_ops_service
        self._ops = []

    def __enter__(self):
        """
        Entering the with block
        """
        BatchOps._current = self

    def __exit__(self, exc_type, exc_value, exc_tb):
        """
        Exiting from the with block
        """
        LOG.debug("Executing batch operations")
        requests = (x._request for x in self._ops)
        responses = self._service.execute(requests)
        for i, response in enumerate(responses):
            self._ops[i].update_result(response.status, response.response_body)
        BatchOps._current = None

    def add_op(self, package: str, service: str, method: str, request):
        """
        Queue a single batch operation. Only the `batchable` operations will be
        queued.

        Parameters
        ----------
        package : str
            gRPC package name
        service : str
            gRPC service name
        method : str
            gRPC method name
        request : Any
            gRPC request message

        Returns
        -------
        BatchOps.Op
            BatchOps.Op object with a queued attribute which is true if the operation
            has been queued.
        """
        op = BatchOps.Op(package, service, method, request.SerializeToString())
        if op._supported:
            LOG.debug(f"Adding batch operation with package {package}, service {service} and method {method}")
            self._ops.append(op)
            op.queued = True
        return op
