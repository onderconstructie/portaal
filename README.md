# As Gau Paust (portaal)

De moedersite op [asgaupaust.be](https://asgaupaust.be): één pagina die met grote
blokken doorverwijst naar de deelsites van de "... mee met Mechelen"-familie.

- **Denk mee** — [denkmee.asgaupaust.be](https://denkmee.asgaupaust.be): de besluitvorming in mensentaal
- **Lees mee** — [leesmee.asgaupaust.be](https://leesmee.asgaupaust.be): zeven jaar archief, plus het handboek
- **Reken mee** — het bestuur in cijfers (binnenkort)
- **En meer** — extra toepassingen in voorbereiding

## Bouwen en publiceren

```
python build.py     # template.html -> dist/ (logo en iconen worden ingevuld)
deploy.bat          # bouwen + committen + pushen; GitHub Actions publiceert dist/
```

Zelfde opzet als de deelsites: zelf-gehoste fonts (Geist + JetBrains Mono, OFL),
geen cookies, geen trackers, geen externe verzoeken.
