# Skrifstofulífið

Dagleg skrýtla (3 ramma myndasaga) birt á GitHub Pages:
https://kristjan-jonsson.github.io/skrifstofulif/

Síðan er hrein statísk HTML-síða (engin build). `index.html` les `comics.json` og birtir nýjustu skrýtluna, með flettingu, handahófsvali, safni og varanlegum tenglum (`#YYYY-MM-DD`). Ef `comics.json` er tómt birtist biðsíða.

## Hvernig ný skrýtla er birt (fyrir daglegu rútínuna)

1. Vista myndina sem `comics/YYYY-MM-DD.png` (t.d. `comics/2026-10-15.png`).
2. Bæta færslu aftast í `comics` fylkið í `comics.json`:

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

   `date`, `title` og `image` eru nauðsynleg; `alt`, `panels` og `id` valkvæð. Ef fleiri en ein skrýtla er sama dag, gefðu þeim aukalegu `id` eins og `2026-10-13-2` (notað í varanlega tenglinum `#id`) og vistaðu myndina undir sama nafni. Röðin skiptir ekki máli – síðan raðar eftir `date`. Ef færsla með sömu dagsetningu er til, skipta henni út frekar en að bæta við.
3. Commit og push á `main`, t.d. `git commit -m "Skrýtla 2026-10-15: Stuttur titill"`. GitHub Pages uppfærist innan 1–2 mínútna.

Push með PAT: `git push https://x-access-token:${GITHUB_TOKEN}@github.com/kristjan-jonsson/skrifstofulif.git main`
(PAT þarf aðeins *Contents: Read and write* á þessari einu geymslu.)
