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

## Сегодня — 2026-11-08 (FULL)

- [x] **MIN:** Теория: Kerrisk part 1 (overview) → [part 3 (PID ns)](https://lwn.net/Articles/531419/) → [part 5 (user ns)](https://lwn.net/Articles/532593/); лаба: netns выполнена через `ip netns add day2` + veth (продовый путь вместо `unshare --net`), сквозной пинг 10.1.1.x ✓
- [x] MAX: + [part 7 (network ns)](https://lwn.net/Articles/580893/); обе заметки прогнаны через `devops-verifier` (risk low) *(остаток: mnt/uts/user/ipc + Namespaces.md → evergreen переезжают в Д3)*
- [ ] Go-слот: Tour of Go, старт фазы 1 *(перенос, 2-й день)*
- [x] Лёгкий слот: Таненбаум гл. 8 *(сверх плана: редизайн конспектов гл. 1–8 + «Самое важное», гл. 7–8 написаны)*

## Очередь — Этап 1 (Linux internals: практика)

- [x] Д2: netns-лаба выполнена (`ip netns add` + veth-пара, сквозной пинг), cleanup полный; заметка [[DevOps/Notes/Linux/Network namespace]] финализирована
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

| Дата       | Тип  | MIN | Что сделано                                                                       | Пробел  |
| ---------- | ---- | --- | --------------------------------------------------------------------------------- | ------- |
| 2026-11-07 | FULL | ☐   | план зафиксирован, агенты перенесены                                              | —       |
| 2026-11-07 | FULL | ☑   | namespaces-лаба (lsns, unshare, nsenter), черновик Namespaces.md, Таненбаум гл. 8 | Go-слот |
| 2026-11-08 | FULL | ☐   | harness/ритуалы OpenCode (systemd timers, коммит a78da47); редизайн конспектов Таненбаум гл. 1–8 + «Самое важное» (коммит 0e7ee99, вне DevOpsNotes/DevOps) | MIN дня не закрыт (Kerrisk + `unshare --net`), Go не стартовал |
| 2026-11-08 | FULL | ☑   | *вечер, после ритуала:* netns-лаба (ip netns + veth, сквозной пинг, cleanup ✓); квиз Q1–Q4 (Q3 чисто, Q1/Q2/Q4 частично); обе заметки финализированы верификатором (risk low); наблюдение: firefox contentproc в отдельных net ns | Go-слот; mnt/uts/ipc + Namespaces.md → evergreen (в Д3) |

## Связи

- [[DevOps/Roadmap|Roadmap]] · [[DevOps/Learning Log|Learning Log]] · [[DevOps/Review Queue|Review Queue]]
