#!/usr/bin/env bash
# Генерация структурных схем главы 4 (Таненбаум, «Компьютерные сети», 6-е изд.).
# Требуется только graphviz (dot) — он есть в системе по умолчанию.
# Запуск:  bash gen-ch4-diagrams.sh [каталог_для_png]
set -euo pipefail
OUT="${1:-.}"
mkdir -p "$OUT"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

# общие настройки оформления
COMMON='digraph {
  rankdir=TB; splines=ortho; nodesep=0.45; ranksep=0.55;
  bgcolor="#ffffff";
  fontname="DejaVu Sans"; fontsize=15;
  node [shape=box, style="rounded,filled", fillcolor="#eef3fb",
        color="#4a6fa5", fontname="DejaVu Sans", fontsize=12, penwidth=1.2];
  edge [color="#4a6fa5", fontname="DejaVu Sans", fontsize=11, penwidth=1.1];
}'

# ============================================================ двоичная экспоненциальная выдержка
cat > "$TMP/backoff.dot" <<'EOF'
digraph {
  rankdir=LR; nodesep=0.18; ranksep=0.35; bgcolor="#ffffff";
  fontname="DejaVu Sans"; fontsize=16;
  node [shape=plaintext, fontname="DejaVu Sans"];
  lab [label=<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="9" COLOR="#4a6fa5">
    <TR><TD BGCOLOR="#4a6fa5" COLSPAN="2"><FONT COLOR="white"><B>Двоичная экспоненциальная выдержка (Ethernet)</B></FONT></TD></TR>
    <TR><TD BGCOLOR="#dce7f7"><B>коллизия</B></TD><TD BGCOLOR="#dce7f7"><B>случайное число слотов из диапазона</B></TD></TR>
    <TR><TD ALIGN="CENTER">1</TD><TD ALIGN="CENTER">0 … 2¹−1 = 0 … 1</TD></TR>
    <TR><TD ALIGN="CENTER">2</TD><TD ALIGN="CENTER">0 … 2²−1 = 0 … 3</TD></TR>
    <TR><TD ALIGN="CENTER">3</TD><TD ALIGN="CENTER">0 … 2³−1 = 0 … 7</TD></TR>
    <TR><TD ALIGN="CENTER">4…9</TD><TD ALIGN="CENTER">0 … 2⁹−1 = 0 … 511</TD></TR>
    <TR><TD BGCOLOR="#ffe0e0"><B>10 и выше</B></TD><TD BGCOLOR="#ffe0e0"><B>диапазон заморожен: 0 … 1023</B></TD></TR>
    <TR><TD BGCOLOR="#ffd0d0"><B>16</B></TD><TD BGCOLOR="#ffd0d0"><B>отказ: ошибка возвращается в ОС</B></TD></TR>
  </TABLE>>];
}
EOF

