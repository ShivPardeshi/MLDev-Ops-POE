"""
Simple Single-File Application for MLOps Internal POE
Demonstrates a modular, testable Python application for CI/CD and MLOps pipelines.
"""

import sys


def get_greeting(name: str = "World") -> str:
    """Return a formatted greeting message."""
    clean_name = name.strip() if name else "World"
    return f"Hello, {clean_name}! Welcome to the MLOps POE Pipeline."


def calculate_metric(input_val: float) -> float:
    """
    Simulate a lightweight predictive score or metric calculation.
    Example transformation: y = round(input_val * 1.5 + 2.0, 2)
    """
    return round(float(input_val) * 1.5 + 2.0, 2)


def main():
    """Main application entry point."""
    print("=" * 60)
    print("   MLOps POE - Hello Application   ")
    print("=" * 60)

    # Greeting output
    message = get_greeting("DevOps Engineer")
    print(f"[Application Output] {message}")

    # Metric prediction output
    sample_input = 4.0
    metric_output = calculate_metric(sample_input)
    print(f"[Model/Metric Output] Input: {sample_input} -> Prediction: {metric_output}")
    print("=" * 60)


if __name__ == "__main__":
    main()
