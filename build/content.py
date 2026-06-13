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
]
