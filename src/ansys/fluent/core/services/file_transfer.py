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

"""This module provides a class to handle file transfer operations."""

import os
from pathlib import Path
from typing import List, Tuple

import grpc

from ansys.api.fluent.v0 import file_transfer_service_pb2 as FileTransferProtoModule
from ansys.api.fluent.v0 import file_transfer_service_pb2_grpc as FileTransferGrpcModule


class FileTransferService:
    """FileTransfer Service."""

    def __init__(self, channel: grpc.Channel, metadata: List[Tuple[str, str]]):
        """__init__ method of AppUtilities class."""
        from ansys.fluent.core.services.interceptors import GrpcErrorInterceptor

        intercept_channel = grpc.intercept_channel(
            channel,
            GrpcErrorInterceptor(),
        )
        self._stub = FileTransferGrpcModule.FileTransferServiceStub(intercept_channel)
        self._metadata = metadata

    def upload(
        self, request: FileTransferProtoModule.FileUploadRequest
    ) -> FileTransferProtoModule.FileUploadResponse:
        """Upload file RPC of FileTransfer service."""
        return self._stub.Upload(request, metadata=self._metadata)

    def download(
        self, request: FileTransferProtoModule.FileDownloadRequest
    ) -> FileTransferProtoModule.FileDownloadResponse:
        """Download file RPC of FileTransfer service."""
        return self._stub.Download(request, metadata=self._metadata)


class FileTransfer:
    """FileTransferService."""

    def __init__(self, service: FileTransferService):
        """__init__ method of FileTransfer class."""
        self._service = service

    def upload(self, file_path: str) -> None:
        """Upload file to the server.

        Parameters
        ----------
        file_path : str
            Path to the file to be uploaded.
        Returns
        -------
        dict
            Server response or error message.
        """
        if not Path(file_path).exists():
            print(f"File '{file_path}' does not exist.")
            return

        def request_generator(file_path):
            filename_only = Path(file_path).name
            yield FileTransferProtoModule.FileUploadRequest(name=filename_only)
            with open(file_path, "rb") as file:
                while True:
                    chunk = file.read(1024)
                    if not chunk:
                        break
                    yield FileTransferProtoModule.FileUploadRequest(chunk=chunk)

        self._service.upload(request_generator(file_path))

    def download(self, remote_file: str, local_path: str | None = None) -> None:
        """Download file from the server.

        Parameters
        ----------
        remote_file : str
            Name of the file to be downloaded.
        local_path : str
            Path to save the downloaded file.
        """
        request = FileTransferProtoModule.FileDownloadRequest(name=remote_file)
        response_stream = self._service.download(request)
        path = local_path if local_path else Path(os.getcwd()) / remote_file
        with open(path, "wb") as file:
            for response in response_stream:
                file.write(response.chunk)
