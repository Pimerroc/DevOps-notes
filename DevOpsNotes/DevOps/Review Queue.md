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
| Таненбаум гл. 7 | Прикладной уровень: DNS, HTTP, email, CDN (заметка не сделана) | 2026-11-11 | 2 | pending |
| HTTP-статусы | 504 vs 502 vs 503 vs 301/308 — пробел диагностики | 2026-11-09 | 2 | pending |
| [[Practice/DevOps/harness/README\|harness]] | systemd timers → opencode run: одна сессия, `--auto`, Persistent | 2026-11-15 | 3 | pending |
| [[DevOps/Notes/Linux/Network namespace]] | Network namespace: `unshare --net`, veth, перенос интерфейса, cleanup (Д2) | 2026-11-16 | 3 | pending |
| — | Go: Tour of Go, старт фазы 1 (переносится) | 2026-11-09 | 1 | pending |
| [[DevOps/Notes/Linux/Namespaces]] | 8 типов ns, mnt/uts/ipc/user, uid_map — active recall | 2026-11-10 | 2 | pending |
| [[DevOps/Notes/Linux/Namespaces]] | фактчек Q1/Q2/Q4: uid_map, `--fork`, `--mount-proc`; лабы mnt/uts/ipc — `verified: false` | 2026-11-10 | 1 | done |
| [[Linux/Сценарии Bash (кратко)]] | bash: pipes, awk/sed/grep/xargs, exit codes | 2026-11-10 | 2 | pending |
| [[Practice/DevOps/drills/pipelines]] | pipeline drills #1–10: nginx logs, awk/jq | 2026-11-10 | 1 | pending |
| How Linux Works (PDF) | boot/systemd, processes, memory, fs — 5 вопросов | 2026-11-12 | 2 | pending |
| Таненбаум гл. 7–8 | квиз: DNS/HTTP/TLS/DNSSEC/security | 2026-11-11 | 2 | pending |

## Правила

- `review_at` ставится при создании заметки.
- Повторение = active recall: 5 вопросов или 1 задача без заметок, потом сверка с источником.
- Confidence 1–2 → интервал 1 день; 3 → оставить; 4–5 → следующий (1 → 3 → 7 → 14 → 30).
- Для практических тем (bash, livecoding) повторение — задача на время, не перечитывание.
- Если тема забыта — интервал сокращается.
- Просроченные заметки имеют приоритет.
- В недельное повторение включаются только заметки с `review_at <= сегодня`.
