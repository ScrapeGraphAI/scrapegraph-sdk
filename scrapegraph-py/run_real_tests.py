#!/usr/bin/env python3
"""
Real API Test Runner for ScrapeGraph Python SDK
Runs tests with actual API calls using environment variables
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd, cwd=None, env=None):
    """Run a command and return the result"""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
    return result


def main():
    parser = argparse.ArgumentParser(
        description="Run ScrapeGraph Python SDK real API tests"
    )
    parser.add_argument("--api-key", help="API key to use for testing")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument(
        "--test-file", default="tests/test_real_apis.py", help="Test file to run"
    )
    parser.add_argument(
        "--async-only", action="store_true", help="Run only async tests"
    )
    parser.add_argument("--sync-only", action="store_true", help="Run only sync tests")

    args = parser.parse_args()

    # Change to the scrapegraph-py directory
    os.chdir(Path(__file__).parent)

    # Set up environment
    env = os.environ.copy()

    # Use provided API key or check environment
    if args.api_key:
        env["SGAI_API_KEY"] = args.api_key
        print(f"Using provided API key: {args.api_key[:10]}...")
    elif "SGAI_API_KEY" not in env:
        print(
            "❌ No API key provided. Set SGAI_API_KEY environment variable or use --api-key"
        )
        print("Example: export SGAI_API_KEY=your-api-key-here")
        sys.exit(1)
    else:
        print(f"Using API key from environment: {env['SGAI_API_KEY'][:10]}...")

    # Build pytest command
    cmd = ["python", "-m", "pytest"]

    if args.verbose:
        cmd.append("-v")

    if args.async_only:
        cmd.append("-m asyncio")
    elif args.sync_only:
        cmd.append("-m 'not asyncio'")

    cmd.append(args.test_file)

    # Run the tests
    print("🚀 Starting real API test suite...")
    print("⚠️  This will make actual API calls and may consume credits!")

    result = run_command(cmd, env=env)

    if result.returncode == 0:
        print("✅ All real API tests passed!")
        print("\n📊 Test Results:")
        print(result.stdout)
    else:
        print("❌ Real API tests failed!")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
