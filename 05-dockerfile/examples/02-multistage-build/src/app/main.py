"""간단한 FastAPI 애플리케이션."""

from fastapi import FastAPI

app = FastAPI(title="멀티스테이지 빌드 예제", version="1.0.0")


@app.get("/")
def root():
    return {"message": "Multistage build image 🏗️", "status": "running"}
