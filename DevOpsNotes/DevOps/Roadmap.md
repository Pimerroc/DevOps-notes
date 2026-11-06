---
type: moc
status: growing
topic: roadmap
difficulty: 1
created: 2026-11-06
review_at:
verified: true
last_verified: 2026-11-06
tags: [devops, roadmap]
---

# DevOps Roadmap

> [!summary] 12-недельный интенсив: глубокая теория + лабораторные + проекты + фактчек. Цель — самостоятельная работа с инфраструктурой и подготовка к найму.

> [!info] Диагностика 2026-11-06: **20/30 (67%)**. Сильные — IaC/CI-CD и сети; приоритет — Linux internals, containers, Kubernetes, security. Начинаем с модуля 1.

## Формат

- 7 часов в день, без выходных.
- 4 блока: повторение → теория → практика → фактчек и заметки.
- Воскресенье — consolidation: без новой теории, только повторение, проект и рефакторинг заметок.
- Каждая неделя заканчивается артефактом: runbook, лабораторная или проект.

## Распорядок дня

| Блок | Время | Содержание |
|---|---|---|
| Review + план | 60 мин | Повторение, квиз, цель дня |
| Глубокая теория | 120 мин | Книга/официальные docs, внутреннее устройство |
| Практика / livecoding | 180 мин | Лабораторная, пайплайн, отладка, инцидент |
| Фактчек + заметка | 60 мин | Проверка, заметка, коммит, план на завтра |

## Недельный ритм

- **Пн, вт, чт, пт** — новая теория + лабораторная.
- **Ср** — pipeline/livecoding day.
- **Сб** — build day: проект целиком, сильная модель.
- **Вс** — consolidation: повторение, фактчек, недельный квиз.

## Проверка знаний

- По умолчанию — открытые вопросы: объясни своими словами, предскажи результат, найди ошибку, напиши команду или конфиг.
- Multiple choice — только для быстрой проверки; правильный вариант не ставится первым.
- Каждый вопрос и эталонный ответ проверяются по официальному источнику; источник указывается.
- Практические задания проверяются выполнением: запуск, тест, линтер, валидатор.

## 12 недель

| Недели | Тема | Глубина | Артефакт |
|---|---|---|---|
| 1 | Linux internals I | boot, systemd, cgroups v2, namespaces | Unit + cgroup-лимиты + runbook |
| 2 | Linux internals II | memory/CPU/IO, `strace`, `perf`, FS, capabilities, seccomp | Разбор зависания/утечки |
| 3 | Networking I | TCP/IP, routing, NAT, DNS, netfilter, `tcpdump` | Сеть в network namespaces |
| 4 | Networking II | HTTP/1–3, TLS, reverse proxy, load balancing | Nginx + TLS + VPS |
| 5 | Containers internals | namespaces, cgroups, overlayfs, runc/containerd, OCI | Минимальный образ + Compose |
| 6 | Kubernetes I | control plane, etcd, kubelet, CNI/CSI/CRI | kind/k3s + деплой приложения |
| 7 | Kubernetes II | scheduling, probes, resources, RBAC, NetworkPolicy, Helm | Helm-чарт + политики |
| 8 | Kubernetes III | troubleshooting, operators, GitOps | Break/fix + GitOps-репозиторий |
| 9 | IaC | Terraform/OpenTofu, Ansible roles, state, idempotency | Провизion VPS/локального стенда |
| 10 | CI/CD | GitHub Actions/GitLab CI, cache, artifacts, secrets, OIDC | Пайплайн build → scan → deploy |
| 11 | Observability + Security | Prometheus, Grafana, Loki, OTel, SLO, supply chain | Дашборды + алерты + security gates |
| 12 | Capstone + SRE | инциденты, postmortem, runbooks, mock interview | Полный стенд + портфолио |

## Результаты

- 3 проекта в портфолио: VPS + Docker, Kubernetes + CI/CD + observability, IaC + capstone.
- Набор runbook'ов и разборов инцидентов.
- Матрица навыков с доказательствами.
- Подготовка к интервью: troubleshooting, design, security, incident response.

## Связанное

- [[DevOps/Learning Log|Learning Log]]
- [[DevOps/Skills Matrix|Skills Matrix]]
- [[DevOps/Review Queue|Review Queue]]
- [[DevOps/Sources|Sources]]
- [[DevOps/Fact Check Queue|Fact Check Queue]]
