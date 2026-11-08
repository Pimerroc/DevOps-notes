---
type: runbook
status: growing
topic: opencode-rituals
difficulty: 2
created: 2026-11-08
review_at: 2026-11-15
verified: true
last_verified: 2026-11-08
tags: [devops, opencode, systemd, automation]
---

# Harness: ритуалы утро/вечер в OpenCode

> [!summary] Заменяет ZCode automations на systemd user timers + `opencode run` в одной постоянной сессии. Модель получает детерминированный брифинг из файлов vault, а не догадывается о состоянии.

## Зачем

ZCode automations работают только пока запущен десктоп-хост. OpenCode-вариант:

- работает, пока живёт user systemd (TUI открывать не нужно);
- одна и та же сессия на утро и вечер — история ритуала не фрагментируется;
- контекст собирается из файлов (`Board`, `Roadmap`, `Review Queue`, `Learning Log`), а не из памяти модели;
- всё в git: units, промпты, скрипты — воспроизводимо на другой машине.

## Состав

```
Practice/DevOps/harness/
├── brief.sh                  # читает vault → markdown-брифинг (stdout)
├── run.sh                    # init | morning | evening | smoke [--dry-run]
├── install.sh                # install | uninstall | --dry-run
├── prompts/morning.md        # жёсткий промпт утра
├── prompts/evening.md        # жёсткий промпт вечера
└── systemd/
    ├── devops-ritual@.service
    ├── devops-ritual-morning.timer   # 10:00, Persistent=true
    └── devops-ritual-evening.timer   # 21:00, Persistent=true
```

Состояние (не в git):

- `~/.local/state/devops-ritual/session-id` — id единственной ритуальной сессии;
- `/tmp/opencode/devops-ritual/brief-*.md` — последний собранный брифинг.

## Установка

```sh
cd /home/max/DevOps_Notes/Practice/DevOps/harness
./run.sh init          # создать сессию, привязанную к vault
./run.sh smoke         # проверка конвейера, ничего не меняет
./install.sh           # units → ~/.config/systemd/user, enable --now таймеры
```

## Проверка

```sh
systemctl --user list-timers --all | grep devops-ritual
systemctl --user start devops-ritual@smoke.service
journalctl --user -u devops-ritual@smoke.service -n 30 --no-pager
opencode api get "/api/session/$(cat ~/.local/state/devops-ritual/session-id)" | grep -o '"directory":"[^"]*"'
```

Ожидаемо: два таймера, `harness ok` в journal, `directory` = `/home/max/DevOps_Notes`.

Ручное продолжение той же сессии:

```sh
opencode -s "$(cat ~/.local/state/devops-ritual/session-id)"
```

## Откат

```sh
./install.sh uninstall                 # disable, clean state, удалить units
rm -f ~/.local/state/devops-ritual/session-id
```

`uninstall` идемпотентен: повторный запуск не падает. Порядок важен:

1. `disable --now` таймеров (ошибка «unit не существует» погашена);
2. `stop 'devops-ritual@*.service'` — чтобы откат не оставил работать начатый прогон;
3. `systemctl --user clean --what=state` **до** удаления файлов — иначе stamp-файлы `Persistent=true` остаются и после переустановки дают немедленный догон;
4. удаление units и `daemon-reload`.

Все шаги с `|| true`: цена — вместе с ожидаемыми ошибками глушатся и настоящие (нет D-Bus, сломанный user-менеджер). Проверять вывод глазами.

## Ограничения и риски

- **`opencode run --auto` снимает все `ask`**, а не только shell: правку `AGENTS.md` и `.opencode/opencode.jsonc`, чтение `*.env`, `external_directory`. Реально ограничивают только правила `deny` из `.opencode/opencode.jsonc`. Для необслуживаемого прогона это осознанный компромисс; при усилении запретов сначала менять `deny`, потом ждать от `--auto` защиты.
- `Linger=no`: таймеры идут только при активной user-сессии. Для работы после логаута: `loginctl enable-linger max` (меняет систему, делать осознанно).
- `Persistent=true` догоняет пропущенный запуск при следующем входе — **в любое время суток**: утренний ритуал может отработать вечером, вечерний — утром.
- `RandomizedDelaySec` не используется: для одного домашнего таймера разброс только сдвигает запуск без пользы. `AccuracySec=1s` — старт в пределах секунды от `OnCalendar`.
- При смене `OnCalendar` у таймера с `Persistent=true` возможен **немедленный догон**: systemd считает, что новое время уже прошло. Если догон не нужен — перед `restart` обновить stamp: `systemctl --user stop <timer> && touch ~/.local/share/systemd/timers/stamp-<timer> && systemctl --user start <timer>`.
- Сессия намеренно видима в `opencode session list` — это точка входа для ручного продолжения. `--archived` не используется: на существующую сессию он не действует.
- Если сессия недоступна (404 или ошибка сервера), `run.sh` создаёт новую и перезаписывает `session-id`. Ошибка сервера трактуется так же, как удалённая сессия — это осознанное упрощение.
- `question` в `opencode run` не работает: вызов отменяется, ответа нет (проверено на v2.2.6; в docs гарантировано только «dismissing cancels»). Поэтому вечерний промпт фиксирует состояние по фактам, без вопросов.
- Брифинг растёт вместе с Board и очередями; следить за размером `/tmp/opencode/devops-ritual/brief-*.md`.

## Отличия от ZCode automations

| | ZCode | harness |
|---|---|---|
| Триггер | встроенный cron, нужен запущенный хост | systemd user timer |
| Сессия | новая задача на запуск (или `target_task_id`) | одна постоянная |
| Контекст | промпт + модель сама читает файлы | брифинг + промпт |
| Логи | внутри приложения | journald |
| Переносимость | привязано к приложению | git + systemd |

ZCode-автоматизации не удалены; при желании выключить их в приложении, чтобы не было двойных прогонов.

> [!check] Проверено
> - Дата: 2026-11-08
> - Окружение: Arch Linux, opencode v2.2.6, systemd 262.1-1, user-сессия, Linger=no, Europe/Moscow
> - Источники: `opencode run --help`, `opencode session --help`, живой OpenAPI (`POST /api/session`, `PATCH /api/session/{id}`), `systemd-analyze verify --user`, `man systemd.timer`, `man systemd.unit`, журнал `devops-ritual@smoke.service`
> - Проверенные команды: `brief.sh morning|evening`, `run.sh init|smoke|--help|--dry-run`, `install.sh` + `uninstall` (дважды), `systemctl --user start devops-ritual@smoke.service`, `opencode api get /api/session/<id>`
> - Не проверено: реальное срабатывание 10:00/20:30, поведение после `loginctl enable-linger`, `shellcheck` (не установлен — только `bash -n` + `systemd-analyze verify`)
