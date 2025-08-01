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

import pytest

from ansys.fluent.core.utils.fluent_version import (
    AnsysVersionNotFound,
    FluentVersion,
    all_versions,
    between,
    except_for,
    only_at,
    since,
    until,
)


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


def test_get_latest_installed(helpers, fs):
    helpers.mock_awp_vars()
    with pytest.raises(FileNotFoundError):
        assert FluentVersion.get_latest_installed() == FluentVersion.current_release()
    fs.create_file(FluentVersion.current_release().get_fluent_exe_path())
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
    assert str(FluentVersion.v232) == "Ansys Fluent 2023 R2"
    assert str(FluentVersion.v251) == "Ansys Fluent 2025 R1"


def test_fluent_version_set():
    set0 = all_versions()
    set1 = since(FluentVersion.v232)
    set2 = until(FluentVersion.v232)
    set3 = only_at(FluentVersion.v232)
    set4 = except_for(FluentVersion.v232)
    set5 = between(FluentVersion.v231, FluentVersion.v241)
    assert FluentVersion.v232 in set1
    assert FluentVersion.v232 not in set2
    assert FluentVersion.v232 in set3
    assert FluentVersion.v232 not in set4
    assert set4 - set2 == set1 - set3
    assert set1 | set2 == set3 | set4 == set0
    assert set1 & set4 == set1 - set3
    assert set1 > set4 - set2
    assert len(set5) == 2
    assert set5 == since(FluentVersion.v231) & until(FluentVersion.v241)
    d = {}
    d[set1] = "test"
    assert set1 in d
