#!/usr/bin/env python3
"""Live dashboard for a livecoding session. Read-only: does not touch the workspace."""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from analyze import compute_metrics, fmt_duration, load_events

CLEAR = "\033[2J\033[H"


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: watch.py <session.json>")
        return 2
    session_path = Path(sys.argv[1]).expanduser().resolve()
    if not session_path.exists():
        print(f"session.json not found: {session_path}")
        return 1
    meta = json.loads(session_path.read_text(encoding="utf-8"))
    log_path = Path(meta["log"]).expanduser().resolve()
    topic = meta.get("topic", "Livecoding")

    try:
        while True:
            events = load_events(log_path)
            metrics = compute_metrics(events, meta)
            print(CLEAR, end="")
            print(f"LIVECODING  {topic}")
            print("=" * 60)
            if not events:
                print(f"waiting for: {log_path}")
                print("Открой nvim и начни работу. Окно обновляется каждую секунду.")
                time.sleep(1)
                continue
            print(
                f"elapsed {fmt_duration(metrics['duration_s'])}  "
                f"active {fmt_duration(metrics['active_s'])}  "
                f"idle {fmt_duration(metrics['idle_s'])}"
            )
            print(
                f"edits {len([e for e in events if e.get('event') == 'edit'])}  "
                f"chars +{metrics['inserted_chars']} / -{metrics['deleted_chars']}  "
                f"delete {metrics['delete_ratio']:.0%}"
            )
            print(
                f"chars/min {metrics['chars_per_min']}  "
                f"wpm {metrics['wpm']}  "
                f"keys/min {metrics['keys_per_min']}"
            )
            print(
                f"pauses>30s {len(metrics['pauses'])}  "
                f"longest {fmt_duration(metrics['longest_pause_s'])}"
            )
            print(
                f"saves {metrics['saves']}  "
                f"files {len(metrics['files'])}  "
                f"LSP E{metrics['diagnostics'].get('max_errors', 0)} "
                f"W{metrics['diagnostics'].get('max_warnings', 0)}"
            )
            print("=" * 60)
            for signal in metrics.get("heuristics", [])[:3]:
                print(f"signal: {signal}")
            if metrics.get("commands"):
                top = ", ".join(f"{k}×{v}" for k, v in list(metrics["commands"].items())[:5])
                print(f"commands: {top}")
            last = events[-1]
            print(f"last: {last.get('event')}  {last.get('ts', '')}")
            detail = last.get("file") or last.get("cmd") or last.get("mode") or ""
            if detail:
                print(f"      {detail}")
            print("\nCtrl+C закрывает только это окно. Работа продолжается.")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nmetrics window closed")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
