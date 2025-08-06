#!/usr/bin/env python3
"""
Test runner script for ScrapeGraph Python SDK
Runs all tests with coverage and generates reports
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd, cwd=None):
    """Run a command and return the result"""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return result


def main():
    parser = argparse.ArgumentParser(description="Run ScrapeGraph Python SDK tests")
    parser.add_argument("--coverage", action="store_true", help="Run with coverage")
    parser.add_argument(
        "--html", action="store_true", help="Generate HTML coverage report"
    )
    parser.add_argument(
        "--xml", action="store_true", help="Generate XML coverage report"
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument(
        "--async-only", action="store_true", help="Run only async tests"
    )
    parser.add_argument("--sync-only", action="store_true", help="Run only sync tests")
    parser.add_argument("--test-file", help="Run specific test file")

    args = parser.parse_args()

    # Change to the scrapegraph-py directory
    os.chdir(Path(__file__).parent)

    # Build pytest command
    cmd = ["python", "-m", "pytest"]

    if args.verbose:
        cmd.append("-v")

    if args.coverage:
        cmd.extend(["--cov=scrapegraph_py", "--cov-report=term-missing"])

        if args.html:
            cmd.append("--cov-report=html")
        if args.xml:
            cmd.append("--cov-report=xml")

    if args.async_only:
        cmd.append("-m asyncio")
    elif args.sync_only:
        cmd.append("-m 'not asyncio'")

    if args.test_file:
        cmd.append(args.test_file)
    else:
        cmd.append("tests/")

    # Run the tests
    print("🚀 Starting test suite...")
    result = run_command(cmd)

    if result.returncode == 0:
        print("✅ All tests passed!")

        if args.coverage:
            print("\n📊 Coverage Summary:")
            print(result.stdout)

            if args.html:
                print("📄 HTML coverage report generated in htmlcov/")
            if args.xml:
                print("📄 XML coverage report generated as coverage.xml")
    else:
        print("❌ Tests failed!")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
