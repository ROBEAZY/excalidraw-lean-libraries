"""Lean workplace and visual management symbols.

Usage: python tools/build_lean.py <repo_root>
Writes libraries/lean-workplace.excalidrawlib and previews/lean-workplace.excalidraw
"""
import sys
from excalib import *

seed(20261023)

GREY, LIGHT = "#868e96", "#e9ecef"
RED, AMBER, GREEN, BLUE, YELLOW, PINK, ORANGE = "#ff8787", "#ffd43b", "#69db7c", "#a5d8ff", "#ffec99", "#fcc2d7", "#ffd8a8"


def sticky(x, y, g, label="Note", fill=YELLOW, size=110):
    return shape("rectangle", x, y, size, size, g, label=label, size=16, rounded=True, backgroundColor=fill)


def grid_table(x0, y0, cols, header_h, row_h, nrows, g, header_fill=LIGHT, header_size=12, row_labels=None):
    """Outlined table drawn with lines (cheap on elements). Returns (elements, xs, total_w, total_h)."""
    xs = [0]
    for _, w in cols:
        xs.append(xs[-1] + w)
    W = xs[-1]
    H = header_h + nrows * row_h
    els = [base("rectangle", x0, y0, W, header_h, g, backgroundColor=header_fill),
           base("rectangle", x0, y0, W, H, g)]
    for x in xs[1:-1]:
        els.append(poly([[0, 0], [0, H]], x0 + x, y0, g, strokeWidth=1))
    for r in range(1, nrows):
        els.append(poly([[0, 0], [W, 0]], x0, y0 + header_h + r * row_h, g, strokeWidth=1, strokeColor=GREY))
    for i, (name, w) in enumerate(cols):
        if name:
            els.append(centered_text(x0 + xs[i] + w / 2, y0 + header_h / 2, name, g, size=header_size))
    if row_labels:
        for r, lab in enumerate(row_labels):
            els.append(centered_text(x0 + cols[0][1] / 2, y0 + header_h + r * row_h + row_h / 2, lab, g, size=11, color=GREY))
    return els, xs, W, H


# --- Kanban board ------------------------------------------------------------------------------
g = nid()
els = []
cw, ch, hh = 190, 330, 40
for i, (name, fill) in enumerate((("To do", LIGHT), ("Doing  (WIP 3)", LIGHT), ("Done", LIGHT))):
    x = i * cw
    els += shape("rectangle", x, 0, cw, hh, g, label=name, size=15, backgroundColor=fill)
    els.append(base("rectangle", x, hh, cw, ch - hh, g))
els += sticky(20, hh + 15, g, "Task", YELLOW, 100)
els += sticky(50, hh + 95, g, "Task", PINK, 100)
els += sticky(cw + 45, hh + 15, g, "Task", BLUE, 100)
els += sticky(2 * cw + 45, hh + 15, g, "Task", GREEN, 100)
item("Kanban board", els)

g = nid(); item("Sticky note, yellow", sticky(0, 0, g, "Note", YELLOW))
g = nid(); item("Sticky note, pink", sticky(0, 0, g, "Note", PINK))
g = nid(); item("Sticky note, blue", sticky(0, 0, g, "Note", BLUE))

# --- Andon light stack ----------------------------------------------------------------------------
g = nid()
els = [base("rectangle", 14, 0, 40, 126, g, rounded=True, roundness={"type": 3}, backgroundColor="#ffffff")]
for i, fill in enumerate((RED, AMBER, GREEN)):
    els.append(base("ellipse", 18, 4 + i * 40, 32, 32, g, roundness={"type": 2}, backgroundColor=fill))
els.append(poly([[0, 0], [0, 40]], 34, 126, g, strokeWidth=3))
els.append(base("rectangle", 4, 166, 60, 10, g, backgroundColor=STROKE))
item("Andon light stack", els)

# --- 5S red tag -------------------------------------------------------------------------------------
g = nid()
els = [poly([[20, 0], [100, 0], [120, 20], [120, 200], [0, 200], [0, 20]], 0, 0, g, closed=True, backgroundColor="#ffc9c9")]
els.append(base("ellipse", 52, 8, 16, 16, g, roundness={"type": 2}, backgroundColor="#ffffff"))
els.append(centered_text(60, 44, "RED TAG", g, size=16, color="#c92a2a"))
for i, lab in enumerate(("Item:", "Reason:", "Date:", "Action:")):
    y = 70 + i * 32
    els.append(text(10, y, lab, g, size=12, align="left"))
    els.append(poly([[0, 0], [100, 0]], 10, y + 22, g, strokeWidth=1, strokeColor=GREY))
item("5S red tag", els)

# --- 5S cycle -----------------------------------------------------------------------------------------
g = nid()
els = []
bw, bh, gap = 112, 52, 34
steps = (("Sort", RED), ("Set in order", ORANGE), ("Shine", YELLOW), ("Standardize", GREEN), ("Sustain", BLUE))
for i, (name, fill) in enumerate(steps):
    x = i * (bw + gap)
    els += shape("rectangle", x, 0, bw, bh, g, label=name, size=14, rounded=True, backgroundColor=fill)
    if i < len(steps) - 1:
        els.append(poly([[0, 0], [gap - 6, 0]], x + bw + 3, bh / 2, g, arrow=True, end="arrow"))
total = len(steps) * bw + (len(steps) - 1) * gap
els.append(poly([[0, 0], [-total / 2 + bw / 2, 48], [-(total - bw), 0]], total - bw / 2, bh + 4, g,
                arrow=True, end="arrow", smooth=True, strokeColor=GREY))
