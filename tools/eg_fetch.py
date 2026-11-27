"""Download the Gazette PDFs listed in catalogue.json from assets.egazette.gov.sg, core law first.

Starts with 1 request in flight about 1 s apart; after 10 clean minutes steps up by one (max 4); any timeout or 5xx
drops back to 1. A challenge, 429 or a run of 403s stops the run. Logs to eg/progress.log.
"""
import json
import os
import random
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(HERE, "pdf")
LOG = os.path.join(HERE, "progress.log")
UA = "Mozilla/5.0 (compatible; LexifinaCorpus/1.0; +https://lexifina.com)"
CORE = ["Constitution of the Republic of Singapore", "Penal Code", "Criminal Procedure Code", "Evidence Act",
        "Companies Act", "Employment Act", "Civil Law Act", "Land Titles Act", "Interpretation Act",
        "Supreme Court of Judicature Act", "Contracts", "Women", "Income Tax Act", "Goods and Services Tax Act",
        "Sale of Goods Act", "Misrepresentation Act", "Limitation Act", "Conveyancing and Law of Property Act",
        "Insolvency, Restructuring and Dissolution Act", "Partnership Act", "State Courts Act", "Bankruptcy Act",
        "Arbitration Act", "International Arbitration Act", "Copyright Act", "Patents Act", "Trade Marks Act"]
SUBORDER = {"Revised Acts": 1, "Acts Supplement": 2, "Revised Subsidiary Legislation": 3}
lock = threading.RLock()
state = {"level": 1, "clean_since": time.time(), "stop": None, "done": 0, "bytes": 0, "err": 0, "f403": 0}


def log(m):
    with lock:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now(timezone.utc):%Y-%m-%dT%H:%M:%SZ} {m}\n")


def local(url):
    p = urllib.parse.unquote(urllib.parse.urlparse(url).path).lstrip("/")
    return os.path.join(PDF, *p.split("/"))


def prio(v):
    core = any(v["title"].startswith(c) or (" - " + c) in v["title"] for c in CORE)
    return (0 if core and v["sub"] == "Revised Acts" else 1, SUBORDER.get(v["sub"], 9),
            -int(v["date"][6:] or 0) if v["sub"] == "Revised Acts" else 0, v["url"])


def get(url):
    req = urllib.request.Request(url.replace(" ", "%20"), headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.status, r.read(), r.headers.get("Content-Type", "")


def worker(q, idx):
    while not state["stop"]:
        with lock:
            if idx >= state["level"]:
                pass
            item = q.pop(0) if (q and idx < state["level"]) else None
        if item is None:
            if not q:
                return
            time.sleep(2)
            continue
        dst = local(item["url"])
        t0 = time.time()
        try:
            st, body, ct = get(item["url"])
            if not body.startswith(b"%PDF"):
                if b"awswaf" in body or b"challenge" in body.lower():
                    state["stop"] = f"challenge on {item['url']}"
                    return
                log(f"not a pdf ({ct}, {len(body)} B): {item['url']}")
            else:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                with open(dst + ".part", "wb") as f:
                    f.write(body)
                os.replace(dst + ".part", dst)
                with lock:
                    state["done"] += 1
                    state["bytes"] += len(body)
                    state["f403"] = 0
        except urllib.error.HTTPError as e:
            if e.code == 403:
                with lock:
                    state["f403"] += 1
                log(f"403 {item['url']}")
                if state["f403"] >= 5:
                    state["stop"] = "five 403s in a row"
                    return
            elif e.code == 429:
                state["stop"] = f"429 on {item['url']}"
                return
            else:
                with lock:
                    state["level"] = 1
                    state["clean_since"] = time.time()
                    state["err"] += 1
                    q.append(item)
                log(f"HTTP {e.code} {item['url']}; back to 1 in flight, waiting 60 s")
                time.sleep(60)
        except Exception as e:
            with lock:
                state["level"] = 1
                state["clean_since"] = time.time()
                state["err"] += 1
                item["tries"] = item.get("tries", 0) + 1
                if item["tries"] < 5:
                    q.append(item)
            log(f"error {e!r} {item['url']}; back to 1 in flight, waiting 30 s")
            time.sleep(30)
        with lock:
            if time.time() - state["clean_since"] > 600 and state["level"] < 4:
                state["level"] += 1
                state["clean_since"] = time.time()
                log(f"10 clean minutes: {state['level']} in flight")
        time.sleep(max(0.0, 1.0 - (time.time() - t0)) + random.random() * 0.2)


def main():
    with open(os.path.join(HERE, "fetch.pid"), "w") as f:
        f.write(str(os.getpid()))
    cat = json.load(open(os.path.join(HERE, "catalogue.json"), encoding="utf-8"))
    q = [v for v in cat if not os.path.exists(local(v["url"]))]
    q.sort(key=prio)
    log(f"fetch start pid {os.getpid()}: {len(q)} of {len(cat)} to get")
    ts = [threading.Thread(target=worker, args=(q, i), daemon=True) for i in range(4)]
    for t in ts:
        t.start()
    last = time.time()
    while any(t.is_alive() for t in ts):
        time.sleep(5)
        if time.time() - last > 300:
            last = time.time()
            log(f"progress: {state['done']} got ({state['bytes'] / 1e6:.0f} MB), {len(q)} left, "
                f"{state['level']} in flight, {state['err']} errors")
    log(f"fetch end: {state['done']} got, {len(q)} left, stop={state['stop']}")


if __name__ == "__main__":
    main()
