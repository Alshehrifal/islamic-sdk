---
name: islamic-news
description: >
  Search Google News for Islamic announcements (moon sightings, Eid dates, prayer schedules)
  or read a full webpage. Use this skill whenever the user wants to look up news about
  Islamic events: "هل أُعلن عن رؤية هلال شوال؟", "search for Eid announcement Saudi Arabia",
  "ابحث عن إعلان صلاة العيد في الرياض", "read this article about moon sighting",
  "latest news about Ramadan 2026", "spa.gov.sa هلال", or any request to search news
  about Islamic occasions or to fetch/read a specific Islamic news URL.
---

# Islamic News Search & Reader

Searches Google News (Arabic or English) for Islamic announcements, or reads a full webpage.

## Script

```
islamic-news/scripts/islamic_news.py
```

## Usage

**Search news:**
```bash
python scripts/islamic_news.py search "Eid al-Fitr 2026 Saudi Arabia"
python scripts/islamic_news.py search "صلاة عيد الفطر الرياض 2026" --max-results 8
python scripts/islamic_news.py search "moon sighting 2026" --site spa.gov.sa
python scripts/islamic_news.py search "هلال شوال 1447 السعودية"
```

**Read a webpage:**
```bash
python scripts/islamic_news.py read "https://spa.gov.sa/article-url" --max-chars 5000
```

## Output

**search:** `{query, results: [{title, link, snippet, published}]}`  
**read:** `{url, content}` (plain text, stripped HTML)

## Agent workflow

### For news search:
1. Run with relevant query in Arabic if the user/topic is Arabic, English otherwise.
2. For official Saudi sources, add `--site spa.gov.sa`.
3. Present results as a list: title + snippet + date.
4. If a result looks relevant and has a URL, use `read` to fetch full details.

### For official announcement hunting:
1. Try Arabic query first: `"هلال [month] [year] [country]"`
2. Then English: `"[country] [month] hilal announced [year]"`
3. Try `--site spa.gov.sa` for Saudi announcements.

## Preferred sources

| Country      | Preferred site         |
|--------------|------------------------|
| Saudi Arabia | spa.gov.sa             |
| Egypt        | alazhar.gov.eg         |
| Morocco      | habous.gov.ma          |
| Turkey       | diyanet.gov.tr         |
| Malaysia     | islam.gov.my           |

## Language detection

The script auto-detects Arabic queries (by Unicode range) and sets Google News locale to `ar-SA` accordingly.
