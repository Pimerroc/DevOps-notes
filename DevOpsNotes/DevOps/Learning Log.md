---
type: log
status: growing
topic: learning-log
difficulty: 1
created: 2026-11-06
review_at:
verified: true
last_verified: 2026-11-06
tags:
  - devops
  - log
---

# Learning Log

> [!summary] Журнал учебных и рабочих сессий: что сделано, какой артефакт, какие пробелы, следующий шаг.

| Дата | Тема | Режим | Что сделано | Артефакт | Пробелы | Следующий шаг |
|---|---|---|---|---|---|---|
| 2026-11-06 | Старт | setup | Создан учебный контур и агенты | [[DevOps/Roadmap]] | Диагностика не пройдена | `/diagnostic` |
| 2026-11-06 | Стартовая диагностика | diagnostic | 20/30 (67%); сильные — IaC/CI-CD и сети, слабые — Linux internals, containers, K8s, security | [[DevOps/Diagnostics/2026-11-06]] | namespaces, systemd, Docker layers, Service/Secret, least privilege | Модуль 1: Linux internals |
| 2026-11-06 | Livecoding | build | Скилл kitty + nvim: JSONL-логгер, live-метрики, анализ; smoke-тесты пройдены | `.opencode/skills/livecoding/SKILL.md` | живой ввод с клавиатуры не проверен | Первая сессия `/live` |
| 2026-11-07 | Планирование | plan | Roadmap переписан на 8 этапов с MIN/MAX днями; канбан [[DevOps/Board\|Board]]; агенты перенесены в `.zcode/`; добавлены потоки Go, реальные задачи, тренды | [[DevOps/Roadmap]] | день-за-днём детализирован только этап 1 | День 1 этапа 1: namespaces-лаба |
| 2026-11-07 | Namespaces, День 1 этапа 1 | lab | Отработаны user+pid+mount namespaces: `lsns`, `unshare --user --map-root-user --pid --fork --mount-proc`, `nsenter` обратно; начат черновик заметки; Таненбаум гл. 8 | [[DevOps/Notes/Linux/Namespaces]] | Go-слот не стартовал; теория по статье — завтра | Д2: `unshare --net` в двух терминалах, сравнить `ip link` |
| 2026-11-08 | Ритуалы в OpenCode | build | systemd user timers вместо ZCode automations: `brief.sh` (брифинг из vault), `run.sh` (одна сессия утро+вечер), `install.sh`; e2e smoke через unit; разбор experimental `schedule` API | [[Practice/DevOps/harness/README\|harness]] | реальное срабатывание 10:00/20:30 не проверено; `shellcheck` отсутствует | Дождаться вечернего прогона, сверить Board и Learning Log |
| 2026-11-08 | Редизайн конспектов Таненбаум | review | Главы 1–6 сжаты в единый формат (143–265 строк), написаны новые конспекты глав 7–8 из книги, создан [[Networks/Таненбаум/Самое важное\|Самое важное]] (заголовки + дословные вырезки всей книги), Словарь дополнен до всех 120 аббревиатур списка книги; удалены 10 файлов-разборов, квиз, gen-скрипты и AI-графики | [[Networks/Таненбаум/Глава 7\|Глава 7]] · [[Networks/Таненбаум/Глава 8\|Глава 8]] | проверка знаний по главам 7–8 не проведена — по запросу | Пройти проверку знаний по главам 7–8 |
| 2026-11-08 | Вечерний ритуал | review | По брифингу/git/журналу: доказаны harness (a78da47) и редизайн Таненбаум (0e7ee99); пункты плана 2026-11-08 (MIN Kerrisk+`unshare --net`, MAX, Go, лёгкий слот) без доказательств выполнения — оставлены открытыми | [[DevOps/Board]] | MIN этапа 1 Д2 не закрыт; Go Tour of Go не стартован; Namespaces.md не доведён до evergreen/verifier | Завтра: закрыть MIN Д2 (`unshare --net`, сравнить `ip link`) + теория Kerrisk по плану; старт Go-слота |
| 2026-11-08 | Day 2: network namespace | lab | Вечером, после ритуала: netns-лаба продовым путём (`ip netns add day2` + veth-пара, адреса 10.1.1.x, сквозной ping, cleanup ✓); квиз Q1–Q4 (в чате; ответы перенесены в заметку): Q2 неверно — при переносе интерфейса в другой net ns адрес и флаг UP сбрасываются, но только для переносимых интерфейсов (veth/dummy проверено 2026-11-09; `lo`/bridge/wireless — netns immutable); Q3 содержал ошибку — после освобождения ns исчезает вся veth-пара, veth0 не остаётся (исправлено 2026-11-09 живым прогоном); Q1/Q4 неполные — дописаны со ссылками на man; обе заметки прошли первый фактчек; повторный 2026-11-09 нашёл ошибку Q3 | [[DevOps/Notes/Linux/Network namespace]] | Go-слот не сделан (перенос 2-й день); mnt/uts/ipc не пройдены; Namespaces.md в growing | Д3: 5 открытых вопросов по namespaces; mnt/uts/ipc; Namespaces.md → evergreen |
| 2026-11-08 | Выжимка + полные вырезки Таненбаум | review | «Самое важное» переписано: выжимка ~45 важных тем с кратким объяснением + индекс; создана папка `Вырезки/` — 36 файлов с дословным текстом книги по DevOps-частым темам (главы 3.5–8.12) и 234 скриншота страниц с рисунками в `Глава N/Images/` (Илл. N.M.png); таблицы восстановлены агентами по скриншотам | [[Networks/Таненбаум/Самое важное\|Самое важное]] | выборочная сверка таблиц; вырезки не гонялись через фактчек-агента | Выборочно сверить 3–4 таблицы с PDF; проверка знаний по главам 7–8 |
| 2026-11-09 | Namespaces Д3 + старт Go | lab | Лабы mnt/uts/user/ipc (tmpfs, hostname, `ipcs`/`ipcmk`, `uid_map`) и черновик Q1–Q5 в [[DevOps/Notes/Linux/Namespaces]]; Go: 3 файла в `DevOpsNotes/Practice/Go_lang/basic/`; создан [[Practice/DevOps/drills/pipelines]] (10 задач); обновлены Skills Matrix и Roadmap | [[DevOps/Notes/Linux/Namespaces]] · [[Practice/DevOps/drills/pipelines]] | Q1/Q2/Q4 не сверены с man7, `verified: false`; заметка не evergreen; Go Basics не завершён; лёгкий слот не подтверждён | Д4: фактчек Q1–Q5 по man, добить mnt/uts/ipc, evergreen; затем cgroups v2 |
| 2026-11-10 | Закрытие Д3 + план хвостов | review | `Namespaces.md` → `status: evergreen` (`verified: true`, last_verified 2026-11-09), карточка фактчека Q1/Q2/Q4 в Review Queue → `done`, Д3 в Board `[x]`; Board переписан под закрытие хвостов: сети (квиз 7–8), поток В (drill #1), поток Д (`flow.go`), HTTP-статусы; cgroups перенесён на 2026-11-11 | [[DevOps/Notes/Linux/Namespaces]] · [[DevOps/Board]] | квиз 7–8, drill #1, `flow.go` и HTTP-статусы не начаты — доказательств нет; cgroups не сделан | 2026-11-11: квиз 7–8 + drill #1 + `flow.go`; затем cgroups v2 |

## Как вести

- Одна строка на сессию.
- «Что сделано» — результат, а не процесс.
- «Артефакт» — ссылка на заметку, лабораторную или runbook.
- «Пробелы» — что не получилось или осталось непонятным.
- «Следующий шаг» — конкретное действие на следующую сессию.
