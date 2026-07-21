# -*- coding: utf-8 -*-
"""
build.py  -  template.html  ->  dist/index.html

Bouwt het zelfstandige portaal van As Gau Paust (de moedersite boven Denk mee,
Lees mee, Reken mee en Doe mee). Geen data-JSON: de enige "injectie" is het
gedeelde toren-logo en de vier blok-iconen, zodat er maar één bron van waarheid
is voor het merk. Zelf-gehoste fonts gaan mee naar dist/. Geen internet nodig.
"""
from pathlib import Path
import sys
import shutil

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

BASE = Path(__file__).parent
CUSTOM_DOMAIN = "asgaupaust.be"

# --- Het merk van het platform: de mug in de kamer (het originele As Gau Paust-beeld,
#     beelden/mug.png). De deelsites houden de Sint-Romboutstoren als sitemerk. ---
MARK = '<img src="/beelden/mug.png" alt="De mug in de kamer" width="512" height="512">'

# --- Vier blok-iconen (24x24, lijntekening in currentColor = pink). ---
def _ic(paths):
    return ('<svg class="ic-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="1.6" stroke-linecap="square" stroke-linejoin="round" aria-hidden="true">' + paths + '</svg>')

IC = {
    # Denk mee: gedachtenwolkje (echte wolkvorm) met drie punten en twee dalende bolletjes
    "__IC_DENK__": _ic('<g transform="translate(2.4 -1.5) scale(0.8)">'
                       '<path stroke-width="2" d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/></g>'
                       # De sleepbolletjes moeten de wolk NIET raken: op (7.6,16.4) r1.5 was de
                       # speling -0,16 (dus raak). Nagemeten langs de wolkrand: dit geeft ~0,8
                       # speling tot de wolk en ~0,8 tussen de bolletjes onderling.
                       '<circle cx="7.6" cy="17.2" r="1.3"/>'
                       '<circle cx="5.1" cy="20.9" r=".75"/>'),
    # Lees mee: document met tekstregels (het archief)
    "__IC_LEES__": _ic('<rect x="5" y="3" width="14" height="18"/>'
                       '<line x1="8" y1="8" x2="16" y2="8"/><line x1="8" y1="12" x2="16" y2="12"/>'
                       '<line x1="8" y1="16" x2="13" y2="16"/>'),
    # Reken mee: staafdiagram op een aslijn (de cijfers)
    "__IC_REKEN__": _ic('<line x1="4" y1="20" x2="20" y2="20"/>'
                        '<rect x="6" y="12" width="3" height="8"/><rect x="11" y="7" width="3" height="13"/>'
                        '<rect x="16" y="15" width="3" height="5"/>'),
    # En meer: een plusteken in een gestippeld kader (er komt nog bij)
    "__IC_MEER__": _ic('<rect x="4" y="4" width="16" height="16" stroke-dasharray="3 2.4"/>'
                       '<line x1="12" y1="8.5" x2="12" y2="15.5"/><line x1="8.5" y1="12" x2="15.5" y2="12"/>'),
}

# 1) Schil lezen en de placeholders invullen.
html = (BASE / "template.html").read_text(encoding="utf-8")
html = html.replace("__MARK__", MARK)
for key, svg in IC.items():
    html = html.replace(key, svg)

if "__" in html.replace("__PROJECTS", ""):  # ruwe waarschuwing bij een vergeten placeholder
    import re
    rest = re.findall(r"__[A-Z_]+__", html)
    if rest:
        print("       LET OP: niet-ingevulde placeholders:", ", ".join(sorted(set(rest))))

# 2) Eindproduct schrijven.
out_dir = BASE / "dist"
out_dir.mkdir(exist_ok=True)
(out_dir / "index.html").write_text(html, encoding="utf-8")

