"""Append Singapore's Acts from the Government Gazette to the singapore-law history with git fast-import.

Phase "reved": every revised edition of an Act in the Gazette's Revised Acts supplement (1999-2022, including the
2020 Revised Edition of 31 December 2021), one commit per edition, dated noon Singapore time on the day the edition's
title page says it comes into operation. After the 2020 Revised Edition, folders of Acts it does not contain are
removed in one commit.

Phase "passed": every Act as passed in the Gazette's Acts Supplement (1998-2026), one commit per Act under
acts-as-passed/<year>/<number>-<slug>/, dated noon on the day the Act gives for its commencement, or, when the Act
leaves commencement to a later notification, on the day of the President's assent (stated on the Act).

The new commits go on branch --branch, starting from --parent; state of what is already in git is kept in
eg/state.json so later runs append only what is new.

Usage: python -X utf8 eg_build.py --repo <dir> --parent <sha> --branch eg --phase reved|passed [--docs <dir>]
"""
import argparse
import csv
import hashlib
import io
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import eg_parse as P  # noqa: E402
from eg_fetch import local  # noqa: E402

PCACHE = os.path.join(HERE, "parsed")
COMMITTER = "Lexifina <world-law@lexifina.com>"
PKEY = hashlib.sha1(open(os.path.join(HERE, "eg_parse.py"), "rb").read()).hexdigest()[:12]
NOTICE = ("Reproduced from the Republic of Singapore Government Gazette (egazette.gov.sg). The e-Gazettes are subject "
          "to copyright of the Singapore Government and are reproduced with the permission of the Singapore "
          "Government; check egazette.gov.sg for the latest e-Gazettes.")


def slug(s):
    s = s.lower().replace("’", "").replace("'", "")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def short_title(t):
    t = re.sub(r"^Chapter\s+[\w.]+\s*-\s*", "", t.strip())
    t = re.sub(r"\s*\(Chapter [^)]*\)\s*$", "", t)
    return re.sub(r"\s+\d{4}$", "", t).strip()


def parse_one(args):
    path, cons = args
    key = [PKEY, os.path.getmtime(path)]
    jp = os.path.join(PCACHE, hashlib.sha1(path.encode()).hexdigest()[:16] + ".json")
    if os.path.exists(jp):
        try:
            c = json.load(open(jp, encoding="utf-8"))
            if c.get("key") == key:
                return path, c
        except Exception:
            pass
    try:
        r = P.parse(path, constitution=cons)
        c = {"key": key, "ok": True, **r}
    except Exception as e:  # ParseError or a broken PDF
        c = {"key": key, "ok": False, "error": f"{type(e).__name__}: {e}"}
    os.makedirs(PCACHE, exist_ok=True)
    json.dump(c, open(jp, "w", encoding="utf-8"), ensure_ascii=False)
    return path, c


def parse_all(items):
    todo = [(local(v["url"]), v["title"].startswith("Constitution of the Republic")) for v in items
            if os.path.exists(local(v["url"]))]
    out = {}
    with ProcessPoolExecutor(max_workers=3) as ex:
        for path, c in ex.map(parse_one, todo, chunksize=4):
            out[path] = c
    return out


def passed_dates(cover):
    t = re.sub(r"\s+", " ", " ".join(cover))
    assent = None
    m = re.search(r"assented to by the President on (\d{1,2})(?:st|nd|rd|th)? (\w+),? (\d{4})", t)
    if m:
        assent = P.dmy(m.group(1), m.group(2), m.group(3))
    no = re.search(r"\bNo\.\s*(\d+)\s*of\s*(\d{4})\b", t)
    return assent, (int(no.group(1)), int(no.group(2))) if no else None


