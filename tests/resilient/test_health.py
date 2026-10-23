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

"""Tests for the session health monitor."""

import time

import pytest

from ansys.fluent.core.resilient.health import SessionHealthMonitor
from tests.resilient._fakes import FakeSession

pytestmark = pytest.mark.resilient


def test_callback_marks_fatal():
    session = FakeSession()
    monitor = SessionHealthMonitor(session, interval=100.0)
    monitor.start()
    try:
        assert not monitor.is_fatal()
        # Simulate the server flipping fatal, then firing the event.
        session.go_fatal("solver crash")
        session.events.fire(type("Info", (), {"message": "solver crash"})())
        assert monitor.is_fatal()
        assert monitor.details() == "solver crash"
        assert not monitor.is_healthy()
    finally:
        monitor.stop()


def test_poll_backstop_detects_fatal():
    session = FakeSession()
    monitor = SessionHealthMonitor(session, interval=0.05)
    monitor.start()
    try:
        session.go_fatal("silent death")  # no event fired -> poll must catch it
        deadline = time.time() + 2.0
        while time.time() < deadline and not monitor.is_fatal():
            time.sleep(0.05)
        assert monitor.is_fatal()
    finally:
        monitor.stop()


def test_fatal_is_sticky():
    session = FakeSession()
    monitor = SessionHealthMonitor(session, interval=100.0)
    monitor.start()
    try:
        session.go_fatal("first")
        session.events.fire(type("Info", (), {"message": "first"})())
        session._error_state.clear()  # even if cleared, monitor stays fatal
        assert monitor.is_fatal()
    finally:
        monitor.stop()
