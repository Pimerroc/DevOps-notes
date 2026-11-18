#!/usr/bin/env bash
# doctor.sh — сенсор дрифта harness: пути, юниты, allowlist, застарелые ссылки.
#
# Использование:
#   doctor.sh            # все проверки; exit 1 при [fail], [warn] не мешают
#   doctor.sh --quiet    # только [fail]/[warn]
#
# Назначение: ловить последствия переименований до того, как упадёт ритуал
# (кейс 2026-11-13: 203/EXEC — путь зашит в 6 местах, обновили одно).
# Запускается в утреннем ритуале; можно вручную после любого переноса.

set -uo pipefail

SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./config.env
source "$SELF_DIR/config.env"

QUIET=0
for a in "$@"; do
  case "$a" in
    --quiet) QUIET=1 ;;
    -h|--help) sed -n '2,13p' "$0"; exit 0 ;;
    *) echo "doctor.sh: неизвестный аргумент $a" >&2; exit 2 ;;
  esac
done

FAIL=0
WARN=0
ok()   { (( QUIET )) || printf '[ok]   %s\n' "$1"; }
warn() { WARN=$((WARN+1)); printf '[warn] %s\n' "$1"; }
fail() { FAIL=$((FAIL+1)); printf '[fail] %s\n' "$1"; }

# 1. Пути из config.env существуют
for var in VAULT_ROOT AGENTSTUFF_ROOT HARNESS_ROOT PRACTICE_CODE_ROOT PRACTICE_NOTES_ROOT LIVECODING_ROOT TEMPLATES_ROOT; do
  p="${!var:-}"
  if [[ -n "$p" && -e "$p" ]]; then
    ok "путь $var: $p"
  else
    fail "путь $var не существует: ${p:-<пусто>}"
  fi
done

# 2. Пути автокоммита существуют
for p in "${COMMIT_PATHS[@]}"; do
  if [[ -e "$VAULT_ROOT/$p" ]]; then
    ok "COMMIT_PATHS: $p"
  else
    fail "COMMIT_PATHS: '$p' не существует — вечерний коммит пропустит или упадёт"
  fi
done

# 3. Установленный unit: ExecStart указывает на HARNESS_ROOT/run.sh
INSTALLED="$UNIT_DIR/$RITUAL_UNIT"
if [[ -r "$INSTALLED" ]]; then
  exec_line="$(grep -m1 '^ExecStart=' "$INSTALLED" | sed 's/^ExecStart=//' || true)"
  # %h → $HOME, тогда как в config VAULT_ROOT может отличаться: сравниваем нормализованно
  norm="${exec_line//\%h/$HOME}"
  expected="$HARNESS_ROOT/run.sh"
  if [[ "$norm" == *run.sh* && -e "${norm%% *}" ]]; then
    ok "unit ExecStart: $exec_line"
  else
    fail "unit ExecStart сломан или путь не существует: '$exec_line' (ожидали $expected)"
  fi
  # 4. Дрифт установленного vs репо-юнит
  repo="$HARNESS_ROOT/systemd/$RITUAL_UNIT"
  if [[ -r "$repo" ]] && ! diff -q "$repo" "$INSTALLED" >/dev/null 2>&1; then
    warn "unit-дрифт: $INSTALLED отличается от $repo — запусти install.sh"
  else
    ok "unit в ~/.config соответствует репозиторию"
  fi
else
  fail "установленный unit не найден: $INSTALLED (install.sh не запускался?)"
fi

# 5. Таймеры включены и активны
for t in devops-ritual-morning.timer devops-ritual-evening.timer; do
  state="$(systemctl --user is-enabled "$t" 2>/dev/null || true)"
  if [[ "$state" == enabled ]]; then
    ok "таймер $t включён"
  else
    fail "таймер $t не включён (state: ${state:-unknown})"
  fi
done

# 6. git status покрыт allowlist
outside="$(git -C "$VAULT_ROOT" status --porcelain 2>/dev/null \
  | sed -E 's/^.{3}//' \
  | sed -E 's/^"(.*)"$/\1/' \
  | grep -vE "$COMMIT_PATHS_RE" || true)"
if [[ -n "$outside" ]]; then
  warn "git status содержит пути вне allowlist (коммитить вручную или расширить config.env):"
  printf '%s\n' "$outside" | sed 's/^/       /'
else
  ok "git status покрыт allowlist"
fi

# 7. Застарелые ссылки на старые пути (кроме журналов с историей)
stale="$(grep -rln 'Practice/DevOps/' "$VAULT_ROOT" \
  --include='*.md' --include='*.sh' --include='*.jsonc' --include='*.service' 2>/dev/null \
  | grep -v '/.git/' \
  | grep -vF "$VAULT_ROOT/DevOpsNotes/DevOps/Learning Log.md" \
  | grep -vF "$VAULT_ROOT/DevOpsNotes/DevOps/Board.md" \
  | grep -vF "$SELF_DIR/doctor.sh" || true)"
if [[ -n "$stale" ]]; then
  warn "остались ссылки на старый путь Practice/DevOps/ (переименовать или обновить):"
  printf '%s\n' "$stale" | sed 's/^/       /'
else
  ok "застарелых ссылок Practice/DevOps/ нет"
fi

# 8. Паритет канонических агентов с установленными копиями
canon_dir="$AGENTSTUFF_ROOT/DevOps/agents"
for canon in "$canon_dir"/*.md; do
  name="$(basename "$canon" .md)"
  installed="$VAULT_ROOT/.zcode/agents/$name.md"
  if [[ ! -s "$installed" ]]; then
    fail "zcode-агент '$name' не установлен — запусти AgentStuff/DevOps/agents/install.sh"
  else
    fm_end="$(grep -nm2 '^---$' "$installed" | tail -1 | cut -d: -f1)"
    if ! diff -q <(tail -n "+$((fm_end + 1))" "$installed") "$canon" >/dev/null 2>&1; then
      warn "zcode-агент '$name' расходится с каноном — перезапусти agents/install.sh"
    else
      ok "агент $name соответствует канону"
    fi
  fi
  if [[ ! -s "${HOME}/.config/opencode/agents/$name.md" ]]; then
    warn "глобальный OpenCode-агент '$name' отсутствует — полный прогон agents/install.sh вне vault-сессии"
  fi
done
[[ -r "$VAULT_ROOT/.opencode/skills/livecoding/SKILL.md" ]] \
  && ok "opencode-скилл livecoding установлен" \
  || fail "opencode-скилл livecoding отсутствует"

# Итог
printf '\ndoctor: %d fail, %d warn\n' "$FAIL" "$WARN"
(( FAIL == 0 ))
