"""SwasthyaSetu Translation Service — Multi-language support."""

from fastapi import FastAPI
from datetime import datetime, timezone

from routers import translate

app = FastAPI(
    title="SwasthyaSetu Translation Service",
    version="1.0.0",
    docs_url="/docs",
)


@app.get("/health")
async def health_check():
    return {
        "service": "translation-service",
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "1.0.0",
        "supportedLanguages": ["hi", "bn", "ta", "te", "mr", "gu", "kn", "or", "en"],
    }


app.include_router(translate.router, prefix="/api/v1/translate", tags=["Translation"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=5002, reload=True)
