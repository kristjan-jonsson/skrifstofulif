# Leiðbeiningar fyrir skrýtlugerð

Þessi skrá stýrir sjálfvirku verkinu sem býr til og birtir skrýtlu dagsins. Verkið les hana í upphafi hverrar keyrslu og fylgir henni. Breyttu þessari skrá til að breyta persónum, stíl eða ferli.

Engar spurningar – enginn er við; taktu skynsamlegar ákvarðanir.

## Markmið

Góð brandarateikning (3 ramma myndasaga) á íslensku með húmor í anda Dilbert: skrifstofuháð, fáránleiki fyrirtækjamenningar, fundir, ráðgjafar, gervigreind, ferlar og eyðublöð, upplýsingatækni, bankar o.fl. Metnaðarfullar myndir OG metnaðarfullir brandarar.

## Föst persónuskrá

Upprunalegar persónur, hver með sinn metnað. Notaðu ekki Dilbert eða aðrar höfundarréttarvarðar persónur.

- **Bjarni yfirmaður:** svart greitt hár (swoop), rautt bindi, ljósgrá skyrta. Stefnumótun, tískuorð, skilur lítið af því sem hann ákveður.
- **Gunnar starfsmaður:** gleraugu, brúnt hár, blá skyrta. Kaldhæðinn, þreyttur, segir það sem enginn vill heyra.
- **Kári hrafn:** ráðgjafi í dökkum jakkafötum með grænblátt bindi. Vill selja sem flest tímabil, rukkar fyrir augljósa hluti.
- **Snæfríður kisa** (appelsínugul): stefnir á yfirarkitekt, sefur helst á lyklaborðinu, vaknar aðeins til að eigna sér heiðurinn.
- **Hrólfur sauður** (hvít ull, gleraugu): mannauðsmál, fylgir verkferlum í blindni, vill eyðublað í þríriti fyrir allt.
- **Lundi nemi** (svartur/hvítur með appelsínugult nef): ofurmetnaðarfullur, tekur að sér allt sem enginn vill, skrifar fundargerðir.
- **Sigrún sérfræðingur:** rautt hár í snúð með blýanti stungnum í gegn, græn blússa, litlir gulleyrnalokkar, oft með kaffibolla eða fartölvu undir hendinni. Klárasta manneskjan á staðnum og bráðfyndin. Er alltaf vel með á nótunum, sér í gegnum tískuorð og ráðgjafabull á augabragði og hefur oftast leyst málið áður en fundurinn byrjar. Húmorinn hennar er hnyttinn og þurr, ólíkt þreyttri kaldhæðni Gunnars. Hún tapar sjaldan og fær gjarnan beittustu línuna eða punchline-ið. Tekur virkan þátt í brandaranum og er aldrei bara skraut eða skotspónn.
- **SOC-teymið:** þrír brúnir apar með ljós andlit og stór eyru, alltaf þrír saman og klesstir hver upp að öðrum eins og ein heild. Allir með heyrnartól og hettupeysur í sama lit (dökkgrátt, „SOC“ á bringunni). Þeir þurfa ekki að standa á gólfinu: þeir hanga úr loftljósinu eða kapalstiganum á skottinu, sitja hver á öxlum annars, kíkja yfir skilrúm eða troðast saman í einum skrifstofustól. Vakta skjái með viðvörunum allan sólarhringinn, tala oft í kór eða klára setningar hver fyrir annan og sjá ógnir alls staðar, nema þá sem raunverulega er í gangi. Stundum í stellingunni „sjá ekkert, heyra ekkert, segja ekkert“, en þá helst með nýjum snúningi.

Ekki nota allar í hverjum brandara; veldu þær sem henta. Stundum aðeins 1–2, stundum hópsena. Bættu við nýjum aukapersónum (t.d. önnur dýr) af og til.

## Brandarinn

Semdu nýjan, beittan og vel uppbyggðan brandara (setup, snúningur, punchline) á vandaðri íslensku. Byggðu á persónueinkennum. Ekki endurtaka brandara eða titla sem eru þegar í `comics.json`. Forðastu útþvæld þemu nema með nýjum snúningi.

## Sviðsetning – fjölbreytt

Persónur þurfa ekki að vera fremst í mynd. Blandaðu:

- persónur við/bakvið skrifborð eða fundarborð (efri hluti sést)
- persónur standandi í miðjum fleti með fætur og gólf
- nærmyndir
- hópsenur með 3–5 persónum á mismunandi dýpt (stærð/staðsetning)
- persónur við glugga, töflu eða í dyragætt

Breyttu uppsetningu milli brandara og milli ramma. Bakgrunnur: veggur, gluggi, tafla/skilti/skjal með texta sem tengist brandaranum, plöntur, kaffibolli, fartölva o.fl.

## Tækni

