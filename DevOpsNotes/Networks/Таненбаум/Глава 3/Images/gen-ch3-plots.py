#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Графики для главы 3 (Таненбаум, «Компьютерные сети», 6-е изд.).
Рисует кривые и диаграммы прямо в SVG (без matplotlib), затем конвертирует в PNG
через rsvg-convert. Числа взяты из текста глав; ссылки на страницы указаны в комментариях.

Запуск:  python3 gen-ch3-plots.py [каталог_для_png]
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


# ==================================================== 7. Коды: Хэмминг против CRC
def plot_codes(outdir):
    """Стр. 252-265: корректирующие и обнаруживающие коды, пример Хэмминга (11,7)."""
    svg = Svg(1180, 920, "Обнаружение или коррекция? (разд. 3.2, стр. 252-265)")
    pos = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    par = {1, 2, 4, 8}
    PITCH, CW, BX, BW, BP = 92, 84, 190, 54, 62

    # --- две стратегии
    for i, (name, lines, col) in enumerate([
            ("КОД ХЭММИНГА — корректирующий", [
                "По синдрому точно указывает, какой бит сломан, и восстанавливает",
                "его на месте. За это платит 2ᵐ проверочных бит."], "#c05a1e"),
            ("CRC — обнаруживающий", [
                "Делит принятое на образующий многочлен. Ненулевой остаток →",
                "«переспроси». Не исправляет ничего."], "#2e7d29")]):
        x = 40 + i * 560
        svg.rect(x, 76, 520, 100, "#fafafa", col, 1.8, 8)
        svg.text(x + 260, 104, name, 15, col, "middle", weight="bold")
        for k, t in enumerate(lines):
            svg.text(x + 260, 132 + k * 20, t, 12, "#555", "middle")
    svg.text(300, 212, "надёжный канал → дешевле обнаружить и повторить", 12, "#2e7d29", "middle")
    svg.text(860, 212, "шумный канал → повтор не поможет, нужна коррекция", 12, "#c05a1e", "middle")
    svg.text(40, 244, "Смешивать можно: ADSL использует Рида — Соломона (FEC) + 1-байтный CRC одновременно.", 12, "#666")

    # --- раскладка битов кода (11,7)
    y = 296
    svg.text(40, y, "Код Хэмминга (11, 7): r = 4 проверочных бита, m = 7 бит данных", 14, "#1a1a1a", weight="bold")
    svg.text(40, y + 20, "Проверочные биты стоят на позициях 1, 2, 4, 8 — то есть на степенях двойки. Жёлтый — проверочный, зелёный — данные.", 12, "#666")
    for k, p in enumerate(pos):
        isp = p in par
        svg.rect(40 + k * PITCH, y + 32, CW, 26, "#ffd93d" if isp else "#cde8cd", "#333", 1.2)
        svg.text(40 + k * PITCH + CW / 2, y + 50, f"{'p' if isp else 'm'}{p}", 12, "#333", "middle", weight="bold")
    svg.text(40, y + 78, "Бит данных k проверяют только те проверочные биты, номера которых входят в разложение k:", 11.5, "#555")
    svg.text(40, y + 96, "11 = 8 + 2 + 1  →  бит 11 проверяют p1, p2 и p8.        29 = 16 + 8 + 4 + 1  →  p1, p4, p8, p16.", 11.5, "#c05a1e", mono=True)

    # --- пример из илл. 3.6
    y = 428
    svg.text(40, y, "Разбор примера (илл. 3.6, стр. 256): сообщение «A» = 1000001, ошибка в бите 5", 14, "#1a1a1a", weight="bold")
    for k, p in enumerate(pos):
        svg.text(BX + k * BP + BW / 2, y + 24, f"{'p' if p in par else 'm'}{p}", 11, "#888", "middle")
    rows = [
        ("сообщение", "1000001", None),
        ("отправлено", "00100001001", "#333"),
        ("принято", "00101001001", "#d62728"),
    ]
    ry = y + 38
    for label, bits, col in rows:
        svg.text(40, ry + 16, label, 11.5, "#555")
        for i, ch in enumerate(bits):
            svg.rect(BX + i * BP, ry, BW, 22, "#f5f5f5" if col is None else "#eef3fb",
                     "#999" if col is None else col, 1.1)
            svg.text(BX + i * BP + BW / 2, ry + 16, ch, 12.5, col or "#666", "middle",
                     weight="bold", mono=True)
        ry += 28
    svg.text(BX, ry + 14, "ошибка пришлась на m5 — на схеме это пятая клетка слева", 11.5, "#d62728")
    svg.text(BX, ry + 36, "Синдром: проверки p8, p4, p2, p1 дают 0101 = 4 + 1 = 5  →  ошибка в бите 5. Инвертируем его, отбрасываем проверочные → снова «A».", 12, "#2e7d29")
    svg.text(BX, ry + 56, "Минимальное расстояние кода = 3 = 2·1 + 1  →  исправляет одиночные ошибки или обнаруживает двойные.", 12, "#2e7d29")

    # --- формула (3.1) и таблица m
    y = 632
    svg.text(40, y, "Формула (3.1) — нижний предел проверочных бит", 13.5, "#1a1a1a", weight="bold")
    svg.rect(40, y + 14, 500, 46, "#fff8dc", "#e68a00", 1.4, 6)
    svg.text(58, y + 44, "m + r + 1 ≤ 2ʳ", 14.5, "#333", mono=True, weight="bold")
    svg.text(190, y + 44, "для блока 1000 бит → r = 10", 12.5, "#c05a1e")
    svg.text(600, y, "Сколько данных даёт m проверочных бит", 13.5, "#1a1a1a", weight="bold")
    for i, (m, d) in enumerate([(3, 7), (4, 15), (5, 31), (6, 63), (7, 127)]):
        x = 600 + i * 108
        svg.rect(x, y + 16, 98, 44, "#ffe8b3", "#c05a1e", 1.3)
        svg.text(x + 49, y + 36, f"m={m}", 11.5, "#333", "middle", weight="bold")
        svg.text(x + 49, y + 54, f"{d} бит", 11.5, "#c05a1e", "middle")

    # --- численное сравнение
    y = 742
    svg.text(40, y, "Почему в надёжном канале дешевле обнаружить и повторить (стр. 260), накладные на 1 Мбит данных", 13.5, "#1a1a1a", weight="bold")
    svg.rect(40, y + 14, 1100, 96, "#fafafa", "#bbb", 1.2, 6)
    svg.text(64, y + 42, "бит чётности:  ошибок 1 на каждые 1000 блоков  →  повтор 1001 бит  →  итого 2001 бит накладных", 12.5, "#2e7d29")
    svg.text(64, y + 66, "код Хэмминга:  исправляет на месте,  но платит 10 000 бит проверки", 12.5, "#c05a1e")
    svg.text(64, y + 92, "В надёжном канале CRC в 5 раз дешевле. В шумном повтор не помогает — и выигрывает Хэмминг.", 12.5, "#555")

    svg.text(590, 890, "CRC не исправляет ничего: он лишь сообщает «кадр испорчен, переспроси».", 13, "#666", "middle", style="italic")

    svg.save(f"{outdir}/_cd.svg")
    to_png(f"{outdir}/_cd.svg", f"{outdir}/ch3-error-codes.png")


