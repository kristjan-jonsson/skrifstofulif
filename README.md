# Skrifstofulífið

Dagleg skrýtla (3-ramma myndasaga) birt á GitHub Pages:
https://kristjan-jonsson.github.io/skrifstofulif/

Síðan er hreinn statísk HTML-síða án build-ferlis. `index.html` les `comics.json` og birtir nýjustu skrýtlu, með flettingu, handahófsvali, safni og varanlegum tenglum (`#YYYY-MM-DD`).

## Hvernig ný skrýtla er birt

1. Vista myndina sem `comics/YYYY-MM-DD.png` (t.d. `comics/2026-10-15.png`).
2. Bæta færslu aftast í `comics`-listann í `comics.json`:

```json
{
  "date": "2026-10-15",
  "title": "Stuttur titill",
  "image": "comics/2026-10-15.png",
  "alt": "Ein setning sem lýsir myndinni",
  "panels": [
    "Rammi 1 – Bjarni: „…“",
    "Rammi 2 – Gunnar: „…“",
    "Rammi 3 – Snæfríður: „…“"
  ]
}
```

`date`, `title` og `image` eru nauðsynleg; `alt`, `panels` og `id` eru valfrjáls. Ef fleiri en ein skrýtla er sama dag, gefðu þeim aukalegu `id` eins og `2026-10-13-2` (notað í varanlegum tenglum).

3. Commit-a og push-a á `main`:

```bash
git add .
git commit -m "Skrýtla 2026-10-15: Stuttur titill"
git push origin main
```

GitHub Pages uppfærir síðu sjálfkrafa innan 1–2 mínútna.

## Leyfi

© 2026 Kristján Jónsson. Skrýtlurnar og kóðinn eru gefin út undir [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE). Þér er frjálst að deila og aðlaga efnið, svo lengi sem þú getur höfundar.
