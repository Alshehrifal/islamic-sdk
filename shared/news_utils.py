"""
Shared: Google News RSS search + webpage reader.
"""
import urllib.request
import urllib.parse
import json
import re
import html
from datetime import datetime


_UA = "Mozilla/5.0 (compatible; IslamicSkillBot/1.0)"


def search_news(query: str, max_results: int = 5, site: str | None = None) -> list[dict]:
    """
    Search Google News RSS.  Returns list of {title, link, snippet, published}.
    """
    if site:
        query = f"site:{site} {query}"

    # detect Arabic to pick locale
    is_arabic = bool(re.search(r'[\u0600-\u06FF]', query))
    hl = "ar" if is_arabic else "en"
    gl = "SA" if is_arabic else "US"

    params = urllib.parse.urlencode({"q": query, "hl": hl, "gl": gl, "ceid": f"{gl}:{hl}"})
    url = f"https://news.google.com/rss/search?{params}"

    req = urllib.request.Request(url, headers={"User-Agent": _UA})
    with urllib.request.urlopen(req, timeout=10) as r:
        raw = r.read().decode("utf-8", errors="replace")

    items = re.findall(r"<item>(.*?)</item>", raw, re.DOTALL)
    results = []
    for item in items[:max_results]:
        title   = html.unescape(re.search(r"<title>(.*?)</title>", item, re.DOTALL).group(1).strip()) if re.search(r"<title>", item) else ""
        link    = re.search(r"<link\s*/?>(.*?)</link>|<link>(.*?)</link>", item, re.DOTALL)
        link    = (link.group(1) or link.group(2) or "").strip() if link else ""
        snippet = html.unescape(re.sub(r"<[^>]+>", "", re.search(r"<description>(.*?)</description>", item, re.DOTALL).group(1) if re.search(r"<description>", item) else "").strip())
        pub     = re.search(r"<pubDate>(.*?)</pubDate>", item)
        pub     = pub.group(1).strip() if pub else ""
        if title:
            results.append({"title": title, "link": link, "snippet": snippet[:300], "published": pub})

    return results


def read_webpage(url: str, max_chars: int = 4000) -> str:
    """
    Fetch a webpage and return cleaned text.
    """
    req = urllib.request.Request(url, headers={"User-Agent": _UA})
    with urllib.request.urlopen(req, timeout=12) as r:
        raw = r.read().decode("utf-8", errors="replace")

    # strip scripts/styles
    raw = re.sub(r"<(script|style)[^>]*>.*?</(script|style)>", " ", raw, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", raw)
    text = html.unescape(text)
    text = re.sub(r"\s{2,}", " ", text).strip()
    return text[:max_chars]


def extract_announced_date(news_results: list[dict], keywords: list[str]) -> dict | None:
    """
    Scan news results for a date announcement.
    Returns {date_str, source_title, source_link} or None.
    """
    date_patterns = [
        r"\b(\d{1,2})[/-](\d{1,2})[/-](20\d{2})\b",   # DD/MM/YYYY
        r"\b(20\d{2})[/-](\d{1,2})[/-](\d{1,2})\b",   # YYYY-MM-DD
    ]
    for item in news_results:
        text = (item.get("title","") + " " + item.get("snippet","")).lower()
        if not any(k.lower() in text for k in keywords):
            continue
        for pat in date_patterns:
            m = re.search(pat, item.get("snippet","") + " " + item.get("title",""))
            if m:
                g = m.groups()
                if len(g[0]) == 4:   # YYYY-MM-DD
                    y, mo, d = int(g[0]), int(g[1]), int(g[2])
                else:
                    d, mo, y = int(g[0]), int(g[1]), int(g[2])
                try:
                    dt = datetime(y, mo, d)
                    return {
                        "date_str": dt.strftime("%d-%m-%Y"),
                        "source_title": item["title"],
                        "source_link":  item["link"],
                    }
                except ValueError:
                    pass
    return None
