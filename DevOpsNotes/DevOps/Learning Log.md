---
type: log
status: growing
topic: learning-log
difficulty: 1
created: 2026-11-06
review_at:
verified: true
last_verified: 2026-11-06
tags: [devops, log]
---

# Learning Log

> [!summary] Журнал учебных и рабочих сессий: что сделано, какой артефакт, какие пробелы, следующий шаг.

| Дата | Тема | Режим | Что сделано | Артефакт | Пробелы | Следующий шаг |
|---|---|---|---|---|---|---|
| 2026-11-06 | Старт | setup | Создан учебный контур и агенты | [[DevOps/Roadmap]] | Диагностика не пройдена | `/diagnostic` |
| 2026-11-06 | Стартовая диагностика | diagnostic | 20/30 (67%); сильные — IaC/CI-CD и сети, слабые — Linux internals, containers, K8s, security | [[DevOps/Diagnostics/2026-11-06]] | namespaces, systemd, Docker layers, Service/Secret, least privilege | Модуль 1: Linux internals |
| 2026-11-06 | Livecoding | build | Скилл kitty + nvim: JSONL-логгер, live-метрики, анализ; smoke-тесты пройдены | `.opencode/skills/livecoding/SKILL.md` | живой ввод с клавиатуры не проверен | Первая сессия `/live` |
| 2026-11-07 | Планирование | plan | Roadmap переписан на 8 этапов с MIN/MAX днями; канбан [[DevOps/Board\|Board]]; агенты перенесены в `.zcode/`; добавлены потоки Go, реальные задачи, тренды | [[DevOps/Roadmap]] | день-за-днём детализирован только этап 1 | День 1 этапа 1: namespaces-лаба |

## Как вести

- Одна строка на сессию.
- «Что сделано» — результат, а не процесс.
- «Артефакт» — ссылка на заметку, лабораторную или runbook.
- «Пробелы» — что не получилось или осталось непонятным.
- «Следующий шаг» — конкретное действие на следующую сессию.
