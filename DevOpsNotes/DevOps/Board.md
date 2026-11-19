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

## Сегодня — 2026-11-18 (FULL, закрытие Таненбаума)

- [x] **MIN:** квиз T1–T6 закрыт на уровне книги (2026-11-18); глубинные темы — anycast/BGP, ECS, ALG/FTP, `CertificateVerify`, QUIC loss — вынесены отдельным треком «статья → вопросы».
- [x] **MIN-2:** P4 — пересдача выполнена 2026-11-18: `openssl x509 -text` по цепочке, trust anchor (anchor — `depth=2`, не `cert3.pem`), `pathlen:0`, негативный тест по hostname (`error 62`).
- [x] **MAX:** лаба DNS/TLS и квиз 7–8 финализированы (`verified: true`), поток А Roadmap закрыт.
- [ ] **Лёгкий слот:** — (Review Queue: ближайшие карточки 2026-11-23).
- Go-слот — в заморозке до 2026-11-23.

> [!note] План дня — факт 2026-11-18
> - Квиз T1–T6 закрыт на уровне книги; F1 отменён, глубина ушла в отдельный трек.
> - Лаба DNS/TLS: P4 пересдан, выводы P1–P4 и «Что сломалось» заполнены — пользователь.
> - Финализация: лаба и квиз `verified: true`, Roadmap и Review Queue обновлены — `devops` (2026-11-19, 06:45).
> - Фактчек `devops-verifier` не выполнен: квота провайдера. Проверено локально `devops`: версии инструментов, `verify` с `-untrusted` и без, hostname mismatch, `man x509v3_config`, fake-IP через DoH.
> Статус: MIN-2 и MAX закрыты, поток А закрыт.

## Заморозка (вскрытие пакетом 2026-11-23)

Заморозка ≠ провал: хвост уезжает за главной нитью и вскрывается всё разом, не по карточке.

> [!note] Снято 2026-11-18: разбор лабы DNS/TLS и повтор T1–T6 — закрываются сегодня, вне пакета. Остальное вскрывается 2026-11-23.

- [ ] Фактчек `Cgroups.md` + блок `[!check]` + заполнение «Как работает» (материал уже выдан в чате 2026-11-15)
- [ ] Повтор Diagnostics 2026-11-06 (интервал сброшен на 2026-11-23 — догонять не нужно)
- [ ] Д5–Д8 этапа 1: OOM+journald, разбор compose-override с `mem_limit`, Type=notify, LVM-лаба, runbook «Диагностика зависшего сервиса»
- [ ] SadServers — первый сценарий (уместнее после этапа 2 — сеть)
- [ ] io.max (15 мин): unit `cgio` с `IOReadIOPSMax`/`IOWriteIOPSMax` на `/dev/sda`; отказ ядра на устройстве — тоже результат
- [ ] Go: `flow.go`, фаза 2 (Learn Go with Tests), goroutines/channels — Basics не дедлайн

## Очередь — Этап 1 (Linux internals: практика)

- [x] Д2: netns-лаба выполнена (`ip netns add` + veth-пара, сквозной пинг), cleanup полный; заметка [[DevOps/Notes/Linux/Network namespace]] финализирована
- [x] Д3: 5 открытых вопросов по namespaces; заметка → evergreen (2026-11-10)
- [x] Д4: cgroups v2 — cgtest/cghigh/cgoom (2026-11-14); io.max → «Заморозка»
- Д5–Д8 → «Заморозка» до 2026-11-23
- В: SadServers → «Заморозка» (после этапа 2)

## Очередь — Сети (Таненбаум)

- [x] Квиз 7–8 закрыт на уровне книги (2026-11-18); глубинные темы — anycast/BGP, ECS, ALG/FTP, `CertificateVerify`, QUIC loss — вынесены отдельным треком «статья → вопросы».
- [ ] Практика: P4 — пересдача, выводы P1–P4, «Что сломалось», фактчек лабы.

## Очередь — Поток В (bash/логи)

- Pipeline drill #1 → «Заморозка» (без движения с 2026-11-10)

## Очередь — Go (поток Д)

- [ ] Фаза 1: Tour of Go — основы *(частично: 5 файлов Basics; `flow.go` в «Заморозке»)*
- [ ] Фаза 1: Go by Example — goroutines/channels → «Заморозка» до 2026-11-23
- [ ] Фаза 2: Learn Go with Tests — старт → «Заморозка»
- [ ] Фаза 3: порт `analyze.py` на Go — CLI с тестами → «Заморозка»

## Готово (неделя)

- [x] План этапов + канбан (2026-11-07)

## Отчёты недели

