#!/usr/bin/env python3
"""
Master test runner for Islamic SDK.

Usage:
  python run_tests.py                    # Unit tests only (offline-safe)
  python run_tests.py --skill hijri      # Single skill
  python run_tests.py --integration      # Integration tests (requires network)

Set ISLAMIC_INTEGRATION_TESTS=1 to enable network-dependent tests.
"""
from __future__ import annotations

import sys
import os
import argparse
import unittest

SKILLS = [
    "islamic-prayer-times",
    "islamic-day-info",
    "islamic-qiyam",
    "islamic-hijri",
    "islamic-hilal",
    "islamic-eid",
    "islamic-arafah",
    "islamic-ashura",
    "islamic-next-events",
    "islamic-news",
]


def discover_tests(skill_filter: str | None = None) -> unittest.TestSuite:
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    root = os.path.dirname(os.path.abspath(__file__))
    skills = [skill_filter] if skill_filter else SKILLS

    for skill in skills:
        full_name = skill if skill.startswith("islamic-") else f"islamic-{skill}"
        test_dir = os.path.join(root, full_name, "tests")
        if os.path.isdir(test_dir):
            discovered = loader.discover(test_dir, pattern="test_*.py", top_level_dir=root)
            suite.addTests(discovered)

    return suite


def main():
    ap = argparse.ArgumentParser(description="Islamic SDK test runner")
    ap.add_argument("--skill", default=None, help="Run tests for a single skill (e.g., hijri)")
    ap.add_argument("--integration", action="store_true", help="Enable integration tests")
    args = ap.parse_args()

    if args.integration:
        os.environ["ISLAMIC_INTEGRATION_TESTS"] = "1"

    suite = discover_tests(args.skill)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    main()
