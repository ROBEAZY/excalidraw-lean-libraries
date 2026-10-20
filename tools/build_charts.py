"""Lean Six Sigma charts and problem-solving templates.

Usage: python tools/build_charts.py <repo_root>
Writes libraries/lean-six-sigma-charts.excalidrawlib and previews/lean-six-sigma-charts.excalidraw
"""
import sys, math
from excalib import *

seed(20261021)

BLUE, GREEN, YELLOW, ORANGE, RED, GREY = "#a5d8ff", "#b2f2bb", "#ffec99", "#ffd8a8", "#ffc9c9", "#e9ecef"

# --- PDCA cycle: four arc segments with arrow tips, clockwise from top-right -------------------
g = nid()
els = []
cx, cy, R, r = 150, 150, 130, 80
for name, a0, a1, fill in (("Plan", 274, 356, BLUE), ("Do", 4, 86, GREEN),
                           ("Check", 94, 176, YELLOW), ("Act", 184, 266, RED)):
    pts = [arc_point(cx, cy, R, a) for a in frange(a0, a1, 6)]
    pts.append(arc_point(cx, cy, (R + r) / 2, a1 + 8))            # arrow tip
    pts += [arc_point(cx, cy, r, a) for a in frange(a1, a0, -6)]
    els.append(poly(pts, 0, 0, g, closed=True, backgroundColor=fill))
    lx, ly = arc_point(cx, cy, (R + r) / 2, (a0 + a1) / 2)
    els.append(centered_text(lx, ly, name, g, size=20))
item("PDCA cycle", els)

# --- DMAIC chevrons -----------------------------------------------------------------------------
g = nid()
els = []
w, h, notch, gap = 150, 70, 25, 6
for i, (p, f) in enumerate(zip(["Define", "Measure", "Analyze", "Improve", "Control"],
                               [BLUE, GREEN, YELLOW, ORANGE, RED])):
    x0 = i * (w + gap)
    pts = [[0, 0], [w - notch, 0], [w, h / 2], [w - notch, h], [0, h]]
    if i > 0:
        pts.append([notch, h / 2])
    els.append(poly(pts, x0, 0, g, closed=True, backgroundColor=f))
    els.append(centered_text(x0 + (w + (notch if i > 0 else 0)) / 2, h / 2, p, g, size=18))
item("DMAIC chevrons", els)

# --- Fishbone (Ishikawa) with the 6M categories --------------------------------------------------
g = nid()
els = []
cy = 170
spine_x0, spine_x1 = 40, 660
els += shape("rectangle", spine_x1, cy - 35, 150, 70, g, label="Problem /\nEffect", size=18,
             backgroundColor="#ffffff")
els.append(poly([[0, 0], [spine_x1 - spine_x0, 0]], spine_x0, cy, g, arrow=True, end="arrow", strokeWidth=3))
dx, dy = 70, 120
for i, (top, bottom) in enumerate(zip(["People", "Machine", "Method"],
                                      ["Material", "Measurement", "Environment"])):
    bx = 220 + i * 200
    for sign, label in ((-1, top), (1, bottom)):
        els.append(poly([[0, 0], [-dx, sign * dy]], bx, cy, g))
        els.append(centered_text(bx - dx, cy + sign * (dy + 16), label, g, size=16))
        for t in (0.35, 0.7):                                        # sub-bones
            els.append(poly([[0, 0], [-50, 0]], bx - dx * t, cy + sign * dy * t, g, strokeWidth=1))
item("Fishbone (Ishikawa) diagram, 6M", els)

# --- 5 Whys ladder --------------------------------------------------------------------------------
g = nid()
els = []
bw, bh, x0, step = 260, 48, 90, 26
els += shape("rectangle", x0, 0, bw, bh, g, label="Problem statement", size=16, backgroundColor=GREY)
y = bh
for i in range(1, 6):
    els.append(poly([[0, 0], [0, step]], x0 + bw / 2, y, g, arrow=True, end="arrow"))
    els.append(centered_text(x0 - 48, y + step + bh / 2, f"Why {i}?", g, size=14))
    y += step
    els += shape("rectangle", x0, y, bw, bh, g, label="Because ...", size=16)
    y += bh
els.append(poly([[0, 0], [0, step]], x0 + bw / 2, y, g, arrow=True, end="arrow"))
y += step
els += shape("rectangle", x0, y, bw, bh, g, label="Root cause", size=16, backgroundColor=RED)
y += bh
els.append(poly([[0, 0], [0, step]], x0 + bw / 2, y, g, arrow=True, end="arrow"))
y += step
els += shape("rectangle", x0, y, bw, bh, g, label="Countermeasure", size=16, backgroundColor=GREEN)
item("5 Whys ladder", els)

# --- Pareto chart: counts on the left axis, cumulative % on the right -----------------------------
g = nid()
els = []
ox, oy, pw, ph = 70, 280, 380, 240
els.append(poly([[0, 0], [pw + 20, 0]], ox, oy, g, arrow=True, end="arrow"))
els.append(poly([[0, 0], [0, -(ph + 20)]], ox, oy, g, arrow=True, end="arrow"))
els.append(poly([[0, 0], [0, -ph]], ox + pw, oy, g))
counts = [200, 120, 80, 50, 30, 20]
total, bar_w, bar_gap, cum, line_pts = sum(counts), 42, 18, 0, []
for i, c in enumerate(counts):
    bx = ox + 15 + i * (bar_w + bar_gap)
    bar_h = ph * 0.85 * c / max(counts)
    els.append(base("rectangle", bx, oy - bar_h, bar_w, bar_h, g, backgroundColor=BLUE))
    els.append(centered_text(bx + bar_w / 2, oy + 14, "ABCDEF"[i], g, size=14))
    cum += c
    line_pts.append([bx + bar_w / 2, oy - ph * cum / total])
