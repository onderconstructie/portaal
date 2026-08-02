# -*- coding: utf-8 -*-
"""
build.py  -  template.html  ->  dist/index.html

Bouwt het zelfstandige portaal van As Gau Paust (de moedersite boven Denk mee,
Lees mee, Reken mee en En meer). Geen data-JSON: de enige "injectie" is het
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

def subpagina_head(portaal_html, titel, omschrijving, url):
    """De <head> van het portaal hergebruiken, maar met de eigen identiteit van de subpagina.

    Naast <title> en de description moeten ook de deelkaart-tags mee: anders toont een gedeelde
    link naar /pers/ of /en-meer/ de titel en omschrijving van de startpagina. og:image blijft
    voor alle pagina's hetzelfde merkbeeld; dat is bewust, het is één familie.
    """
    import re
    m = re.search(r"<head>.*?</head>", portaal_html, flags=re.DOTALL)
    head = m.group(0) if m else ""
    head = re.sub(r"<title>.*?</title>", "<title>%s</title>" % titel, head, count=1, flags=re.DOTALL)
    for patroon, nieuw in (
        (r'(<meta name="description" content=")[^"]*(">)', omschrijving),
        (r'(<meta property="og:title" content=")[^"]*(">)', titel),
        (r'(<meta property="og:description" content=")[^"]*(">)', omschrijving),
        (r'(<meta property="og:url" content=")[^"]*(">)', url),
        (r'(<link rel="canonical" href=")[^"]*(">)', url),
    ):
        head = re.sub(patroon, lambda mm, w=nieuw: mm.group(1) + w + mm.group(2), head, count=1)
    return head


def strip_html_commentaar(s):
    """Haalt HTML-commentaren uit een gebouwde pagina: dev-notities horen in de template (voor
    onderhoud), niet in de publieke view-source. Non-greedy en veilig omdat geen <script> op deze
    pagina de reeks <!-- of --> bevat; ruimt ook de lege regel op die een gestript blok achterlaat."""
    import re
    return re.sub(r"[ \t]*<!--.*?-->[ \t]*\n?", "", s, flags=re.DOTALL)

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

# 2b) Aparte pagina /en-meer/ : de filosofie van het platform. De tekst staat rechtstreeks in
#     template-enmeer.html (op keuze van de maker); enkel de NAAM van de initiatiefnemer blijft
#     uit git en wordt bij het publiceren uit de secret OVER_NAAM gestikt (.github/inject_over.py).
#     De pagina deelt de <head> van het portaal (zelfde CSS, fonts en merk), met een eigen titel
#     en omschrijving.
enmeer_tpl = BASE / "template-enmeer.html"
if enmeer_tpl.exists():
    head = subpagina_head(
        html,
        "En meer As Gau Paust",
        "En meer: de filosofie van As Gau Paust. Waar het experimentele platform voor staat "
        "en waar het heen groeit.",
        "https://asgaupaust.be/en-meer/")
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
    head = subpagina_head(
        html,
        "Pers As Gau Paust",
        "Persmap van As Gau Paust: de feiten, een kant-en-klare omschrijving, de juiste "
        "schrijfwijze, het logo en het perscontact van het platform voor hyperlokale journalistiek.",
        "https://asgaupaust.be/pers/")
    pers_html = pers_tpl.read_text(encoding="utf-8").replace("__PORTAAL_HEAD__", head).replace("__MARK__", MARK)
    for _k, _svg in IC.items():
        pers_html = pers_html.replace(_k, _svg)
    pers_html = strip_html_commentaar(pers_html)  # dev-notities weg uit de publieke view-source (blijven in de template)
    (out_dir / "pers").mkdir(exist_ok=True)
    (out_dir / "pers" / "index.html").write_text(pers_html, encoding="utf-8")
    print("       pers-pagina gebouwd: dist/pers/index.html")

# 2c-bis) Aparte pagina /privacy/ : de privacyverklaring. Nodig omdat een bezoeker sowieso zijn
#     IP-adres bij de host achterlaat, ook op een site zonder cookies en zonder trackers; de
#     informatieplicht geldt dan. Draagt wél de naam van de verantwoordelijke (via de secret,
#     zoals /en-meer/), want een privacyverklaring hoort te zeggen wie erachter zit.
privacy_tpl = BASE / "template-privacy.html"
if privacy_tpl.exists():
    head = subpagina_head(
        html,
        "Privacy op As Gau Paust",
        "Wat er met je gegevens gebeurt op de sites van As Gau Paust: geen cookies, geen "
        "trackers, geen statistieken. Wat je instelt blijft in je eigen browser.",
        "https://asgaupaust.be/privacy/")
    privacy_html = privacy_tpl.read_text(encoding="utf-8").replace("__PORTAAL_HEAD__", head).replace("__MARK__", MARK)
    for _k, _svg in IC.items():
        privacy_html = privacy_html.replace(_k, _svg)
    privacy_html = strip_html_commentaar(privacy_html)  # dev-notities niet mee naar de publieke bron
    (out_dir / "privacy").mkdir(exist_ok=True)
    (out_dir / "privacy" / "index.html").write_text(privacy_html, encoding="utf-8")
    print("       privacy-pagina gebouwd: dist/privacy/index.html")

# 2d) Eigen 404-pagina. GitHub Pages toont zonder dit bestand zijn eigen Engelstalige
#     "Page not found"-scherm: geen merk, geen Nederlands, geen weg terug. Eén typfout in een
#     gedeelde link volstaat om daar te belanden, dus dit hoort bij de schil van de site.
#     Zelfstandig bestand (eigen stijl inline): een 404 mag niet afhangen van de rest.
PAGINA_404 = """<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#FF0066">
<title>Pagina niet gevonden, As Gau Paust</title>
<meta name="robots" content="noindex">
<link rel="icon" type="image/png" href="/beelden/mug.png">
<style>
@font-face{font-family:'Geist';font-style:normal;font-weight:100 900;font-display:swap;src:url('/fonts/geist-var.woff2') format('woff2')}
@font-face{font-family:'JetBrains Mono';font-style:normal;font-weight:100 800;font-display:swap;src:url('/fonts/jbmono-var.woff2') format('woff2')}
*{box-sizing:border-box}
body{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;
  background:#f5f1e8;color:#2b2621;font-family:'Geist',system-ui,sans-serif;line-height:1.6;padding:1.5rem}
.doos{max-width:34rem;text-align:center}
.mug{width:96px;height:96px;border-radius:50%;margin:0 auto 1.6rem;display:block}
.code{font-family:'JetBrains Mono',ui-monospace,monospace;font-size:.72rem;letter-spacing:.14em;
  text-transform:uppercase;color:#c80054;margin:0 0 .6rem}
h1{font-family:'JetBrains Mono',ui-monospace,monospace;font-size:clamp(1.5rem,5vw,2.2rem);
  font-weight:600;letter-spacing:-.02em;margin:0 0 .9rem}
p{color:#514a40;margin:0 0 1.8rem}
.wegen{display:flex;flex-wrap:wrap;gap:.7rem;justify-content:center}
.wegen a{font-family:'JetBrains Mono',ui-monospace,monospace;font-size:.74rem;letter-spacing:.06em;
  text-transform:uppercase;text-decoration:none;padding:.7rem 1.1rem;border-radius:999px;
  border:1px solid rgba(0,0,0,.18);color:#2b2621;transition:.15s}
.wegen a:hover{border-color:#FF0066;color:#c80054}
.wegen a.prim{background:#FF0066;border-color:#FF0066;color:#fff}
.wegen a.prim:hover{background:#b3004a;border-color:#b3004a;color:#fff}
</style>
</head>
<body>
  <main class="doos">
    <img class="mug" src="/beelden/mug.png" alt="" aria-hidden="true" width="512" height="512">
    <p class="code">Fout 404</p>
    <h1>Deze pagina bestaat niet</h1>
    <p>Misschien is de link verouderd, of staat er een tikfout in het adres.
       Hieronder raak je weer op weg.</p>
    <div class="wegen">
      <a class="prim" href="/">Naar de startpagina</a>
      <a href="https://denkmee.asgaupaust.be/">Denk mee</a>
      <a href="https://leesmee.asgaupaust.be/">Lees mee</a>
      <a href="/pers/">Persmap</a>
    </div>
  </main>
</body>
</html>
"""
(out_dir / "404.html").write_text(PAGINA_404, encoding="utf-8")
print("       404-pagina gebouwd: dist/404.html")

# 3) CNAME voor GitHub Pages. Eenmalig, pas bij live-zetten: Settings -> Pages ->
#    Custom domain = asgaupaust.be, plus een DNS-record naar <gebruiker>.github.io.
(out_dir / "CNAME").write_text(CUSTOM_DOMAIN + "\n", encoding="utf-8")

# robots.txt. Er stond er geen, dus elke bot kreeg tot nu toe helemaal geen signaal (en bij een
# eigen domein zet GitHub Pages er zelf niets neer). Bewust OPEN: deze site bestaat om gevonden
# en gelezen te worden, en het project draait om hergebruik. Zelf de deur dichtdoen die we bij
# het stadsportaal voorbijlopen, zou slecht passen. Enkel de eigen foutpagina blijft eruit.
ROBOTS = """# %s
# Van harte welkom. Deze site is openbaar en mag gelezen, geciteerd en hergebruikt worden.
# De code staat publiek. Wil je zoiets voor je eigen stad bouwen, neem gerust contact op.
User-agent: *
Allow: /
Disallow: /404.html

# Zoekmachines en archieven blijven welkom: gevonden en bewaard worden is het punt.
# Deze crawlers niet. Ze brengen geen lezers, ze verzamelen linkprofielen om door te
# verkopen aan marketingbureaus, en ze halen daarvoor telkens de volledige pagina op.
User-agent: AhrefsBot
User-agent: SemrushBot
User-agent: MJ12bot
User-agent: DotBot
User-agent: BLEXBot
User-agent: DataForSeoBot
User-agent: Barkrowler
User-agent: SEOkicks
Disallow: /
"""
(out_dir / "robots.txt").write_text(ROBOTS % CUSTOM_DOMAIN, encoding="utf-8")
print("       robots.txt geschreven (open, zoekmachines welkom)")

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
