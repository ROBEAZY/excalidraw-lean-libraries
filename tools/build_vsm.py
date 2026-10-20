"""Value Stream Mapping symbols (Rother & Shook, Learning to See conventions).

Usage: python tools/build_vsm.py <repo_root>
Writes libraries/value-stream-mapping.excalidrawlib and previews/value-stream-mapping.excalidraw
"""
import sys, math
from excalib import *

seed(20261020)

# --- Material / process flow ------------------------------------------------------------------
g = nid()
item("Process", shape("rectangle", 0, 0, 170, 70, g, label="Process", size=20))

g = nid()
els = shape("rectangle", 0, 0, 170, 60, g, label="Process", size=20)
els += shape("rectangle", 0, 60, 170, 130, g,
             label="C/T =\nC/O =\nUptime =\nShifts =\nEPE =", size=16, align="left")
item("Process with data box", els)

g = nid()
item("Data box", shape("rectangle", 0, 0, 170, 130, g,
                       label="C/T =\nC/O =\nUptime =\nShifts =\nEPE =", size=16, align="left"))

g = nid()
roof = [[0, 100], [0, 40], [30, 10], [30, 40], [60, 10], [60, 40], [90, 10], [90, 40],
        [120, 10], [120, 40], [150, 10], [150, 40], [180, 40], [180, 100]]
els = [poly(roof, 0, 0, g, closed=True)]
els.append(centered_text(90, 72, "Supplier /\nCustomer", g, size=16))
item("Outside source (supplier / customer)", els)

g = nid()
els = [poly([[0, 70], [40, 0], [80, 70]], 0, 0, g, closed=True)]
els.append(centered_text(40, 48, "I", g, size=24))
els.append(centered_text(40, 92, "300 pcs\n1.5 days", g, size=14))
item("Inventory", els)

g = nid()
els = [poly([[0, 70], [40, 0], [80, 70]], 0, 0, g, closed=True, fillStyle="hachure", backgroundColor=STROKE)]
els.append(centered_text(40, 92, "Safety\nstock", g, size=14))
item("Safety / buffer stock", els)

g = nid()
sm = [[100, 0], [0, 0], [0, 90], [100, 90], [0, 90], [0, 60], [100, 60], [0, 60], [0, 30], [100, 30]]
item("Supermarket", [poly(sm, 0, 0, g)])

g = nid()
els = [poly([[0, 0], [160, 0]], 0, 0, g), poly([[0, 0], [160, 0]], 0, 50, g)]
els.append(centered_text(60, 25, "FIFO", g, size=18))
els.append(poly([[0, 0], [45, 0]], 110, 25, g, arrow=True, end="arrow", strokeWidth=1))
item("FIFO lane", els)

g = nid()
pa = [[0, 15], [90, 15], [90, 0], [130, 30], [90, 60], [90, 45], [0, 45]]
item("Push arrow", [poly(pa, 0, 0, g, closed=True, fillStyle="hachure", backgroundColor=STROKE)])

g = nid()
item("Shipment arrow (to customer)", [poly(pa, 0, 0, g, closed=True, backgroundColor="#ffffff")])

g = nid()
els = [base("rectangle", 0, 10, 110, 60, g)]
els.append(poly([[0, 0], [0, 45], [30, 45], [30, 15], [20, 0]], 110, 25, g, closed=True))
els.append(base("ellipse", 15, 60, 24, 24, g, roundness={"type": 2}, backgroundColor="#ffffff"))
els.append(base("ellipse", 105, 60, 24, 24, g, roundness={"type": 2}, backgroundColor="#ffffff"))
els.append(centered_text(55, 40, "Daily", g, size=16))
item("Truck shipment", els)

g = nid()
els = [poly([[0, 0], [60, -45], [120, 0]], 0, 50, g, arrow=True, end="triangle", smooth=True)]
els.append(base("ellipse", -6, 44, 12, 12, g, roundness={"type": 2}, backgroundColor=STROKE))
item("Material pull (withdrawal)", els)

g = nid()
els = [base("ellipse", 0, 0, 36, 36, g, roundness={"type": 2}, backgroundColor=STROKE)]
els.append(poly([[0, 0], [0, 50]], 18, 36, g, arrow=True, end="arrow"))
item("Sequenced pull ball", els)

