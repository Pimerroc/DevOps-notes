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

## Сегодня — 2026-11-11 (FULL)

> [!note] Добавлено агентом

- [ ] **MIN (Д4):** cgroups v2: `sudo pacman -S --needed stress-ng strace lvm2`; `systemd-run --unit=cgtest --property=MemoryMax=50M --property=CPUQuota=20% stress-ng --cpu 2 --vm 1 --timeout 60s`; снять `systemd-cgtop` и `systemctl show cgtest -p MemoryMax,CPUQuotaPerSecUSec`; проверить путь юнита в `/sys/fs/cgroup`. Результат — unit `cgtest` с лимитами и снятые значения *(не сделан: лабы нет, `cgroups v2.md` нет — перенос на 2026-11-12)*
- [ ] MAX (Д4): продолжить cgroups v2 — `IOReadIOPSMax=`/`IOWriteIOPSMax=` (io.max), проверить `systemctl show`; создать `DevOpsNotes/DevOps/Notes/Linux/cgroups v2.md` с лабой и наблюдениями *(не сделан — перенос на 2026-11-12)*
- [ ] Go-слот: Tour of Go «Basics» — flow control (`for`/`if`/`switch`/`defer`); `flow.go` в `DevOpsNotes/Practice/Go_lang/basic/`, `go run` *(перенос с 2026-11-10; 2026-11-11 частично: `functions.go`, `multiple-results.go`, `named-results.go`, `imports.go`, `exported-names.go`; `flow.go` не сделан — перенос на 2026-11-12)*
- [ ] Лёгкий слот (Review Queue, просрочено с 2026-11-09): [[DevOps/Diagnostics/2026-11-06]] — Linux internals: namespaces, systemd, overlayfs (conf 1) *(не сделан — перенос на 2026-11-12)*
- [x] **Сети — квиз 7–8, теория:** T1–T6 + добор сданы, разбор и повторный ответ — в [[Квиз 7–8|Квиз 7–8]]; практика P1–P5 — отдельная сессия *(2026-11-11)*
- Хвосты с 2026-11-10 (остаются в очереди, не дублирую): квиз Таненбаума 7–8 (практика), pipeline drill #1.

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
| 2026-11-11 | FULL | ☐   | Квиз Таненбаум 7–8: теория T1–T6 + добор сдана, разбор и эталоны — в `DevOpsNotes/Networks/Таненбаум/Квиз 7–8.md`; проверены реальные `dig +trace` и `dig +dnssec`: resolver 192.168.0.1 не валидирует DNSSEC, 1.1.1.1/8.8.8.8/9.9.9.9 валидируют; Go: `imports.go`, `exported-names.go`, `functions.go`, `multiple-results.go`, `named-results.go`, `.golangci.yml`; гигиена git: английские сообщения 12 коммитов | cgroups v2 (MIN и MAX) не сделан — лабы и `cgroups v2.md` нет; `flow.go` (flow control) не сделан; pipeline drill #1 и лёгкий слот не сделаны; force-push после `filter-branch` не согласован |

## Связи

- [[DevOps/Roadmap|Roadmap]] · [[DevOps/Learning Log|Learning Log]] · [[DevOps/Review Queue|Review Queue]]
