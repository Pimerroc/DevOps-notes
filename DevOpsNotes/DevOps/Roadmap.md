---
type: moc
status: growing
topic: roadmap
difficulty: 1
created: 2026-11-06
review_at: 2026-11-14
verified: true
last_verified: 2026-11-07
tags: [devops, roadmap]
---

# DevOps Roadmap

> [!summary] Этапный план практики поверх имеющейся теории. Порядок этапов фиксирован, темп свободный. Этап закрыт выходным критерием (артефакт + проверка), а не временем. Дневные цели — минимум/максимум, не часы.

> [!info] Диагностика 2026-11-06: **20/30 (67%)**. Сильные — IaC/CI-CD и сети (теория); приоритет — Linux internals, containers, Kubernetes, security. Git пропущен (learngitbranching + практика).

## Как работать с планом

**Потоки** (параллельные, у каждого своя дорожка в [[DevOps/Board|Board]]):

| Поток | Что это | Слоты |
|---|---|---|
| А — книга | Таненбаум: книга прочитана; квиз по гл. 7–8 (теория + практика) | 1 слот на квиз, затем закрыт |
| Б — этапы | Основной трек практики, порядок ниже | 2 слота/день |
| В — реальные задачи | SadServers / KodeKloud Engineer, bash/awk на задачах | 2–3 слота/нед |
| Г — тренды и сертификаты | platform engineering, AIOps, SPE; Terraform Associate, KCNA | 1 слот/нед |
| Д — Go | Фазы 1–4, см. ниже | 1 слот/день |

**Типы дня** (определяется утром):

- **FULL** — свободный день: MIN + MAX.
- **SHORT** — учёба/жизнь забрала день: только MIN. Это нормальный день, не провал.

**Правила:**

1. **Минимум первым.** MIN делается до всего остального; сделан MIN — день засчитан.
2. Порядок этапов жёсткий, внутри этапа темы можно менять местами.
3. Тема знакома → теория сжимается в повторение, сразу лаба. Пробел всплыл → карточка в [[DevOps/Review Queue|Review Queue]], без прыжков.
4. Сравнение с решениями (SadServers/KodeKloud) — не на идентичность, а на работоспособность и понимание расхождения.
5. Уровень в [[DevOps/Skills Matrix|Skills Matrix]] растёт только от артефакта.

## Структура дня (без часов — последовательность)

Учтено: тренировка 60–90+ мин каждое утро; учёба в плавающие дни; сон нестабильный, энергия растёт к вечеру.

1. **После тренировки — лёгкий слот** (поток А или повторение): не требует холодной головы.
2. **День/вечер — тяжёлые слоты** (поток Б этап, поток Д Go): на пик энергии.
3. **Вечер — ритуал отчёта** (5 минут): [[DevOps/Board|Board]] + строка в [[DevOps/Learning Log|Learning Log]].
4. Учёба-день → SHORT: слоты 1–2 исчезают, MIN остаётся.

Воскресенье — consolidation: повторение, фактчек, [[Templates/Weekly Review|Weekly Review]], без новой теории.

## Поток А — книга (до закрытия)

> [!note] Добавлено агентом — статус на 2026-11-18
> Пункты 1–2 фактически закрыты: конспекты [[Networks/Таненбаум/Глава 7/Глава 7|Глава 7]] и [[Networks/Таненбаум/Глава 8/Глава 8|Глава 8]] есть, оба `verified: true`; квиз [[Networks/Таненбаум/Квиз 7–8|Квиз 7–8]] закрыт на уровне книги, практика P1–P5 выполнена в лабе [[AgentStuff/DevOps/networks/2026-11-11-dns-tls-ss|2026-11-11 DNS/TLS/ss]] (`verified: true`, 2026-11-18). Глубинные темы (anycast/BGP, ECS, ALG/FTP, `CertificateVerify`, QUIC loss) в зачёт книги не входят и вынесены в отдельный трек «статья → вопросы» — карточка в [[DevOps/Review Queue|Review Queue]] на 2026-11-25. Поток А закрыт, слот переходит потоку Д.

1. Заметка по главе 7 (прикладной уровень: DNS, HTTP, email, CDN) — 5 тезисов + схема. Пропущена при чтении.
2. Дочитать главу 8 (осталось ~50 стр. до стр. 959) → заметка: криптография, подписи, сертификаты/PKI, TLS. Станет базой этапа 7.
3. После закрытия — слот переходит потоку Д. Фоновое чтение: How Linux Works выборочно; TLPI — только справочник.

