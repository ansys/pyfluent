import os

import pytest

from ansys.fluent.core import launch_fluent


def _get_certs_folder():
    return os.path.join(os.getcwd(), "certs")


def test_invalid_launch_arguments():
    with pytest.raises(ValueError):
        launch_fluent()

    assert launch_fluent(certificates_folder=_get_certs_folder()) is not None
    assert launch_fluent(insecure_mode=True) is not None

    with pytest.raises(ValueError):
        launch_fluent(certificates_folder=_get_certs_folder(), insecure_mode=True)
