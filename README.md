# Singapore law: building

This repository is being built: Singapore's Acts as git history, one file per section, one commit per amending law
on the day it took effect, following the same rules as the other lexifina law repositories.

**Source.** Singapore Statutes Online (https://sso.agc.gov.sg), the Attorney-General's Chambers' consolidated
legislation, with every version of each Act it holds (back to 1987 for older Acts) and the amending legislation SSO
pairs with each version.

**Pace.** SSO's Terms of Use (clause 13(d)) allow automated reading only between 3 a.m. and 7 a.m. Singapore time,
and its robots.txt asks for 6 seconds between requests. Reading is done one request at a time inside that window
only, so the full history takes several nights; acts are added here as each one is read whole and checked.
Every act not yet here will be listed in data/held.json with its reason.

The Singapore legislation in this repository is subject to copyright of the Singapore Government and is reproduced
with the permission of the Attorney-General's Chambers. Check Singapore Statutes Online for the latest version of
Singapore legislation.
