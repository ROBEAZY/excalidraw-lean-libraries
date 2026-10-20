"""ASME flow process chart symbols and templates (method study / process analysis).

Usage: python tools/build_asme.py <repo_root>
Writes libraries/asme-flow-process-chart.excalidrawlib and previews/asme-flow-process-chart.excalidraw
"""
import sys
from excalib import *

seed(20261022)

GREY, LIGHT = "#868e96", "#e9ecef"
S = 48  # standalone symbol size


# --- symbol builders (origin at x, y; size s; optional label) ----------------------------------
def sym_operation(x, y, s, g, label=None, **kw):
    return shape("ellipse", x, y, s, s, g, label=label, size=max(10, int(s * 0.4)), **kw)


def sym_inspection(x, y, s, g, label=None, **kw):
    return shape("rectangle", x, y, s, s, g, label=label, size=max(10, int(s * 0.4)), **kw)


def sym_transport(x, y, s, g, **kw):
    shaft_top, shaft_bot, neck = s * 0.25, s * 0.75, s * 0.58
    pts = [[0, shaft_top], [neck, shaft_top], [neck, 0], [s, s / 2], [neck, s], [neck, shaft_bot], [0, shaft_bot]]
    return [poly(pts, x, y, g, closed=True, **kw)]


def sym_delay(x, y, s, g, **kw):
    pts = [[0, 0], [0, s]] + [arc_point(0, s / 2, s / 2, a) for a in frange(80, -80, -10)]
    return [poly(pts, x, y, g, closed=True, **kw)]


def sym_storage(x, y, s, g, **kw):
    return [poly([[0, 0], [s, 0], [s / 2, s]], x, y, g, closed=True, **kw)]


def sym_combined(x, y, s, g, **kw):
    inset = s * 0.17
    return [base("rectangle", x, y, s, s, g, **kw),
            base("ellipse", x + inset, y + inset, s - 2 * inset, s - 2 * inset, g, roundness={"type": 2}, **kw)]


SYMBOLS = [("Operation", sym_operation), ("Transport", sym_transport), ("Inspection", sym_inspection),
           ("Delay", sym_delay), ("Storage", sym_storage)]

# --- standalone symbols --------------------------------------------------------------------------
g = nid(); item("Operation", sym_operation(0, 0, S, g))
g = nid(); item("Operation, numbered", sym_operation(0, 0, S, g, label="1"))
g = nid(); item("Transport", sym_transport(0, 0, S, g))
g = nid(); item("Inspection", sym_inspection(0, 0, S, g))
g = nid(); item("Inspection, numbered", sym_inspection(0, 0, S, g, label="1"))
g = nid(); item("Delay", sym_delay(0, 0, S, g))
g = nid(); item("Storage", sym_storage(0, 0, S, g))
g = nid(); item("Combined operation and inspection", sym_combined(0, 0, S, g))

# --- legend: the five ASME symbols with names ----------------------------------------------------
g = nid()
els = []
for i, (name, fn) in enumerate(SYMBOLS + [("Operation +\ninspection", sym_combined)]):
    x = i * 110
    els += fn(x + 10, 0, 40, g)
    els.append(centered_text(x + 30, 60, name, g, size=13))
item("ASME symbol legend", els)

# --- flow process chart template -----------------------------------------------------------------
g = nid()
els = []
W = 740
els += shape("rectangle", 0, 0, W, 48, g, backgroundColor=LIGHT, size=14, align="left",
             label="Flow process chart  |  Process:            Method: present / proposed  |  Sheet:     Date:")
cols = [("No.", 40), ("Description", 220)] + [(s[0], 36) for s in SYMBOLS] + [("Dist.\n(m)", 70), ("Time\n(min)", 80), ("Remarks", 150)]
xs = [0]
for _, w in cols:
    xs.append(xs[-1] + w)