item("5S cycle", els)

# --- RAG status indicators -------------------------------------------------------------------------------
g = nid()
els = []
for i, (fill, lab) in enumerate(((RED, "Behind"), (AMBER, "At risk"), (GREEN, "On track"))):
    els.append(base("ellipse", i * 90, 0, 30, 30, g, roundness={"type": 2}, backgroundColor=fill))
    els.append(centered_text(i * 90 + 15, 46, lab, g, size=13))
item("RAG status indicators", els)

# --- Spaghetti diagram paths ----------------------------------------------------------------------------
for name, col in (("Spaghetti path, red", "#e03131"), ("Spaghetti path, blue", "#1971c2")):
    g = nid()
    pts = [[0, 0], [80, -40], [150, 30], [70, 90], [190, 125], [250, 60]]
    els = [poly(pts, 10, 50, g, arrow=True, end="arrow", smooth=True, strokeColor=col)]
    els.append(base("ellipse", 4, 44, 12, 12, g, roundness={"type": 2}, strokeColor=col, backgroundColor=col))
    els.append(centered_text(0, 32, "Start", g, size=12, color=col))
    item(name, els)

g = nid()
els = shape("rectangle", 0, 0, 100, 60, g, label="WS 1", size=16)
els.append(base("ellipse", 43, 68, 14, 14, g, roundness={"type": 2}, backgroundColor=STROKE))
item("Workstation with operator position", els)

# --- Operator balance chart (takt vs cycle time) ----------------------------------------------------------
g = nid()
els = []
ox, oy, pw, ph = 60, 240, 340, 200
els.append(poly([[0, 0], [pw + 20, 0]], ox, oy, g, arrow=True, end="arrow"))
els.append(poly([[0, 0], [0, -(ph + 20)]], ox, oy, g, arrow=True, end="arrow"))
heights = [0.62, 0.9, 0.55, 0.78, 0.7]
bw, gap = 42, 22
for i, h in enumerate(heights):
    bx = ox + 18 + i * (bw + gap)
    els.append(base("rectangle", bx, oy - ph * h, bw, ph * h, g, backgroundColor=BLUE))
    els.append(centered_text(bx + bw / 2, oy + 14, f"Op {i + 1}", g, size=13))
els.append(poly([[0, 0], [pw, 0]], ox, oy - ph * 0.8, g, strokeStyle="dashed", strokeColor="#e03131"))
els.append(text(ox + pw + 6, oy - ph * 0.8 - 9, "Takt", g, size=13, align="left", color="#e03131"))
els.append(rotated_text(ox - 30, oy - ph / 2, "Cycle time (s)", g, size=13))
item("Operator balance chart (takt vs cycle time)", els)

# --- Standard work combination sheet -------------------------------------------------------------------------
g = nid()
cols = [("Step", 40), ("Work element", 200), ("Manual", 52), ("Auto", 52), ("Walk", 52), ("", 300)]
els, xs, W, H = grid_table(0, 48, cols, 44, 30, 6, g, row_labels=[str(i) for i in range(1, 7)])
els = shape("rectangle", 0, 0, W, 48, g, backgroundColor=LIGHT, size=14, align="left",
            label="Standard work combination sheet  |  Process:            Takt time:          Date:") + els
tx0 = xs[5]
for k in range(7):
    x = tx0 + k * 300 / 6
    els.append(poly([[0, 0], [0, 6]], x, 48 + 44 - 6, g, strokeWidth=1))
    els.append(centered_text(x, 48 + 16, str(k * 10), g, size=11))
    if 0 < k < 6:
        els.append(poly([[0, 0], [0, H - 44]], x, 48 + 44, g, strokeWidth=1, strokeColor=GREY, strokeStyle="dotted"))
els.append(text(tx0 + 4, 48 + 28, "time (s)", g, size=10, align="left", color=GREY))
els.append(text(0, 48 + H + 8, "—— manual     - - - auto     ~~~ walk", g, size=12, align="left", color=GREY))
item("Standard work combination sheet", els)

# --- Hour-by-hour production board -------------------------------------------------------------------------------
g = nid()
hours = [f"{h:02d}:00" for h in range(7, 15)]
cols = [("Hour", 70), ("Plan", 70), ("Actual", 70), ("Cum.", 70), ("Variance", 80), ("Comments / actions", 220)]
els, xs, W, H = grid_table(0, 48, cols, 40, 30, len(hours), g, row_labels=hours)
els = shape("rectangle", 0, 0, W, 48, g, backgroundColor=LIGHT, size=14, align="left",
            label="Hour-by-hour board  |  Line:            Date:            Target / hour:") + els
item("Hour-by-hour board", els)

# --- Safety cross (31 days) ------------------------------------------------------------------------------------------
g = nid()
els = []
cell = 26
cells = []
for r in range(7):
    for c in range(7):
        if 2 <= c <= 4 or 2 <= r <= 4:
            cells.append((r, c))
for n, (r, c) in enumerate(cells):
    label = str(n + 1) if n < 31 else None
    els += shape("rectangle", c * cell, 30 + r * cell, cell, cell, g, label=label, size=10, backgroundColor=GREEN)
els.append(centered_text(3.5 * cell, 12, "Days without incident", g, size=13))
item("Safety cross (31 days)", els)

finish(sys.argv[1], "lean-workplace", cols=4)
