"""Repinta las tintas de save-the-date-lekshmy-jaylin a tema oscuro (cielo nocturno).

Papel -> #0A1430 exacto; tinta -> mapa de gradiente 6 paradas zafiro -> acero;
vetas doradas en los bordes de la tinta: (gaussian_blur - original) x6, al 85 % con dorado.

Uso: python _src/recolor_ink.py
"""
import os
import numpy as np
from PIL import Image, ImageFilter

SRC = r"C:/Users/aleja/save-the-date-lekshmy-jaylin"
DST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ink")
NAMES = ["hero", "top", "oval", "corner", "footer"]
MAX_W = 860

def hx(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.float32)

INK = hx("#0A1430")
# 6 paradas: papel -> zafiro -> acero (la tinta más densa en el tono más vivo)
STOPS = [
    (0.00, hx("#0A1430")),
    (0.18, hx("#0D1B40")),
    (0.38, hx("#132857")),
    (0.60, hx("#1E3A8A")),
    (0.82, hx("#3460A2")),
    (1.00, hx("#4A7BB7")),
]
GOLD = hx("#D4AF37")
GOLD_HI = hx("#F1DC8A")

INTENSITY = 0.74      # techo de la tinta (mantiene luminosidad media como máx.)
PAPER_L = 244.0       # luminosidad del papel
DARK_L = 80.0         # tinta más densa esperada
FLOOR = 0.05          # textura de papel por debajo de esto = fondo puro


def gradient(d):
    out = np.zeros(d.shape + (3,), np.float32)
    for (p0, c0), (p1, c1) in zip(STOPS[:-1], STOPS[1:]):
        m = (d >= p0) & (d <= p1)
        t = ((d[m] - p0) / (p1 - p0))[:, None]
        out[m] = c0 * (1 - t) + c1 * t
    return out


def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


def process(name):
    im = Image.open(os.path.join(SRC, f"ink-{name}.jpg")).convert("RGB")
    if im.width > MAX_W:
        im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
    a = np.asarray(im, np.float32)
    L = 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]

    # densidad de tinta (sin la textura del papel)
    Ls = np.asarray(Image.fromarray(L.astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2)), np.float32)
    d = np.clip((PAPER_L - Ls) / (PAPER_L - DARK_L), 0, 1)
    d = smoothstep(FLOOR, 1.0, d)
    # normaliza por imagen: la tinta más densa (p99.5) llega al mismo techo en todas
    ref = np.percentile(d[d > 0], 99.5) if (d > 0).any() else 1.0
    d = np.clip(d / max(ref, 1e-3), 0, 1) ** 0.9 * INTENSITY
    rgb = gradient(d)

    # vetas: blur - original (las líneas oscuras quedan positivas) x6
    g = Image.fromarray(Ls.astype(np.uint8))
    blur = np.asarray(g.filter(ImageFilter.GaussianBlur(4)), np.float32)
    edge = np.clip((blur - Ls) / 255.0 * 6.0, 0, 1)
    edge = smoothstep(0.10, 0.75, edge)
    edge *= smoothstep(0.02, 0.12, d)            # solo donde hay tinta, nunca en papel
    gold = GOLD * (1 - edge[..., None] ** 3) + GOLD_HI * edge[..., None] ** 3   # puntas más claras
    alpha = (edge * 0.85)[..., None] * 0.80      # 85 % de mezcla, atenuado para ser sutil
    rgb = rgb * (1 - alpha) + gold * alpha

    # papel puro exactamente en #0A1430
    paper = (d <= 1e-6) & (edge <= 1e-6)
    rgb[paper] = INK
    out = Image.fromarray(np.clip(np.round(rgb), 0, 255).astype(np.uint8))

    path = os.path.join(DST, f"ink-{name}.webp")
    for q in (90, 82, 76, 70, 64, 58, 50):
        out.save(path, "WEBP", quality=q, method=6)
        if os.path.getsize(path) <= 120_000:
            break
    print(f"{name}: {out.size} q={q} {os.path.getsize(path) // 1024} KB, paper={paper.mean():.0%}")
    return out


if __name__ == "__main__":
    os.makedirs(DST, exist_ok=True)
    outs = [process(n) for n in NAMES]
    th = [o.resize((256, round(o.height * 256 / o.width))) for o in outs]
    m = Image.new("RGB", (256 * len(th), max(t.height for t in th)), tuple(int(x) for x in INK))
    for i, t in enumerate(th):
        m.paste(t, (i * 256, 0))
    m.save(os.path.join(os.environ.get("MONTAGE_DIR", DST), "_montage.png"))
