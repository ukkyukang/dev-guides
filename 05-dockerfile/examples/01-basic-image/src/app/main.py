"""간단한 FastAPI 애플리케이션."""

from fastapi import FastAPI

app = FastAPI(title="Docker 예제 API", version="1.0.0")


@app.get("/")
def root():
    return {"message": "Hello from Docker! 🐳", "status": "running"}


@app.get("/health")
def health():
    return {"status": "healthy"}
