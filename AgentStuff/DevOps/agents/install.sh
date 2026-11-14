#!/usr/bin/env bash
# install.sh (agents) — разворачивает канонические промпты из AgentStuff/DevOps/agents
# в оба контура: ZCode (.zcode) и OpenCode (.opencode в vault + глобальный ~/.config/opencode).
#
# Канон версионируется git'ом; установленные файлы — артефакты. Править промпты
# только здесь, затем: ./install.sh && (в другом контуре для глобальных: полный прогон).
#
# Использование:
#   install.sh                # всё: .zcode + .opencode + глобальные OpenCode-агенты
#   install.sh --skip-global  # только vault-локальное (глобальный ~/.config не трогать)
#   install.sh --dry-run      # показать, что будет сделано
#
# Правило vault: глобальный ~/.config/opencode правится НЕ из vault-сессии.
# Поэтому из vault запускай с --skip-global, а полный прогон — из другой сессии:
#   cd ~/DevOps_Notes && AgentStuff/DevOps/agents/install.sh

set -euo pipefail

SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=../../harness/config.env
source "$SELF_DIR/../harness/config.env"

SKIP_GLOBAL=0
DRY=0
for a in "$@"; do
  case "$a" in
    --skip-global) SKIP_GLOBAL=1 ;;
    --dry-run) DRY=1 ;;
    -h|--help) sed -n '2,20p' "$0"; exit 0 ;;
    *) echo "install.sh: неизвестный аргумент $a" >&2; exit 2 ;;
  esac
done

Z_AGENTS="$VAULT_ROOT/.zcode/agents"
Z_SKILL="$VAULT_ROOT/.zcode/skills/livecoding"
Z_CMD="$VAULT_ROOT/.zcode/commands"
O_SKILL="$VAULT_ROOT/.opencode/skills/livecoding"
O_CMD="$VAULT_ROOT/.opencode/commands"
GLOBAL_AGENTS="${HOME}/.config/opencode/agents"

# Порожние метаданные ZCode: name|description|color|tools (пусто = инструменты по умолчанию)
ZMETA=(
  "devops|Senior DevOps engineer and mentor. Works on infrastructure, diagnoses incidents, writes runbooks, teaches while doing, and keeps Obsidian notes fact-checked.|cyan|"
  "devops-tutor|Deep DevOps tutor. Diagnoses level, explains internals, runs quizzes and labs, and writes learning notes to Obsidian.|green|Read, Edit, Write, Bash"
  "devops-reviewer|Read-only reviewer for DevOps code and infrastructure. Finds correctness, security, reliability, idempotency and rollback issues.|orange|Read, Bash"
  "devops-verifier|Fact-checker and finalizer for DevOps notes. Verifies claims, commands, versions, APIs and configurations against local tools and official documentation, then finalizes the note itself.|yellow|Read, Edit, Bash, WebFetch, WebSearch"
  "devops-secrets-auditor|Read-only auditor for real secrets and personal data. Vault policy: default creds of learning stands (admin/admin) are not secrets.|red|Read, Bash"
)

ACT() { if (( DRY )); then printf '+ %s\n' "$*"; else "$@"; fi; }

echo "== ZCode: агенты =="
ACT mkdir -p "$Z_AGENTS"
for row in "${ZMETA[@]}"; do
  IFS='|' read -r name desc color tools <<< "$row"
  body="$SELF_DIR/$name.md"
  [[ -r "$body" ]] || { echo "нет канона: $body" >&2; exit 1; }
  out="$Z_AGENTS/$name.md"
  {
    printf -- '---\nname: %s\ndescription: "%s"\ncolor: %s\n' "$name" "$desc" "$color"
    [[ -n "$tools" ]] && printf 'tools: [%s]\n' "$tools"
    printf -- '---\n'
    cat "$body"
  } > "$out.tmp"
  ACT mv "$out.tmp" "$out"
  echo "  zcode: $out"
done

