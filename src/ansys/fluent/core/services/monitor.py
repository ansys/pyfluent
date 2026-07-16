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

"""Wrapper over the monitor gRPC service of Fluent."""


class Monitor:
    """Monitor backed by the Monitor gRPC service."""

    def __init__(self, service):
        """Initialize Monitor."""
        self.service = service

    def get_monitors_info(self) -> dict:
        """Get monitors information.

        Parameters
        ----------
        None

        Returns
        -------
        dict
            Dictionary containing the monitors information.
        """
        return self.service.get_monitors_info()

    def begin_streaming(self, request, started_evt, id, stream_begin_method):
        """Begin streaming from Fluent."""
        return self.service.begin_streaming(
            request, started_evt, id=id, stream_begin_method=stream_begin_method
        )

    def end_streaming(self, id, stream_begin_method) -> None:
        """End streaming from Fluent."""
        self.service.end_streaming(id, stream_begin_method)
