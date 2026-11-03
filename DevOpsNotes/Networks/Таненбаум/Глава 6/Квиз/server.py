#!/usr/bin/env python3
"""Локальный сервер для квиза по главе 6.

Зачем: браузерная страница quiz.html умеет работать сама по себе, но тогда
результат приходится скачивать вручную. Этот сервер добавляет автоматическое
сохранение: после прохождения квиза JSON попадает в results/latest.json,
откуда его может прочитать агент.

Запуск:
    python3 server.py
    python3 server.py --port 8766 --no-browser

Маршруты:
    GET  /                 — страница квиза
    GET  /api/health       — проверка, что сервер жив
    GET  /api/latest       — последний сохранённый результат
    POST /api/save         — сохранить результат
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import threading
import webbrowser
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

BASE_DIR = Path(__file__).resolve().parent
QUIZ_FILE = BASE_DIR / "quiz.html"
RESULTS_DIR = BASE_DIR / "results"
MAX_BODY_BYTES = 1_000_000
EXPECTED_ANSWERS = 15


def write_json_atomic(path: Path, payload: dict) -> None:
    """Пишет JSON через временный файл, чтобы не оставить половину файла."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    os.replace(temporary, path)


class QuizHandler(BaseHTTPRequestHandler):
    server_version = "Ch6Quiz/1.0"

    # ---------- ответы ----------

    def _send(
        self,
        status: int,
        body: bytes | str,
        content_type: str = "application/json; charset=utf-8",
    ) -> None:
        if isinstance(body, str):
            body = body.encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, status: int, payload: dict) -> None:
        self._send(status, json.dumps(payload, ensure_ascii=False, indent=2))

    def _not_found(self) -> None:
        self._json(404, {"ok": False, "error": "not found"})

    # ---------- CORS ----------

    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Max-Age", "86400")
        self.end_headers()

    # ---------- GET ----------

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path

        if path in ("/", "/index.html", "/quiz.html"):
            if not QUIZ_FILE.exists():
                self._json(500, {"ok": False, "error": "quiz.html not found"})
                return
            self._send(200, QUIZ_FILE.read_bytes(), "text/html; charset=utf-8")
            return

        if path == "/api/health":
            self._json(200, {"ok": True, "quiz": "ch6-transport"})
            return

        if path == "/api/latest":
            latest = RESULTS_DIR / "latest.json"
            if latest.exists():
                self._send(200, latest.read_bytes(), "application/json; charset=utf-8")
            else:
                self._json(404, {"ok": False, "error": "no results yet"})
            return

        self._not_found()

    # ---------- POST ----------

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path != "/api/save":
            self._not_found()
            return

        length_header = self.headers.get("Content-Length")
        try:
            length = int(length_header or "0")
        except ValueError:
            self._json(400, {"ok": False, "error": "bad Content-Length"})
            return

        if length <= 0:
            self._json(411, {"ok": False, "error": "Content-Length required"})
            return
        if length > MAX_BODY_BYTES:
            self._json(413, {"ok": False, "error": "payload too large"})
            return

        raw = self.rfile.read(length)
        try:
            payload = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._json(400, {"ok": False, "error": "invalid JSON"})
            return

        error = validate_payload(payload)
        if error:
            self._json(400, {"ok": False, "error": error})
            return

        saved_at = datetime.now().astimezone().isoformat(timespec="seconds")
        payload["savedAt"] = saved_at

        RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        base_name = f"quiz-ch6-{stamp}"
        target = RESULTS_DIR / f"{base_name}.json"
        counter = 2
        while target.exists():
            target = RESULTS_DIR / f"{base_name}-{counter}.json"
            counter += 1

        write_json_atomic(target, payload)
        write_json_atomic(RESULTS_DIR / "latest.json", payload)

        relative = target.relative_to(BASE_DIR).as_posix()
        self._json(200, {"ok": True, "file": relative, "savedAt": saved_at})

    # ---------- логи ----------

    def log_message(self, fmt: str, *args) -> None:
        stamp = datetime.now().strftime("%H:%M:%S")
        sys.stderr.write(f"[{stamp}] {fmt % args}\n")


def validate_payload(payload: object) -> str | None:
    """Минимальная проверка, чтобы в results не попал случайный мусор."""
    if not isinstance(payload, dict):
        return "payload must be an object"
    if payload.get("quiz") != "ch6-transport":
        return "unknown quiz"
    answers = payload.get("answers")
    if not isinstance(answers, list) or len(answers) != EXPECTED_ANSWERS:
        return f"expected {EXPECTED_ANSWERS} answers"

    for index, item in enumerate(answers, start=1):
        if not isinstance(item, dict):
            return f"answer {index} must be an object"
        if item.get("id") != index:
            return f"answer {index} has wrong id"
        if item.get("selected") not in ("A", "B", "C", "D"):
            return f"answer {index} has wrong selected value"
        if item.get("correct") not in ("A", "B", "C", "D"):
            return f"answer {index} has wrong correct value"
        if item.get("confidence") not in (1, 2, 3):
            return f"answer {index} has wrong confidence value"

    return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Локальный сервер для квиза по главе 6.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8765,
        help="порт на 127.0.0.1 (по умолчанию 8765)",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="не открывать браузер автоматически",
    )
    args = parser.parse_args()

    if not QUIZ_FILE.exists():
        print(f"Не найден файл квиза: {QUIZ_FILE}", file=sys.stderr)
        return 1

    try:
        server = ThreadingHTTPServer(("127.0.0.1", args.port), QuizHandler)
    except OSError as exc:
        print(f"Не удалось занять 127.0.0.1:{args.port}: {exc}", file=sys.stderr)
        print("Попробуй другой порт: python3 server.py --port 8766", file=sys.stderr)
        return 1

    url = f"http://127.0.0.1:{args.port}/"
    print("Глава 6 · квиз")
    print(f"Страница:   {url}")
    print(f"Результаты: {RESULTS_DIR / 'latest.json'}")
    print("Остановить: Ctrl+C")
    print()

    if not args.no_browser:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен.")
    finally:
        server.server_close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
