"""Parse a Singapore Gazette Act PDF (a revised edition, or an Act as passed) into one file per section and schedule.

The PDF's own text layer is read (no OCR). The Arrangement of Sections (or Articles) gives the expected sections and
their headings; the body is cut at each section's first line in that order. Raises ParseError when the sections found
do not match the arrangement closely enough.
"""
import re
import unicodedata

import pymupdf

MARK = re.compile(r"^\((?:\d+[A-Z]*|[a-z]{1,5}|[A-Z]{1,3})\)\s")
NUM = r"(\d+[A-Z]{0,4})"
TOCROW = re.compile(r"^" + NUM + r"\.\s*(.*)$")
SCHED = re.compile(r"^(THE\s+)?((FIRST|SECOND|THIRD|FOURTH|FIFTH|SIXTH|SEVENTH|EIGHTH|NINTH|TENTH|ELEVENTH|TWELFTH|"
                   r"THIRTEENTH|FOURTEENTH|FIFTEENTH|SIXTEENTH|SEVENTEENTH|EIGHTEENTH|NINETEENTH|TWENTIETH|"
                   r"TWENTY-\w+|THIRTIETH)\s+)?SCHEDULE\b(.*)$")
FOOT = re.compile(r"^(\d{1,4}|\d{1,2}\.\d{1,2}\.\d{4}|(\d{1,4} )?\d{4} Ed\.( \d{1,4})?|CAP\. ?\d+[A-Z]*|"
                  r"Informal Consolidation.*|.{0,60}\b\d{4} Ed\.)$")
ENDMARK = re.compile(r"^(LEGISLATIVE HISTORY|COMPARATIVE TABLE|LEGISLATIVE SOURCE KEY|ABBREVIATIONS)\b")
STRUCT = re.compile(r"^(PART|CHAPTER|DIVISION|SUBDIVISION|Part|Chapter|Division|Subdivision|SUB-PART)\b")
ORD = {w: i + 1 for i, w in enumerate("FIRST SECOND THIRD FOURTH FIFTH SIXTH SEVENTH EIGHTH NINTH TENTH ELEVENTH "
                                      "TWELFTH THIRTEENTH FOURTEENTH FIFTEENTH SIXTEENTH SEVENTEENTH EIGHTEENTH "
                                      "NINETEENTH TWENTIETH".split())}


class ParseError(Exception):
    pass


def norm(s):
    s = unicodedata.normalize("NFKC", s).replace("‘‘", "“").replace("’’", "”")
    s = re.sub(r"[“”\"'‘’]", "", s)
    return re.sub(r"\s+", " ", s).strip().lower()


def rows_of(doc):
    """Every printed line as (page, y, x0, text, size, bold, italic), headers and footers dropped."""
    out = []
    for pno, page in enumerate(doc):
        h = page.rect.height
        spans = []
        for b in page.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                if l.get("dir", (1, 0))[0] < 0.9:
                    continue
                for s in l["spans"]:
                    if s["text"].strip():
                        spans.append(s)
        spans.sort(key=lambda s: (round(s["origin"][1]), s["bbox"][0]))
        groups = []
        for s in spans:
            y = s["origin"][1]
            if groups and abs(groups[-1][0] - y) <= 2.5:
                groups[-1][1].append(s)
            else:
                groups.append([y, [s]])
        for y, ss in groups:
            ss.sort(key=lambda s: s["bbox"][0])
            txt, prev = "", None
            for s in ss:
                t = s["text"]
                if prev is not None:
                    gap = s["bbox"][0] - prev["bbox"][2]
                    if gap > 0.18 * s["size"] and not txt.endswith(" ") and not t.startswith(" "):
                        txt += " "
                txt += t
                prev = s
            txt = re.sub(r"\s+", " ", txt.replace("�", "—")).strip()
            if not txt:
                continue
            size = max(ss, key=lambda s: len(s["text"]))["size"]
            nch = sum(len(s["text"].strip()) for s in ss) or 1
            bold = sum(len(s["text"].strip()) for s in ss if ".B" in s["font"] or "Bold" in s["font"]
                       or s["flags"] & 16) / nch
            ital = sum(len(s["text"].strip()) for s in ss if ".I" in s["font"] or "Italic" in s["font"]
                       or s["flags"] & 2) / nch
            if y < 76 and (len(txt) < 90):
                continue  # running header
            if y > h - 60 and FOOT.match(txt):
                continue  # footer: page number, date, edition
            out.append({"p": pno, "y": y, "x": ss[0]["bbox"][0], "t": txt, "size": size, "bold": bold,
                        "ital": ital, "x1": ss[-1]["bbox"][2]})
    return out


