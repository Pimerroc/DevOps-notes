#!/usr/bin/env bash
# run.sh — единая точка запуска ритуала OpenCode (утро/вечер) в одной сессии.
#
# Использование:
#   run.sh init [--dry-run]          # создать ритуальную сессию и запомнить её id
#   run.sh morning [--dry-run]       # брифинг + промпт утра
#   run.sh evening [--dry-run]       # брифинг + промпт вечера
#   run.sh smoke [--dry-run]         # проверка конвейера без изменений в vault
#   run.sh open [--dry-run]          # открыть сессию ритуала в TUI (пообщаться)
#   run.sh id                        # напечатать id сессии
#   run.sh log                       # журнал последних прогонов (journalctl)
#
# Одна сессия: id лежит в $XDG_STATE_HOME/devops-ritual/session-id
# (по умолчанию ~/.local/state/devops-ritual/session-id).

set -euo pipefail

SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./config.env
source "$SELF_DIR/config.env"
ROOT="$VAULT_ROOT"
STATE_DIR="${XDG_STATE_HOME:-$HOME/.local/state}/devops-ritual"
SID_FILE="$STATE_DIR/session-id"
TMP_DIR="${TMPDIR:-/tmp}/opencode/devops-ritual"
AGENT="${RITUAL_AGENT:-devops}"
LOG_LINES="${RITUAL_LOG_LINES:-60}"

usage() {
  sed -n '2,14p' "$0"
}

MODE=""
DRY=0
for a in "$@"; do
  case "$a" in
    --dry-run) DRY=1 ;;
    -h|--help)
      usage
      exit 0
      ;;
    init|morning|evening|smoke|open|id|log) MODE="$a" ;;
    *)
      echo "run.sh: неизвестный аргумент $a" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ -z "$MODE" ]]; then
  usage >&2
  exit 2
fi

create_session() {
  local resp sid payload
  if (( DRY )); then
    echo "dry-run: создал бы сессию с location=$ROOT"
    return 0
  fi
  mkdir -p "$STATE_DIR"
  payload="$(printf '{"title":"DevOps ритуал — утро и вечер","location":{"directory":"%s"}}' "$ROOT")"
  resp="$(opencode api post /api/session -d "$payload")"
  sid="$(printf '%s' "$resp" | grep -o '"id":"ses_[A-Za-z0-9]*"' | head -1 | grep -o 'ses_[A-Za-z0-9]*' || true)"
  if [[ -z "$sid" ]]; then
    echo "run.sh: не удалось создать сессию, ответ API:" >&2
    printf '%s\n' "$resp" >&2
    exit 1
  fi
  printf '%s\n' "$sid" > "$SID_FILE"
  echo "создана сессия: $sid"
  echo "id сохранён: $SID_FILE"
}

session_alive() {
  opencode api get "/api/session/$1" >/dev/null 2>&1
}

if [[ "$MODE" == init ]]; then
  create_session
  exit 0
fi

if [[ "$MODE" == id ]]; then
  if [[ ! -s "$SID_FILE" ]]; then
    echo "run.sh: сессии ещё нет — выполни: $0 init" >&2
    exit 1
  fi
  tr -d '[:space:]' < "$SID_FILE"
  echo
  exit 0
fi

if [[ "$MODE" == log ]]; then
  exec journalctl --user \
    -u devops-ritual@morning.service \
    -u devops-ritual@evening.service \
    -n "$LOG_LINES" --no-pager
fi

if [[ -s "$SID_FILE" ]]; then
  SID="$(tr -d '[:space:]' < "$SID_FILE")"
  if ! session_alive "$SID"; then
    echo "run.sh: сессия $SID недоступна — создаю новую" >&2
    create_session
    SID="$(tr -d '[:space:]' < "$SID_FILE")"
  fi
else
  create_session
  SID="$(tr -d '[:space:]' < "$SID_FILE")"
fi

if [[ "$MODE" == open ]]; then
  CMD=(opencode -s "$SID")
  if (( DRY )); then
    printf '%q ' "${CMD[@]}"
    printf '\n'
    exit 0
  fi
  cd "$ROOT"
  exec "${CMD[@]}"
fi

case "$MODE" in
  smoke)
    BRIEF_MODE=morning
    PROMPT="Проверка конвейера. Ответь одной строкой: harness ok. Не читай и не меняй файлы, инструменты не вызывай."
    ;;
  morning)
    BRIEF_MODE=morning
    PROMPT="$(cat "$SELF_DIR/prompts/morning.md")"
    ;;
  evening)
    BRIEF_MODE=evening
    PROMPT="$(cat "$SELF_DIR/prompts/evening.md")"
    ;;
esac

BRIEF_FILE="$TMP_DIR/brief-$BRIEF_MODE.md"
mkdir -p "$TMP_DIR"
"$SELF_DIR/brief.sh" "$BRIEF_MODE" > "$BRIEF_FILE"

# Сенсоры: doctor (утро/вечер) и vault-lint (вечер). В dry-run не мешаем
# предпросмотру — их вывод будет в живом брифинге.
if (( ! DRY )); then
  if "$SELF_DIR/doctor.sh" --quiet >> "$BRIEF_FILE" 2>&1; then
    printf '\n(doctor: ok)\n' >> "$BRIEF_FILE"
  else
    printf '\n( doctor: ЕСТЬ ПРОБЛЕМЫ — блок выше )\n' >> "$BRIEF_FILE"
  fi
  if [[ "$MODE" == evening ]]; then
    printf '\n## Vault lint\n\n```\n' >> "$BRIEF_FILE"
    "$SELF_DIR/vault-lint.sh" >> "$BRIEF_FILE" 2>&1 || true
    printf '```\n' >> "$BRIEF_FILE"
  fi
fi

TITLE="DevOps ритуал — $MODE $(date +%F)"
CMD=(opencode run --agent "$AGENT" --auto --title "$TITLE" -s "$SID" -f "$BRIEF_FILE" "$PROMPT")

if (( DRY )); then
  printf '%q ' "${CMD[@]}"
  printf '\n'
  echo "brief: $BRIEF_FILE ($(wc -l < "$BRIEF_FILE") строк)"
  exit 0
fi

cd "$ROOT"
exec "${CMD[@]}"
