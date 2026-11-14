#!/usr/bin/env bash
# vault-lint.sh — линтер заметок vault: wikilinks, frontmatter, фактчек-блоки.
#
# Использование:
#   vault-lint.sh            # вывод всех находок; exit 0
#   vault-lint.sh --strict   # exit 1, если есть errors
#
# Правила:
#   R1 (error)  wikilink [[...]] не резолвится ни в один файл vault
#   R2 (warn)   во frontmatter нет ключа type/status/created/tags
#   R2b (warn)  для type: note|lab|runbook|incident пустой review_at
#   R3 (error)  verified: true, но блока «[!check]» нет
#   R4 (warn)   в блоке [!check] есть пустые поля («- Дата:» без значения)
#
# Журналы из config.env LINT_SKIP_PATHS не проверяются (история не переписывается).

set -uo pipefail

SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./config.env
source "$SELF_DIR/config.env"

STRICT=0
for a in "$@"; do
  case "$a" in
    --strict) STRICT=1 ;;
    -h|--help) sed -n '2,18p' "$0"; exit 0 ;;
    *) echo "vault-lint.sh: неизвестный аргумент $a" >&2; exit 2 ;;
  esac
done

ERR=0
WARN=0
err()  { ERR=$((ERR+1)); printf '[err]  %s\n' "$1"; }
warn() { WARN=$((WARN+1)); printf '[warn] %s\n' "$1"; }

# Индекс файлов один раз — дальше только O(1) Lookups, без повторных find.
mapfile -t ALL_FILES < <(find "$VAULT_ROOT" -type f \
  -not -path '*/.git/*' -not -path '*/.obsidian/*' \
  -not -path '*/.venv/*' -not -path '*/node_modules/*' -not -path '*/__pycache__/*' \
  -not -path "$VAULT_ROOT/.zcode/*" -not -path "$VAULT_ROOT/.opencode/*" \
  2>/dev/null || true)
mapfile -t MD_FILES < <(printf '%s\n' "${ALL_FILES[@]}" | grep '\.md$' || true)

declare -A PATH_IDX=()
declare -A BASE_IDX=()
for f in "${ALL_FILES[@]}"; do
  PATH_IDX["${f#"$VAULT_ROOT"/}"]=1
  BASE_IDX["${f##*/}"]=1
done

# Заметки (frontmatter-правила) — только домены заметок; ссылки проверяем везде.
NOTES_RE='^(DevOpsNotes/|Templates/)'

# Плейсхолдеры в текстах правил — не ссылки.
STOPWORDS_RE='^(вики-ссылки|\.\.\..*|Pasted image.*|Илл\. .*)$'

# Исключения из линта: пути заданы относительно VAULT_ROOT (см. config.env).
SKIP_RE=''
for p in "${LINT_SKIP_PATHS[@]}"; do
  SKIP_RE="${SKIP_RE:+$SKIP_RE|}^$p(/.*)?\$"
done

resolve_link() {
  local t="$1"
  # точный относительный путь от корня vault (path-ссылки и не-md вложения)
  [[ -n "${PATH_IDX[$t]:-}" ]] && return 0
  # basename-резолюция, как Obsidian: «DevOps/Board» → …/Board.md
  [[ -n "${BASE_IDX[$t]:-}" ]] && return 0
  local base="${t##*/}"
  [[ -n "${BASE_IDX[$base]:-}" ]] && return 0
  [[ -n "${BASE_IDX[$base.md]:-}" ]] && return 0
  return 1
}

for f in "${MD_FILES[@]}"; do
  rel="${f#$VAULT_ROOT/}"
  [[ -n "$SKIP_RE" && "$rel" =~ $SKIP_RE ]] && continue

  # --- frontmatter (только домены заметок) -----------------------------------
  if [[ "$rel" =~ $NOTES_RE ]]; then
  fm="$(awk 'NR==1 && /^---[[:space:]]*$/ { in_fm=1; next }
             in_fm && /^---[[:space:]]*$/ { exit }
             in_fm { print }' "$f")"
  if [[ -n "$fm" ]]; then
    fm_type="$(printf '%s\n' "$fm" | sed -n 's/^type:[[:space:]]*//p' | head -1)"
    for key in type status created tags; do
      if ! printf '%s\n' "$fm" | grep -q "^$key:"; then
        warn "R2 $rel: frontmatter без '$key'"
      fi
    done
    case "$fm_type" in
      note|lab|runbook|incident)
        if printf '%s\n' "$fm" | grep -qE '^review_at:[[:space:]]*$'; then
          warn "R2b $rel: пустой review_at для type: $fm_type"
        fi
        # R3 — только для заметок с техническими утверждениями; справочные
        # типы (moc/queue/reference) без [!check] — не ошибка.
        if printf '%s\n' "$fm" | grep -qi '^verified:[[:space:]]*true'; then
          if ! grep -q '\[!check\]' "$f"; then
            err "R3 $rel: verified: true, но блока [!check] нет"
          fi
        fi
        ;;
    esac
  fi
  fi

  # --- блок [!check]: пустые поля --------------------------------------------
  empty_fields="$(grep -E '^> - [^:]+:[[:space:]]*$' "$f" 2>/dev/null | head -5 || true)"
  while IFS= read -r line; do
    [[ -n "$line" ]] || continue
    warn "R4 $rel: пустое поле в [!check]: '$line'"
  done <<< "$empty_fields"

  # --- wikilinks --------------------------------------------------------------
  links="$(grep -oE '\[\[[^]]+\]\]' "$f" 2>/dev/null || true)"
  [[ -z "$links" ]] && continue
  while IFS= read -r m; do
    [[ -z "$m" ]] && continue
    t="${m#\[\[}"
    t="${t%\]\]}"
    t="${t//\\|/|}"   # экранирование в таблицах: [[X\|alias]] → [[X|alias]]
    t="${t%%|*}"      # alias
    t="${t%%#*}"      # heading
    t="${t%%^*}"      # block ref
    t="$(printf '%s' "$t" | sed -E 's/^[[:space:]]+|[[:space:]]+$//g')"
    [[ -z "$t" ]] && continue
    case "$t" in
      http:*|https:*|mailto:*|obsidian:*|'<'*) continue ;;
    esac
    [[ "$t" =~ $STOPWORDS_RE ]] && continue
    if ! resolve_link "$t"; then
      err "R1 $rel: не резолвится [[$t]]"
    fi
  done <<< "$links"
done

printf '\nlint: %d errors, %d warnings%s\n' "$ERR" "$WARN" "$([[ $STRICT == 1 ]] && printf ' (strict)')"
if (( STRICT && ERR > 0 )); then
  exit 1
fi
exit 0
