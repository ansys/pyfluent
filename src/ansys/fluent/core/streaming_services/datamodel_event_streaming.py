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

"""Provides a module for datamodel event streaming."""

from collections.abc import Callable
import logging
import threading

from google.protobuf.json_format import MessageToDict

from ansys.fluent.core.streaming_services.streaming import StreamingService

network_logger: logging.Logger = logging.getLogger("pyfluent.networking")


class DatamodelEvents(StreamingService):
    """Encapsulates a datamodel events streaming service (version-agnostic).

    All proto-specific logic (request construction, response field access, and
    variant conversion) lives in the gRPC service layer via
    ``_process_event_streaming`` and ``parse_event_response``.
    """

    def __init__(self, service):
        """Initialize DatamodelEvents."""
        # `service` may be a high-level wrapper (ObjectModel / ObjectModelV261).
        # The underlying gRPC service is accessible via ``_service``.
        grpc_service = getattr(service, "_service", service)
        super().__init__(
            stream_begin_method=grpc_service._event_stream_begin_method,
            target=DatamodelEvents._process_streaming,
            streaming_service=grpc_service,
        )
        self._cbs: dict[str, Callable] = {}
        grpc_service.event_streaming = self
        self._lock = threading.RLock()

    def register_callback(self, tag: str, cb: Callable) -> None:
        """Register a callback for a subscription tag."""
        with self._lock:
            self._cbs[tag] = cb

    def unregister_callback(self, tag: str) -> None:
        """Unregister the callback for a subscription tag."""
        with self._lock:
            self._cbs.pop(tag, None)

    def _process_streaming(self, id, stream_begin_method, started_evt, *args, **kwargs):
        """Process incoming datamodel event responses."""
        from ansys.fluent.core.module_config import config

        responses = self._streaming_service._process_event_streaming(
            *args, id=id, started_evt=started_evt, **kwargs
        )
        while True:
            try:
                response = next(responses)
                if not config.hide_log_secrets:
                    network_logger.debug(
                        f"GRPC_TRACE: RPC = "
                        f"{self._streaming_service._event_streaming_rpc_path}, "
                        f"response = {MessageToDict(response)}"
                    )
                with self._lock:
                    self._streaming = True
                    cb = self._cbs.get(response.tag, None)
                    if cb:
                        event_type, cb_args = (
                            self._streaming_service.parse_event_response(response)
                        )
                        if event_type is not None:
                            cb(*cb_args)
            except StopIteration:
                break
