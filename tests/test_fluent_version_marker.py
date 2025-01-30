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
