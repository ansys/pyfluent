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

"""Error classification and repair proposals."""

from _resilient_fakes import FakeAdapter, FakeLeaf, FakeSession
import pytest

from ansys.fluent.core.resilient.engine import ActivationCandidate, ErrorClasses
from ansys.fluent.core.resilient.engine.classifier import (
    ErrorClassifier,
    make_classification,
)
from ansys.fluent.core.resilient.engine.resolver import RecoverableErrorResolver
from ansys.fluent.core.resilient.engine.types import ErrorCategory, Severity

pytestmark = pytest.mark.resilient


class _Inactive(RuntimeError):
    pass


class _TypedAdapter(FakeAdapter):
    def error_classes(self):
        return ErrorClasses(inactive=_Inactive)


@pytest.fixture
def classifier():
    return ErrorClassifier(_TypedAdapter())


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


def test_unknown_error_from_dead_server_is_catastrophic(classifier):
    session = FakeSession()
    session.serving = False
    cls = classifier.classify(ConnectionError("Socket closed"), session)
    assert cls.catastrophic


def test_unknown_error_from_healthy_server_is_hard(classifier):
    cls = classifier.classify(RuntimeError("something odd"), FakeSession())
    assert cls.category is ErrorCategory.UNKNOWN
    assert cls.severity is Severity.HARD


@pytest.mark.parametrize(
    "message, category",
    [
        ("Value is not in range.", ErrorCategory.OUT_OF_RANGE),
        ("'x' is not an allowed value.", ErrorCategory.WRONG_VALUE),
        ("'a.b' is currently inactive.", ErrorCategory.INACTIVE_TARGET),
        ("object is read-only", ErrorCategory.READ_ONLY),
    ],
)
def test_message_heuristics(classifier, message, category):
    assert classifier.classify(RuntimeError(message)).category is category


def test_typed_errors_take_precedence(classifier):
    assert classifier.classify(_Inactive("x")).category is ErrorCategory.INACTIVE_TARGET
    assert classifier.classify(TypeError("x")).category is ErrorCategory.WRONG_TYPE


def _resolver(session, *, allow=False, candidates=()):
    adapter = FakeAdapter(candidates=candidates)
    return RecoverableErrorResolver(adapter, session, allow_model_activation=allow)


def test_clamp_uses_live_bounds():
    fix = RecoverableErrorResolver.fix_range(FakeLeaf(0, minimum=0, maximum=1), 5.0)
    assert fix.kind == "clamp" and fix.new_value == 1
    assert RecoverableErrorResolver.fix_range(FakeLeaf(0, minimum=0), True) is None


def test_snap_requires_a_close_match():
    leaf = FakeLeaf("laminar", allowed=["laminar", "k-epsilon"])
    assert RecoverableErrorResolver.fix_allowed_value(leaf, "k-epsilo").new_value == (
        "k-epsilon"
    )
    assert RecoverableErrorResolver.fix_allowed_value(leaf, "zzzz") is None


def test_coerce_numeric_strings_only():
    assert RecoverableErrorResolver.fix_type("42").new_value == 42
    assert RecoverableErrorResolver.fix_type("4.5").new_value == 4.5
    assert RecoverableErrorResolver.fix_type("abc") is None


def test_activation_keeps_only_the_candidate_that_activates_the_target():
    session = FakeSession()
    resolver = _resolver(
        session,
        allow=True,
        candidates=[("setup.radiation", True), ("setup.energy", True)],
    )
    target = session.settings.setup.temperature
    activated = resolver.activate(target)
    assert activated == [ActivationCandidate("setup.energy", True)]
    assert session.settings.setup.energy.value is True
    # The candidate that did not help was reverted.
    assert session.settings.setup.radiation.value is False


def test_activation_is_disabled_by_default():
    session = FakeSession()
    resolver = _resolver(session, candidates=[("setup.energy", True)])
    assert resolver.activate(session.settings.setup.temperature) == []
    cls = make_classification(ErrorCategory.INACTIVE_TARGET, "inactive")
    assert resolver.propose("setup.temperature", 350.0, cls) is None
    assert session.settings.setup.energy.value is False


def test_inactive_target_is_detected_whatever_the_message():
    session = FakeSession()
    resolver = _resolver(session, allow=True, candidates=[("setup.energy", True)])
    cls = make_classification(ErrorCategory.WRONG_VALUE, "not allowed")
    fix = resolver.propose("setup.temperature", 350.0, cls)
    assert fix.kind == "activate_model"
    assert session.settings.setup.energy.value is True