def commencement(files):
    """The bracketed commencement date printed under the long title, if the Act gives one."""
    t = files.get("title.md", "")
    m = re.findall(r"\[(\d{1,2})(?:st|nd|rd|th)? (\w+) (\d{4})\]", t)
    if m:
        d = P.dmy(*m[-1])
        if d:
            return d
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--parent", required=True)
    ap.add_argument("--branch", default="eg")
    ap.add_argument("--phase", choices=["reved", "passed"], required=True)
    ap.add_argument("--today", default=datetime.now(timezone.utc).date().isoformat())
    ap.add_argument("--docs", default=None)
    ap.add_argument("--state", default=os.path.join(HERE, "state.json"))
    args = ap.parse_args()
    state = json.load(open(args.state, encoding="utf-8")) if os.path.exists(args.state) else \
        {"done": [], "folders": {}, "held": {}}
    done = set(state["done"])
    cat = json.load(open(os.path.join(HERE, "catalogue.json"), encoding="utf-8"))
    sub = "Revised Acts" if args.phase == "reved" else "Acts Supplement"
    items = [v for v in cat if v["sub"] == sub and v["url"] not in done]
    if args.phase == "reved":
        items = [v for v in items if not re.search(r"(?i)Alphabetical List|Chronological|Table of|Index|Pre-Publication", v["title"])]
    parsed = parse_all(items)
    events, held = [], dict(state.get("held", {}))
    revised_2020 = set()
    for v in items:
        p = local(v["url"])
        if p not in parsed:
            continue
        c = parsed[p]
        if not c["ok"]:
            held[v["url"]] = c["error"]
            continue
        files = c["files"]
        if args.phase == "reved":
            d, basis = P.in_force(" ".join(c["cover"]))
            if not d:
                held[v["url"]] = "no in-operation date on the title page"
                continue
            stitle = short_title(v["title"])
            folder = "acts/" + slug(stitle)
            m = re.search(r"(\d{4}) REVISED EDITION|REVISED EDITION (\d{4})", " ".join(c["cover"]))
            ed = (m.group(1) or m.group(2)) if m else d[:4]
            author = (f"{ed} Revised Edition", f"reved-{ed}")
            subj = f"{v['title'] if not v['title'].startswith('Chapter') else stitle}: {ed} Revised Edition, " \
                   f"in operation {int(d[8:])} {datetime.strptime(d, '%Y-%m-%d'):%B %Y}"
            if d == "2021-12-31":
                revised_2020.add(folder)
            tr = [f"In-force: {d}", f"In-force-basis: {basis}",
                  f"Edition: {ed} Revised Edition (Revised Edition of the Laws Act)",
                  f"Gazette: Revised Acts supplement, published {v['date']}"]
        else:
            assent, no = passed_dates(c["cover"])
            com = commencement(files)
            if not no:
                held[v["url"]] = "no Act number on the Act"
                continue
            if com:
                d, basis = com, "the commencement date printed under the Act's long title"
            elif assent:
                d, basis = assent, ("the day of the President's assent, printed on the Act (the Act as enacted; "
                                    "it comes into operation as its commencement section or a later Gazette "
                                    "notification provides)")
            else:
                held[v["url"]] = "no commencement or assent date on the Act"
                continue
            stitle = v["title"].strip()
            folder = f"acts-as-passed/{no[1]}/{no[0]:03d}-{slug(re.sub(r'\s+' + str(no[1]) + r'$', '', stitle))[:70]}"
            author = (f"Act {no[0]} of {no[1]}", f"act-{no[1]}-{no[0]}")
            subj = f"{stitle} (Act {no[0]} of {no[1]}), as passed"
            tr = [f"In-force: {d}", f"In-force-basis: {basis}"]
            if assent:
                tr.append(f"Assented: {assent}")
            tr.append(f"Gazette: Acts Supplement, published {v['date']}")
        if d < "1970-01-02" or d > args.today:
            held[v["url"]] = f"date {d} outside 1970-01-02..{args.today}"
            continue
        tr.append(f"Source: {v['url']}")
        tr.append("Text-source: the PDF's own text layer")
        if c.get("missing"):
            tr.append(f"Not-split: sections {', '.join(c['missing'][:20])} (left inside the section before)")
        events.append((d, folder, subj, author, tr, files, v["url"]))
    events.sort(key=lambda e: (e[0], e[1]))

    out = io.BytesIO()
    w = out.write
    prev_day, sec, first = None, 0, True
    n = 0

    def header(ts, name, mail, msg):
        nonlocal first
        mb = msg.encode("utf-8")
        w(f"commit refs/heads/{args.branch}\n".encode())
        w(f"author {name} <{mail}> {ts} +0800\n".encode("utf-8"))
        w(f"committer {COMMITTER} {ts} +0800\n".encode())
        w(f"data {len(mb)}\n".encode() + mb + b"\n")
        if first:
            w(f"from {args.parent}\n".encode())
            first = False

    removed_done = state.get("removed_2020", False)
    for i, (d, folder, subj, author, tr, files, url) in enumerate(events):
        sec = sec + 1 if d == prev_day else 0
        prev_day = d
        ts = int(datetime(*map(int, d.split("-")), 4, 0, 0, tzinfo=timezone.utc).timestamp()) + sec
        header(ts, author[0], f"{author[1]}@egazette.gov.sg.invalid", subj + "\n\n" + "\n".join(tr) + "\n")
        w(f"D {folder}\n".encode())
        for fn in sorted(files):
            b = files[fn].encode("utf-8")
            w(f"M 100644 inline {folder}/{fn}\ndata {len(b)}\n".encode() + b + b"\n")
        w(b"\n")
        state["folders"][folder] = d
        n += 1
        nxt = events[i + 1][0] if i + 1 < len(events) else None
        if args.phase == "reved" and d == "2021-12-31" and nxt != d and not removed_done and revised_2020:
            gone = sorted(f for f in state["folders"] if f.startswith("acts/") and f not in revised_2020)
            if gone:
                sec += 1
                msg = (f"Acts not in the 2020 Revised Edition: {len(gone)} folders removed\n\n"
                       "In-force: 2021-12-31\nIn-force-basis: the 2020 Revised Edition, in operation on 31 December "
                       "2021, contains every Act then in force; an Act revised earlier and absent from it had been "
                       "repealed or renamed by then\nKind: removal\n" + "".join(f"Removed: {g}\n" for g in gone))
                header(ts + 1, "2020 Revised Edition", "reved-2020@egazette.gov.sg.invalid", msg)
                for g in gone:
                    w(f"D {g}\n".encode())
                    state["folders"].pop(g, None)
                w(b"\n")
            removed_done = True
    state["removed_2020"] = removed_done

    if args.docs:
        tsd = int(datetime(*map(int, args.today.split("-")), 4, 0, 0, tzinfo=timezone.utc).timestamp())
        docs = {}
        for dp, _, fns in os.walk(args.docs):
            for fn in fns:
                full = os.path.join(dp, fn)
                docs[os.path.relpath(full, args.docs).replace(os.sep, "/")] = open(full, encoding="utf-8").read()
        n_rev = state.get("n_reved", 0) + (n if args.phase == "reved" else 0)
        n_pas = state.get("n_passed", 0) + (n if args.phase == "passed" else 0)
        if "README.md" in docs:
            docs["README.md"] = docs["README.md"].replace(
                "{acts_by_title}", f"{len([f for f in state['folders'] if f.startswith('acts/')]):,}").replace(
                "{versions_reved}", f"{n_rev:,}").replace("{acts_passed}", f"{n_pas:,}")
        for fn in ("eg_catalogue.py", "eg_fetch.py", "eg_parse.py", "eg_build.py"):
            docs[f"tools/{fn}"] = open(os.path.join(HERE, fn), encoding="utf-8").read()
        s = io.StringIO()
        cw = csv.writer(s, lineterminator="\n")
        cw.writerow(["folder", "latest_version_in_force"])
        cw.writerows(sorted(state["folders"].items()))
        docs["data/acts.csv"] = s.getvalue()
        s = io.StringIO()
        cw = csv.writer(s, lineterminator="\n")
        cw.writerow(["source", "reason"])
        cw.writerows(sorted({**held}.items()))
        docs["data/held.csv"] = s.getvalue()
        corpus = {"corpus": "sg/national/acts", "name": "Singapore law: Acts from the Government Gazette",
                  "label": "Singapore", "language": "en", "root": "acts",
                  "roots": ["acts", "acts-as-passed"]}
        docs["corpus.json"] = json.dumps(corpus, indent=2, ensure_ascii=False) + "\n"
        msg = (f"Documents and tables: {len([f for f in state['folders'] if f.startswith('acts/')])} Acts by title, "
               f"{len([f for f in state['folders'] if f.startswith('acts-as-passed/')])} Acts as passed\n\n"
               f"Kind: documents\nRetrieved: Republic of Singapore Government Gazette, {args.today}\n").encode()
        w(f"commit refs/heads/{args.branch}\n".encode())
        w(f"author {COMMITTER} {tsd} +0800\ncommitter {COMMITTER} {tsd} +0800\n".encode())
        w(f"data {len(msg)}\n".encode() + msg + b"\n")
        if first:
            w(f"from {args.parent}\n".encode())
            first = False
        for fn in sorted(docs):
            b = docs[fn].encode("utf-8")
            w(f"M 100644 inline {fn}\ndata {len(b)}\n".encode() + b + b"\n")
        w(b"\n")
    if first:
        print(json.dumps({"head": args.parent, "commits": 0, "held": len(held)}))
        return
    subprocess.run(["git", "-C", args.repo, "update-ref", "-d", f"refs/heads/{args.branch}"], check=False,
                   stderr=subprocess.DEVNULL)
    r = subprocess.run(["git", "-C", args.repo, "fast-import", "--quiet"], input=out.getvalue())
    if r.returncode:
        sys.exit("fast-import failed")
    head = subprocess.run(["git", "-C", args.repo, "rev-parse", args.branch], capture_output=True,
                          text=True).stdout.strip()
    key = "n_reved" if args.phase == "reved" else "n_passed"
    state[key] = state.get(key, 0) + n
    state["done"] = sorted(done | {e[6] for e in events})
    state["held"] = held
    state["head"] = head
    json.dump(state, open(args.state + ".pending", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(json.dumps({"head": head, "commits": n, "held": len(held)}))


if __name__ == "__main__":
    main()