## Поток Б — этапы

| Этап | Тема | Артефакт | Выходной критерий (DoD) |
|---|---|---|---|
| 1 | **Linux internals — практика**: namespaces, cgroups v2, systemd, LVM | Runbook «Диагностика зависшего сервиса» | 4 лабы выполнены, заметки Namespaces/cgroups, 10 открытых вопросов по man7/docs |
| 2 | **Сеть — из теории в руки**: netns, veth, NAT, tcpdump, DNS, TLS, nginx | Схема стенда + runbook «Недоступен сервис — проверка по слоям» | netns-лаба сквозная, tcpdump-выводы разобраны, nginx+TLS стенд, quiz HTTP-статусы |
| 3 | **Containers — Docker всерьёз**: слои/кэш, PID 1, volumes, compose | Минимальный образ + Compose-стенд nginx+app+db | кэш-эксперименты задокументированы, PID 1/зомби разбор, аудит Dockerfile'ов digradation |
| 4 | **IaC — Terraform + Ansible** | Стенд разворачивается кодом | `terraform validate/plan`, `ansible-playbook --syntax-check --check` зелёные, роль «первичная настройка сервера» |
| 5 | **CI/CD — усиление digradation** | CD до compose-стенда | скан (trivy), кэш, артефакты, секреты, деплой по мержу на 8 существующих workflows |
| 6 | **Kubernetes — kind/k3s** | Helm-чарт digradation в кластере | Service/Secret/RBAC/probes/NetworkPolicy лабы, 3 break/fix-разбора. **Старт досрочно: 2026-11-15–16** — реальное подключение digradation к Kubernetes (см. [[DevOps/Board|Board]]); артефакты выходных засчитываются в этап |
| 7 | **Observability + Security** | Дашборд + алерты на свой стенд | алерт срабатывает на сломанный сервис, security-чеклист стенда, least privilege |
| 8 | **Capstone** | Полный стенд + портфолио | Terraform→Ansible→CI/CD→K8s→obs end-to-end, 2–3 разбора инцидентов, mock-интервью |

Ставить kubectl/terraform/trivy/dive — в начале соответствующего этапа. Ставка инструментов этапа 1 (на хосте отсутствуют): `stress-ng`, `strace`, `lvm2` — в день 1. Ansible уже есть в `Practice/.venv` (pip), системного нет.

**Правило детализации:** этап, на который заходим, раскладывается на дни (MIN/MAX) в момент старта — так план не протухает. **Каждый день начинается с теоретического блока** (один источник + 3–5 тезисов своими словами, ≤30 мин): лаба без теории — это набор команд. Источники-минимум на этап указываются при старте этапа; если темы нет в книгах — man 7 / official docs / kernel docs. Детальный план этапа 1 ниже; этапы 2–8 раскладываются по той же схеме.

### Этап 1 — детальный план (8 дней)

