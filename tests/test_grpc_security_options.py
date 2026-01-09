import os
import random

import pytest

from ansys.fluent.core.launcher.launcher import connect_to_fluent, launch_fluent
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
        if not is_localhost(address):
            return address


def test_launch_arguments():
    with pytest.raises(ValueError):
        launch_fluent()

    assert launch_fluent(certificates_folder=_get_certs_folder()) is not None
    assert launch_fluent(insecure_mode=True) is not None

    with pytest.raises(ValueError):
        launch_fluent(certificates_folder=_get_certs_folder(), insecure_mode=True)


def test_connect_to_fluent_arguments():
    solver = launch_fluent(certificates_folder=_get_certs_folder())
    address_and_password = dict(
        zip(["address", "password"], _get_address_and_password(solver))
    )
    with pytest.raises(ValueError):
        connect_to_fluent(
            certificates_folder=_get_certs_folder(), **address_and_password
        )

    with pytest.raises(ValueError):
        connect_to_fluent(insecure_mode=True, **address_and_password)

    with pytest.raises(ValueError):
        connect_to_fluent(allow_remote_host=True, **address_and_password)

    assert (
        connect_to_fluent(
            allow_remote_host=True,
            certificates_folder=_get_certs_folder(),
            **address_and_password,
        )
        is not None
    )

    with pytest.raises(ValueError):
        connect_to_fluent(
            allow_remote_host=True,
            certificates_folder=_get_certs_folder(),
            insecure_mode=True,
            **address_and_password,
        )


def test_allowed_ips():
    with pytest.raises(ValueError):
        connect_to_fluent(
            address=_generate_random_remote_address(),
        )

    with pytest.raises(ValueError):
        connect_to_fluent(
            address="localhost:5000",
            insecure_mode=True,
        )

    with pytest.raises(ValueError):
        connect_to_fluent(
            address="localhost:5000",
            allow_remote_host=True,
        )