# ============================================================ формат фрейма Ethernet
cat > "$TMP/frame.dot" <<'EOF'
digraph {
  rankdir=TB; nodesep=0.12; ranksep=0.3; bgcolor="#ffffff";
  fontname="DejaVu Sans"; fontsize=16; labeljust=l;
  node [shape=plaintext, fontname="DejaVu Sans"];
  dix [label=<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="7" COLOR="#333">
    <TR><TD BGCOLOR="#4a6fa5" COLSPAN="7"><FONT COLOR="white"><B>DIX Ethernet</B></FONT></TD></TR>
    <TR>
      <TD BGCOLOR="#e8e8e8">Преамбула<br/>8 Б</TD>
      <TD BGCOLOR="#cde8cd">адрес<br/>получателя<br/>6 Б</TD>
      <TD BGCOLOR="#cde8cd">адрес<br/>отправителя<br/>6 Б</TD>
      <TD BGCOLOR="#ffe8b3">Type<br/>2 Б</TD>
      <TD BGCOLOR="#f5f5f5">Данные<br/>0–1500 Б</TD>
      <TD BGCOLOR="#e8e8e8">Pad<br/>0–46 Б</TD>
      <TD BGCOLOR="#e8d0e8">CRC<br/>4 Б</TD>
    </TR></TABLE>>];

  ieee [label=<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="7" COLOR="#333">
    <TR><TD BGCOLOR="#4a6fa5" COLSPAN="7"><FONT COLOR="white"><B>IEEE 802.3</B></FONT></TD></TR>
    <TR>
      <TD BGCOLOR="#e8e8e8">Преамбула<br/>8 Б</TD>
      <TD BGCOLOR="#cde8cd">адрес<br/>получателя<br/>6 Б</TD>
      <TD BGCOLOR="#cde8cd">адрес<br/>отправителя<br/>6 Б</TD>
      <TD BGCOLOR="#ffe8b3">Length<br/>2 Б</TD>
      <TD BGCOLOR="#f5f5f5">Данные<br/>0–1500 Б</TD>
      <TD BGCOLOR="#e8e8e8">Pad<br/>0–46 Б</TD>
      <TD BGCOLOR="#e8d0e8">CRC<br/>4 Б</TD>
    </TR></TABLE>>];

  rule [label=<<TABLE BORDER="0" CELLSPACING="0" CELLPADDING="6">
    <TR><TD ALIGN="LEFT" BGCOLOR="#fffbe6">
      <FONT POINT-SIZE="13"><B>Правило 1997 года:</B> значение &lt; 0x600 (1536) читается как <B>Length</B>,<BR/>
      больше 0x600 — как <B>Type</B>. Значения Type всегда были &gt; 1500, поэтому старые карты<BR/>
      не сломались. Пример: <B>0x0800 = IPv4</B>, <B>0x0806 = ARP</B>, <B>0x8100 = тег 802.1Q</B>, <B>0x8808 = PAUSE</B>.</FONT>
    </TD></TR></TABLE>>];

  minf [label=<<TABLE BORDER="0" CELLSPACING="0" CELLPADDING="6">
    <TR><TD ALIGN="LEFT" BGCOLOR="#f0f7ff">
      <FONT POINT-SIZE="13"><B>Минимум 64 байта</B> (от адреса получателя до CRC).<BR/>
      Если данных &lt; 46 байт — добавляется <B>Pad</B>.<BR/>
      Причина не в красоте: время передачи должно быть <B>&gt; 2τ</B>, иначе отправитель<BR/>
      закончит раньше, чем вернётся шумовой всплеск, и решит, что коллизии не было.</FONT>
    </TD></TR></TABLE>>];

  { rank=same; dix; ieee; }
  dix -> rule [style=dashed, arrowhead=none];
  ieee -> minf [style=dashed, arrowhead=none];
}
EOF

# ============================================================ уровни устройств
cat > "$TMP/devices.dot" <<'EOF'
digraph {
  rankdir=TB; nodesep=0.3; ranksep=0.4; bgcolor="#ffffff";
  fontname="DejaVu Sans"; fontsize=16;
  node [shape=plaintext, fontname="DejaVu Sans"];

  app  [label=<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="7" COLOR="#555">
    <TR><TD BGCOLOR="#efefef"><FONT POINT-SIZE="11">уровень приложений</FONT></TD></TR>
    <TR><TD BGCOLOR="#ffffff"><B>шлюз приложений</B><BR/><FONT POINT-SIZE="11">email → SMS</FONT></TD></TR></TABLE>>];

  tr   [label=<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="7" COLOR="#555">
    <TR><TD BGCOLOR="#efefef"><FONT POINT-SIZE="11">транспортный уровень</FONT></TD></TR>
    <TR><TD BGCOLOR="#ffffff"><B>транспортный шлюз</B><BR/><FONT POINT-SIZE="11">TCP/IP ↔ SCTP</FONT></TD></TR></TABLE>>];

  net  [label=<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="7" COLOR="#555">
    <TR><TD BGCOLOR="#efefef"><FONT POINT-SIZE="11">сетевой уровень</FONT></TD></TR>
    <TR><TD BGCOLOR="#ffffff"><B>маршрутизатор</B><BR/><FONT POINT-SIZE="11">смотрит в IP-адрес (32/128 бит)</FONT></TD></TR></TABLE>>];

  dl   [label=<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="7" COLOR="#555">
    <TR><TD BGCOLOR="#efefef"><FONT POINT-SIZE="11">канальный уровень</FONT></TD></TR>
    <TR><TD BGCOLOR="#ffffff"><B>мост = коммутатор</B><BR/><FONT POINT-SIZE="11">смотрит в MAC-адрес (48 бит)</FONT></TD></TR></TABLE>>];

  ph   [label=<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="7" COLOR="#555">
    <TR><TD BGCOLOR="#efefef"><FONT POINT-SIZE="11">физический уровень</FONT></TD></TR>
    <TR><TD BGCOLOR="#ffffff"><B>повторитель</B> / <B>концентратор</B><BR/><FONT POINT-SIZE="11">адресов не знает, только усиливает сигнал</FONT></TD></TR></TABLE>>];

  { rank=same; app; tr; net; dl; ph; }
  app -> tr -> net -> dl -> ph [style=invis];
}
EOF

