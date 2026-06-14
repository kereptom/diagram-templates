# Diagramy a grafy

Knihovna **100 datově řízených SVG diagramů**. Každý typ je samostatný HTML soubor
s inline SVG (žádné JS knihovny, žádné závislosti za běhu). Snadno se vloží do
prezentace, dokumentu nebo webu.

> Obsahuje **ukázková (dummy) data**. Před použitím nahraď vlastními.

Živá galerie: `index.html` (kořen webu po nasazení).

## Typy (100, plný seznam v `CLAUDE.md`)
- **Grafy:** sloupcové, vodorovné, skládané, seskupené, spojnicové, plošné,
  skládané plošné, schodové, hladká křivka, koláč, prstenec, více prstenců,
  paprskové (radar), bodové, bublinové, bublinová mřížka, histogram, vodopád,
  Pareto, kombinovaný, lízátkový, tečkový, činkový, rozsahový, krabicový,
  svíčkový, růžicový, radiální, Marimekko, sklonový, srovnání ploch, malé násobky.
- **Procesy a toky:** procesní tok, vývojový diagram, plavecké dráhy, cyklus,
  kruhový proces, hodnotový řetězec, Stage-Gate, uživatelský tok, stavový
  automat, Sankey, rozhodovací strom.
- **Hierarchie a vztahy:** org. schéma, vodorovná hierarchie, strom, WBS,
  myšlenková mapa, mapa webu, ER diagram, matice závislostí, obloukový,
  tětivový, sluneční záře, ledový, kruhové balení, hub a paprsky, fishbone.
- **Časové osy:** časová osa, svislá, zakřivená, stuhová, milníkové vlajky,
  roadmap, gantt, kroky postupu.
- **Matice a rámce:** matice 2x2, devítipolí, BCG, bublinový kvadrant, SWOT,
  srovnávací tabulka, porovnání proti sobě, afinitní diagram, pyramida,
  segmentová pyramida, žebřík, soustředné kruhy, Venn, turnajový pavouk.
- **Ukazatele:** KPI dlaždice, metrické karty, statistické dlaždice, měřidlo,
  prstencové měřidlo, kruhové ukazatele, teploměr, pruhy postupu, terčový,
  piktograf, trychtýř (svislý i vodorovný), kalendářová a teplotní mapa,
  stromová mapa.

## Použití
1. Najdi typ a uprav jeho data v `build/content.py`.
2. Spusť `python3 build/build.py` (přegeneruje `templates/`).
3. Galerii obnovíš `python3 build/gallery.py`.

Barvy jsou CSS proměnné `--c-1` až `--c-5` v každém souboru. Diagram je čisté
inline SVG, takže se dá zkopírovat kamkoli a obarvit přes `currentColor`/proměnné.

## Nasazení
Statické. `vercel deploy --prod`. Nikdy nepoužívej znak dlouhé pomlčky (em dash).