lx0, ly0 = line_pts[0]
els.append(poly([[px - lx0, py - ly0] for px, py in line_pts], lx0, ly0, g, strokeColor="#e03131"))
for px, py in line_pts:
    els.append(base("ellipse", px - 5, py - 5, 10, 10, g, roundness={"type": 2},
                    strokeColor="#e03131", backgroundColor="#e03131"))
els.append(poly([[0, 0], [pw, 0]], ox, oy - ph * 0.8, g, strokeStyle="dashed", strokeColor="#868e96", strokeWidth=1))
for pct, lab in ((1.0, "100%"), (0.8, "80%"), (0.5, "50%"), (0.0, "0%")):
    els.append(text(ox + pw + 8, oy - ph * pct - 9, lab, g, size=13, align="left"))
els.append(centered_text(ox + pw / 2, oy + 38, "Causes", g, size=14))
els.append(rotated_text(ox - 32, oy - ph / 2, "Count", g, size=14))
els.append(centered_text(ox + pw + 40, oy - ph - 26, "Cumulative %", g, size=13))
item("Pareto chart", els)

# --- SIPOC table ---------------------------------------------------------------------------------
g = nid()
els = []
cw, hh, rh, rows = 140, 44, 56, 3
for i, col in enumerate(["Suppliers", "Inputs", "Process", "Outputs", "Customers"]):
    els += shape("rectangle", i * cw, 0, cw, hh, g, label=col, size=16, backgroundColor=GREY)
    for rr in range(rows):
        els.append(base("rectangle", i * cw, hh + rr * rh, cw, rh, g))
item("SIPOC table", els)

# --- Control chart frame --------------------------------------------------------------------------
g = nid()
els = []
ox, oy, pw, ph = 50, 260, 400, 220
els.append(poly([[0, 0], [pw + 20, 0]], ox, oy, g, arrow=True, end="arrow"))
els.append(poly([[0, 0], [0, -(ph + 20)]], ox, oy, g, arrow=True, end="arrow"))
for lab, f, style, col in (("UCL", 0.85, "dashed", "#e03131"), ("CL", 0.5, "solid", STROKE),
                           ("LCL", 0.15, "dashed", "#e03131")):
    yy = oy - ph * f
    els.append(poly([[0, 0], [pw, 0]], ox, yy, g, strokeStyle=style, strokeColor=col, strokeWidth=1))
    els.append(text(ox + pw + 8, yy - 9, lab, g, size=13, align="left", color=col))
vals = [0.5, 0.58, 0.44, 0.62, 0.53, 0.4, 0.57, 0.66, 0.48, 0.55, 0.42, 0.6]
abs_pts = [[ox + 10 + i * (pw - 20) / (len(vals) - 1), oy - ph * v] for i, v in enumerate(vals)]
px0, py0 = abs_pts[0]
els.append(poly([[px - px0, py - py0] for px, py in abs_pts], px0, py0, g, strokeColor="#1971c2"))
for px, py in abs_pts:
    els.append(base("ellipse", px - 4, py - 4, 8, 8, g, roundness={"type": 2},
                    strokeColor="#1971c2", backgroundColor="#1971c2"))
els.append(centered_text(ox + pw / 2, oy + 22, "Sample", g, size=14))
els.append(rotated_text(ox - 26, oy - ph / 2, "Measurement", g, size=14))
item("Control chart", els)

# --- Impact / effort matrix -----------------------------------------------------------------------
g = nid()
els = []
s, ox, oy = 150, 50, 0
for col, row, lab, f in ((0, 0, "Quick wins", GREEN), (1, 0, "Major projects", BLUE),
                         (0, 1, "Fill-ins", YELLOW), (1, 1, "Thankless tasks", RED)):
    els += shape("rectangle", ox + col * s, oy + row * s, s, s, g, label=lab, size=16, backgroundColor=f)
els.append(poly([[0, 0], [2 * s, 0]], ox, oy + 2 * s + 10, g, arrow=True, end="arrow"))
els.append(centered_text(ox + s, oy + 2 * s + 30, "Effort", g, size=14))
els.append(poly([[0, 0], [0, -2 * s]], ox - 10, oy + 2 * s, g, arrow=True, end="arrow"))
els.append(rotated_text(ox - 30, oy + s, "Impact", g, size=14))
item("Impact / effort matrix", els)

# --- A3 problem-solving template ------------------------------------------------------------------
g = nid()
els = []
W = 840
els += shape("rectangle", 0, 0, W, 50, g, label="A3 title   |   Owner   |   Date", size=16, backgroundColor=GREY)
y = 50
for lab, hh in (("1. Background", 100), ("2. Current condition", 150),
                ("3. Goal / target", 90), ("4. Root cause analysis", 170)):
    els += shape("rectangle", 0, y, W / 2, hh, g, label=lab, size=14, align="left", valign="top")
    y += hh
y = 50
for lab, hh in (("5. Countermeasures", 170), ("6. Implementation plan", 170),
                ("7. Follow-up / results", 170)):
    els += shape("rectangle", W / 2, y, W / 2, hh, g, label=lab, size=14, align="left", valign="top")
    y += hh
item("A3 problem-solving template", els)

finish(sys.argv[1], "lean-six-sigma-charts", cols=3)
