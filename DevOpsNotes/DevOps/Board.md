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

## Сегодня — 2026-11-16 (SHORT)

> [!note] Добавлено агентом — обновлено по решению пользователя (2026-11-16, вечер): сегодня только rabbit → StatefulSet; digradation дальше — по выходным. Вечерний таймер остановлен, ритуал запустится вручную после работы.

- [ ] **MIN:** rabbitmq → **StatefulSet** (не Deployment): манифест StatefulSet + headless Service + `volumeClaimTemplates` (PVC под данные rabbit). Артефакт — `kubectl apply` → pod Ready, PVC Bound, `kubectl get sts` виден *(доказательств нет: манифестов StatefulSet в vault нет, `Practice/Kubernetes/` не менялся с 2026-11-15; minikube API `192.168.49.2:8443` недоступен — `no route to host`; перенос: бонус-слот или выходные 2026-11-21/22 — K8s-нить только по выходным)*
- [x] **cgroups v2:** лаба cgtest/cghigh/cgoom (OOM) + заметка-заготовка; разбор квиза: Q2/Q4 в цель, Q1/Q3 — вывод «лимит принадлежит группе, файлы = интерфейс лимитов» (разбор в чате 2026-11-15)
- [x] **K8s день 1 (11-15):** nginx-deployment (`replicas: 3`, requests/limits), kubectl v1.37.2
- [x] **Сети — квиз 7–8:** теория 2026-11-11, практика P1–P5 — 2026-11-12, разбор — 2026-11-13
- Ритм K8s-нити: **только выходные** + бонус-слоты после закрытия MAX дня. Helm-чарт — после стабилизации манифестов (руками → потом шаблонизация).
- Ритуал: таймер `devops-ritual-evening` остановлен на сегодня; после работы — `systemctl --user start devops-ritual-evening.timer` (Persistent догонит пропущенный запуск сразу).

## Заморозка (вскрытие пакетом 2026-11-23)

Заморозка ≠ провал: хвост уезжает за главной нитью и вскрывается всё разом, не по карточке.

- [ ] Разбор лабы DNS/TLS: правки выводов P1–P4, «Что сломалось», фактчек лабы
- [ ] Фактчек `Cgroups.md` + блок `[!check]` + заполнение «Как работает» (материал уже выдан в чате 2026-11-15)
- [ ] Повтор T1–T6 полный; повтор Diagnostics 2026-11-06 (интервалы в Review Queue сброшены на 2026-11-23 — догонять не нужно)
- [ ] Д5–Д8 этапа 1: OOM+journald, разбор `docker-compose.override.yml.memlim`, Type=notify, LVM-лаба, runbook «Диагностика зависшего сервиса»
- [ ] SadServers — первый сценарий (уместнее после этапа 2 — сеть)
- [ ] io.max (15 мин): unit `cgio` с `IOReadIOPSMax`/`IOWriteIOPSMax` на `/dev/sda`; отказ ядра на устройстве — тоже результат (было MIN-2 на 11-16, снято)
- [ ] Go: `flow.go`, фаза 2 (Learn Go with Tests), goroutines/channels — Basics не дедлайн
- Инфра-мелочи на 5 минут в любой момент: `agents/install.sh` полный прогон вне vault; `git push --force-with-lease origin main`

## Очередь — Этап 1 (Linux internals: практика)

- [x] Д2: netns-лаба выполнена (`ip netns add` + veth-пара, сквозной пинг), cleanup полный; заметка [[DevOps/Notes/Linux/Network namespace]] финализирована
- [x] Д3: 5 открытых вопросов по namespaces; заметка → evergreen (2026-11-10)
- [x] Д4: cgroups v2 — cgtest/cghigh/cgoom (2026-11-14); io.max → «Заморозка»
- Д5–Д8 → «Заморозка» до 2026-11-23
- В: SadServers → «Заморозка» (после этапа 2)

## Выходные (2026-11-15…16) — digradation → Kubernetes: итог

