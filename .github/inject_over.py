#!/usr/bin/env python3
"""Stikt de geheime inhoud in dist/, vlak voor het publiceren.

Nog EEN ding staat bewust niet in de repo en komt uit een GitHub-secret
(Settings -> Secrets and variables -> Actions):

- OVER_NAAM: de naam van de initiatiefnemer, in de placeholder %%OVER_NAAM%%
  van dist/en-meer/index.html. Is de secret leeg, dan verdwijnt de hele zin.

De filosofietekst kwam hier vroeger ook langs (secret ENMEER_FILOSOFIE), maar staat
sinds 20/07/2026 op uitdrukkelijke keuze van de maker gewoon in template-enmeer.html.
Die secret wordt niet meer gelezen en mag in GitHub verwijderd worden.
"""
import os
import re

# --- 1. De initiatiefnemer-naam, op /en-meer/ (daar staat de wie-sectie sinds de verhuizing). ---
PAD = "dist/en-meer/index.html"
naam = os.environ.get("OVER_NAAM", "").strip()
if os.path.exists(PAD):
    s = open(PAD, encoding="utf-8").read()
    if naam:
        s = s.replace("%%OVER_NAAM%%", naam)
    else:
        # geen naam: de hele placeholder-zin weg (niet-hebzuchtig, blijft binnen die ene <p>)
        s = re.sub(r'\s*<p class="wie-init">.*?</p>', "", s, flags=re.DOTALL)
    open(PAD, "w", encoding="utf-8").write(s)
    print("initiatiefnemer: " + ("gezet" if naam else "geen secret, zin verwijderd"))
else:
    print("initiatiefnemer: %s ontbreekt, overgeslagen" % PAD)

# --- 2. Vangnet: nooit een rauwe placeholder publiceren. ---
#     Verhuist een blok ooit naar een ander bestand terwijl dit script nog naar het oude wijst,
#     dan zou %%OVER_NAAM%% letterlijk op de site belanden. Liever de publicatie afbreken.
for wortel, _mappen, bestanden in os.walk("dist"):
    for bestand in bestanden:
        if not bestand.endswith(".html"):
            continue
        pad = os.path.join(wortel, bestand)
        inhoud = open(pad, encoding="utf-8").read()
        for merk in ("%%OVER_NAAM%%",):
            if merk in inhoud:
                raise SystemExit("FOUT: %s staat nog in %s. Publiceren afgebroken." % (merk, pad))
print("vangnet: geen rauwe placeholders in dist/")
