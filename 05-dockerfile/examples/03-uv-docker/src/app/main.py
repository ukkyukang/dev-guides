"""FastAPI 애플리케이션 — uv Docker 예제."""

from fastapi import FastAPI

app = FastAPI(title="uv Docker 예제", version="1.0.0")


@app.get("/")
def root():
    return {"message": "Built with uv + Docker! ⚡🐳", "status": "running"}


@app.get("/health")
def health():
    return {"status": "healthy"}
