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

Þetta verkefni er gefið út undir MIT-leyfi.

Copyright (c) 2026 Kristján Jónsson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
