"""개발/프로덕션 설정 분리 데모 앱."""
import os
from fastapi import FastAPI

debug = os.environ.get("DEBUG", "false").lower() == "true"
app = FastAPI(title="Dev Override Demo", debug=debug)

@app.get("/")
def root():
    return {
        "mode": "development" if debug else "production",
        "debug": debug,
    }