| Дата       | Тип  | MIN | Что сделано                                                                                                                                                                                                                                                                                       | Пробел                                                                                                                |
| ---------- | ---- | --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| 2026-11-07 | FULL | ☑   | план этапов зафиксирован, канбан заведён                                                                                                                                                                                                                                                              | —                                                                                                                     |
| 2026-11-07 | FULL | ☑   | namespaces-лаба (lsns, unshare, nsenter), черновик Namespaces.md, Таненбаум гл. 8                                                                                                                                                                                                                 | Go-слот                                                                                                               |
| 2026-11-08 | FULL | ☑   | *вечер, после ритуала:* netns-лаба (ip netns + veth, сквозной пинг, cleanup ✓); квиз Q1–Q4 (Q2 неверно: адрес не переезжает с интерфейсом; Q3 с ошибкой: veth-пара удаляется целиком — исправлено 2026-11-09); первый фактчек заметок пройден; наблюдение: firefox contentproc в отдельных net ns | Go-слот; mnt/uts/ipc + Namespaces.md → evergreen (в Д3)                                                               |
| 2026-11-09 | FULL | ☐   | namespaces Д3: лабы mnt/uts/user/ipc (tmpfs, hostname, `ipcs`/`ipcmk`, `uid_map`) + черновик Q1–Q5 в `Namespaces.md`; Go: 3 файла в `DevOpsNotes/Practice/Go_lang/basic/`; создан `Practice/DevOps/drills/pipelines.md` (10 задач); обновлены Skills Matrix и Roadmap                             | Q1/Q2/Q4 не сверены с man (`verified: false`), evergreen не закрыт; Go Basics не завершён; лёгкий слот не подтверждён |
| 2026-11-10 | FULL | ☑   | Д3 закрыт: `Namespaces.md` → `status: evergreen` (`verified: true`, last_verified 2026-11-09), карточка фактчека в Review Queue → `done`, Д3 в Board `[x]`; Board переписан под закрытие хвостов (сети, В, Д, HTTP-статусы), cgroups перенесён на 2026-11-11                                                                                                         | квиз 7–8, drill #1, `flow.go`, HTTP-статусы не начаты — доказательств нет; cgroups не сделан                   |
| 2026-11-11 | FULL | ☐   | Квиз Таненбаум 7–8: теория T1–T6 + добор сдана, разбор и эталоны — в `DevOpsNotes/Networks/Таненбаум/Квиз 7–8.md`; проверены реальные `dig +trace` и `dig +dnssec`: resolver 192.168.0.1 не валидирует DNSSEC, 1.1.1.1/8.8.8.8/9.9.9.9 валидируют; Go: `imports.go`, `exported-names.go`, `functions.go`, `multiple-results.go`, `named-results.go`, `.golangci.yml` | cgroups v2 (MIN и MAX) не сделан — лабы и `cgroups v2.md` нет; `flow.go` (flow control) не сделан; pipeline drill #1 и лёгкий слот не сделаны |
| 2026-11-12 | FULL | ☐   | Практика квиза 7–8 P1–P5 выполнена: `dig +trace` (делегирование), `dig +dnssec` (+ `dnssec-failed.org`, `+cd`), `curl -vI`, `openssl s_client`/`x509`, `ss`; выводы 3–6 предложений и разборы — в лабе `DevOpsNotes/Practice/networks/2026-11-11-dns-tls-ss.md`; в «Самое важное» добавлены ссылки Cloudflare по DNSSEC/anycast | cgroups v2 (MIN и MAX) не сделан — лабы и `cgroups v2.md` нет; `flow.go` не сделан; лёгкий слот и drill #1 не сделаны; лаба `status: seed`, `verified: false`, frontmatter повреждён; файлы вне разрешённых путей — не в git |
| 2026-11-13 | SHORT | ☐   | Разбор практики P1–P5: 5 контрольных ответов проверены (2.2/5) — P5 почти зачёт, P1/P2/P3 половина, P4 пересдать; в лабе исправлен `review_at`, добавлены выводы P1 (`dig +trace +comments edu.vsu.ru`) | повтор T1–T6 не подтверждён; `flow.go`, drill #1 и «Что сломалось» в лабе не сделаны |
| 2026-11-14 | FULL | ☑   | cgroups v2 MIN: unit `cgtest` (`memory.max=52428800`, `cpu.max=20000 100000`, путь `/sys/fs/cgroup/system.slice/cgtest.service`), `cghigh` (`MemoryHigh=30M`), `cgoom` (OOM kill, `Failed with result 'oom-kill'`); создана заметка `Cgroups.md` (`status: seed`) | `io.max` не проверен; в `Cgroups.md` пусты «Как работает», «Ошибки», «Проверка себя» и блок `[!check]`; `flow.go`, drill #1, повтор T1–T6 и лёгкий слот не сделаны |
| 2026-11-17 | SHORT | ☐   | `Cgroups.md` — заполнен раздел «Как работает» (юниты service/scope/slice, контроллеры cgroups v1/v2, `/proc/self/cgroup`, `systemd-cgtop`), исправлен frontmatter (`topic: linux-cgroups`, `created: 2026-11-14`, `tags`) | `Cgroups.md` — 6 lint warnings (пустой `review_at`, `[!check]`) |

## Связи

- [[DevOps/Roadmap|Roadmap]] · [[DevOps/Learning Log|Learning Log]] · [[DevOps/Review Queue|Review Queue]]
