#!/usr/bin/env bash
# commit.sh — детерминированный коммит «итоги дня» для вечернего ритуала.
#
# Использование:
#   commit.sh            # stage разрешённых путей и коммит
#   commit.sh --dry-run  # показать, что попадёт в коммит
#
# Разрешённые пути (AGENTS.md, синхронизировано 2026-11-14):
#   DevOpsNotes/DevOps/**, DevOpsNotes/DevOps.md, DevOpsNotes/Practice/**,
#   DevOpsNotes/Practice Theory/**, AgentStuff/**, Templates/**
# Всё остальное в индекс не попадает; если там уже что-то есть — скрипт падает.

set -euo pipefail

SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./config.env
source "$SELF_DIR/config.env"
ROOT="$VAULT_ROOT"

ALLOWED=("${COMMIT_PATHS[@]}")
ALLOWED_RE="$COMMIT_PATHS_RE"

DRY=0
for a in "$@"; do
  case "$a" in
    --dry-run) DRY=1 ;;
    -h|--help)
      sed -n '2,12p' "$0"
      exit 0
      ;;
    *) echo "commit.sh: неизвестный аргумент $a" >&2; exit 2 ;;
  esac
done

MSG="docs(devops): daily summary — $(date +%F)"

if (( DRY )); then
  PREVIEW="$(git -C "$ROOT" status --porcelain -- "${ALLOWED[@]}" 2>/dev/null | sed -E 's/^.{3}//' || true)"
  if [[ -z "$PREVIEW" ]]; then
    echo "итоги дня: нечего коммитить"
    exit 0
  fi
  echo "dry-run: git commit -m \"$MSG\""
  printf '%s\n' "$PREVIEW" | sed 's/^/  /'
  exit 0
fi

for p in "${ALLOWED[@]}"; do
  [[ -e "$ROOT/$p" ]] && git -C "$ROOT" add -A -- "$p"
done

STAGED="$(git -C "$ROOT" diff --cached --name-only || true)"

if [[ -z "$STAGED" ]]; then
  echo "итоги дня: нечего коммитить"
  exit 0
fi

OUTSIDE="$(printf '%s\n' "$STAGED" | grep -vE "$ALLOWED_RE" || true)"
if [[ -n "$OUTSIDE" ]]; then
  echo "СТОП: в индексе файлы вне разрешённых путей — коммит отменён:" >&2
  printf '%s\n' "$OUTSIDE" >&2
  echo "Разбери их вручную: git -C \"$ROOT\" status --short" >&2
  exit 1
fi

git -C "$ROOT" commit -m "$MSG"
echo "закоммичено: $MSG"
