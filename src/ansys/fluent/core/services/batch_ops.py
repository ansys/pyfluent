"""Batch rpc service."""

import inspect
import logging
from typing import List, Tuple
import weakref

import grpc

import ansys.api.fluent.v0 as api
from ansys.api.fluent.v0 import batch_ops_pb2, batch_ops_pb2_grpc
from ansys.fluent.core.services.error_handler import catch_grpc_error

network_logger = logging.getLogger("ansys.fluent.networking")


class BatchOpsService:
    """Class wrapping methods in batch rpc service."""

    def __init__(self, channel: grpc.Channel, metadata: List[Tuple[str, str]]):
        """__init__ method of BatchOpsService class."""
        self._stub = batch_ops_pb2_grpc.BatchOpsStub(channel)
        self._metadata = metadata

    @catch_grpc_error
    def execute(self, request):
        """Execute rpc of BatchOps service."""
        return self._stub.Execute(request, metadata=self._metadata)


class BatchOps:
    """Class to execute operations in batch in Fluent.

    Examples
    --------
    >>> with pyfluent.BatchOps(solver):
    >>>     solver.tui.file.read_case("mixing_elbow.cas.h5")
    >>>     solver.results.graphics.mesh["mesh-1"] = {}

    Above code will execute both operations through a single gRPC call upon exiting the
    ``with`` block.

    Operations that perform queries in Fluent are executed immediately, while others are
    queued for batch execution. Some queries are executed behind the scenes while
    queueing an operation for batch execution, and we must ensure that they do not
    depend on previously queued operations.


    For example,

    >>> with pyfluent.BatchOps(solver):
    >>>     solver.tui.file.read_case("mixing_elbow.cas.h5")
    >>>     solver.results.graphics.mesh["mesh-1"] = {}
    >>>     solver.results.graphics.mesh["mesh-1"].surfaces_list = ["wall-elbow"]

    will throw a ``KeyError`` as ``solver.results.graphics.mesh["mesh-1"]`` attempts to
    access the ``mesh-1`` mesh object which has not been created yet.
    """

    _proto_files = None
    _instance = lambda: None

    @classmethod
    def instance(cls) -> "BatchOps":
        """Get the BatchOps instance.

        Returns
        -------
        BatchOps
            BatchOps instance
        """
        return cls._instance()

    class Op:
        """Class to create a single batch operation."""

        def __init__(
            self, package: str, service: str, method: str, request_body: bytes
        ):
            """__init__ method of Op class."""
            self._request = batch_ops_pb2.ExecuteRequest(
                package=package,
                service=service,
                method=method,
                request_body=request_body,
            )
            if not BatchOps._proto_files:
                BatchOps._proto_files = [
                    x[1]
                    for x in inspect.getmembers(api, inspect.ismodule)
                    if hasattr(x[1], "DESCRIPTOR")
                ]
            self._supported = False
            self.response_cls = None
            for file in BatchOps._proto_files:
                file_desc = file.DESCRIPTOR
                if file_desc.package == package:
                    service_desc = file_desc.services_by_name.get(service)
                    if service_desc:
                        # TODO Add custom option in .proto files to identify getters
                        if not method.startswith("Get") and not method.startswith(
                            "get"
                        ):
                            method_desc = service_desc.methods_by_name.get(method)
                            if (
                                method_desc
                                and not method_desc.client_streaming
                                and not method_desc.server_streaming
                            ):
                                self._supported = True
                                response_cls_name = method_desc.output_type.name
                                # TODO Get the respnse_cls from message_factory
                                self.response_cls = getattr(file, response_cls_name)
                                break
            if self._supported:
                self._request = batch_ops_pb2.ExecuteRequest(
                    package=package,
                    service=service,
                    method=method,
                    request_body=request_body,
                )
                self._status = None
                self._result = None
            self.queued = False

        def update_result(self, status, data):
            """Update results after the batch operation is executed."""
            obj = self.response_cls()
            try:
                obj.ParseFromString(data)
            except Exception:
                pass
            self._status = status
            self._result = obj

    def __new__(cls, session):
        if cls.instance() is None:
            instance = super(BatchOps, cls).__new__(cls)
            instance._service = session._batch_ops_service
            instance._ops: List[BatchOps.Op] = []
            instance.batching = False
            cls._instance = weakref.ref(instance)
        return cls.instance()

    def __enter__(self):
        """Entering the with block."""
        self.clear_ops()
        self.batching = True
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        """Exiting from the with block."""
        network_logger.debug("Executing batch operations")
        self.batching = False
        if not exc_type:
            requests = (x._request for x in self._ops)
            responses = self._service.execute(requests)
            for i, response in enumerate(responses):
                self._ops[i].update_result(response.status, response.response_body)

    def add_op(self, package: str, service: str, method: str, request):
        """Queue a single batch operation. Only the non-getter operations will
        be queued.

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
            network_logger.debug(
                f"Adding batch operation with package {package}, service {service} and method {method}"
            )
            self._ops.append(op)
            op.queued = True
        return op

    def clear_ops(self):
        """Clear all queued batch operations."""
        self._ops.clear()
