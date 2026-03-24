#!/usr/bin/env python3
"""
Generate a 4K knowledge tree PNG from skills/ folder structure.
Colors are defined per-domain in skills/<domain>/_meta.yml.

Requirements: pip install pillow pyyaml
Usage:        python tools/build_tree_image.py
"""

import re, math, colorsys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import yaml

# ── paths ─────────────────────────────────────────────────────────────────────
REPO   = Path(__file__).parent.parent
SKILLS = REPO / "skills"
ASSETS = REPO / "assets"
OUT    = ASSETS / "knowledge-tree.png"
README = REPO / "readme.md"

FONT   = "/System/Library/Fonts/HelveticaNeue.ttc"
EMOJIF = "/System/Library/Fonts/Apple Color Emoji.ttc"
EMOJI_VALID = [20, 32, 40, 48, 64, 96, 160]

# ── output ────────────────────────────────────────────────────────────────────
OUT_W, OUT_H = 3840, 2160        # final 4K
AA = 2                            # anti-alias supersample
RW, RH = OUT_W * AA, OUT_H * AA  # render canvas

# ── dark palette ──────────────────────────────────────────────────────────────
BG_TOP  = (10, 14, 24)
BG_BOT  = (18, 22, 38)
LINE_A  = 180                     # line alpha
SHADOW  = (0, 0, 0, 50)

NATURAL_GROUPS = {"physics", "biology", "chemistry", "neuroscience"}
FORMAL_GROUPS  = {"mathematics", "computer-science"}

# ── helpers ───────────────────────────────────────────────────────────────────
def hsl(h, s, l):
    r, g, b = colorsys.hls_to_rgb((h % 360) / 360, l, s)
    return (int(r * 255), int(g * 255), int(b * 255))

def font(size):
    try:    return ImageFont.truetype(FONT, size)
    except: return ImageFont.load_default()

def emoji_font(size):
    s = min(EMOJI_VALID, key=lambda v: abs(v - size))
    try:    return ImageFont.truetype(EMOJIF, s)
    except: return font(size)

def tsize(f, t):
    b = f.getbbox(t); return b[2] - b[0], b[3] - b[1]

# ── color from hue ────────────────────────────────────────────────────────────
def make_palette(hue):
    """Build a full colour set from a single hue (0-360)."""
    return dict(
        fill   = hsl(hue, 0.68, 0.50),
        border = hsl(hue, 0.75, 0.58),
        glow   = hsl(hue, 0.80, 0.55),
        text   = (255, 255, 255),
        sub_fill   = hsl(hue, 0.35, 0.20),
        sub_border = hsl(hue, 0.55, 0.40),
        sub_text   = hsl(hue, 0.25, 0.82),
    )

# ── scan & meta ───────────────────────────────────────────────────────────────
def read_meta(domain_path):
    meta_f = domain_path / "_meta.yml"
    if meta_f.exists():
        return yaml.safe_load(meta_f.read_text())
    return {}

def scan():
    """Return {domain: {meta, subs: [str]}} sorted by order."""
    raw = {}
    for d in SKILLS.iterdir():
        if d.is_dir() and not d.name.startswith("_"):
            meta = read_meta(d)
            subs = sorted(s.name for s in d.iterdir()
                          if s.is_dir() and not s.name.startswith("_"))
            raw[d.name] = {"meta": meta, "subs": subs}
    return dict(sorted(raw.items(), key=lambda kv: kv[1]["meta"].get("order", 99)))

# ── tree ──────────────────────────────────────────────────────────────────────
class N:
    """Tree node."""
    __slots__ = "key emoji label kind domain hue pal children x y span".split()
    def __init__(self, key, emoji, label, kind, domain=None, hue=0):
        self.key=key; self.emoji=emoji; self.label=label
        self.kind=kind; self.domain=domain; self.hue=hue
        self.pal=make_palette(hue)
        self.children=[]; self.x=self.y=self.span=0.0

def fmt(name):
    return name.replace("-", " ").title()

def build(data):
    root = N("root", "🌍", "OpenScientist", "root", hue=220)

    # group into natural / formal / other
    groups = {"natural": [], "formal": [], "other": []}
    for dom, info in data.items():
        g = info["meta"].get("group", "other")
        groups.setdefault(g, []).append((dom, info))

    def add_domains(parent, domains):
        for dom, info in domains:
            m   = info["meta"]
            hue = m.get("hue", 0)
            e   = m.get("emoji", "◉")
            dn  = N(dom, e, fmt(dom), "domain", domain=dom, hue=hue)
            parent.children.append(dn)
            subs = info["subs"]
            ns   = len(subs)
            spread = min(30, 60 / max(ns, 1))
            for i, sub in enumerate(subs):
                sh = hue + (i - (ns - 1) / 2) * spread / max(ns - 1, 1) if ns > 1 else hue
                dn.children.append(N(f"{dom}/{sub}", "", fmt(sub), "sub", domain=dom, hue=sh))

    if groups["natural"]:
        # average hue of children for group colour
        avg_h = sum(d[1]["meta"].get("hue", 0) for d in groups["natural"]) // len(groups["natural"])
        gn = N("natural", "🔬", "Natural Sciences", "group", hue=avg_h)
        root.children.append(gn)
        add_domains(gn, groups["natural"])

    if groups["formal"]:
        avg_h = sum(d[1]["meta"].get("hue", 0) for d in groups["formal"]) // len(groups["formal"])
        gn = N("formal", "📐", "Formal Sciences", "group", hue=avg_h)
        root.children.append(gn)
        add_domains(gn, groups["formal"])

    if groups["other"]:
        add_domains(root, groups["other"])

    return root

