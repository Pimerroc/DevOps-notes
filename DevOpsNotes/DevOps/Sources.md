---
type: reference
status: growing
topic: sources
difficulty: 1
created: 2026-11-06
review_at:
verified: true
last_verified: 2026-11-06
tags: [devops, sources]
---

# Sources

> [!summary] Доверенные источники для фактчека. Приоритет: официальная документация → release notes → man/--help → локальный эксперимент → качественный вторичный источник.

## Официальная документация

| Тема | Источник |
|---|---|
| Linux kernel | https://docs.kernel.org/ |
| Linux man pages | https://man7.org/linux/man-pages/ |
| systemd | https://www.freedesktop.org/software/systemd/man/latest/ |
| Docker | https://docs.docker.com/ |
| Kubernetes | https://kubernetes.io/docs/ |
| Terraform | https://developer.hashicorp.com/terraform/docs |
| OpenTofu | https://opentofu.org/docs/ |
| Ansible | https://docs.ansible.com/ |
| GitHub Actions | https://docs.github.com/en/actions |
| GitLab CI | https://docs.gitlab.com/ee/ci/ |
| Prometheus | https://prometheus.io/docs/ |
| Grafana | https://grafana.com/docs/ |
| OpenTelemetry | https://opentelemetry.io/docs/ |
| Argo CD | https://argo-cd.readthedocs.io/ |
| Flux | https://fluxcd.io/flux/ |
| CNCF | https://www.cncf.io/ |
| OWASP | https://owasp.org/ |
| CIS Benchmarks | https://www.cisecurity.org/cis-benchmarks |
| NIST | https://www.nist.gov/ |

## Правила проверки

1. Сначала локальное поведение: `--help`, `--version`, `man`, `--dry-run`.
2. Затем официальная документация и release notes.
3. Для конфигов — валидаторы и линтеры.
4. Для облака — документация провайдера и проверка в временном окружении.
5. Блог, Stack Overflow и AI-ответ — не источник истины; только подсказка, что проверить.

## Книги и учебные ресурсы

> [!note] Добавлено агентом

**Сейчас:** Docker Deep Dive, 2025 edition — Nigel Poulton. Этап 3: слои, образы, контейнеры, volumes, Compose, networking.

**Позже, по мере этапов:**
- Ansible: Up and Running, 3rd ed. — Bas Meijer, Lorin Hochstein, René Moser. Этап 4; Ansible применим почти везде.
- CI/CD: официальная документация GitLab CI/CD + GitHub Actions in Action — Michael Kaufmann, Rob Bos, Marcel de Vries. Этап 5; закрывает GitLab и GitHub Actions.
- The Kubernetes Book — Nigel Poulton. Этап 6.

**Отложено:** Terraform: Up & Running — не приоритет для джуна; вернуться, когда появится реальная IaC-задача.

## Связанное

- [[DevOps/Fact Check Queue|Fact Check Queue]]
