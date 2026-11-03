#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генерация графиков главы 4 (Таненбаум, «Компьютерные сети», 6-е изд.) для Obsidian.
Рисует кривые и диаграммы напрямую в SVG (без matplotlib), затем конвертирует в PNG
через rsvg-convert. Все формулы взяты из главы 4; числа сверены с текстом книги.

Запуск:  python3 gen-ch4-plots.py [каталог_для_png]
"""
import math
import os
import subprocess
import sys

E = math.e

# ---------------------------------------------------------------- параметры
W, H = 900, 600
M = dict(l=95, r=40, t=60, b=80)          # поля
FONT = "DejaVu Sans"


def _esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


class Svg:
    """Минимальный помощник для сборки SVG."""

    def __init__(self, w=W, h=H, title="", head=7):
        self.w, self.h, self.head = w, h, head
        self.p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
                  f'viewBox="0 0 {w} {h}" font-family="{FONT}">']
        self.p.append(f'<rect width="{w}" height="{h}" fill="#ffffff"/>')
        if title:
            self.p.append(
                f'<text x="{w/2}" y="30" font-size="19" font-weight="bold" '
                f'text-anchor="middle" fill="#1a1a1a">{_esc(title)}</text>')

    def line(self, x1, y1, x2, y2, stroke="#333", width=1, dash=None, cap="butt"):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.p.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
                      f'stroke="{stroke}" stroke-width="{width}" stroke-linecap="{cap}"{d}/>')

    def rect(self, x, y, w, h, fill="#69f", stroke="#333", width=1, rx=0):
        self.p.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" '
                      f'fill="{fill}" stroke="{stroke}" stroke-width="{width}" rx="{rx}"/>')

    def text(self, x, y, s, size=13, fill="#1a1a1a", anchor="start",
             weight="normal", style="normal", rotate=None):
        tr = f' transform="rotate({rotate} {x:.2f} {y:.2f})"' if rotate else ""
        self.p.append(f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" fill="{fill}" '
                      f'text-anchor="{anchor}" font-weight="{weight}" '
                      f'font-style="{style}"{tr}>{_esc(s)}</text>')

    def path(self, pts, stroke="#c33", width=2.5, fill="none", dash=None):
        if not pts:
            return
        d = "M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in pts)
        da = f' stroke-dasharray="{dash}"' if dash else ""
        self.p.append(f'<path d="{d}" fill="{fill}" stroke="{stroke}" '
                      f'stroke-width="{width}" stroke-linejoin="round"{da}/>')

    def dot(self, x, y, r=5, fill="#c33", stroke="#fff", width=1.5):
        self.p.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{fill}" '
                      f'stroke="{stroke}" stroke-width="{width}"/>')

    def arrow(self, x1, y1, x2, y2, stroke="#333", width=1.6, head=7):
        self.p.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
                      f'stroke="{stroke}" stroke-width="{width}" marker-end="url(#ah)"/>')

    def save(self, path_svg):
        h = self.head
        self.p.append(f'<defs><marker id="ah" markerWidth="{h*1.4}" markerHeight="{h*1.4}" '
                      f'refX="{h}" refY="{h/2}" orient="auto">'
                      f'<path d="M0,0 L{h*1.4},{h/2} L0,{h} z" fill="#333"/>'
                      f'</marker></defs>')
        self.p.append("</svg>")
        with open(path_svg, "w", encoding="utf-8") as f:
            f.write("\n".join(self.p))


def to_png(svg_path, png_path):
    subprocess.run(["rsvg-convert", "-z", "2.0", "-b", "white",
                    "-o", png_path, svg_path], check=True)


# ------------------------------------------------------- ось / сетка
def make_axes(svg, xlim, ylim, xlabel, ylabel, xticks, yticks,
              xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", bottom=None):
    """Рисует систему координат и возвращает функции проекции X, Y."""
    px0, px1 = M["l"], svg.w - M["r"]
    py0, py1 = svg.h - (M["b"] if bottom is None else bottom), M["t"]

    def X(v):
        return px0 + (v - xlim[0]) / (xlim[1] - xlim[0]) * (px1 - px0)

    def Y(v):
        # py0 — низ полотна (в SVG y растёт вниз), py1 — верх
        return py0 + (v - ylim[0]) / (ylim[1] - ylim[0]) * (py1 - py0)

    # сетка
    for xv in xticks:
        svg.line(X(xv), py1, X(xv), py0, "#e0e0e0", 1)
        svg.text(X(xv), py0 + 20, xfmt(xv), 12, "#555", "middle")
    for yv in yticks:
        svg.line(px0, Y(yv), px1, Y(yv), "#e0e0e0", 1)
        svg.text(px0 - 10, Y(yv) + 4, yfmt(yv), 12, "#555", "end")
    # рамка
    svg.rect(px0, py1, px1 - px0, py0 - py1, "none", "#333", 1.4)
    # подписи осей
    svg.text((px0 + px1) / 2, H - 22, xlabel, 14, "#1a1a1a", "middle")
    svg.text(26, (py0 + py1) / 2, ylabel, 14, "#1a1a1a", "middle", rotate=-90)
    return X, Y


def curve(X, Y, fn, lo, hi, n=500):
    return [(X(lo + (hi - lo) * i / n), Y(fn(lo + (hi - lo) * i / n))) for i in range(n + 1)]


# ============================================================== 1. S(G) ALOHA
def plot_aloha(outdir):
    svg = Svg(title="Производительность S в зависимости от предлагаемой загрузки G")
    X, Y = make_axes(svg, (0, 2.0), (0, 0.45), "G — число попыток передачи за время фрейма",
                     "S — производительность за время фрейма",
                     [0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0],
                     [0, 0.1, 0.2, 0.3, 0.4],
                     xfmt=lambda v: f"{v:.2f}".rstrip("0").rstrip("."),
                     yfmt=lambda v: f"{v:.1f}".replace(".", ","))

    pure = lambda g: g * math.exp(-2 * g)          # S = G·e^-2G  (чистая ALOHA)
    slot = lambda g: g * math.exp(-g)             # S = G·e^-G   (дискретная ALOHA)

    svg.path(curve(X, Y, pure, 0, 2.0), "#1f77b4", 3)
    svg.path(curve(X, Y, slot, 0, 2.0), "#d62728", 3)

    # максимумы
    svg.dot(*[X(0.5), Y(1 / (2 * E))], 6, "#1f77b4")
    svg.text(X(0.5) - 12, Y(1 / (2 * E)) - 12, "G = 0,5   S = 1/2e ≈ 0,184", 13, "#1f77b4", "end", weight="bold")
    svg.dot(*[X(1.0), Y(1 / E)], 6, "#d62728")
    svg.text(X(1.0) + 14, Y(1 / E) + 34, "G = 1   S = 1/e ≈ 0,368", 13, "#d62728", weight="bold")

    # горизонтальные отметки пиков
    for val, col in ((1 / (2 * E), "#1f77b4"), (1 / E, "#d62728")):
        svg.line(X(0), Y(val), X(2.0), Y(val), col, 1, dash="5,4")

    # легенда
    lx, ly = X(0.42), Y(0.415)
    svg.line(lx, ly, lx + 46, ly, "#d62728", 3)
    svg.text(lx + 54, ly + 5, "дискретная ALOHA:  S = G·e^-G", 13.5, "#1a1a1a")
    svg.line(lx, ly + 26, lx + 46, ly + 26, "#1f77b4", 3)
    svg.text(lx + 54, ly + 31, "чистая ALOHA:  S = G·e^-2G", 13.5, "#1a1a1a")

    svg.text(W / 2, H - 44, "Уязвимый период чистой ALOHA — 2t, поэтому в показателе экспоненты "
                             "стоит 2G, а не G", 12.5, "#666", "middle", style="italic")

    svg.save(f"{outdir}/_aloha.svg")
    to_png(f"{outdir}/_aloha.svg", f"{outdir}/ch4-aloha-throughput.png")


# ================================================== 2. Разбор слота ALOHA G=1
def plot_slots(outdir):
    svg = Svg(900, 420, title="Дискретная ALOHA при G = 1: что происходит в каждом слоте")
    px0, px1 = 120, W - 60
    top, bw = 110, 130

    parts = [(0.368, "#d9d9d9", "ПУСТО", "e^-1 = 0,368"),
             (0.368, "#4CAF50", "УСПЕХ", "G·e^-G = 0,368"),
             (0.264, "#d62728", "КОЛЛИЗИЯ", "1 - 2·e^-1 = 0,264")]
    x = px0
    for frac, col, name, val in parts:
        w = (px1 - px0) * frac
        svg.rect(x, top, w, bw, col, "#333", 1.5)
        svg.text(x + w / 2, top + bw / 2 - 4, name, 15, "#fff" if col != "#d9d9d9" else "#333",
                 "middle", weight="bold")
        svg.text(x + w / 2, top + bw / 2 + 20, f"{frac*100:.1f} %", 13,
                 "#fff" if col != "#d9d9d9" else "#333", "middle")
        svg.text(x + w / 2, top + bw + 26, val, 12.5, "#555", "middle")
        x += w

    svg.text((px0 + px1) / 2, top - 22, "100 слотов, передано 37 фреймов — в канале 37 % ёмкости",
             14, "#1a1a1a", "middle")
    svg.text(W / 2, top + bw + 70,
             "S = 1/e ≈ 0,368 — вдвое выше, чем у чистой ALOHA (1/2e ≈ 0,184), "
             "потому что уязвимый период вдвое короче",
             13, "#666", "middle", style="italic")
    svg.text(W / 2, top + bw + 96,
             "При росте G доля пустых слотов падает, но коллизии растут лавинообразно: "
             "вероятность коллизии = 1 − e^-G",
             12.5, "#666", "middle", style="italic")

    svg.save(f"{outdir}/_slots.svg")
    to_png(f"{outdir}/_slots.svg", f"{outdir}/ch4-aloha-slots.png")


# ============================================= 3. Эффективность Ethernet
def plot_eth(outdir):
    svg = Svg(w=900, h=680,
              title="Эффективность классического Ethernet (10 Мбит/с, слот 2τ = 51,2 мкс)")
    X, Y = make_axes(svg, (0, 1600), (0, 1.0), "Размер фрейма F, байт",
                     "Эффективность канала", [0, 200, 400, 600, 800, 1000, 1200, 1400, 1600],
                     [0, 0.2, 0.4, 0.6, 0.8, 1.0],
                     xfmt=lambda v: f"{v:.0f}",
                     yfmt=lambda v: f"{v:.1f}".replace(".", ","),
                     bottom=150)

    B, two_tau = 10e6, 51.2e-6
    slot_bytes = two_tau * B / 8                         # 2τ — это уже весь слот => 64 байта
    overhead = E * slot_bytes                            # ≈ 174 байта
    eff = lambda f: f / (f + overhead)
    svg.path(curve(X, Y, eff, 1, 1600, 700), "#2E7D32", 3.2)

    svg.text(X(0), Y(0.0) + 52,
             f"Формула (4.3):  S = F / (F + e·L),   L = e·слот = {overhead:.0f} байт "
             f"(слот 2τ = 51,2 мкс = {slot_bytes:.0f} байт)",
             13.5, "#2E7D32", "start", weight="bold")

    for f, col in ((64, "#d62728"), (1024, "#1565C0")):
        svg.line(X(f), Y(eff(f)), X(f), Y(0), col, 1.2, dash="4,4")
        svg.dot(X(f), Y(eff(f)), 6, col)
        lbl = "64 Б — треть ёмкости уходит в конкуренцию" if f == 64 else "1024 Б — 85 % (цифра из книги)"
        svg.text(X(f) + 12, Y(eff(f)) - 10, f"F = {f} Б: {eff(f)*100:.1f} %".replace(".", ","),
                 13, col, weight="bold")
        svg.text(X(f) + 12, Y(eff(f)) + 9, lbl, 11.5, col)

    svg.text(450, 632,
             "Каждый фрейм «покупает» конкуренцию ценой ≈ e·2τ бит. Это постоянная величина,",
             12.5, "#666", "middle", style="italic")
    svg.text(450, 654,
             "поэтому короткие фреймы проигрывают: накладные расходы не масштабируются вниз вместе с F.",
             12.5, "#666", "middle", style="italic")

    svg.save(f"{outdir}/_eth.svg")
    to_png(f"{outdir}/_eth.svg", f"{outdir}/ch4-ethernet-efficiency.png")


# ============================================= 4. Спектральная эффективность кодирования
def plot_coding(outdir):
    svg = Svg(900, 520,
              title="Сколько полосы тратит каждый код: тактический расчёт расширения полосы")
    # Manchester: 1 бит -> 2 такта => x2 полосы ; NRZ x1 ; 4B/5B x1.25 ; 8B/10B x1.25 ; 64B/66B x1.031
    schemes = [("Манчестер (Ethernet 10 Мбит/с)", 2.00, "#d62728"),
               ("NRZ — без кодирования", 1.00, "#4CAF50"),
               ("4B/5B (FDDI, 100Base-TX)", 1.25, "#FF9800"),
               ("8B/10B (Gigabit, Fibre Channel)", 1.25, "#FF9800"),
               ("64B/66B (10/40/100GE)", 1.031, "#1565C0")]
    px0, pw = 330, 430
    y0 = 120
    for i, (name, k, col) in enumerate(schemes):
        y = y0 + i * 58
        svg.text(px0 - 14, y + 20, name, 13, "#1a1a1a", "end")
        w = pw * (k / 2.0)
        svg.rect(px0, y, max(w, 3), 40, col, "#333", 1.2)
        svg.text(px0 + w + 12, y + 26, f"x{k:.3g}".replace("1.", "1,"), 14, col, weight="bold")
    svg.line(px0, y0 - 18, px0, y0 + 5 * 58 - 18, "#333", 1.6)
    svg.text(px0, y0 - 28, "полоса, необходимая на 1 бит данных", 12.5, "#555")
    svg.text(450, y0 + 5 * 58 + 30,
             "Манчестер удваивает полосу — поэтому от него отказались.",
             12.5, "#666", "middle", style="italic")
    svg.text(450, y0 + 5 * 58 + 52,
             "8B/10B требует +25 % вместо +100 % у Манчестера, а 64B/66B почти ничего не добавляет.",
             12.5, "#666", "middle", style="italic")
    svg.save(f"{outdir}/_coding.svg")
    to_png(f"{outdir}/_coding.svg", f"{outdir}/ch4-line-coding.png")


if __name__ == "__main__":
    outdir = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(outdir, exist_ok=True)
    plot_aloha(outdir)
    print("  ch4-aloha-throughput.png")
    plot_slots(outdir)
    print("  ch4-aloha-slots.png")
    plot_eth(outdir)
    print("  ch4-ethernet-efficiency.png")
    plot_coding(outdir)
    print("  ch4-line-coding.png")
    for f in os.listdir(outdir):
        if f.startswith("_") and f.endswith(".svg"):
            os.remove(os.path.join(outdir, f))