#!/usr/bin/env python
"""
Test script to verify the timeout_loop fix.

This script demonstrates:
1. The bug: timeout_loop hangs when passed a non-callable (method call result)
2. The fix: timeout_loop now validates input and raises a helpful error
3. Correct usage: timeout_loop works properly with method references and lambdas
"""

import sys
import time

from ansys.fluent.core.exceptions import InvalidArgument
from ansys.fluent.core.utils.execution import timeout_loop


class MockSession:
    """Mock Fluent session for testing."""

    def __init__(self):
        self.is_serving = True
        self.check_count = 0

    def is_active(self):
        """Check if session is active."""
        self.check_count += 1
        print(f"  is_active() called (call #{self.check_count})")
        # After 3 calls, return False to simulate session becoming inactive
        return self.check_count < 3


def test_bug_detection():
    """Test that the fix detects the bug and provides helpful error message."""
    print("\n=== Test 1: Bug Detection (Passing method call result) ===")

    session = MockSession()

    try:
        print("Attempting: timeout_loop(session.is_active(), 2.0, expected='falsy')")
        print("  (This is the INCORRECT usage that was causing hangs)")
        result = timeout_loop(session.is_active(), 2.0, expected="falsy")
        print(f"ERROR: Should have raised InvalidArgument but got result: {result}")
        return False
    except InvalidArgument as e:
        print("✓ Correctly raised InvalidArgument:")
        print(f"  {str(e)}")
        return True
    except Exception as e:
        print(f"ERROR: Unexpected exception: {type(e).__name__}: {e}")
        return False


def test_correct_usage_method_reference():
    """Test correct usage with method reference."""
    print("\n=== Test 2: Correct Usage (Method Reference) ===")

    session = MockSession()

    try:
        print("Attempting: timeout_loop(session.is_active, 5.0, expected='falsy')")
        print("  (This is the CORRECT usage)")
        start = time.time()
        result = timeout_loop(session.is_active, 5.0, expected="falsy")
        elapsed = time.time() - start
        print(f"✓ Success! Result: {result}, Elapsed: {elapsed:.2f}s")
        print(f"  Session was checked {session.check_count} times")
        return True
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        return False


def test_correct_usage_lambda():
    """Test correct usage with lambda."""
    print("\n=== Test 3: Correct Usage (Lambda) ===")

    session = MockSession()

    try:
        print(
            "Attempting: timeout_loop(lambda: session.is_active(), 5.0, expected='falsy')"
        )
        print("  (Using lambda for complex conditions)")
        start = time.time()
        result = timeout_loop(lambda: session.is_active(), 5.0, expected="falsy")
        elapsed = time.time() - start
        print(f"✓ Success! Result: {result}, Elapsed: {elapsed:.2f}s")
        print(f"  Session was checked {session.check_count} times")
        return True
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        return False


def test_timeout_behavior():
    """Test timeout behavior when condition never met."""
    print("\n=== Test 4: Timeout Behavior ===")

    def always_true():
        return True

    try:
        print("Attempting: timeout_loop(always_true, 1.0, expected='falsy')")
        print("  (Expecting timeout since always_true never returns False)")
        start = time.time()
        result = timeout_loop(always_true, 1.0, expected="falsy")
        elapsed = time.time() - start
        print(f"✓ Timeout returned: {result}, Elapsed: {elapsed:.2f}s")
        if result is True and elapsed >= 1.0:
            print("  ✓ Correctly returned True (opposite of 'falsy' expectation)")
            return True
        else:
            print(f"  ERROR: Expected True and ~1.0s, got {result} and {elapsed:.2f}s")
            return False
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("Testing timeout_loop Fix")
    print("=" * 70)

    results = []
    results.append(("Bug Detection", test_bug_detection()))
    results.append(("Method Reference", test_correct_usage_method_reference()))
    results.append(("Lambda", test_correct_usage_lambda()))
    results.append(("Timeout Behavior", test_timeout_behavior()))

    print("\n" + "=" * 70)
    print("Test Results Summary")
    print("=" * 70)
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")

    all_passed = all(result for _, result in results)
    print("\n" + ("=" * 70))
    if all_passed:
        print("✓ All tests PASSED!")
        print("=" * 70)
        sys.exit(0)
    else:
        print("✗ Some tests FAILED!")
        print("=" * 70)
        sys.exit(1)
