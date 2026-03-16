#!/usr/bin/env python3
"""
islamic-news/scripts/islamic_news.py
Search Google News for Islamic announcements, or read a webpage.

Usage:
  python islamic_news.py search "Eid al-Fitr 2026 Saudi Arabia"
  python islamic_news.py search "صلاة عيد الفطر الرياض 2026" --max-results 8
  python islamic_news.py search "moon sighting" --site spa.gov.sa
  python islamic_news.py read "https://spa.gov.sa/some-article" --max-chars 5000
"""
import sys, os, json, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "shared"))

from news_utils import search_news, read_webpage


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")

    s = sub.add_parser("search")
    s.add_argument("query")
    s.add_argument("--max-results", type=int, default=5)
    s.add_argument("--site",        default=None)

    r = sub.add_parser("read")
    r.add_argument("url")
    r.add_argument("--max-chars", type=int, default=4000)

    args = ap.parse_args()

    if args.cmd == "search":
        results = search_news(args.query, max_results=args.max_results, site=args.site)
        print(json.dumps({"query": args.query, "results": results}, ensure_ascii=False, indent=2))

    elif args.cmd == "read":
        text = read_webpage(args.url, max_chars=args.max_chars)
        print(json.dumps({"url": args.url, "content": text}, ensure_ascii=False, indent=2))

    else:
        ap.print_help()

if __name__ == "__main__":
    main()