# ── layout ────────────────────────────────────────────────────────────────────
def comp_span(n):
    if not n.children: n.span = 1.0; return
    for c in n.children: comp_span(c)
    n.span = sum(c.span for c in n.children)

def layout(n, xl, depth, ys):
    n.y = depth * ys
    if not n.children:
        n.x = xl + n.span / 2; return
    cur = xl
    for c in n.children:
        layout(c, cur, depth + 1, ys); cur += c.span
    n.x = xl + n.span / 2

def tree_depth(n, d=0):
    return d if not n.children else max(tree_depth(c, d + 1) for c in n.children)

# ── drawing ───────────────────────────────────────────────────────────────────
def gradient_bg(w, h, top, bot):
    img = Image.new("RGBA", (w, h))
    for y in range(h):
        t = y / h
        c = tuple(int(top[i] * (1 - t) + bot[i] * t) for i in range(3)) + (255,)
        img.paste(c, (0, y, w, y + 1))
    return img

def gradient_fill(img, x0, y0, x1, y1, ct, cb, r):
    """Vertical gradient rounded rect composited onto img."""
    w, h = x1 - x0, y1 - y0
    if w <= 0 or h <= 0: return
    strip = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sd = ImageDraw.Draw(strip)
    for row in range(h):
        t = row / max(h - 1, 1)
        c = tuple(int(ct[i] * (1 - t) + cb[i] * t) for i in range(3)) + (255,)
        sd.line([(0, row), (w, row)], fill=c)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=255)
    strip.putalpha(mask)
    img.paste(strip, (x0, y0), strip)

