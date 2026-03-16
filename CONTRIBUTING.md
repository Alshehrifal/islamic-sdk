# Contributing to Islamic SDK

Thank you for contributing! This guide covers everything you need to add a new skill, fix a bug, or improve an existing one.

---

## Table of Contents

- [Project structure](#project-structure)
- [Adding a new skill](#adding-a-new-skill)
- [Writing tests](#writing-tests)
- [Using the shared library](#using-the-shared-library)
- [Islamic accuracy guidelines](#islamic-accuracy-guidelines)
- [Pull request checklist](#pull-request-checklist)

---

## Project structure

```
islamic-sdk/
├── shared/              ← shared utilities (prayer_api, hijri_utils, news_utils)
├── islamic-*/           ← one directory per skill
│   ├── SKILL.md         ← trigger description (required)
│   ├── scripts/         ← main script(s)
│   └── tests/           ← unit and integration tests
├── run_tests.py         ← master test runner
└── .github/workflows/   ← CI
```

---

## Adding a new skill

### 1. Create the directory structure

```bash
SKILL=islamic-my-skill
mkdir -p $SKILL/scripts $SKILL/tests
touch $SKILL/scripts/__init__.py $SKILL/tests/__init__.py
```

### 2. Write the script

```python
# islamic-my-skill/scripts/my_skill.py
import sys, os, json, argparse

# Shared library import (always use this pattern)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "shared"))
from hijri_utils import current_hijri_year
from prayer_api import fetch_prayer_times, parse_date_arg
from news_utils import search_news, extract_announced_date

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--city", required=True)
    ap.add_argument("--country", default="Saudi Arabia")
    args = ap.parse_args()

    result = {
        "city": args.city,
        "country": args.country,
        # ... your logic here
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
```

### 3. Write SKILL.md

```markdown
---
name: islamic-my-skill
description: >
  One-paragraph description with Arabic and English trigger examples.
  Include: "متى...", "when is...", and all realistic phrasings a user
  might use that should trigger this skill.
---

# My Skill Title

Brief explanation of what this skill does.

## Script
islamic-my-skill/scripts/my_skill.py

## Usage
python scripts/my_skill.py --city Riyadh
python scripts/my_skill.py --city London --country "United Kingdom"

## Output fields
...

## Agent workflow
Step-by-step instructions for Claude when presenting results.
```

### 4. Package

```bash
cd /path/to/skill-creator
python -m scripts.package_skill /path/to/islamic-my-skill ./dist
```

---

## Writing tests

All tests must follow this pattern:

```python
import os, unittest

# Network-dependent tests MUST use this guard
INTEGRATION = os.environ.get("ISLAMIC_INTEGRATION_TESTS") == "1"

@unittest.skipUnless(INTEGRATION, "Set ISLAMIC_INTEGRATION_TESTS=1 to run")
class TestMySkill(unittest.TestCase):
    def test_required_fields(self):
        ...

# Pure logic tests (no network) run always — no decorator needed
class TestMySkillLogic(unittest.TestCase):
    def test_date_calculation(self):
        ...
```

**Rules:**
- Any test that calls the Aladhan API or Google News must be under `@unittest.skipUnless(INTEGRATION, ...)`
- Pure-logic tests (Hijri math, string parsing, date arithmetic) must run without any decorator
- Minimum 5 tests per skill
- Test both happy paths and edge cases

**Running tests:**
```bash
python run_tests.py                             # unit only (CI default)
ISLAMIC_INTEGRATION_TESTS=1 python run_tests.py # live API tests
python run_tests.py --skill my-skill            # one skill
```

---

## Using the shared library

```python
# Always import shared this way (relative from scripts/)
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "shared"))

# Prayer times (Aladhan API)
from prayer_api import fetch_prayer_times, parse_date_arg, get_method

# Hijri calendar (offline, no network)
from hijri_utils import (
    gregorian_to_hijri,
    hijri_to_gregorian,
    hijri_month_start_gregorian,
    current_hijri_year,
    month_key_to_number,
    HIJRI_MONTHS,
    HIJRI_MONTH_AR,
)

# News search (Google News RSS)
from news_utils import search_news, read_webpage, extract_announced_date
```

---

## Islamic accuracy guidelines

These are non-negotiable requirements for all skills:

### Dates and moon sighting
- **Never** present a calculated date as officially announced. Always check `date_status`.
- Valid `date_status` values: `"announced"` or `"calculated (Umm al-Qura — unconfirmed)"`.
- Eid and Ramadan dates differ by country due to local hilal sighting.

### Arafah
- **Always follows Saudi Arabia** — Hajj is in Mecca.
- Do **not** use the local country's Dhul Hijjah announcement for Arafah.

### Ashura
- **Follows the country's own Muharram** announcement (unlike Arafah).

### Hadith references
- Any Hadith cited in `fasting_virtue`, `virtues`, or `recommended_acts` must include the source collection and hadith number (e.g., `Muslim 1162`).
- Do not paraphrase Hadith in ways that change meaning.

### Prayer times
- Always display `⚠️ Verify with your local mosque` when presenting estimated prayer times for Eid.
- Eid prayer time is estimated as Sunrise + 15 min — this is an approximation.

---

## Pull request checklist

Before opening a PR, confirm:

- [ ] New skill has `SKILL.md` with frontmatter `name` and `description`
- [ ] Script outputs valid JSON to stdout
- [ ] Script has `--city` and `--country` arguments where applicable
- [ ] All network-dependent tests use `@unittest.skipUnless(INTEGRATION, ...)`
- [ ] At least one pure-logic unit test runs offline
- [ ] `python run_tests.py` passes with 0 failures
- [ ] Islamic accuracy guidelines followed (date_status, no false announcements)
- [ ] Arabic text uses `ensure_ascii=False` in JSON output

---

## Questions?

Open an issue or start a discussion. جزاكم الله خيراً