# ============================================================ интервалы 802.11
cat > "$TMP/intervals.dot" <<'EOF'
digraph {
  rankdir=TB; nodesep=0.12; ranksep=0.3; bgcolor="#ffffff";
  fontname="DejaVu Sans"; fontsize=16;
  node [shape=plaintext, fontname="DejaVu Sans"];

  t [label=<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="6" COLOR="#333">
    <TR><TD BGCOLOR="#4a6fa5"><FONT COLOR="white"><B>время →</B></FONT></TD>
        <TD BGCOLOR="#c8e6c9">SIFS</TD>
        <TD BGCOLOR="#fff9c4">DIFS</TD>
        <TD BGCOLOR="#ffe0b2">AIFS1</TD>
        <TD BGCOLOR="#ef9a9a">AIFS4</TD>
        <TD BGCOLOR="#e1bee7">EIFS</TD></TR>
  </TABLE>>];

  who [label=<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="6" COLOR="#333">
    <TR><TD BGCOLOR="#4a6fa5"><FONT COLOR="white"><B>кто ждёт</B></FONT></TD>
        <TD><FONT POINT-SIZE="11"><B>участник обмена:</B> ACK,<BR/>RTS/CTS, след. фрагмент</FONT></TD>
        <TD><FONT POINT-SIZE="11"><B>любая станция</B> для<BR/>нового фрейма данных</FONT></TD>
        <TD><FONT POINT-SIZE="11"><B>точка доступа</B><BR/>для голоса</FONT></TD>
        <TD><FONT POINT-SIZE="11"><B>точка доступа</B><BR/>для фона</FONT></TD>
        <TD><FONT POINT-SIZE="11">станция, принявшая<BR/><B>битый</B> фрейм</FONT></TD></TR>
  </TABLE>>];

  ord [label=<<TABLE BORDER="0" CELLSPACING="0" CELLPADDING="6">
    <TR><TD ALIGN="LEFT" BGCOLOR="#f7f7f7"><FONT POINT-SIZE="14">
      <B>Ключ к QoS — это порядок ожидания, а не приоритет в очереди.</B><BR/>
      Чем <I>короче</I> интервал, тем раньше станция вырвется в канал: SIFS &lt; AIFS1 &lt; DIFS &lt; AIFS4.<BR/>
      SIFS всегда самый короткий, иначе другая станция вмешается и разорвёт текущий обмен.
    </FONT></TD></TR></TABLE>>];
  t -> who [style=invis];
  who -> ord [style=invis];
}
EOF

