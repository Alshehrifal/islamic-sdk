#!/usr/bin/env python3
"""Tests for islamic-next-events skill."""
import subprocess, sys, json, unittest, os, re
from datetime import date

SCRIPT = os.path.join(os.path.dirname(__file__), "..", "scripts", "next_events.py")
DATE_RE = re.compile(r"^\d{2}-\d{2}-20\d{2}$")


def run(args: list) -> dict:
    r = subprocess.run([sys.executable, SCRIPT] + args, capture_output=True, text=True)
    assert r.returncode == 0, f"Script failed:\n{r.stderr}"
    return json.loads(r.stdout)


INTEGRATION = os.environ.get("ISLAMIC_INTEGRATION_TESTS") == "1"

@unittest.skipUnless(INTEGRATION, "Set ISLAMIC_INTEGRATION_TESTS=1 to run live network tests")

class TestNextEvents(unittest.TestCase):

    def test_required_fields(self):
        d = run(["--city", "Riyadh"])
        for f in ["city", "country", "today", "events"]:
            self.assertIn(f, d)

    def test_events_is_list(self):
        d = run(["--city", "Riyadh"])
        self.assertIsInstance(d["events"], list)

    def test_all_events_in_future(self):
        d = run(["--city", "Riyadh"])
        today = date.today()
        for event in d["events"]:
            self.assertGreaterEqual(event["days_until"], 0,
                f"{event['event']} has negative days_until: {event['days_until']}")

    def test_events_sorted_by_date(self):
        d = run(["--city", "Riyadh"])
        days = [e["days_until"] for e in d["events"]]
        self.assertEqual(days, sorted(days), "Events should be sorted by days_until")

    def test_event_date_format(self):
        d = run(["--city", "Riyadh"])
        for event in d["events"]:
            self.assertRegex(event["date"], DATE_RE, f"Bad date format: {event['date']}")

    def test_contains_eid_fitr(self):
        d = run(["--city", "Riyadh"])
        names = [e["event"] for e in d["events"]]
        self.assertTrue(any("Fitr" in n for n in names), f"Missing Eid al-Fitr in {names}")

    def test_contains_arafah(self):
        d = run(["--city", "Riyadh"])
        names = [e["event"] for e in d["events"]]
        self.assertTrue(any("Arafah" in n for n in names), f"Missing Arafah in {names}")

    def test_contains_eid_adha(self):
        d = run(["--city", "Riyadh"])
        names = [e["event"] for e in d["events"]]
        self.assertTrue(any("Adha" in n for n in names), f"Missing Eid al-Adha in {names}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
