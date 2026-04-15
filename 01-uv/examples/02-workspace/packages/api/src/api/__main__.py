"""api 패키지를 `python -m api`로 실행할 수 있도록 합니다."""

import uvicorn

from api.server import app

if __name__ == "__main__":
    print("🚀 API 서버를 시작합니다...")
    print("📖 API 문서: http://127.0.0.1:8000/docs")
    uvicorn.run(app, host="127.0.0.1", port=8000)
