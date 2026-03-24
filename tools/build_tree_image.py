#!/usr/bin/env python3
"""
Scan skills/ folder structure, draw a knowledge-tree PNG with full emoji
support using Pillow + Apple Color Emoji, save to assets/knowledge-tree.png,
and update the image tag in readme.md.

Requirements: pip install pillow   (already satisfies matplotlib users too)
Usage:        python tools/build_tree_image.py
"""

import re, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ── paths ─────────────────────────────────────────────────────────────────────
REPO_ROOT  = Path(__file__).parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
ASSETS_DIR = REPO_ROOT / "assets"
OUTPUT_PNG = ASSETS_DIR / "knowledge-tree.png"
README     = REPO_ROOT / "readme.md"

# ── font paths (macOS) ────────────────────────────────────────────────────────
FONT_REGULAR = "/System/Library/Fonts/HelveticaNeue.ttc"
FONT_BOLD    = "/System/Library/Fonts/HelveticaNeue.ttc"
FONT_EMOJI   = "/System/Library/Fonts/Apple Color Emoji.ttc"

# ── domain metadata ───────────────────────────────────────────────────────────
DOMAIN_EMOJI = {
    "physics":          "⚛️",
    "biology":          "🧬",
    "chemistry":        "⚗️",
    "mathematics":      "➗",
    "neuroscience":     "🧠",
    "computer-science": "💻",
    "cross-domain":     "🔀",
}
NATURAL = {"physics", "biology", "chemistry", "neuroscience"}
FORMAL  = {"mathematics", "computer-science"}

# ── colours ───────────────────────────────────────────────────────────────────
BG          = "#F6F8FA"
LINE_COL    = "#ADC8E6"
ROOT_FILL   = "#0D2137";  ROOT_TEXT   = "#FFFFFF"
GROUP_FILL  = "#174D7A";  GROUP_TEXT  = "#FFFFFF"
DOM_FILL    = "#2A7EC8";  DOM_TEXT    = "#FFFFFF"
SUB_FILL    = "#FFFFFF";  SUB_TEXT    = "#1B3A6B";  SUB_EDGE = "#ADC8E6"
TITLE_COL   = "#5A7A9A"

def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

# ── tree node ─────────────────────────────────────────────────────────────────
class Node:
    def __init__(self, key, emoji, label, kind):
        self.key      = key
        self.emoji    = emoji   # may be "" for groups/root
        self.label    = label
        self.kind     = kind    # root | group | domain | subdomain
        self.children = []
        self.x = self.y = 0.0
        self._span    = 0.0

# ── scan ──────────────────────────────────────────────────────────────────────
def scan():
    tree = {}
    for d in sorted(SKILLS_DIR.iterdir()):
        if d.is_dir() and not d.name.startswith("_"):
            tree[d.name] = sorted(
                s.name for s in d.iterdir()
                if s.is_dir() and not s.name.startswith("_"))
    return tree

def fmt(name):
    words = name.replace("-", " ").title().split()
    if len(words) > 2:
        mid = math.ceil(len(words) / 2)
        return " ".join(words[:mid]) + "\n" + " ".join(words[mid:])
    return " ".join(words)

def build_tree(data):
    root = Node("root", "🌍", "OpenScientist", "root")

    nat_d  = [d for d in data if d in NATURAL]
    form_d = [d for d in data if d in FORMAL]
    other  = [d for d in data if d not in NATURAL and d not in FORMAL]

    def add_domain(parent, domain):
        e = DOMAIN_EMOJI.get(domain, "◉")
        n = Node(domain, e, fmt(domain), "domain")
        parent.children.append(n)
        for sub in data.get(domain, []):
            n.children.append(Node(f"{domain}/{sub}", "", fmt(sub), "subdomain"))

    if nat_d:
        nat = Node("natural", "🔬", "Natural Sciences", "group")
        root.children.append(nat)
        for d in nat_d: add_domain(nat, d)

    if form_d:
        frm = Node("formal", "📐", "Formal Sciences", "group")
        root.children.append(frm)
        for d in form_d: add_domain(frm, d)

    for d in other: add_domain(root, d)
    return root