def draw_node(img, draw, n, cx, cy, A):
    """Draw a single node. Returns (x0, y0, x1, y1)."""
    p = n.pal

    if n.kind == "root":
        fs = 56 * A; px = 50 * A; py = 28 * A; r = 22 * A
        ct = (230, 235, 250); cb = (200, 210, 235)
        border = (150, 170, 220); tc = (15, 20, 40); bw = 0
    elif n.kind == "group":
        fs = 42 * A; px = 38 * A; py = 22 * A; r = 18 * A
        ct = (p["fill"][0] // 4 + 10, p["fill"][1] // 4 + 10, p["fill"][2] // 4 + 10)
        cb = (ct[0] - 8, ct[1] - 8, ct[2] - 8)
        border = p["glow"]; tc = (220, 225, 240); bw = 3 * A
    elif n.kind == "domain":
        fs = 36 * A; px = 32 * A; py = 18 * A; r = 14 * A
        ct = tuple(min(255, c + 25) for c in p["fill"])
        cb = p["fill"]
        border = p["border"]; tc = p["text"]; bw = 3 * A
    else:  # sub
        fs = 30 * A; px = 26 * A; py = 14 * A; r = 12 * A
        ct = tuple(min(255, c + 10) for c in p["sub_fill"])
        cb = p["sub_fill"]
        border = p["sub_border"]; tc = p["sub_text"]; bw = 2 * A

    ft = font(fs); fe = emoji_font(fs)
    lines = n.label.split("\n")
    lh = max(tsize(ft, l)[1] for l in lines)
    tw = max(tsize(ft, l)[0] for l in lines)
    th = lh * len(lines) + 6 * A * (len(lines) - 1)

    ew = 0
    if n.emoji:
        eb = fe.getbbox(n.emoji)
        ew = (eb[2] - eb[0]) + 12 * A

    w = ew + tw + px * 2
    h = th + py * 2
    x0, y0 = cx - w // 2, cy - h // 2
    x1, y1 = cx + w // 2, cy + h // 2

    # shadow
    draw.rounded_rectangle([x0 + 6 * A, y0 + 6 * A, x1 + 6 * A, y1 + 6 * A],
                            radius=r, fill=SHADOW)

    # gradient fill
    gradient_fill(img, x0, y0, x1, y1, ct, cb, r)

    # border
    if bw:
        draw.rounded_rectangle([x0, y0, x1, y1], radius=r,
                                outline=border, width=bw)

    # emoji
    if n.emoji:
        ey = y0 + py + (th - lh) // 2
        draw.text((x0 + px, ey), n.emoji, font=fe, fill=tc, embedded_color=True)

    # text
    tx = x0 + px + ew; ty = y0 + py
    for i, line in enumerate(lines):
        draw.text((tx, ty + i * (lh + 6 * A)), line, font=ft, fill=tc)

    return x0, y0, x1, y1

def compute_bounds(n, ox, oy, spx, A, bounds):
    """Pass 1: compute and store bounding boxes for every node."""
    cx = int(n.x * spx) + ox
    cy = int(n.y) + oy
    p = n.pal

    if n.kind == "root":
        fs = 56 * A; px = 50 * A; py = 28 * A
    elif n.kind == "group":
        fs = 42 * A; px = 38 * A; py = 22 * A
    elif n.kind == "domain":
        fs = 36 * A; px = 32 * A; py = 18 * A
    else:
        fs = 30 * A; px = 26 * A; py = 14 * A

    ft = font(fs); fe = emoji_font(fs)
    lines = n.label.split("\n")
    lh = max(tsize(ft, l)[1] for l in lines)
    tw = max(tsize(ft, l)[0] for l in lines)
    th = lh * len(lines) + 6 * A * (len(lines) - 1)

    ew = 0
    if n.emoji:
        eb = fe.getbbox(n.emoji)
        ew = (eb[2] - eb[0]) + 12 * A

    w = ew + tw + px * 2
    h = th + py * 2
    x0, y0 = cx - w // 2, cy - h // 2
    x1, y1 = cx + w // 2, cy + h // 2
    bounds[id(n)] = (x0, y0, x1, y1, cx, cy)

    for c in n.children:
        compute_bounds(c, ox, oy, spx, A, bounds)

def draw_connectors(draw, n, ox, oy, spx, A, bounds):
    """Pass 2: draw all connector lines using precomputed bounds."""
    if not n.children:
        return

    _, _, _, y1, cx, _ = bounds[id(n)]
    gap = 20 * A
    bus_y = y1 + gap
    lw = max(2, 3 * A)
    p_col = n.pal["glow"] + (LINE_A,)

    child_data = []
    for c in n.children:
        c_x0, c_y0, c_x1, c_y1, ccx, ccy = bounds[id(c)]
        child_data.append((c, ccx, c_y0))

    # parent stem down
    draw.line([(cx, y1), (cx, bus_y)], fill=p_col, width=lw)

    # horizontal bus
    xs = [cd[1] for cd in child_data]
    draw.line([(min(xs), bus_y), (max(xs), bus_y)], fill=p_col, width=lw)

    # child stems down to each child's actual top
    for c, ccx, c_y0 in child_data:
        c_col = c.pal["glow"] + (LINE_A,)
        draw.line([(ccx, bus_y), (ccx, c_y0)], fill=c_col, width=lw)

    # recurse
    for c in n.children:
        draw_connectors(draw, c, ox, oy, spx, A, bounds)

def draw_nodes(img, draw, n, ox, oy, spx, A, bounds):
    """Pass 3: draw all nodes on top of connectors."""
    cx = int(n.x * spx) + ox
    cy = int(n.y) + oy
    draw_node(img, draw, n, cx, cy, A)
    for c in n.children:
        draw_nodes(img, draw, c, ox, oy, spx, A, bounds)

# ── main ──────────────────────────────────────────────────────────────────────
def main():
    ASSETS.mkdir(exist_ok=True)
    data = scan()
    root = build(data)
    comp_span(root)
    depth = tree_depth(root)

    A     = AA
    YS    = 420 * A
    MX    = 240 * A
    MY    = 180 * A

    layout(root, 0, 0, YS)

    SPAN_PX = (RW - MX * 2) / root.span  # pixels per span unit
    H = depth * YS + MY * 2 + 80 * A

    img  = gradient_bg(RW, H, BG_TOP, BG_BOT)
    draw = ImageDraw.Draw(img)

    # subtle grid dots
    for gx in range(0, RW, 60 * A):
        for gy in range(0, H, 60 * A):
            draw.ellipse([gx - 1, gy - 1, gx + 1, gy + 1], fill=(40, 50, 80, 50))

    OX = MX
    OY = MY + 60 * A

    bounds = {}
    compute_bounds(root, OX, OY, SPAN_PX, A, bounds)
    draw_connectors(draw, root, OX, OY, SPAN_PX, A, bounds)
    draw_nodes(img, draw, root, OX, OY, SPAN_PX, A, bounds)

    # title
    tf = font(34 * A)
    title = "OpenScientist — Knowledge Tree"
    tw, _ = tsize(tf, title)
    draw.text(((RW - tw) // 2, 28 * A), title, font=tf, fill=(120, 140, 180, 200))

    # downscale
    final_w, final_h = RW // A, H // A
    final = img.resize((final_w, final_h), Image.LANCZOS).convert("RGB")
    final.save(OUT, dpi=(220, 220))
    print(f"Saved {OUT}  ({final_w}×{final_h}px)")

    # patch README
    txt = README.read_text()
    tag = "![Knowledge Tree](assets/knowledge-tree.png)\n"
    pat = re.compile(r"```mermaid\ngraph TD.*?```\n?", re.DOTALL)
    if pat.search(txt):
        README.write_text(pat.sub(tag, txt, count=1))
    elif "![Knowledge Tree]" in txt:
        README.write_text(re.sub(r"!\[Knowledge Tree\]\([^)]+\)", tag.strip(), txt))
    print("Updated README")

if __name__ == "__main__":
    main()
