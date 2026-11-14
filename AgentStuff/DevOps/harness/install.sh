#!/usr/bin/env bash
# install.sh — ставит systemd user units для ритуалов утро/вечер.
#
# Использование:
#   install.sh            # скопировать units, daemon-reload, enable --now таймеры
#   install.sh --dry-run  # только показать, что будет сделано
#   install.sh uninstall  # выключить таймеры, удалить units и их state
#
# Units лежат в репозитории (systemd/), в ~/.config/systemd/user/ копируются,
# чтобы установка была воспроизводимой и откатываемой.

set -euo pipefail

SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="$SELF_DIR/systemd"
UNIT_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
UNITS=(devops-ritual@.service devops-ritual-morning.timer devops-ritual-evening.timer)
TIMERS=(devops-ritual-morning.timer devops-ritual-evening.timer)

DRY=0
ACTION=install
for a in "$@"; do
  case "$a" in
    --dry-run) DRY=1 ;;
    uninstall) ACTION=uninstall ;;
    -h|--help) sed -n '2,10p' "$0"; exit 0 ;;
    *) echo "install.sh: неизвестный аргумент $a" >&2; exit 2 ;;
  esac
done

run() {
  if (( DRY )); then
    printf '+ %s\n' "$*"
  else
    "$@"
  fi
}

if [[ "$ACTION" == uninstall ]]; then
  # disable падает, если unit уже отсутствует — для идемпотентности глушим.
  run systemctl --user disable --now "${TIMERS[@]}" 2>/dev/null || true
  # Остановить возможный незавершённый прогон шаблона (все инстансы сразу).
  run systemctl --user stop 'devops-ritual@*.service' 2>/dev/null || true
  # Persistent=true хранит stamp-файлы; clean нужен, пока unit ещё известен
  # systemd (то есть до удаления файлов), иначе после переустановки возможен
  # немедленный догон пропущенного запуска.
  run systemctl --user clean --what=state "${TIMERS[@]}" 2>/dev/null || true
  for u in "${UNITS[@]}"; do
    run rm -f "$UNIT_DIR/$u"
  done
  run systemctl --user daemon-reload
  if (( DRY )); then
    echo "dry-run: таймеры и units не тронуты"
  else
    echo "units удалены, таймеры выключены"
  fi
  exit 0
fi

for f in "${UNITS[@]}"; do
  [[ -r "$SRC_DIR/$f" ]] || { echo "нет файла $SRC_DIR/$f" >&2; exit 1; }
done

run mkdir -p "$UNIT_DIR"
for f in "${UNITS[@]}"; do
  run install -m 0644 "$SRC_DIR/$f" "$UNIT_DIR/$f"
done

run systemctl --user daemon-reload
run systemctl --user enable --now "${TIMERS[@]}"

if (( ! DRY )); then
  echo
  systemctl --user list-timers --all 'devops-ritual-*' --no-pager
  echo
  echo "Проверить: systemctl --user list-timers --all | grep devops-ritual"
  echo "Логи:      journalctl --user -u devops-ritual@morning.service -n 50"
  echo "Откат:     $SELF_DIR/install.sh uninstall"
fi
