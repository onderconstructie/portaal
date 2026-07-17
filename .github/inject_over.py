#!/usr/bin/env python3
"""Stikt de initiatiefnemer-naam in dist/index.html, vlak voor het publiceren.

De naam staat BEWUST niet in de repo. Hij komt enkel uit de GitHub-secret OVER_NAAM
(Settings -> Secrets and variables -> Actions) en wordt hier in de placeholder
%%OVER_NAAM%% gestikt. Zo staat de naam wel op de live site, maar nooit in git.

Is de secret leeg of niet gezet, dan halen we de hele 'Initiatiefnemer'-zin weg, zodat
er nooit een ruwe placeholder op de site verschijnt.
"""
import os
import re

PAD = "dist/index.html"

naam = os.environ.get("OVER_NAAM", "").strip()
s = open(PAD, encoding="utf-8").read()

if naam:
    s = s.replace("%%OVER_NAAM%%", naam)
else:
    # geen naam: de hele placeholder-zin weg (niet-hebzuchtig, blijft binnen die ene <p>)
    s = re.sub(r'\s*<p class="wie-init">.*?</p>', "", s, flags=re.DOTALL)

open(PAD, "w", encoding="utf-8").write(s)
print("initiatiefnemer: " + ("gezet" if naam else "geen secret, zin verwijderd"))