# ============================================================ Bluetooth: фрейм
cat > "$TMP/btframe.dot" <<'EOF'
digraph {
  rankdir=TB; nodesep=0.12; ranksep=0.3; bgcolor="#ffffff";
  fontname="DejaVu Sans"; fontsize=16;
  node [shape=plaintext, fontname="DejaVu Sans"];
  base [label=<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="7" COLOR="#333">
    <TR><TD BGCOLOR="#4a6fa5" COLSPAN="4"><FONT COLOR="white"><B>Фрейм на базовой скорости</B></FONT></TD></TR>
    <TR>
      <TD BGCOLOR="#e8e8e8">Access code<br/>72 бит</TD>
      <TD BGCOLOR="#ffe8b3">Header<br/>54 бит = 18 × 3</TD>
      <TD BGCOLOR="#cde8cd">Data<br/>0–2744 бит</TD>
      <TD BGCOLOR="#e8d0e8">CRC<br/>16 бит</TD>
    </TR></TABLE>>];

  hdr [label=<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="6" COLOR="#c9a227">
    <TR><TD BGCOLOR="#fff8dc"><FONT POINT-SIZE="13">Заголовок 18 бит, повторён <B>3 раза</B> = 54 бит.<BR/>
    Приёмник сравнивает три копии каждого бита: совпали — берёт, иначе —<BR/>
    решает большинство. На 10 бит заголовка уходит 54 бита полосы —<BR/>
    цена дешёвых маломощных устройств (2,5 мВт).</FONT></TD></TR></TABLE>>];

  eff [label=<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="6" COLOR="#999">
    <TR><TD BGCOLOR="#f7f7f7"><FONT POINT-SIZE="13">
      <B>Почему эффективность всего 13 %:</B> 41 % уходит на стабилизацию частоты,<BR/>
      20 % — на заголовки, 26 % — на повторное кодирование.<BR/>
      Несмотря на 1 Мбит/с радиолинии, полнодуплексный голос всё равно занимает<BR/>
      64 000 бит/с в каждую сторону (800 нечётных слотов × 80 бит) —<BR/>
      и этого хватает ровно на один канал PCM.
    </FONT></TD></TR></TABLE>>];

  base -> hdr [style=dashed, arrowhead=none];
  hdr -> eff [style=dashed, arrowhead=none];
}
EOF

# ============================================================ двоичный обратный отсчёт
cat > "$TMP/countdown.dot" <<'EOF'
digraph {
  rankdir=TB; nodesep=0.15; ranksep=0.35; bgcolor="#ffffff";
  fontname="DejaVu Sans"; fontsize=16;
  node [shape=plaintext, fontname="DejaVu Sans"];

  tbl [label=<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="8" COLOR="#4a6fa5">
    <TR><TD BGCOLOR="#4a6fa5" COLSPAN="6"><FONT COLOR="white"><B>Протокол с двоичным обратным отсчётом</B></FONT></TD></TR>
    <TR><TD BGCOLOR="#dce7f7"><B>бит</B></TD><TD BGCOLOR="#dce7f7">0010</TD><TD BGCOLOR="#dce7f7">0100</TD><TD BGCOLOR="#dce7f7">1001</TD><TD BGCOLOR="#dce7f7">1010</TD><TD BGCOLOR="#dce7f7"><B>результат</B></TD></TR>
    <TR><TD ALIGN="CENTER"><B>старший</B></TD><TD ALIGN="CENTER">0</TD><TD ALIGN="CENTER">0</TD><TD ALIGN="CENTER">1</TD><TD ALIGN="CENTER">1</TD><TD ALIGN="CENTER"><B>1</B></TD></TR>
    <TR><TD ALIGN="CENTER">2</TD><TD ALIGN="CENTER" BGCOLOR="#eeeeee">–</TD><TD ALIGN="CENTER" BGCOLOR="#eeeeee">–</TD><TD ALIGN="CENTER">0</TD><TD ALIGN="CENTER">0</TD><TD ALIGN="CENTER"><B>0</B></TD></TR>
    <TR><TD ALIGN="CENTER">3</TD><TD ALIGN="CENTER" BGCOLOR="#eeeeee">–</TD><TD ALIGN="CENTER" BGCOLOR="#eeeeee">–</TD><TD ALIGN="CENTER" BGCOLOR="#ffd0d0">0<BR/>сдалась</TD><TD ALIGN="CENTER" BGCOLOR="#c8e6c9">1<BR/><B>победа</B></TD><TD ALIGN="CENTER"><B>1</B></TD></TR>
  </TABLE>>];

  rule [label=<<TABLE BORDER="0" CELLSPACING="0" CELLPADDING="6">
    <TR><TD ALIGN="LEFT" BGCOLOR="#f7f7f7"><FONT POINT-SIZE="13">
      <B>Арбитраж:</B> биты адресов складываются по ИЛИ прямо в канале. Стация, у которой в этом<BR/>
      бите стоял 0, а сумма дала 1, <B>сдаётся сразу</B> и ждёт следующего цикла.<BR/>
      Выигрывает станция с <B>наибольшим адресом</B> — приоритет жёстко привязан к номеру.<BR/>
      Эффективность: <B>d / (d + log₂N)</B> — вместо N бит накладных, как у битовой карты.
    </FONT></TD></TR></TABLE>>];
  tbl -> rule [style=dashed, arrowhead=none];
}
EOF

