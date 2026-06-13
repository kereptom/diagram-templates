# -*- coding: utf-8 -*-
# Sample (dummy) data for each diagram type. Edit freely; em dash forbidden.
ITEMS = [
 dict(slug="01-process-flow", name="Procesní tok", kind="process", accent="#5b6cf0", cap="Pět kroků od poptávky ke spuštění.",
   data=dict(steps=[["Poptávka","z webu"],["Konzultace","30 minut"],["Návrh","do 3 dnů"],["Schválení","klient"],["Spuštění","do týdne"]])),

 dict(slug="02-timeline", name="Časová osa", kind="timeline", accent="#0e9e8e", cap="Milníky firmy v čase.",
   data=dict(items=[["2019","Založení"],["2021","1000 klientů"],["2023","Expanze do EU"],["2025","Nový produkt"],["2026","Série A"]])),

 dict(slug="03-funnel", name="Prodejní trychtýř", kind="funnel", accent="#f0883a", c2="#ef6a4a", c3="#e0468a", c4="#a23bd6", cap="Konverze od návštěvy k zákazníkovi.",
   data=dict(stages=[["Návštěvníci","48 200"],["Registrace","12 400"],["Vyzkoušeli","3 800"],["Zákazníci","920"]])),

 dict(slug="04-pyramid", name="Pyramida potřeb", kind="pyramid", accent="#e0468a", c2="#c43bd6", c3="#7b5bf0", c4="#3a72bf", c5="#0e9e8e", cap="Vrstvy od základu k vrcholu.",
   data=dict(layers=["Seberealizace","Uznání","Sociální vazby","Bezpečí","Fyziologické"])),

 dict(slug="05-matrix-2x2", name="Matice 2x2", kind="matrix", accent="#5b6cf0", c2="#0e9e8e", c3="#f0883a", c4="#e0468a", cap="Priorita podle dopadu a náročnosti.",
   data=dict(axes=dict(ytop="Vysoký dopad", ybot="Nízký dopad", xlo="Snadné", xhi="Náročné"),
     points=[{"x":0.22,"y":0.82,"label":"Quick win"},{"x":0.78,"y":0.8,"label":"Velký projekt"},{"x":0.25,"y":0.25,"label":"Drobnost"},{"x":0.8,"y":0.22,"label":"Zvážit"}])),

 dict(slug="06-org-chart", name="Organizační schéma", kind="orgchart", accent="#3a72bf", cap="Týmová struktura na třech úrovních.",
   data=dict(root={"name":"Ředitel","role":"CEO","children":[
     {"name":"Produkt","role":"CPO","children":[{"name":"Design"},{"name":"Výzkum"}]},
     {"name":"Vývoj","role":"CTO","children":[{"name":"Backend"},{"name":"Frontend"}]},
     {"name":"Obchod","role":"CSO","children":[{"name":"Sales"}]},
     {"name":"Provoz","role":"COO","children":[{"name":"Podpora"}]}]})),

 dict(slug="07-roadmap", name="Roadmap", kind="roadmap", accent="#0e9e8e", c2="#5b6cf0", c3="#f0883a", cap="Plán na čtyři kvartály ve třech proudech.",
   data=dict(quarters=["Q1","Q2","Q3","Q4"], lanes=[
     {"name":"Produkt","items":[{"q":0,"span":2,"label":"Onboarding"},{"q":2,"span":2,"label":"Mobilní app"}]},
     {"name":"Růst","items":[{"q":1,"span":1,"label":"SEO"},{"q":2,"span":2,"label":"Partnerství"}]},
     {"name":"Platforma","items":[{"q":0,"span":1,"label":"API"},{"q":3,"span":1,"label":"SSO"}]}])),

 dict(slug="08-gantt", name="Ganttův diagram", kind="gantt", accent="#7b5bf0", c2="#0e9e8e", c3="#f0883a", c4="#e0468a", c5="#3a72bf", cap="Úkoly v čase, osm týdnů.",
   data=dict(weeks=8, tasks=[
     {"name":"Analýza","start":0,"len":2},{"name":"Design","start":1,"len":2},
     {"name":"Vývoj","start":3,"len":3},{"name":"Testy","start":5,"len":2},{"name":"Nasazení","start":7,"len":1}])),

 dict(slug="09-kpi-tiles", name="KPI dlaždice", kind="kpis", accent="#0e9e8e", c2="#5b6cf0", c3="#f0883a", c4="#e0468a", cap="Klíčová čísla na jeden pohled.",
   data=dict(items=[{"num":"+24%","label":"meziroční růst","trend":"nahoru"},{"num":"4,8","label":"hodnocení","trend":"stabilní"},
     {"num":"1,2k","label":"nových klientů","trend":"+18%"},{"num":"-9%","label":"odchody","trend":"zlepšení"}])),

 dict(slug="10-donut", name="Prstencový graf", kind="donut", accent="#5b6cf0", c2="#0e9e8e", c3="#f0883a", c4="#e0468a", c5="#a23bd6", cap="Rozdělení rozpočtu podle oblastí.",
   data=dict(center="2,4M", centersub="celkem Kč", slices=[
     {"label":"Vývoj","value":40},{"label":"Marketing","value":25},{"label":"Provoz","value":18},{"label":"Podpora","value":11},{"label":"Ostatní","value":6}])),

 dict(slug="11-bar-chart", name="Sloupcový graf", kind="bars", accent="#f0883a", c2="#ef6a4a", c3="#e0468a", c4="#a23bd6", c5="#5b6cf0", cap="Tržby po měsících (tis. Kč).",
   data=dict(data=[{"label":"Led","value":120},{"label":"Úno","value":150},{"label":"Bře","value":135},{"label":"Dub","value":190},{"label":"Kvě","value":210},{"label":"Čer","value":248}])),

 dict(slug="12-venn", name="Vennův diagram", kind="venn", accent="#5b6cf0", c2="#0e9e8e", c3="#f0883a", cap="Průnik tří oblastí.",
   data=dict(sets=["Design","Technologie","Byznys"], labels=[{"x":400,"y":250,"text":"Produkt"}])),

 dict(slug="13-comparison", name="Srovnávací tabulka", kind="compare", accent="#5b6cf0", cap="Funkce napříč tarify.",
   data=dict(plans=[{"name":"Start"},{"name":"Tým","featured":True},{"name":"Firma"}], rows=[
     {"label":"Uživatelé","vals":["5","25","neomezeně"]},{"label":"Reporty","vals":[True,True,True]},
     {"label":"Automatizace","vals":[False,True,True]},{"label":"SSO a audit","vals":[False,False,True]},
     {"label":"Podpora","vals":["e-mail","přednostní","dedikovaná"]}])),

 dict(slug="14-journey-map", name="Mapa cesty", kind="journey", accent="#0e9e8e", cap="Zkušenost zákazníka po fázích.",
   data=dict(stages=[{"name":"Objevení","emotion":0.5},{"name":"Registrace","emotion":0.35},{"name":"První úspěch","emotion":0.8},
     {"name":"Každodenní","emotion":0.7},{"name":"Doporučení","emotion":0.9}])),

 dict(slug="15-line-chart", name="Spojnicový graf", kind="line", accent="#2f6bff", cap="Trend v čase.", data=dict(data=[["Led",120],["Úno",150],["Bře",135],["Dub",190],["Kvě",210],["Čer",248]])),
 dict(slug="16-area-chart", name="Plošný graf", kind="area", accent="#0e9e8e", cap="Objem pod křivkou.", data=dict(data=[["Po",30],["Út",45],["St",38],["Čt",60],["Pá",72],["So",55],["Ne",40]])),
 dict(slug="17-stacked-bars", name="Skládané sloupce", kind="stackedbars", accent="#6d4aff", c2="#0e9e8e", c3="#f0883a", cap="Podíl segmentů v čase.", data=dict(cats=["Q1","Q2","Q3","Q4"], series=[{"name":"Produkt A","vals":[20,30,25,35]},{"name":"Produkt B","vals":[15,18,22,20]},{"name":"Produkt C","vals":[10,12,14,18]}])),
 dict(slug="18-grouped-bars", name="Seskupené sloupce", kind="groupedbars", accent="#2f6bff", c2="#e0468a", cap="Porovnání dvou let.", data=dict(cats=["Led","Úno","Bře","Dub"], series=[{"name":"2025","vals":[120,140,130,160]},{"name":"2026","vals":[150,170,190,210]}])),
 dict(slug="19-horizontal-bars", name="Vodorovné sloupce", kind="hbars", accent="#0e9e8e", c2="#2f6bff", c3="#f0883a", c4="#e0468a", c5="#a23bd6", cap="Žebříček podle hodnoty.", data=dict(data=[["Praha",248],["Brno",180],["Ostrava",120],["Plzeň",95],["Liberec",60]])),
 dict(slug="20-pie", name="Koláčový graf", kind="pie", accent="#f0883a", c2="#2f6bff", c3="#0e9e8e", cap="Rozdělení zařízení.", data=dict(slices=[{"label":"Mobil","value":52},{"label":"Desktop","value":33},{"label":"Tablet","value":15}])),
 dict(slug="21-radar", name="Paprskový graf", kind="radar", accent="#6d4aff", cap="Profil v pěti osách.", data=dict(axes=["Rychlost","Cena","Kvalita","Podpora","Design"], values=[0.8,0.6,0.9,0.7,0.85])),
 dict(slug="22-scatter", name="Bodový graf", kind="scatter", accent="#2f6bff", c2="#0e9e8e", c3="#f0883a", cap="Vztah dvou veličin.", data=dict(xlabel="Cena", ylabel="Kvalita", points=[{"x":0.2,"y":0.3},{"x":0.4,"y":0.5},{"x":0.55,"y":0.6},{"x":0.7,"y":0.78},{"x":0.85,"y":0.82},{"x":0.3,"y":0.65}])),
 dict(slug="23-bubble", name="Bublinový graf", kind="bubble", accent="#e0468a", c2="#2f6bff", c3="#0e9e8e", c4="#f0883a", cap="Tři rozměry v jednom.", data=dict(points=[{"x":0.25,"y":0.6,"r":0.5,"label":"A"},{"x":0.55,"y":0.4,"r":0.8,"label":"B"},{"x":0.75,"y":0.75,"r":0.3,"label":"C"},{"x":0.4,"y":0.2,"r":0.6,"label":"D"}])),
 dict(slug="24-heatmap", name="Teplotní mapa", kind="heatmap", accent="#2f6bff", cap="Intenzita v mřížce.", data=dict(rows=["Po","Út","St","Čt"], cols=["8","10","12","14","16","18"], cells=[[0.2,0.5,0.8,0.6,0.9,0.4],[0.3,0.7,0.9,0.5,0.8,0.6],[0.1,0.4,0.6,0.9,0.7,0.3],[0.5,0.6,0.7,0.8,0.5,0.2]])),
 dict(slug="25-gauge", name="Měřidlo", kind="gauge", accent="#0e9e8e", cap="Jedna hodnota na škále.", data=dict(value=0.72, center="72 %", label="využití kapacity")),
 dict(slug="26-progress-rings", name="Kruhové ukazatele", kind="rings", accent="#2f6bff", c2="#0e9e8e", c3="#f0883a", cap="Více cílů najednou.", data=dict(items=[{"label":"Cíl tržeb","pct":0.78},{"label":"Noví klienti","pct":0.62},{"label":"Spokojenost","pct":0.9}])),
 dict(slug="27-waterfall", name="Vodopádový graf", kind="waterfall", accent="#2f6bff", cap="Přírůstky a úbytky.", data=dict(steps=[{"label":"Počátek","delta":80},{"label":"Q1","delta":30},{"label":"Q2","delta":-20},{"label":"Q3","delta":40},{"label":"Q4","delta":-15}])),
 dict(slug="28-histogram", name="Histogram", kind="histogram", accent="#6d4aff", cap="Četnost v intervalech.", data=dict(xlabel="Rozdělení skóre", bins=[2,5,9,14,18,15,10,6,3,1])),
 dict(slug="29-slope-chart", name="Sklonový graf", kind="slope", accent="#0e9e8e", c2="#2f6bff", c3="#e0468a", cap="Změna mezi dvěma body.", data=dict(left="2025", right="2026", items=[{"label":"Tržby","l":120,"r":180},{"label":"Náklady","l":90,"r":85},{"label":"Zisk","l":30,"r":95}])),
 dict(slug="30-mindmap", name="Myšlenková mapa", kind="mindmap", accent="#6d4aff", c2="#0e9e8e", c3="#f0883a", c4="#e0468a", c5="#2f6bff", cap="Centrum a větve.", data=dict(center="Projekt", branches=["Cíle","Tým","Rozpočet","Termíny","Rizika","Výstupy"])),
 dict(slug="31-tree", name="Stromový diagram", kind="tree", accent="#2f6bff", cap="Hierarchie shora dolů.", data=dict(root={"name":"Vedení","children":[{"name":"Produkt","children":[{"name":"Design"},{"name":"Výzkum"}]},{"name":"Vývoj","children":[{"name":"Backend"},{"name":"Frontend"}]},{"name":"Obchod","children":[{"name":"Sales"}]}]})),
 dict(slug="32-flowchart", name="Vývojový diagram", kind="flowchart", accent="#0e9e8e", cap="Kroky s rozhodováním.", data=dict(steps=[{"label":"Start"},{"label":"Vstup","sub":"data"},{"label":"Validní?","decision":True},{"label":"Uložit"},{"label":"Konec"}])),
 dict(slug="33-swimlane", name="Plavecké dráhy", kind="swimlane", accent="#2f6bff", c2="#0e9e8e", c3="#f0883a", cap="Proces napříč rolemi.", data=dict(steps=["Poptávka","Nabídka","Výroba","Schválení","Předání"], lanes=[{"name":"Zákazník","cells":[{"s":0,"label":"Poptávka"},{"s":3,"label":"Schválení"}]},{"name":"Obchod","cells":[{"s":1,"label":"Nabídka"}]},{"name":"Realizace","cells":[{"s":2,"label":"Výroba"},{"s":4,"label":"Předání"}]}])),
 dict(slug="34-fishbone", name="Diagram příčin", kind="fishbone", accent="#2f6bff", c2="#0e9e8e", c3="#f0883a", c4="#e0468a", cap="Ishikawa: příčiny a následek.", data=dict(effect="Zpoždění", causes=[{"name":"Lidé","items":["nábor","školení"]},{"name":"Proces","items":["fronty"]},{"name":"Nástroje","items":["výpadky"]},{"name":"Materiál","items":["dodávky"]}])),
 dict(slug="35-cycle", name="Cyklus", kind="cycle", accent="#6d4aff", c2="#0e9e8e", c3="#f0883a", c4="#2f6bff", cap="Opakující se proces (PDCA).", data=dict(stages=["Plánuj","Udělej","Zkontroluj","Zlepši"])),
 dict(slug="36-hub-spoke", name="Hub a paprsky", kind="hubspoke", accent="#2f6bff", c2="#0e9e8e", c3="#f0883a", c4="#e0468a", c5="#a23bd6", cap="Centrum a okolní uzly.", data=dict(hub="Data", spokes=["Sales","Marketing","Produkt","Podpora","Finance"])),
 dict(slug="37-kanban", name="Kanban", kind="kanban", accent="#0e9e8e", cap="Úkoly ve třech sloupcích.", data=dict(columns=[{"name":"K udělání","cards":["Návrh API","Testy","Dokumentace"]},{"name":"Probíhá","cards":["Onboarding","Mobilní app"]},{"name":"Hotovo","cards":["Login","Dashboard","Export"]}])),
 dict(slug="38-step-progress", name="Kroky postupu", kind="stepprogress", accent="#2f6bff", cap="Kde se právě nacházíte.", data=dict(current=3, steps=["Objednávka","Platba","Zpracování","Odeslání","Doručeno"])),
 dict(slug="39-calendar-heatmap", name="Kalendářová mapa", kind="calheat", accent="#2c8a5a", cap="Aktivita po dnech.", data=dict(weeks=16, label="aktivita za 16 týdnů", cells=[[0.2,0.6,0.1,0.8,0.4,0.0,0.3],[0.5,0.9,0.3,0.6,0.7,0.1,0.2],[0.1,0.4,0.8,0.5,0.9,0.2,0.0],[0.7,0.3,0.6,0.9,0.4,0.5,0.1]])),
 dict(slug="40-treemap", name="Stromová mapa", kind="treemap", accent="#2f6bff", c2="#0e9e8e", c3="#f0883a", c4="#e0468a", cap="Plocha podle podílu.", data=dict(items=[{"label":"Vývoj","value":40},{"label":"Marketing","value":25},{"label":"Provoz","value":20},{"label":"Ostatní","value":15}])),
 dict(slug="41-pictograph", name="Piktograf", kind="pictograph", accent="#0e9e8e", cap="Podíl pomocí ikon.", data=dict(total=10, filled=7, label="7 z 10 zákazníků doporučuje")),
 dict(slug="42-nine-box", name="Devítipolí", kind="ninebox", accent="#6d4aff", cap="Matice 3x3 (talent grid).", data=dict(highlight=[2,2], xaxis="Výkon", yaxis="Potenciál", labels=[{"x":460,"y":114,"t":"Top","on":True},{"x":220,"y":230,"t":"Rozvíjet"},{"x":340,"y":392,"t":"Sledovat"}])),
 dict(slug="43-bullet-chart", name="Terčový graf", kind="bullet", accent="#2f6bff", cap="Hodnota proti cíli.", data=dict(rows=[{"label":"Tržby","value":78,"target":90,"max":100},{"label":"Marže","value":62,"target":60,"max":100},{"label":"NPS","value":48,"target":50,"max":100}])),
 dict(slug="44-diverging-bars", name="Rozbíhavé sloupce", kind="diverging", accent="#0e9e8e", c2="#e0468a", cap="Souhlas vs nesouhlas.", data=dict(rows=[{"label":"Souhlas","value":58},{"label":"Spíše ano","value":24},{"label":"Spíše ne","value":-12},{"label":"Nesouhlas","value":-6}])),
 dict(slug="45-vertical-timeline", name="Svislá osa", kind="vtimeline", accent="#2f6bff", cap="Milníky pod sebou.", data=dict(items=[["2019","Založení firmy"],["2021","Expanze do EU"],["2023","Nový produkt"],["2025","Investice série A"]])),
 dict(slug="46-concentric", name="Soustředné kruhy", kind="concentric", accent="#6d4aff", c2="#7b5bf0", c3="#9a7bf5", c4="#b89cf8", cap="Vrstvy od jádra ven.", data=dict(layers=["Vize","Strategie","Cíle","Akce"])),
 dict(slug="47-ladder", name="Žebřík", kind="ladder", accent="#0e9e8e", c2="#2bbdab", c3="#56b257", c4="#65bd62", c5="#f0883a", cap="Postupný růst.", data=dict(steps=["Povědomí","Zájem","Zvažování","Nákup","Loajalita"])),
 dict(slug="48-segmented-pyramid", name="Segmentová pyramida", kind="segpyramid", accent="#e0468a", c2="#c43bd6", c3="#7b5bf0", c4="#2f6bff", cap="Vrstvy s hodnotami.", data=dict(layers=[["VIP","3 %"],["Stálí","18 %"],["Příležitostní","34 %"],["Noví","45 %"]])),
 dict(slug="49-sankey", name="Sankeyův diagram", kind="sankey", accent="#2f6bff", c3="#0e9e8e", cap="Toky mezi uzly.", data=dict(left=[["Zdroj A",20],["Zdroj B",14],["Zdroj C",10]], right=[["Cíl X",24],["Cíl Y",20]], flows=[{"from":"Zdroj A","to":"Cíl X","v":12},{"from":"Zdroj A","to":"Cíl Y","v":8},{"from":"Zdroj B","to":"Cíl X","v":8},{"from":"Zdroj B","to":"Cíl Y","v":6},{"from":"Zdroj C","to":"Cíl Y","v":6},{"from":"Zdroj C","to":"Cíl X","v":4}])),
 dict(slug="50-multi-donut", name="Více prstenců", kind="multidonut", accent="#2f6bff", c2="#0e9e8e", c3="#f0883a", cap="Sada ukazatelů.", data=dict(items=[{"label":"Web","pct":0.82},{"label":"Mobil","pct":0.64},{"label":"E-mail","pct":0.91}])),
]
