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

"""Script to test viability of gRPC connection in the current machine."""


from argparse import ArgumentParser
import socket

import grpc
from grpc_health.v1 import health_pb2, health_pb2_grpc

from ansys.fluent.core.utils.networking import _GrpcServer, get_free_port


def _test_connection_using_specified_ip(ip: str, port: int | None = None) -> bool:
    if not port:
        port = get_free_port()
    address = f"{ip}:{port}"
    try:
        with _GrpcServer(address):
            with grpc.insecure_channel(address) as channel:
                stub = health_pb2_grpc.HealthStub(channel)
                return (
                    stub.Check(
                        health_pb2.HealthCheckRequest(),
                        timeout=1,
                    ).status
                    == health_pb2.HealthCheckResponse.ServingStatus.SERVING
                )
    except Exception:
        return False


def _test_connection_using_all_available_ips(port: int | None = None) -> list[str]:
    successful_ips = []
    for addrinfo in socket.getaddrinfo(
        "localhost",
        0,
        family=socket.AF_INET,
        type=socket.SOCK_STREAM,
        flags=socket.AI_PASSIVE,
    ):
        ip = addrinfo[-1][0]
        if _test_connection_using_specified_ip(ip, port):
            successful_ips.append(ip)
    return successful_ips


def test_connection(ip: str | None = None, port: int | None = None):
    """
    Test viability of gRPC connection in the current machine.
    Parameters
    ----------
    ip : str, optional
        IP address to test connection with. If not provided, will test using all available ips.
    port : int, optional
        Port to test connection with. If not provided, will test using random port.
    """

    if ip is not None and port is not None:
        print(f"Testing gRPC connection using ip={ip} and port={port}.")
        if _test_connection_using_specified_ip(ip, port):
            print(f"gRPC connection can be established using ip={ip} and port={port}.")
        else:
            print(
                f"gRPC connection cannot be established using ip={ip} and port={port}. "
                "Try with a different ip and/or port. You can run the script again without "
                "providing any ip to print all viable ips where gRPC connection can be established."
            )
    elif ip is not None and port is None:
        print(f"Testing gRPC connection using ip={ip} and random port.")
        if _test_connection_using_specified_ip(ip):
            print(f"gRPC connection can be established using ip={ip}.")
        else:
            print(
                f"gRPC connection cannot be established using ip={ip}. "
                "Try with a different ip. You can run the script again without "
                "providing any ip to print all viable ips where gRPC connection can be established."
            )
    elif ip is None and port is not None:
        print(f"Testing gRPC connection using all available ips and port={port}.")
        successful_ips = _test_connection_using_all_available_ips(port)
        if successful_ips:
            for ip in successful_ips:
                print(
                    f"gRPC connection can be established using ip={ip} and port={port}."
                )
        else:
            print(
                f"gRPC connection cannot be established using any ip and port={port}. "
                "Try with a different port. You can run the script again without "
                "providing any port to test using random port."
            )
    else:
        print("Testing gRPC connection using all available ips and random port.")
        successful_ips = _test_connection_using_all_available_ips()
        if successful_ips:
            for ip in successful_ips:
                print(f"gRPC connection can be established using ip={ip}.")
        else:
            print("gRPC connection cannot be established using any ip.")


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Script to test viability of gRPC connection in the current machine."
    )
    parser.add_argument(
        "-i",
        "--ip",
        help="IP address to test connection with. If not provided, will test using all available ips.",
    )
    parser.add_argument(
        "-p",
        "--port",
        help="Port to test connection with. If not provided, will test using random port.",
    )
    args = parser.parse_args()
    test_connection(args.ip, args.port)
