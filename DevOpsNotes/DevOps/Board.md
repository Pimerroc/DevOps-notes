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

## Сегодня — 2026-11-09 (FULL)

- [ ] **MIN (Д3):** Сформулировать 5 открытых вопросов по namespaces и проверить ответы по `man7.org` (`namespaces(7)`, `user_namespaces(7)`/релевантные); результат — раздел с вопросами/ответами+источниками в `DevOpsNotes/DevOps/Notes/Linux/Namespaces.md` *(Q1–Q5 написаны 2026-11-09; Q1/Q2/Q4 не сверены с man — `verified: false`)*
- [ ] MAX (Д3): пройти mnt/uts/user/ipc в заметке; довести `Namespaces.md` до `status: evergreen`, выставить `review_at`, добавить карточку в `Review Queue` *(mnt/uts/user/ipc добавлены с лабами; `status: growing` — evergreen блокирован фактчеком Q1/Q2/Q4)*
- [ ] Go-слот: Tour of Go — старт фазы 1, пройти раздел «Basics» (packages/variables/functions) *(старт: 3 файла в `DevOpsNotes/Practice/Go_lang/basic/`; завершение Basics не подтверждено)*
- [ ] Лёгкий слот (Review Queue, 2026-11-09): [[DevOps/Diagnostics/2026-11-06]] — Linux internals: namespaces, systemd, overlayfs (conf 1) *(доказательств повторения нет)*

## Очередь — Этап 1 (Linux internals: практика)

- [x] Д2: netns-лаба выполнена (`ip netns add` + veth-пара, сквозной пинг), cleanup полный; заметка [[DevOps/Notes/Linux/Network namespace]] финализирована
- [ ] Д3: 5 открытых вопросов по namespaces; заметка → evergreen
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

| Дата       | Тип  | MIN | Что сделано                                                                                                                                                                                                                       | Пробел                                                  |
| ---------- | ---- | --- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| 2026-11-07 | FULL | ☑   | план зафиксирован, агенты перенесены                                                                                                                                                                                              | —                                                       |
| 2026-11-07 | FULL | ☑   | namespaces-лаба (lsns, unshare, nsenter), черновик Namespaces.md, Таненбаум гл. 8                                                                                                                                                 | Go-слот                                                 |
| 2026-11-08 | FULL | ☑   | *вечер, после ритуала:* netns-лаба (ip netns + veth, сквозной пинг, cleanup ✓); квиз Q1–Q4 (Q2 неверно: адрес не переезжает с интерфейсом; Q3 с ошибкой: veth-пара удаляется целиком — исправлено 2026-11-09); первый фактчек заметок пройден; наблюдение: firefox contentproc в отдельных net ns | Go-слот; mnt/uts/ipc + Namespaces.md → evergreen (в Д3) |
| 2026-11-09 | FULL | ☐   | namespaces Д3: лабы mnt/uts/user/ipc (tmpfs, hostname, `ipcs`/`ipcmk`, `uid_map`) + черновик Q1–Q5 в `Namespaces.md`; Go: 3 файла в `DevOpsNotes/Practice/Go_lang/basic/`; создан `Practice/DevOps/drills/pipelines.md` (10 задач); обновлены Skills Matrix и Roadmap | Q1/Q2/Q4 не сверены с man (`verified: false`), evergreen не закрыт; Go Basics не завершён; лёгкий слот не подтверждён |

## Связи

- [[DevOps/Roadmap|Roadmap]] · [[DevOps/Learning Log|Learning Log]] · [[DevOps/Review Queue|Review Queue]]
