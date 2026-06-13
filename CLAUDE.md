# CLAUDE.md  (read this first, then stop)

Knihovna 50 datově řízených SVG diagramů a grafů. Tahle stránka je celý kontext.

## Jak to funguje
- `templates/NN-slug/index.html` = vygenerované výstupy, NEEDITUJ ručně.
- Zdroj pravdy: `build/build.py` (renderery `r_<kind>` + CSS) a `build/content.py`
  (seznam `ITEMS` = data každého diagramu).
- Build: `python3 build/build.py`. Galerie: `python3 build/gallery.py`.

## Nejčastější úkol: upravit jeden diagram
1. Najdi `NN` v tabulce dole (uživatel řekne typ nebo název).
2. Uprav jeho `dict(...)` v `build/content.py` (klíč `data`). Tvar dat odpovídá
   funkci `r_<kind>` v `build/build.py`.
3. Spusť `python3 build/build.py`. Hotovo.
4. Deploy jen na vyžádání: `vercel deploy --prod --yes`.
   Web: https://29diagramtemplates.vercel.app  GitHub: kereptom/diagram-templates

## Přidat nový typ
Napiš `r_<kind>(d)` v `build/build.py` (vrací `svg(body)`, helpery `txt, box,
polar, arc, PAL, _grid`), zaregistruj v `RENDER.update(...)`, přidej položku do
`ITEMS`. Standardní plátno viewBox 0 0 800 460.

## Co NEČÍST: jiné projekty, templates/ ručně.
## Pravidla: ukázková data (dummy); nikdy em dash (U+2014); barvy = proměnné --c-1..5.

## Index (NN -> slug -> typ)

| NN | slug | název | kind |
|----|------|-------|------|
| 01 | `01-process-flow` | Procesní tok | process |
| 02 | `02-timeline` | Časová osa | timeline |
| 03 | `03-funnel` | Prodejní trychtýř | funnel |
| 04 | `04-pyramid` | Pyramida potřeb | pyramid |
| 05 | `05-matrix-2x2` | Matice 2x2 | matrix |
| 06 | `06-org-chart` | Organizační schéma | orgchart |
| 07 | `07-roadmap` | Roadmap | roadmap |
| 08 | `08-gantt` | Ganttův diagram | gantt |
| 09 | `09-kpi-tiles` | KPI dlaždice | kpis |
| 10 | `10-donut` | Prstencový graf | donut |
| 11 | `11-bar-chart` | Sloupcový graf | bars |
| 12 | `12-venn` | Vennův diagram | venn |
| 13 | `13-comparison` | Srovnávací tabulka | compare |
| 14 | `14-journey-map` | Mapa cesty | journey |
| 15 | `15-line-chart` | Spojnicový graf | line |
| 16 | `16-area-chart` | Plošný graf | area |
| 17 | `17-stacked-bars` | Skládané sloupce | stackedbars |
| 18 | `18-grouped-bars` | Seskupené sloupce | groupedbars |
| 19 | `19-horizontal-bars` | Vodorovné sloupce | hbars |
| 20 | `20-pie` | Koláčový graf | pie |
| 21 | `21-radar` | Paprskový graf | radar |
| 22 | `22-scatter` | Bodový graf | scatter |
| 23 | `23-bubble` | Bublinový graf | bubble |
| 24 | `24-heatmap` | Teplotní mapa | heatmap |
| 25 | `25-gauge` | Měřidlo | gauge |
| 26 | `26-progress-rings` | Kruhové ukazatele | rings |
| 27 | `27-waterfall` | Vodopádový graf | waterfall |
| 28 | `28-histogram` | Histogram | histogram |
| 29 | `29-slope-chart` | Sklonový graf | slope |
| 30 | `30-mindmap` | Myšlenková mapa | mindmap |
| 31 | `31-tree` | Stromový diagram | tree |
| 32 | `32-flowchart` | Vývojový diagram | flowchart |
| 33 | `33-swimlane` | Plavecké dráhy | swimlane |
| 34 | `34-fishbone` | Diagram příčin | fishbone |
| 35 | `35-cycle` | Cyklus | cycle |
| 36 | `36-hub-spoke` | Hub a paprsky | hubspoke |
| 37 | `37-kanban` | Kanban | kanban |
| 38 | `38-step-progress` | Kroky postupu | stepprogress |
| 39 | `39-calendar-heatmap` | Kalendářová mapa | calheat |
| 40 | `40-treemap` | Stromová mapa | treemap |
| 41 | `41-pictograph` | Piktograf | pictograph |
| 42 | `42-nine-box` | Devítipolí | ninebox |
| 43 | `43-bullet-chart` | Terčový graf | bullet |
| 44 | `44-diverging-bars` | Rozbíhavé sloupce | diverging |
| 45 | `45-vertical-timeline` | Svislá osa | vtimeline |
| 46 | `46-concentric` | Soustředné kruhy | concentric |
| 47 | `47-ladder` | Žebřík | ladder |
| 48 | `48-segmented-pyramid` | Segmentová pyramida | segpyramid |
| 49 | `49-sankey` | Sankeyův diagram | sankey |
| 50 | `50-multi-donut` | Více prstenců | multidonut |
