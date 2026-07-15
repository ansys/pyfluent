# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

"""Test suite for timeout_loop function validation and behavior.

This module tests the timeout_loop utility function to ensure:
1. Invalid inputs (non-callables) are rejected with helpful error messages
2. Valid callables (method references, functions, lambdas) work correctly
3. Timeout behavior functions as expected
4. Issue #3680 is fixed - no more silent hangs

The tests verify that passing method call results (e.g., session.is_active())
raises InvalidArgument instead of causing silent hangs.
"""

import time

import pytest

from ansys.fluent.core.exceptions import InvalidArgument
from ansys.fluent.core.utils.execution import timeout_loop


class MockSession:
    """Mock Fluent session for testing timeout_loop behavior.

    Simulates a session with is_active() method that transitions from
    active to inactive state after a certain number of calls.

    Attributes
    ----------
    is_serving : bool
        Whether session is serving (always True for mock)
    check_count : int
        Number of times is_active() has been called
    """

    def __init__(self):
        """Initialize mock session with active state."""
        self.is_serving = True
        self.check_count = 0

    def is_active(self):
        """Check if session is active.

        Returns False after 3 calls, simulating a session becoming inactive.

        Returns
        -------
        bool
            True if session is active (check_count < 3), False otherwise
        """
        self.check_count += 1
        return self.check_count < 3


class TestTimeoutLoopInputValidation:
    """Test input validation for timeout_loop function.

    Verifies that timeout_loop rejects invalid inputs with helpful error
    messages instead of silently hanging.
    """

    def test_rejects_non_callable_method_call_result(self):
        """Test that passing method call result (not reference) raises error.

        This test addresses Issue #3680 where users accidentally passed
        session.is_active() instead of session.is_active, causing hangs.

        Raises
        ------
        InvalidArgument
            When non-callable (boolean) is passed
        """
        session = MockSession()

        # INCORRECT: Passing method call result (boolean)
        with pytest.raises(
            InvalidArgument,
            match=".*must be callable.*Did you accidentally call the method.*",
        ):
            timeout_loop(session.is_active(), 2.0, expected="falsy")

    def test_error_message_contains_helpful_guidance(self):
        """Test error message provides clear guidance on correct usage.

        Error message should:
        - Identify problem (parameter not callable)
        - Show type that was passed
        - Suggest correct approach (method reference or lambda)
        - Provide examples
        """
        session = MockSession()

        with pytest.raises(InvalidArgument) as exc_info:
            timeout_loop(session.is_active(), 2.0, expected="falsy")

        error_msg = str(exc_info.value)
        # Verify all helpful elements are in error message
        assert "callable" in error_msg
        assert "bool" in error_msg
        assert "session.is_active" in error_msg
        assert "lambda" in error_msg

    def test_rejects_string_as_non_callable(self):
        """Test that string values are rejected (not callable)."""
        with pytest.raises(InvalidArgument, match=".*must be callable.*str.*"):
            timeout_loop("not_a_function", 1.0)

    def test_rejects_none_as_non_callable(self):
        """Test that None value is rejected (not callable)."""
        with pytest.raises(InvalidArgument, match=".*must be callable.*NoneType.*"):
            timeout_loop(None, 1.0)

    def test_rejects_integer_as_non_callable(self):
        """Test that integer values are rejected (not callable)."""
        with pytest.raises(InvalidArgument, match=".*must be callable.*int.*"):
            timeout_loop(42, 1.0)

    def test_rejects_boolean_as_non_callable(self):
        """Test that boolean values are rejected (not callable)."""
        with pytest.raises(InvalidArgument, match=".*must be callable.*bool.*"):
            timeout_loop(True, 1.0)


class TestTimeoutLoopCorrectUsage:
    """Test correct usage patterns for timeout_loop function."""

    def test_method_reference_pattern(self):
        """Test timeout_loop with method reference (recommended pattern).

        Pattern:
            timeout_loop(session.is_active, timeout, expected="falsy")

        Note: No parentheses after method name. This is the simplest and
        most efficient pattern.
        """
        session = MockSession()

        result = timeout_loop(session.is_active, 5.0, expected="falsy")

        # Should complete successfully and return falsy value
        assert result is False
        # Should have called is_active multiple times
        assert session.check_count >= 3

    def test_lambda_pattern_with_method_call(self):
        """Test timeout_loop using lambda to wrap method call.

        Pattern:
            timeout_loop(lambda: session.is_active(), timeout, expected="falsy")

        Useful for:
        - Complex conditions
        - Method calls with arguments
        - Arbitrary expressions
        """
        session = MockSession()

        result = timeout_loop(lambda: session.is_active(), 5.0, expected="falsy")

        # Should complete successfully and return falsy value
        assert result is False
        # Should have called is_active multiple times
        assert session.check_count >= 3

    def test_lambda_pattern_with_complex_condition(self):
        """Test lambda pattern with more complex condition.

        Shows flexibility of lambda for any condition:
        timeout_loop(lambda: obj.value > 10, ...)
        """

        class Counter:
            def __init__(self):
                self.value = 0

            def increment(self):
                self.value += 1
                return self.value

        counter = Counter()

        # Should succeed - counter will reach 10 within timeout
        result = timeout_loop(lambda: counter.increment() >= 10, 5.0, expected="truthy")

        assert result is True
        assert counter.value >= 10

    def test_function_reference_pattern(self):
        """Test timeout_loop with regular function reference.

        Pattern:
            def check_status():
                return session.is_active()

            timeout_loop(check_status, timeout, expected="falsy")

        Useful for:
        - Reusable check functions
        - Complex logic that doesn't fit in lambda
        - Named functions for clarity
        """
        session = MockSession()

        def check_status():
            """Custom function to check session status."""
            return session.is_active()

        result = timeout_loop(check_status, 5.0, expected="falsy")

        assert result is False
        assert session.check_count >= 3

    def test_with_args_and_kwargs(self):
        """Test timeout_loop passing args and kwargs to callable.

        Args and kwargs are passed to the callable on each iteration:
        timeout_loop(func, timeout, args=(val1,), kwargs={'key': val2})
        """

        def compare(x, y=0):
            """Compare two values."""
            return x > y

        # Should succeed immediately - 5 > 2 is True
        result = timeout_loop(
            compare, 2.0, args=(5,), kwargs={"y": 2}, expected="truthy"
        )

        assert result is True