Источники-минимум этапа: `man 7 namespaces`, `man 7 pid_namespaces`, `man 1 unshare`, `man 1 nsenter` (дни 1–3); `man 5 systemd.resource-control`, `man 1 systemd-cgtop` (дни 4–5); `man 5 systemd.service`, freedesktop sd_notify (день 6); `man 8 lvm` / Red Hat LVM admin guide (день 7). Kerrisk, LWN «Namespaces in operation»: [p1](https://lwn.net/Articles/531114/), [p3](https://lwn.net/Articles/531419/), [p5](https://lwn.net/Articles/532593/), [p7](https://lwn.net/Articles/580893/).

| День | Теория-минимум | MIN | MAX |
|---|---|---|---|
| 1 | mental model ns + 3 syscall (clone/unshare/setns) | `lsns`; `unshare --user --map-root-user --pid --fork --mount-proc bash`; сравнить `ps -ef` и `readlink /proc/$$/ns/pid` внутри/снаружи | + `nsenter` обратно; начать `Notes/Linux/Namespaces.md` |
| 2 | типы ns: за что отвечает каждый (таблица из man 7) | Второй терминал: `unshare --net`, сравнить `ip link` внутри/снаружи | пройтись по mnt/uts/user/ipc; дописать заметку |
| 3 | user ns как граница привилегий; CVE-паттерн «userns + баг ядра = escape» | 5 открытых вопросов по namespaces (проверка по man7.org) | заметка до `evergreen`, `review_at`, карточка в Review Queue |
| 4 | cgroups v2: единая иерархия, контроллеры, `systemd` как API | `sudo pacman -S --needed stress-ng strace lvm2`; `systemd-run --property=MemoryMax=50M --property=CPUQuota=20% stress-ng ...`; наблюдать в `systemd-cgtop`, `/sys/fs/cgroup` | + `IOReadIOPSMax=`/`IOWriteIOPSMax=` (io.max в cgroup v2); заметка `cgroups v2.md` |
| 5 | OOM killer: как выбирает жертву, что пишет journald | OOM-эксперимент: лимит и превышение, что пишет journald | разбор `docker-compose.override.yml.memlim` из digradation: какие лимиты и почему |
| 6 | Типы юнитов и `Type=`: кто сигнализирует о готовности и почему это важно | Порт `Systemd-unit.md` на `Type=notify` + `sd_notify` | сравнение simple/exec/notify на своём сервисе, разбор в journald |
| 7 | LVM: PV/VG/LV, snapshot как CoW | LVM-лаба: snapshot, resize | восстановление из snapshot; заметка (у тебя уже есть база — эксперименты были) |
| 8 | Метод диагностики: от симптома к слою (proc → fd → syscall → cgroup → лог) | Черновик runbook «Диагностика зависшего сервиса» (ps → lsof → strace → journalctl → systemd-cgtop) | прогнать runbook на живом случае + фактчек + модульный квиз 10 открытых вопросов |

## Поток В — реальные задачи

- [SadServers](https://sadservers.com) — инцидент-сценарии на сломанных серверах. С этапа 1.
- [KodeKloud Engineer](https://kodekloud-engineer.com) — бесплатные задачи с автопроверкой. С этапа 1.
- [100 Days of DevOps](https://kodekloud.com/100-days-of-devops) — пул задач по текущему этапу, не подряд.
- bash/awk прикреплять сюда: задачи на обработку логов/вывода (плюс подготовка к этапу 7).
- Ритуал: решил сам → сравнил с решением → расхождение зафиксировал в заметке/Board.

## Поток Г — тренды и сертификаты

- Тренды 2026 (1 слот/нед, без углубления): platform engineering / IDP, AIOps, DevSecOps, GitOps, FinOps.
- SPE (Systems Performance Engineering) — специализация после этапа 3: метод USE, flamegraphs, eBPF, Brendan Gregg. Естественное продолжение Linux-крена, не отдельный поток сейчас.
- Сертификаты (маршрут из сессии 2026-11-07): Terraform Associate ($70.50, [hashicorp](https://developer.hashicorp.com/certifications/terraform-associate)) — после этапа 4; KCNA ($250, [cncf](https://www.cncf.io/training/certification/kcna)) — после этапа 6; бесплатно: SFC → SODFC ([SCRUMstudy](https://www.scrumstudy.com/certification/scrum-for-ops-and-devops-fundamentals-certified): Scrum Fundamentals → Scrum for Operations & DevOps Fundamentals, 1 вечер), LFS158 перед KCNA ([Linux Foundation](https://training.linuxfoundation.org/training/introduction-to-kubernetes)).

## Поток Д — Go

Go — язык экосистемы DevOps (Docker, Kubernetes, Terraform, Prometheus). Python не трогаем (digradation остаётся на Python).

| Фаза                           | Содержание                                                                                                                   | Артефакт                                   |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| 1. База                        | [A Tour of Go](https://go.dev/tour/welcome/1) + [Go by Example](https://gobyexample.com): синтаксис, stdlib, горутины/каналы | решение задач из Tour в репо `go-practice` |
| 2. С тестами                   | [Learn Go with Tests](https://github.com/quii/learn-go-with-tests) (TDD)                                                     | пакет с тестами по книге                   |
| 3. Мост в практику             | переписать свои bash/awk-скрипты и `analyze.py` (livecoding-метрики) на Go                                                   | CLI-тулза с тестами — портфолио            |
| 4. DevOps-мост (после этапа 6) | мини-сервис `net/http`, клиент Kubernetes API, чтение исходников kubectl                                                     | утилита поверх K8s API                     |

Ритм: 1 слот/день, слот атомарен, с этапом дня не смешивается. При сжатом дне режутся слоты В, затем А — но не этап и не Go.

## Режимы недели

**Базовый (сейчас, ~7 ч/день):**

| День  | Слоты                                                                           |
| ----- | ------------------------------------------------------------------------------- |
| Пн–Пт | лёгкий (А/повторение) → этап (2 слота) → Go → по остатку В                      |
| Сб    | build day: digradation по текущему этапу; повторение недели                     |
| Вс    | consolidation: квиз, фактчек, Weekly Review, Review Queue, план недели, поток Г |

**Рабочий (после выхода на эникей):**

| День     | Слоты                  |
| -------- | ---------------------- |
| Пн/Ср/Пт | этап (1–2 слота)       |
| Вт/Чт    | Go (1–2 слота)         |
| Сб       | build day              |
| Вс       | короткий consolidation |

Практика с работы (Linux, тикеты, пользователи) фиксируется в Learning Log — это тоже доказательства для Skills Matrix.

## Ритуалы и уведомления

- **Утро (07:00)** — systemd user timer `devops-ritual-morning.timer` → `AgentStuff/DevOps/harness/run.sh morning`: брифинг из Board/Roadmap/Review Queue/Learning Log, ставит MIN/MAX в «Сегодня».
- **Вечер (21:00)** — `devops-ritual-evening.timer` → `run.sh evening`: фиксирует день по фактам (git, изменённые заметки, журнал), обновляет Board, Learning Log, Review Queue. Вопросов не задаёт: `opencode run` неинтерактивен, вызов `question` там отменяется.
- Оба ритуала идут в одной сессии «DevOps ритуал — утро и вечер»; id — `~/.local/state/devops-ritual/session-id`. Ручное продолжение: `opencode -s "$(cat ~/.local/state/devops-ritual/session-id)"`.
- `Persistent=true` догоняет пропуск при следующем входе, поэтому «пропустил» не теряется, но может отработать не в свой час. Вручную: `run.sh morning|evening`. Разбор — [[AgentStuff/DevOps/harness/README|harness]].
- **Коммит — только вечером**: `AgentStuff/DevOps/harness/commit.sh` → `docs(devops): итоги дня — YYYY-MM-DD`, stage только разрешённых путей. Утренний прогон не коммитит.
- Канбан-правило: карточка без движения 3 дня → либо режется на две, либо снимается.

## Проверка знаний

- По умолчанию — открытые вопросы: объясни своими словами, предскажи результат, найди ошибку, напиши команду или конфиг.
- Multiple choice — только для быстрой проверки; правильный вариант не ставится первым.
- Каждый вопрос и эталонный ответ проверяются по официальному источнику; источник указывается.
- Практические задания проверяются выполнением: запуск, тест, линтер, валидатор.

## Связанное

- [[DevOps/Board|Board]] — канбан недели
- [[DevOps/Learning Log|Learning Log]] · [[DevOps/Skills Matrix|Skills Matrix]] · [[DevOps/Review Queue|Review Queue]] · [[DevOps/Sources|Sources]] · [[DevOps/Fact Check Queue|Fact Check Queue]]

> [!check] Проверено
> - Дата: 2026-11-07
> - Окружение: Arch Linux, kernel 7.2.14-arch1-1, systemd 262.1-1, Docker 29.9.2
> - Источники: man7.org (namespaces), man systemd.resource-control, docs freedesktop (systemd), [go.dev/tour](https://go.dev/tour/welcome/1), [gobyexample.com](https://gobyexample.com/), [quii/learn-go-with-tests](https://github.com/quii/learn-go-with-tests), [sadservers.com](https://sadservers.com), [kodekloud-engineer.com](https://kodekloud-engineer.com), цены сертификатов — hashicorp/cncf/linuxfoundation/scrumstudy (проверено 2026-11-07)
> - Проверенные команды: `lsns`, `nsenter`, `systemd-run --property`, флаги `unshare --user --map-root-user --pid --fork --mount-proc` — на этом хосте 2026-11-07; `unshare --pid` без user namespace даёт Operation not permitted (воспроизведено)
> - Фактчек: прогон верификатором 2026-11-07, риск low; исправлены `cgtop`→`systemd-cgtop`, несуществующее `IOMax`→`io.max`/`IOReadIOPSMax=`, добавлены отсутствующие инструменты этапа 1 (stress-ng, strace, lvm2)
> - Не проверено: наличие kubectl/terraform/dive/trivy (не установлены — установка внутри своих этапов); SadServers/KodeKloud — доступность и формат задач сверить при первом заходе; TLPI — файл в Books отсутствует, только справочник по необходимости