g = nid()
els = [base("ellipse", 15, 0, 20, 20, g, roundness={"type": 2})]
els.append(poly([[0, 30], [25, 0], [50, 30]], 0, 22, g, smooth=True))
els.append(poly([[0, 0], [50, 0]], 0, 52, g))
item("Operator", els)

g = nid()
els = [poly([[0, 0], [0, 90], [120, 90], [120, 0]], 0, 0, g)]
els.append(centered_text(60, 45, "Cell", g, size=16))
item("Work cell", els)

# --- Information flow ---------------------------------------------------------------------------
g = nid()
item("Manual information arrow", [poly([[0, 0], [150, 0]], 0, 0, g, arrow=True, end="arrow")])

g = nid()
zz = [[0, 0], [55, 0], [70, -18], [85, 18], [100, 0], [150, 0]]
item("Electronic information arrow", [poly(zz, 0, 20, g, arrow=True, end="arrow")])

g = nid()
item("Kanban path (dashed)", [poly([[0, 0], [150, 0]], 0, 0, g, arrow=True, end="arrow", strokeStyle="dashed")])

g = nid()
item("Production control", shape("rectangle", 0, 0, 170, 70, g, label="Production\nControl", size=18))

g = nid()
item("Schedule", shape("rectangle", 0, 0, 120, 60, g, label="Daily\nschedule", size=16))

card = [[0, 0], [80, 0], [100, 20], [100, 60], [0, 60]]
g = nid()
els = [poly(card, 0, 0, g, closed=True, backgroundColor="#ffffff")]
els.append(centered_text(50, 32, "P", g, size=18))
item("Production kanban", els)

g = nid()
els = [poly(card, 0, 0, g, closed=True, fillStyle="hachure", backgroundColor=STROKE)]
els.append(centered_text(50, 32, "W", g, size=18, color="#ffffff"))
item("Withdrawal kanban", els)

g = nid()
els = [poly([[0, 0], [80, 0], [40, 60]], 0, 0, g, closed=True, backgroundColor="#ffffff")]
els.append(centered_text(40, 20, "S", g, size=18))
item("Signal kanban", els)

g = nid()
els = [poly(card, i * 12, (2 - i) * 10, g, closed=True, backgroundColor="#ffffff") for i in range(3)]
item("Kanban arriving in batches", els)

g = nid()
els = [poly([[0, 0], [0, 110]], 50, 0, g, strokeWidth=3)]
els.append(base("rectangle", 20, 0, 60, 30, g, backgroundColor="#ffffff"))
els.append(base("rectangle", 20, 40, 60, 30, g, backgroundColor="#ffffff"))
item("Kanban post", els)

g = nid()
item("Load levelling (heijunka) box", shape("rectangle", 0, 0, 120, 50, g, label="OXOX", size=20))

g = nid()
els = [base("ellipse", 0, 0, 44, 30, g, roundness={"type": 2}),
       base("ellipse", 56, 0, 44, 30, g, roundness={"type": 2}),
       poly([[0, 0], [12, 0]], 44, 15, g),
       poly([[0, 0], [-15, -8]], 0, 15, g),
       poly([[0, 0], [15, -8]], 100, 15, g)]
item("Go-see scheduling", els)

# --- General -----------------------------------------------------------------------------------
g = nid()
pts = []
cx, cy, R, r, n = 80, 55, 80, 55, 14
for i in range(2 * n):
    a = math.pi * i / n - math.pi / 2
    rad = R if i % 2 == 0 else r
    pts.append([round(cx + rad * math.cos(a), 2), round(cy + rad * math.sin(a) * 0.7, 2)])
els = [poly(pts, 0, 0, g, closed=True, backgroundColor="#ffec99", strokeColor="#e8590c")]
els.append(centered_text(cx, cy, "Kaizen", g, size=20, color="#e8590c"))
item("Kaizen burst", els)

g = nid()
els = [poly([[0, 0], [120, 0], [120, 40], [240, 40], [240, 0]], 0, 20, g)]
els.append(centered_text(60, 8, "2 days", g, size=14))
els.append(centered_text(180, 74, "45 sec", g, size=14))
item("Timeline segment", els)

g = nid()
item("Timeline totals", shape("rectangle", 0, 0, 190, 70, g,
                             label="Lead time = 12 days\nVA time = 180 sec", size=15, align="left"))

finish(sys.argv[1], "value-stream-mapping", cols=6)
