#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Графики для Глава 1 (Таненбаум, «Компьютерные сети», 6-е изд.).
Рисует кривые и диаграммы прямо в SVG (без matplotlib), затем конвертирует в PNG
через rsvg-convert. Числа взяты из текста глав; ссылки на страницы указаны в комментариях.

Запуск:  python3 gen-ch13-plots.py [каталог_для_png]
"""
import math
import os
import subprocess
import sys

E = math.e
W, H = 920, 600
M = dict(l=100, r=40, t=60, b=80)
FONT = "DejaVu Sans"


def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class Svg:
    def __init__(self, w=W, h=H, title=""):
        self.w, self.h = w, h
        self.p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
                  f'viewBox="0 0 {w} {h}" font-family="{FONT}">',
                  f'<rect width="{w}" height="{h}" fill="#ffffff"/>']
        if title:
            self.p.append(f'<text x="{w/2}" y="30" font-size="19" font-weight="bold" '
                          f'text-anchor="middle" fill="#1a1a1a">{_esc(title)}</text>')

    def line(self, x1, y1, x2, y2, stroke="#333", width=1, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.p.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
                      f'stroke="{stroke}" stroke-width="{width}"{d}/>')

    def poly(self, pts, stroke="#c33", width=2.2, fill="none", dash=None, close=False):
        if len(pts) < 2:
            return
        tag = "polygon" if close else "polyline"
        d = f' stroke-dasharray="{dash}"' if dash else ""
        pts_s = " ".join(f"{x:.2f},{y:.2f}" for x, y in pts)
        self.p.append(f'<{tag} points="{pts_s}" fill="{fill}" stroke="{stroke}" '
                      f'stroke-width="{width}" stroke-linejoin="round"{d}/>')

    def rect(self, x, y, w, h, fill="#69f", stroke="#333", width=1, rx=0):
        self.p.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" '
                      f'fill="{fill}" stroke="{stroke}" stroke-width="{width}" rx="{rx}"/>')

    def circle(self, x, y, r, fill="#333", stroke="none", width=1):
        self.p.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.1f}" fill="{fill}" '
                      f'stroke="{stroke}" stroke-width="{width}"/>')

    def text(self, x, y, s, size=13, fill="#1a1a1a", anchor="start", weight="normal",
             style="normal", rotate=None, mono=False):
        tr = f' transform="rotate({rotate} {x:.2f} {y:.2f})"' if rotate else ""
        fam = "DejaVu Sans Mono" if mono else FONT
        self.p.append(f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" fill="{fill}" '
                      f'text-anchor="{anchor}" font-weight="{weight}" font-style="{style}" '
                      f'font-family="{fam}"{tr}>{_esc(s)}</text>')

    def save(self, path):
        self.p.append("</svg>")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.p))


def to_png(svg_path, png_path):
    subprocess.run(["rsvg-convert", "-z", "2.0", "-b", "white", "-o", png_path, svg_path],
                   check=True)


def axes(svg, xlim, ylim, xlabel, ylabel, xticks, yticks,
         xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", bottom=None):
    px0, px1 = M["l"], svg.w - M["r"]
    py0, py1 = svg.h - (M["b"] if bottom is None else bottom), M["t"]

    def X(v):
        return px0 + (v - xlim[0]) / (xlim[1] - xlim[0]) * (px1 - px0)

    def Y(v):
        return py0 + (v - ylim[0]) / (ylim[1] - ylim[0]) * (py1 - py0)

    for xv in xticks:
        svg.line(X(xv), py1, X(xv), py0, "#e8e8e8", 1)
        svg.text(X(xv), py0 + 20, xfmt(xv), 12, "#555", "middle")
    for yv in yticks:
        svg.line(px0, Y(yv), px1, Y(yv), "#e8e8e8", 1)
        svg.text(px0 - 10, Y(yv) + 4, yfmt(yv), 12, "#555", "end")
    svg.rect(px0, py1, px1 - px0, py0 - py1, "none", "#333", 1.4)
    svg.text((px0 + px1) / 2, svg.h - 22, xlabel, 14, "#1a1a1a", "middle")
    svg.text(26, (py0 + py1) / 2, ylabel, 14, "#1a1a1a", "middle", rotate=-90)
    return X, Y


def curve(X, Y, fn, lo, hi, n=600):
    return [(X(lo + (hi - lo) * i / n), Y(fn(lo + (hi - lo) * i / n))) for i in range(n + 1)]


# ==================================================== 9. Префиксы и единицы
def plot_units(outdir):
    """Стр. 111–113 и 2.4.1: десятичные и двоичные префиксы, бод против бит/с."""
    svg = Svg(920, 560, "Две ловушки измерений: префиксы и бод")
    svg.text(460, 84, "Ловушка 1: кило и мега", 15, "#1f77b4", "middle", weight="bold")
    rows = [("К", 10 ** 3, "2¹⁰ = 1024"), ("М", 10 ** 6, "2²⁰ ≈ 1,05 · 10⁶"),
            ("Г", 10 ** 9, "2³⁰ ≈ 1,07 · 10⁹"), ("Т", 10 ** 12, "2⁴⁰ ≈ 1,1 · 10¹²")]
    x = 90
    for name, dec, binr in rows:
        svg.rect(x, 108, 190, 62, "#eef3fb", "#4a6fa5", 1.4, 6)
        svg.text(x + 95, 132, name, 15, "#4a6fa5", "middle", weight="bold")
        svg.text(x + 95, 152, f"десятичный: {dec:,}".replace(",", " "), 11.5, "#333", "middle")
        svg.text(x + 95, 166, f"двоичный: {binr}", 11.5, "#666", "middle")
        x += 200
    svg.text(460, 194, "Производители дисков пишут «килобайт» про двоичные 1024 байта.",
             12.5, "#666", "middle", style="italic")
    svg.text(460, 214, "Стандарт IEC ввёл отдельные приставки: KiB, MiB, GiB — честные 1024, 10⁶, 10⁹.",
             12.5, "#666", "middle", style="italic")

    svg.text(460, 274, "Ловушка 2: бод ≠ бит/с", 15, "#d62728", "middle", weight="bold")
    svg.text(60, 306, "симв./с", 11.5, "#666")
    cases = [("2400 бод, 4 бит/символ", 2400, 9600, "QAM-16"),
             ("2400 бод, 5 бит/символ", 2400, 12000, "QAM-32"),
             ("2400 бод, 6 бит/символ", 2400, 14400, "QAM-64")]
    y = 326
    for name, baud, bps, mod in cases:
        svg.text(60, y + 16, name, 12.5, "#333")
        bw = 480 * (baud / 2400)
        svg.rect(330, y, bw, 26, "#cde8cd", "#2e7d29", 1.3)
        svg.text(330 + bw + 10, y + 18, f"{baud} бод", 12, "#2e7d29")
        svg.rect(600, y, 480 * (bps / 14400), 26, "#ffe0e8", "#d62728", 1.3)
        svg.text(600 + 480 * (bps / 14400) + 10, y + 18,
                 f"{bps} бит/с ({mod})", 12, "#d62728")
        y += 40
    svg.text(60, y + 24, "Бод — единица СИ, это символы в секунду. Бит/с получается умножением",
             12.5, "#666", style="italic")
    svg.text(60, y + 46, "на число бит в символе. Модем V.32bis: 2400 бод → 9600 бит/с.",
             12.5, "#666", style="italic")

    svg.text(460, 512, "Отсюда разница между аналоговым модемом и сетевым адаптером.",
             13, "#666", "middle", style="italic")

    svg.save(f"{outdir}/_un.svg")
    to_png(f"{outdir}/_un.svg", f"{outdir}/ch1-units.png")
# ==================================================== 10. Масштабы сетей
def plot_scales(outdir):
    """Стр. 33–52: PAN, LAN, MAN, WAN — радиусы и типичные скорости."""
    svg = Svg(920, 560, "Масштаб сетей (разд. 1.3, стр. 33–52)")
    data = [("PAN", "комната", "до 10 м", "1–3 Мбит/с", "#06d6a0", 10),
            ("LAN", "здание", "до 1–2 км", "100 Мбит/с – 100 Гбит/с", "#1f77b4", 2000),
            ("MAN", "город", "до 50 км", "1–10 Гбит/с", "#7b4ea3", 50000),
            ("WAN", "страна, континент", "тысячи км", "Мбит/с – Тбит/с", "#d62728", 1e6)]
    px0, px1 = 130, 880
    for i, (name, place, dist, speed, col, metres) in enumerate(data):
        y = 100 + i * 100
        svg.rect(px0, y, px1 - px0, 66, "#fafafa", col, 1.6, 6)
        svg.rect(px0, y, 118, 66, col, "none", 0, 6)
        svg.text(px0 + 59, y + 42, name, 19, "#fff", "middle", weight="bold")
        svg.text(px0 + 140, y + 26, place, 13.5, "#333", weight="bold")
        svg.text(px0 + 140, y + 48, dist, 12.5, col, weight="bold")
        svg.text(px0 + 330, y + 37, speed, 12.5, "#555")
    svg.text(460, 528, "Радиус растёт на порядки, а скорость на единицу расстояния — падает.",
             13, "#666", "middle", style="italic")

    svg.save(f"{outdir}/_sc.svg")
    to_png(f"{outdir}/_sc.svg", f"{outdir}/ch1-network-scales.png")


if __name__ == "__main__":
    outdir = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(outdir, exist_ok=True)
    for name in [n for n in dir() if n.startswith("plot_")]:
        globals()[name](outdir)
    for f in os.listdir(outdir):
        if f.startswith("_") and f.endswith(".svg"):
            os.remove(os.path.join(outdir, f))
