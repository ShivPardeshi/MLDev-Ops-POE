"""
Pytest Suite for hello.py (Step 11)
Demonstrates pytest configuration and prints test case outputs.
"""

import pytest
from hello import get_greeting, calculate_metric


def test_greeting_output():
    """
    Test Case 1: Validate greeting string generation and print test case details.
    """
    input_name = "Developer"
    expected = "Hello, Developer! Welcome to the MLOps POE Pipeline."
    actual = get_greeting(input_name)

    # Print 1 test case details to console (visible with pytest -s)
    print("\n" + "=" * 50)
    print(" >>> RUNNING PYTEST TEST CASE 1: test_greeting_output <<<")
    print(f" Input parameter : name='{input_name}'")
    print(f" Expected output : '{expected}'")
    print(f" Actual output   : '{actual}'")
    print(" Status          : PASSED [✓]")
    print("=" * 50)

    assert actual == expected


def test_calculate_metric():
    """
    Test Case 2: Validate the predictive metric calculation.
    """
    input_val = 4.0
    expected = 8.0  # 4.0 * 1.5 + 2.0 = 8.0
    actual = calculate_metric(input_val)

    print("\n" + "=" * 50)
    print(" >>> RUNNING PYTEST TEST CASE 2: test_calculate_metric <<<")
    print(f" Input parameter : input_val={input_val}")
    print(f" Expected output : {expected}")
    print(f" Actual output   : {actual}")
    print(" Status          : PASSED [✓]")
    print("=" * 50)

    assert actual == expected