HDR, ROW, NROWS = 44, 34, 8
top, bottom = 48, 48 + HDR + NROWS * ROW
els.append(base("rectangle", 0, top, W, bottom - top, g))
for x in xs[1:-1]:
    els.append(poly([[0, 0], [0, bottom - top]], x, top, g, strokeWidth=1))
els.append(poly([[0, 0], [W, 0]], 0, top + HDR, g))
for r in range(1, NROWS):
    els.append(poly([[0, 0], [W, 0]], 0, top + HDR + r * ROW, g, strokeWidth=1, strokeColor=GREY))
for i, (name, w) in enumerate(cols):
    cx = xs[i] + w / 2
    if 2 <= i <= 6:
        els += SYMBOLS[i - 2][1](cx - 10, top + HDR / 2 - 10, 20, g)
    else:
        els.append(centered_text(cx, top + HDR / 2, name, g, size=12))
for r in range(NROWS):
    cy = top + HDR + r * ROW + ROW / 2
    els.append(centered_text(xs[0] + 20, cy, str(r + 1), g, size=12, color=GREY))
    for k, (_, fn) in enumerate(SYMBOLS):
        cx = xs[2 + k] + 18
        els += fn(cx - 8, cy - 8, 16, g, strokeColor=GREY, strokeWidth=1, roughness=0)
item("Flow process chart template", els)

# --- summary block: present vs proposed ------------------------------------------------------------
g = nid()
els = []
cols = [("", 50), ("Activity", 150), ("Present", 90), ("Proposed", 90), ("Saving", 90)]
xs = [0]
for _, w in cols:
    xs.append(xs[-1] + w)
W2 = xs[-1]
rows = [(n, fn) for n, fn in SYMBOLS] + [("Distance (m)", None), ("Time (min)", None)]
HDR, ROW = 36, 36
H2 = HDR + len(rows) * ROW
els += shape("rectangle", 0, 0, W2, HDR, g, backgroundColor=LIGHT, label="Summary", size=14, align="left")
els.append(base("rectangle", 0, HDR, W2, H2 - HDR, g))
for x in xs[1:-1]:
    els.append(poly([[0, 0], [0, H2 - HDR]], x, HDR, g, strokeWidth=1))
for r in range(1, len(rows)):
    els.append(poly([[0, 0], [W2, 0]], 0, HDR + r * ROW, g, strokeWidth=1, strokeColor=GREY))
for i, (name, w) in enumerate(cols[2:], start=2):
    els.append(centered_text(xs[i] + w / 2, HDR / 2, name, g, size=12))
for r, (name, fn) in enumerate(rows):
    cy = HDR + r * ROW + ROW / 2
    if fn:
        els += fn(xs[0] + 25 - 10, cy - 10, 20, g)
    els.append(text(xs[1] + 10, cy - 8.75, name, g, size=14, align="left"))
item("Flow process chart summary", els)

# --- operation process chart (OPC) column ---------------------------------------------------------
g = nid()
els = []
x0, y0 = 120, 0
els.append(poly([[0, 0], [0, 330]], x0 + 24, y0 + 20, g))                       # vertical flow line
els.append(poly([[0, 0], [100, 0]], x0 - 76, y0 + 20, g))                         # material entry
els.append(centered_text(x0 - 26, y0 + 6, "Material / part", g, size=12))
steps = [("1", sym_operation, "Operation description", "0.5 min"),
         ("2", sym_operation, "Operation description", "1.2 min"),
         ("1", sym_inspection, "Inspection", "0.3 min"),
         ("3", sym_operation, "Operation description", "0.8 min")]
for i, (num, fn, desc, t) in enumerate(steps):
    cy = y0 + 60 + i * 80
    els += fn(x0, cy, 48, g, label=num, backgroundColor="#ffffff")
    els.append(text(x0 + 64, cy + 6, desc, g, size=13, align="left"))
    els.append(text(x0 - 60, cy + 15, t, g, size=12, align="left", color=GREY))
item("Operation process chart column", els)

finish(sys.argv[1], "asme-flow-process-chart", cols=4)