# ==================================================== 8. Скорость и размер кадра CRC
def plot_crc_power(outdir):
    """Стр. 259–265: вероятность необнаруженной ошибки для кодов."""
    svg = Svg(920, 600, "Вероятность необнаруженной ошибки (илл. 3.8–3.9, стр. 259–265)")
    X, Y = axes(svg, (0, 1600), (0, 1e-5), "длина кадра, бит", "вероятность, что ошибка не обнаружена",
                [0, 200, 400, 800, 1200, 1600], [1e-5], bottom=170,
                xfmt=lambda v: f"{v:g}", yfmt=lambda v: "1e-5")

    # оси логарифмические по смыслу: рисуем обратную зависимость 2^-r для r = 16 и 32
    def curve_for(r):
        return [(x, y) for x, y in
                curve(X, Y, lambda f: 2.0 ** (-r * f / 32.0), 0, 1600)]
    # вместо абсолютных значений покажем форму: чем больше бит проверки, тем круче спад
    svg.poly(curve(X, Y, lambda f: 10 ** (-(f / 1600) * 1.6), 0, 1600), "#d62728", 2.8)
    svg.poly(curve(X, Y, lambda f: 10 ** (-(f / 1600) * 3.4), 0, 1600), "#2e7d29", 2.8)
    svg.text(X(420), Y(10 ** -(420 / 1600 * 1.6)) - 12, "16-разрядная проверка", 12.5, "#d62728", weight="bold")
    svg.text(X(900), Y(10 ** -(900 / 1600 * 3.4)) - 12, "32-разрядная проверка", 12.5, "#2e7d29", weight="bold")

    svg.text(460, 530, "Схема условная: показана только сама форма зависимости.", 12.5, "#666", "middle", style="italic")
    svg.text(460, 552, "Главное из книги: вероятность необнаруженной ошибки мала и стремится к нулю,",
             13, "#666", "middle", style="italic")
    svg.text(460, 574, "а вот одиночная ошибка всегда обнаруживается — если её не «съел» код Хэмминга.",
             13, "#666", "middle", style="italic")

    svg.save(f"{outdir}/_crc.svg")
    to_png(f"{outdir}/_crc.svg", f"{outdir}/ch3-crc-power.png")


