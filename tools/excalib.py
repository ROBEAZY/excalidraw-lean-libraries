"""Small helper layer for generating Excalidraw libraries (.excalidrawlib v2)
and preview scenes (.excalidraw) from Python.

Element fields follow the Excalidraw element schema. Fields that are omitted
are filled with defaults by Excalidraw's restore step on load, but we write
the full set so the files look like what the app itself exports.
"""
import json, math, os, random, string, time

NOW = int(time.time() * 1000)
STROKE = "#1e1e1e"
FONT = 5          # Excalifont (hand-drawn default). 1 = legacy Virgil.
ITEMS = []        # (name, [elements]) in registration order


def seed(n):
    random.seed(n)


def nid(n=20):
    return "".join(random.choice(string.ascii_letters + string.digits + "_-") for _ in range(n))


def rint():
    return random.randint(1, 2_000_000_000)


def base(type_, x, y, w, h, group, **kw):
    el = {
        "id": nid(), "type": type_, "x": x, "y": y, "width": w, "height": h, "angle": 0,
        "strokeColor": STROKE, "backgroundColor": "transparent", "fillStyle": "solid",
        "strokeWidth": 2, "strokeStyle": "solid", "roughness": 1, "opacity": 100,
        "groupIds": [group] if group else [], "frameId": None, "roundness": None,
        "seed": rint(), "version": 1, "versionNonce": rint(), "isDeleted": False,
        "boundElements": [], "updated": NOW, "link": None, "locked": False,
    }
    el.update(kw)
    return el


def text_dims(txt, size):
    """Rough Excalifont metrics; Excalidraw re-measures on edit."""
    lines = txt.split("\n")
    w = max(len(l) for l in lines) * size * 0.52
    h = len(lines) * size * 1.25
    return w, h


def text(x, y, txt, group, size=20, align="center", valign="middle", container=None,
         color=STROKE, **kw):
    w, h = text_dims(txt, size)
    return base("text", x, y, w, h, group, strokeColor=color, text=txt, fontSize=size,
                fontFamily=FONT, textAlign=align, verticalAlign=valign, containerId=container,
                originalText=txt, autoResize=True, lineHeight=1.25, **kw)


def centered_text(cx, cy, txt, group, size=20, **kw):
    w, h = text_dims(txt, size)
    return text(cx - w / 2, cy - h / 2, txt, group, size=size, **kw)


def rotated_text(cx, cy, txt, group, size=14, angle=-math.pi / 2, **kw):
    """Text rotated about its centre (Excalidraw rotates around the element centre)."""
    t = centered_text(cx, cy, txt, group, size=size, **kw)
    t["angle"] = angle
    return t


def shape(type_, x, y, w, h, group, label=None, size=20, align="center", valign="middle",
          rounded=False, **kw):
    """rectangle / ellipse / diamond, optionally with bound text (edits in place)."""
    el = base(type_, x, y, w, h, group, **kw)
    if rounded:
        el["roundness"] = {"type": 3}
    if type_ == "ellipse":
        el["roundness"] = {"type": 2}
    out = [el]
    if label is not None:
        tw, th = text_dims(label, size)
        tx = x + 10 if align == "left" else x + (w - tw) / 2
        ty = y + 8 if valign == "top" else y + (h - th) / 2
        t = text(tx, ty, label, group, size=size, align=align, valign=valign, container=el["id"])
        el["boundElements"] = [{"type": "text", "id": t["id"]}]
        out.append(t)
    return out


def poly(points, x, y, group, closed=False, arrow=False, end=None, start=None, smooth=False, **kw):
    """line / arrow from points relative to (x, y); width/height = bounding box."""
    pts = [list(p) for p in points]
    if closed and pts[-1] != pts[0]:
        pts.append(list(pts[0]))
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    el = base("arrow" if arrow else "line", x, y, max(xs) - min(xs), max(ys) - min(ys), group,
              points=pts, lastCommittedPoint=None, startBinding=None, endBinding=None,
              startArrowhead=start, endArrowhead=end, **kw)
    if smooth:
        el["roundness"] = {"type": 2}
    if arrow:
        el["elbowed"] = False
    return el


