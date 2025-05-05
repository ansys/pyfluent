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

import grpc

from ansys.api.fluent.v0 import file_transfer_service_pb2 as FileTransferProtoModule
from ansys.api.fluent.v0 import file_transfer_service_pb2_grpc as FileTransferGrpcModule


class FileTransferService:
    """FileTransfer Service."""

    def __init__(self, ip: str, port: str):
        """__init__ method of AppUtilities class."""
        channel = grpc.insecure_channel(f"{ip}:{port}")
        self._stub = FileTransferGrpcModule.FileTransferServiceStub(channel)


class FileTransfer:
    """FileTransferService."""

    def __init__(self, service: FileTransferService, ip: str, port: str):
        """__init__ method of FileTransfer class."""
        self.service = service
        self._ip = ip
        self._port = port

    def start_server(self) -> str:
        """Start server."""
        request = FileTransferProtoModule.StartServerRequest()
        request.ip = self._ip
        request.port = self._port
        self.service._stub.StartServer(request)

    def upload(self, file_path: str) -> dict:
        """Upload file to the server.

        Parameters
        ----------
        file_path : str
            Path to the file to be uploaded.
        """

        def request_generator():
            yield FileTransferProtoModule.FileUploadRequest(
                metadata=FileTransferProtoModule.FileMetaData(
                    name=file_path, type="application/octet-stream"
                )
            )
            with open(file_path, "rb") as f:
                while True:
                    chunk = f.read(1024 * 1024)
                    if not chunk:
                        break
                    yield FileTransferProtoModule.FileUploadRequest(
                        chunk=FileTransferProtoModule.FileChunk(content=chunk)
                    )

        self.service._stub.Upload(request_generator())

    def download(self, remote_file, local_path):
        """Download file from the server.

        Parameters
        ----------
        remote_file : str
            Name of the file to be downloaded.
        local_path : str
            Path to save the downloaded file.
        """
        request = FileTransferProtoModule.FileDownloadRequest(name=remote_file)
        with open(local_path, "wb") as f:
            for resp in self.service._stub.Download(request):
                f.write(resp.content)
