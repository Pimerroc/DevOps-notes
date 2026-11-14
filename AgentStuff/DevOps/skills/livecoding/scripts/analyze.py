#!/usr/bin/env python3
"""Analyze a livecoding JSONL session and write metrics.json + summary.md."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

IDLE_SECONDS = 30.0
LARGE_REVERT = -50


def load_events(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    if not path.exists():
        return events
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(obj, dict):
                events.append(obj)
    events.sort(key=lambda e: e.get("ms", 0))
    return events


def fmt_duration(seconds: float) -> str:
    seconds = max(0, int(round(seconds)))
    hours, rem = divmod(seconds, 3600)
    minutes, secs = divmod(rem, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def compute_metrics(events: list[dict[str, Any]], meta: dict[str, Any]) -> dict[str, Any]:
    if not events:
        return {
            "session_id": meta.get("session_id", ""),
            "topic": meta.get("topic", ""),
            "task": meta.get("task", ""),
            "workspace": meta.get("workspace", ""),
            "file": meta.get("file", ""),
            "events": 0,
            "duration_s": 0,
            "active_s": 0,
            "idle_s": 0,
            "inserted_chars": 0,
            "deleted_chars": 0,
            "chars_per_min": 0,
            "keystrokes": 0,
            "typed_chars": 0,
            "keys_per_min": 0,
            "wpm": 0,
            "delete_ratio": 0,
            "pauses": [],
            "large_reverts": [],
            "saves": 0,
            "commands": {},
            "files": [],
            "diagnostics": {},
            "focus_lost": 0,
            "mode_switches": 0,
            "heuristics": ["Нет событий: nvim-логгер не запустился или сессия не началась."],
            "timeline": [],
        }

    start_ms = events[0].get("ms", 0)
    end_ms = events[-1].get("ms", start_ms)
    duration_s = max(0.0, (end_ms - start_ms) / 1000)

    gaps: list[tuple[dict[str, Any], dict[str, Any], float]] = []
    idle_s = 0.0
    pauses: list[dict[str, Any]] = []
    for prev, cur in zip(events, events[1:]):
        gap = max(0.0, (cur.get("ms", 0) - prev.get("ms", 0)) / 1000)
        gaps.append((prev, cur, gap))
        if gap > IDLE_SECONDS:
            idle_s += gap - IDLE_SECONDS
            pauses.append(
                {
                    "from": prev.get("ts"),
                    "to": cur.get("ts"),
                    "seconds": round(gap, 1),
                }
            )

    active_s = max(0.0, duration_s - idle_s)
    edit_events = [e for e in events if e.get("event") == "edit"]
    inserted = sum(int(e.get("delta", 0)) for e in edit_events if int(e.get("delta", 0)) > 0)
    deleted = -sum(int(e.get("delta", 0)) for e in edit_events if int(e.get("delta", 0)) < 0)
    total_changed = inserted + deleted
    delete_ratio = (deleted / total_changed) if total_changed else 0.0
    chars_per_min = (inserted / (active_s / 60)) if active_s > 0 else 0.0

    key_events = [e for e in events if e.get("event") == "keys"]
    keystrokes = sum(int(e.get("keys", 0)) for e in key_events)
    typed_chars = sum(int(e.get("typed", 0)) for e in key_events)
    keys_per_min = (keystrokes / (active_s / 60)) if active_s > 0 else 0.0
    # Standard typing WPM: one word = 5 characters.
    wpm = (chars_per_min / 5) if chars_per_min else 0.0

    large_reverts = [
        {
            "ts": e.get("ts"),
            "file": e.get("file"),
            "delta": int(e.get("delta", 0)),
        }
        for e in edit_events
        if int(e.get("delta", 0)) <= LARGE_REVERT
    ]

    cmd_counter: Counter[str] = Counter()
    for e in events:
        if e.get("event") != "cmdline":
            continue
        cmd = str(e.get("cmd", "")).strip()
        if cmd:
            cmd_counter[cmd[:20]] += 1

    files: list[str] = []
    for e in events:
        if e.get("event") == "buf_enter":
            name = e.get("file") or ""
            if name and name not in files:
                files.append(name)

    diag_events = [e for e in events if e.get("event") == "diagnostics"]
    latest_diag = diag_events[-1].get("counts", {}) if diag_events else {}
    max_errors = max((int(e.get("counts", {}).get("ERROR", 0)) for e in diag_events), default=0)
    max_warnings = max((int(e.get("counts", {}).get("WARN", 0)) for e in diag_events), default=0)

    focus_lost = sum(1 for e in events if e.get("event") == "focus" and e.get("state") == "FocusLost")
    mode_switches = sum(1 for e in events if e.get("event") == "mode")
    saves = sum(1 for e in events if e.get("event") == "save")
    longest_pause = max((p["seconds"] for p in pauses), default=0.0)

    heuristics: list[str] = []
    if delete_ratio > 0.35:
        heuristics.append(
            f"Высокая доля удалений: {delete_ratio:.0%}. Много переписывания или борьбы с синтаксисом."
        )
    if len(large_reverts) >= 3:
        heuristics.append(
            f"Крупных откатов: {len(large_reverts)}. Похоже на перепроектирование по ходу."
        )
    if longest_pause > 120:
        heuristics.append(
            f"Самая длинная пауза: {fmt_duration(longest_pause)}. Проверить, где именно и почему."
        )
    if saves > 10:
        heuristics.append(f"Сохранений: {saves}. Частые сохранения могут быть признаком тревоги или мелких шагов.")
    if max_errors > 0:
        heuristics.append(f"LSP фиксировал до {max_errors} ошибок. Проверить, исправлены ли они к концу.")
    if duration_s > 0 and active_s / duration_s < 0.5:
        heuristics.append("Активное время меньше половины сессии: много пауз или переключений.")
    if not heuristics:
        heuristics.append("Резких поведенческих сигналов нет. Смотреть на код и ретроспективу.")

    timeline: list[dict[str, Any]] = []
    first_edit = edit_events[0] if edit_events else None
    for e in events:
        kind = e.get("event")
        if kind == "start":
            timeline.append({"ts": e.get("ts"), "kind": "start", "detail": e.get("cwd", "")})
        elif kind == "stop":
            timeline.append(
                {"ts": e.get("ts"), "kind": "stop", "detail": fmt_duration(duration_s)}
            )
        elif kind == "save":
            timeline.append({"ts": e.get("ts"), "kind": "save", "detail": e.get("file", "")})
        elif kind == "diagnostics":
            counts = e.get("counts", {})
            if int(counts.get("ERROR", 0)) > 0:
                timeline.append(
                    {
                        "ts": e.get("ts"),
                        "kind": "diagnostics",
                        "detail": f"E{counts.get('ERROR', 0)} W{counts.get('WARN', 0)}",
                    }
                )
    if first_edit:
        timeline.append(
            {
                "ts": first_edit.get("ts"),
                "kind": "first_edit",
                "detail": first_edit.get("file", ""),
            }
        )
    for p in pauses:
        if p["seconds"] > 60:
            timeline.append(
                {
                    "ts": p.get("from"),
                    "kind": "pause",
                    "detail": fmt_duration(p["seconds"]),
                }
            )
    for r in large_reverts:
        timeline.append(
            {
                "ts": r.get("ts"),
                "kind": "large_revert",
                "detail": f"{r.get('delta')} chars",
            }
        )
    timeline.sort(key=lambda item: item.get("ts") or "")
    timeline = timeline[:60]

    return {
        "session_id": meta.get("session_id", ""),
        "topic": meta.get("topic", ""),
        "task": meta.get("task", ""),
        "workspace": meta.get("workspace", ""),
        "file": meta.get("file", ""),
        "started_at": events[0].get("ts"),
        "ended_at": events[-1].get("ts"),
        "events": len(events),
        "duration_s": round(duration_s, 1),
        "active_s": round(active_s, 1),
        "idle_s": round(idle_s, 1),
        "inserted_chars": inserted,
        "deleted_chars": deleted,
        "chars_per_min": round(chars_per_min, 1),
        "keystrokes": keystrokes,
        "typed_chars": typed_chars,
        "keys_per_min": round(keys_per_min, 1),
        "wpm": round(wpm, 1),
        "delete_ratio": round(delete_ratio, 3),
        "pauses": pauses,
        "longest_pause_s": round(longest_pause, 1),
        "large_reverts": large_reverts,
        "saves": saves,
        "commands": dict(cmd_counter.most_common()),
        "files": files,
        "diagnostics": {
            "latest": latest_diag,
            "max_errors": max_errors,
            "max_warnings": max_warnings,
            "events": len(diag_events),
        },
        "focus_lost": focus_lost,
        "mode_switches": mode_switches,
        "heuristics": heuristics,
        "timeline": timeline,
    }


def build_summary(metrics: dict[str, Any]) -> str:
    topic = metrics.get("topic") or "Livecoding"
    lines: list[str] = [
        f"# Livecoding: {topic}",
        "",
        f"- Задача: {metrics.get('task') or '—'}",
        f"- Workspace: `{metrics.get('workspace') or '—'}`",
        f"- Файл: `{metrics.get('file') or '—'}`",
        f"- Начало: {metrics.get('started_at') or '—'}",
        f"- Конец: {metrics.get('ended_at') or '—'}",
        "",
        "## Метрики",
        "",
        "| Метрика | Значение |",
        "|---|---|",
        f"| Длительность | {fmt_duration(metrics.get('duration_s', 0))} |",
        f"| Активное время | {fmt_duration(metrics.get('active_s', 0))} |",
        f"| Паузы (idle) | {fmt_duration(metrics.get('idle_s', 0))} |",
        f"| Символы в минуту | {metrics.get('chars_per_min', 0)} |",
        f"| Скорость (WPM) | {metrics.get('wpm', 0)} |",
        f"| Нажатий / typed | {metrics.get('keystrokes', 0)} / {metrics.get('typed_chars', 0)} |",
        f"| Нажатий в минуту | {metrics.get('keys_per_min', 0)} |",
        f"| Вставлено / удалено | +{metrics.get('inserted_chars', 0)} / −{metrics.get('deleted_chars', 0)} |",
        f"| Доля удалений | {metrics.get('delete_ratio', 0):.0%} |",
        f"| Пауз > 30 с | {len(metrics.get('pauses', []))} |",
        f"| Самая длинная пауза | {fmt_duration(metrics.get('longest_pause_s', 0))} |",
        f"| Крупных откатов | {len(metrics.get('large_reverts', []))} |",
        f"| Сохранений | {metrics.get('saves', 0)} |",
        f"| Переключений файлов | {len(metrics.get('files', []))} |",
        f"| Ошибок LSP (макс.) | {metrics.get('diagnostics', {}).get('max_errors', 0)} |",
        f"| Предупреждений LSP (макс.) | {metrics.get('diagnostics', {}).get('max_warnings', 0)} |",
        f"| Потеря фокуса | {metrics.get('focus_lost', 0)} |",
        "",
        "## Наблюдения",
        "",
    ]
    for item in metrics.get("heuristics", []):
        lines.append(f"- {item}")
    lines += ["", "## Таймлайн", "", "| Время | Событие | Детали |", "|---|---|---|"]
    for item in metrics.get("timeline", []):
        lines.append(f"| {item.get('ts', '—')} | {item.get('kind', '—')} | {item.get('detail', '')} |")
    lines += [
        "",
        "## Вопросы на рефлексию",
        "",
        "1. Где были паузы дольше 60 секунд и о чём ты думал в этот момент?",
        "2. Какие крупные откаты были и почему решение изменилось?",
        "3. Что бы ты сделал иначе в следующей похожей задаче?",
        "",
        "## Ограничения",
        "",
        "- Это поведенческие метрики, а не оценка мышления.",
        "- Причины пауз и откатов выясняются ретроспективой и ревью кода.",
        "- Сырой лог хранится вне vault и не коммитится.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze a livecoding session")
    parser.add_argument("--session", required=True, help="Path to session.json")
    parser.add_argument("--log", help="Override log path")
    args = parser.parse_args()

    session_path = Path(args.session).expanduser().resolve()
    if not session_path.exists():
        print(f"session.json not found: {session_path}")
        return 1
    meta = json.loads(session_path.read_text(encoding="utf-8"))
    log_path = Path(args.log).expanduser().resolve() if args.log else Path(meta["log"]).expanduser().resolve()

    events = load_events(log_path)
    if not events:
        print(f"No events in {log_path}")
        return 1

    metrics = compute_metrics(events, meta)
    metrics_path = session_path.parent / "metrics.json"
    summary_path = session_path.parent / "summary.md"
    metrics_path.write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary_path.write_text(build_summary(metrics), encoding="utf-8")

    print(f"metrics: {metrics_path}")
    print(f"summary: {summary_path}")
    print(
        f"duration={fmt_duration(metrics['duration_s'])} "
        f"active={fmt_duration(metrics['active_s'])} "
        f"chars/min={metrics['chars_per_min']} "
        f"wpm={metrics['wpm']} "
        f"keys/min={metrics['keys_per_min']} "
        f"delete={metrics['delete_ratio']:.0%} "
        f"pauses={len(metrics['pauses'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
