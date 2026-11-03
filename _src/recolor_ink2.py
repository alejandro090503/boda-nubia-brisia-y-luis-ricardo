"""Tintas de lekshmy en tres tonos (azul, champán y oro) con fondo TRANSPARENTE,
para que la bruma animada se vea por debajo.

dark  -> para secciones azul noche: bordes de la tinta champán, núcleo azul acero, vetas oro
light -> para secciones champán:    bordes arena/oro, núcleo azul polvo, vetas oro antiguo
Uso: python _src/recolor_ink2.py
"""
import os
import numpy as np
from PIL import Image, ImageFilter

SRC = r"C:/Users/aleja/save-the-date-lekshmy-jaylin"
DST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ink")
NAMES = ["hero", "top", "oval", "corner", "footer"]
MAX_W = 640

def hx(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float32)

PAL = {
    "dark": dict(stops=[(0, "#2E5596"), (.30, "#4A7BB7"), (.55, "#9DB3D0"), (.78, "#E2CFA6"), (1, "#F4E6C6")],
                 vein=("#D4AF37", "#FFF1C2"), amax=.95, vmix=.85, acurve=(.08, .85)),
    "light": dict(stops=[(0, "#E2C990"), (.30, "#C9A45A"), (.55, "#8FAACB"), (.80, "#4A7BB7"), (1, "#2C5296")],
                  vein=("#A8811C", "#D4AF37"), amax=.72, vmix=.9),
}

def ss(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)

def grad(d, stops):
    st = [(p, hx(c)) for p, c in stops]
    out = np.zeros(d.shape + (3,), np.float32)
    for (p0, c0), (p1, c1) in zip(st[:-1], st[1:]):
        m = (d >= p0) & (d <= p1)
        t = ((d[m] - p0) / (p1 - p0))[:, None]
        out[m] = c0 * (1 - t) + c1 * t
    return out

def process(name, mode):
    P = PAL[mode]
    im = Image.open(os.path.join(SRC, f"ink-{name}.jpg")).convert("RGB")
    if im.width > MAX_W:
        im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
    a = np.asarray(im, np.float32)
    L = 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]
    Ls = np.asarray(Image.fromarray(L.astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2)), np.float32)
    d = np.clip((244 - Ls) / (244 - 80), 0, 1)
    d = ss(.05, 1, d)
    ref = np.percentile(d[d > 0], 99.5) if (d > 0).any() else 1
    d = np.clip(d / max(ref, 1e-3), 0, 1) ** .85
    rgb = grad(d, P["stops"])
    blur = np.asarray(Image.fromarray(Ls.astype(np.uint8)).filter(ImageFilter.GaussianBlur(4)), np.float32)
    edge = ss(.10, .75, np.clip((blur - Ls) / 255 * 6, 0, 1)) * ss(.02, .12, d)
    g0, g1 = hx(P["vein"][0]), hx(P["vein"][1])
    gold = g0 * (1 - edge[..., None] ** 3) + g1 * edge[..., None] ** 3
    va = (edge * P["vmix"])[..., None]
    rgb = rgb * (1 - va) + gold * va
    ac = P.get("acurve", (0, .55))
    alpha = np.clip(ss(ac[0], ac[1], d) * P["amax"] + edge * .5, 0, 1)
    out = Image.fromarray(np.dstack([np.clip(rgb, 0, 255), alpha * 255]).astype(np.uint8), "RGBA")
    path = os.path.join(DST, f"tri-{mode}-{name}.webp")
    for q in (86, 78, 70, 62, 54):
        out.save(path, "WEBP", quality=q, method=4)
        if os.path.getsize(path) <= 130_000:
            break
    print(mode, name, out.size, os.path.getsize(path) // 1024, "KB")
    return out

if __name__ == "__main__":
    tiles = []
    for mode, bg in (("dark", "#0A1430"), ("light", "#F7E7CE")):
        if mode not in os.environ.get("MODES", "dark,light"): continue
        for n in NAMES:
            o = process(n, mode)
            t = o.resize((220, round(o.height * 220 / o.width)))
            base = Image.new("RGBA", t.size, bg); base.alpha_composite(t); tiles.append(base)
    rows = (len(tiles) + 4) // 5; th = max(t.height for t in tiles)
    m = Image.new("RGB", (1100, th * rows), "white")
    for i, t in enumerate(tiles):
        m.paste(t.convert("RGB"), ((i % 5) * 220, (i // 5) * th))
    m.save(os.environ.get("MONTAGE", os.path.join(DST, "_tri.jpg")))
