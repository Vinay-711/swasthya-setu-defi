import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.deps import mock_mode_param
from app.core.logging import configure_logging
from app.routes.router_registry import api_router
from app.services.mock_responses import build_mock_response, is_mock_mode
from database.init_db import init_db

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    configure_logging()
    try:
        await init_db()
        logger.info("Database initialized")
    except Exception as exc:
        if settings.allow_start_without_db:
            logger.warning("Database unavailable, starting in degraded demo mode: %s", exc)
        else:
            raise
    yield


app = FastAPI(
    title="SwasthyaSetu API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
    dependencies=[Depends(mock_mode_param)],
)

app.add_middleware(
    # pyre-ignore[6]
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def mock_mode_middleware(request: Request, call_next):
    is_api_request = request.url.path.startswith(settings.api_prefix)

    if is_api_request and is_mock_mode(request):
        return await build_mock_response(request)

    try:
        return await call_next(request)
    except Exception:
        # Demo-safe fallback guard: if a request explicitly asks for mock mode,
        # always return a stable fake payload instead of an exception.
        if is_api_request and is_mock_mode(request):
            return await build_mock_response(request)
        raise


@app.exception_handler(Exception)
async def unhandled_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled exception", exc_info=exc)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


app.include_router(api_router, prefix=settings.api_prefix)
