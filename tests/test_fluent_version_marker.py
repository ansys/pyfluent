import pytest


def test_dev_fluent_any():
    pass


@pytest.mark.fluent_version(">=24.1")
def test_dev_fluent_gt_241():
    pass


@pytest.mark.fluent_version(">=23.2")
def test_dev_fluent_gt_232():
    pass


@pytest.mark.fluent_version(">=23.1")
def test_dev_fluent_gt_231():
    pass


@pytest.mark.fluent_version(">=22.2")
def test_dev_fluent_gt_222():
    pass


@pytest.mark.nightly
def test_nightly_fluent_any():
    pass


@pytest.mark.nightly
@pytest.mark.fluent_version(">=24.1")
def test_nightly_fluent_gt_241():
    pass


@pytest.mark.nightly
@pytest.mark.fluent_version(">=23.2")
def test_nightly_fluent_gt_232():
    pass


@pytest.mark.nightly
@pytest.mark.fluent_version(">=23.1")
def test_nightly_fluent_gt_231():
    pass


@pytest.mark.nightly
@pytest.mark.fluent_version(">=22.2")
def test_nightly_fluent_gt_222():
    pass
