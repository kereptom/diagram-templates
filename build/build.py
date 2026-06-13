#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Diagram & chart library. Data-driven inline-SVG diagrams, one self-contained
HTML per type, plus a white gallery. No em dashes."""
import os, html, math, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(ROOT, "templates")

# ---- small svg helpers ----------------------------------------------------
def esc(s): return html.escape(str(s), quote=True)
def txt(x, y, s, size=15, anchor="middle", weight="500", fill="var(--ink)", font="var(--ui)"):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{font}" font-size="{size}" font-weight="{weight}" fill="{fill}">{esc(s)}</text>'
def box(x, y, w, h, title, sub="", fill="var(--soft)", stroke="var(--c-1)", r=12, tcol="var(--ink)", tsize=16):
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
    cy = y + h/2 + (tsize*0.34 if not sub else -2)
    out += txt(x+w/2, cy, title, tsize, weight="600", fill=tcol)
    if sub: out += txt(x+w/2, y+h/2+tsize*0.9, sub, tsize-3, weight="400", fill="var(--muted)")
    return out
def polar(cx, cy, r, deg):
    a = math.radians(deg-90); return (cx + r*math.cos(a), cy + r*math.sin(a))
def arc(cx, cy, r, a0, a1):
    x0, y0 = polar(cx, cy, r, a0); x1, y1 = polar(cx, cy, r, a1)
    large = 1 if (a1-a0) % 360 > 180 else 0
    return f"M{cx},{cy} L{x0:.1f},{y0:.1f} A{r},{r} 0 {large} 1 {x1:.1f},{y1:.1f} Z"

def svg(body, vb="0 0 800 460"):
    return f'<svg class="dgm" viewBox="{vb}" xmlns="http://www.w3.org/2000/svg">{body}</svg>'

PAL = ["var(--c-1)", "var(--c-2)", "var(--c-3)", "var(--c-4)", "var(--c-5)"]

# ---- renderers (kind -> fn(data) -> svg) ----------------------------------
def r_process(d):
    st = d["steps"]; n = len(st); gap = 26; w = (760 - gap*(n-1))/n; b = ""
    for i, s in enumerate(st):
        x = 20 + i*(w+gap)
        b += box(x, 180, w, 96, s[0], s[1] if len(s) > 1 else "")
        if i < n-1:
            ax = x+w+4; b += f'<path d="M{ax},228 h{gap-8}" stroke="var(--c-1)" stroke-width="2.5" marker-end="url(#ar)"/>'
    return svg(f'<defs><marker id="ar" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L8,4.5 L0,9 z" fill="var(--c-1)"/></marker></defs>{b}')

def r_timeline(d):
    it = d["items"]; n = len(it); y = 230; x0 = 50; x1 = 750; step = (x1-x0)/(n-1)
    b = f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="var(--rule)" stroke-width="3"/>'
    for i, (date, label) in enumerate(it):
        x = x0 + i*step; up = i % 2 == 0
        b += f'<circle cx="{x}" cy="{y}" r="9" fill="var(--c-1)"/>'
        ly = y-70 if up else y+50
        b += f'<line x1="{x}" y1="{y}" x2="{x}" y2="{ly+(40 if up else -10)}" stroke="var(--rule)" stroke-width="1.5"/>'
        b += txt(x, ly, label, 15, weight="600")
        b += txt(x, ly+(-22 if up else 22), date, 13, weight="500", fill="var(--c-1)")
    return svg(b)

def r_funnel(d):
    st = d["stages"]; n = len(st); top = 40; H = 360; topw = 560; botw = 200; cx = 400
    b = ""
    for i, (label, val) in enumerate(st):
        y0 = top + i*(H/n); y1 = top + (i+1)*(H/n)
        w0 = topw - (topw-botw)*(i/n); w1 = topw - (topw-botw)*((i+1)/n)
        col = PAL[i % len(PAL)]
        pts = f"{cx-w0/2},{y0} {cx+w0/2},{y0} {cx+w1/2},{y1} {cx-w1/2},{y1}"
        b += f'<polygon points="{pts}" fill="{col}" opacity="0.9"/>'
        b += txt(cx, (y0+y1)/2-4, label, 16, weight="600", fill="#fff")
        b += txt(cx, (y0+y1)/2+18, val, 14, weight="500", fill="#fff")
    return svg(b)

def r_pyramid(d):
    ly = d["layers"]; n = len(ly); top = 40; H = 360; baseW = 560; cx = 400
    b = ""
    for i, label in enumerate(ly):
        y0 = top + i*(H/n); y1 = top + (i+1)*(H/n)
        w0 = baseW*(i/n); w1 = baseW*((i+1)/n)
        col = PAL[i % len(PAL)]
        pts = f"{cx-w0/2},{y0} {cx+w0/2},{y0} {cx+w1/2},{y1} {cx-w1/2},{y1}"
        b += f'<polygon points="{pts}" fill="{col}" opacity="0.92"/>'
        b += txt(cx, (y0+y1)/2+5, label, 15, weight="600", fill="#fff")
    return svg(b)

def r_matrix(d):
    ox, oy, S = 130, 50, 340; b = ""
    b += f'<rect x="{ox}" y="{oy}" width="{S}" height="{S}" fill="var(--soft)" stroke="var(--rule)"/>'
    b += f'<line x1="{ox+S/2}" y1="{oy}" x2="{ox+S/2}" y2="{oy+S}" stroke="var(--rule)" stroke-width="1.5"/>'
    b += f'<line x1="{ox}" y1="{oy+S/2}" x2="{ox+S}" y2="{oy+S/2}" stroke="var(--rule)" stroke-width="1.5"/>'
    ax = d.get("axes", {})
    b += txt(ox+S/2, oy-14, ax.get("ytop", "High"), 13, fill="var(--muted)")
    b += txt(ox+S/2, oy+S+24, ax.get("ybot", "Low"), 13, fill="var(--muted)")
    b += txt(ox-14, oy+S/2, ax.get("xlo", "Low"), 13, anchor="end", fill="var(--muted)")
    b += txt(ox+S+14, oy+S/2, ax.get("xhi", "High"), 13, anchor="start", fill="var(--muted)")
    for i, p in enumerate(d["points"]):
        px = ox + p["x"]*S; py = oy + (1-p["y"])*S; col = PAL[i % len(PAL)]
        b += f'<circle cx="{px}" cy="{py}" r="11" fill="{col}"/>'
        b += txt(px, py-18, p["label"], 13, weight="600")
    return svg(b)

def r_orgchart(d):
    root = d["root"]; ch = root.get("children", []); n = len(ch); b = ""
    b += box(300, 30, 200, 60, root["name"], root.get("role", ""))
    cw, cgap = 150, 22; total = n*cw + (n-1)*cgap; x0 = 400 - total/2
    b += f'<line x1="400" y1="90" x2="400" y2="120" stroke="var(--rule)" stroke-width="1.5"/>'
    if n: b += f'<line x1="{x0+cw/2}" y1="120" x2="{x0+total-cw/2}" y2="120" stroke="var(--rule)" stroke-width="1.5"/>'
    for i, c in enumerate(ch):
        cx = x0 + i*(cw+cgap)
        b += f'<line x1="{cx+cw/2}" y1="120" x2="{cx+cw/2}" y2="150" stroke="var(--rule)" stroke-width="1.5"/>'
        b += box(cx, 150, cw, 56, c["name"], c.get("role", ""), fill="var(--paper)")
        for j, g in enumerate(c.get("children", [])[:2]):
            gy = 240 + j*64
            b += f'<line x1="{cx+cw/2}" y1="206" x2="{cx+cw/2}" y2="{gy+28}" stroke="var(--rule)" stroke-width="1.2"/>'
            b += box(cx+18, gy, cw-36, 48, g["name"], g.get("role", ""), fill="var(--soft)", tsize=13)
    return svg(b)

def r_roadmap(d):
    qs = d["quarters"]; lanes = d["lanes"]; ox, oy = 130, 60; cw = (790-ox)/len(qs); rh = 64; b = ""
    for i, q in enumerate(qs):
        b += txt(ox+cw*i+cw/2, oy-12, q, 14, weight="600", fill="var(--c-1)")
        b += f'<line x1="{ox+cw*i}" y1="{oy}" x2="{ox+cw*i}" y2="{oy+rh*len(lanes)}" stroke="var(--rule)" stroke-width="1"/>'
    for li, lane in enumerate(lanes):
        ly = oy + li*rh
        b += txt(ox-12, ly+rh/2+5, lane["name"], 14, anchor="end", weight="600")
        b += f'<line x1="{ox}" y1="{ly}" x2="790" y2="{ly}" stroke="var(--rule)" stroke-width="1"/>'
        for it in lane["items"]:
            x = ox + cw*it["q"] + 8; w = cw*it.get("span", 1) - 16
            b += f'<rect x="{x}" y="{ly+12}" width="{w}" height="{rh-24}" rx="9" fill="{PAL[li%len(PAL)]}" opacity="0.9"/>'
            b += txt(x+w/2, ly+rh/2+5, it["label"], 13, weight="600", fill="#fff")
    b += f'<line x1="{ox}" y1="{oy+rh*len(lanes)}" x2="790" y2="{oy+rh*len(lanes)}" stroke="var(--rule)"/>'
    return svg(b)

def r_gantt(d):
    tasks = d["tasks"]; W = d["weeks"]; ox, oy = 150, 60; cw = (780-ox)/W; rh = 46; b = ""
    for w in range(W+1):
        b += f'<line x1="{ox+cw*w}" y1="{oy}" x2="{ox+cw*w}" y2="{oy+rh*len(tasks)}" stroke="var(--rule)" stroke-width="1"/>'
        if w < W: b += txt(ox+cw*w+cw/2, oy-10, f"T{w+1}", 12, fill="var(--muted)")
    for i, t in enumerate(tasks):
        y = oy + i*rh
        b += txt(ox-12, y+rh/2+5, t["name"], 13, anchor="end", weight="600")
        x = ox + cw*t["start"]; w = cw*t["len"]
        b += f'<rect x="{x+4}" y="{y+10}" width="{w-8}" height="{rh-20}" rx="7" fill="{PAL[i%len(PAL)]}"/>'
    b += f'<line x1="{ox}" y1="{oy+rh*len(tasks)}" x2="{ox+cw*W}" y2="{oy+rh*len(tasks)}" stroke="var(--rule)"/>'
    return svg(b)

def r_kpis(d):
    it = d["items"]; n = len(it); gap = 24; w = (760-gap*(n-1))/n; b = ""
    for i, k in enumerate(it):
        x = 20 + i*(w+gap)
        b += f'<rect x="{x}" y="120" width="{w}" height="220" rx="16" fill="var(--soft)" stroke="var(--rule)"/>'
        b += txt(x+w/2, 215, k["num"], 44, weight="800", fill=PAL[i % len(PAL)])
        b += txt(x+w/2, 255, k["label"], 14, fill="var(--muted)")
        tr = k.get("trend", ""); tc = "var(--c-1)"
        if tr: b += txt(x+w/2, 295, tr, 14, weight="600", fill=tc)
    return svg(b)

def r_donut(d):
    sl = d["slices"]; tot = sum(s["value"] for s in sl); cx, cy, r = 270, 230, 150; a = 0; b = ""
    for i, s in enumerate(sl):
        ang = 360*s["value"]/tot
        b += f'<path d="{arc(cx,cy,r,a,a+ang)}" fill="{PAL[i%len(PAL)]}"/>'
        a += ang
    b += f'<circle cx="{cx}" cy="{cy}" r="82" fill="var(--paper)"/>'
    b += txt(cx, cy-2, d.get("center", ""), 30, weight="800")
    b += txt(cx, cy+26, d.get("centersub", ""), 13, fill="var(--muted)")
    ly = 110
    for i, s in enumerate(sl):
        b += f'<rect x="540" y="{ly-12}" width="16" height="16" rx="4" fill="{PAL[i%len(PAL)]}"/>'
        b += txt(566, ly+1, f'{s["label"]}', 14, anchor="start", weight="500")
        b += txt(780, ly+1, f'{round(100*s["value"]/tot)}%', 14, anchor="end", weight="600", fill="var(--muted)")
        ly += 40
    return svg(b)

def r_bars(d):
    data = d["data"]; n = len(data); ox, oy, H, BW = 70, 60, 320, 60
    mx = max(v["value"] for v in data); gap = (700-ox - n*BW)/(n-1) if n > 1 else 0; b = ""
    for g in range(5):
        yy = oy + H*g/4; b += f'<line x1="{ox}" y1="{yy}" x2="760" y2="{yy}" stroke="var(--rule)" stroke-width="1"/>'
    for i, v in enumerate(data):
        x = ox + i*(BW+gap); h = H*v["value"]/mx; y = oy+H-h
        b += f'<rect x="{x}" y="{y}" width="{BW}" height="{h}" rx="8" fill="{PAL[i%len(PAL)]}"/>'
        b += txt(x+BW/2, y-10, str(v["value"]), 14, weight="700")
        b += txt(x+BW/2, oy+H+24, v["label"], 13, fill="var(--muted)")
    return svg(b)

def r_venn(d):
    s = d["sets"]; b = ""
    cfg = [(310, 230, "var(--c-1)"), (490, 230, "var(--c-2)"), (400, 320, "var(--c-3)")][:len(s)]
    for (cx, cy, col), name in zip(cfg, s):
        b += f'<circle cx="{cx}" cy="{cy}" r="120" fill="{col}" opacity="0.32"/>'
    labels = d.get("labels", [])
    for (cx, cy, col), name in zip(cfg, s):
        ly = cy-150 if cy < 300 else cy+150
        b += txt(cx, ly, name, 16, weight="700", fill=col)
    for lab in labels:
        b += txt(lab["x"], lab["y"], lab["text"], 13, weight="600")
    return svg(b)

def r_compare(d):
    cols = d["plans"]; rows = d["rows"]; ox, oy = 40, 70; lw = 280; cw = (760-lw)/len(cols); b = ""
    for j, c in enumerate(cols):
        cx = ox+lw+cw*j; feat = c.get("featured")
        if feat: b += f'<rect x="{cx}" y="{oy-50}" width="{cw}" height="{50+len(rows)*44+10}" rx="12" fill="var(--soft)" stroke="var(--c-1)" stroke-width="2"/>'
        b += txt(cx+cw/2, oy-18, c["name"], 17, weight="700", fill="var(--c-1)" if feat else "var(--ink)")
    for i, row in enumerate(rows):
        y = oy + i*44 + 24
        b += txt(ox, y, row["label"], 15, anchor="start", weight="500")
        b += f'<line x1="{ox}" y1="{y+14}" x2="760" y2="{y+14}" stroke="var(--rule)" stroke-width="1"/>'
        for j, val in enumerate(row["vals"]):
            cx = ox+lw+cw*j+cw/2
            if val is True: b += f'<path d="M{cx-7},{y-4} l5,6 l9,-12" stroke="var(--c-1)" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
            elif val is False: b += f'<path d="M{cx-6},{y-7} l12,12 M{cx+6},{y-7} l-12,12" stroke="var(--muted)" stroke-width="2.2" stroke-linecap="round"/>'
            else: b += txt(cx, y, str(val), 14, weight="600")
    return svg(b, "0 0 800 480")

def r_journey(d):
    st = d["stages"]; n = len(st); ox, oy = 40, 70; cw = (760-ox)/n; b = ""
    pts = []
    for i, s in enumerate(st):
        cx = ox + cw*i + cw/2; em = s.get("emotion", 0.5); ey = 360 - em*200; pts.append((cx, ey))
        b += f'<rect x="{ox+cw*i+8}" y="{oy}" width="{cw-16}" height="60" rx="10" fill="var(--soft)" stroke="var(--rule)"/>'
        b += txt(cx, oy+36, s["name"], 14, weight="600")
    path = "M" + " L".join(f"{x:.0f},{y:.0f}" for x, y in pts)
    b += f'<path d="{path}" fill="none" stroke="var(--c-1)" stroke-width="3"/>'
    for x, y in pts: b += f'<circle cx="{x}" cy="{y}" r="7" fill="var(--c-1)"/>'
    b += txt(40, 300, "Pocit", 13, anchor="start", fill="var(--muted)")
    return svg(b)

RENDER = dict(process=r_process, timeline=r_timeline, funnel=r_funnel, pyramid=r_pyramid,
    matrix=r_matrix, orgchart=r_orgchart, roadmap=r_roadmap, gantt=r_gantt, kpis=r_kpis,
    donut=r_donut, bars=r_bars, venn=r_venn, compare=r_compare, journey=r_journey)

# ---- items (each = one diagram type with sample data) ---------------------
from content import ITEMS  # defined separately for readability

PAGE = """<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='{fav}'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400..800&family=JetBrains+Mono:wght@400..600&display=swap" rel="stylesheet">
<style>
:root{{--c-1:{c1};--c-2:{c2};--c-3:{c3};--c-4:{c4};--c-5:{c5};--ink:#1c2230;--muted:#6b7280;--paper:#fff;--soft:{soft};--rule:#e4e7ee;--ui:"Inter Tight",system-ui,sans-serif;--mono:"JetBrains Mono",monospace}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#f4f5f8;color:var(--ink);font-family:var(--ui);-webkit-font-smoothing:antialiased;min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:40px 20px}}
.frame{{background:var(--paper);border:1px solid var(--rule);border-radius:22px;box-shadow:0 20px 60px -30px rgba(0,0,0,.3);max-width:920px;width:100%;padding:34px 38px 28px}}
.kick{{font-family:var(--mono);font-size:12.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--c-1)}}
h1{{font-size:30px;font-weight:800;letter-spacing:-.02em;margin:6px 0 4px}}
.cap{{color:var(--muted);font-size:15px;margin-bottom:18px}}
.dgm{{width:100%;height:auto;display:block}}
.note{{font-family:var(--mono);font-size:12px;color:var(--muted);margin-top:18px;border-top:1px solid var(--rule);padding-top:14px}}
.back{{margin-top:24px;font-family:var(--mono);font-size:13px;color:#6b7280;text-decoration:none}}
.back:hover{{color:var(--c-1)}}
</style></head>
<body>
<div class="frame">
  <div class="kick">// {kind} diagram</div>
  <h1>{name}</h1>
  <p class="cap">{cap}</p>
  {svg}
  <div class="note">// data-driven SVG &middot; ukázková data (dummy) &middot; uprav data v build/content.py</div>
</div>
<a class="back" href="../../index.html">&larr; zpět na galerii</a>
</body></html>"""

def build_one(it):
    body = RENDER[it["kind"]](it["data"])
    p = PAGE.format(lang=it.get("lang", "cs"), title=esc(it["name"]+" diagram"), fav=it["accent"].replace("#", "%23"),
        c1=it["accent"], c2=it.get("c2", "#5b6cf0"), c3=it.get("c3", "#0e9e8e"), c4=it.get("c4", "#f0883a"), c5=it.get("c5", "#e0468a"),
        soft=it.get("soft", "#f5f7fb"), kind=it["kind"], name=esc(it["name"]), cap=esc(it.get("cap", "")), svg=body)
    d = os.path.join(TPL, it["slug"]); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(p)

if __name__ == "__main__":
    for it in ITEMS:
        build_one(it)
    print("built", len(ITEMS), "diagrams")
