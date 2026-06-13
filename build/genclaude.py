# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import ITEMS
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = "\n".join(f"| {i['slug'].split('-')[0]} | `{i['slug']}` | {i['name']} | {i['kind']} |" for i in ITEMS)
doc = """# CLAUDE.md  (read this first, then stop)

Knihovna {N} datově řízených SVG diagramů a grafů. Tahle stránka je celý kontext.

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
{ROWS}
""".replace("{N}", str(len(ITEMS))).replace("{ROWS}", rows)
assert chr(0x2014) not in doc
open(os.path.join(ROOT, "CLAUDE.md"), "w", encoding="utf-8").write(doc)
print("CLAUDE.md regenerated with", len(ITEMS), "rows")
