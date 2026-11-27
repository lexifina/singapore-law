"""List the Gazette's legislative supplements from eGazette's own public search index (the one its search page uses).

One query per sub-category and year (the index returns at most 1,000 hits per query). Writes eg/catalogue.json.
"""
import json
import os
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
URL = "https://1V7DZGZJKK-dsn.algolia.net/1/indexes/prod_ogp_egazettes_index/query"
HDR = {"X-Algolia-Application-Id": "1V7DZGZJKK", "X-Algolia-API-Key": "ff6219a3539653aa48773bf03199b95e",
       "Referer": "https://www.egazette.gov.sg/", "Content-Type": "application/json",
       "User-Agent": "Mozilla/5.0 (compatible; LexifinaCorpus/1.0; +https://lexifina.com)"}
SUBS = ["Revised Acts", "Acts Supplement", "Revised Subsidiary Legislation"]


def q(body):
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), headers=HDR, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def main():
    out = {}
    for sub in SUBS:
        years = q({"query": "", "hitsPerPage": 0, "filters": f'subCategory:"{sub}"', "facets": ["publishYear"]})
        for y in sorted(years["facets"]["publishYear"]):
            for page in range(5):
                r = q({"query": "", "hitsPerPage": 1000, "page": page,
                       "filters": f'subCategory:"{sub}" AND publishYear={y}',
                       "attributesToRetrieve": ["title", "publishDate", "fileUrl", "notificationNum", "objectGroup",
                                                "publishTimestamp"],
                       "attributesToHighlight": [], "attributesToSnippet": []})
                for h in r["hits"]:
                    k = h["fileUrl"]
                    if k not in out:
                        out[k] = {"sub": sub, "title": h.get("title", ""), "date": h.get("publishDate", ""),
                                  "no": h.get("notificationNum", ""), "url": k}
                time.sleep(0.5)
                if page + 1 >= r.get("nbPages", 1):
                    break
            print(sub, y, sum(1 for v in out.values() if v["sub"] == sub), flush=True)
    json.dump(sorted(out.values(), key=lambda v: (v["sub"], v["date"][6:] + v["date"][3:5] + v["date"][:2], v["url"])),
              open(os.path.join(HERE, "catalogue.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
