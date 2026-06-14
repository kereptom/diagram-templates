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

# ====== extra renderers (diagrams 15..50) ==================================
def _grid(ox, oy, W, H, steps=4):
    return "".join(f'<line x1="{ox}" y1="{oy+H*g/steps:.0f}" x2="{ox+W}" y2="{oy+H*g/steps:.0f}" stroke="var(--rule)" stroke-width="1"/>' for g in range(steps+1))

def r_line(d):
    data = d["data"]; ox, oy, W, H = 64, 46, 690, 320; n = len(data)
    vs = [v for _, v in data]; mx = max(vs); mn = min(min(vs), 0)
    pts = [(ox+W*i/(n-1), oy+H-H*(v-mn)/((mx-mn) or 1)) for i, (_, v) in enumerate(data)]
    b = _grid(ox, oy, W, H) + f'<polyline points="{" ".join(f"{x:.0f},{y:.0f}" for x,y in pts)}" fill="none" stroke="var(--c-1)" stroke-width="3.5"/>'
    for (x, y), (lab, v) in zip(pts, data):
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="6" fill="var(--c-1)"/>' + txt(x, oy+H+24, lab, 12, fill="var(--muted)")
    return svg(b)

def r_area(d):
    data = d["data"]; ox, oy, W, H = 64, 46, 690, 320; n = len(data)
    vs = [v for _, v in data]; mx = max(vs)
    pts = [(ox+W*i/(n-1), oy+H-H*v/mx) for i, (_, v) in enumerate(data)]
    poly = f"{ox},{oy+H} " + " ".join(f"{x:.0f},{y:.0f}" for x, y in pts) + f" {ox+W},{oy+H}"
    b = _grid(ox, oy, W, H) + f'<polygon points="{poly}" fill="var(--c-1)" opacity="0.18"/>'
    b += f'<polyline points="{" ".join(f"{x:.0f},{y:.0f}" for x,y in pts)}" fill="none" stroke="var(--c-1)" stroke-width="3.5"/>'
    for (x, y), (lab, v) in zip(pts, data): b += txt(x, oy+H+24, lab, 12, fill="var(--muted)")
    return svg(b)

def r_stackedbars(d):
    cats = d["cats"]; ser = d["series"]; ox, oy, W, H = 70, 46, 680, 320; n = len(cats)
    tot = [sum(s["vals"][i] for s in ser) for i in range(n)]; mx = max(tot)
    bw = W/n*0.6; b = _grid(ox, oy, W, H)
    for i in range(n):
        x = ox + W*i/n + (W/n-bw)/2; yy = oy+H
        for si, s in enumerate(ser):
            h = H*s["vals"][i]/mx; yy -= h
            b += f'<rect x="{x:.0f}" y="{yy:.0f}" width="{bw:.0f}" height="{h:.0f}" fill="{PAL[si%len(PAL)]}"/>'
        b += txt(x+bw/2, oy+H+24, cats[i], 12, fill="var(--muted)")
    for si, s in enumerate(ser):
        b += f'<rect x="{ox+si*120}" y="20" width="14" height="14" rx="3" fill="{PAL[si%len(PAL)]}"/>' + txt(ox+si*120+20, 32, s["name"], 12, anchor="start")
    return svg(b)

def r_groupedbars(d):
    cats = d["cats"]; ser = d["series"]; ox, oy, W, H = 70, 46, 680, 320; n = len(cats); m = len(ser)
    mx = max(max(s["vals"]) for s in ser); gw = W/n*0.7; bw = gw/m; b = _grid(ox, oy, W, H)
    for i in range(n):
        gx = ox + W*i/n + (W/n-gw)/2
        for si, s in enumerate(ser):
            h = H*s["vals"][i]/mx; x = gx+si*bw
            b += f'<rect x="{x:.0f}" y="{oy+H-h:.0f}" width="{bw-3:.0f}" height="{h:.0f}" rx="3" fill="{PAL[si%len(PAL)]}"/>'
        b += txt(gx+gw/2, oy+H+24, cats[i], 12, fill="var(--muted)")
    return svg(b)

def r_hbars(d):
    data = d["data"]; ox, oy, W, H = 150, 46, 600, 330; n = len(data); mx = max(v for _, v in data); rh = H/n
    b = ""
    for i, (lab, v) in enumerate(data):
        y = oy+i*rh+rh*0.2; w = W*v/mx
        b += f'<rect x="{ox}" y="{y:.0f}" width="{w:.0f}" height="{rh*0.6:.0f}" rx="5" fill="{PAL[i%len(PAL)]}"/>'
        b += txt(ox-12, y+rh*0.42, lab, 13, anchor="end") + txt(ox+w+10, y+rh*0.42, str(v), 13, anchor="start", weight="700")
    return svg(b)

def r_pie(d):
    sl = d["slices"]; tot = sum(s["value"] for s in sl); cx, cy, r = 250, 230, 160; a = 0; b = ""
    for i, s in enumerate(sl):
        ang = 360*s["value"]/tot; b += f'<path d="{arc(cx,cy,r,a,a+ang)}" fill="{PAL[i%len(PAL)]}"/>'; a += ang
    ly = 110
    for i, s in enumerate(sl):
        b += f'<rect x="540" y="{ly-12}" width="16" height="16" rx="4" fill="{PAL[i%len(PAL)]}"/>' + txt(566, ly+1, s["label"], 14, anchor="start") + txt(780, ly+1, f'{round(100*s["value"]/tot)}%', 14, anchor="end", weight="600", fill="var(--muted)")
        ly += 40
    return svg(b)

def r_radar(d):
    ax = d["axes"]; vals = d["values"]; cx, cy, R = 400, 240, 170; n = len(ax); b = ""
    for ring in (0.33, 0.66, 1.0):
        pts = " ".join(f"{polar(cx,cy,R*ring,360*i/n)[0]:.0f},{polar(cx,cy,R*ring,360*i/n)[1]:.0f}" for i in range(n))
        b += f'<polygon points="{pts}" fill="none" stroke="var(--rule)" stroke-width="1"/>'
    for i in range(n):
        x, y = polar(cx, cy, R, 360*i/n); b += f'<line x1="{cx}" y1="{cy}" x2="{x:.0f}" y2="{y:.0f}" stroke="var(--rule)"/>'
        lx, ly = polar(cx, cy, R+24, 360*i/n); b += txt(lx, ly, ax[i], 12, fill="var(--muted)")
    dp = " ".join(f"{polar(cx,cy,R*vals[i],360*i/n)[0]:.0f},{polar(cx,cy,R*vals[i],360*i/n)[1]:.0f}" for i in range(n))
    b += f'<polygon points="{dp}" fill="var(--c-1)" opacity="0.3" stroke="var(--c-1)" stroke-width="2.5"/>'
    return svg(b)

def r_scatter(d):
    pts = d["points"]; ox, oy, S = 90, 40, 360; b = f'<rect x="{ox}" y="{oy}" width="{S}" height="{S}" fill="var(--soft)"/>' + _grid(ox, oy, S, S)
    b += "".join(f'<line x1="{ox}" y1="{oy+S*g/4:.0f}" x2="{ox}" y2="{oy+S*g/4:.0f}"/>' for g in range(0))
    b += f'<line x1="{ox}" y1="{oy}" x2="{ox}" y2="{oy+S}" stroke="var(--rule)"/>'
    for i, p in enumerate(pts):
        x = ox+p["x"]*S; y = oy+(1-p["y"])*S; b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="8" fill="{PAL[i%len(PAL)]}" opacity="0.85"/>'
    b += txt(ox+S/2, oy+S+30, d.get("xlabel", ""), 13, fill="var(--muted)") + txt(ox-16, oy+S/2, d.get("ylabel", ""), 13, anchor="end", fill="var(--muted)")
    return svg(b)

def r_bubble(d):
    pts = d["points"]; ox, oy, S = 110, 40, 360; b = f'<rect x="{ox}" y="{oy}" width="{S}" height="{S}" fill="var(--soft)"/>' + _grid(ox, oy, S, S)
    for i, p in enumerate(pts):
        x = ox+p["x"]*S; y = oy+(1-p["y"])*S; r = 14+p["r"]*36
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="{PAL[i%len(PAL)]}" opacity="0.55"/>' + txt(x, y+4, p.get("label", ""), 12, weight="600")
    return svg(b)

def r_heatmap(d):
    rows = d["rows"]; cols = d["cols"]; cells = d["cells"]; ox, oy = 120, 60; cw = 560/len(cols); ch = 56
    b = ""
    for ci, c in enumerate(cols): b += txt(ox+cw*ci+cw/2, oy-12, c, 12, fill="var(--muted)")
    for ri, r in enumerate(rows):
        b += txt(ox-12, oy+ch*ri+ch/2+4, r, 13, anchor="end")
        for ci in range(len(cols)):
            v = cells[ri][ci]; b += f'<rect x="{ox+cw*ci:.0f}" y="{oy+ch*ri:.0f}" width="{cw-3:.0f}" height="{ch-3:.0f}" rx="5" fill="var(--c-1)" opacity="{0.12+0.82*v:.2f}"/>'
            b += txt(ox+cw*ci+cw/2, oy+ch*ri+ch/2+4, str(int(v*100)), 12, weight="600", fill="#fff" if v > 0.5 else "var(--ink)")
    return svg(b)

def r_gauge(d):
    import math as _m
    cx, cy, R = 400, 300, 185; v = d["value"]
    def gp(t):
        th = _m.pi*(1-t); return (cx+R*_m.cos(th), cy-R*_m.sin(th))
    l = gp(0); r = gp(1); pv = gp(v)
    b = f'<path d="M{l[0]:.0f},{l[1]:.0f} A{R},{R} 0 0 1 {r[0]:.0f},{r[1]:.0f}" fill="none" stroke="var(--rule)" stroke-width="28" stroke-linecap="round"/>'
    b += f'<path d="M{l[0]:.0f},{l[1]:.0f} A{R},{R} 0 0 1 {pv[0]:.0f},{pv[1]:.0f}" fill="none" stroke="var(--c-1)" stroke-width="28" stroke-linecap="round"/>'
    b += txt(cx, cy-26, d.get("center", f"{int(v*100)}%"), 50, weight="800", fill="var(--c-1)") + txt(cx, cy+6, d.get("label", ""), 16, fill="var(--muted)")
    return svg(b)

