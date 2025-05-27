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

"""Provides a module for streaming services."""

import itertools
import logging
import threading
from typing import Callable

logger = logging.getLogger("pyfluent.networking")


class StreamingService:
    """Encapsulates a Fluent streaming service."""

    _service_id = itertools.count()

    def __init__(self, stream_begin_method, target, streaming_service):
        """__init__ method of StreamingService class."""
        self._lock: threading.RLock = threading.RLock()
        self._streaming: bool = False
        self._id = f"stream-{next(StreamingService._service_id)}"
        self._stream_begin_method = stream_begin_method
        self._target = target
        self._streaming_service = streaming_service
        self._stream_thread: threading.Thread | None = None
        self._service_callback_id = itertools.count()
        self._service_callbacks: dict = {}

    @property
    def is_streaming(self):
        """Checks whether it is streaming."""
        with self._lock:
            return self._streaming

    def register_callback(self, callback: Callable, *args, **kwargs) -> str:
        """Register the callback.

        Parameters
        ----------
        callback : Callable
            Callback to register.
        args : Any
            Arguments.
        kwargs : Any
            Keyword arguments.

        Returns
        -------
        str
            Registered callback ID.
        """
        with self._lock:
            callback_id = f"{next(self._service_callback_id)}"
            self._service_callbacks[callback_id] = [callback, args, kwargs]
            return callback_id

    def unregister_callback(self, callback_id: str):
        """Unregister the callback.

        Parameters
        ----------
        callback_id : str
            ID of the registered callback.
        """
        with self._lock:
            if callback_id in self._service_callbacks:
                del self._service_callbacks[callback_id]

    def start(self, *args, **kwargs) -> None:
        """Start streaming."""
        with self._lock:
            if not self.is_streaming:
                self._prepare()
                started_evt = threading.Event()
                self._stream_thread = threading.Thread(
                    target=self._target,
                    args=(
                        self,
                        self._id,
                        self._stream_begin_method,
                        started_evt,
                        *args,
                    ),
                    kwargs=kwargs,
                )
                self._stream_thread.start()
                started_evt.wait()
                self._streaming = True

    def stop(self) -> None:
        """Stop streaming."""
        if self.is_streaming:
            self._streaming_service.end_streaming(self._id, self._stream_begin_method)
            self._stream_thread.join(timeout=5)
            if self._stream_thread.is_alive():
                logger.warning(f"Streaming service {self._id} is unresponsive.")
            self._streaming = False
            self._stream_thread = None

    def _prepare(self):
        pass  # Currently only used by monitor services.
