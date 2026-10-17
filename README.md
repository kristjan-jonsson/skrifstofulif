# Skrifstofulífið

Dagleg skrýtla (3-ramma myndasaga): https://skrifstofulif.oskasteinar.is/

![Kerfismynd af Skrifstofulífinu](docs/skrifstofulif-kerfismynd.png)

- **Skrýtlur:** Claude Routine keyrir daglega, fylgir [`LEIDBEININGAR.md`](LEIDBEININGAR.md) og push-ar nýrri mynd í `comics/` og færslu í `comics.json` á `main`.
- **Síðan:** `pages.yml` byggir síðuna, RSS-strauminn (`feed.xml`) og deilisíður og birtir á GitHub Pages. `index.html` er statísk síða sem les `comics.json`.
- **Atkvæði (👍/👎):** Cloudflare Worker (`worker/`) ræsir `vote.yml`, sem uppfærir `votes.json` á greininni `votes`. Uppsetning: [`voting-setup.md`](voting-setup.md).

## Leyfi

© 2026 Kristján Jónsson. Skrýtlurnar og kóðinn eru gefin út undir [CC BY 4.0](LICENSE).