class TestTimeoutLoopBehavior:
    """Test timeout_loop behavior with different conditions and parameters."""

    def test_immediate_success_returns_quickly(self):
        """Test that satisfied condition returns immediately.

        If condition is satisfied on first check, should return immediately
        without waiting for timeout.
        """

        def always_false():
            return False

        start = time.time()
        result = timeout_loop(always_false, 5.0, expected="falsy")
        elapsed = time.time() - start

        # Should return the falsy value
        assert result is False
        # Should return quickly (within idle_period), not wait for timeout
        assert elapsed < 0.5

    def test_timeout_returns_opposite_of_expected(self):
        """Test timeout returns opposite of expected condition.

        When timeout elapses without condition being met:
        - If expecting 'truthy' and gets falsy -> returns False
        - If expecting 'falsy' and gets truthy -> returns True
        """

        def always_true():
            return True

        start = time.time()
        # Expecting falsy but always gets truthy - should timeout
        result = timeout_loop(always_true, 1.0, expected="falsy")
        elapsed = time.time() - start

        # Returns opposite of expected (True instead of False)
        assert result is True
        # Waited approximately the timeout duration
        assert elapsed >= 1.0
        assert elapsed < 1.5  # Allow some tolerance

    def test_custom_idle_period_affects_frequency(self):
        """Test that custom idle_period controls check frequency.

        Smaller idle_period means more frequent checks, more iterations.
        Larger idle_period means fewer, less frequent checks.
        """
        call_count = 0

        def counter():
            nonlocal call_count
            call_count += 1
            return False  # Never truthy, will timeout

        # With small idle_period=0.05 and timeout=0.5
        timeout_loop(counter, 0.5, idle_period=0.05, expected="truthy")

        # With idle_period=0.05 and timeout=0.5, expect ~10 iterations
        # Allow tolerance due to system timing variations
        assert call_count >= 8

    def test_truthy_expectation(self):
        """Test timeout_loop with expected='truthy'."""
        call_count = 0

        def counter():
            nonlocal call_count
            call_count += 1
            return call_count >= 2

        result = timeout_loop(counter, 5.0, expected="truthy")

        assert result is True
        assert call_count == 2

    def test_falsy_expectation(self):
        """Test timeout_loop with expected='falsy'."""
        call_count = 0

        def counter():
            nonlocal call_count
            call_count += 1
            return call_count < 3

        result = timeout_loop(counter, 5.0, expected="falsy")

        assert result is False
        assert call_count == 3


class TestTimeoutLoopErrorConditions:
    """Test error conditions and invalid parameter combinations."""

    def test_invalid_expected_parameter(self):
        """Test that invalid 'expected' value raises error.

        Expected must be exactly 'truthy' or 'falsy', nothing else.
        """

        def dummy():
            return True

        with pytest.raises(InvalidArgument, match="expected.*truthy.*falsy"):
            timeout_loop(dummy, 1.0, expected="invalid")

    def test_invalid_expected_empty_string(self):
        """Test that empty string for expected raises error."""

        def dummy():
            return True

        with pytest.raises(InvalidArgument, match="expected.*truthy.*falsy"):
            timeout_loop(dummy, 1.0, expected="")

    def test_callable_builtin_functions(self):
        """Test that built-in callables work correctly."""

        def is_positive():
            return True

        # Built-in function should work
        result = timeout_loop(is_positive, 1.0, expected="truthy")
        assert result is True

    def test_callable_class_method(self):
        """Test that class methods work as callable."""

        class MyClass:
            def __init__(self):
                self.count = 0

            def check(self):
                self.count += 1
                return self.count >= 2

        obj = MyClass()
        result = timeout_loop(obj.check, 2.0, expected="truthy")
        assert result is True
        assert obj.count >= 2


class TestTimeoutLoopIssue3680Fix:
    """Tests specifically for Issue #3680 fix verification."""

    def test_issue_3680_silent_hang_prevented(self):
        """Verify Issue #3680 fix prevents silent hangs.

        Before fix: Passing session.is_active() would cause silent hang
        After fix: Raises InvalidArgument with helpful error message
        """
        session = MockSession()

        with pytest.raises(InvalidArgument) as exc_info:
            timeout_loop(
                session.is_active(),  # WRONG - method call
                5.0,
                expected="falsy",
            )

        # Verify error is caught immediately
        error_msg = str(exc_info.value)
        assert "accidentally call the method" in error_msg

    def test_issue_3680_correct_pattern_works(self):
        """Verify the correct pattern from Issue #3680 works properly."""
        session = MockSession()

        result = timeout_loop(
            session.is_active,
            5.0,
            expected="falsy",
        )

        assert result is False
        assert session.check_count >= 3