# ============================================================ адаптивный проход по дереву
cat > "$TMP/tree.dot" <<'EOF'
digraph {
  rankdir=TB; nodesep=0.2; ranksep=0.45; bgcolor="#ffffff";
  fontname="DejaVu Sans"; fontsize=15;
  node [shape=circle, style=filled, fillcolor="#eef3fb", color="#4a6fa5", fontname="DejaVu Sans", fontsize=13, width=0.42, fixedsize=true];
  edge [color="#4a6fa5", fontname="DejaVu Sans", fontsize=11];

  n1 [label="1"];
  n2 [label="2"]; n3 [label="3"];
  n4 [label="4"]; n5 [label="5"]; n6 [label="6"]; n7 [label="7"];
  A [label="A"]; B [label="B"]; C [label="C"]; D [label="D"];
  E [label="E"]; F [label="F"]; G [label="G"]; H [label="H"];

  n1 -> n2 [label="слот 1"]; n1 -> n3 [label="слот 1"];
  n2 -> n4 [label="слот 2"]; n2 -> n5 [label="слот 2"];
  n3 -> n6 [label="слот 2"]; n3 -> n7 [label="слот 2"];
  n4 -> A; n4 -> B; n5 -> C; n5 -> D;
  n6 -> E; n6 -> F; n7 -> G; n7 -> H;

  note [shape=note, style=filled, fillcolor="#fffbe6", color="#c9a227",
    fontname="DejaVu Sans", fontsize=11, width=2.6, fixedsize=false,
    label="Слот 0 — все станции.\nКоллизия в слоте 1 — сканируем узел 2.\nВсего станций q: старт с уровня\ni = log₂q, где 2⁻ⁱ·q = 1."];
  n1 -> note [style=dotted, arrowhead=none, color="#c9a227"];
}
EOF

