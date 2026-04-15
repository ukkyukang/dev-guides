"""다중 서비스 API — DB/Redis 연결 데모."""
import os
from fastapi import FastAPI

app = FastAPI(title="Multi-Service API")

@app.get("/")
def root():
    return {
        "status": "running",
        "database": os.environ.get("DATABASE_URL", "not set"),
        "redis": os.environ.get("REDIS_URL", "not set"),
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
