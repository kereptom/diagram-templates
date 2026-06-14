# CLAUDE.md  (read this first, then stop)

Knihovna 100 datově řízených SVG diagramů a grafů. Tahle stránka je celý kontext.

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
| 51 | `51-stacked-area` | Skládaný plošný graf | stackarea |
| 52 | `52-lollipop` | Lízátkový graf | lollipop |
| 53 | `53-dumbbell` | Činkový graf | dumbbell |
| 54 | `54-spline` | Hladká křivka | spline |
| 55 | `55-rose-chart` | Růžicový graf | rose |
| 56 | `56-ring-gauge` | Prstencové měřidlo | ringgauge |
| 57 | `57-boxplot` | Krabicový graf | boxplot |
| 58 | `58-candlestick` | Svíčkový graf | candle |
| 59 | `59-pct-stacked` | Procentně skládané | pctstacked |
| 60 | `60-grouped-hbars` | Seskupené vodorovné | ghbars |
| 61 | `61-range-bars` | Rozsahové sloupce | rangebars |
| 62 | `62-marimekko` | Marimekko | marimekko |
| 63 | `63-pareto` | Paretův graf | pareto |
| 64 | `64-combo` | Kombinovaný graf | combo |
| 65 | `65-radial-bars` | Radiální sloupce | radialbars |
| 66 | `66-small-multiples` | Malé násobky | smallmult |
| 67 | `67-dot-plot` | Tečkový graf | dotplot |
| 68 | `68-step-line` | Schodová linka | stepline |
| 69 | `69-bubble-grid` | Bublinová mřížka | bubblegrid |
| 70 | `70-area-compare` | Srovnání ploch | areacompare |
| 71 | `71-sitemap` | Mapa webu | sitemap |
| 72 | `72-wbs` | WBS rozpad | wbs |
| 73 | `73-decision-tree` | Rozhodovací strom | dectree |
| 74 | `74-state-machine` | Stavový automat | statemachine |
| 75 | `75-er-diagram` | ER diagram | er |
| 76 | `76-user-flow` | Uživatelský tok | userflow |
| 77 | `77-affinity` | Afinitní diagram | affinity |
| 78 | `78-dependency-matrix` | Matice závislostí | depmatrix |
| 79 | `79-arc-diagram` | Obloukový diagram | arcdiagram |
| 80 | `80-chord` | Tětivový diagram | chord |
| 81 | `81-sunburst` | Sluneční záře | sunburst |
| 82 | `82-icicle` | Ledový diagram | icicle |
| 83 | `83-circle-packing` | Kruhové balení | packing |
| 84 | `84-bracket` | Turnajový pavouk | bracket |
| 85 | `85-process-circular` | Kruhový proces | proccircular |
| 86 | `86-hierarchy-h` | Vodorovná hierarchie | hierh |
| 87 | `87-swot` | SWOT analýza | swot |
| 88 | `88-bcg-matrix` | BCG matice | bcg |
| 89 | `89-value-chain` | Hodnotový řetězec | valuechain |
| 90 | `90-stage-gate` | Stage-Gate | stagegate |
| 91 | `91-milestone-flags` | Milníkové vlajky | mileflags |
| 92 | `92-progress-bars` | Pruhy postupu | progbars |
| 93 | `93-thermometer` | Teploměr | thermometer |
| 94 | `94-curved-timeline` | Zakřivená osa | curvedtl |
| 95 | `95-icon-stats` | Statistické dlaždice | iconstats |
| 96 | `96-versus` | Porovnání proti sobě | versus |
| 97 | `97-quad-bubble` | Bublinový kvadrant | quadbubble |
| 98 | `98-funnel-horizontal` | Vodorovný trychtýř | funnelh |
| 99 | `99-metric-cards` | Metrické karty | metriccards |
| 100 | `100-ribbon-timeline` | Stuhová osa | ribbontl |
