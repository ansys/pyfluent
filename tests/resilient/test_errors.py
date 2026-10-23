# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
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

"""Tests for the error classifier."""

import pytest

from ansys.fluent.core.resilient.errors import ErrorClassifier
from ansys.fluent.core.resilient.types import ErrorCategory, Severity
from tests.resilient._fakes import FakeSession

pytestmark = pytest.mark.resilient


def test_benign_interrupt_sentinel():
    cls = ErrorClassifier().classify(RuntimeError("()"))
    assert cls.category is ErrorCategory.BENIGN_INTERRUPT
    assert cls.severity is Severity.BENIGN
    assert not cls.recoverable and not cls.catastrophic


def test_fatal_state_is_catastrophic():
    session = FakeSession()
    session.go_fatal("solver died")
    cls = ErrorClassifier().classify(RuntimeError("anything"), session)
    assert cls.category is ErrorCategory.FATAL
    assert cls.catastrophic
    assert "solver died" in (cls.details or "")


def test_text_mentioning_fatal_on_healthy_session_is_not_catastrophic():
    # A recoverable/benign message that merely contains the word "fatal" must NOT
    # escalate to a failover when the session's ErrorState is healthy. Only the
    # authoritative ErrorState marks a session fatal.
    session = FakeSession()  # healthy: not fatal
    cls = ErrorClassifier().classify(
        RuntimeError("Warning: this may cause a fatal error during solve"),
        session,
    )
    assert cls.category is not ErrorCategory.FATAL
    assert not cls.catastrophic


def test_text_mentioning_fatal_without_session_is_not_catastrophic():
    # With no session to consult, a "fatal"-containing string still must not be
    # classified catastrophic from text alone.
    cls = ErrorClassifier().classify(RuntimeError("fatal-sounding but benign"))
    assert cls.category is not ErrorCategory.FATAL
    assert not cls.catastrophic


def test_text_heuristics_out_of_range():
    cls = ErrorClassifier().classify(RuntimeError("value is below minimum 0.0"))
    assert cls.category is ErrorCategory.OUT_OF_RANGE
    assert cls.recoverable


def test_text_heuristics_fluent_not_in_range():
    # Fluent's actual wording for a range violation (seen live on v271).
    cls = ErrorClassifier().classify(
        RuntimeError("Value is not in range\nError Object: (0 1)")
    )
    assert cls.category is ErrorCategory.OUT_OF_RANGE
    assert cls.recoverable


def test_text_heuristics_wrong_value():
    cls = ErrorClassifier().classify(RuntimeError("'foo' is not an allowed value"))
    assert cls.category is ErrorCategory.WRONG_VALUE
    assert cls.recoverable


def test_text_heuristics_inactive():
    cls = ErrorClassifier().classify(RuntimeError("the object is not active"))
    assert cls.category is ErrorCategory.INACTIVE_TARGET
    assert cls.recoverable


def test_type_error_is_wrong_type():
    cls = ErrorClassifier().classify(TypeError("expected float"))
    assert cls.category is ErrorCategory.WRONG_TYPE
    assert cls.recoverable


def test_unknown_is_hard():
    cls = ErrorClassifier().classify(RuntimeError("some opaque failure"))
    assert cls.category is ErrorCategory.UNKNOWN
    assert cls.severity is Severity.HARD
    assert not cls.recoverable and not cls.catastrophic


def test_benign_checked_before_fatal():
    # Even on a fatal session, a clean-interrupt sentinel is benign.
    session = FakeSession()
    session.go_fatal()
    cls = ErrorClassifier().classify(RuntimeError("()"), session)
    assert cls.category is ErrorCategory.BENIGN_INTERRUPT


def test_typed_core_errors_classified():
    pytest.importorskip("ansys.fluent.core.solver.flobject")
    from ansys.fluent.core.solver.flobject import (
        InactiveObjectError,
        ReadOnlyActionError,
    )

    classifier = ErrorClassifier()
    assert (
        classifier.classify(InactiveObjectError("x")).category
        is ErrorCategory.INACTIVE_TARGET
    )
    ro = classifier.classify(ReadOnlyActionError("x"))
    assert ro.category is ErrorCategory.READ_ONLY
    assert ro.severity is Severity.HARD
