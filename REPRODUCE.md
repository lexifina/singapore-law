# Reproduce

Everything below is deterministic: the same downloaded PDFs give the same commits and hashes.

## Steps

1. `python -X utf8 tools/eg_catalogue.py` lists the Gazette's Revised Acts, Acts Supplement and Revised Subsidiary
   Legislation from eGazette's own public search index (the Algolia index its search page queries, with the search-only
   key the page itself carries), one query per sub-category and year, into `catalogue.json`.
2. `python -X utf8 tools/eg_fetch.py` downloads each listed PDF from `assets.egazette.gov.sg`, core law first (the
   Constitution, Penal Code, Criminal Procedure Code, Evidence Act, Companies Act, Employment Act, Civil Law Act, Land
   Titles Act and other principal Acts), then every revised edition, newest first, then the Acts as passed. One request
   in flight about one second apart; one more after each 10 clean minutes (at most 4); back to one at any timeout or
   5xx; a challenge page, a 429 or five 403s in a row stop the run. User-Agent
   `Mozilla/5.0 (compatible; LexifinaCorpus/1.0; +https://lexifina.com)`.
3. `python -X utf8 tools/eg_build.py --repo <dir> --parent <sha> --branch <branch> --phase reved` then
   `--phase passed` parse every PDF (`eg_parse.py`) and append the history with `git fast-import`.

## Method

- Text: the PDF's own text layer (PyMuPDF), printed lines rebuilt from their positions and joined into paragraphs.
  No OCR. Running headers, page numbers and edition footers are dropped.
- Sections: the Arrangement of Sections (or Articles) lists every section with its heading; the body is cut at each
  section's first line (`21.—(1) ...`), in that order. A PDF where fewer than 90% of the listed sections are found is
  held. A section not found stays inside the section before it, named in the commit's `Not-split:` trailer.
  Schedules start at their `... SCHEDULE` heading after the last section. The Law Revision Commission's Legislative
  History (not part of the Act) is kept as `legislative-history.md`.
- Dates. A revised edition: the day its title page says it comes into operation ("comes into operation on 31 December
  2021"; older editions "REVISED EDITION 2008 (30th November 2008)"). An Act as passed: the commencement date printed
  under its long title; if the Act leaves commencement to a later notification, the day of the President's assent
  printed on the Act. Commits are dated noon Singapore time (+0800) on that day; commits on the same day are a second
  apart, ordered by folder.
- After the last 2020 Revised Edition commit (31 December 2021), one commit removes the folders of Acts that the 2020
  Revised Edition does not contain (repealed or renamed by then).
- Authors: the edition (`2008 Revised Edition <reved-2008@egazette.gov.sg.invalid>`) or the Act
  (`Act 15 of 2010 <act-2010-15@egazette.gov.sg.invalid>`); committer Lexifina.
- Trailers: `In-force`, `In-force-basis`, `Edition` or `Assented`, `Gazette` (supplement and publication day),
  `Source` (the PDF's address), `Text-source`, and `Not-split` where it applies.
- The history is appended to the earlier placeholder commits; nothing is rewritten.