# ============================================================ пикосеть и рассеянная сеть
cat > "$TMP/piconet.dot" <<'EOF'
digraph {
  rankdir=LR; nodesep=0.2; ranksep=0.5; bgcolor="#ffffff";
  fontname="DejaVu Sans"; fontsize=15;
  node [shape=box, style="rounded,filled", fillcolor="#eef3fb", color="#4a6fa5", fontname="DejaVu Sans", fontsize=12];
  edge [color="#4a6fa5", fontname="DejaVu Sans", fontsize=10];

  subgraph cluster_1 {
    label="Пикосеть 1"; color="#4a6fa5"; style="rounded"; fontname="DejaVu Sans"; fontsize=13;
    m1 [label="M\nглавный", fillcolor="#ffe8b3"];
    s1 [label="S"]; s2 [label="S"]; s3 [label="S"];
    p1 [label="S\nзапаркован", fillcolor="#eeeeee", style="rounded,filled,dashed"];
    m1 -> s1; m1 -> s2; m1 -> s3; m1 -> p1 [style=dashed, color="#999"];
  }

  bridge [label="S\nмост", fillcolor="#cde8cd"];
  m2 [label="M\nглавный", fillcolor="#ffe8b3"];
  subgraph cluster_2 {
    label="Пикосеть 2"; color="#4a6fa5"; style="rounded"; fontname="DejaVu Sans"; fontsize=13;
    s4 [label="S"]; s5 [label="S"]; s6 [label="S"]; s7 [label="S"];
  }
  m2 -> s4; m2 -> s5; m2 -> s6; m2 -> s7;
  s3 -> bridge -> m2 [color="#2e7d32", penwidth=2];

  fact [shape=note, style=filled, fillcolor="#fffbe6", color="#c9a227", fontsize=12, fontname="DejaVu Sans",
    label="1 главный + до 7 активных подчинённых\n+ до 255 запаркованных, радиус ~10 м\n\nПикосеть = централизованный TDM:\nглавный в чётные слоты, подчинённые\nв нечётные. Между подчинёнными связи нет.\nДве пикосети через мост = рассеянная сеть."];
  bridge -> fact [style=dotted, arrowhead=none, color="#c9a227"];
}
EOF

# ============================================================ устройства рядом: концентратор vs коммутатор
cat > "$TMP/hubswitch.dot" <<'EOF'
digraph {
  rankdir=LR; nodesep=0.18; ranksep=0.4; bgcolor="#ffffff";
  fontname="DejaVu Sans"; fontsize=15;
  node [shape=box, style="rounded,filled", fillcolor="#eef3fb", color="#4a6fa5", fontname="DejaVu Sans", fontsize=12];
  edge [color="#4a6fa5", fontname="DejaVu Sans", fontsize=10];

  subgraph cluster_hub {
    label="Концентратор (hub)"; color="#d62728"; style="rounded"; fontname="DejaVu Sans"; fontsize=13;
    h1 [label="PC 1"]; h2 [label="PC 2"]; h3 [label="PC 3"];
    hub [label="концентратор\nОДНА область коллизий\nна все порты", fillcolor="#ffd6d6"];
    h1 -> hub; h2 -> hub; h3 -> hub;
  }
  hubsw [shape=note, label="CSMA/CD нужен.\nВсе делят одну полосу.\n promiscuous-трафик\nвиден всем", fillcolor="#ffecec", color="#d62728"];

  subgraph cluster_sw {
    label="Коммутатор (switch)"; color="#2e7d32"; style="rounded"; fontname="DejaVu Sans"; fontsize=13;
    s1 [label="PC 1"]; s2 [label="PC 2"]; s3 [label="PC 3"];
    sw [label="коммутатор\nу каждого порта СВОЯ\nобласть коллизий", fillcolor="#d6f5d6"];
    s1 -> sw; s2 -> sw; s3 -> sw;
  }
  swnote [shape=note, label="Дуплекс => коллизий нет,\nCSMA/CD не нужен.\nРазные порты шлют\nодновременно", fillcolor="#eafaea", color="#2e7d32"];

  hub -> hubsw [style=dotted, arrowhead=none];
  sw -> swnote [style=dotted, arrowhead=none];
  hub -> sw [style=invis, weight=3];
}
EOF

