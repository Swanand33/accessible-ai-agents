"""
Test runner script for AccessibleAI project.
Runs all tests and generates a report.
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

import pytest


def main():
    """Run all tests with verbose output."""
    print("=" * 60)
    print("Running AccessibleAI Test Suite")
    print("=" * 60)
    print()

    # Run pytest with options
    exit_code = pytest.main([
        "tests/",
        "-v",  # Verbose
        "-s",  # Show print statements
        "--tb=short",  # Short traceback format
        "--color=yes"  # Colored output
    ])

    print()
    print("=" * 60)
    print("Test Suite Complete")
    print("=" * 60)

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