def body_left(rows):
    from collections import Counter
    c = Counter(round(r["x"]) for r in rows if len(r["t"]) > 50)
    return c.most_common(1)[0][0] if c else 70


def parse_toc(rows, start):
    """Entries [(num, heading, context)] from the arrangement that starts at rows[start]."""
    entries, ctx, group, i = [], {}, [], start + 1
    head_x = None
    sched = []
    last_kind = None
    while i < len(rows):
        t = rows[i]["t"]
        m = TOCROW.match(t)
        if t in ("Section", "Article", "Sections", "Articles", "Regulation", "Rule", "Paragraph"):
            i += 1
            continue
        if m and (not entries or not (entries and m.group(1) == entries[0][0] and len(entries) > 1)):
            if entries and m.group(1) == entries[0][0]:
                break
            if group:
                ctx = merge_ctx(ctx, " ".join(group))
                group = []
            entries.append([m.group(1), m.group(2), dict(ctx)])
            head_x = None
            if m.group(2):
                head_x = rows[i]["x"] + (len(m.group(1)) + 1) * rows[i]["size"] * 0.5
            last_kind = "entry"
            i += 1
            continue
        if m:
            break
        if t.startswith("[There ") or t.startswith("[Repealed") and last_kind == "entry" and entries[-1][1]:
            i += 1
            continue
        if SCHED.match(t) or re.match(r"^(First|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth|Tenth|"
                                      r"Eleventh|Twelfth|The)?\s*Schedules?\b", t):
            sched.append(t)
            last_kind = "sched"
            i += 1
            continue
        if ENDMARK.match(t.upper()) or t.startswith("Legislative History") or t.startswith("Comparative Table"):
            i += 1
            continue
        if re.match(r"^(An Act|An Ordinance|WHEREAS|BE IT ENACTED|We, the people)", t):
            break
        if last_kind == "entry" and entries and not entries[-1][1]:
            entries[-1][1] = t
            head_x = rows[i]["x"]
            i += 1
            continue
        upper = t.upper() == t and re.search(r"[A-Z]", t)
        if last_kind == "entry" and not upper and not STRUCT.match(t) and head_x is not None \
                and rows[i]["x"] >= head_x - 6:
            entries[-1][1] += " " + t
            i += 1
            continue
        if last_kind == "sched":
            sched[-1] += " " + t
            i += 1
            continue
        group.append(t)
        last_kind = "struct"
        i += 1
    return entries, sched, i


def scan_entries(rows):
    """No arrangement printed (a short Act): sections numbered 1, 2, 3 ... in the body, each with the bold or italic
    heading printed above it."""
    body_i = next((i for i, r in enumerate(rows) if re.match(r"^(An Act|An Ordinance|AN ACT|WHEREAS|BE IT ENACTED|"
                                                             r"Be it enacted)", r["t"])), None)
    if body_i is None:
        return [], 0
    bl = body_left(rows[body_i:])
    entries, want = [], 1
    for k in range(body_i, len(rows)):
        r = rows[k]
        m = re.match(r"^\*?(\d+)([A-Z]{0,3})\.(?![\d])", r["t"])
        if not m or r["x"] > bl + 40 or ENDMARK.match(r["t"]):
            continue
        n = int(m.group(1))
        if n == want or (entries and n == want - 1 and m.group(2)):
            pv = rows[k - 1]
            head = pv["t"] if (pv["bold"] > 0.5 or pv["ital"] > 0.5) and not TOCROW.match(pv["t"]) else ""
            entries.append([m.group(1) + m.group(2), head, {}])
            want = n + 1
    return entries, body_i


def merge_ctx(ctx, g):
    g = re.sub(r"\s+", " ", g).strip()
    u = g.upper()
    if u.startswith("PART") or u.startswith("SUB-PART"):
        return {"Part": g}
    if u.startswith("CHAPTER"):
        return {"Chapter": g} if "Part" not in ctx else {"Part": ctx["Part"], "Chapter": g}
    if u.startswith("DIVISION"):
        d = {k: v for k, v in ctx.items() if k in ("Part", "Chapter")}
        d["Division"] = g
        return d
    if u.startswith("SUBDIVISION"):
        d = {k: v for k, v in ctx.items() if k in ("Part", "Chapter", "Division")}
        d["Subdivision"] = g
        return d
    d = {k: v for k, v in ctx.items() if k in ("Part", "Chapter", "Division", "Subdivision")}
    d["Heading"] = g
    return d