- [x] **День 1 (11-15):** kubectl v1.37.2, nginx-deployment с лимитами ресурсов — `Practice/Kubernetes/Deployment/`
- [ ] **День 2 (11-16):** см. «Сегодня» — MIN: Service + db digradation; MAX: helm-чарт скелет

## Очередь — Сети (Таненбаум)

- [ ] Гл. 7–8: квиз — теория сдана 2026-11-11, практика P1–P5 — 2026-11-12, разбор — 2026-11-13; слабые пункты (T3, DoH/ECS, TLS 1.3 у CDN, типы firewall, base rate, IPS inline) → «Заморозка» / Review Queue

## Очередь — Поток В (bash/логи)

- Pipeline drill #1 → «Заморозка» (без движения с 2026-11-10)

## Очередь — Go (поток Д)

- [ ] Фаза 1: Tour of Go — основы *(частично: 5 файлов Basics; `flow.go` в «Заморозке»)*
- [ ] Фаза 1: Go by Example — goroutines/channels → «Заморозка» до 2026-11-23
- [ ] Фаза 2: Learn Go with Tests — старт → «Заморозка»
- [ ] Фаза 3: порт `analyze.py` на Go — CLI с тестами → «Заморозка»

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
| 2026-11-14 | FULL | ☑   | cgroups v2 MIN: unit `cgtest` (`memory.max=52428800`, `cpu.max=20000 100000`, путь `/sys/fs/cgroup/system.slice/cgtest.service`), `cghigh` (`MemoryHigh=30M`), `cgoom` (OOM kill, `Failed with result 'oom-kill'`); создана заметка `DevOpsNotes/DevOps/Notes/Linux/Cgroups.md` (`status: seed`); инфраструктура: `config.env`, `doctor.sh`, `vault-lint.sh`, allowlist `commit.sh`, канонические промпты в `AgentStuff/DevOps/agents`; 13 вырезок Таненбаума → `verified: false`; коммиты `0596500`, `7665158`, `7da04dd` | `io.max` не проверен; в `Cgroups.md` пусты «Как работает», «Ошибки», «Проверка себя» и блок `[!check]` (6 lint warnings); `flow.go`, drill #1, повтор T1–T6 и лёгкий слот не сделаны; глобальный агент `devops-secrets-auditor` отсутствует (doctor: 1 warn) |
| 2026-11-15 | FULL | ☐   | Вне плана: Kubernetes Deployment — `DevOpsNotes/Practice/Kubernetes/Deployment/services/nginx-deployment.yaml` (`replicas: 3`, `selector.matchLabels`, `requests` 50m/64Mi, `limits` 200m/512Mi) и `Deployment/docs.md` со ссылкой на docs; в Board объединены дубли строки «Хвосты» | `io.max` не сделан — unit `cgio` нет; `Cgroups.md` не менялся с 2026-11-14, lint: 6 warnings (пустой `review_at` и `[!check]`); `flow.go`, drill #1, повтор T1–T6 и лёгкий слот не сделаны; doctor: 1 warn — глобальный `devops-secrets-auditor` не установлен |
| 2026-11-16 | SHORT | ☐   | По решению пользователя день сведён к rabbit → StatefulSet; Board переработан: «Заморозка» до 2026-11-23 (DNS/TLS, Cgroups, T1–T6, Д5–Д8, drill #1, Go), K8s-нить — только выходные + бонус-слоты, вечерний таймер остановлен; тримаж Review Queue: просроченные интервалы → 2026-11-23; коммиты `bf3d31d`, `e39f7de`, `e74d9fa` | MIN rabbit → StatefulSet не сделан: манифестов нет, `Practice/Kubernetes/` не менялся с 11-15, minikube API недоступен (`no route to host`); `Cgroups.md` — 6 lint warnings (в заморозке); глобальный `devops-secrets-auditor` не установлен (doctor: 1 warn) |

## Связи

- [[DevOps/Roadmap|Roadmap]] · [[DevOps/Learning Log|Learning Log]] · [[DevOps/Review Queue|Review Queue]]
