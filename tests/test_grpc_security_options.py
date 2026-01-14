# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
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

import os
import random

import grpc
import pytest

from ansys.fluent.core.launcher.error_warning_messages import (
    ALLOW_REMOTE_HOST_NOT_PROVIDED_IN_REMOTE,
    ALLOW_REMOTE_HOST_NOT_PROVIDED_WITH_CERTIFICATES_FOLDER,
    ALLOW_REMOTE_HOST_NOT_PROVIDED_WITH_INSECURE_MODE,
    BOTH_CERTIFICATES_FOLDER_AND_INSECURE_MODE_PROVIDED,
    CERTIFICATES_FOLDER_NOT_PROVIDED_AT_CONNECT,
    CERTIFICATES_FOLDER_NOT_PROVIDED_AT_LAUNCH,
    CONNECTING_TO_LOCALHOST_INSECURE_MODE,
    INSECURE_MODE_WARNING,
)
from ansys.fluent.core.launcher.launcher import connect_to_fluent, launch_fluent
from ansys.fluent.core.pyfluent_warnings import InsecureGrpcWarning
from ansys.fluent.core.utils.networking import is_localhost


def _get_certs_folder():
    return os.path.join(os.getcwd(), "certs")


def _get_address_and_password(solver):
    address = solver._fluent_connection._channel_str
    password = solver._fluent_connection._metadata[0][1]
    return address, password


def _generate_random_remote_address():
    while True:
        octets = [
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        ]
        ip = ".".join(map(str, octets))
        port = random.randint(1024, 65535)
        address = f"{ip}:{port}"
        if not is_localhost(ip):
            return address


def test_launch_arguments(monkeypatch):
    with pytest.raises(ValueError, match=CERTIFICATES_FOLDER_NOT_PROVIDED_AT_LAUNCH):
        launch_fluent()

    with monkeypatch.context() as m:
        m.setenv("ANSYS_GRPC_CERTIFICATES", _get_certs_folder())
        assert launch_fluent() is not None

    assert launch_fluent(certificates_folder=_get_certs_folder()) is not None
    assert launch_fluent(insecure_mode=True) is not None

    with pytest.raises(
        ValueError, match=BOTH_CERTIFICATES_FOLDER_AND_INSECURE_MODE_PROVIDED
    ):
        launch_fluent(certificates_folder=_get_certs_folder(), insecure_mode=True)


def test_connect_to_fluent_arguments():
    solver = launch_fluent(certificates_folder=_get_certs_folder())
    address_and_password = dict(
        zip(["address", "password"], _get_address_and_password(solver))
    )
    with pytest.raises(
        ValueError, match=ALLOW_REMOTE_HOST_NOT_PROVIDED_WITH_CERTIFICATES_FOLDER
    ):
        connect_to_fluent(
            certificates_folder=_get_certs_folder(), **address_and_password
        )

    with pytest.raises(
        ValueError, match=ALLOW_REMOTE_HOST_NOT_PROVIDED_WITH_INSECURE_MODE
    ):
        connect_to_fluent(insecure_mode=True, **address_and_password)

    with pytest.raises(ValueError, match=CERTIFICATES_FOLDER_NOT_PROVIDED_AT_CONNECT):
        connect_to_fluent(allow_remote_host=True, **address_and_password)

    assert (
        connect_to_fluent(
            allow_remote_host=True,
            certificates_folder=_get_certs_folder(),
            **address_and_password,
        )
        is not None
    )

    with pytest.raises(
        ValueError, match=BOTH_CERTIFICATES_FOLDER_AND_INSECURE_MODE_PROVIDED
    ):
        connect_to_fluent(
            allow_remote_host=True,
            certificates_folder=_get_certs_folder(),
            insecure_mode=True,
            **address_and_password,
        )


def test_allowed_ips():
    with pytest.raises(ValueError, match=ALLOW_REMOTE_HOST_NOT_PROVIDED_IN_REMOTE):
        connect_to_fluent(
            address=_generate_random_remote_address(),
        )

    with pytest.raises(RuntimeError, match=CONNECTING_TO_LOCALHOST_INSECURE_MODE):
        connect_to_fluent(
            address="localhost:5000",
            allow_remote_host=True,
            insecure_mode=True,
        )


def test_insecure_mode_warning():
    with pytest.warns(InsecureGrpcWarning, match=INSECURE_MODE_WARNING):
        with pytest.raises(RuntimeError) as ex:
            connect_to_fluent(
                allow_remote_host=True,
                insecure_mode=True,
                address=_generate_random_remote_address(),
            )
        assert isinstance(ex.value.__context__, grpc.RpcError)
        assert ex.value.__context__.code() == grpc.StatusCode.UNAVAILABLE
