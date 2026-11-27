# Structure

How this repository lays out Singapore's law. Agreed before any bulk reading; the builder follows it exactly.

## Source

The Republic of Singapore Government Gazette, Electronic Edition (eGazette), Government of Singapore (MDDI): the
revised editions of Acts in its Revised Acts supplement (1999 to 2022, including the 2020 Revised Edition, in operation
on 31 December 2021) and the Acts as passed in its Acts Supplement (1998 to 2026). Each is one PDF with a text layer;
no OCR is used. Singapore Statutes Online (SSO) was planned as the source; it is not used (see the README).

## Folders and files

- `acts/<title>/`: one folder per Act, named from its short title in English (Singapore's legislative language),
  lower case with hyphens and without the year or chapter number: `acts/constitution-of-the-republic-of-singapore/`,
  `acts/companies-act/`, `acts/penal-code/`. Each commit to it is a revised edition of the whole Act.
- `acts-as-passed/<year>/<number>-<title>/`: one folder per Act as passed by Parliament, by year and Act number:
  `acts-as-passed/2010/015-criminal-procedure-code/`. Amending Acts are here, as enacted.
- One file per section (per Article in the Constitution): `section-001.md`, `section-017a.md`, `article-022h.md`.
  Numbers are zero-padded to three digits; a letter suffix is lower case.
- One file per Schedule: `schedule.md` (a single Schedule), `schedule-01.md` (First Schedule), `schedule-02.md`, ...
- `title.md`: the title page, the long title, the commencement line and the enacting words.
- `legislative-history.md`: the Law Revision Commission's legislative history, where the edition prints one (not
  part of the Act).
- Each provision file starts with its heading line (`# 9. Liberty of the person`) and lines for its context
  (`Part:`, `Chapter:`, `Division:`). The text follows, one paragraph per subsection or item, as the Gazette prints
  it. Amendment notes (`[19/2016; 15/2019]`) are kept, since they are part of the printed text.
- `data/acts.csv`: every folder and the in-force day of its latest version. `data/held.csv`: PDFs not committed, with
  the reason.

## Commits

- One commit per revised edition and per Act as passed, in in-force order.
- Date: noon Singapore time (+0800) on the in-force day (see REPRODUCE.md for where each day comes from).
- Author: the edition (`2020 Revised Edition`) or the Act (`Act 15 of 2010`); committer Lexifina.
- Trailers: `In-force:` (YYYY-MM-DD), `In-force-basis:`, `Edition:` or `Assented:`, `Gazette:`, `Source:`,
  `Text-source:`.

## global-law

`corpus.json` names the corpus `sg/national/acts` (3-part form).

## Order of work

Core law first: the Constitution, the Penal Code, Criminal Procedure Code, Evidence Act, Companies Act, Employment
Act, Civil Law Act, Land Titles Act and other principal Acts; then every revised edition; then the Acts as passed;
then revised subsidiary legislation.
