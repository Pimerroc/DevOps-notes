#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Графики для Глава 2 (Таненбаум, «Компьютерные сети», 6-е изд.).
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


# ==================================================== 1. Ёмкость канала: Найквист и Шеннон
def plot_capacity(outdir):
    """Формулы главы 2, разд. 2.4: Найквист и Шеннон."""
    svg = Svg(920, 640, "Предельная скорость канала: теорема Найквиста и формула Шеннона")
    X, Y = axes(svg, (0, 12), (0, 6000), "полоса B, кГц", "предельная скорость, бит/с",
                [0, 2, 4, 6, 8, 10, 12], [0, 1000, 2000, 3000, 4000, 5000, 6000],
                xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", bottom=150)

    # Найквист для 2 уровней: C = 2B  →  Бит/с = 2 * B(кГц) * 1000
    svg.poly(curve(X, Y, lambda b: 2 * b * 1000, 0, 12), "#1f77b4", 3.2)
    # Шеннон для разных SNR (дБ)
    for snr_db, col, lbl in ((0, "#2e7d32", "Шеннон, SNR = 0 дБ"),
                             (10, "#e68a00", "Шеннон, SNR = 10 дБ"),
                             (20, "#d62728", "Шеннон, SNR = 20 дБ")):
        snr = 10 ** (snr_db / 10)
        svg.poly(curve(X, Y, lambda b, s=snr: b * 1000 * math.log2(1 + s), 0, 12), col, 2.8)
        svg.text(X(6.3), Y(6.3 * 1000 * math.log2(1 + snr)) - 10, lbl, 12.5, col, weight="bold")

    svg.text(X(0.2), Y(1500), "Найквист (2 уровня):  C = 2B", 14, "#1f77b4", weight="bold")
    svg.text(X(0.2), Y(1050), "Шеннон:  C = B · log₂(1 + S/N)", 14, "#2e7d32", weight="bold")

    svg.text(460, 555, "Ключевая мысль главы: Найквист — это потолок из-за самой системы передачи,",
             13, "#666", "middle", style="italic")
    svg.text(460, 577, "а Шеннон — из-за шума. Реальный канал берёт минимум из двух ограничений.",
             13, "#666", "middle", style="italic")
    svg.text(460, 606, "Пример: полоса 4 кГц (телефон) → Найквист даёт 8000 бит/с, и этого",
             13, "#666", "middle", style="italic")
    svg.text(460, 628, "в точности хватает для оцифровки голоса с частотой до 4 кГц.",
             13, "#666", "middle", style="italic")

    svg.save(f"{outdir}/_cap.svg")
    to_png(f"{outdir}/_cap.svg", f"{outdir}/ch2-capacity.png")
# ==================================================== 2. Кодирование линий
def plot_linecodes(outdir):
    """Илл. 2.14: NRZ, NRZI, Манчестер, AMI. Стр. 150–151."""
    svg = Svg(920, 620, "Линейные коды (илл. 2.14, стр. 150): одни и те же биты — четыре сигнала")
    bits = "10000101111"
    y0 = 110
    bh = 56
    names = [("NRZ — «без возврата к нулю»", "#1f77b4"),
             ("NRZI — инвертированный NRZ", "#7b4ea3"),
             ("Манчестер", "#2e7d32"),
             ("AMI — чередование полярности", "#e68a00")]
    n = len(bits)
    x_start = 300
    step = (880 - x_start) / n

    for bi, b in enumerate(bits):
        x = x_start + bi * step
        svg.text(x + step / 2, y0 - 12, b, 15, "#1a1a1a", "middle", weight="bold")
    svg.text(x_start - 14, y0 - 12, "биты", 13, "#555", "end", weight="bold")

    def hi(level):        # верхний уровень
        return y0 + 18

    def lo(level):        # нижний уровень
        return y0 + bh - 8

    for row, (name, col) in enumerate(names):
        base = y0 + row * (bh + 46)
        svg.text(286, base + 22, name, 12.5, col, "end", weight="bold")

        def lvl(i, kind):
            b = int(bits[i])
            if kind == "nrz":
                return 0 if b else 1           # 1 = высокий уровень
            if kind == "nrzi":
                # уровень кумулятивный: инверсия на каждой единице,
                # на нуле уровень сохраняется. Иначе получился бы NRZ-инверсия.
                prev = 1                       # произвольный начальный уровень
                for k in range(i + 1):
                    if bits[k] == "1":
                        prev ^= 1
                return 0 if prev else 1
            return 0 if b else 1               # man / ami

        kind = ["nrz", "nrzi", "man", "ami"][row]
        top, bot = base + 6, base + bh - 12
        pts = []
        cur = None
        for i in range(n):
            L = lvl(i, kind)
            y = top if L == 0 else bot
            # манчестер и AMI рисуем по интервалам
            x1 = x_start + i * step
            if kind == "man":
                # каждый бит = два интервала: смена уровня в середине
                a = top if bits[i] == "1" else bot
                b2 = bot if bits[i] == "1" else top
                svg.line(x1, a, x1 + step / 2, a, col, 2.4)
                svg.line(x1 + step / 2, a, x1 + step / 2, b2, col, 2.4)
                svg.line(x1 + step / 2, b2, x1 + step, b2, col, 2.4)
            elif kind == "ami":
                if bits[i] == "0":
                    svg.line(x1, (top + bot) / 2, x1 + step, (top + bot) / 2, "#999", 1.4, "3,3")
                else:
                    yv = top if (cur is None or cur == "low") else bot
                    svg.line(x1, yv, x1 + step, yv, col, 2.4)
                    cur = "high" if cur is None or cur == "low" else "low"
            else:
                y = top if L == 0 else bot
                if pts and pts[-1][1] == y:
                    pass
                else:
                    pts.append((x1, y))
                svg.line(x1, y, x1 + step, y, col, 2.4)
            svg.line(x1, bot + 4, x1, bot + 10, "#bbb", 1)
        if kind in ("nrz", "nrzi"):
            svg.poly(pts + [(x_start + n * step, pts[-1][1])], col, 2.4)

    svg.text(460, y0 + 4 * (bh + 46) + 24,
             "NRZ дешевле всего, но не даёт тактовой синхронизации: при длинной серии единиц сигнал «залипает».",
             13, "#666", "middle", style="italic")
    svg.text(460, y0 + 4 * (bh + 46) + 48,
             "Манчестер всегда переключается в середине бита — синхронизация гарантирована, но полоса удваивается (x2).",
             13, "#666", "middle", style="italic")
    svg.text(460, y0 + 4 * (bh + 46) + 72,
             "AMI ноль не передаёт вовсе (пунктир) — зато полярность не «залипает», постоянная составляющая равна нулю.",
             13, "#666", "middle", style="italic")

    svg.save(f"{outdir}/_lc.svg")
    to_png(f"{outdir}/_lc.svg", f"{outdir}/ch2-line-codes.png")
# ==================================================== 3. Диаграммы созвездий
def plot_constellations(outdir):
    """Илл. 2.16-2.18: ASK, FSK, PSK, QAM. Стр. 154-158."""
    import math as m
    svg = Svg(1180, 640, "Диаграммы созвездий (илл. 2.16-2.18, стр. 154-158)")

    PW, PH, GAP = 266, 300, 18
    X0, Y0 = 26, 78

    def panel(i, l1, l2, col, pts, hint):
        px, py = X0 + i * (PW + GAP), Y0
        svg.rect(px, py, PW, PH, "#fafafa", "#ccc", 1.2, 8)
        svg.text(px + PW / 2, py + 26, l1, 13.5, col, "middle", weight="bold")
        svg.text(px + PW / 2, py + 46, l2, 12.5, col, "middle", weight="bold")
        cx, cy, L = px + PW / 2, py + 200, 95
        svg.line(cx - L - 20, cy, cx + L + 20, cy, "#bbb", 1)
        svg.line(cx, cy - L - 20, cx, cy + L + 20, "#bbb", 1)
        svg.text(cx + L + 16, cy + 14, "I", 10.5, "#999")
        svg.text(cx + 6, cy - L - 10, "Q", 10.5, "#999")
        for (di, dq) in pts:
            svg.circle(cx + di * L, cy - dq * L, 5.5, col, "#fff", 1.5)
        svg.text(px + PW / 2, py + PH - 14, hint, 11, "#666", "middle")

    r45 = m.cos(m.radians(45))
    # ASK: 2 амплитуды, фаза фиксирована -> 2 точки на оси I
    panel(0, "ASK", "2 амплитуды · 1 бит/символ", "#1f77b4",
          [(0.25, 0), (0.8, 0)], "«0» и «1» — две амплитуды")
    # BPSK: 2 фазы
    panel(1, "PSK (BPSK)", "2 фазы · 1 бит/символ", "#1f77b4",
          [(0.8 * r45, 0.8 * r45), (-0.8 * r45, -0.8 * r45)], "фаза 0° и 180°")
    # QPSK: 4 фазы
    panel(2, "QPSK", "4 фазы · 2 бита/символ", "#2e7d29",
          [(0.8 * m.cos(m.radians(a)), 0.8 * m.sin(m.radians(a)))
           for a in (45, 135, 225, 315)], "45° · 135° · 225° · 315°")
    # QAM-16: 4 фазы x 4 амплитуды = 16
    q16 = []
    for a in (45, 135, 225, 315):
        for rr in (0.2, 0.4, 0.6, 0.8):
            q16.append((rr * m.cos(m.radians(a)), rr * m.sin(m.radians(a))))
    panel(3, "QAM-16", "4 × 4 = 16 точек · 4 бита/символ", "#d62728",
          q16, "16 точек — отсюда log₂16 = 4 бита")

    svg.text(590, 424, "Бод — это число СИМВОЛОВ в секунду.  Бит/с = бод × бит на символ.", 14.5, "#1a1a1a", "middle", weight="bold")
    svg.text(590, 452, "QAM-64 несёт 6 бит на символ, QAM-256 — 8. Модем V.32 при 2400 бод даёт 9600 бит/с: 2400 × 4 = 9600.", 12.5, "#666", "middle")

    svg.rect(30, 478, 1120, 96, "#eef3fb", "#4a6fa5", 1.2, 8)
    svg.text(52, 504, "Как читать созвездие", 13.5, "#4a6fa5", weight="bold")
    svg.text(52, 528, "Фаза — это угол отрезка от начала координат.  Амплитуда — длина отрезка.  Частота и фаза связаны,", 12, "#555")
    svg.text(52, 548, "поэтому модулировать их одновременно нельзя — совместно меняют амплитуду и фазу, отсюда название QAM.", 12, "#555")

    svg.text(590, 612, "FSK в созвездии не рисуется: там различается сама частота несущей — это другая система координат.", 12.5, "#666", "middle", style="italic")
    svg.text(590, 634, "Код Грея: соседние точки должны отличаться ровно одним битом, иначе всплеск шума испортит сразу несколько бит.", 12.5, "#666", "middle", style="italic")

    svg.save(f"{outdir}/_cst.svg")
    to_png(f"{outdir}/_cst.svg", f"{outdir}/ch2-constellations.png")


# ==================================================== 4. Мультиплексирование
def plot_multiplexing(outdir):
    """Стр. 158-170: FDM, OFDM, TDM, WDM, CDM — что именно делится."""
    svg = Svg(1180, 880, "Что именно делится в каждом способе мультиплексирования (разд. 2.4.4)")
    SX, SW, SH = 200, 460, 32
    cols = ["#cde8cd", "#ffe8b3", "#e6d0e8", "#cde0f0"]

    def axis(y, label):
        svg.line(SX, y, SX + SW, y, "#666", 1.4)
        svg.poly([(SX + SW, y), (SX + SW - 8, y - 4), (SX + SW - 8, y + 4)],
                 "#666", 1.4, fill="#666", close=True)
        svg.text(SX - 14, y + 5, label, 12.5, "#555", "end", weight="bold")

    def row(y, name, col, lines, draw):
        svg.text(56, y, name, 15.5, col, weight="bold")
        draw(y + 14)
        axis(y + 14 + SH + 18, lines[0])
        svg.text(SX, y + 14 + SH + 44, lines[1], 11.5, col)
        if len(lines) > 2:
            svg.text(SX, y + 14 + SH + 62, lines[2], 11.5, col)

    def draw_bands(y, n):
        w = SW / n
        for i in range(n):
            svg.rect(SX + i * w, y, w - 1.5, SH, cols[i % 4], "#333", 1.1)

    def draw_carriers(y):
        w = SW / 32
        for i in range(32):
            svg.rect(SX + i * w, y, w - 1, SH,
                     "#e6d9f0" if i % 2 == 0 else "#d9c2e9", "#aaa", 0.8)

    def draw_waves(y):
        for i in range(5):
            c = ["#ff6b6b", "#ffd93d", "#6bdc75", "#4d96ff", "#b983ff"][i]
            svg.rect(SX + i * (SW / 5), y, SW / 5 - 4, SH, c, "#333", 1.1)
            svg.text(SX + i * (SW / 5) + (SW / 5 - 4) / 2, y + 21, f"λ{i+1}", 12,
                     "#fff", "middle", weight="bold")

    def draw_cdma(y):
        for k, (col, dash) in enumerate([("#d62728", "6,4"), ("#1f77b4", "6,4"), ("#2e7d29", "2,3")]):
            pts = [(SX + i * (SW / 60), y + 3 + k * 10 + (7 if ((i // 3 + k) % 2 == 0) else 0))
                   for i in range(61)]
            svg.poly(pts, col, 1.8, dash=dash)
        for k, t in enumerate(["сигнал A", "сигнал B", "сигнал C"]):
            svg.text(SX + SW + 16, y + 12 + k * 11, t, 11,
                     ["#d62728", "#1f77b4", "#2e7d29"][k])

    row(80, "FDM", "#1f77b4",
        ["частота →", "Защитные полосы: голосовой канал 3100 Гц занимает 4000 Гц. Молчащий канал всё равно держит полосу."],
        lambda y: draw_bands(y, 4))
    row(196, "OFDM", "#7b4ea3",
        ["частота →",
         "АЧХ каждой несущей нулевая в центре соседней — защитные полосы не нужны, взамен вводится защитный",
         "интервал времени. Основа DMT в DSL и 802.11."],
        draw_carriers)
    row(330, "TDM", "#d62728",
        ["время →", "Нужна синхронизация потоков и защитные интервалы времени. STDM выдаёт слоты по статистике — это уже пакетная коммутация."],
        lambda y: draw_bands(y, 12))
    row(446, "WDM", "#b15928",
        ["длина волны →", "По сути FDM, но частота заменена на цвет. Разделение полностью пассивно — дифракционная решётка."],
        draw_waves)
    row(562, "CDM / CDMA", "#e68a00",
        ["одновременно",
         "Приёмник умножает принятое на тот же код, что и отправитель: чужой сигнал гаснет, свой — нет.",
         "Бит делится на 64 или 128 «чипов», поэтому полоса в m раз шире, чем у станции без CDMA."],
        draw_cdma)

    svg.rect(30, 700, 1120, 66, "#eef3fb", "#4a6fa5", 1.2, 8)
    svg.text(52, 726, "Аналогия из книги — зал ожидания в аэропорту", 13, "#4a6fa5", weight="bold")
    svg.text(52, 750, "TDM — пары говорят по очереди.   FDM — на разных высотах голоса.   CDMA — все одновременно, но на разных языках.", 12, "#555")

    svg.text(590, 800, "Главное различие — ось, по которой идёт разделение: частота, время, длина волны или код.", 13, "#666", "middle", style="italic")
    svg.text(590, 824, "OFDM — не шестой способ, а разновидность FDM с ортогональными несущими и защитным интервалом времени.", 12.5, "#666", "middle", style="italic")

    svg.save(f"{outdir}/_mx.svg")
    to_png(f"{outdir}/_mx.svg", f"{outdir}/ch2-multiplexing.png")


# ==================================================== 5. Спектры: расширение
def plot_spread(outdir):
    """FHSS, DSSS, UWB. Стр. 135–137."""
    svg = Svg(920, 620, "Расширение спектра: FHSS, DSSS, UWB (разд. 2.2, стр. 135–137)")
    py = 470          # базовая линия частот

    def freq_axis(x0, w, title, y0=py, marks=None):
        svg.line(x0, y0, x0 + w, y0, "#333", 1.4)
        svg.text(x0 + w / 2, y0 + 46, title, 13, "#1a1a1a", "middle")
        svg.text(x0, y0 + 26, "частота →", 11.5, "#666")
        if marks:
            for frac, lbl in marks:
                svg.line(x0 + w * frac, y0, x0 + w * frac, y0 + 7, "#333", 1.2)
                svg.text(x0 + w * frac, y0 + 22, lbl, 11, "#555", "middle")

    # исходный узкий сигнал
    svg.text(40, 100, "Узкий сигнал (несущая)", 13.5, "#1f77b4", weight="bold")
    svg.rect(300, 78, 26, 30, "#1f77b4", "none", 0)
    freq_axis(60, 380, "спектр")

    # FHSS: скачки
    svg.text(40, 200, "FHSS — псевдослучайные скачки", 13.5, "#d62728", weight="bold")
    import random
    random.seed(7)
    seq = [3, 1, 4, 0, 3, 2, 4, 1]
    bw = 380 / 8
    for i, k in enumerate(seq):
        svg.rect(60 + i * bw, 186, bw - 3, 22, "#d62728", "none", 0)
        svg.line(60 + i * bw, 208, 60 + (i + 1) * bw - 3, 208, "#d62728", 1.4)
    freq_axis(60, 380, "весь разрешённый диапазон")
    svg.text(460, 200, "Передача прыгает по каналам.", 12.5, "#555")
    svg.text(460, 220, "Вредная помеха портит лишь один канал.", 12.5, "#555")
    svg.text(460, 240, "Bluetooth: 1600 скачков/с.", 12.5, "#555", style="italic")

    # DSSS: умножение на код
    svg.text(40, 320, "DSSS — умножение на кодовую последовательность", 13.5, "#2e7d29",
             weight="bold")
    seq2 = [1, -1, 1, 1, -1, -1, 1, -1, 1, 1, 1, -1, -1, 1, -1, 1]
    cw = 380 / 32
    for i, v in enumerate(seq2):
        y = 300 + (0 if v > 0 else 18)
        svg.rect(60 + i * cw, y, cw, 18, "#2e7d29", "none", 0)
    freq_axis(60, 380, "тот же диапазон, но мощность «размазана»")
    svg.text(460, 320, "Каждый бит умножается на код из 11 «чипов» —", 12.5, "#555")
    svg.text(460, 340, "полоса растёт, зато сигнал невозможно", 12.5, "#555")
    svg.text(460, 360, "принять как обычный узкий сигнал.", 12.5, "#555", style="italic")

    # UWB
    svg.text(40, 560, "UWB — сверхширокополосная связь", 13.5, "#7b4ea3", weight="bold")
    svg.rect(60, 528, 380, 26, "#d9c2e9", "#7b4ea3", 1.5)
    svg.text(250, 546, "занимает сразу очень широкую полосу", 12.5, "#4a235a", "middle")
    svg.text(460, 546, "Дешевле: мощность не нужна, можно даже не использовать несущую.", 12.5, "#555")

    svg.save(f"{outdir}/_sp.svg")
    to_png(f"{outdir}/_sp.svg", f"{outdir}/ch2-spectrum-spreading.png")
# ==================================================== 6. Спутниковые орбиты
def plot_satellites(outdir):
    """Илл. 2.48, стр. 216. Числа — из книги."""
    svg = Svg(920, 600, "Спутниковые орбиты (илл. 2.48, стр. 216): высота против задержки")
    px0, py0, pw, ph = 150, 110, 320, 340
    svg.rect(px0, py0, pw, ph, "#0b1020", "none", 0)

    # Земля
    svg.circle(px0 + pw / 2, py0 + ph - 70, 62, "#1d4e89", "#4d94d9", 2)

    def orbit(km, col, label, delay, count):
        # логарифмическая шкала высоты
        r = 12 + (km / 35000) ** 0.5 * 118
        svg.circle(px0 + pw / 2, py0 + ph - 70, r, "none", col, 1.8, ) \
            if False else svg.circle(px0 + pw / 2, py0 + ph - 70, r, "none", col, 1.8)
        svg.circle(px0 + pw / 2, py0 + ph - 70 - r, 5, col)
        svg.text(px0 + pw / 2 + r * 0.72, py0 + ph - 70 - r, label, 12.5, col, weight="bold")
        svg.text(px0 + pw / 2 + r * 0.72, py0 + ph - 70 - r + 16,
                 f"{delay} мс · нужно {count}", 11.5, col)

    orbit(20000, "#ffd166", "MEO", "10", "1–7")
    orbit(35000, "#ef476f", "GEO", "270", "3")
    orbit(1500, "#06d6a0", "LEO", "1–7", "50")

    svg.text(px0 + pw / 2, py0 + ph + 26, "LEO — низкая орбита", 12.5, "#06d6a0", "middle")
    svg.text(px0 + pw / 2, py0 + ph + 46, "MEO — средняя орбита", 12.5, "#ffd166", "middle")
    svg.text(px0 + pw / 2, py0 + ph + 66, "GEO — геостационарная", 12.5, "#ef476f", "middle")

    # таблица чисел
    tx = 530
    svg.text(tx, 150, "Высота", 13, "#333", weight="bold")
    svg.text(tx + 110, 150, "Задержка", 13, "#333", weight="bold")
    svg.text(tx + 210, 150, "Спутников", 13, "#333", weight="bold")
    rows = [("35 000 км", "270 мс", "3", "#ef476f"),
            ("35–85 тыс. км", "10 мс", "1–7", "#ffd166"),
            ("до 10 000 км", "1–7 мс", "50", "#06d6a0")]
    y = 176
    for a, b, c, col in rows:
        svg.text(tx, y, a, 12.5, col)
        svg.text(tx + 110, y, b, 12.5, col, weight="bold")
        svg.text(tx + 210, y, c, 12.5, col)
        y += 24
    svg.line(tx, 160, tx + 300, 160, "#ccc", 1)

    svg.text(tx, y + 24, "Задержка растёт пропорционально высоте.", 12.5, "#555")
    svg.text(tx, y + 48, "GEO даёт 270 мс — онлайн-игры и голос там", 12.5, "#555")
    svg.text(tx, y + 70, "невозможны в принципе.", 12.5, "#555", style="italic")
    svg.text(tx, y + 102, "LEO — обратная сторона: спутников нужно", 12.5, "#555")
    svg.text(tx, y + 124, "много (50), и они быстро «умирают»", 12.5, "#555")
    svg.text(tx, y + 146, "из-за радиационных поясов.", 12.5, "#555", style="italic")

    svg.text(920 / 2, 580, "Ключ: спутников нужно столько, чтобы покрыть небо — чем выше орбита, тем меньше.",
             13, "#666", "middle", style="italic")

    svg.save(f"{outdir}/_sat.svg")
    to_png(f"{outdir}/_sat.svg", f"{outdir}/ch2-satellites.png")


if __name__ == "__main__":
    outdir = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(outdir, exist_ok=True)
    for name in [n for n in dir() if n.startswith("plot_")]:
        globals()[name](outdir)
    for f in os.listdir(outdir):
        if f.startswith("_") and f.endswith(".svg"):
            os.remove(os.path.join(outdir, f))