def r_rings(d):
    its = d["items"]; cx, cy = 250, 230; b = ""
    for i, it in enumerate(its):
        R = 160-i*44; circ = 2*3.14159*R; off = circ*(1-it["pct"])
        b += f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="var(--rule)" stroke-width="20"/>'
        b += f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{PAL[i%len(PAL)]}" stroke-width="20" stroke-linecap="round" stroke-dasharray="{circ:.0f}" stroke-dashoffset="{off:.0f}" transform="rotate(-90 {cx} {cy})"/>'
    ly = 150
    for i, it in enumerate(its):
        b += f'<rect x="510" y="{ly-12}" width="16" height="16" rx="4" fill="{PAL[i%len(PAL)]}"/>' + txt(536, ly+1, it["label"], 14, anchor="start") + txt(770, ly+1, f'{int(it["pct"]*100)}%', 14, anchor="end", weight="700", fill="var(--muted)")
        ly += 42
    return svg(b)

def r_waterfall(d):
    st = d["steps"]; ox, oy, W, H = 70, 50, 680, 320; n = len(st)
    cum = []; run = 0
    for s in st: cum.append((run, run+s["delta"])); run += s["delta"]
    mx = max(max(a, b2) for a, b2 in cum); bw = W/n*0.6; b = ""
    for i, (s, (a, b2)) in enumerate(zip(st, cum)):
        x = ox+W*i/n+(W/n-bw)/2; y0 = oy+H-H*max(a, b2)/mx; h = H*abs(b2-a)/mx
        col = PAL[0] if s["delta"] >= 0 else PAL[3]
        b += f'<rect x="{x:.0f}" y="{y0:.0f}" width="{bw:.0f}" height="{max(h,2):.0f}" rx="3" fill="{col}"/>'
        b += txt(x+bw/2, oy+H+24, s["label"], 11, fill="var(--muted)") + txt(x+bw/2, y0-8, f'{"+" if s["delta"]>=0 else ""}{s["delta"]}', 12, weight="700")
    return svg(b)

def r_histogram(d):
    bins = d["bins"]; ox, oy, W, H = 70, 50, 680, 320; n = len(bins); mx = max(bins); bw = W/n
    b = _grid(ox, oy, W, H)
    for i, v in enumerate(bins):
        h = H*v/mx; b += f'<rect x="{ox+bw*i+1:.0f}" y="{oy+H-h:.0f}" width="{bw-2:.0f}" height="{h:.0f}" fill="var(--c-1)" opacity="0.85"/>'
    b += txt(ox, oy+H+24, d.get("xlabel", ""), 12, anchor="start", fill="var(--muted)")
    return svg(b)

def r_slope(d):
    its = d["items"]; lx, rx, oy, H = 220, 580, 60, 330; b = ""
    mx = max(max(i["l"], i["r"]) for i in its)
    b += txt(lx, 36, d.get("left", "Před"), 14, weight="700") + txt(rx, 36, d.get("right", "Po"), 14, weight="700")
    for i, it in enumerate(its):
        yl = oy+H-H*it["l"]/mx; yr = oy+H-H*it["r"]/mx; col = PAL[i % len(PAL)]
        b += f'<line x1="{lx}" y1="{yl:.0f}" x2="{rx}" y2="{yr:.0f}" stroke="{col}" stroke-width="3"/>'
        b += f'<circle cx="{lx}" cy="{yl:.0f}" r="6" fill="{col}"/><circle cx="{rx}" cy="{yr:.0f}" r="6" fill="{col}"/>'
        b += txt(lx-14, yl+4, it["label"], 12, anchor="end") + txt(rx+14, yr+4, str(it["r"]), 12, anchor="start", weight="600")
    return svg(b)

def r_mindmap(d):
    cx, cy = 400, 230; br = d["branches"]; n = len(br); b = box(cx-90, cy-34, 180, 68, d["center"], "", fill="var(--c-1)", stroke="var(--c-1)", tcol="#fff")
    import math as _m
    for i, br1 in enumerate(br):
        ang = 360*i/n; x, y = polar(cx, cy, 178, ang)
        b += f'<path d="M{cx},{cy} Q{(cx+x)/2:.0f},{(cy+y)/2-20:.0f} {x:.0f},{y:.0f}" fill="none" stroke="{PAL[i%len(PAL)]}" stroke-width="2.5"/>'
        b += f'<rect x="{x-66:.0f}" y="{y-22:.0f}" width="132" height="44" rx="10" fill="var(--soft)" stroke="{PAL[i%len(PAL)]}" stroke-width="1.5"/>' + txt(x, y+4, br1, 13, weight="600")
    return svg(b)

def r_tree(d):
    root = d["root"]; ch = root.get("children", []); n = len(ch); b = box(330, 26, 140, 50, root["name"], "", fill="var(--c-1)", tcol="#fff", stroke="var(--c-1)")
    cw = 150; total = n*cw; x0 = 400-total/2
    b += f'<line x1="400" y1="76" x2="400" y2="100"/>'
    for i, c in enumerate(ch):
        cx = x0+i*cw+cw/2; b += f'<line x1="400" y1="100" x2="{cx:.0f}" y2="100"/><line x1="{cx:.0f}" y1="100" x2="{cx:.0f}" y2="130"/>'
        b += box(cx-62, 130, 124, 46, c["name"], "", fill="var(--paper)")
        for j, g in enumerate(c.get("children", [])[:3]):
            gy = 210+j*54; b += f'<line x1="{cx:.0f}" y1="176" x2="{cx:.0f}" y2="{gy+24:.0f}"/>' + box(cx-54, gy, 108, 40, g["name"], "", fill="var(--soft)", tsize=12)
    return svg(b.replace("<line ", '<line stroke="var(--rule)" stroke-width="1.4" '))

def r_flowchart(d):
    st = d["steps"]; x = 26; y = 200; bw = 126; b = ""
    for i, s in enumerate(st):
        if s.get("decision"):
            b += f'<polygon points="{x+63},{y-44} {x+138},{y} {x+63},{y+44} {x-12},{y}" fill="var(--soft)" stroke="var(--c-1)" stroke-width="1.5"/>' + txt(x+63, y+4, s["label"], 11, weight="600"); w = 150
        else:
            b += box(x, y-34, bw, 68, s["label"], s.get("sub", ""), tsize=14); w = bw
        if i < len(st)-1:
            b += f'<path d="M{x+w},{y} h18" stroke="var(--c-1)" stroke-width="2.5" marker-end="url(#fa)"/>'; x += w+18
    return svg(f'<defs><marker id="fa" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L8,4.5 L0,9 z" fill="var(--c-1)"/></marker></defs>{b}')

def r_swimlane(d):
    lanes = d["lanes"]; steps = d["steps"]; ox, oy = 140, 50; cw = (770-ox)/len(steps); rh = 90; b = ""
    for ci, s in enumerate(steps): b += txt(ox+cw*ci+cw/2, oy-12, s, 13, weight="600", fill="var(--c-1)")
    for li, lane in enumerate(lanes):
        ly = oy+li*rh; b += f'<rect x="{ox}" y="{ly}" width="{cw*len(steps)}" height="{rh}" fill="{"var(--soft)" if li%2 else "var(--paper)"}" stroke="var(--rule)"/>' + txt(ox-12, ly+rh/2, lane["name"], 13, anchor="end", weight="600")
        for it in lane.get("cells", []):
            x = ox+cw*it["s"]+10; b += box(x, ly+18, cw-20, rh-36, it["label"], "", fill="var(--paper)", tsize=12, stroke=PAL[li % len(PAL)])
    return svg(b)

