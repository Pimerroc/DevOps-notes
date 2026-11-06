---
type: queue
status: growing
topic: review
difficulty: 1
created: 2026-11-06
review_at:
verified: true
last_verified: 2026-11-06
tags: [devops, review]
---

# Review Queue

> [!summary] Очередь повторения. Сюда попадают заметки и темы, которые нужно проверить через 1, 3, 7, 14 или 30 дней.

| Заметка | Тема | review_at | confidence 1-5 | Статус |
|---|---|---|---|---|
| [[DevOps/Diagnostics/2026-11-06]] | Linux internals: namespaces, systemd, overlayfs | 2026-11-09 | 1 | pending |
| [[DevOps/Diagnostics/2026-11-06]] | Containers: layers, PID 1, volumes | 2026-11-10 | 1 | pending |
| [[DevOps/Diagnostics/2026-11-06]] | Kubernetes: Service, Secret, RBAC | 2026-11-12 | 2 | pending |
| [[DevOps/Diagnostics/2026-11-06]] | Security: least privilege, secrets at rest | 2026-11-12 | 1 | pending |

## Правила

- `review_at` ставится при создании заметки.
- После успешного повторения интервал увеличивается: 1 → 3 → 7 → 14 → 30 дней.
- Если тема забыта — интервал сокращается.
- Просроченные заметки имеют приоритет.
- В недельное повторение включаются только заметки с `review_at <= сегодня`.
