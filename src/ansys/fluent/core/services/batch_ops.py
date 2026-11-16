# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
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

"""Batch RPC service."""

import logging
from typing import TypeVar
import weakref

__all__ = ("BatchOps",)

_TBatchOps = TypeVar("_TBatchOps", bound="BatchOps")

network_logger: logging.Logger = logging.getLogger("pyfluent.networking")


class BatchOps:
    """Class to execute operations in batch in Fluent.

    Examples
    --------
    >>> with pyfluent.BatchOps(solver):
    >>>     solver.tui.file.read_case("mixing_elbow.cas.h5")
    >>>     solver.settings.results.graphics.mesh["mesh-1"] = {}

    Above code will execute both operations through a single gRPC call upon exiting the
    ``with`` block.

    Operations that perform queries in Fluent are executed immediately, while others are
    queued for batch execution. Some queries are executed behind the scenes while
    queueing an operation for batch execution, and we must ensure that they do not
    depend on previously queued operations.


    For example,

    >>> with pyfluent.BatchOps(solver):
    >>>     solver.tui.file.read_case("mixing_elbow.cas.h5")
    >>>     solver.settings.results.graphics.mesh["mesh-1"] = {}
    >>>     solver.settings.results.graphics.mesh["mesh-1"].surfaces_list = ["wall-elbow"]

    will throw a ``KeyError`` as ``solver.settings.results.graphics.mesh["mesh-1"]`` attempts to
    access the ``mesh-1`` mesh object which has not been created yet.
    """

    def _instance():
        return None

    @classmethod
    def instance(cls) -> _TBatchOps | None:
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
            self,
            package: str,
            service: str,
            method: str,
            request_body: bytes,
        ) -> None:
            """__init__ method of Op class."""
            self._package = package
            self._service_name = service
            self._method = method
            self._request_body = request_body
            self._supported = False
            self.response_cls = None
            self._status = None
            self._result = None
            self.queued = False

        def update_result(self, status, result) -> None:
            """Update results after the batch operation is executed."""
            self._status = status
            self._result = result

    def __new__(cls, session) -> _TBatchOps:
        if cls.instance() is None:
            instance = super().__new__(cls)
            instance._service = session._batch_ops_service
            instance._ops: list[BatchOps.Op] = []
            instance.batching = False
            cls._instance = weakref.ref(instance)
        return cls.instance()

    def __enter__(self) -> _TBatchOps:
        """Entering the with block."""
        self.clear_ops()
        self.batching = True
        return self

    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        """Exiting from the with block."""
        network_logger.debug("Executing batch operations")
        self.batching = False
        if not exc_type:
            results = self._service.execute(self._ops)
            for op, (status, result) in zip(self._ops, results):
                op.update_result(status, result)

    def add_op(self, package: str, service: str, method: str, request) -> Op:
        """Queue a single batch operation. Only the non-getter operations will be
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
        op = self.__class__.Op(package, service, method, request.SerializeToString())
        op._supported, op.response_cls = self._service.get_op_metadata(
            package, service, method
        )
        if op._supported:
            network_logger.debug(
                f"Adding batch operation with package {package}, service {service} and method {method}"
            )
            self._ops.append(op)
            op.queued = True
        return op

    def clear_ops(self) -> None:
        """Clear all queued batch operations."""
        self._ops.clear()
