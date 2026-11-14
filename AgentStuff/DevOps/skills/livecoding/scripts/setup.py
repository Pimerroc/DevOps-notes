#!/usr/bin/env python3
"""Create a livecoding session and launch kitty + nvim with the logger."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT = Path(__file__).resolve()
SKILL_DIR = SCRIPT.parents[1]
ROOT = SCRIPT.parents[4]
LIVE_ROOT = Path(os.environ.get("LIVECODING_LOG_ROOT", str(Path.home() / ".local/share/livecoding")))
PRACTICE_ROOT = ROOT / "DevOpsNotes/Practice/livecoding"
LOGGER = SKILL_DIR / "scripts/nvim_logger.lua"
WATCH = SKILL_DIR / "scripts/watch.py"


def slugify(topic: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", topic.lower()).strip("-")
    if not slug:
        slug = hashlib.sha1(topic.encode("utf-8")).hexdigest()[:8]
    return slug[:40]


def make_launch_script(
    path: Path,
    *,
    log_path: Path,
    session_id: str,
    topic: str,
    workspace: Path,
    file_path: Path,
) -> None:
    logger = str(LOGGER).replace("'", "\\'")
    lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        f"export LIVECODING_LOG={shlex.quote(str(log_path))}",
        f"export LIVECODING_SESSION={shlex.quote(session_id)}",
        f"export LIVECODING_TOPIC={shlex.quote(topic)}",
        "",
        "kitty --detach --title {} --directory {} nvim --cmd {} {}".format(
            shlex.quote(f"Livecoding: {topic}"),
            shlex.quote(str(workspace)),
            shlex.quote(f"lua dofile('{logger}')"),
            shlex.quote(str(file_path)),
        ),
        "kitty --detach --title {} python3 {} {}".format(
            shlex.quote(f"Livecoding metrics: {topic}"),
            shlex.quote(str(WATCH)),
            shlex.quote(str(path.parent / "session.json")),
        ),
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    path.chmod(0o700)


def main() -> int:
    parser = argparse.ArgumentParser(description="Set up a livecoding session")
    parser.add_argument("--topic", required=True, help="Topic of the session")
    parser.add_argument("--task", default="", help="Task or goal")
    parser.add_argument("--file", default="main.py", help="File inside workspace")
    parser.add_argument("--workspace", help="Override workspace directory")
    parser.add_argument("--no-launch", action="store_true", help="Only create files and launch.sh")
    args = parser.parse_args()

    if shutil.which("nvim") is None:
        print("ERROR: nvim not found", file=sys.stderr)
        return 1

    now = datetime.now(timezone.utc)
    session_id = f"{now.strftime('%Y-%m-%d_%H-%M-%S')}_{slugify(args.topic)}"
    session_dir = PRACTICE_ROOT / session_id
    workspace = Path(args.workspace).expanduser().resolve() if args.workspace else session_dir / "workspace"
    workspace.mkdir(parents=True, exist_ok=True)
    session_dir.mkdir(parents=True, exist_ok=True)

    file_path = (workspace / args.file).resolve()
    file_path.parent.mkdir(parents=True, exist_ok=True)
    if not file_path.exists():
        suffix = file_path.suffix.lower()
        if suffix == ".py":
            starter = f"# Livecoding: {args.topic}\n# Task: {args.task or '—'}\n\n"
        elif suffix in {".md", ".txt"}:
            starter = f"# {args.topic}\n\n{args.task or ''}\n\n"
        else:
            starter = ""
        file_path.write_text(starter, encoding="utf-8")

    log_dir = LIVE_ROOT / session_id
    log_dir.mkdir(parents=True, exist_ok=True)
    log_dir.chmod(0o700)
    log_path = log_dir / "session.jsonl"
    log_path.touch(exist_ok=True)
    log_path.chmod(0o600)

    meta = {
        "session_id": session_id,
        "topic": args.topic,
        "task": args.task,
        "workspace": str(workspace),
        "file": str(file_path),
        "log": str(log_path),
        "started_at": now.isoformat(),
        "status": "running",
    }
    session_path = session_dir / "session.json"
    session_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    launch_path = session_dir / "launch.sh"
    make_launch_script(
        launch_path,
        log_path=log_path,
        session_id=session_id,
        topic=args.topic,
        workspace=workspace,
        file_path=file_path,
    )

    logger = str(LOGGER).replace("'", "\\'")
    env = os.environ.copy()
    env["LIVECODING_LOG"] = str(log_path)
    env["LIVECODING_SESSION"] = session_id
    env["LIVECODING_TOPIC"] = args.topic

    nvim_cmd = [
        "kitty",
        "--detach",
        "--title",
        f"Livecoding: {args.topic}",
        "--directory",
        str(workspace),
        "nvim",
        "--cmd",
        f"lua dofile('{logger}')",
        str(file_path),
    ]
    watch_cmd = [
        "kitty",
        "--detach",
        "--title",
        f"Livecoding metrics: {args.topic}",
        "python3",
        str(WATCH),
        str(session_path),
    ]

    print(f"session:   {session_path}")
    print(f"workspace: {workspace}")
    print(f"file:      {file_path}")
    print(f"log:       {log_path}")
    print(f"launch:    {launch_path}")

    if args.no_launch:
        print("status:    created (--no-launch)")
        print("nvim:      " + shlex.join(nvim_cmd))
        print("metrics:   " + shlex.join(watch_cmd))
        return 0

    if shutil.which("kitty") is None:
        print("status:    kitty not found; run launch.sh manually", file=sys.stderr)
        return 0

    nvim_result = subprocess.run(
        nvim_cmd,
        env=env,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if nvim_result.returncode != 0:
        print(f"status:    kitty/nvim failed: {nvim_result.stderr.strip()}", file=sys.stderr)
        print(f"fallback:  {launch_path}", file=sys.stderr)
        return 0

    watch_result = subprocess.run(
        watch_cmd,
        env=env,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if watch_result.returncode != 0:
        print(f"status:    nvim launched; metrics window failed: {watch_result.stderr.strip()}", file=sys.stderr)
        print(f"fallback:  {launch_path}", file=sys.stderr)
        return 0

    print("status:    launched")
    print("next:      работай; когда закончишь, напиши «готово»")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
