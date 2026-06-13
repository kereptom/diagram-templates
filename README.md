# Diagramy a grafy

Knihovna **50 datově řízených SVG diagramů**. Každý typ je samostatný HTML soubor
s inline SVG (žádné JS knihovny, žádné závislosti za běhu). Snadno se vloží do
prezentace, dokumentu nebo webu.

> Obsahuje **ukázková (dummy) data**. Před použitím nahraď vlastními.

Živá galerie: `index.html` (kořen webu po nasazení).

## Typy
process (procesní tok), timeline (časová osa), funnel (trychtýř), pyramid
(pyramida), matrix (matice 2x2), orgchart (org. schéma), roadmap, gantt,
kpis (KPI dlaždice), donut (prstenec), bars (sloupce), venn, compare
(srovnávací tabulka), journey (mapa cesty).

## Použití
1. Najdi typ a uprav jeho data v `build/content.py`.
2. Spusť `python3 build/build.py` (přegeneruje `templates/`).
3. Galerii obnovíš `python3 build/gallery.py`.

Barvy jsou CSS proměnné `--c-1` až `--c-5` v každém souboru. Diagram je čisté
inline SVG, takže se dá zkopírovat kamkoli a obarvit přes `currentColor`/proměnné.

## Nasazení
Statické. `vercel deploy --prod`. Nikdy nepoužívej znak dlouhé pomlčky (em dash).