def arc_point(cx, cy, radius, deg):
    """Point on a circle; degrees increase clockwise because y points down."""
    a = math.radians(deg)
    return [round(cx + radius * math.cos(a), 2), round(cy + radius * math.sin(a), 2)]


def frange(a, b, step):
    n = int(abs(b - a) / abs(step))
    return [a + i * step for i in range(n + 1)]


def item(name, elements):
    ITEMS.append((name, elements))


def bbox(els):
    xs = [e["x"] for e in els] + [e["x"] + e["width"] for e in els]
    ys = [e["y"] for e in els] + [e["y"] + e["height"] for e in els]
    return min(xs), min(ys), max(xs), max(ys)


def write_library(path):
    lib_items = [{"status": "unpublished", "elements": els, "id": nid(), "created": NOW, "name": name}
                 for name, els in ITEMS]
    lib = {"type": "excalidrawlib", "version": 2, "source": "https://excalidraw.com",
           "libraryItems": lib_items}
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(lib, f, indent=2)


def write_preview(path, cols):
    """Scene with every item in a grid plus grey captions (captions are not library content).
    Each row is as tall as its tallest item, so small items do not float in empty cells."""
    boxes = [bbox(els) for _, els in ITEMS]
    cell_w = max(b[2] - b[0] for b in boxes) + 80
    scene = []
    oy = 0
    for r0 in range(0, len(ITEMS), cols):
        row = list(zip(ITEMS[r0:r0 + cols], boxes[r0:r0 + cols]))
        row_h = max(b[3] - b[1] for _, b in row) + 70
        for ci, ((name, els), (minx, miny, maxx, maxy)) in enumerate(row):
            ox = ci * cell_w
            dx = ox + (cell_w - (maxx - minx)) / 2 - minx
            dy = oy + 20 - miny
            for e in els:
                c = json.loads(json.dumps(e))
                c["id"] += "s"
                c["x"] += dx
                c["y"] += dy
                if c.get("containerId"):
                    c["containerId"] += "s"
                if c.get("boundElements"):
                    c["boundElements"] = [{"type": b["type"], "id": b["id"] + "s"} for b in c["boundElements"]]
                scene.append(c)
            cap = text(0, oy + 20 + (maxy - miny) + 14, name, None, size=14, color="#868e96")
            cap["x"] = ox + (cell_w - cap["width"]) / 2
            scene.append(cap)
        oy += row_h
    doc = {"type": "excalidraw", "version": 2, "source": "https://excalidraw.com",
           "elements": scene, "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None},
           "files": {}}
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2)


def validate(path):
    d = json.load(open(path, encoding="utf-8"))
    assert d["type"] == "excalidrawlib" and d["version"] == 2
    names = [i["name"] for i in d["libraryItems"]]
    assert len(names) == len(set(names)), "duplicate item names"
    for it in d["libraryItems"]:
        groups = {tuple(e["groupIds"]) for e in it["elements"]}
        assert len(groups) == 1, (it["name"], groups)
        ids = {e["id"] for e in it["elements"]}
        for e in it["elements"]:
            if e.get("containerId"):
                assert e["containerId"] in ids, it["name"]
            for b in e.get("boundElements") or []:
                assert b["id"] in ids, it["name"]
    return len(d["libraryItems"]), sum(len(i["elements"]) for i in d["libraryItems"])


def finish(root, stem, cols):
    lib = os.path.join(root, "libraries", f"{stem}.excalidrawlib")
    prev = os.path.join(root, "previews", f"{stem}.excalidraw")
    write_library(lib)
    write_preview(prev, cols)
    n, m = validate(lib)
    print(f"{stem}: {n} items, {m} elements -> OK")
    for name, els in ITEMS:
        print(f"  - {name} ({len(els)} el)")