# ============================================================ связующее дерево
cat > "$TMP/spanning.dot" <<'EOF'
digraph {
  rankdir=LR; nodesep=0.22; ranksep=0.55; bgcolor="#ffffff";
  fontname="DejaVu Sans"; fontsize=15;
  node [shape=box, style="rounded,filled", fillcolor="#eef3fb", color="#4a6fa5", fontname="DejaVu Sans", fontsize=12];
  edge [fontname="DejaVu Sans", fontsize=10];

  b1 [label="B1\nкорень\nнаименьший MAC", fillcolor="#c8e6c9"];
  b2 [label="B2"]; b3 [label="B3"]; b4 [label="B4"]; b5 [label="B5"];

  b1 -> b2 [label="1 шаг", color="#2e7d32", penwidth=2.2];
  b1 -> b3 [label="1 шаг", color="#2e7d32", penwidth=2.2];
  b2 -> b4 [label="2 шага", color="#2e7d32", penwidth=2.2];
  b3 -> b5 [label="2 шага", color="#2e7d32", penwidth=2.2];

  b2 -> b5 [label="лишнее\n→ блокируется", color="#d62728", style=dashed, penwidth=1.6];
  b3 -> b4 [label="лишнее\n→ блокируется", color="#d62728", style=dashed, penwidth=1.6];

  rule [shape=note, style=filled, fillcolor="#fffbe6", color="#c9a227", fontsize=12, fontname="DejaVu Sans",
    label="Шаг 1: корнем становится мост\nс наименьшим идентификатором (из MAC).\n\nШаг 2: каждый считает кратчайший\nпуть до корня и отключает порты,\nне входящие в этот путь.\n\nРезультат — поддерево без циклов,\nпоэтому лавинная адресация\nне зацикливается.\n\nIEEE 802.1D, автор алгоритма —\nРадья Перлман."];
  b1 -> rule [style=dotted, arrowhead=none, color="#c9a227"];
}
EOF

# ============================================================ ретроградный обмен в 802.1Q
cat > "$TMP/vlan.dot" <<'EOF'
digraph {
  rankdir=LR; nodesep=0.25; ranksep=0.5; bgcolor="#ffffff";
  fontname="DejaVu Sans"; fontsize=15;
  node [shape=box, style="rounded,filled", fontname="DejaVu Sans", fontsize=12];
  edge [fontname="DejaVu Sans", fontsize=10];

  pc1 [label="PC<br/>VLAN 4", fillcolor="#cde8cd", color="#2e7d32"];
  b1  [label="B1\nтаблица портов:\nп1→VLAN 4", fillcolor="#eef3fb", color="#4a6fa5"];
  b2  [label="B2", fillcolor="#eef3fb", color="#4a6fa5"];
  pc2 [label="PC\nVLAN 4", fillcolor="#cde8cd", color="#2e7d32"];
  legacy [label="старый PC\nбез 802.1Q", fillcolor="#e0e0e0", color="#888"];
  b3  [label="B3\nтег удаляет", fillcolor="#eef3fb", color="#4a6fa5"];

  pc1 -> b1 -> b2 -> b3 -> pc2 [label="фрейм с тегом VLAN 4", color="#2e7d32", penwidth=2];
  b3 -> legacy [label="обычный фрейм 802.3", color="#888", style=dashed];

  note [shape=note, style=filled, fillcolor="#f0f7ff", color="#4a6fa5", fontsize=12, fontname="DejaVu Sans",
    label="Тег добавляет ПЕРВЫЙ\nVLAN-совместимый мост\nна пути и удаляет ПОСЛЕДНИЙ.\n\nПоэтому менять формат фрейма\nне пришлось: компьютеры\nтега не видят.\n\n+4 байта => лимит фрейма\nподнят с 1518 до 1522."];
  b2 -> note [style=dotted, arrowhead=none];
}
EOF

render() {
  dot -Tpng -Gdpi=110 "$TMP/$1" -o "$OUT/$2"
  echo "  $2"
}

echo "Генерация схем главы 4:"
render backoff.dot     ch4-backoff.png
render frame.dot       ch4-ethernet-frame.png
render devices.dot     ch4-devices-layers.png
render intervals.dot   ch4-80211-intervals.png
render btframe.dot     ch4-bluetooth-frame.png
render countdown.dot   ch4-binary-countdown.png
render tree.dot        ch4-contention-tree.png
render piconet.dot     ch4-bluetooth-piconet.png
render hubswitch.dot   ch4-hub-vs-switch.png
render spanning.dot    ch4-spanning-tree.png
render vlan.dot        ch4-vlan-tagging.png