def paragraphs(rows):
    """Join printed lines into paragraphs."""
    out, cur, prev = [], [], None
    gaps = sorted(b["y"] - a["y"] for a, b in zip(rows, rows[1:]) if a["p"] == b["p"] and 0 < b["y"] - a["y"] < 40)
    lg = gaps[len(gaps) // 3] if gaps else 15
    for r in rows:
        t = r["t"]
        new = prev is None
        if prev is not None:
            pt = prev["t"]
            if MARK.match(t) or t.startswith("[") or t.startswith("Explanation") or t.startswith("Illustration"):
                new = True
            elif re.search(r"([.;:—\]]|;\s+(and|or))$", pt):
                new = True
            elif prev["p"] == r["p"] and r["y"] - prev["y"] > lg * 1.45:
                new = True
            elif abs(r["size"] - prev["size"]) > 1.2:
                new = True
            elif prev["ital"] > 0.9 and r["ital"] < 0.5 and len(pt) < 80:
                new = True
        if new and cur:
            out.append(" ".join(cur))
            cur = []
        cur.append(t)
        prev = r
    if cur:
        out.append(" ".join(cur))
    return [re.sub(r"\s+", " ", p).replace(" —", "—" if False else " —").strip() for p in out]


def fname(num, kind):
    m = re.match(r"(\d+)([A-Z]*)", num)
    return f"{kind}-{int(m.group(1)):03d}{m.group(2).lower()}.md"


def sched_name(t, n):
    m = SCHED.match(t.upper())
    if m and m.group(3):
        w = m.group(3)
        k = ORD.get(w)
        return f"schedule-{k:02d}.md" if k else f"schedule-{w.lower()}.md"
    return "schedule.md" if n == 0 else f"schedule-x{n + 1:02d}.md"


def parse(path, constitution=False):
    doc = pymupdf.open(path)
    rows = rows_of(doc)
    if not rows:
        raise ParseError("no text layer")
    cover = [r["t"] for r in rows if r["p"] == 0]
    kind = "article" if constitution else "section"
    toc_i = next((i for i, r in enumerate(rows) if re.match(r"^ARRANGEMENT OF (SECTIONS|ARTICLES|PROVISIONS)", r["t"])),
                 None)
    if toc_i is None:
        entries, body_i = scan_entries(rows)
        if not entries:
            rest = [r for r in rows if r["p"] > 0] or rows
            paras = paragraphs(rest)
            return {"files": {"text.md": "\n\n".join(paras) + "\n",
                              "title.md": "\n\n".join(cover_lines(cover)).strip() + "\n"},
                    "cover": cover, "entries": 0, "found": 0, "missing": [], "schedules": 0, "whole": True}
    else:
        entries, scheds, body_i = parse_toc(rows, toc_i)
    if not entries:
        raise ParseError("empty arrangement")
    bl = body_left(rows[body_i:])
    # locate each section's first line, in order
    starts, j = [], body_i
    for num, head, ctx in entries:
        pat = re.compile(r"^\*?" + re.escape(num) + r"\.(?![\d])")
        k = j
        found = None
        while k < len(rows):
            r = rows[k]
            if pat.match(r["t"]) and r["x"] < bl + 40:
                pv = rows[k - 1]
                bare = len(r["t"].strip("*")) <= len(num) + 1
                if not bare or pv["bold"] > 0.5 or pv["ital"] > 0.5 or re.search(r"[.;:\])]$", pv["t"]) \
                        or pv["p"] != r["p"]:
                    found = k
                    break
            if ENDMARK.match(r["t"]):
                break
            k += 1
        if found is None:
            continue
        starts.append((found, num, head, ctx))
        j = found + 1
    if len(starts) < max(1, int(len(entries) * 0.9)):
        raise ParseError(f"found {len(starts)} of {len(entries)} sections")
    # end of the body text
    end = len(rows)
    for k in range(starts[-1][0], len(rows)):
        if ENDMARK.match(rows[k]["t"]):
            end = k
            break
    # schedule starts after the last section
    sstarts = []
    for k in range(starts[-1][0] + 1, end):
        t = rows[k]["t"]
        if SCHED.match(t) and t.upper() == t and len(t) < 120 and rows[k]["x"] > bl + 10:
            if not sstarts or k - sstarts[-1] > 2:
                sstarts.append(k)
    files = {}
    heads = {norm(h) for _, h, _ in entries}

    def strip_tail(seg, nexthead):
        """Drop the next section's heading and structural headings printed above it."""
        nh = norm(nexthead) if nexthead else None
        while seg:
            last = seg[-1]
            t = last["t"]
            if nh is not None:
                acc = ""
                for back in range(1, min(5, len(seg)) + 1):
                    acc = (seg[-back]["t"] + " " + acc).strip()
                    if norm(acc) == nh:
                        del seg[-back:]
                        nh = None
                        break
                else:
                    pass
                if nh is None:
                    continue
            if (t.upper() == t and re.search(r"[A-Z]{3}", t) and not t.startswith("[")) or STRUCT.match(t) \
                    and last["x"] > bl + 15:
                seg.pop()
                continue
            if last["bold"] > 0.9 and not t.startswith("["):
                seg.pop()
                continue
            break
        return seg

    title_rows = strip_tail(list(rows[body_i:starts[0][0]]), starts[0][2])
    tit = paragraphs(title_rows)
    for n, (k, num, head, ctx) in enumerate(starts):
        stop = starts[n + 1][0] if n + 1 < len(starts) else (sstarts[0] if sstarts else end)
        seg = list(rows[k:stop])
        seg = strip_tail(seg, starts[n + 1][2] if n + 1 < len(starts) else None)
        first = seg[0]["t"]
        seg[0] = dict(seg[0], t=re.sub(r"^\*?" + re.escape(num) + r"\.\s*", "", first).lstrip())
        if not seg[0]["t"]:
            seg = seg[1:]
        paras = paragraphs(seg) if seg else []
        if paras and paras[0].startswith("—"):
            paras[0] = paras[0][1:].lstrip()
        lines = [f"# {num}. {head}".rstrip()]
        for key in ("Part", "Chapter", "Division", "Subdivision", "Heading"):
            if key in ctx:
                lines.append(f"{key}: {ctx[key]}")
        body = "\n\n".join(paras)
        files[fname(num, kind)] = "\n".join(lines) + "\n\n" + body + "\n"
    for n, k in enumerate(sstarts):
        stop = sstarts[n + 1] if n + 1 < len(sstarts) else end
        seg = list(rows[k:stop])
        name = sched_name(rows[k]["t"], n)
        while name in files:
            name = name[:-3] + "-b.md"
        paras = paragraphs(seg)
        files[name] = "# " + paras[0] + "\n\n" + "\n\n".join(paras[1:]) + "\n"
    if end < len(rows) and rows[end]["t"].startswith("LEGISLATIVE HISTORY"):
        stop = next((k for k in range(end + 1, len(rows)) if rows[k]["t"].startswith("COMPARATIVE TABLE")), len(rows))
        paras = paragraphs(rows[end:stop])
        files["legislative-history.md"] = "# " + paras[0] + "\n\n" + "\n\n".join(paras[1:]) + "\n"
    files["title.md"] = "\n\n".join(cover_lines(cover) + [""] + tit).strip() + "\n"
    return {"files": files, "cover": cover, "entries": len(entries), "found": len(starts),
            "missing": [e[0] for e in entries if e[0] not in {s[1] for s in starts}],
            "schedules": len(sstarts)}


def cover_lines(cover):
    keep = []
    for t in cover:
        if re.match(r"^(An Act|An Ordinance|ARRANGEMENT OF)", t):
            break
        keep.append(t)
    return ["\n".join(keep)]


def in_force(cover_text):
    """The day a revised edition comes into operation, from its title page."""
    t = re.sub(r"\s+", " ", cover_text)
    m = re.search(r"comes? into operation on (\d{1,2}) (\w+) (\d{4})", t)
    if m:
        return dmy(m.group(1), m.group(2), m.group(3)), "the title page: 'comes into operation on " + \
            f"{m.group(1)} {m.group(2)} {m.group(3)}'"
    m = re.search(r"REVISED EDITION (\d{4}) \((\d{1,2})(?:st|nd|rd|th)? (\w+) (\d{4})\)", t)
    if m:
        return dmy(m.group(2), m.group(3), m.group(4)), \
            f"the title page: 'REVISED EDITION {m.group(1)} ({m.group(2)} {m.group(3)} {m.group(4)})'"
    return None, None


MONTHS = {m: i + 1 for i, m in enumerate("january february march april may june july august september october "
                                         "november december".split())}


def dmy(d, mo, y):
    k = MONTHS.get(mo.lower())
    if not k:
        return None
    return f"{int(y):04d}-{k:02d}-{int(d):02d}"
