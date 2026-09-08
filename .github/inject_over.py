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

# Deze injectie hoort ALLEEN in GitHub Actions te draaien. Lokaal zou ze de naam schrijven in
# dist/index.html, dist/pers/index.html en dist/privacy/index.html, en die drie staan onder
# versiebeheer: een volgende "git add -A" neemt de naam dan gewoon mee. Gemeten aanleiding:
# op 07/09/2026 belandde de naam op precies die manier in een commit, via een andere kopie van
# een gepubliceerde pagina. GitHub Actions zet GITHUB_ACTIONS zelf, dus in de workflow verandert
# er niets; wie het script hier probeert, krijgt een stop in plaats van een lek.
if not os.environ.get("GITHUB_ACTIONS"):
    raise SystemExit("inject_over.py draait alleen in GitHub Actions, niet lokaal.")

# --- 1. De initiatiefnemer-naam, in de "Wie zit hierachter"-uitklap. Die staat op /pers/ en
#        /privacy/. De startpagina droeg hem tot 07/09/2026 ook in het colofon; daar is hij weg
#        omdat hij dan drie keer op het portaal stond. dist/index.html blijft toch in de lijst:
#        keert het blok ooit terug, dan wordt het meteen weer bediend, en zonder placeholder is
#        de vervanging gewoon een lege bewerking. Het vangnet onderaan pakt een vergeten
#        placeholder sowieso op. ---
naam = os.environ.get("OVER_NAAM", "").strip()
for PAD in ("dist/pers/index.html", "dist/index.html", "dist/privacy/index.html"):
    if not os.path.exists(PAD):
        print("initiatiefnemer: %s ontbreekt, overgeslagen" % PAD)
        continue
    s = open(PAD, encoding="utf-8").read()
    if naam:
        s = s.replace("%%OVER_NAAM%%", naam)
    else:
        # geen naam: de hele placeholder-zin weg (niet-hebzuchtig, blijft binnen die ene <p>)
        s = re.sub(r'\s*<p class="wie-init">.*?</p>', "", s, flags=re.DOTALL)
    open(PAD, "w", encoding="utf-8").write(s)
    print("initiatiefnemer (%s): %s" % (PAD, "gezet" if naam else "geen secret, zin verwijderd"))

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
