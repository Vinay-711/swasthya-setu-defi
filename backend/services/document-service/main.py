"""SwasthyaSetu Document Service — Upload, store, and manage medical documents."""

from fastapi import FastAPI
from datetime import datetime, timezone

from routers import documents

app = FastAPI(
    title="SwasthyaSetu Document Service",
    version="1.0.0",
    docs_url="/docs",
)


@app.get("/health")
async def health_check():
    return {
        "service": "document-service",
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "1.0.0",
        "storage": "s3-compatible",
    }


app.include_router(documents.router, prefix="/api/v1/documents", tags=["Documents"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=5003, reload=True)
