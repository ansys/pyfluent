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

"""Provides a module for datamodel streaming."""

import logging

from ansys.fluent.core.module_config import config
from ansys.fluent.core.streaming_services.streaming import StreamingService

network_logger: logging.Logger = logging.getLogger("pyfluent.networking")


class DatamodelStream(StreamingService):
    """Encapsulates a datamodel streaming service."""

    def __init__(self, service):
        """Initialize DatamodelStream."""
        grpc_service = getattr(service, "_service", service)
        super().__init__(
            stream_begin_method="BeginStreaming",
            target=DatamodelStream._process_streaming,
            streaming_service=grpc_service,
        )

    def _process_streaming(
        self,
        id,
        stream_begin_method,
        started_evt,
        rules,
        no_commands_diff_state,
        *args,
        **kwargs,
    ):
        """Processes datamodel events."""
        responses = self._streaming_service._process_streaming(
            *args,
            id=id,
            stream_begin_method=stream_begin_method,
            started_evt=started_evt,
            rules=rules,
            datamodel_return_state_changes=config.datamodel_return_state_changes,
            no_commands_diff_state=no_commands_diff_state,
            **kwargs,
        )
        while True:
            try:
                response = next(responses)
                network_logger.debug(
                    "GRPC_TRACE: RPC = /grpcRemoting.DataModel/BeginStreaming."
                )
                with self._lock:
                    self._streaming = True
                    for _, cb_list in self._service_callbacks.items():
                        state, deleted_paths = (
                            self._streaming_service.parse_streaming_response(response)
                        )
                        cb_list[0](state=state, deleted_paths=deleted_paths)
            except StopIteration:
                break
