import os
import random

import pytest

from ansys.fluent.core import connect_to_fluent, launch_fluent
from ansys.fluent.core.fluent_connection import _is_localhost


def _get_certs_folder():
    return os.path.join(os.getcwd(), "certs")


def _generate_random_address():
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
        if not _is_localhost(address):
            return address


def test_invalid_launch_arguments():
    with pytest.raises(ValueError):
        launch_fluent()

    assert launch_fluent(certificates_folder=_get_certs_folder()) is not None
    assert launch_fluent(insecure_mode=True) is not None

    with pytest.raises(ValueError):
        launch_fluent(certificates_folder=_get_certs_folder(), insecure_mode=True)


def test_invalid_connect_to_fluent_arguments():
    with pytest.raises(ValueError):
        connect_to_fluent(certificates_folder=_get_certs_folder())

    with pytest.raises(ValueError):
        connect_to_fluent(insecure_mode=True)

    with pytest.raises(ValueError):
        connect_to_fluent(allow_remote_host=True)

    assert (
        connect_to_fluent(
            allow_remote_host=True,
            certificates_folder=_get_certs_folder(),
            address=_generate_random_address(),
        )
        is not None
    )
    assert (
        connect_to_fluent(
            allow_remote_host=True,
            insecure_mode=True,
            address=_generate_random_address(),
        )
        is not None
    )

    with pytest.raises(ValueError):
        connect_to_fluent(
            allow_remote_host=True,
            certificates_folder=_get_certs_folder(),
            insecure_mode=True,
        )