# ==================================================== 11. Формирование фрейма
def plot_framing(outdir):
    """Стр. 246-250: четыре метода маркировки границ фрейма."""
    svg = Svg(1180, 900, "Четыре способа найти границы фрейма (разд. 3.1.2, стр. 246-250)")

    def header(y, num, name, col, note):
        svg.circle(56, y + 4, 15, col)
        svg.text(56, y + 9, str(num), 14, "#fff", "middle", weight="bold")
        svg.text(86, y - 2, name, 15, col, weight="bold")
        svg.text(86, y + 16, note, 12, "#666")

    def cell(x, y, w, txt, fill, txtcol="#fff", size=11.5):
        svg.rect(x, y, w, 26, fill, "#333", 1.1)
        svg.text(x + w / 2, y + 18, txt, size, txtcol, "middle", weight="bold", mono=True)

    def mono(x, y, s, col="#333", size=11.5):
        svg.text(x, y, s, size, col, "start", mono=True)

    # --- 1
    y = 86
    header(y, 1, "Подсчёт байтов", "#c05a1e",
           "В заголовке — число байт фрейма. Практически НЕ применяется.")
    for i, t in enumerate(["5", "5", "8", "8"]):
        cell(90 + i * 56, y + 34, 52, t, "#ffe8b3", "#333")
    mono(340, y + 52, "илл. 3.3(а): фреймы 5, 5, 8, 8 байт", 11.5, "#888")
    mono(340, y + 74, "ошибка в одном бите счётчика (5 → 7)  →  синхронизация потеряна НАВСЕГДА", 11.5, "#c05a1e")

    # --- 2
    y = 216
    header(y, 2, "Флаговые байты + байт-стаффинг", "#2e7d29",
           "FLAG = 0x7E. Два соседних флага = граница. ESC = 0x7D.  Упрощённая модель PPP.")
    for i, (t, c) in enumerate([("7E", "#2e7d29"), ("41", "#cde8cd"), ("42", "#cde8cd"),
                                ("7D", "#ffd93d"), ("5E", "#ffe8b3"), ("43", "#cde8cd"),
                                ("7E", "#2e7d29")]):
        cell(90 + i * 50, y + 34, 46, t, c, "#ffffff" if t == "7E" else "#333")
    mono(470, y + 52, "данные содержали 7E → перед ним вставлен 7D, а 5E = 7E XOR 0x20", 11.5, "#888")
    mono(470, y + 74, "Накладные расходы: без флагов ≈ 100 байт; одни флаги ≈ 200 байт", 11.5, "#2e7d29")

    # --- 3
    y = 356
    header(y, 3, "Сигнальные биты + бит-стаффинг", "#4a6fa5",
           "Флаг 01111110. После пяти единиц вставляется 0.  Применён в HDLC.")
    mono(90, y + 52, "память:  01101111 11111111 11111111 0010      24 бита", 11.5, "#333")
    mono(90, y + 76, "линия:   01101111 0 11111 0 11111 0 0010     27 бит", 11.5, "#4a6fa5")
    mono(90, y + 100, "три вставленных нуля; получатель удаляет 0 после пяти единиц", 11.5, "#888")
    mono(620, y + 52, "Плюс: размер фрейма в битах — ЛЮБОЙ, не кратен 8", 11.5, "#4a6fa5")
    mono(620, y + 76, "Минус: накладные расходы ≈ 12,5 % (1 бит на байт)", 11.5, "#4a6fa5")
    mono(620, y + 100, "Гарантирует синхронизацию физ. уровня — применяется в USB", 11.5, "#888")

    # --- 4
    y = 496
    header(y, 4, "Запрещённые сигналы физического уровня", "#7b4ea3",
           "Используются «нарушения правил кодирования».  В линии 4B/5B не занято 16 из 32 сигналов.")
    for i, t in enumerate(["11000", "00101", "10110", "11000"]):
        cell(90 + i * 60, y + 34, 56, t, "#e6d9f0", "#333")
    mono(350, y + 52, "11000 = начало фрейма,  11111 = свободная линия", 11.5, "#888")
    mono(350, y + 74, "Границы ищутся простейшим сканированием; данные не раздуваются", 11.5, "#7b4ea3")

    # --- преамбула
    y = 640
    svg.rect(40, y, 1100, 96, "#fafafa", "#bbb", 1.2, 6)
    svg.text(64, y + 26, "Общее для Ethernet и 802.11: преамбула (preamble)", 14, "#1a1a1a", weight="bold")
    svg.text(64, y + 50, "Фрейм начинается с чётко заданного шаблона — по нему приёмник настраивает уровень", 12, "#555")
    svg.text(64, y + 68, "и тактовую частоту ещё до прихода данных.  У 802.11 преамбула — 72 бита.", 12, "#555")
    svg.text(64, y + 86, "Вслед за преамбулой в заголовке идёт поле длины (счётчик битов).", 12, "#555")

    svg.text(590, 782, "Главное различие: первые два метода работают с байтами, третий — с битами,", 13, "#666", "middle", style="italic")
    svg.text(590, 806, "четвёртый вообще не трогает данные — он эксплуатирует избыточность кода.", 13, "#666", "middle", style="italic")
    svg.text(590, 838, "Подсчёт байтов провалился; остальные три работают.  Илл. 3.5 — разбор бит-стаффинга.", 13, "#666", "middle", style="italic")
    svg.text(590, 870, "Метод 2 — байт-ориентированный (PPP), метод 3 — бит-ориентированный (HDLC).", 13, "#666", "middle", style="italic")

    svg.save(f"{outdir}/_fr.svg")
    to_png(f"{outdir}/_fr.svg", f"{outdir}/ch3-framing.png")


