import asyncio
import json
import logging
import sys
import time
import uuid
from collections.abc import AsyncIterator
from contextvars import ContextVar
from datetime import datetime, timezone

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.responses import Response
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Gauge,
    Histogram,
    generate_latest,
)

request_id_var: ContextVar[str] = ContextVar("request_id", default="-")


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "time": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname.lower(),
            "logger": record.name,
            "service": "backend",
            "message": record.getMessage(),
            "request_id": request_id_var.get(),
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JsonFormatter())
logging.basicConfig(level=logging.INFO, handlers=[handler], force=True)
logger = logging.getLogger(__name__)

APP_NAME = "fastapi"

REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Общее количество HTTP запросов",
    ["app_name", "method", "path", "status_code"],
)

REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "Длительность обработки HTTP запроса в секундах",
    ["app_name", "method", "path"],
)

REQUESTS_IN_PROGRESS = Gauge(
    "http_requests_in_progress",
    "Количество HTTP запросов, обрабатываемых в данный момент",
    ["app_name", "method", "path"],
)


async def track_in_progress(request: Request) -> AsyncIterator[None]:
    """Считает запросы, которые обрабатываются прямо сейчас."""
    if request.url.path == "/metrics":
        yield
        return

    route = request.scope.get("route")
    path = getattr(route, "path", None) or request.url.path
    gauge = REQUESTS_IN_PROGRESS.labels(
        app_name=APP_NAME, method=request.method, path=path
    )
    gauge.inc()
    try:
        yield
    finally:
        gauge.dec()


app = FastAPI(
    title="Тестовый Бэкенд",
    description="Пример OpenAPI документации",
    version="0.0.1",
    docs_url="/docs",
    redoc_url=None,
    dependencies=[Depends(track_in_progress)],
)


@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    if request.url.path == "/metrics":
        return await call_next(request)

    method = request.method
    raw_path = request.url.path
    start = time.perf_counter()
    status_code = 500
    path = raw_path

    request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
    token = request_id_var.set(request_id)

    try:
        response = await call_next(request)
        status_code = response.status_code
        route = request.scope.get("route")
        path = getattr(route, "path", None) or raw_path
        response.headers["x-request-id"] = request_id
        return response
    finally:
        duration = time.perf_counter() - start
        logger.info(
            "request finished method=%s path=%s status=%s duration_ms=%.2f",
            method,
            path,
            status_code,
            duration * 1000,
        )
        REQUESTS_TOTAL.labels(
            app_name=APP_NAME,
            method=method,
            path=path,
            status_code=str(status_code),
        ).inc()
        REQUEST_DURATION.labels(
            app_name=APP_NAME,
            method=method,
            path=path,
        ).observe(duration)
        request_id_var.reset(token)


@app.get("/")
async def root() -> str:
    return "root"


@app.get("/status/{status_code}")
async def return_status(
    status_code: int,
    seconds_sleep: int | None = Query(default=None),
) -> dict:
    logger.info(
        "Hello from FastAPI! status_code=%s, seconds_sleep=%s",
        status_code,
        seconds_sleep,
    )
    if seconds_sleep:
        await asyncio.sleep(seconds_sleep)
    if status_code and status_code != 200:
        logger.error("Shit happens")
        raise HTTPException(status_code=status_code, detail="an error occurred")
    return {"data": "Hello"}


@app.get("/metrics", include_in_schema=False)
async def metrics() -> Response:
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