def r_fishbone(d):
    cx, cy = 720, 230; b = f'<line x1="60" y1="{cy}" x2="{cx}" y2="{cy}" stroke="var(--ink)" stroke-width="3"/>'
    b += f'<polygon points="{cx},{cy-14} {cx+30},{cy} {cx},{cy+14}" fill="var(--c-1)"/>' + box(cx+34, cy-26, 0, 0, "", "")
    b += txt(cx+40, cy+4, d["effect"], 14, anchor="start", weight="700", fill="var(--c-1)")
    cats = d["causes"]; n = len(cats)
    for i, c in enumerate(cats):
        up = i % 2 == 0; bx = 140+(i//2)*180; by = cy+(-90 if up else 90)
        b += f'<line x1="{bx}" y1="{by}" x2="{bx+70}" y2="{cy}" stroke="{PAL[i%len(PAL)]}" stroke-width="2.5"/>'
        b += txt(bx, by+(-8 if up else 18), c["name"], 13, weight="700", fill=PAL[i % len(PAL)])
        for j, cause in enumerate(c.get("items", [])[:2]):
            b += txt(bx+10, by+(-26 if up else 36)+(j*16*(1 if not up else -1)), cause, 11, anchor="start", fill="var(--muted)")
    return svg(b)

def r_cycle(d):
    st = d["stages"]; cx, cy, R = 400, 230, 150; n = len(st); b = ""
    for i in range(n):
        a0 = 360*i/n; a1 = 360*(i+0.82)/n
        b += f'<path d="{arc(cx,cy,R+18,a0,a1).replace(f"M{cx},{cy} L","M").split("Z")[0]}" fill="none" stroke="{PAL[i%len(PAL)]}" stroke-width="6"/>'
        x, y = polar(cx, cy, R, a0+18)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="36" fill="{PAL[i%len(PAL)]}"/>' + txt(x, y+5, str(i+1), 22, weight="800", fill="#fff")
        lx, ly = polar(cx, cy, R+72, a0+18); b += txt(lx, ly, st[i], 13, weight="600")
    return svg(b)

def r_hubspoke(d):
    cx, cy = 400, 230; sp = d["spokes"]; n = len(sp); b = ""
    for i in range(n):
        x, y = polar(cx, cy, 180, 360*i/n); b += f'<line x1="{cx}" y1="{cy}" x2="{x:.0f}" y2="{y:.0f}" stroke="var(--rule)" stroke-width="2"/>'
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="40" fill="{PAL[i%len(PAL)]}" opacity="0.9"/>' + txt(x, y+5, sp[i], 12, weight="600", fill="#fff")
    b += f'<circle cx="{cx}" cy="{cy}" r="52" fill="var(--c-1)"/>' + txt(cx, cy+6, d["hub"], 15, weight="800", fill="#fff")
    return svg(b)

def r_kanban(d):
    cols = d["columns"]; ox = 40; cw = (760-ox)/len(cols)-12; b = ""
    for ci, c in enumerate(cols):
        x = ox+ci*(cw+18); b += f'<rect x="{x:.0f}" y="40" width="{cw:.0f}" height="380" rx="12" fill="var(--soft)"/>' + txt(x+cw/2, 66, c["name"], 14, weight="700", fill="var(--c-1)")
        for j, card in enumerate(c["cards"][:4]):
            cy = 88+j*72; b += f'<rect x="{x+12:.0f}" y="{cy}" width="{cw-24:.0f}" height="58" rx="9" fill="var(--paper)" stroke="var(--rule)"/>' + txt(x+24, cy+34, card, 12, anchor="start")
    return svg(b)

def r_stepprogress(d):
    st = d["steps"]; cur = d.get("current", 1); ox = 70; n = len(st); gap = (660)/(n-1); y = 200; b = f'<line x1="{ox}" y1="{y}" x2="{ox+660}" y2="{y}" stroke="var(--rule)" stroke-width="4"/>'
    b += f'<line x1="{ox}" y1="{y}" x2="{ox+gap*(cur-1):.0f}" y2="{y}" stroke="var(--c-1)" stroke-width="4"/>'
    for i, s in enumerate(st):
        x = ox+gap*i; done = i < cur; col = "var(--c-1)" if done else "var(--rule)"
        b += f'<circle cx="{x:.0f}" cy="{y}" r="22" fill="{col}"/>' + txt(x, y+6, str(i+1), 18, weight="800", fill="#fff")
        b += txt(x, y+54, s, 13, weight="600" if done else "400", fill="var(--ink)" if done else "var(--muted)")
    return svg(b)

def r_calheat(d):
    weeks = d.get("weeks", 16); cells = d["cells"]; ox, oy, sz = 90, 70, 22; b = ""
    days = ["Po", "St", "Pá"]
    for di, dd in enumerate(days): b += txt(ox-12, oy+di*2*sz+sz, dd, 11, anchor="end", fill="var(--muted)")
    for w in range(weeks):
        for day in range(7):
            v = cells[w % len(cells)][day]
            b += f'<rect x="{ox+w*sz:.0f}" y="{oy+day*sz:.0f}" width="{sz-3}" height="{sz-3}" rx="4" fill="var(--c-1)" opacity="{0.1+0.85*v:.2f}"/>'
    b += txt(ox, oy+7*sz+24, d.get("label", ""), 12, anchor="start", fill="var(--muted)")
    return svg(b)

def r_treemap(d):
    its = d["items"]; tot = sum(i["value"] for i in its); ox, oy, W, H = 50, 50, 700, 360; b = ""; x = ox
    for i, it in enumerate(its[:4]):
        w = W*it["value"]/tot; b += f'<rect x="{x:.0f}" y="{oy}" width="{w-4:.0f}" height="{H}" rx="6" fill="{PAL[i%len(PAL)]}" opacity="0.9"/>'
        b += txt(x+w/2, oy+H/2-6, it["label"], 15, weight="700", fill="#fff") + txt(x+w/2, oy+H/2+18, str(it["value"]), 13, fill="#fff")
        x += w
    return svg(b)

def r_pictograph(d):
    total = d.get("total", 10); filled = d["filled"]; ox, oy = 80, 110; cols = 5; b = ""
    for i in range(total):
        r, c = divmod(i, cols); x = ox+c*120; y = oy+r*120; col = "var(--c-1)" if i < filled else "var(--rule)"
        b += f'<circle cx="{x+30}" cy="{y+24}" r="20" fill="{col}"/><path d="M{x+8},{y+78} a22,26 0 0 1 44,0 z" fill="{col}"/>'
    b += txt(ox, oy-30, d.get("label", ""), 16, anchor="start", weight="600")
    return svg(b)

def r_ninebox(d):
    ox, oy, S = 160, 50, 360; cell = S/3; b = ""
    hl = d.get("highlight", [1, 1])
    for r in range(3):
        for c in range(3):
            fill = "var(--c-1)" if [c, 2-r] == hl else ("var(--soft)" if (c+r) % 2 else "var(--paper)")
            b += f'<rect x="{ox+c*cell:.0f}" y="{oy+r*cell:.0f}" width="{cell-2:.0f}" height="{cell-2:.0f}" fill="{fill}" stroke="var(--rule)"/>'
    labels = d.get("labels", [])
    for lab in labels: b += txt(lab["x"], lab["y"], lab["t"], 12, weight="600", fill="#fff" if lab.get("on") else "var(--ink)")
    b += txt(ox+S/2, oy+S+24, d.get("xaxis", ""), 12, fill="var(--muted)") + txt(ox-16, oy+S/2, d.get("yaxis", ""), 12, anchor="end", fill="var(--muted)")
    return svg(b)

def r_bullet(d):
    rows = d["rows"]; ox, oy, W = 180, 70, 540; rh = 70; b = ""
    for i, r in enumerate(rows):
        y = oy+i*rh; mx = r["max"]
        b += txt(ox-14, y+14, r["label"], 13, anchor="end", weight="600")
        b += f'<rect x="{ox}" y="{y}" width="{W}" height="28" rx="5" fill="var(--soft)"/>'
        b += f'<rect x="{ox}" y="{y+6}" width="{W*r["value"]/mx:.0f}" height="16" rx="4" fill="var(--c-1)"/>'
        tx = ox+W*r["target"]/mx; b += f'<rect x="{tx-2:.0f}" y="{y-4}" width="4" height="36" fill="var(--ink)"/>'
    return svg(b)

def r_diverging(d):
    rows = d["rows"]; cx = 400; ox = 60; W = 320; oy = 60; rh = 60; b = f'<line x1="{cx}" y1="{oy-10}" x2="{cx}" y2="{oy+rh*len(rows)}" stroke="var(--rule)"/>'
    mx = max(abs(r["value"]) for r in rows)
    for i, r in enumerate(rows):
        y = oy+i*rh; v = r["value"]; w = W*abs(v)/mx; col = PAL[0] if v >= 0 else PAL[3]
        x = cx if v >= 0 else cx-w
        b += f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="36" rx="5" fill="{col}"/>' + txt(cx+(8 if v < 0 else -8)*(1 if v < 0 else 1), y-6, r["label"], 12, anchor="middle", fill="var(--muted)")
        b += txt(x+(w+12 if v >= 0 else -12), y+24, f'{"+" if v>=0 else ""}{v}', 12, anchor="start" if v >= 0 else "end", weight="700")
    return svg(b)

def r_vtimeline(d):
    its = d["items"]; x = 200; oy = 50; gap = 340/(len(its)); b = f'<line x1="{x}" y1="{oy}" x2="{x}" y2="{oy+gap*len(its)}" stroke="var(--rule)" stroke-width="3"/>'
    for i, (date, label) in enumerate(its):
        y = oy+gap*i+gap/2; b += f'<circle cx="{x}" cy="{y:.0f}" r="9" fill="var(--c-1)"/>'
        b += txt(x-22, y+5, date, 13, anchor="end", weight="600", fill="var(--c-1)") + txt(x+22, y+5, label, 14, anchor="start")
    return svg(b)

def r_concentric(d):
    cx, cy = 270, 230; ls = d["layers"]; b = ""
    for i, lab in enumerate(ls):
        R = 60+(len(ls)-1-i)*48; b += f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{PAL[i%len(PAL)]}" opacity="{0.85-i*0.12}"/>'
    for i, lab in enumerate(ls):
        R = 60+(len(ls)-1-i)*48; b += txt(cx, cy-R+22, lab, 13, weight="600", fill="#fff")
    return svg(b)

def r_ladder(d):
    st = d["steps"]; n = len(st); ox, oy, W, H = 70, 60, 680, 340; sw = W/n; sh = H/n; b = ""
    for i, s in enumerate(st):
        x = ox+sw*i; y = oy+H-sh*(i+1); h = sh*(i+1)
        b += f'<rect x="{x:.0f}" y="{y:.0f}" width="{sw-8:.0f}" height="{h:.0f}" rx="6" fill="{PAL[i%len(PAL)]}" opacity="0.9"/>'
        b += txt(x+sw/2, y-10, s, 13, weight="600")
    return svg(b)

def r_segpyramid(d):
    ly = d["layers"]; n = len(ly); top = 40; H = 360; baseW = 600; cx = 400; b = ""
    for i, (label, val) in enumerate(ly):
        y0 = top+i*(H/n); y1 = top+(i+1)*(H/n); w0 = baseW*(i/n); w1 = baseW*((i+1)/n); col = PAL[i % len(PAL)]
        b += f'<polygon points="{cx-w0/2},{y0} {cx+w0/2},{y0} {cx+w1/2},{y1} {cx-w1/2},{y1}" fill="{col}" opacity="0.92"/>'
        b += txt(cx, (y0+y1)/2-2, label, 14, weight="600", fill="#fff") + txt(cx, (y0+y1)/2+18, val, 12, fill="#fff")
    return svg(b)

def r_sankey(d):
    L = d["left"]; R = d["right"]; flows = d["flows"]; lx, rx = 120, 680; oy = 60; b = ""
    lh = {}; rh = {}; ly = oy; ry = oy
    for nm, v in L: lh[nm] = (ly, v); b += f'<rect x="{lx-14}" y="{ly}" width="14" height="{v*4}" fill="var(--c-1)"/>' + txt(lx-22, ly+v*2, nm, 12, anchor="end"); ly += v*4+14
    for nm, v in R: rh[nm] = (ry, v); b += f'<rect x="{rx}" y="{ry}" width="14" height="{v*4}" fill="var(--c-3)"/>' + txt(rx+22, ry+v*2, nm, 12, anchor="start"); ry += v*4+14
    loff = {k: 0 for k in lh}; roff = {k: 0 for k in rh}
    for f in flows:
        a, bnode, val = f["from"], f["to"], f["v"]; y0 = lh[a][0]+loff[a]; y1 = rh[bnode][0]+roff[bnode]; th = val*4
        b += f'<path d="M{lx},{y0:.0f} C{(lx+rx)/2},{y0:.0f} {(lx+rx)/2},{y1:.0f} {rx},{y1:.0f}" fill="none" stroke="{PAL[0]}" stroke-width="{th:.0f}" opacity="0.32"/>'
        loff[a] += th; roff[bnode] += th
    return svg(b)

def r_multidonut(d):
    its = d["items"]; n = len(its); gap = 760/n; b = ""
    for i, it in enumerate(its):
        cx = 60+gap*i+gap/2-30; cy = 200; R = 80; pct = it["pct"]; circ = 2*3.14159*R
        b += f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="var(--rule)" stroke-width="18"/>'
        b += f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{PAL[i%len(PAL)]}" stroke-width="18" stroke-linecap="round" stroke-dasharray="{circ:.0f}" stroke-dashoffset="{circ*(1-pct):.0f}" transform="rotate(-90 {cx} {cy})"/>'
        b += txt(cx, cy+6, f'{int(pct*100)}%', 26, weight="800") + txt(cx, cy+R+34, it["label"], 13, weight="600")
    return svg(b)

RENDER.update(line=r_line, area=r_area, stackedbars=r_stackedbars, groupedbars=r_groupedbars,
    hbars=r_hbars, pie=r_pie, radar=r_radar, scatter=r_scatter, bubble=r_bubble, heatmap=r_heatmap,
    gauge=r_gauge, rings=r_rings, waterfall=r_waterfall, histogram=r_histogram, slope=r_slope,
    mindmap=r_mindmap, tree=r_tree, flowchart=r_flowchart, swimlane=r_swimlane, fishbone=r_fishbone,
    cycle=r_cycle, hubspoke=r_hubspoke, kanban=r_kanban, stepprogress=r_stepprogress, calheat=r_calheat,
    treemap=r_treemap, pictograph=r_pictograph, ninebox=r_ninebox, bullet=r_bullet, diverging=r_diverging,
    vtimeline=r_vtimeline, concentric=r_concentric, ladder=r_ladder, segpyramid=r_segpyramid,
    sankey=r_sankey, multidonut=r_multidonut)

# ====== extra renderers (diagrams 51..100) =================================
_PI = 3.14159265

def r_stackarea(d):
    cats = d["cats"]; ser = d["series"]; ox, oy, W, H = 64, 46, 690, 320; n = len(cats)
    tot = [sum(s["vals"][i] for s in ser) for i in range(n)]; mx = max(tot); b = _grid(ox, oy, W, H)
    cum = [0]*n; xs = [ox+W*i/(n-1) for i in range(n)]
    for si, s in enumerate(ser):
        low = [oy+H-H*cum[i]/mx for i in range(n)]
        for i in range(n): cum[i] += s["vals"][i]
        up = [oy+H-H*cum[i]/mx for i in range(n)]
        pts = " ".join(f"{xs[i]:.0f},{up[i]:.0f}" for i in range(n)) + " " + " ".join(f"{xs[i]:.0f},{low[i]:.0f}" for i in range(n-1, -1, -1))
        b += f'<polygon points="{pts}" fill="{PAL[si%len(PAL)]}" opacity="0.85"/>'
    for i, c in enumerate(cats): b += txt(xs[i], oy+H+24, c, 12, fill="var(--muted)")
    return svg(b)

def r_lollipop(d):
    data = d["data"]; ox, oy, W, H = 64, 46, 690, 320; n = len(data); mx = max(v for _, v in data); b = _grid(ox, oy, W, H)
    for i, (lab, v) in enumerate(data):
        x = ox+W*(i+0.5)/n; y = oy+H-H*v/mx
        b += f'<line x1="{x:.0f}" y1="{oy+H}" x2="{x:.0f}" y2="{y:.0f}" stroke="var(--rule)" stroke-width="3"/><circle cx="{x:.0f}" cy="{y:.0f}" r="9" fill="{PAL[i%len(PAL)]}"/>' + txt(x, oy+H+24, lab, 12, fill="var(--muted)")
    return svg(b)

def r_dumbbell(d):
    rows = d["rows"]; ox, oy, W = 170, 56, 560; n = len(rows); rh = 330/n; mx = max(max(r["a"], r["b"]) for r in rows); b = ""
    for i, r in enumerate(rows):
        y = oy+i*rh+rh/2; xa = ox+W*r["a"]/mx; xb = ox+W*r["b"]/mx
        b += f'<line x1="{xa:.0f}" y1="{y:.0f}" x2="{xb:.0f}" y2="{y:.0f}" stroke="var(--rule)" stroke-width="3"/><circle cx="{xa:.0f}" cy="{y:.0f}" r="8" fill="{PAL[0]}"/><circle cx="{xb:.0f}" cy="{y:.0f}" r="8" fill="{PAL[3]}"/>' + txt(ox-14, y+4, r["label"], 12, anchor="end")
    b += f'<rect x="{ox}" y="28" width="13" height="13" rx="3" fill="{PAL[0]}"/>' + txt(ox+19, 39, d.get("la", "A"), 12, anchor="start") + f'<rect x="{ox+110}" y="28" width="13" height="13" rx="3" fill="{PAL[3]}"/>' + txt(ox+129, 39, d.get("lb", "B"), 12, anchor="start")
    return svg(b)

def r_spline(d):
    data = d["data"]; ox, oy, W, H = 64, 46, 690, 320; n = len(data); vs = [v for _, v in data]; mx = max(vs); mn = min(min(vs), 0)
    pts = [(ox+W*i/(n-1), oy+H-H*(v-mn)/((mx-mn) or 1)) for i, (_, v) in enumerate(data)]
    path = f"M{pts[0][0]:.0f},{pts[0][1]:.0f}"
    for i in range(1, len(pts)):
        x0, y0 = pts[i-1]; x1, y1 = pts[i]; mid = (x0+x1)/2
        path += f" C{mid:.0f},{y0:.0f} {mid:.0f},{y1:.0f} {x1:.0f},{y1:.0f}"
    b = _grid(ox, oy, W, H) + f'<path d="{path}" fill="none" stroke="var(--c-1)" stroke-width="3.5"/>'
    for (x, y), (lab, _) in zip(pts, data): b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="5" fill="var(--c-1)"/>' + txt(x, oy+H+24, lab, 12, fill="var(--muted)")
    return svg(b)

def r_rose(d):
    data = d["data"]; n = len(data); cx, cy, R = 270, 230, 165; mx = max(v for _, v in data); b = ""
    for i, (lab, v) in enumerate(data):
        b += f'<path d="{arc(cx,cy,R*v/mx,360*i/n,360*(i+1)/n)}" fill="{PAL[i%len(PAL)]}" opacity="0.85"/>'
    ly = 120
    for i, (lab, v) in enumerate(data):
        b += f'<rect x="540" y="{ly-12}" width="14" height="14" rx="3" fill="{PAL[i%len(PAL)]}"/>' + txt(564, ly+1, lab, 13, anchor="start"); ly += 34
    return svg(b)

def r_ringgauge(d):
    cx, cy, R = 270, 230, 150; pct = d["pct"]; circ = 2*_PI*R
    b = f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="var(--rule)" stroke-width="30"/>'
    b += f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="var(--c-1)" stroke-width="30" stroke-linecap="round" stroke-dasharray="{circ:.0f}" stroke-dashoffset="{circ*(1-pct):.0f}" transform="rotate(-90 {cx} {cy})"/>'
    b += txt(cx, cy+4, f'{int(pct*100)}%', 56, weight="800", fill="var(--c-1)") + txt(cx, cy+40, d.get("label", ""), 15, fill="var(--muted)")
    return svg(b)

def r_boxplot(d):
    g = d["groups"]; ox, oy, W, H = 70, 46, 680, 320; n = len(g); mx = max(x["max"] for x in g); mn = min(x["min"] for x in g)
    Y = lambda v: oy+H-H*(v-mn)/((mx-mn) or 1); b = _grid(ox, oy, W, H); bw = W/n*0.4
    for i, x in enumerate(g):
        cx = ox+W*(i+0.5)/n
        b += f'<line x1="{cx:.0f}" y1="{Y(x["min"]):.0f}" x2="{cx:.0f}" y2="{Y(x["max"]):.0f}" stroke="var(--ink)" stroke-width="1.5"/>'
        b += f'<rect x="{cx-bw/2:.0f}" y="{Y(x["q3"]):.0f}" width="{bw:.0f}" height="{Y(x["q1"])-Y(x["q3"]):.0f}" fill="{PAL[i%len(PAL)]}" opacity="0.55" stroke="{PAL[i%len(PAL)]}"/>'
        b += f'<line x1="{cx-bw/2:.0f}" y1="{Y(x["med"]):.0f}" x2="{cx+bw/2:.0f}" y2="{Y(x["med"]):.0f}" stroke="var(--ink)" stroke-width="2.5"/>' + txt(cx, oy+H+24, x["label"], 12, fill="var(--muted)")
    return svg(b)

def r_candle(d):
    data = d["data"]; ox, oy, W, H = 70, 46, 680, 320; n = len(data); allv = [v for c in data for v in (c["h"], c["l"])]; mx = max(allv); mn = min(allv)
    Y = lambda v: oy+H-H*(v-mn)/((mx-mn) or 1); b = _grid(ox, oy, W, H); bw = W/n*0.45
    for i, c in enumerate(data):
        x = ox+W*(i+0.5)/n; col = PAL[0] if c["c"] >= c["o"] else PAL[3]
        b += f'<line x1="{x:.0f}" y1="{Y(c["h"]):.0f}" x2="{x:.0f}" y2="{Y(c["l"]):.0f}" stroke="{col}" stroke-width="1.5"/>'
        yo = Y(c["o"]); yc = Y(c["c"]); b += f'<rect x="{x-bw/2:.0f}" y="{min(yo,yc):.0f}" width="{bw:.0f}" height="{max(abs(yc-yo),2):.0f}" fill="{col}"/>'
    return svg(b)

def r_pctstacked(d):
    rows = d["rows"]; ser = d["series"]; ox, oy, W = 140, 64, 600; n = len(rows); rh = 320/n; b = ""
    for i, r in enumerate(rows):
        y = oy+i*rh+rh*0.2; tot = sum(r["vals"]); x = ox
        for si, v in enumerate(r["vals"]):
            w = W*v/tot; b += f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{rh*0.6:.0f}" fill="{PAL[si%len(PAL)]}"/>'
            if w > 32: b += txt(x+w/2, y+rh*0.4, f'{round(100*v/tot)}%', 11, fill="#fff", weight="600")
            x += w
        b += txt(ox-12, y+rh*0.4, r["label"], 12, anchor="end")
    for si, nm in enumerate(ser): b += f'<rect x="{ox+si*130}" y="30" width="13" height="13" rx="3" fill="{PAL[si%len(PAL)]}"/>' + txt(ox+si*130+19, 41, nm, 12, anchor="start")
    return svg(b)

def r_ghbars(d):
    cats = d["cats"]; ser = d["series"]; ox, oy, W = 150, 54, 580; n = len(cats); m = len(ser); gh = 330/n; bh = gh*0.7/m; mx = max(max(s["vals"]) for s in ser); b = ""
    for i, c in enumerate(cats):
        gy = oy+i*gh+gh*0.15
        for si, s in enumerate(ser):
            b += f'<rect x="{ox}" y="{gy+si*bh:.0f}" width="{W*s["vals"][i]/mx:.0f}" height="{bh-2:.0f}" rx="3" fill="{PAL[si%len(PAL)]}"/>'
        b += txt(ox-12, gy+gh*0.35, c, 12, anchor="end")
    for si, s in enumerate(ser): b += f'<rect x="{ox+si*120}" y="28" width="13" height="13" rx="3" fill="{PAL[si%len(PAL)]}"/>' + txt(ox+si*120+19, 39, s["name"], 12, anchor="start")
    return svg(b)

def r_rangebars(d):
    rows = d["rows"]; ox, oy, W = 160, 54, 570; n = len(rows); rh = 330/n; mx = max(r["hi"] for r in rows); mn = min(r["lo"] for r in rows); b = ""
    for i, r in enumerate(rows):
        y = oy+i*rh+rh*0.25; x0 = ox+W*(r["lo"]-mn)/((mx-mn) or 1); x1 = ox+W*(r["hi"]-mn)/((mx-mn) or 1)
        b += f'<rect x="{x0:.0f}" y="{y:.0f}" width="{max(x1-x0,4):.0f}" height="{rh*0.5:.0f}" rx="6" fill="{PAL[i%len(PAL)]}"/>' + txt(ox-12, y+rh*0.32, r["label"], 12, anchor="end") + txt(x0-8, y+rh*0.34, str(r["lo"]), 11, anchor="end", fill="var(--muted)") + txt(x1+8, y+rh*0.34, str(r["hi"]), 11, anchor="start", fill="var(--muted)")
    return svg(b)

def r_marimekko(d):
    cols = d["cols"]; ox, oy, W, H = 60, 50, 680, 340; totw = sum(c["w"] for c in cols); x = ox; b = ""
    for ci, c in enumerate(cols):
        cw = W*c["w"]/totw; tot = sum(c["vals"]); y = oy
        for si, v in enumerate(c["vals"]):
            h = H*v/tot; b += f'<rect x="{x:.0f}" y="{y:.0f}" width="{cw-2:.0f}" height="{h-2:.0f}" fill="{PAL[si%len(PAL)]}" opacity="0.88"/>'; y += h
        b += txt(x+cw/2, oy+H+22, c["label"], 12, fill="var(--muted)"); x += cw
    return svg(b)

def r_pareto(d):
    data = d["data"]; ox, oy, W, H = 70, 46, 680, 320; n = len(data); mx = max(v for _, v in data); tot = sum(v for _, v in data)
    b = _grid(ox, oy, W, H); bw = W/n*0.6; cum = 0; pts = []
    for i, (lab, v) in enumerate(data):
        x = ox+W*i/n+(W/n-bw)/2; h = H*v/mx; b += f'<rect x="{x:.0f}" y="{oy+H-h:.0f}" width="{bw:.0f}" height="{h:.0f}" fill="{PAL[0]}" opacity="0.8"/>' + txt(x+bw/2, oy+H+22, lab, 11, fill="var(--muted)")
        cum += v; pts.append((x+bw/2, oy+H-H*cum/tot))
    b += f'<polyline points="{" ".join(f"{x:.0f},{y:.0f}" for x,y in pts)}" fill="none" stroke="{PAL[3]}" stroke-width="3"/>'
    for x, y in pts: b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="5" fill="{PAL[3]}"/>'
    return svg(b)

def r_combo(d):
    cats = d["cats"]; bars = d["bars"]; line = d["line"]; ox, oy, W, H = 70, 46, 680, 320; n = len(cats); mxb = max(bars); mxl = max(line)
    b = _grid(ox, oy, W, H); bw = W/n*0.55
    for i in range(n):
        x = ox+W*i/n+(W/n-bw)/2; h = H*bars[i]/mxb; b += f'<rect x="{x:.0f}" y="{oy+H-h:.0f}" width="{bw:.0f}" height="{h:.0f}" fill="{PAL[0]}" opacity="0.55"/>' + txt(ox+W*(i+0.5)/n, oy+H+22, cats[i], 11, fill="var(--muted)")
    pts = [(ox+W*(i+0.5)/n, oy+H-H*line[i]/mxl) for i in range(n)]
    b += f'<polyline points="{" ".join(f"{x:.0f},{y:.0f}" for x,y in pts)}" fill="none" stroke="{PAL[3]}" stroke-width="3"/>'
    for x, y in pts: b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="5" fill="{PAL[3]}"/>'
    return svg(b)

def r_radialbars(d):
    data = d["data"]; cx, cy = 400, 235; n = len(data); mx = max(v for _, v in data); b = ""
    for i, (lab, v) in enumerate(data):
        ang = 360*i/n; x0, y0 = polar(cx, cy, 64, ang); x1, y1 = polar(cx, cy, 64+150*v/mx, ang)
        b += f'<line x1="{x0:.0f}" y1="{y0:.0f}" x2="{x1:.0f}" y2="{y1:.0f}" stroke="{PAL[i%len(PAL)]}" stroke-width="15" stroke-linecap="round"/>'
        lx, ly = polar(cx, cy, 64+150*v/mx+20, ang); b += txt(lx, ly, lab, 11)
    b += f'<circle cx="{cx}" cy="{cy}" r="54" fill="var(--soft)"/>' + txt(cx, cy+5, d.get("center", ""), 15, weight="700")
    return svg(b)

def r_smallmult(d):
    panels = d["panels"]; pw, ph, ox, oy = 350, 178, 40, 44; b = ""
    for i, p in enumerate(panels[:4]):
        r, c = divmod(i, 2); px = ox+c*(pw+20); py = oy+r*(ph+20)
        b += f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="10" fill="var(--soft)"/>' + txt(px+16, py+26, p["label"], 13, anchor="start", weight="600") + txt(px+pw-16, py+26, p.get("val", ""), 14, anchor="end", weight="700", fill=PAL[i%len(PAL)])
        data = p["data"]; m = len(data); mx = max(data); mn = min(data)
        pts = [(px+16+(pw-32)*j/(m-1), py+ph-20-(ph-58)*(data[j]-mn)/((mx-mn) or 1)) for j in range(m)]
        b += f'<polyline points="{" ".join(f"{x:.0f},{y:.0f}" for x,y in pts)}" fill="none" stroke="{PAL[i%len(PAL)]}" stroke-width="2.5"/>'
    return svg(b)

def r_dotplot(d):
    rows = d["rows"]; ox, oy, W = 160, 50, 560; n = len(rows); rh = 330/n; mx = max(r["v"] for r in rows); b = ""
    for i, r in enumerate(rows):
        y = oy+i*rh+rh/2; x = ox+W*r["v"]/mx
        b += f'<line x1="{ox}" y1="{y:.0f}" x2="{x:.0f}" y2="{y:.0f}" stroke="var(--rule)" stroke-width="1.5"/><circle cx="{x:.0f}" cy="{y:.0f}" r="9" fill="{PAL[i%len(PAL)]}"/>' + txt(ox-12, y+4, r["label"], 12, anchor="end") + txt(x+16, y+4, str(r["v"]), 11, anchor="start", weight="600")
    return svg(b)

def r_stepline(d):
    data = d["data"]; ox, oy, W, H = 64, 46, 690, 320; n = len(data); vs = [v for _, v in data]; mx = max(vs); mn = min(min(vs), 0)
    pts = [(ox+W*i/(n-1), oy+H-H*(v-mn)/((mx-mn) or 1)) for i, (_, v) in enumerate(data)]
    path = f"M{pts[0][0]:.0f},{pts[0][1]:.0f}"
    for i in range(1, len(pts)): path += f" H{pts[i][0]:.0f} V{pts[i][1]:.0f}"
    b = _grid(ox, oy, W, H) + f'<path d="{path}" fill="none" stroke="var(--c-1)" stroke-width="3"/>'
    for (x, y), (lab, _) in zip(pts, data): b += txt(x, oy+H+24, lab, 12, fill="var(--muted)")
    return svg(b)

def r_bubblegrid(d):
    rows = d["rows"]; cols = d["cols"]; cells = d["cells"]; ox, oy = 150, 60; cw = 560/len(cols); ch = 64; mx = max(max(r) for r in cells); b = ""
    for ci, c in enumerate(cols): b += txt(ox+cw*ci+cw/2, oy-12, c, 12, fill="var(--muted)")
    for ri, rn in enumerate(rows):
        b += txt(ox-12, oy+ch*ri+ch/2+4, rn, 12, anchor="end")
        for ci in range(len(cols)):
            b += f'<circle cx="{ox+cw*ci+cw/2:.0f}" cy="{oy+ch*ri+ch/2:.0f}" r="{4+18*cells[ri][ci]/mx:.0f}" fill="{PAL[ci%len(PAL)]}" opacity="0.8"/>'
    return svg(b)

def r_areacompare(d):
    a = d["a"]; bb = d["b"]; ox, oy, W, H = 64, 46, 690, 320; n = len(a); mx = max(max(a), max(bb))
    def poly(s, col, op):
        ps = [(ox+W*i/(n-1), oy+H-H*s[i]/mx) for i in range(n)]
        return f'<polygon points="{ox},{oy+H} {" ".join(f"{x:.0f},{y:.0f}" for x,y in ps)} {ox+W},{oy+H}" fill="{col}" opacity="{op}"/><polyline points="{" ".join(f"{x:.0f},{y:.0f}" for x,y in ps)}" fill="none" stroke="{col}" stroke-width="2.5"/>'
    b = _grid(ox, oy, W, H) + poly(a, PAL[0], "0.22") + poly(bb, PAL[3], "0.22")
    b += f'<rect x="{ox}" y="24" width="13" height="13" rx="3" fill="{PAL[0]}"/>' + txt(ox+19, 35, d.get("la", "A"), 12, anchor="start") + f'<rect x="{ox+110}" y="24" width="13" height="13" rx="3" fill="{PAL[3]}"/>' + txt(ox+129, 35, d.get("lb", "B"), 12, anchor="start")
    return svg(b)

def r_sitemap(d):
    b = box(320, 30, 160, 48, d["home"], "", fill="var(--c-1)", tcol="#fff", stroke="var(--c-1)"); y = 120
    for p in d["pages"]:
        b += f'<line x1="340" y1="78" x2="340" y2="{y+22:.0f}" stroke="var(--rule)" stroke-width="1.4"/><line x1="340" y1="{y+22:.0f}" x2="360" y2="{y+22:.0f}" stroke="var(--rule)" stroke-width="1.4"/>'
        b += box(360, y, 150, 40, p["name"], "", fill="var(--soft)", tsize=13); sx = 540
        for j, s in enumerate(p.get("sub", [])[:2]):
            b += f'<line x1="510" y1="{y+20:.0f}" x2="{sx+j*150:.0f}" y2="{y+20:.0f}" stroke="var(--rule)" stroke-width="1.2"/><rect x="{sx+j*150:.0f}" y="{y+2:.0f}" width="140" height="36" rx="6" fill="var(--paper)" stroke="var(--rule)"/>' + txt(sx+j*150+70, y+24, s, 11)
        y += 56
    return svg(b, "0 0 800 480")

def r_wbs(d):
    root = d["root"]; ch = root.get("children", []); n = len(ch); b = box(330, 26, 140, 50, "1 " + root["name"], "", fill="var(--c-1)", tcol="#fff", stroke="var(--c-1)")
    cw = 150; total = n*cw; x0 = 400-total/2; b += '<line x1="400" y1="76" x2="400" y2="100" stroke="var(--rule)" stroke-width="1.4"/>'
    for i, c in enumerate(ch):
        cx = x0+i*cw+cw/2; b += f'<line x1="400" y1="100" x2="{cx:.0f}" y2="100" stroke="var(--rule)" stroke-width="1.4"/><line x1="{cx:.0f}" y1="100" x2="{cx:.0f}" y2="130" stroke="var(--rule)" stroke-width="1.4"/>'
        b += box(cx-62, 130, 124, 46, f'1.{i+1} {c["name"]}', "", fill="var(--soft)", tsize=12)
        for j, g in enumerate(c.get("children", [])[:3]):
            gy = 210+j*46; b += f'<line x1="{cx:.0f}" y1="176" x2="{cx:.0f}" y2="{gy+22:.0f}" stroke="var(--rule)" stroke-width="1.2"/>' + box(cx-54, gy, 108, 38, f'1.{i+1}.{j+1}', "", fill="var(--paper)", tsize=11)
    return svg(b)

def r_dectree(d):
    b = f'<polygon points="400,30 500,80 400,130 300,80" fill="var(--soft)" stroke="var(--c-1)" stroke-width="1.6"/>' + txt(400, 84, d["q"], 13, weight="600")
    opts = d["branches"]; n = len(opts); ox = 80; bw = (640)/n
    for i, o in enumerate(opts):
        x = ox+bw*i+bw/2; b += f'<line x1="400" y1="130" x2="{x:.0f}" y2="200" stroke="var(--c-1)" stroke-width="2"/>' + txt((400+x)/2+10, 168, o["edge"], 11, fill="var(--muted)")
        b += box(x-70, 200, 140, 56, o["label"], o.get("sub", ""), fill="var(--paper)")
    return svg(b)

def r_statemachine(d):
    st = d["states"]; n = len(st); cx, cy = 400, 230; b = ""
    pos = [polar(cx, cy, 150, 360*i/n) for i in range(n)]
    for tr in d.get("transitions", []):
        x0, y0 = pos[tr["from"]]; x1, y1 = pos[tr["to"]]
        b += f'<path d="M{x0:.0f},{y0:.0f} L{x1:.0f},{y1:.0f}" stroke="var(--rule)" stroke-width="2" marker-end="url(#sm)"/>'
    for i, s in enumerate(st):
        x, y = pos[i]; b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="40" fill="var(--soft)" stroke="var(--c-1)" stroke-width="2"/>' + txt(x, y+5, s, 12, weight="600")
    return svg(f'<defs><marker id="sm" markerWidth="9" markerHeight="9" refX="20" refY="4.5" orient="auto"><path d="M0,0 L8,4.5 L0,9 z" fill="var(--c-1)"/></marker></defs>{b}')

def r_er(d):
    ent = d["entities"]; pos = [(80, 70), (460, 70), (270, 280)][:len(ent)]; b = ""
    boxes = []
    for (x, y), en in zip(pos, ent):
        h = 40+len(en["attrs"])*26; boxes.append((x+130, y+h/2))
        b += f'<rect x="{x}" y="{y}" width="260" height="{h}" rx="8" fill="var(--paper)" stroke="var(--c-1)" stroke-width="1.6"/>'
        b += f'<rect x="{x}" y="{y}" width="260" height="34" rx="8" fill="var(--c-1)"/>' + txt(x+130, y+22, en["name"], 14, weight="700", fill="#fff")
        for j, a in enumerate(en["attrs"]): b += txt(x+16, y+58+j*26, a, 12, anchor="start", fill="var(--ink)")
    for rel in d.get("relations", []):
        a = boxes[rel[0]]; c = boxes[rel[1]]; b += f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{c[0]:.0f}" y2="{c[1]:.0f}" stroke="var(--rule)" stroke-width="2"/>'
    return svg(b)

def r_userflow(d):
    steps = d["steps"]; ox, oy = 50, 120; cw = 150; gap = 30; b = ""
    x = ox
    for i, s in enumerate(steps):
        if s.get("decision"):
            b += f'<polygon points="{x+60},{oy-40} {x+135},{oy+28} {x+60},{oy+96} {x-15},{oy+28}" fill="var(--soft)" stroke="var(--c-1)" stroke-width="1.5"/>' + txt(x+60, oy+32, s["label"], 11, weight="600"); w = 135
        else:
            b += f'<rect x="{x}" y="{oy}" width="{cw}" height="56" rx="9" fill="var(--paper)" stroke="var(--rule)"/>' + txt(x+cw/2, oy+32, s["label"], 13, weight="600"); w = cw
        if i < len(steps)-1: b += f'<path d="M{x+w},{oy+28} h{gap-6}" stroke="var(--c-1)" stroke-width="2.2" marker-end="url(#uf)"/>'; x += w+gap
    return svg(f'<defs><marker id="uf" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L8,4.5 L0,9 z" fill="var(--c-1)"/></marker></defs>{b}')

def r_affinity(d):
    groups = d["groups"]; n = len(groups); gw = 760/n; b = ""
    for gi, g in enumerate(groups):
        gx = 30+gi*gw; b += txt(gx+gw/2-10, 50, g["name"], 14, weight="700", fill=PAL[gi%len(PAL)])
        for j, note in enumerate(g["notes"][:4]):
            y = 70+j*88; b += f'<rect x="{gx+10:.0f}" y="{y}" width="{gw-30:.0f}" height="76" rx="6" fill="{PAL[gi%len(PAL)]}" opacity="0.16" stroke="{PAL[gi%len(PAL)]}" stroke-width="1"/>' + txt(gx+gw/2-10, y+42, note, 12)
    return svg(b)

def r_depmatrix(d):
    items = d["items"]; deps = d["deps"]; n = len(items); ox, oy = 150, 130; cell = min(46, 320/n); b = ""
    for i, it in enumerate(items):
        b += txt(ox+cell*i+cell/2, oy-12, str(i+1), 12, fill="var(--muted)") + txt(ox-12, oy+cell*i+cell/2+4, f'{i+1}. {it}', 12, anchor="end")
    for i in range(n):
        for j in range(n):
            x = ox+cell*j; y = oy+cell*i
            b += f'<rect x="{x:.0f}" y="{y:.0f}" width="{cell-2:.0f}" height="{cell-2:.0f}" fill="{"var(--rule-soft)" if i==j else "var(--paper)"}" stroke="var(--rule)"/>'
            if [i, j] in deps: b += f'<circle cx="{x+cell/2:.0f}" cy="{y+cell/2:.0f}" r="{cell*0.28:.0f}" fill="var(--c-1)"/>'
    return svg(b)

def r_arcdiagram(d):
    nodes = d["nodes"]; edges = d["edges"]; n = len(nodes); ox, W, y = 70, 660, 300; xs = [ox+W*i/(n-1) for i in range(n)]; b = ""
    for e in edges:
        x0 = xs[e[0]]; x1 = xs[e[1]]; r = abs(x1-x0)/2; mx = (x0+x1)/2
        b += f'<path d="M{x0:.0f},{y} A{r:.0f},{r:.0f} 0 0 1 {x1:.0f},{y}" fill="none" stroke="var(--c-1)" stroke-width="2" opacity="0.6"/>'
    b += f'<line x1="{ox}" y1="{y}" x2="{ox+W}" y2="{y}" stroke="var(--rule)" stroke-width="2"/>'
    for i, nm in enumerate(nodes): b += f'<circle cx="{xs[i]:.0f}" cy="{y}" r="9" fill="{PAL[i%len(PAL)]}"/>' + txt(xs[i], y+30, nm, 11)
    return svg(b)

def r_chord(d):
    nodes = d["nodes"]; links = d["links"]; n = len(nodes); cx, cy, R = 400, 230, 170; b = ""
    pos = [polar(cx, cy, R, 360*i/n) for i in range(n)]
    for l in links:
        x0, y0 = pos[l[0]]; x1, y1 = pos[l[1]]; b += f'<path d="M{x0:.0f},{y0:.0f} Q{cx},{cy} {x1:.0f},{y1:.0f}" fill="none" stroke="{PAL[l[0]%len(PAL)]}" stroke-width="3" opacity="0.4"/>'
    for i, nm in enumerate(nodes):
        x, y = pos[i]; b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="11" fill="{PAL[i%len(PAL)]}"/>'; lx, ly = polar(cx, cy, R+26, 360*i/n); b += txt(lx, ly, nm, 12)
    return svg(b)

def r_sunburst(d):
    cx, cy = 270, 230; root = d["root"]; ch = root["children"]; tot = sum(c["value"] for c in ch); a = 0; b = f'<circle cx="{cx}" cy="{cy}" r="50" fill="var(--c-1)"/>' + txt(cx, cy+5, root["name"], 13, weight="700", fill="#fff")
    for i, c in enumerate(ch):
        ang = 360*c["value"]/tot; col = PAL[i%len(PAL)]
        b += f'<path d="{_ring(cx,cy,50,110,a,a+ang)}" fill="{col}" opacity="0.85"/>'
        sub = c.get("children", []); st = sum(s["value"] for s in sub) or 1; aa = a
        for s in sub:
            sang = ang*s["value"]/st; b += f'<path d="{_ring(cx,cy,110,165,aa,aa+sang)}" fill="{col}" opacity="0.5"/>'; aa += sang
        a += ang
    return svg(b)

def _ring(cx, cy, r0, r1, a0, a1):
    import math as _m
    p0 = polar(cx, cy, r1, a0); p1 = polar(cx, cy, r1, a1); p2 = polar(cx, cy, r0, a1); p3 = polar(cx, cy, r0, a0)
    large = 1 if (a1-a0) % 360 > 180 else 0
    return f"M{p0[0]:.1f},{p0[1]:.1f} A{r1},{r1} 0 {large} 1 {p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} A{r0},{r0} 0 {large} 0 {p3[0]:.1f},{p3[1]:.1f} Z"

def r_icicle(d):
    root = d["root"]; ox, oy, W = 40, 60, 720; rh = 90; tot = sum(c["value"] for c in root["children"]); b = ""
    b += f'<rect x="{ox}" y="{oy}" width="{W}" height="{rh-6}" rx="6" fill="var(--c-1)"/>' + txt(ox+W/2, oy+rh/2, root["name"], 14, weight="700", fill="#fff")
    x = ox
    for i, c in enumerate(root["children"]):
        w = W*c["value"]/tot; b += f'<rect x="{x:.0f}" y="{oy+rh}" width="{w-4:.0f}" height="{rh-6}" rx="6" fill="{PAL[i%len(PAL)]}" opacity="0.85"/>' + txt(x+w/2, oy+rh+rh/2, c["name"], 12, fill="#fff")
        sub = c.get("children", []); st = sum(s["value"] for s in sub) or 1; xx = x
        for s in sub:
            sw = w*s["value"]/st; b += f'<rect x="{xx:.0f}" y="{oy+2*rh}" width="{sw-3:.0f}" height="{rh-6}" rx="6" fill="{PAL[i%len(PAL)]}" opacity="0.5"/>' + txt(xx+sw/2, oy+2*rh+rh/2, s["name"], 11); xx += sw
        x += w
    return svg(b)

def r_packing(d):
    cx, cy = 400, 230; b = f'<circle cx="{cx}" cy="{cy}" r="200" fill="var(--soft)" stroke="var(--rule)"/>'
    cfg = [(-90, 0, 80), (80, -40, 60), (60, 90, 70), (-70, 90, 50), (160, 70, 44)]
    for i, c in enumerate(d["circles"][:5]):
        dx, dy, r = cfg[i]; b += f'<circle cx="{cx+dx}" cy="{cy+dy}" r="{r}" fill="{PAL[i%len(PAL)]}" opacity="0.85"/>' + txt(cx+dx, cy+dy+4, c["label"], 12, weight="600", fill="#fff")
    return svg(b)

def r_bracket(d):
    t = d["teams"]; ox = 40; b = ""
    y = [70, 150, 250, 330]
    for i in range(4): b += f'<rect x="{ox}" y="{y[i]-18}" width="150" height="36" rx="6" fill="var(--soft)" stroke="var(--rule)"/>' + txt(ox+75, y[i]+4, t[i], 12, weight="600")
    s1 = (y[0]+y[1])/2; s2 = (y[2]+y[3])/2
    for a, c in ((y[0], s1), (y[1], s1), (y[2], s2), (y[3], s2)): b += f'<path d="M{ox+150},{a} H{ox+220} V{c}" fill="none" stroke="var(--rule)" stroke-width="1.6"/>'
    for yy in (s1, s2): b += f'<rect x="{ox+220}" y="{yy-18}" width="150" height="36" rx="6" fill="var(--paper)" stroke="var(--c-1)"/>' + txt(ox+295, yy+4, "Finalista", 11, fill="var(--muted)")
    fin = (s1+s2)/2
    for a in (s1, s2): b += f'<path d="M{ox+370},{a} H{ox+430} V{fin}" fill="none" stroke="var(--rule)" stroke-width="1.6"/>'
    b += f'<rect x="{ox+430}" y="{fin-22}" width="160" height="44" rx="8" fill="var(--c-1)"/>' + txt(ox+510, fin+5, d.get("winner", "Vítěz"), 14, weight="700", fill="#fff")
    return svg(b)

def r_proccircular(d):
    st = d["stages"]; n = len(st); cx, cy = 400, 230; b = ""
    for i in range(n):
        b += f'<path d="{_ring(cx,cy,90,160,360*i/n+3,360*(i+1)/n-3)}" fill="{PAL[i%len(PAL)]}" opacity="0.85"/>'
        x, y = polar(cx, cy, 125, 360*(i+0.5)/n); b += txt(x, y+4, st[i], 12, weight="600", fill="#fff")
    b += f'<circle cx="{cx}" cy="{cy}" r="60" fill="var(--soft)"/>' + txt(cx, cy+5, d.get("center", ""), 15, weight="700")
    return svg(b)

def r_hierh(d):
    root = d["root"]; ch = root.get("children", []); n = len(ch); b = box(40, 200-30, 130, 60, root["name"], "", fill="var(--c-1)", tcol="#fff", stroke="var(--c-1)")
    ch_h = 360/max(n, 1)
    for i, c in enumerate(ch):
        cy = 40+ch_h*i+ch_h/2; b += f'<path d="M170,200 H230 V{cy:.0f} H290" fill="none" stroke="var(--rule)" stroke-width="1.5"/>' + box(290, cy-24, 150, 48, c["name"], c.get("role", ""), fill="var(--soft)", tsize=13)
        for j, g in enumerate(c.get("children", [])[:2]):
            gy = cy-16+j*34; b += f'<path d="M440,{cy:.0f} H470 V{gy+14:.0f} H500" fill="none" stroke="var(--rule)" stroke-width="1.2"/>' + box(500, gy, 130, 30, g["name"], "", fill="var(--paper)", tsize=11)
    return svg(b)

def r_swot(d):
    q = d["quadrants"]; ox, oy, S = 80, 50, 640; cell = S/2; titles = ["Silné stránky", "Slabé stránky", "Příležitosti", "Hrozby"]; cols = [PAL[0], PAL[3], PAL[1], PAL[2]]
    b = ""
    for i in range(4):
        r, c = divmod(i, 2); x = ox+c*cell; y = oy+r*(cell*0.55+8)
        b += f'<rect x="{x:.0f}" y="{y:.0f}" width="{cell-8:.0f}" height="{cell*0.55:.0f}" rx="10" fill="{cols[i]}" opacity="0.12" stroke="{cols[i]}"/>' + txt(x+18, y+28, q[i].get("h", titles[i]), 14, anchor="start", weight="700", fill=cols[i])
        for j, it in enumerate(q[i]["items"][:3]): b += txt(x+18, y+56+j*24, "&#8226; " + it, 12, anchor="start")
    return svg(b, "0 0 800 480")

def r_bcg(d):
    ox, oy, S = 150, 40, 360; b = f'<rect x="{ox}" y="{oy}" width="{S}" height="{S}" fill="var(--soft)" stroke="var(--rule)"/>'
    b += f'<line x1="{ox+S/2}" y1="{oy}" x2="{ox+S/2}" y2="{oy+S}" stroke="var(--rule)"/><line x1="{ox}" y1="{oy+S/2}" x2="{ox+S}" y2="{oy+S/2}" stroke="var(--rule)"/>'
    labs = [("Hvězdy", 0.25, 0.25), ("Otazníky", 0.75, 0.25), ("Dojné krávy", 0.25, 0.75), ("Bídní psi", 0.75, 0.75)]
    for nm, fx, fy in labs: b += txt(ox+S*fx, oy+S*fy-S*0.18, nm, 12, weight="600", fill="var(--muted)")
    for i, p in enumerate(d["points"]):
        x = ox+p["x"]*S; y = oy+(1-p["y"])*S; b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{10+p.get("r",0.4)*26:.0f}" fill="{PAL[i%len(PAL)]}" opacity="0.7"/>' + txt(x, y+4, p["label"], 11, weight="600")
    b += txt(ox+S/2, oy+S+24, "Podíl na trhu", 12, fill="var(--muted)") + txt(ox-16, oy+S/2, "Růst trhu", 12, anchor="end", fill="var(--muted)")
    return svg(b)

def r_valuechain(d):
    st = d["steps"]; n = len(st); ox, oy, H = 40, 175, 110; cw = 720/n; b = ""
    for i, s in enumerate(st):
        x = ox+cw*i; tip = 24
        pts = f"{x},{oy} {x+cw-tip-4},{oy} {x+cw-4},{oy+H/2} {x+cw-tip-4},{oy+H} {x},{oy+H} {x+tip},{oy+H/2}" if i else f"{x},{oy} {x+cw-tip-4},{oy} {x+cw-4},{oy+H/2} {x+cw-tip-4},{oy+H} {x},{oy+H}"
        b += f'<polygon points="{pts}" fill="{PAL[i%len(PAL)]}" opacity="0.9"/>' + txt(x+cw/2, oy+H/2+4, s, 12, weight="600", fill="#fff")
    return svg(b)

def r_stagegate(d):
    st = d["stages"]; n = len(st); ox = 40; y = 200; b = ""; x = ox
    for i, s in enumerate(st):
        b += box(x, y-40, 120, 80, s["label"], s.get("sub", ""), tsize=13); x += 120
        if i < n-1:
            b += f'<polygon points="{x+24},{y-26} {x+52},{y} {x+24},{y+26} {x-4},{y}" fill="var(--soft)" stroke="var(--c-1)" stroke-width="1.5"/>' + txt(x+24, y+4, "G" + str(i+1), 12, weight="700", fill="var(--c-1)"); x += 56
    return svg(b)

def r_mileflags(d):
    its = d["items"]; n = len(its); ox, W, y = 50, 700, 250; b = f'<line x1="{ox}" y1="{y}" x2="{ox+W}" y2="{y}" stroke="var(--rule)" stroke-width="3"/>'
    for i, (date, label) in enumerate(its):
        x = ox+W*(i+0.5)/n; b += f'<line x1="{x:.0f}" y1="{y}" x2="{x:.0f}" y2="{y-70}" stroke="{PAL[i%len(PAL)]}" stroke-width="2"/>'
        b += f'<rect x="{x:.0f}" y="{y-94}" width="120" height="40" rx="6" fill="{PAL[i%len(PAL)]}"/>' + txt(x+60, y-69, label, 12, weight="600", fill="#fff") + f'<circle cx="{x:.0f}" cy="{y}" r="8" fill="{PAL[i%len(PAL)]}"/>' + txt(x, y+26, date, 11, fill="var(--muted)")
    return svg(b)

def r_progbars(d):
    rows = d["rows"]; ox, oy, W = 200, 60, 520; n = len(rows); rh = 320/n; b = ""
    for i, r in enumerate(rows):
        y = oy+i*rh+rh*0.25; b += f'<rect x="{ox}" y="{y:.0f}" width="{W}" height="22" rx="11" fill="var(--rule-soft)"/>'
        b += f'<rect x="{ox}" y="{y:.0f}" width="{W*r["pct"]:.0f}" height="22" rx="11" fill="{PAL[i%len(PAL)]}"/>' + txt(ox-14, y+17, r["label"], 13, anchor="end") + txt(ox+W+14, y+17, f'{int(r["pct"]*100)}%', 13, anchor="start", weight="700")
    return svg(b)

def r_thermometer(d):
    cx = 250; top = 50; H = 300; b = f'<rect x="{cx-24}" y="{top}" width="48" height="{H}" rx="24" fill="var(--rule-soft)"/>'
    fill = H*d["pct"]; b += f'<rect x="{cx-24}" y="{top+H-fill:.0f}" width="48" height="{fill:.0f}" rx="24" fill="var(--c-1)"/>'
    b += f'<circle cx="{cx}" cy="{top+H+30}" r="40" fill="var(--c-1)"/>'
    for g in range(6):
        yy = top+H*g/5; b += f'<line x1="{cx+30}" y1="{yy:.0f}" x2="{cx+44}" y2="{yy:.0f}" stroke="var(--rule)"/>' + txt(cx+52, yy+4, str(int(100-20*g)) + "%", 11, anchor="start", fill="var(--muted)")
    b += txt(450, 180, d.get("center", f'{int(d["pct"]*100)}%'), 46, weight="800", fill="var(--c-1)") + txt(450, 215, d.get("label", ""), 14, fill="var(--muted)")
    return svg(b)

def r_curvedtl(d):
    its = d["items"]; n = len(its); ox, W = 60, 680; b = f'<path d="M{ox},360 C{ox+W*0.3:.0f},360 {ox+W*0.2:.0f},80 {ox+W*0.5:.0f},80 C{ox+W*0.8:.0f},80 {ox+W*0.7:.0f},360 {ox+W:.0f},360" fill="none" stroke="var(--rule)" stroke-width="3"/>'
    for i, (date, label) in enumerate(its):
        t = i/(n-1); x = ox+W*t
        y = 360 if t in (0, 1) else (80 if abs(t-0.5) < 0.18 else 220)
        y = 360 - 280*( - (2*t-1)**2 + 1)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="9" fill="{PAL[i%len(PAL)]}"/>' + txt(x, y-18, label, 12, weight="600") + txt(x, y+26, date, 11, fill="var(--muted)")
    return svg(b)

def r_iconstats(d):
    its = d["items"]; n = len(its); gap = 24; w = (760-gap*(n-1))/n; b = ""
    for i, k in enumerate(its):
        x = 20+i*(w+gap); b += f'<rect x="{x:.0f}" y="90" width="{w:.0f}" height="280" rx="16" fill="var(--soft)" stroke="var(--rule)"/>'
        b += txt(x+w/2, 180, k["num"], 40, weight="800", fill=PAL[i%len(PAL)]) + txt(x+w/2, 215, k["label"], 13, fill="var(--muted)")
        spk = k.get("spark", []); m = len(spk)
        if m > 1:
            mx = max(spk); mn = min(spk); pts = [(x+20+(w-40)*j/(m-1), 330-50*(spk[j]-mn)/((mx-mn) or 1)) for j in range(m)]
            b += f'<polyline points="{" ".join(f"{px:.0f},{py:.0f}" for px,py in pts)}" fill="none" stroke="{PAL[i%len(PAL)]}" stroke-width="2.5"/>'
    return svg(b)

def r_versus(d):
    b = f'<rect x="40" y="60" width="330" height="340" rx="14" fill="{PAL[0]}" opacity="0.1" stroke="{PAL[0]}"/>' + f'<rect x="430" y="60" width="330" height="340" rx="14" fill="{PAL[3]}" opacity="0.1" stroke="{PAL[3]}"/>'
    b += txt(205, 100, d["a"]["name"], 18, weight="800", fill=PAL[0]) + txt(595, 100, d["b"]["name"], 18, weight="800", fill=PAL[3])
    b += f'<circle cx="400" cy="100" r="28" fill="var(--ink)"/>' + txt(400, 107, "VS", 15, weight="800", fill="#fff")
    for j, (la, lb) in enumerate(zip(d["a"]["rows"], d["b"]["rows"])):
        y = 160+j*56; b += txt(205, y, la, 13) + txt(595, y, lb, 13) + f'<line x1="70" y1="{y+18}" x2="340" y2="{y+18}" stroke="var(--rule)"/><line x1="460" y1="{y+18}" x2="730" y2="{y+18}" stroke="var(--rule)"/>'
    return svg(b)

def r_quadbubble(d):
    ox, oy, S = 150, 40, 360; b = f'<rect x="{ox}" y="{oy}" width="{S}" height="{S}" fill="var(--soft)" stroke="var(--rule)"/>'
    b += f'<line x1="{ox+S/2}" y1="{oy}" x2="{ox+S/2}" y2="{oy+S}" stroke="var(--rule)"/><line x1="{ox}" y1="{oy+S/2}" x2="{ox+S}" y2="{oy+S/2}" stroke="var(--rule)"/>'
    b += txt(ox+S*0.25, oy+18, "Rychlé výhry", 11, fill="var(--muted)") + txt(ox+S*0.75, oy+18, "Velké projekty", 11, fill="var(--muted)")
    for i, p in enumerate(d["points"]):
        x = ox+p["x"]*S; y = oy+(1-p["y"])*S; b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{10+p.get("r",0.4)*26:.0f}" fill="{PAL[i%len(PAL)]}" opacity="0.7"/>' + txt(x, y+4, p["label"], 11, weight="600")
    b += txt(ox+S/2, oy+S+24, "Náročnost", 12, fill="var(--muted)") + txt(ox-16, oy+S/2, "Dopad", 12, anchor="end", fill="var(--muted)")
    return svg(b)

def r_funnelh(d):
    st = d["stages"]; n = len(st); ox, W = 40, 720; topH = 320; b = ""
    for i, (label, val) in enumerate(st):
        x0 = ox+W*i/n; x1 = ox+W*(i+1)/n; h0 = topH*(1-i/(n+1)); h1 = topH*(1-(i+1)/(n+1)); cy = 230
        pts = f"{x0:.0f},{cy-h0/2:.0f} {x1:.0f},{cy-h1/2:.0f} {x1:.0f},{cy+h1/2:.0f} {x0:.0f},{cy+h0/2:.0f}"
        b += f'<polygon points="{pts}" fill="{PAL[i%len(PAL)]}" opacity="0.9"/>' + txt((x0+x1)/2, cy-4, label, 13, weight="600", fill="#fff") + txt((x0+x1)/2, cy+18, val, 12, fill="#fff")
    return svg(b)

def r_metriccards(d):
    its = d["items"]; n = len(its); gap = 22; w = (760-gap*(n-1))/n; b = ""
    for i, k in enumerate(its):
        x = 20+i*(w+gap); b += f'<rect x="{x:.0f}" y="110" width="{w:.0f}" height="240" rx="16" fill="var(--paper)" stroke="var(--rule)"/>'
        b += txt(x+24, 160, k["label"], 13, anchor="start", fill="var(--muted)") + txt(x+24, 210, k["num"], 36, anchor="start", weight="800", fill=PAL[i%len(PAL)])
        b += txt(x+w-24, 160, k.get("delta", ""), 13, anchor="end", weight="700", fill=PAL[i%len(PAL)])
        spk = k.get("spark", []); m = len(spk)
        if m > 1:
            mx = max(spk); mn = min(spk); pts = [(x+24+(w-48)*j/(m-1), 320-46*(spk[j]-mn)/((mx-mn) or 1)) for j in range(m)]
            b += f'<polyline points="{" ".join(f"{px:.0f},{py:.0f}" for px,py in pts)}" fill="none" stroke="{PAL[i%len(PAL)]}" stroke-width="2.5"/>'
    return svg(b)

def r_ribbontl(d):
    its = d["items"]; n = len(its); ox, W, y = 60, 680, 230; b = f'<line x1="{ox}" y1="{y}" x2="{ox+W}" y2="{y}" stroke="var(--c-1)" stroke-width="3"/>'
    for i, (date, label) in enumerate(its):
        x = ox+W*(i+0.5)/n; up = i % 2 == 0; cy = y-110 if up else y+50
        b += f'<line x1="{x:.0f}" y1="{y}" x2="{x:.0f}" y2="{cy+(60 if up else 0):.0f}" stroke="var(--rule)" stroke-width="1.5"/>'
        b += f'<rect x="{x-80:.0f}" y="{cy:.0f}" width="160" height="60" rx="10" fill="var(--soft)" stroke="{PAL[i%len(PAL)]}" stroke-width="1.4"/>' + txt(x, cy+26, label, 12, weight="600") + txt(x, cy+44, date, 11, fill="var(--muted)")
        b += f'<circle cx="{x:.0f}" cy="{y}" r="8" fill="{PAL[i%len(PAL)]}"/>'
    return svg(b)

RENDER.update(stackarea=r_stackarea, lollipop=r_lollipop, dumbbell=r_dumbbell, spline=r_spline,
    rose=r_rose, ringgauge=r_ringgauge, boxplot=r_boxplot, candle=r_candle, pctstacked=r_pctstacked,
    ghbars=r_ghbars, rangebars=r_rangebars, marimekko=r_marimekko, pareto=r_pareto, combo=r_combo,
    radialbars=r_radialbars, smallmult=r_smallmult, dotplot=r_dotplot, stepline=r_stepline,
    bubblegrid=r_bubblegrid, areacompare=r_areacompare, sitemap=r_sitemap, wbs=r_wbs, dectree=r_dectree,
    statemachine=r_statemachine, er=r_er, userflow=r_userflow, affinity=r_affinity, depmatrix=r_depmatrix,
    arcdiagram=r_arcdiagram, chord=r_chord, sunburst=r_sunburst, icicle=r_icicle, packing=r_packing,
    bracket=r_bracket, proccircular=r_proccircular, hierh=r_hierh, swot=r_swot, bcg=r_bcg,
    valuechain=r_valuechain, stagegate=r_stagegate, mileflags=r_mileflags, progbars=r_progbars,
    thermometer=r_thermometer, curvedtl=r_curvedtl, iconstats=r_iconstats, versus=r_versus,
    quadbubble=r_quadbubble, funnelh=r_funnelh, metriccards=r_metriccards, ribbontl=r_ribbontl)

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
:root{{--c-1:{c1};--c-2:{c2};--c-3:{c3};--c-4:{c4};--c-5:{c5};--ink:#1c2230;--muted:#6b7280;--paper:#fff;--soft:{soft};--rule:#e4e7ee;--rule-soft:#eef1f6;--ui:"Inter Tight",system-ui,sans-serif;--mono:"JetBrains Mono",monospace}}
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
