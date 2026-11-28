# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
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

"""Error classification."""

from _resilient_fakes import FakeAdapter, FakeSession
import pytest

from ansys.fluent.core.resilient.engine.classifier import ErrorClassifier
from ansys.fluent.core.resilient.engine.types import ErrorCategory, Severity

pytestmark = pytest.mark.resilient


@pytest.fixture
def classifier():
    return ErrorClassifier(FakeAdapter())


def test_clean_stop_is_benign_only_for_interruptible_commands(classifier):
    err = RuntimeError("()")
    assert classifier.classify(err, interruptible=True).benign
    assert not classifier.classify(err, interruptible=False).benign


def test_fatal_state_is_catastrophic(classifier):
    session = FakeSession()
    session.error_state.set("fatal", "solver died")
    cls = classifier.classify(RuntimeError("anything"), session)
    assert cls.category is ErrorCategory.FATAL
    assert cls.severity is Severity.CATASTROPHIC
    assert cls.details == "solver died"


def test_fatal_text_on_healthy_session_is_not_catastrophic(classifier):
    cls = classifier.classify(
        RuntimeError("this may cause a fatal error"), FakeSession()
    )
    assert not cls.catastrophic