# ── layout ────────────────────────────────────────────────────────────────────
UNIT = 1.0

def compute_span(n):
    if not n.children: n._span = UNIT; return
    for c in n.children: compute_span(c)
    n._span = sum(c._span for c in n.children)

def assign_xy(n, x_left, depth, y_step):
    n.y = depth * y_step
    if not n.children:
        n.x = x_left + n._span / 2; return
    cur = x_left
    for c in n.children:
        assign_xy(c, cur, depth + 1, y_step); cur += c._span
    n.x = x_left + n._span / 2

def max_depth(n, d=0):
    return d if not n.children else max(max_depth(c, d+1) for c in n.children)

# ── drawing helpers ───────────────────────────────────────────────────────────
def rounded_rect(draw, x0, y0, x1, y1, r, fill, outline=None, lw=0):
    draw.rounded_rectangle([x0, y0, x1, y1], radius=r,
                            fill=hex2rgb(fill),
                            outline=hex2rgb(outline) if outline else None,
                            width=lw)

_EMOJI_VALID = [20, 32, 40, 48, 64, 96, 160]

def _nearest_emoji_size(size):
    return min(_EMOJI_VALID, key=lambda s: abs(s - size))

def get_fonts(size_text, size_emoji):
    try:
        ft = ImageFont.truetype(FONT_BOLD, size_text)
    except Exception:
        ft = ImageFont.load_default()
    try:
        fe = ImageFont.truetype(FONT_EMOJI, _nearest_emoji_size(size_emoji))
    except Exception:
        fe = ft
    return ft, fe

# ── node dimensions (in pixels) ───────────────────────────────────────────────
NODE_SPEC = {
    "root":      dict(fill=ROOT_FILL,  text=ROOT_TEXT,  size=22, pad_x=32, pad_y=14, r=14),
    "group":     dict(fill=GROUP_FILL, text=GROUP_TEXT, size=18, pad_x=26, pad_y=11, r=12),
    "domain":    dict(fill=DOM_FILL,   text=DOM_TEXT,   size=16, pad_x=22, pad_y=10, r=10),
    "subdomain": dict(fill=SUB_FILL,   text=SUB_TEXT,   size=14, pad_x=18, pad_y=8,  r=8,
                      outline=SUB_EDGE, lw=2),
}

def measure_node(n, scale):
    sp = NODE_SPEC[n.kind]
    ft, _ = get_fonts(sp["size"], sp["size"])
    # measure text block
    lines  = n.label.split("\n")
    bbox   = [ft.getbbox(l) for l in lines]
    tw     = max(b[2]-b[0] for b in bbox)
    th_sum = sum(b[3]-b[1] for b in bbox) + (len(lines)-1)*4
    # emoji prefix width
    ew = 0
    if n.emoji:
        _, fe = get_fonts(sp["size"], sp["size"])
        eb = fe.getbbox(n.emoji + " ")
        ew = eb[2] - eb[0]
    w = ew + tw + sp["pad_x"]*2
    h = th_sum + sp["pad_y"]*2
    return int(w), int(h)

