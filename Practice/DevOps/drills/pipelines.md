---
type: lab
status: seed
topic: bash-pipelines
difficulty: 2
created: 2026-11-09
review_at: 2026-11-10
verified: false
last_verified:
tags: [devops, bash, awk, logs]
---

# Pipeline drills

> [!summary] 10 задач на пайплайны по логам. Одна задача = 30 минут, без AI; после — сверка с эталоном и запись в [[DevOps/Review Queue|Review Queue]].

## Правила

- Одна задача за подход, 30 минут.
- Запрещено: просить AI, искать готовый ответ, редактировать входной файл.
- Разрешено: `man`, `--help`, одна заметка с синтаксисом.
- Скрипт — `set -euo pipefail`; пайплайн — одной строкой, если получается.
- После: время, что сломалось, эталон, confidence 1–5.

## Вход

Любой `access.log` в формате nginx combined + `$request_time`:

```text
$remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent" $request_time
```

Своего лога нет — сгенерируй 2000 строк или возьми `/var/log/nginx/access.log`. Формат проверь `head -1`.

## Задачи

1. **Top-10 IP по числу запросов.** Вывод: `count ip`, по убыванию. Проверка: сумма counts = `wc -l`.
2. **Доля 5xx по часам.** Вывод: `hour total_5xx total percent`. Проверка: percent = 5xx/total×100, сумма total = числу строк.
3. **Top-5 URL по среднему `$request_time`.** Вывод: `avg_time count path`; пропусти строки, где время `-`.
4. **Уникальные User-Agent.** Выведи количество уникальных и top-3 по частоте.
5. **Пик запросов в минуту.** Вывод: `minute count` для максимума; проверь, что минута действительно пиковая.
6. **Top-10 404-путей.** Вывод: `count path`; проверь, что все статусы 404.
7. **Email-адреса из текста.** Из произвольного файла вытащи все email, посчитай по доменам: `count domain`.
8. **JSON-логи через `jq`.** Для строк вида `{"time":"...","request":"...","status":500,"request_time":0.12}` выведи top-10 `request` по количеству.
9. **Дедупликация с сохранением порядка.** Убери повторные строки, оставь первое вхождение; выведи `строк_было строк_стало`. Проверка: `sort -u | wc -l` совпадает с числом уникальных.
10. **`key=value` → CSV.** Для строк `ts=... level=... msg="..."` собери CSV с колонками `ts,level,msg`; отсутствующий ключ — пустое поле.

## Проверка

- Для каждой задачи — эталонный пайплайн и 3 контрольные строки (`grep`/`sed -n`).
- Скрипт — `shellcheck`; пайплайн — `bash -n` не нужен, но проверь `set -o pipefail`.
- Результат: дата, задача, время, confidence, что не получилось — в [[DevOps/Review Queue|Review Queue]].
- Провал (<3) — повторить через 3 дня; успех (4–5) — следующий drill.

## Cleanup

Временные файлы — в `/tmp/opencode/drills/`, после задачи удалить: `rm -rf /tmp/opencode/drills`.