# 2b) Aparte pagina /en-meer/ : de filosofie van het platform. De ECHTE tekst staat er bewust
#     nog niet in (die werken we eerst uit voor we publiceren); dit is voorlopig een lorem-
#     plaatshouder. De pagina deelt de <head> van het portaal (zelfde CSS, fonts en merk),
#     met een eigen titel en omschrijving.
enmeer_tpl = BASE / "template-enmeer.html"
if enmeer_tpl.exists():
    import re
    m = re.search(r"<head>.*?</head>", html, flags=re.DOTALL)
    head = m.group(0) if m else ""
    head = re.sub(r"<title>.*?</title>",
                  "<title>En meer As Gau Paust</title>",
                  head, count=1, flags=re.DOTALL)
    head = re.sub(r'(<meta name="description" content=")[^"]*(">)',
                  r"\g<1>En meer: waar het experimentele platform van As Gau Paust voor staat en waar "
                  r"het heen groeit. Deze pagina is nog in de maak.\g<2>",
                  head, count=1, flags=re.DOTALL)
    enmeer_html = enmeer_tpl.read_text(encoding="utf-8").replace("__PORTAAL_HEAD__", head).replace("__MARK__", MARK)
    for _k, _svg in IC.items():
        enmeer_html = enmeer_html.replace(_k, _svg)
    (out_dir / "en-meer").mkdir(exist_ok=True)
    (out_dir / "en-meer" / "index.html").write_text(enmeer_html, encoding="utf-8")
    print("       en-meer-pagina gebouwd: dist/en-meer/index.html")

# 2c) Aparte pagina /pers/ : de persmap. Werkinstrument voor journalisten (feiten, een vaste omschrijving,
#     schrijfwijze, logo, contact). Deelt net als /en-meer/ de <head> van het portaal, met een
#     eigen titel en omschrijving. Geen persoonsnaam, geen externe verzoeken.
pers_tpl = BASE / "template-pers.html"
if pers_tpl.exists():
    import re
    m = re.search(r"<head>.*?</head>", html, flags=re.DOTALL)
    head = m.group(0) if m else ""
    head = re.sub(r"<title>.*?</title>",
                  "<title>Pers As Gau Paust</title>",
                  head, count=1, flags=re.DOTALL)
    head = re.sub(r'(<meta name="description" content=")[^"]*(">)',
                  r"\g<1>Persmap van As Gau Paust: de feiten, een kant-en-klare omschrijving, de juiste "
                  r"schrijfwijze, het logo en het perscontact van het platform voor hyperlokale journalistiek.\g<2>",
                  head, count=1, flags=re.DOTALL)
    pers_html = pers_tpl.read_text(encoding="utf-8").replace("__PORTAAL_HEAD__", head).replace("__MARK__", MARK)
    for _k, _svg in IC.items():
        pers_html = pers_html.replace(_k, _svg)
    (out_dir / "pers").mkdir(exist_ok=True)
    (out_dir / "pers" / "index.html").write_text(pers_html, encoding="utf-8")
    print("       pers-pagina gebouwd: dist/pers/index.html")

# 3) CNAME voor GitHub Pages. Eenmalig, pas bij live-zetten: Settings -> Pages ->
#    Custom domain = asgaupaust.be, plus een DNS-record naar <gebruiker>.github.io.
(out_dir / "CNAME").write_text(CUSTOM_DOMAIN + "\n", encoding="utf-8")

# 4) Zelf-gehoste lettertypes meekopieren naar dist/fonts/ (woff2 + OFL-licenties).
fonts_src = BASE / "fonts"
n = 0
if fonts_src.exists():
    fonts_dst = out_dir / "fonts"
    fonts_dst.mkdir(exist_ok=True)
    for f in fonts_src.iterdir():
        if f.suffix.lower() in (".woff2", ".txt"):
            shutil.copy2(f, fonts_dst / f.name)
            n += 1

# 4b) Beelden (het mug-merk) meekopieren naar dist/beelden/.
beelden_src = BASE / "beelden"
if beelden_src.exists():
    beelden_dst = out_dir / "beelden"
    beelden_dst.mkdir(exist_ok=True)
    for f in beelden_src.iterdir():
        if f.is_file():
            shutil.copy2(f, beelden_dst / f.name)

# 4c) PWA-bestanden: manifest en service worker meekopieren (installeerbaar op het beginscherm
#     + offline). Geen tracking, enkel een lokale cache op het toestel van de bezoeker.
for _naam in ("manifest.json", "sw.js"):
    _src = BASE / _naam
    if _src.exists():
        shutil.copy2(_src, out_dir / _naam)
        print("       PWA-bestand gekopieerd: dist/%s" % _naam)

print("Klaar! dist/index.html gebouwd: %s tekens" % format(len(html), ","))
print("       fonts gekopieerd naar dist/fonts/: %d bestanden" % n)
print("       CNAME: %s  (nog niet live; pas activeren wanneer je publiceert)" % CUSTOM_DOMAIN)
