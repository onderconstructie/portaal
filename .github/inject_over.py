#!/usr/bin/env python3
"""Stikt de geheime inhoud in dist/, vlak voor het publiceren.

Twee dingen staan BEWUST niet in de repo en komen enkel uit GitHub-secrets
(Settings -> Secrets and variables -> Actions):

1. OVER_NAAM: de naam van de initiatiefnemer, in de placeholder %%OVER_NAAM%%
   van dist/index.html. Is de secret leeg, dan verdwijnt de hele zin.

2. ENMEER_FILOSOFIE: de filosofietekst van het platform, als platte tekst met
   lege regels tussen de alinea's. Elke alinea wordt hier een <p> in
   dist/en-meer/index.html; het plaatshouder-blok verdwijnt dan. Is de secret
   leeg, dan blijft de plaatshouder staan en verdwijnt het lege echt-blok.
"""
import html as htmllib
import os
import re

# --- 1. De initiatiefnemer-naam op het portaal. ---
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

# --- 2. De filosofie op /en-meer/. ---
PAD2 = "dist/en-meer/index.html"
tekst = os.environ.get("ENMEER_FILOSOFIE", "").strip()
if os.path.exists(PAD2):
    s = open(PAD2, encoding="utf-8").read()
    if tekst:
        # platte tekst -> <p>-alinea's (een eventuele "# titel"-regel slaan we over:
        # de pagina heeft haar eigen hoofdtitel)
        alineas = [a.strip() for a in re.split(r"\n\s*\n", tekst)
                   if a.strip() and not a.strip().startswith("#")]
        blok = "\n".join("  <p>%s</p>" % htmllib.escape(" ".join(a.split())) for a in alineas)
        s = s.replace("%%ENMEER_FILOSOFIE%%", blok)
        s = re.sub(r'\s*<div id="filosofie-plaatshouder">.*?</div>', "", s, flags=re.DOTALL)
        # de pagina is niet langer "in de maak"
        s = s.replace("En meer &#183; in de maak", "En meer &#183; de filosofie")
        s = re.sub(r'(<meta name="description" content=")[^"]*(">)',
                   r"\g<1>En meer: waar het experimentele platform van As Gau Paust voor staat "
                   r"en waar het heen groeit, in mensentaal.\g<2>", s, count=1)
        open(PAD2, "w", encoding="utf-8").write(s)
        print("filosofie: gezet (%d alinea's)" % len(alineas))
    else:
        s = re.sub(r'\s*<div id="filosofie-echt">.*?</div>', "", s, flags=re.DOTALL)
        open(PAD2, "w", encoding="utf-8").write(s)
        print("filosofie: geen secret, plaatshouder blijft staan")