echo "== ZCode: скилл livecoding и команда /live =="
ACT mkdir -p "$Z_SKILL/scripts" "$Z_CMD"
# ZCode-вариант SKILL.md — без opencode-метаданных (канон их не содержит).
ACT cp "$SELF_DIR/../skills/livecoding/SKILL.md" "$Z_SKILL/SKILL.md"
for s in "$SELF_DIR/../skills/livecoding/scripts/"*; do
  ACT cp "$s" "$Z_SKILL/scripts/$(basename "$s")"
done
ACT cp "$SELF_DIR/../commands/live.md" "$Z_CMD/live.md"

echo "== OpenCode (vault .opencode) =="
ACT mkdir -p "$O_SKILL/scripts" "$O_CMD"
# OpenCode-вариант SKILL.md — добавляем autoinvoke-метаданные после description.
tmp="$O_SKILL/SKILL.md.tmp"
if (( DRY )); then
  echo "+ cp канона + метаданные → $O_SKILL/SKILL.md"
else
  awk '/^description:/ && !done { print; print "metadata:"; print "  opencode/autoinvoke: false"; done=1; next } { print }' \
    "$SELF_DIR/../skills/livecoding/SKILL.md" > "$tmp"
  mv "$tmp" "$O_SKILL/SKILL.md"
fi
for s in "$SELF_DIR/../skills/livecoding/scripts/"*; do
  ACT cp "$s" "$O_SKILL/scripts/$(basename "$s")"
done
# OpenCode-команда: добавляем agent: devops в frontmatter.
if (( DRY )); then
  echo "+ cp канона + agent: devops → $O_CMD/live.md"
else
  awk '/^---$/ && c==0 { print; print "agent: devops"; c++; next } { print }' \
    "$SELF_DIR/../commands/live.md" > "$O_CMD/live.md"
fi

if (( SKIP_GLOBAL )); then
  echo "== Глобальные OpenCode-агенты пропущены (--skip-global) =="
else
  echo "== OpenCode: глобальные агенты (body-sync, frontmatter сохраняется) =="
  ACT mkdir -p "$GLOBAL_AGENTS"
  for row in "${ZMETA[@]}"; do
    IFS='|' read -r name desc _color _tools <<< "$row"
    body="$SELF_DIR/$name.md"
    out="$GLOBAL_AGENTS/$name.md"
    if [[ -s "$out" ]]; then
      # Заменяем только тело: существующий frontmatter (description, mode,
      # permissions) не трогаем — он настроен под OpenCode.
      if (( DRY )); then
        echo "+ body-sync: $out"
      else
        n="$(grep -nm2 '^---$' "$out" | tail -1 | cut -d: -f1)"
        { head -n "$n" "$out"; cat "$body"; } > "$out.tmp"
        mv "$out.tmp" "$out"
        echo "  global body-sync: $out"
      fi
    else
      # Новый агент: сеем frontmatter subagent-профиля.
      if (( DRY )); then
        echo "+ seed: $out"
      else
        {
          printf -- '---\ndescription: "%s"\nmode: subagent\n' "$desc"
          cat <<'PERM'
permissions:
  - action: edit
    resource: "*"
    effect: deny
  - action: shell
    resource: "*"
    effect: ask
  - action: shell
    resource: "* --help"
    effect: allow
  - action: shell
    resource: "grep *"
    effect: allow
  - action: shell
    resource: "rg *"
    effect: allow
  - action: shell
    resource: "ls *"
    effect: allow
  - action: shell
    resource: "find *"
    effect: allow
  - action: shell
    resource: "git log *"
    effect: allow
  - action: shell
    resource: "git show *"
    effect: allow
  - action: read
    resource: "*.env"
    effect: ask
  - action: read
    resource: "*.pem"
    effect: deny
  - action: read
    resource: "*.key"
    effect: deny
---
PERM
          cat "$body"
        } > "$out"
        echo "  global seed: $out"
      fi
    fi
  done
  echo "  (сессии OpenCode перечитают агентов при следующем запуске)"
fi

echo "install.sh: готово"
