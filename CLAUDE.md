# CLAUDE.md  (read this first, then stop)

Knihovna 14 datově řízených SVG diagramů. Tahle stránka je celý kontext.

## Jak to funguje
- `templates/NN-slug/index.html` = vygenerované výstupy, NEEDITUJ ručně.
- Zdroj pravdy: `build/build.py` (renderery diagramů `r_<kind>` + CSS) a
  `build/content.py` (seznam `ITEMS` = data každého diagramu).
- Build: `python3 build/build.py`. Galerie: `python3 build/gallery.py`.

## Nejčastější úkol: upravit jeden diagram
1. Najdi `NN` v tabulce dole (uživatel řekne typ nebo název).
2. Uprav jeho `dict(...)` v `build/content.py` (hlavně klíč `data`). Tvar dat
   odpovídá funkci `r_<kind>` v `build/build.py`.
3. Spusť `python3 build/build.py`. Hotovo.
4. Deploy jen na vyžádání: `vercel deploy --prod --yes` z kořene.
   Web: https://29diagramtemplates.vercel.app  GitHub: kereptom/diagram-templates

## Co NEČÍST
Nechoď do jiných projektů, needituj `templates/` ručně, README čti jen cíleně.

## Pravidla
- Ukázková (dummy) data. Drž styl, pokud uživatel nechce reálná.
- NIKDY dlouhou pomlčku (em dash, U+2014). Místo ní `:` `,` `.` nebo závorku.
- Barvy = CSS proměnné `--c-1` až `--c-5` v každém souboru.

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
