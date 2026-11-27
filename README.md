# Singapore: law history in git

The law of Singapore as a git history: one file per section or schedule of an Act, one commit per version on the day it took effect, and the legislation that made each change as the commit's author. `git blame` names the edition or Act behind every line; `git log` lists every change to a section; picking a date gives the text in force that day, as far as the record goes.

Part of [lexifina/global-law](https://github.com/lexifina/global-law), one git history for every country's law: this is Singapore's national law, which global-law reads at `singapore/national/acts/`.

**What is in it now:** 512 Acts by title under `acts/`, each as every revised edition the Government Gazette published from 1999 to 2022, ending with the 2020 Revised Edition of every Act in force on 31 December 2021 (926 editions in all), and 1,086 Acts as passed by Parliament from 1998 to 2026 under `acts-as-passed/<year>/` (the Constitution and its amending Acts, the Penal Code, the Criminal Procedure Code, the Evidence Act, the Companies Act, the Employment Act, the Civil Law Act and the Land Titles Act among them). Changes made by amending Acts after an Act's last revised edition are in those amending Acts, not yet merged into the Act's own sections. Versions not committed are listed in [data/held.csv](data/held.csv).

**What is planned:** revised subsidiary legislation from the Gazette; then the versions between revised editions, where an open source gives them.

**Where the text comes from.** Every text is the Gazette's own PDF, read from its text layer (no OCR): the revised editions in its Revised Acts supplement and the Acts in its Acts Supplement. Singapore Statutes Online (SSO), which holds every point-in-time version, is not used: its Terms of Use (clause 13(d)) allow automated reading only between 3 and 7 a.m. Singapore time, and inside that window its AWS firewall answered our requests with a challenge page on 28 October and 26 November 2026 (and a block on 10 November 2026), which we do not get round. The layout is in [STRUCTURE.md](STRUCTURE.md); how it is built is in [REPRODUCE.md](REPRODUCE.md).

The Acts are in English, as the Gazette publishes them.

## Sources

| Source | Kind | Past versions | Notes |
| --- | --- | --- | --- |
| [Republic of Singapore Government Gazette](https://www.egazette.gov.sg) (eGazette) | Revised editions of Acts (1999 to 2022, including the 2020 Revised Edition); Acts as passed (1998 to 2026) | yes: each revised edition, dated by its title page | Reproduced under clause 11 of the eGazette Terms of Use; see [LICENSE](LICENSE) |
| [Singapore Statutes Online](https://sso.agc.gov.sg) (Attorney-General's Chambers) | Consolidated legislation, every version | yes | Not used: automated reading only from 3 to 7 a.m. Singapore time (Terms of Use, clause 13(d)), and challenged by its firewall inside that window |

## Licence

The e-Gazettes reproduced here are subject to copyright of the Singapore Government and are reproduced with the permission of the Singapore Government (eGazette Terms of Use, clause 11); readers may check [egazette.gov.sg](https://www.egazette.gov.sg) for the latest e-Gazettes. Lexifina's own work (the history, tables, documents and tools) is CC0. Details are in [LICENSE](LICENSE).

## How it is checked

- [vulnerabilities/](vulnerabilities/): possible drafting mistakes in this law, found by global-law's detectors and checked by hand. Not run yet.

## Visualisations

- [visualisations/](visualisations/): charts drawn from this repository. Not drawn yet.

## More

From [lexifina/global-law](https://github.com/lexifina/global-law):

- [FEATURES.md](https://github.com/lexifina/global-law/blob/main/FEATURES.md): every feature, and what every corpus must support (`git blame`, `law.py`, the MCP tools)
- [FAQ.md](https://github.com/lexifina/global-law/blob/main/FAQ.md): questions and answers · [CONTRIBUTING.md](https://github.com/lexifina/global-law/blob/main/CONTRIBUTING.md): proposing changes · [MCP.md](https://github.com/lexifina/global-law/blob/main/MCP.md): the MCP server · [REPRODUCE.md](https://github.com/lexifina/global-law/blob/main/REPRODUCE.md): how it was built · [CHANGELOG.md](https://github.com/lexifina/global-law/blob/main/CHANGELOG.md)
- [FRESHNESS.md](https://github.com/lexifina/global-law/blob/main/FRESHNESS.md): how current each corpus is · [Monitoring](https://github.com/lexifina/global-law/tree/main/monitoring): whether updates are running · [WATCHING.md](https://github.com/lexifina/global-law/blob/main/WATCHING.md): how each official source is watched for changes
- [performance/](https://github.com/lexifina/global-law/tree/main/performance): how fast the tools are, measured
- [visualisations/](https://github.com/lexifina/global-law/tree/main/visualisations): charts and bridges across the world's law
- [Vulnerabilities](https://github.com/lexifina/global-law/tree/main/vulnerabilities): mistakes in legislation as published
