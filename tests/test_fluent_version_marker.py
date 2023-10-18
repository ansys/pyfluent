import pytest


def test_dev_fluent_any():
    pass


@pytest.mark.fluent_version("latest")
def test_dev_fluent_latest():
    pass


@pytest.mark.fluent_version(">=24.1")
def test_dev_fluent_ge_241():
    pass


@pytest.mark.fluent_version(">=23.2")
def test_dev_fluent_ge_232():
    pass


@pytest.mark.fluent_version(">=23.1")
def test_dev_fluent_ge_231():
    pass


@pytest.mark.fluent_version(">=22.2")
def test_dev_fluent_ge_222():
    pass


@pytest.mark.nightly
def test_nightly_fluent_any():
    pass


@pytest.mark.nightly
@pytest.mark.fluent_version("latest")
def test_nightly_fluent_latest():
    pass


@pytest.mark.nightly
@pytest.mark.fluent_version(">=24.1")
def test_nightly_fluent_ge_241():
    pass


@pytest.mark.nightly
@pytest.mark.fluent_version(">=23.2")
def test_nightly_fluent_ge_232():
    pass


@pytest.mark.nightly
@pytest.mark.fluent_version(">=23.1")
def test_nightly_fluent_ge_231():
    pass


@pytest.mark.nightly
@pytest.mark.fluent_version(">=22.2")
def test_nightly_fluent_ge_222():
    pass
