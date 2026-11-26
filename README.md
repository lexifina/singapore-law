# Singapore: law history in git

The law of Singapore as a git history, once it is built: one file per section or schedule of an Act, one commit per version on the day it took effect, and the legislation that made each change as the commit's author. `git blame` will name the law behind every line; `git log` will list every change to a section; picking a date will give the text in force that day.

Part of [lexifina/global-law](https://github.com/lexifina/global-law), one git history for every country's law: this is Singapore's national law, which global-law reads at `singapore/national/acts/`.

**What is in it now:** no law text yet; this README is the only file. There is nothing yet to run git commands on, and global-law, which already lists Singapore, has no Singaporean text to search.

**What is planned:** every Act on Singapore Statutes Online (SSO), current and repealed, with every version on its legislation timeline, each credited to what SSO pairs with it (an amending Act, a piece of subsidiary legislation or a revised edition); subsidiary legislation itself once every Act is in. An act is added only after it has been read whole and checked.

**Why there is none yet.** SSO's Terms of Use (clause 13(d)) allow automated reading only between 3 and 7 a.m. Singapore time, and its robots.txt asks for 6 seconds between requests. On 10 November 2026 SSO refused the first requests made inside that window (HTTP 403); requests on 26 November 2026 were answered, and reading resumes inside the permitted hours from that night. The layout is in [STRUCTURE.md](STRUCTURE.md).

The Acts are in English, as SSO publishes them.

## Sources

| Source | Kind | Past versions | Notes |
| --- | --- | --- | --- |
| [Singapore Statutes Online](https://sso.agc.gov.sg) (Attorney-General's Chambers) | Consolidated legislation; its Terms of Use say it is not the authoritative text | yes, a legislation timeline per Act | Automated reading only from 3 to 7 a.m. Singapore time (Terms of Use, clause 13(d)) |

## Licence

There is no legal text here yet, and no `LICENSE`. SSO's Terms of Use (clause 13) allow Singapore legislation to be reproduced if the reproduction says that it is subject to copyright of the Singapore Government and reproduced with the permission of the Attorney-General's Chambers, and that readers may check [Singapore Statutes Online](https://sso.agc.gov.sg) for the latest version; the acts will carry that notice when they are added.

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
