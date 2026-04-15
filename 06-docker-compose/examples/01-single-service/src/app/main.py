"""단일 서비스 FastAPI 앱."""
import os
from fastapi import FastAPI

app = FastAPI(title=os.environ.get("APP_NAME", "API"))

@app.get("/")
def root():
    return {"service": os.environ.get("APP_NAME", "unknown"), "status": "running"}
