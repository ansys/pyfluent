import os

import pytest

from ansys.fluent.core.launcher.launcher import connect_to_fluent, launch_fluent


def _get_certs_folder():
    return os.path.join(os.getcwd(), "certs")


def _get_address_and_password(solver):
    address = solver._fluent_connection._channel_str
    password = solver._fluent_connection._metadata[0][1]
    return address, password


def test_invalid_launch_arguments():
    with pytest.raises(ValueError):
        launch_fluent()

    assert launch_fluent(certificates_folder=_get_certs_folder()) is not None
    assert launch_fluent(insecure_mode=True) is not None

    with pytest.raises(ValueError):
        launch_fluent(certificates_folder=_get_certs_folder(), insecure_mode=True)


def test_invalid_connect_to_fluent_arguments():
    solver = launch_fluent(certificates_folder=_get_certs_folder())
    address_and_password = dict(
        zip(["address", "password"], _get_address_and_password(solver))
    )
    insecure_solver = launch_fluent(insecure_mode=True)
    insecure_address_and_password = dict(
        zip(["address", "password"], _get_address_and_password(insecure_solver))
    )
    with pytest.raises(ValueError):
        connect_to_fluent(
            certificates_folder=_get_certs_folder(), **address_and_password
        )

    with pytest.raises(ValueError):
        connect_to_fluent(insecure_mode=True, **insecure_address_and_password)

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

    assert (
        connect_to_fluent(
            allow_remote_host=True,
            insecure_mode=True,
            inside_container=True,
            **insecure_address_and_password,
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
