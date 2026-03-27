"""SwasthyaSetu AI/ML Service — Voice, Risk Prediction, OCR."""

from fastapi import FastAPI
from datetime import datetime, timezone

from routers import voice, risk, ocr

app = FastAPI(
    title="SwasthyaSetu AI/ML Service",
    version="1.0.0",
    docs_url="/docs",
)


@app.get("/health")
async def health_check():
    return {
        "service": "ai-ml-service",
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "1.0.0",
        "models_loaded": ["whisper-base", "xgboost-risk", "layoutlmv3"],
    }


app.include_router(voice.router, prefix="/api/v1/ai/voice", tags=["Voice"])
app.include_router(risk.router, prefix="/api/v1/ai/risk", tags=["Risk Prediction"])
app.include_router(ocr.router, prefix="/api/v1/ai/ocr", tags=["OCR"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)
