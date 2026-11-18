---
description: Livecoding in kitty + nvim with non-interfering live analysis
---

Задача: $ARGUMENTS

Язык: если не указан явно — Go; Python — по запросу.

1. Загрузи skill `livecoding` через инструмент skill.
2. Выполни preflight и setup строго по skill.
3. После запуска сессии не вмешивайся: не подсказывай, не задавай вопросы, не комментируй и не проверяй лог, пока пользователь не напишет «готово», «стоп» или явно не попросит помощь.
4. Когда пользователь закончит, запусти `analyze.py`, разбери метрики и код, задай 3 вопроса на рефлексию.
5. Создай отчёт в `DevOpsNotes/Practice/livecoding/<session-id>/README.md` и обнови Learning Log, Skills Matrix, Review Queue и Board.
