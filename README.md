# As Gau Paust (portaal)

De moedersite op [asgaupaust.be](https://asgaupaust.be), de voordeur van de
"... mee met Mechelen"-familie:

- **Denk mee** — [denkmee.asgaupaust.be](https://denkmee.asgaupaust.be): de besluitvorming in mensentaal
- **Lees mee** — [leesmee.asgaupaust.be](https://leesmee.asgaupaust.be): zeven jaar archief, plus de formule
- **Reken mee** — het bestuur in cijfers, nog in de maak
- **En meer** — [asgaupaust.be/en-meer](https://asgaupaust.be/en-meer/): waarom dit platform bestaat

Het portaal draagt ook de [persmap](https://asgaupaust.be/pers/) en de
[privacyverklaring](https://asgaupaust.be/privacy/) van de hele familie.

## Bouwen en publiceren

```
python build.py     # template.html -> dist/ (logo en iconen worden ingevuld)
```

`dist/` publiceert via de GitHub Pages-workflow (`.github/workflows/pages.yml`).
Zelfde opzet als de deelsites: zelf-gehoste fonts, geen cookies, geen trackers,
geen externe verzoeken.
