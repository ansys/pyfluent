import pytest

from ansys.fluent.core.utils.fluent_version import AnsysVersionNotFound, FluentVersion


def test_examples():
    assert FluentVersion("23.2.0") == FluentVersion.v232
    assert FluentVersion.v232.number == 232
    assert FluentVersion.v232.awp_var == "AWP_ROOT232"
    assert FluentVersion.v232.name == "v232"
    assert FluentVersion.v232.value == "23.2.0"


def test_version_found():
    assert FluentVersion("23.2") == FluentVersion.v232
    assert FluentVersion(23.2) == FluentVersion.v232
    assert FluentVersion(232) == FluentVersion.v232


def test_version_not_found():
    with pytest.raises(AnsysVersionNotFound):
        FluentVersion("25.3.0")

    with pytest.raises(AnsysVersionNotFound):
        FluentVersion(22)


def test_get_latest_installed(helpers):
    helpers.mock_awp_vars()
    assert FluentVersion.get_latest_installed() == FluentVersion.current_release()


def test_gt():
    assert FluentVersion.v232 > FluentVersion.v231
    assert FluentVersion.v232 > FluentVersion.v222


def test_ge():
    assert FluentVersion.v232 >= FluentVersion.v232
    assert FluentVersion.v232 >= FluentVersion.v231
    assert FluentVersion.v232 >= FluentVersion.v222


def test_lt():
    assert FluentVersion.v232 < FluentVersion.v242
    assert FluentVersion.v232 < FluentVersion.v241


def test_le():
    assert FluentVersion.v232 <= FluentVersion.v232
    assert FluentVersion.v232 <= FluentVersion.v242
    assert FluentVersion.v232 <= FluentVersion.v241


def test_ne():
    assert FluentVersion.v232 != FluentVersion.v242


def test_eq():
    assert FluentVersion.v232 == FluentVersion.v232
    assert FluentVersion.v241 == FluentVersion.v241


def test_str_output():
    assert str(FluentVersion.v232) == "Fluent version 2023 R2"
    assert str(FluentVersion.v251) == "Fluent version 2025 R1"