# ==================================================== 12. Лестница протоколов 1-6
def plot_protocols(outdir):
    """Стр. 271-295: шесть протоколов и что добавляет каждый."""
    svg = Svg(1180, 990, "Шесть протоколов канального уровня (гл. 3, стр. 271-295)")
    protos = [
        ("1", "Утопия", "#8a8a8a", "симплексный, идеальный канал", "ничего"),
        ("2", "Остановка и ожидание", "#4a9e4a", "симплексный, идеальный канал", "+ управление потоком"),
        ("3", "PAR / ARQ", "#2e7d29", "ненадёжный канал, 1 бит номера", "+ номера и подтверждения"),
        ("4", "Окно 1 бит", "#1f6fb2", "дуплексный канал", "+ вложенные подтверждения"),
        ("5", "Возврат к n", "#c05a1e", "MAX_SEQ = 7, номера 0…7", "+ конвейер, окно растёт"),
        ("6", "Выборочный повтор", "#d62728", "NR_BUFS = 4, окно ≤ половины", "+ буферизация и NAK"),
    ]
    y = 78
    for idx, (num, name, col, cond, add) in enumerate(protos):
        svg.rect(40, y, 300, 54, col, "#333", 1.2, 6)
        svg.text(60, y + 34, num, 22, "#fff", "start", weight="bold")
        svg.text(94, y + 26, name, 13, "#fff", "start", weight="bold")
        svg.text(94, y + 43, add, 11, "#ffffff", "start")
        svg.text(360, y + 33, cond, 12.5, "#333")
        if idx < len(protos) - 1:
            svg.line(58, y + 54, 58, y + 66, "#bbb", 1.4)
            svg.poly([(53, y + 58), (63, y + 58), (58, y + 66)], "#bbb", 0, fill="#bbb", close=True)
        y += 66

    # окно
    y = 500
    svg.text(40, y, "Протокол 6: восемь номеров, но буферов только четыре", 14, "#1a1a1a", weight="bold")
    svg.text(40, y + 21, "Окно не должно перекрывать само себя после сдвига — иначе повтор будет принят за новый фрейм.", 12, "#666")
    for i in range(8):
        inwin = i < 4
        svg.rect(60 + i * 56, y + 36, 52, 32, "#ffe8b3" if inwin else "#f2f2f2", "#333", 1.2)
        svg.text(60 + i * 56 + 26, y + 57, str(i), 13.5, "#333", "middle", weight="bold")
    svg.rect(60, y + 36, 4 * 56, 32, "none", "#c05a1e", 2.4)
    svg.text(60, y + 86, "окно = буферы 0…3   →   фрейм i кладётся в буфер i mod 4", 12, "#c05a1e")

    # 2BD+1
    y = 640
    svg.text(40, y, "Размер окна через полосу и задержку (стр. 284)", 14, "#1a1a1a", weight="bold")
    svg.rect(40, y + 16, 1100, 104, "#eef3fb", "#4a6fa5", 1.4, 6)
    svg.text(60, y + 42, "BD = полоса × задержка в одну сторону ÷ бит во фрейме   →   BD измеряется во фреймах", 13, "#333", mono=True)
    svg.text(60, y + 66, "w = 2·BD + 1        +1 — потому что подтверждение уходит только после полного фрейма", 13, "#333", mono=True)
    svg.text(60, y + 92, "Пример: 50 Кбит/с × 250 мс ÷ 1000 бит = BD 12,5 фрейма  →  w = 26 фреймов", 13, "#c05a1e", mono=True)

    # go-back-n vs selective
    y = 800
    svg.text(40, y, "Возврат к n против выборочного повтора (илл. 3.18): кадр 2 потерян", 14, "#1a1a1a", weight="bold")
    for k, (title, col, fills, note) in enumerate([
            ("Возврат к n", "#c05a1e",
             ["#c8e6c9", "#c8e6c9", "#ffcdd2", "#eeeeee", "#eeeeee"],
             "0 и 1 приняты; 3 и 4 отброшены, повторить придётся всё"),
            ("Выборочный повтор", "#2e7d29",
             ["#c8e6c9", "#c8e6c9", "#ffcdd2", "#ffe8b3", "#ffe8b3"],
             "0 и 1 приняты; 3 и 4 лежат в буфере, повторяется только 2")]):
        x = 60 + k * 540
        svg.text(x, y + 28, title, 13, col, weight="bold")
        for i in range(5):
            svg.rect(x + i * 42, y + 40, 38, 26, fills[i], "#333", 1.1)
            svg.text(x + i * 42 + 19, y + 58, str(i), 12, "#333", "middle")
        svg.text(x, y + 90, note, 11.5, "#555")
        svg.text(x, y + 110, "окно получателя = 1" if k == 0 else "окно получателя > 1, нужен буфер",
                 11, col, style="italic")
    for i, (lbl, c) in enumerate([("принят", "#c8e6c9"), ("потерян", "#ffcdd2"),
                                  ("отброшен", "#eeeeee"), ("в буфере", "#ffe8b3")]):
        svg.rect(60 + i * 130, y + 140, 20, 14, c, "#333", 1)
        svg.text(86 + i * 130, y + 151, lbl, 11, "#555")

    svg.save(f"{outdir}/_pr.svg")
    to_png(f"{outdir}/_pr.svg", f"{outdir}/ch3-protocols.png")


if __name__ == "__main__":
    outdir = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(outdir, exist_ok=True)
    for name in [n for n in dir() if n.startswith("plot_")]:
        globals()[name](outdir)
    for f in os.listdir(outdir):
        if f.startswith("_") and f.endswith(".svg"):
            os.remove(os.path.join(outdir, f))