def draw_node_pil(draw, n, cx, cy, scale):
    sp  = NODE_SPEC[n.kind]
    ft, fe = get_fonts(sp["size"], sp["size"])
    lines = n.label.split("\n")

    # measure
    bboxes = [ft.getbbox(l) for l in lines]
    tw = max(b[2]-b[0] for b in bboxes)
    lh = max(b[3]-b[1] for b in bboxes)
    th = lh * len(lines) + 4 * (len(lines)-1)

    ew = 0
    if n.emoji:
        eb = fe.getbbox(n.emoji)
        ew = (eb[2]-eb[0]) + 8

    total_w = ew + tw + sp["pad_x"]*2
    total_h = th + sp["pad_y"]*2

    x0, y0 = cx - total_w//2, cy - total_h//2
    x1, y1 = cx + total_w//2, cy + total_h//2

    # box
    outline = sp.get("outline"); lw = sp.get("lw", 0)
    draw.rounded_rectangle(
        [x0, y0, x1, y1], radius=sp["r"],
        fill=hex2rgb(sp["fill"]),
        outline=hex2rgb(outline) if outline else None, width=lw,
    )

    # text
    text_x = x0 + sp["pad_x"] + ew
    text_y = y0 + sp["pad_y"]
    tc = hex2rgb(sp["text"])
    for i, (line, bb) in enumerate(zip(lines, bboxes)):
        draw.text((text_x, text_y + i*(lh+4)), line, font=ft, fill=tc)

    # emoji
    if n.emoji:
        draw.text((x0 + sp["pad_x"], y0 + sp["pad_y"]), n.emoji,
                  font=fe, fill=hex2rgb(sp["text"]),
                  embedded_color=True)

    return x0, y0, x1, y1, total_w, total_h

# ── recursive draw ────────────────────────────────────────────────────────────
def draw_tree_pil(draw, n, ox, oy, scale, parent_bottom=None):
    px = int(n.x * scale) + ox
    py = int(n.y * scale) + oy

    x0, y0, x1, y1, w, h = draw_node_pil(draw, n, px, py, scale)

    lc = hex2rgb(LINE_COL)
    if parent_bottom is not None:
        draw.line([(px, y0), (px, parent_bottom)], fill=lc, width=2)

    if n.children:
        bus_y = y1 + 18
        draw.line([(px, y1), (px, bus_y)], fill=lc, width=2)
        child_xs = [int(c.x * scale) + ox for c in n.children]
        draw.line([(min(child_xs), bus_y), (max(child_xs), bus_y)], fill=lc, width=2)
        for c in n.children:
            draw_tree_pil(draw, c, ox, oy, scale, parent_bottom=bus_y)

# ── main ──────────────────────────────────────────────────────────────────────
def main():
    ASSETS_DIR.mkdir(exist_ok=True)

    data  = scan()
    root  = build_tree(data)
    compute_span(root)

    depth  = max_depth(root)
    Y_STEP = 130
    SCALE  = 180
    MARGIN = 60

    assign_xy(root, 0, 0, Y_STEP / SCALE)

    img_w = int(root._span * SCALE) + MARGIN * 2
    img_h = int((depth + 1) * Y_STEP) + MARGIN * 2 + 50  # +50 for title

    img  = Image.new("RGBA", (img_w, img_h), hex2rgb(BG) + (255,))
    draw = ImageDraw.Draw(img)

    # title
    try:
        tf = ImageFont.truetype(FONT_REGULAR, 20)
    except Exception:
        tf = ImageFont.load_default()
    title = "OpenScientist — Knowledge Tree"
    tb = tf.getbbox(title)
    draw.text(((img_w - (tb[2]-tb[0]))//2, 18), title,
              font=tf, fill=hex2rgb(TITLE_COL))

    OX = MARGIN
    OY = MARGIN + 40

    draw_tree_pil(draw, root, OX, OY, SCALE)

    img.convert("RGB").save(OUTPUT_PNG, dpi=(160, 160))
    print(f"Saved: {OUTPUT_PNG}")

    # ── patch README ──────────────────────────────────────────────────────────
    text    = README.read_text(encoding="utf-8")
    img_tag = "![Knowledge Tree](assets/knowledge-tree.png)\n"

    mermaid = re.compile(r"```mermaid\ngraph TD.*?```\n?", re.DOTALL)
    if mermaid.search(text):
        new_text = mermaid.sub(img_tag, text, count=1)
    elif "![Knowledge Tree]" in text:
        new_text = re.sub(r"!\[Knowledge Tree\]\([^)]+\)", img_tag.strip(), text)
    else:
        print("Warning: no block to replace in README — add manually.")
        return

    README.write_text(new_text, encoding="utf-8")
    print(f"Updated: {README}")


if __name__ == "__main__":
    main()
