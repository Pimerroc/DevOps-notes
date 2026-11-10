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

## Сегодня — 2026-11-10 (FULL)

> [!note] Добавлено агентом

- [x] **MIN — закрыть Д3:** `Namespaces.md` → `status: evergreen`, `verified: true`; карточка фактчека в Review Queue → `done`; Д3 в «Очереди» `[x]` *(2026-11-10)*
- [ ] **Сети — квиз 7–8:** 5 теоретических + 5 практических вопросов (DNS, HTTP, CDN, TLS/DNSSEC; `dig +trace`, `dig +dnssec`, `curl -vI`, `openssl s_client`), ответы 3–6 предложений + источник; результат — `DevOpsNotes/Networks/Таненбаум/Квиз 7–8.md` *(не начат, перенос на 2026-11-11)*
- [ ] **Поток В:** pipeline drill #1 — top-10 IP; лог в `/tmp/access.log`; 25 мин без AI; проверка: сумма counts = `wc -l` *(не начат, перенос на 2026-11-11)*
- [ ] **Поток Д:** Tour of Go «Basics» — flow control (`for`/`if`/`switch`/`defer`); `flow.go` в `DevOpsNotes/Practice/Go_lang/basic/`, `go run` *(не начат, перенос на 2026-11-11)*
- [ ] **Лёгкий слот:** HTTP-статусы 504/502/503/301/308 — 10 мин, закрыть просроченную карточку *(не сделан, перенос на 2026-11-11)*
- Перенос: cgroups v2 (Д4) — на 2026-11-11, после закрытия хвостов.

## Очередь — Этап 1 (Linux internals: практика)

- [x] Д2: netns-лаба выполнена (`ip netns add` + veth-пара, сквозной пинг), cleanup полный; заметка [[DevOps/Notes/Linux/Network namespace]] финализирована
- [x] Д3: 5 открытых вопросов по namespaces; заметка → evergreen (2026-11-10)
- [ ] Д4: `systemd-run` MemoryMax/CPUQuota + cgtop; заметка `cgroups v2.md`
- [ ] Д5: OOM-эксперимент + journald; разбор `docker-compose.override.yml.memlim` (digradation)
- [ ] Д6: `Type=notify` + `sd_notify` (порт Systemd-unit.md)
- [ ] Д7: LVM-лаба: snapshot, resize, восстановление
- [ ] Д8: runbook «Диагностика зависшего сервиса» + квиз 10 открытых вопросов
- [ ] В: первый сценарий SadServers (Linux)

## Очередь — Сети (Таненбаум)

- [ ] Гл. 7–8: квиз — 5–6 теоретических + 5–6 практических открытых вопросов с развёрнутыми ответами. Теория: DNS, HTTP/HTTPS, CDN, TLS, DNSSEC, брандмауэры/IDS. Практика: `dig +trace`, `dig +dnssec`, `curl -vI`, `openssl s_client`, `openssl x509`, `ss` (и `tcpdump`, если установлен и есть root). Ответ — 3–6 предложений + источник (раздел/стр. книги, RFC, man). Результат: `DevOpsNotes/Networks/Таненбаум/Квиз 7–8.md`; слабые пункты → Review Queue.

## Очередь — Поток В (bash/логи)

- [ ] Pipeline drill #1: [[Practice/DevOps/drills/pipelines|drills]], задачи 1–3; 30 мин, без AI; эталон + запись в Review Queue.

## Очередь — Go (поток Д)

- [ ] Фаза 1: Tour of Go — основы (переменные, функции, структуры)
- [ ] Фаза 1: Go by Example — goroutines/channels
- [ ] Фаза 2: Learn Go with Tests — старт
- [ ] Фаза 3: порт `analyze.py` на Go — CLI с тестами

## Готово (неделя)

- [x] План этапов + канбан + перенос агентов (2026-11-07)

## Отчёты недели

| Дата       | Тип  | MIN | Что сделано                                                                                                                                                                                                                                                                                       | Пробел                                                                                                                |
| ---------- | ---- | --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| 2026-11-07 | FULL | ☑   | план зафиксирован, агенты перенесены                                                                                                                                                                                                                                                              | —                                                                                                                     |
| 2026-11-07 | FULL | ☑   | namespaces-лаба (lsns, unshare, nsenter), черновик Namespaces.md, Таненбаум гл. 8                                                                                                                                                                                                                 | Go-слот                                                                                                               |
| 2026-11-08 | FULL | ☑   | *вечер, после ритуала:* netns-лаба (ip netns + veth, сквозной пинг, cleanup ✓); квиз Q1–Q4 (Q2 неверно: адрес не переезжает с интерфейсом; Q3 с ошибкой: veth-пара удаляется целиком — исправлено 2026-11-09); первый фактчек заметок пройден; наблюдение: firefox contentproc в отдельных net ns | Go-слот; mnt/uts/ipc + Namespaces.md → evergreen (в Д3)                                                               |
| 2026-11-09 | FULL | ☐   | namespaces Д3: лабы mnt/uts/user/ipc (tmpfs, hostname, `ipcs`/`ipcmk`, `uid_map`) + черновик Q1–Q5 в `Namespaces.md`; Go: 3 файла в `DevOpsNotes/Practice/Go_lang/basic/`; создан `Practice/DevOps/drills/pipelines.md` (10 задач); обновлены Skills Matrix и Roadmap                             | Q1/Q2/Q4 не сверены с man (`verified: false`), evergreen не закрыт; Go Basics не завершён; лёгкий слот не подтверждён |
| 2026-11-10 | FULL | ☑   | Д3 закрыт: `Namespaces.md` → `status: evergreen` (`verified: true`, last_verified 2026-11-09), карточка фактчека в Review Queue → `done`, Д3 в Board `[x]`; Board переписан под закрытие хвостов (сети, В, Д, HTTP-статусы), cgroups перенесён на 2026-11-11                                                                                                         | квиз 7–8, drill #1, `flow.go`, HTTP-статусы не начаты — доказательств нет; cgroups не сделан                   |

## Связи

- [[DevOps/Roadmap|Roadmap]] · [[DevOps/Learning Log|Learning Log]] · [[DevOps/Review Queue|Review Queue]]
