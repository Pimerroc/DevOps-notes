#!/usr/bin/env bash
# brief.sh — собирает детерминированный markdown-брифинг состояния vault.
#
# Использование:
#   brief.sh morning
#   brief.sh evening
#
# Контракт: только читает файлы, ничего не меняет. Вывод — в stdout.
# Источник истины — заметки, а не состояние модели.

set -euo pipefail

MODE="${1:-}"
case "$MODE" in
  morning|evening) ;;
  -h|--help)
    sed -n '2,9p' "$0"
    exit 0
    ;;
  *)
    echo "usage: brief.sh morning|evening" >&2
    exit 2
    ;;
esac

SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="${VAULT_ROOT:-$(cd "$SELF_DIR/../../.." && pwd)}"
N="$ROOT/DevOpsNotes/DevOps"
BOARD="$N/Board.md"
ROADMAP="$N/Roadmap.md"
QUEUE="$N/Review Queue.md"
LOG="$N/Learning Log.md"

for f in "$BOARD" "$ROADMAP" "$QUEUE" "$LOG"; do
  if [[ ! -r "$f" ]]; then
    echo "brief: нет доступа к $f" >&2
    exit 1
  fi
done

TODAY="$(date +%F)"
case "$(date +%u)" in
  1) DOW=Пн ;; 2) DOW=Вт ;; 3) DOW=Ср ;; 4) DOW=Чт ;;
  5) DOW=Пт ;; 6) DOW=Сб ;; 7) DOW=Вс ;;
  *) DOW=?? ;;
esac
TZ_NAME="$(timedatectl show -p Timezone --value 2>/dev/null || date +%Z)"

h2() { printf '\n## %s\n\n' "$1"; }
trim() { sed -E 's/^[[:space:]]+|[[:space:]]+$//g'; }

# --- Board: блок «Сегодня» ---------------------------------------------------
board_today() {
  awk '
    /^## Сегодня/ { inside = 1; print; next }
    inside && /^## / { exit }
    inside { print }
  ' "$BOARD"
}

BOARD_DAY="$(grep -m1 '^## Сегодня' "$BOARD" 2>/dev/null | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' | head -1 || true)"
BOARD_BLOCK="$(board_today)"
BOARD_MIN="$(printf '%s\n' "$BOARD_BLOCK" | grep -c '^- \[ \] \*\*MIN' || true)"
BOARD_OPEN="$(printf '%s\n' "$BOARD_BLOCK" | grep -c '^- \[ \]' || true)"
BOARD_DONE="$(printf '%s\n' "$BOARD_BLOCK" | grep -c '^- \[x\]' || true)"

# --- Roadmap: текущий этап ---------------------------------------------------
STAGE_NUM="$(grep -oE '^### Этап [0-9]+' "$ROADMAP" 2>/dev/null | head -1 | grep -oE '[0-9]+' || true)"
STAGE_ROW=""
STAGE_DAYS=""
if [[ -n "$STAGE_NUM" ]]; then
  STAGE_ROW="$(awk -F'|' -v n="$STAGE_NUM" '
    $1 ~ /^[[:space:]]*$/ && $2 ~ ("^[[:space:]]*" n "[[:space:]]*$") { print; exit }
  ' "$ROADMAP" | trim || true)"
  STAGE_DAYS="$(awk -v n="$STAGE_NUM" '
    $0 ~ ("^### Этап " n " —") { inside = 1; next }
    inside && /^## / { exit }
    inside && /^\|/ { print }
  ' "$ROADMAP" | trim | head -12 || true)"
fi

# --- Review Queue: просроченное и на сегодня ---------------------------------
REVIEW_DUE="$(awk -F'|' -v today="$TODAY" '
  {
    d = $4; st = $6
    gsub(/^[ \t]+|[ \t]+$/, "", d)
    gsub(/^[ \t]+|[ \t]+$/, "", st)
    if (d ~ /^[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]$/ && d <= today && st != "done") {
      printf "|%s|%s|%s|%s|\n", $2, $3, $4, $5
    }
  }
' "$QUEUE" | head -10 || true)"

# --- Learning Log: последние сессии -----------------------------------------
LOG_TAIL="$(awk -F'|' '
  $2 ~ /[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]/ { print }
' "$LOG" | tail -3 || true)"

# --- Незавершённый фактчек ---------------------------------------------------
UNVERIFIED="$(rg -l --glob '*.md' '^verified: false' "$ROOT/DevOpsNotes" 2>/dev/null \
  | sed "s|^$ROOT/||" | head -10 || true)"

# --- Git: что грязно ---------------------------------------------------------
GIT_DIRTY="$(git -C "$ROOT" status --short 2>/dev/null | head -15 || true)"
GIT_COUNT="$(printf '%s\n' "$GIT_DIRTY" | grep -c . || true)"

# --- Вывод -------------------------------------------------------------------
cat <<EOF
# Брифинг: $MODE

- Дата: $TODAY ($DOW), таймзона: $TZ_NAME
- Vault: $ROOT
- Текущий этап Roadmap: ${STAGE_NUM:-не определён}
EOF

if [[ -n "$BOARD_DAY" && "$BOARD_DAY" != "$TODAY" ]]; then
  printf -- '- ВНИМАНИЕ: Board «Сегодня» датирован %s, а не %s — блок устарел.\n' "$BOARD_DAY" "$TODAY"
fi

h2 "Board — сегодня"
if [[ -n "$BOARD_BLOCK" ]]; then
  printf '%s\n' "$BOARD_BLOCK"
  printf '\nОткрыто: %s, закрыто: %s, MIN-строк: %s\n' "$BOARD_OPEN" "$BOARD_DONE" "$BOARD_MIN"
else
  echo "_Блок «## Сегодня» не найден._"
fi

if [[ "$MODE" == evening ]]; then
  h2 "Board — что осталось незакрытым"
  printf '%s\n' "$BOARD_BLOCK" | grep '^- \[ \]' || echo "_нет_"
fi

h2 "Roadmap — этап $STAGE_NUM"
if [[ -n "$STAGE_ROW" ]]; then
  printf '%s\n' "$STAGE_ROW"
else
  echo "_строка этапа не найдена_"
fi
if [[ -n "$STAGE_DAYS" ]]; then
  printf '\nПлан этапа:\n\n%s\n' "$STAGE_DAYS"
fi

h2 "Review Queue — на сегодня и просрочено"
if [[ -n "$REVIEW_DUE" ]]; then
  printf '| Заметка | Тема | review_at | conf |\n|---|---|---|---|\n%s\n' "$REVIEW_DUE"
else
  echo "_ничего не подошло_"
fi

h2 "Learning Log — последние 3 сессии"
if [[ -n "$LOG_TAIL" ]]; then
  printf '%s\n' "$LOG_TAIL"
else
  echo "_пусто_"
fi

h2 "Фактчек не закрыт"
if [[ -n "$UNVERIFIED" ]]; then
  printf '%s\n' "$UNVERIFIED" | sed 's/^/- /'
else
  echo "_все заметки verified_"
fi

h2 "Git"
printf 'Изменённых путей: %s\n' "$GIT_COUNT"
if [[ -n "$GIT_DIRTY" ]]; then
  printf '```\n%s\n```\n' "$GIT_DIRTY"
fi

printf '\n---\n_Брифинг собран %s из файлов vault; модель не должна придумывать состояние, которого здесь нет._\n' "$TODAY"