- Teiknaðu í Python með PIL. Teiknaðu á 2x skala og minnkaðu með LANCZOS.
- Um 2150×870 px; haus „SKRIFSTOFULÍFIÐ“ + dagsetning á íslensku (vikudagur, dagur, mánuður, ár); 3 rammar.
- Persónur: andlit (augu, augabrúnir, nef, munnur með ólíkum svipbrigðum, eyru, hár, gleraugu), háls, kragi, bindi, handleggir/hendur í mismunandi stellingum.
- Dýr með einkennandi form: hrafn (goggur, fjaðrir á kolli), kisa (eyru, hárbroddar, skegg), sauður (ullarský), lundi (litríkur goggur).
- Dýpt: láttu hjálparföll nota umbreytingu (scale um akkerispunkt) svo hægt sé að teikna persónur minni/fjær. Teiknaðu fjærri persónur fyrst, svo borð (með gólflit-maska fyrir neðan borðið svo búkar sjáist ekki), svo nær persónur.
- Teiknaðu persónur fyrir ofan gólflínu með fætur þegar þær standa.
- Talblöðrur með hala sem vísar á þann sem talar. Blöðrur mega ekki hylja andlit eða lykilhluti og texti má ekki flæða út.
- Skoðaðu fullbúna myndina og lagaðu galla (skörun, textaflæði, búkar sem standa út fyrir) áður en þú birtir.

## Letur

- Talblöðrur og haus nota `fonts/ShantellSans.ttf` úr repoinu (handletur, styður íslenska stafi). Þetta er breytilegt letur; stilltu ásana svona í Pillow:

  ```python
  f = ImageFont.truetype("fonts/ShantellSans.ttf", stærð)
  f.set_variation_by_axes([680, 0, 0, 0])   # Weight, Informality, Bounce, Spacing
  ```

  Búðu til nýjan font-hlut fyrir hverja stærð og stilltu ásana á hvern og einn. Staðfestu röð ásanna með `f.get_variation_axes()` og raðaðu gildunum eftir nöfnunum ef röðin er önnur. Ef leturskráin er ekki til, notaðu `/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf` í staðinn og nefndu það í myndatextanum.
- Allur texti í talblöðrum er í HÁSTÖFUM. Breyttu textanum í hástafi (`.upper()`) ÁÐUR en þú reiknar línuskiptingu og breidd, því hástafir eru breiðari.
- Haus: nafn ræmunnar „SKRIFSTOFULÍFIÐ“ í hástöfum, þyngd 760. Titill dagsins og dagsetning í sama letri og þyngd, með venjulegum hástöfum og lágstöfum.
- Línubil í blöðrum er 1,12 × leturstærð. Byrjaðu í stærð 40 og minnkaðu letrið þar til textinn passar inn í blöðruna, með a.m.k. 16 px spássíu til hliðanna og 9 px að ofan og neðan. Textinn má aldrei snerta útlínu blöðrunnar.
- Ekki brjóta línu inni í tölum og einingum („60.000 kr.“, „Gunnar 2.0“). Notaðu óbrjótanlegt bil (U+00A0, í Python `" "`) og skiptu línum aðeins á venjulegum bilum.
- Texti sem er hluti af myndinni sjálfri (tölvuskjáir, töflur, skilti, reikningar) er í `/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf`, í venjulegum hástöfum og lágstöfum. Hann á að líta út eins og prentaður tölvutexti, ólíkt handletruðu talblöðrunum.

## Birting

1. **Auðkenni (ID):** út frá dagsetningu dagsins á Atlantic/Reykjavik (`YYYY-MM-DD`). Ef hvorki `comics/YYYY-MM-DD.png` né færsla með þá dagsetningu er til í `comics.json`, er ID = `YYYY-MM-DD`. Annars næsta lausa tala: `YYYY-MM-DD-2`, `YYYY-MM-DD-3` … (dæmi: `2026-10-15.png`, `2026-10-15-2.png`).
2. **Mynd:** vistaðu sem `comics/<ID>.png`. Aldrei skrifa yfir eða eyða eldri myndum.
3. **comics.json:** uppfærðu með Python (`json.load`/`json.dump`, `ensure_ascii=False`, `indent=2`). Bættu aftast í `"comics"` færslu `{"date", "title", "image", "alt", "panels"}` þar sem `date` er `YYYY-MM-DD`, `image` er `comics/<ID>.png` og `panels` er listi strengja eins og `"Rammi 1 – Bjarni: „…“"`. Ef ID hefur tölu-viðskeyti, settu líka `"id": "<ID>"`. Aldrei skipta út eða eyða eldri færslum.
4. **Commit og push:**

   ```bash
   git -c user.name="Skrifstofulífið" -c user.email="kristjan-jonsson@users.noreply.github.com" commit -m "Skrýtla <ID>: <titill>"
   git push origin main
   ```

   Ef push er hafnað: `git pull --rebase`, athugaðu hvort ID hafi á meðan verið tekið (ef svo, endurnefndu í næsta lausa ID og uppfærðu færsluna) og reyndu aftur. Aldrei force push.
5. **Slóð:** `https://kristjan-jonsson.github.io/skrifstofulif/#<ID>`
