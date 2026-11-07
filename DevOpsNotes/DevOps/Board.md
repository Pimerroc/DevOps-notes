---
type: moc
status: growing
topic: kanban
difficulty: 1
created: 2026-11-07
review_at:
verified: true
last_verified: 2026-11-07
tags: [devops, kanban]
---

# Board

> [!summary] Канбан недели. Утром automation ставит MIN/MAX в «Сегодня». Вечером — отчёт: галочки, строка в «Отчёты», строка в [[DevOps/Learning Log|Learning Log]]. Голова не хранилище — тут всё.

**Правила:**

- MIN первым. Сделан MIN — день засчитан, что бы ни было дальше.
- Карточка без движения 3 дня → режется на две или снимается.
- Учёба-день → тип SHORT, делаем только MIN.
- В конце недели карточки из «Готово» исчезают (архив — Learning Log).

## Сегодня — 2026-11-07 (FULL)

- [ ] **MIN:** День 1 этапа 1: `lsns` + `unshare --user --map-root-user --pid --fork --mount-proc bash`, сравнить `ps -ef` и namespace-дескрипторы
- [ ] MAX: + `nsenter` обратно; начать `Notes/Linux/Namespaces.md`
- [ ] Go-слот: Tour of Go, старт фазы 1
- [ ] Лёгкий слот: Таненбаум гл. 8 (30–40 стр.)

## Очередь — Этап 1 (Linux internals: практика)

- [ ] Д2: `unshare --net` в двух терминалах, сравнить `ip link`
- [ ] Д3: 5 открытых вопросов по namespaces; заметка → evergreen
- [ ] Д4: `systemd-run` MemoryMax/CPUQuota + cgtop; заметка `cgroups v2.md`
- [ ] Д5: OOM-эксперимент + journald; разбор `docker-compose.override.yml.memlim` (digradation)
- [ ] Д6: `Type=notify` + `sd_notify` (порт Systemd-unit.md)
- [ ] Д7: LVM-лаба: snapshot, resize, восстановление
- [ ] Д8: runbook «Диагностика зависшего сервиса» + квиз 10 открытых вопросов
- [ ] В: первый сценарий SadServers (Linux)

## Очередь — Go (поток Д)

- [ ] Фаза 1: Tour of Go — основы (переменные, функции, структуры)
- [ ] Фаза 1: Go by Example — goroutines/channels
- [ ] Фаза 2: Learn Go with Tests — старт
- [ ] Фаза 3: порт `analyze.py` на Go — CLI с тестами

## Готово (неделя)

- [x] План этапов + канбан + перенос агентов (2026-11-07)

## Отчёты недели

| Дата | Тип | MIN | Что сделано | Пробел |
|---|---|---|---|---|
| 2026-11-07 | FULL | ☐ | план зафиксирован, агенты перенесены | — |

## Связи

- [[DevOps/Roadmap|Roadmap]] · [[DevOps/Learning Log|Learning Log]] · [[DevOps/Review Queue|Review Queue]]
