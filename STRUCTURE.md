# Structure

How this repository lays out Singapore's law. Agreed before any bulk reading; the builder follows it exactly.

## Source

[Singapore Statutes Online](https://sso.agc.gov.sg) (SSO), Attorney-General's Chambers. Each Act's page lists its
legislation timeline: one entry per version, with the day the version took effect (`ValidDate`) and what made it
("Amended by Act 9 of 2025", "Amended by S 123/2024", "2020 RevEd"). Each version is read whole, in one request, from
SSO's own print view (`/Act/<code>[/Historical/<date>]?...&ViewType=Print&PrintType=html&ProvIds=all-.,toc-.`), which
is HTML with a text layer: no PDF and no OCR is used.

Reading follows SSO's Terms of Use, clause 13(d): automated reading only between 3 and 7 a.m. Singapore time
(19:00 to 23:00 UTC), one request at a time, at least 6 seconds apart (robots.txt `crawl-delay: 6`), with back-off on
any 403, 429 or 5xx.

## Folders and files

- `acts/<title>/`: one folder per Act, named from its current short title in English (Singapore's legislative
  language), lower case with hyphens and without the year: `acts/constitution-of-the-republic-of-singapore/`,
  `acts/companies-act/`, `acts/penal-code/`. A title shared by two Acts takes the year: `acts/<title>-<year>/`.
- One file per section (per Article in the Constitution): `section-001.md`, `section-017a.md`, `article-022h.md`.
  Numbers are zero-padded to three digits; a letter suffix is lower case.
- One file per Schedule: `first-schedule.md`, `schedule.md`, `schedule-02.md`.
- `title.md`: the long title, the commencement date line and the revised-edition note.
- Each provision file starts with its heading line (`# 9. Liberty of the person`) and lines for its context
  (`Part:`, `Division:`, `Chapter:`). The text follows, one paragraph per subsection or item, as SSO prints it.
  SSO's amendment notes (`[Act 32 of 2021 wef 14/01/2022]`) are kept, since they are part of SSO's text.
- `data/acts.csv`: SSO code, folder, title, status (current/repealed), number of versions on SSO and in git.
- `data/held.csv`: versions not committed, with the reason.

## Commits

- One commit per version on an Act's SSO timeline, in in-force order across all Acts.
- Date: noon Singapore time (+0800) on the version's `ValidDate`. Versions sharing a day are ordered by Act, then by
  seconds 00, 01, ... only to keep order.
- Author: what SSO names for the version: `Act 9 of 2025 <act-2025-9@sso.agc.gov.sg.invalid>`,
  `S 123/2024 <s-2024-123@sso.agc.gov.sg.invalid>`, `2020 Revised Edition <reved-2020@sso.agc.gov.sg.invalid>`; for the
  oldest version SSO holds, what made it (usually a revised edition). Committer: Lexifina.
- Trailers: `In-force:` (YYYY-MM-DD), `In-force-basis:` (where the day comes from: the SSO timeline's ValidDate),
  `Amended-by:` (each act SSO lists for the version), `Act:` (SSO code), `Source:` (the version's SSO address).

## global-law

`corpus.json` names the corpus `sg/national/acts` (3-part form).

## Order of work

Core law first: the Constitution, then the Penal Code, Criminal Procedure Code, Evidence Act, Companies Act,
Interpretation Act, Supreme Court of Judicature Act, Civil Law Act, Contracts and other principal Acts; then every
current Act; then repealed Acts; then subsidiary legislation.
