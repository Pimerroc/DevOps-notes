---
type: moc
status: growing
topic: skills
difficulty: 1
created: 2026-11-06
review_at:
verified: true
last_verified: 2026-11-06
tags: [devops, skills]
---

# Skills Matrix

> [!summary] Матрица компетенций: уровень, доказательства, следующий шаг. Заполняется после диагностики и обновляется после каждой сессии.

## Уровни

| Уровень | Значение |
|---|---|
| 0 | Не знаю |
| 1 | Знаю термины, но не делал |
| 2 | Делаю с подсказкой |
| 3 | Делаю самостоятельно |
| 4 | Проектирую, объясняю, ревьюю |

## Матрица

| Домен | Уровень | Доказательства | Следующий шаг |
|---|---|---|---|
| Linux internals | 2 | Диагностика 2/5; с тех пор: эксперименты с LVM, systemd-unit с MemoryMax (cgroup); namespaces: netns/mnt/uts/ipc/user (2026-11-09) | Этап 1: namespaces, cgroups, Type=notify, LVM-лаба |
| Networking | 2 | 4/5; TCP, NAT, DNS, TLS — верно; HTTP-статусы — пробел | Практика: tcpdump, DNS, TLS |
| Git | 2 | rebase — верно | Практика: rebase/merge, конфликты |
| Containers | 1 | 2/5; latest — верно; cache, PID 1, volumes — пробелы | Docker layers, PID 1, volumes |
| Kubernetes | 1 | 3/5; readiness, Deployment, etcd — верно; Service, Secret — пробелы | Service, Secret, practice kind |
| IaC (Terraform/Ansible) | 2 | 5/5; state, plan, idempotency — верно; практики пока нет | Terraform + Ansible lab |
| CI/CD | 2 | 5/5; pipeline order, secrets/OIDC — верно; практики пока нет | GitHub Actions pipeline |
| Observability | 2 | metrics, PromQL rate, SLO — верно | Prometheus/Grafana lab |
| Security | 1 | least privilege — не знаю; остальное не проверялось | RBAC, secrets, supply chain |
| SRE / incidents | 1 | incident priority — верно; практики нет | Incident drill, postmortem |
| Скриптинг (bash/awk) | 2 | свои bash-скрипты с awk, но практики мало | Pipeline drills #1–5; задачи на обработку логов |
| Live-coding (пайплайны) | 2 | пайплайны для логов/текста есть, регулярной практики нет | 30 мин/нед по [[Practice/DevOps/drills/pipelines\|drills]] |
| Go | 1 | опыта нет; старт потока Д | Фаза 1: Tour of Go, Go by Example |

## Итог диагностики

**20/30 (67%).** Сильные стороны: IaC, CI/CD, сети. Приоритет: Linux internals, containers, Kubernetes, security.

Диагностика 2026-11-06 была в формате multiple choice. Дальше основной формат — открытые вопросы и практические задачи с проверкой выполнения, а не выбор варианта.

## Правило обновления

Уровень повышается только при наличии доказательства: лабораторная, проект, runbook, разбор инцидента или открытый ответ, проверенный по источнику. Без доказательства уровень не меняется.
