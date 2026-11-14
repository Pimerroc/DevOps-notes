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

## Сегодня — 2026-11-14 (FULL)

> [!note] Добавлено агентом

- [ ] **MIN (Д4):** cgroups v2 — инструменты уже в системе (`stress-ng` 0.22.02, `strace`, `lvm2`); `systemd-run --unit=cgtest --property=MemoryMax=50M --property=CPUQuota=20% stress-ng --cpu 2 --vm 1 --timeout 60s`; снять `systemd-cgtop` и `systemctl show cgtest -p MemoryMax,CPUQuotaPerSecUSec`; проверить путь юнита в `/sys/fs/cgroup`. Результат — unit `cgtest` с лимитами и снятые значения *(перенос с 2026-11-13)*
- [ ] **MAX (Д4):** cgroups v2 — `IOReadIOPSMax=`/`IOWriteIOPSMax=` (io.max), `systemctl show`; заметка `DevOpsNotes/DevOps/Notes/Linux/cgroups v2.md` *(перенос с 2026-11-13)*
- [ ] **Go-слот:** Tour of Go «Basics» — flow control (`for`/`if`/`switch`/`defer`); `flow.go` в `DevOpsNotes/Practice/Go_lang/basic/`, `go run` *(перенос с 2026-11-13; остальные Basics-файлы уже есть)*
- [ ] **Лёгкий слот (Review Queue, просрочено с 2026-11-09):** [[DevOps/Diagnostics/2026-11-06]] — Linux internals: namespaces, systemd, overlayfs (conf 1) *(перенос с 2026-11-13)*
- [ ] **Теория (если останется время):** повтор T1–T6 по [[Квиз 7–8]] — 3–5 предложений своими словами + источник *(перенос с 2026-11-13; карточки в Review Queue — 2026-11-14)*
- [x] **Разбор практики P1–P5:** 5 контрольных ответов проверены (2.2/5), разбор выдан 2026-11-13; лаба — правки/фактчек 2026-11-16.
- [x] **Сети — квиз 7–8:** теория сдана 2026-11-11, практика P1–P5 — 2026-11-12, разбор — 2026-11-13.
- Хвосты: pipeline drill #1 (перенос с 2026-11-10); разбор выводов лабы DNS/TLS + «Что сломалось» + фактчек — 2026-11-16.

## Очередь — Этап 1 (Linux internals: практика)

- [x] Д2: netns-лаба выполнена (`ip netns add` + veth-пара, сквозной пинг), cleanup полный; заметка [[DevOps/Notes/Linux/Network namespace]] финализирована
- [x] Д3: 5 открытых вопросов по namespaces; заметка → evergreen (2026-11-10)
- [ ] Д4: `systemd-run` MemoryMax/CPUQuota + cgtop; заметка `cgroups v2.md`
- [ ] Д5: OOM-эксперимент + journald; разбор `docker-compose.override.yml.memlim` (digradation)
- [ ] Д6: `Type=notify` + `sd_notify` (порт Systemd-unit.md)
- [ ] Д7: LVM-лаба: snapshot, resize, восстановление
- [ ] Д8: runbook «Диагностика зависшего сервиса» + квиз 10 открытых вопросов
- [ ] В: первый сценарий SadServers (Linux)

## Выходные (2026-11-15…16) — digradation → Kubernetes (досрочный старт этапа 6)

Реальная задача вместо синтетики: то же, что этап 6, но на живом проекте. Остатки этапа 1 (Д5–Д8) и потоки В/Д не отменяются — уезжают на следующую неделю после закрытия weekend-цели.

- [ ] **Сб (11-15):** окружение: `sudo pacman -S --needed kubectl helm` + выбрать и поставить **kind** или **k3s**; digradation: собрать образы, поднять локальный кластер, задеплоить первый сервис (db или backend) с Service. Артефакт — кластер с работающим подом + заметка `Notes/Kubernetes/digradation-01.md` (что поставил, какие манифесты, где споткнулся)
- [ ] **Вс (11-16):** digradation: скелет helm-чарта (db + backend + frontend), ConfigMap/Secret для конфигов, probes. Артефакт — чарт разворачивается `helm install` + short consolidation (Review Queue — 1 слот, без новой теории)
- Формат: build day в оба дня. Если кластер съест больше времени — MIN выходного = только окружение/первый под, остальное переносится без штрафа.

## Очередь — Сети (Таненбаум)

- [ ] Гл. 7–8: квиз — 5–6 теоретических + 5–6 практических открытых вопросов с развёрнутыми ответами. Теория: DNS, HTTP/HTTPS, CDN, TLS, DNSSEC, брандмауэры/IDS. Практика: `dig +trace`, `dig +dnssec`, `curl -vI`, `openssl s_client`, `openssl x509`, `ss` (и `tcpdump`, если установлен и есть root). Ответ — 3–6 предложений + источник (раздел/стр. книги, RFC, man). Результат: `DevOpsNotes/Networks/Таненбаум/Квиз 7–8.md`; слабые пункты → Review Queue.

## Очередь — Поток В (bash/логи)

- [ ] Pipeline drill #1: [[pipelines|drills]], задачи 1–3; 30 мин, без AI; эталон + запись в Review Queue.

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
| 2026-11-12 | FULL | ☐   | Практика квиза 7–8 P1–P5 выполнена: `dig +trace` (делегирование), `dig +dnssec` (+ `dnssec-failed.org`, `+cd`), `curl -vI`, `openssl s_client`/`x509`, `ss`; выводы 3–6 предложений и разборы — в лабе `DevOpsNotes/Practice/networks/2026-11-11-dns-tls-ss.md`; в «Самое важное» добавлены ссылки Cloudflare по DNSSEC/anycast | cgroups v2 (MIN и MAX) не сделан — лабы и `cgroups v2.md` нет; `flow.go` не сделан; лёгкий слот и drill #1 не сделаны; лаба `status: seed`, `verified: false`, frontmatter повреждён; файлы вне разрешённых путей — не в git |
| 2026-11-13 | SHORT | ☐   | Разбор практики P1–P5: 5 контрольных ответов проверены (2.2/5) — P5 почти зачёт, P1/P2/P3 половина, P4 пересдать; в лабе исправлен frontmatter `review_at`, добавлены выводы P1 (`dig +trace +comments edu.vsu.ru`); vault реорганизован: harness и drills → `AgentStuff/DevOps/`, лаба → `AgentStuff/DevOps/networks/`; обновлены Sources (Docker Deep Dive и план книг), Skills Matrix, Roadmap, `DevOps.md`; квиз 7–8 и Go-файлы застейджены | cgroups v2 MIN не сделан — лабы и `cgroups v2.md` нет; повтор T1–T6 не подтверждён (карточки pending); `flow.go` не сделан; drill #1 не сделан; «Что сломалось» в лабе не заполнено; коммит не выполнен — `Practice/DevOps/harness/commit.sh` переехал в `AgentStuff/`, а в индексе пути вне allowlist |

## Связи

- [[DevOps/Roadmap|Roadmap]] · [[DevOps/Learning Log|Learning Log]] · [[DevOps/Review Queue|Review Queue]]
